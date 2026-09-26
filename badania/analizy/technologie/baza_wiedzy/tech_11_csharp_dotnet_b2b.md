# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B

## TEMAT: C#, .NET 8 / 9 Backend B2B — Budowa Wydajnych Web API, Entity Framework Core, Kolejkowanie Asynchroniczne (MassTransit / RabbitMQ) i Usługi Windows / On-Prem

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1. Typologia zleceń w bloku DevOps & Backend

| Kategoria zlecenia | Typowy zakres | Sygnały w ogłoszeniu |
|---|---|---|
| **Modernizacja legacy .NET Framework 4.x → .NET 8/9** | Przepisanie warstwy danych, WCF → Minimal API, ASP.NET Web Forms → REST | „mamy starą aplikację", „chcemy przenieść na nowszy framework", „potrzebujemy wsparcia" |
| **Optymalizacja wydajności EF Core** | Redukcja zużycia RAM, przyspieszenie raportów, eliminacja N+1 | „aplikacja zjada za dużo pamięci", „raporty ładują się minutami", „baza jest obciążona" |
| **Serwisy integracyjne (ERP / AD / MS SQL)** | Windows Service łączący systemy korporacyjne, synchronizacja danych | „potrzebujemy usługi w tle", „synchronizacja z ERP", „Active Directory", „on-prem" |
| **Kolejkowanie i event-driven** | MassTransit + RabbitMQ / Azure Service Bus, Outbox  p.CategoryId == categoryId)
    .ToListAsync(ct);

// ❌ BŁĄD — Change Tracker śledzi każdą encję
var products = await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(ct);
```

**Reguła:** `AsNoTracking()` dla **każdego** zapytania, którego wynik nie będzie modyfikowany. Odstępstwo tylko przy jawnym UPDATE w tej samej sesji.

#### 2.3.2. `AsSplit o.Items)
    .Include(o => o.Payments)
    .Include(o => o.ShippingHistory)
    .AsSplit o.CustomerId == customerId)
    .ToListAsync(ct);
```

**Ważne:** Cartesian Explosion **nie występuje**, gdy JOINy są na różnych poziomach (np. `Blogs.Include(Posts).ThenInclude(Comments)`). `AsSplit> GetById
        ctx.Products.AsNoTracking().FirstOrDefault(p => p.Id == id));
```

#### 2.3.4. Unikanie N+1

Lazy loading (jeśli włączony) generuje osobne zapytanie dla każdej encji potomnej. Rozwiązanie: jawne `.Include()` / `.ThenInclude()` z eager loading lub projekcja do DTO.

#### 2.3.5. Projekcja zamiast pełnych encji

Pobieranie pełnych encji, gdy potrzebne są 3 kolumny, to marnotrawstwo I/O i pamięci. `.Select(p => new ProductDto { ... })` redukuje transfer danych i eliminuje potrzebę trackowania.

### 2.4. MassTransit i Transactional Outbox

MassTransit to biblioteka orkiestracji komunikatów (abstrakcja nad RabbitMQ, Azure Service Bus, Kafka, SQS). W wersji **v9.1.0** (pre-release 2026) dodano wsparcie **Kafka** dla Outboxa — wiadomości produkowane do topiców Kafki i innych endpointów są staged w tym samym Outboxie.

**Transactional Outbox  „Problem, który Państwo opisują, to klasyczny objaw dwóch antywzorców EF Core: Change Tracker utrzymujący referencje do wszystkich pobranych encji (brak `.AsNoTracking()`) oraz Cartesian Explosion przy wielokrotnym `.Include()` na tym samym poziomie relacji. W pierwszym kroku wyłączam Change Tracker dla operacji read-only i wprowadzam `.AsSplit „Brak Transactional Outbox  „`BackgroundService` w .NET domyślnie kończy host przy nieobsłużonym wyjątku (`StopHost`), a bez `Environment.Exit(1)` system Windows nie restartuje usługi — proces staje się zombie. Buduję usługę z pełną polityką recovery: Polly retry z exponential backoff + jitter, jawny exit code przy krytycznych błędach i Serilog do strukturalnego logowania zdarzeń w środowisku bez dostępu do chmury."

---

## 5. CZERWONA LISTA / ANTYWZORCE

| # | Antywzorzec | Konsekwencja | Prawidłowe rozwiązanie |
|---|---|---|---|
| 1 | **`DbContext` jako singleton** | `DbContext` **nie jest thread-safe** — równoległe requesty powodują corruption stanu, wyjątki `InvalidOperationException`, niespójne dane | Rejestracja jako `Scoped` (domyślnie w ASP.NET Core) lub `Transient` w workerach |
| 2 | **Brak `.AsSplit` + sekrety przez `dotnet user-secrets` (dev) / Azure Key Vault (prod) |
| **Szacowany czas** | 2–3 dni |

### Moduł 2 — Wydajna warstwa danych EF Core

| Element | Opis |
|---|---|
| **Mapowanie** | `IEntityTypeConfiguration<T>` — fluent API, jawna konfiguracja indeksów |
| **Migracje** | `dotnet ef migrations` — generowanie skryptów SQL z opcją `--idempotent` |
| **Optymalizacja zapytań** | `AsNoTracking()` (read-only), `AsSplitQuery()` (multi-include), `EF.CompileAsyncQuery` (hot path) |
| **Raporty krytyczne** | Dapper dla zapytań o ekstremalnej złożoności (window functions, CTE, pivot) |
| **Indeksy** | Covering indexes dla najczęstszych `WHERE` + `ORDER BY` |
| **Szacowany czas** | 3–4 dni |

