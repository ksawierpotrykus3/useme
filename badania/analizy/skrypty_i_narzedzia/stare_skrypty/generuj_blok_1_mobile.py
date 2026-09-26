# -*- coding: utf-8 -*-
"""Generator kart wiedzy dla Bloku 1: Aplikacje Mobilne (Kotlin, Flutter, Swift).
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

SYSTEM_PROMPT = """Jesteś Głównym Architektem Aplikacji Mobilnych i Starszym Inżynierem Systemowym tworzącym elitarną bazę wiedzy dla bota ofertowego na platformie Useme / B2B.

KONTEKST I REALIA ZLECENIODAWCÓW (WYNIKI AUDYTU USEME - BLOK MOBILE):
- Segment mobilny charakteryzuje się najwyższym współczynnikiem wygranych (Win Rate dla Kotlina: 27.3%, dla Fluttera: 20.0%), ponieważ próg wejścia odcina 90% amatorów.
- Klienci to founderzy startupów, software house'y szukające wyspecjalizowanego dev-a oraz firmy logistyczno-przemysłowe (skanery, hardware, magazyn).
- Elita wygrywa zlecenia za 4 000 - 18 000 zł, ponieważ:
  1. OTWIERA PROBLEMEM ARCHITEKTONICZNYM W PIERWSZYCH 2 ZDANIACH (zamiast pisać o swoim doświadczeniu, uderza w restrykcje systemowe Google Play / Apple App Store, ubijanie procesów w tle czy zarządzanie pamięcią).
  2. ZNA AKTUALNE REALIA SYSTEMOWE NA 2026 ROK (Android 14/15/16 foreground service types, 16 KB page size support, Apple Privacy Manifests, StoreKit 2, Impeller rendering engine).
  3. ZADAJE 2-3 CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODKU ANALIZY (zmusza klienta do natychmiastowego odpisania na priv).
  4. WSKAZUJE ANTYWZORCE I CZERWONE FLAGI (np. obietnice ciągłego GPS w tle bez Foreground Service, ignorowanie specyfiki producentów OEM np. Xiaomi/Samsung battery killers, hybrydowe webview udające natywną apkę).
  5. ROZBIJA WYCENĘ NA LOGICZNE MODUŁY ARCHITEKTONICZNE (nie ryczałt).

