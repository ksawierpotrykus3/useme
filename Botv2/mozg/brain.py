# -*- coding: utf-8 -*-
"""MOZG V2 - jedno myslenie w iteracjach, nie pipeline slotow.

V1: 4 sloty, kazdy gluchy na siebie (research -> wycena -> tekst -> walidacja).
V2: jeden umysl. Najpierw mysli (dziennik), potem weryfikuje, wycenia, na koncu pisze.
Wycena liczona deterministycznie (kalkulator) - LLM zwraca tylko strukture.
Checkpoint = dziennik myslenia zapisany na dysk (widac JAK i DLACZEGO).

Mechanika (proxy DeepSeek) - kopiowana z V1.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from wycena_debata import wycen_przez_debate
from sanitizer import sanitize_opis
from checker import sprawdz

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
DZIENNIKI_DIR = BASE_DIR / "dzienniki"
DZIENNIKI_DIR.mkdir(parents=True, exist_ok=True)

DEEPSEEK_API_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-v4-pro"
RESEARCH_MODEL = "deepseek-v4-pro-search"

# Staly podpis (imie) - Useme, konto wykonawcy
PODPIS = "Ksawier"


def call_ai(system_prompt: str, user_prompt: str, model: str = MODEL,
            timeout: int = 300, temperature: float = 0.7,
            max_tokens: int = 4000) -> Optional[str]:
    """Wywolanie modelu przez lokalne proxy (to samo co V1). Zwraca tekst lub None."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    session = requests.Session()
    try:
        resp = session.post(DEEPSEEK_API_URL, json=payload,
                            headers={"Content-Type": "application/json"},
                            timeout=(10, timeout), stream=True)
        if resp.status_code != 200:
            print(f"[AI] http {resp.status_code}", flush=True)
            return None
        full = ""
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            line = line.strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                if delta:
                    full += delta
            except json.JSONDecodeError:
                pass
        return full or None
    except requests.exceptions.RequestException as e:
        print(f"[AI] blad sieci: {e}", flush=True)
        return None
    finally:
        session.close()


GEMINI_API_URL = "http://127.0.0.1:8045/v1/chat/completions"
GEMINI_MODEL = "gemini-3.8-flash"


