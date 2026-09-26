# SYNTEZA BOJOWA BOTA — GRUPA 4: INFRASTRUKTURA, AI & SEGMENT BIZNESOWY (TECH-AGNOSTIC)
## DOKUMENT OPERACYJNY DLA GENERATORA OFERT USEME

**Wersja:** 1.0 | **Data:** 2026.Q4 | **Klasyfikacja:** Wewnętrzny dokument operacyjny bota ofertowego

---

## 1. STRATEGIA DEKLASACJI W PIERWSZYCH 2 ZDANIACH (KATALOG CIOSÓW OTWIERAJĄCYCH)

### 1.1 DEVOPS / DOCKER / LINUX / HARDENING / DISASTER RECOVERY

**Cel:** W 5 sekund klient ma pomyśleć: „Ten człowiek wie o moim systemie więcej niż ja".

| Wariant | Otwarcie (dokładnie 2 zdania) | Zastosowanie |
|---|---|---|
| **A — uniwersalny** | Zanim dotkniemy reverse proxy, sprawdzam czy baza danych ma jakikolwiek port opublikowany na `0.0.0.0` — to najczęstszy wektor przejęcia w 48h. Drugi priorytet to limity logów Dockera (`max-size: "50m"`), bo domyślny `json-file` bez limitu zapycha dysk w 6–8 tygodni i crashuje bazę. | Konfiguracja VPS, Docker Compose, hardening |
| **B — migracja do Docker** | Migracja na Docker Compose bez **izolowanej sieci `internal: true` dla bazy** i **limitów OOM** to przeniesienie tych samych problemów z bare-metal na kontenery — z bonusem w postaci szybszego zapychania dysku przez logi. Zaczynam od `daemon.json` z log-opts i limitami, dopiero potem piszę compose. | Legacy → Docker, konteneryzacja |
| **C — backup / disaster recovery** | Kopia zapasowa, która nie została **przetestowana procedurą odtworzenia (test restore)**, nie istnieje — to nie backup, to placebo. Druga rzecz: `cp -r` na żywym PGDATA to nie backup, to **gwarantowane uszkodzenie spójności transakcyjnej**. | Backup, restic, borg, S3, disaster recovery |
| **D — serwer po infekcji** | Pierwsze 15 minut to **nie** czyszczenie malware — to **odcięcie sieci** i pobranie snapshotu dysku do forensics. Drugie 15 minut: weryfikacja, czy backupy **nie zostały zaszyfrowane razem z danymi produkcyjnymi** — jeśli były na tym samym koncie S3 bez Object Lock, są bezużyteczne. | Forensics, ratowanie po włamaniu |

---

### 1.2 SQL / OPTYMALIZACJA / MIGRACJE (PostgreSQL, MySQL/MariaDB)

**Cel:** Klient ma zrozumieć, że problem nie leży tam, gdzie myśli — i że wykonawca to widzi.

| Wariant | Otwarcie (dokładnie 2 zdania) | Zastosowanie |
|---|---|---|
| **A — problem wydajności** | Przed dokupieniem RAM-u uruchom `EXPLAIN (ANALYZE, BUFFERS)` na trzech najczęstszych zapytaniach produkcyjnych i sprawdź, czy nie masz `Seq Scan` na tabeli z milionami rekordów oraz czy `temp read/written` nie wskazuje na zrzut sortowania na dysk przy zbyt małym `work_mem`. W 90% przypadków problemem nie jest brak pamięci, tylko brak indeksu na kluczu obcym lub N+1 w ORM. | „Baza muli", „CPU 100%", „strona wolno działa" |
| **B — migracja / DDL na dużej tabeli** | Standardowy `CREATE INDEX` na tabeli z 20 mln rekordów pobiera lock `SHARE` na całą tabelę i blokuje wszystkie zapisy na czas budowy indeksu — przy tej skali to godziny przestoju produkcyjnego. Jedyną bezpieczną opcją jest `CREATE INDEX CONCURRENTLY`, który nie blokuje DML, ale wymaga wydzielenia z bloku transakcji i obsługi potencjalnego stanu `INVALID`. | „Trzeba dodać kolumnę/indeks do tabeli z 20 mln rekordów" |
| **C — connection pooling** | PostgreSQL tworzy osobny proces OS dla każdego połączenia — przy 1000 równoczesnych klientów to 5–10 GB RAM wyłącznie na overhead, a `max_connections` (domyślnie 100) zostaje wyczerpany. W architekturze mikroserwisowej lub serverless brak poolera to wyrok śmierci na bazę przy pierwszym skalowaniu. | „Aplikacja muli przy 100+ użytkownikach", SaaS, serverless |
| **D — deadlocki** | Deadlocki w transakcjach to prawie zawsze niespójna kolejność blokowania wierszy — wątek A blokuje wiersz 1, potem 2; wątek B blokuje wiersz 2, potem 1. Naprawa wymaga analizy `pg_locks` i standaryzacji kolejności operacji w transakcjach biznesowych, nie zwiększania `deadlock_timeout`. | „Występują deadlocki w transakcjach" |

