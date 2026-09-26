# STRATEGIA ZLECENIODAWCY (MYSTERY SHOPPING, TEORIA GIER I KONTRWYWIAD)
## Zaawansowane Badanie Rynku, Dekonstrukcja Konkurencji i Cykl Obrony Know-How
**Dokument:** `STRAT-08-MYSTERY-SHOPPING-MASTER-V2-HARDENED`  
**Data opracowania:** 23 września 2026  
**Autorzy:** Ksawier Potrykus & Maksymilian (Tandem Inżynierów Oprogramowania)  
**Weryfikacja:** Przeprowadzona przez niezależnych subagentów (OpSec Auditor & Game Theory Strategist)  
**Baza analityczna:** 551 zleceń Useme (56 wygranych z `wygrane_oferty_historia.json`, 406 zamkniętych z `badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json`)

---

# 1. WNIOSKI Z AUDYTU STRATEGII: DLACZEGO PIERWOTNY PLAN WYMAGAŁ POPRAWEK?

Niezależny audyt subagentów potwierdził fundamentalną trafność koncepcji odwrócenia asymetrii rynkowej, ale ujawnił **3 krytyczne błędy (Blind Spots)**, które w pierwotnej wersji spaliłyby tożsamość zleceniodawcy:

1. **Pułapka Żargonu Programistycznego (Self-Doxxing):**  
   Prawdziwy dyrektor hurtowni czy fabryki nie pisze w ogłoszeniu o *„Draco texture compression”*, *„Playwright Stealth / curl_cffi”* ani *„FastAPI vs Livewire vs Inertia”*.  
   Użycie takiego słownictwa natychmiast demaskuje zlecającego jako programistę / konkurenta wyciągającego darmowy consulting. Doświadczony senior odmówi darmowej odpowiedzi lub zażąda płatnych warsztatów (3 500 PLN).
2. **Ryzyko Konta-Widma (Hire Rate = 0%):**  
   Wystawienie kilku zleceń o budżetach 6k–14k PLN i zamknięcie wszystkich bez wyboru wykonawcy uruchamia algorytmy antyfraudowe Useme i oznacza konto jako „Ghost Requester”.
3. **Zagrożenie Kontrwywiadowcze (Teoria Gier):**  
   Software house'y na Useme stosują dokładnie te same techniki – wystawiają zlecenia, by badać ceny i wyciągać architekturę od freelancerów pod własne przetargi enterprise.

Poniższy dokument stanowi **utwardzoną (hardened) wersję operacyjną**, eliminującą powyższe ryzyka.

---

# 2. PANCERNY PROTOKÓŁ BEZPIECZEŃSTWA (OPSEC 2.0)

### KROK 1: Uwiarygodnienie Konta – Manewr „Seed Contract” (Koszt: ~120–150 PLN)
Nigdy nie wystawiaj drogich zleceń badawczych z pustego, świeżego konta:
1. Zarejestruj profil zleceniodawcy na odrębny podmiot gospodarczy (inny NIP, inny e-mail, dedykowana karta SIM).
2. Opublikuj mikrozlecenie o autentycznym charakterze:  
   *„Optymalizacja i formatowanie szablonu dokumentu PDF / audyt wizualny formularza”* (Budżet sztywny: 120–150 PLN).
3. Wybierz wykonawcę (np. studenta/grafika), opłać zlecenie przez Useme i wystaw 5 gwiazdek.
4. **Zysk operacyjny:** Konto uzyskuje status **„Zweryfikowany Płatnik”**, wskaźnik **Hire Rate = 100%** i ocenę **5.0/5.0**. Moderatorzy Useme traktują Cię priorytetowo, a software house'y widzą wypłacalnego klienta.

### KROK 2: Sprzętowa i Sieciowa Izolacja Środowiska
* **Anti-Detect Browser:** Używaj profilu w **Dolphin Anty** lub **AdsPower** (zmienne Canvas Hash, AudioContext, WebGL Renderer, inna rozdzielczość niż sesja Ksawiera), aby systemy telemetryczne nie powiązały konta zleceniodawcy z kontem wykonawcy.
* **Separacja IP:** Korzystaj wyłącznie z mobilnego połączenia LTE/5G (zmienny adres IP per sesja) lub dedykowanego polskiego proxy mobilnego.
* **Święta zasada:** **ZERO ofert z konta `Ksawier Potrykus` pod zleceniem badawczym.**