def call_gemini(system_prompt: str, user_prompt: str, model: str = GEMINI_MODEL,
                timeout: int = 90, temperature: float = 0.3,
                max_tokens: int = 1000) -> Optional[str]:
    """Wywolanie Gemini przez lokalne proxy na porcie 8045. W razie niedostępności zwraca None."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        resp = requests.post(GEMINI_API_URL, json=payload, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip() or None
    except Exception as e:
        print(f"[Gemini Proxy Błąd]: {e}", flush=True)
    return None


def _czytaj(name: str) -> str:
    p = PROMPTS_DIR / name
    return p.read_text(encoding="utf-8-sig") if p.exists() else ""


def _tresc_zlecenia(zlecenie: Dict[str, Any]) -> str:
    fd = zlecenie.get("full_details") or {}
    ld = zlecenie.get("list_details") or {}
    title = zlecenie.get("title") or fd.get("title") or ld.get("title") or ""
    desc = (
        zlecenie.get("full_description")
        or fd.get("full_description")
        or zlecenie.get("description")
        or zlecenie.get("short_desc")
        or ld.get("short_desc")
        or ""
    )
    budget = zlecenie.get("budget") or ld.get("budget") or ""
    return (
        f"TYTUL: {title}\n"
        f"BUDZET (jesli podany): {budget}\n"
        f"TRESC OGLOSZENIA:\n{desc}"
    )


def _tekst_klienta(zlecenie: Dict[str, Any]) -> str:
    fd = zlecenie.get("full_details") or {}
    ld = zlecenie.get("list_details") or {}
    return (
        str(zlecenie.get("title") or fd.get("title") or ld.get("title") or "") + " " +
        str(zlecenie.get("full_description") or fd.get("full_description") or
            zlecenie.get("description") or zlecenie.get("short_desc") or ld.get("short_desc") or "")
    ).lower()


def _parsuj_dziennik(tekst: str) -> Dict[str, str]:
    pola = {}
    if not tekst:
        return pola
    klucze = [
        "KWALIFIKOWALNOSC", "TYP_ZLECENIA", "INTENCJA", "DECYDENT_I_BOL",
        "WYKONALNE", "POLE_DO_POPISU", "SCIEZKA_MERYTORYKI", "MINY_I_CIEKAWOSTKI",
        "PYTANIA", "CO_ZLECENIE_MOWI", "CZEGO_NIE_MOWI", "GRANICA_CIECIA",
        "RESEARCH_POTRZEBNY",
    ]
    for k in klucze:
        m = re.search(rf"{k}\s*:\s*(.+?)(?=\n[A-Z_ĄĆĘŁŃÓŚŹŻ]+\s*:|\Z)", tekst, re.DOTALL)
        if m:
            pola[k] = m.group(1).strip()
    return pola


def _wyciagnij_json_blok(tekst: str, tag: str) -> Optional[Dict[str, Any]]:
    m = re.search(rf"\[{tag}\](.*?)(?:\[/{tag}\]|\Z)", tekst or "", re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        mm = re.search(r"\{.*\}", raw, re.DOTALL)
        if mm:
            try:
                return json.loads(mm.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _wyciagnij_blok(tekst: str, tag: str) -> str:
    m = re.search(rf"\[{tag}\](.*?)(?:\[/{tag}\]|\Z)", tekst or "", re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


# Wycena realizowana jest przez moduł wycena_debata.py (Adversarial Debate Useme)


def zbuduj_oferte(zlecenie: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
    """Glowna petla V2. Zwraca pelny wynik z dziennikiem, oferta, wycena, checkerem."""
    job_id = str(zlecenie.get("id", "?"))
    tresc = _tresc_zlecenia(zlecenie)
    client_text = _tekst_klienta(zlecenie)
    system_myslenie = _czytaj("myslenie.md")
    system_pismo = _czytaj("pismo.md")
    system_sedzia = _czytaj("sedzia.md")
    log: list[str] = []

    def say(msg):
        log.append(msg)
        if verbose:
            print(msg, flush=True)

    # ---------- ITERACJA 1: ANALIZA ----------
    say(f"[1/6] Analiza #{job_id}...")
    dziennik = call_ai(
        system_myslenie,
        f"OTO ZLECENIE:\n\n{tresc}\n\nZrob dziennik myslenia wg formatu.",
        temperature=0.4,
    )
    if not dziennik:
        return {"ok": False, "blad": "brak odpowiedzi AI w iteracji 1", "log": log}
    dziennik_iter1 = dziennik  # zachowujemy surowe, pierwsze czytanie zlecenia
    pola = _parsuj_dziennik(dziennik)
    say(f"    kwalifikowalnosc={pola.get('KWALIFIKOWALNOSC', '?')[:60]}")

    if "NIE" in (pola.get("KWALIFIKOWALNOSC") or "").upper()[:20]:
        say("    -> ODRZUCONE (kwalifikowalnosc NIE)")
        return {"ok": False, "blad": "odrzucone na kwalifikowalnosci", "dziennik": dziennik,
                "pola": pola, "log": log}

    # ---------- ITERACJA 2: WERYFIKACJA + RESEARCH ----------
    say(f"[2/6] Weryfikacja #{job_id}...")
    research = ""
    if "TAK" in (pola.get("RESEARCH_POTRZEBNY") or "").upper():
        say("    research ON")
        research = call_ai(
            "Jestes agentem researchu. Odpowiadaj zwiezle, tylko fakty ze zrodlem "
            "(URL/cytat). Czego nie potwierdzisz, oznacz jako niepotwierdzone. Nie zmyslaj. "
            "Interesuje nas GDZIE i DLACZEGO grozne, nie JAK naprawic (diagnoza, nie recepta).",
            f"Zlecenie:\n{tresc}\n\nDziennik:\n{dziennik}\n\n"
            f"Zbadaj TYLKO to, co dziennik wskazal jako potrzebne. Max 2-3 miny.",
            model=RESEARCH_MODEL, timeout=180,
        ) or "BRAK_ISTOTNYCH_FAKTOW"
    else:
        say("    research OFF")

    weryfikacja = call_ai(
        system_myslenie,
        f"OTO ZLECENIE:\n{tresc}\n\nTWOJ DZIENNIK Z ITERACJI 1:\n{dziennik}\n\n"
        f"WYNIK RESEARCHU (moze byc BRAK_ISTOTNYCH_FAKTOW):\n{research or 'BRAK'}\n\n"
        "Spojrz na wlasne myslenie krytycznie: gdzie zgadujesz? ktora mina nie ma dowodu? "
        "czy research cos realnie zmienia? czy pytania sa naprawde konieczne? gdzie jestes "
        "za granica ciecia, a gdzie przed? Popraw dziennik. Zwroc POPRAWIONY dziennik w tym "
        "samym formacie, na koncu dopisz linie DECYZJE: co DOPISAC / ODPOWIEDZIEC / DOPYTAC.",
        temperature=0.4,
    )
    if weryfikacja:
        dziennik = weryfikacja
        pola = _parsuj_dziennik(dziennik)

    # ---------- WYCENA (debata dwumodelowa Useme: DeepSeek vs Gemini) ----------
    say(f"[3/6] Wycena #{job_id}...")
    try:
        wynik_wyceny = wycen_przez_debate(
            tresc_zlecenia=tresc,
            dziennik=dziennik,
            research=research,
            call_wyceniacz_fn=call_ai,      # DeepSeek-v4-Pro (port 4571)
            call_reviewer_fn=call_gemini,   # Gemini-3.8-Flash (port 8045)
            say=say,
            max_rundy=2,
        )
        kwota = int(wynik_wyceny["kwota"])
        dni_od = int(wynik_wyceny.get("dni_od", wynik_wyceny["dni"]))
        dni_do = int(wynik_wyceny.get("dni_do", wynik_wyceny["dni"]))
        say(f"    wycena debata: {kwota} zl / {dni_od}-{dni_do} dni ({wynik_wyceny.get('typ', 'projekt')})")
    except Exception as e:
        say(f"    debata blad: {e} - fallback 3000/14-21")
        kwota, dni_od, dni_do, wynik_wyceny = 3000, 14, 21, {"rozbicie": {"blad": str(e)}}

    # ---------- ITERACJA 3: PISMO ----------
    # Pismo dostaje CALY PRZEBIEG (analiza iter1 + weryfikacja + research + wszystkie
    # rundy debaty wycenowej), nie wyciag. Sam decyduje, jak zbudowac oferte wg pismo.md.
    say(f"[4/6] Pismo #{job_id}...")

    przebieg = wynik_wyceny.get("przebieg") or []
    linie_przebiegu = []
    for krok in przebieg:
        aktor = krok.get("aktor", "?")
        if aktor == "REVIEWER":
            linie_przebiegu.append(
                f"  [runda {krok.get('runda')}] REVIEWER (rynek): {krok.get('werdykt')} | "
                f"sugeruje {krok.get('kwota_sugerowana')} zł | jego widelki rynku: {krok.get('rynek')}\n"
                f"      krytyka: {krok.get('uzasadnienie')}"
            )
        else:
            linie_przebiegu.append(
                f"  [runda {krok.get('runda')}] {aktor}: {krok.get('kwota')} zł / "
                f"{krok.get('dni_od')}-{krok.get('dni_do')} dni\n"
                f"      uzasadnienie: {krok.get('uzasadnienie')}"
            )
    przebieg_txt = "\n".join(linie_przebiegu) or "  (brak rund)"

    oferta_raw = call_ai(
        system_pismo,
        f"OTO ZLECENIE:\n{tresc}\n\n"
        f"=== ANALIZA (pierwsze czytanie zlecenia, iteracja 1) ===\n{dziennik_iter1}\n\n"
        f"=== WERYFIKACJA (dojrzaly dziennik po researchu, iteracja 2) ===\n{dziennik}\n\n"
        f"=== RESEARCH (dowody, jesli byly) ===\n{research or 'BRAK'}\n\n"
        f"=== PRZEBIEG DEBATY WYCENOWEJ (wyceniacz inzynierski vs recenzent rynkowy, wszystkie rundy) ===\n{przebieg_txt}\n\n"
        f"=== WYNIK KONCOWY DEBATY ===\n"
        f"Kwota: {kwota} zł netto | Czas: od {dni_od} do {dni_do} dni | Typ: {wynik_wyceny.get('typ', 'projekt')}\n\n"
        f"DECYZJA NALEZY DO CIEBIE. Masz przed soba caly przebieg rozumowania i wszystkie glosy. "
        f"Zdecyduj sam, jak zbudowac oferte zgodnie z pismo.md. "
        f"Jesli zakres zlecenia jest niejasny, mozesz podac widelki zamiast jednej liczby (pismo.md, sekcja Cena). "
        f"Jesli jest klarowny, podaj jedna kwote {kwota} zł. Czas podaj jako zakres lub przyblizeniem slowym. "
        f"Podpis na koncu: {PODPIS}\n\n"
        "Napisz oferte. Wynik ma wynikac z calego przebiegu. Wyslij tylko tekst oferty.",
        temperature=0.8,
    )
    if not oferta_raw:
        return {"ok": False, "blad": "brak odpowiedzi AI w iteracji 3", "log": log}

    # Usuń ewentualny blok [WYCENA] jeśli model go dokleil
    oferta = re.sub(r"\[WYCENA\].*?(?:\[/WYCENA\]|\Z)", "", oferta_raw, flags=re.DOTALL | re.IGNORECASE).strip()

    # ---------- SANITIZER ----------
    oferta = sanitize_opis(oferta, wycena=kwota, dni=dni_do)

    # ---------- CHECKER ----------
    say(f"[5/6] Checker #{job_id}...")
    sciezka = "biznes" if "biznes" in (pola.get("SCIEZKA_MERYTORYKI", "") or "").lower() else "inzynieria"
    check = sprawdz(oferta, dni=dni_do, sciezka=sciezka, client_text=client_text)
    if not check["ok"]:
        say(f"    checker: {[p['regula'] for p in check['problemy']]}")

    # ---------- SĘDZIA ----------
    sedzia = {"status": "OK", "kara_pkt": 0}
    if system_sedzia:
        say(f"[6/6] Sedzia #{job_id}...")
        sedzia_raw = call_ai(
            system_sedzia,
            f"--- OGLOSZENIE KLIENTA ---\n{tresc}\n\n"
            f"--- WYCENA: {kwota} zl netto / {dni_od}-{dni_do} dni ---\n\n"
            f"--- OFERTA DO OCENY ---\n{oferta}",
            model="deepseek-v4-pro-nothink", timeout=120, temperature=0.3,
        )
        sedzia = _wyciagnij_json_blok(sedzia_raw or "", "COMMON_SENSE_JSON") or {"status": "OK", "kara_pkt": 0}
        if str(sedzia.get("status", "")).upper() == "VETO":
            say(f"    sedzia VETO: {sedzia.get('uzasadnienie', '')[:80]}")

    wynik = {
        "ok": True,
        "job_id": job_id,
        "dziennik": dziennik,
        "pola": pola,
        "oferta": oferta,
        "wycena": kwota,
        "dni": dni_do, "dni_od": dni_od, "dni_do": dni_do,
        "wycena_rozbicie": wynik_wyceny.get("rozbicie", {}),
        "checker": check,
        "sedzia": sedzia,
        "research": research,
        "log": log,
    }

    (DZIENNIKI_DIR / f"{job_id}.json").write_text(
        json.dumps(wynik, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return wynik
