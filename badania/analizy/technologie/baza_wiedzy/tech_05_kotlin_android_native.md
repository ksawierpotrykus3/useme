# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME
## TEMAT: Kotlin & Android Native — Architektura Usług w Tle, Integracje ze Sprzętem i Wymogi Google Play 2026

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1 Typowe zlecenia w segmencie mobilnym

Na platformie Useme segment Kotlin/Android Native koncentruje się wokół kilku powtarzalnych kategorii zleceń:

| Kategoria | Charakterystyka | Typowy klient |
|---|---|---|
| **Aplikacje logistyczno-magazynowe na terminale przemysłowe** | Integracja ze skanerami Zebra/Honeywell, praca w sieci offline-first, synchronizacja z WMS/ERP | Kierownik operacji/logistyki, integrator systemów magazynowych |
| **Aplikacje telemetryczne/IoT z Bluetooth BLE** | Odczyt danych z czujników, GATT Client/Server, reconnections, praca w tle | Startup IoT, software house bez kompetencji natywnych |
| **Natywne moduły hardware** | Sterowniki do drukarek, wag, czytników RFID, integracja przez USB/Bluetooth | Firma przemysłowa, producent urządzeń |
| **Refaktoryzacja legacy Java → Kotlin** | Przepisanie aplikacji biznesowej, modernizacja stosu technologicznego, migracja z AsyncTask na Coroutines | Software house przejmujący utrzymanie, dział IT przedsiębiorstwa |

### 1.2 Budżety

Wyniki audytu Useme dla bloku mobilnego wskazują, że zlecenia wygrywane przez elitę mieszczą się w przedziale **4 500 – 18 000 zł**. Średnie stawki na platformie Useme dla kategorii „tworzenie aplikacji" wynoszą ok. 3 974 zł, dla „usług IT" – ok. 3 995 zł, natomiast specjaliści od architektury osiągają średnio 3 809 zł za zlecenie. Oznacza to, że zlecenia z zakresu architektury usług w tle i integracji sprzętowych lokują się w górnej części widełek rynkowych, ponieważ wymagają wiedzy wykraczającej poza standardowe kompetencje dewelopera aplikacji CRUD.

### 1.3 Profil klienta

- **Founder startupu IoT** — potrzebuje prototypu MVP z komunikacją BLE, ale nie rozumie ograniczeń systemowych Androida.
- **Kierownik operacji/logistyki** — chce zastąpić papierowe procesy magazynowe aplikacją na terminale Zebra, ale nie ma świadomości różnicy między skanowaniem aparatem a natywnym SDK.
- **Software house bez natywnego Android dev-a** — przejął projekt po freelancerze, ma problem z utrzymaniem usług tła i musi przeprowadzić audyt zgodności z Google Play.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1 Restrykcje `foregroundServiceType` — Android 14/15

Od Android 14 (API 34) każda usługa pierwszoplanowa musi mieć zadeklarowany konkretny typ w manifeście przez atrybut `android:foregroundServiceType`. System wymusza tę deklarację, a przy jej braku generuje `MissingForegroundServiceTypeException` przy wywołaniu `startForeground()`.

**Dostępne typy istotne dla zleceń mobilnych:**

| Typ | Zastosowanie | Wymagane uprawnienie manifestu |
|---|---|---|
| `location` | Ciągłe śledzenie GPS, geofencing | `FOREGROUND_SERVICE_LOCATION` + runtime `ACCESS_FINE_LOCATION` / `ACCESS_BACKGROUND_LOCATION` |
| `connectedDevice` | Komunikacja Bluetooth BLE, USB, NFC, IR | `FOREGROUND_SERVICE_CONNECTED_DEVICE` + co najmniej jedno z: `BLUETOOTH_CONNECT`, `BLUETOOTH_SCAN`, `NFC`, `USB` |
| `dataSync` | Synchronizacja danych z backendem | `FOREGROUND_SERVICE_DATA_SYNC` |



