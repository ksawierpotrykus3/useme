# KARTA WIEDZY INŻYNIERSKIEJ — INTEGRACJE SUBIEKT GT / NEXO PRO

**Dokument wewnętrzny bota ofertowego | Wersja 2026.1 | Klasyfikacja: Elitarna**


## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1 Typowe zlecenia (na podstawie audytu #144890)

| Kategoria zlecenia | Opis | Częstotliwość |
|---|---|---|
| Integracja sklepu z Subiektem | Dwukierunkowa synchronizacja stanów i cen (WooCommerce, PrestaShop, Shoper) | ~40% |
| Integracja BaseLinker ↔ Subiekt | Pobieranie zamówień, wystawianie dokumentów, synchronizacja stanów z marketplace | ~30% |
| Automatyczne dokumenty | Wystawianie PA/PAi (paragony), FS (faktury), ZK z rezerwacją z poziomu API | ~20% |
| Warstwa API / middleware | Budowa REST API pośredniczącego między Subiektem a aplikacją webową klienta | ~10% |

### 1.2 Budżety i profil klienta

- **Widełki budżetowe:** 3 000 – 12 000 zł netto. Realne stawki rynkowe za profesjonalne integracje (dane z cenników integratorów na 2026): jednorazowa integracja BaseLinker + ERP od 4 900 zł netto, subskrypcja od 246 zł/mies. 
- **Profil zleceniodawcy:** właściciel e-commerce (1–3 kanały sprzedaży), hurtownia wielokanałowa (Allegro + sklep + marketplace), menedżer logistyki odpowiedzialny za zgodność stanów.
- **Poziom świadomości technicznej:** niski do średniego — klient zna problem biznesowy („stany się nie zgadzają”), ale nie zna ograniczeń architektonicznych Subiekta ani SQL Servera.


## 2. KRYTYCZNE REALIA TECHNOLOGICZNE — STAN NA 2026 ROK

### 2.1 Subiekt GT Sfera — architektura COM/OLE Automation

| Cecha | Wartość |
|---|---|
| Technologia | COM / OLE Automation, znana i sprawdzona technologia Microsoftu  |
| Architektura | 32-bitowa (procesy x86) |
| Licencja | **Osobny dodatek płatny** — cena netto ok. 945 zł za stanowisko (licencja elektroniczna, stan na 2025)  |
| Inicjalizacja | `gt = win32com.client.Dispatch("InsERT.Subiekt")` następnie `gt.Uruchom(True, True)`  |
| Silnik bazy | MS SQL Server 2008 R2 / 2012 / 2014 / nowsze  |
| Ograniczenie SQL Express | 1 GB adresowalnej pamięci RAM, 1 CPU, historycznie limit 10 GB bazy (wersje 2025+ zmieniły ten limit)  |

**Kluczowa mina:** Sfera GT działa wyłącznie w procesie 32-bitowym. Każde wywołanie COM przechodzi przez marshalling międzyprocesowy, co przy dużej częstotliwości (np. pollingu co 5 s) generuje gigantyczny narzut i jest podatne na timeouty.

### 2.2 Subiekt nexo PRO Sfera — architektura .NET

| Cecha | Wartość |
|---|---|
| Technologia | Natywna biblioteka .NET: `InsERT.Moria.*`, `InsERT.Mox.*`  |
| Architektura od v57 | .NET 8, wyłącznie x64  |
| Licencja | **Wbudowana w każdą licencję nexo PRO** — nie wymaga dokupywania dodatku |
| Kluczowe DLL | `InsERT.Moria.API.dll`, `InsERT.Moria.Sfera.dll`, `InsERT.Moria.ModelDanych.dll`, `InsERT.Mox.Core.dll`  |
| Praca z DI | Obsługa Dependency Injection, kontener wbudowany w SDK |

**Przełom v57 (2025/2026):** Wszystkie rozwiązania własne musiały zostać przebudowane na .NET 8 / x64. Instalatory z SDK starszych niż 57 przestały działać — lokalizacja folderu instalacyjnego zmieniła się z `C:\Program Files (x86)\InsERT\nexo` na `C:\Program Files\InsERT\nexo` .

### 2.3 Dokumenty handlowe i magazynowe — mapowanie procesów