---

### 1.3 AI / RAG / LLM / WYSZUKIWANIE SEMANTYCZNE

**Cel:** Klient ma zobaczyć, że rozumiesz, gdzie jego obecne rozwiązanie zawodzi — zanim zdąży powiedzieć „mam problem z halucynacjami".

| Wariant | Otwarcie (dokładnie 2 zdania) | Zastosowanie |
|---|---|---|
| **A — dla klienta nietechnicznego** | Pana/Pani obecne rozwiązanie prawdopodobnie gubi połowę trafnych dokumentów, bo wyszukiwanie opiera się wyłącznie na podobieństwie semantycznym — a to nie działa na kodach produktów, numerach umów i nazwach własnych. Standardem produkcyjnym w 2026 roku jest wyszukiwanie hybrydowe: BM25 dla dokładnych identyfikatorów + wektory dla parafraz, scalone przez Reciprocal Rank Fusion i doprecyzowane przez Cross-Encoder Reranker. | Chatbot, wyszukiwarka semantyczna, RAG MVP |
| **B — dla klienta technicznego** | Dense-only retrieval na encjach takich jak SKU, ID zgłoszeń czy sygnatury metod generuje 5–8% awarii ugruntowania (RAGTruth 2026) — sam prompt tego nie naprawi. Architektura musi przejść na hybrydę BM25 + wektory z fuzją RRF i rerankingiem Cross-Encoder, a wyjście LLM musi być związane przez JSON Schema w trybie strict, inaczej nie ma gwarancji parsowalności. | Optymalizacja istniejącego RAG, systemy z cytowaniem źródeł |
| **C — dla projektu optymalizacyjnego** | Jeśli koszt tokenów rósł szybciej niż liczba zapytań, to prawdopodobnie każde zapytanie — nawet trywialne — idzie do modelu frontier. Routing krokowy (TRIM, ICLR 2026) pozwala przypisać tylko krytyczne kroki rozumowania do drogiego modelu, redukując koszt tokenów o 60–80% bez utraty dokładności. Druga dźwignia to re-ranking przed wywołaniem LLM — Cohere Rerank tnie 50 kandydatów do 5 za ~$0,30/10k dokumentów, oszczędzając tokeny kontekstu. | „Koszty API rosną", „chcę taniej", optymalizacja RAG |
| **D — dla zastosowań prawnych / compliance** | W zastosowaniach prawnych i compliance odpowiedź bez cytowania konkretnego dokumentu i strony jest bezwartościowa — klient musi móc zweryfikować źródło. To wymusza architekturę, w której każdy chunk niesie `source_document_id`, `page_number` i `section_title`, a LLM generuje odpowiedź przez Structured Outputs z polem `source_citations`. | Kancelarie, compliance, medycyna, audyt |

---

### 1.4 TECH-AGNOSTIC (SEGMENT BIZNESOWY — 33% RYNKU)

**Cel:** Klient nietechniczny ma zobaczyć stan docelowy — nie metodę, nie technologię, nie doświadczenie wykonawcy.

