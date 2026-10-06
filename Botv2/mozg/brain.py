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
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from wycena_rada import wycen_rada
from sanitizer import sanitize_opis
from checker import sprawdz

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
DZIENNIKI_DIR = BASE_DIR / "dzienniki"
DZIENNIKI_DIR.mkdir(parents=True, exist_ok=True)

# Artefakty produkcyjne (analiza/research/wycena/oferta) trafiaja do ofertowarki.
CORE_DIR = BASE_DIR.parent.parent                       # .../useme_core
OFERTOWARKA_DIR = CORE_DIR / "badania/baza/ksawierpotrykus3/01_ofertowarka"

# Pelne logi calego lancucha per zlecenie (wszystko, zawsze, posegregowane).
LOGI_DIR = BASE_DIR.parent / "logi"                     # .../Botv2/logi

DEEPSEEK_API_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-v4-pro"
RESEARCH_MODEL = "deepseek-v4-pro-search"

# Staly podpis (imie) - Useme, konto wykonawcy
PODPIS = "Ksawier"


def _call_ai_once(system_prompt: str, user_prompt: str, model: str,
                  timeout: int, temperature: float, max_tokens: int) -> Optional[str]:
    """Pojedyncze wywolanie modelu przez lokalne proxy. Zwraca tekst lub None."""
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


def call_ai(system_prompt: str, user_prompt: str, model: str = MODEL,
            timeout: int = 300, temperature: float = 0.7,
            max_tokens: int = 4000, proby: int = 3) -> Optional[str]:
    """Wywolanie modelu z automatycznym retry (odpornosc na chwilowe bledy proxy).

    Proboje do `proby` razy. Miedzy probami krotka pauza. Zwraca tekst lub None
    po wyczerpaniu prob. Puste/None odpowiedzi tez sa ponawiane.
    """
    for i in range(1, proby + 1):
        wynik = _call_ai_once(system_prompt, user_prompt, model, timeout, temperature, max_tokens)
        if wynik:
            return wynik
        if i < proby:
            print(f"[AI] pusta odpowiedz, retry {i}/{proby - 1}...", flush=True)
            time.sleep(2.0)
    return None


GEMINI_API_URL = "http://127.0.0.1:8045/v1/chat/completions"
GEMINI_MODEL = "gemini-3.8-flash-thinking"


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


def _ocen_u_sedziego(system_sedzia: str, tresc: str, oferta: str,
                     kwota: int, dni_od: int, dni_do: int) -> Dict[str, Any]:
    """Ocenia oferte sedzia zdrowego rozsadku. Zwraca dict (status/kara/uzasadnienie/...)."""
    raw = call_ai(
        system_sedzia,
        f"--- OGLOSZENIE KLIENTA ---\n{tresc}\n\n"
        f"--- WYCENA: {kwota} zl netto / {dni_od}-{dni_do} dni ---\n\n"
        f"--- OFERTA DO OCENY ---\n{oferta}",
        model="deepseek-v4-pro-nothink", timeout=120, temperature=0.3,
    )
    return _wyciagnij_json_blok(raw or "", "COMMON_SENSE_JSON") or {"status": "OK", "kara_pkt": 0}


def _weryfikuj_veto(sedzia: Dict[str, Any], oferta: str, tresc: str) -> str:
    """Researcher weryfikuje zakwestionowane przez sedziego twierdzenia.

    Zwraca surowy tekst: dla kazdego twierdzenia PRAWDA/FALSZ/NIEPOTWIERDZONE + dowod.
    """
    cytat = sedzia.get("cytat_lub_brak", "")
    uzas = sedzia.get("uzasadnienie", "")
    instrukcja = sedzia.get("instrukcja_naprawy", "")
    raw = call_ai(
        "Jestes researcherem-weryfikatorem. Dostajesz zakwestionowane twierdzenia z oferty. "
        "Sprawdz KAZDE z osobna: czy to prawda, czy falsz, czy nie da sie potwierdzic. "
        "Podaj dowod (URL, cytat, dokumentacja). Czego nie potwierdzisz, oznaczone jako "
        "NIEPOTWIERDZONE. Nie zmyslaj. Zwroc zwiezle: dla kazdego twierdzenia werdykt + dowod.",
        f"ZLECENIE:\n{tresc}\n\nOFERTA:\n{oferta}\n\n"
        f"ZAKWESTIONOWANE PRZEZ SEDZIEGO:\n{uzas}\n\n"
        f"CYTAT Z OFERTY: {cytat}\n\nINSTRUKCJA NAPRAWY: {instrukcja}",
        model=RESEARCH_MODEL, timeout=180,
    )
    return raw or "BRAK_WYNIKU_WERYFIKACJI"