**Kluczowa zmiana dla Android 15 (API 35):** system wprowadza timeout dla usług typu `dataSync` — łączny czas działania w oknie 24-godzinnym jest ograniczony do **6 godzin**. Po przekroczeniu tego limitu system wywołuje `Service.onTimeout(int, int)`, a usługa jest zatrzymywana. Dla aplikacji logistycznych działających w trybie ciągłym oznacza to konieczność migracji logiki synchronizacji do **WorkManager** lub podziału na wiele krótkich sesji `dataSync` zamiast jednej długotrwałej usługi.

**Konsekwencja biznesowa:** brak uzasadnienia typu usługi w Google Play Console (sekcja „App  „Potrzebujemy prostej aplikacji, która w tle co 10 sekund sprawdza pozycję GPS pracownika/kierowcy i wysyła na serwer."

**Co go utopi:**
1. **System Android ubije standardowy serwis** po 1–3 minutach od wygaszenia ekranu, jeśli nie jest to Foreground Service z widocznym powiadomieniem i zadeklarowanym typem `location`.
2. **Ciągły GPS wyczerpie baterię w 4 godziny** — każdy cykl `requestLocationUpdates` z wysoką dokładnością to skok zużycia energii. W praktyce magazynowej oznacza to konieczność wymiany baterii w terminalu co pół zmiany.
3. **Brak trwałego powiadomienia (Notification)** i uprawnienia `ACCESS_BACKGROUND_LOCATION` — to uprawnienie wymaga **osobnego formularza weryfikacji w Google Play Console**. Google od 2026 roku prowadzi audyt użycia lokalizacji w tle i w przypadku braku uzasadnienia **usuwa aplikację oraz konto dewelopera**.
4. **Geofencing zamiast ciągłego pollingu** — prawidłowe rozwiązanie architektoniczne to użycie `FusedLocationProviderClient` z geofencingiem: aplikacja rejestruje geofences wokół stref magazynowych i budzi się tylko przy przekroczeniu granicy, zamiast odpytywać GPS co 10 sekund.

### 3.2 Mina terminali Zebra/Honeywell — skanowanie aparatem vs natywne SDK

**Antywzorzec:** Próba czytania kodów kreskowych przez `Camera2` / `ML Kit` zamiast integracji z natywnym SDK skanera.

**Konsekwencje:**
- Opóźnienie **~2 sekundy na skan** zamiast **~50 ms** przy użyciu sprzętowego skanera.
- Konieczność utrzymywania ostrości, oświetlenia, kąta — magazynier traci 3–4 sekundy na każdy odczyt.
- Bunt załogi i odrzucenie aplikacji po pierwszym dniu pilotażu.

**Prawidłowe rozwiązanie:**
- **Zebra:** DataWedge API (Intent-based) lub EMDK dla Android. DataWedge to rekomendowane podejście — Zebra wprost zaleca używanie DataWedge API zamiast EMDK Barcode APIs, ponieważ nowe funkcje trafiają najpierw do DataWedge.
- **Honeywell:** Mobility SDK lub Data Collection Intent API (nie wymaga instalacji pełnego SDK, wystarczy wysłanie Intentów do claim/release skanera).

**Architektura integracji:** `BroadcastReceiver` nasłuchujący Intentów z DataWedge (akcja `com.symbol.datawedge.api.RESULT_ACTION`) lub `Intent` z Honeywell. Dane skanowania trafiają bezpośrednio do aplikacji bez pośrednictwa aparatu fotograficznego.

---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

### 4.1 Gotowe otwarcia ofertowe

**Wariant A — dla zleceń logistycznych/magazynowych:**
> „Zanim zaczniemy mówić o funkcjach aplikacji — jeśli w tym projekcie ma działać ciągłe śledzenie pozycji pracownika w tle, to bez zadeklarowania `foregroundServiceType="location"` i przejścia audytu Google Play dla `ACCESS_BACKGROUND_LOCATION` aplikacja nie przejdzie weryfikacji. Drugi punkt krytyczny: terminale Zebra/Honeywell wymagają integracji przez DataWedge/Mobility SDK, a nie aparatu — inaczej skan trwa 2 sekundy zamiast 50 ms."

**Wariant B — dla zleceń IoT/BLE:**
> „Aplikacja łącząca się z czujnikami przez BLE w tle na Androidzie 14+ wymaga zadeklarowania `foregroundServiceType="connectedDevice"` i przemyślanej strategii reconnections z exponential backoff — standardowe `autoConnect=true` zawodzi na Xiaomi i Samsungu. Drugi problem architektoniczny to wymóg 16 KB page size dla bibliotek natywnych, który wchodzi w życie w Google Play 1 listopada 2025 (z możliwością przedłużenia do maja 2026)."

### 4.2 Natychmiastowe rozwiązania wskazywane w ofercie

- **Dla lokalizacji:** Fused Location Provider + geofencing zamiast ciągłego pollingu.
- **Dla terminali:** DataWedge API (Zebra) / Mobility SDK (Honeywell) — natywne skanowanie sprzętowe.
- **Dla synchronizacji:** WorkManager z ograniczeniem `dataSync` do 6 godzin na dobę lub podział na krótkie sesje.

---

## 5. CZERWONA LISTA / ANTYWZORCE

### 5.1 Kategoryczne zakazy

| Antywzorzec | Dlaczego jest katastrofalny |
|---|---|
| **Obiecywanie „niewidocznego śledzenia w tle bez powiadomienia na pasku"** | Technicznie niemożliwe od Androida 8+. Foreground Service **musi** mieć widoczne powiadomienie. Próby obejścia (ukryte powiadomienia, `setForegroundServiceBehavior`) grożą natychmiastowym banem konta dewelopera w Google Play. |
| **Ignorowanie specyfiki OEM (Xiaomi/Huawei/Samsung)** | Bez instrukcji dla użytkownika o wyłączeniu optymalizacji baterii i whitelisty autostartu aplikacja „działa u dewelopera na Pixelu", ale nie na terminalu w magazynie. |
| **WebView jako rozwiązanie dla komunikacji z Bluetooth/hardware** | WebView nie ma dostępu do natywnych API Bluetooth, USB ani skanerów. Aplikacja „hybrydowa udająca natywną" w kontekście hardware to strata budżetu i czasu. |
| **Polling GPS co 10 sekund przez całą dobę** | Zabija baterię w 4 godziny i nie przechodzi audytu Google Play. |
| **Poleganie na `autoConnect=true` w BLE** | Nie działa niezawodnie na większości urządzeń peryferyjnych i OEM — wymagana własna logika reconnections. |

### 5.2 Czerwone flagi w komunikacji z klientem

- Klient mówi „prosta aplikacja" w kontekście usług tła → **zawsze** oznacza to co najmniej 2–3 tygodnie pracy architektonicznej.
- Klient mówi „będzie działać na telefonach pracowników" (BYOD) → dodatkowe komplikacje: fragmentacja Androida, brak kontroli nad MDM, problemy z uprawnieniami na urządzeniach prywatnych.
- Klient nie wie, czy aplikacja idzie do Google Play, czy przez MDM → to determinuje strategię dystrybucji i wymagania uprawnień (dla MDM można pominąć część polityk Google Play, ale traci się dostęp do niektórych API).

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE

### 6.1 Proponowany podział modułowy (wycena 6 000 – 16 000 zł)

| Moduł | Zakres | Szacowany czas | Wycena cząstkowa |
|---|---|---|---|
| **M1. Warstwa komunikacji hardware** | GATT Client (BLE) lub DataWedge BroadcastReceiver (Zebra) / Mobility SDK (Honeywell); reconnections, MTU negotiation | 5–10 dni | 2 000 – 4 500 zł |
| **M2. Silnik usług tła** | Foreground Service z `NotificationChannel`, deklaracja `foregroundServiceType`, WorkManager fallback, obsługa `Service.onTimeout()` dla Android 15 | 4–8 dni | 1 800 – 3 500 zł |
| **M3. Lokalna baza offline-first** | Room z KSP, szyfrowanie SQLCipher, migracje schematu, indeksy pod zapytania magazynowe | 3–5 dni | 1 200 – 2 000 zł |
| **M4. Interfejs użytkownika** | Jetpack Compose, nawigacja, obsługa skanowania, tryb ciemny dla hali magazynowej | 5–8 dni | 2 000 – 3 500 zł |
| **M5. Moduł synchronizacji** | Retrofit/Ktor, exponential retry, wykrywanie sieci, kolejkowanie offline | 4–6 dni | 1 500 – 2 500 zł |
| **M6. Przygotowanie do publikacji** | Zgodność z Android 14/15, deklaracje uprawnień w Play Console, 16 KB page size, polityki prywatności | 3–5 dni | 1 000 – 2 000 zł |
| **RAZEM** | | **24–42 dni** | **9 500 – 18 000 zł** |

### 6.2 Kluczowe decyzje architektoniczne

1. **Offline-first:** Room jako źródło prawdy, synchronizacja jako proces w tle. Aplikacja musi działać bez internetu — magazyn często ma martwe strefy Wi-Fi.
2. **WorkManager dla `dataSync`:** zamiast długotrwałej usługi `dataSync` (limit 6h/24h na Androidzie 15), stosujemy periodyczne workery z ograniczeniem `NetworkType.CONNECTED`.
3. **Foreground Service tylko dla `connectedDevice` i `location`:** skanowanie i śledzenie wymagają natychmiastowej reakcji, więc uzasadnione jest trwałe powiadomienie.
4. **Testy na fizycznych urządzeniach docelowych:** emulator nie odzwierciedli zachowania BLE ani DataWedge. Testy na Zebra TC21/TC22, Honeywell CT45, Xiaomi Redmi (jako „worst case" dla battery killera).

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE

Poniższe pytania należy wpleść w środek analizy ofertowej — zmuszają klienta do natychmiastowej odpowiedzi i weryfikują, czy projekt jest wykonalny w podanym budżecie:

**Pytanie 1 — determinuje architekturę dystrybucji i uprawnień:**
> „Czy aplikacja ma trafić do Google Play (publicznie), czy będzie dystrybuowana wewnętrznie przez MDM (np. SOTI, VMware Workspace ONE) na dedykowane terminale firmowe? Od tego zależy zakres wymaganych deklaracji w Play Console i możliwość użycia uprawnień, które w Google Play wymagają audytu."

**Pytanie 2 — determinuje budżet modułu lokalizacji:**
> „Jaki jest akceptowalny interwał raportowania pozycji i czy lokalizacja ma być zbierana również poza strefą magazynu, czy tylko w geofence'ach? Ciągłe śledzenie z interwałem <30 s wymaga `ACCESS_BACKGROUND_LOCATION` i osobnego audytu Google Play — to dodatkowe 2–3 dni pracy i ryzyko odrzucenia, którego nie da się wycenić ryczałtowo."

**Pytanie 3 — determinuje architekturę hardware'u:**
> „Czy aplikacja będzie działać na dedykowanych terminalach magazynowych (Zebra/Honeywell z wbudowanym skanerem), czy na prywatnych telefonach pracowników (BYOD) ze skanowaniem przez aparat? W pierwszym przypadku integrujemy DataWedge/Mobility SDK (50 ms/skan), w drugim — ML Kit/CameraX (2 s/skan). To fundamentalnie różne moduły i różne budżety."

---

## PODSUMOWANIE — ESENCJA OFERTY DLA BOTA

Oferta wygrywająca w segmencie Kotlin/Android Native na Useme **nie zaczyna się od „mam 5 lat doświadczenia"**, ale od:

1. **Zdiagnozowania problemu architektonicznego w pierwszych 2 zdaniach** (foregroundServiceType, OEM battery killers, 16 KB page size).
2. **Wskazania antywzorca, którego klient nie widzi** (skanowanie aparatem zamiast DataWedge, ciągły GPS zamiast geofencingu).
3. **Zadania 2–3 pytań kwalifikujących w środku tekstu**, które wymuszają odpowiedź na priv.
4. **Rozbicia wyceny na moduły** z jasnym uzasadnieniem, dlaczego moduł usług tła kosztuje więcej niż moduł UI.

Ta karta stanowi bazę operacyjną bota — każde odstępstwo od wymienionych faktów inżynierskich powinno być traktowane jako sygnał do weryfikacji źródła.