### KROK 3: Płatny Mikro-Etap zamiast Chamskiego Anulowania
Po zebraniu 15–30 ofert z danego zlecenia badawczego:
* Zamiast bezdusznie zamykać zlecenie powodem *„Projekt wstrzymany”* (co obniża wskaźnik zatrudnienia do 50%), wybierz **jednego, najlepszego architekta** i zaoferuj mu mini-umowę na Useme:  
  *„Płatna konsultacja architektoniczna i rozpisanie specyfikacji wdrożeniowej (200–300 PLN brutto)”*.
* **Podwójny profit:**  
  1. Konto zachowuje wzorowy wskaźnik Hire Rate.  
  2. Ksawier otrzymuje od czołowego eksperta rynkowego legalny, profesjonalny, wielostronicowy dokument architektoniczny (blueprint), z którego wiedzę natychmiast wdrażamy do bota!

---

# 3. PRZEKŁAD ZLECEŃ NA JĘZYK BIZNESOWY (ELIMINACJA SELF-DOXXINGU)

Zastępujemy żargon programistyczny opisem **realnego bólu biznesowego**. W ten sposób zmuszamy prawdziwych ekspertów, by **sami dobrowolnie zaproponowali stack i rozwiązania brzegowe**, aby udowodnić swoją wyższość nad botami:

---

### ZLECENIE BADAWCZE 1: AI, OBIEG DOKUMENTÓW I OCR (TIER A)
* **Kategoria:** `Programowanie i IT -> Oprogramowanie`
* **Tytuł:** `Automatyzacja wprowadzania faktur kosztowych i dokumentów WZ do systemu magazynowego (OCR + weryfikacja kwot)`
* **Budżet:** `Do negocjacji` (lub wpisz `8 500,00 PLN`)
* **Termin:** `14 dni`

#### Treść do wklejenia:
```text
Dzień dobry,

Zlecimy wdrożenie automatycznego systemu odczytu i wprowadzania dokumentów zakupowych (faktury, dokumenty dostaw WZ) w firmie handlowo-produkcyjnej (obsługujemy ok. 1000-1500 dokumentów w miesiącu).

Obecny problem:
Dokumenty spływają jako załączniki PDF na dedykowaną skrzynkę e-mail. Część to czyste pliki z programów księgowych, ale duża część to skany i zdjęcia z telefonów o różnej jakości i zagięciach. Zespół traci kilkadziesiąt godzin miesięcznie na ręczne przepisywanie danych i pozycji towarowych.

Oczekiwany rezultat:
1. Automatyczne pobieranie załączników ze skrzynki pocztowej lub wskazanego folderu.
2. Odczyt danych nagłówkowych (dane sprzedawcy, NIP, numer, data, numer konta bankowego) oraz pozycji tabelarycznych (nazwa towaru, ilość, cena netto, stawka VAT).
3. Bezwarunkowa zgodność matematyczna: suma pozycji musi co do grosza zgadzać się z kwotą podsumowania dokumentu. Jeśli cokolwiek się nie zgadza, dokument ma trafić do kolejki ręcznego sprawdzenia z powiadomieniem zespołu.
4. Automatyczna weryfikacja statusu NIP na Białej Liście podatników VAT.
5. Przygotowanie danych w formacie JSON / gotowym do zasilenia naszego systemu ERP.

Zależy nam na rozwiązaniu stabilnym, które nie generuje ogromnych comiesięcznych rachunków za przetwarzanie danych i nie wymaga płatnych platform chmurowych, jeśli można to uruchomić na naszym serwerze.

W ofercie prosimy o:
- Informację, jak planujesz rozwiązać problem trudnych, niewyraźnych skanów i tabel wielostronicowych,
- Rekomendowane podejście i szacowany koszt utrzymania systemu (np. licencje, serwer, koszty zapytań),
- Wycenę przygotowania wersji pilotażowej oraz docelowego wdrożenia,
- Przykłady podobnych systemów, które już z powodzeniem wdrożyłeś.
```

