# -*- coding: utf-8 -*-
"""Test realistycznej debaty wycenowej na Useme.

Wyceniacz vs Reviewer z pełnym kontekstem:
- Freelancer solo na Useme (wspierany AI)
- Realia polskiego rynku MŚP na Useme (dane empiryczne z bazy: mediana 5-12k, sufit 25-45k)
- Zero stawek enterprise software house'u
"""
import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai

PROMPT_WYCENIACZ = """Jesteś Ksawierem – polskim freelancerem IT składającym ofertę na platformie Useme.
Rozliczasz się przez Useme (umowa o dzieło, bez pośredników i bez narzutu software house'u).
Pracujesz solo, wspomagany AI (piszesz kod i testy wielokrotnie szybciej niż tradycyjny zespół, ale bierzesz pełną odpowiedzialność inżynierską).

Twoim celem jest wycenić projekt tak, aby:
1. NIE ZANIŻAĆ ceny (żadnego dumpingu za 1000 zł jak amatorzy na Useme – klient płaci za spokój, architekturę i brak wtóp).
2. NIE ODLECIEC W KOSMOS (to jest Useme dla polskich firm MŚP, a nie przetarg korporacyjny w Warszawie dla banku za 150 000 zł).
Realne widełki dla zleceń na Useme dla top seniora z AI:
- Średnie integracje/automatyzacje/skrypty: 4 000 – 12 000 zł.
- Złożone systemy, trudny ERP/KSeF, cała aplikacja mobilna, autorski moduł OMS: 15 000 – 40 000 zł.
- Powyżej 45 000 zł klient na Useme natychmiast odrzuca ofertę jako absurdalną stawkę korpo-agencji.

Oszacuj realną kwotę (zł netto na Useme) oraz czas realizacji (dni kalendarzowe, min. 7 dni).

Zwróć WYŁĄCZNIE JSON:
{"kwota": <int>, "dni_od": <int>, "dni_do": <int>, "uzasadnienie": "2-3 konkretne zdania: dlaczego tyle dla freelancera z AI na Useme"}
"""

PROMPT_REVIEWER = """Jesteś bezwzględnym, doświadczonym freelancerem-mentorem z Useme. Znasz polski rynek, konkurencję i psychologię klientów na Useme od podszewki.
Oceniasz wycenę zaproponowaną przez drugiego freelancera.

Twoje kryteria oceny:
1. CZY TO REALNE DLA USEME? 
   - Jeśli cena jest powyżej 45 000 zł -> ZA_DUZA (klient ucieknie, to stawka agencji z biurem w szklanym wieżowcu, a nie freelancera na Useme).
   - Jeśli cena jest poniżej 5 000 zł przy złożonym systemie architektonicznym -> ZA_MALA (dumping, robienie z siebie taniej siły roboczej, brak marginesu na ryzyko).
2. ZŁOTY ŚRODEK (SWEET SPOT): Chcemy być w górnym kwartylu rynku Useme (klient widzi profesjonalizm, a my zarabiamy świetne pieniądze za czas pracy z AI), ale w granicach akceptowalności dla właściciela małej/średniej firmy.
3. DNI: Minimum 7 dni (wymóg Useme).

Werdykt:
- "ZA_MALA" (jeśli niedoszacował ryzyka lub zaniżył swoją wartość).
- "ZA_DUZA" (jeśli odleciał w stawki software house'u i odstraszy klienta Useme).
- "OK" (jeśli trafił w punkt: maksymalna marża, która wciąż ma realną szansę wygrać na Useme).

Zwróć WYŁĄCZNIE JSON:
{"werdykt": "ZA_MALA" / "OK" / "ZA_DUZA", "kwota_sugerowana": <int>, "uzasadnienie": "2-3 zdania bez owijania w bawełnę", "widełki_useme": "od X do Y zł"}
"""


