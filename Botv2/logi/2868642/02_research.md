## Miny i pułapki przy wdrożeniu Comarch e-Sklep z Comarch ERP Optima (stacjonarna)

Poniżej zestawienie zidentyfikowanych min na podstawie dostępnej dokumentacji Comarch i źródeł branżowych. Każda mina zawiera dowód, mechanizm działania i konsekwencję.

---

### Mina 1: Wymagane moduły Kasa/Bank (KB) i Handel (HA) w Comarch ERP Optima

**Dowód:** Dokumentacja Comarch e-Sklep wprost stwierdza: „Do współpracy z Comarch e-Sklep konieczne jest posiadanie modułów w Comarch ERP Optima (minimum) Kasa/Bank (KB) i Handel (HA)”.

**Mechanizm:** Integracja e-Sklep z Optima nie jest samodzielnym dodatkiem – wymaga aktywnego modułu Handel oraz Kasa/Bank po stronie ERP. Bez tych modułów synchronizacja danych nie uruchomi się.

**Konsekwencja:** Jeśli klient posiada tylko podstawową licencję Optima bez modułu Handel, konieczne jest dokupienie modułu przed rozpoczęciem wdrożenia integracji. Opóźnienie startu i dodatkowy koszt po stronie klienta.

**Status:** Potwierdzone w oficjalnej dokumentacji Comarch.

---

### Mina 2: Integracja CDN.API zajmuje stanowisko licencyjne w Optima

**Dowód:** Analiza techniczna wskazuje: „CDN.API logs in as an operator, so your integration is a user in the licensing sense. It occupies a module seat while it works, and it competes for that seat with the people the system was bought for”. Dodatkowo: „Integrators who do this for a living put the integration's licences on a separate key, allocated to it exclusively”.

**Mechanizm:** Integracja działa jako operator w systemie Optima – pobiera licencję na moduł Handel/Kasa-Bank. W momencie gdy wszyscy użytkownicy pracują (np. przy zamykaniu miesiąca), automatyczna synchronizacja może nie uzyskać licencji lub odebrać ją użytkownikowi.

**Konsekwencja:** Konieczna jest dodatkowa licencja dostępowa dla integracji lub dedykowany klucz. Bez tego synchronizacja będzie przerywana w szczytowych momentach, a użytkownicy mogą być blokowani.

**Status:** Potwierdzone przez analizę techniczną (źródło branżowe, nie oficjalna dokumentacja Comarch).

---

### Mina 3: Limit bazy danych MS SQL Server Express (10 GB)

**Dowód:** „MS SQL Server Express editions from 2016 through 2022 cap a single database at 10 GB”. „A great many Optima installations run on Express because Express arrived with the installer. That was not a capacity decision. It was a default, taken years ago”.

**Mechanizm:** Integracja e-commerce generuje dużą liczbę operacji zapisu (synchronizacja towarów, zamówień, stanów). Jeśli Optima działa na darmowej wersji SQL Server Express, baza może osiągnąć limit 10 GB, co zablokuje zapisy.

**Konsekwencja:** Przed wdrożeniem należy sprawdzić wersję SQL Server i rozmiar bazy. Jeśli to Express – istnieje ryzyko, że integracja przyspieszy osiągnięcie limitu i konieczna będzie migracja do pełnej wersji SQL Server (dodatkowy koszt licencji).

**Status:** Potwierdzone przez dokumentację Microsoft (limit Express) i analizę techniczną.

---

### Mina 4: Brak zdefiniowanego rate limitu API

**Dowód:** „The Optima API has no rate limit. Comarch publishes no number you can design against, and that is a problem rather than the licence it sounds like”. „Nothing in the system will tell you that your five-minute polling loop is now the heaviest single consumer of a database that eleven people are trying to issue invoices in”.

**Mechanizm:** Brak limitu nie oznacza, że można odpytywać API bez ograniczeń. Przeciążenie bazy przez integrację objawia się spowolnieniem całego ERP, a nie błędem po stronie integracji.

**Konsekwencja:** Jeśli wdrożenie nie zaplanuje rozsądnych interwałów synchronizacji (np. zamiast co 5 minut – co 15–30 minut w godzinach pracy), może dojść do degradacji wydajności Optima dla wszystkich użytkowników. Problem ujawnia się dopiero po czasie.

**Status:** Potwierdzone przez analizę techniczną.

---

### Podsumowanie

| Mina | Dowód | Konsekwencja |
|------|-------|--------------|
| Brak modułów KB + HA | Dokumentacja Comarch | Konieczność dokupienia modułów, opóźnienie |
| Zajęcie stanowiska licencyjnego przez integrację | Analiza techniczna | Konieczna dodatkowa licencja lub dedykowany klucz |
| Limit 10 GB bazy SQL Express | Dokumentacja Microsoft + analiza | Ryzyko zablokowania zapisów, migracja do pełnego SQL |
| Brak rate limitu API | Analiza techniczna | Ryzyko przeciążenia bazy i spowolnienia ERP |

Wszystkie miny dotyczą warunków wstępnych lub ograniczeń infrastrukturalnych – nie są to problemy do naprawienia w trakcie wdrożenia, lecz czynniki, które należy zweryfikować przed złożeniem oferty.