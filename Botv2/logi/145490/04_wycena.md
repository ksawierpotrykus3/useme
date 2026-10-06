=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
Wycena: **18 000–32 000 zł netto** (156–278 h × 115 zł/h). Czas: **25–40 dni roboczych** przy jednej osobie.

Rekomendacja: **WooCommerce/WordPress + custom animacje (GSAP) + Przelewy24/BLIK/Stripe**. Framer/Webflow tylko jako front, jeśli sklep ma ≤500 produktów i nie zależy Ci na P24/BLIK; inaczej headless 40k+.

Uzasadnienie: zakres to nie portfolio, ale pełny sklep z koszykiem, checkoutem, płatnościami, produktami, zamówieniami i CMS-em. Animacje z referencji muszą być interaktywne, nie jako wideo, więc trzeba je zakodować i przetestować mobile. Do tego responsywność, szybkie ładowanie i wdrożenie.

Brakuje: **1) ile produktów i czy asortyment rośnie; 2) rynek docelowy i płatności** — to zmienia stack i compliance (B2C UE: przycisk odstąpienia, Omnibus). Tak, realizuję e-commerce i płatności online.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: 18 000 zł na dole widełek jest zaniżone — przy tylu osobnych, autorskich animacjach (każda sekcja to inny problem techniczny) + pełnym sklepie z backoffice’em 156 h to bardzo optymistyczne założenie, realniej 200–280 h, czyli **23 000–32 000 zł**. Górna granica 32k się broni, dolna nie — poprawiam widełki na **23 000–35 000 zł netto** (stack headless wyżej, ~40k+). Compliance (Omnibus, przycisk odstąpienia) i P24/BLIK nie są dopisane na siłę — wynikają wprost z „sklep + płatności online” i polskiego rynku, ale słusznie zostały uwarunkowane rynkiem docelowym, więc ich nie usuwam. Nie zgadłem liczby produktów ani rynku — bez tego każda kwota to widełki, nie oferta, i dlatego dwa pytania zostają kluczowe przed wiążącą wyceną.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna**

**Kwota:** 18 000 – 26 000 zł netto (umowa o dzieło)
**Czas:** 25–35 dni roboczych

**Uzasadnienie:**
Zakres to de facto dwie rzeczy w jednym: portfolio z autorskimi animacjami (8 typów sekcji, każda z osobną referencją) plus pełny sklep z koszykiem, checkoutem, płatnościami i backoffice produktów/zamówień. Same animacje to ~60h, sklep z integracjami płatności i CMS-em kolejne ~80–100h, plus responsywność, wydajność i testy — przy 115 zł/h daje to ok. 160–220h. Widełki zależą od wyboru stacku: im więcej custom animacji i mniej gotowych komponentów platformy, tym bliżej górnej granicy.

**Rekomendacja technologii:**
Do sklepu z prawdziwym backoffice (produkty, ceny, dostępność, zamówienia) + CMS + szybkie mobile polecam **WooCommerce** — brak limitów produktów, natywne Przelewy24/BLIK/Stripe, pełna kontrola nad animacjami przez custom frontend. Framer i Webflow odpadają jako fundament sklepu: Framer nie ma natywnego sklepu (limit 100 pozycji w CMS), Webflow ma twardy sufit 500 produktów i tylko Stripe/PayPal (bez P24/BLIK). Headless (Next.js + Shopify/Medusa) daje najlepszą wydajność i animacje, ale podnosi wycenę do 40 000+ zł.

**Tak, realizuję e-commerce i płatności online** — koszyk, checkout, płatności, zarządzanie produktami, cenami, dostępnością i zamówieniami.

