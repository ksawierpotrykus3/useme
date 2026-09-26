# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## BLOK: BAZY DANYCH SQL (PostgreSQL, MySQL / MariaDB)

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1. Typowe zlecenia w tym bloku

| Sygnał w treści zlecenia | Rzeczywisty problem architektoniczny |
|---|---|
| „Aplikacja muli przy 100+ jednoczesnych użytkownikach” | Brak connection poolingu — każde żądanie otwiera nowe połączenie do PostgreSQL. Każde połączenie to osobny proces OS zużywający 5–10 MB RAM. Przy 1000 równoczesnych klientów to 5–10 GB wyłącznie na overhead połączeń, zanim baza wykona jakąkolwiek pracę. |
| „CPU bazy dobija do 100% przy normalnym ruchu” | Seq Scan na wielomilionowej tabeli zamiast Index Scan. ORM generuje zapytania bez indeksów na kluczach obcych. |
| „Trzeba bezpiecznie dodać kolumnę/indeks do tabeli z 20 mln rekordów” | Standardowy `CREATE INDEX` w PostgreSQL blokuje wszystkie operacje zapisu na tabeli (lock SHARE) na czas budowy indeksu — przy 20 mln rekordów to godziny przestoju. |
| „Baza rośnie, trzeba archiwizować stare dane” | Brak polityki retencji + brak indeksów BRIN dla danych szeregów czasowych. Tabela historyczna nie jest odpytywana przez indeks, tylko przez Seq Scan. |
| „Występują deadlocki w transakcjach” | Niespójna kolejność blokowania wierszy w transakcjach biznesowych (wątek A blokuje wiersz 1, potem 2; wątek B blokuje wiersz 2, potem 1). |

### 1.2. Budżety i profil klienta

- **Budżet:** 3 000 – 12 000 zł (typowo 4 500 – 11 000 zł za pełny pakiet audyt + optymalizacja + migracje).
- **Profil klienta:**
  - Właściciel platformy SaaS (znający technologię, ale bez dedykowanego DBA).
  - Główny programista szukający wsparcia DBA przy konkretnym problemie (np. „dodaj indeks bez downtime”).
  - Firma e-commerce po wpadce w Black Friday — serwer bazy padł przy szczycie ruchu.
- **Poziom techniczny:** półtechniczny do technicznego. Klient rozumie pojęcia typu `EXPLAIN`, `index`, `deadlock`, ale nie potrafi samodzielnie zdiagnozować wąskiego gardła. **Wyczuwa marketingowe lanie wody w 2 zdaniach.**

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1. Diagnoza wąskich gardeł — `EXPLAIN (ANALYZE, BUFFERS)` i `pg_stat_statements`

Podstawą diagnostyki w PostgreSQL jest jednoczesne użycie dwóch narzędzi:

