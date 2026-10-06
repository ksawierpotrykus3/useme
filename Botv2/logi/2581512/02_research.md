**Kontekst:** Poniższe wnioski opierają się na publicznie dostępnych źródłach. Bez URL/stagingu nie da się zweryfikować, który element jest LCP ani jak działa konfiguracja LiteSpeed/QUIC.cloud w tym konkretnym przypadku.

---

**1. Dlaczego LCP może być 5s+ mimo LiteSpeed + Redis + QUIC.cloud**

- **Element LCP bywa wstrzykiwany przez JS lub slider, nie przez `<img>` w HTML.** W jednym z audytów baner hero – faktyczny element LCP – był ładowany przez własny JavaScript wtyczki slidera, a nie przez zwykły tag `<img>` w kodzie strony. Wtedy preload, `fetchpriority` i optymalizacja formatu nie działają, bo przeglądarka nie widzi obrazu w HTML.
- **Galeria produktu lazy-loaduje się „eagerly, ale w złej kolejności”.** WooCommerce/Storefront wstawia galerię z URL-ami w pełnej rozdzielczości (często 2000–3000 px), a lazy-loader opóźnia główny obraz do momentu wykonania JS – LCP czeka na `wc-cart-fragments.js`, co daje 3,5–5 s na 4G.
- **`wc-cart-fragments.js` odpala się na każdej stronie** (także home i blog), blokując `domInteractive`; strony z tym wywołaniem pokazują 600–900 ms luki między FCP a LCP.
- **Render-blocking CSS nadal występuje mimo włączonego „Load CSS Asynchronously”.** W jednym z wątków użytkownik LiteSpeed Cache 7.9.1 na WooCommerce (Elementor Pro + Hello Elementor) miał CCSS aktywne, ale PageSpeed nadal raportował ~3,6 s render-blocking CSS z plików Elementora, WooCommerce, Font Awesome i powiązanych wtyczek.
- **UCSS potrafi usuwać style potrzebne dla dynamicznych komponentów motywu.** W przypadku WoodMart + LiteSpeed + QUIC.cloud ~50 z 65 plików CSS miało 0% selektorów zachowanych w wygenerowanym UCSS; style dla koszyka, bannerów, sliderów i menu mobilnego znikały. To pokazuje, że UCSS nie jest „bezpieczne” dla każdego motywu bez ręcznej weryfikacji wykluczeń.

---

**2. Konfiguracja LiteSpeed/QUIC.cloud – co źródła potwierdzają jako problematyczne**

- QUIC.cloud CCSS (Critical CSS) **może paradoksalnie pogorszyć wyniki**, jeśli callbacki REST nie działają poprawnie lub generowany krytyczny CSS nie pokrywa faktycznego widoku. W wątku na wordpress.org po włączeniu CCSS PageSpeed spadł poniżej 30 zarówno na mobile, jak i desktopie, a LCP breakdown i request delay pozostały wysokie.
- LiteSpeed Cache **nie zastąpi optymalizacji na poziomie szablonu** – w wątku z Divi mobile utknął na 60–65 mimo włączonych UCSS, CCSS, Delay JS, lazy load i optymalizacji Google Fonts.
- Konwersja do WebP/AVIF **sama w sobie nie zdejmie LCP**, jeśli obraz jest lazy-loaded, tłem CSS albo elementem slidera – to wynika wprost z natury LCP (element musi być widoczny w pierwszym viewporcie, a jego ładowanie nie może być odroczone).

---

**3. Konflikty z 50+ wtyczkami – dlaczego „gwarancja braku konfliktów” jest nie do utrzymania**

- Konflikt w WooCommerce to sytuacja, w której dwa lub więcej kawałków kodu wysyła sprzeczne sygnały; prawdopodobieństwo rośnie wraz z liczbą wtyczek i nakładaniem się funkcji.
- Standardowa procedura testowa to staging + backup + dezaktywacja wszystkich wtyczek poza WooCommerce + przywracanie po jednej z testem po każdej – ale to **wykrywa konflikty istniejące**, nie gwarantuje, że ich nie będzie po wdrożeniu optymalizacji.
- Konflikt może ujawnić się dopiero po aktualizacji wtyczki, zmianie kolejności ładowania skryptów lub włączeniu minifikacji/combine CSS – bo zmienia to kolejność arkuszy i wykonania JS.

---

**4. Czego nie można potwierdzić bez URL/stagingu**

- Który element jest LCP na stronie głównej mobile (baner hero, slajd, obrazek produktu, nagłówek).
- Czy baner to `<img>`, tło CSS, element slidera czy blok page buildera.
- Czy `fetchpriority="high"` i preload są już stosowane do elementu LCP.
- Czy LiteSpeed/QUIC.cloud generują poprawne CCSS/UCSS dla tego motywu i czy nie usuwają wymaganych stylów.
- Czy `wc-cart-fragments.js` jest zoptymalizowany (np. wyłączony poza stronami sklepu).
- Jaki jest realny zakres stron objętych celem 85–90+ (tylko home vs. kategorie/produkty/koszyk).

---

**Pytania do zleceniodawcy (bez zmian względem dziennika):**

1. Czy podacie URL strony i dostęp do stagingu?
2. Czy cel 85–90+ dotyczy tylko strony głównej mobile, czy całego sklepu?
3. Czy są wtyczki krytyczne, których nie można wyłączać nawet na stagingu (płatności, kurierzy, subskrypcje)?