**Czego brakuje w zleceniu (2 pytania krytyczne):**
1. **Ile produktów ma być w sklepie i czy asortyment ma rosnąć?** — od tego zależy wybór platformy (Webflow ma limit 500/5000/15000, WooCommerce nie ma go wcale) i czy w ogóle warto rozważać Framer/Webflow.
2. **Do kogo sprzedajesz (konsumenci UE / B2B / poza UE) i jakie metody płatności?** — sprzedaż B2C w UE uruchamia obowiązek przycisku odstąpienia (od 19.06.2026) i Omnibus (najniższa cena z 30 dni); to elementy, które trzeba wpisać w zakres, jeśli dotyczą. Domyślnie proponuję Stripe + Przelewy24/BLIK.

Do ustalenia na callu: hosting i domena, kto dostarcza treści prawne (regulamin, polityki), termin startu.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: kwota **18–26k jest raczej dolną granicą i prawdopodobnie zaniżona**. Przeliczając uczciwie: 8 typów sekcji z osobnymi, autorskimi animacjami (każda to mini-projekt, nie komponent z biblioteki) to realnie 80–100h, nie 60h — sam hover w GRAPHIC DESIGN, naprzemienne kolumny w POSTERS i zoom w GALERIACH to osobne mechaniki. Sklep z backoffice, płatnościami i CMS-em to kolejne 90–110h, plus responsywność, wydajność (LCP), testy i wdrożenie — razem ~200–260h, czyli **23 000–30 000 zł** przy 115 zł/h. Nie dodałem nic „na siłę" — compliance UE wpisałem warunkowo („jeśli B2C w UE"), a nie jako pewnik, i tak zostaje. Korekta: **widełki 22 000–30 000 zł netto**, czas 30–40 dni roboczych; jeśli klient odpowie, że produktów jest <200 i bez rozbudowy, można zejść w dół, ale nie poniżej 20k.

=== DeepSeek-C — RUNDA 1 ===
**Wycena wstępna:**

- **Widełki:** 18 000 – 45 000 zł (zależnie od stacku)
- **Czas:** 4–8 tygodni (25–40 dni roboczych)
- **Rozbicie wg technologii:**
  - Webflow + Shopify jako backend sklepu: **~18 000–25 000 zł**, 4–5 tygodni
  - WooCommerce (WordPress): **~25 000–35 000 zł**, 6–7 tygodni
  - Headless (Next.js + Sanity/Shopify + Stripe/P24): **~38 000–50 000 zł**, 8+ tygodni

**Uzasadnienie (3 zdania):**
Zakres obejmuje 8 typów sekcji z zaawansowanymi animacjami interaktywnymi (nie wideo), pełny sklep z koszykiem, checkoutem, płatnościami i backoffice produktów/zamówień oraz CMS do samodzielnej edycji — to nie jest „strona z sklepem", a dwie złożone aplikacje w jednej spójnej estetyce editorial. Animacje per sekcja (HOME, POSTERS, GALERIE, GRAPHIC DESIGN) to osobny blok pracy, bo każda ma inne zachowanie i wymaga dopracowania na mobile. Kluczowa decyzja to stack — determinuje 60% wyceny i terminu.

**Tak, realizuję e-commerce i płatności online** (koszyk, checkout, Stripe/PayPal/Przelewy24/BLIK, backoffice zamówień).

**Czego brakuje w briefie — 2 pytania krytyczne:**

1. **Ile produktów ma być w sklepie i czy asortyment ma rosnąć?** Framer ma limit ~100 pozycji w CMS, Webflow 500 na najtańszym planie e-commerce — od tej liczby zależy, czy te platformy są w ogóle kandydatami, czy od razu idziemy w WooCommerce/headless. To zmienia wycenę o kilkanaście tysięcy złotych.

2. **Do kogo sprzedajesz (konsumenci UE / B2B / poza UE)?** Sprzedaż B2C w UE uruchamia obowiązek przycisku odstąpienia (od 19.06.2026) i Omnibus (najniższa cena z 30 dni) — to elementy, które trzeba wpiąć w zakres i wycenić. Jeśli sprzedajesz tylko B2B albo poza UE, ten blok znika.

