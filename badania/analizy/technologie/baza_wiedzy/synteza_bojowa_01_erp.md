# SYNTEZA BOJOWA BOTA — GRUPA 1: ERP & INTEGRACJE FINANSOWO-MAGAZYNOWE
## DOKUMENT OPERACYJNY DLA GENERATORA OFERT USEME

### 1. STRATEGIA DEKLASACJI W PIERWSZYCH 2 ZDANIACH (KATALOG CIOSÓW OTWIERAJĄCYCH)

**Comarch ERP Optima + KSeF 2.0:**
> „Od 1 lutego 2026 faktury krajowe są w KSeF jako XML FA(3) — budowanie OCR dla nich to palenie 60% budżetu. Realny problem architektoniczny to nie odczyt PDF, a tolerancja groszowa VAT między FA(3) a rejestrem VAT w Optimie i deduplikacja dokumentów przychodzących jednocześnie z KSeF i mailem.”

**Subiekt GT (Sfera COM):**
> „Zanim cokolwiek zaimplementuję: Pana Subiekt GT lockuje tabelę `st__Stan` przy każdym zapisie, a przy trzech kanałach sprzedaży wysyłających równoległe requesty co 5 minut dojdzie do deadlocków MS SQL i utraty transakcji — to nie kwestia ‘prostego skryptu’, ale architektury kolejkowania. Czy Państwa baza działa na SQL Server Express (limit 1 GB RAM / 10 GB bazy), czy na pełnym Standard/Enterprise?”

**Subiekt nexo PRO (Sfera .NET):**
> „Subiekt GT Sfera to 32-bitowa biblioteka COM z osobną licencją (~945 zł netto), a nexo PRO od wersji 57 działa wyłącznie na .NET 8 / x64 — te dwie architektury wykluczają ten sam kod integracyjny. Czy pracujemy na Subiekcie GT ze Sferą, czy na nexo PRO, gdzie Sfera jest wbudowana w licencję?”

**Enova365:**
> „Zanim dotkniemy integracji — czy Państwa enova365 ma aktywną licencję na moduł Soneta WebAPI? Bez niego każda integracja z KSeF przez REST jest niemożliwa bezpośrednio z systemu, a obejście przez SQL do tabel Sonety kończy się cichą utratą spójności danych przy najbliższej aktualizacji schematu.”

**Odoo:**
> „Jeśli Państwa modyfikacje Odoo były robione przez edycję plików w `odoo/addons/`, to przy najbliższej aktualizacji (17→18) stracą Państwo wszystkie zmiany — a jeśli pole zostało dodane do rdzenia, Odoo może crashować przy logowaniu. Standardowa naprawa to refaktoryzacja do modułu dziedziczącego `_inherit`.”

### 2. TABELA MIN TECHNICZNYCH

