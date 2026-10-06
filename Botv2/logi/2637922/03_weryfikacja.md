```
KWALIFIKOWALNOSC: TAK, ale warunkowo — zlecenie wykonalne tylko wtedy, gdy klient zaakceptuje ścieżkę, która nie łamie regulaminu gry. Bez tego — odmowa.
TYP_ZLECENIA: projekt jednorazowy (userscript / nakładka dostępnościowa)
INTENCJA: wykonawcze
DECYDENT_I_BOL: osoba niewidoma (NVDA), gracz pokewars.pl. Ból: bariera dostępności — interfejs mapy/lokacji nie jest czytelny z klawiatury, więc funkcja walki z bossem jest dla klienta nieosiągalna. Cel realny: móc samodzielnie grać, nie „auto-grać”.
WYKONALNE: TAK — ale w wariancie zgodnym z regulaminem. Najbliższa wykonalna opcja: userscript/rozszerzenie, które **odczytuje strukturę strony i wystawia klientowi informację** (gdzie jest przycisk, jaki jest stan walki), a nie klika za niego. Wariant „kliknij sam automatycznie” jest wykonalny technicznie, ale sprzeczny z §7.6 regulaminu → patrz ODMOWA. Warunek wstępny obu wariantów: trzeba zobaczyć DOM po zalogowaniu. Bez tego nie wiemy nawet, czy przycisk da się wybrać selektywnie.

POLE_DO_POPISU: JEST — (1) różnica między „skrypt klika za Ciebie” a „skrypt mówi Ci, gdzie kliknąć” — to zmienia ryzyko bana na zero i nadal rozwiązuje ból; (2) sposób komunikacji z NVDA (live region / komunikat na żywo); (3) ścieżka diagnozy DOM przed pisaniem kodu.

SCIEZKA_MERYTORYKI: B

MINY_I_CIEKAWOSTKI:
- MINA (twarda, z dowodem): Regulamin pokewars.pl §7 pkt 7.6: „Zabronione jest korzystanie z botów, skryptów, bindów oraz wszelkich innych nieprzewidzianych przez twórców serwisu rzeczy wpływających na polepszenie sytuacji gracza (np. poprzez automatyczne wędrowanie do lokacji).” Źródło: https://pokewars.pl/regulamin. Mechanizm awarii: skrypt klikający „walcz z bossem” automatycznie = automatyczne wykonanie akcji w grze = polepszenie sytuacji gracza = naruszenie §7.6. Konsekwencja: ryzyko blokady konta, na którym klient grał. To jest fakt ze źródła, nie domysł. Ton: rzeczowo, bez straszenia — mówię jak jest i daję alternatywę zgodną z regulaminem.

- CIEKAWOSTKA (nie mina, bo nie mam dowodu): Klient pisze „z klawiatury nigdzie tego nie widzę”. To znaczy tylko tyle: przycisk nie jest w kolejności Tab. NIE znaczy, że jest w `<canvas>` ani że nie ma go w DOM — równie dobrze może być `<div>` z `onclick` bez `tabindex`/ARIA. Tego NIE rozstrzygam w ofercie, to weryfikujemy po wejściu na konto. Wycofuję z iteracji 1 spekulację o canvasie — nie miała dowodu.

- WYCOFANE z iteracji 1: „informacja o braku latarki wymaga odczytu stanu graficznego” — nie mam dowodu, jak gra przekazuje ten stan. To było zgadywanie. Do weryfikacji przy diagnozie DOM, nie do oferty.

ODMOWA:
Typ 4 (zgodność i regulacje) — realizacja wprost tego, o co prosi klient w punkcie „skrypt klika przycisk za mnie”, narusza regulamin gry.
Obiekt odmowy słowami klienta: „skrypt przechodzi do zakładki… a następnie klika przycisk walcz z bossem”.
Mechanizm: §7.6 regulaminu.
Konsekwencja: blokada konta.
Alternatywa (i to jest właściwa oferta): ten sam efekt dla klienta, ale bezpieczny — skrypt, który **informuje** (gdzie na mapie jest boss, jaki jest stan walki, czego brakuje do walki), a kliknięcie zostaje po stronie klienta (jedno naciśnięcie klawisza / NVDA). Klient zachowuje sprawczość, nie łamie regulaminu, dostaje to, po co przyszedł. Akceptuję resztę zakresu — diagnozę, komunikaty, obsługę NVDA.

PYTANIA:
1. Czy klient może udostępnić osobne konto testowe (albo zgodzić się, żebyśmy założyli własne)? Pytam, bo bez wejścia po zalogowaniu nie ustalimy, czy przycisk walki da się w ogóle wybrać selektywnie — a od tego zależy, czy wariant informacyjny jest wykonalny, czy trzeba iść ścieżką zgłoszenia problemu dostępności do twórców.
2. Czy po wejściu w „walcz z bossem” walka toczy się automatycznie, czy wymaga kolejnych decyzji (atak, przedmiot, wybór)? Pytam, bo od tego zależy, czy zakres kończy się na jednym komunikacie, czy na obsłudze całej walki — a to zmienia wycenę.
3. Czy klient dopuszcza wariant „skrypt tylko informuje, ja klikam sam”? Pytam wprost, bo to rozstrzyga, czy w ogóle składamy ofertę wykonawczą, czy tylko ścieżkę zgłoszenia do twórców gry.

(TYP 2, nie pytanie): przeglądarka/system — zakładam Chrome + Tampermonkey na Windows, bo to najprostsza ścieżka dla NVDA i najczęstszy setup; jeśli klient używa czegoś innego, dostroję. Nie pytam.

CO_ZLECENIE_MOWI: gra pokewars.pl; kroki: logowanie → uruchomienie skryptu → mapa>lokacje → kliknięcie „walcz z bossem”; opcjonalnie komunikat o braku warunków (np. latarki); klient jest osobą niewidomą korzystającą z NVDA; przycisk nieosiągalny z klawiatury; budżet do negocjacji; płatność do 15 maja.
CZEGO_NIE_MOWI: jak zbudowana jest strona po zalogowaniu (DOM vs canvas, SPA vs klasyczna); czy walka jest automatyczna; jaka przeglądarka/system; skąd czerpać stan wymagań walki; że skrypty są w regulaminie zabronione (a to jest — sprawdzone w researchu).
GRANICA_CIECIA: krótko. Jedna mina (regulaminowa, z cytatem i linkiem) + jedna propozycja wariantu zgodnego + 3 pytania. Bez technologii na zapas, bez spekulacji o canvasie, bez wyceny kwotowej (brak zakresu → widełki po diagnozie).
RESEARCH_POTRZEBNY: TAK — już wykonany i realnie zmienił obraz zlecenia (ujawnił §7.6). Kolejny krok: po uzyskaniu dostępu do konta testowego sprawdzić DOM mapy/lokacji (selektor przycisku, sposób renderowania, jak przekazywany jest stan walki). Publicznie — już zweryfikowane.

DECYZJE:
- DOPISAĆ: (1) minę regulaminową z cytatem §7.6 i linkiem — bez tego oferta jest nieodpowiedzialna; (2) propozycję wariantu zgodnego z regulaminem (skrypt informuje, klient klika); (3) zastrzeżenie, że wycena wstępna dopiero po wglądzie w DOM po zalogowaniu.
- ODPOWIEDZIEĆ: na wprost na pytanie klienta „gdzie jest przycisk” — nie wiemy bez wglądu w DOM; ale wiemy, dlaczego NVDA go nie widzi (nie ma go w tab-order), i wiemy, że automatyzacja klikania jest w tym serwisie zabroniona. Zaproponować wariant, który daje efekt bez bana.
- DOPYTAĆ: tylko o 3 rzeczy z listy powyżej — konto testowe, przebieg walki, akceptacja wariantu „informuję, nie klikam”. Przeglądarkę przyją

*Stream został przerwany przez DeepSeek. Wyślij 'kontynuuj' aby dokończyć — kontekst został zachowany.*