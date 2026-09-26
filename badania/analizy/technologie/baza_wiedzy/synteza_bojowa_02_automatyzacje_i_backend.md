# SYNTEZJA BOJOWA BOTA — GRUPA 2: WEB SCRAPING, AUTOMATYZACJE B2B & BACKEND
## DOKUMENT OPERACYJNY DLA GENERATORA OFERT USEME

---

### 1. STRATEGIA DEKLASACJI W PIERWSZYCH 2 ZDANIACH (KATALOG CIOSÓW OTWIERAJĄCYCH)

Poniżej gotowe, bezbłędne otwarcia dla każdej technologii z grupy. Każde uderza w newralgiczny punkt techniczny, buduje wrażenie wiedzy o systemie klienta i nie zawiera ani jednego słowa o „doświadczeniu”, „chęci pomocy” czy „zaproszeniu do kontaktu”.

**Web Scraping (Cloudflare / DataDome / Akamai / TLS JA4):**
> „Cloudflare Turnstile blokuje `requests` na poziomie TLS ClientHello, zanim wyśle pierwszy bajt HTTP — zanim wydasz budżet na Selenium: sprawdźmy, czy istnieje endpoint REST/PWA z danymi hydratacji (`__NEXT_DATA__`, `window.__APOLLO_STATE__`), wtedy `curl_cffi` z JA4 spoofingiem wystarczy. Jeśli nie, potrzebna jest architektura z rezydencjalnym proxy i stealth browserem, bo DataDome flaguje datacenter IP przy pierwszym żądaniu.”

**FastAPI / Celery / Redis (webhooki płatności, automatyzacje B2B):**
> „Stripe dostarcza webhooki z gwarancją at-least-once — bez warstwy deduplikacji po `event_id` Państwa system wystawi podwójne faktury przy pierwszym lagu sieciowym. Architektura wymaga wzorca Fast-Ack: endpoint zwraca 200 OK w <50 ms, a przetwarzanie odbywa się asynchronicznie w workerze Celery z kolejką Redis i Dead Letter Queue.”

**NestJS / Node.js (backend, WebSockets, gRPC):**
> „Backend WebSocket bez Redis Adaptera to gwarantowana awaria przy pierwszym skalowaniu poziomym — wiadomości z instancji A nigdy nie dotrą do użytkownika na instancji B, a klient nawet nie zobaczy błędu, tylko zamrożony interfejs. Zanim wdrożymy Socket.io, trzeba zaprojektować warstwę broadcastu przez Redis Streams z persystencją ostatnich N wiadomości i sticky sessions na load balancerze.”