### Moduł 3 — Asynchroniczny silnik eventów

| Element | Opis |
|---|---|
| **Broker** | RabbitMQ (on-prem) lub Azure Service Bus (cloud) — abstrakcja przez MassTransit |
| **Outbox** | MassTransit EF Core Outbox — tabela `OutboxMessage`, background publisher |
| **Idempotentność** | Konsumenci z deduplikacją po `MessageId` (tabela `InboxState`) |
| **Retry** | MassTransit message retry + Polly dla zależności HTTP / SQL |
| **Szacowany czas** | 3–4 dni |

### Moduł 4 — Usługa wykonawcza (Windows Service / Worker)

| Element | Opis |
|---|---|
| **Hosting** | `IHostBuilder.UseWindowsService()` — instalacja przez `sc.exe create` |
| **Recovery** | `sc.exe failure` — restart po 60 s, drugi restart po 60 s |
| **Resilience** | Polly `ResiliencePipelineBuilder` — retry (3 próby, exponential backoff + jitter) |
| **Graceful shutdown** | `IHostApplicationLifetime` + `CancellationToken` z `stoppingToken` |
| **Szacowany czas** | 2–3 dni |

### Moduł 5 — Logowanie strukturalne i telemetria

| Element | Opis |
|---|---|
| **Logowanie** | Serilog → Seq (on-prem) / Elasticsearch (rozproszone) — logi strukturalne z `RequestId` |
| **Telemetria** | OpenTelemetry — traces, metrics, logs; eksport do OTLP endpoint (Jaeger / Grafana Tempo) |
| **Health checks** | `Microsoft.Extensions.Diagnostics.HealthChecks` — endpoint `/health` dla load balancera |
| **Szacowany czas** | 1–2 dni |

### Podsumowanie wyceny

| Moduł | Czas | Widełki cenowe |
|---|---|---|
| M1 — Szkielet | 2–3 dni | 1 500 – 3 000 zł |
| M2 — Warstwa danych | 3–4 dni | 2 000 – 4 000 zł |
| M3 — Silnik eventów | 3–4 dni | 2 500 – 4 500 zł |
| M4 — Worker / Windows Service | 2–3 dni | 1 500 – 3 000 zł |
| M5 — Logowanie i telemetria | 1–2 dni | 800 – 1 500 zł |
| **RAZEM** | **11–16 dni** | **5 000 – 16 000 zł** |

**Zasada wyceny:** każdy moduł wyceniany osobno. Klient może wziąć M2 (optymalizacja EF) bez M3 (Outbox) — moduły są niezależne.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU)

Pytania należy wpleść w środek analizy — po przedstawieniu diagnozy, przed rozbiciem wyceny. Cel: zmusić klienta do natychmiastowego odpisania na priv.

1. **„Czy docelowe środowisko to chmura (Azure / AWS) czy Windows Server on-prem z usługą instalowaną przez `sc.exe`? Od tego zależy wybór brokera (Azure Service Bus vs RabbitMQ) i strategia deploymentu."**

2. **„Jaka wersja .NET i silnika bazy danych jest obecnie używana? Jeśli to .NET Framework 4.x lub EF6, modernizacja do .NET 8/9 (LTS do listopada 2026) wymaga przepisania warstwy danych — to zmienia zakres prac."**

3. **„Jaki jest wolumen pobieranych rekordów przy pojedynczym zapytaniu raportowym? Poniżej 10 000 rekordów — `AsNoTracking` + indeksy wystarczą. Powyżej 100 000 — konieczna projekcja, paginacja i potencjalnie Dapper dla krytycznych ścieżek."**

4. **„Czy system downstream wymaga gwarancji exactly-once dla eventów? Jeśli tak, Transactional Outbox + idempotentny konsument to warunek konieczny — bez tego każdy crash bazy może trwale usunąć event z systemu."**

5. **„Czy usługa synchronizująca ma działać 24/7 i być restartowana przez system Windows po awarii? Jeśli tak, wymagana jest konfiguracja `sc.exe failure` + exit code ≠ 0 przy krytycznych błędach — inaczej proces staje się zombie."**

---

## ZAŁĄCZNIK: SŁOWNIK POJĘĆ DLA BOTA

| Pojęcie | Definicja operacyjna |
|---|---|
| **AsNoTracking** | Wyłączenie Change Trackera — encje nie są śledzone, brak narzutu na GC |
| **AsSplitQuery** | Podział jednego zapytania z JOINami na osobne zapytania — eliminacja Cartesian Explosion |
| **Cartesian Explosion** | Iloczyn kartezjański przy równoległych JOINach — n wierszy × m wierszy = n*m wierszy |
| **Compiled Query** | `EF.CompileAsyncQuery` — zapytanie kompilowane raz, reużywane z gotowym planem |
| **Outbox Pattern** | Zapis danych + wiadomości w jednej transakcji — gwarancja exactly-once |
| **Native AOT** | Kompilacja do kodu natywnego — brak JIT, szybki start, mały RAM |
| **BackgroundService** | Klasa bazowa dla długotrwałych zadań w tle w .NET |
| **Polly** | Biblioteka resilience — retry, circuit breaker, timeout, bulkhead |
| **Jitter** | Losowe odchylenie opóźnienia retry — zapobiega thundering herd |