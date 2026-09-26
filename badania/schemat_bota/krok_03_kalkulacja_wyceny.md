# KROK 3: Kalkulacja Wyceny i Terminu (Kalkulator Stawek i Reguły)

Moduł obliczający bezpieczną kwotę netto oraz liczbę dni roboczych zgodnie z polityką cenową Ksawiera i specyfiką Useme.

---

## 1. Reguły Podstawowe

Wycena jest deterministycznie wyliczana na podstawie reguł w [`kod/wycena_kalkulator.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py) oraz zaleceń w [`mechanika_wyceniania.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md):

1. **Stawka Godzinowa Bazowa**:
   - Stała i jedyna obowiązująca stawka wszędzie: **90 PLN / godzinę netto** (zarówno Tier A, jak i Tier B).
2. **Minimalny Czas Realizacji na Useme**:
   - **Zasada twarda: Minimum 7 dni**.
   - Deklarowanie w formularzu Useme terminu 1-2 dni rodzi ryzyko wpadnięcia w kary umowne przy jakimkolwiek opóźnieniu ze strony klienta (np. brak dostępu do FTP/API).
   - Nawet w przypadku zadania na 4 godziny pracy, w formularzu wpisujemy 7 dni (z adnotacją w tekście, że sam kod powstanie w 1 dzień, a pozostały czas to testy klienta).

---

## 2. Obsługa Budżetu Klienta

Kalkulator przetwarza pole budżetu ze zlecenia:
- **Budżet sztywny (np. 1500 PLN)**:
   - Bot wycenia pełny zakres zlecenia. Jeśli budżet klienta jest wyższy niż wyliczona cena bazowa, celuje w 85% budżetu klienta (z capem 1.4x ceny bazowej). Zakaz samowolnego dzielenia projektu na „Fazę 1 PoC za 800 zł" (Obalony Mit 6 — 0% konwersji); etapowanie dopuszczalne wyłącznie gdy klient wprost o to prosi w ogłoszeniu lub tak wycenia konkurencja.
- **Brak budżetu ("Do negocjacji" / "Brak kwoty")**:
  - Estymacja pracochłonności:
    * Zadania małe (skrypt, scraper, prosty webhook): 500 – 1 200 PLN (7 dni).
    * Zadania średnie (moduł sklepu, integracja ERP, aplikacja konsolowa): 1 500 – 3 500 PLN (10-14 dni).
    * Zadania duże (kompletny system dedykowany, aplikacja mobilna): 4 500 – 8 500 PLN (14-21 dni).
- **Budżety 50–250 PLN w zleceniach programistycznych**:
  - Dekodowane jako stawka godzinowa klienta (PLN/h) — kalkulator wycenia pełny zakres ze stałą stawką 90 PLN/h (lub jako mikrozadanie z minimum 500 PLN).

---

## 3. Deterministyczny Seed Per Oferta

W przypadku korzystania z trybu multi-account lub wariantowości, kalkulator wykorzystuje `stawka_seed = f"{job_id}-{konto_id}"`:
- Zapewnia spójny kontekst per konto i powtarzalność w testach regresyjnych przy zachowaniu stałej stawki 90 PLN/h.

---

## 4. Sanity Check Bezpieczeństwa

Przed zatwierdzeniem wyceny moduł weryfikuje:
- Czy kwota $\ge 500$ PLN oraz efektywna stawka godzinowa $\ge 85$ PLN/h.
- Czy liczba dni $\ge 7$.
- Jeśli kalkulator zgłosi anomalię (`sanity_ok = False`), zlecenie otrzymuje status `SANITY_BLOK` i nie zostaje wysłane w trybie live bez ręcznej autoryzacji.