**.NET 8/9 / EF Core / MassTransit:**
> „Problem, który Państwo opisują, to klasyczny objaw dwóch antywzorców EF Core: Change Tracker utrzymujący referencje do wszystkich pobranych encji (brak `.AsNoTracking()`) oraz Cartesian Explosion przy wielokrotnym `.Include()` na tym samym poziomie relacji. W pierwszym kroku wyłączam Change Tracker dla operacji read-only i wprowadzam `.AsSplit „Pani/Pana skrypt przestaje działać po 6 minutach, ponieważ Google wymusza twardy limit wykonania na każdym pojedynczym uruchomieniu — i nie da się go obejść. Rozwiązaniem nie jest szybszy kod, ale architektura porcjowa z continuation triggers, która przetwarza dane w partiach i automatycznie wznawia pracę.”

---

### 2. TABELA MIN TECHNICZNYCH (CO KLIENT PISZE VS CO GO UTOPI VS RIPOSTA BOTA)

| Technologia | Pozorne życzenie klienta | Prawdziwa mina pod maską | Twardy fakt inżynierski używany przez bota |
|---|---|---|---|
| **Web Scraping** | „Prosty scraper w Pythonie do pobierania 50k produktów dziennie z 5 sklepów. Budżet: 2000 zł.” | Cloudflare/DataDome blokują na poziomie TLS JA4 i HTTP/2 SETTINGS; datacenter IP flagowane natychmiast; selektory DOM zmieniają się co 2–4 tygodnie; brak rotacji proxy = 403 | `curl_cffi` z JA4 spoofingiem omija TLS fingerprinting; dla DataDome konieczne proxy rezydencjalne; reverse-engineering API mobilnego (GraphQL) redukuje koszty 20×; `fetchAll` z porcjami 3–5 żądań |
| **FastAPI / Celery** | „Webhook, który po opłaceniu zamówienia w Stripe przesyła dane do CRM i wystawia fakturę.” | Brak idempotencji → podwójne faktury; synchroniczne przetwarzanie → timeouty i wyłączenie webhooka przez Stripe po 72 h; brak HMAC = fałszywe zdarzenia | At-least-once delivery wymusza deduplikację po `event_id` (atomowy INSERT z unique constraint); Fast-Ack + kolejka Redis/Celery z DLQ; weryfikacja HMAC-SHA256 na surowych bajtach; `task_acks_late=True` |
| **NestJS / Node.js** | „Dodajcie WebSockets do backendu, żeby przesyłać lokalizację kierowców do 5000 użytkowników na żywo.” | Brak Redis Adaptera → wiadomości nie propagują się między instancjami; brak rate limitingu → 25 mln dostarczeń/s przy 500 kierowcach i 5000 użytkowników; brak heartbeat → zombie połączenia; synchroniczne operacje blokują Event Loop | Redis Adapter (Pub/Sub) lub Redis Streams dla reliable delivery; rate limiting per socket (1 wiadomość/500 ms); binarny format (MessagePack) redukuje payload 4×; Worker Threads dla CPU-bound; FastifyAdapter daje 2–3× wyższy RPS |
| **.NET 8/9** | „Aplikacja zjada za dużo pamięci, raporty ładują się minutami, potrzebujemy optymalizacji.” | Change Tracker śledzi wszystkie encje (brak `AsNoTracking`); Cartesian Explosion przy równoległych `Include`; brak Outbox → utrata eventów przy crashu bazy; `BackgroundService` kończy host przy nieobsłużonym wyjątku | `AsNoTracking()` dla read-only; `AsSplit500/min (platforma B2B)?” — determinuje dobór brokera (Redis vs RabbitMQ) i liczbę workerów.
2. „Czy istnieje wymóg SLA na czas od otrzymania webhooka do wystawienia faktury w ERP? Czy faktura musi być wystawiona w <5 sekund, czy akceptowalne jest okno 30–60 sekund z kolejką asynchroniczną?” — determinuje potrzebę kolejki priorytetowej.
3. „Gdzie docelowo ma działać system: VPS klienta, chmura (AWS/GCP/Azure) czy infrastruktura on-premise? Czy są wymagania compliance (RODO, PCI DSS) dotyczące rezydencji danych?” — determinuje wybór regionu i architektury.

**NestJS / Node.js:**
1. „Ile jednoczesnych połączeń WebSocket ma obsługiwać system w szczycie i czy backend docelowo działa na więcej niż jednej instancji za load balancerem? Jeśli tak — czy warstwa broadcastu jest już zaprojektowana pod Redis Adapter, czy obecny kod zakłada jeden proces Node.js?”
2. „Czy system docelowo będzie podzielony na osobne serwisy (np. serwis użytkowników, zamówień, powiadomień), czy pozostaje modularnym monolitem? Jeśli mikrousługi — jakie są wymagania opóźnień komunikacji wewnętrznej i czy rozważaliście gRPC zamiast REST/JSON?”
3. „Czy w backendzie są operacje blokujące Event Loop — generowanie raportów, eksporty, transformacje dużych zbiorów danych, synchroniczne operacje kryptograficzne? Czy obecny monitoring obejmuje Event Loop Lag i czy mierzyliście P99 tego wskaźnika pod obciążeniem produkcyjnym?”

