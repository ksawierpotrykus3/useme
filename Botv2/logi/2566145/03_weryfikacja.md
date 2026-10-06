```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy — migracja/rebuild e-commerce (PrestaShop 1.6 → 8.x)
INTENCJA: wykonawcze
DECYDENT_I_BOL: Właściciel sklepu budcena.pl. Ból: przestarzały PS 1.6/PHP 5.6, bezpieczeństwo, wydajność, stabilna integracja z BaseLinker, ochrona SEO.
WYKONALNE: TAK. Najbliższa opcja: staging + czysta instalacja PS 8.1/8.2, migracja danych, nowy szablon Warehouse PS8, odpowiedniki modułów, BaseLinker przez oficjalny moduł + WebService, przekierowania 301.
POLE_DO_POPISU: JEST. (1) 1.6→8.x to nie upgrade 1-Click, tylko czysta instalacja + migracja danych; (2) BaseLinker: oficjalny moduł PS8 + klucz WebService z pełnymi uprawnieniami; (3) 301 mapować z GSC; (4) moduły 1.6 dobieramy, nie przenosimy.
SCIEZKA_MERYTORYKI: B/C
MINY_I_CIEKAWOSTKI:
- Mina: klucz WebService dla BaseLinker musi mieć pełne uprawnienia, inaczej synchronizacja stanów, cen i zamówień może być niepełna. Dowód: klient zleca „Konfiguracja i testy kluczy API WebService dla BaseLinker (synchronizacja stanów, cen i zamówień)”. Research: BaseLinker ma oficjalny moduł PS8 i wymaga pełnego klucza.
- Ciekawostka/framing: 1.6→8.x to nie upgrade, tylko migracja do czystej instalacji. Dowód: 1.6.1.24 vs 8.1/8.2. Klient prawdopodobnie wie, ale warto potwierdzić, że nie idziemy ścieżką autoupgrade.
- Ciekawostka: Warehouse ma wersję pod PS8. Dowód: klient wymaga „wersji kompatybilnej z PS 8”. To potwierdzenie, nie mina.
- Ciekawostka: 301 warto mapować z GSC, nie tylko przepisać stare URL-e. Dowód: klient zleca 301, aby nie stracić pozycji w Google.
ODMOWA: puste. Brak twardej bariery. Jeśli klient oczekuje przeniesienia modułów 1.6 1:1 lub customizacji szablonu bez zmian — to konflikt zakresu, ale ogłoszenie tego nie mówi; wtedy pytanie + propozycja, nie odmowa.
PYTANIA:
1. Jakie moduły i integracje są aktywne i które muszą działać po migracji (płatności, wysyłki, faktury, marketing, BaseLinker)? Uzasadnienie: od tego zależy, czy są odpowiedniki PS8 i ile pracy.
2. Czy szablon Warehouse był modyfikowany indywidualnie (layout, checkout, funkcje)? Jeśli tak, czy są pliki/dokumentacja? Uzasadnienie: nowa wersja Warehouse nie przeniesie customizacji 1:1; to zmienia zakres i cenę.
3. Jaki jest wolumen: liczba produktów, kombinacji, klientów, zamówień, rozmiar bazy i zdjęć? Uzasadnienie: od tego zależy czas migracji, narzędzia i ryzyko limitów.
CO_ZLECENIE_MOWI: PS 1.6.1.24 → 8.1.x/8.2.x; PHP 5.6.40 → 8.1+; MariaDB 11.4.9; LiteSpeed; szablon Warehouse 1.6; staging; migracja produktów/kombinacji/zdjęć/kategorii/klientów/zamówień; moduły; BaseLinker WebService; 301 SEO; przeniesienie na domenę; kopie zapasowe.
CZEGO_NIE_MOWI: listy modułów, wolumenu danych, zakresu customizacji szablonu, terminu, budżetu poza „do negocjacji”, obecnego sposobu integracji BaseLinker, płatności/wysyłek, innych integracji, oczekiwanego okna przełączenia, multistore/walut/języków.
GRANICA_CIECIA: Zlecenie bogate, więc oferta zwięzła: potwierdzić zrozumienie, dać 2 konkrety, zadać 3 pytania. Nie przepytywać.
RESEARCH_POTRZEBNY: NIE — research wykonany. Kluczowe: PS8 wspiera PHP 8.1/8.2; Warehouse 4.7.x dla PS8; BaseLinker ma oficjalny moduł; MariaDB 11.4.9 niepotwierdzona explicit w dokumentacji, ale przewyższa minimum PS8.

DECYZJE:
- DOPISAĆ do oferty: „To migracja do czystej instalacji PS 8.x, nie upgrade 1-Click. Staging + migracja danych. BaseLinker: oficjalny moduł PS8 + klucz WebService z pełnymi uprawnieniami. 301 mapowane z GSC. Zakładam standard jednojęzyczny/walutowy; jeśli inaczej — dostroję wycenę.”
- ODPOWIEDZIEĆ: Potwierdzić wykonalność i doświadczenie w migracjach 1.6→8.x; nie wchodzić w szczegóły techniczne bez danych.
- DOPYTAĆ: (1) lista aktywnych modułów/integracji i które krytyczne; (2) czy Warehouse był modyfikowany i czy są pliki; (3) wolumen produktów/kombinacji/klientów/zamówień/rozmiar bazy i zdjęć.
```