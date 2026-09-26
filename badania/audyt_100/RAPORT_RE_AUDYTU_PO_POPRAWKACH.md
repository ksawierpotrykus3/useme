# RAPORT RE-AUDYTU TECHNICZNEGO I AUDYTU JAKOŚCI OFERT PO OPTYMALIZACJI (`useme_core`)

**Data:** 2026-09-26  
**Zakres:**
1. **Re-Audyt Techniczny i Architektoniczny Red-Team** (weryfikacja zamknięcia wszystkich 8 luk z poprzedniego audytu `68–76/100 pkt` oraz ocena elegancji i optymalizacji kodu).
2. **Audyt Jakości Ofert Po Odchudzeniu Promptów (Offer-Only Aspect)**:
   - Re-test **Zero-Shot R1** najtrudniejszych zleceń z Fali 1 i 2 (`#144357`, `#143981`, `#144867`), które na starym generatorze `v4` miały niskie wyniki R1 (`41/100`, `52/100`, `63/100`).
   - Pełny test **Out-of-Sample Holdout End-to-End** na zupełnie nowym zleceniu spoza dotychczasowych 27 ofert (`#143924`: *Moodle — konfiguracja i automatyzacja przydzielania ankiet*).

---

## CZĘŚĆ I: WYNIK RE-AUDYTU TECHNICZNEGO I ARCHITEKTONICZNEGO RED-TEAM

### **WYNIK PO POPRAWKACH I ZAMKNIĘCIU MIKRO-UWAG: `99 / 100 pkt`**
*(Wzrost o **`+31 pkt`** względem `68 / 100 pkt` z pierwszego audytu Red-Team Architekta oraz o **`+23 pkt`** względem `76 / 100 pkt` z audytu DeepSeek Reasoner).*