---

### ZLECENIE BADAWCZE 2: INTEGRACJE ERP, BASELINKER & MARKETPLACE
* **Kategoria:** `Programowanie i IT -> Oprogramowanie`
* **Tytuł:** `Szybka synchronizacja stanów magazynowych i cen między Subiektem a BaseLinkerem (duża baza produktów)`
* **Budżet:** `Do negocjacji` (lub wpisz `7 000,00 PLN`)
* **Termin:** `14 dni`

#### Treść do wklejenia:
```text
Dzień dobry,

Szukamy doświadczonego programisty / integratora do przygotowania niezawodnego modułu synchronizacji stanów magazynowych i cen pomiędzy naszym systemem Subiekt a kontem BaseLinker (sprzedaż wielokanałowa Allegro/sklep).

Główne wyzwanie:
Posiadamy bazę ponad 40 000 produktów. Standardowe rozwiązania, z których korzystaliśmy, powodują zawieszanie pracy programu magazynowego w ciągu dnia lub generują zbyt dużo zapytań, przez co stany na portalach aktualizują się z wielogodzinnym opóźnieniem i dochodzi do sprzedaży towaru, którego nie ma na stanie.

Wymagania:
1. Sprawdzanie i wysyłanie tylko tych produktów, w których stan lub cena faktycznie uległy zmianie od ostatniego sprawdzenia (częstotliwość co kilka minut).
2. Prawidłowa obsługa wariantów produktów i kodów EAN.
3. Odporność na chwilowe braki internetu w magazynie – system musi automatycznie ponawiać próby i nie gubić danych.
4. Pobieranie zamówień z BaseLinkera z zakładaniem rezerwacji towaru w Subiekcie.

W ofercie prosimy o podanie:
- Twojego doświadczenia w integracjach z Subiektem i BaseLinkerem przy dużych bazach produktów,
- Jak technicznie planujesz rozwiązać problem, aby synchronizacja nie spowalniała pracy bazy w firmie i mieściła się w limitach BaseLinkera,
- Czasu realizacji i szacunkowego kosztu wdrożenia.
```

---

### ZLECENIE BADAWCZE 3: KONFIGURATOR 3D / THREE.JS
* **Kategoria:** `Programowanie i IT -> Aplikacje webowe`
* **Tytuł:** `Interaktywny podgląd 3D produktu na stronę internetową – meble modułowe (płynne działanie na telefonach)`
* **Budżet:** `Do negocjacji` (lub wpisz `9 500,00 PLN`)
* **Termin:** `14 dni`

#### Treść do wklejenia:
```text
Dzień dobry,

Zlecimy wykonanie konfiguratora 3D na stronę www dla producenta mebli modułowych / regałów customowych.

Funkcjonalność:
1. Klient na stronie w przeglądarce może zmieniać wymiary mebla (wysokość, szerokość, liczba półek), wybierać kolory płyt oraz rodzaj nóżek i uchwytów.
2. Zmiany parametrów widoczne na żywo w trójwymiarze, z możliwością obracania i przybliżania modelu.
3. Kluczowy wymóg: konfigurator musi działać idealnie płynnie na telefonach komórkowych (ponad 65% naszych klientów przegląda ofertę ze smartfonów) i ładować się w kilka sekund.
4. Dynamiczne przeliczanie ceny w oparciu o wybrane wymiary i materiały.
5. Możliwość pobrania podsumowania zamówienia ze zdjęciem skonfigurowanego mebla.

Dysponujemy podstawowymi modelami brył z programu produkcyjnego oraz próbkami dekorów.

W ofercie prosimy o:
- Linki do działających konfiguratorów 3D Twojego autorstwa, które możemy otworzyć na smartfonie,
- Informację, w jakiej technologii rekomendujesz to napisać i jak przygotowujesz modele, by nie obciążały telefonu,
- Wycenę oraz czas potrzebny na realizację.
```

---

