# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## TEMAT: Web Scraping, Boty Ekstrakcyjne i Zaawansowane Omijanie Systemów Anty-Botowych (Cloudflare Turnstile, DataDome, Akamai, sygnatury TLS JA4)

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

### 1.1 Typy zleceń (realne, powtarzalne)

| Typ zlecenia | Opis techniczny | Częstotliwość na Useme |
|---|---|---|
| **Monitoring cen konkurencji** | Ekstrakcja cen, stanów magazynowych, czasów dostawy z 3–15 domen e-commerce; porównanie z własnym cennikiem; alerty przy zmianie > X% | Bardzo wysoka |
| **Boty na portale ogłoszeniowe** | OLX, OtoMoto, Otodom, Allegro Lokalnie: scraping ofert z filtrami (marka, rocznik, cena, region), deduplikacja, wykrywanie nowych ofert | Wysoka |
| **Agregatory e-commerce** | Ceneo, Skąpiec, Google Shopping: mapowanie EAN/SKU, ekstrakcja parametrów, normalizacja nazw producentów | Średnia |
| **Ekstrakcja baz leadów B2B** | Rejestry firm (KRS, CEIDG, REGON), portale branżowe, LinkedIn (publiczne profile), Google Maps: nazwa, NIP, adres, e-mail, telefon, strona www | Wysoka |

### 1.2 Realne widełki budżetowe (2026)

- **1 500 – 2 500 zł**: prosty scraper jednej domeny bez WAF (statyczny HTML/JSON API), eksport do CSV/Excel. Czas: 3–5 dni.
- **2 500 – 4 500 zł**: 3–7 domen, część za Cloudflare/DataDome, rotacja proxy, normalizacja danych, prosty panel/CLI, harmonogram.
- **4 500 – 8 500 zł**: 10+ domen, WAF enterprise (Akamai BMP, Kasada), reverse-engineering API mobilnego, architektura kolejkowa, baza danych, monitoring i alerty, pipeline eksportu.

### 1.3 Profil klienta

- **Właściciel e-commerce** (60%): chce monitorować ceny konkurencji, często nie rozumie różnicy między proxy datacenter a rezydencjalnym.
- **Startup / analityk rynku** (30%): potrzebuje danych do modelu cenowego lub raportu; oczekuje danych w formacie Parquet/JSON.
- **Agencja marketingowa / leadgen** (10%): ekstrakcja baz leadów, często bez świadomości RODO i regulaminów serwisów.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1 Zabezpieczenia: Cloudflare Turnstile

Cloudflare Turnstile to następca reCAPTCHA — niewidzialny challenge, który weryfikuje przeglądarkę na podstawie:
- **IP reputation**: datacenter IP (AWS, Hetzner, OVH) są natychmiast flagowane; rezydencjalne i mobilne przechodzą.
- **TLS fingerprint**: nieprawidłowy JA3/JA4 handshake = blokada przed wykonaniem JS.
- **JavaScript execution**: Turnstile wymaga wykonania kodu, który generuje `cf_clearance` cookie.
- **Browser fingerprint**: Canvas, WebGL, AudioContext, `navigator.webdriver`.

**Stan na 2026**: Cloudflare obsługuje ok. 22% wszystkich stron internetowych. Prosty `requests` + user-agent = 403 Forbidden lub nieskończona pętla „Checking your browser…”. Skuteczne podejścia: `curl_cffi` z TLS spoofingiem (dla endpointów API bez JS challenge) oraz stealth browser (Camoufox, nodriver) dla stron z Turnstile.

### 2.2 Zabezpieczenia: DataDome

DataDome ocenia każde żądanie na podstawie **kilkudziesięciu sygnałów jednocześnie**: TLS handshake, IP, nagłówki HTTP, JavaScript, zachowanie użytkownika. Werdykt zapada w milisekundach — nie ma jednego „złego sygnału”, który można naprawić.

- **Block page**: HTTP 403 z `x-datadome: protected`, ciało zawiera `captcha-delivery.com` i `datadome` cookie.
- **Skala**: DataDome przetwarza > 5 bilionów sygnałów dziennie; model ML retrenowany ciągle.
- **Bypass**: rezydencjalne/mobilne proxy jest **obowiązkowe** — datacenter IP są flagowane przy pierwszym żądaniu. Bez tego nawet idealny browser fingerprint nie pomoże.

### 2.3 Zabezpieczenia: Kasada

