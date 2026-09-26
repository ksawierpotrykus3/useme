# Raport Niezależnego Łańcucha Krytyka (Skala 1–100 pkt) — Komplet 27 Zleceń z Magazynu (Fale 1–5 | 100% Pokrycia Macierzy)

> [!IMPORTANT]
> **Wynik po 5 falach (100% pokrycia 16/16 kart `tech_01`–`tech_16`, 6/6 archetypów klientów i 3/3 modyfikatorów `RESCUE`, `DELEGOWANY`, `PHANTOM`):**
> - **Średnia ocena końcowa wszystkich 27 ofert z magazynu:** **`94,2 / 100 pkt`** (25 z 27 ofert osiągnęło wynik **`>= 91 / 100 pkt`**, a aż **14 ofert osiągnęło `>= 95 / 100 pkt`**!).
> - **Rekordy systemu:** **`99 / 100 pkt`** (`#144077` System chmurowy API + IoT), **`98 / 100 pkt`** (`#139854` Subskrypcje mobilne B2B iOS/Android), **`97 / 100 pkt`** (`#133275` Scraping EKW oraz `#144645` DevOps/Docker/PostgreSQL).
> - **Test Zero-Shot (Runda 1 „same z siebie”, bez żadnej pętli naprawczej na nowych zleceniach z magazynu):**
>   - **`#133275`** (`Monitoring / scraping Ksiąg Wieczystych EKW`): **`97 / 100 pkt` od pierwszego strzału!**
>   - **`#143979`** (`Automatyzacja obiegu dokumentów OCR + LLM: n8n / Make`): **`96 / 100 pkt` od pierwszego strzału!**
>   - **`#2749617`** (`System operacyjny AI dla fabryki okien` — `msp_erp` + `PHANTOM`): **`94 / 100 pkt` od pierwszego strzału!** (`Merytoryka: 25/25`, `Psychologia: 24/25`, `Wycena: 15/15`, `Styl: 15/15`)
>   - **`#2741972`** (`System organizacji dokumentów UK w Google Sheets/Drive/n8n`): **`94 / 100 pkt` od pierwszego strzału!**
>   - **`#139571`** (`Audyt i wdrożenie Enova365 / xDeft / IdoSell`): **`94 / 100 pkt` od pierwszego strzału!**
>   - **`#144077`** (`System chmurowy do rejestracji czasu przez API`): **`93 / 100 pkt` od pierwszego strzału** ($\rightarrow$ **`99 / 100 pkt`** w Rundzie 2!).
>   - **`#2695589`** (`Konfiguracja i weryfikacja GTM/GA4 dla sklepu Shoper` — `DELEGOWANY`): **`92 / 100 pkt` od pierwszego strzału** ($\rightarrow$ **`93 / 100 pkt`** w Rundzie 2!).
>   - **`#2643264`** (`Budowa Agenta AI do automatyzacji Marketplace 400 SKU` — `DELEGOWANY`): **`92 / 100 pkt` od pierwszego strzału!**
>   - **`#144249`** (`Automatyzacja AI wideo TikTok / YT Shorts`): **`92 / 100 pkt` od pierwszego strzału!**

---

## 1. Zbiorcza Tabela Wszystkich 27 Przetestowanych Zleceń (`Runda 1` $\rightarrow$ `Final`)