| Wariant | Otwarcie (dokładnie 2 zdania) | Zastosowanie |
|---|---|---|
| **A — automatyzacja przepisywania danych** | Wyobraź sobie, że faktury z maila same trafiają do Twojego Excela — bez przepisywania, bez błędów, bez siedzenia po godzinach. Program, który to robi, działa w tle i uruchamia się jednym kliknięciem. | „Ręcznie przepisuję faktury do Excela" |
| **B — synchronizacja danych** | Dane w Twoim sklepie i magazynie zawsze się zgadzają — bez ręcznego poprawiania. Program łączy oba systemy i aktualizuje wszystko automatycznie, gdy tylko pojawi się zmiana. | „Dane w sklepie nie zgadzają się z magazynem" |
| **C — raportowanie** | Raport, który teraz zajmuje Ci godzinę w piątek, będzie gotowy w 10 sekund — jednym kliknięciem. Dostajesz plik, który możesz od razu wysłać dalej. | „W piątek siedzę i robię raport" |
| **D — powtarzalne maile** | Maile do klientów wysyłają się same — w odpowiednim momencie, z właściwą treścią. Program pilnuje terminów i nie wymaga od Ciebie pamiętania o niczym. | „Wysyłam te same wiadomości do klientów" |

---

## 2. TABELA MIN TECHNICZNYCH (CO KLIENT PISZE VS CO GO UTOPI VS RIPOSTA BOTA)