def _przepisz_z_faktami(oferta: str, sedzia: Dict[str, Any], fakty: str, tresc: str,
                        system_pismo: str, kwota_dolna: int, kwota_gorna: int,
                        definitywna: bool) -> str:
    """Pismo przepisuje oferte po VETO: usuwa zakwestionowane twierdzenia / zamienia na pytania."""
    if definitywna:
        wytyczna = f"podaj jedna kwote {kwota_dolna} zl netto"
    else:
        wytyczna = f"podaj widelki od {kwota_dolna} do {kwota_gorna} zl netto"
    raw = call_ai(
        system_pismo,
        f"OTO ZLECENIE:\n{tresc}\n\n"
        f"=== OFERTA KTORA ZOSTALA ZAWETOWANA (przepisz ja) ===\n{oferta}\n\n"
        f"=== DLACZEGO SEDZIA JA ZAWETOWAL ===\n{sedzia.get('uzasadnienie', '')}\n"
        f"Instrukcja naprawy: {sedzia.get('instrukcja_naprawy', '')}\n\n"
        f"=== WERYFIKACJA FAKTOW (researcher sprawdzil zakwestionowane twierdzenia) ===\n{fakty}\n\n"
        f"Przepisz oferte. Zakwestionowane twierdzenia USUN albo zamien na pytania/hipotezy "
        f"zgodnie z weryfikacja faktow. Nie pisz jako pewnika tego, czego nie potwierdzono. "
        f"Zachowaj zakres i cene: {wytyczna}. Podpis na koncu: {PODPIS}. "
        f"Wyslij tylko tekst oferty.",
        temperature=0.7,
    )
    return (raw or oferta).strip()


# Wycena realizowana jest przez moduł wycena_debata.py (Adversarial Debate Useme)