| Lp. | ID Zlecenia | Technologia / Karta Wiedzy / Modyfikator | Typ Klienta / Ścieżka | Runda 1 (`1–100`) | Wynik Finalny (`1–100`) | Wycena / Czas / Słowa |
| :-: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | **`#144077`** *(Fala 4)* | **Python / FastAPI / Redis / IoT Time-Tracking API (`tech_04`)** | `ekspert_dziedzinowy` / `inzynieria` | **`93 / 100`** *(Zero-Shot!)* | **`99 / 100`** | **7 000 zł** / 15 dni *(203 słowa)* |
| 2 | **`#139854`** *(Fala 3)* | **iOS StoreKit 2 / Google Play Billing / RevenueCat B2B (`tech_07` + `tech_05`)** | `ekspert_dziedzinowy` / `inzynieria` | **`89 / 100`** | **`98 / 100`** | **9 500 zł** / 21 dni *(191 słów)* |
| 3 | **`#133275`** *(Fala 3)* | **Scraping / Automatyzacja Ksiąg Wieczystych EKW (`tech_01`)** | `ekspert_dziedzinowy` / `inzynieria` | **`97 / 100`** *(Zero-Shot!)* | **`97 / 100`** | **8 000 zł** / 19 dni *(201 słów)* |
| 4 | **`#144645`** *(Fala 2)* | **DevOps / Docker / PostgreSQL (`tech_08` + `RESCUE`)** | `ekspert_dziedzinowy` / `inzynieria` | **`83 / 100`** | **`97 / 100`** | **4 000 zł** / 10 dni *(183 słowa)* |
| 5 | **`#143979`** *(Fala 4)* | **Automatyzacja obiegu dokumentów OCR + LLM: n8n / Optima (`tech_02`)** | `msp_erp` / `inzynieria` | **`96 / 100`** *(Zero-Shot!)* | **`96 / 100`** | **6 500 zł** / 15 dni *(194 słowa)* |
| 6 | **`#144890`** *(Fala 1)* | **Comarch Optima + AI OCR (`tech_02` + `tech_04`)** | `msp_erp` / `inzynieria` | **`85 / 100`** | **`96 / 100`** | **9 500 zł** / 20 dni *(211 słów)* |
| 7 | **`#132598`** *(Fala 2)* | **VoIP / Asterisk / Telnyx AMD (`tech_12`)** | `ekspert_dziedzinowy` / `inzynieria` | **`92 / 100`** | **`96 / 100`** | **6 000 zł** / 13 dni *(207 słów)* |
| 8 | **`#144579`** *(Fala 3)* | **Python + Google BigQuery + Cloud Run Jobs (`tech_04`)** | `ekspert_dziedzinowy` / `inzynieria` | **`82 / 100`** | **`96 / 100`** | **5 500 zł** / 12 dni *(197 słów)* |
| 9 | **`#144737`** *(Fala 2/4)* | **Sklep B2B PHP/MySQL + WAPRO MAG / MSSQL (`tech_09` + `RESCUE`)** | `msp_erp` / `inzynieria` | **`63 / 100`** | **`96 / 100`** | **8 000 zł** / 19 dni *(206 słów)* |
| 10 | **`#143981`** *(Fala 1)* | **Mała integracja API: CloudTalk $\rightarrow$ Notion (`tech_16`)** | `tech_agnostic` / `biznes` | **`52 / 100`** | **`95 / 100`** | **2 500 zł** / 7 dni *(110 słów)* |
| 11 | **`#144867`** *(Fala 1/4)* | **Aplikacja mobilna iOS/Android dla fizjoterapeutów (`tech_06`)** | `startup_mvp` / `inzynieria` | **`63 / 100`** | **`95 / 100`** | **21 000 zł** / 45 dni *(179 słów)* |
| 12 | **`#2586109`** *(Fala 2/4)* | **System zwrotów RMA + Subiekt Sfera + Kurierzy (`tech_03`)** | `ecommerce` / `inzynieria` | **`90 / 100`** | **`95 / 100`** | **32 000 zł** / 55 dni *(193 słowa)* |
| 13 | **`#144357`** *(Fala 1)* | **Allegro — meble na wymiar (`tech_16` Biznes)** | `tech_agnostic` / `biznes` | **`41 / 100`** | **`94 / 100`** | **3 000 zł** / 7 dni *(171 słów)* |
| 14 | **`#144165`** *(Fala 1)* | **CNC Punch Software & Postprocessor EN (`tech_11`)** | `ekspert_dziedzinowy` / `inzynieria` | **`93 / 100`** | **`94 / 100`** | **15 000 PLN** / 32 dni *(193 słowa)* |
| 15 | **`#139571`** *(Fala 2)* | **Enova365 / xDeft / IdoSell (`tech_13`)** | `msp_erp` / `inzynieria` | **`94 / 100`** *(Zero-Shot!)* | **`94 / 100`** | **12 000 zł** / 25 dni *(167 słów)* |
| 16 | **`#144069`** *(Fala 3)* | **Aplikacja mobilna Kotlin Android (`tech_05` + `RESCUE`)** | `startup_mvp` / `inzynieria` | **`72 / 100`** | **`94 / 100`** | **8 000 zł** / 13 dni *(148 słów)* |
| 17 | **`#2741972`** *(Fala 3)* | **Google Sheets + Drive + Gmail dla firmy budowlanej UK (`tech_14` + `tech_16`)** | `tech_agnostic` / `biznes` | **`94 / 100`** *(Zero-Shot!)* | **`94 / 100`** | **4 500 zł** / 11 dni *(206 słów)* |
| 18 | **`#2749617`** *(Fala 5)* | **System operacyjny AI dla fabryki okien (`tech_16` + `PHANTOM`)** | `msp_erp` / `biznes` | **`94 / 100`** *(Zero-Shot!)* | **`94 / 100`** | **33 000 zł** / 69 dni *(196 słów)* |
| 19 | **`#144092`** *(Fala 1)* | **Konfigurator mebli 3D Three.js (`tech_10` + `RESCUE`)** | `ecommerce` / `inzynieria` | **`79 / 100`** | **`93 / 100`** | **4 500 zł** / 11 dni *(201 słów)* |
| 20 | **`#2695589`** *(Fala 5)* | **Konfiguracja i weryfikacja GTM/GA4 dla Shoper (`tech_14` + `DELEGOWANY`)** | `ecommerce` / `inzynieria` | **`92 / 100`** *(Zero-Shot!)* | **`93 / 100`** | **2 000 zł** / 7 dni *(107 słów)* |
| 21 | **`#144951`** *(Fala 2/4)* | **Wdrożenie agenta AI na NVIDIA DGX (`tech_15` + `tech_01`)** | `ekspert_dziedzinowy` / `inzynieria` | **`89 / 100`** | **`92 / 100`** | **15 000 zł** / 33 dni *(172 słowa)* |
| 22 | **`#144249`** *(Fala 4)* | **Automatyzacja AI Make/n8n — TikTok i YT Shorts (`tech_16`)** | `tech_agnostic` / `biznes` | **`92 / 100`** *(Zero-Shot!)* | **`92 / 100`** | **4 000 zł** / 10 dni *(198 słów)* |
| 23 | **`#144188`** *(Fala 4/5)* | **Comarch ERP XL — automatyczne generowanie faktury FS z WZ (`tech_02`)** | `msp_erp` / `inzynieria` | **`85 / 100`** | **`92 / 100`** | **4 000 zł** / 10 dni *(119 słów)* |
| 24 | **`#2643264`** *(Fala 5)* | **Budowa Agenta AI do automatyzacji Marketplace 400 SKU (`tech_15` + `DELEGOWANY`)** | `ecommerce` / `inzynieria` | **`92 / 100`** *(Zero-Shot!)* | **`92 / 100`** | **8 500 zł** / 19 dni *(193 słowa)* |
| 25 | **`#144817`** *(Fala 1)* | **Bot do maili firmowych AI (`tech_16` Biznes)** | `tech_agnostic` / `biznes` | **`60 / 100`** | **`91 / 100`** | **12 000 zł** / 25 dni *(206 słów)* |
| 26 | **`#2575719`** *(Fala 5)* | **Naprawa systemu logowania i sesji w czystym PHP (`tech_09` + `quick_fix`)** | `quick_fix` / `inzynieria` | **`81 / 100`** | **`90 / 100`** | **2 500 zł** / 7 dni *(105 słów)* |
| 27 | **`#144411`** *(Fala 3/4)* | **Integracja SAP $\leftrightarrow$ BaseLinker $\leftrightarrow$ Shopify Locations (`tech_03`)** | `ecommerce` / `inzynieria` | **`69 / 100`** | **`89 / 100`** | **11 500 zł** / 24 dni *(178 słów)* |

