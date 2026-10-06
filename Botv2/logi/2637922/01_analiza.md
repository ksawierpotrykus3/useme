```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (skrypt do gry + funkcja informacyjna)
INTENCJA: wykonawcze
DECYDENT_I_BOL: osoba niewidoma, użytkownik pokewars.pl. Ból: bariera dostępności — NVDA nie widzi przycisku "walcz z bossem", więc klient nie może korzystać z funkcji walki. Chce grać samodzielnie, bez pomocy widzącej osoby.
WYKONALNE: TAK, ale warunkowo — jako userscript w przeglądarce klienta. Warunek: musimy najpierw zobaczyć strukturę strony (mapa>lokacje), żeby wiedzieć, jak zlokalizować przycisk walki. Bez tego nie ma czego klikać.
POLE_DO_POPISU: JEST — (1) wybór: userscript w przeglądarce vs zewnętrzna automatyzacja (Selenium) — uzasadnienie i rekomendacja; (2) sposób ogłaszania stanu przez NVDA (komunikat w konsoli / overlay / live region); (3) podejście iteracyjne: najpierw skrypt-diagnostyczny, który wypisze strukturę strony, potem właściwy.
SCIEZKA_MERYTORYKI: B
MINY_I_CIEKAWOSTKI:
- Jeśli mapa>lokacje jest renderowana graficznie (canvas/obraz), NVDA jej nie odczyta — i skrypt też nie kliknie selektywnie, tylko po współrzędnych, których nie znamy. Dowód: klient pisze "używając czytnika ekranu z poziomu klawiatury nigdzie tego nie widzę". To silny sygnał, że element nie jest zwykłym, dostępnym przyciskiem w DOM. Konsekwencja: kluczowa staje się najpierw diagnoza struktury strony, a nie pisanie skryptu „na oko”.
- Funkcja „informuj, gdy nie możesz walczyć z bossem (np. brak latarki)” wymaga odczytania stanu walki z gry. Jeśli stan jest przekazywany graficznie — tej informacji nie da się wydobyć, tak samo jak przycisku. To trzeba zweryfikować razem z punktem powyżej.
ODMOWA: (puste — żadna z 6 okazji nie zachodzi jednoznacznie; ToS gry sprawdzimy w researchu, ale to nie przesądza z góry o odmowie)
PYTANIA:
1. Czy możemy założyć własne konto testowe na pokewars.pl (publiczna rejestracja), żeby zbadać strukturę strony? A jeśli nie, czy klient może udostępnić osobne konto testowe? Pytam, bo bez wejścia na stronę nie ustalimy, jak zlokalizować przycisk walki i czy w ogóle da się go kliknąć selektywnie.
2. Czy po kliknięciu „walcz z bossem” walka toczy się automatycznie, czy wymaga dalszych akcji (kliknięć, wyborów)? Pytam, bo od tego zależy, czy skrypt kończy się na kliknięciu, czy musi obsłużyć cały przebieg walki.
3. Jakiej przeglądarki i systemu klient używa na co dzień (Chrome/Firefox/Edge, Windows/macOS)? Pytam, bo od tego zależy forma skryptu (np. Tampermonkey) i sposób, w jaki NVDA odczyta komunikaty.
CO_ZLECENIE_MOWI: gra pokewars.pl; kroki: logowanie → uruchomienie skryptu → mapa>lokacje → kliknięcie „walcz z bossem”; opcjonalnie komunikat o braku warunków walki (np. latarki); klient jest osobą niewidomą korzystającą z NVDA; przycisk nieosiągalny z klawiatury; budżet do negocjacji; płatność do 15 maja.
CZEGO_NIE_MOWI: jak zbudowana jest strona (canvas vs DOM, SPA vs klasyczna); czy walka jest automatyczna; jaka przeglądarka/system; skąd czerpać informację o wymaganiach walki; czy automatyzacja jest zgodna z regulaminem gry; czy skrypt ma działać na koncie klienta, czy osobnym; jaki jest realny termin (data 15 maja jest przy płatności, nie przy oddaniu).
GRANICA_CIECIA: Krótko. 3 pytania + jedna propozycja podejścia (userscript) + jedna mina z dowodem. Bez rozpisywania technologii, bez wyceny kwotowej (brak zakresu — widełki orientacyjne dopiero po zbadaniu strony), bez listy funkcji „na wszelki wypadek”.
RESEARCH_POTRZEBNY: TAK — po pytaniu 1 wejść na pokewars.pl, sprawdzić: czy mapa>lokacje jest w DOM, czy w canvas; jak wygląda żądanie po kliknięciu walki; regulamin dot. automatyzacji. Publicznie (przed kontaktem): zerknąć na stronę, sprawdzić czy rejestracja jest otwarta i czy widać strukturę frontu.
```