| Technologia | Pozorne życzenie klienta | Prawdziwa mina pod maską | Twardy fakt inżynierski używany przez bota |
|-------------|---------------------------|---------------------------|--------------------------------------------|
| **Comarch Optima + KSeF** | „Chcemy prosty OCR AI z czytaniem faktur PDF i zapisem do Optimy” | OCR dla faktur krajowych po 1.02.2026 to spalanie budżetu – są w KSeF jako XML FA(3). Prawdziwe wyzwania: tolerancja groszowa VAT i deduplikacja. | FA(3) zawiera komplet pól (P_1, P_2A, P_11, P_12, P_13_x, P_14_x). VAT liczony od sumy vs od pozycji daje rozjazd do 1 grosza na 15% faktur. Klucz deduplikacji: NIP + NumerFakturyOryginalny + DataWystawienia. |
| **Subiekt GT** | „Potrzebuję prostego skryptu, który co 5 minut aktualizuje stany i pobiera zamówienia” | Deadlocki MS SQL przy równoległych zapisach na `tw__Towar`, `dok__Dokument`, `st__Stan`. Overselling, bo ZK bez rezerwacji nie zdejmuje stanu. | Sfera GT to 32-bit COM z osobną licencją (~945 zł). ZK z pełną rezerwacją blokuje stan. Tylko Sfera (COM) może zapisywać – bezpośredni SQL psuje FIFO/LIFO i integralność. |
| **Subiekt nexo PRO** | „Integracja przez API Subiekta” | Od v57 nexo PRO działa wyłącznie na .NET 8 / x64. Stary kod x86 nie zadziała. Sfera wbudowana w licencję. | `InsERT.Moria.*`, `InsERT.Mox.*` – wymagane .NET 8. Lokalizacja `C:\Program Files\InsERT\nexo`. |
| **Enova365** | „Mamy stary dodatek, który przestał działać po aktualizacji” | Prawdopodobnie bezpośredni SQL do tabel Sonety – cicha utrata spójności przy zmianie schematu. Brak obsługi LockException. | Soneta WebAPI to płatny moduł. Zapis wyłącznie przez sesje `Soneta.Business.Session`. LockException przy współbieżności – konieczna kolejka FIFO per typ dokumentu. |
| **Odoo** | „Chcemy dostosować Odoo do naszych potrzeb” | Edycja plików w `odoo/addons/` zamiast modułu `_inherit` – aktualizacja nadpisze zmiany, możliwy crash przy logowaniu. N+1 queries. | Od Odoo 17 `_inherit` na klasach rejestru poza frameworkiem jest zabronione. Custom moduły w `custom_addons/`. KSeF przez `l10n_pl_edi` (FA(3)), certyfikat `.pem`. |

### 3. ZESTAW PYTAŃ ZMUSZAJĄCYCH DO ODPOWIEDZI NA PRIV

**Comarch Optima + KSeF:**
1. „Czy Państwa Comarch ERP Optima pracuje w modelu stacjonarnym (serwer Windows w siedzibie), czy w Chmurze Comarch (`OptimaCloudMode = true`)? Od tego zależy, czy integracja pójdzie przez CDN.API (tylko Windows, in-process), czy przez Comarch ERP Web API (REST, chmura).”
2. „Jaki procent faktur kosztowych to faktury krajowe z NIP PL (które po 1 lutego 2026 są w KSeF jako XML FA(3)), a jaki to faktury zagraniczne, paragony, WZ lub dokumenty spoza KSeF? Od tego zależy, czy OCR jest w ogóle potrzebny, czy wystarczy konektor KSeF API 2.0.”
3. „Czy posiadają Państwo moduł Handel / Kasa / Magazyn (faktury zakupowe trafiają do modułu handlowego z mapowaniem pozycji), czy wyłącznie Księga Handlowa / Rejestry VAT (dokumenty trafiają bezpośrednio do rejestru VAT bez rozbijania na pozycje)? To determinuje, czy mostek importowy musi mapować pozycje na towary, czy tylko nagłówek dokumentu.”

**Subiekt GT / nexo PRO:**
1. „Czy pracują Państwo na Subiekcie GT ze Sferą (COM, 32-bit, osobna licencja ok. 945 zł netto), czy na Subiekcie nexo PRO (.NET 8 / x64, Sfera wbudowana w licencję)?”
2. „Czy baza Subiekta działa na SQL Server Express (limit 1 GB RAM, 1 CPU, historycznie 10 GB bazy), czy na pełnym Standard/Enterprise? Przy Express musimy liczyć się z kolejką jednokierunkową i ograniczeniem wolumenu.”
3. „Ile zamówień na dobę obsługują Państwo łącznie (sklep + marketplace + hurt)? Czy ZK w Subiekcie są tworzone z pełną rezerwacją dostaw, czy bez blokowania stanu?”

**Enova365:**
1. „Czy Państwa licencja enova365 obejmuje aktywny moduł Soneta WebAPI, czy integracja ma być realizowana przez Harmonogram Zadań z zapisem do pliku/bazy pośredniej?”
2. „Czy obecny dodatek/integracja używa bezpośredniego SQL do tabel Sonety, czy operuje przez obiekty `Soneta.Business`?”
3. „Jaki jest klucz idempotencji dla dokumentów w Państwa systemie — numer KSeF, NIP + numer obcy, czy inny? Czy przy duplikacie system ma tworzyć nowy dokument, czy aktualizować istniejący?”