**.NET 8/9:**
1. „Czy docelowe środowisko to chmura (Azure/AWS) czy Windows Server on-prem z usługą instalowaną przez `sc.exe`? Od tego zależy wybór brokera (Azure Service Bus vs RabbitMQ) i strategia deploymentu.”
2. „Jaka wersja .NET i silnika bazy danych jest obecnie używana? Jeśli to .NET Framework 4.x lub EF6, modernizacja do .NET 8/9 wymaga przepisania warstwy danych — to zmienia zakres prac.”
3. „Jaki jest wolumen pobieranych rekordów przy pojedynczym zapytaniu raportowym? Poniżej 10 000 — `AsNoTracking` + indeksy wystarczą. Powyżej 100 000 — konieczna projekcja, paginacja i potencjalnie Dapper dla krytycznych ścieżek.”
4. „Czy system downstream wymaga gwarancji exactly-once dla eventów? Jeśli tak, Transactional Outbox + idempotentny konsument to warunek konieczny — bez tego każdy crash bazy może trwale usunąć event z systemu.”

**Apps Script:**
1. „Czy zleceniodawca pracuje na koncie Google Workspace (firmowym), czy consumer (gmail.com)? Ma to bezpośredni wpływ na dzienny limit triggerów — 90 minut vs 6 godzin — i determinuje architekturę kolejkowania.”
2. „Ile wierszy/rekordów ma być przetwarzanych w jednym cyklu? Czy 5000 to wartość stała, czy rośnie w czasie? Przy jakim wolumenie obecny skrypt przestaje działać?”
3. „Skąd dokładnie pochodzą dane — z maila (`GmailApp`), z API zewnętrznego (`UrlFetchApp`), czy z innego arkusza? Czy obecny trigger jest czasowy, czy oparty na zdarzeniu (onEdit/onChange)?”
4. „Czy przetwarzanie może trwać 15–30 minut w tle, pod warunkiem, że dane są kompletne i nikt nie ingeruje w arkusz w trakcie? Czy jest wymóg, aby całość zakończyła się w jednym oknie czasowym?”

---

### 4. CZERWONA LISTA ANTYWZORCÓW (AUTOMATYCZNA DYSKWALIFIKACJA)

Bot pod żadnym pozorem nie może popełnić poniższych błędów.

**Web Scraping:**
- ❌ Używanie `requests` + BeautifulSoup na stronach za Cloudflare/DataDome — blokada na TLS ClientHello.
- ❌ Brak rotacji proxy rezydencjalnych przy WAF enterprise (DataDome, Akamai).
- ❌ Obietnica „100% niewykrywalności” — nie istnieje.
- ❌ Ignorowanie kosztów proxy w wycenie (klient musi wiedzieć o $1–$15/GB).
- ❌ Brak memory management dla headless Chromium (wycieki RAM przy długotrwałym działaniu).
- ❌ Poleganie wyłącznie na selektorach CSS/X1 instancji backendu.
- ❌ Operacje blokujące CPU w głównym wątku (JSON.parse na gigantycznym payloadzie, pętle po 500k elementów, synchroniczne crypto).
- ❌ Twierdzenie, że Express jest najlepszym silnikiem dla NestJS przy wysokim RPS (>10 000).
- ❌ Brak connection poolingu przy ORM (domyślne `pg.Pool` max: 10 jest zbyt niskie).
- ❌ Brak walidacji DTO na granicy aplikacji.
- ❌ Używanie `forwardRef()` jako standardowego rozwiązania circular dependencies.

**.NET 8/9:**
- ❌ `DbContext` jako singleton (nie jest thread-safe).
- ❌ Brak `.AsNoTracking()` dla zapytań read-only.
- ❌ Brak `.AsSplitQuery()` przy równoległych `Include` (Cartesian Explosion).
- ❌ Brak Transactional Outbox przy wymaganiu exactly-once.
- ❌ `BackgroundService` bez obsługi wyjątków i bez jawnego exit code (proces zombie).
- ❌ Sekrety w `appsettings.json` zamiast `dotnet user-secrets` / Azure Key Vault.

