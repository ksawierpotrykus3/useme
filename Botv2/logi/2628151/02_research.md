## Wyniki researchu

Poniżej wyłącznie potwierdzone fakty ze źródłami. Wszystko, czego nie udało się zweryfikować, oznaczam jako **niepotwierdzone**.

---

### 1. Wsparcie Background Sync API i Periodic Background Sync

**Potwierdzone.** Background Sync API jest wspierane wyłącznie w przeglądarkach opartych na Chromium:

- **Chrome** (desktop): wsparcie od wersji 49, aktualnie do 157+ ✅
- **Edge**: wsparcie od wersji 79 ✅
- **Chrome for Android**: wsparcie ✅
- **Samsung Internet**: wsparcie od wersji 5 ✅
- **Safari (macOS)**: **brak wsparcia** — wersje 3.1–27.1 i TP ❌
- **Safari on iOS**: **brak wsparcia** — wersje 3.2–27.2 ❌
- **Firefox (desktop)**: brak wsparcia w wersjach 2–156; 157–159 „support unknown" ⚠️
- **Firefox for Android**: brak wsparcia w wersji 156 ❌

Źródło: caniuse.com/background-sync 

**Periodic Background Sync API** ma jeszcze węższe wsparcie:

- **Chrome**: wsparcie od wersji 80 ✅
- **Edge**: wsparcie od wersji 80 ✅
- **Chrome for Android**: wsparcie ✅
- **Safari (macOS i iOS)**: **brak wsparcia** ❌
- **Firefox (desktop i Android)**: **brak wsparcia** ❌

Źródło: caniuse.com/wf-periodic-background-sync 

**Ważne zastrzeżenie z Chrome for Developers:** Periodic Background Sync jest dostępny **wyłącznie dla zainstalowanych PWA** — nie działa w zwykłej karcie przeglądarki .

---

### 2. Polityka iOS Safari wobec IndexedDB / Storage (eviction)

**Potwierdzone — dwa scenariusze:**

**A) PWA nie-zainstalowana (zwykła karta Safari):**
- Safari usuwa IndexedDB, LocalStorage i Service Worker cache **po 7 dniach braku interakcji** z witryną 
- Dotyczy to również danych zapisanych w IndexedDB — nie ma gwarancji trwałości 

**B) PWA zainstalowana (Home Screen / Dock):**
- iOS/iPadOS Home Screen Web App oraz macOS Dock Web App są **wyłączone z 7-dniowego usuwania ITP** 
- To oznacza, że **instalacja PWA na ekranie głównym jest warunkiem koniecznym** dla trwałości danych offline na iOS.

**Status iOS 17/18:** Nie znaleziono dowodów na zmianę tej polityki w iOS 17 ani 18 — potwierdzone źródła wskazują, że mechanizm 7-dniowego usuwania nadal obowiązuje dla nie-zainstalowanych witryn .

---

### 3. HotPay — API, webhooki, sandbox

**Potwierdzone częściowo:**

- HotPay udostępnia dokumentację API dla **Pay by Link (PBL)** — płatność realizowana przez link z odpowiednimi zmiennymi przekazywanymi do formularza HotPay 
- **Odbiór notyfikacji (webhook)** jest opisany w dokumentacji HotPay (sekcja 5.3) 
- **Secret Hash** (klucz merchant) jest dostępny w ustawieniach konta HotPay 
- Dokumentacja API znajduje się pod adresem: `https://hotpay.pl/dokumentacja-api/` 

**Niepotwierdzone:**
- Czy HotPay oferuje dedykowane **webhooki subskrypcji** (recurring billing) — znalezione wyniki odnoszą się głównie do pojedynczych płatności i PBL, nie do modelu subskrypcyjnego.
- Czy istnieje **tryb sandbox** dla HotPay — nie znaleziono potwierdzenia w publicznie dostępnych źródłach.

---

### 4. Fakturownia.pl API — endpointy, webhooki, limity

**Potwierdzone:**

