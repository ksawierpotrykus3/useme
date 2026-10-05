# -*- coding: utf-8 -*-
"""Niezależny test debaty DWÓCH RÓŻNYCH MODELI (DeepSeek vs Gemini) BEZ widełek kwotowych.

Cel:
1. Usunięcie jakichkolwiek hardkodowanych przedziałów kwotowych (zero 5-12k, zero 15k bariera).
2. Prawdziwa debata dwóch różnych rodzin modeli:
   - DeepSeek (port 4571)
   - Gemini (port 8045)
3. Sprawdzenie w obu kierunkach:
   - Wariant 1: Wyceniacz = DeepSeek, Reviewer = Gemini
   - Wariant 2: Wyceniacz = Gemini, Reviewer = DeepSeek
4. Zapis surowych logów (prompty, odpowiedzi, czasy) do pliku.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEEPSEEK_URL = "http://127.0.0.1:4571/v1/chat/completions"
GEMINI_URL = "http://127.0.0.1:8045/v1/chat/completions"

# --- PROMPTY BEZ JAKICHKOLWIEK LICZB / WIDEŁEK ---
PROMPT_WYCENIACZ_CZYSTY = """Jesteś Ksawierem – polskim inżynierem-freelancerem na platformie Useme.
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
   - Wyceniaj za wartość biznesową, trudność inżynierską, ryzyko i odpowiedzialność.
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