| Dokument | Symbol | Skutek magazynowy | Rola w integracji |
|---|---|---|---|
| Zamówienie od klienta | **ZK** | Rezerwacja stanu (opcjonalnie pełna) | Dokument wstępny — tworzony automatycznie z zamówienia e-commerce |
| Wydanie zewnętrzne | **WZ** | **Tak — zdejmuje stan** | Realizacja wysyłki, generowany po spakowaniu |
| Faktura sprzedaży | **FS** | Pośrednio (przez WZ) | Dokument księgowy dla klienta B2B |
| Paragon fiskalny | **PA/PAi** | Pośrednio (przez WZ) | Sprzedaż detaliczna, wymaga sterownika fiskalnego |

**Krytyczne rozróżnienie:** ZK z rezerwacją **nie zdejmuje** stanu magazynowego — jedynie blokuje dostępność. Dopiero WZ wywołuje skutek magazynowy. Brak tego rozróżnienia w architekturze integracji prowadzi wprost do oversellingu (patrz sekcja 3).


## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1 Cytat klienta vs rzeczywistość

> **Klient pisze:** „Potrzebuję prostego skryptu, który co 5 minut aktualizuje stany magazynowe w WooCommerce i pobiera zamówienia do Subiekta.”

> **Co go utopi:** „Prosty skrypt” w Pythonie z pętlą `while True: subiekt.Towary[...]` uruchomiony na 3 kanałach sprzedaży jednocześnie.

### 3.2 MINA 1 — Deadlocki i blokady w MS SQL

Baza `InsERT` w Subiekcie GT **intensywnie lockuje tabele** przy operacjach zapisu. Krytyczne tabele:

- `tw__Towar` — kartoteki towarów (odczyt/zapis przy każdej aktualizacji ceny)
- `dok__Dokument` — nagłówki dokumentów (insert przy każdym ZK/FS)
- `st__Stan` — stany magazynowe (aktualizacja przy każdym WZ)
- `dok_Pozycja` — pozycje dokumentów (insert równolegle z nagłówkiem)

**Scenariusz awarii:** Trzy wątki (WooCommerce, BaseLinker, Allegro) próbują jednocześnie zapisać ZK na ten sam towar. Wątek A blokuje `tw__Towar`, wątek B czeka na `dok__Dokument`, wątek C na `st__Stan`. Powstaje klasyczny deadlock — SQL Server zabija jedno z połączeń, COM zwraca błąd `Lock timeout` lub `RPC_E_SERVERFAULT`, a transakcja przepada bez śladu.

**Dodatkowe ryzyko:** SQL Express z limitem **1 GB RAM** i **1 CPU** nie jest w stanie obsłużyć więcej niż 2–3 równoległych transakcji piszących bez degradacji wydajności. Przy bazie > 7 GB każdy zapis staje się operacją wysokiego ryzyka .

### 3.3 MINA 2 — Overselling (nadmiarowa sprzedaż)

**Mechanizm awarii:**
1. Klient kupuje ostatnią sztukę na Allegro → Sello tworzy ZK **bez rezerwacji**.
2. W tym samym momencie inny klient kupuje tę samą sztukę w WooCommerce → integrator tworzy kolejne ZK.
3. Żadne z ZK nie zdjęło stanu (ZK **nie ma skutku magazynowego**).
4. Subiekt pokazuje stan „1 szt.” dla obu zamówień.
5. Przy wystawianiu WZ okazuje się, że towaru fizycznie brak.

**Rozwiązanie:** ZK **musi** być tworzone z **pełną rezerwacją dostaw**. Tylko wtedy Subiekt zablokuje towar i kolejne ZK nie będzie w stanie zarezerwować nieistniejącego stanu .

### 3.4 MINA 3 — Wariantowość i mapowanie kartotek

**Problem:** W WooCommerce/PrestaShop produkt „Koszulka” ma warianty: rozmiar S/M/L × kolor czerwony/niebieski/zielony = 9 SKU. W Subiekcie GT te 9 wariantów to **9 osobnych kartotek** powiązanych polem `Model` lub cechami.

**Pułapka mapowania:** Integrator, który mapuje po `product_id` z WooCommerce (np. 1234 dla „Koszulki”), przypisze wszystkie 9 wariantów do jednej kartoteki. Subiekt GT nie zna pojęcia „produkt nadrzędny z wariantami” w sposób natywny dla API — wymaga to konfiguracji słownika **modele towarów** i pól własnych (`kolor`, `rozmiar`) .

**Rozwiązanie:** Mapowanie musi odbywać się po **EAN/PLU** lub **polu własnym `external_id`** zmapowanym na kartotekę Subiekta, nie po ID sklepu. Dla PrestaShop z wariantami wagowymi (np. herbata 50g/100g/250g) każdy wariant wagowy musi być osobną kartoteką w Subiekcie .


## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

