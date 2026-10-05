# -*- coding: utf-8 -*-
"""Ulepszony, odporny test debaty DWÓCH RÓŻNYCH MODELI (DeepSeek vs Gemini) BEZ widełek kwotowych.

Usprawnienia v2:
1. Automatyczny retry (do 3 prób z backoffem 2s) w przypadku pustej odpowiedzi lub błędu parsowania JSON.
2. Robust parser JSON obsługujący formatowanie '15 000 zł', stringi, spacje, markdown ```json.
3. Nigdy nie przekazujemy 'BŁĄD' do drugiego modelu jako merytorycznego werdyktu.
4. Sprawdzenie obu kierunków:
   - Wariant A: Wyceniacz = DeepSeek-v4-Pro, Reviewer = Gemini-3.8-Flash
   - Wariant B: Wyceniacz = Gemini-3.8-Flash, Reviewer = DeepSeek-v4-Pro
5. Zapis surowych logów do Botv2/debug/eksperyment_debata_dwumodelowa_v2.json.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEEPSEEK_URL = "http://127.0.0.1:4571/v1/chat/completions"
GEMINI_URL = "http://127.0.0.1:8045/v1/chat/completions"

# --- CZYSTE PROMPTY BEZ JAKICHKOLWIEK LICZB I WIDEŁEK ---
PROMPT_WYCENIACZ = """Jesteś Ksawierem – polskim inżynierem-freelancerem na platformie Useme.
Rozliczasz się przez umowę o dzieło na Useme (bez pośredników, bez firmy, bez kosztów biura agencji).
Pracujesz solo, wspomagany zaawansowanymi narzędziami programistycznymi AI (piszesz architekturę, kod i testy znacznie szybciej niż tradycyjne zespoły, zachowując najwyższą jakość).

ZASADY WYCENY DLA FREELANCERA NA USEME:
1. BRAK 'STAWKI DZIENNEJ' (MAN-DAY):
   - Termin w dniach to czas kalendarzowy projektu (etapowanie, testy klienta na rzeczywistych danych, poprawki). Nie przeliczasz tego jak etatu korporacyjnego (dni * 8h).
2. PSYCHOLOGIA I REALIA POLSKICH KLIENTÓW MŚP NA USEME:
   - Klienci na Useme to zazwyczaj małe i średnie polskie firmy, które szukają zwinnego specjalisty, bo agencja software house wyceniła ich na kosmiczne kwoty enterprise.
   - Pamiętaj o dwóch skrajnościach:
     * Unikaj amatorskiego dumpingu za grosze (klient ucieka przed kimś, kto rzuca kwotami niepoważnymi za trudny system).
     * Unikaj stawek korporacyjnego software house'u z Warszawy (przetargi korporacyjne to nie ten rynek; klient na Useme natychmiast odrzuci taką ofertę).
   - Wyceniaj za wartość biznesową, trudność inżynierską, ryzyko i odpowiedzialność za dane/proces klienta.
3. KOTWICA BUDŻETU:
   - Jeśli klient w ogłoszeniu podał kwotę 50–250 zł, to zazwyczaj oznacza deklarowaną stawkę za godzinę konsultacji/rozwoju, a NIE budżet na całość!
   - Jeśli klient podał jawny budżet całkowity, weź go pod uwagę przy ocenie realnych możliwości klienta.

Na podstawie zlecenia oszacuj rzetelną kwotę w PLN netto oraz termin w dniach kalendarzowych (min. 7 dni).

Zwróć WYŁĄCZNIE JSON:
{
  "kwota": <int>,
  "dni_od": <int>,
  "dni_do": <int>,
  "uzasadnienie": "2-3 konkretne zdania inżynierskie: dlaczego taka kwota i termin dla freelancera z AI na Useme"
}
"""

PROMPT_REVIEWER = """Jesteś bezwzględnym, doświadczonym recenzentem zleceń freelancerskich na polskim Useme.
Widzisz treść zlecenia oraz propozycję wyceny przesłaną przez innego freelancera.

