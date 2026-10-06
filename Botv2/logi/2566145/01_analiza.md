KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy — migracja/rebuild e-commerce
INTENCJA: wykonawcze
DECYDENT_I_BOL: Właściciel sklepu budcena.pl („posiadam”, domena). Ból: przestarzały PS 1.6/PHP 5.6, bezpieczeństwo, wydajność, stabilna integracja z BaseLinker, ochrona SEO.
WYKONALNE: TAK. Najbliższa opcja: staging + czysta instalacja PS 8.1/8.2, nie upgrade in-place; migracja danych, nowy szablon Warehouse PS8, odpowiedniki modułów, WebService/BaseLinker, 301.
POLE_DO_POPISU: JEST
SCIEZKA_MERYTORYKI: B/C
MINY_I_CIEKAWOSTKI:
- 1.6→8.x to nie zwykły upgrade, tylko migracja do czystej instalacji. Dowód: 1.6.1.24 vs 8.1/8.2. Konsekwencja: inny czas i zakres niż autoupgrade.
- Szablon Warehouse 1.6 nie jest kompatybilny z PS 8. Dowód: „posiadam obecną wersję na 1.6… wersji kompatybilnej z PS 8”. Customizacje nie przeniosą się 1:1.
- Moduły 1.6 mogą nie mieć odpowiedników PS 8. Dowód: „Weryfikacja i instalacja odpowiedników obecnych modułów”. Część może wymagać zamiennika lub przepisania.
- PHP 5.6.40 → 8.1/8.2 to duży skok. Dowód: „PHP: 5.6.40 (do zmiany na 8.1+)”. Stary kod modułów/szablonu może sypać błędami.
- BaseLinker/WebService do potwierdzenia. Dowód: „kluczy API WebService dla BaseLinker”. Sprawdzić, czy integracja nie zależy od modułu 1.6.
ODMOWA: puste. Brak twardej bariery. Jeśli klient oczekuje wyłącznie autoupgrade 1-Click, to konflikt zakresu — ale ogłoszenie tego nie mówi.
PYTANIA:
1. Lista aktywnych modułów i integracji (płatności, wysyłki, faktury, marketing) oraz które są krytyczne? Uzasadnienie: od tego zależy, czy są odpowiedniki PS 8 i ile pracy.
2. Czy szablon Warehouse był modyfikowany indywidualnie (layout, checkout, funkcje)? Jeśli tak, czy są pliki/dokumentacja? Uzasadnienie: nowa wersja Warehouse nie przeniesie customizacji; to zmienia zakres i cenę.
3. Jaki jest wolumen: liczba produktów, kombinacji, klientów, zamówień, rozmiar bazy i zdjęć? Uzasadnienie: od tego zależy czas migracji, narzędzia i ryzyko limitów.
CO_ZLECENIE_MOWI: PrestaShop 1.6.1.24 → 8.1.x/8.2.x; PHP 5.6.40 → 8.1+; MariaDB 11.4.9; LiteSpeed; szablon Warehouse stara wersja; staging; migracja produktów/kombinacji/zdjęć/kategorii/klientów/zamówień; moduły; BaseLinker WebService; 301 SEO; przeniesienie na domenę; kopie zapasowe.
CZEGO_NIE_MOWI: listy modułów, wolumenu danych, zakresu customizacji szablonu, terminu, budżetu poza „do negocjacji”, obecnego sposobu integracji BaseLinker, płatności/wysyłek, innych integracji, oczekiwanego okna przełączenia.
GRANICA_CIECIA: Zlecenie bogate, więc oferta zwięzła: pokazać, że wiemy, że to migracja do czystej instalacji, a nie upgrade; nie przepytywać. 3 pytania, bez listy 5+.
RESEARCH_POTRZEBNY: TAK. Sprawdzić: oficjalne wsparcie PS 8.1/8.2 dla PHP 8.1/8.2 i MariaDB 11.4.9 na LiteSpeed; dostępność szablonu Warehouse pod PS 8; kompatybilność BaseLinker/WebService; typowe pułapki migracji 1.6→8.