# -*- coding: utf-8 -*-
"""Wycena debaty wieloagentowej (Adversarial Pricing Debate) dla Useme.

Zastępuje sztywny kalkulator godzinowy (90 zł/h).
Wyceniacz (freelancer solo z AI) vs Reviewer (wyjadacz z Useme)
dyskutują o wartości biznesowej, ryzyku i granicach budżetowych MŚP,
aż dojdą do porozumienia.

Deterministyczny wrapper na końcu dba o zaokrąglenie psychologiczne i twarde limity Useme.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, Optional

PROMPT_WYCENIACZ = """Jesteś Ksawierem – polskim freelancerem IT na platformie Useme.
Rozliczasz się przez Useme (umowa o dzieło, bez firmy, bez pośredników, bez narzutu software house'u).
Pracujesz solo z zaawansowanym AI (piszesz kod i testy w kilka dni, a reszta terminu to wdrożenie, testy klienta i poprawki).

KRYTYCZNE ZASADY FREELANCINGU NA USEME:
1. NA USEME NIE MA CZEGOŚ TAKIEGO JAK 'STAWKA DZIENNA' (MAN-DAY)!
   - Termin w dniach (np. 21 dni czy 30 dni) to czas kalendarzowy projektu z buforem na kontakt i testy klienta, a NIE 30 dni pracy po 8 godzin! Z AI pracujesz wydajnie, nie rozliczasz roboczogodzin jak na etacie w korpo.
2. REALIA CENOWE POLSKICH KLIENTÓW MŚP NA USEME:
   - Polscy przedsiębiorcy na Useme szukają pojedynczego wykonawcy, który zrobi to taniej i sprawniej niż agencja.
   - Poniżej 3 000 - 4 000 zł to amatorski dumping (odrzucany przez mądrych klientów za brak powagi), chyba że to drobne mikrozadanie na pół godziny (wtedy 500-1500 zł).
   - Złoty środek dla solidnego freelancera na Useme:
     * Integracje, automatyzacje n8n/Make, mostki Subiekt/BaseLinker: 5 000 – 14 000 zł.
     * Złożone wdrożenia ERP/OCR/Optima z wieloma dokumentami: 8 000 – 16 000 zł (15k to psychologiczna bariera dla wielu MŚP).
     * Aplikacje mobilne / dedykowane systemy od zera: 12 000 – 25 000 zł.
     * Stała współpraca / retainer: 1 500 – 3 500 zł miesięcznie.
   - Powyżej 25 000 - 30 000 zł klient MŚP zaczyna się wycofywać, a powyżej 40 000 zł uznaje to za ofertę z sufitu od agencji.
3. KOTWICA BUDŻETU JAWNEGO:
   - Jeśli klient podał budżet 50–250 zł (np. 100 zł), to najczęściej preferowana stawka godzinowa klienta, a nie budżet całości! Wyceniaj całość normalnie.
   - Jeśli klient podał jawny budżet całkowity (np. 10 000 zł), dopasuj się do niego (np. 80-90% budżetu), jeśli jest realistyczny.

Oszacuj kwotę w PLN netto oraz termin w dniach kalendarzowych (od-do, min. 7 dni).
Zwróć WYŁĄCZNIE JSON:
{
  "kwota": <int>,
  "dni_od": <int>,
  "dni_do": <int>,
  "typ": "projekt" lub "male" lub "retainer",
  "uzasadnienie": "2 zdania: specyfika zadania i dlaczego taka kwota na Useme"
}
"""

PROMPT_REVIEWER = """Jesteś bezwzględnym recenzentem – starym wyjadaczem z Useme, który widział setki wygranych i przegranych ofert.
Oceniasz wycenę freelancera pod kątem szansy na wygranie zlecenia u polskiego klienta MŚP.

PAMIĘTAJ:
1. NIE LICZ 'STAWEK DZIENNYCH'! To nie jest B2B body leasing w korporacji. Freelancer na Useme sprzedaje dowiezienie rezultatu w wyznaczonym terminie kalendarzowym.
2. W głowie klienta MŚP na Useme:
   - Powyżej 15 000 zł przy automatyzacji/ERP pojawia się silny opór (chyba że to duży system od zera).
   - Oferty powyżej 25 000 – 30 000 zł na Useme najczęściej przegrywają z ofertami za 10–18k zł od innych doświadczonych ludzi.
   - Z kolei 2 000 – 3 000 zł to podejrzany dumping studenta przy zaawansowanym systemie.

Oceń propozycję:
- "ZA_MALA" (dumping, strata marży, brak bufora na ryzyko).
- "ZA_DUZA" (przekroczenie budżetu psychologicznego MŚP na Useme, przegra z dobrą konkurencją za 10-15k).
- "OK" (maksymalna wysoka marża, która wciąż ma realną szansę wygrać).

Zwróć WYŁĄCZNIE JSON:
{
  "werdykt": "ZA_MALA" lub "OK" lub "ZA_DUZA",
  "kwota_sugerowana": <int>,
  "dni_sugerowane_do": <int>,
  "uzasadnienie": "2 zdania merytoryczne bez owijania w bawełnę",
  "widełki_useme": "od X do Y zł"
}
"""


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


def _zaokraglij_psychologicznie(kwota: int) -> int:
    """Zaokrąglenie cenowe pod psychologię klienta Useme."""
    if kwota <= 2000:
        return int(round(kwota / 50.0) * 50)
    if kwota <= 10000:
        return int(round(kwota / 500.0) * 500)
    return int(round(kwota / 1000.0) * 1000)


def wycen_przez_debate(
    tresc_zlecenia: str,
    dziennik: str = "",
    research: str = "",
    call_ai_fn: Optional[Callable] = None,
    say: Optional[Callable[[str], None]] = None,
    max_rundy: int = 2,
) -> Dict[str, Any]:
    """Przeprowadza debatę wieloagentową między Wyceniaczem a Reviewerem Useme.

    Zwraca ustrukturyzowany wynik wyceny gotowy do wstrzyknięcia do oferty.
    """
    if say is None:
        say = lambda msg: None

    if call_ai_fn is None:
        # Fallback lokalny import
        from brain import call_ai
        call_ai_fn = call_ai

    say("    debata wycenowa: Wyceniacz analizuje zlecenie...")

    kontekst_wejsciowy = (
        f"ZLECENIE KLIENTA:\n{tresc_zlecenia}\n\n"
        f"DZIENNIK MYŚLENIA:\n{dziennik or 'Brak'}\n\n"
        f"RESEARCH DOWODOWY:\n{research or 'Brak'}"
    )

    # Runda 0: Wyceniacz
    odp_w0 = call_ai_fn(PROMPT_WYCENIACZ, kontekst_wejsciowy, temperature=0.3, max_tokens=1000)
    prop = _parsuj_json(odp_w0) or {
        "kwota": 6000,
        "dni_od": 14,
        "dni_do": 21,
        "typ": "projekt",
        "uzasadnienie": "Standardowa realizacja freelancerska z AI.",
    }

    kwota_start = prop.get("kwota", 6000)
    dni_od_start = prop.get("dni_od", 14)
    dni_do_start = prop.get("dni_do", 21)
    say(f"    [Wyceniacz R0] {kwota_start} zł / {dni_od_start}-{dni_do_start} dni ({prop.get('uzasadnienie', '')[:70]}...)")

    rev: Dict[str, Any] = {"werdykt": "OK"}
    wynegocjowane_w_rundzie = 0

    for runda in range(1, max_rundy + 1):
        prompt_rev_usr = (
            f"{kontekst_wejsciowy}\n\n"
            f"--- AKTUALNA PROPOZYCJA WYCENIACZA ---\n"
            f"KWOTA: {prop.get('kwota')} zł netto\n"
            f"TERMIN: {prop.get('dni_od')}-{prop.get('dni_do')} dni kalendarzowych\n"
            f"TYP: {prop.get('typ', 'projekt')}\n"
            f"UZASADNIENIE: {prop.get('uzasadnienie', '')}\n\n"
            f"Oceń tę propozycję bezlitośnie pod kątem realiów Useme."
        )

        odp_r = call_ai_fn(PROMPT_REVIEWER, prompt_rev_usr, temperature=0.3, max_tokens=1000)
        rev = _parsuj_json(odp_r) or {"werdykt": "OK", "uzasadnienie": "Wycena akceptowalna."}
        werdykt = str(rev.get("werdykt", "OK")).upper()

        say(f"    [Reviewer R{runda}] {werdykt} (sugeruje: {rev.get('kwota_sugerowana')} zł, rynek: {rev.get('widełki_useme', '?')})")

        if werdykt == "OK":
            wynegocjowane_w_rundzie = runda
            break

        # Wyceniacz odpowiada na krytykę
        prompt_w_kontra = (
            f"{kontekst_wejsciowy}\n\n"
            f"TWOJA POPRZEDNIA PROPOZYCJA: {prop.get('kwota')} zł / {prop.get('dni_od')}-{prop.get('dni_do')} dni.\n"
            f"RECENZENT Z USEME MÓWI: {werdykt}\n"
            f"KRYTYKA RECENZENTA: {rev.get('uzasadnienie', '')}\n"
            f"SUGESTIA RECENZENTA: {rev.get('kwota_sugerowana')} zł, widełki: {rev.get('widełki_useme', '')}\n\n"
            f"Ustosunkuj się merytorycznie. Skoryguj wycenę lub obroń swoje racje. Zwróć JSON."
        )

        odp_w = call_ai_fn(PROMPT_WYCENIACZ, prompt_w_kontra, temperature=0.3, max_tokens=1000)
        nowy_prop = _parsuj_json(odp_w)
        if nowy_prop:
            prop = nowy_prop
            say(f"    [Wyceniacz R{runda} Kontra] -> {prop.get('kwota')} zł / {prop.get('dni_od')}-{prop.get('dni_do')} dni")
        wynegocjowane_w_rundzie = runda

    # --- DETERMINISTYCZNY GUARDRAIL (twarde wymogi Useme) ---
    surowa_kwota = int(prop.get("kwota") or 3000)
    kwota = _zaokraglij_psychologicznie(max(surowa_kwota, 500))

    dni_do = int(prop.get("dni_do") or prop.get("dni") or 21)
    dni_od = int(prop.get("dni_od") or max(7, dni_do - 7))
    dni_do = max(dni_do, 7)
    dni_od = max(min(dni_od, dni_do), 7)

    typ = prop.get("typ") or "projekt"
    say(f"    -> [Finał Debaty] {kwota} zł / {dni_od}-{dni_do} dni (zaokrąglono, Useme ready)")

    return {
        "kwota": kwota,
        "dni": dni_do,
        "dni_od": dni_od,
        "dni_do": dni_do,
        "typ": typ,
        "uzasadnienie": prop.get("uzasadnienie", ""),
        "reviewer_werdykt": rev.get("werdykt", "OK"),
        "reviewer_uwagi": rev.get("uzasadnienie", ""),
        "widełki_rynkowe": rev.get("widełki_useme", ""),
        "rundy": wynegocjowane_w_rundzie,
        "rozbicie": {
            "tryb": "debata_useme",
            "surowa_kwota_ai": surowa_kwota,
            "kwota_koncowa": kwota,
            "dni_od": dni_od,
            "dni_do": dni_do,
            "rundy_debaty": wynegocjowane_w_rundzie,
            "uzasadnienie_wyceniacza": prop.get("uzasadnienie", ""),
            "krytyka_reviewera": rev.get("uzasadnienie", ""),
            "widełki_rynkowe": rev.get("widełki_useme", ""),
        },
    }
