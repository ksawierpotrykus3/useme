# Baza Realizacji i Dowodów Inżynierskich (Portfolio B2B)
**Hierarchia Priorytetów Portfela:** Zgodna z badaniem 406 zleceń Useme (Popyt AI: 50%, API: 61%, Czerwony Ocean WP: odrzucony)  
**Zasada Ksawiera:** ZERO BLUEPRINTÓW, ZERO SZABLONÓW, 100% PRAWDZIWEJ INŻYNIERII  

---

## 1. ZASADY UŻYCIA PORTFOLIO W OFERTACH (ŻELAZNE REGUŁY)

1. **CAŁKOWITY ZAKAZ SZABLONÓW I PŁATNYCH BLUEPRINTÓW:**
   Nigdy nie proponujemy płatnych analiz czy blueprintów (100% porażek w historii Useme). Klient chce widzieć działający efekt, a nie kupować dokumentację od obcej osoby.
2. **BEZWZGLĘDNY WARUNEK DOPASOWANIA (ZAKAZ ŁOŻA PROKRUSTESA I ZAKAZ PUSTYCH FRAZESÓW „MAMY DOŚWIADCZENIE"):**
   - Jeśli któreś z poniższych case studies pasuje wprost do zlecenia (np. faktury/OCR do faktur, BaseLinker/Allegro do e-commerce, Three.js do 3D, CNC/G-code do maszyn CNC, Klinika Doktor Monika do systemów medycznych/rezerwacyjnych), wpleć z niego **1 konkretne zdanie z liczbą lub faktem technicznym**.
   - JEŚLI ZLECENIE NIE PASUJE WPROST – **CAŁKOWITY ZAKAZ** wklejania obcych historii ORAZ **CAŁKOWITY ZAKAZ** pisania pustych, szablonowych zdań typu *„Mamy doświadczenie w łączeniu platform sprzedażowych z systemami produkcyjnymi"* czy *„Zrealizowaliśmy wiele podobnych projektów"*. Jeśli nie masz twardego case study z liczbą pasującego do domeny, po prostu **pomiń zdanie o swoim doświadczeniu** — Twoim dowodem kompetencji jest sama diagnoza problemu i opis rozwiązania!
3. **DECYZJA ODWRACALNA (SANDBOX-FIRST ZAMIAST DARMOWYCH KONSULTACJI):**
   Nigdy nie proś klienta o wysyłanie swoich plików produkcyjnych do „darmowego przemielenia przed umową" i nigdy nie tłumacz się ze swoich reguł wewnętrznych („nie przekażę kodu produkcyjnego"). Zamiast tego daj twarde bezpieczeństwo inżynierskie: wszystkie wstępne testy i importy wykonujemy na kopii bazy lub w odseparowanym środowisku testowym (sandbox), bez dotykania żywej produkcji klienta.
4. **BEZPIECZEŃSTWO WDROŻENIA I 30 DNI GWARANCJI:**
   Standardowo gwarantujemy 30 dni asysty rozruchowej na własny kod po wdrożeniu (z wyłączeniem przyszłych zmian po stronie zewnętrznych dostawców API).

---

## 2. POSEGREGOWANA BAZA PORTFOLIO WG PRIORYTETÓW RYNKOWYCH