**Uwaga do rekomendacji:** Framer odpada jako fundament sklepu (brak natywnego koszyka/checkoutu/backoffice — tylko nakładki). Webflow ma twarde limity produktów i brak Przelewy24/BLIK natywnie. Jeśli zależy Ci na prawdziwym sklepie z pełnym backoffice i polskimi płatnościami — WooCommerce lub headless, nie Framer/Webflow.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: dolna granica widełek (18 000 zł przy Webflow+Shopify) jest nierealistyczna, jeśli animacje mają być odtworzone jako interaktywne elementy, a nie szablon — 8 typów sekcji z hoverami, sliderami, zoomami i scroll-triggerami to przy 115 zł/h samo ~120–160 h, czyli 14–18 tys. zł, zanim dołożymy sklep, płatności i CMS. WooCommerce poniżej 28 000 zł nie zejdzie przy tym zakresie, a headless startuje realnie od ~55–60 tys. zł, nie 38 tys. Nie dodałem nic na siłę — compliance UE (Omnibus, przycisk odstąpienia) i pytanie o liczbę produktów to realne blokery, nie wypełniacz. Pominąłem za to: wysyłkę/fulfillment, strony prawne (regulamin, RODO, cookies), hosting/domenę/SSL i szkolenie z CMS — to osobne pozycje, które zawyżają widełki o kolejne kilka–kilkanaście tysięcy. Skorygowana kwota: **WooCommerce 28–40 tys. zł, headless 55–80 tys. zł, Webflow/Shopify tylko jako świadomy kompromis dla <200 produktów i bez natywnego P24/BLIK**.

=== DeepSeek-D — RUNDA 1 ===
**Wycena: 28 000 – 42 000 zł** (netto, umowa o dzieło)

**Czas:** 6–9 tygodni roboczych (przy pracy równoległej z Twoim designem)

**Uzasadnienie:**
- Zakres = portfolio z autorskimi animacjami (7+ typów sekcji, każda inna) **plus** pełny sklep z koszykiem, checkoutem, płatnościami i backoffice. To nie jest jedna strona — to dwa produkty w jednym.
- Animacje jako interaktywne elementy (nie wideo) oznaczają pisanie logiki od zera: scroll-linked, hover states, parallax, przejścia między podstronami. To najdroższa część projektu.
- Widełki zależą od stacku: WooCommerce (~28–35k) vs headless Next.js (~38–42k+). Headless daje lepsze animacje i szybkość, ale jest droższy w budowie i utrzymaniu.

**Realizuję e-commerce i płatności** (Przelewy24, BLIK, Stripe, PayPal). Pełny zakres: koszyk, checkout, produkty, ceny, dostępność, zamówienia.

**Technologia — moja rekomendacja:**
- **Framer jako fundament sklepu — odpada.** Nie ma natywnego koszyka ani backoffice, limit 100 pozycji w CMS. Nadaje się na portfolio, nie na sklep.
- **Webflow** — działa, ale limity produktów (500/5000/15000) i tylko Stripe/PayPal (bez P24/BLIK). Sensowny, jeśli asortyment <500 i nie rośnie.
- **WooCommerce** — bezpieczny wybór, bez limitów, pełne płatności PL, więcej pracy przy animacjach.
- **Headless (Next.js + Sanity/Shopify + Stripe/P24)** — najlepsza kontrola nad animacjami i szybkością, najdroższy.

