# -*- coding: utf-8 -*-
"""Test debaty wycenowej: wyceniacz vs reviewer, az do porozumienia. Zlecenie KSeF."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai, _wyciagnij_json_blok

BASE = Path("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
dane = json.loads(BASE.read_text(encoding="utf-8"))
rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
z = next((r for r in rek if "KSeF" in json.dumps(r, ensure_ascii=False) and "moduł faktur" in json.dumps(r, ensure_ascii=False)), None)
opis = z.get("job_description", "")

PROMPT_WYCENIACZ = """Jesteś wyceniaczem. Na podstawie zlecenia oszacuj ile to jest warte (kwota projektu, zł netto) i ile dni.

Zasady:
- Szacuj realistycznie dla freelancera z AI, ale NIE zaniżaj - klient płaci za doświadczenie i ryzyko.
- Bierz pod uwagę wymagania klienta, zakres, technologie, ryzyko.
- Nie musisz podawać stawki godzinowej.

Zwróć TYLKO JSON:
{"kwota": <int>, "dni_od": <int>, "dni_do": <int>, "uzasadnienie": "1-2 zdania"}"""

PROMPT_REVIEWER = """Jesteś doświadczonym kontraktorem .NET/architektem, który ocenia cudzą wycenę. Widzisz zlecenie i wycenę.

Twoje zadanie: powiedzieć szczerze, czy cena jest ZA MAŁA, OK, czy ZA DUŻA.

Bądź konkretny. Jeśli za mała/duża - o ile i dlaczego. Jeśli OK - powiedz wprost i podaj widełki akceptacji.

Zasady:
- Klient płaci za doświadczenie, nie tylko za godziny.
- Weź pod uwagę wymagania (kolejki, idempotencja, monitoring = architektura, nie klepanie).
- Bądź brutalnie szczery, ale sprawiedliwy.

Zwróć TYLKO JSON:
{"werdykt": "ZA_MALA"/"OK"/"ZA_DUZA", "kwota_ocena": <int lub null>, "uzasadnienie": "2-3 zdania", "widełki_rynkowe": "od X do Y zł"}"""


def debata(tresc, max_rundy=4):
    print("=" * 70)
    print("DEBATA WYCENOWA")
    print("=" * 70)
    # Runda 0: wyceniacz
    odp = call_ai(PROMPT_WYCENIACZ, f"ZLECENIE:\n{tresc}", temperature=0.3, max_tokens=1000)
    prop = _wyciagnij_json_blok(odp or "", "X") or None
    # parsuj JSON (bez bloku)
    import re
    m = re.search(r"\{.*\}", odp or "", re.DOTALL)
    prop = json.loads(m.group(0)) if m else {"kwota": 6500, "dni_od": 13, "dni_do": 21, "uzasadnienie": "fallback"}
    print(f"[WYCENIACZ] {prop['kwota']} zł / {prop.get('dni_od')}-{prop.get('dni_do')} dni")
    print(f"   {prop.get('uzasadnienie','')}")

    historia = []
    for runda in range(1, max_rundy + 1):
        # Reviewer ocenia
        r_odp = call_ai(PROMPT_REVIEWER,
                        f"ZLECENIE:\n{tresc}\n\nWYCENA DO OCENY: {prop['kwota']} zł / {prop.get('dni_od')}-{prop.get('dni_do')} dni\nUZASADNIENIE WYCENIACZA: {prop.get('uzasadnienie','')}",
                        model="deepseek-v4-pro-nothink", temperature=0.3, max_tokens=1000)
        m = re.search(r"\{.*\}", r_odp or "", re.DOTALL)
        rev = json.loads(m.group(0)) if m else {"werdykt": "?", "uzasadnienie": "brak", "widełki_rynkowe": "?"}
        print(f"\n[REVIEWER r{runda}] {rev['werdykt']} | rynek: {rev.get('widełki_rynkowe','?')}")
        print(f"   {rev.get('uzasadnienie','')}")

        if rev["werdykt"] == "OK":
            print(f"\n>>> POROZUMIENIE po {runda} rundach: {prop['kwota']} zł")
            return prop, rev

        # Wyceniacz odpowiada na krytyke
        w_odp = call_ai(PROMPT_WYCENIACZ,
                        f"ZLECENIE:\n{tresc}\n\nTWOJA POPRZEDNIA WYCENA: {prop['kwota']} zł\n\nREVIEWER MÓWI: {rev['werdykt']} - {rev.get('uzasadnienie','')} (rynek: {rev.get('widełki_rynkowe','')})\n\nUstosunkuj się. Albo popraw wycenę, albo obroń swoją. Zwróć JSON.",
                        temperature=0.3, max_tokens=1000)
        m = re.search(r"\{.*\}", w_odp or "", re.DOTALL)
        nowy = json.loads(m.group(0)) if m else prop
        print(f"[WYCENIACZ r{runda}] -> {nowy['kwota']} zł | {nowy.get('uzasadnienie','')[:120]}")
        historia.append((prop['kwota'], rev['werdykt']))
        prop = nowy

    print(f"\n>>> BRAK POROZUMIENIA po {max_rundy} rundach. Ostatnia: {prop['kwota']} zł")
    return prop, None


debata(opis)