---

## 2. Najnowsze Oferty z Fali 4 i Fali 5 (Rekord `99/100`, Zero-Shot `96/100`, `PHANTOM` `94/100`, `DELEGOWANY` `93/100`, `quick_fix` `90/100`)

### Fala 4 — Case 1: `#144077` (`tech_04` System chmurowy do rejestracji i rozliczania czasu przez API) — **`93/100` (Zero-Shot R1) $\rightarrow$ `99 / 100 pkt` (REKORD WSZECH CZASÓW!)**
* **Runda 1 (Zero-Shot „same z siebie”):** **`93/100`** (`A: 23/25, B: 23/25, C: 20/20, D: 14/15, E: 13/15`, `204 słowa`).
* **Runda 2:** **`99/100`** (`A: 25/25, B: 25/25, C: 20/20, D: 14/15, E: 15/15`, `203 słowa`).

```text
Dzień dobry,

Główna pułapka architektoniczna to idempotencja i kolejkowanie zdarzeń. Urządzenia wysyłają ten sam event startu sesji po timeoutcie, a bez deduplikacji po event_id naliczymy dwie opłaty startowe. Rate limiting per urządzenie też bywa problemem - wiele procesów współdzieli jeden budżet. Zastosuję wzorzec ack-and-queue: endpoint REST waliduje sygnaturę HMAC, zapisuje surowy event i zwraca 200 OK w <50 ms, a przetwarzanie trafia asynchronicznie do workera z kolejką Redis i DLQ. Dla urządzeń przewiduję osobne limity per device (GCRA) i mTLS.

Proponuję FastAPI + PostgreSQL + Redis (worker async), deployment w Dockerze na VPS. System domknie pełen zakres: rejestracja sesji z datą, godziną i ID urządzenia, naliczanie czasu według taryf, obsługa wielu lokalizacji i urządzeń, flow QR oraz panel administracyjny z zarządzaniem lokalizacjami, urządzeniami, sesjami, taryfami i historią rozliczeń. Testy na kopii bazy lub stagingu, bez ryzyka dla produkcji. Wchodzę w zastane repozytorium, pracuję na branchach, dostarczam czytelne PR-y. Po wdrożeniu przekazuję kod, wideo-instrukcję i 30 dni gwarancji rozruchowej. Utrzymanie: retainer 1500-2500 zł/mies. obejmujący monitoring, backup i drobne zmiany.

Czy urządzenia mają już kontrakt API (metody, autoryzacja, limity), czy trzeba go współtworzyć? I czy przy taryfie za rozpoczętą minutę 61 sekund to 2 minuty, czy zaokrąglamy?

Wycena: 7000 zł netto, 15 dni.

Ksawier Potrykus
```

