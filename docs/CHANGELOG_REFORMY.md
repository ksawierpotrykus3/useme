# KRONIKA ZMIAN I MATRYCA ŚLEDZENIA SYSTEMU (CHANGELOG)
**Data:** 22 września 2026  
**Szczegółowy dokument inżynierski:** [`badania/strategia/04_rejestr_hipotez_i_falsyfikacji/03_kronika_zmian_i_matryca_sledzenia.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/strategia/04_rejestr_hipotez_i_falsyfikacji/03_kronika_zmian_i_matryca_sledzenia.md)

---

## Szybka Mapa Zmian (Co z czego wynika)

1. **Audyt 16 Przegranych Ofert (`01_audyt_16_przegranych_ofert.md`):**
   - Wykazał: 87.5% call spam, 81.2% „15 minut”, 56.2% „dwuosobowy zespół”, 0% podpisu wykonawcy.
   - Wdrożono w: [`prompts/kontekst/jak_pisac_oferty.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md) oraz [`agent_02a_opis_oferty.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) -> Całkowity zakaz szablonów, sytuacyjne CTA, podpis *„Pozdrawiam, Ksawier”*.

2. **Case Study Adriana (#144788 - 34k zł, `05_case_study_adrian_mental_health.md`):**
   - Klient chciał partnerstwa/udziałów; AI zaproponowało hybrydę ze stawką godzinową i zdobyło kontakt mailowy.
   - Wykazał regułę: budżety 50–250 zł na Useme to stawki godzinowe (PLN/h), nie cały projekt.
   - Wdrożono w: [`wycena_kalkulator.py`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py) i [`mechanika_wyceniania.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) -> Dekodowanie `budzet_jawny: 100` jako 100 zł/h (wycena 3000 zł zamiast 100 zł).

3. **Audyt Rynku 138 Zleceń & Matryca Tier (`02_analiza_rynku_138_zlecen.md`):**
   - Nisze ERP, KSeF, AI i scraping zaawansowany to wysokie marże. Niska stawka 90 zł/h wzbudzała nieufność klientów B2B.
   - Wdrożono w: [`wycena_kalkulator.py`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py) -> Stawka ekspercka Tier A (`140 zł/h`) oraz likwidacja dumpingu cenowego (KOREKTY min 1.0).
   - Wdrożono w: [`ai_pipeline.py`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py) -> Sortowanie priorytetowe kolejki (Tier A przed Tier B) przed wyczerpaniem limitu 21 ofert/dobę.