**`pg_stat_statements`** — rozszerzenie śledzące zagregowane statystyki wykonania zapytań. Pozwala zidentyfikować najkosztowniejsze zapytania nawet jeśli pojedynczo wykonują się szybko, ale uruchamiane są dziesiątki tysięcy razy na minutę. Zapytanie 3 ms wykonywane 40 000 razy na minutę kosztuje 2 minuty CPU na każde 60 sekund — i tylko jedno z tych zapytań pojawi się w slow  95% odczytów.
- `shared read` — strony czytane z dysku (zbyt mały `shared_buffers`).
- `temp read/written` — **krytyczny sygnał**: `work_mem` jest zbyt mały, sortowanie/hashowanie zrzucane jest na dysk do plików tymczasowych.

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...;
```

**Krytyczna różnica:** Seq Scan vs Index Scan / Bitmap Index Scan. Seq Scan na tabeli z 15 mln rekordów przy każdym odświeżeniu koszyka oznacza, że PostgreSQL czyta całą tabelę, aby znaleźć 300 wierszy. To jest problem indeksu, nie problem RAM-u.

### 2.2. Indeksowanie zaawansowane

**Indeksy częściowe (`WHERE deleted_at IS NULL`)** — indeksują wyłącznie wiersze spełniające warunek filtrujący. Jeśli 80% rekordów to soft-deleted, indeks częściowy jest **5–20× mniejszy** od pełnego indeksu B-Tree, szybszy w utrzymaniu (INSERT/UPDATE nie aktualizują indeksu dla usuniętych wierszy) i szybszy w skanowaniu.

```sql
CREATE INDEX CONCURRENTLY idx_users_email_active
ON users (email)
WHERE deleted_at IS NULL;
```

**Indeksy pokrywające (`INCLUDE`)** — dodają kolumny niebędące kluczem wyszukiwania, umożliwiając **Index Only Scan** bez odwołania do tabeli (heap). Kluczowa uwaga: `INCLUDE` inhibuje deduplikację wartości w indeksie, więc indeks może być większy niż klasyczny wielokolumnowy. Ma sens wyłącznie gdy tabela zmienia się na tyle rzadko, że mapa all-visible jest aktualna — inaczej i tak nastąpi odwołanie do heap.

```sql
CREATE INDEX CONCURRENTLY idx_orders_covering
ON orders (user_id)
INCLUDE (amount, status);
```

**Indeksy wielokolumnowe** — kolejność kolumn ma znaczenie. Indeks `(user_id, order_date DESC)` obsłuży `WHERE user_id = ?` oraz `WHERE user_id = ? AND order_date > ?`, ale **nie** obsłuży `WHERE order_date > ?` (brak lewej kolumny prefiksu).

**Indeksy BRIN (Block Range Index)** — dla danych naturalnie uporządkowanych (timestamp, sekwencje) i bardzo dużych tabel append-only. BRIN przechowuje min/max wartości dla zakresów stron (domyślnie 128 stron, można zmniejszyć do 32 dla lepszej selektywności). Rozmiar indeksu BRIN to **ułamek rozmiaru B-Tree** — w benchmarku AWS na tabeli 126 GB dwa indeksy BRIN zajmowały po 24 KB każdy, redukując rozmiar bazy o 19,8% i skracając czas ładowania metryk o 12 minut.

```sql
CREATE INDEX CONCURRENTLY idx_readings_time_brin
ON readings USING BRIN (time)
WITH (pages_per_range = 32);
```

**PostgreSQL 17** wprowadza **równoległą budowę indeksów BRIN** — istotne dla bardzo dużych tabel.

### 2.3. Connection pooling — BgBouncer vs Supavisor (stan 2026)

PostgreSQL tworzy **osobny proces OS dla każdego połączenia**, zużywający 5–10 MB RAM. Przy 1000 równoczesnych klientów to 5–10 GB wyłącznie na overhead, a `max_connections` (domyślnie 100) zostaje wyczerpany — nowe żądania otrzymują `FATAL: sorry, too many clients already`.

| Cecha | PgBouncer | Supavisor |
|---|---|---|
| Język | C | Elixir (BEAM VM) |
| Zużycie RAM | ~2 MB na 1000 klientów | Zaprojektowany dla setek tysięcy połączeń |
| Tryb transaction pooling | ✓ | ✓ (port 6543) |
| Prepared statements w transaction mode | Konfigurowalne (wsparcie dodane w 2026) | Domyślnie wyłączone; wymaga obejść w ORM |
| Zastosowanie | Klasyczne aplikacje serwerowe, dedykowane instancje | Serverless, edge functions, multi-tenant SaaS |

**PgBouncer** pozostaje standardem dla tradycyjnych aplikacji — lekki, sprawdzony, wspiera prepared statements po konfiguracji. **Supavisor** to rozwiązanie Supabase dla serverless i edge — obsługuje 1M+ połączeń, ale transaction pooling domyślnie wyłącza prepared statements, co wymaga dostosowania w ORM (Prisma, Drizzle, SQLAlchemy).

**Krytyczne:** W architekturze mikroserwisowej lub serverless **brak connection poolera to wyrok śmierci** na bazę przy pierwszym skalowaniu. Transaction pooling to standard — session pooling nie multiplexuje wystarczająco agresywnie.

### 2.4. Migracje Zero-Downtime — stan 2026

**PostgreSQL:** Standardowy `CREATE INDEX` (bez `CONCURRENTLY`) pobiera lock `SHARE` na tabeli — blokuje wszystkie operacje zapisu (INSERT/UPDATE/DELETE) na czas budowy indeksu. Przy tabeli z 20 mln rekordów i 200 GB danych to godziny, w których aplikacja nie może zapisywać.

**`CREATE INDEX CONCURRENTLY`** — pobiera `SHARE UPDATE EXCLUSIVE`, który **nie blokuje** operacji DML (zapisów i odczytów), blokuje jedynie inne DDL. Wymaga dwóch skanów tabeli, może zakończyć się niepowodzeniem pozostawiając indeks w stanie `INVALID` — wówczas należy go usunąć `DROP INDEX CONCURRENTLY` i ponowić.

**Ograniczenie krytyczne:** `CREATE INDEX CONCURRENTLY` **nie może być uruchomiony wewnątrz bloku transakcji**. Wiele narzędzi migracyjnych (Drizzle, niektóre konfiguracje Flyway) domyślnie opakowuje każdą migrację w transakcję — co powoduje błąd wykonania. Konieczne jest wydzielenie kroku nie-transakcyjnego (np. `autocommit_block` w Alembic).

**`pg_repack`** — dla operacji wymagających przepisania całej tabeli (`VACUUM FULL`, `CLUSTER`, zmiana typu kolumny). Tworzy kopię cienia, synchronizuje zmiany przez triggery, następnie atomowo podmienia tabelę. **Nie wymaga downtime** ani wyłącznego dostępu do tabeli (poza krótkim momentem na początku i końcu operacji).

**MySQL/MariaDB:**
- **`ALTER TABLE ... ALGORITHM=INPLACE, LOCK=NONE`** — natywny online DDL InnoDB. Operacja przebudowuje tabelę, ale zezwala na równoczesne DML. Domyślne w MySQL 8.0 dla wielu operacji. **Nie wszystkie zmiany wspierają INPLACE** — dodanie kolumny STORED generated wymaga `ALGORITHM=COPY`, który blokuje tabelę.
- **`gh-ost`** — standard w 2026 dla MySQL. Oparty na binlogu, **nie tworzy triggerów** na tabeli źródłowej. Tworzy tabelę cienia, kopiuje dane w chunkach, śledzi binlog dla zmian, przełącza atomowo. Brak triggerów = brak write amplification i trigger lock  „Przed dokupieniem RAM-u uruchom `EXPLAIN (ANALYZE, BUFFERS)` na trzech najczęstszych zapytaniach produkcyjnych i sprawdź, czy nie masz `Seq Scan` na tabeli z milionami rekordów oraz czy `temp read/written` nie wskazuje na zrzut sortowania na dysk przy zbyt małym `work_mem`. W 90% przypadków problemem nie jest brak pamięci, tylko brak indeksu na kluczu obcym lub N+1 w ORM.”

**Insight 2 — Ryzyko migracji:**
> „Standardowy `CREATE INDEX` na tabeli z 20 mln rekordów pobiera lock `SHARE` na całą tabelę i blokuje wszystkie zapisy na czas budowy indeksu — przy tej skali to godziny przestoju produkcyjnego. Jedyną bezpieczną opcją jest `CREATE INDEX CONCURRENTLY`, który nie blokuje DML, ale wymaga wydzielenia z bloku transakcji i obsługi potencjalnego stanu `INVALID`.”

---

## 5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ)

❌ **„Dokup mocniejszy VPS jako pierwszą rekomendację”** — to nie diagnoza, to unikanie diagnozy. Skalowanie pionowe maskuje problem na 2 tygodnie i nie rozwiązuje Seq Scan ani N+1.

❌ **„Uruchomimy migrację DDL w godzinach szczytu”** — `CREATE INDEX` bez `CONCURRENTLY` zablokuje cały serwis. Nawet `CONCURRENTLY` dodaje obciążenie I/O i autovacuum — planować na okno serwisowe.

❌ **„Nie trzeba connection poolera, mamy mało ruchu”** — przy architekturze mikroserwisowej lub serverless brak poolera to gwarantowany problem przy pierwszym skalowaniu. Każde wywołanie funkcji Lambda otwiera nowe połączenie do PostgreSQL.

❌ **„Zoptymalizujemy zapytania przez dodanie indeksów na wszystkich kolumnach”** — każdy indeks spowalnia INSERT/UPDATE/DELETE. Indeksować tylko kolumny używane w `WHERE`, `JOIN`, `ORDER BY` i mające wysoką selektywność.

❌ **„Zwiększymy `work_mem` globalnie do 1 GB”** — `work_mem` jest per operacja sortowania/hashowania. Przy 100 równoczesnych zapytaniach 1 GB × 100 = 100 GB RAM → OOM killer zabije bazę.

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 500 – 11 000 ZŁ)

### Moduł 1 — Audyt metryk i profilowanie powolnych zapytań (1 200 – 2 000 zł)

- Włączenie i konfiguracja `pg_stat_statements` (PostgreSQL) lub `slow_ 0, długość transakcji > 5 min, deadlocki > 0.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU OFERTY)

