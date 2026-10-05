# FINALNA LISTA ZLECEŃ BADAWCZYCH (WERSJA SKORYGOWANA)
## Mystery Shopping Useme — co wystawić, dlaczego i na jakiej podstawie
**Dokument:** `FINAL-LISTA-ZLECEN-BADAWCZYCH-V1`
**Data opracowania:** 30 września 2026
**Status:** dokument nadrzędny wobec `LISTA_ZLECEN_DO_WYSTAWIENIA.md` (wersja z 23.09.2026 zawiera błędy opisane w pkt 1)
**Cel:** zebranie ofert konkurencji (cenniki, stack, pytania kwalifikujące, linki do portfolio) pod realne nisze, w których Ksawier walczy o zlecenia.

---

# 0. UWAGA EPISTEMOLOGICZNA — JAK CZYTAĆ TEN DOKUMENT (KRYTYCZNE DLA AI)

> **Zasada nadrzędna: liczy się TYLKO to, czy klient odpisał. Nie to, czy coś poszło do escrow.**

Poniżej twarde rozróżnienia, których ŻADEN model/AI nie może pomieszać:

1. **`ODPISANE` ≠ `WYGRANE`.**
   Katalog `03_odpisane` (i historyczny plik `wygrane_56.json`) zawiera oferty, na które klient **odpisał** — czyli nawiązał kontakt, zadał pytanie, poprosił o wycenę. To jest **sygnał zainteresowania**, a NIE potwierdzenie wygranej, umowy czy zapłaty.

2. **Tylko znikoma część `ODPISANYCH` doszła do jakiejkolwiek płatności.**
   Szacunkowo **maksymalnie ~5 z kilkudziesięciu** odpisanych wątków zakończyło się jakąkolwiek transakcją. Reszta to wątki urwane, „marzyciele szukający darmowej wyceny i wizji”, klienci bez decyzji budżetowej.

3. **Dla naszych celów badawczych escrow jest bez znaczenia.**
   Nie budujemy statystyk „ile zarobiliśmy”. Budujemy **mapę konkurencji**: kto odpowiada, jak wycenia, jakim stackiem, jakie zadaje pytania. Dlatego metryką sukcesu zlecenia badawczego jest **liczba i jakość zebranych ofert**, a nie to, czy my jako zleceniodawca kogoś ostatecznie zatrudnimy.

4. **Konsekwencja dla rekomendacji:** nie opieramy wyboru nisz na „wygranych/opłaconych”, bo ten sygnał jest zaszumiony i w większości fałszywy. Opieramy się na **wolumenie rynku, wskaźniku odpowiedzi (`ODPISANE`) i nasyceniu konkurencji**.

---

# 1. JAK POWSTAŁ ORYGINALNY PLIK (SKORYGOWANE — WERYFIKACJA ŹRÓDEŁ)

Plik `LISTA_ZLECEN_DO_WYSTAWIENIA.md` (23.09.2026) to operacyjna wersja 5 zleceń badawczych z wcześniejszej strategii Mystery Shopping (`STRAT-08-MYSTERY-SHOPPING-MASTER-V2-HARDENED`, plik źródłowy usunięty jako wersja nieaktualna), rozbudowana o parametry formularza Useme. Metoda: oryginalne ogłoszenia klientów z bazy przegranych → usunięcie danych firm/osób → gotowe wzorce 1:1.

**Weryfikacja odwołań źródłowych wykazała błędy, które tu korygujemy:**

| Element | Stan w wersji z 23.09 | Weryfikacja | Poprawka |
|---|---|---|---|
| `02_przegrane/przegrane_pelne_416.json` | odwołanie | ✅ **ISTNIEJE** (416 rekordów) | bez zmian |
| `wygrane_oferty_historia.json` | odwołanie | ❌ **PLIK NIE ISTNIEJE** | to zmyślone odwołanie; realny plik to `03_odpisane/wygrane_56.json` |
| „406 zakończonych” w nagłówku | liczba | ⚠️ rozbieżność z nazwą pliku (416) | usunięte z tego dokumentu |
| ID 2865390, 2564058, 2725737, 2865441, 2798896, 2628151 | źródła zleceń | ✅ potwierdzone w bazie | bez zmian |
| ID 2568606 | źródło zlecenia | ⚠️ **niepotwierdzone** bezpośrednio | oznaczone jako niepewne |
| Opis #2725737 (Bedecor) | „panele/fototapety/meble” | ⚠️ **nadinterpretacja** — oryginał dotyczył wyłącznie fototapet | poprawione |

**Wniosek z pkt 1:** plik z 23.09 był w większości oparty na prawdziwych danych, ale zawierał **jedno zmyślone odwołanie źródłowe** (`wygrane_oferty_historia.json`) oraz **drobne nadinterpretacje opisów**. Nie unieważnia to metodologii, ale nakazuje ostrożność przy cytowaniu źródeł.

---

# 2. CZY NOWE DANE Z BAZY `ksawierpotrykus3` ZMIENIAJĄ REKOMENDACJE

**Tak — i to istotnie.** Baza jest świeża (`last_job_id = 145247`, stan 30.09.2026; `01_ofertowarka` = 164 pliki zleceń; `02_przegrane` = ~414–421 rekordów; `03_odpisane` = 56 odpisanych).

**Kluczowe ustalenia po korekcie epistemologicznej (pkt 0):**

1. **Liczba „odpisanych” to nie liczba wygranych.** Z 56 odpisanych wątków zaledwie ~5 doszło do jakiejkolwiek płatności. Dla badań nie ma to znaczenia — liczymy odpisanych.

2. **Wzorzec OCR/n8n jest już przebadany i przesycony.** Zlecenie #144890 zebrało **101 ofert publicznych + 19 PV = 112 wykonawców**. Powtarzanie go 1:1 da nakładające się dane o tej samej puli.

3. **Rynek n8n/Make ma fatalny wskaźnik odpowiedzi w bazie:** Make/n8n/Zapier (n=26), Computer Vision/OCR/AI (n=24). Wysoka konkurencja = niskie szanse.

4. **Potwierdzone największym wolumenem:** BaseLinker/Subiekt/ERP (7 zleceń w bazie) — to realnie najczęściej pojawiająca się nisza.

5. **Wykryto nowe, mocniejsze sygnały:**
   - **IdoSell (IAI)** — n=9, Win Rate **33.3%** (najwyższy w e-commerce, poszlaka).
   - **Mobile native** — Kotlin 27.3%, Swift 20.0% (najwyższe wskaźniki w bazie, wysoka bariera wejścia).
   - **Enova365** — 28.6%.
   - **Testy penetracyjne** — zlecenie #145234 za **15 853,67 PLN** (OWASP MASVS/ASVS) → 5–10x wartość pojedynczego zlecenia.

---

# 3. FINALNY ZESTAW ZLECEŃ BADAWCZYCH