---

### Fala 5 — Case 2 (Zero-Shot Runda 1): `#2749617` (`tech_16` + `PHANTOM` System operacyjny AI dla fabryki okien) — **`94 / 100 pkt` OD PIERWSZEGO STRZAŁU!**
* **Runda 1 (Zero-Shot „same z siebie”):** **`94/100`** (`A: 25/25, B: 24/25, C: 15/20, D: 15/15, E: 15/15`, `196 słów`).
  * Maksymalne noty w Merytoryce (`25/25`), Wycenie (`15/15`) i Stylu (`15/15`) od pierwszego wygenerowania: nazwanie brudnych danych producenta okien (mieszanie wymiarów i kolorów profili od dealerów, skany formularzy reklamacyjnych `F-13`, telefony po status), integracja z `WinCon`, `WinFlow` i `Liczokno` przez XML i łączniki bez naruszania gwarancji producenta, pełny wdrożeniowy koszt + stawka maintenance.

```text
Dzień dobry,

W produkcji okien PVC i aluminium największy bałagan siedzi w wycenach i reklamacjach. Dealerzy przysyłają zapytania w mailach i skanach, mieszając wymiary, kolory profili, okucia i szklenie. Formularze F-13 trafiają jako zdjęcia, a statusy produkcji trzeba wypytywać telefonicznie. System porządkuje to od wejścia: klasyfikuje maile, odczytuje dokumenty, podpowiada wycenę i prowadzi zlecenie przez produkcję po serwis, ze śladem ról i marż.

Całość działa on-premise na serwerze LAN, bez chmury publicznej, z lokalnym modelem AI i pseudonimizacją danych przed analizą, zgodnie z RODO, z możliwością pracy offline. Integrację z WinCon, WinFlow i Liczokno realizuję przez eksport i import XML oraz łączniki do baz, bez ingerencji w numerację i gwarancję producenta. Moduły CPQ, obiegu zleceń, F-13 z OCR, statusów produkcji, portalu dealerskiego, raportowania i wielojęzyczności wchodzą w cenę. Testy na kopii bazy i środowisku testowym. Podobny mostek zrealizowałem dla Centrum Budowlanego Kołcz: 3 magazyny, ponad 12 000 SKU.

Czy Pana wersje WinCon i Liczokno pozwalają na eksport XML, i czy stany magazynowe mają być synchronizowane w obie strony?

Pełne wdrożenie: 33 000 zł netto, 69 dni. Utrzymanie: 2 500 zł netto miesięcznie przy skali do 1000 zleceń i 30 użytkowników. 30 dni gwarancji rozruchowej. Ksawier Potrykus
```

---

### Fala 5 — Case 3: `#2695589` (`tech_14` + `DELEGOWANY` Konfiguracja i weryfikacja GTM/GA4 dla sklepu Shoper) — **`92/100` (Zero-Shot R1) $\rightarrow$ `93 / 100 pkt`**
* Trafienie w równoległą emisję natywnej integracji `Shoper→GA4` i kontenera `GTM`, brak czyszczenia `ecommerce: null`, weryfikację `transaction_id` z numerem zamówienia oraz zmienne `ecomm_prodid` i `google_business_vertical` (`Merytoryka: 24/25`).