**Czego brakuje w briefie (2 pytania):**
1. Ile produktów ma być w sklepie i czy asortyment ma rosnąć? Od tego zależy, czy Webflow w ogóle wchodzi w grę, czy od razu idziemy w WooCommerce/headless.
2. Sprzedajesz konsumentom w UE? Jeśli tak — od 19.06.2026 wchodzi obowiązek przycisku odstąpienia, a Omnibus wymaga historii cen z 30 dni. To elementy, które trzeba wpisać w zakres i wycenę.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena 28–42k była OK dla WooCommerce, ale górna granica zaniża headless — przy Next.js + Sanity/Shopify + P24/BLIK i tym zakresie animacji realnie wychodzi 45–70k+. Framer/Webflow nie dopisałem na siłę: to twarde limity (100/500 produktów, brak natywnego P24/BLIK), więc jako fundament sklepu odpadają, chyba że asortyment <200 i akceptujesz Shopify jako backend. Compliance (przycisk odstąpienia, Omnibus) słusznie wisi jako pytanie, ale jeśli sprzedajesz B2C w UE, dochodzi 2–4k do zakresu. Koryguję: WooCommerce 28–38k, headless 45–70k+, Webflow tylko jako portfolio + Shopify 15–25k. Pytania o liczbę produktów i rynek zostają — bez nich każda kwota to zgadywanie.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 25000,
  "kwota_gorna": 40000,
  "definitywna": false,
  "od_czego_zaleza": [
    "wybór stacku: WooCommerce vs Webflow+Shopify vs headless Next.js",
    "liczba produktów w sklepie i czy asortyment ma rosnąć",
    "rynek docelowy i obowiązki compliance UE dla B2C",
    "metody płatności: Przelewy24/BLIK/Stripe/PayPal",
    "zakres autorskich animacji i integracji z CMS",
    "hosting, utrzymanie, treści prawne i szkolenie z CMS"
  ],
  "dni_od": 30,
  "dni_do": 45,
  "uzasadnienie": "Finalne widełki 25 000–40 000 zł netto dotyczą rekomendowanego kompromisu, czyli WooCommerce/WordPress z customowymi animacjami i płatnościami PL; headless startuje realnie od 45 000–80 000 zł, a Webflow+Shopify ma sens głównie przy małym, nierosnącym asortymencie i bez natywnego P24/BLIK. Modele zgodnie odrzuciły Framer jako fundament sklepu i wskazały WooCommerce lub headless jako uczciwe rozwiązanie dla pełnego backoffice’u. Największa rozbieżność dotyczyła dolnej granicy: część modeli po autokrytyce zeszła do 22–23 tys. zł, ale przy 8 typach autorskich animacji i pełnym sklepie bezpieczniejsza jest dolna granica 25 tys. zł. Wycena nie jest definitywna, bo brak liczby produktów, rynku docelowego, metod płatności i finalnego stacku — te czynniki mogą przesunąć kwotę zarówno w dół, jak i w górę."
}

=== FINALNA WYCENA ===
25000-40000 zl netto | 30-45 dni | WIDELKI
Od czego zalezy: wybór stacku: WooCommerce vs Webflow+Shopify vs headless Next.js, liczba produktów w sklepie i czy asortyment ma rosnąć, rynek docelowy i obowiązki compliance UE dla B2C, metody płatności: Przelewy24/BLIK/Stripe/PayPal, zakres autorskich animacji i integracji z CMS, hosting, utrzymanie, treści prawne i szkolenie z CMS
Uzasadnienie rozjemcy: Finalne widełki 25 000–40 000 zł netto dotyczą rekomendowanego kompromisu, czyli WooCommerce/WordPress z customowymi animacjami i płatnościami PL; headless startuje realnie od 45 000–80 000 zł, a Webflow+Shopify ma sens głównie przy małym, nierosnącym asortymencie i bez natywnego P24/BLIK. Modele zgodnie odrzuciły Framer jako fundament sklepu i wskazały WooCommerce lub headless jako uczciwe rozwiązanie dla pełnego backoffice’u. Największa rozbieżność dotyczyła dolnej granicy: część modeli po autokrytyce zeszła do 22–23 tys. zł, ale przy 8 typach autorskich animacji i pełnym sklepie bezpieczniejsza jest dolna granica 25 tys. zł. Wycena nie jest definitywna, bo brak liczby produktów, rynku docelowego, metod płatności i finalnego stacku — te czynniki mogą przesunąć kwotę zarówno w dół, jak i w górę.
