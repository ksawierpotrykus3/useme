# SYNTEZA BOJOWA BOTA — GRUPA 3: MOBILE NATIVE, HARDWARE & VOIP
## DOKUMENT OPERACYJNY DLA GENERATORA OFERT USEME

**Wersja:** 1.0 | **Stan na:** wrzesień 2026 | **Zakres:** Kotlin/Android Native (Zebra, BLE, tło), Flutter/Dart (Impeller, SPM, offline-first), Swift/iOS Native (StoreKit 2, Privacy Manifests, BackgroundTasks), VoIP/Asterisk/PJSIP (transkrypcja AI, NAT, hardening)

**Zasada nadrzędna:** Oferta wygrywa w 5 sekund albo przegrywa w 5 sekund. Pierwsze dwa zdania nie mówią o wykonawcy — mówią o ukrytym problemie architektonicznym klienta. Jedyne CTA to odpowiedź na priv. Zero calli, zero „chętnie pomogę".

---

## 1. STRATEGIA DEKLASACJI W PIERWSZYCH 2 ZDANIACH (KATALOG CIOSÓW OTWIERAJĄCYCH)

### 1.1 Kotlin / Android Native (Zebra, BLE, usługi tła)

> „Zanim przejdziemy do funkcji — jeśli w projekcie ma działać ciągłe śledzenie pozycji pracownika w tle, to bez zadeklarowania `foregroundServiceType="location"` i przejścia audytu Google Play dla `ACCESS_BACKGROUND_LOCATION` aplikacja nie przejdzie weryfikacji; a terminale Zebra/Honeywell wymagają integracji przez DataWedge/Mobility SDK (50 ms/skan), nie przez aparat (2 s/skan). Drugi punkt krytyczny: na Androidzie 15 usługa typu `dataSync` ma twardy limit 6h/24h, a `autoConnect=true` w BLE zawodzi na Xiaomi i Samsungu — to determinuje architekturę modułu synchronizacji i reconnections jeszcze przed pierwszą linią kodu."

### 1.2 Flutter / Dart (Impeller, wieloplatformowość, SPM)

> „Impeller prekompiluje shadery w czasie budowania, więc „shader compilation jank" ze Skii znika — ale nie kompensuje złej architektury stanu: `setState` na szczycie hierarchii nadal dropuje klatki ze 120 do 20 FPS. Równolegle trzeba zaadresować, że iOS `BGTaskScheduler` i Android `WorkManager` to dwa różne cykle życia, których framework nie abstrahuje, a SPM zastępuje CocoaPods (rejestr read-only od 2 grudnia 2026) — bez tego oferta jest niekompletna."

### 1.3 Swift / iOS Native (StoreKit 2, Privacy Manifests)

> „Od 2024 Apple wymaga `PrivacyInfo.xcprivacy` dla **każdej aplikacji i każdego SDK firm trzecich** — brak manifestu u któregoś z nich to odrzucenie uploadu z błędem `ITMS-91053`, nie ostrzeżenie; w praktyce 80% odrzuceń wynika z zaniedbanych SDK, nie z kodu aplikacji. Drugi punkt: jeśli planujesz monetyzację treści cyfrowych, Stripe/PayPal jest wykluczony przez Guideline 3.1.1 — jedyna droga to StoreKit 2 z walidacją JWS, a „pobieranie co 5 minut w tle" jest na iOS niemożliwe bez Silent Push (APNs ` „Problem, który opisujesz — audio tylko w jedną stronę — to w 80% przypadków skutek tego, że Asterisk za NAT-em reklamuje w SDP swój prywatny adres IP zamiast publicznego; `externip`, `localnet` i wyłączony SIP ALG na routerze to trzy osobne warstwy do naprawy, których amatorzy nie rozdzielają. Drugi punkt: `chan_sip` nie istnieje w Asterisk 21+, więc `Dial(SIP/...)` w dialplanie wymaga konwersji na `Dial(PJSIP/...)` przed upgrade'em, a przy >20 kanałach WebRTC (Opus) transkodowanie na G.711 dla trunkingu operatorskiego wymaga osobnego planu CPU."

---

## 2. TABELA MIN TECHNICZNYCH