### ZLECENIE BADAWCZE 4: ZAAWANSOWANY WEB SCRAPING I BOTY
* **Kategoria:** `Programowanie i IT -> Oprogramowanie`
* **Tytuł:** `Monitoring i codzienne pobieranie cen z portali ogłoszeniowych (problem z blokowaniem IP)`
* **Budżet:** `Do negocjacji` (lub wpisz `3 500,00 PLN`)
* **Termin:** `10 dni`

#### Treść do wklejenia:
```text
Dzień dobry,

Szukamy programisty Pythona do stworzenia niezawodnego skryptu do codziennego monitoringu ogłoszeń i cen z dwóch polskich serwisów branżowych (ok. 8 000 - 10 000 ogłoszeń na dobę).

Problem:
Nasz poprzedni prosty skrypt przestał działać – portale wprowadziły zaawansowane zabezpieczenia przed botami (po kilku zapytaniach pojawia się weryfikacja lub biały ekran i adres IP serwera zostaje zablokowany).

Oczekujemy:
1. Stabilnego pobierania danych w cyklu nocnym bez blokowania adresów IP.
2. Zbierania parametrów ogłoszenia: data, tytuł, cena, parametry techniczne, lokalizacja.
3. Zapisu do bazy danych (PostgreSQL) z oznaczaniem ogłoszeń wygasłych i zmian cen.
4. Całość spakowana w kontenerze (Docker), gotowa do uruchomienia na naszym serwerze.

W ofercie prosimy o:
- Informację, jak radzisz sobie z zaawansowanymi zabezpieczeniami i blokadami stron,
- Szacowany miesięczny koszt utrzymania infrastruktury (np. proxy) przy tej liczbie zapytań,
- Informację o zasadach gwarancji, jeśli portal zmieni układ strony,
- Wycenę i termin realizacji.
```

---

### ZLECENIE BADAWCZE 5: PORTAL ZAMÓWIEŃ B2B / MVP SAAS
* **Kategoria:** `Programowanie i IT -> Aplikacje webowe`
* **Tytuł:** `Dedykowany panel zamówień hurtowych B2B dla stałych klientów (wersja MVP)`
* **Budżet:** `Do negocjacji` (lub wpisz `14 000,00 PLN`)
* **Termin:** `14 dni`

#### Treść do wklejenia:
```text
Dzień dobry,

Poszukujemy zespołu lub doświadczonego developera do stworzenia od podstaw panelu zamówień hurtowych B2B dla naszych kontrahentów.

Główne funkcje MVP:
1. Logowanie i indywidualne poziomy rabatowe przypisane do firmy kontrahenta (różne cenniki dla różnych grup).
2. Wygodny katalog produktów z szybkim koszykiem (możliwość wklejenia listy kodów EAN lub importu zamówienia z pliku Excel/CSV).
3. Podgląd historii zamówień, statusów realizacji oraz pobieranie faktur w PDF.
4. Podział uprawnień po stronie klienta (pracownik składający zamówienie vs osoba decyzyjna akceptująca koszyk).
5. Panel administracyjny do zarządzania użytkownikami, limitami kupieckimi i importu bazy towarowej.

Zależy nam na czystej, nowoczesnej aplikacji webowej, w pełni responsywnej, z możliwością późniejszego połączenia przez API z systemem magazynowym.

W odpowiedzi prosimy o:
- Przykłady zrealizowanych paneli B2B lub aplikacji biznesowych,
- Rekomendację technologii i propozycji podziału wdrożenia na etapy,
- Wycenę wersji MVP oraz przewidywany czas realizacji.
```

---

# 4. KADENCJA MONITORINGU I TEORIA GIER (CO ILE SPRAWDZAĆ?)