1. **Czy silnikiem jest PostgreSQL czy MySQL/MariaDB i w jakiej wersji?** — od tego zależą dostępne mechanizmy: PostgreSQL 16/17 ma równoległe BRIN i ulepszone CTE; MySQL 8.0 ma natywne `ALGORITHM=INPLACE`. Wersja determinuje strategię migracji i dostępne indeksy.

2. **Jaki jest rozmiar największej tabeli w bazie i średni wolumen transakcji na sekundę (TPS) w szczycie?** — tabela 5 mln rekordów vs 500 mln rekordów wymaga zupełnie innego podejścia do migracji. TPS w szczycie determinuje, czy `CREATE INDEX CONCURRENTLY` w ogóle ma szansę się zakończyć, czy trzeba użyć `pg_repack` / `gh-ost`.

3. **Czy macie włączone rozszerzenie `pg_stat_statements` (PostgreSQL) lub wgląd w slow query log (MySQL/MariaDB)?** — brak tych narzędzi oznacza, że diagnoza jest zgadywaniem. Jeśli nie są włączone, pierwszym krokiem audytu jest ich aktywacja i zebranie danych z 24–48 godzin normalnego ruchu.

---

*Karta zweryfikowana na podstawie dokumentacji PostgreSQL 16/17, MySQL 8.0, Supabase Docs (2026), AWS RDS Best Practices (2025–2026) oraz benchmarków społecznościowych z 2026 roku.*