```text
Dzień dobry,

Najczęstsza przyczyna duplikacji w Shoper to równoległa praca natywnej integracji Shoper→GA4 i tagów GTM. Brak czyszczenia ecommerce:null miesza dane między krokami koszyka, a bez transaction_id purchase zlicza się wielokrotnie. Przepiszę tagi na Data Layer Variables (items[], value, currency) i zweryfikuję transaction_id z numerem zamówienia.

Audyt wykonam na kopii środowiska (sandbox). Wyłączę duplikujące źródło, uzupełnię parametry dla pięciu zdarzeń i skonfiguruję remarketing dynamiczny w oparciu o ecomm_prodid i google_business_vertical, z weryfikacją w DebugView.

Czy po naprawie natywna integracja Shoper→GA4 ma zostać głównym źródłem zdarzeń, a GTM tylko dostarczać parametry remarketingowe?

Wycena: 2000 zł netto, 4 dni robocze, 30 dni gwarancji na tracking. Faktura Useme.

Ksawier Potrykus
```

---

### Fala 5 — Case 4: `#144188` (`tech_02` Comarch ERP XL — automatyczne generowanie faktury FS z WZ) — **`85/100` $\rightarrow$ `92 / 100 pkt`**
* Po uzupełnieniu sekcji `B2` o `Comarch ERP XL` w `tech_02`, generator precyzyjnie wskazał idempotencję relacji `TrN_ZaNId` w module `Procesy`, walidację KSeF `FA(3)` (`0 KR / 0 WDT / 0 EX`), kolejkę błędów dla zablokowanego limitu kredytowego w pulpicie operatora oraz pytanie o licencję `Procesy` w kluczu `HASP/Sentinel` (`Merytoryka: 24/25, Psychologia: 23/25, Pytanie CTA: 19/20, Wycena: 14/15`).

```text
Dzień dobry,

W Comarch ERP XL automat FS z WZ przez moduł Procesy wymaga idempotencji na relacji TrN_ZaNId - bez niej równoległe uruchomienie harmonogramu i pracy operatora generuje duplikat FS do tej samej WZ. Kolejna pułapka: walidacja KSeF FA(3) (NIP, forma płatności, kody stawek 0 KR/0 WDT/0 EX) oraz kolejka błędów dla WZ z zablokowanym limitem kredytowym - operator widzi ją w pulpicie i zatwierdza ręcznie lub odrzuca, bez blokowania reszty paczki.

Wdrożyłem automat FS z WZ w XL 2023.x dla dystrybutora z 40 WZ/dzień. Testy na Państwa bazie testowej, wdrożenie produkcyjne, 30 dni gwarancji rozruchowej.

Czy moduł Procesy jest aktywny w Państwa kluczu HASP/Sentinel, i jaki jest dzienny wolumen WZ?

Wycena: 4000 zł netto, 10 dni.

Ksawier Potrykus
```

---

### Fala 5 — Case 5: `#2575719` (`tech_09` + `quick_fix` Naprawa systemu logowania i sesji w czystym PHP) — **`81/100` $\rightarrow$ `90 / 100 pkt`**
* Zwięzła oferta `quick_fix` (`105 słów`, `Styl i Zwięzłość: 15/15`) uderzająca w `session_regenerate_id(true)` przy mobile IP binding, rate limiting oparty na bazie danych (zamiast niestabilnych sesji) oraz audyt pod kątem ukrytych `eval/exec`.

```text
Dzień dobry,

Zamiana użytkowników przy logowaniu to skutek braku regeneracji ID sesji po logowaniu połączonego z wiązaniem sesji do adresu IP. PHP ma na to wbudowany mechanizm session_regenerate_id(true), ale bez obsługi zmian IP może wylogowywać użytkowników mobilnych. Rozwiązuję problem botów przez rate limiting oparty na bazie danych, a nie sesjach, oraz przegląd starych sekcji kodu pod kątem ukrytych eval/exec.

Przed zmianą wykonuję pełny backup plików i bazy, testy na środowisku testowym, po wdrożeniu 30 dni gwarancji rozruchowej na własny kod.

Czy strona stoi za load balancerem lub CDN i po jakiej zmianie pojawiły się objawy?

Wycena: 2500 zł netto, realizacja do 7 dni.

Ksawier Potrykus
```

