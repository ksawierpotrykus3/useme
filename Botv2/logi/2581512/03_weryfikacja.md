```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (audyt LCP + wdrożenie optymalizacji CWV); retainer możliwy tylko jeśli klient sam rozszerzy — nie zakładam.
INTENCJA: wykonawcze
DECYDENT_I_BOL: Prawdopodobnie właściciel/e-commerce manager lub tech lead. Ból: mobile ~65 i LCP 5s+ mimo LiteSpeed+Redis+QUIC.cloud; nie dopisuję SEO/konwersji, bo tego nie ma w ogłoszeniu.
WYKONALNE: TAK. Cel 85–90+ mobile jako cel, nie absolutna gwarancja. „Gwarancja braku konfliktów z 50+ wtyczkami” jest niewykonalna jako 100%; wykonalna jest procedura: staging, backup, rollback, testy regresji, monitoring.
POLE_DO_POPISU: JEST (wąskie: procedura zamiast gwarancji konfliktów; ew. po dostępie identyfikacja elementu LCP). Bez wykładu o CWV.
SCIEZKA_MERYTORYKI: B
MINY_I_CIEKAWOSTKI:
- Mina: „Gwarancja braku konfliktow z 50+ wtyczkami” (dowód: ten zwrot). Mechanizm: konflikt zależy od wersji, kolejności ładowania, minifikacji/combine; nie da się wykluczyć wszystkich kombinacji. Konsekwencja: obietnica 100% może wrócić jako reklamacja. Alternatywa: staging + backup + rollback + testy + monitoring.
- Ciekawość dla nas: LCP 5s+ przy LiteSpeed+Redis+QUIC.cloud i snippetach (dowód: stan obecny). To znaczy, że nie dublujemy cache; najpierw trzeba zidentyfikować element LCP i ścieżkę renderowania. Do klienta tylko jako pytanie o dostęp, nie jako wykład.
ODMOWA: puste (brak okazji 1–6; korekta zakresu w minach)
PYTANIA:
1. Czy podacie URL i dostęp do stagingu? Pytam, bo bez sprawdzenia elementu LCP i render-blockingu nie da się rzetelnie wycenić zakresu.
2. Czy cel 85–90+ mobile dotyczy tylko strony głównej, czy całego sklepu (kategorie, produkty, koszyk)? Pytam, bo to zmienia liczbę szablonów i zakres testów.
3. Czy na stagingu są wtyczki, których nie można wyłączyć nawet punktowo (płatności, kurierzy, subskrypcje)? Pytam, bo to określa zakres testów regresji i ryzyko konfliktów.
CO_ZLECENIE_MOWI: WooCommerce; mobile Performance ~65; LCP 5s+; baza wyczyszczona; LiteSpeed Cache + Redis Object Cache + QUIC.cloud (UCSS/VPI); snippety usuwające style blokowe WP/WooCommerce; główny baner AVIF/WebP; eliminacja render-blocking; 50+ wtyczek; staging/backup; white-hat; cel 85–90+ mobile; budżet do negocjacji.
CZEGO_NIE_MOWI: URL; dostęp do stagingu; motyw/page builder; hosting; wersje WP/Woo/PHP; który element jest LCP; zakres stron dla celu; lista wtyczek; czy staging = produkcja; czy baner to <img>, tło CSS czy slider; czy 85–90+ to tylko home; czy akceptują procedurę zamiast absolutnej gwarancji konfliktów.
GRANICA_CIECIA: Krótko, na styk. Bez wykładu o CWV. Odnieść się do ich stacku i LCP, 3 pytania, żadnych obietnic 100% braku konfliktów. Wycena po URL/stagingu; jeśli teraz, widełki orientacyjne + otwartość. Głębokość tylko do LCP i testów konfliktów.
RESEARCH_POTRZEBNY: NIE na etapie oferty; po dostępie TAK (sprawdzić LCP element, render-blocking, UCSS/CCSS, wc-cart-fragments, konfigurację LiteSpeed/QUIC).
DECYZJE: DOPISAC: w ofercie krótko: nie dubluję cache; najpierw identyfikuję element LCP i render-blocking; gwarancję braku konfliktów zamieniam na procedurę staging+backup+rollback+testy; cel 85–90+ jako cel, nie absolutna gwarancja. ODPOWIEDZIEC: potwierdzić wykonanie i odnieść się do ich stacku, bez merytoryki o CWV. DOPYTAC: URL/staging; zakres stron dla 85–90+; wtyczki krytyczne na stagingu.
```