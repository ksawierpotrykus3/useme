# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B

## TEMAT: Flutter & Dart — Architektura Aplikacji Wieloplatformowych (iOS + Android), Silnik Renderowania Impeller, Zarządzanie Stanem (BLoC / Riverpod) i Obsługa Natywnych Platform Channels

**Wersja dokumentu:** 1.0 | **Stan na:** wrzesień 2026 | **Klasyfikacja:** Wewnętrzna baza wiedzy ofertowej


## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1 Typologia zleceń

| Kategoria | Opis | Częstotliwość |
|---|---|---|
| **MVP dla startupu** | Budowa aplikacji na obie platformy (iOS/Android) z jednego kodu, z podstawową logiką biznesową, autoryzacją i minimum jednym przepływem monetyzacji | Wysoka |
| **E-commerce / B2B** | Katalog produktów, płatności, koszyk, integracja z backendem (REST/GraphQL), panel administracyjny | Średnia |
| **Migracja hybrydowa → Flutter** | Przepisanie aplikacji Ionic/Cordova na Fluttera z zachowaniem funkcjonalności i poprawą wydajności | Rosnąca (2026) |
| **Aplikacje logistyczno-przemysłowe** | Skanery kodów, integracja z hardware (Bluetooth, NFC, kamera), praca offline-first, synchronizacja z systemami WMS/ERP | Niszowa, ale wysokobudżetowa |

### 1.2 Budżety i profil klienta

- **Przedział budżetowy:** 5 000 – 20 000 zł za projekt.
- **Profil klienta #1:** Founder startupu z ograniczonym budżetem — nie stać go na dwa osobne zespoły (iOS + Android). Szuka jednego wykonawcy, który dostarczy obie platformy.
- **Profil klienta #2:** Agencja interaktywna — potrzebuje podwykonawcy do realizacji części mobilnej większego projektu.
- **Średnia wartość zlecenia programistycznego na Useme:** ponad 5 000 zł za projekt; tworzenie aplikacji mobilnych oscyluje wokół 3 974 zł dla prostszych zleceń, ale zlecenia Flutterowe z pełną architekturą regularnie osiągają 12 000 – 18 000 zł.


## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1 Silnik renderowania: Impeller jako domyślny backend

Impeller jest domyślnym silnikiem renderowania na iOS i Androidzie API 29+ od Fluttera 3.27. Na iOS jest to **jedyny obsługiwany** silnik — nie ma możliwości przełączenia na Skia. Na Androidzie Impeller działa domyślnie na API 29+, a na starszych urządzeniach lub bez wsparcia Vulkan następuje fallback do OpenGL.

**Dlaczego to ma znaczenie dla klienta:** Impeller prekompiluje shadery w czasie budowania, eliminując problem „shader compilation jank” charakterystyczny dla starego Skia — klatki nie dropują przy pierwszym uruchomieniu animacji czy przejść między ekranami. Używa Metal na iOS i Vulkan na Androidzie, co daje przewidywalne 120 FPS na urządzeniach z ProMotion / wysokoodświeżalnymi ekranami.

**Konsekwencja architektoniczna:** Niekontrolowane przebudowywanie drzewa widżetów (np. `setState` na szczycie hierarchii) nadal powoduje drop klatek — Impeller nie kompensuje złej architektury stanu. To krytyczny punkt, który odróżnia profesjonalną implementację od amatorskiej.

### 2.2 Toolchain i integracja natywna

**Swift Package Manager (SPM) zastępuje CocoaPods.** Od Fluttera 3.44 SPM jest domyślnym menedżerem zależności dla iOS i macOS. CocoaPods jest w trybie maintenance, a jego rejestr staje się **tylko do odczytu 2 grudnia 2026 roku**. Flutter nadal wspiera CocoaPods jako fallback dla pluginów, które nie mają jeszcze wsparcia SPM.

**Platform Channels i FFI.** Komunikacja Dart ↔ kod natywny odbywa się przez `MethodChannel` (asynchroniczna wymiana komunikatów) lub `dart:ffi` do bezpośredniego wywoływania kodu C/C++ bez pośrednictwa message-passingu. Dla type-safe komunikacji rekomendowane jest użycie pakietu `pigeon`, który generuje boilerplate po obu stronach.

