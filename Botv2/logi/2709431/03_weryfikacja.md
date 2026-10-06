```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy — naprawa integracji (diagnoza + przywrócenie synchronizacji + rekomendacja)
INTENCJA: wykonawcze (główny ciężar: naprawa i weryfikacja), z elementem doradczym na końcu (rekomendacja stabilności)
DECYDENT_I_BOL: właściciel/manager sklepu Shopify. Ból realny, nie techniczny: brak produktów w Google Shopping = brak ruchu i sprzedaży z Google. Warstwa techniczna to tylko objaw. Support Shopify odbił piłkę → klient ma poczucie, że został sam.
WYKONALNE: TAK. Diagnoza i naprawa przez dostęp do Shopify + GMC; sprawdzenie stanu konta GMC, uprawnień OAuth, konfiguracji aplikacji, feedu i konfliktów z innymi aplikacjami. Jeśli przyczyna okaże się nieustalalna — przywrócić synchronizację i zabezpieczyć monitoringiem.
POLE_DO_POPISU: JEST — doświadczenie z rozłączeniami Shopify–GMC, świadomość że przyczyna bywa po stronie GMC (zawieszenia, ostrzeżenia, konflikt domeny, wielokrotne konta) lub po stronie cyklu życia tokenów OAuth, a nie samej aplikacji. Ale to NIE wchodzi jako teza — wchodzi jako zakres diagnostyki.
SCIEZKA_MERYTORYKI: ZADNA. Klient nie zadaje nam pytania „co jest przyczyną" — zleca naprawę. Odpowiedź na to pytanie jest przedmiotem zlecenia, nie gratisem w ofercie. Zakres prac opisujemy jako element oferty, nie jako ścieżkę A/B/C.
MINY_I_CIEKAWOSTKI: puste. Iteracja 1 miała dwie kandydatury, obie odrzucone:
  - „Jeśli problem jest po stronie GMC, sama aplikacja go nie naprawi" — warunek „jeśli" + brak dowodu ze zlecenia, że problem JEST po stronie GMC. To nie mina, to hipoteza. Zamienione na pytanie 1.
  - „Aplikacja ma ograniczone logi" — fakt ogólny, nie dotyka klienta osobiście, nie zmienia decyzji. Wypada.
  Research potwierdził, że zjawisko jest znane i wieloprzyczynowe, ale nie dał dowodu na KONKRETNĄ przyczynę w tym przypadku. Bez dowodu — żadnej tezy.
ODMOWA: puste. Brak okazji do odmowy: Shopify API i GMC istnieją, brak limitów zewnętrznych łamiących zakres, brak konfliktu prawnego ani zakresowego.
PYTANIA:
1. Czy w Google Merchant Center konto jest aktywne, czy widoczne są ostrzeżenia lub zawieszenie? Pytam, bo od tego zależy, czy naprawa sprowadza się do samej aplikacji, czy obejmuje też odwołanie i poprawę danych w GMC — to istotnie zmienia zakres i czas.
2. Czy problem dotyczy wszystkich produktów, czy tylko części? Pytam, bo „wszystkie" wskazuje na warstwę połączenia/uprawnień, a „część" na warstwę feedu lub atrybutów — inne miejsce diagnozy.
3. Ile produktów i wariantów jest w sklepie? Pytam, bo wolumen wpływa na czas weryfikacji synchronizacji i orientacyjną wycenę.
4. Czy oprócz aplikacji Google & YouTube używacie innych aplikacji do feedów lub Google Ads? Pytam, bo konflikt uprawnień między integracjami bywa przyczyną rozłączenia i zmienia kolejność diagnozy.
CO_ZLECENIE_MOWI: Shopify; Google Merchant Center; aplikacja Google & YouTube; integracja rozłączyła się samoistnie; standardowa aplikacja nie pozwala przywrócić połączenia; support bez pomysłu; zakres: diagnostyka, sprawdzenie konfiguracji, weryfikacja przez API, przywrócenie synchronizacji, sprawdzenie produktów, wskazanie przyczyny (jeśli ustalalna), rekomendacja stabilizacji; wymagane doświadczenie z integracjami i feedami.
CZEGO_NIE_MOWI: statusu konta GMC; liczby produktów; czy problem dotyczy całości czy części asortymentu; czy używane są inne aplikacje feed; czy zmieniała się domena lub uprawnienia; czy jest Google Ads; konkretnego budżetu; dokładnych dostępów.
GRANICA_CIECIA: krótka oferta — potwierdzenie doświadczenia z podobnymi rozłączeniami, zarys procesu diagnostycznego w 4–5 punktach, widełki orientacyjne z otwartością na dopasowanie po poznaniu stanu GMC i wolumenu, 4 pytania. Bez wykładu o przyczynach, bez straszenia zawieszeniem konta, bez listy „możliwych przyczyn" — tego nie wiemy.
RESEARCH_POTRZEBNY: NIE. Research z iteracji 1 potwierdził jedynie, że problem jest znany i wieloprzyczynowy — nie dał dowodu na konkretną przyczynę w tym zleceniu ani nie zmienił pytań. Proces diagnostyczny wynika z wiedzy własnej i doświadczenia, nie z researchu.

DECYZJE:
- DOPISAĆ do oferty: potwierdzenie doświadczenia z rozłączeniami Shopify–GMC; krótki zarys procesu diagnostycznego (stan konta GMC → uprawnienia OAuth → konfiguracja aplikacji → domena → inne integracje → feed); widełki orientacyjne + otwartość; 4 pytania z uzasadnieniem.
- ODPOWIEDZIEĆ: nie wykładać teorii przyczyn w ofercie — to jest przedmiot zlecenia. Ton spokojny, rzeczowy: „tak, robiłem to, wiem gdzie patrzeć".
- DOPYTAĆ: pytania 1–4 jak wyżej. Żadne inne — reszta wychodzi po dostępie.
```