def debata_useme(nazwa_zlecenia: str, tresc: str, max_rundy: int = 3):
    print("=" * 75)
    print(f"DEBATA WYCENOWA USEME: {nazwa_zlecenia}")
    print("=" * 75)

    # Runda 0: Wyceniacz
    odp = call_ai(PROMPT_WYCENIACZ, f"ZLECENIE KLIENTA NA USEME:\n{tresc}", temperature=0.3, max_tokens=1000)
    m = re.search(r"\{.*\}", odp or "", re.DOTALL)
    prop = json.loads(m.group(0)) if m else {"kwota": 10000, "dni_od": 14, "dni_do": 21, "uzasadnienie": "fallback"}
    print(f"[WYCENIACZ Start] {prop['kwota']} zł | {prop.get('dni_od')}-{prop.get('dni_do')} dni")
    print(f"   Uzasadnienie: {prop.get('uzasadnienie','')}\n")

    for runda in range(1, max_rundy + 1):
        # Reviewer ocenia
        r_odp = call_ai(
            PROMPT_REVIEWER,
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\nPROPOZYCJA WYCENIACZA: {prop['kwota']} zł netto | {prop.get('dni_od')}-{prop.get('dni_do')} dni\nUZASADNIENIE: {prop.get('uzasadnienie','')}",
            temperature=0.3, max_tokens=1000
        )
        m = re.search(r"\{.*\}", r_odp or "", re.DOTALL)
        rev = json.loads(m.group(0)) if m else {"werdykt": "?", "uzasadnienie": "brak", "widełki_useme": "?"}
        print(f"[REVIEWER Runda {runda}] Werdykt: {rev['werdykt']} (sugeruje: {rev.get('kwota_sugerowana')} zł, rynek: {rev.get('widełki_useme')})")
        print(f"   Krytyka: {rev.get('uzasadnienie','')}\n")

        if rev.get("werdykt") == "OK":
            print(f">>> [SUKCES] POROZUMIENIE OSIĄGNIĘTE W RUNDZIE {runda}!")
            print(f">>> FINALNA CENA: {prop['kwota']} zł netto | {prop.get('dni_od')}-{prop.get('dni_do')} dni")
            print("=" * 75 + "\n")
            return prop

        # Wyceniacz reaguje na krytykę
        w_odp = call_ai(
            PROMPT_WYCENIACZ,
            f"ZLECENIE KLIENTA NA USEME:\n{tresc}\n\nTWOJA POPRZEDNIA PROPOZYCJA: {prop['kwota']} zł\n"
            f"MENTOR Z USEME OCENIŁ: {rev['werdykt']}. Sugeruje: {rev.get('kwota_sugerowana')} zł (widełki Useme: {rev.get('widełki_useme')}).\n"
            f"Uwagi mentora: {rev.get('uzasadnienie','')}\n\n"
            f"Skoryguj wycenę lub obroń swoje stanowisko z uwzględnieniem realiów Useme. Zwróć JSON.",
            temperature=0.3, max_tokens=1000
        )
        m = re.search(r"\{.*\}", w_odp or "", re.DOTALL)
        if m:
            prop = json.loads(m.group(0))
        print(f"[WYCENIACZ Runda {runda} Kontra] -> {prop['kwota']} zł | {prop.get('dni_od')}-{prop.get('dni_do')} dni")
        print(f"   Uzasadnienie: {prop.get('uzasadnienie','')}\n")

    print(f">>> [KONIEC DEBATY] Ostateczna kompromisowa wycena: {prop['kwota']} zł")
    print("=" * 75 + "\n")
    return prop


if __name__ == "__main__":
    # Test 1: Zlecenie KSeF / OMS .NET (#145290)
    base_ksef = Path("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
    if base_ksef.exists():
        dane = json.loads(base_ksef.read_text(encoding="utf-8"))
        rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
        z1 = next((r for r in rek if "KSeF" in json.dumps(r, ensure_ascii=False) and "moduł faktur" in json.dumps(r, ensure_ascii=False)), None)
        if z1:
            debata_useme("145290 - KSeF moduł faktur OMS (.NET)", z1.get("job_description", ""))

    # Test 2: Zlecenie #145285 - Subiekt <-> BaseLinker (z bazy moje_zlecenia)
    z2_file = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia/145285/zlecenie.json")
    if z2_file.exists():
        z2 = json.loads(z2_file.read_text(encoding="utf-8"))
        debata_useme("145285 - Subiekt <-> BaseLinker integracja", z2.get("description", z2.get("opis", "")))