| Technologia | Pozorne życzenie klienta | Prawdziwa mina pod maską | Twardy fakt inżynierski używany przez bota |
|---|---|---|---|
| **DevOps / Docker** | „Skonfiguruj mi serwer VPS pod aplikację w Dockerze" | Domyślny `json-file` bez limitu → logi zapychają `/var/lib/docker` → crash aplikacji i bazy w 6–8 tygodni | „Log-opts `max-size: 50m`, `max-file: 3` w `daemon.json` to nie opcja — to warunek przetrwania. Domyślny sterownik nie ma limitu." |
| **DevOps / Docker** | „Aplikacja czasem się zawiesza, restart pomaga" | Memory leak w Node/Python → OOM-killer zabija **bazę danych**, nie aplikację → uszkodzenie indeksów, utrata transakcji | „Limity `deploy.resources.limits.memory` dla każdego kontenera + `pids: 100`. OOM-killer nie wybiera aplikacji — wybiera proces o najwyższym zużyciu." |
| **DevOps / Docker** | „Chcę się łączyć z DataGripem z laptopa do Postgresa" | `ports: - "5432:5432"` → botnety skanują cały IPv4 w godzinach → przejęcie bazy w 48h | „Sieć `internal: true`, zero ekspozycji publicznej. Dostęp wyłącznie przez SSH tunnel `ssh -L 5432:localhost:5432` lub WireGuard." |
| **DevOps / Backup** | „Mamy skrypt kopiujący `/var/lib/docker/volumes/postgres_data`" | `cp -r` na żywej bazie → niekompletny WAL → baza w stanie crash recovery lub całkowicie nienadająca się do uruchomienia | „Backup bazy to **logiczny dump** (`pg_dump -Fc`), nie kopia plików. Kopia bez testu restore to placebo." |
| **DevOps / Backup** | „Zrobię backup na S3" | S3 bez Object Lock → ransomware szyfruje również backupy → odtworzenie niemożliwe | „S3 Object Lock w **Compliance mode** — WORM. Bez tego backup jest równie podatny na szyfrowanie jak dane produkcyjne." |
| **SQL / Wydajność** | „Dokupmy mocniejszy VPS, bo baza muli" | Seq Scan na wielomilionowej tabeli → problem to brak indeksu, nie brak RAM-u | „`EXPLAIN (ANALYZE, BUFFERS)` na trzech najczęstszych zapytaniach. `Seq Scan` na tabeli z milionami rekordów = brak indeksu, nie brak pamięci." |
| **SQL / Wydajność** | „Aplikacja muli przy 100+ użytkownikach" | Brak connection poolingu → każde żądanie otwiera nowe połączenie → proces OS 5–10 MB RAM → `max_connections` wyczerpany | „PgBouncer w trybie transaction pooling. PostgreSQL tworzy osobny proces OS dla każdego połączenia — przy 1000 klientów to 5–10 GB na overhead." |
| **SQL / Migracje** | „Trzeba dodać indeks do tabeli z 20 mln rekordów" | Standardowy `CREATE INDEX` blokuje wszystkie zapisy (lock `SHARE`) na czas budowy indeksu — godziny przestoju | „`CREATE INDEX CONCURRENTLY` — nie blokuje DML, wymaga wydzielenia z bloku transakcji i obsługi stanu `INVALID`." |
| **SQL / Migracje** | „Musimy zmienić typ kolumny w tabeli z 50 mln rekordów" | `ALTER TABLE` bez `ALGORITHM=INPLACE, LOCK=NONE` (MySQL) lub bez `pg_repack` (PostgreSQL) → blokada tabeli na godziny | „`pg_repack` dla PostgreSQL — kopia cienia, synchronizacja triggerami, atomowa podmiana bez downtime. Dla MySQL: `gh-ost` oparty na binlogu, bez triggerów." |
| **SQL / Deadlocki** | „Występują deadlocki w transakcjach" | Niespójna kolejność blokowania wierszy — wątek A blokuje 1→2, wątek B blokuje 2→1 | „Analiza `pg_locks` i standaryzacja kolejności operacji w transakcjach biznesowych. Zwiększanie `deadlock_timeout` to nie naprawa — to maskowanie." |
| **AI / RAG** | „Chatbot wymyśla odpowiedzi" | Brak ugruntowania w źródłach → retriever zwrócił chybione fragmenty → model generuje plausible brzmiącą odpowiedź | „5–8% awarii ugruntowania na modelach frontier to chybienia wyszukiwania (RAGTruth 2026). Bez hybrydowego wyszukiwania i rerankingu nie da się tego naprawić na poziomie promptu." |
| **AI / RAG** | „Klient dostał błędną informację o zwrocie" | Brak cytowań i identyfikowalności źródeł → odpowiedź bez `source_document_id` | „Każdy chunk musi nieść `source_document_id`, `page_number`, `section_title`. Prompt musi wymuszać format odpowiedzi z cytowaniem przez Structured Outputs." |
| **AI / RAG** | „Koszty API rosną szybciej niż liczba zapytań" | Każde zapytanie — nawet trywialne — idzie do modelu frontier | „RouteLLM: redukcja kosztów o 85% przez routing. TRIM (ICLR 2026): tylko krytyczne kroki do dużego modelu — 20% drogich tokenów." |
| **AI / RAG** | „Wdrożyliśmy RAG, ale odpowiedzi są słabe" | Proste dzielenie dokumentów po 500 znaków → chunk urwany w połowie zdania → brak kontekstu | „Recursive character splitting z nakładką 10–20% + chunkowanie semantyczne oparte na nagłówkach. Chunk musi być samowystarczalny semantycznie." |
| **Tech-Agnostic** | „Potrzebuję automatyzacji" | Klient nie odróżnia frontendu od backendu → każda wzmianka o technologii wywołuje paraliż decyzyjny | „Program działa w tle — jednym kliknięciem. Otwierasz komputer, na pulpicie jest ikona. Klikasz. Program robi resztę." |
| **Tech-Agnostic** | „Boję się, że programista zniknie" | Strach przed brakiem wsparcia po zakończeniu współpracy | „Dostaniesz nagranie wideo, jak obsługiwać program. Kod i dokumentacja zostaną przekazane na Twoją własność. Program działa na Twoim komputerze bez mojego udziału." |
| **Tech-Agnostic** | „Nie wiem, czego dokładnie potrzebuję" | Brak zdefiniowanego problemu → ryzyko budowy czegoś, czego klient nie użyje | „Zaczynamy od krótkiej diagnozy — 1–2 dni. Dostajesz prosty opis na piśmie, co program będzie robił i jak będzie wyglądał. Na tym etapie możesz się wycofać." |

---

## 3. ZESTAW PYTAŃ ZMUSZAJĄCYCH DO ODPOWIEDZI NA PRIV (W ŚRODEK TEKSTU)

**Zasada:** Pytania umieszcza się **w środku analizy oferty** — po opisaniu rezultatu, ale **przed wyceną**. Cel: zmusić klienta do natychmiastowego odpisania na priv i wejścia w tryb dialogu. Maksymalnie 2–3 pytania na ofertę.

### 3.1 DevOps / Docker / Linux

