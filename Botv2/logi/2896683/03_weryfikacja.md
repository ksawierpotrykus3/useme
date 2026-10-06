```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wdrożenie motywu Liquid + konfiguracja sklepu) z wbudowanym egzaminem wiedzy (3 pytania techniczne od klienta). Potencjał dalszej współpracy (Ads/optymalizacja) — ale to NIE jest przedmiotem zlecenia, nie dopisuję.
INTENCJA: mieszane — wykonawcze (wdrożenie + konfiguracja) + doradcze (3 odpowiedzi techniczne, architektura wideo, CMP, lista appek).
DECYDENT_I_BOL: Kto pisze — NIE WIEM (właściciel / PM / agencja) i do oferty tego nie potrzebuję. Pewne z tonu: klient jest techniczny (Liquid, OS 2.0, Shopify CLI, Consent Mode v2, PageSpeed). Ból wyprowadzony z pytań (nie z domysłu): wdrożyć prototyp bez utraty jakości wizualnej i bez utraty PageSpeed na mobile, gotowy na kampanie Google. Sygnał TCO (nie ból): żąda listy appek z kosztem miesięcznym — myśli o koszcie utrzymania, nie tylko wdrożenia.
WYKONALNE: TAK, z jednym doprecyzowaniem zakresu: „1:1 z HTML" nie znaczy kopiowania kodu — na Shopify to przekład na Liquid/OS 2.0. „1:1 wizualno-funkcjonalne" — tak. Najbliższa wykonalna opcja: jeden motyw responsywny + sekcje warunkowe dla miejsc, gdzie desktop/mobile NAPRAWDĘ się różnią.
POLE_DO_POPISU: JEST — trzy pytania klienta to czysty test kompetencji. Kto odpowie ogólnikami, wypada.
SCIEZKA_MERYTORYKI: A (klient pyta WPROST o trzy rzeczy). B i C NIE zachodzą — nie ma miny, której klient by nie znał; wszystko, co „nie wie", już sformułował jako pytanie. W poprzedniej iteracji wpisałem tu „plus B dla wideo" — to był błąd: klient sam zadaje to pytanie, więc to A, nie B.
MINY_I_CIEKAWOSTKI: BRAK realnych min (w sensie ścieżki B). Trzy punkty, które w innym zleceniu byłyby minami, tutaj są treścią odpowiedzi A, nie ostrzeżeniami:
 - „desktop/mobile o różnym układzie" (dowód: klient pisze „nie tylko skalowanie") → nie dwa motywy, jeden motyw + warunkowe sekcje.
 - „duże wideo w tle bez psucia PageSpeed" (dowód: pytanie klienta) → hosting zewnętrzny + lazy load + poster.
 - „Consent Mode v2" (dowód: wymóg klienta) → Shopify Customer Privacy API + CMP.
 Nie sprzedaję tego jako „uwaga, katastrofa" — to odpowiedzi.
ODMOWA: BRAK. Żaden typ 1–6 nie zachodzi. Nie ma paywalla, konfliktu z celem, limitu zewnętrznego, licencji blokującej, wymyślonej funkcji ani bariery autorskiej. „Nie 1:1 w kodzie, ale 1:1 wizualno-funkcjonalne" to doprecyzowanie zakresu, nie odmowa.
PYTANIA:
 1. Czy pliki źródłowe wideo są gotowe, czy wchodzi przygotowanie/kompresja pod web? — TYP 1. Pytam, bo to realna pozycja w etapie „motyw" i zmienia wycenę (gotowe vs. my robimy transkodowanie/poster).
 2. Kiedy podpisujemy NDA, żeby zobaczyć prototyp? — TYP 1. Bez tego wycena etapowa jest tylko widełkowa; po NDA dostroję liczby. Kontekst: to nie „chcę pooglądać", tylko warunek konkretnej wyceny.
 (Czego NIE pytam i dlaczego:
  - Liczba SKU akcesoriów — Shopify ma jeden szablon produktu z wariantami, liczba SKU nie zmienia pracy nad motywem. Wyciąłem z iter. 1 jako pytanie za granicą.
  - Plan Shopify — TYP 2, nie TYP 1. Proponuję domyślnie: dla tego zakresu Grow (Shopify) wystarczy; jeśli macie Plus, dostroję warstwę checkoutu. Nie pytam.
  - Nowy sklep vs migracja — TYP 2 z zastrzeżeniem: zakładam budowę od zera; jeśli migrujecie z istniejącego, doliczę etap importu i przekierowań. Nie pytam.
  - Budżet, technologia, cokolwiek z ogłoszenia — wycięte.)
CO_ZLECENIE_MOWI: gotowy prototyp HTML (Claude), desktop + mobile o różnych układach; ~12 szablonów; 1 produkt główny + akcesoria; dużo wideo, slidery, animacje; PL, sprzedaż PL; NDA; min 3 sklepy Shopify z custom theme + linki; Liquid, OS 2.0, Shopify CLI; rynek PL: płatności, InPost, faktury; GA4, Google Ads, Consent Mode v2; wymagana wycena etapami, termin, linki, lista appek z kosztem miesięcznym, odpowiedzi na 3 pytania.
CZEGO_NIE_MOWI: budżetu („do negocjacji" = brak widełek); czy nowy sklep czy migracja; planu Shopify; liczby SKU akcesoriów; czy pliki wideo są gotowe czy do przygotowania; kto odpowiada za treści/zdjęcia; preferowanego CMP; czy kampanie Ads już działają, czy my je stawiamy; na czym dokładnie polega „inny układ" mobile vs desktop (zobaczymy pod NDA).
GRANICA_CIECIA: Oferta = dokładnie to, co klient zażądał: (1) wycena etapami, (2) termin, (3) linki, (4) lista płatnych appek z kosztem miesięcznym, (5) odpowiedzi na 3 pytania. Ani akapitu więcej. Bez „o mnie", bez ogólników o Shopify, bez rozwijania każdego narzędzia w osobny esej.
RESEARCH_POTRZEBNY: NIE — research iter. 1 wystarcza. Wchodzi do oferty: Bunny/Cloudflare Stream (wideo — Bunny najtańszy, Cloudflare złoty środek), Shopify Customer Privacy API + CMP Google Certified (Cookiebot/Pandectes — nie CookieYes, bo przy Ads chcemy pełnej zgodności), InPost appki, Fakturownia. Ceny Fakturowni oraz Przelewy24/Tpay oznaczyć jako „do potwierdzenia w App Store" — nie wstawiać niepotwierdzonych kwot.

DECYZJE:
DOPISAĆ (do oferty, dokładnie tyle): (1) wycena etapowa — motyw / konfiguracja / analityka / opcje — widełki, po NDA dostrojenie; (2) harmonogram; (3) linki do min. 3 sklepów z custom theme; (4) lista płatnych appek z kosztem miesięcznym (CMP, InPost, Fakturownia, hosting wideo) — przy Fakturowni/przelewach oznaczyć „do potwierdzenia"; (5) odpowiedzi na 3 pytania — konkretnie, technicznie; (6) jedna linia: „1:1 wizualno-funkcjonalne w Liquid, nie kopiowanie HTML".
ODPOWIEDZIEĆ (na 3 pytania klienta): (a) jeden motyw Liquid/OS 2.0 + sekcje warunkowe dla realnych różnic desktop/mobile — nie dwa motywy; (b) wideo w tle: pliki na Bunny lub Cloudflare Stream, w Liquid lazy load + poster + `playsinline muted` + ograniczenie autoplay na mobile, weryfikacja PageSpeed Insights; (c) Consent Mode v2: CMP Google Certified (Cookiebot/Pandectes) → Shopify Customer Privacy API → 4 sygnały (ad_storage, ad_user_data, ad_personalization, analytics_storage), weryfikacja konwersji w GA4 DebugView + Google Ads (status „Recording conversions").
DOPYTAĆ: (1) czy pliki wideo są gotowe czy do przygotowania; (2) kiedy NDA, żeby zobaczyć prototyp i dostroić wycenę.
```