Poniżej **ostateczna, uporządkowana lista**. Składa się z:
- **1 zlecenia już wysłanego** (#144890 — OCR/n8n, dowód słuszności metody),
- **2 zleceń wystawionych** (Zlecenie 1 — Subiekt/BaseLinker, Zlecenie 3 — Mobile native),
- **4 zleceń do wystawienia** (Zlecenia 2 — Konfigurator 3D, 4 — Scraping, 5 — PWA/panel B2B; mix archetypów bez monokultury automatyzacyjnej),
- **1 zlecenia dodatkowego** (Zlecenie 6 — IdoSell, na wyraźną prośbę, najwyższy wskaźnik w e-commerce).

> **Uwaga o zakresie:** ten zestaw (7 zleceń bazowych + 6 uzupełniających U1–U6 opisanych niżej) pokrywa docelowo ~17 z 19 realnych pod-pul wykonawców (patrz sekcja 4.5–4.8 oraz blok „ZLECENIA UZUPEŁNIAJĄCE").

> **ZASADA BUDŻETOWA (obowiązuje wszystkie zlecenia):** w ogłoszeniu **nie podajemy żadnej kwoty ani widełek**. Wykonawca sam proponuje stawkę w ofercie — to część badania (patrz: jak wyceniają konkurenci). Dawniej wpisywane „orientacyjnie X PLN" to wyłącznie wewnętrzna referencja do planowania, NIE do wklejenia w formularz Useme.

| Slot | Nisza | Archetyp | Status |
|---|---|---|---|
| — | OCR / obieg dokumentów + n8n | Automatyzacja | ✅ **WYSŁANE** (#144890) |
| 1 | Subiekt / BaseLinker / ERP | ERP & e-commerce | ✅ **WYSTAWIONE** |
| 2 | Konfigurator 3D (Three.js) | Frontend / e-commerce | do wystawienia |
| 3 | Mobile native (Kotlin/Flutter, offline) | Mobile | ✅ **WYSTAWIONE** |
| 4 | Scraping / boty (twardy ból: blokady) | Automatyzacja | do wystawienia |
| 5 | PWA / panel B2B (MVP) | Tech-agnostic | do wystawienia |
| 6 | **IdoSell B2B (dodatek)** | ERP & e-commerce | do wystawienia |
| U1 | Webdev e-commerce (Shopify/PrestaShop) | E-commerce webdev | do wystawienia |
| U2 | KSeF / XML księgowy / walidacja VAT | Księgowość / ERP | do wystawienia |
| U3 | Data engineering / BigQuery / ETL | Chmura / dane | do wystawienia |
| U4 | SaaS booking / concurrency | Backend SaaS | do wystawienia |
| U5 | iOS native (Swift) | Mobile | do wystawienia |
| U6 | CAD/CAM/CNC / G-code / DXF | Inżynieria mechaniczna | do wystawienia |

**Razem: 3 zlecenia wystawione/wysłane** (#144890 + Zlecenie 1 + Zlecenie 3) **oraz 10 zleceń do wystawienia** (Zlecenia 2, 4, 5, 6 + U1–U6).

---

## ✅ ZLECENIE JUŻ WYSŁANE — #144890 (WZORZEC 1, OCR/n8n)

*Konto zleceniodawcy: `weronikabuchholc13`. Zamknięte 28.09.2026.*

**Zebrane dane:** 101 ofert publicznych + 19 wątków PV = **112 unikalnych wykonawców**.
**Statystyki cenowe:** min 95 / mediana 5 900 / średnia 9 059 / max 120 000 PLN. Czas realizacji: 7–126 dni.
**Wnioski badawcze:** n8n pojawił się w 91.1% ofert, Docker/VPS w 47.5%, KSeF w 17.8%. 46.5% oferentów ma 0 umów na Useme — liczba umów NIE koreluje z jakością merytoryczną.

**Dlaczego to zlecenie było złote dla badań:** jedno dobrze skrojone zlecenie = cała mikroanaliza niszy. Ale jako nisza zarobkowa to czerwony ocean (nasycona konkurencja). Wystawienie go ponownie 1:1 nie ma sensu.

---

## ZLECENIE 1 — SUBIEKT / BASELINKER / ERP (NAJMOCNIEJSZY WOLUMEN) — ✅ **WYSTAWIONE**

> **STATUS: WYSTAWIONE** (opublikowane na Useme z konta zleceniodawcy). Oferty zbierane — patrz protokół operacyjny (sekcja 6).
> **Formularz:** poszło w **1 bloku** (standardowy formularz Useme).

*Kategoria:* `Programowanie i IT → Oprogramowanie`
*Tytuł:* `Szybka synchronizacja stanów magazynowych i cen między Subiektem a BaseLinkerem (duża baza produktów)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `14 dni`

**Treść do wklejenia:**
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

**Dlaczego to jest #1:** największy wolumen w bazie (7 zleceń), wąska i profesjonalna konkurencja, realne portfolio Ksawiera (tagi: BaseLinker, ERP, Subiekt, WooCommerce). Podniesiony budżet (z 4 500 → 7 000+) wchodzi w „sweet spot” 6–10k, gdzie odpowiada czołówka, a nie dumping.

**⚠️ ZASIĘG — CO TO ZLECENIE POKRYWA, A CZEGO NIE (WAŻNE):**
To zlecenie bada **JEDNĄ pod-pulę wykonawców**, a nie cały klaster P4 (10,3% z PLAN_PORTFOLIO).
- ✅ **Pokrywa:** pod-pulę A — integratorzy magazynowi (Subiekt ↔ BaseLinker ↔ Allegro/Sfera). Realny zasięg: **~4–6% rynku**.
- ❌ **NIE pokrywa:** webdev e-commerce (Shopify/PrestaShop — pod-pula B), konsultantów ciężkiego ERP (Enova365/Comarch XL — pod-pula C), specjalistów IdoSell (pod-pula D).
- ❌ **NIE pokrywa:** ludzi od sklepów na Shopify/PrestaShop — to inna pula wykonawców niż integratorzy Subiekta.
Szczegółowe rozbicie klastra P4 na pod-pule → patrz sekcja 4.2; pełna mapa pod-pul → sekcja 4.5.

---

## ZLECENIE 2 — KONFIGURATOR 3D / THREE.JS (WYSOKA MARŻA)

*Kategoria:* `Programowanie i IT → Aplikacje webowe`
*Tytuł:* `Interaktywny podgląd 3D produktu na stronę internetową – meble modułowe (płynne działanie na telefonach)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `14 dni`

**Treść do wklejenia:**
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

**Dlaczego:** nisza o najwyższej marży (konfiguratory to ewenement — Ksawier dostał realną odpowiedź od klienta na konfigurator mebli 3D). Wymóg „płynnie na telefonie” odsiewa szablonowców i ujawnia, kto realnie robił konfiguratory.

---

## ZLECENIE 3 — MOBILE NATIVE (NAJWYŻSZY POTENCJAŁ, POMINIĘTY W STAREJ LIŚCIE) — ✅ **WYSTAWIONE**

> **STATUS: WYSTAWIONE** (opublikowane na Useme z konta zleceniodawcy).
> **Formularz:** poszło w **3 osobnych polach** (Opis / Wymagane funkcje / System operacyjny) — patrz niżej.

*Kategoria:* `Programowanie i IT → Aplikacje mobilne`
*Tytuł:* `Aplikacja mobilna dla pracowników terenowych z trybem offline (Kotlin / Flutter)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `14 dni`

**Treść — UWAGA: zlecenie poszło w 3 osobnych polach formularza Useme (nie jednym blokiem). Poniżej dokładnie to, co wklejono:**

**Pole 1 — „Opis":**
```text
Dzień dobry,

Szukamy wykonawcy aplikacji mobilnej (Android, ewentualnie iOS) dla pracowników terenowych naszej firmy — kierowców i serwisantów pracujących w halach i na trasach, gdzie często nie ma zasięgu.

Problem:
Nasi pracownicy wypełniają formularze i robią zdjęcia dokumentów, ale gdy nie ma internetu, dane się gubią lub aplikacja się zawiesza. Potrzebujemy rozwiązania, które działa niezawodnie bez sieci.

Termin realizacji:
Zależy nam na wdrożeniu w ciągu maksymalnie 60 dni od wyboru wykonawcy, z możliwością podziału na etapy (najpierw formularze offline, potem zdjęcia i synchronizacja).

W ofercie prosimy o:
- Rekomendację technologii (natywna Android vs Flutter) i uzasadnienie,
- Przykłady zrealizowanych aplikacji mobilnych Twojego autorstwa,
- Propozycję podziału prac na etapy oraz szacunkową wycenę i czas realizacji (w dniach),
- Krótką informację, czego nie da się zrobić offline na starszych telefonach.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Praca w pełni offline — formularze i zdjęcia zapisują się lokalnie na telefonie i automatycznie synchronizują z serwerem, gdy wróci zasięg.
2. Kompresja zdjęć przed wysłaniem (oszczędność transferu i miejsca).
3. Prosty, szybki interfejs — aplikacja musi działać płynnie na starszych telefonach.
4. Podstawowe powiadomienia push (np. nowe zadanie, potwierdzenie synchronizacji).
5. Wykorzystanie trybu deep-sync, który w tle utrzymuje spójność lokalnej bazy z serwerem.
```

**Pole 3 — „System operacyjny":**
```text
Android (priorytet), opcjonalnie iOS. Większość naszych pracowników używa telefonów z Androidem, dlatego preferujemy natywną aplikację Android lub rozwiązanie cross-platform (Flutter).
```

**Rozkład min na pola:** Pole 1 → pytanie o granice (C). Pole 2 → nieistniejący moduł „deep-sync" (A) + canary phrase „gubienie danych" (B). Pole 3 → czyste (bez min, żeby nie przesadzić).

**Dlaczego:** mobile native to najwyższe wskaźniki odpowiedzi w bazie (Kotlin 27.3%, Swift 20.0%), a jednocześnie najwyższa bariera wejścia (Gradle/Xcode) = filtr na amatorów. Całkowicie pominięte w starej liście. Średnie budżety aplikacji mobilnych są najwyższe na platformie.

**⚠️ ZASIĘG — CO TO ZLECENIE POKRYWA, A CZEGO NIE:**
- ✅ **Pokrywa:** Android native (Kotlin, ~4%) + Cross-platform (Flutter/RN, ~1-2%).
- ❌ **NIE pokrywa:** iOS native (Swift, ~3%) — to osobna pula, iOS-owiec nie odpisze na brief z Kotlinem.

**Formularz Useme — 3 pola:** to zlecenie realnie poszło w 3 osobnych polach (Opis / Wymagane funkcje / System operacyjny), a nie jednym blokiem. Miny rozłożone między pola (patrz wyżej).

---

## ZLECENIE 4 — SCRAPING / BOTY (TWARDY BÓL, NIE OGÓLNIKI)

*Kategoria:* `Programowanie i IT → Oprogramowanie`
*Tytuł:* `Monitoring i codzienne pobieranie cen z portali ogłoszeniowych (problem z blokowaniem IP)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `10 dni`

**Treść do wklejenia:**
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

**Dlaczego:** stara wersja miała 3 500 zł i ogólnikowy brief — wpadał dumping i amatorzy. Tu: podniesiony budżet (5 500 zł) + twardy ból (blokady, Cloudflare, rate-limiting) → przyciąga realnych specjalistów od scrapingu, którzy od razu ostrzegą o kosztach proxy i limitach.

---

## ZLECENIE 5 — PWA / PANEL B2B (TECH-AGNOSTIC, GÓRNA PÓŁKA)

*Kategoria:* `Programowanie i IT → Aplikacje webowe`
*Tytuł:* `Dedykowany panel zamówień hurtowych B2B dla stałych klientów (wersja MVP)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `14 dni`

**Treść do wklejenia:**
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

**Dlaczego:** segment tech-agnostic to 32.8% całego rynku (158 zleceń) — niedoreprezentowany w starej liście. Wysoki budżet przyciąga software house'y, prezentacje PDF i podział na milestones. Uwaga operacyjna: przy drogim zleceniu warto zastosować protokół OPSEC (Seed Contract, płatny mikro-etap), by nie zostać „Ghost Requesterem”.

---

## ZLECENIE 6 — IDOSELL B2B (DODATEK, NA ŻYCZENIE)

*Kategoria:* `Programowanie i IT → Oprogramowanie` / `Sklepy internetowe`
*Tytuł:* `Wdrożenie i konfiguracja IdoSell B2B dla hurtowni – cenniki grupowe i integracja z magazynem`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas ofert:* `14 dni`

**Treść do wklejenia:**
```text
Dzień dobry,

Prowadzimy hurtownię i chcemy uruchomić na platformie IdoSell (IAI) dedykowany panel B2B dla naszych stałych kontrahentów — sklepów i firm, które kupują u nas regularnie.

Zakres prac:
1. Konfiguracja IdoSell B2B: indywidualne cenniki i poziomy rabatowe przypisane do kontrahenta, limity kupieckie, blokady płatności.
2. Import bazy towarowej (kilka tysięcy pozycji) oraz mapowanie wariantów i jednostek miary.
3. Integracja z naszym systemem magazynowym — potrzebujemy aktualnych stanów i automatycznego tworzenia zamówień po stronie magazynu.
4. Dodatkowa weryfikacja numerów NIP kontrahentów w bazie GUS przy rejestracji.
5. Testy poprawności cenników i rabatów przed uruchomieniem na żywej bazie klientów.

W ofercie prosimy o:
- Twoje doświadczenie konkretnie z platformą IdoSell (IAI) i wdrożeniami B2B,
- Sposób realizacji integracji z magazynem (API, pliki wymiany),
- Orientacyjną wycenę, czas realizacji oraz warunki późniejszego wsparcia.
```

**Dlaczego:** IdoSell to najwyższy wskaźnik w całym e-commerce w bazie (**33.3%**, n=9) i jednocześnie nisza wąska, mało przebadana. Interesuje nas poznanie rynku wykonawców specjalizujących się w tej konkretnej platformie — ich stawek, sposobu integracji i głębokości wiedzy.

---

## ZLECENIA UZUPEŁNIAJĄCE (U1–U6) — DOMKNIĘCIE LUK POD-PUL WYKONAWCÓW

> **Skąd te zlecenia:** analiza w sekcji 4 wykazała, że klaster rynkowy ≠ jedna pula wykonawców. 8 klastrów P1–P8 rozbija się na **19 realnych, różnych pod-pul wykonawców**. Obecny zestaw 7 zleceń pokrywa ~10–11 z nich. Poniższe 6 zleceń domyka kluczowe luki — każde zlecenie = jedna osobna pula (bo to osobni ludzie). Każde rozbite na **3 pola formularza Useme** + miny detekcji AI.

**Świadomie POMIJAMY:**
- **Ciężki ERP (Enova365/Comarch XL, pod-pula 9)** — pula praktycznie pusta na Useme (Win Rate Optimy = 0%, n=5; robią to partnerzy, nie freelancerzy).
- **CRM integracje (Salesforce/HubSpot, pod-pula 17)** i **DevOps (pod-pula 19)** — opcjonalne, do decyzji później.

---

### U1. WEBDEV E-COMMERCE (SHOPIFY / PRESTASHOP)

**Pod-pula:** Webdev e-commerce (pod-pula 8 z mapy). **To największa luka** — 55 zleceń w bazie (Shopify 31 + PrestaShop 24).

*Kategoria:* `Programowanie i IT → Sklepy internetowe`
*Tytuł:* `Przebudowa sklepu na Shopify / PrestaShop – niestandardowa logika koszyka i integracja z magazynem`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Prowadzimy sklep internetowy i planujemy przebudowę / rozbudowę platformy sprzedażowej. Rozważamy Shopify lub PrestaShop — zależy nam na wykonawcy, który ma doświadczenie w obu i pomoże wybrać lepszą drogę.

Obecny problem:
Nasz sklep działa, ale brakuje mu niestandardowych funkcji, których nie da się ustawić z panelu: własne reguły koszyka, rabaty warunkowe, nietypowe metody dostawy dla wybranych grup produktów. Standardowe wtyczki się nie sprawdzają.

Zakres prac:
1. Konfiguracja i/lub przebudowa sklepu (Shopify lub PrestaShop) pod niestandardową logikę koszyka i rabatów.
2. Integracja z naszym systemem magazynowym — aktualne stany i automatyczne tworzenie zamówień.
3. Migracja danych z obecnego sklepu (produkty, klienci, historia).
4. Testy poprawności koszyka, rabatów i wysyłek przed startem.

W ofercie prosimy o:
- Rekomendację platformy (Shopify vs PrestaShop) i uzasadnienie,
- Przykłady wdrożeń z niestandardową logiką koszyka/rabatów,
- Wycenę, czas realizacji (w dniach) oraz co odradzasz przy migracji danych ze starego sklepu.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Niestandardowe reguły koszyka (rabaty warunkowe, progi, wykluczenia produktów).
2. Automatyczne przeliczanie dostawy dla wybranych grup produktów.
3. Integracja stanów magazynowych z systemem magazynowym (bez rozjazdu koszyka przy równoczesnych zamówieniach).
4. Wykorzystanie modułu cart-guard pilnującego spójności koszyka przy modyfikacjach.
5. Import historii zamówień i klientów ze starego sklepu.
```

**Pole 3 — „System operacyjny / platforma":**
```text
Shopify lub PrestaShop (do rekomendacji przez wykonawcę). Obecny sklep działa na starszej platformie, jesteśmy otwarci na migrację.
```

**Miny:** A = „moduł cart-guard" (nieistniejący) · B = „bez rozjazdu koszyka" (canary phrase) · C = „co odradzasz przy migracji" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 8 (webdev e-commerce, ~4–5%). NIE pokrywa integratorów magazynowych (Zlecenie 1), NIE pokrywa IdoSell (Zlecenie 6).

---

### U2. KSEF / XML KSIĘGOWY / WALIDACJA VAT

**Pod-pula:** KSeF / XML księgowy (pod-pula 3 z mapy). Osobni specjaliści księgowo-ERP — nie odpiszą na brief OCR/n8n.

*Kategoria:* `Programowanie i IT → Oprogramowanie`
*Tytuł:* `Integracja KSeF – generowanie i walidacja plików XML FA(2)/FA(3) oraz zgodność z systemem księgowym`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Nasza firma musi dostosować obieg faktur do wymogów KSeF. Szukamy specjalisty, który zbuduje i wdroży rozwiązanie do generowania, wysyłania i walidacji plików XML w strukturze FA(2) / FA(3).

Zakres prac:
1. Generowanie plików XML faktur zgodnych ze schematem ministerstwa (FA(2)/FA(3)).
2. Walidacja poprawności pliku przed wysłaniem (kwoty, stawki VAT, NIP, sumy pozycji).
3. Wysyłka i odbiór potwierdzeń z systemu KSeF.
4. Integracja z naszym programem księgowym — dane mają spływać automatycznie, bez ręcznego przepisywania.

Kluczowe: dokument musi przejść walidację KSeF za pierwszym razem, a kwoty pozycji muszą zgadzać się co do grosza z podsumowaniem.

W ofercie prosimy o:
- Doświadczenie z KSeF i strukturą FA(2)/FA(3),
- Sposób walidacji pliku przed wysłaniem,
- Wycenę, czas realizacji (w dniach) oraz czego nie da się zwalidować automatycznie.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Generowanie XML FA(2)/FA(3) zgodnie z aktualnym schematem ministerstwa.
2. Walidator grosh-match sprawdzający zgodność sum pozycji z podsumowaniem do 0,01 zł.
3. Automatyczna korekta zaokrągleń VAT dla stawek 5/8/23%.
4. Wysyłka do KSeF i obsługa potwierdzeń (UPO).
5. Integracja z programem księgowym (import/eksport XML).
```

**Pole 3 — „System operacyjny / środowisko":**
```text
Środowisko firmowe (serwer własny lub chmura). Nasz program księgowy obsługuje wymianę przez pliki XML — szczegóły przekażemy po wyborze wykonawcy.
```

**Miny:** A = „walidator grosh-match" (nieistniejący) · B = „bez odrzucenia przez KSeF" (canary phrase) · C = „czego nie da się zwalidować automatycznie" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 3 (KSeF/XML, ~3%). NIE pokrywa OCR/n8n (#144890) — to inna pula (dokumenty vs księgowość XML).

---

### U3. DATA ENGINEERING / BIGQUERY / ETL

**Pod-pula:** Data engineering (pod-pula 16 z mapy). Największa pojedyncza luka w klastrze P8 (43,3% rynku).

*Kategoria:* `Programowanie i IT → Oprogramowanie`
*Tytuł:* `Potok danych do Google BigQuery – automatyczne zasilanie i analiza obłożenia (Python / GCP)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Szukamy inżyniera danych do zbudowania potoku ETL zasilającego Google BigQuery danymi z naszych systemów operacyjnych (m.in. dane rezerwacji, sprzedaży i ruchu).

Zakres prac:
1. Pobieranie danych z kilku źródeł (API, baza SQL, pliki) — kilka tysięcy rekordów dziennie.
2. Transformacja i ładowanie do BigQuery (partycjonowanie, deduplikacja).
3. Codzienne zasilanie w oknie nocnym + obsługa błędów i ponowień.
4. Prosty pulpit / zapytania analityczne pod raporty obłożenia i sprzedaży.

Kluczowe: dane w BigQuery muszą być spójne — bez duplikatów przy ponownym uruchomieniu potoku.

W ofercie prosimy o:
- Doświadczenie z BigQuery, GCP i Pythonem,
- Sposób zapewnienia spójności danych przy ponowieniach,
- Wycenę, czas realizacji (w dniach) oraz miesięczny koszt utrzymania (zapytania, storage),
- Jakich źródeł danych nie da się stabilnie podłączyć.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Pobieranie danych z API i bazy SQL (Python).
2. Ładowanie do BigQuery z partycjonowaniem i deduplikacją.
3. Wykorzystanie potoku exactly-once-flow gwarantującego brak duplikatów wierszy.
4. Harmonogram nocny + obsługa błędów i ponowień.
5. Zestaw zapytań SQL / prosty widok analityczny pod raporty.
```

**Pole 3 — „System operacyjny / chmura":**
```text
Google Cloud Platform (BigQuery). Źródła danych: API zewnętrzne + lokalna baza SQL. Preferujemy rozwiązanie bezserwerowe (Cloud Run / Cloud Functions).
```

**Miny:** A = „potok exactly-once-flow" (nieistniejący) · B = „bez duplikatów wierszy" (canary phrase) · C = „jakich źródeł nie da się stabilnie podłączyć" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 16 (data engineering, ~5%). To największa luka % w całym zestawie (P8 = 43,3%, my badamy tylko fragment).

---

### U4. SAAS BOOKING / CONCURRENCY

**Pod-pula:** SaaS booking / concurrency (pod-pula 12 z mapy). Backendowcy systemów rezerwacji — inna pula niż integracje czy frontend.

*Kategoria:* `Programowanie i IT → Aplikacje webowe`
*Tytuł:* `System rezerwacji online z blokadą terminów w czasie rzeczywistym (eliminacja podwójnych rezerwacji)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Prowadzimy firmę usługową i potrzebujemy systemu rezerwacji online z kalendarzem, w którym klienci sami wybierają wolne terminy.

Główny problem:
Zdarza się, że dwie osoby rezerwują ten sam termin w tym samym momencie — system nie blokuje slotu wystarczająco szybko. Efekt: nakładające się wizyty i zamieszanie. Musimy to wyeliminować.

Zakres prac:
1. Kalendarz rezerwacji z podglądem wolnych terminów.
2. Blokada terminu w momencie rezerwacji — natychmiastowe zniknięcie slotu dla innych użytkowników.
3. Potwierdzenia e-mail/SMS dla klienta i obsługi.
4. Panel administracyjny do zarządzania terminami i pracownikami.

Kluczowe: zero podwójnych rezerwacji nawet przy dużym ruchu w jednej chwili.

W ofercie prosimy o:
- Doświadczenie z systemami rezerwacji i obsługą współbieżności,
- Sposób techniczny blokady terminu (np. blokada bazodanowa),
- Wycenę, czas realizacji (w dniach) oraz co odradzasz przy takim modelu współbieżności.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Kalendarz z podglądem dostępnych terminów.
2. Blokada slotu w momencie rezerwacji (bez podwójnej rezerwacji).
3. Wykorzystanie mechanizmu slot-lock blokującego termin na czas transakcji.
4. Powiadomienia e-mail/SMS (potwierdzenie, przypomnienie).
5. Panel administracyjny (pracownicy, godziny, nieobecności).
```

**Pole 3 — „System operacyjny / środowisko":**
```text
Aplikacja webowa (przeglądarka + mobile). Backend i baza do rekomendacji przez wykonawcę. Zależy nam na rozwiązaniu, które wytrzyma skoki ruchu (np. kampania promocyjna).
```

**Miny:** A = „mechanizm slot-lock" (nieistniejący) · B = „bez podwójnej rezerwacji" (canary phrase) · C = „co odradzasz przy takim modelu współbieżności" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 12 (SaaS booking, ~1,8%). To pula, którą w bazie reprezentuje wygrana Doktor Monika (system rezerwacji z blokowaniem SQL).

---

### U5. iOS NATIVE (SWIFT)

**Pod-pula:** iOS native (pod-pula 14 z mapy). Osobna pula od Androida — iOS-owiec używa Xcode, nie odpisze na brief z Kotlinem.

*Kategoria:* `Programowanie i IT → Aplikacje mobilne`
*Tytuł:* `Aplikacja iOS (Swift) dla klientów – katalog, zamówienia i powiadomienia push`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Szukamy wykonawcy natywnej aplikacji iOS (Swift) dla naszych klientów. Chcemy, aby klienci mogli przeglądać naszą ofertę, składać zamówienia i otrzymywać powiadomienia bezpośrednio na iPhone'a.

Zakres prac:
1. Katalog produktów/usług z wyszukiwarką i filtrami.
2. Składanie zamówienia / rezerwacji z poziomu aplikacji.
3. Powiadomienia push (status zamówienia, promocje).
4. Logowanie i profil klienta z zapamiętywaniem preferencji.
5. Praca w tle bez utraty stanu, gdy użytkownik przełącza aplikacje.

Kluczowe: aplikacja musi działać płynnie na starszych iPhone'ach i nie rozładowywać baterii.

W ofercie prosimy o:
- Doświadczenie z natywnym iOS (Swift / SwiftUI),
- Linki do aplikacji w App Store Twojego autorstwa,
- Wycenę, czas realizacji (w dniach) oraz czego nie da się zrobić w tle na iOS.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Katalog z wyszukiwarką i filtrami.
2. Składanie zamówienia / rezerwacji.
3. Powiadomienia push (status, promocje).
4. Wykorzystanie trybu background-refresh-v2 do odświeżania danych w tle.
5. Profil klienta z zapamiętywaniem preferencji i logowaniem.
```

**Pole 3 — „System operacyjny":**
```text
iOS (natywnie, Swift). Zależy nam na wsparciu dla starszych wersji systemu — nie tylko najnowszego iPhone'a.
```

**Miny:** A = „tryb background-refresh-v2" (nieistniejący) · B = „bez utraty stanu" (canary phrase) · C = „czego nie da się zrobić w tle na iOS" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 14 (iOS native, ~3%). Uzupełnia Zlecenie 3 (Android/Flutter) — razem domykają całą pod-pulę mobile.

---

### U6. CAD / CAM / CNC / G-CODE

**Pod-pula:** CAD/CAM/CNC (pod-pula 5 z mapy). Inżynierowie mechanicy — zupełnie inna branża niż webdev 3D (Zlecenie 2).

*Kategoria:* `Programowanie i IT → Oprogramowanie`
*Tytuł:* `Generowanie plików DXF i kodu G-code z konfiguratora produktu (integracja z maszynami CNC)`
*Budżet:* **nie podajemy** — wykonawca proponuje kwotę sam
*Czas na składanie ofert:* `14 dni`
*Prawa autorskie:* `Przeniesienie praw autorskich`

**Pole 1 — „Opis":**
```text
Dzień dobry,

Produkujemy meble / elementy na wymiar. Chcemy, aby po skonfigurowaniu produktu przez klienta system automatycznie generował pliki produkcyjne dla naszych maszyn CNC.

Zakres prac:
1. Na podstawie parametrów produktu (wymiary, materiał, wiercenia) generowanie pliku DXF (obwiednia elementu).
2. Generowanie kodu G-code pod nasze maszyny stolarskie (punkty wierceń pod kołki, obwiednia freza).
3. Integracja z naszym programem produkcyjnym (TopSolid) — eksport danych.
4. Testy na rzeczywistych projektach przed wdrożeniem produkcyjnym.

Kluczowe: wygenerowany kod musi być kompatybilny z maszynami i nie powodować błędów przy cięciu.

W ofercie prosimy o:
- Doświadczenie z CAD/CAM, DXF i G-code pod maszyny stolarskie,
- Sposób generowania kodu i jego testowania,
- Wycenę, czas realizacji (w dniach) oraz jakich maszyn nie da się obsłużyć tym rozwiązaniem.
```

**Pole 2 — „Wymagane funkcje":**
```text
1. Generowanie DXF z parametrów produktu (obwiednia).
2. Generowanie G-code pod maszyny stolarskie (wiercenia, frezowanie).
3. Wykorzystanie warstwy toolpath-guard pilnującej poprawności ścieżek narzędzia.
4. Integracja z TopSolid (eksport danych produkcyjnych).
5. Testy na rzeczywistych projektach.
```

**Pole 3 — „System operacyjny / maszyny":**
```text
Rozwiązanie desktopowe lub serwerowe (do rekomendacji). Maszyny: stolarskie CNC (dokładne modele przekażemy po wyborze wykonawcy). Program produkcyjny: TopSolid.
```

**Miny:** A = „warstwa toolpath-guard" (nieistniejący) · B = „bez błędów przy cięciu" (canary phrase) · C = „jakich maszyn nie da się obsłużyć" (pytanie o granice).

**Zasięg:** pokrywa pod-pulę 5 (CAD/CAM/CNC, ~1%). To inżynierowie mechanicy — NIE frontendowcy 3D (Zlecenie 2). Osobna pula.

---

**Podsumowanie zleceń uzupełniających:**

| # | Nowe zlecenie | Pod-pula | Priorytet |
|:--:|---|:--:|---|
| U1 | Webdev e-commerce (Shopify/PrestaShop) | 8 | **#1 (55 zleceń w bazie)** |
| U2 | KSeF / XML księgowy | 3 | #2 |
| U3 | Data engineering / BigQuery | 16 | #3 (P8 = 43,3%) |
| U4 | SaaS booking / concurrency | 12 | #4 |
| U5 | iOS native (Swift) | 14 | #5 |
| U6 | CAD/CAM/CNC / G-code | 5 | #6 |

**Po wystawieniu tych 6 zleceń** (razem z obecnymi 7) zestaw pokryje **~17 z 19 pod-pul** (89%). Pozostaną tylko: ciężki ERP (świadomie pominięty — pusta pula), CRM Salesforce i DevOps (opcjonalne, do decyzji).

---

# 4. ANALIZA PUL WYKONAWCÓW (KOREKTA METODOLOGICZNA)

> **Kluczowa teza:** klaster rynkowy ≠ jedna pula wykonawców. Zlecenie badawcze bada **podaż** (konkretną grupę ludzi), a nie **popyt** (udział zleceń w rynku). To rozróżnienie zmienia liczbę potrzebnych zleceń z ~8 do ~15–19.

## 4.1. Problem, który korygujemy

`PLAN_PORTFOLIO.md` definiuje klaster **P4 „Marketplace Sync & Inventory Hub” = 40 zleceń = 10,3% akceptowanego rynku**. To prawda **na poziomie rynku** (popyt). Ale to NIE jest jedna pula wykonawców (podaż).

Wrzucenie Subiekta, BaseLinkera, Shopify, PrestaShop, Enova365, Comarch XL i IdoSell do jednego worka jest błędem redukcyjnym. **To różni ludzie.** Dlatego 10,3% nie jest zasięgiem jednego zlecenia — to suma kilku niezależnych pod-pul.

## 4.2. Rozbicie klastra P4 na pod-pule

| Pod-pula | Technologie | Kto to realnie robi | % rynku | Które zlecenie to bada |
|---|---|---|---|---|
| **A. Integratorzy magazynowi** | Subiekt, BaseLinker, Allegro, Sfera PRO+, Insert GT | Programiści C#/PHP, specjaliści ERP↔marketplace | **~4–6%** | **Zlecenie 1** |
| **B. Webdev e-commerce** | PrestaShop, Shopify, WooCommerce, Shoper | Frontend PHP/Liquid/JS, agencje e-commerce | **~4–5%** | ❌ **brak — luka** |
| **C. Konsultanci ciężkiego ERP** | Enova365, Comarch XL/Optima | Certyfikowani partnerzy/wdrożeniowcy (rzadko freelancerzy na Useme) | **~1–2%** | ❌ **odpuścić — pusta pula** |
| **D. Specjaliści IdoSell** | IdoSell (IAI), API IAI | Specjaliści od jednej platformy SaaS | **~1%** | **Zlecenie 6** |

**Suma = ~10–14%** (zależnie od nakładania się). Ale **żadne pojedyncze zlecenie nie pokrywa całości**.

## 4.3. Wnioski operacyjne (klaster P4)

1. **Zlecenie 1 zamyka TYLKO pod-pulę A (~4–6%).** Nie badamy nim webdevu, ERP-owców ani IdoSell.
2. **Pod-pula C (Enova365/Comarch XL) jest praktycznie pusta na Useme** — Win Rate dla Optimy = 0% (n=5), bo tych zleceń nie robią freelancerzy, tylko partnerzy. **Nie ma sensu wystawiać tam zlecenia badawczego.**
3. **Pod-pula B (Shopify/PrestaShop) jest niedoreprezentowana w naszym zestawie** — 31 + 24 = 55 zleceń w bazie, a nie ma na to osobnego zlecenia. To luka.
4. **Wniosek dla AI czytającego ten plik:** NIE traktuj „10,3% klastra P4” jako zasięgu Zlecenia 1. To zasięg **całego klastra = suma 4 pod-pul**, z których badamy na razie 2 (A przez Zlecenie 1, D przez Zlecenie 6).

## 4.4. Otwarta decyzja — czy dodać zlecenie na pod-pulę B (Shopify/PrestaShop)?

**Za:** 55 zleceń w bazie, całkowita luka w zestawie, wyraźnie inna pula wykonawców (webdev e-commerce, nie integratorzy).
**Przeciw:** WooCommerce/WordPress to czerwony ocean (6.5% WR) — ryzyko, że Shopify/PrestaShop okaże się podobnie nasycony i mało wartościowy.
**Rekomendacja:** **do decyzji innego AI / osobnej analizy** — nie dopisujemy tu na siłę. Gdyby dodawać, to jako osobne zlecenie (Shopify/PrestaShop z niestandardową logiką, budżet 5–8k).

## 4.5. PEŁNA MAPA POD-PUL WYKONAWCÓW — CAŁY RYNEK (19 pod-pul)

Rozbicie wszystkich 8 klastrów P1–P8 z `PLAN_PORTFOLIO.md` na realne, **różne** pule wykonawców. Kryterium: *czy wykonawca technologii A odpowie też na technologię B (ta sama pula), czy to inny człowiek?*

| # | Pod-pula wykonawców | Klaster źródłowy | Osobna pula? |
|:--:|---|---|:--:|
| 1 | OCR / Computer Vision / ekstrakcja dokumentów | P1 | tak |
| 2 | LLM / RAG / n8n / automatyzacje AI | P1 | tak |
| 3 | KSeF / XML księgowy / walidacja VAT | P1 | **tak** |
| 4 | WebGL / Three.js / frontend 3D | P2 | tak |
| 5 | CAD/CAM/CNC / DXF / G-code / TopSolid | P2 | **tak** (inżynierowie mechanicy) |
| 6 | Scraping / boty / WAF bypass | P3 | jedna pula (spektrum) |
| 7 | Subiekt / BaseLinker / integratorzy magazynowi | P4 | tak |
| 8 | Webdev e-commerce (PrestaShop/Shopify/Woo/Shoper) | P4 / P5 | **tak** |
| 9 | Ciężki ERP (Enova365/Comarch XL) — **pusta na Useme** | P4 / P8 | tak (praktycznie pusta) |
| 10 | IdoSell (IAI) | P4 / P5 | tak |
| 11 | Custom B2B portal (Laravel/PHP/React) | P5 | tak |
| 12 | SaaS booking / concurrency | P6 | jedna pula |
| 13 | Android native (Kotlin) | P7 | tak |
| 14 | iOS native (Swift) | P7 | **tak** (inne narzędzia: Xcode) |
| 15 | Cross-platform (Flutter / React Native) | P7 | tak |
| 16 | Data engineering / BigQuery / ETL / GCP | P8 | tak |
| 17 | CRM integracje (Salesforce / HubSpot) | P8 | tak |
| 18 | Backend SaaS ogólny (Python / Node / .NET / REST) | P8 | tak |
| 19 | DevOps / Docker / VPS / Cloud infra | P8 | tak |

**Razem: 19 realnych, różnych pod-pul wykonawców.** (Przy założeniu, że Flutter i RN to jedna pula cross-platformowców; po rozdzieleniu — 20.)

## 4.6. Pokrycie obecnego zestawu (7 zleceń)

| Pod-pula | Pokryta przez | Status |
|---|:--:|:--:|
| 1. OCR / CV | OCR/n8n (#144890) | ✅ |
| 2. LLM / n8n | OCR/n8n (#144890) | ✅ |
| 3. KSeF / XML księgowy | — | ❌ |
| 4. WebGL / Three.js | Zlecenie 2 (Konfigurator 3D) | ✅ |
| 5. CAD/CAM/CNC / G-code | — | ❌ |
| 6. Scraping / WAF | Zlecenie 4 (Scraping) | ✅ |
| 7. Subiekt / BaseLinker | Zlecenie 1 | ✅ |
| 8. Webdev e-commerce (Shopify/PrestaShop) | — | ❌ |
| 9. Ciężki ERP (Enova/Comarch) | — | ❌ (świadomie odpuszczona) |
| 10. IdoSell (IAI) | Zlecenie 6 | ✅ |
| 11. Custom B2B portal | Zlecenie 5 (PWA/panel B2B) | ✅ |
| 12. SaaS booking / concurrency | — | ❌ |
| 13. Android native (Kotlin) | Zlecenie 3 | ✅ |
| 14. iOS native (Swift) | — | ❌ |
| 15. Cross-platform (Flutter/RN) | Zlecenie 3 | ✅ |
| 16. Data engineering / BigQuery | — | ❌ |
| 17. CRM integracje (Salesforce) | — | ❌ |
| 18. Backend SaaS ogólny | Zlecenie 5 (panel B2B) — częściowo | ⚠️ częściowo |
| 19. DevOps / infra | — (rozproszone po innych) | ⚠️ brak dedykowanej |

**Podsumowanie pokrycia:**
- Pokryte w pełni: **10 z 19** (pod-pule 1, 2, 4, 6, 7, 10, 11, 13, 15 + częściowo 18)
- Niepokryte: **9 z 19** (pod-pule 3, 5, 8, 9, 12, 14, 16, 17, 19)

> **Uwaga o definicji „pokryte":** w tej tabeli „pokryte" = pod-pula ma **przypisane zlecenie** (niezależnie od tego, czy zostało już opublikowane na Useme). Statusy publikacji poszczególnych zleceń są w sekcji 3. Dlatego Zlecenia 2 i 4 są tu liczone jako pokrycie, mimo że wg sekcji 3 są jeszcze „do wystawienia".

Obecny zestaw 7 zleceń pokrywa ~**10–11 z 19 realnych pod-pul (52–58% podaży wykonawców)**, mimo deklarowanego „100% pokrycia rynku” w `PLAN_PORTFOLIO` — bo plan liczył **popyt** (udziały w rynku), a nie **podaż** (osobne pule wykonawców).

## 4.7. Niepokryte pod-pule — lista luk (BEZ nowych zleceń w tym dokumencie)

| # | Niepokryta pod-pula | Klaster | Uwaga |
|:--:|---|---|---|
| 3 | KSeF / XML księgowy / walidacja VAT | P1 | specjaliści księgowo-ERP, osobni od OCR/n8n |
| 5 | CAD/CAM/CNC / G-code / DXF | P2 | inżynierowie mechanicy, inna branża niż webdev 3D |
| 8 | Webdev e-commerce (Shopify/PrestaShop/Woo/Shoper) | P4/P5 | 55 zleceń w bazie — największa luka |
| 12 | SaaS booking / concurrency | P6 | backendowcy rezerwacji/klinik |
| 14 | iOS native (Swift) | P7 | Zlecenie 3 jest na Kotlin/Flutter, iOS-owiec nie odpisze |
| 16 | Data engineering / BigQuery / ETL / GCP | P8 | największa pojedyncza luka w P8 (klaster = 43,3%) |
| 17 | CRM integracje (Salesforce / HubSpot) | P8 | brak dedykowanego zlecenia |
| 19 | DevOps / infra / Docker / VPS | P8 | brak dedykowanego (rozproszone jako wymóg poboczny) |
| 9 | Ciężki ERP (Enova365 / Comarch XL) | P4/P8 | **świadomie pomijamy** — pula praktycznie pusta na Useme |

**Uwaga:** ten dokument **nie tworzy nowych zleceń** na te luki. Lista służy jako mapa decyzyjna — ewentualne nowe zlecenia to osobna decyzja/analiza.

## 4.8. Ile zleceń finalnie potrzeba — bilans

| Wariant | Liczba zleceń | Uwagi |
|---|---|---|
| Konserwatywny (1 zlecenie = 1 pod-pula) | **19** | pełne pokrycie 19 pod-pul |
| Realistyczny (łączenie pokrewnych: OCR+n8n, Android+Flutter) | **~15–16** | część zleceń bada 2 pod-pule naraz |
| Obecnie | **7** (w tym 1 wysłane, 1 wystawione) | pokrywa ~10–11 pod-pul |
| **Braku je** | **~8–12** | zależnie od wariantu |

**Kluczowy wniosek metodologiczny:** deklaracja „100% pokrycia rynku” w `PLAN_PORTFOLIO` jest prawdziwa **tylko na poziomie popytu**. Na poziomie **podaży wykonawców** 8 projektów portfolia i 7 zleceń badawczych pokrywa jedynie ~10–11 z 19 realnych pod-pul. Reszta to osobni ludzie, których żadne z obecnych zleceń nie przyciągnie — bo np. integrator Subiekta nie odpowie na brief o Shopify, a frontendowiec Three.js nie odpowie na brief o G-code.

**Zlecenie badawcze bada pulę wykonawców, nie klaster rynkowy** — dlatego liczba potrzebnych zleceń wynika z liczby pod-pul (19), a nie z liczby klastrów (8).

---

# 5. DLACZEGO TAKI ZESTAW (PODSUMOWANIE LOGIKI)

**Stara lista miała jeden grzech: monokulturę automatyzacyjną.** 4 z 5 slotów to ten sam archetyp (n8n + AI + integracja) — badała w kółko tę samą pulę wykonawców.

**Nowy zestaw to przekrój przez archetypy:**
1. ERP / e-commerce (Subiekt/BaseLinker) — największy wolumen,
2. Frontend / konfigurator 3D — wysoka marża,
3. **Mobile native** — najwyższy potencjał, pominięty wcześniej,
4. Automatyzacja / scraping — z twardym bólem, nie ogólnikami,
5. Tech-agnostic / PWA B2B — 32.8% rynku,
6. **IdoSell** — dodatek, najwyższy wskaźnik w e-commerce.

**Wspólne zasady wszystkich zleceń:**
- Budżety w „sweet spot” 6–10k lub wyżej (nie dumping poniżej 5k),
- Konkretne nazwy systemów w briefie (Subiekt, BaseLinker, IdoSell, GUS, NIP) — to wyzwala merytoryczne pytania kwalifikujące,
- Zakaz self-doxxingu — język biznesowy, nie żargon programisty,
- Cel: **liczymy zebrane oferty**, nie escrow.

**Czego świadomie NIE robimy:** nie opieramy wyboru nisz na „wygranych/opłaconych” z bazy, bo ten sygnał jest zaszumiony (z 56 odpisanych tylko ~5 doszło do płatności). Bazujemy na wolumenie rynku, wskaźniku odpowiedzi i nasyceniu konkurencji.

---

# 6. PROTOKÓŁ OPERACYJNY (SKRÓT)

1. Wystawiaj zlecenia z konta zleceniodawcy, nigdy z profilu Ksawier Potrykus.
2. Zero ofert własnych pod własnym zleceniem badawczym.
3. Zbieraj oferty przez 7–14 dni.
4. Po zebraniu: nie zamykaj „po cichu” — zastosuj płatny mikro-etap konsultacyjny (Seed Contract) dla jednego najlepszego wykonawcy, by zachować wskaźnik odpowiedzi konta.
5. Każde zlecenie = jedna mikroanaliza niszy (cenniki, stack, pytania kwalifikujące, linki do portfolio).

---

*Dokument nadrzędny. Zastępuje `LISTA_ZLECEN_DO_WYSTAWIENIA.md` w zakresie wyboru i treści zleceń. Korekty źródeł i zasada epistemologiczna (`ODPISANE` ≠ `WYGRANE`) obowiązują wszystkie pochodne analizy.*

---

# 7. TAKTYKI DETEKCJI AI W OFERTACH (MINY / CANARY TRAPS)

## 7.1. Po co to robimy

Rynek Useme zalewają oferty generowane przez LLM — tanie, szybkie, ale bez zrozumienia problemu. Chcemy umieć je odsiać od ofert ludzi z realnym doświadczeniem, bo to odróżnia wartościowe dane badawcze od szumu.

**Zasada działania miny:** wkładamy w treść zlecenia element, który **człowiek z branży wyłapie, zignoruje lub o niego zapyta**, a **AI potraktuje jako fakt i przepisze bez zastanowienia**. Nie chodzi o to, żeby oferta była dziwna — brief ma pozostać naturalny i wiarygodny dla moderatorów Useme.

## 7.2. Katalog taktyk

| # | Taktyka | Na czym polega | Jak wygląda sygnał w ofercie | Siła |
|---|---|---|---|---|
| 1 | **Bait na nieistniejący moduł** | Wplata się nazwę funkcji, która brzmi branżowo, ale nie istnieje (np. „tryb silent-guard”, „sync-kernel”, „lock-layer v2”) | AI traktuje to jako realną funkcję i odnosi się do niej wprost. Człowiek zapyta „co masz na myśli?” lub pominie | ★★★ bardzo silna |
| 2 | **Canary phrase (fraza-znacznik)** | Unikalne, nienaturalne sformułowanie (np. „bez zatoru przy zapisach”, „wdrożenie bez przestoju linii”) | Ta sama fraza pojawia się w ofercie = prawie na pewno AI przekleiło brief. Człowiek opisze to swoimi słowami | ★★★ bardzo silna |
| 3 | **Pytanie o granice („czego NIE robisz”)** | Prośba o wskazanie, czego się nie da zrobić lub co się odradza | AI rzadko mówi „nie da się” — potwierdzi wszystko. Człowiek chętnie wskaże ograniczenia | ★★★ bardzo silna |
| 4 | **Wymóg konkretnej liczby** | Prośba o podanie liczby (dni realizacji, zapytań/dobę, kosztu utrzymania) | AI unika twardych liczb. Człowiek szacuje z doświadczenia | ★★ silna |
| 5 | **Sprzeczność liczbowa** | Niespójność w danych (np. „55 000 wariantów przy 40 000 produktów” w nietypowym układzie) | AI często nie wyłapie i przepisze dalej. Człowiek zapyta lub poprawi | ★★ silna |
| 6 | **Literówka / błędna nazwa systemu** | Np. „BaseLinker Connect v3”, „Subiekt Nexo Pro” (zła kapitalizacja) | AI powtórzy błąd. Człowiek napisze poprawnie lub zapyta o wersję | ★★ silna |
| 7 | **Pytanie o głęboki szczegół** | Pytanie, na które nie da się odpowiedzieć ogólnikiem (np. „co gdy EAN z Allegro nie zgadza się z formatem w Subiekcie po migracji z Insert GT?”) | AI odpowie generycznie („zastosujemy mapowanie”). Człowiek opowie konkretny przypadek | ★★ silna |
| 8 | **Sprzeczność techniczna** | Np. „synchronizacja asynchroniczna w czasie rzeczywistym co 2 minuty” (async + real-time + interwał) | AI potraktuje jako wymóg. Człowiek wyłapie sprzeczność | ★ mała (ryzyko: wygląda jak błąd klienta) |

## 7.3. Zasada dawkowania

**Nie przesadzać.** Optymalnie **2–3 miny na jedno zlecenie**. Jak dasz 6, doświadczony człowiek też się zgubi, a brief zacznie wyglądać sztucznie — moderator Useme może to wyłapać.

**Rekomendowany zestaw bazowy (do wplecenia w każde zlecenie):**
1. **Bait na nieistniejący moduł** (taktyka #1) — podmieniasz nazwę pod domenę.
2. **Canary phrase** (taktyka #2) — unikalna fraza pod domenę.
3. **Pytanie o granice** (taktyka #3) — ten sam mechanizm, inne brzmienie.

## 7.4. Jak czytać wyniki po zebraniu ofert

- Oferta traktuje nieistniejący moduł jako potwierdzoną funkcję → **AI (hallucynacja)**.
- Oferta zawiera frazę-znacznik → **prawdopodobnie AI przekleiło brief**.
- Oferta mówi wprost „tego nie da się zrobić / odradzam” → **prawie na pewno człowiek z doświadczeniem**.
- Oferta podaje konkretne dni/liczby → **człowiek** (AI unika liczb).
- Oferta wyłapuje sprzeczność liczbową lub pyta o wersję systemu → **człowiek**.

---

# 8. MANUAL: JAK ZMIENIAĆ ZLECENIE, ŻEBY NIE STRACIĆ MIN

## 8.1. Zasada nadrzędna

Miny są **wtopione w naturalny język briefu**. Nie wolno ich wyodrębniać, podkreślać ani tłumaczyć — muszą wyglądać jak zwykły wymóg klienta. Celem jest, by brief czytał się jak autentyczne ogłoszenie przedsiębiorcy.

## 8.2. Krok po kroku — procedura modyfikacji

1. **Zacznij od gotowego zlecenia bazowego** z pkt 3 tego dokumentu. Nie pisz od zera — kopiuj i adaptuj.

2. **Zidentyfikuj 3 miejsca na miny:**
   - Miejsce A: lista wymagań technicznych (tu wchodzi **nieistniejący moduł**).
   - Miejsce B: opis problemu lub wymagań (tu wchodzi **canary phrase**).
   - Miejsce C: prośba o ofertę (tu wchodzi **pytanie o granice**).

3. **Podmień nazwy pod domenę zlecenia** (patrz tabela 8.3). Miny NIE mogą być identyczne we wszystkich zleceniach — inaczej konkurencja je wyłapie i przestaną działać.

4. **Sprawdź naturalność.** Przeczytaj brief na głos. Jeśli mina „wystaje” — przeredaguj tak, by brzmiała jak wymóg biznesowy, nie jak test.

5. **Nie zmieniaj parametrów formularza** (kategoria, budżet, czas ofert) — miny dotyczą wyłącznie treści.

6. **Zapisz wersję z minami** obok wersji czystej, żeby móc porównać wyniki i wycofać miny, jeśli zniekształcą zbyt mocno brief.

## 8.3. Bank min pod domeny (do rotacji)

| Domena | Nieistniejący moduł (A) | Canary phrase (B) | Pytanie o granice (C) |
|---|---|---|---|
| ERP / Subiekt / BaseLinker | „tryb silent-guard zabezpieczający tabelę stanów” | „synchronizacja bez zatoru przy zapisach” | „czego nie da się zrobić przy takiej skali bazy” |
| Konfigurator 3D | „warstwa adaptive-mesh redukująca model w locie” | „podgląd bez klatkowania na telefonie” | „co odradzasz przy modelach z programu produkcyjnego” |
| Mobile native | „tryb deep-sync utrzymujący bazę w tle” | „aplikacja bez gubienia danych w tunelu” | „czego nie da się zrobić offline na starych telefonach” |
| Scraping / boty | „silnik stealth-fingerprint maskujący sesję” | „pobieranie bez bicia na biały ekran” | „jakich portali nie da się stabilnie obsłużyć” |
| PWA / panel B2B | „moduł auth-flow z podwójnym potwierdzeniem koszyka” | „zamówienia bez przestoju w godzinach szczytu” | „co odradzasz przy podziale na etapy” |
| IdoSell | „warstwa price-guard pilnująca progów rabatowych” | „cenniki bez rozjazdu między grupami” | „czego nie da się zrobić na standardowym API IdoSell” |

## 8.4. Checklist przed publikacją

- [ ] 3 miny wtopione w naturalny język (A + B + C).
- [ ] Nazwy min unikalne dla tej domeny (nie powtarzają się z innymi zleceniami).
- [ ] Brief czyta się jak autentyczne ogłoszenie przedsiębiorcy.
- [ ] Parametry formularza bez zmian.
- [ ] Zapisana wersja czysta + wersja z minami (do porównania).
- [ ] Notatka: które miny gdzie wtopiono (do analizy wyników).

## 8.5. Czego NIE robić

- ❌ Nie wstawiać więcej niż 3 min (brief traci naturalność).
- ❌ Nie używać tych samych min w różnych zleceniach (konkurencja wyłapie wzorzec).
- ❌ Nie tłumaczyć min w treści ani ich nie podkreślać.
- ❌ Nie dodawać min do parametrów formularza (kategoria, budżet) — tylko treść.
- ❌ Nie używać min, które mogą urazić wykonawcę lub wyglądać jak próba wyłudzenia darmowej konsultacji.

---

*Sekcje 7 i 8 stanowią operacyjny manual detekcji AI dla wszystkich zleceń badawczych z tego dokumentu.*