**Apps Script:**
- ❌ Pętla `for` z `setValue()` wewnątrz — 10 000 wywołań API = timeout.
- ❌ Obietnica „skryptu na 30 minut” — limit 6 minut jest nieprzekraczalny.
- ❌ Brak zapisu stanu między wykonaniami (duplikaty, nieskończone pętle).
- ❌ `fetchAll()` z 10+ żądaniami w jednej partii (błąd „Bandwidth quota exceeded”).
- ❌ Ignorowanie różnicy consumer vs Workspace (90 min vs 6 h dziennie).
- ❌ Stosowanie `onEdit` do batch processingu.

---

### 5. MODUŁOWE SZABLONY KOSZTORYSÓW DLA ELITY (4 500 – 16 000 ZŁ)

Poniżej rozbicie na moduły architektoniczne dla każdej technologii. Każdy moduł adresuje konkretne ryzyko produkcyjne, co uzasadnia wysoką wycenę.

#### 5.1 Web Scraping (4 000 – 8 500 zł)

| Moduł | Zakres | Czas | Wycena |
|---|---|---|---|
| M1: Analiza anty-bot i reverse-engineering API | Identyfikacja endpointów (REST/GraphQL), test JA3/JA4, analiza challengey, wybór strategii | 1–2 dni | 800–1 200 zł |
| M2: Moduł rotacji sesji i proxy | Integracja proxy rezydencjalnych/mobilnych, rotacja per sesja, monitoring zużycia GB | 1 dzień | 600–1 000 zł |
| M3: Silnik parsowania i normalizacji | Pydantic schemas, normalizacja danych, deduplikacja, obsługa błędów parsowania | 1–2 dni | 800–1 500 zł |
| M4: Baza danych i pipeline eksportu | PostgreSQL/ClickHouse, eksport CSV/Parquet/JSON, API do odczytu danych | 1–2 dni | 800–1 500 zł |
| M5: Monitoring, alerty i retry policy | Prometheus/Grafana, alerty RAM/success rate, exponential backoff | 1 dzień | 600–1 000 zł |
| **RAZEM** | | **5–8 dni** | **4 000–8 500 zł** |

#### 5.2 FastAPI / Celery / Redis (6 300 – 12 000 zł)

| Moduł | Zakres | Czas | Wycena |
|---|---|---|---|
| M1: Warstwa odbiorcza API | FastAPI endpoint, walidacja HMAC-SHA256, tabela idempotencji (PostgreSQL), zwrot 200 OK w <50 ms | 8–12 h | 1 200–1 800 zł |
| M2: Silnik kolejkowy | Konfiguracja Celery + Redis, worker pool, retry policy z exponential backoff + jitter, DLQ, monitoring Flower | 10–14 h | 1 500–2 200 zł |
| M3: Konektory integracyjne | Adaptery do CRM/ERP (REST API), obsługa rate limitów (token bucket), circuit breaker, idempotentne zapisy | 12–18 h | 1 800–2 800 zł |
| M4: Audyt i observability | Schemat bazy audytowej, logowanie strukturalne (JSON), integracja Sentry, dashboardy metryk | 6–10 h | 900–1 500 zł |
| M5: Konteneryzacja i wdrożenie | Dockerfile (multi-stage build), Docker Compose (API + worker + Redis + PostgreSQL), skrypt wdrożeniowy, dokumentacja | 6–8 h | 900–1 200 zł |
| **RAZEM** | | **42–62 h** | **6 300–9 500 zł** |

**Warianty:** MVP (webhook + kolejka + 1 konektor): 4 500–6 000 zł; Standard (2 konektory + audyt): 7 000–9 500 zł; Enterprise (multi-tenant, SLA, runbook): 10 000–12 000 zł.

#### 5.3 NestJS / Node.js (5 500 – 15 000 zł)