1. **Czy baza danych działa na tym samym hoście co aplikacja (single-node) i czy jest już w Dockerze, czy na bare-metal? Jeśli w Dockerze — czy jej port jest publikowany na `0.0.0.0`, czy wyłącznie w sieci wewnętrznej?**
   *Mapowanie:* odpowiedź determinuje, czy moduł 2 wymaga rekonfiguracji sieci (usunięcie `ports:` z bazy), czy tylko hardeningu istniejącej konfiguracji.

2. **Jaki jest obecny wolumen danych produkcyjnych (rozmiar bazy + uploadów) i jaki jest akceptowalny RTO (czas odtworzenia po awarii) oraz RPO (maksymalna utrata danych w minutach/godzinach)?**
   *Mapowanie:* RPO < 15 min = wymagany PITR (wal-g / pgBackRest). RTO < 1h = wymagany hot standby lub szybki restore ze snapshotu.

3. **Czy serwer był już skanowany przez CrowdSec/Lynis, czy w ostatnich 6 miesiącach były nieudane próby logowania SSH lub nietypowe procesy? Czy backupy już istnieją — a jeśli tak, czy był wykonywany test restore?**
   *Mapowanie:* Jeśli były incydenty — moduł 1 wymaga forensics przed hardeningiem. Jeśli backupy istnieją, ale bez testu restore — nie istnieją z punktu widzenia ciągłości działania.

---

### 3.2 SQL / Optymalizacja / Migracje

1. **Czy silnikiem jest PostgreSQL czy MySQL/MariaDB i w jakiej wersji?**
   *Mapowanie:* PostgreSQL 16/17 ma równoległe BRIN i ulepszone CTE; MySQL 8.0 ma natywne `ALGORITHM=INPLACE`. Wersja determinuje strategię migracji i dostępne indeksy.

2. **Jaki jest rozmiar największej tabeli w bazie i średni wolumen transakcji na sekundę (TPS) w szczycie?**
   *Mapowanie:* tabela 5 mln vs 500 mln rekordów wymaga zupełnie innego podejścia do migracji. TPS w szczycie determinuje, czy `CREATE INDEX CONCURRENTLY` w ogóle ma szansę się zakończyć.

3. **Czy macie włączone rozszerzenie `pg_stat_statements` (PostgreSQL) lub wgląd w slow 1 mln wektorów → Qdrant; PostgreSQL już w stacku → pgvector.

2. **Czy odpowiedzi muszą zawierać cytowanie konkretnego dokumentu i strony, czy wystarczy ogólna odpowiedź?**
   *Mapowanie:* w zastosowaniach prawnych i compliance cytowanie jest wymogiem twardym i wymusza Structured Outputs z polem `source_citations` — to zmienia architekturę promptu i walidacji.

3. **Jaki jest przewidywany miesięczny wolumen zapytań i czy koszt API jest kluczowym ograniczeniem?**
   *Mapowanie:* przy wolumenie >10 000 zapytań/miesiąc routing na małe modele (DeepSeek V4.1 Flash, Claude Haiku) redukuje koszt tokenów o 60–85% — ale wymaga dodatkowego modułu klasyfikacji intencji.

4. **Czy system ma być samodzielnym API, czy zintegrowanym z istniejącym CRM/ERP/stroną?**
   *Mapowanie:* klient ma już infrastrukturę PostgreSQL (pgvector naturalnym wyborem) czy Elasticsearch (upraszcza wdrożenie BM25).

---

### 3.4 Tech-Agnostic (Segment Biznesowy)

**Zestaw A — automatyzacja przepisywania danych:**

1. Ile czasu zajmuje Ci teraz ręczne przepisywanie danych — godzina dziennie, kilka godzin w tygodniu?
2. Czy dane, które przepisujesz, mają zawsze taki sam format, czy zdarzają się wyjątki?
3. Czy program, z którego teraz korzystasz, pozwala na eksport danych do pliku Excel/CSV?

**Zestaw B — synchronizacja między systemami:**

1. Z jakich programów teraz korzystasz — czy oba działają na tym samym komputerze, czy w przeglądarce?
2. Co się dzieje teraz, gdy dane się nie zgadzają — kto to poprawia i ile to zajmuje?
3. Czy dane muszą być aktualizowane natychmiast, czy wystarczy raz dziennie?

**Zestaw C — raportowanie:**