```
┌────────────────────────────────────────────────────────────────────────┐
│               HIERARCHIA PORTFOLIO KSAWIERA I MAKSYMILIANA             │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 1: ABSOLUTNY PRIORYTET (Generuje 80% wartości rynku Useme)        │
│  1. AI Document & Vision Pipeline (n8n + LLM + OCR + Walidacja Grosza)  │
│  2. API & Marketplace Integration Engine (BaseLinker / Allegro / ERP)  │
│  3. Scraping z omijaniem WAF (Patchowany TLS/JA4 + HTTP/2 + Proxy)     │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: WYSOKOMARŻOWE NISZE SPECJALISTYCZNE (Brak konkurencji, wysoka marża)
│  4. Konfigurator Produktowy 3D / WebGL (Three.js + Draco + 60 FPS iOS) │
│  5. Panel Hurtowy B2B & Dynamiczne Cenniki (IdoSell / Shopify B2B)     │
│  6. System Rezerwacji i Zarządzania (Referencja Prezesa Dominika Łyżwy) │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: WSPIERAJĄCE / WYCIĘTE                                          │
│  7. Szybki Web Dev Headless / Next.js (PageSpeed 95-99, Staging)       │
│  8. Aplikacje Mobilne MVP (Kotlin / Android / Flutter)                 │
│  ❌ Prosty WordPress / Elementor / Wizytówki -> CAŁKOWICIE WYCIĘTE      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### TIER 1: ABSOLUTNY PRIORYTET (AI, API, AUTOMATYZACJA)

#### Projekt 1: Enterprise Autonomous Document Pipeline & Automatyzacja ERP (Comarch Optima / Comarch ERP XL / AI OCR / n8n / KSeF)
- **Rynkowy popyt Useme:** 50.0% najnowszych zleceń (AI + automatyzacja + ERP).
- **Triggery zapytania:** ai, llm, chatgpt, openai, n8n, make, ocr, faktury, obieg dokumentów, automatyzacja, rag, comarch optima, comarch erp xl, moduł procesy, ksef
- **Wąskie gardło:** Modele LLM halucynują i gubią grosze przy sumowaniu podatku VAT na nieregularnych skanach; chmurowy Make generuje gigantyczne koszty operacji przy pętlach po pozycjach dokumentu; w Comarch ERP XL równoległe uruchomienie harmonogramu modułu Procesy i pracy operatora bez idempotencji `TrN_ZaNId` generuje duplikaty FS do tej samej WZ.
- **Inżynierskie rozwiązanie:** Rozdzielenie semantyki od matematyki oraz 3 strumieni dokumentów (KSeF XML / cyfrowy PDF z warstwą tekstową / skany i zdjęcia z telefonów z preprocessingiem obrazu i progiem pewności). Model Vision dokonuje wyłącznie ustrukturyzowanej ekstrakcji do JSON, a deterministyczny skrypt waliduje sumy netto/VAT/brutto z tolerancją 1–2 groszy (ustawa o VAT), deduplikuje po kluczu `NIP + numer dokumentu + typ` oraz sprawdza rachunek na Białej Liście MF. Całość na self-hosted n8n bez opłat za operację. Zrealizowane na wolumenie 3500+ dokumentów z precyzją 99.4%, a w Comarch ERP XL 2023.x – wdrożenie bezpośrednie B2B zespołu (poza Useme, objęte NDA – zanonimizowany schemat procesu i zapytania SQL dostępne do wglądu na priv): automat generowania FS z WZ w module Procesy dla dystrybutora B2B (45 WZ/dzień, redukcja duplikatów do 0 i skrócenie obsługi o 85%).
- **Bezpieczeństwo wdrożenia (Sandbox-First):** Pierwsze testy i importy wykonujemy na kopii bazy / buforze testowym, bez zatrzymywania bieżącego fakturowania.

#### Projekt 2: API & Marketplace Integration Engine (BaseLinker / Allegro / Otomoto / Shopify / ERP)
- **Rynkowy popyt Useme:** 61.0% najnowszych zleceń (Integracje API i webhooki).
- **Triggery zapytania:** api, baselinker, allegro, otomoto, shopify, erp, integracja, webhook, synchronizacja, stany magazynowe
- **Wąskie gardło:** Błędy limitu zapytań (429 Rate Limit) blokujące konto sprzedawcy; gubienie webhooków przy chwilowej niedostępności serwera; nadsprzedaż towaru (overselling).
- **Inżynierskie rozwiązanie:** Asynchroniczny potok z algorytmem Leaky Bucket sterującym tempem zapytań, buforowanie kolejki w Redis, rozproszone blokady atomowe (Redlock) rezerwujące stany w momencie przejścia do kasy (soft locking), transakcje idempotencyjne zapobiegające duplikatom.
- **Zweryfikowany dowód transakcyjny:** Case Centrum Budowlane Kołcz (5 500 PLN netto) – wielomagazynowy mostek e-commerce z ERP Enova365/BaseLinker (synchronizacja 3 magazynów i ponad 12 000 SKU z kontrolą `warehouse_type`, blokadami stanów i regułami priorytetów magazynów realizujących); Case Arkadiusz (5 500 PLN netto) – integracja PrestaShop z Allegro REST API; Case Gardd Shopify B2B – obsługa Shopify Locations i wielomagazynowych cenników B2B.
- **Bezpieczeństwo wdrożenia (Sandbox-First):** Synchronizacja testowana najpierw w trybie dry-run / na środowisku testowym przed przepięciem na produkcyjne stany magazynowe.

#### Projekt 3: Low-Latency Scraping Engine & WAF Bypass (OLX / Otomoto / Allegro / Google Maps)
- **Rynkowy popyt Useme:** Ciągły popyt w kategorii oprogramowania i skryptów (średnia wycena: 6 888 zł).
- **Triggery zapytania:** scraping, scraper, bot, crawler, olx, otomoto, allegro, monitorowanie, pobieranie danych
- **Wąskie gardło:** Cloudflare Bot Management i WAF blokują skrypty po powtarzalnym odcisku TLS i IP w kilka sekund (błędy 403); przeciążenie bazy danych duplikatami.
- **Inżynierskie rozwiązanie:** Patchowany klient HTTP (`curl_cffi`) emulujący pełny handshake TLS/JA4 oraz ramki HTTP/2 (lub odpytywanie wewnętrznych endpointów GraphQL/JSON zamiast ciężkiego Selenium), rotacja sesyjnych residential IP, filtry Blooma w Redis do natychmiastowej deduplikacji bez obciążania dysku. Czas detekcji: poniżej 3 minut 40 sekund od wystawienia ogłoszenia, 99.8% skuteczności bypassu.
- **Zweryfikowany dowód:** Case SmartCare OLX Bot (czas reakcji poniżej 3 min 40 s, filtr Blooma w Redis, brak banów IP).

---

### TIER 2: WYSOKOMARŻOWE NISZE SPECJALISTYCZNE (BRAK KONKURENCJI)

#### Projekt 4: Ultra-High Performance 3D Configurator (Three.js / WebGL / Draco / Basis)
- **Rynkowy popyt Useme:** Zlecenia 4 500 – 15 000 zł przy zerowej konkurencji (brak programistów 3D na platformie).
- **Triggery zapytania:** konfigurator, 3d, three.js, webgl, personalizator, modele 3d, meble 3d, r3f
- **Wąskie gardło:** Surowe modele CAD (40–60 MB) oraz brak zwalniania pamięci (`dispose()` na starych geometriach i materiałach przy każdej zmianie parametru przez użytkownika) przepełniają pamięć VRAM i crashują Safari na iOS; spadek FPS poniżej 20; brak czystego eksportu wybranej konfiguracji (JSON: wymiary, materiał, SKU, wyliczona cena) do koszyka sklepu (PrestaShop/WooCommerce).
- **Inżynierskie rozwiązanie i dowód:** Odseparowanie stanu konfiguracji od warstwy sceny 3D, kompresja geometrii Draco i tekstur KTX2/Basis Universal (-92% wagi, z 48 MB do 3.8 MB), manualny garbage collection GPU (`dispose()` na buforach), stabilne 60 FPS na smartfonach.

#### Projekt 4B: Maszyny CNC, Postprocesory G-code & Automatyzacja Produkcji (CAD/CAM / Stolarnie / Obróbka Blach i Drewna)
- **Triggery zapytania:** cnc, postprocessor, postprocesor, g-code, dxf, cam, cad, topsolid, lvd, amada, trumpf, formatki meblowe, rozkrój płyt, oklejanie obrzeży, produkcja na wymiar
- **Wąskie gardło:** Gotowe darmowe programy CAM generują kod pod jeden typ sterownika (np. Amada zamiast LVD/ADTECH), duplikują obroty głowicy Auto-Index dla każdego odcinka osobno i gubią numerację mikrowiązań (micro-joints); w stolarniach zamówienia na wymiar z Allegro przychodzą w dowolnym zapisie (mieszanie `cm` i `mm`, brak wskazanego obrzeża lub kierunku usłojenia).
- **Twardy dowód inżynierski:** Praktyczne doświadczenie maszynowe w zespole (budowa własnej maszyny CNC od zera, pisanie deterministycznych postprocesorów G-code/NC, optymalizacja ścieżek narzędzia i integracje z systemami rozkroju / TopSolid'Automation API) oraz automatyczna normalizacja wymiarów (`cm -> mm`) i walidacja kompletności oklejania przed wrzuceniem zlecenia na pilarkę/CNC.

#### Projekt 5: Panel Hurtowy B2B & Dynamiczne Cenniki (IdoSell / Shopify / WooCommerce B2B)
- **Rynkowy popyt Useme:** Stabilny popyt B2B o wycenach 5 000 – 12 000 zł.
- **Triggery zapytania:** idosell, panel b2b, cennik hurtowy, hurtownia, rabaty b2b, shoper b2b
- **Wąskie gardło:** Wyciek cen hurtowych do widoku detalicznego w kodzie JS; zacinanie bazy przy przeliczaniu progów rabatowych dla tysięcy SKU.
- **Inżynierskie rozwiązanie:** Dedykowany middleware cenowy na serwerze, automatyczna walidacja NIP w GUS/VIES w 90 sekund, transakcyjne cache'owanie progów marżowych w Redis, brak możliwości podejrzenia cen hurtowych w przeglądarce.
- **Zweryfikowany dowód:** Case Gardd Shopify B2B (3 929 PLN netto — wielomagazynowe Shopify Locations i dynamiczne cenniki B2B) oraz Case Paweł IdoSell Dropshipping (1 600 PLN netto).

#### Projekt 6: Mission-Critical Clinical Booking & Architecture (Klinika Doktor Monika – Dominik Łyżwa)
- **Rynkowy popyt Useme:** Dedykowane serwisy i systemy operacyjne firm (wyceny 8 000 – 25 000 zł).
- **Triggery zapytania:** rezerwacje, klinika, medyczna, kalendarz, wizyty, system operacyjny, gabinety
- **Wąskie gardło:** Kolizje terminów (double-booking aparatura + lekarz + sala); paniczny lęk klienta przed przestojem i awarią.
- **Inżynierskie rozwiązanie:** Twarde blokady transakcyjne w PostgreSQL (SELECT FOR UPDATE) na czas płatności, macierz zależności zasobów, praca wyłącznie na serwerze stagingowym (zero przestoju głównej domeny).
- **Twardy Fakt Transakcyjny (>95% pewności):** Zlecenie Doktor Monika sp. z o.o. (12 100,00 PLN netto, 11 083,52 PLN wypłacone na konto 22.06.2026).
- **Główny Dowód:** Oficjalna referencja Prezesa Kliniki Dominika Łyżwy na profilu Useme: zero kolizji terminów przez 18 miesięcy, wyłapanie luk architektonicznych przed kodowaniem, pełen spokój procesowy zleceniodawcy.

---

### TIER 3: WSPIERAJĄCE / WYCIĘTE

#### Projekt 7: High-Speed Web Optimization & Headless (Next.js / czysty kod)
- **Zastosowanie:** Jako element większych projektów e-commerce/B2B (PageSpeed 95-99, LCP < 1.1s).
- **Zasada wdrożenia:** Zawsze środowisko stagingowe – obecna strona i maile klienta działają bez zakłóceń do momentu odbioru.

#### Projekt 8: Aplikacje Mobilne Offline-First, Przejęcia Legacy (Kotlin / Flutter / iOS) & Subskrypcje B2B (Wdrożenia bezpośrednie B2B pod NDA)
- **Triggery zapytania:** kotlin, android, ios, swift, flutter, react native, aplikacja mobilna, storekit, google play billing, revenuecat, offline, gabinet, przejazdy, gps
- **Wąskie gardło:** Zrywanie sesji i utrata wpisów przy braku zasięgu Wi-Fi/LTE (gabinety, teren); odrzucenia w Google Play przez brak deklaracji `foregroundServiceType` lub 6-godzinny limit `dataSync` na Androidzie 15; brak natywnego wsparcia subskrypcji zespołowych B2B w RevenueCat.
- **Twardy dowód inżynierski (Bezpośrednie kontrakty B2B zespołu poza Useme, objęte NDA — zanonimizowane wycinki kodu i architektury gotowe do pokazania na priv):** Przejęcia i refaktoryzacje zastanych aplikacji Android/Kotlin (migracja z `AsyncTask` na `Coroutines` i `WorkManager`, audyty `foregroundServiceType="location"` pod Android 14/15 bez przepisywania kodu od zera), architektury mobilne Offline-First z lokalną zaszyfrowaną bazą `SQLCipher` (100% ciągłości pracy gabinetu bez Wi-Fi i doganianie synchronizacji po powrocie łącza, wzorzec sprawdzony m.in. w systemie dla Kliniki Doktor Monika – 18 mies. bez kolizji) oraz customowe backendy subskrypcji B2B (`StoreKit 2` / `Google Play Billing` / `RevenueCat` z deduplikacją po `event_id`).

#### Projekt 9: Przejęcia Systemów Legacy PHP/MySQL, Bazy SQL Server (WAPRO MAG / Subiekt), Analityka GTM/GA4 & Hurtownie Danych (Wdrożenia bezpośrednie B2B pod NDA)
- **Triggery zapytania:** php, mysql, mssql, sql server, wapro, subiekt, sfera, procedury składowane, bigquery, etl, hurtownia danych, przejęcie kodu, sesje, logowanie, gtm, ga4, datalayer, shoper
- **Twardy dowód inżynierski (Bezpośrednie kontrakty B2B zespołu poza Useme, objęte NDA — zanonimizowane procedury T-SQL, kontenery DataLayer i wycinki kodu gotowe do wglądu na priv):** Bezpieczne przejęcia zastanych sklepów B2B w PHP/MySQL z integracją `MSSQL / WAPRO MAG` i `Subiekt Sfera` (optymalizacja procedur składowanych T-SQL, zastąpienie brakującego `SQL Server Agent` na edycji Express własnym atomowym schedulerem z blokadami `UPDATE ... OUTPUT`, kolejkowanie zapisów Sfery COM eliminujące deadlocki na `tw__Towar` i `dok__Dokument` dla >12 000 SKU), naprawy bezpieczeństwa i sesji w aplikacjach PHP bez frameworka (eliminacja `session fixation` i bot-floodu na serwisach z >15 000 sesji/dobę), audyty i naprawy `GTM / GA4 DataLayer` w e-commerce (eliminacja duplikacji `purchase` i naprawa remarketingu dynamicznego w sklepach Shoper/WooCommerce z >2 500 zamówień/mies., zgodność transakcji 99,2%) oraz potoki ETL w Pythonie do `Google BigQuery` (`Cloud Run Jobs`, ładowanie przez `Storage Write API` i inkrementalny `MERGE` po kluczach biznesowych).

#### ❌ CZEGO KSAWIER NIE ROBI I CO WYCIĘTO Z PORTFOLIO:
1. **Zero prostych stron na WordPressie / Elementorze:** Udział w rynku spadł do 16.9%, konkurencja wynosi 150 osób, stawki to 200 zł. Nie marnujemy czasu ani energii na budowanie takiego portfolio.
2. **Zero teoretycznych blueprintów / płatnych audytów:** 100% porażek w historii konta. Klient płaci za działający kod, a nie za papier.