| Moduł | Zakres | Wycena |
|---|---|---|
| M1: Szkielet architektury NestJS | FastifyAdapter, struktura domenowa, globalne ValidationPipe, ExceptionFilter, LoggingInterceptor, ConfigModule | 3 500–5 000 zł |
| M2: Warstwa danych i relacji | ORM (Drizzle/Prisma), migracje, indeksy, connection pooling, repozytoria | 2 500–4 000 zł |
| M3: Skalowalna brama WebSockets/gRPC | Socket.io + Redis Adapter, room management, rate limiting, heartbeat, dla gRPC: `.proto`, deadline propagation, mTLS | 3 500–5 500 zł |
| M4: Bezpieczeństwo i uwierzytelnianie | JWT (access + refresh z rotacją), Guards, RBAC, rate limiting na auth, CORS/CSRF/helmet, autoryzacja socketu | 2 000–3 500 zł |
| M5: Testy i konteneryzacja | Testy jednostkowe (Vitest/Jest), e2e (supertest/light-my-request), Dockerfile multi-stage, non-root user | 2 500–4 000 zł |
| **RAZEM** | | **14 000–22 000 zł** |

Dla Useme realny zakres do 15 000 zł wymaga priorytetyzacji: M1 + M2 + M3 (bez gRPC) + podstawowe testy i Docker = ~11 500–15 000 zł.

#### 5.4 .NET 8/9 (5 000 – 16 000 zł)

| Moduł | Zakres | Czas | Wycena |
|---|---|---|---|
| M1: Szkielet | Minimal API, DI, konfiguracja, middleware, health checks | 2–3 dni | 1 500–3 000 zł |
| M2: Wydajna warstwa danych EF Core | `AsNoTracking`, `AsSplitQuery`, `EF.CompileAsyncQuery`, Dapper dla raportów, indeksy | 3–4 dni | 2 000–4 000 zł |
| M3: Asynchroniczny silnik eventów | MassTransit + RabbitMQ/Azure Service Bus, Outbox, idempotentność, retry + Polly | 3–4 dni | 2 500–4 500 zł |
| M4: Usługa wykonawcza (Windows Service / Worker) | `IHostBuilder.UseWindowsService()`, `sc.exe failure`, graceful shutdown | 2–3 dni | 1 500–3 000 zł |
| M5: Logowanie i telemetria | Serilog → Seq/Elasticsearch, OpenTelemetry, health checks | 1–2 dni | 800–1 500 zł |
| **RAZEM** | | **11–16 dni** | **8 300–16 000 zł** |

#### 5.5 Google Apps Script (2 000 – 5 500 zł)

| Moduł | Zakres | Czas | Wycena |
|---|---|---|---|
| M1: Audyt i projekt kontraktu danych | Analiza arkusza, identyfikacja wąskich gardeł, projekt struktury docelowej, mapowanie API | 1–2 dni | 400–800 zł |
| M2: Batch Processor Core | Silnik porcjowania: `getValues()` → przetwarzanie w pamięci → `setValues()`. Zapis stanu w PropertiesService | 2–3 dni | 800–1 500 zł |
| M3: Continuation Trigger Engine | Tworzenie triggera czasowego, wznawianie od ostatniego indeksu, cleanup, idempotencja | 1–2 dni | 500–1 000 zł |
| M4: Warstwa integracji Gmail/Drive/API | Parsowanie maili (`GmailApp`), zapis na Drive (`DriveApp`), `fetchAll()` z kontrolą partii | 2–3 dni | 800–1 500 zł |
| M5: Panel kontrolny i monitoring | Arkusz „Status”, licznik błędów, powiadomienia mailowe o zakończeniu | 1 dzień | 400–700 zł |
| **RAZEM** | | **7–11 dni** | **2 000–5 500 zł** |

---

### 6. WZORCOWA OFERTA BOJOWA 1:1 (BENCHMARK MISTRZOWSKI)