| Technologia | Pozorne życzenie klienta | Prawdziwa mina pod maską | Twardy fakt inżynierski używany przez bota |
|---|---|---|---|
| **Kotlin / tło** | „Prosta apka, w tle co 10 s sprawdza GPS i wysyła na serwer" | System ubije serwis po 1–3 min od wygaszenia ekranu; ciągły GPS = bateria w 4 h; brak trwałego powiadomienia = ban dewelopera | `foregroundServiceType="location"` + `FusedLocationProviderClient` + geofencing zamiast pollingu; `ACCESS_BACKGROUND_LOCATION` wymaga osobnego audytu w Play Console |
| **Kotlin / skanowanie** | „Skanowanie kodów kreskowych aparatem telefonu" | 2 s/skan vs 50 ms; bunt załogi po pierwszym dniu pilotażu | Zebra DataWedge API (Intent-based) lub Honeywell Mobility SDK; `BroadcastReceiver` na `com.symbol.datawedge.api.RESULT_ACTION` |
| **Kotlin / BYOD** | „Aplikacja na telefony pracowników" | Fragmentacja Androida, brak MDM, brak kontroli nad uprawnieniami, brak whitelisty autostartu | BYOD = ML Kit/CameraX; dedykowane terminale = natywne SDK. Dwie fundamentalnie różne architektury i budżety |
| **Kotlin / sync** | „Synchronizacja z WMS przez cały dzień" | Na Androidzie 15 `dataSync` ma limit 6h/24h; po przekroczeniu `Service.onTimeout()` zabija usługę | WorkManager z `NetworkType.CONNECTED` + podział na krótkie sesje; `Service.onTimeout(int,int)` jako punkt kontrolny |
| **Kotlin / 16 KB** | „Targetujemy Android 15" | Brak wsparcia 16 KB page size = blokada uploadu w Google Play na urządzeniach 64-bit | `useLegacyPackaging = false` w `build.gradle.kts` + aktualizacja NDK i wszystkich bibliotek natywnych |
| **Kotlin / BLE** | „Czujniki łączą się przez BLE w tle" | `autoConnect=true` zawodzi na Xiaomi, Samsung, Oppo; brak reconnections z backoffem | `foregroundServiceType="connectedDevice"` + własna logika reconnections z exponential backoff |
| **Flutter / shared code** | „Jedna aplikacja identyczna na iOS i Androidzie, działa idealnie w tle" | 100% shared code to iluzja: kamera, push (APNs vs FCM), deep linking (Universal vs App Links), tło — zawsze natywne per platforma | `Info.plist`, `AndroidManifest.xml`, `PrivacyInfo.xcprivacy`, `build.gradle.kts` — ręczna konfiguracja per platforma |
| **Flutter / migracja** | „Przepisz z Ionic/Cordova na Fluttera" | `localStorage` nie ma odpowiednika natywnego; routing WebView nie zadziała z Universal Links po wymianie silnika | `go_router` z deklaratywnym routingiem + Drift/Hive CE z migracją schematu; `localStorage` → SQLite/NoSQL |
| **Flutter / state** | „Szybkie MVP, zrobimy potem" | Wybór BLoC vs Riverpod determinuje ~40% kodu i koszt utrzymania | Riverpod 3.x dla MVP/startupu; BLoC 9.x dla enterprise/audytu (fintech, medtech); `bloc_concurrency` dla kontroli współbieżności |
| **Flutter / bazy** | „Baza lokalna offline-first, byle szybko" | Isar ma niepewny status maintenance — ryzyko dla nowego projektu produkcyjnego w 2026; Hive v2 jest przestarzały | Drift (SQLite, relacyjny, migracje, SQLCipher) lub Hive CE (społecznościowy fork); Isar tylko z zastrzeżeniem |
| **Flutter / 16 KB** | „Targetujemy Android 15" | Google Play blokuje upload bez wsparcia 16 KB page size na urządzeniach 64-bit | Flutter 3.38+ obsługuje wymóg, ale wymaga `useLegacyPackaging = false` i aktualnych bibliotek NDK |
| **Swift / monetyzacja** | „Subskrypcja w aplikacji, płatność Stripe/PayPal" | Guideline 3.1.1 = odrzucenie w Review; bypass IAP = ban konta | StoreKit 2 + walidacja JWS (`Transaction.updates`, `Product.purchase()`); jeśli dobra fizyczne — Guideline 3.1.5 dopuszcza płatności zewnętrzne |
| **Swift / tło** | „Pobieranie danych co 5 minut w tle" | iOS sam decyduje o czasie procesora; `BGAppRefreshTask` ~30 s, `BGProcessingTask` 1–10 min, tylko przy bezczynności | Silent Push (APNs `20 kanałach różnica między 2 vCPU a 8 vCPU; klient tego nie uwzględnił | Dla trunków operatorskich: `allow=ulaw,alaw`, `disallow=all`; dla WebRTC: Opus z fallbackiem; dedykowany serwer mediów przy skali |
| **VoIP / bezpieczeństwo** | „Wystawiamy port 5060 na publiczny internet" | Skanery SIP uderzają w kilka godzin od wystawienia; toll fraud = tysiące euro w jedną noc | Fail2Ban/CrowdSec + TLS (5061) + SRTP + VPN (Tailscale/WireGuard/ZeroTier) dla zdalnych extensionów; ACL do `localnet` |
| **VoIP / AI** | „Dodaj transkrypcję rozmów" | Batch vs real-time to dwie różne architektury; real-time wymaga AudioSocket + resampling 16 kHz + WebSocket STT | Batch: Whisper large-v3 (tańsza, dokładniejsza); real-time: AudioSocket + Deepgram Nova-2 WebSocket (1–5 s opóźnienia) |

