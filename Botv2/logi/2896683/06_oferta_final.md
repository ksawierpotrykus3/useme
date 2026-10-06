Wdrożenie tego prototypu to nie przeklejenie HTML do Shopify, tylko odtworzenie go w Liquid i Online Store 2.0 tak, żeby dał się edytować z panelu i nie rozsypał się przy pierwszej zmianie treści.

Różne układy desktop i mobile robię w jednym motywie, sekcjami warunkowymi i media queries, bez dwóch motywów i bez skalowania. Tam, gdzie układy faktycznie się rozjeżdżają, decyduję per sekcja, bo inaczej mobile zjada PageSpeed.

Linki do trzech sklepów z customowym motywem wysyłam w osobnej wiadomości tuż po tej ofercie, z opisem co dokładnie było moją pracą przy każdym z nich, czy motyw od zera, czy sekcje produktowe, czy konfiguracja analityki. Wolę, żebyś miał je pod ręką obok wyceny, a nie szukał ich w treści.

Wycena etapowa. Motyw 8 000 do 11 000 zł, konfiguracja 2 000 do 3 000 zł, analityka 1 500 do 2 500 zł, opcje 1 500 zł. Razem 13 000 do 18 000 zł netto. Termin około trzech do czterech tygodni roboczych. Po NDA i zobaczeniu prototypu dostroję kwoty, bo zależą od realnej złożoności animacji, różnic mobile i desktop oraz gotowości plików wideo.

Płatne aplikacje i koszty miesięczne. CMP Google Certified, Pandectes albo Cookiebot, 40 do 120 zł. InPost Paczkomaty 0 do 200 zł. Fakturownia, koszt do potwierdzenia w App Store. Hosting wideo Bunny Stream 6 do 60 zł albo Cloudflare Stream 22 do 220 zł. Płatności Przelewy24 lub Tpay, koszt do potwierdzenia w App Store.

Duże wideo w tle strony głównej wrzucam na zewnętrzny hosting, Bunny Stream albo Cloudflare Stream, i podpinam w Liquid z lazy loadem, posterem i wyłączonym autoplayem na mobile. PageSpeed sprawdzam przed i po. Consent Mode v2 stawiam przez CMP Google Certified, które pisze do Shopify Customer Privacy API. Ustawiam cztery sygnały, ad_storage, ad_user_data, ad_personalization, analytics_storage. Konwersję sprawdzam w GA4 DebugView i w Google Ads, status Recording conversions.

Domyślnie proponuję plan Shopify Grow, dla tego zakresu wystarczy.

Czy pliki wideo są gotowe, czy wchodzi przygotowanie i kompresja pod web? Kiedy podpisujemy NDA, żeby zobaczyć prototyp i domknąć wycenę?

Ksawier