1. Jak często potrzebujesz raportu — codziennie, co tydzień, raz w miesiącu?
2. Co dokładnie zawiera raport — jakie kolumny, jakie podsumowania?
3. Komu wysyłasz raport i w jakiej formie — plik Excel, PDF, wiadomość mailowa?

**Zestaw D — ogólny (bez sprecyzowanego typu):**

1. Która czynność w Twojej pracy zajmuje najwięcej czasu i jest najbardziej powtarzalna?
2. Czy korzystasz z komputera z systemem Windows, czy pracujesz głównie w przeglądarce?
3. Kiedy program będzie gotowy — czy chcesz go uruchamiać na swoim komputerze, czy ma działać w tle bez Twojej obecności?

**Mechanizm psychologiczny:** Pytanie wymusza aktywność — klient musi przetworzyć odpowiedź, wrócić do komputera, sprawdzić jak coś działa. To buduje zaangażowanie i sprawia, że odpisu je na priv.

---

## 4. CZERWONA LISTA ANTYWZORCÓW (AUTOMATYCZNA DYSKWALIFIKACJA)

### 4.1 DevOps / Docker / Linux — ZAKAZY ABSOLUTNE

| Antywzorzec | Dlaczego zabija ofertę |
|---|---|
| `ports: - "5432:5432"` w Docker Compose | Natychmiastowa dyskwalifikacja w oczach CTO — publiczne zaproszenie do przejęcia bazy w 48h |
| `USER root` w Dockerfile | Kontener root = root na hoście przy breakout. Junior nie wie, że to wyrok |
| `cp -r /var/lib/docker/volumes/...` jako backup | Gwarantowane uszkodzenie spójności transakcyjnej bazy |
| „Skonfiguruję Nginx i certbot" bez TLS 1.3 i HSTS | Klient techniczny wie, że TLS 1.2 to już nie standard w 2026 |
| „Zrobię backup na S3" bez Object Lock | Backup na S3 bez WORM = ransomware szyfruje również backup |
| „Użyję fail2ban" bez wzmianki o CrowdSec | W 2026 fail2ban to legacy — klient techniczny to wyłapie |
| Brak `log-opts` w `daemon.json` | Domyślny `json-file` bez limitu = zapchany dysk w 6–8 tygodni |
| Brak limitów `deploy.resources.limits` | OOM-killer zabije bazę danych, nie aplikację |

### 4.2 SQL / Optymalizacja / Migracje — ZAKAZY ABSOLUTNE

| Antywzorzec | Dlaczego zabija ofertę |
|---|---|
| „Dokup mocniejszy VPS jako pierwszą rekomendację" | To nie diagnoza, to unikanie diagnozy. Skalowanie pionowe maskuje problem na 2 tygodnie |
| „Uruchomimy migrację DDL w godzinach szczytu" | `CREATE INDEX` bez `CONCURRENTLY` zablokuje cały serwis |
| „Nie trzeba connection poolera, mamy mało ruchu" | Przy architekturze mikroserwisowej lub serverless brak poolera to gwarantowany problem przy pierwszym skalowaniu |
| „Zoptymalizujemy zapytania przez dodanie indeksów na wszystkich kolumnach" | Każdy indeks spowalnia INSERT/UPDATE/DELETE. Indeksować tylko kolumny w `WHERE`, `JOIN`, `ORDER BY` o wysokiej selektywności |
| „Zwiększymy `work_mem` globalnie do 1 GB" | `work_mem` jest per operacja sortowania. Przy 100 równoczesnych zapytaniach 1 GB × 100 = 100 GB RAM → OOM killer zabije bazę |

### 4.3 AI / RAG / LLM — ZAKAZY ABSOLUTNE

| Antywzorzec | Dlaczego zabija ofertę |
|---|---|
| Proste dzielenie dokumentów po 500 znaków | Niszczy kontekst — chunk musi być samowystarczalny semantycznie |
| Brak walidacji schematów wyjściowych | Poleganie na tym, że LLM „zwróci JSON" bez `strict: true` i `json_schema` to przepis na awarię produkcyjną |
| Brak rerankingu przy top-k > 10 | Wstrzykiwanie 20–50 fragmentów do promptu bez rerankingu to marnowanie tokenów i degradacja jakości |
| Brak routingu na małe modele | Wysyłanie każdego zapytania — w tym klasyfikacji intencji — do modelu frontier to niepotrzebne koszty |
| Brak metadanych o źródle w chunku | Chunk bez `source_document_id`, `page_number` i `section` uniemożliwia cytowanie — w prawie i compliance wymóg twardy |
| Brak ewaluacji na danych klienta | Wdrażanie RAG bez zestawu testowego to zgadywanie, nie inżynieria |

