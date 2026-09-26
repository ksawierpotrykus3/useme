# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## TEMAT: SWIFT & iOS NATIVE — NOWOCZESNY SWIFTUI, STOREKIT 2, PRIVACY MANIFESTS I BACKGROUNDTASKS (STAN NA 2026)

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

**Typowe zlecenia w segmencie iOS Native (2026):**

| Kategoria zlecenia | Charakterystyka | Przedział budżetowy |
|---|---|---|
| Natywna aplikacja iPhone/iPad dla startupu | MVP + architektura skalowalna, SwiftUI + Swift 6, gotowość pod App Store | 12 000 – 22 000 zł |
| Wdrożenie monetyzacji StoreKit 2 / RevenueCat | Subskrypcje SaaS, paywalle, obsługa grace period, refundów, restore purchases | 6 000 – 14 000 zł |
| Naprawa odrzuconej aplikacji w App Store Review | Audyt kodu, Privacy Manifests, Guideline 3.1.1, 5.1.1 Privacy, 2.1 Completeness | 5 000 – 12 000 zł |
| Optymalizacja aplikacji pod iOS 17/18/26 | Migracja ObservableObject → @Observable, Swift 6 strict concurrency, SwiftData | 7 000 – 15 000 zł |
| Aplikacja B2B dla kadry zarządzającej | SSO, Keychain / Secure Enclave, SSL Pinning, raportowanie, offline-first | 15 000 – 22 000 zł |

**Profil klienta:**
- Founder startupu celujący w rynek US/UK (wysoka tolerancja na budżet, niska na opóźnienia).
- Software house bez kompetencji natywnych iOS szukający podwykonawcy architektonicznego.
- Firma logistyczno-przemysłowa wdrażająca aplikację wewnętrzną (B2B) — tu kluczowe są konta Enterprise, dystrybucja wewnętrzna, bezpieczeństwo danych.
- Zamożny klient biznesowy, który doświadczył już odrzucenia w App Store Review i szuka kogoś, kto rozumie wytyczne.

**Kontekst rynkowy:** Segment mobilny na Useme charakteryzuje się najwyższym współczynnikiem wygranych (Win Rate dla Kotlina: 27.3%, dla Fluttera: 20.0%), ponieważ próg wejścia odcina 90% amatorów. Elita wygrywa zlecenia za 4 000 – 18 000 zł, ponieważ otwiera problemem architektonicznym w pierwszych 2 zdaniach, zna aktualne realia systemowe na 2026 rok i rozbija wycenę na moduły architektoniczne.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1. Privacy Manifests — twarde wymogi App Store Review

Od 2024 roku Apple wymaga pliku `PrivacyInfo.xcprivacy` dla **każdej aplikacji i każdego biblioteki firm trzecich** (Third-Party SDKs). Brak ważnego manifestu — lub manifestu dla SDK, który używa flagowanych API — skutkuje **natychmiastowym odrzuceniem uploadu** w App Store Connect, z błędami typu `ITMS-91053`. Nie jest to ostrzeżenie — to twarda brama.

**Struktura `PrivacyInfo.xcprivacy` — cztery obowiązkowe klucze:**

1. `NSPrivacyTracking` (Boolean) — czy aplikacja śledzi użytkownika.
2. `NSPrivacyTrackingDomains` (Array) — domeny wykorzystywane do trackingu.
3. `NSPrivacyCollectedDataTypes` (Array) — deklaracja zbieranych danych.
4. `NSPrivacyAccessedAPITypes` (Array) — deklaracja API z „required reason”, wraz z kodem powodu. Kluczowe kategorie required reason API: File Timestamp (`C617.1`), System Boot Time (`35F9.1`), Disk Space (`85F4.1`), User Defaults (`CA92.1`), Active Keyboards (`3EC4.1`).

**Pozycja pliku:** W iOS/iPadOS/tvOS/visionOS/watchOS — katalog główny bundle aplikacji (obok `Info.plist`). W frameworkach — katalog główny frameworku. Dla Swift Packages — Xcode automatycznie umieszcza manifest w bundlu paczki.