**Konsekwencja architektoniczna:** Integracja z hardware (skanery, drukarki Bluetooth, NFC) wymaga natywnego kodu per platforma — nie ma „jednego kodu na wszystko”.

### 2.3 Zarządzanie stanem: BLoC vs Riverpod

| Kryterium | BLoC (v9.x) | Riverpod (3.x) |
|---|---|---|
| **Paradygmat** | Zdarzenia → Stany (explicit event queue) | Graf providerów z automatycznym cachingiem i inwalidacją |
| **Kiedy wybierać** | Duże zespoły, wymogi audytowe, regulacje (fintech, medtech) | Nowe aplikacje, szybkie MVP, startup |
| **Boilerplate** | Wysoki (event + state + handler) | Niski (szczególnie z code generation) |
| **Wydajność UI** | Deterministyczne przebudowy, kontrolowane przez `bloc_concurrency` | Fine-grained rebuilds przez `ref.watch` / `ref.select` |
| **Persystencja** | `hydrated_bloc` — drop-in state persistence | Eksperymentalna offline persistence w Riverpod 3 |

Riverpod 3.x wprowadził unified `Ref`, automatyczny retry z backoffem oraz eksperymentalne „Mutations” do efektów ubocznych. BLoC v9 utrzymuje model event/cubit z dojrzałym ekosystemem `bloc_concurrency` dla kontroli współbieżności (concurrent, sequential, droppable, restartable).

**Rekomendacja dla bota ofertowego:** Dla startupowego MVP — Riverpod. Dla klienta korporacyjnego z wymogami audytowymi — BLoC.

### 2.4 Architektura Offline-First i lokalny cache

| Baza | Typ | Zastosowanie | Status 2026 |
|---|---|---|---|
| **Drift** | Relacyjny SQLite z code generation | Dane offline-first, złożone zapytania, migracje schematu | **Rekomendowany** dla danych relacyjnych |
| **Isar** | NoSQL, błyskawiczne zapytania | Dokumenty JSON, reaktywne wzorce | Niepewny status maintenance — ryzyko dla nowych projektów produkcyjnych |
| **Hive CE** | Key-value, zero natywnych zależności | Proste preferencje, cache sesji | Społecznościowy fork po stagnacji Hive v2 |
| **Hive v2** | Key-value | — | **Przestarzały — nie używać** |

Drift oferuje opcjonalne szyfrowanie SQLCipher dla danych regulowanych (medycznych, finansowych). Isar, mimo świetnych parametrów wydajnościowych, ma niepewny status utrzymania — rekomendowanie go bez zastrzeżeń w nowym projekcie 2026 jest czerwoną flagą.


## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1 „Jedna aplikacja, identyczna na iOS i Androidzie, działająca idealnie w tle”

**Co klient pisze:** „Chcemy jedną aplikację na iOS i Androida, która będzie identyczna i będzie działać idealnie w tle.”

**Co go utopi:** Złudzenie 100% współdzielonego kodu. Funkcje systemowe — kamera, powiadomienia push (APNs vs FCM), deep linking (Universal Links vs App Links), uprawnienia w tle — **zawsze** wymagają konfiguracji natywnej per platforma. Pliki `Info.plist`, `Podfile`/`Package.swift`, `build.gradle.kts`, `AndroidManifest.xml` muszą być ręcznie skonfigurowane pod wymogi sklepów.

**Dodatkowa mina — Android 15/16 i 16 KB page size:** Od Android 15 AOSP wspiera urządzenia z 16 KB stronami pamięci. Wszystkie aplikacje targetujące Android 15 (API 35) i wyżej **muszą** wspierać 16 KB page size na urządzeniach 64-bitowych, inaczej Google Play zablokuje upload. Flutter 3.38 wspiera ten wymóg, ale wymaga poprawnej konfiguracji natywnych bibliotek (`useLegacyPackaging = false`).

### 3.2 Mina wydajnościowa: zarządzanie stanem i cyklem życia kontrolerów