**Odoo:**
1. „Czy istniejące customizacje Odoo są w `custom_addons/` jako moduły dziedziczące, czy były wprowadzane przez edycję plików w `odoo/addons/`?”
2. „Czy Państwa Odoo ma już włączoną integrację KSeF w `l10n_pl_edi` i skonfigurowany certyfikat `.pem`? Jaki jest obecny status wysyłki faktur do KSeF — ręczna, przez cron, czy brak?”
3. „Czy modyfikacje są wersjonowane w Git i czy istnieje środowisko staging z dumpem produkcyjnym do testowania aktualizacji?”

### 4. CZERWONA LISTA ANTYWZORCÓW (AUTOMATYCZNA DYSKWALIFIKACJA)

- **Zakaz bezpośredniego SQL do tabel ERP** (Comarch `CDN.*`, Subiekt `tw__Towar`, `dok__Dokument`, `st__Stan`, Enova tabele Sonety). Łamie licencję, psuje integralność, uniemożliwia upgrade.
- **Zakaz edycji plików rdzenia Odoo** (`odoo/addons/`). Zawsze moduł `_inherit` w `custom_addons/`.
- **Zakaz pomijania obsługi `LockException`** w Enova365 – wymagany retry z backoffem i kolejka FIFO per typ dokumentu.
- **Zakaz tworzenia ZK bez rezerwacji w Subiekcie** – gwarantowany overselling.
- **Zakaz obiecywania 100% bezobsługowego księgowania** – zawsze panel korekt i akceptacja wyjątków (5–15%).
- **Zakaz proponowania rozmów telefonicznych, Google Meet, Zoom** – komunikacja wyłącznie pisemna na priv.
- **Zakaz używania `self.env.registry['model']._inherit` poza frameworkiem Odoo.**
- **Zakaz pollingu bez kolejkowania i delta sync** – deadlocki.
- **Zakaz OCR dla faktur krajowych objętych KSeF** – to XML FA(3).
- **Zakaz sztywnej walidacji równości groszowej VAT** – stosować tolerancję ±0,02 zł.

### 5. MODUŁOWE SZABLONY KOSZTORYSÓW DLA ELITY (4 500 - 16 000 ZŁ)

**Dla integracji Comarch Optima + KSeF:**
- M1: Konektor źródeł (KSeF API 2.0 + IMAP/Drive) – 1 800–3 500 zł
- M2: Silnik parsowania FA(3) + OCR AI dla zagranicy – 2 000–4 000 zł
- M3: Moduł walidacji biznesowej i tolerancji VAT – 1 500–2 500 zł
- M4: Mostek importowy do Optimy (Praca Rozproszona / CDN.API / Web API) – 2 000–4 000 zł
- M5: Panel korekt i zatwierdzeń – 1 500–3 000 zł
- M6: Wdrożenie i 30 dni asysty – 1 200–2 000 zł
**Suma:** 10 000–19 000 zł (pełny zakres); 6 500–12 000 zł (podstawowy: M1–M4 + M6).

**Dla Subiekt GT / nexo PRO:**
- M1: Demon integracyjny (wrapper na Sferę, single-thread write queue) – 1 800–3 000 zł
- M2: Kolejka asynchroniczna (RabbitMQ/Redis/SQLite FIFO) – 1 200–2 000 zł
- M3: Konektor e-commerce (BaseLinker, WooCommerce, PrestaShop, Allegro) – 1 800–2 800 zł
- M4: Silnik mapowania kartotek i cen – 1 800–2 800 zł
- M5: Logowanie, monitoring, alerty – 1 200–1 800 zł
**Suma:** 7 800–12 400 zł.