**Najczęstsza przyczyna odrzucenia:** Manifesty SDK firm trzecich. Apple egzekwuje to od wiosny 2024 roku. Xcode agreguje wszystkie `PrivacyInfo.xcprivacy` w jeden raport prywatności i App Review weryfikuje, czy deklarowane użycie danych zgadza się z rzeczywistością. **SDK bez własnego, podpisanego manifestu = odrzucenie całej aplikacji.**

### 2.2. StoreKit 2 — jedyny standard monetyzacji w 2026

StoreKit 2 zastępuje StoreKit 1 i opiera się na Swift Concurrency (`async/await`, `Transaction.updates`, `Product.PurchaseResult`). **Kryptograficzna walidacja JWS (JSON Web Signature)** — zamiast parsowania paragonów base64 typu PKCS#7 — to standard walidacji transakcji.

**Architektura walidacji JWS:**
- Każda transakcja w StoreKit 2 jest podpisana przez Apple jako JWS.
- `VerificationResult.getJwsRepresentation()` zwraca podpisany token transakcji.
- Walidacja może odbywać się lokalnie (offline, z przypiętymi certyfikatami Apple) lub przez App Store Server API / Server Notifications.
- Eliminuje potrzebę własnego backendu walidującego stare paragony — choć dla subskrypcji SaaS nadal rekomendowane jest App Store Server API do zarządzania cyklem życia subskrypcji, grace period i refundów.

**Kluczowe elementy StoreKit 2 w 2026:**
- `Transaction.updates` — strumień asynchroniczny nasłuchujący zmian transakcji (odnowienia, anulacje, refundy).
- `Product.products(for:)` — asynchroniczne pobieranie produktów z App Store Connect.
- `Product.purchase()` — asynchroniczny zakup z obsługą `pending`, `success`, `userCancelled`.
- `AppStore.sync()` — synchronizacja transakcji (restore purchases).
- `Transaction.currentEntitlements` — bieżące uprawnienia użytkownika.

### 2.3. BackgroundTasks — ekstremalnie rygorystyczne ograniczenia iOS

System iOS **sam decyduje, KIEDY** da aplikacji czas procesora w tle — na podstawie nawyków użytkownika, poziomu naładowania baterii, stanu termicznego i priorytetu systemowego. Nie ma gwarancji częstotliwości ani czasu wykonania.

**Twarde limity na 2026:**

| Typ zadania | Limit czasu | Wyzwalacz | Wymagania |
|---|---|---|---|
| `BGAppRefreshTask` | **~30 sekund** | Opportunistyczny (system decyduje) | Brak wymogu zasilania |
| `BGProcessingTask` | **1–10 minut** (dynamicznie) | Urządzenie bezczynne | Opcjonalnie zewnętrzne zasilanie / sieć |
| `BGContinuedProcessingTask` (iOS 26+) | Minuty | Urządzenie bezczynne | Nowy typ z WWDC 2025 |

