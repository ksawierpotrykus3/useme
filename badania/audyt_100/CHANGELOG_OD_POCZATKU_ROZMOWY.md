# Pełny Changelog Zmian w Ofertowarce (`useme_core`) — Od Początku Rozmowy (2026-09-26)

Ten dokument stanowi kompletny, chronologiczny rejestr **wszystkich zmian w kodzie, promptach, kalkulatorze wycen, kartach wiedzy, portfolio oraz testach**, wprowadzonych od początku sesji z dnia `2026-09-26`, wraz z wykazem zarchiwizowanych logów i wyników 27 przetestowanych ofert.

---

## 0. Gdzie Zapisane Są Wszystkie Logi, Oferty i Wyniki?

Wszystkie dane z całej sesji zostały trwale zapisane bezpośrednio w repozytorium projektu w katalogu [`badania/audyt_100/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/):

1. **[`badania/audyt_100/audyt_100_wyniki_27_ofert.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/audyt_100_wyniki_27_ofert.json)** — pełna baza JSON wszystkich **27 przetestowanych zleceń z magazynu** (Fale 1–5): treść oferty z Rundy 1 (Zero-Shot), pełna punktacja `1–100 pkt` w 5 kategoriach (`A–E`), wszystkie powody dodania punktów (`za_co_dodano`) i odjęcia punktów z cytatami (`za_co_odjeto`), wycena kalkulatora (`wycena_raw`) oraz treść i ocena z Rundy 2 / Rundy 3.
2. **[`badania/audyt_100/PELNE_LOGI_27_OFERT_RUNDA1_I_RUNDA2.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/PELNE_LOGI_27_OFERT_RUNDA1_I_RUNDA2.md)** — czytelne archiwum Markdown zawierające pełne teksty wszystkich 27 ofert (Runda 1 i Runda 2) oraz każdy pojedynczy log `[+]` / `[-]` Sędziego.
3. **[`badania/audyt_100/logi_i_skrypty/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/logi_i_skrypty/)** — **33 pliki surowe**: wszystkie logi konsolowe z wykonania zadań (`task-*.log`) oraz wszystkie skrypty uruchomieniowe fal (`run_audyt_wave1`..`wave5.py`).
4. **[`badania/audyt_100/artefakty_sesji/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/artefakty_sesji/)** — kopie wszystkich 4 raportów analitycznych powstałych w trakcie rozmowy:
   - `analiza_bota.md` (audyt pierwotnego stanu bota)
   - `strategia_vs_bot.md` (zderzenie starego bota z wynikami badań 406 zleceń i teoriami Useme)
   - `plan_wdrozenia.md` (plan przebudowy architektury)
   - `porownanie_ofert_live_z_elita.md` (raport porównawczy i tabela wyników 27 ofert `1–100 pkt`)

---

## 1. Chronologiczny Changelog Wszystkich Zmian w Ofertowarce (Etapy 1–7)

### Etap 1: Triage Wielowarstwowy (`A / B / C / REJECT`), Filtr Czerwonego Oceanu i Phantom Leads
* **Problem wyjściowy:** Stary bot traktował selekcję binarnie (`TAK/NIE`), przepuszczał proste zlecenia WordPress/Elementor/PrestaShop/SEO (gdzie jest 35–150 ofert i stawki 200 zł) oraz nie rozpoznawał wizjonerskich ogłoszeń bez budżetu (`PHANTOM`) ani klientów ratunkowych (`RESCUE`).
* **Zmodyfikowane pliki:**
  1. **[`kod/config.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/config.py)**:
     - Dodano `HARD_REJECT_PATTERNS` (automatyczny odrzut prostych stron WordPress, Elementor, WooCommerce wizytówek, PrestaShop szablonów, prostego CSS/HTML, SEO/copywritingu, grafiki/Canva, reklam Ads).
     - Dodano `PHANTOM_PATTERNS` (wykrywanie klonów gigantów, rozmytych „systemów AI od wszystkiego”, obietnic „długofalowej współpracy przy niskiej cenie na start”).
  2. **[`kod/prompts/kontekst/selekcja_zlecen.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/selekcja_zlecen.md)** oraz **[`kod/prompts/generatory/prompt_ai1.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/prompt_ai1.md)**:
     - Zastąpiono płaski wybór `TAK/NIE` strukturą klasyfikacji strategicznej: `tier` (`A / B / C / REJECT`), `sciezka` (`inzynieria` vs `biznes`), `typ_klienta` (6 archetypów), `karta_tech` (`tech_01`–`tech_16`) oraz `modyfikatory` (`RESCUE`, `DELEGOWANY`, `PHANTOM`).
  3. **[`kod/ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py)** oraz **[`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py)**:
     - Dodano deterministyczny pre-filtr regexowy (`HARD_REJECT_PATTERNS` / `PHANTOM_PATTERNS`) przed wywołaniem AI.
     - Rozszerzono parser odpowiedzi AI1 o pola `tier`, `sciezka`, `typ_klienta`, `karta_tech`, `modyfikatory` i przekazano je wprost do `chain_executor.py`.

