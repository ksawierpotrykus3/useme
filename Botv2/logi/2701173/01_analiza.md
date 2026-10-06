```
KWALIFIKOWALNOSC: TAK

TYP_ZLECENIA: projekt jednorazowy (wdrożenie modułu) z możliwością stałej współpracy przy rozwoju sklepu

INTENCJA: mieszane — wykonawcze (wdrożenie, konfiguracja, testy) + doradcze (analiza najlepszego rozwiązania, rekomendacja gotowego modułu)

DECYDENT_I_BOL: właściciel sklepu PrestaShop. Ból: ręczna edycja cen każdego produktu przy zmianie cen komponentów, brak centralnego cennika, ryzyko błędów i marnowanie czasu.

WYKONALNE: TAK. Najbliższa opcja: moduł custom z centralną tabelą komponentów, który przy zapisie przelicza kombinacje wszystkich produktów (SQL) LUB dynamiczne przeliczanie ceny na karcie produktu. Ewentualnie gotowy moduł jeśli istnieje.

POLE_DO_POPISU: JEST. Klient prawdopodobnie nie wie, że PrestaShop natywnie nie ma centralnego cennika komponentów — kombinacje mają price impact per produkt, nie per globalna tabela. To jest sedno problemu i miejsce na merytorykę.

SCIEZKA_MERYTORYKI: A — klient wprost pyta o "proponowany sposób realizacji" i "analizę najlepszego rozwiązania".

MINY_I_CIEKAWOSTKI:
Mina: PrestaShop natywne kombinacje (attributes + combinations) obsługują price impact per produkt, ale NIE mają centralnego cennika. Zmiana ceny komponentu wymaga ręcznej edycji każdego produktu — dokładnie to, czego klient chce uniknąć. Dowód: klient pisze "zmiana wartości komponentów w jednym miejscu oraz automatyczne przeliczenie wszystkich produktów bez ręcznej edycji każdej oferty". To nie jest natywne. Trzeba custom moduł (sync centralnej tabeli → kombinacje) albo gotowy moduł, albo dynamiczne nadpisanie ceny na karcie produktu.
Konsekwencja: jeśli klient myśli, że to wbudowane — będzie zawiedziony. Jeśli my to nazwiemy i damy rozwiązanie — budujemy zaufanie.
Alternatywa: proponujemy moduł z centralną tabelą i synchronizacją do kombinacji przy zapisie (static, wydajne) albo dynamiczne przeliczanie (prostsze, ale wolniejsze przy dużym ruchu). Rekomendacja: static sync.

ODMOWA: puste. Nie ma tu twardej bariery typu brak API, limit zewnętrzny, konflikt zakresu, regulacje, nieistniejący termin ani bariera prawno-autorska. Budget 1000 PLN jest niski, ale to kwestia handlowa, nie odmowa techniczna.

PYTANIA:
1. Wersja PrestaShop (1.7 czy 8.x)? — od tego zależy kompatybilność modułu i ewentualne różnice w API kombinacji. Nie pisaliście o tym, więc pytam, bo od tego zależy, czy gotowy moduł w ogóle zadziała.
2. Ile produktów ma być objętych automatycznym przeliczaniem? — od tego zależy wydajność synchronizacji (przy 100 produktach sync przy zapisie jest natychmiastowy, przy 10 000 może wymagać kolejkowania) i czas realizacji. Nie pisaliście o skali, więc pytam, bo to wpływa na architekturę i wycenę.
3. Czy produkty mają już zdefiniowane kombinacje RAM/dysk w PrestaShop, czy budujemy od zera? — od tego zależy, czy migrujemy istniejące dane, czy tworzymy nowe. Nie pisaliście o obecnym stanie, więc pytam, bo to zmienia zakres prac.
4. Czy w przyszłości dochodzą inne komponenty (CPU, GPU, przekątna ekranu)? — od tego zależy, czy budować moduł elastyczny (dowolne grupy atrybutów) czy tylko RAM/dysk. Nie pisaliście o tym, więc pytam, bo elastyczna architektura to większy zakres, ale oszczędza przepisanie za pół roku.

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
- Czy inne komponenty (CPU, GPU) mają być uwzględnione.
- Czy ceny komponentów są zależne od producenta (np. DDR4 8GB może mieć różne ceny u różnych dostawców).
- Czy klient ma już jakiś moduł do kombinacji lub cen.
- Czy ceny bazowe produktów już zawierają komponenty bazowe (choć z opisu wynika, że tak).
- Budżetu poza podanym 1000 PLN (ale to w ogłoszeniu).
- Terminu — klient pyta o termin, ale sam go nie narzuca.

GRANICA_CIECIA: Krótka odpowiedź. Klient wie czego chce, ma tabelę. Nie ma sensu lanie wody. Struktura: rekomendacja (ścieżka A) + 3-4 pytania + widełki orientacyjne. Bez rozwodzenia się nad technologią, bez listy funkcji, bez "chętnie opowiem na rozmowie". Maksymalnie 1 akapit rekomendacji + pytania.

RESEARCH_POTRZEBNY: TAK. Sprawdzić, czy istnieje gotowy moduł PrestaShop do centralnego cennika komponentów / kombinacji (np. "Advanced Combinations", "Price Calculator", moduły od PrestaShop Partners). Jeśli istnieje — rekomendujemy, zakres maleje, cena może zmieścić się w 1000 PLN. Jeśli nie — custom moduł, cena wyższa, trzeba to uczciwie powiedzieć. Sprawdzić też, jak PrestaShop 8.x obsługuje kombinacje i price impact (czy są zmiany względem 1.7).
```