def zbuduj_oferte(zlecenie: Dict[str, Any], verbose: bool = True,
                  zapisz_dziennik: bool = True, tryb_zapisu: str = "pelne") -> Dict[str, Any]:
    """Glowna petla V2. Zwraca pelny wynik z dziennikiem, oferta, wycena, checkerem.

    zapisz_dziennik=False -> nie zostawia roboczego pliku w mozg/dzienniki
    (tryb produkcyjny: artefakty trafiaja tylko do ofertowarki).
    tryb_zapisu: "pelne" (wszystko), "wycena" (tylko wycena - do zbierania danych), "brak".
    """
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

    # ---------- WYCENA (rada 4 modeli: 2x DeepSeek + 2x Gemini + rozjemca) ----------
    say(f"[3/6] Wycena #{job_id}...")
    try:
        wynik_wyceny = wycen_rada(
            tresc_zlecenia=tresc,
            dziennik=dziennik,
            research=research,
            call_ai_fn=call_ai,          # DeepSeek (port 4571)
            call_gemini_fn=call_gemini,  # Gemini (port 8045)
            say=say,
        )
        kwota_dolna = int(wynik_wyceny["kwota_dolna"])
        kwota_gorna = int(wynik_wyceny["kwota_gorna"])
        kwota = int(wynik_wyceny["kwota"])
        dni_od = int(wynik_wyceny.get("dni_od", 14))
        dni_do = int(wynik_wyceny.get("dni_do", 21))
        say(f"    wycena: {kwota_dolna}-{kwota_gorna} zl / {dni_od}-{dni_do} dni")
    except Exception as e:
        say(f"    wycena blad: {e} - fallback 3000-6000/14-21")
        kwota_dolna, kwota_gorna, kwota = 3000, 6000, 4500
        dni_od, dni_do = 14, 21
        wynik_wyceny = {"rozbicie": {"blad": str(e)}, "surowy_tekst": ""}

    # ---------- ITERACJA 3: PISMO ----------
    # Pismo dostaje CALY PRZEBIEG (analiza iter1 + weryfikacja + research + wszystkie
    # rundy debaty wycenowej), nie wyciag. Sam decyduje, jak zbudowac oferte wg pismo.md.
    say(f"[4/6] Pismo #{job_id}...")

    surowy_tekst_wyceny = wynik_wyceny.get("surowy_tekst") or "  (brak surowych glosow wyceny)"

    oferta_raw = call_ai(
        system_pismo,
        f"OTO ZLECENIE:\n{tresc}\n\n"
        f"=== ANALIZA (pierwsze czytanie zlecenia, iteracja 1) ===\n{dziennik_iter1}\n\n"
        f"=== WERYFIKACJA (dojrzaly dziennik po researchu, iteracja 2) ===\n{dziennik}\n\n"
        f"=== RESEARCH (dowody, jesli byly) ===\n{research or 'BRAK'}\n\n"
        f"=== SUROWY ZAPIS WYCENY (glosy 4 modeli + rozjemca, NIC NIE UCIETE) ===\n{surowy_tekst_wyceny}\n\n"
        + (
            f"=== WYTYCZNA CENY (z rozjemcy) ===\n"
            f"Wycena DEFINITYWNA: podaj JEDNA konkretna kwote {kwota_dolna} zł netto. Zero widelek.\n\n"
            if wynik_wyceny.get("definitywna")
            else f"=== WYTYCZNA CENY (z rozjemcy) ===\n"
                 f"Wycena NIEJASNA, sa realne niewiadome: podaj WIDELKI od {kwota_dolna} do {kwota_gorna} zł netto "
                 f"i powiedz od czego zaleza. Nigdy nie schodz ponizej {kwota_dolna} zł.\n\n"
        )
        + f"DECYZJA NALEZY DO CIEBIE. Masz przed soba cale surowe rozumowanie czterech modeli, "
        f"werdykt rozjemcy oraz to, ktore glosy wybral, a ktore odrzucil i dlaczego. "
        f"Zdecyduj sam, jak zbudowac oferte zgodnie z pismo.md. "
        f"Czas podaj jako zakres lub przyblizeniem slowym. "
        f"Podpis na koncu: {PODPIS}\n\n"
        "Napisz oferte. Wynik ma wynikac z surowego rozumowania wyceny. Wyslij tylko tekst oferty.",
        temperature=0.8,
    )
    if not oferta_raw:
        return {"ok": False, "blad": "brak odpowiedzi AI w iteracji 3", "log": log}

    # Usuń ewentualny blok [WYCENA] jeśli model go dokleil
    oferta = re.sub(r"\[WYCENA\].*?(?:\[/WYCENA\]|\Z)", "", oferta_raw, flags=re.DOTALL | re.IGNORECASE).strip()

    # ---------- SANITIZER ----------
    oferta = sanitize_opis(oferta, wycena=kwota, dni=dni_do)

    # ---------- SĘDZIA (z pętlą naprawczą VETO) ----------
    # VETO -> researcher weryfikuje zakwestionowane twierdzenia -> pismo przepisuje
    # z faktami -> sędzia ocenia ponownie. Max 2 próby, żeby nie kręcić w nieskończoność.
    sedzia = {"status": "OK", "kara_pkt": 0}
    veto_przebieg: list = []
    if system_sedzia:
        say(f"[6/6] Sedzia #{job_id}...")
        sedzia = _ocen_u_sedziego(system_sedzia, tresc, oferta, kwota, dni_od, dni_do)

        for proba in range(1, 3):
            if str(sedzia.get("status", "")).upper() != "VETO":
                break
            say(f"    sedzia VETO (proba {proba}): {sedzia.get('uzasadnienie', '')[:70]}")
            say("    -> researcher weryfikuje zakwestionowane twierdzenia...")
            fakty = _weryfikuj_veto(sedzia, oferta, tresc)
            veto_przebieg.append({"proba": proba, "sedzia": sedzia, "fakty": fakty})
            say("    -> pismo przepisuje z faktami...")
            oferta = _przepisz_z_faktami(
                oferta, sedzia, fakty, tresc, system_pismo,
                kwota_dolna, kwota_gorna, bool(wynik_wyceny.get("definitywna")),
            )
            oferta = sanitize_opis(oferta, wycena=kwota, dni=dni_do)
            say("    -> sedzia ocenia ponownie...")
            sedzia = _ocen_u_sedziego(system_sedzia, tresc, oferta, kwota, dni_od, dni_do)

        if str(sedzia.get("status", "")).upper() == "VETO":
            say(f"    sedzia nadal VETO po {len(veto_przebieg)} probach - oferta do przegladu")
        else:
            say(f"    sedzia po naprawie: {sedzia.get('status')}")

    # ---------- CHECKER (na finalnej wersji, po ewentualnej naprawie) ----------
    say(f"[5/6] Checker #{job_id}...")
    sciezka = "biznes" if "biznes" in (pola.get("SCIEZKA_MERYTORYKI", "") or "").lower() else "inzynieria"
    check = sprawdz(oferta, dni=dni_do, sciezka=sciezka, client_text=client_text)
    if not check["ok"]:
        say(f"    checker: {[p['regula'] for p in check['problemy']]}")

    wynik = {
        "ok": True,
        "job_id": job_id,
        "dziennik": dziennik,
        "pola": pola,
        "oferta": oferta,
        "wycena": kwota,
        "wycena_dolna": kwota_dolna,
        "wycena_gorna": kwota_gorna,
        "dni": dni_do, "dni_od": dni_od, "dni_do": dni_do,
        "komponenty": wynik_wyceny.get("komponenty", []),
        "niepewnosci": wynik_wyceny.get("niepewnosci", []),
        "wycena_rozbicie": wynik_wyceny.get("rozbicie", {}),
        "checker": check,
        "sedzia": sedzia,
        "veto_przebieg": veto_przebieg,
        "research": research,
        "wycena_surowa": wynik_wyceny.get("surowy_tekst", ""),
        "dziennik_iter1": dziennik_iter1,
        "log": log,
    }

    # ---------- ZAPIS ARTEFAKTOW ----------
    # Produkcyjnie: pelny zapis do ofertowarki (analiza, research, wycena, oferta).
    # Dziennik roboczy w mozg/dzienniki tylko na zadanie (dev).
    # PELNE LOGI calego lancucha -> Botv2/logi/<job_id>/ (zawsze, posegregowane).
    _zapisz_logi(job_id, zlecenie, dziennik_iter1, dziennik, research, wynik_wyceny,
                 oferta_raw, oferta, check, sedzia, veto_przebieg, log)
    _zapisz_artefakty_ofertowarka(job_id, dziennik_iter1, dziennik, research, wynik_wyceny, oferta, check, sedzia, tryb_zapisu)
    if zapisz_dziennik:
        (DZIENNIKI_DIR / f"{job_id}.json").write_text(
            json.dumps(wynik, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return wynik


def _zapisz_logi(job_id: str, zlecenie: Dict[str, Any], dziennik_iter1: str,
                 dziennik: str, research: str, wynik_wyceny: Dict[str, Any],
                 oferta_raw: str, oferta: str, check: Dict[str, Any],
                 sedzia: Dict[str, Any], veto_przebieg: list, log: list) -> None:
    """Zapisuje WSZYSTKO z calego lancucha do Botv2/logi/<job_id>/.

    Posegregowane per zlecenie. Zawsze (niezaleznie od trybu ofertowarki).
    Zawartosc:
      00_zlecenie.txt     - surowa tresc wejsciowa
      01_analiza.md       - dziennik iteracji 1
      02_research.md      - surowy research
      03_weryfikacja.md   - dziennik po weryfikacji (iteracja 2)
      04_wycena.md        - surowy zapis rady 4 modeli + rozjemca
      05_pismo_raw.md     - pismo przed sanitizerem
      06_oferta_final.md  - oferta po sanitizerze
      07_checker.json     - wynik checkera
      08_sedzia.json      - werdykt sedziego (+ petla VETO)
      09_veto_przebieg.md - przebieg napraw po VETO (jesli byl)
      10_log.txt          - pelny log przebiegu (kroki)
      wynik.json          - podsumowanie strukturalne
    """
    try:
        out = LOGI_DIR / str(job_id)
        out.mkdir(parents=True, exist_ok=True)

        (out / "00_zlecenie.txt").write_text(
            f"TYTUL: {zlecenie.get('title', '')}\n"
            f"BUDZET: {zlecenie.get('budget', '')}\n\n"
            f"OPIS:\n{zlecenie.get('full_description', '')}\n", encoding="utf-8")
        (out / "01_analiza.md").write_text(dziennik_iter1 or "", encoding="utf-8")
        (out / "02_research.md").write_text(research or "", encoding="utf-8")
        (out / "03_weryfikacja.md").write_text(dziennik or "", encoding="utf-8")
        (out / "04_wycena.md").write_text(wynik_wyceny.get("surowy_tekst", "") or "", encoding="utf-8")
        (out / "05_pismo_raw.md").write_text(oferta_raw or "", encoding="utf-8")
        (out / "06_oferta_final.md").write_text(oferta or "", encoding="utf-8")
        (out / "07_checker.json").write_text(
            json.dumps(check, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "08_sedzia.json").write_text(
            json.dumps(sedzia, ensure_ascii=False, indent=2), encoding="utf-8")
        if veto_przebieg:
            bloki = []
            for v in veto_przebieg:
                bloki.append(
                    f"=== PROBA {v.get('proba')} ===\n"
                    f"SEDZIA: {json.dumps(v.get('sedzia'), ensure_ascii=False)}\n\n"
                    f"WERYFIKACJA FAKTOW:\n{v.get('fakty')}\n"
                )
            (out / "09_veto_przebieg.md").write_text("\n\n".join(bloki), encoding="utf-8")
        (out / "10_log.txt").write_text("\n".join(log or []), encoding="utf-8")

        podsum = {
            "job_id": job_id,
            "title": zlecenie.get("title", ""),
            "budget": zlecenie.get("budget", ""),
            "wycena_dolna": wynik_wyceny.get("kwota_dolna"),
            "wycena_gorna": wynik_wyceny.get("kwota_gorna"),
            "definitywna": wynik_wyceny.get("definitywna"),
            "dni_od": wynik_wyceny.get("dni_od"),
            "dni_do": wynik_wyceny.get("dni_do"),
            "uzasadnienie_rozjemcy": wynik_wyceny.get("uzasadnienie_rozjemcy"),
            "od_czego_zaleza": wynik_wyceny.get("od_czego_zaleza"),
            "checker_ok": check.get("ok"),
            "sedzia": sedzia.get("status"),
            "veto_napraw": len(veto_przebieg),
        }
        (out / "wynik.json").write_text(
            json.dumps(podsum, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[ZAPIS-LOGI] blad dla #{job_id}: {e}", flush=True)


def _zapisz_artefakty_ofertowarka(job_id: str, dziennik_iter1: str, dziennik: str,
                                  research: str, wynik_wyceny: Dict[str, Any],
                                  oferta: str, check: Dict[str, Any],
                                  sedzia: Dict[str, Any], tryb: str = "pelne") -> None:
    """Zapisuje artefakty lancucha do 01_ofertowarka/<job_id>/.

    tryb="pelne"   -> analiza + research + weryfikacja + wycena + pismo + koncowa
    tryb="wycena"  -> TYLKO wycena (do zbierania danych / analizy wycen)
    tryb="brak"    -> nic nie zapisuje
    """
    if tryb == "brak":
        return
    try:
        out = OFERTOWARKA_DIR / str(job_id)
        out.mkdir(parents=True, exist_ok=True)

        if tryb == "wycena":
            # Tylko wycena + krotki wynik z decyzja.
            (out / "4_wycena.md").write_text(wynik_wyceny.get("surowy_tekst", "") or "", encoding="utf-8")
            wynik_wyc = {
                "job_id": job_id,
                "wycena_dolna": wynik_wyceny.get("kwota_dolna"),
                "wycena_gorna": wynik_wyceny.get("kwota_gorna"),
                "definitywna": wynik_wyceny.get("definitywna"),
                "dni_od": wynik_wyceny.get("dni_od"),
                "dni_do": wynik_wyceny.get("dni_do"),
                "uzasadnienie_rozjemcy": wynik_wyceny.get("uzasadnienie_rozjemcy"),
                "od_czego_zaleza": wynik_wyceny.get("od_czego_zaleza"),
                "sedzia": sedzia.get("status"),
                "checker_ok": check.get("ok"),
            }
            (out / "wycena.json").write_text(
                json.dumps(wynik_wyc, ensure_ascii=False, indent=2), encoding="utf-8")
            return

        # tryb pelne
        (out / "1_analiza.md").write_text(dziennik_iter1 or "", encoding="utf-8")
        (out / "2_research.md").write_text(research or "", encoding="utf-8")
        (out / "3_weryfikacja.md").write_text(dziennik or "", encoding="utf-8")
        (out / "4_wycena.md").write_text(wynik_wyceny.get("surowy_tekst", "") or "", encoding="utf-8")
        (out / "5_pismo.md").write_text(oferta or "", encoding="utf-8")
        koncowa = (
            f"# OFERTA KONCOWA #{job_id}\n\n"
            f"WYCENA: {wynik_wyceny.get('kwota_dolna')}-{wynik_wyceny.get('kwota_gorna')} zl netto\n"
            f"CHECKER: {'OK' if check.get('ok') else [p['regula'] for p in check.get('problemy', [])]}\n"
            f"SEDZIA: {sedzia.get('status')} (kara {sedzia.get('kara_pkt')} pkt)\n\n---\n\n{oferta}\n"
        )
        (out / "6_koncowa.md").write_text(koncowa, encoding="utf-8")
    except Exception as e:
        print(f"[ZAPIS-ARTEFAKTY] blad dla #{job_id}: {e}", flush=True)
