=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena wstępna:** 1 440–2 160 zł przy 90 zł/h (16–24 h).  
**Czas:** 5–8 dni roboczych od dostępu do stagingu.

**Uzasadnienie:** Przy LiteSpeed + Redis + QUIC.cloud wąskim gardłem zwykle nie jest cache, tylko element LCP, render-blocking i JS pokroju `wc-cart-fragments`. Bez URL/stagingu nie da się tego rzetelnie zmierzyć, a dochodzi jeszcze test regresji na 50+ wtyczkach. „Gwarancję braku konfliktów” zamieniam na procedurę: staging + backup + rollback + testy + monitoring; cel 85–90+ traktuję jako cel, nie absolutną gwarancję.

**Brakuje:**
1. URL i dostępu do stagingu.
2. Czy cel 85–90+ dotyczy tylko home mobile, czy całego sklepu.
3. Listy wtyczek krytycznych, których nie można wyłączyć nawet punktowo.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 1 440–2 160 zł (16–24 h) jest obroniona, ale bliżej dolnej granicy ryzyka, bo przy 50+ wtyczkach i UCSS/CCSS, które wg źródeł potrafią ciąć potrzebne style (WoodMart: 50/65 plików CSS z 0% selektorów), same testy regresji to realnie 6–10 h, nie 3–4. Nie zgadłem na siłę niczego — widełki i „cel, nie gwarancja” to uczciwe ustawienie. Gdybym miał korygować: dół bym podniósł do ~1 800 zł (20 h), a górę zostawił 2 160–2 400 zł, zwłaszcza jeśli cel 85–90+ dotyczy całego sklepu, a nie tylko home mobile. Zastrzeżenie: to nadal orientacja bez URL/stagingu — po dostępie może się okazać, że LCP siedzi w sliderze ładowanym JS-em albo w tle CSS i wtedy robota jest większa, niż wynika z ogłoszenia.

=== DeepSeek-B — RUNDA 1 ===
**Wycena orientacyjna:** 3600–5400 zł (40–60 h × 90 zł/h). Po dostępie do stagingu widełki mogą się zawęzić.

**Czas:** 7–10 dni roboczych.

**Uzasadnienie:** LCP 5s+ przy LiteSpeed+Redis+QUIC.cloud oznacza, że problem siedzi w samym elemencie LCP (slider/JS/tło CSS) albo w render-blockingu, a nie w cache — to trzeba najpierw zidentyfikować na stagingu. Przy 50+ wtyczkach dochodzą testy regresji i rollback po każdej zmianie, więc nie jest to zadanie na 2–3 h. Zamiast gwarancji braku konfliktów proponuję procedurę: staging + backup + rollback + testy po każdej zmianie.

**Czego brakuje:**
1. URL i dostęp do stagingu?
2. Cel 85–90+ mobile dotyczy tylko strony głównej, czy całego sklepu (kategorie, produkty, koszyk)?
3. Są wtyczki krytyczne, których nie można wyłączyć nawet punktowo na stagingu (płatności, kurierzy, subskrypcje)?

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 3600–5400 zł jest obroniona, ale górna granica jest ryzykowna bez zobaczenia stagingu — przy 50+ wtyczkach i sliderze/banerze jako LCP realnie może wyjść 30–40 h, jeśli UCSS/CCSS okaże się do naprawy od zera (a research pokazuje, że to częsty przypadek na WoodMarcie/Elementorze). Nie zgadłem tu nic „na siłę” poza jednym: założyłem, że problem siedzi w samym elemencie LCP, a to nadal hipoteza — dopóki nie zobaczę URL-a, nie wiem, czy to `<img>`, tło CSS, slider JS czy blok page buildera. Kwotę bym zostawił jako widełki, ale dopisałbym jedno zdanie: „jeśli okaże się, że CCSS/UCSS trzeba odbudować lub wykluczyć ręcznie dla motywu — wycena idzie w górę, po audycie stagingu”. Nie dodawałbym nic więcej do zakresu, bo ogłoszenie jest wąskie (LCP + render-blocking + testy konfliktów) i rozszerzanie go o SEO/konwersję byłoby naciąganiem.

=== DeepSeek-C — RUNDA 1 ===
Wycena orientacyjna: **2 200–4 000 zł** (24–44 h × 90 zł/h).  
Czas: **6–10 dni roboczych** od dostępu do stagingu.

Uzasadnienie: LCP 5s+ przy LiteSpeed/Redis/QUIC wymaga najpierw audytu elementu LCP i render-blockingu, a dopiero potem wdrożeń — sama konwersja banera na AVIF/WebP tego nie zdejmie. Przy 50+ wtyczkach dochodzą testy regresji, więc zamiast gwarancji „zero konfliktów” daję staging + backup + rollback + testy. Po dostępie do stagingu podam stałą kwotę.

Brakuje: URL/stagingu, zakresu stron dla celu 85–90+ (tylko home czy cały sklep), listy wtyczek krytycznych, informacji czy baner to `<img>`/tło CSS/slider oraz motywu/page buildera.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 2 200–4 000 zł są lekko niedoszacowane po dolnej granicy — przy 50+ wtyczkach, stagingu, testach regresji i weryfikacji po wdrożeniu realne minimum to ~30 h, nie 24 h, więc sensowniej wygląda **2 700–4 500 zł (30–50 h × 90 zł/h)**. Nie zgadłem jednej rzeczy na siłę: „cel 85–90+ jako cel, nie gwarancja” jest uczciwe, ale warto to było dopisać wprost także w wycenie, bo inaczej klient czyta widełki jako obietnicę wyniku. UCSS/CCSS przy tym stacku to realne ryzyko regresji (motyw + WoodMart/Elementor + 50 wtyczek), czego wcześniej nie zaakcentowałem — to podnosi zakres testów, nie obniża. Reszta (3 pytania, procedura zamiast gwarancji konfliktów, brak dublowania cache) — bez zmian, to jest dobrze.

