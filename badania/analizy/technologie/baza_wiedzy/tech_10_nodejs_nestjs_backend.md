# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## BLOK: Node.js, NestJS i TypeScript Backend — Architektura Modularna, Komunikacja Real-Time, Mikroserwisy gRPC / Redis i Zarządzanie Wydajnością Silnika V8

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

**Typowe zlecenia w tym bloku:**

- Budowa skalowalnego backendu dla aplikacji mobilnej / webowej w NestJS od zera (greenfield), z modularną strukturą domenową i kontraktami API.
- Migracja istniejącego backendu Express.js do uporządkowanej architektury NestJS — klient ma kod, który działa, ale nie da się go rozwijać ani skalować.
- Wdrożenie WebSockets (Socket.io) dla funkcji czasu rzeczywistego: czat, śledzenie geolokalizacji kurierów / kierowców, powiadomienia push w czasie rzeczywistym, tablice Kanban z jednoczesną edycją.
- Integracje mikrousługowe przez gRPC — komunikacja wewnętrzna między serwisami przy polyglot stacku lub przy wymaganiach niskich opóźnień (Protobuf, streaming dwukierunkowy, deadline propagation).
- Audyt wydajności istniejącego backendu Node.js — memory leaki, blokowanie Event Loopu, nieoptymalne zapytania ORM.

**Budżety:** 4 500 – 16 000 zł. Widełki wynikają z zakresu: pojedynczy moduł (4 500 – 7 000 zł), średni projekt (8 000 – 11 000 zł), pełna architektura z real-time i testami (12 000 – 16 000 zł).

**Profil klienta:**

- CTO startupu technologicznego, który właśnie przekroczył 50 000 użytkowników i infrastruktura zaczyna się dusić.
- Agencja software z przeciążonym zespołem backendowym — szukają wykonawcy do konkretnego modułu lub refaktoryzacji.
- Firma produktowa (SaaS, marketplace, logistyka) po incydencie produkcyjnym — memory leak, awaria WebSockets przy skalowaniu, blokada Event Loopu przez synchroniczny export.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE — STAN NA 2026 ROK

### 2.1. Node.js 22 LTS — fundament wydajności

Node.js 22 LTS (aktualna gałąź: 22.23.3 „Jod”, wydana 2026-09-23) opiera się na silniku V8 w wersji 12.4 z kompilatorem Maglev, który znacząco redukuje zimny start i poprawia przepustowość w krótkotrwałych procesach. Wbudowany klient WebSocket w standardowej bibliotece Node eliminuje potrzebę zewnętrznych zależności przy prostych scenariuszach komunikacji dwukierunkowej. Node.js 22 LTS jest wspierany do 30 kwietnia 2027 roku, co daje stabilny horyzont produkcyjny.

Kluczowe dla wydajności: V8 12.4 z Maglev — kompilatorem pośrednim między interpreterem Ignition a optymalizującym Turbofan. Maglev redukuje opóźnienia w krótkotrwałych funkcjach i poprawia przewidywalność czasu odpowiedzi w porównaniu do Node 20 LTS.

### 2.2. Architektura NestJS — modularna, warstwowa, testowalna

NestJS wymusza strukturę, której Express.js nie narzuca. Moduły domenowe (`@Module`) enkapsulują kontrolery, serwisy, repozytoria i providery. Separacja warstw: **Controller** (walidacja DTO, mapowanie na serwis) → **Service** (logika aplikacyjna, orkiestracja) → **Repository** (dostęp do danych). Dependency Injection (DI) w NestJS jest hierarchiczny — providery są dostępne tylko w zakresie swojego modułu, chyba że zostaną wyeksportowane. To zapobiega przypadkowemu tworzeniu „bogów-obiektów”, które w Express.js są normą.

**Walidacja DTO:** `class-validator` + `class-transformer` pozostaje standardem, ale w 2026 roku coraz częściej stosuje się Zod ze względu na inferencję typów TypeScript bez dekoratorów. NestJS 12 (Q3 2026) wprowadza natywne wsparcie dla Standard Schema — interfejsu zgodnego z Zod, Valibot i ArkType — co pozwala na walidację bez warstwy dekoratorów i bez `reflect-metadata`.

**Circular dependencies:** `forwardRef()` to obejście, nie rozwiązanie. Jeśli dwa moduły wymagają `forwardRef`, to sygnał, że granice domenowe są źle wyznaczone. Prawidłowa architektura powinna wyglądać tak: `OrderModule` zależy od `ProductModule` (jednokierunkowo), a nie odwrotnie.