4. **Audyt Profilu Ksawiera (`03_audyt_profilu_ksawiera_i_bledy_bota.md`):**
   - Wstrzyknięto do [`prompts/kontekst/lore.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/lore.md) kompetencje z 9 projektów z portfolio i referencję Dominika Łyżwy (spokój, eliminacja ryzyk), przy twardym zakazie podawania surowych zewnętrznych linków dopóki nie zostaną w 100% dopracowane.

5. **Korekta po Audycie Red Teamu i Psychologii Sprzedaży (Refinement 22.09 wieczór):**
   - **Tandem 2 specjalistów:** Całkowite usunięcie korporacyjnych tytułów typu „Lead Architekt”. Działamy jako dwóch konkretnych inżynierów-praktyków (Ksawier i Maksymilian), co uwiarygadnia moce przerobowe bez udawania agencji.
   - **Interaktywne demo / Proof of Concept zamiast starych materiałów:** Zamiast obiecywać podsyłanie starych nagrań (często pod NDA lub niedostępnych dla danej niszy), AI może zaproponować postawienie szybkiego działającego dema / prototypu bezpośrednio pod problem klienta przed umową.
   - **Elastyczność budżetu 50–250 zł:** Zdjęcie sztywnego przymusu mnożenia godzin. AI kontekstowo decyduje, czy budżet to stawka godzinowa (projekt/stała współpraca), czy ryczałt za mikrozadanie.
   - **Architektura Multi-Konta:** Sparametryzowano podpisy w `config.py`, przygotowując silnik na bezpieczne wpięcie drugiego profilu w przyszłości.

6. **Audyt Audytów i Arbitraż Dialektyczny (Runda II - Raporty `06`, `07`, `08`, `09`):**
   - **Eliminacja efektu Nixona i dat z przeszłości:** Bezwzględny zakaz otwierania ofert zaprzeczeniami patologii (*„nie będę zawyżać godzin”*) oraz zakaz wklejania faktów z researchu z datą przeszłą (anachronizm Shopify 26 sierpnia w ofercie z 22 września).
   - **Segmentacja domenowa zamiast bid-riggingu:** Odrzucenie równoległego wysyłania 2 ofert na to samo zlecenie (ryzyko blokady Useme). Konto 1 (Ksawier) obsługuje wyłącznie zlecenia Tier A, a Konto 2 (Maksymilian) zlecenia Tier B i C.
   - **Prymat stawki Tier A w kalkulatorze:** Ochrona marży w zleceniach enterprise (`STAWKA_TIER_A = 140 zł/h` nie może zostać obniżona przez placeholder budżetu klienta np. 80 zł).
   - **Harmonizacja Walidatora 08:** Dodanie wyjątku w Regule 7 zezwalającego na stawkę godzinową i pakiet godzin w retainerach i ofertach hybrydowych.
   - **Veto dla Self-Healing Pricing:** Odrzucenie zamiatania błędów pod dywan; utrzymanie bezpiecznika `SANITY_BLOK` przy jednoczesnej eliminacji przyczyn spadku stawki w kalkulatorze.

7. **Czystka Szablonów i Odcięcie Starego Cache w `chain_executor.py`:**
   - **Zero Szablonów i Cytatów:** Wszystkie przykładowe zwroty i kalki zdań zostały bezwzględnie usunięte z promptów. Zastąpiono je czystymi regułami myślenia inżynierskiego i kryteriami oceny.
   - **Odcięcie zanieczyszczenia `ai_proposal` w `_slim_zlecenie`:** Naprawiono błąd architektoniczny w `chain_executor.py`, gdzie stara oferta sprzed reformy z 18 września była przekazywana do promptu AI jako część zlecenia z magazynu.
   - **Weryfikacja na żywo (#144590):** Model DeepSeek wygenerował ofertę o 100% autorskim charakterze, zaczynającą się od trafnej diagnozy migracji koszyka w Shopify (Checkout Extensibility vs checkout.liquid) i bloków checkoutowych WooCommerce, z precyzyjnym rozliczeniem 120 zł/h, bezpiecznikiem Demo Guard na danych testowych i podpisem Ksawier Potrykus.

8. **Aktualizacja Stawek Bazowych (100 zł/h) & Harmonizacja Walidatora 08:**
   - **Stawka Standardowa:** Przestawiono stawkę standardową (Tier B) z 90 na 100 zł/h netto (pasmo losowania 90–110 zł/h, offset +-10 zł) w [`wycena_kalkulator.py`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py) i [`mechanika_wyceniania.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md).
   - **Walidator 08:** W [`agent_08_weryfikacja_zasad.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) dopisano stawkę ekspercką Tier A (`140 zł/h`) do dozwolonych stawek, zaktualizowano przykłady i usunięto stary kwiatek chwalący „call na 15 minut”.

9. **Reforma Architektury i Higieny Projektu (Audyt Alpha & Beta):**
   - **Izolacja `marker.json`:** W [`storage.py`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/storage.py) powiązano `marker_file` z instancją magazynu. Testy z katalogiem tymczasowym zapisują marker lokalnie, eliminując zatruwanie produkcyjnego `marker.json`. Przywrócono autentyczny stan markera (#144836).
   - **Struktura `tests/` i `pytest.ini`:** Utworzono katalog [`tests/`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tests) i przeniesiono tam 13 modułów testowych (z unifikacją nazw `test_*.py`). Dodano [`pytest.ini`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/pytest.ini) z wykluczeniem `lab/`, `tech/`, `magazyn/`, `data/`.
   - **Optymalizacja czasu testów (Mockowanie `sleep`):** Zamockowano `time.sleep` w testach odporności i multi-konta, skracając czas wykonania pełnej baterii 40 testów z kilkunastu minut do **4.65 sekundy** (100% PASS).
   - **Porządki w badaniach i roocie:** Przeniesiono `analiza_przegranych.py` (zabezpieczone przez `main()`) oraz `przegrane_checkpoint.json` do katalogu [`dane_badania/`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/dane_badania). Usunięto 5 plików tymczasowych `.txt` z katalogu głównego.

---
Pełne szczegóły zmian, kody przed/po oraz raport testów znajdują się w pliku:  
👉 [`badania/strategia/04_rejestr_hipotez_i_falsyfikacji/03_kronika_zmian_i_matryca_sledzenia.md`](file:///C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/strategia/04_rejestr_hipotez_i_falsyfikacji/03_kronika_zmian_i_matryca_sledzenia.md)