=== DeepSeek-D — RUNDA 1 ===
**Wycena wstępna:** 1600–2400 zł (przy 90 zł/h, szacunek 18–27h).  
**Czas:** 4–6 dni roboczych.  
**Uzasadnienie:** Bez URL/stagingu nie wiem, który element jest LCP ani jakie jest realne render-blocking, więc wycena orientacyjna. Zakładam audyt, wdrożenie (baner AVIF/WebP, preload, fetchpriority, eliminacja blokujących zasobów) i testy regresji z 50+ wtyczkami. Gwarancję braku konfliktów zastępuję procedurą: staging + backup + rollback + testy – inaczej się nie da. Cel 85–90+ traktuję jako cel, nie absolutną gwarancję.

**Brakuje mi:**
1. URL i dostęp do stagingu.
2. Czy cel 85–90+ dotyczy tylko strony głównej mobile, czy całego sklepu (kategorie, produkty, koszyk)?
3. Czy są wtyczki krytyczne, których nie można wyłączyć nawet punktowo na stagingu (płatności, kurierzy, subskrypcje)?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 1600–2400 zł są OK dla wariantu „tylko strona główna mobile, LCP to zwykły `<img>` banera, UCSS/CCSS nie psują stylów” — ale to jest wariant optymistyczny, nie bazowy. Research pokazuje, że przy tym stacku (LiteSpeed + QUIC.cloud UCSS + 50+ wtyczek + WooCommerce) bardzo często okazuje się, że LCP jest wstrzykiwany przez JS slidera albo UCSS wyciął style i wtedy robota rośnie o ręczne wykluczenia, weryfikację szablonów i testy — realnie 30–40h, czyli 2700–3600 zł. Nie zgadłem niczego „na siłę”, ale powinienem w ofercie twardo zapisać, że 1600–2400 to zakres dla zakresu „home + typowe kategorie/produkt”, a rozszerzenie na cały sklep lub konieczność przepisania ładowania LCP na poziomie szablonu to osobna wycena po dostępie do stagingu. Rekomendacja: zostawić widełki, ale dopisać jedno zdanie o warunku i widełki rozszerzone 2400–3600 zł jako górna widełka przy najgorszym scenariuszu — inaczej klient może później uznać, że 1600 to cena sztywna.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 2700,
  "kwota_gorna": 4500,
  "definitywna": false,
  "od_czego_zaleza": [
    "od dostępu do URL/stagingu i identyfikacji faktycznego elementu LCP (img, tło CSS, slider JS, blok buildera)",
    "od zakresu stron dla celu 85–90+ mobile: tylko home czy także kategorie, produkty i koszyk",
    "od liczby i krytyczności wtyczek oraz zakresu testów regresji, backupu i rollbacku",
    "od stanu UCSS/CCSS i konfiguracji LiteSpeed/QUIC.cloud — czy wymagają ręcznych wykluczeń i czy nie tną stylów motywu",
    "od motywu/page buildera, hostingu i wersji WordPress/WooCommerce/PHP"
  ],
  "dni_od": 7,
  "dni_do": 10,
  "uzasadnienie": "Wszystkie modele zgadzają się, że wycena nie może być definitywna bez URL/stagingu, a gwarancję braku konfliktów z 50+ wtyczkami trzeba zamienić na procedurę staging+backup+rollback+testy. Rozbieżność jest głównie w pracochłonności: A i D zakładają prostszy LCP i zakres home, B i C słusznie doliczają ryzyko UCSS/CCSS, regresji i szerszego zakresu stron. Wybieram 2700–4500 zł jako środek ciężkości po autokorektach: to nie jest najniższa optymistyczna wycena, ale też nie skrajny górny wariant B bez potwierdzonego zakresu. Cel 85–90+ traktuję jako cel, nie gwarancję, a kwota może się zawęzić po audycie stagingu."
}

=== FINALNA WYCENA ===
2500-4500 zl netto | 7-10 dni | WIDELKI
Od czego zalezy: od dostępu do URL/stagingu i identyfikacji faktycznego elementu LCP (img, tło CSS, slider JS, blok buildera), od zakresu stron dla celu 85–90+ mobile: tylko home czy także kategorie, produkty i koszyk, od liczby i krytyczności wtyczek oraz zakresu testów regresji, backupu i rollbacku, od stanu UCSS/CCSS i konfiguracji LiteSpeed/QUIC.cloud — czy wymagają ręcznych wykluczeń i czy nie tną stylów motywu, od motywu/page buildera, hostingu i wersji WordPress/WooCommerce/PHP
Uzasadnienie rozjemcy: Wszystkie modele zgadzają się, że wycena nie może być definitywna bez URL/stagingu, a gwarancję braku konfliktów z 50+ wtyczkami trzeba zamienić na procedurę staging+backup+rollback+testy. Rozbieżność jest głównie w pracochłonności: A i D zakładają prostszy LCP i zakres home, B i C słusznie doliczają ryzyko UCSS/CCSS, regresji i szerszego zakresu stron. Wybieram 2700–4500 zł jako środek ciężkości po autokorektach: to nie jest najniższa optymistyczna wycena, ale też nie skrajny górny wariant B bez potwierdzonego zakresu. Cel 85–90+ traktuję jako cel, nie gwarancję, a kwota może się zawęzić po audycie stagingu.