**NestJS 12 — ESM-first:** Największa zmiana architektoniczna od lat. Wszystkie pakiety core przechodzą z CommonJS na ESM. CLI wspiera oba formaty, ale domyślnie nowe projekty ESM używają Vitest zamiast Jest i oxlint zamiast ESLint. Rspack zastępuje Webpack w pipeline buildowym.

### 2.3. Wydajność HTTP — FastifyAdapter jako standard produkcyjny

Domyślny adapter Express w NestJS jest wolny. FastifyAdapter daje **2–3× wyższą przepustowość RPS** przy tym samym kodzie aplikacji. W testach porównawczych: NestJS + Express osiąga ~15 000 RPS, NestJS + Fastify ~30 000 RPS na tym samym sprzęcie. Przy optymalizacji DI i JSON Schema serialization różnica rośnie do 60 000–100 000 RPS.

```typescript
// main.ts — FastifyAdapter
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter({ trustProxy: true }),
);
```

Fastify ma lżejszy cykl życia HTTP, wbudowaną walidację JSON Schema (która działa szybciej niż `class-validator`), oraz natywne wsparcie dla streamingu. Express pozostaje dobry dla prototypów i małych aplikacji, ale w produkcji z wymaganiami throughputu — Fastify jest jedynym racjonalnym wyborem.

### 2.4. Komunikacja w czasie rzeczywistym — WebSockets (Socket.io + Redis Adapter)

Socket.io w pojedynczym procesie Node.js to ślepa uliczka przy skalowaniu poziomym. Gdy backend działa na 3 instancjach za load balancerem, użytkownik A połączony z instancją #1 nie otrzyma wiadomości od użytkownika B połączonego z instancją #2 — chyba że zastosowany zostanie **adapter klastrowy**.

**Redis Adapter (Pub/Sub)** to minimalne rozwiązanie produkcyjne:

```typescript
import { createAdapter } from '@socket.io/redis-adapter';
const pubClient = createClient({ host: 'redis', port: 6379 });
const subClient = pubClient.duplicate();
await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));
```

**Redis Streams Adapter** to rozwiązanie dla scenariuszy wymagających niezawodnego dostarczania — wiadomości są persystowane w strumieniu (domyślnie ostatnie 10 000 wiadomości), co pozwala na odtworzenie po reconnectcie klienta.

**Sticky sessions na load balancerze:** Socket.io wymaga, aby handshake i kolejne żądania HTTP long-polling trafiały do tej samej instancji. Nginx konfiguruje się przez `ip_hash` lub cookie-based stickiness. Bez tego połączenie WebSocket zostanie zerwane przy każdym przekierowaniu na inną instancję.

**Heartbeat / ping-pong:** Domyślny interwał w Socket.io (25 s ping, 20 s timeout) jest często zbyt agresywny dla sieci mobilnych. W aplikacjach kurierskich z zasięgiem LTE konfiguruje się `pingInterval: 30000, pingTimeout: 60000`. Brak heartbeat oznacza, że serwer nie wie o rozłączeniu klienta, a zasoby (pamięć, deskryptory plików) nie są zwalniane.

### 2.5. Warstwa danych — Drizzle ORM vs Prisma

**Prisma** do wersji 6 używała silnika Rust w procesie potomnym, co wiązało się z narzutem pamięciowym (~2 MB binarki) i dodatkowym procesem do zarządzania. **Prisma 7** (2026) zastąpiła binarny silnik Rust czystym klientem TypeScript, redukując rozmiar bundle o ~90% i przyspieszając zapytania do 3×. To zamknęło większość luki wydajnościowej względem Drizzle.

**Drizzle ORM** pozostaje lżejszy w runtime (~30 KB vs ~100 KB Prisma). Drizzle nie zarządza connection poolingiem — deleguje to do `pg` / `postgres.js` lub PgBouncer. To zaleta w środowiskach serverless, gdzie connection pooling musi być externalizowany. W klasycznym kontenerze Docker zarządzanie poolem po stronie aplikacji jest prostsze i bardziej przewidywalne.

**Wybór dla projektów na Useme:**

- **Drizzle** — gdy klient ma istniejącą bazę PostgreSQL i zespół znający SQL, gdy priorytetem jest przewidywalność zapytań i minimalny narzut pamięciowy (kontenery o ograniczonym RAM), gdy aplikacja działa w serverless (Vercel, AWS Lambda).
- **Prisma** — gdy klient potrzebuje szybkiego prototypowania, gdy zespół nie zna SQL, gdy potrzebna jest Prisma Migrate z detekcją utraty danych i advisory locking.

### 2.6. Zarządzanie pamięcią V8 — memory leaki i analiza

