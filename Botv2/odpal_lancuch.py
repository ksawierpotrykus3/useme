# -*- coding: utf-8 -*-
"""Odpala CALY lancuch V2 surowo i zrzuca kazdy etap jako plik do ofertowarki.

Lancuch:
  1_analiza.md      -> surowy dziennik myslenia (iteracja 1)
  2_research.md     -> surowy research (jesli byl potrzebny)
  3_weryfikacja.md  -> surowy dziennik po weryfikacji (iteracja 2)
  4_wycena.md       -> surowy zapis rady 4x DeepSeek + rozjemca (NIC NIE UCIETE)
  5_pismo.md        -> surowa oferta (przed sanitizerem)
  6_koncowa.md      -> oferta po sanitizerze + werdykt checkera i sedziego
  wynik.json        -> wszystko strukturalnie

Foldery:
  badania/baza/ksawierpotrykus3/01_ofertowarka/<job_id>/

Uzycie:
    python odpal_lancuch.py 2897327
    python odpal_lancuch.py 2897327 2538404
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).parent                      # .../useme_core/Botv2
CORE = BASE.parent                                 # .../useme_core
KOD_DIR = CORE / "kod"
sys.path.insert(0, str(KOD_DIR))
sys.path.insert(0, str(BASE / "mozg"))

import brain  # noqa: E402
from wycena_rada import wycen_rada  # noqa: E402
from sanitizer import sanitize_opis  # noqa: E402
from checker import sprawdz  # noqa: E402

BAZA = CORE / "badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json"
OFERTOWARKA = CORE / "badania/baza/ksawierpotrykus3/01_ofertowarka"


def _clean(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _dopasuj(z: dict) -> dict:
    return {
        "id": str(z.get("offer_id") or "?"),
        "title": z.get("title") or "",
        "full_description": _clean(z.get("job_description")),
        "budget": z.get("budget") or "",
    }


def uruchom(zlecenie: dict) -> dict:
    job_id = str(zlecenie.get("id", "?"))
    out = OFERTOWARKA / job_id
    out.mkdir(parents=True, exist_ok=True)

    tresc = brain._tresc_zlecenia(zlecenie)
    client_text = brain._tekst_klienta(zlecenie)
    sys_myslenie = brain._czytaj("myslenie.md")
    sys_pismo = brain._czytaj("pismo.md")
    sys_sedzia = brain._czytaj("sedzia.md")

    log: list[str] = []

    def say(msg):
        log.append(msg)
        print(msg, flush=True)

    # ---------- 1. ANALIZA ----------
    say(f"[1/6] Analiza #{job_id}...")
    dziennik_iter1 = brain.call_ai(
        sys_myslenie,
        f"OTO ZLECENIE:\n\n{tresc}\n\nZrob dziennik myslenia wg formatu.",
        temperature=0.4,
    )
    if not dziennik_iter1:
        say("    STOP: brak odpowiedzi AI w iteracji 1")
        (out / "1_analiza.md").write_text("BRAK ODPOWIEDZI AI", encoding="utf-8")
        return {"ok": False, "blad": "brak odpowiedzi AI w iteracji 1"}
    (out / "1_analiza.md").write_text(dziennik_iter1, encoding="utf-8")
    pola = brain._parsuj_dziennik(dziennik_iter1)
    say(f"    kwalifikowalnosc={pola.get('KWALIFIKOWALNOSC', '?')[:60]}")

    # ---------- 2. RESEARCH (warunkowy) ----------
    research = ""
    if "TAK" in (pola.get("RESEARCH_POTRZEBNY") or "").upper():
        say(f"[2/6] Research #{job_id} ON...")
        research = brain.call_ai(
            "Jestes agentem researchu. Odpowiadaj zwiezle, tylko fakty ze zrodlem "
            "(URL/cytat). Czego nie potwierdzisz, oznacz jako niepotwierdzone. Nie zmyslaj. "
            "Interesuje nas GDZIE i DLACZEGO grozne, nie JAK naprawic (diagnoza, nie recepta).",
            f"Zlecenie:\n{tresc}\n\nDziennik:\n{dziennik_iter1}\n\n"
            f"Zbadaj TYLKO to, co dziennik wskazal jako potrzebne. Max 2-3 miny.",
            model=brain.RESEARCH_MODEL, timeout=180,
        ) or "BRAK_ISTOTNYCH_FAKTOW"
    else:
        say(f"[2/6] Research #{job_id} OFF")
        research = "RESEARCH_NIE_BYL_POTRZEBNY"
    (out / "2_research.md").write_text(research, encoding="utf-8")

    # ---------- 3. WERYFIKACJA ----------
    say(f"[3/6] Weryfikacja #{job_id}...")
    dziennik = dziennik_iter1
    weryfikacja = brain.call_ai(
        sys_myslenie,
        f"OTO ZLECENIE:\n{tresc}\n\nTWOJ DZIENNIK Z ITERACJI 1:\n{dziennik_iter1}\n\n"
        f"WYNIK RESEARCHU (moze byc BRAK_ISTOTNYCH_FAKTOW):\n{research or 'BRAK'}\n\n"
        "Spojrz na wlasne myslenie krytycznie: gdzie zgadujesz? ktora mina nie ma dowodu? "
        "czy research cos realnie zmienia? czy pytania sa naprawde konieczne? gdzie jestes "
        "za granica ciecia, a gdzie przed? Popraw dziennik. Zwroc POPRAWIONY dziennik w tym "
        "samym formacie, na koncu dopisz linie DECYZJE: co DOPISAC / ODPOWIEDZIEC / DOPYTAC.",
        temperature=0.4,
    )
    if weryfikacja:
        dziennik = weryfikacja
        pola = brain._parsuj_dziennik(dziennik)
    (out / "3_weryfikacja.md").write_text(dziennik, encoding="utf-8")

    # ---------- 4. WYCENA (rada 4x DeepSeek + rozjemca) ----------
    say(f"[4/6] Wycena #{job_id}...")
    wynik_wyceny = wycen_rada(
        tresc_zlecenia=tresc,
        dziennik=dziennik,
        research=research,
        call_ai_fn=brain.call_ai,
        say=say,
    )
    kwota_dolna = int(wynik_wyceny["kwota_dolna"])
    kwota_gorna = int(wynik_wyceny["kwota_gorna"])
    kwota = int(wynik_wyceny["kwota"])
    dni_od = int(wynik_wyceny.get("dni_od", 14))
    dni_do = int(wynik_wyceny.get("dni_do", 21))
    (out / "4_wycena.md").write_text(wynik_wyceny.get("surowy_tekst", ""), encoding="utf-8")

    # ---------- 5. PISMO ----------
    say(f"[5/6] Pismo #{job_id}...")
    surowy_tekst_wyceny = wynik_wyceny.get("surowy_tekst") or "(brak)"
    oferta_raw = brain.call_ai(
        sys_pismo,
        f"OTO ZLECENIE:\n{tresc}\n\n"
        f"=== ANALIZA (pierwsze czytanie zlecenia, iteracja 1) ===\n{dziennik_iter1}\n\n"
        f"=== WERYFIKACJA (dojrzaly dziennik po researchu, iteracja 2) ===\n{dziennik}\n\n"
        f"=== RESEARCH (dowody, jesli byly) ===\n{research or 'BRAK'}\n\n"
        f"=== SUROWY ZAPIS WYCENY (glosy 4 modeli + rozjemca, NIC NIE UCIETE) ===\n{surowy_tekst_wyceny}\n\n"
        f"DECYZJA NALEZY DO CIEBIE. Masz przed soba cale surowe rozumowanie czterech modeli "
        f"i werdykt rozjemcy. Zdecyduj sam, jak zbudowac oferte zgodnie z pismo.md. "
        f"Jesli wycena jest definitywna, podaj jedna kwote. Jesli sa widelki, podaj przedzial "
        f"od {kwota_dolna} do {kwota_gorna} zł i powiedz, od czego zaleza. "
        f"Nigdy nie schodz ponizej {kwota_dolna} zł. Czas podaj jako zakres lub przyblizeniem slowym. "
        f"Podpis na koncu: {brain.PODPIS}\n\n"
        "Napisz oferte. Wynik ma wynikac z surowego rozumowania wyceny. Wyslij tylko tekst oferty.",
        temperature=0.8,
    ) or ""
    (out / "5_pismo.md").write_text(oferta_raw, encoding="utf-8")
    if not oferta_raw:
        say("    STOP: brak odpowiedzi AI w iteracji pisma")
        return {"ok": False, "blad": "brak odpowiedzi AI w pismie"}

    oferta = re.sub(r"\[WYCENA\].*?(?:\[/WYCENA\]|\Z)", "", oferta_raw,
                    flags=re.DOTALL | re.IGNORECASE).strip()
    oferta = sanitize_opis(oferta, wycena=kwota, dni=dni_do)

    # ---------- 6. CHECKER + SEDZIA ----------
    say(f"[6/6] Checker + Sedzia #{job_id}...")
    sciezka = "biznes" if "biznes" in (pola.get("SCIEZKA_MERYTORYKI", "") or "").lower() else "inzynieria"
    check = sprawdz(oferta, dni=dni_do, sciezka=sciezka, client_text=client_text)

    sedzia = {"status": "OK", "kara_pkt": 0}
    if sys_sedzia:
        sedzia_raw = brain.call_ai(
            sys_sedzia,
            f"--- OGLOSZENIE KLIENTA ---\n{tresc}\n\n"
            f"--- WYCENA: {kwota} zl netto / {dni_od}-{dni_do} dni ---\n\n"
            f"--- OFERTA DO OCENY ---\n{oferta}",
            model="deepseek-v4-pro-nothink", timeout=120, temperature=0.3,
        )
        sedzia = brain._wyciagnij_json_blok(sedzia_raw or "", "COMMON_SENSE_JSON") or {"status": "OK", "kara_pkt": 0}
        (out / "6_sedzia_raw.md").write_text(sedzia_raw or "", encoding="utf-8")

    koncowa = (
        f"# OFERTA KONCOWA #{job_id}\n\n"
        f"WYCENA: {kwota_dolna}-{kwota_gorna} zl netto | {dni_od}-{dni_do} dni\n"
        f"CHECKER: {'OK' if check['ok'] else [p['regula'] for p in check['problemy']]}\n"
        f"SEDZIA: {sedzia.get('status')} (kara {sedzia.get('kara_pkt')} pkt)\n\n"
        f"---\n\n{oferta}\n"
    )
    (out / "6_koncowa.md").write_text(koncowa, encoding="utf-8")

    wynik = {
        "ok": True,
        "job_id": job_id,
        "title": zlecenie.get("title", ""),
        "wycena": kwota,
        "wycena_dolna": kwota_dolna,
        "wycena_gorna": kwota_gorna,
        "dni_od": dni_od,
        "dni_do": dni_do,
        "pola": pola,
        "checker": check,
        "sedzia": sedzia,
        "log": log,
    }
    (out / "wynik.json").write_text(json.dumps(wynik, ensure_ascii=False, indent=2), encoding="utf-8")
    say(f"    -> ZAPIS: {out}")
    return wynik


def main():
    ids = [a for a in sys.argv[1:] if len(a) >= 5]
    if not ids:
        print("Uzycie: python odpal_lancuch.py <job_id> [job_id2 ...]")
        return

    dane = json.loads(BAZA.read_text(encoding="utf-8"))
    rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
    mapa = {str(r.get("offer_id")): r for r in rek}

    wyniki = []
    for jid in ids:
        surowy = mapa.get(jid)
        if not surowy:
            print(f"[BRAK] #{jid} nie ma w bazie przegranych")
            continue
        zl = _dopasuj(surowy)
        print("\n" + "=" * 78, flush=True)
        print(f"ZLECENIE #{jid} | {zl['title'][:60]}", flush=True)
        print("=" * 78, flush=True)
        try:
            w = uruchom(zl)
        except Exception as e:
            print(f"[BLAD] #{jid}: {e}", flush=True)
            continue
        wyniki.append(w)

    print("\n" + "=" * 78, flush=True)
    print(f"GOTOWE. Wyniki w: {OFERTOWARKA}", flush=True)
    for w in wyniki:
        if w.get("ok"):
            print(f"  #{w['job_id']}: {w['wycena_dolna']}-{w['wycena_gorna']} zl "
                  f"| checker {'OK' if w['checker']['ok'] else 'PROBLEMY'} "
                  f"| sedzia {w['sedzia'].get('status')}", flush=True)
        else:
            print(f"  #{w.get('job_id')}: STOP - {w.get('blad')}", flush=True)


if __name__ == "__main__":
    main()