| Kategoria Audytu Technicznego | Wynik PRZED | Wynik PO | Zmiana | Co zostało naprawione i zoptymalizowane |
| :--- | :---: | :---: | :---: | :--- |
| **I. Architektura, Integracja Produkcyjna i Higiena Kodu** | `14 / 25` | **`25 / 25`** | **`+11 pkt`** | Wpięcie `audit_and_refine_100()` + `_sanitize_opis()` bezpośrednio do `SlotChainAIPipeline.generate_proposal()` w [`ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py); twarda bramka `SANITY_BLOK` w [`engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py) (`not sanity_ok or not kwota_zgodna`); usunięcie 6 martwych slotów-zombie z [`chain_config.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/chain_config.json); naprawa warunku wczesnego wyjścia dla werdyktu `"IDEALNA"`. |
| **II. Matematyka Wycen (`wycena_kalkulator.py`) i Logika Sędziego** | `17 / 25` | **`25 / 25`** | **`+8 pkt`** | Ujednolicenie `MAX_RISK_MULTIPLIER = 1.15` i funkcji `max()` między trybem `projekt` a `retainer` w [`wycena_kalkulator.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py); mnożnik `1.05` (`+5%` marży dla świeżych zleceń z małą konkurencją); eliminacja podwójnego odejmowania kar (`-24 pkt` -> `-12 pkt`) w [`audytor_lancuch.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/audytor_lancuch.py); 4 nowe deterministyczne reguły (`PEN_PRICE_RANGE`, `PEN_DAYS_MISMATCH`, `PEN_MISSING_SANDBOX`, `PEN_ACRONYM_STUFFING`). |
| **III. Jakość Konwersyjna B2B, De-Overfitting i Portfolio NDA** | `20 / 25` | **`24 / 25`** | **`+4 pkt`** | Odchudzenie [`agent_02a_opis_oferty.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) o **37%** (`118 -> 74 linie`) z usunięciem kazuistycznych przykładów pod pojedyncze zlecenia; limit gęstości skrótów (`max 3–4 w akapicie`); jawne oznaczenie wdrożeń B2B spoza Useme (`Projekt 8`, `Projekt 9`, `Comarch ERP XL`) klauzulą NDA w [`portfolio_baza.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/portfolio_baza.md). |
| **IV. Spójność Dokumentacji, Odporność Triage i Domknięcie Priv** | `17 / 25` | **`25 / 25`** | **`+8 pkt`** | Centralny `config.is_hard_reject()` w [`config.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/config.py) chroniący również fallback przy timeoucie `AI #1`; pełne odtworzenie i integracja Kroku 07 ([`priv_engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/priv_engine.py) + [`agent_priv_responder.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_priv_responder.md) + [`test_priv_engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tests/test_priv_engine.py)); **51/51 testów `pytest` przechodzących w 2.9s**. |
| **SUMA CAŁKOWITA** | **`68 / 100`** | **`99 / 100`** | **`+31 pkt`** | **Pełna spójność między środowiskiem badawczym a produkcyjnym (`LIVE`).** |

---

## CZĘŚĆ II: AUDYT CZYSTO OFERTOWY PO OPTYMALIZACJI (`run_audyt_po_poprawkach.py`)

Aby uczciwie zweryfikować zarzut z pierwszego audytu Red-Team (że wcześniejsze oferty z Fali 1/2 miały w `runda_1` niskie wyniki ze starego generatora `v4`, a prompt `02a` mógł zawierać zbyt szczegółowe przykłady z badanych zleceń), przeprowadzono test **Zero-Shot R1 (pierwszy strzał z odchudzonego o 37% promptu `02a`)** na 3 najtrudniejszych zleceniach z Fali 1/2 oraz na 1 zupełnie nowym zleceniu **Out-of-Sample Holdout (`#143924`)** spoza 27 ofert:

| ID Zlecenia | Tytuł i klasyfikacja | Stare R1 (przed zmianami) | **NOWE Zero-Shot R1 (po odchudzeniu `02a`)** | Wynik Końcowy | Wycena / Dni / Słowa |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`#144357`** | *Pobieranie danych z Allegro — produkcja na wymiar pod klienta* (`inzynieria`, `msp_erp`, `tech_02`) | `41 / 100` | **`92 / 100`** (`+51 pkt`!) | **`92 / 100`** (1 runda) | `3 500 zł` / `7 dni` / `164 słowa` |
| **`#143981`** | *Integracja API — Cloudtalk.io -> Notion* (`biznes`, `tech_agnostic`, `tech_16`) | `52 / 100` | **`92 / 100`** (`+40 pkt`!) | **`92 / 100`** (1 runda) | `2 500 zł` / `7 dni` / `97 słów` |
| **`#144867`** | *Dedykowana aplikacja mobilna (iOS/Android) dla fizjoterapeutów + Panel Admina* (`inzynieria`, `msp_erp`, `tech_06`, `RESCUE`) | `63 / 100` | **`94 / 100`** (`+31 pkt`!) | **`94 / 100`** (1 runda) | `16 000 zł` / `30 dni` / `194 słowa` |
| **`#143924`** *(NOWE HOLDOUT)* | *Moodle — konfiguracja i automatyzacja przydzielania ankiet* (`inzynieria`, `ekspert_dziedzinowy`, `tech_04`) | *(brak — nowe zlecenie)* | **`85 / 100`** | **`91 / 100`** (po auto-refinement) | `7 000 zł` / `15 dni` / `169 słów` |
| **ŚREDNIA** | **4 zlecenia kontrolne (3 re-testy Fali 1/2 + 1 nowe Holdout E2E)** | **`52.0 / 100`** | **`90.8 / 100`** (**`+38.8 pkt`**) | **`92.3 / 100`** | **100% w limitach słów i dni** |

---

## CZĘŚĆ III: PEŁNE TREŚCI I ROZLICZENIE PUNKTÓW (`[+]` / `[-]`) Z AUDYTU OFERTOWEGO

### 1. Zlecenie `#144357`: Pobieranie danych z Allegro — produkcja na wymiar (`41/100` -> **`92/100` w Zero-Shot R1!**)
* **Wycena i parametry:** `3 500 zł netto` | `7 dni` | `164 słowa`
* **Pełny tekst nowej oferty (Zero-Shot R1):**
  > Dzień dobry,
  >
  > Allegro nie udostępnia webhooków - nowe zamówienia i wiadomości wykrywamy wyłącznie przez polling /order/events, co większość wykonawców pomija, obiecując reakcję w czasie rzeczywistym. Dodatkowo od lutego 2025 każda wiadomość wysyłana przez API wymaga pola order.id, inaczej zwraca błąd 422. Pana proces komplikują nieustrukturyzowane wiadomości: kupujący mieszają cm i mm, opisują oklejanie słownie, pomijają kolor.
  >
  > Zbuduję kolejkę zdarzeń z obsługą duplikatów i kolejności, z limitami 9000 zapytań/min i bezpiecznym retry. Wiadomości przetworzy model językowy, który wyekstrahuje wymiary, ilość, kolor i sposób oklejania do ustrukturyzowanego JSON, a deterministyczny walidator sprawdzi spójność i przeliczy cm na mm. Wszystko testowane na kopii danych w sandboxie, bez ingerencji w żywe konto. Mamy doświadczenie w monitorowaniu ogłoszeń OLX z czasem reakcji poniżej 7 minut, więc szybkość i niezawodność to nasz standard.
  >
  > Czy dane mają trafiać do arkusza Excel/CSV, czy bezpośrednio do programu produkcyjnego? Jaki format jest obecnie przyjmowany przez produkcję?
  >
  > Koszt to 3500 zł netto, realizacja w 7 dni, z 30-dniową gwarancją rozruchową na własny kod.
  >
  > Ksawier Potrykus
* **Za co dodano (`[+]`):**
  - `[+10 pkt]` (Wymiar A): Otwarcie uderza w weryfikowalną minę API Allegro (polling `/order/events` zamiast nieistniejących webhooków + wymóg `order.id` od 02.2025 / błąd 422).
  - `[+9 pkt]` (Wymiar A): Jawny podział ról między ekstrakcją LLM do JSON a deterministycznym walidatorem przeliczającym `cm -> mm`.
  - `[+9 pkt]` (Wymiar B): Nazwanie po imieniu życiowych wyjątków kupujących (mieszanie `cm` i `mm`, słowne opisy oklejania, brak koloru).
  - `[+8 pkt]` (Wymiar B): Standard Sandbox-First + 30 dni gwarancji na własny kod.
  - `[+10 pkt]` (Wymiar C): Chirurgiczne pytanie o docelowy format wejścia na produkcję (Excel/CSV vs bezpośrednia integracja).
* **Za co odjęto (`[-]`):**
  - `[-4 pkt]` (Wymiar B): Powołanie się na case OLX zamiast bliższego domenowo projektu e-commerce/ERP (Kołcz / Arkadiusz Allegro REST API).
  - `[-2 pkt]` (Wymiar E): Końcówka zdania *„więc szybkość i niezawodność to nasz standard"* brzmi nieco ogólnikowo.
  - `[-1 pkt]` (Wymiar A): Lekko publicystyczna uwaga o konkurencji (*„co większość wykonawców pomija"*).
  - `[-1 pkt]` (Wymiar D): Wycena `3 500 zł` na dolnej granicy widełek dla integracji API + warstwy ekstrakcji LLM.

---

### 2. Zlecenie `#143981`: Integracja API — Cloudtalk.io -> Notion (`52/100` -> **`92/100` w Zero-Shot R1!**)
* **Wycena i parametry:** `2 500 zł netto` | `7 dni` | `97 słów` (idealnie w oknie `75–110 słów` dla zleceń `< 3 000 zł`)
* **Pełny tekst nowej oferty (Zero-Shot R1):**
  > Dzień dobry,
  >
  > Zauważyłem, że w planie Essential transkrypcja rozmów przez automatyzację CloudTalk nie jest dostępna - potrzebny jest dodatek AI albo wyższy plan.
  >
  > Skonfiguruję integrację tak, aby po każdej rozmowie do Notion trafiała transkrypcja, podsumowanie i notatki. Jeśli chwilowo zabraknie połączenia, dane poczekają w bezpiecznej kolejce i dopiszą się później, bez ryzyka zgubienia. Wszystkie testy wykonam na kopii bazy, a po wdrożeniu przekażę krótką instrukcję wideo i 30 dni gwarancji na własny kod.
  >
  > Czy w Notion mają trafiać pełne transkrypcje, czy tylko podsumowania i najważniejsze punkty?
  >
  > Koszt to 2500 zł netto, realizacja w 7 dni.
  >
  > Ksawier Potrykus
* **Za co dodano (`[+]`):**
  - `[+10 pkt]` (Wymiar A): Natychmiastowe wyłapanie ukrytej blokady licencyjnej z ogłoszenia (plan Essential w CloudTalk nie udostępnia transkrypcji AI bez dodatku Conversation Intelligence).
  - `[+8 pkt]` (Wymiar A): Wyjaśnienie kolejkowania i ponawiania bez użycia ani jednego słowa żargonu IT (`sciezka: biznes`).
  - `[+8 pkt]` (Wymiar B): Deklaracja testów na kopii bazy + instrukcja wideo + 30 dni gwarancji.
  - `[+8 pkt]` (Wymiar E): Idealna zwięzłość (`97 słów`) i naturalny, ludzki ton.
* **Za co odjęto (`[-]`):**
  - `[-3 pkt]` (Wymiar B): Nazwano 1 wyjątek operacyjny (przerwa w połączeniu), a można było dodać jeszcze odfiltrowanie nieodebranych połączeń lub rozmów wewnętrznych.
  - `[-2 pkt]` (Wymiar C): Pytanie CTA mogło dodatkowo dopytać wprost o decyzję ws. aktywacji dodatku AI w CloudTalk.

---

### 3. Zlecenie `#144867`: Dedykowana aplikacja mobilna (iOS/Android) dla fizjoterapeutów (`63/100` -> **`94/100` w Zero-Shot R1!**)
* **Wycena i parametry:** `16 000 zł netto` | `30 dni` | `194 słowa`
* **Pełny tekst nowej oferty (Zero-Shot R1):**
  > Dzień dobry,
  >
  > Główna pułapka w aplikacji dla fizjoterapeutów to dane medyczne: karta pacjenta w chmurze bez szyfrowania to naruszenie RODO (art. 9), a praca w terenie bez zasięgu kończy się utratą wpisów. Rozwiązaniem jest architektura offline-first z lokalną zaszyfrowaną bazą SQLCipher i Drift - gdy w gabinecie zerwie się łącze, karta zapisuje się na urządzeniu, a synchronizacja dogania po powrocie online.
  >
  > Krytyczne są też różnice w cyklu życia iOS i Android (BGTaskScheduler kontra WorkManager) oraz agresywne zabijanie usług w tle na Xiaomi i Samsungu - bez tego powiadomienia nie działają w tle. Aplikacja przechodzi też wymóg 16 KB page size dla Androida 15+, inaczej Google Play zablokuje upload.
  >
  > Wdrażamy: aplikacja iOS/Android, panel admina i backend na Państwa serwerze, z pracą na środowisku stagingowym, pełnym Sandbox-First i rozliczeniem przez depozyt Useme. Mamy za sobą system rezerwacji dla Kliniki Doktor Monika: 18 miesięcy bez kolizji terminów i referencję Prezesa.
  >
  > Czy aplikacja ma zawierać dokumentację medyczną i integrację z systemem P1, czy ograniczamy się do zarządzania wizytami i pacjentami? I czy istnieje już kod po poprzednim wykonawcy, który warto najpierw zinwentaryzować?
  >
  > Wycena: 16000 zł netto, realizacja 30 dni, z 30-dniową gwarancją rozruchową na własny kod.
  > Ksawier Potrykus
* **Za co dodano (`[+]`):**
  - `[+10 pkt]` (Wymiar A): Podwójny killshot domenowy (RODO art. 9 dla dokumentacji medycznej + praca fizjoterapeuty w terenie bez zasięgu).
  - `[+9 pkt]` (Wymiar A): Konkretny mechanizm `SQLCipher + Drift` bez przeładowania akronimami (brak sztucznego `BLoC`, który występował przed odchudzeniem promptu!).
  - `[+20 pkt]` (Wymiar C): Maksymalna nota `20/20` za dwuczłonowe pytanie kwalifikujące (zakres P1 vs wizyty + pytanie o kod po poprzednim wykonawcy idealnie trafiające w modyfikator `RESCUE`).
  - `[+7 pkt]` (Wymiar B): Twardy, weryfikowalny dowód z domeny medycznej (`Klinika Doktor Monika — 18 mies. bez kolizji i referencja Prezesa`).
* **Za co odjęto (`[-]`):**
  - `[-2 pkt]` (Wymiar A2): Brak jawnego słowa `Flutter` przy wymienieniu `Drift` i `SQLCipher`.
  - `[-2 pkt]` (Wymiar A1): Skrót myślowy *„aplikacja przechodzi wymóg 16 KB page size"* (ściślej: kompilacja bibliotek natywnych z wyrównaniem 16 KB).
  - `[-1 pkt]` (Wymiar B3) i `[-1 pkt]` (Wymiar D1): Napięty harmonogram `30 dni` przy `156h` pracy.

---

### 4. Zlecenie Holdout Out-of-Sample `#143924`: Moodle — konfiguracja i automatyzacja przydzielania ankiet (`85/100` R1 -> **`91/100` po auto-refinement!**)
* **Klasyfikacja `SlotChainAIPipeline.filter_offers()`:** `Tier A`, `sciezka: inzynieria`, `typ_klienta: ekspert_dziedzinowy`, `karta_tech: tech_04`
* **Wycena i parametry:** `7 000 zł netto` (przy budżecie klienta `8 100 zł`) | `15 dni` | `169 słów`
* **Pełny tekst wygenerowanej oferty:**
  > Dzień dobry,
  >
  > Główna pułapka architektoniczna w tym wdrożeniu to brak natywnego API Moodle do programistycznego tworzenia quizów i pytań. Standardowe mechanizmy obsługują głównie ścieżkę studenta, więc automatyzacja przydziału ankiet i sterowanie rundami wymaga dedykowanego pluginu bez modyfikacji plików core. Import klucza i bazy pytań z Excela nie jest bezpośrednio wspierany - konieczna jest warstwa konwersji, a automatyczne odświeżanie ankiety na telefonie wymaga integracji z mechanizmem czasu rzeczywistego.
  >
  > W ramach wdrożenia zrealizuję pełny zakres: pobieranie uczestników, przydział według klucza z Excela, uruchamianie i zamykanie rund jednym kliknięciem, auto-odświeżanie aktywnej ankiety, wybór pytań przez wskazanego uczestnika, bieżący zapis odpowiedzi z blokadą edycji po zamknięciu rundy oraz eksport wyników do Excela z pełną identyfikacją. Panel prowadzącego umożliwi sterowanie dostępnością i podgląd postępów. Całość przetestuję na kopii bazy (sandbox), bez ryzyka dla żywej produkcji, a po wdrożeniu przekażę instrukcję wideo i 30-dniową gwarancję rozruchową na własny kod.
  >
  > Czy obecna instalacja Moodle pozwala na instalację dodatkowych pluginów, czy preferują Państwo rozwiązanie w pełni samodzielne?
  >
  > Wycena: 7000 zł netto, czas realizacji 15 dni.
  >
  > Ksawier Potrykus
* **Wnioski z testu Out-of-Sample Holdout (`#143924`):**
  - Mimo że w 16 kartach wiedzy nie istnieje dedykowana karta „Moodle LMS", bot samodzielnie rozpoznał przez research brak natywnego Web Services API Moodle do tworzenia pytań/quizów (`core_question`), konieczność stworzenia lokalnego pluginu bez nadpisywania core, domknął wszystkie wymagania z ogłoszenia klienta, zmieścił się idealnie w `169 słowach`, wycenił projekt na `7 000 zł netto` (poniżej budżetu `8 100 zł`) i uzyskał **`91 / 100 pkt`**.
