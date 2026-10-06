## 1. HubSpot Forms + upload plików — potwierdzone ograniczenie

**Ustalenie kluczowe:** HubSpot **nie oferuje już standardowego, wbudowanego pola uploadu plików**, które można swobodnie dodać do każdego nowego formularza. Dotychczasowa opcja jest traktowana jako **legacy file upload field** i występuje wyłącznie w ograniczonych scenariuszach.

**Gdzie legacy field jeszcze działa:**
- w formularzach utworzonych przed zmianą funkcjonalności,
- w niektórych historycznych formularzach szablonowych,
- w istniejących formularzach osadzonych na stronie, które nie zostały przebudowane.

**Czego nie można zrobić:** nie da się dodać nowego legacy upload field do dowolnego przyszłego formularza.

**Limity rozmiaru plików:**
- **100 MB** na pole uploadu (single i multiple) — limit samego formularza.
- W File Manager: **20 MB** dla kont z dostępem wyłącznie do darmowych narzędzi HubSpot; **2 GB** dla kont płatnych.

**Konsekwencja dla zlecenia:** klient wymaga „formularza z możliwością dodawania załączników" oraz „integracji formularzy z HubSpot CRM". Jeśli formularz ma być budowany od zera, **nie ma gwarancji, że pole uploadu będzie dostępne**. Nawet jeśli istnieje, plik trafia do ukrytego folderu File Managera z widocznością „private", a link do niego pojawia się w rekordzie kontaktu. **Nie jest to więc klasyczny załącznik w CRM, lecz link do pliku.**

**Status:** potwierdzone na podstawie dokumentacji HubSpot i niezależnego przewodnika opartego na oficjalnej dokumentacji.

---

## 2. WPML vs Polylang — wydajność

**Potwierdzone dane:**
- WPML może generować **wysoką liczbę zapytań SQL**, szczególnie na stronach z rozbudowanymi taksonomiami i treścią wielojęzyczną. W jednym z raportowanych przypadków strona główna generowała **325 zapytań** i ładowała się **6,63 s**.
- Polylang jest **generalnie lżejszy i wydajniejszy** od WPML.
- Testy WP Rocket: WPML i Polylang są „szyja w szyję", ale Polylang wypadł **nieznacznie lepiej** pod względem wydajności.

**Konsekwencja dla zlecenia:** przy wymaganiu PL+EN oraz rozbudowanym CMS wybór pluginu wielojęzycznego ma bezpośredni wpływ na szybkość ładowania, którą klient wymaga w zakresie („optymalizacja szybkości"). **Polylang wydaje się bezpieczniejszym wyborem wydajnościowym**, ale wymaga weryfikacji kompatybilności z wybranym motywem i ACF.

**Status:** potwierdzone na podstawie raportów użytkowników i testów porównawczych.

---

## 3. ACF — wydajność

**Potwierdzone:**
- ACF domyślnie przechowuje dane w `wp_postmeta`, co **staje się nieefektywne przy dużej skali** — nadmiarowe wiersze, wolniejsze zapytania, problemy z indeksowaniem.
- Meta queries mogą **poważnie obciążać wydajność**, jeśli nie są zoptymalizowane — każdy warunek meta query generuje dodatkowe JOIN-y lub odczyty tabeli.
- Zalecane strategie: **custom tables** dla dużych struktur, **object caching** (Redis/Memcached), **lazy loading** dla dużej liczby pól.

**Konsekwencja dla zlecenia:** rozbudowany CMS z case studies, certyfikatami, mapą zasięgu i wielojęzycznością oznacza **wiele grup pól ACF**. Bez optymalizacji (custom tables, caching) strona może nie osiągnąć wymaganej szybkości. **To nie jest problem krytyczny, ale wymaga świadomej decyzji architektonicznej już na etapie wyceny.**

**Status:** potwierdzone na podstawie oficjalnej dokumentacji ACF.

---

## Podsumowanie: miny potwierdzone vs niepotwierdzone

| Mina | Status |
|---|---|
| HubSpot Forms — brak standardowego uploadu dla nowych formularzy | **Potwierdzone** |
| HubSpot — limit rozmiaru zależny od planu (20 MB free / 2 GB paid) | **Potwierdzone** |
| WPML — ryzyko wydajnościowe vs Polylang | **Potwierdzone** |
| ACF — ryzyko wydajnościowe przy dużej skali | **Potwierdzone** |
| Konkretny plan HubSpot klienta — nieznany | **Niepotwierdzone** |
| Dokładny mechanizm „interaktywnej mapy zasięgu" — nieokreślony w ogłoszeniu | **Niepotwierdzone** |