**Dla Enova365:**
- M1: Analiza i projekt interfejsu – 2 000–3 500 zł
- M2: Warstwa transportowa (Soneta WebAPI) – 2 500–4 500 zł
- M3: Logika biznesowa i mapowanie – 3 000–5 000 zł
- M4: Harmonogram i kolejkowanie – 1 500–2 500 zł
- M5: Rekoncyliacja i monitoring – 1 500–2 500 zł
- M6: Testy i dokumentacja – 1 500–2 500 zł
**Suma:** 12 000–20 500 zł (pełny); 5 000–14 000 zł (M2–M4).

**Dla Odoo:**
- M1: Audyt istniejących customizacji – 1 500–2 500 zł
- M2: Moduł dziedziczący (`_inherit`) – 2 500–4 500 zł
- M3: Warstwa OWL – 2 000–3 500 zł
- M4: Integracja KSeF (`l10n_pl_edi`) – 1 500–2 500 zł
- M5: Migracja/upgrade – 2 500–4 500 zł
- M6: Testy i dokumentacja – 1 500–2 500 zł
**Suma:** 11 500–20 000 zł (pełny); 4 500–14 000 zł (M2–M4).

### 6. WZORCOWA OFERTA BOJOWA 1:1 (BENCHMARK MISTRZOWSKI)

**Zlecenie:** Integracja KSeF 2.0 z Comarch ERP Optima dla biura rachunkowego obsługującego 50 podmiotów. Budżet klienta: 8 000–12 000 zł.

**Treść oferty:**

Od 1 lutego 2026 faktury krajowe są w KSeF jako XML FA(3) — budowanie OCR dla nich to palenie 60% budżetu. Realny problem architektoniczny to nie odczyt PDF, a tolerancja groszowa VAT między FA(3) a rejestrem VAT w Optimie i deduplikacja dokumentów przychodzących jednocześnie z KSeF i mailem.

Biuro rachunkowe na Optimie ma trzy równoległe kanały dokumentów: KSeF API, skrzynka IMAP i praca rozproszona od klientów. Bez bufora akceptacji dla księgowej — zamiast bezpośredniego zapisu do rejestru VAT — każdy błąd parsowania FA(3) ląduje w księdze. Pytanie brzmi: czy księgowa ma widzieć kolejkę wyjątków, czy ma dostawać gotowe dokumenty do zatwierdzenia.

Zanim przejdę do wyceny, muszę ustalić trzy rzeczy:
1. Czy Państwa Optima pracuje w modelu stacjonarnym (serwer Windows), czy w Chmurze Comarch (`OptimaCloudMode = true`)? Od tego zależy, czy integracja pójdzie przez CDN.API (tylko Windows, in-process), czy przez Comarch ERP Web API (REST, chmura).
2. Jaki procent faktur kosztowych to faktury krajowe z NIP PL (KSeF XML), a jaki to faktury zagraniczne, paragony, WZ? Od tego zależy, czy OCR jest w ogóle potrzebny.
3. Czy posiadają Państwo moduł Handel/Kasa/Magazyn, czy wyłącznie Księga Handlowa/Rejestry VAT? To determinuje, czy mostek importowy musi mapować pozycje na towary, czy tylko nagłówek dokumentu.

Proponowana architektura modułowa:
- M1: Konektor źródeł (KSeF API 2.0 + IMAP) – 2 500 zł
- M2: Parser FA(3) + OCR dla zagranicy – 2 500 zł
- M3: Walidacja biznesowa i tolerancja VAT – 1 800 zł
- M4: Mostek importowy do Optimy (wariant zależny od odpowiedzi) – 2 500 zł
- M5: Panel korekt i zatwierdzeń – 2 000 zł
- M6: Wdrożenie i 30 dni asysty – 1 500 zł
Razem: 12 800 zł netto.

Jeśli odpowiedzą Państwo na powyższe pytania, przygotuję precyzyjną wycenę w ciągu 24 godzin. Proszę o odpowiedź w wiadomości prywatnej.