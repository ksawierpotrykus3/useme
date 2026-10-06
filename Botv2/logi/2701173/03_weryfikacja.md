```
KWALIFIKOWALNOSC: TAK warunkowo. Jeśli budżet 1000 PLN jest sztywny — NIE (custom moduł nie zmieści się; brak gotowego modułu realizującego całość). Jeśli klient elastyczny — TAK.

TYP_ZLECENIA: projekt jednorazowy (wdrożenie modułu) z możliwością stałej współpracy przy rozwoju sklepu.

INTENCJA: mieszane — wykonawcze (wdrożenie, konfiguracja, testy) + doradcze (analiza, rekomendacja gotowego modułu).

DECYDENT_I_BOL: właściciel sklepu PrestaShop. Ból: ręczna edycja cen każdego produktu przy zmianie cen komponentów, brak centralnego cennika, ryzyko błędów i marnowanie czasu.

WYKONALNE: TAK technicznie. Najbliższa opcja: custom moduł z centralną tabelą komponentów i synchronizacją do natywnych kombinacji (static) LUB dynamiczne przeliczanie ceny. Research: brak gotowego modułu realizującego całość. Moja ocena: custom nie zmieści się w 1000 PLN.

POLE_DO_POPISU: JEST. PrestaShop natywnie nie ma centralnego cennika komponentów — kombinacje mają price impact per produkt. Dowód: klient chce centralnego cennika i automatycznego przeliczenia wszystkich produktów bez ręcznej edycji. Nie zgaduję, czy klient o tym wie — nazywam fakt.

SCIEZKA_MERYTORYKI: A (klient wprost pyta o proponowany sposób realizacji) + B (mina o natywnym braku centralnego cennika).

MINY_I_CIEKAWOSTKI:
- Mina: PrestaShop natywnie nie ma centralnego cennika komponentów. Dowód: klient pisze o centralnym cenniku i automatycznym przeliczeniu wszystkich produktów bez ręcznej edycji każdej oferty. Konsekwencja: jeśli klient myśli, że to wbudowane, będzie zawiedziony. Alternatywa: custom moduł z centralną tabelą i synchronizacją do kombinacji.
- Brak innych min opartych na dowodzie ze zlecenia. Wydajność przy dużej liczbie kombinacji to potencjalny problem, ale brak liczby produktów/kombinacji — to pytanie, nie mina. Research o PS 8.1 niepotwierdzony — nie używać.

ODMOWA: puste (brak twardej bariery technicznej z typów 1-6). Budżet 1000 PLN vs custom to kwestia kwalifikacji/opłacalności, nie odmowa techniczna.

PYTANIA:
1. Wersja PrestaShop (1.7 czy 8.x)? — od tego zależy kompatybilność modułu. Nie pisaliście, więc pytam, bo to wpływa na wybór rozwiązania.
2. Ile produktów ma być objętych automatycznym przeliczaniem? — od tego zależy wydajność synchronizacji i czas realizacji. Nie pisaliście o skali, więc pytam, bo to wpływa na architekturę i wycenę.
3. Czy produkty mają już zdefiniowane kombinacje RAM/dysk w PrestaShop, czy budujemy od zera? — od tego zależy, czy migrujemy istniejące dane, czy tworzymy nowe. Nie pisaliście o obecnym stanie, więc pytam, bo to zmienia zakres prac.
4. Czy cena bazowa produktu (np. 1500 zł) ma pozostać stała, a centralny cennik służy tylko do wyliczania różnic za zmianę konfiguracji? Czy też cena produktu ma być sumą komponentów z centralnego cennika? — to zmienia architekturę i wycenę. Nie pisaliście o tym wprost.

CO_ZLECENIE_MOWI:
- PrestaShop, moduł do automatycznego przeliczania cen konfiguracji komputerów i laptopów.
- Centralny cennik komponentów (RAM DDR4/DDR5, SSD) z wartościami w zł.
- Każdy produkt ma konfigurację bazową, cena produktu dotyczy tej konfiguracji.
- System ma automatycznie odejmować wartość bazowych komponentów i dodawać wartość nowo wybranych.
- Zmiana cen w jednym miejscu → automatyczne przeliczenie wszystkich produktów bez ręcznej edycji.
- Zakres: analiza najlepszego rozwiązania, gotowy moduł jeśli dostępny, wdrożenie, konfiguracja, testy.
- W odpowiedzi: proponowany sposób realizacji, orientacyjny koszt, termin, przykłady podobnych wdrożeń.
- Możliwa dalsza współpraca.
- Załącznik: Obrazek.png — tabela z cenami komponentów.

CZEGO_NIE_MOWI:
- Wersji PrestaShop.
- Liczby produktów.
- Czy kombinacje już istnieją w produktach.
- Czy cena bazowa ma się zmieniać przy zmianie cen komponentów, czy tylko różnice.
- Czy inne komponenty (CPU, GPU) mają być uwzględnione.
- Czy ceny komponentów są zależne od producenta.
- Czy klient ma już jakiś moduł do kombinacji lub cen.
- Czy ceny bazowe produktów już zawierają komponenty bazowe (choć z opisu wynika, że tak).
- Budżetu poza podanym 1000 PLN.
- Terminu — klient pyta o termin, ale sam go nie narzuca.

GRANICA_CIECIA: Krótka odpowiedź. Klient wie czego chce, ma tabelę. Struktura: rekomendacja (custom, bo brak gotowego modułu) + 3-4 pytania + widełki orientacyjne lub informacja o budżecie. Bez rozwodzenia się nad technologią. Maksymalnie 1 akapit rekomendacji + pytania.

RESEARCH_POTRZEBNY: TAK (już zrobiony). Sprawdzić gotowe moduły. Wynik: brak modułu realizującego całość. To realnie zmienia: rekomendacja custom, budżet 1000 PLN niewystarczający. Dalszy research: niepotrzebny do decyzji.

DECYZJE: DOPISAĆ: W ofercie (jeśli składać) napisać wprost: brak gotowego modułu realizującego centralny cennik komponentów w PrestaShop; potrzebny custom moduł. Nie obiecywać, że 1000 PLN wystarczy. Jeśli budżet sztywny — podziękować i zaproponować gotowy moduł częściowy (globalne opcje) lub zwiększenie budżetu. / ODPOWIEDZIEĆ: Krótko: rekomendacja custom z centralną tabelą i synchronizacją do kombinacji; widełki orientacyjne po poznaniu odpowiedzi; pytania 1-4. / DOPYTAĆ: 1) wersja PS, 2) liczba produktów, 3) czy kombinacje już są, 4) czy cena bazowa stała czy suma komponentów.
```