Poniżej kompletna oferta dla reprezentatywnego zlecenia z grupy (web scraping). Pokazuje połączenie wszystkich zasad: diagnoza w pierwszych 2 zdaniach, analiza z pytaniami kwalifikującymi, rozbicie modułowe z wyceną, wezwanie do odpowiedzi na priv. Zero „doświadczenia”, zero „chęci pomocy”, zero rozmów telefonicznych.

---

**Zlecenie:** „Potrzebuję prostego skryptu w Pythonie do pobierania 50k produktów dziennie z 5 sklepów internetowych. Budżet: 2000 zł.”

**Oferta:**

Dzień dobry,

Zanim uruchomisz jakikolwiek headless browser: te 5 sklepów najprawdopodobniej blokuje `requests` na poziomie TLS ClientHello (JA3/JA4) lub HTTP/2 SETTINGS, zanim wyślesz pierwszy bajt HTTP. Zanim wydasz budżet na Selenium: sprawdźmy, czy istnieje endpoint REST/PWA z danymi hydratacji (`__NEXT_DATA__`, `window.__APOLLO_STATE__`) — wtedy `curl_cffi` z JA4 spoofingiem wystarczy, a koszt infrastruktury spada do zera.

Analizując opis zlecenia, widzę trzy krytyczne niewiadome, które determinują architekturę:

1. **Częstotliwość odświeżania:** Czy 50 000 produktów dziennie to jednorazowy batch, czy dane mają być odświeżane co godzinę? Przy częstotliwości godzinowej potrzebna jest kolejka zadań i rotacja sesji proxy — to zwielokrotnia koszty operacyjne.
2. **Format docelowy:** Czy dane mają trafiać do CSV, JSON, czy bezpośrednio do Państwa bazy (PostgreSQL/BigQuery)? Od tego zależy moduł eksportu i ewentualna integracja.
3. **Budżet na proxy:** Czy akceptują Państwo koszty proxy rezydencjalnych (ok. $1–$15/GB) oddzielnie od wynagrodzenia? Przy 5 sklepach za Cloudflare/DataDome bez proxy rezydencjalnego sukces jest bliski zeru.

Proponowana architektura (modułowa):

- **Moduł 1: Analiza anty-bot i reverse-engineering API** (1–2 dni, 800–1 200 zł) – identyfikacja endpointów, test JA3/JA4, wybór strategii.
- **Moduł 2: Moduł rotacji sesji i proxy** (1 dzień, 600–1 000 zł) – integracja proxy rezydencjalnych, rotacja per sesja.
- **Moduł 3: Silnik parsowania i normalizacji** (1–2 dni, 800–1 500 zł) – Pydantic, deduplikacja, obsługa błędów.
- **Moduł 4: Baza danych i pipeline eksportu** (1–2 dni, 800–1 500 zł) – PostgreSQL/ClickHouse, eksport CSV/JSON.
- **Moduł 5: Monitoring i retry policy** (1 dzień, 600–1 000 zł) – alerty, exponential backoff.

Łącznie: **4 000 – 6 500 zł** (w zależności od liczby domen za WAF enterprise i wymagań co do częstotliwości). Budżet 2 000 zł pozwala na wykonanie wyłącznie prostego scrapera jednej domeny bez zabezpieczeń — przy 5 sklepach z Cloudflare to nieosiągalne.

Proszę o odpowiedź na priv: która z trzech niewiadomych (częstotliwość, format, budżet na proxy) jest najbardziej krytyczna? Na tej podstawie przygotuję dokładny kosztorys w ciągu 2 godzin.

---

**Koniec oferty.**

---

**Podsumowanie:** Oferta wygrywająca na Useme w 2026 roku nie mówi „znam się na scrapingu”. Mówi: „Wiem, gdzie pęknie Twój system — na 6-minutowym wallu, na TLS JA4, na braku idempotencji. Mam architekturę, która to omija.” Reszta to już tylko wycena.