**Przebudowywanie całego drzewa widżetów** — `setState` na szczycie hierarchii przy przewijaniu długich list powoduje drop klatek z 120 FPS do 20 FPS. Rozwiązanie: granularne zarządzanie stanem (Riverpod `select`, BLoC `buildWhen`) + `ListView.builder` z `itemExtent`.

**Wycieki pamięci** — nieodłączone `TextEditingController`, `AnimationController`, `ScrollController`, `StreamSubscription`. Każdy kontroler musi być zwolniony w `dispose()`. W aplikacji z 50 ekranami zaniedbanie tego powoduje degradację wydajności po 10–15 minutach użytkowania.

**Zarządzanie pamięcią w Dart 3.7+:** Lekkie izolaty z 50% redukcją overheadu pamięciowego. `Isolate.run()` obsługuje większość przypadków użycia, `compute()` pozostaje dla zadań specyficznych dla Fluttera. Ciężkie obliczenia (parsowanie JSON >1 MB, przetwarzanie obrazów, kryptografia) muszą być przenoszone do izolatów — w przeciwnym razie UI zamarza.

### 3.3 OEM battery killers (Xiaomi, Samsung, Oppo, Vivo)

Na agresywnych skinach Androidowych (Samsung OneUI, Xiaomi MIUI/HyperOS, Oppo ColorOS) headless Flutter engines są zabijane zanim zdążą się uruchomić. Aplikacje wymagające pracy w tle (skanery, logistyka, GPS tracking) **muszą** implementować:
- Foreground Service z odpowiednim `foregroundServiceType` w manifeście
- WorkManager dla zadań okresowych
- Detekcję optymalizacji baterii i instrukcje dla użytkownika (deep link do ustawień producenta)

Pakiety typu `background_guard` i `flutter_lifecycle_guard` diagnozują ryzyko restrykcji OEM i zarządzają foreground service automatycznie.


## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW)

### 4.1 Gotowe otwarcia inżynierskie

**Wariant A — dla zlecenia „przepisz z Ionic/Cordova na Fluttera”:**

> „Migracja z WebView na Fluttera wymaga przepisania warstwy nawigacji na `go_router` z deklaratywnym routingiem i deep linkingiem — w przeciwnym razie Universal Links (iOS) i App Links (Android) nie zadziałają po wymianie silnika. Drugim krytycznym punktem jest zastąpienie `localStorage` przez Drift lub Hive CE z uwzględnieniem migracji schematu, ponieważ WebView-based storage nie ma odpowiednika w środowisku natywnym.”

**Wariant B — dla zlecenia „MVP na obie platformy”:**

> „Przy budowie MVP na iOS i Androida z jednego kodu kluczowa jest separacja logiki biznesowej od warstwy widżetów — warstwa domain w czystym Darcie (bez importów Fluttera) pozwala na testy jednostkowe bez emulatora i wymianę backendu bez dotykania UI. Równolegle trzeba zaadresować fundamentalną różnicę w cyklu życia: iOS `BGTaskScheduler` vs Android `WorkManager` — to nie jest abstrahowane przez framework i wymaga natywnej konfiguracji per platforma.”

### 4.2 Dlaczego to deklasuje amatorów

Amator pisze: „Zrobię tanią apkę we Flutterze, jedna baza kodu, szybko i tanio.”

Profesjonalista otwiera problemem architektonicznym: separacja warstw, różnice w cyklu życia iOS vs Android, konkretne wymagania sklepów (Privacy Manifests, 16 KB page size). To natychmiast sygnalizuje klientowi, że rozmawia z inżynierem, a nie z wykonawcą „na sztuki”.


## 5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ)

### 5.1 Zakaz obiecywania „zerowego dotykania kodu natywnego”

Pliki `Info.plist`, `AndroidManifest.xml`, `build.gradle.kts` **muszą** być ręcznie skonfigurowane. Apple Privacy Manifests (`PrivacyInfo.xcprivacy`) są wymagane od lutego 2025 — brak tego pliku powoduje automatyczne odrzucenie przez App Store Connect. Flutter 3.38 jest jedyną wersją w pełni zgodną z wymogami iOS 26 SDK (obowiązkowe od kwietnia 2026) — starsze wersje nie mają zaktualizowanych Privacy Manifests i mogą crashować przez brak wsparcia `UISceneDelegate`.