---

## 3. ZESTAW PYTAŃ ZMUSZAJĄCYCH DO ODPOWIEDZI NA PRIV

> **Zasada:** Pytania umieszczamy **w środku analizy**, nigdy na końcu. Klient musi je przeczytać w kontekście problemu, który właśnie zdiagnozowaliśmy — dopiero wtedy stanowią dźwignię.

### Kotlin / Android Native

1. **Dystrybucja i uprawnienia:** „Czy aplikacja trafi do Google Play publicznie, czy będzie dystrybuowana wewnętrznie przez MDM (SOTI, VMware Workspace ONE) na dedykowane terminale firmowe? Od tego zależy zakres deklaracji w Play Console i możliwość użycia uprawnień, które w Google Play wymagają audytu."
2. **Lokalizacja:** „Jaki jest akceptowalny interwał raportowania pozycji i czy lokalizacja ma być zbierana również poza strefą magazynu, czy tylko w geofence'ach? Ciągłe śledzenie <30 s wymaga `ACCESS_BACKGROUND_LOCATION` i osobnego audytu Google Play — to dodatkowe 2–3 dni pracy i ryzyko odrzucenia, którego nie da się wycenić ryczałtowo."
3. **Hardware:** „Czy aplikacja pójdzie na dedykowane terminale Zebra/Honeywell z wbudowanym skanerem, czy na prywatne telefony pracowników (BYOD) ze skanowaniem przez aparat? W pierwszym przypadku integrujemy DataWedge/Mobility SDK (50 ms/skan), w drugim ML Kit/CameraX (2 s/skan). To fundamentalnie różne moduły i różne budżety."

### Flutter / Dart

1. **Tło i hardware:** „Czy aplikacja wymaga dostępu do funkcji sprzętowych w tle (ciągła lokalizacja GPS, Bluetooth do skanera, synchronizacja z urządzeniami peryferyjnymi)? Jeśli tak — konieczne jest zadeklarowanie `foregroundServiceType` w manifeście i wdrożenie Foreground Service, a na iOS użycie `BGTaskScheduler`. To determinuje architekturę modułu tła i wpływa na czas realizacji."
2. **Konta:** „Czy posiadają Państwo już założone konta Apple Developer Program (99 USD/rok) i Google Play Console (25 USD jednorazowo)? Brak konta Apple oznacza, że proces publikacji — w tym generowanie certyfikatów i provisioning profiles — będzie częścią zakresu prac."
3. **Offline-first:** „Czy projekt wymaga trybu offline-first z pełną synchronizacją dwukierunkową? Jeśli tak — kluczowa jest decyzja między Drift (SQLite, relacyjny, migracje) a Hive CE (key-value, szybszy dla prostych struktur), plus zaprojektowanie strategii rozwiązywania konfliktów (last-write-wins vs CRDT)."

### Swift / iOS Native