PROMPT_REVIEWER_CZYSTY = """Jesteś bezwzględnym, doświadczonym recenzentem zleceń freelancerskich na polskim Useme.
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


def _call_deepseek(system_prompt: str, user_prompt: str, timeout: int = 120) -> Optional[str]:
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
        return full or None
    except Exception as e:
        print(f"[DeepSeek Błąd]: {e}")
    return None


def _call_gemini(system_prompt: str, user_prompt: str, timeout: int = 60) -> Optional[str]:
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
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"[Gemini Błąd]: {e}")
    return None


def _parsuj_json(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def debata_dwumodelowa(
    nazwa: str,
    tresc: str,
    nazwa_wyceniacza: str,
    fn_wyceniacz,
    nazwa_reviewera: str,
    fn_reviewer,
    max_rundy: int = 2,
) -> Dict[str, Any]:
    print("\n" + "=" * 80)
    print(f"DEBATA: {nazwa}")
    print(f"Role: WYCENIACZ = [{nazwa_wyceniacza}] vs REVIEWER = [{nazwa_reviewera}] (BEZ WIDEŁEK KWOTOWYCH)")
    print("=" * 80)

    log_rund = []

    # Runda 0: Wyceniacz
    t0 = time.time()
    odp_w0 = fn_wyceniacz(PROMPT_WYCENIACZ_CZYSTY, f"ZLECENIE KLIENTA NA USEME:\n{tresc}")
    czas_w0 = time.time() - t0
    prop = _parsuj_json(odp_w0) or {"kwota": 0, "dni_od": 0, "dni_do": 0, "uzasadnienie": "Błąd parsowania"}

    print(f"[{nazwa_wyceniacza} R0] {prop.get('kwota')} zł | {prop.get('dni_od')}-{prop.get('dni_do')} dni ({czas_w0:.2f}s)")
    print(f"   Uzasadnienie: {prop.get('uzasadnienie')}")

    log_rund.append({
        "runda": 0,
        "aktor": nazwa_wyceniacza,
        "kwota": prop.get("kwota"),
        "dni_od": prop.get("dni_od"),
        "dni_do": prop.get("dni_do"),
        "uzasadnienie": prop.get("uzasadnienie"),
        "surowy_tekst": odp_w0,
        "czas_s": round(czas_w0, 2),
    })

    rev = {}
    for runda in range(1, max_rundy + 1):
        # Reviewer
        prompt_rev = (
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\n"
            f"--- PROPOZYCJA WYCENIACZA ({nazwa_wyceniacza}) ---\n"
            f"KWOTA: {prop.get('kwota')} zł netto\n"
            f"TERMIN: {prop.get('dni_od')}-{prop.get('dni_do')} dni kalendarzowych\n"
            f"UZASADNIENIE: {prop.get('uzasadnienie')}\n\n"
            f"Oceń tę propozycję obiektywnie dla rynku Useme."
        )
        t1 = time.time()
        odp_r = fn_reviewer(PROMPT_REVIEWER_CZYSTY, prompt_rev)
        czas_r = time.time() - t1
        rev = _parsuj_json(odp_r) or {"werdykt": "BŁĄD", "uzasadnienie": "Błąd parsowania"}

        print(f"\n[{nazwa_reviewera} R{runda}] Werdykt: {rev.get('werdykt')} (sugeruje: {rev.get('kwota_sugerowana')} zł, rynek: {rev.get('twoje_oszacowanie_rynku')}) ({czas_r:.2f}s)")
        print(f"   Krytyka: {rev.get('uzasadnienie')}")

        log_rund.append({
            "runda": runda,
            "aktor": nazwa_reviewera,
            "werdykt": rev.get("werdykt"),
            "kwota_sugerowana": rev.get("kwota_sugerowana"),
            "dni_sugerowane_do": rev.get("dni_sugerowane_do"),
            "twoje_oszacowanie_rynku": rev.get("twoje_oszacowanie_rynku"),
            "uzasadnienie": rev.get("uzasadnienie"),
            "surowy_tekst": odp_r,
            "czas_s": round(czas_r, 2),
        })

        if str(rev.get("werdykt", "")).upper() == "OK":
            print(f"\n>>> [KONSENSUS W RUNDZIE {runda}] Kwota: {prop.get('kwota')} zł | {prop.get('dni_od')}-{prop.get('dni_do')} dni")
            break

        # Wyceniacz kontra
        prompt_kontra = (
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\n"
            f"TWOJA POPRZEDNIA PROPOZYCJA: {prop.get('kwota')} zł / {prop.get('dni_od')}-{prop.get('dni_do')} dni.\n"
            f"RECENZENT ({nazwa_reviewera}) OCENIŁ: {rev.get('werdykt')}\n"
            f"KRYTYKA RECENZENTA: {rev.get('uzasadnienie')}\n"
            f"SUGESTIA RECENZENTA: {rev.get('kwota_sugerowana')} zł (jego szacunek rynku: {rev.get('twoje_oszacowanie_rynku')})\n\n"
            f"Ustosunkuj się merytorycznie. Jeśli recenzent ma rację, skoryguj kwotę. Jeśli uważasz, że Twoja wycena broni się inżyniersko, uzasadnij to. Zwróć JSON."
        )
        t2 = time.time()
        odp_w = fn_wyceniacz(PROMPT_WYCENIACZ_CZYSTY, prompt_kontra)
        czas_w = time.time() - t2
        nowy_prop = _parsuj_json(odp_w)
        if nowy_prop:
            prop = nowy_prop
        print(f"\n[{nazwa_wyceniacza} R{runda} Kontra] -> {prop.get('kwota')} zł | {prop.get('dni_od')}-{prop.get('dni_do')} dni ({czas_w:.2f}s)")
        print(f"   Uzasadnienie: {prop.get('uzasadnienie')}")

        log_rund.append({
            "runda": runda,
            "aktor": f"{nazwa_wyceniacza}_kontra",
            "kwota": prop.get("kwota"),
            "dni_od": prop.get("dni_od"),
            "dni_do": prop.get("dni_do"),
            "uzasadnienie": prop.get("uzasadnienie"),
            "surowy_tekst": odp_w,
            "czas_s": round(czas_w, 2),
        })

    return {
        "nazwa": nazwa,
        "wyceniacz_model": nazwa_wyceniacza,
        "reviewer_model": nazwa_reviewera,
        "kwota_finalna": prop.get("kwota"),
        "dni_od": prop.get("dni_od"),
        "dni_do": prop.get("dni_do"),
        "uzasadnienie_finalne": prop.get("uzasadnienie"),
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

    wszystkie_wyniki = []

    for z in zlecenia:
        dane = json.loads(z["plik"].read_text(encoding="utf-8"))
        tresc = dane.get("description") or dane.get("opis", "")

        # --- KONFIGURACJA 1: Wyceniacz = DeepSeek, Reviewer = Gemini ---
        w1 = debata_dwumodelowa(
            z["nazwa"],
            tresc,
            nazwa_wyceniacza="DeepSeek-v4-Pro",
            fn_wyceniacz=_call_deepseek,
            nazwa_reviewera="Gemini-3.8-Flash",
            fn_reviewer=_call_gemini,
            max_rundy=2,
        )
        wszystkie_wyniki.append(w1)

        # --- KONFIGURACJA 2: Wyceniacz = Gemini, Reviewer = DeepSeek ---
        w2 = debata_dwumodelowa(
            z["nazwa"],
            tresc,
            nazwa_wyceniacza="Gemini-3.8-Flash",
            fn_wyceniacz=_call_gemini,
            nazwa_reviewera="DeepSeek-v4-Pro",
            fn_reviewer=_call_deepseek,
            max_rundy=2,
        )
        wszystkie_wyniki.append(w2)

    # Zapis surowych logów do pliku
    out_dir = Path("Botv2/debug")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "eksperyment_debata_dwumodelowa.json"
    out_file.write_text(json.dumps(wszystkie_wyniki, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n=======================================================")
    print(f"PEŁNY RAPORT I SUROWE LOGI ZAPISANE W: {out_file}")
    print(f"=======================================================")


if __name__ == "__main__":
    main()