TWOJA ROLA:
Oceń szczerze, czy ta wycena ma realną szansę wygrać zlecenie u polskiego klienta MŚP na Useme:
1. PAMIĘTAJ: To jest rynek freelancingu, a nie body-leasing korporacyjny. Nie przeliczaj dni na stawkę dzienną. Dni to czas kalendarzowy z testami i rezerwą.
2. Zdiagnozuj:
   - Czy kwota to "ZA_MALA" (dumping, niedoszacowanie ryzyka i skali, robienie z siebie taniej siły roboczej)?
   - Czy kwota to "ZA_DUZA" (przestrzelenie realiów budżetowych MŚP, wejście w stawki agencji enterprise, które odstraszą klienta)?
   - Czy kwota to "OK" (maksymalna profesjonalna marża, która wciąż mieści się w granicach akceptowalności dla decydenta MŚP)?

Zwróć WYŁĄCZNIE JSON:
{
  "werdykt": "ZA_MALA" lub "OK" lub "ZA_DUZA",
  "kwota_sugerowana": <int>,
  "dni_sugerowane_do": <int>,
  "uzasadnienie": "2-3 zdania twardej krytyki lub potwierdzenia",
  "twoje_oszacowanie_rynku": "Twoje widełki w PLN netto dla tego zlecenia na Useme"
}
"""


def _oczysc_int(wartosc: Any, domyslna: int = 0) -> int:
    """Konwertuje dowolną wartość (int, str np. '15 000 zł', float) na czysty int."""
    if wartosc is None:
        return domyslna
    if isinstance(wartosc, (int, float)):
        return int(wartosc)
    s = str(wartosc).strip()
    tylko_cyfry = re.sub(r"[^\d]", "", s)
    if tylko_cyfry:
        return int(tylko_cyfry)
    return domyslna


def parsuj_json_wyceniacz(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass

    if isinstance(data, dict):
        kwota = _oczysc_int(data.get("kwota"))
        dni_od = _oczysc_int(data.get("dni_od"), 7)
        dni_do = _oczysc_int(data.get("dni_do"), max(dni_od, 14))
        if kwota > 0:
            return {
                "kwota": kwota,
                "dni_od": dni_od,
                "dni_do": dni_do,
                "uzasadnienie": str(data.get("uzasadnienie", "")).strip(),
            }

    # Fallback regex (w przypadku obcięcia strumienia pod koniec)
    m_kwota = re.search(r'"kwota"\s*:\s*["\']?(\d[\d\s]*)', raw)
    if m_kwota:
        kwota = _oczysc_int(m_kwota.group(1))
        if kwota > 0:
            m_od = re.search(r'"dni_od"\s*:\s*["\']?(\d[\d\s]*)', raw)
            m_do = re.search(r'"dni_do"\s*:\s*["\']?(\d[\d\s]*)', raw)
            m_uz = re.search(r'"uzasadnienie"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
            dni_od = _oczysc_int(m_od.group(1), 7) if m_od else 7
            dni_do = _oczysc_int(m_do.group(1), max(dni_od, 14)) if m_do else 21
            uz = m_uz.group(1) if m_uz else "Uzasadnienie z debaty."
            return {
                "kwota": kwota,
                "dni_od": dni_od,
                "dni_do": dni_do,
                "uzasadnienie": uz.strip(),
            }
    return None


def parsuj_json_reviewer(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass

    if isinstance(data, dict):
        werdykt_raw = str(data.get("werdykt", "")).upper().strip()
        if "MALA" in werdykt_raw or "MAŁA" in werdykt_raw:
            werdykt = "ZA_MALA"
        elif "DUZA" in werdykt_raw or "DUŻA" in werdykt_raw:
            werdykt = "ZA_DUZA"
        elif "OK" in werdykt_raw:
            werdykt = "OK"
        else:
            werdykt = "OK"

        kwota_sug = _oczysc_int(data.get("kwota_sugerowana"), 0)
        dni_sug = _oczysc_int(data.get("dni_sugerowane_do"), 0)

        return {
            "werdykt": werdykt,
            "kwota_sugerowana": kwota_sug,
            "dni_sugerowane_do": dni_sug,
            "uzasadnienie": str(data.get("uzasadnienie", "")).strip(),
            "twoje_oszacowanie_rynku": str(data.get("twoje_oszacowanie_rynku", "")).strip(),
        }

    # Fallback regex
    m_w = re.search(r'"werdykt"\s*:\s*["\']?([A-Za-z_]+)', raw)
    if m_w:
        werdykt_raw = m_w.group(1).upper().strip()
        if "MALA" in werdykt_raw or "MAŁA" in werdykt_raw:
            werdykt = "ZA_MALA"
        elif "DUZA" in werdykt_raw or "DUŻA" in werdykt_raw:
            werdykt = "ZA_DUZA"
        else:
            werdykt = "OK"
        m_kw = re.search(r'"kwota_sugerowana"\s*:\s*["\']?(\d[\d\s]*)', raw)
        kwota_sug = _oczysc_int(m_kw.group(1)) if m_kw else 0
        m_dni = re.search(r'"dni_sugerowane_do"\s*:\s*["\']?(\d[\d\s]*)', raw)
        dni_sug = _oczysc_int(m_dni.group(1)) if m_dni else 0
        m_uz = re.search(r'"uzasadnienie"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
        uz = m_uz.group(1) if m_uz else ""
        m_ryn = re.search(r'"twoje_oszacowanie_rynku"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
        ryn = m_ryn.group(1) if m_ryn else ""
        return {
            "werdykt": werdykt,
            "kwota_sugerowana": kwota_sug,
            "dni_sugerowane_do": dni_sug,
            "uzasadnienie": uz.strip(),
            "twoje_oszacowanie_rynku": ryn.strip(),
        }
    return None


def call_deepseek_raw(system_prompt: str, user_prompt: str, timeout: int = 120) -> Optional[str]:
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 1000,
        "stream": True,
    }
    try:
        r = requests.post(DEEPSEEK_URL, json=payload, timeout=(10, timeout), stream=True)
        if r.status_code != 200:
            print(f"[DeepSeek HTTP {r.status_code}]")
            return None
        full = ""
        for line in r.iter_lines(decode_unicode=True):
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
        return full.strip() or None
    except Exception as e:
        print(f"[DeepSeek Błąd połączenia]: {e}")
        return None


def call_gemini_raw(system_prompt: str, user_prompt: str, timeout: int = 90) -> Optional[str]:
    payload = {
        "model": "gemini-3.8-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 1000,
    }
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip() or None
        else:
            print(f"[Gemini HTTP {r.status_code}] {r.text[:200]}")
    except Exception as e:
        print(f"[Gemini Błąd połączenia]: {e}")
    return None


def call_with_retry(
    fn_call: Callable[[str, str], Optional[str]],
    parser_fn: Callable[[Optional[str]], Optional[Dict[str, Any]]],
    system_prompt: str,
    user_prompt: str,
    nazwa_modelu: str,
    max_proby: int = 3,
    delay: float = 2.0,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], float]:
    """Wywoluje model z automatycznym ponawianiem w przypadku błędu sieci lub parsowania."""
    t_start = time.time()
    for proba in range(1, max_proby + 1):
        if proba > 1:
            print(f"    [{nazwa_modelu}] Retry próba {proba}/{max_proby} po {delay}s...")
            time.sleep(delay)
        raw = fn_call(system_prompt, user_prompt)
        parsed = parser_fn(raw)
        if parsed is not None:
            czas = time.time() - t_start
            return parsed, raw, czas
        print(f"    [{nazwa_modelu}] Nieudane parsowanie JSON w próbie {proba}. Surowy tekst: {repr(raw)[:100]}")
    czas = time.time() - t_start
    return None, None, czas


def wykonaj_debate(
    nazwa: str,
    tresc: str,
    nazwa_wyceniacza: str,
    fn_wyceniacz: Callable[[str, str], Optional[str]],
    nazwa_reviewera: str,
    fn_reviewer: Callable[[str, str], Optional[str]],
    max_rundy: int = 2,
) -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print(f"DEBATA: {nazwa}")
    print(f"Role: WYCENIACZ = [{nazwa_wyceniacza}] vs REVIEWER = [{nazwa_reviewera}]")
    print("=" * 80)

    log_rund = []

    # --- RUNDA 0: Wyceniacz ---
    prompt_w0 = f"ZLECENIE KLIENTA NA USEME:\n{tresc}"
    prop, raw_w0, czas_w0 = call_with_retry(
        fn_wyceniacz,
        parsuj_json_wyceniacz,
        PROMPT_WYCENIACZ,
        prompt_w0,
        nazwa_modelu=nazwa_wyceniacza,
    )
    if not prop:
        raise RuntimeError(f"Model wyceniacza {nazwa_wyceniacza} nie zwrocil poprawnej wyceny po 3 próbach!")

    print(f"[{nazwa_wyceniacza} R0] {prop['kwota']} zł | {prop['dni_od']}-{prop['dni_do']} dni ({czas_w0:.2f}s)")
    print(f"   Uzasadnienie: {prop['uzasadnienie']}")

    log_rund.append({
        "runda": 0,
        "aktor": nazwa_wyceniacza,
        "kwota": prop["kwota"],
        "dni_od": prop["dni_od"],
        "dni_do": prop["dni_do"],
        "uzasadnienie": prop["uzasadnienie"],
        "surowy_tekst": raw_w0,
        "czas_s": round(czas_w0, 2),
    })

    rev = {}
    for runda in range(1, max_rundy + 1):
        # Odczekaj 1s dla ustabilizowania przeglądarki Gemini
        time.sleep(1.5)

        # --- REVIEWER ---
        prompt_rev = (
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\n"
            f"--- PROPOZYCJA WYCENIACZA ({nazwa_wyceniacza}) ---\n"
            f"KWOTA: {prop['kwota']} zł netto\n"
            f"TERMIN: {prop['dni_od']}-{prop['dni_do']} dni kalendarzowych\n"
            f"UZASADNIENIE: {prop['uzasadnienie']}\n\n"
            f"Oceń tę propozycję obiektywnie dla rynku Useme."
        )
        rev, raw_r, czas_r = call_with_retry(
            fn_reviewer,
            parsuj_json_reviewer,
            PROMPT_REVIEWER,
            prompt_rev,
            nazwa_modelu=nazwa_reviewera,
        )
        if not rev:
            print(f"    [{nazwa_reviewera}] Brak odpowiedzi reviewera po 3 próbach - zakończenie debaty.")
            rev = {
                "werdykt": "OK",
                "kwota_sugerowana": prop["kwota"],
                "dni_sugerowane_do": prop["dni_do"],
                "uzasadnienie": "Zakończono z powodu braku odpowiedzi recenzenta.",
                "twoje_oszacowanie_rynku": "",
            }
            break

        print(f"\n[{nazwa_reviewera} R{runda}] Werdykt: {rev['werdykt']} (sugeruje: {rev['kwota_sugerowana']} zł, rynek: {rev['twoje_oszacowanie_rynku']}) ({czas_r:.2f}s)")
        print(f"   Krytyka: {rev['uzasadnienie']}")

        log_rund.append({
            "runda": runda,
            "aktor": nazwa_reviewera,
            "werdykt": rev["werdykt"],
            "kwota_sugerowana": rev["kwota_sugerowana"],
            "dni_sugerowane_do": rev["dni_sugerowane_do"],
            "twoje_oszacowanie_rynku": rev["twoje_oszacowanie_rynku"],
            "uzasadnienie": rev["uzasadnienie"],
            "surowy_tekst": raw_r,
            "czas_s": round(czas_r, 2),
        })

        if rev["werdykt"] == "OK":
            print(f"\n>>> [KONSENSUS W RUNDZIE {runda}] Kwota: {prop['kwota']} zł | {prop['dni_od']}-{prop['dni_do']} dni")
            break

        # Odczekaj 1s
        time.sleep(1.0)

        # --- WYCENIACZ KONTRA ---
        prompt_kontra = (
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\n"
            f"TWOJA POPRZEDNIA PROPOZYCJA: {prop['kwota']} zł / {prop['dni_od']}-{prop['dni_do']} dni.\n"
            f"RECENZENT ({nazwa_reviewera}) OCENIŁ: {rev['werdykt']}\n"
            f"KRYTYKA RECENZENTA: {rev['uzasadnienie']}\n"
            f"SUGESTIA RECENZENTA: {rev['kwota_sugerowana']} zł (jego szacunek rynku: {rev['twoje_oszacowanie_rynku']})\n\n"
            f"Ustosunkuj się merytorycznie. Jeśli recenzent ma rację, skoryguj kwotę. Jeśli uważasz, że Twoja wycena broni się inżyniersko, uzasadnij to. Zwróć JSON."
        )
        nowy_prop, raw_kontra, czas_kontra = call_with_retry(
            fn_wyceniacz,
            parsuj_json_wyceniacz,
            PROMPT_WYCENIACZ,
            prompt_kontra,
            nazwa_modelu=nazwa_wyceniacza,
        )
        if not nowy_prop:
            print(f"    [{nazwa_wyceniacza}] Brak odpowiedzi kontry po 3 próbach - zachowanie kwoty {prop['kwota']} zł.")
            break

        prop = nowy_prop
        print(f"\n[{nazwa_wyceniacza} R{runda} Kontra] -> {prop['kwota']} zł | {prop['dni_od']}-{prop['dni_do']} dni ({czas_kontra:.2f}s)")
        print(f"   Uzasadnienie: {prop['uzasadnienie']}")

        log_rund.append({
            "runda": runda,
            "aktor": f"{nazwa_wyceniacza}_kontra",
            "kwota": prop["kwota"],
            "dni_od": prop["dni_od"],
            "dni_do": prop["dni_do"],
            "uzasadnienie": prop["uzasadnienie"],
            "surowy_tekst": raw_kontra,
            "czas_s": round(czas_kontra, 2),
        })

    return {
        "nazwa": nazwa,
        "wyceniacz_model": nazwa_wyceniacza,
        "reviewer_model": nazwa_reviewera,
        "kwota_finalna": prop["kwota"],
        "dni_od": prop["dni_od"],
        "dni_do": prop["dni_do"],
        "uzasadnienie_finalne": prop["uzasadnienie"],
        "ostatni_werdykt_reviewera": rev.get("werdykt"),
        "log_rund": log_rund,
    }


def main():
    root = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia")
    zlecenia = [
        {
            "id": "145285",
            "nazwa": "145285 Subiekt <-> BaseLinker (40k produktów)",
            "plik": root / "145285" / "zlecenie.json",
        },
        {
            "id": "145287",
            "nazwa": "145287 Aplikacja mobilna offline (kierowcy/serwis)",
            "plik": root / "145287" / "zlecenie.json",
        },
        {
            "id": "144890",
            "nazwa": "144890 Automatyzacja faktur OCR + Optima",
            "plik": root / "zlecenie_testowe_144890" / "zlecenie.json",
        },
    ]

    wyniki = []

    for z in zlecenia:
        dane = json.loads(z["plik"].read_text(encoding="utf-8"))
        tresc = dane.get("description") or dane.get("opis", "")

        # --- KIERUNEK A: Wyceniacz = DeepSeek, Reviewer = Gemini ---
        res_a = wykonaj_debate(
            nazwa=f"{z['nazwa']} [A: DS->GEM]",
            tresc=tresc,
            nazwa_wyceniacza="DeepSeek-v4-Pro",
            fn_wyceniacz=call_deepseek_raw,
            nazwa_reviewera="Gemini-3.8-Flash",
            fn_reviewer=call_gemini_raw,
            max_rundy=2,
        )
        wyniki.append(res_a)

        # Odpoczynek 2s między kierunkami
        time.sleep(2.0)

        # --- KIERUNEK B: Wyceniacz = Gemini, Reviewer = DeepSeek ---
        res_b = wykonaj_debate(
            nazwa=f"{z['nazwa']} [B: GEM->DS]",
            tresc=tresc,
            nazwa_wyceniacza="Gemini-3.8-Flash",
            fn_wyceniacz=call_gemini_raw,
            nazwa_reviewera="DeepSeek-v4-Pro",
            fn_reviewer=call_deepseek_raw,
            max_rundy=2,
        )
        wyniki.append(res_b)

        time.sleep(2.0)

    # Zapis surowych logów do pliku
    out_dir = Path("Botv2/debug")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "eksperyment_debata_dwumodelowa_v2.json"
    out_file.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 80)
    print("PODSUMOWANIE DEBATY DWUMODELOWEJ V2 (BEZ ARTEFAKTÓW PARSERA):")
    print("=" * 80)
    for r in wyniki:
        print(f"* {r['nazwa']}: {r['kwota_finalna']} zł ({r['dni_od']}-{r['dni_do']} dni) | Ostatni werdykt: {r['ostatni_werdykt_reviewera']}")
    print(f"\nPełne surowe logi zapisano w: {out_file}")


if __name__ == "__main__":
    main()