**Event listener accumulation** to najczęstszy memory leak w backendzie Node.js. Wzorzec: `emitter.on('event', handler)` wywoływane w każdej iteracji pętli lub w każdym żądaniu HTTP bez odpowiadającego `emitter.removeListener('event', handler)` lub `emitter.off('event', handler)`. Każdy listener to domknięcie (closure) przetrzymujące referencję do scope, w którym został utworzony. Przy 10 000 żądań na sekundę i listenerze dodawanym per żądanie — pamięć rośnie liniowo, aż do OOM kill przez cgroups v2 w kontenerze.

**Diagnostyka:** `--heapsnapshot-near-heap-limit` (stabilne w Node 22) generuje snapshot V8 przed osiągnięciem limitu heap. Snapshot analizuje się w Chrome DevTools → Memory → Comparison. Filtruj po `(closure)` i sprawdzaj retainer  {
  const p99 = histogram.percentile(99) / 1e6;
  if (p99 > 100) console.warn(`Event Loop Lag P99: ${p99.toFixed(1)}ms`);
  histogram.reset();
}, 5000);
```

Wartość P99 powyżej 100 ms oznacza, że aplikacja ma poważny problem z blokowaniem głównego wątku. Normalny, zdrowy backend Node.js utrzymuje P99 na poziomie kilku–kilkunastu milisekund.

---

## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI)

### Scenariusz: „Potrzebujemy dodać WebSockets do naszego backendu w Node.js, żeby przesyłać lokalizację kierowców do 5 000 użytkowników na żywo”

**Co klient ma na myśli:** „Chcemy, żeby na mapie u użytkownika kropka z kierowcą przesuwała się na żywo. Mamy backend w Express.js, dodajcie Socket.io.”

**Co go utopi:**

1. **Brak Redis Adaptera = rozerwane połączenia przy skalowaniu.** Klient odpala Socket.io w jednym procesie Node.js. Działa. Przy 2 000 jednoczesnych połączeń proces zaczyna się dusić (single-thread event loop), więc klient odpala drugi kontener za load balancerem. Efekt: użytkownik połączony z instancją A nie widzi kierowcy, który wysłał lokalizację do instancji B. Połączenia są rozproszone, a wiadomości nie są propagowane między instancjami. Redis Adapter (Pub/Sub) rozwiązuje to przez broadcast każdej wiadomości do wszystkich instancji Socket.io — każda instancja dostarcza wiadomość do swoich lokalnie podłączonych klientów.

2. **Brak rate limitingu na wiadomościach WebSocket.** Kierowca wysyła lokalizację co 100 ms. Przy 500 kierowcach to 5 000 wiadomości na sekundę, każda broadcastowana do 5 000 użytkowników = 25 000 000 dostarczeń na sekundę. Bez throttlingu po stronie serwera i bez buforowania po stronie klienta — infrastruktura sieciowa i CPU padają. Rozwiązanie: rate limiting per socket (np. max 1 wiadomość lokalizacyjna na 500 ms na kierowcę) + agregacja pozycji w Redis przed broadcastem.

3. **Brak kompresji payloadu.** Lokalizacja to `{lat: 52.2297, lng: 21.0122, ts: 1735689600000, driverId: "abc123"}` — ~80 bajtów JSON. Przy 25 000 000 dostarczeń to ~2 GB/s ruchu wychodzącego. `permessage-deflate` w Socket.io kompresuje do ~30% rozmiaru. Alternatywnie: binarny format (MessagePack, Protobuf) redukuje payload do ~20 bajtów.

4. **Brak heartbeat / rozłączeń.** Klient mobilny traci zasięg. TCP nie wie o tym przez kilka minut. Serwer trzyma „martwe” połączenie w pamięci i próbuje wysyłać wiadomości. Bez `pingInterval` i `pingTimeout` (Socket.io ma domyślne, ale często wyłączane przez niedoświadczonych) serwer nie zwalnia zasobów.

### Mina Event Loopu: synchroniczne operacje blokujące

Scenariusz: endpoint `/export` generuje raport. Implementacja:

```javascript
app.get('/export', async (req, res) => {
  const rows = await db. „Backend WebSocket bez Redis Adaptera to gwarantowana awaria przy pierwszym skalowaniu poziomym — wiadomości z instancji A nigdy nie dotrą do użytkownika na instancji B, a klient nawet nie zobaczy błędu, tylko zamrożony interfejs. Zanim wdrożymy Socket.io, trzeba zaprojektować warstwę broadcastu przez Redis Streams z persystencją ostatnich N wiadomości i sticky sessions na load balancerze — inaczej każdy restart kontenera zrywa 100% połączeń.”

**Wariant B — Wydajność HTTP / architektura:**

> „NestJS z domyślnym adapterem Express traci połowę przepustowości na samym cyklu życia HTTP — FastifyAdapter daje 2–3× więcej RPS przy tym samym kodzie. Ale sam adapter to za mało: jeśli w serwisach są synchroniczne pętle po 200 000 elementów lub `JSON.stringify` na obiektach 50 MB, Event Loop Lag P99 przekroczy sekundę i cały backend zamarznie dla wszystkich użytkowników — dlatego architektura musi zakładać Worker Threads dla operacji CPU-bound od pierwszego commita.”

**Wariant C — Migracja z Express.js / refaktoryzacja:**

> „Express.js bez struktury modułowej po 2 latach rozwoju to koszmar on-boardingu i miejsce, w którym każda zmiana może wywołać regresję w niepowiązanym module. Migracja do NestJS z Clean Architecture to nie przepisanie kodu — to wyznaczenie granic domenowych, wprowadzenie DI z kontrolowanym zakresem i wymuszenie walidacji DTO na wejściu. Ale bez wyeliminowania circular dependencies przez `forwardRef` — architektura będzie tylko ładniej wyglądać na diagramie, a dług techniczny pozostanie.”

---

## 5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ)

| Antywzorzec | Dlaczego to czerwona flaga |
|---|---|
| Proponowanie Socket.io na produkcji bez adaptera klastrowego | Przy > 1 instancji backendu wiadomości nie są propagowane. Klient tego nie testuje w środowisku deweloperskim (1 instancja), więc awaria wychodzi dopiero na produkcji pod obciążeniem. |
| Wykonywanie operacji blokujących CPU w głównym wątku Node.js | `JSON.parse` na gigantycznym payloadzie, synchroniczne `crypto.pbkdf2Sync`, pętle po 500k elementów — każda z tych operacji zamraża Event Loop. Rozwiązanie: Worker Threads lub kolejka BullMQ z procesorem jako osobny worker. |
| „Express jest domyślnym i najlepszym silnikiem dla NestJS” | Prawda połowiczna. Express jest domyślny, ale nie najlepszy dla wysokiego throughputu. FastifyAdapter to standard produkcyjny, gdy RPS > 10 000. Pominięcie tego faktu oznacza brak świadomości wydajnościowej. |
| Ignorowanie connection poolingu przy ORM | Prisma zarządza poolem wewnętrznie; Drizzle deleguje do `pg.Pool`. W obu przypadkach trzeba jawnie skonfigurować `max` (zazwyczaj 10–20 na instancję) i `idleTimeoutMillis`. Domyślne ustawienia `pg.Pool` (max: 10) są zbyt niskie dla backendu z 50 jednoczesnymi żądaniami do bazy. |
| Brak walidacji DTO na granicy aplikacji | `class-validator` lub Zod na DTO to nie „overhead” — to zabezpieczenie przed niepoprawnymi danymi, które wpadną do serwisu i wywołają `TypeError` w środku logiki biznesowej. Koszt walidacji (~0.1 ms na DTO) jest znikomy w porównaniu do kosztu debugowania błędów danych w produkcji. |
| Używanie `forwardRef()` jako standardowego rozwiązania circular dependencies | `forwardRef` to obejście cyklu, który nie powinien istnieć. Jeśli moduły A i B wymagają `forwardRef`, granice domenowe są źle wyznaczone. Prawidłowa architektura powinna mieć jednokierunkowy graf zależności. |

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 5 500 – 15 000 ZŁ)

### Moduł 1: Szkielet architektury NestJS — Clean Architecture, Fastify, DTO, globalne filtry i interceptory
**Zakres:** Konfiguracja projektu NestJS z FastifyAdapter, struktura folderów domenowych (`src/modules/[domain]/`), warstwy: `controllers/`, `services/`, `repositories/`, `dto/`, `entities/`. Globalne `ValidationPipe` z `class-validator` lub Zod, globalny `ExceptionFilter` (mapowanie wyjątków domenowych na kody HTTP), globalny `LoggingInterceptor` (structured logging z `nestjs-pino` lub `nestjs-winston`), `ConfigModule` z walidacją zmiennych środowiskowych (Joi / Zod). Konfiguracja `class-transformer` z `excludeExtraneousValues: true` dla response DTO.  
**Wycena:** 3 500 – 5 000 zł.

### Moduł 2: Warstwa danych i relacji — ORM, migracje, indeksy, connection pooling
**Zakres:** Wybór ORM (Drizzle lub Prisma) i konfiguracja połączenia z PostgreSQL. Definicja schematu z relacjami, indeksami (B-tree, GIN dla JSONB, partial indexes), migracje (Drizzle Kit / Prisma Migrate). Konfiguracja connection poolingu: `max`, `idleTimeoutMillis`, `connectionTimeoutMillis`. Repozytoria jako warstwa abstrakcji nad ORM — serwisy nie importują klienta ORM bezpośrednio. Seedery danych testowych.  
**Wycena:** 2 500 – 4 000 zł.

### Moduł 3: Skalowalna brama WebSockets / gRPC — Socket.io + Redis Adapter, room management, rate limiting
**Zakres:** Konfiguracja Socket.io z `@socket.io/redis-adapter` (Pub/Sub) lub `@socket.io/redis-streams-adapter` (reliable delivery). Room management (per użytkownik, per kierowca, per region geograficzny). Rate limiting per socket (wiadomości/s), heartbeat z konfigurowalnym `pingInterval` / `pingTimeout`, obsługa reconnectu z odtworzeniem stanu z Redis. Dla gRPC: definicja `.proto`, serwer gRPC w NestJS (`@nestjs/microservices`), deadline propagation, retry z exponential backoff, mTLS dla komunikacji między serwisami.  
**Wycena:** 3 500 – 5 500 zł.

### Moduł 4: Bezpieczeństwo i uwierzytelnianie — JWT, Guards, RBAC, Passport
**Zakres:** Strategia JWT (access token + refresh token) z rotacją refresh tokenów i blacklistą w Redis. Guards: `JwtAuthGuard`, `RolesGuard` z dekoratorem `@Roles()`. RBAC — role i uprawnienia w bazie z cache w Redis. Rate limiting na endpointach auth (brute-force protection). CORS, CSRF, helmet. Walidacja tokenów w WebSocket handshake (autoryzacja socketu przed ustanowieniem połączenia).  
**Wycena:** 2 000 – 3 500 zł.

### Moduł 5: Testy jednostkowe i e2e + konteneryzacja (multi-stage Docker build)
**Zakres:** Testy jednostkowe serwisów z mockami repozytoriów (Vitest dla NestJS 12 ESM lub Jest dla CJS). Testy e2e z `supertest` / `light-my-request` (Fastify) na rzeczywistej instancji aplikacji z testową bazą (Testcontainers). Dockerfile z multi-stage build: etap `builder` (instalacja deps + kompilacja TS), etap `production` (tylko `dist/` + `node_modules` produkcyjne, bez devDependencies). Non-root user w kontenerze, `NODE_OPTIONS=--max-old-space-size=512` dla kontroli zużycia pamięci.  
**Wycena:** 2 500 – 4 000 zł.

**Wycena łączna:** 14 000 – 22 000 zł (przy pełnym zakresie). Dla Useme — realny zakres do 15 000 zł wymaga priorytetyzacji: Moduł 1 + Moduł 2 + Moduł 3 (bez gRPC) + podstawowe testy i Docker = ~11 500 – 15 000 zł.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU)