`BGAppRefreshTask` ma twardy limit ~30 sekund bez API rozszerzenia. `BGProcessingTask` jest dostosowywany dynamicznie na podstawie stanu baterii i termicznego — typowo 1–10 minut. **Ciągłe odpytywanie w tle (np. „pobieraj dane co 5 minut w nocy”) jest absolutnie niemożliwe** bez Silent Push Notification (APNs z flagą ` „Jeżeli planujesz monetyzację treści cyfrowych w aplikacji iOS, integracja Stripe/PayPal jest **wykluczona przez App Store Review Guideline 3.1.1** — każda subskrypcja SaaS musi przejść przez StoreKit 2 z walidacją JWS, w przeciwnym razie aplikacja zostanie odrzucona w Review z kodem 3.1.1 IAP Bypassing. Zanim przejdę do architektury, muszę zweryfikować czy Twój model biznesowy kwalifikuje się jako dobra cyfrowe (StoreKit 2) czy dobra fizyczne (płatności zewnętrzne dopuszczalne).”

**Otwarcie B (Privacy Manifests):**
> „Od 2024 roku Apple wymaga pliku `PrivacyInfo.xcprivacy` dla każdej aplikacji i **każdego SDK firm trzecich** — brak manifestu lub nieaktualny manifest SDK skutkuje odrzuceniem uploadu z błędem `ITMS-91053`. W praktyce 80% odrzuceń Privacy Manifests wynika z zaniedbanych SDK, nie z kodu aplikacji. Zanim oszacuję budżet, muszę sprawdzić, czy używasz bibliotek, które nie dostarczają podpisanych manifestów.”

**Otwarcie C (BackgroundTasks):**
> „Żądanie ‚pobierania danych co 5 minut w tle' jest na iOS niemożliwe do spełnienia w sposób gwarantowany — system iOS sam decyduje o czasie procesora dla `BGAppRefreshTask` (limit ~30s) i `BGProcessingTask` (1–10 min, tylko przy bezczynności i ładowaniu). Jedyne realne rozwiązanie to architektura oparta na Silent Push (APNs ` Czy posiadasz już zweryfikowane konto **Apple Developer Program dla organizacji** z numerem **D-U-N-S**? Proces uzyskania D-U-N-S i weryfikacji Apple trwa 2–4 tygodnie. Bez tego konta nie możemy opublikować aplikacji, nawet jeśli development zakończy się wcześniej. Jeżeli nie — rekomenduję rozpoczęcie procedury **natychmiast**, równolegle z pracami koncepcyjnymi.

**Pytanie 2 — Kwalifikacja dóbr:**
> Czy oferowane w aplikacji usługi/produkty kwalifikują się jako **dobra cyfrowe** podlegające StoreKit 2 (subskrypcje, odblokowanie funkcji, treści premium), czy jako **dobra fizyczne / usługi offline** (dopuszczalne płatności zewnętrzne zgodnie z Guideline 3.1.5)? Od tej kwalifikacji zależy cała architektura monetyzacji i czy integracja Stripe/PayPal jest w ogóle dopuszczalna.

**Pytanie 3 — Plan obsługi powiadomień w tle:**
> Jaki jest plan obsługi powiadomień w tle — **Silent Push (APNs z `content-available: 1`)** czy standardowy **`BGAppRefreshTask`**? Silent Push wymaga backendu wysyłającego push do APNs i jest jedynym sposobem na „częste” odświeżanie danych, ale nie gwarantuje dostarczenia. `BGAppRefreshTask` jest w pełni lokalny, ale system iOS decyduje o czasie uruchomienia. Od tej decyzji zależy architektura warstwy synchronizacji.

---

## 8. PODSUMOWANIE STRATEGICZNE DLA BOTA OFERTOWEGO

**Struktura oferty, która wygrywa:**

1. **Otwarcie problemem architektonicznym** (Privacy Manifests, Guideline 3.1.1, BackgroundTasks) — 2 zdania, które natychmiast dyskwalifikują amatorów.
2. **Pytania kwalifikujące** — umieścić w środku analizy, zmusić klienta do odpowiedzi na priv.
3. **Rozbicie modułowe** — 6 modułów z czasem i zakresem, nie ryczałt.
4. **Czerwone flagi** — pokazać, że rozumiemy ryzyko (Stripe dla dóbr cyfrowych = ban, „ciągłe tło” = niemożliwe, brak konta Apple = opóźnienie).
5. **Domknięcie techniczne** — Swift 6, @Observable, SwiftData, JWS, SSL Pinning — sygnały kompetencji.

**Czego nie robić:**
- Nie proponować spotkań wideo/telefonicznych — komunikacja wyłącznie pisemna na priv.
- Nie używać języka potocznego („no hej”, „w sumie”).
- Nie obiecywać funkcji, które są technicznie niemożliwe na iOS.
- Nie ignorować wymogów Apple dotyczących konta deweloperskiego i Privacy Manifests.