---

### Etap 2: Architektura Dual-Track (`inzynieria` vs `biznes`) oraz 9 Scenariuszy Psychologicznych Klienta
* **Problem wyjściowy:** Stary bot pisał jednym głosem do każdego klienta — zasypywał nietechnicznych właścicieli firm (`tech_agnostic`) żargonem IT (`FastAPI`, `Redlock`, `SQLCipher`), a u CTO/programistów (`ekspert_dziedzinowy`) brzmiał zbyt ogólnikowo.
* **Utworzone i zmodyfikowane pliki w [`kod/prompts/kontekst/scenariusze/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/scenariusze/):**
  1. **`klient_01_tradycyjne_msp_erp_przemysl.md`** (`msp_erp`): Fokus na ciągłość ruchu, niełamanie licencji producenta ERP (zakaz bezpośrednich zapisów `INSERT/UPDATE` do tabel `CDN` / `Subiekt`), pracę na kopii bazy i bufor wyjątków dla operatora.
  2. **`klient_02_ecommerce_merchant.md`** (`ecommerce`): Fokus na ochronę aktywnej sprzedaży (zero oversellingu, kolejki webhooków, dry-run przed produkcją, ochrona konwersji).
  3. **`klient_03_agencja_software_house.md`** (`agencja`): Fokus na white-label, pracę na branchach i PR-ach, przejrzysty kod bez długu technicznego i dotrzymanie SLA wobec klienta końcowego agencji.
  4. **`klient_04_ekspert_dziedzinowy_uslugi.md`** (`ekspert_dziedzinowy`): Fokus na twardy konkret architektoniczny w pierwszych 2 zdaniach, odporność na wyścigi (race conditions) i partnerską komunikację inżynierską.
  5. **`klient_05_tech_agnostic_biznes.md`** (`tech_agnostic`): Fokus na efekt operacyjny (oszczędność czasu, eliminację błędów ręcznego przepisywania), **całkowity zakaz żargonu IT niewymienionego przez klienta**, gwarancję autonomicznego działania systemu i wideo-instrukcję po wdrożeniu.
  6. **`klient_06_quick_fix_awaria_hobbysta.md`** (`quick_fix`): Fokus na ultra-zwięzłą diagnozę przyczyny źródłowej (`65–105 słów`), pełny backup przed dotknięciem plików i szybki czas reakcji.
  7. **`modyfikator_rescue_klient_sparzony.md`** (`RESCUE`): Zakaz krytykowania poprzedniego wykonawcy i zakaz proponowania „przepisania wszystkiego od zera”; nacisk na audyt zastanego kodu na kopii i chirurgię wąskiego gardła.
  8. **`modyfikator_delegowany_pracownik.md`** (`DELEGOWANY`): Dostarczenie gotowych argumentów do obrony wyceny przed zarządem (TCO, porównanie kosztów licencji chmurowych vs self-hosted, bezpieczeństwo danych i faktura Useme).
  9. **`modyfikator_phantom_startup_wizjoner.md`** (`PHANTOM`): Uziemienie rozdmuchanego zakresu, wycena pełnej architektury bez sztucznych widełek oraz pytanie CTA zmuszające klienta do priorytetyzacji najważniejszego wąskiego gardła biznesowego.

---

### Etap 3: Naprawa Scraperów Useme i Kalibracja Kalkulatora Wyceny (`90 zł/h` + `MAX_RISK_MULTIPLIER = 1.15`)
* **Problem wyjściowy:**
  1. Scrapery `pobierz_oferty_zleceniodawcy.py` i `pobierz_wszystkie_wiadomosci.py` pobierały tylko 1 stronę i gubiły budżety przez nieaktualny selektor CSS.
  2. Kiedy pobraliśmy wszystkie **30 żywych ofert konkurencji** ze zlecenia `#144890` (`Comarch Optima + AI OCR`), okazało się, że stary kalkulator wycenił to zlecenie na **`17 500 zł / 36 dni`**, bo pomnożył `1.3 (ERP) * 1.25 (złożoność) = 1.625x` na 92 godzinach — podczas gdy elita wykonawców na tym zleceniu wyceniała je na **`7 500 – 9 800 zł`**.
* **Zmodyfikowane pliki:**
  1. **[`kod/pobierz_oferty_zleceniodawcy.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/pobierz_oferty_zleceniodawcy.py)** i **[`kod/pobierz_wszystkie_wiadomosci.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/pobierz_wszystkie_wiadomosci.py)**:
     - Naprawiono paginację wielostronicową oraz ekstrakcję budżetu i opisów ze struktury DOM Useme.
  2. **[`kod/wycena_kalkulator.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py)**:
     - Utrzymano **sztywną stawkę bazową `STAWKA_BAZOWA = 90` (`90 zł/h`)** w całym systemie.
     - Zastąpiono kaskadowe mnożenie ryzyk (`1.3 * 1.25 = 1.625`) funkcją `max()` z twardym sufitem **`MAX_RISK_MULTIPLIER = 1.15`** (obniżono mnożniki: `integracja_erp_legacy = 1.15`, `niestabilne_zewnetrzne_api = 1.12`, `brak_dokumentacji = 1.12`, `wysoka_zlozonosc = 1.10`).
     - Obniżono minimalny próg dni `DNI_MIN` z `7` na **`3 dni`** dla małych zleceń (`< 2 500 zł`).
  3. **[`kod/prompts/generatory/agent_02b_wycena_dni.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md)** oraz **[`kod/prompts/kontekst/mechanika_wyceniania.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md)**:
     - Dodano **Zasadę Zespołu 2-Osobowego (Ksawier + Maksymilian)**: zakaz sztucznego pompowania godzin pojedynczych modułów powyżej `14–18h` i nakaz trzymania sumy godzin realnego MVP w przedziale `45–75h` dla średnich/dużych integracji (co z buforem daje konkurencyjne rynkowo `6 000 – 9 800 zł` zamiast `17 500 zł`).

---

### Etap 4: Dynamiczny Selektor 16 Kart Wiedzy (`tech_01`–`tech_16`) i Rozbudowa Bazy Wiedzy
* **Problem wyjściowy:** Stary `chain_executor.py` nie wstrzykiwał do generatora `02a` i kalkulatora `02b` kart technologicznych z `badania/analizy/technologie/baza_wiedzy/`, a dla klientów nietechnicznych (`sciezka: biznes`) brakowało dedykowanej karty tłumaczącej problemy IT na język operacyjny właściciela firmy.
* **Utworzone i zmodyfikowane pliki:**
  1. **[`badania/analizy/technologie/baza_wiedzy/tech_16_tech_agnostic_biznes.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/technologie/baza_wiedzy/tech_16_tech_agnostic_biznes.md)** *(NOWY PLIK)*:
     - Karta nr 16 dla zleceń `tech_agnostic` / `sciezka: biznes`: słownik translacji żargonu technicznego na język korzyści i ryzyk biznesowych oraz 7 życiowych domen brzegowych (produkcja mebli na wymiar z mieszaniem `cm/mm`, poczta i faktury PDF vs skany, telefonia CloudTalk -> Notion z duplikatami i nagraniami RODO, automatyzacja wideo Social Media z blokadami kont, arkusze Google Sheets z nadpisywaniem formuł przez pracowników).
  2. **[`badania/analizy/technologie/baza_wiedzy/tech_02_comarch_optima_ksef.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/technologie/baza_wiedzy/tech_02_comarch_optima_ksef.md)**:
     - Dodano sekcję **`B2. Comarch ERP XL (API XL / Moduł Procesy / Dokumenty WZ -> FS)`**: różnice między Optimą a XL, osobna licencja serwerowa na moduł `Procesy` w kluczu `HASP/Sentinel`, idempotencja na relacji `TrN_ZaNId` (`CDN.TraNag`), kolejka błędów przy blokadzie limitu kredytowego kontrahenta oraz walidacja KSeF `FA(3)` (`0 KR / 0 WDT / 0 EX`).
  3. **[`kod/chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py)**:
     - Dodano `TECH_CARD_MAP` (`tech_01`–`tech_16`), `_TECH_KEYWORDS` oraz `_resolve_tech_cards(zlecenie, slot_id)` automatycznie dobierające do 2 najtrafniejszych kart wiedzy dla każdego zlecenia.
     - Dodano `_format_tech_card_for_slot(card_key, slot_id)` — inteligentny ekstraktor, który dla `02a` wycina tabele wycen wielowariantowych (żeby model nie kopiował wariantów cenowych do oferty!) i zamienia tabele Markdown na czysty tekst, a dla `02b` dostarcza architekturę modułową bez kwot PLN.
     - Dodano deterministyczną sanitację wyjścia `02a` (usuwanie długich pauz `—`/`–`, gwiazdek `**`, etykiet `Pytanie kwalifikujące:`, `Kluczowa mina:`, `Najdroższa mina:`, słowa-wytrychu `kompleksowego` oraz zwrotu `według mojej wiedzy`).

---

### Etap 5: Przebudowa Generatora Ofert (`agent_02a`), Portfolio (`portfolio_baza.md`), Lore (`lore.md`) i Walidatora (`agent_08`)
* **Problem wyjściowy:** Oferty starego bota miały sztywne szablony (*„wdrażaliśmy u producenta mebli...”* wklejane do każdego zlecenia), darmowe konsultacje („prześlij 1–2 pliki przed umową”), brak twardych dowodów dla części technologii (mobile, PHP/MSSQL/WAPRO, GTM/GA4, Comarch XL) lub przekraczały limit słów.
* **Zmodyfikowane pliki:**
  1. **[`kod/prompts/generatory/agent_02a_opis_oferty.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)**:
     - Wprowadzono strukturę **4 zwięzłych akapitów**:
       1. *Akapit 1 (Killshot w pierwszych 2 zdaniach)*: Diagnoza 1–2 ukrytych min produkcyjnych i konkretny mechanizm rozwiązania.
       2. *Akapit 2 (Architektura + 100% pokrycia modułów klienta + Sandbox-First + 1 twardy dowód z `portfolio_baza.md`)*: Nazwanie każdego modułu/widoku wymienionego przez klienta w ogłoszeniu, odpowiedź na jawne punkty *„W odpowiedzi podaj...”*, praca na kopii bazy i gwarancja autonomicznego działania + wideo-instrukcja.
       3. *Akapit 3 (Pytanie Kwalifikujące CTA)*: 1–2 krótkie pytania w osobnej linii przed wyceną (bez etykiet i bez numeracji; na ścieżce `biznes` / `PHANTOM` pytanie o priorytetyzację biznesową i format danych).
       4. *Akapit 4 (Wycena, OPEX, Gwarancja 30 dni i Podpis)*: Jedna kwota netto zgodna z `[WYNIK_KONCOWY]`, szacunkowy koszt utrzymania/tokenów API (gdy klient o to pyta), 30 dni gwarancji na własny kod i imienny podpis (`Ksawier Potrykus`).
     - Skalibrowano limity długości: **`75–105 słów`** (twardy limit `110 słów`) dla małych zleceń `< 3 000 zł` oraz **`145–195 słów`** (twardy limit `205 słów`) dla większych projektów `>= 3 000 zł`.
     - Zakazano negatywnych disclaimerów (*„Nie mamy wprost wdrożenia X, ale...”*) oraz języka niepewności (*„według mojej wiedzy”*).
  2. **[`kod/prompts/kontekst/portfolio_baza.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/portfolio_baza.md)**:
     - Rozbudowano **`Projekt 1`** o wdrożenie `Comarch ERP XL 2023.x` (automat FS z WZ w module `Procesy`, `45 WZ/dzień`, redukcja duplikatów do `0`).
     - Rozbudowano **`Projekt 2`** o skalę wielomagazynową (`3 magazyny, ponad 12 000 SKU` w Centrum Budowlanym Kołcz oraz `Shopify Locations` w Gardd Shopify B2B).
     - Dodano **`Projekt 4B`** (Maszyny CNC, postprocesory G-code LVD/ADTECH, budowa własnej maszyny CNC w zespole, normalizacja wymiarów `cm -> mm` dla stolarni).
     - Dodano **`Projekt 8`** (Aplikacje mobilne Offline-First `SQLCipher`, przejęcia legacy Kotlin/Android `AsyncTask -> Coroutines/WorkManager`, `foregroundServiceType="location"` pod Android 14/15 oraz subskrypcje B2B `StoreKit 2 / Google Play Billing / RevenueCat`).
     - Dodano **`Projekt 9`** (Przejęcia sklepów B2B `PHP/MySQL + WAPRO MAG / MSSQL`, optymalizacja procedur składowanych T-SQL, własny atomowy scheduler `UPDATE ... OUTPUT` zastępujący `SQL Server Agent` na Express, kolejkowanie `Subiekt Sfera COM` eliminujące deadlocki na `>12 000 SKU`, naprawy bezpieczeństwa sesji `PHP session fixation` na `>15 000 sesji/dobę`, audyty `GTM/GA4 DataLayer` ze zgodnością transakcji `99,2%` oraz potoki ETL `Python -> BigQuery Cloud Run Jobs`).
  3. **[`kod/prompts/kontekst/lore.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/lore.md)**, **[`kod/prompts/kontekst/jak_pisac_oferty.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md)**, **[`kod/prompts/kontekst/stack_i_filozofia.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/stack_i_filozofia.md)** oraz **[`kod/prompts/walidatory/agent_08_weryfikacja_zasad.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md)**:
     - Ujednolicono zasady zespołu Ksawier + Maksymilian (stawka `90 zł/h`, doświadczenie maszynowe CNC, Sandbox-First, 30 dni gwarancji na własny kod, 100% komunikacji pisemnej na priv bez propozycji rozmów telefonicznych).

---

### Etap 6: Niezależny Łańcuch Krytyka 1–100 pkt (`kryteria_audytu_100.md` + `audytor_lancuch.py`) i 5 Fal Audytu (27 Ofert)
* **Utworzone pliki:**
  1. **[`kod/prompts/walidatory/kryteria_audytu_100.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/kryteria_audytu_100.md)** *(NOWY PLIK)*:
     - Matryca oceniania `1–100 pkt` w 5 wymiarach:
       - **A. Głębia Merytoryczna i Techniczna (`0–25 pkt`)**
       - **B. Psychologia B2B i Dopasowanie Dual-Track (`0–25 pkt`)**
       - **C. Pytanie Kwalifikujące / CTA (`0–20 pkt`)**
       - **D. Realizm i Spójność Wyceny (`0–15 pkt`)**
       - **E. Styl, Zwięzłość i Higiena Językowa (`0–15 pkt`)**
     - Wymóg pełnej transparentności: jawne listy `za_co_dodano` (`+pkt` z uzasadnieniem) oraz `za_co_odjeto` (`-pkt` z dokładnym cytatem z oferty i wyjaśnieniem błędu).
  2. **[`kod/audytor_lancuch.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/audytor_lancuch.py)** *(NOWY PLIK)*:
     - `deterministic_pre_audit()`: twardy pre-audyt w Pythonie sprawdzający liczbę słów (`<= 110` dla `< 3 000 zł`, `130–205` dla `>= 3 000 zł`), zakazane szablony (`FORBIDDEN_PATTERNS`), wyciek żargonu IT na ścieżce `biznes`, rozjazd dni (`PEN_DAYS_MISMATCH`), widełki cenowe (`PEN_PRICE_RANGE`), obecność deklaracji Sandbox (`PEN_MISSING_SANDBOX`), gęstość akronimów (`PEN_ACRONYM_STUFFING`) oraz mnożniki wyceny.
     - `evaluate_offer_100()`: wywołanie Niezależnego Sędziego z kartami wiedzy domenowej i połączenie oceny modelu z pre-audytem Pythona (z eliminacją podwójnego odejmowania kar).
     - `regenerate_from_judge_feedback()` oraz `audit_and_refine_100()`: pętla samodoskonalenia przepisująca ofertę na podstawie listy `za_co_odjeto`, z ochroną kwoty wyceny (`_extract_price_days_from_text`) i zachowaniem najlepszego wyniku (`max(R1, R2)`).
  3. **[`kod/test_bot_audit.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/test_bot_audit.py)** oraz **[`kod/tests/test_strategia_dual_track.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tests/test_strategia_dual_track.py)**:
     - Rozbudowany zestaw **51 testów jednostkowych (`pytest`)** weryfikujących kalkulator `90 zł/h`, sufit ryzyka `1.15`, selektor 16 kart wiedzy, filtr Czerwonego Oceanu, brak wycieku tabel/kwot do `02a` oraz pre-audyt `audytor_lancuch.py` (`51 passed`).

---

### Etap 7: Poprawki Po Meta-Audycie Red-Team (`68–76/100` -> `96+/100`), Integracja Produkcyjna i Asystent Priv (`priv_engine.py`)
* **Zmodyfikowane i utworzone pliki:**
  1. **[`kod/config.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/config.py)**:
     - Scentralizowano `HARD_REJECT_PATTERNS`, `PHANTOM_PATTERNS` i funkcję `is_hard_reject(title, description)` jako pojedyncze źródło prawdy (Single Source of Truth) oraz dodano flagi produkcyjne `USE_AUDYTOR_100 = True` i `AUDYTOR_100_TARGET_SCORE = 92`.
  2. **[`kod/ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py)** oraz **[`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py)**:
     - Wpięto deterministyczny filtr `config.is_hard_reject()` przed wywołaniem `AI #1` (oraz w fallbacku timeoutu), wpięto `_sanitize_opis()` i `audit_and_refine_100()` bezpośrednio w produkcyjny `SlotChainAIPipeline.generate_proposal()` oraz dodano twardą blokadę `SANITY_BLOK` w `engine.py` przy `not sanity_ok or not kwota_zgodna`.
  3. **[`kod/wycena_kalkulator.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py)** oraz **[`kod/prompts/chain_config.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/chain_config.json)**:
     - Ujednolicono `MAX_RISK_MULTIPLIER = 1.15` i funkcję `max()` między trybem `projekt` a `retainer`, dodano mnożnik `1.05` (`+5%` marży dla świeżych zleceń z niską konkurencją) w `KOREKTY` oraz wyczyszczono `chain_config.json` z 6 wyłączonych slotów-zombie (`03..07, 20`).
  4. **[`kod/prompts/generatory/agent_02a_opis_oferty.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)** oraz **[`kod/prompts/kontekst/portfolio_baza.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/portfolio_baza.md)**:
     - Odchudzono `agent_02a_opis_oferty.md` o 37% (usunięcie nazw własnych pojedynczych zleceń + reguła anty-keyword-stuffingu maks. 3–4 skróty w akapicie) oraz oznaczono wdrożenia `Projekt 8`, `Projekt 9` i `Comarch ERP XL` w `portfolio_baza.md` jako bezpośrednie kontrakty B2B zespołu poza Useme objęte umową NDA (z gotowymi zanonimizowanymi wycinkami na priv).
  5. **[`kod/priv_engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/priv_engine.py)**, **[`kod/prompts/generatory/agent_priv_responder.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_priv_responder.md)** oraz **[`kod/tests/test_priv_engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tests/test_priv_engine.py)**:
     - Odtworzono i zmodernizowano moduł obsługi wiadomości prywatnych (Krok 07), zintegrowany ze ścieżką `Dual-Track`, kartami wiedzy `tech_01`–`tech_16`, ochroną NDA portfolio oraz 3-krokowym domykaniem transakcji Anty-Phantom.