Poniższe formuły są gotowymi „hakami”, które w pierwszych 2 zdaniach oferty deklasują 90% amatorów. Każda zawiera **problem architektoniczny**, którego klient nie zna, oraz **natychmiastowe pytanie kwalifikujące**.

### Formuła A — dla zleceń „prosta synchronizacja stanów”

> „Zanim cokolwiek zaimplementuję: Pana Subiekt GT lockuje tabelę `st__Stan` przy każdym zapisie, a przy trzech kanałach sprzedaży wysyłających równoległe requesty co 5 minut dojdzie do deadlocków MS SQL i utraty transakcji — to nie kwestia ‘prostego skryptu’, ale architektury kolejkowania. **Czy Państwa baza działa na SQL Server Express (limit 1 GB RAM / 10 GB bazy), czy na pełnym Standard/Enterprise?** To determinuje, czy w ogóle możemy mówić o synchronizacji w czasie rzeczywistym.”

### Formuła B — dla zleceń „automatyczne zamówienia z BaseLinkera”

> „BaseLinker wyśle zamówienie do Subiekta w momencie jego utworzenia — jeśli integrator utworzy ZK **bez rezerwacji**, ten sam towar zostanie sprzedany równolegle na Allegro i w sklepie, zanim ktokolwiek zdąży wystawić WZ. **Czy Państwa Subiekt ma włączoną pełną rezerwację dostaw na ZK, czy tworzy dokumenty bez blokowania stanu?** Od tego zależy, czy wdrożenie w ogóle ochroni Pana przed oversellingiem.”

### Formuła C — dla zleceń „API dla Subiekta”

> „Subiekt GT Sfera to 32-bitowa biblioteka COM z osobną licencją (~945 zł netto), a nexo PRO od wersji 57 działa wyłącznie na .NET 8 / x64 — te dwie architektury wykluczają ten sam kod integracyjny. **Czy pracujemy na Subiekcie GT ze Sferą, czy na nexo PRO?** Jeśli GT — czy Sfera jest już zakupiona i aktywowana na bieżącej wersji?”


## 5. CZERWONA LISTA — ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ)

### 5.1 Bezwzględny zakaz bezpośredniego SQL

> **NIE WOLNO** proponować ani akceptować rozwiązań typu `INSERT INTO dok__Dokument`, `UPDATE tw__Towar SET cena = ...`, `DELETE FROM dok_Pozycja`.

**Dlaczego to zabija bazę:**
- Subiekt GT nie używa triggerów do przeliczania kosztów FIFO/LIFO — te kalkulacje wykonuje **wyłącznie warstwa aplikacji (Sfera)**.
- Bezpośredni UPDATE na `tw__Towar` rozspójnia stany z historią dostaw i dokumentów magazynowych.
- INSERT do `dok__Dokument` bez odpowiedniego rekordu w `dok_Pozycja` i `st__Stan` tworzy „sierotę” — dokument widnieje w bazie, ale nie ma skutku magazynowego, co przy kolejnym przeliczeniu stanów powoduje błąd integralności.
- **Jedyna dozwolona droga zapisu:** Sfera COM (GT) lub `InsERT.Moria.*` (nexo PRO). Odczyt — SQL bezpośredni jest dopuszczalny TYLKO dla raportowania (widoki, `WITH (NOLOCK)`).

### 5.2 Zakaz „ciągłego pollingu co 10 sekund”

Polling bez kolejkowania i mechanizmu **delta sync** (timestamps / `rowversion`) to:
- Gwarantowane deadlocki przy > 1 kanale sprzedaży.
- Marnowanie cykli CPU na odpytywanie niezmienionych rekordów.
- Brak gwarancji kolejności zdarzeń — dwa zamówienia z tego samego SKU mogą zostać przetworzone w złej kolejności.

**Zamiast tego:** Webhooki (BaseLinker, WooCommerce), kolejka FIFO, mechanizm `LastModified` z bazy Subiekta.

### 5.3 Zakaz obiecywania „rozmowy telefonicznej” i „darmowej konsultacji”

Komunikacja na Useme jest **w 100% asynchroniczna i pisemna**. Proponowanie Google Meet / rozmowy telefonicznej to sygnał amatorski — profesjonalny oferent zadaje pytania w ofercie i oczekuje odpowiedzi w wątku zlecenia.


## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE

### 6.1 Schemat architektury

