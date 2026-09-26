# -*- coding: utf-8 -*-
"""Generator kart wiedzy dla Bloku 2: DevOps, Infrastruktura i Backend (Linux/Docker, SQL, NestJS, .NET).
Wykorzystuje model deepseek-chat-search na lokalnym proxy laboratorium_modeli (port 4571)
oraz rygorystyczny schemat inżynierski wymuszający odpowiedź na priv.
"""

import json
from pathlib import Path
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-chat-search"

OUTPUT_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\badania\analizy\technologie\baza_wiedzy")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """Jesteś Głównym Architektem Infrastruktury i Starszym Inżynierem Backendowym tworzącym elitarną bazę wiedzy dla bota ofertowego na platformie Useme / B2B.

KONTEKST I REALIA ZLECENIODAWCÓW (WYNIKI AUDYTU USEME - BLOK DEVOPS & BACKEND):
- Zlecenia z tego bloku pochodzą od CTO, założycieli platform o rosnącym ruchu, menedżerów IT oraz firm po incydentach bezpieczeństwa / awariach produkcyjnych.
- Budżety wynoszą typowo 3 500 - 16 000 zł. Klienci to ludzie techniczni lub półtechniczni — natychmiast wyczuwają marketingowe lanie wody i juniorów.
- Elita wygrywa zlecenia, ponieważ:
  1. OTWIERA PROBLEMEM ARCHITEKTONICZNYM W PIERWSZYCH 2 ZDANIACH (zamiast pisać o swoim stażu, uderza w wąskie gardła: I/O dyskowe, brak connection poolingu, podatności sieciowe, blokady tabel przy migracjach).
  2. ZNA AKTUALNE REALIA SYSTEMOWE NA 2026 ROK (bezpieczeństwo Docker rootless, cgroups v2, PostgreSQL 16/17, NestJS 10/11, .NET 8/9 AOT, systemy telemetryczne OpenTelemetry).
  3. ZADAJE 2-3 CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODKU ANALIZY (zmusza klienta do natychmiastowego odpisania na priv).
  4. WSKAZUJE ANTYWZORCE I CZERWONE FLAGI (np. migracje `ALTER TABLE` na żywej bazie bez narzędzi online, kontenery odpalane jako root, brak izolacji sieci bazodanowych, brak polityki retencji logów zatykającej dysk).
  5. ROZBIJA WYCENĘ NA LOGICZNE MODUŁY ARCHITEKTONICZNE (nie ryczałt).