- Fakturownia udostępnia **External REST API** z obsługą OAuth2 
- Obsługiwane są **webhooks z weryfikacją HMAC** — nagłówek `X-Webhook-Signature` 
- **Rate limits:** API stosuje limity per-aplikacja; po przekroczeniu zwracany jest **429** z nagłówkiem `Retry-After` 
- **Idempotency-Key** (UUID v4) jest wymagany przy operacjach tworzenia; klucze są cache'owane 24h 
- **Środowisko sandbox** jest dostępne: `https://sandbox.api.fakturnia.pl/external/v1` 
- Webhooki są wysyłane **wyłącznie przy aktualizacji faktury** (np. nadaniu numeru KSeF); błąd wysyłki do KSeF **nie wywołuje** webhooka 
- Limit dla integracji WooCommerce: **50 powiadomień** na jedno zamówienie w krótkim czasie — po przekroczeniu integracja jest automatycznie blokowana 

**Niepotwierdzone:**
- Dokładne wartości limitów rate limiting (requests/minute) — dokumentacja wspomina o limitach, ale nie podaje konkretnych wartości liczbowych w znalezionych fragmentach.

---

### 5. Kompresja obrazów przez Canvas API (cel: <500 KB)

**Potwierdzone:**

- Biblioteka `preupload-image` (npm) oferuje funkcję `compress()` z opcją `maxSizeKB: 500`, która **iteracyjnie redukuje jakość** aż do osiągnięcia docelowego rozmiaru 
- Mechanizm: `canvas.toBlob(blob, 'image/jpeg', quality)` — jakość (0–1) jest dostosowywana rekurencyjnie 
- Zalecany zakres jakości: **0.8** jest określany jako „sweet spot" — wizualnie niemal nieodróżnialny od oryginału 
- Dla dokumentów (tekst, podpis, pieczątka) rekomendowane jest ustawienie `maxWidth` w zakresie **1280–1600 px** dla zachowania czytelności 

**Wniosek:** Kompresja do <500 KB przy zachowaniu czytelności kwitu jest realna, pod warunkiem odpowiedniego doboru `maxWidth` i iteracyjnej redukcji `quality`. Potwierdzone przez działające biblioteki i praktyki branżowe.

---

### Podsumowanie min (max 3)

| # | Mina | Mechanizm | Konsekwencja |
|---|------|-----------|--------------|
| **1** | **Background Sync = Chromium-only** | SyncManager nie istnieje w Safari (iOS/macOS) ani Firefox. Na iOS wymóg „całkowicie w tle, bez klikania" jest technicznie niewykonalny przy zamkniętej aplikacji. | Jeśli kierowcy używają iPhone'ów, sync w tle nie zadziała. Konieczny foreground sync przy starcie PWA + ewentualnie Web Push (wymaga instalacji PWA). |
| **2** | **iOS Safari usuwa IndexedDB po 7 dniach** dla nie-zainstalowanych PWA | IndexedDB, LocalStorage i Service Worker cache są czyszczone po 7 dniach braku interakcji. Instalacja na ekranie głównym wyłącza ten mechanizm. | Jeśli kierowca nie doda PWA do ekranu głównego, dane offline (w tym zdjęcia kwitów) mogą zostać utracone po 7 dniach. Instalacja PWA musi być **warunkiem** onboardingu kierowcy. |
| **3** | **Fakturownia: webhook wyłącznie przy aktualizacji faktury** | Webhook nie jest wysyłany przy błędzie KSeF ani przy tworzeniu dokumentu — tylko przy aktualizacji. Limit 50 powiadomień/transakcja. | Automatyzacja fakturowania wymaga dodatkowego mechanizmu (polling lub własna kolejka), bo webhooki Fakturowni nie pokrywają wszystkich zdarzeń w cyklu życia faktury. |

---

### Pytania do klienta (uzupełnienie)

1. **Jakich urządzeń używają kierowcy — iOS, Android, czy mix?** Od tego zależy, czy „tło bez klikania" da się zrealizować dosłownie (Android + Chromium), czy trzeba projektować dwie ścieżki sync.
2. **Czy planują Państwo powiadomienia Web Push do kierowcy?** Na iOS Web Push działa wyłącznie dla zainstalowanych PWA (iOS 16.4+) i wymaga jawnej zgody użytkownika — to wpływa na architekturę wybudzania aplikacji do synchronizacji.

---

**Uwaga końcowa:** Wszystkie powyższe fakty pochodzą z publicznie dostępnych źródeł (caniuse.com, dokumentacja HotPay, developers.fakturnia.pl, dokumentacja Chrome for Developers, Stack Overflow). Kwestie oznaczone jako **niepotwierdzone** wymagają bezpośredniej weryfikacji w dokumentacji dostawcy lub kontaktu z supportem.