```
[WooCommerce]  [BaseLinker]  [Allegro REST]
      │              │              │
      └──────────────┼──────────────┘
                     ▼
         ┌───────────────────────┐
         │  KOLEJKA ASYNCHRONICZNA │  ← RabbitMQ / Redis / SQLite FIFO
         │  (jedna kolejka per kanał)│
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │  DEMON INTEGRACYJNY    │  ← Usługa Windows (.NET 8 / Python)
         │  (wrapper na Sferę)    │
         │  - SINGLE THREAD WRITE │
         │  - retry + circuit br.  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │    SUBIEKT (Sfera)     │
         │  GT COM / nexo .NET    │
         └───────────────────────┘
```

### 6.2 Rozbicie na moduły architektoniczne i wycena

| # | Moduł | Zakres | Nakład | Wycena (zł netto) |
|---|---|---|---|---|
| **1** | **Demon integracyjny** | Usługa Windows (.NET 8 / Python), wrapper na Sferę COM lub `InsERT.Moria.*`. Single-thread write queue. Obsługa błędów COM/DI. | 3–5 dni | 1 800 – 3 000 |
| **2** | **Kolejka asynchroniczna** | RabbitMQ / Redis / SQLite FIFO. Trwałość kolejki, retry z backoffem, dead-letter queue, idempotencja zleceń. | 2–3 dni | 1 200 – 2 000 |
| **3** | **Konektor e-commerce** | Klient API BaseLinker (REST), WooCommerce (REST v3), PrestaShop (Webservice), Allegro (REST). Mapowanie statusów i zdarzeń. | 3–4 dni | 1 800 – 2 800 |
| **4** | **Silnik mapowania kartotek i cen** | Mapowanie SKU/EAN/PLU → `tw__Towar`. Obsługa 10 poziomów cen Subiekta. Synchronizacja wariantów (model + cechy). | 3–4 dni | 1 800 – 2 800 |
| **5** | **Logowanie, monitoring, alerty** | Log transakcji (kto, kiedy, jaki dokument), powiadomienia e-mail/webhook przy błędach, dashboard statusu synchronizacji. | 2 dni | 1 200 – 1 800 |
| | **RAZEM** | | **13–18 dni** | **7 800 – 12 400** |

**Uwaga cenowa:** Realny rynek na 2026: integracje BaseLinker ↔ Subiekt GT w modelu subskrypcyjnym startują od 246 zł/mies. + koszt wdrożenia, a jednorazowe integracje od 4 900 zł netto . Wycena poniżej 4 500 zł za pełną integrację dwukierunkową z rezerwacją i kolejką jest **nierealna** — oznacza brak modułu kolejkowania (gwarantowane deadlocki) lub brak rezerwacji (gwarantowany overselling).


## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK ANALIZY)

Poniższe pytania należy wpleść w treść oferty — **nie na końcu**, ale w środku analizy technicznej. Ich jedyny cel: zmusić klienta do odpowiedzi w wiadomości prywatnej na Useme.

### Pytanie 1 — wersja i architektura Subiekta

> **„Czy pracują Państwo na Subiekcie GT ze Sferą (COM, 32-bit, osobna licencja ok. 945 zł netto), czy na Subiekcie nexo PRO (.NET 8 / x64, Sfera wbudowana w licencję)?”**

**Dlaczego to pytanie działa:** Odpowiedź determinuje całą architekturę — kod integracyjny dla GT i nexo PRO jest **niekompatybilny**. Jeśli klient nie wie, odpowie „muszę sprawdzić” → nawiązany kontakt.

### Pytanie 2 — baza danych i limit SQL Express

> **„Czy baza Subiekta działa na SQL Server Express (limit 1 GB RAM, 1 CPU, historycznie 10 GB bazy), czy na pełnym Standard/Enterprise? Przy Express musimy liczyć się z kolejką jednokierunkową i ograniczeniem wolumenu.”**

**Dlaczego to pytanie działa:** 80% małych firm używa darmowego Express. Klient, który nie wie o limicie 1 GB RAM, dostanie sygnał, że rozmawia z inżynierem, który rozumie jego infrastrukturę.

### Pytanie 3 — wolumen i rezerwacje

> **„Ile zamówień na dobę obsługują Państwo łącznie (sklep + marketplace + hurt)? Czy ZK w Subiekcie są tworzone z pełną rezerwacją dostaw, czy bez blokowania stanu?”**

**Dlaczego to pytanie działa:** Wymusza ujawnienie wolumenu (klucz do wyceny) i pokazuje, że rozumiemy ryzyko oversellingu. Klient, który nie wie, czy ma rezerwacje, jest idealnym kandydatem na wdrożenie z audytem.


**KONIEC KARTY WIEDZY**

*Dokument przeznaczony wyłącznie do wewnętrznego użytku bota ofertowego. Aktualizacja: 2026.*