ZASADY TREŚCI:
- Zero udawania mowy ludzkiej ("no hej", "w sumie", sztuczne idiomy).
- Zero proponowania spotkań wideo, Google Meet czy rozmów telefonicznych (komunikacja wyłącznie pisemna na priv).
- Twarde, zweryfikowane fakty inżynierskie, zaktualizowane pod kątem 2026 roku.
- Język: Polski, wysoce precyzyjny, inżynierski.
"""

TASKS = [
    {
        "id": "tech_08_devops_docker_linux",
        "nazwa": "DevOps, Docker, Linux Hardening i Disaster Recovery (VPS, Nginx/Traefik, TLS)",
        "plik": OUTPUT_DIR / "tech_08_devops_docker_linux.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **DevOps, Konteneryzacja Docker, Hardening Serwerów Linux (Ubuntu/Debian), Reverse Proxy (Nginx / Traefik / Caddy) i Strategie Disaster Recovery (Borg / Restic / S3)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić najnowsze standardy bezpieczeństwa i konteneryzacji w 2026 roku (Docker rootless, cgroups v2, TLS 1.3, zautomatyzowane snapshoty S3 z immutability / object lock przed ransomware).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: konfiguracja i zabezpieczenie nowego serwera VPS/Dedyk (Hetzner, OVH, AWS), migracja aplikacji do Docker Compose, konfiguracja reverse proxy z certyfikatami SSL (Let's Encrypt / Cloudflare), ratowanie serwera po infekcji malware lub awarii dysku, wdrożenie automatycznych backupów.
   - Budżety: 2 500 – 10 000 zł. Profil klienta: software house bez dedykowanego admina, e-commerce z problemami ze stabilnością w szczycie, founder startupu.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Linux Hardening: Wyłączenie logowania po haśle w SSH (klucze Ed25519), niestandardowy port, fail2ban / crowdsec (nowocześniejsza alternatywa z bazą zagrożeń p2p), UFW / nftables, automatyczne aktualizacje bezpieczeństwa (unattended-upgrades), konfiguracja pamięci SWAP z zram / vm.swappiness.
   - Bezpieczeństwo Docker: Rootless mode lub User namespace remapping; zasada nieodpalania kontenerów jako root (`USER 1001`); izolacja sieciowa (`internal: true` dla bazy danych w Docker Compose – port bazy nigdy nie jest wystawiony na 0.0.0.0 do internetu!); limity zasobów `deploy.resources.limits` (CPU i pamięć, ochrona przed OOM killerem).
   - Reverse Proxy: Wybór między Nginx (najwyższa wydajność statyczna), Traefik (automatyczne wykrywanie kontenerów przez Docker socket z socket-proxy) a Caddy (automatyczny TLS). Wymuszenie TLS 1.3, nagłówki bezpieczeństwa HSTS, CSP, X-Frame-Options.
   - Disaster Recovery: Zasada backupu 3-2-1. Narzędzia nowoczesne: Restic lub BorgBackup z deduplikacją, kompresją i szyfrowaniem end-to-end, wysyłka do niezależnego storage (np. Hetzner Storage Box, Backblaze B2, AWS S3 z włączonym Object Lock przeciwko usunięciu przez ransomware).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję skonfigurować serwer VPS pod naszą aplikację w Dockerze i podpiąć domenę".
   - Co go utopi (Mina 1 - Dysk zapchany logami): Domyślny sterownik logów Dockera (`json-file`) nie ma limitu wielkości — po 2 miesiącach logi kontenera zapychają cały dysk serwera (100% inode lub storage), co powoduje nagły crash bazy danych i uszkodzenie tabel. Wymóg konfiguracji `max-size: "50m"` i `max-file: "3"` w `/etc/docker/daemon.json`.
   - Co go utopi (Mina 2 - OOM Killer bazy): Aplikacja Node/Python dostaje memory leak, zużywa cały RAM serwera, po czym jądro Linuksa OOM-killerem zabija proces bazy danych (Postgres/MySQL) z utratą transakcji.
   - Co go utopi (Mina 3 - Baza otwarta na świat): Otworzenie portu `5432:5432` lub `3306:3306` na interfejs publiczny `0.0.0.0` — botnety skanujące internet przejmują bazę i żądają okupu w Bitcoinach w ciągu 48 godzin.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Otwarcie uderzające w izolację sieci bazy (brak ekspozycji na interfejs publiczny), sterowniki logów chroniące przed zapchaniem dysku i limity OOM dla kontenerów.
   - Natychmiastowe wskazanie na weryfikowalność backupów: "Kopia zapasowa, która nie została przetestowana procedurą odtworzenia (test restore), nie istnieje".
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz wystawiania portów bazodanowych na świat (`0.0.0.0:5432`).
   - Zakaz używania domyślnego użytkownika root w kontenerach aplikacyjnych.
   - Zakaz backupowania bazy danych przez kopiowanie plików z dysku (`cp -r /var/lib/docker/volumes/...`) podczas pracy silnika bazy (gwarantowane uszkodzenie spójności transakcyjnej; wymagany `pg_dump` / snapshot ze spójnością transakcyjną).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 000 – 9 000 ZŁ):
   - Moduły: 1. Audyt i hardening bazowy systemu Linux (SSH, firewall, crowdsec, unattended-upgrades); 2. Środowisko Docker z polityką bezpieczeństwa (daemon.json limits, rootless, izolowane sieci bridge); 3. Reverse proxy i routing SSL/TLS (Nginx/Traefik + certbot/Let's Encrypt); 4. Zautomatyzowany pipeline backupów 3-2-1 (Restic/Borg + szyfrowany off-site storage S3 z retencją); 5. Monitoring stanu serwera i powiadomienia (Node Exporter, Uptime Kuma / Grafana Cloud / alerty na Telegram/Discord).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy aplikacja posiada już plik docker-compose i czy wymaga bazy stanowej na tym samym serwerze; jaki jest obecny wolumen danych i dopuszczalny RTO/RPO w razie awarii dysku; czy serwer posiada dedykowaną prywatną sieć z bazą czy działa w środowisku single-node).
"""
    },
    {
        "id": "tech_09_sql_optymalizacja_migracje",
        "nazwa": "Bazy Danych, Optymalizacja Zapytań i Migracje Zero-Downtime (PostgreSQL / MySQL)",
        "plik": OUTPUT_DIR / "tech_09_sql_optymalizacja_migracje.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Bazy Danych SQL (PostgreSQL, MySQL / MariaDB) — Optymalizacja Zapytań, Indeksowanie Zaawansowane, Analiza Planów Wykonania (EXPLAIN ANALYZE) i Migracje Schematu bez Przestojów (Zero-Downtime Migrations)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić nowoczesne techniki optymalizacji bazodanowej w 2026 roku (PostgreSQL 16/17 mechanizmy równoległe i indeksy BRIN, migracje zero-downtime z użyciem `gh-ost` / `pg_repack` / `pt-online-schema-change`, mechanizmy connection poolingu PgBouncer vs Supavisor).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: aplikacja muli i zawiesza się przy 100+ jednoczesnych użytkownikach, serwer bazy dobija do 100% CPU, konieczność bezpiecznego dodania kolumny lub indeksu do tabeli z 20 milionami rekordów, czyszczenie i archiwizacja starych danych, usunięcie deadlocków.
   - Budżety: 3 000 – 12 000 zł. Profil klienta: właściciel platformy SaaS, główny programista szukający wsparcia DBA, firma e-commerce po wpadce w Black Friday.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Diagnoza wąskich gardeł: `EXPLAIN (ANALYZE, BUFFERS)` w PostgreSQL; badanie Seq Scan vs Index Scan / Bitmap Index Scan; wycieki I/O przez brak pamięci `shared_buffers` lub zbyt mały `work_mem` (sortowanie zrzucane na dysk do temp files).
   - Indeksowanie zaawansowane: Indeksy częściowe (`WHERE deleted_at IS NULL` - oszczędność 80% rozmiaru indeksu), indeksy pokrywające (`INCLUDE` - Index Only Scan), indeksy wielokolumnowe z uwzględnieniem selektywności, indeksy BRIN dla danych szeregów czasowych (ułamek wielkości B-Tree).
   - Connection Pooling: Baza dławiąca się od nadmiaru połączeń (każde połączenie w Postgresie to osobny proces forkowany z 10MB pamięci). Wymóg PgBouncer lub nowoczesnego Supavisor w trybie transaction pooling.
   - Migracje Zero-Downtime: W PostgreSQL dodanie indeksu zwykłym `CREATE INDEX` blokuje wszystkie operacje zapisu (lock `SHARE`) na godziny przy wielkiej tabeli! Wymóg: `CREATE INDEX CONCURRENTLY` (z obsługą potencjalnego stanu invalid) lub `pg_repack`. W MySQL: `ALTER TABLE ... ALGORITHM=INPLACE` lub narzędzia online jak `gh-ost`.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Baza danych wolno działa, trzeba dokupić większy serwer z 64 GB RAM albo zmienić konfigurację serwera".
   - Co go utopi: Skalowanie pionowe (droższy serwer) rozwiązuje problem tylko na 2 tygodnie. Prawdziwą przyczyną w 95% przypadków jest jedno zapytanie typu N+1 z ORM lub brak indeksu na kluczu obcym generujący `Seq Scan` na 15 milionach rekordów przy każdym odświeżeniu koszyka.
   - Mina deadlocków: Błędna kolejność aktualizacji rekordów w transakcjach biznesowych (wątek A blokuje wiersz 1 potem 2; wątek B blokuje wiersz 2 potem 1).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Natychmiastowe wskazanie na analizę `pg_stat_statements` (lub `slow_query_log` w MySQL) i plany buforów zamiast zgadywania i dokupowania RAM-u.
   - Wskazanie na ryzyko zablokowania bazy przy nieumiejętnym tworzeniu indeksów (`CREATE INDEX CONCURRENTLY` vs lock całego serwisu).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz doradzania "dokupienia mocniejszego VPS-a" jako pierwszej rekomendacji.
   - Zakaz odpalania blokujących migracji DDL na tabelach produkcyjnych w godzinach szczytu.
   - Zakaz ignorowania connection poolera przy architekturze mikroserwisowej lub serverless.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 500 – 11 000 ZŁ):
   - Moduły: 1. Audyt metryk i profilowanie powolnych zapytań (`pg_stat_statements`, logi, bufor cache hit ratio); 2. Refaktoryzacja indeksów i planów wykonania (dodanie brakujących indeksów concurrently, usunięcie nieużywanych indeksów spowalniających zapis); 3. Strojenie parametrów silnika bazy (`shared_buffers`, `work_mem`, `effective_cache_size`, `random_page_cost`); 4. Wdrożenie warstwy connection poolingu (PgBouncer); 5. Wdrożenie procedur bezpiecznych migracji schematu i monitoringu (PMM / pgWatch / Datadog).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy silnikiem jest PostgreSQL czy MySQL/MariaDB i w jakiej wersji; jaki jest rozmiar największej tabeli w bazie i średni wolumen transakcji na sekundę; czy mają włączone rozszerzenie `pg_stat_statements` lub wgląd w slow query log).