### 4.4 Tech-Agnostic — ZAKAZY ABSOLUTNE

| Antywzorzec | Dlaczego zabija ofertę |
|---|---|
| „Używam React, FastAPI, Postgres" | Klient nie wie, co to znaczy. Brzmi jak próba onieśmielenia |
| „Mam 5 lat doświadczenia w programowaniu" | Klient nie kupuje doświadczenia — kupuje rozwiązanie problemu |
| „Zbuduję REST API z endpointami" | Zero informacji o tym, co to da klientowi |
| „Wdrożę na serwerze VPS z Dockerem" | Klient nie wie, co to VPS ani Docker |
| „Proponuję spotkanie na Google Meet" | Zasada kanału: wyłącznie pisemnie na priv |
| „To zależy od wielu czynników" | Brak konkretu = brak zaufania |
| „Mogę to zrobić za X zł" bez rozbicia | Ryczałt bez modułów wywołuje opór |
| Ściana tekstu bez akapitów | Klient nietechniczny przestaje czytać po 3 linijkach |
| Tabele techniczne w ofercie | Nie umieszczać specyfikacji technicznej w ofercie dla tech-agnostic |
| Pytania o system operacyjny / API / stack | „Na czym teraz pracujesz — Windows czy Mac?" zamiast „Jaki masz system operacyjny?" |

---

## 5. MODUŁOWE SZABLONY KOSZTORYSÓW DLA ELITY (4 500 – 16 000 ZŁ)

### 5.1 DevOps / Docker / Linux / Disaster Recovery (4 000 – 9 000 zł)