ZASADY TREŚCI:
- Zero udawania mowy ludzkiej ("no hej", "w sumie", sztuczne idiomy).
- Zero proponowania spotkań wideo, Google Meet czy rozmów telefonicznych (komunikacja wyłącznie pisemna na priv).
- Twarde, zweryfikowane fakty inżynierskie, zaktualizowane pod kątem 2026 roku.
- Język: Polski, wysoce precyzyjny, inżynierski.
"""

TASKS = [
    {
        "id": "tech_05_kotlin_android_native",
        "nazwa": "Kotlin & Android Native (Background Services, Hardware BLE, Android 14/15 Restrykcje)",
        "plik": OUTPUT_DIR / "tech_05_kotlin_android_native.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Kotlin & Android Native — Architektura Usług w Tle (WorkManager, Foreground Service), Integracje ze Sprzętem (Bluetooth BLE, Skanery Kodów Zebra/Honeywell) i Wymogi Google Play 2026**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić najnowsze restrykcje systemowe Androida 14 i 15 (np. Foreground Service Types, polityka uprawnień `FOREGROUND_SERVICE_LOCATION`, wymóg wsparcia stron pamięci 16 KB od 2025/2026 roku w Google Play).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: aplikacje logistyczne/magazynowe na terminale przemysłowe, aplikacje telemetryczne/IoT łączące się przez Bluetooth BLE, natywne moduły hardware, refaktoryzacja legacy Java -> Kotlin.
   - Budżety: 4 500 – 18 000 zł. Profil klienta: kierownik operacji/logistyki, startup IoT, software house z brakiem natywnego Android dev-a.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Restrykcje systemowe procesów w tle: Android 14/15 wymusza deklarację konkretnego typu `foregroundServiceType` w manifeście (np. `location`, `connectedDevice`, `dataSync`) z twardym uzasadnieniem dla Google Play Console; brak uzasadnienia = odrzucenie aktualizacji.
   - Doze Mode, App Standby Buckets i agresywne zabijanie procesów przez nakładki OEM (MIUI/HyperOS, OneUI, ColorOS - DontKillMyApp).
   - Wymóg wsparcia rozmiaru stron pamięci 16 KB (16 KB page size alignment w NDK / bibliotekach C++) wprowadzany przez Google Play.
   - Bluetooth Low Energy (BLE): Praca z GATT Server/Client, obsługa MTU negotiation, obsługa reconnections, ograniczenia skanowania w tle bez lokalizacji (`BLUETOOTH_SCAN` z flagą `neverForLocation`).
   - Nowoczesny stack: Kotlin Coroutines + Flow, Jetpack Compose, Room (KSP), Hilt / Koin, WorkManager (dla zadań odroczonych) vs Foreground Service (dla zadań natychmiastowych użytkownika).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebujemy prostej aplikacji, która w tle co 10 sekund sprawdza pozycję GPS pracownika/kierowcy i wysyła na serwer".
   - Co go utopi: System Android ubije standardowy serwis po 1-3 minutach od wygaszenia ekranu. Użycie ciągłego GPS wyczerpie baterię w 4 godziny. Brak trwałego powiadomienia (Notification) i uprawnienia `ACCESS_BACKGROUND_LOCATION` (które wymaga osobnego formularza weryfikacji w Google Play pod rygorem usunięcia konta dewelopera).
   - Mina terminali Zebra/Honeywell: Próba czytania kodów kreskowych przez aparat fotograficzny zamiast integracji z natywnym SDK skanera (Zebra EMDK / DataWedge Intents) powoduje opóźnienie 2 sekundy na skan zamiast 50ms i bunt magazynierów.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia uderzające prosto w mechanikę `foregroundServiceType`, politykę baterii OEM i weryfikację uprawnień w Google Play.
   - Wskazanie natychmiastowego rozwiązania: wykorzystanie DataWedge API dla terminali lub optymalizacja fused location provider z geofencingiem zamiast ciągłego pollingu.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz obiecywania "niewidocznego śledzenia w tle bez powiadomienia na pasku" (technicznie niemożliwe od Androida 8+, próby obejścia grożą natychmiastowym banem konta dewelopera w Google Play).
   - Zakaz ignorowania specyfiki nakładek chińskich producentów (Xiaomi/Huawei) i braku instrukcji dla użytkownika o wyłączeniu optymalizacji baterii.
   - Zakaz pisania o WebView jako rozwiązaniu dla aplikacji wymagającej intensywnej komunikacji z Bluetooth/hardware.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 6 000 – 16 000 ZŁ):
   - Moduły: 1. Warstwa komunikacji hardware (GATT Client / Zebra DataWedge Broadcast Receiver); 2. Silnik usług tła (Foreground Service + Notification Channel + WorkManager fallback); 3. Lokalna baza danych offline-first (Room z szyfrowaniem SQLCipher); 4. Interfejs użytkownika Jetpack Compose; 5. Moduł synchronizacji z API backendu (Retrofit/Ktor + exponential retry); 6. Przygotowanie do publikacji w Google Play (zgodność z Android 14/15, deklaracje uprawnień).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy aplikacja ma działać na dedykowanych terminalach magazynowych z Androidem czy prywatnych telefonach kierowców BYOD; jaki jest akceptowalny interwał raportowania pozycji; czy aplikacja będzie dystrybuowana przez Google Play czy wewnętrznie jako APK/MDM).
"""
    },
    {
        "id": "tech_06_flutter_dart",
        "nazwa": "Flutter & Dart (BLoC/Riverpod, Cross-Platform, Impeller, Platform Channels)",
        "plik": OUTPUT_DIR / "tech_06_flutter_dart.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Flutter & Dart — Architektura Aplikacji Wieloplatformowych (iOS + Android), Silnik Renderowania Impeller, Zarządzanie Stanem (BLoC / Riverpod) i Obsługa Natywnych Platform Channels**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić najnowszy stan ekosystemu Fluttera w 2026 roku (silnik Impeller na iOS i Androidzie, wsparcie Swift Package Manager w toolchainie Fluttera, migracja z Hive na Isar / Drift, zarządzanie pamięcią w Dart 3.x).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: budowa MVP dla startupu na obie platformy (iOS/Android) z jednego kodu, aplikacje e-commerce/B2B z płatnościami i katalogiem produktów, przepisanie starej aplikacji hybrydowej (Ionic/Cordova) na Fluttera.
   - Budżety: 5 000 – 20 000 zł. Profil klienta: founder startupu z ograniczonym budżetem na 2 osobne zespoły (iOS/Android), agencja interaktywna.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Silnik renderowania: Impeller jako domyślny backend renderujący (wyeliminowanie problemu shader compilation jank obecnego w starym Skia).
   - Toolchain i integracja natywna: Przejście ekosystemu iOS na Swift Package Manager (SPM) w miejsce CocoaPods; MethodChannel i FFI (Foreign Function Interface) do bezpośredniego wywoływania kodu C++/Rust.
   - Zarządzanie stanem: BLoC (dla dużych projektów korporacyjnych o rygorystycznej strukturze zdarzeń) vs Riverpod (dla nowoczesnych, elastycznych aplikacji z compile-time safety).
   - Architektura Offline-First i lokalny cache: Drift (relacyjny SQLite ze sprawdzaniem typów w kompilacji) lub Isar (błyskawiczna baza NoSQL) zamiast przestarzałego Hive.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Chcemy jedną aplikację na iOS i Androida, która będzie identyczna i będzie działać idealnie w tle".
   - Co go utopi: Złudzenie 100% współdzielonego kodu — funkcje systemowe (kamery, powiadomienia push APNs vs FCM, deep linking / Universal Links vs App Links, uprawnienia w tle) ZAWSZE wymagają konfiguracji natywnej per platforma.
   - Mina wydajnościowa: Przebudowywanie całego drzewa widżetów (`setState` na szczycie hierarchii) powodujące drop klatek z 120 FPS do 20 FPS przy przewijaniu długich list; nieprawidłowe zarządzanie kontrolerami (TextEditingController / AnimationController) powodujące memory leaki.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia inżynierskie deklasujące oferty ze sztampowym "zrobię tanią apkę we Flutterze".
   - Wskazanie na konieczność rozdzielenia logiki biznesowej od warstwy widżetów (Clean Architecture / BLoC) oraz precyzyjne zaadresowanie różnic w cyklu życia aplikacji na iOS (background fetch) vs Android (WorkManager).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz obiecywania "zerowego dotykania kodu natywnego" – profesjonalista wie, że pliki `Info.plist`, `Podfile`, `build.gradle.kts` i `AndroidManifest.xml` muszą być skonfigurowane ręcznie pod wymogi sklepów.
   - Zakaz pisania o przestarzałych bibliotekach (np. Hive v2 bez wsparcia, GetX w projektach enterprise ze względu na ukryte zależności i wycieki pamięci).
   - Zakaz ignorowania wymogu Apple Privacy Manifests i zasad App Store dotyczących zgód na śledzenie (ATT - App Tracking Transparency).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 7 000 – 18 000 ZŁ):
   - Moduły: 1. Architektura rdzenia i state management (Riverpod/BLoC + nawigacja go_router); 2. Warstwa sieciowa i cache (Dio + interceptory tokenów JWT + Drift/Isar); 3. Interfejs użytkownika z obsługą platform conventions (Material 3 + Cupertino); 4. Integracja platformowa (Push notifications FCM/APNs + uprawnienia systemowe); 5. Płatności i analityka (In-App Purchases / RevenueCat / Stripe); 6. Testy i proces publikacji (Fastlane, CI/CD, deployment do TestFlight i Google Play Internal).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy aplikacja wymaga zaawansowanych funkcji sprzętowych w tle; czy posiadają już założone konta deweloperskie Apple Developer Program i Google Play Console; czy projekt wymaga trybu offline-first z pełną synchronizacją dwukierunkową).