Kasada stosuje **proof-of-work (POW)** oraz payload generation (CT/CD tokens). Wymaga wykonania JavaScript, który rozwiązuje challenge kryptograficzny. Rozwiązania: dedykowane SDK (Hyper Solutions, Salamoonder) generujące poprawne payloady bez przeglądarki.

### 2.4 Zabezpieczenia: Akamai Bot Manager (BMP)

Akamai BMP to najbardziej złożony system, łączący:
- **JA3/JA4 TLS fingerprinting**
- **HTTP/2 SETTINGS frame fingerprinting** — unikalny „Akamai hash” (`akamai_hash`, `akamai_text`) oparty na kolejności i wartościach ramek SETTINGS.
- **Sensor data** — zaszyfrowany payload generowany przez `sensor.js`, zawierający informacje o środowisku przeglądarki.
- **SBSD challenge** — wymaga wygenerowania poprawnego sensor data.

**Krytyczne**: Chrome 130+ wprowadził nowe ustawienie HTTP/2, którego brak w emulacji powoduje natychmiastową detekcję przez Akamai.

### 2.5 Detekcja na poziomie sieci

#### TLS Fingerprinting (JA3 / JA4)

- **JA3**: hash MD5 z ClientHello (TLS version, cipher suites, extensions, elliptic curves, EC point formats). Python `requests`/`urllib3` mają JA3 zupełnie różny od Chrome/Firefox — to pierwszy sygnał blokady.
- **JA4**: następca JA3, bardziej odporny na „repackaging”. `curl_cffi` implementuje natywny JA3/JA4 spoofing poprzez `curl-impersonate` — generuje ClientHello identyczny z Chrome/Firefox.
- **HTTP/2 fingerprinting**: kolejność pseudo-nagłówków (`:method`, `: „Potrzebuję prostego skryptu w Pythonie do pobierania 50k produktów dziennie z 5 sklepów internetowych. Budżet: 2000 zł.”

**Co jest miną:**

1. **Rotacja selektorów frontendowych**: strony e-commerce przebudowują DOM co 2–4 tygodnie (Next.js, React Server Components). Selektory CSS/X „Zanim uruchomisz jakikolwiek headless browser: ta platforma ma prywatne API GraphQL w aplikacji mobilnej. 50 000 rekordów przez `/graphql` z `operationName: searchProducts` to 1/20 kosztu renderowania HTML — bez proxy rezydencjalnego, bez Cloudflare Turnstile, bo endpoint mobilny nie jest chroniony.”

**Wariant B — dla stron z Cloudflare/DataDome:**
> „Cloudflare Turnstile blokuje `requests` na poziomie TLS ClientHello, zanim wyśle pierwszy bajt HTTP. Zanim wydasz budżet na Selenium: sprawdźmy, czy istnieje endpoint REST/PWA z danymi hydratacji (`__NEXT_DATA__`, `window.__APOLLO_STATE__`) — wtedy `curl_cffi` z JA4 spoofingiem wystarczy.”

**Wariant C — dla OLX/OtoMoto:**
> „OLX ma jawne API mobilne (`api.olx.pl`), ale wymaga tokenu OAuth z aplikacji. Reverse-engineering APK przez `jadx` + `mitmproxy` daje dostęp do endpointu, który zwraca JSON — bez renderowania HTML, bez walki z DOM, 10× szybciej.”

### 4.2 Technika reverse-engineeringu prywatnych endpointów

1. **Decompilacja APK**: `jadx` / `apktool` → szukaj `Retrofit`, `OkHttp`, `GraphQL/Apollo`, `baseUrl`, `authHeaders`.
2. **Przechwycenie ruchu**: `mitmproxy` + certyfikat systemowy (Android 14+ wymaga roota lub Frida do obejścia certificate pinning).
3. **Identyfikacja endpointu**: jeśli GraphQL — wyślij introspection  budżetu), degradacji selektorów i memory leaków.

❌ **„Zrobimy to bez proxy”** — datacenter IP jest flagowane przy pierwszym żądaniu przez Cloudflare/DataDome.

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 000 – 8 000 ZŁ)

### 6.1 Architektura produkcyjna

```
[Źródła zadań: harmonogram / API / plik CSV]
        ↓
[Kolejka zadań: Celery + Redis]
        ↓
[Warstwa pobierania]
  ├── curl_cffi (API/JSON endpoints) — 15–30 MB RAM/proces
  ├── nodriver / Camoufox (strony z JS challenge) — 200–600 MB RAM/instancja
  └── Proxy pool: rezydencjalne (rotacja per sesja) + mobilne (dla DataDome)
        ↓
[Walidator danych: Pydantic v2]
  ├── Schemat produktu: id, nazwa, cena, stan, url
  ├── Normalizacja: waluta, jednostki, kodowanie
  └── Deduplikacja: hash treści / id źródłowy
        ↓
[Magazyn danych]
  ├── PostgreSQL — dane transakcyjne, relacje
  ├── ClickHouse — analityka, agregacje, monitoring cen w czasie
  └── S3 / MinIO — surowe odpowiedzi (raw payloads) do audytu
        ↓
[Monitoring i alerty]
  ├── Prometheus + Grafana: zużycie RAM, czas odpowiedzi, success rate
  ├── Alerty: spadek success rate < 90%, wzrost RAM > 80%
  └── Retry policy: exponential backoff z jitter, max 3 próby
```

### 6.2 Rozbicie modułowe i wycena

| Moduł | Zakres | Czas | Wycena |
|---|---|---|---|
| **1. Analiza anty-bot i reverse-engineering API** | Identyfikacja endpointów (REST/GraphQL), test JA3/JA4, analiza challengey, wybór strategii | 1–2 dni | 800–1 200 zł |
| **2. Moduł rotacji sesji i proxy** | Integracja proxy rezydencjalnych/mobilnych, rotacja per sesja, monitoring zużycia GB, filtrowanie assetów | 1 dzień | 600–1 000 zł |
| **3. Silnik parsowania i normalizacji** | Pydantic schemas, normalizacja danych, deduplikacja, obsługa błędów parsowania | 1–2 dni | 800–1 500 zł |
| **4. Baza danych i pipeline eksportu** | PostgreSQL/ClickHouse, eksport CSV/Parquet/JSON, API do odczytu danych | 1–2 dni | 800–1 500 zł |
| **5. Monitoring, alerty i retry policy** | Prometheus/Grafana, alerty RAM/success rate, exponential backoff | 1 dzień | 600–1 000 zł |
| **Razem** | | **5–8 dni** | **4 000–8 500 zł** |

**Dodatkowe koszty operacyjne** (poza wyceną): proxy rezydencjalne $1–$15/GB, serwer VPS z 8–16 GB RAM (~200–400 zł/mies.), ewentualnie API do rozwiązywania CAPTCHA ($1–$3 za 1000 rozwiązań).

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU)

Poniższe pytania są zaprojektowane tak, aby zleceniodawca **musiał odpowiedzieć na priv** — każde wymaga informacji, której nie ma w opisie zlecenia:

1. **„Jaka jest wymagana częstotliwość odświeżania danych? Raz na dobę czy co godzinę?”**
   → Determinuje architekturę: jednorazowy batch vs. ciągły pipeline z kolejką. Częstotliwość co godzinę wymaga 24× więcej sesji proxy i może zwielokrotnić koszty.

2. **„Czy dane docelowe mają być w formacie CSV, JSON czy zapisywane bezpośrednio do Państwa bazy danych (PostgreSQL/BigQuery)?”**
   → Determinuje moduł eksportu i ewentualną integrację z istniejącym systemem.

3. **„Czy akceptują Państwo koszty proxy rezydencjalnych w wysokości $X–$Y miesięcznie, czy budżet na infrastrukturę jest oddzielony od wynagrodzenia?”**
   → Ujawnia, czy klient rozumie, że proxy to koszt operacyjny, a nie część stawki. Jeśli budżet jest „wszystko w cenie” — zlecenie jest nierentowne przy WAF enterprise.

---

## PODSUMOWANIE DLA BOTA OFERTOWEGO

**Schemat oferty w 3 akapitach:**

1. **Otwarcie problemem (2 zdania)**: wskaż konkretny mechanizm anty-botowy, który klient prawdopodobnie zignorował (TLS JA4, HTTP/2 SETTINGS, reverse-engineering API mobilnego).
2. **Analiza z 2–3 pytaniami kwalifikującymi**: wpleć pytania o częstotliwość, format docelowy i budżet na proxy — zmusza do odpowiedzi na priv.
3. **Rozbicie modułowe z wyceną**: pokaż, że 4 000–8 000 zł to nie „ryczałt za skrypt”, lecz architektura z kolejką, walidacją, monitoringiem i retry policy.

**Czerwone flagi do wytykania w ofercie:** BeautifulSoup na Cloudflare, brak rotacji proxy, brak memory management dla Chromium, obietnica „100% niewykrywalności”.