"""
    },
    {
        "id": "tech_10_nodejs_nestjs_backend",
        "nazwa": "Node.js, NestJS i TypeScript Backend (Architektura Modularna, WebSockets, gRPC)",
        "plik": OUTPUT_DIR / "tech_10_nodejs_nestjs_backend.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Node.js, NestJS i TypeScript Backend — Architektura Modularna (Domain-Driven / Clean Architecture), Komunikacja Real-Time (WebSockets / Socket.io), Mikroserwisy gRPC / Redis i Zarządzanie Wydajnością Silnika V8**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić aktualne trendy w ekosystemie NestJS i Node.js na 2026 rok (Node.js 22 LTS, natywny test runner, Fastify adapter zamiast Express w NestJS, Prisma 5+ vs Drizzle ORM pod kątem connection overhead).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: budowa skalowalnego backendu dla aplikacji mobilnej/webowej w NestJS, migracja bałaganu w Express.js do uporządkowanej architektury NestJS, wdrożenie WebSockets (czat, geolokalizacja kurierów, powiadomienia na żywo), integracje mikrousługowe przez gRPC.
   - Budżety: 4 500 – 16 000 zł. Profil klienta: CTO startupu technologicznego, agencja software z przeciążonym zespołem backendowym, firma produktowa.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Architektura NestJS: Moduły domenowe, separacja warstw (Controllers -> Services -> Repositories), Dependency Injection, DTO z walidacją `class-validator` / Zod, unikanie circular dependencies (`forwardRef`).
   - Wydajność HTTP: Zmiana domyślnego adaptera Express na Fastify (`FastifyAdapter`) — daje 2-3x wyższą przepustowość RPS i niższe opóźnienia.
   - Komunikacja w czasie rzeczywistym: WebSockets (Socket.io z adapterem Redis Streams / Redis PubSub) — kluczowe dla horyzontalnego skalowania (gdy mamy 3 instancje backendu, użytkownik połączony z instancją A musi dostać wiadomość od użytkownika z instancji B).
   - Warstwa danych: Drizzle ORM (zero overheadu, type-safe SQL) vs Prisma (silnik Rust w procesie potomnym z narzutem pamięciowym i connection poolingu).
   - Zarządzanie pamięcią V8: Wykrywanie memory leaków przez nieusunięte event listenery (`EventEmitter.on` bez `removeListener`), domknięcia (closures) przetrzymujące duże obiekty, analiza heap snapshotów w Chrome DevTools / Clinic.js.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebujemy dodać WebSockets do naszego backendu w Node.js, żeby przesyłać lokalizację kierowców do 5 000 użytkowników na żywo".
   - Co go utopi: Odpalenie Socket.io w pamięci pojedynczego procesu Node.js — przy braku Redis Adaptera skalowanie poziome (odpalenie 2 kontenerów za load balancerem) natychmiast rozrywa połączenia (użytkownicy nie widzą wiadomości z innych instancji). Dodatkowo: brak heartbeat/ping-pong i brak kompresji payloadu w WebSockets dławi pasmo sieciowe serwera.
   - Mina event loopu: Wykonywanie synchronicznych operacji blokujących (np. parsowanie gigantycznego JSON-a 50MB, synchroniczne crypto, ciężkie pętle `Array.filter/map` na 200k elementów) zamraża cały serwer dla wszystkich innych użytkowników (Event Loop Lag).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia uderzające w architekturę skalowania WebSockets (Redis adapter) oraz zapobieganie blokowaniu Event Loopu (Event Loop Lag metrics).
   - Wskazanie na wybór Fastify adaptera i modularną Clean Architecture zamiast monolitycznego spaghetti w Express.js.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz proponowania Socket.io na produkcji bez adaptera klastrowego (Redis / RabbitMQ).
   - Zakaz wykonywania operacji blokujących CPU bezpośrednio w głównym wątku Node.js (konieczność Worker Threads lub kolejki BullMQ).
   - Zakaz pisania o "Expressie jako domyślnym i najlepszym silniku dla NestJS" bez wzmianki o Fastify przy wymaganiach wysokiego throughputu.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 5 500 – 15 000 ZŁ):
   - Moduły: 1. Szkielet architektury NestJS (Clean Architecture, Fastify, DTO, global exception filters i interceptory); 2. Warstwa danych i relacji (Drizzle/TypeORM + migracje + indeksy); 3. Skalowalna brama WebSockets / gRPC (Socket.io z Redis Adapterem, room management, rate limiting); 4. Bezpieczeństwo i uwierzytelnianie (JWT, Guards, role RBAC, Passport / Supabase Auth); 5. Testy jednostkowe i e2e (Jest / Vitest) + konteneryzacja z multi-stage build w Dockerze.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. ile jednoczesnych połączeń WebSocket ma obsługiwać system w szczycie; czy backend ma działać w klastrze za load balancerem; jakie są wymagania dotyczące opóźnień i czy rozważali gRPC do komunikacji wewnętrznej).
"""
    },
    {
        "id": "tech_11_csharp_dotnet_b2b",
        "nazwa": "C#, .NET 8/9 Backend B2B (Entity Framework Core, MassTransit, Usługi On-Prem)",
        "plik": OUTPUT_DIR / "tech_11_csharp_dotnet_b2b.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **C#, .NET 8 / 9 Backend B2B — Budowa Wydajnych Web API, Entity Framework Core (Optymalizacja Zapytań, Split Queries), Kolejkowanie Asynchroniczne (MassTransit / RabbitMQ) i Usługi Windows / On-Prem**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić najnowsze funkcje .NET 8 i 9 w 2026 roku (Native AOT dla Web API, optymalizacje pamięci w GC, `AsNoTracking` i compiled queries w EF Core, integracje hybrydowe cloud <-> on-prem dla środowisk korporacyjnych).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: budowa modułów integracyjnych w środowisku Microsoft, modernizacja legacy .NET Framework (4.x) do .NET 8/9, optymalizacja powolnych aplikacji w Entity Framework, serwisy pośredniczące między systemami korporacyjnymi (Active Directory, MS SQL, systemy ERP).
   - Budżety: 4 500 – 18 000 zł. Profil klienta: działy IT średnich i dużych przedsiębiorstw, producenci oprogramowania biznesowego w ekosystemie Windows, integratorzy systemów.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - .NET 8/9 Realia: Wsparcie LTS, Native AOT (Ahead-of-Time compilation) – natychmiastowy start aplikacji i minimalne zużycie RAM (krytyczne dla kontenerów i mikroserwisów).
   - Optymalizacja Entity Framework Core: Pułapka Cartesian Explosion przy relacjach 1:N — wymóg stosowania `.AsSplitQuery()`; bezwzględne używanie `.AsNoTracking()` dla operacji tylko do odczytu; unikanie problemu N+1; stosowanie zapytań skompilowanych (`EF.CompileAsyncQuery`) przy zaciągach o wysokiej częstotliwości.
   - Architektura komunikatów: MassTransit jako biblioteka orkiestracji (abstrakcja nad RabbitMQ / Azure Service Bus) z wbudowanym wzorcem Outbox Pattern (gwarancja spójności transakcyjnej: zapis do bazy i publikacja eventu w jednej transakcji).
   - Praca on-prem i Windows Services: Tworzenie demonów systemowych za pomocą `BackgroundService` i `Microsoft.Extensions.Hosting.WindowsServices` do stabilnej pracy 24/7 na maszynach wewnątrz sieci klienta.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Mamy aplikację w .NET z Entity Framework, która zjada za dużo pamięci i bardzo wolno zwraca raporty z bazy".
   - Co go utopi: Domyślny Change Tracker w EF Core trzyma w pamięci referencje do tysięcy pobranych encji — brak `.AsNoTracking()` powoduje gigantyczny wyciek pamięci i obciążenie Garbage Collectora. Do tego pobranie relacji przez `.Include().Include()` generuje gigantyczny iloczyn kartezjański w SQL (Cartesian Explosion), przesyłając gigabajty redundantnych danych przez sieć.
   - Mina awarii połączeń z ERP: Usługa synchronizująca nie posiada polityki retry (Polly) — chwilowy restart SQL Servera rzuca wyjątek i trwale zabija proces Windows Service.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia inżynierskie uderzające w wyłączenie Change Trackera (`AsNoTracking`), podział zapytań relacyjnych (`AsSplitQuery`) i wzorzec Transactional Outbox.
   - Wskazanie na odporność usług tła (Polly retry policies z jitterem) i bezproblemowe działanie w środowisku Windows Service.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz używania `DbContext` jako singletona (DbContext NIE jest thread-safe — musi być scoped).
   - Zakaz ignorowania `.AsSplitQuery()` przy wielokrotnych `.Include()`.
   - Zakaz publikowania zdarzeń do brokera bez wzorca Outbox (ryzyko utraty eventu przy crashu bazy po zatwierdzeniu transakcji).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 5 000 – 16 000 ZŁ):
   - Moduły: 1. Szkielet rozwiązania .NET 8/9 (Clean Architecture / Vertical Slice Architecture z MediatR lub FastEndpoints); 2. Wydajna warstwa danych EF Core (migracje, split queries, indeksy, Dapper do krytycznych raportów); 3. Asynchroniczny silnik eventów (MassTransit + RabbitMQ + Transactional Outbox); 4. Usługa wykonawcza (Windows Service / Worker z politykami Polly); 5. Logowanie strukturalne i telemetria (Serilog + OpenTelemetry / Seq).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy rozwiązanie ma działać w chmurze (Azure/AWS) czy jako Windows Service w lokalnej sieci on-prem; jaka wersja .NET i silnika bazy danych jest używana; jaki jest wolumen pobieranych rekordów przy pojedynczym zapytaniu).