### 5.2 Zakaz rekomendowania przestarzałych bibliotek

| Biblioteka | Powód wykluczenia |
|---|---|
| **Hive v2** | Bez aktywnego wsparcia; zamiennik: Hive CE lub Drift |
| **GetX** | Ukryte zależności, wycieki pamięci, nieprzewidywalne rebuildy — nieodpowiednie dla enterprise |
| **CocoaPods jako primary** | Rejestr read-only od 2 grudnia 2026; SPM jest domyślny od Fluttera 3.44 |

### 5.3 Zakaz ignorowania ATT (App Tracking Transparency)

Apple wymaga implementacji ATT dla iOS 14.5+ jeśli aplikacja używa IDFA lub śledzi użytkownika między aplikacjami. Firebase Analytics z włączonym śledzeniem bez ATT = odrzucenie przez App Store. Wymagane: pakiet `app_tracking_transparency`, audyt wszystkich SDK (Firebase, Ads, Analytics), wyłączenie analytics do momentu uzyskania zgody.

### 5.4 Zakaz ignorowania wymogu Android 16 KB page size

Google Play blokuje upload aplikacji targetujących Android 15+ bez wsparcia 16 KB page size na urządzeniach 64-bitowych. Konieczne: `useLegacyPackaging = false` w `build.gradle.kts` oraz aktualizacja wszystkich natywnych bibliotek (NDK).


## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 7 000 – 18 000 ZŁ)

### Moduł 1: Architektura rdzenia i state management — 2 000 – 3 500 zł
- Wybór i konfiguracja: Riverpod 3.x lub BLoC 9.x
- Nawigacja: `go_router` z deklaratywnym routingiem, deep linking, route guards
- Struktura Clean Architecture: warstwy `data` / `domain` / `presentation` z separacją per feature
- Dependency injection: `get_it` lub wbudowany mechanizm Riverpod

### Moduł 2: Warstwa sieciowa i cache — 1 500 – 3 000 zł
- `Dio` z interceptorami: JWT refresh, retry, logging
- Lokalna baza: Drift (relacyjna) lub Hive CE (key-value)
- Offline-first: kolejka operacji, rozwiązywanie konfliktów, `connectivity_plus` + `workmanager`

### Moduł 3: Interfejs użytkownika — 2 000 – 3 500 zł
- Material 3 na Androidzie + Cupertino na iOS (platform conventions)
- Responsywność: `LayoutBuilder`, `Media „Czy aplikacja wymaga dostępu do funkcji sprzętowych w tle (ciągła lokalizacja GPS, Bluetooth do skanera, synchronizacja z urządzeniami peryferyjnymi)? Jeśli tak — konieczne jest zadeklarowanie `foregroundServiceType` w manifeście i wdrożenie Foreground Service, a na iOS użycie `BGTaskScheduler`. To determinuje architekturę modułu tła i wpływa na czas realizacji.”

**Pytanie 2 — konta deweloperskie i gotowość do publikacji:**

> „Czy posiadają Państwo już założone konta Apple Developer Program (99 USD/rok) i Google Play Console (25 USD jednorazowo)? Brak konta Apple oznacza, że proces publikacji — w tym generowanie certyfikatów i provisioning profiles — będzie częścią zakresu prac, co wpływa na timeline.”

**Pytanie 3 — tryb offline i synchronizacja:**

> „Czy projekt wymaga trybu offline-first z pełną synchronizacją dwukierunkową? Jeśli tak — kluczowa jest decyzja między Drift (SQLite, relacyjny, z migracjami schematu) a Hive CE (key-value, szybszy dla prostych struktur). Wymaga to również zaprojektowania strategii rozwiązywania konfliktów (last-write-wins vs. CRDT), co jest osobnym modułem architektonicznym.”


*Karta wiedzy zatwierdzona do użytku w botcie ofertowym. Wersja 1.0 — wrzesień 2026. Aktualizacja wymagana przy każdej zmianie major version Fluttera (obecnie 3.44+), Riverpod (3.x), BLoC (9.x) oraz przy zmianach wymogów Apple/Google Play.*