"""
    },
    {
        "id": "tech_07_swift_ios_native",
        "nazwa": "Swift & iOS Native (SwiftUI, StoreKit 2, Privacy Manifests, BackgroundTasks)",
        "plik": OUTPUT_DIR / "tech_07_swift_ios_native.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Swift & iOS Native — Nowoczesny SwiftUI, Subskrypcje StoreKit 2, Wymogi Apple Privacy Manifests i Zadania w Tle (BackgroundTasks)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić wymogi Apple na 2026 rok (obowiązkowe Privacy Manifests `PrivacyInfo.xcprivacy`, StoreKit 2 jako jedyny standard dla in-app purchases, restrykcje BGAppRefreshTask i BGProcessingTask w iOS 17/18).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: natywna aplikacja na iPhone/iPad dla startupu, wdrożenie płatności i subskrypcji w modelu SaaS (StoreKit 2 / RevenueCat), naprawa odrzuconej aplikacji w procesie App Store Review, optymalizacja aplikacji pod iOS 17/18.
   - Budżety: 5 000 – 22 000 zł. Profil klienta: zamożny klient biznesowy, startup celujący w rynek US/UK, firma wdrażająca aplikację dla kadry zarządzającej.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Wymogi App Store Review: Obowiązkowe Privacy Manifests (`PrivacyInfo.xcprivacy`) dla aplikacji i wszystkich bibliotek firm trzecich (Third-Party SDKs); brak sygnatury = natychmiastowe odrzucenie w App Store Connect.
   - Płatności i subskrypcje: Nowy standard **StoreKit 2** (zastępuje stary StoreKit 1) oparty na Swift Concurrency (`async/await`, `Transaction.updates`, kryptograficzna walidacja JWS po stronie Apple bez potrzeby własnego backendu walidującego stare paragony base64).
   - Usługi w tle na iOS: Ekstremalnie rygorystyczny `BackgroundTasks` framework (`BGAppRefreshTask`, `BGProcessingTask`). System iOS sam decyduje, KIEDY da aplikacji czas procesora (na podstawie nawyków użytkownika i poziomu naładowania baterii).
   - Nowoczesny stack: Swift 6 (strict concurrency checking, Data-race safety, Actors), SwiftUI (nowy makro `@Observable` zastępujący stary `ObservableObject`), SwiftData jako następca CoreData, Keychain / Secure Enclave dla wrażliwych tokenów.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję prostej aplikacji na iPhone'a ze subskrypcją 29 zł/mies. i integracją z płatnościami Stripe".
   - Co go utopi (Mina Apple Tax 30%): Złamanie wytycznych App Store Guideline 3.1.1 — próba użycia Stripe do odblokowania cyfrowych treści w aplikacji kończy się natychmiastowym banem i odrzuceniem w Review. Płatności za treści cyfrowe MUSZĄ iść przez Apple In-App Purchase (StoreKit).
   - Mina synchronizacji w tle: Klient żąda "aplikacja musi pobierać dane co 5 minut w nocy". Na iOS jest to absolutnie niemożliwe bez Silent Push Notification (APNs z flagą `content-available: 1`).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia inżynierskie uderzające w zgodność ze StoreKit 2 / App Store Review Guidelines 3.1.1 oraz wymogi Privacy Manifests.
   - Wskazanie na architekturę walidacji transakcji JWS (JSON Web Signature) eliminującą oszustwa i nieaktualne paragony.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz proponowania płatności zewnętrznych (Stripe/PayPal) dla dóbr cyfrowych w aplikacji iOS.
   - Zakaz obiecywania "stałego działania w tle" bez wykorzystania dedykowanych trybów Background Modes (VoIP, Audio, Navigation) dopuszczonych przez Apple.
   - Zakaz ignorowania konta Apple Developer (klient musi posiadać konto firmowe Apple D-U-N-S, co trwa od 2 do 4 tygodni).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 7 000 – 20 000 ZŁ):
   - Moduły: 1. Architektura aplikacji SwiftUI + wzorzec MVVM / @Observable + Swift 6 concurrency; 2. Integracja monetyzacji StoreKit 2 (subskrypcje, paywalle, restore purchases, obsługa grace period i refundów); 3. Bezpieczna persystencja danych (SwiftData + Keychain wrapper); 4. Warstwa sieciowa z walidacją certyfikatów SSL Pinning; 5. Push Notifications (APNs background processing); 6. Przygotowanie do publikacji w App Store Connect (Privacy Manifests, metadata, screenshots, review support).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy klient posiada już zweryfikowane konto Apple Developer Program z numerem D-U-N-S; czy oferowane usługi/produkty kwalifikują się jako dobra cyfrowe podlegające StoreKit 2 czy dobra fizyczne; jaki jest plan obsługi powiadomień w tle - Silent Push czy standardowy BGAppRefresh).
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
    print("=== Generator Kart Wiedzy Bloku 1: Mobile (Kotlin, Flutter, Swift) ===")
    sukcesy = 0
    for zadanie in TASKS:
        ok = wykonaj_zadanie(zadanie)
        if ok:
            sukcesy += 1
        time.sleep(2)
        
    print(f"\n=======================================================")
    print(f"[KONIEC] Pomyślnie ukończono {sukcesy}/{len(TASKS)} kart technologicznych dla Bloku Mobile!")

if __name__ == "__main__":
    main()