"""
    }
]

def wykonaj_zadanie(zadanie):
    print(f"\n=======================================================")
    print(f"[START] Rozpoczynam zadanie: {zadanie['nazwa']}")
    print(f"[PLIK]  {zadanie['plik'].name}")
    print(f"[MODEL] {MODEL}")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": zadanie["prompt"]}
        ],
        "temperature": 0.3,
        "stream": False
    }
    
    start_t = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=240)
        if r.status_code != 200:
            print(f"[BŁĄD HTTP {r.status_code}] {r.text[:500]}")
            return False
            
        dane = r.json()
        tresc = dane["choices"][0]["message"]["content"]
        
        # Zapis do pliku UTF-8
        zadanie["plik"].write_text(tresc, encoding="utf-8")
        duration = round(time.time() - start_t, 1)
        print(f"[SUKCES] Wygenerowano i zapisano: {zadanie['plik'].name} ({len(tresc)} znaków) w {duration}s")
        return True
    except Exception as e:
        print(f"[WYJĄTEK] {e}")
        return False

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== Generator Kart Wiedzy Bloku 2: DevOps, Bazy Danych i Backend ===")
    sukcesy = 0
    for zadanie in TASKS:
        ok = wykonaj_zadanie(zadanie)
        if ok:
            sukcesy += 1
        time.sleep(2)
        
    print(f"\n=======================================================")
    print(f"[KONIEC] Pomyślnie ukończono {sukcesy}/{len(TASKS)} kart technologicznych dla Bloku 2!")

if __name__ == "__main__":
    main()
