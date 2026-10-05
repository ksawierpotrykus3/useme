# -*- coding: utf-8 -*-
"""Test debaty na 3 zleceniach z wiedzą o braku 'stawki dziennej' i realiach Useme."""
import sys, json, re
from pathlib import Path
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai

PROMPT_WYCENIACZ = """Jesteś Ksawierem – polskim freelancerem IT na platformie Useme.
Rozliczasz się przez Useme (umowa o dzieło, bez firmy, bez pośredników, bez narzutu software house'u).
Pracujesz solo z zaawansowanym AI (piszesz kod i testy w kilka dni, a reszta terminu to wdrożenie, testy klienta i poprawki).

KRYTYCZNE ZASADY FREELANCINGU NA USEME:
1. NA USEME NIE MA CZEGOŚ TAKIEGO JAK 'STAWKA DZIENNA' (MAN-DAY)!
   - Termin w dniach (np. 21 dni czy 30 dni) to czas kalendarzowy projektu z buforem na kontakt i testy klienta, a NIE 30 dni pracy po 8 godzin! Z AI pracujesz wydajnie, nie rozliczasz roboczogodzin jak na etacie w korpo.
2. REALIA CENOWE POLSKICH KLIENTÓW MŚP NA USEME:
   - Polscy przedsiębiorcy na Useme szukają pojedynczego wykonawcy, który zrobi to taniej i sprawniej niż agencja.
   - Poniżej 3 000 - 4 000 zł to amatorski dumping (odrzucany przez mądrych klientów za brak powagi).
   - Złoty środek dla solidnego freelancera:
     * Integracje, automatyzacje n8n/Make, mostki Subiekt/BaseLinker: 5 000 – 12 000 zł.
     * Złożone wdrożenia ERP/OCR/Optima z wieloma dokumentami: 8 000 – 15 000 zł (15k to psychologiczna bariera dla MŚP).
     * Aplikacje mobilne / dedykowane systemy od zera: 10 000 – 22 000 zł.
   - Powyżej 25 000 - 30 000 zł klient MŚP zaczyna się wycofywać, a powyżej 35 000 zł uznaje to za ofertę z sufitu.

Oszacuj kwotę w PLN netto i termin w dniach.
Zwróć TYLKO JSON:
{"kwota": <int>, "dni": <int>, "uzasadnienie": "2 zdania: specyfika zlecenia i dlaczego taka kwota na Useme"}
"""

PROMPT_REVIEWER = """Jesteś bezwzględnym recenzentem – starym wyjadaczem z Useme, który widział setki wygranych i przegranych ofert.
Oceniasz wycenę freelancera pod kątem szansy na wygranie zlecenia u polskiego klienta MŚP.

PAMIĘTAJ:
1. NIE LICZ 'STAWEK DZIENNYCH'! To nie jest B2B body leasing w korporacji. Freelancer na Useme sprzedaje dowiezienie rezultatu w wyznaczonym terminie kalendarzowym.
2. W głowie klienta MŚP na Useme:
   - Powyżej 15 000 zł przy automatyzacji/ERP pojawia się silny opór (chyba że to gigantyczny system od zera).
   - Oferty powyżej 25 000 – 30 000 zł na Useme najczęściej przegrywają z ofertami za 10–18k zł od innych doświadczonych ludzi.
   - Z kolei 2 000 – 3 000 zł to podejrzany dumping studenta.

Oceń propozycję:
- "ZA_MALA" (dumping, strata marży, brak bufora na ryzyko).
- "ZA_DUZA" (przekroczenie budżetu psychologicznego MŚP na Useme, przegra z dobrą konkurencją za 10-15k).
- "OK" (maksymalna wysoka marża, która wciąż ma realną szansę wygrać).

Zwróć TYLKO JSON:
{"werdykt": "ZA_MALA" / "OK" / "ZA_DUZA", "kwota_sugerowana": <int>, "uzasadnienie": "2 zdania merytoryczne", "widełki_useme": "od X do Y zł"}
"""

def debata(nazwa, tresc, max_rundy=2):
    print(f"\n=======================================================")
    print(f"DEBATA: {nazwa}")
    print(f"=======================================================")
    odp = call_ai(PROMPT_WYCENIACZ, f"ZLECENIE:\n{tresc}", temperature=0.3, max_tokens=1000)
    m = re.search(r"\{.*\}", odp or "", re.DOTALL)
    prop = json.loads(m.group(0)) if m else {"kwota": 8000, "dni": 21, "uzasadnienie": "fallback"}
    print(f"[WYCENIACZ R0] {prop['kwota']} zł | {prop.get('dni')} dni")
    print(f"   Uzasadnienie: {prop.get('uzasadnienie')}")

    for runda in range(1, max_rundy + 1):
        r_odp = call_ai(PROMPT_REVIEWER,
                        f"ZLECENIE:\n{tresc}\n\nPROPOZYCJA: {prop['kwota']} zł / {prop.get('dni')} dni\nUZASADNIENIE: {prop.get('uzasadnienie')}",
                        temperature=0.3, max_tokens=1000)
        m = re.search(r"\{.*\}", r_odp or "", re.DOTALL)
        rev = json.loads(m.group(0)) if m else {"werdykt": "?", "uzasadnienie": "brak"}
        print(f"[REVIEWER R{runda}] {rev.get('werdykt')} (sugeruje: {rev.get('kwota_sugerowana')} zł, rynek: {rev.get('widełki_useme')})")
        print(f"   Uwagi: {rev.get('uzasadnienie')}")

        if rev.get("werdykt") == "OK":
            print(f">>> POROZUMIENIE: {prop['kwota']} zł / {prop.get('dni')} dni")
            return prop

        w_odp = call_ai(PROMPT_WYCENIACZ,
                        f"ZLECENIE:\n{tresc}\n\nPOPRZEDNIO: {prop['kwota']} zł\nREVIEWER: {rev.get('werdykt')} ({rev.get('uzasadnienie')}, sugeruje {rev.get('kwota_sugerowana')} zł).\nSkoryguj lub obroń. JSON:",
                        temperature=0.3, max_tokens=1000)
        m = re.search(r"\{.*\}", w_odp or "", re.DOTALL)
        if m: prop = json.loads(m.group(0))
        print(f"[WYCENIACZ R{runda}] -> {prop['kwota']} zł / {prop.get('dni')} dni")

    print(f">>> FINAŁ: {prop['kwota']} zł / {prop.get('dni')} dni")
    return prop

if __name__ == "__main__":
    root = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia")
    
    # 1. 145285 Subiekt
    z1 = json.loads((root / "145285" / "zlecenie.json").read_text(encoding="utf-8"))
    debata("145285 Subiekt <-> BaseLinker", z1.get("description") or z1.get("opis"))

    # 2. 145287 Mobilka
    z2 = json.loads((root / "145287" / "zlecenie.json").read_text(encoding="utf-8"))
    debata("145287 Aplikacja mobilna offline", z2.get("description") or z2.get("opis"))

    # 3. 144890 OCR Faktury
    z3 = json.loads((root / "zlecenie_testowe_144890" / "zlecenie.json").read_text(encoding="utf-8"))
    debata("144890 Automatyzacja faktur OCR", z3.get("description") or z3.get("opis"))