1. **Konto i D-U-N-S:** „Czy posiadają Państwo już zweryfikowane konto Apple Developer Program dla organizacji z numerem D-U-N-S? Proces uzyskania D-U-N-S i weryfikacji Apple trwa 2–4 tygodnie. Bez tego konta nie możemy opublikować aplikacji, nawet jeśli development zakończy się wcześniej — rekomenduję rozpoczęcie procedury natychmiast, równolegle z pracami koncepcyjnymi."
2. **Kwalifikacja dóbr:** „Czy oferowane w aplikacji usługi/produkty kwalifikują się jako dobra cyfrowe podlegające StoreKit 2 (subskrypcje, odblokowanie funkcji, treści premium), czy jako dobra fizyczne / usługi offline (dopuszczalne płatności zewnętrzne zgodnie z Guideline 3.1.5)? Od tej kwalifikacji zależy cała architektura monetyzacji i czy integracja Stripe/PayPal jest w ogóle dopuszczalna."
3. **Tło:** „Jaki jest plan obsługi powiadomień w tle — Silent Push (APNs z ` **Zasada:** Każda wycena to 4–7 modułów architektonicznych z jasnym zakresem i widełkami. Cena nie jest ryczałtem — jest sumą decyzji architektonicznych. Klient widzi, za co płaci, i nie może porównać oferty z „3 500 zł za całość" konkurencji, bo tam nie ma rozbicia.

### 5.1 Kotlin / Android Native (terminal, BLE, offline-first) — 9 500 – 18 000 zł

| Moduł | Zakres | Wycena |
|---|---|---|
| **M1. Warstwa komunikacji hardware** | GATT Client (BLE) lub DataWedge `BroadcastReceiver` (Zebra) / Mobility SDK (Honeywell); reconnections z backoffem, MTU negotiation | 2 000 – 4 500 zł |
| **M2. Silnik usług tła** | Foreground Service z `NotificationChannel`, `foregroundServiceType`, WorkManager fallback, obsługa `Service.onTimeout()` dla Android 15 | 1 800 – 3 500 zł |
| **M3. Lokalna baza offline-first** | Room + KSP, SQLCipher, migracje schematu, indeksy pod zapytania magazynowe | 1 200 – 2 000 zł |
| **M4. UI (Jetpack Compose)** | Nawigacja, obsługa skanowania, tryb ciemny dla hali magazynowej, feedback haptyczny | 2 000 – 3 500 zł |
| **M5. Synchronizacja z WMS/ERP** | Retrofit/Ktor, exponential retry, wykrywanie sieci, kolejkowanie offline, rozwiązywanie konfliktów | 1 500 – 2 500 zł |
| **M6. Publikacja i compliance** | Android 14/15, deklaracje uprawnień w Play Console, 16 KB page size, polityka prywatności | 1 000 – 2 000 zł |

### 5.2 Flutter / Dart (MVP wieloplatformowy) — 7 000 – 18 000 zł

| Moduł | Zakres | Wycena |
|---|---|---|
| **M1. Architektura rdzenia + state management** | Riverpod 3.x lub BLoC 9.x, `go_router` z deep linkingiem, Clean Architecture (`data`/`domain`/`presentation`), DI | 2 000 – 3 500 zł |
| **M2. Warstwa sieciowa i cache** | `Dio` z interceptorami (JWT refresh, retry), Drift/Hive CE, offline-first z kolejką operacji | 1 500 – 3 000 zł |
| **M3. UI (Material 3 + Cupertino)** | Responsywność (`LayoutBuilder`), platform conventions, 120 FPS na Impellerze, `ListView.builder` z `itemExtent` | 2 000 – 3 500 zł |
| **M4. Natywna konfiguracja per platforma** | `Info.plist`, `AndroidManifest.xml`, `PrivacyInfo.xcprivacy`, `build.gradle.kts`, 16 KB page size | 1 000 – 2 000 zł |
| **M5. Publikacja** | Konta, certyfikaty, provisioning profiles, App Store Connect, Play Console | 500 – 1 500 zł |
| **M6. Testy i stabilizacja** | Testy jednostkowe domain, testy widgetów, integracja na urządzeniach fizycznych | 1 000 – 2 500 zł |

### 5.3 Swift / iOS Native — 12 000 – 22 000 zł

| Moduł | Zakres | Wycena |
|---|---|---|
| **M1. Architektura + Swift 6 strict concurrency** | `@Observable`, SwiftData, async/await, `Sendable`, struktura MVVM | 2 500 – 4 500 zł |
| **M2. Privacy Manifests + audyt SDK** | `PrivacyInfo.xcprivacy` dla aplikacji i każdego SDK, `NSPrivacyAccessedAPITypes`, audyt Firebase/Ads/Analytics | 1 500 – 3 000 zł |
| **M3. StoreKit 2 + walidacja JWS** | `Transaction.updates`, `Product.purchase()`, `AppStore.sync()`, walidacja JWS, App Store Server API | 2 000 – 4 000 zł |
| **M4. BackgroundTasks + Silent Push** | `BGAppRefreshTask`, `BGProcessingTask`, `BGContinuedProcessingTask` (iOS 26+), APNs ` **Reprezentatywne zlecenie:** „Aplikacja magazynowa na terminale Zebra — skanowanie kodów kreskowych, offline-first, synchronizacja z WMS, praca w tle. Budżet: 10 000 – 15 000 zł."

---

**Temat:** Aplikacja magazynowa Zebra — architektura tła, DataWedge i limit `dataSync` na Androidzie 15

Zanim przejdziemy do funkcji — jeśli w tym projekcie ma działać skanowanie na terminalach Zebra i ciągła synchronizacja z WMS, to bez integracji przez **DataWedge API** (50 ms/skan, nie 2 s przez aparat) i bez rozbicia synchronizacji na **WorkManager** (twardy limit `dataSync` na Androidzie 15 to 6h/24h, po którym `Service.onTimeout()` zabija usługę) aplikacja nie przejdzie ani pilotażu na hali, ani weryfikacji Google Play. Drugi punkt krytyczny: jeśli w grze jest ciągłe śledzenie pozycji pracownika, wymagany jest `foregroundServiceType="location"` + geofencing zamiast pollingu GPS — bez tego system ubije serwis po 1–3 minutach od wygaszenia ekranu, a bateria w terminalu padnie w 4 godziny.

**Co to znaczy dla tego projektu w praktyce:**

1. **Skanowanie sprzętowe vs aparat.** Terminale Zebra (TC21/TC22/TC52) i Honeywell (CT45/CT60) mają wbudowany skaner laserowy. Integrujemy go przez DataWedge `BroadcastReceiver` (akcja `com.symbol.datawedge.api.RESULT_ACTION`) — dane trafiają do aplikacji bez pośrednictwa `Camera2`/ML Kit. Różnica: 50 ms vs 2 s na skan. Przy 500 skanach na zmianę to 250 sekund vs 16 minut — i bunt załogi w pierwszym dniu pilotażu w wariancie „aparat".

2. **Tło — trzy warstwy do rozdzielenia.** `foregroundServiceType="connectedDevice"` dla skanera i Bluetooth (z uprawnieniem `BLUETOOTH_CONNECT`), `foregroundServiceType="dataSync"` dla synchronizacji z WMS — ale **nie jako jedna długa usługa**, bo Android 15 ją zabije po 6h/24h. Architektura: WorkManager z `NetworkType.CONNECTED` dla sync + Foreground Service `connectedDevice` dla skanera. Do tego whitelista autostartu na Xiaomi/Samsung/Oppo — bez instrukcji dla użytkownika aplikacja „działa u dewelopera na Pixelu", nie na terminalu w magazynie.

3. **Offline-first z Room jako źródłem prawdy.** Magazyn ma martwe strefy Wi-Fi. Aplikacja musi działać bez sieci — Room + KSP, migracje schematu, indeksy pod zapytania magazynowe. Synchronizacja z WMS jako proces w tle: kolejka operacji, exponential retry, wykrywanie sieci. Konflikty: `last-write-wins` z timestampem lub CRDT — do decyzji po analizie WMS.

4. **Android 15 i 16 KB page size.** Google Play blokuje upload aplikacji targetujących Android 15+ bez wsparcia 16 KB page size na urządzeniach 64-bitowych. Konieczne: `useLegacyPackaging = false` w `build.gradle.kts` + aktualizacja NDK i wszystkich bibliotek natywnych.

**Zanim oszacuję finalny budżet — trzy pytania, od których zależy architektura:**

**Pytanie 1 — dystrybucja i uprawnienia:** Czy aplikacja trafi do Google Play publicznie, czy będzie dystrybuowana wewnętrznie przez MDM (SOTI, VMware Workspace ONE) na dedykowane terminale firmowe? Od tego zależy zakres wymaganych deklaracji w Play Console i możliwość użycia uprawnień, które w Google Play wymagają audytu (np. `ACCESS_BACKGROUND_LOCATION`).

**Pytanie 2 — lokalizacja:** Jaki jest akceptowalny interwał raportowania pozycji i czy lokalizacja ma być zbierana również poza strefą magazynu, czy tylko w geofence'ach? Ciągłe śledzenie <30 s wymaga `ACCESS_BACKGROUND_LOCATION` i osobnego audytu Google Play — to dodatkowe 2–3 dni pracy i ryzyko odrzucenia, którego nie da się wycenić ryczałtowo.

**Pytanie 3 — hardware:** Czy aplikacja pójdzie na dedykowane terminale Zebra/Honeywell z wbudowanym skanerem, czy na prywatne telefony pracowników (BYOD) ze skanowaniem przez aparat? W pierwszym przypadku integrujemy DataWedge/Mobility SDK (50 ms/skan), w drugim ML Kit/CameraX (2 s/skan) — to fundamentalnie różne moduły i różne budżety.

**Rozbicie modułowe (wstępne, do doprecyzowania po odpowiedziach):**

| Moduł | Zakres | Wycena |
|---|---|---|
| **M1. Warstwa komunikacji hardware** | DataWedge `BroadcastReceiver` / Mobility SDK; reconnections BLE | 2 000 – 4 500 zł |
| **M2. Silnik usług tła** | Foreground Service `connectedDevice`, WorkManager dla sync, `Service.onTimeout()` dla Android 15 | 1 800 – 3 500 zł |
| **M3. Lokalna baza offline-first** | Room + KSP, migracje, indeksy, SQLCipher (opcjonalnie) | 1 200 – 2 000 zł |
| **M4. UI (Jetpack Compose)** | Nawigacja, obsługa skanowania, tryb ciemny dla hali | 2 000 – 3 500 zł |
| **M5. Synchronizacja z WMS** | Retrofit/Ktor, exponential retry, kolejkowanie offline, rozwiązywanie konfliktów | 1 500 – 2 500 zł |
| **M6. Publikacja i compliance** | Android 14/15, Play Console, 16 KB page size, polityka prywatności | 1 000 – 2 000 zł |

**Czerwone flagi, które odrzucam na wejściu:**

- **„Niewidoczne śledzenie w tle bez powiadomienia"** — technicznie niemożliwe od Androida 8+; Foreground Service musi mieć widoczne powiadomienie, próby obejścia = ban konta dewelopera.
- **„Skanowanie aparatem, bo taniej"** — 2 s/skan vs 50 ms; pilotaż na hali kończy się odrzuceniem aplikacji przez załogę.
- **`autoConnect=true` w BLE jako rozwiązanie** — zawodzi na Xiaomi, Samsungu, Oppo; wymagana własna logika reconnections z backoffem.
- **„Zrobimy na jednym telefonie testowym"** — emulator nie odzwierciedli DataWedge ani zachowania BLE; testy muszą iść na Zebra TC21/TC22, Honeywell CT45, Xiaomi Redmi (jako „worst case" dla battery killera).

**Dlaczego to działa:** Klient w pierwszych dwóch zdaniach dostaje diagnozę problemu, którego prawdopodobnie nie znał (limit `dataSync` 6h/24h na Androidzie 15, DataWedge vs aparat). W środku trzy pytania, na które **musi** odpowiedzieć, bo od nich zależy, czy projekt w ogóle ma szansę. Na końcu rozbicie modułowe, które uzasadnia cenę 9 500 – 18 000 zł jako sumę decyzji architektonicznych, a nie ryczałt. Czerwone flagi pokazują, że rozumiemy ryzyko — i że nie podejmiemy się projektu, który jest skazany na porażkę. Jedyne CTA: odpowiedź na priv z odpowiedziami na trzy pytania.

---

*Koniec syntezy bojowej — Grupa 3: Mobile Native, Hardware & VoIP. Dokument przeznaczony wyłącznie do użytku wewnętrznego generatora ofert Useme. Aktualizacja wymagana przy każdej zmianie major version: Flutter (3.44+), Riverpod (3.x), BLoC (9.x), Swift (6+), Asterisk (21+), Kotlin/Android (API 35+).*