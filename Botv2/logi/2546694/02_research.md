## Research: kanał dostępu do APK i formaty paczek (bez nazwy serwera)

### 1. Google Play

**Kanał dostępu:** Brak publicznego API do pobierania APK. Wszystkie istniejące biblioteki są nieoficjalne i wymagają uwierzytelnienia konta Google (OAuth → token AAS).

- `playfast` (PyPI): „APK Download (NEW!) – Direct Download: Download APKs directly from Google Play Store – Smart Authentication: OAuth → AAS token exchange with auto-retry”
- `google-play` (GitHub): „download APK from Google Play or send API requests… sign in with your Google Account. then get authorization code (`oauth_token`) cookie from browser storage”
- `googleplay-python` (PyPI): „unofficial library for Google Play workflows that are not covered by the public Play Developer APIs… authenticated APK and OBB delivery”

**Format zwracany:** Split APK (nie pełny APK). „Google Play delivers apps as split APK bundles behind the scenes”.

**Dlaczego groźne:**  
- Wymaga konta Google, tokeny wygasają, endpointy są prywatne i mogą się zmienić w każdej chwili („Private Google Play endpoints can change without notice”).  
- ToS Google Play prawdopodobnie zabrania scrapingu – **niepotwierdzone bezpośrednim cytatem**, ale wszystkie narzędzia działają w szarej strefie („software is not licensed for commercial use”).  
- Split APK oznacza, że nie ma jednego pliku do analizy – trzeba scalać paczki per konfiguracja urządzenia.

### 2. APKPure

**Kanał dostępu:** API + scraping, oba nieoficjalne, ale działające publicznie.

- `apkpureSkills` (GitHub): „dual-mode (API + scraping), proxy auto-detected”  
- `apkscraper` (PyPI): „Concurrently scrapes and dedupes version histories from APKPure, Uptodown, and APKMirror APIs”

**Format zwracany:** APK **lub** XAPK.  
- XAPK to format APKPure: „XAPK (.xapk) is APKPure's archive format. Under the hood it is a ZIP that contains a base APK, usually a set of Split APKs, and almost always the app's OBB data files”.

**Dlaczego groźne:**  
- XAPK to ZIP, nie pojedynczy APK – trzeba go rozpakować, a w środku mogą być kolejne split APK i pliki OBB.  
- Dostępność zależy od regionu i polityki anti-scraping (proxy auto-detected sugeruje blokady).

### 3. APKMirror

**Kanał dostępu:** API + scraping, nieoficjalne.

- `apkmirror-downloader` (npm): „APKMD is a CLI tool that allows you to download APKs from Apkmirror… Supported types are 'apk' and 'bundle'”  
- `gh-apkmirror-dl` (GitHub): „bundle: (Optional) Whether to use the app bundle instead of the APK file, defaults to `true`”  
- `apkscraper`: wymienia APKMirror APIs jako źródło

**Format zwracany:** APK **lub** APKM (bundle).  
- APKM to format APKMirror: „APKM (.apkm) is APKMirror's equivalent of an AAB split bundle. Internally it is a ZIP of one base APK plus configuration splits (per CPU ABI, per screen density, per language)”.

**Dlaczego groźne:**  
- Rate limiting przez Cloudflare: „Sometimes, download can fail at random. This is most likely due to rate limit protection by APKMirror using Cloudflare”.  
- Domyślnie zwraca bundle (APKM), nie APK – wymaga rekurencyjnego rozpakowania.

### 4. Formaty paczek – porównanie

| Format | Co zawiera | Kto produkuje | Uwagi |
|---|---|---|---|
| **APK** | Pojedynczy instalowalny pakiet | Dowolny build toolchain | 10–100 MB |
| **XAPK** | APK + OBB + opcjonalne split APK, w ZIP | APKPure | 40 MB – 2 GB |
| **APKM** | Base APK + split APK (ABI, DPI, język), w ZIP | APKMirror | 20–500 MB |
| **APKS** | Split APK z AAB, w ZIP | SAI, bundletool | 20–500 MB |
| **AAB** | Nie jest instalowalny bezpośrednio; Google Play konwertuje na split APK | Google Play | – |

### 5. Wnioski dla oferty (GDZIE i DLACZEGO groźne)

1. **Bez nazwy serwera nie da się określić kanału dostępu.** Trzy główne serwery mają różne mechanizmy i różne ryzyka.
2. **Google Play = największe ryzyko.** Brak publicznego API, wymóg konta Google, prywatne endpointy, ToS. Format split APK komplikuje analizę. Projekt jako „scraper” może być niewykonalny bez obejść.
3. **APKPure i APKMirror = wykonalne, ale niestabilne.** API nieoficjalne, scraping podatny na blokady (Cloudflare, rate limit). Format XAPK/APKM to ZIP – konieczne rekurencyjne rozpakowanie.
4. **„Wszystkie wewnętrzne archiwa” to nie przesada.** APK to ZIP, a w środku mogą być JAR/AAR/nested ZIP. Fonty mogą być w `res/font` lub `assets`. Bez rekurencji część fontów zostanie pominięta.

**Niepotwierdzone:** Dokładne zapisy ToS Google Play zakazujące scrapingu – wymagałoby to bezpośredniego cytatu z regulaminu, którego nie znaleziono w dostępnych źródłach.