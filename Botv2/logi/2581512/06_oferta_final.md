Zaczynałbym od tego, co już macie. LiteSpeed z Redisem i QUIC.cloud plus snippety to solidny fundament, więc nie będę dublował cache ani dokładał kolejnej wtyczki do optymalizacji. Przy LCP 5s+ przy takim stacku wąskie gardło prawie nigdy nie siedzi w cache, tylko w samym elemencie LCP albo w tym, co blokuje renderowanie. Sam baner w AVIF czy WebP tego nie zdejmie, jeśli obraz jest lazy-loadowany, siedzi w tle CSS albo w sliderze ładowanym przez JS. Dlatego najpierw identyfikuję, co dokładnie jest elementem LCP i jaka jest ścieżka renderowania, a dopiero potem wdrażam.

Zamiast gwarancji braku konfliktów z 50+ wtyczkami proponuję procedurę, bo tej gwarancji nie da się uczciwie dać. Konflikt zależy od wersji, kolejności ładowania i minifikacji, więc obiecuję staging, backup, rollback i testy po każdej zmianie. Cel 85-90+ na mobile traktuję jako cel, nie jako gwarancję wyniku.

Wycena orientacyjna to 2500-4500 zł netto, 7-10 dni od dostępu do stagingu. Kwota zależy od tego, czy LCP to zwykły obraz, tło CSS czy slider, czy cel dotyczy tylko strony głównej czy całego sklepu, oraz od tego, czy UCSS i CCSS nie tną stylów motywu i nie wymagają ręcznych wykluczeń. Po zobaczeniu stagingu zawężę widełki.

Żeby ruszyć, potrzebuję od was trzech rzeczy. URL i dostępu do stagingu, bo bez sprawdzenia elementu LCP nie wycenię zakresu rzetelnie. Odpowiedzi, czy 85-90+ dotyczy tylko home mobile, czy też kategorii, produktów i koszyka. Oraz informacji, które wtyczki są krytyczne i nie można ich wyłączyć nawet punktowo, bo to określa zakres testów regresji.

Jeśli wolicie, możemy zacząć od samego rozpoznania stagingu i wtedy ustalimy dalszy zakres.

Ksawier