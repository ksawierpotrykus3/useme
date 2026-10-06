KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: jednorazowa sesja wsparcia zdalnego (rozplątanie narzędzi) — mieszane wykonawczo-doradcze, cięższe w stronę wykonawczej (praca na jej ekranie)
INTENCJA: mieszane — chce, żeby ktoś "to zrobił z jej poziomu", ale realnie potrzebuje też diagnozy, którą ścieżką iść
DECYDENT_I_BOL: Ona sama (osoba prywatna, nietechniczna — "pogubiłam się", "to nie dla mnie"). Ból: utopiła czas w trzech narzędziach naraz, nie wie, którą drogą iść, chce, żeby ktoś to poskładał. Ból pod spodem: brak kogoś, kto powie "zostaw to, idź tędy".
WYKONALNE: TAK — sesja zdalna z udostępnianiem ekranu, na jej poziomie. To realnie najprostszy i najwłaściwszy tryb dla tego zlecenia.
POLE_DO_POPISU: JEST — rozplątanie Squarespace vs Netlify vs Stripe. Klientka jest w tym pogubiona, a to dokładnie ta wiedza, której jej brakuje.
SCIEZKA_MERYTORYKI: B (mina)
MINY_I_CIEKAWOSTKI:
- MINA (dowód: klientka sama nazywa trzy systemy i łączy je w jeden pipeline — "strona na Squarespace" + "projekt przez Netlify" + "podłączyć Stripe"). Squarespace buduje i hostuje strony u siebie i ma natywną integrację Stripe w Commerce; Netlify hostuje strony kodowe. To dwa rozłączne światy — projektu Squarespace nie wdraża się przez Netlify, a Stripe w Squarespace podłącza się bezpośrednio, bez Netlify. Skutek: czas (i ewentualne koszty Netlify) idą na darmo, bo Netlify jest tu prawdopodobnie zbędny. Alternatywa: wybrać JEDNĄ ścieżkę — albo Squarespace z jego Stripe, albo Netlify (wtedy Stripe integruje się ręcznie/kodem).
- CIEKAWOSTKA: "dodałam projekt przez Netlify" przy stronie Squarespace to najpewniej źródło całego zamieszania, nie osobny problem do naprawy.
ODMOWA: puste (żadna z 6 okazji do odmowy nie zachodzi — brak kanału dostępu / twardy limit / konflikt zakresu / compliance / nieistniejący termin / bariera autorska)
PYTANIA (max 3, wykrywacze — od nich zależy, co w ogóle rozplątujemy):
1. Co ma być efektem — strona ze sklepem i płatnościami (Stripe), czy zwykła strona/wizytówka? Pytam, bo od tego zależy, czy Stripe i Netlify są w ogóle potrzebne.
2. Co konkretnie już stoi: strona na Squarespace jest gotowa/w budowie, a co dokładnie wrzuciłaś na Netlify? Pytam, bo bez tego nie wiem, czy rozplątujemy jeden projekt, czy dwa osobne.
CO_ZLECENIE_MOWI: tworzy stronę na Squarespace; dodała projekt przez Netlify; chciała podłączyć Stripe; uznała, że to nie dla niej; chce pomocy zdalnie, najlepiej video + udostępnianie ekranu, z jej poziomu; inne rozwiązania też przyjmie; budżet do negocjacji.
CZEGO_NIE_MOWI: co konkretnie zbudowała i w jakim stanie; jaki jest efekt końcowy (sklep? wizytówka?); czy Squarespace ma zostać bazą; jaki produkt/przedmiot płatności; skala i termin.
GRANICA_CIECIA: brief to dwa zdania — odpowiedź krótka. Merytoryka tylko o rozplątaniu Squarespace/Netlify/Stripe (bo stąd całe zamieszanie), bez budowania architektury na zapas. Max 1–2 pytania, nie ankieta.
RESEARCH_POTRZEBNY: NIE — to wiedza powszechna (Squarespace hostuje u siebie i ma natywny Stripe; Netlify hostuje strony kodowe). Ewentualnie lekki check aktualnego stanu integracji, ale nie jest konieczny do odpowiedzi.