Rynek Useme to gra dynamiczna o niepełnej informacji. Sztywne badanie co miesiąc jest błędem operacyjnym (wypala tożsamości i marnuje czas). Stosujemy **Model Hybrydowy**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ MODEL MONITORINGU RYNKOWEGO USEME_CORE                                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. KADENCJA BAZOWA (Baseline Periodic)                                                  │
│    - Częstotliwość: Raz na 90 dni (raz na kwartał).                                   │
│    - Działanie: Wystawienie 1 zlecenia badawczego z głównej niszy (np. ERP lub AI).   │
│    - Cel: Rekalibracja stawek w wycena_kalkulator.py i wykrycie nowych trendów.        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. KADENCJA ZDARZENIOWA (Event-Driven Triggers – Aktywacja Natychmiastowa)              │
│    Uruchamiamy badanie celowane TYLKO wtedy, gdy wystąpi jedna z anomalii:             │
│                                                                                        │
│    a) Wskaźnik odpowiedzi (Reply Rate) < 10% w oknie 20 ostatnich ofert Tier A         │
│       -> Oznacza: Konkurencja skopiowała nasze hooki lub drastycznie zmieniła ceny.    │
│                                                                                        │
│    b) Średnia liczba ofert per zlecenie rośnie o >40% w danym klastrze                 │
│       -> Oznacza: Pojawienie się nowego bota opartego na tanim LLM, który zalał rynek. │
│                                                                                        │
│    c) >50% ofert konkurencji pojawia się w czasie <3 minuty                           │
│       -> Oznacza: Zmiana dynamiki na scraping w czasie rzeczywistym.                   │
│                                                                                        │
│    d) >45% zleceń w danej kategorii kończy się statusem "bez wyboru wykonawcy"         │
│       -> Oznacza: Fala fałszywych zleceń konkurencji / brak realnego popytu.          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# 5. TARCZA OCHRONNA: JAK CHRONIĆ WŁASNE OFERTY PRZED SKOPIOWANIEM?

Gdy konkurencja bada naszą ofertę lub licytuje te same zlecenia, stosujemy 3 zasady ochronne:

1. **Zasada „Proof of Outcome, Not Proof of Blueprint”:**  
   W publicznej ofercie na Useme pokazujemy **rezultat biznesowy, diagnozę problemu i referencję** (np. *„Wdrożyliśmy dwukierunkową synchronizację 45k SKU bez blokowania tabel transakcyjnych z czasem odświeżania 3 minuty”*), ale **NIE ujawniamy nazwy własnej biblioteki, specyficznych zapytań SQL ani kodu hooków**.
2. **Unikanie Publicznej Dekompozycji Cenowej:**  
   Podajemy cenę ryczałtową za etap MVP lub widełki całościowe. Nigdy nie rozpisujemy: *„Moduł A: 4h = 560 zł, Moduł B: 8h = 1120 zł”* – bo konkurent natychmiast zaoferuje klientowi 10% rabatu na każdej pozycji.
3. **Znakowanie Autorskie (Canary Terminology):**  
   Wprowadzamy w tekstach unikalne nazewnictwo metodologiczne (np. *„Mechanizm bezpiecznego buforowania SafeQueue™”*). Jeśli konkurent to skopiuje, kompromituje się w oczach klienta, wklejając termin, do którego wyłącznie my posiadamy case study.

---

# 6. WDROŻENIE DO SILNIKA `useme_core`

1. **Tryb Obronny w `ai_pipeline.py` (`ocena_ryzyka_zwiadu`):**  
   Dodanie funkcji wykrywającej zlecenia, które wyglądają na zwiad konkurencji (nowy klient bez umów, pytania o konkretne biblioteki/kody, żądanie darmowego schematu blokowego). W takich zleceniach generator ofert blokuje ujawnianie nazw bibliotek i skupia się wyłącznie na referencjach biznesowych i cenie premium.
2. **Korekta w `wycena_kalkulator.py`:**  
   Wprowadzenie median pozyskanych z kwartalnych badań jako dynamicznych punktów odniesienia dla stawek minimalnych i optymalnych.
3. **Filtrowanie zleceń-widm w `storage.py`:**  
   Flagowanie zleceń, które zakończyły się bez wyboru zwycięzcy jako `RYNEK_WIDMO`, by nie zniekształcały statystyk naszych realnych przegranych.

---
*Dokument włączony do korpusu wiedzy strategicznej `badania/strategia/` z natychmiastową gotowością operacyjną.*
