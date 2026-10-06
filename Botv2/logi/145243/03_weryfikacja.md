KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: jednorazowa sesja wsparcia zdalnego (video + udostępnianie ekranu) — rozplątanie trzech narzędzi; mieszane wykonawczo-doradcze, bliżej wykonawczej (praca na jej ekranie), ale z diagnozą na wierzchu
INTENCJA: mieszane — mówi "zróbcie to z mojego poziomu", ale realnie kupuje diagnozę: "pogubiłam się, powiedzcie którą drogą iść"
DECYDENT_I_BOL: Ona sama (osoba prywatna, nietechniczna — "pogubiłam się", "to nie dla mnie"). Ból jawny: utopiła czas w trzech narzędziach i nie wie, które zostawić. Ból pod spodem: chce kogoś, kto powie "zostaw X, idź Y" — bo sama się w tym nie odnajdzie.
WYKONALNE: TAK — sesja zdalna z udostępnianiem ekranu, na jej poziomie. To najprostszy i najwłaściwszy tryb dla tego zlecenia.
POLE_DO_POPISU: JEST — rozplątanie Squarespace vs Netlify vs Stripe. Ona tego nie wie, my to wiemy.
SCIEZKA_MERYTORYKI: B (mina — ale podana warunkowo, nie kategorycznie; patrz niżej)
MINY_I_CIEKAWOSTKI:
- WARUNKOWA TEZA (dowód: klientka w jednym zdaniu wymienia trzy systemy i łączy je w jeden pipeline — "strona na Sqaurespace" + "dodałam projekt przez Netlify" + "chciałam podłączyć Stripe"). Squarespace sam buduje i hostuje strony, a jego Commerce ma Stripe wbudowanego. Netlify hostuje strony kodowe — to inny świat niż Squarespace. Jeśli "projekt przez Netlify" to próba tej samej strony, którą buduje w Squarespace, to Netlify jest tu najpewniej zbędny, a Stripe podłącza się bezpośrednio w Squarespace. Skutek: czas i ewentualne koszty Netlify idą na darmo. Falsyfikowalne: "jeśli na Netlify masz coś osobnego — np. podstronę czy landing — dostroję". Nie straszę, tylko pokazuję prostszą drogę.
- CIEKAWOSTKA: "dodałam projekt przez Netlify" przy stronie Squarespace to najpewniej ŹRÓDŁO zamieszania, nie osobny problem do naprawy.
- UWAGA do poprzedniej wersji: w iteracji 1 napisałem "Netlify jest tu prawdopodobnie zbędny" — to było zgadywanie bez dowodu, co jest na Netlify. Naprawiam: zamieniam na tezę WARUNKOWĄ z falsyfikatorem.
ODMOWA: puste — żadna z 6 okazji nie zachodzi (Stripe i Squarespace mają kanały dostępu, brak twardych limitów, brak konfliktu zakresu do przepisania, brak compliance, nazwy narzędzi istnieją, brak bariery autorskiej). Ewentualny "konflikt zakresu" (łączenie Squarespace + Netlify) jest hipotezą, nie faktem — zostaje w tezie warunkowej.
PYTANIA (max 3, TYP 1, każde z uzasadnieniem):
1. Jaki ma być efekt końcowy — strona ze sklepem/płatnościami (Stripe), czy prosta strona/wizytówka? Pytam, bo od tego zależy, czy Stripe i Netlify są w ogóle potrzebne, czy wystarczy sama strona w Squarespace.
2. Co dokładnie stoi na Squarespace, a co wrzuciłaś na Netlify — czy to próba tej samej strony, czy dwie osobne rzeczy? Pytam, bo bez tego nie wiem, czy rozplątujemy jeden projekt, czy dwa, i czy sesja wystarczy na godzinę, czy trzeba więcej.
(Pytanie o budżet — odrzucone. Pytanie o technologię — odrzucone, to TYP 2, proponujemy. Pytanie "porozmawiajmy" — odrzucone, przegrywa z pytaniem.)
CO_ZLECENIE_MOWI: tworzy stronę na Squarespace; dodała projekt przez Netlify; chciała podłączyć Stripe; uznała, że to nie dla niej; chce pomocy zdalnie, najlepiej video + udostępnianie ekranu, z jej poziomu; inne rozwiązania też przyjmie; budżet do negocjacji.
CZEGO_NIE_MOWI: co konkretnie zbudowała i w jakim stanie; jaki jest efekt końcowy (sklep? wizytówka?); czy Squarespace ma zostać bazą; co ma być przedmiotem płatności Stripe; skala, termin, jak długo nad tym siedzi.
GRANICA_CIECIA: brief to dwa zdania. Odpowiedź krótka. Merytoryka tylko o rozplątaniu Squarespace/Netlify/Stripe (bo stąd całe zamieszanie) — warunkowo, nie kategorycznie, bez budowania architektury na zapas. Max 1–2 pytania, nie ankieta. Konkretna propozycja sesji na końcu.
RESEARCH_POTRZEBNY: NIE — wiedza powszechna (Squarespace hostuje u siebie, Commerce ma natywnego Stripe; Netlify hostuje strony kodowe). Ewentualny lekki check aktualnego stanu integracji Squarespace-Stripe, ale nie jest konieczny.

DECYZJE:
- DOPISAĆ: warunkową tezę o rozjeździe Squarespace/Netlify (falsyfikowalną — "jeśli na Netlify masz coś osobnego, dostroję"), + krótką propozycję trybu: sesja video 1h z udostępnianiem ekranu, na jej poziomie, inne rozwiązania też przyjmiemy.
- ODPOWIEDZIEĆ: dać jej diagnozę ("prawdopodobnie Netlify jest tu zbędny, a Stripe w Squarespace podłącza się bezpośrednio") + zaproponować sesję zdalną jako najprostszą drogę.
- DOPYTAĆ: (1) efekt końcowy — sklep czy wizytówka; (2) co jest na Squarespace a co na Netlify — jedna strona czy dwie osobne rzeczy.