| # | Moduł | Zakres | Czas | Wycena (zł) |
|---|---|---|---|---|
| **1** | **Audyt i hardening bazowy Linux** | SSH Ed25519, UFW/nftables, CrowdSec, unattended-upgrades, zram, `sysctl` hardening, audit sesji | 4–6h | 1 000 – 1 500 |
| **2** | **Środowisko Docker z polityką bezpieczeństwa** | `daemon.json` (log-opts, userns-remap), rootless mode, izolowane sieci bridge, limity `deploy.resources`, `USER 1001` w Dockerfile | 4–6h | 1 200 – 1 800 |
| **3** | **Reverse proxy + routing SSL/TLS** | Wybór proxy, konfiguracja TLS 1.3, HSTS, CSP, X-Frame-Options, ACME (Let's Encrypt / Cloudflare), Traefik + socket-proxy | 4–5h | 1 000 – 1 500 |
| **4** | **Pipeline backupów 3-2-1-1-0** | Restic/Borg, `pg_dump` ze spójnością, deduplikacja, szyfrowanie, S3 z Object Lock, retencja, automatyczny test restore | 6–8h | 1 500 – 2 500 |
| **5** | **Monitoring i alerty** | Node Exporter, Uptime Kuma (lub Grafana Cloud), alerty Telegram/Discord, monitoring certyfikatów, dysku, RAM | 3–4h | 800 – 1 200 |
| **6** | **Dokumentacja i handover** | Runbook: procedury restore, rotacja kluczy, skalowanie, troubleshooting | 2–3h | 500 – 800 |
| | **RAZEM** | | **23–32h** | **4 000 – 9 000** |

**Strategia ofertowa:** Moduły 1–3 jako **pakiet bazowy** (hardening + Docker + SSL). Moduły 4–5 jako **pakiet ciągłości** (backup + monitoring). Moduł 6 **zawsze w cenie** — runbook to dowód profesjonalizmu.

---

### 5.2 SQL / Optymalizacja / Migracje (4 500 – 11 000 zł)

| # | Moduł | Zakres | Czas | Wycena (zł) |
|---|---|---|---|---|
| **1** | **Audyt metryk i profilowanie powolnych zapytań** | `pg_stat_statements` / slow 80%, RAM >75%, backup fail, cert expiry <14 dni.
- Monitoring rozmiaru `/var/lib/docker` — zanim zapcha się do 100%.

---

#### Zanim przejdę do wyceny — 3 pytania, od których zależy architektura

**1. Czy baza danych działa na tym samym hoście co aplikacja i czy jest już w Dockerze, czy na bare-metal? Jeśli w Dockerze — czy jej port jest publikowany na `0.0.0.0`, czy wyłącznie w sieci wewnętrznej?**

*Odpowiedź determinuje, czy moduł 2 wymaga rekonfiguracji sieci (usunięcie `ports:` z bazy), czy tylko hardeningu istniejącej konfiguracji.*

**2. Jaki jest obecny wolumen danych produkcyjnych (rozmiar bazy + uploadów) i jaki jest akceptowalny RTO (czas odtworzenia po awarii) oraz RPO (maksymalna utrata danych w minutach/godzinach)?**

*RPO < 15 min = wymagany PITR (wal-g / pgBackRest). RTO < 1h = wymagany hot standby lub szybki restore ze snapshotu. To bezpośrednio wpływa na moduł 4.*

**3. Czy backupy już istnieją — a jeśli tak, czy był wykonywany test restore?**

*Jeśli backupy istnieją, ale bez testu restore — nie istnieją z punktu widzenia ciągłości działania. To argument za modułem 4.*

---

#### Wycena modułowa — płacisz za architekturę, nie za godziny

| Moduł | Zakres | Wycena |
|---|---|---|
| **1. Audyt i hardening bazowy Linux** | SSH Ed25519, UFW/nftables, CrowdSec, unattended-upgrades, zram, `sysctl` hardening | 1 200 zł |
| **2. Docker z polityką bezpieczeństwa** | `daemon.json`, rootless mode, izolowane sieci, limity `deploy.resources`, `USER 1001` | 1 500 zł |
| **3. Reverse proxy + SSL/TLS** | Traefik + ACME, TLS 1.3, HSTS preload, CSP, Cloudflare Tunnel (opcjonalnie) | 1 200 zł |
| **4. Pipeline backupów 3-2-1-1-0** | Restic do S3 z Object Lock, `pg_dump -Fc`, retencja, automatyczny test restore | 1 800 zł |
| **5. Monitoring i alerty** | Node Exporter, Uptime Kuma, alerty Telegram/Discord, monitoring certyfikatów | 900 zł |
| **6. Dokumentacja i handover** | Runbook: procedury restore, rotacja kluczy, skalowanie, troubleshooting | 600 zł |
| **RAZEM** | | **7 200 zł** |

**Co dostajesz w cenie:**

- Serwer skonfigurowany według standardów produkcyjnych 2026 — nie „standardowa konfiguracja VPS".
- Backup, który został przetestowany procedurą restore — nie placebo.
- Monitoring, który powie Ci o problemie, zanim aplikacja padnie.
- Runbook — dokumentację, która pozwoli Ci działać samodzielnie.
- **Kod i konfiguracja na Twoją własność** — nie jesteś zależny ode mnie.

**Czego nie robię:**

- Nie konfiguruję bazy z portem na `0.0.0.0` — to zaproszenie do przejęcia.
- Nie robię backupu przez `cp -r` na żywej bazie — to gwarantowane uszkodzenie spójności.
- Nie używam `fail2ban` — w 2026 to legacy, CrowdSec ma lepszą wykrywalność.
- Nie proponuję spotkań wideo ani calli — komunikacja wyłącznie pisemna na priv.

---

#### Co dalej

Odpowiedz na powyższe 3 pytania na priv — na tej podstawie potwierdzę zakres i termin. Pierwszy moduł (audyt) mogę rozpocząć w ciągu 48 godzin od akceptacji.

---

*Oferta przygotowana na podstawie audytu infrastruktury i standardów produkcyjnych 2026. Wszystkie moduły rozliczane etapowo — płacisz za rezultat, nie za godziny.*

---

**KONIEC DOKUMENTU OPERACYJNEGO**

---

*Dokument zatwierdzony do użytku wewnętrznego generatora ofert Useme. Aktualizacja kwartalna — następny przegląd: 2026.Q1.*