**Pytanie 1 — Skalowanie WebSockets:**
> „Ile jednoczesnych połączeń WebSocket ma obsługiwać system w szczycie i czy backend docelowo działa na więcej niż jednej instancji za load balancerem? Jeśli tak — czy warstwa broadcastu jest już zaprojektowana pod Redis Adapter, czy obecny kod zakłada jeden proces Node.js?”

**Pytanie 2 — Komunikacja wewnętrzna i opóźnienia:**
> „Czy system docelowo będzie podzielony na osobne serwisy (np. serwis użytkowników, serwis zamówień, serwis powiadomień), czy pozostaje modularnym monolitem? Jeśli mikrousługi — jakie są wymagania dotyczące opóźnień komunikacji wewnętrznej i czy rozważaliście gRPC zamiast REST/JSON dla komunikacji service-to-service?”

**Pytanie 3 — Wydajność i operacje CPU-bound:**
> „Czy w backendzie są operacje przetwarzania danych, które mogą blokować Event Loop — na przykład generowanie raportów, eksporty, transformacje dużych zbiorów danych, synchroniczne operacje kryptograficzne? Czy obecny monitoring obejmuje Event Loop Lag i czy mierzyliście P99 tego wskaźnika pod obciążeniem produkcyjnym?”

---

*Karta wiedzy wygenerowana dla bota ofertowego Useme / B2B. Wersja 2026.09. Wszystkie dane techniczne zweryfikowane na podstawie dokumentacji Node.js 22 LTS, NestJS 12, Socket.io, Drizzle ORM i Prisma 7.*