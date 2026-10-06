```
KWALIFIKOWALNOSC: TAK

TYP_ZLECENIA: doradcze — audyt-diagnoza + wskazanie kierunku. 2-3 spotkania online (2-3h łącznie) + rekomendacja rozwiązania. Wprost: "Nie szukam wykonawcy".

INTENCJA: doradcze.

DECYDENT_I_BOL: Osoba budująca system (founder/CTO/product owner stolarki otworowej albo software house dla branży). Pisze pół-technicznie, zna słownictwo (few-shots, fine-tuning, pre-processing, segmentacja, bounding-box, Gemini 3 PRO), myli "bounding" z "bonding" — prawdopodobnie decydent blisko technologii, ale nie ML-engineer. Ból: 70% dokładności blokuje wypuszczenie produktu. Chce wiedzieć, w którą gałąź inwestować, żeby nie przepalić miesięcy na złą drogę. Sygnał: klient jest ekspertem wystarczającym, by zweryfikować tezy — nie stawiamy tez ryzykownych, tylko takie z twardym źródłem.

WYKONALNE: TAK. Można zaproponować architekturę i wycenić spotkania konkretnie (2-3h to zakres klarowny).

POLE_DO_POPISU: JEST — i to mocne, bo research potwierdził trzy twierdzenia, które klient może nie wiedzieć, a które wprost dotykają jego briefu:
1. Fine-tuning Gemini 3 Pro — nie istnieje (dokumentacja Google: tuning nieobsługiwany dla 3.x Pro; SFT tylko dla 3.5 Flash / 3.1 Flash-Lite). Klient wprost wymienia "fine-tuning modelu" jako jedną z dróg.
2. Twardy limit rozdzielczości Gemini (media_resolution: 280/560/1120 tokenów na obraz) — 70% może być artefaktem downsamplingu, nie modelu.
3. Modele dokumentowe (LayoutLM, DocLayout-YOLO) na rysunkach architektonicznych działają GORZEJ niż modele ogólne ("domain interference") — jeśli klient trafi na te nazwy w researchu, to ślepa uliczka.
Reszta (konkretny pipeline, routing, YOLOv8 na symbolach, hybryda detektor+VLM) — do sprzedania na płatnych spotkaniach, nie w ofercie.

SCIEZKA_MERYTORYKI: A (klient pyta wprost o propozycję) + B (jedna mina z twardym dowodem: fine-tuning Gemini 3 Pro).

MINY_I_CIEKAWOSTKI:
1. **Fine-tuning Gemini 3 Pro nie istnieje.** Klient wymienia "fine-tuning modelu" jako rozważaną drogę. Dokumentacja Google Cloud dla rodziny 3.x oznacza tuning jako nieobsługiwany dla wersji Pro; SFT mają tylko 3.5 Flash i 3.1 Flash-Lite. Dowód: wprost w treści ogłoszenia ("Fine-tuning modelu") + dokumentacja Google. Mechanizm: klient może zaplanować budżet i czas na coś, czego nie da się wykonać na jego obecnym modelu. Konsekwencja: zmarnowane tygodnie i budżet. Alternatywa: (a) pozostać na 2.5 Pro (okno się domyka), (b) zejść do 3.5 Flash z SFT, (c) fine-tuning modelu open-weight poza Google — decyzja zależy od tego, co klient w ogóle rozważa. Formuła warunkowa: "jeśli planujecie fine-tuning Gemini 3 Pro, to…".
2. **Limit 1120 tokenów na obraz to twardy sufit Gemini 3 Pro.** Nawet idealny prompt nie ominie downsamplingu. Rysunek okna z detalami kwater i kierunku otwierania na wielostronicowym PDF trafia do modelu w rozdzielczości współdzielonej z całą resztą strony — detale giną PRZED dotarciem do modelu. Dowód: "kilku stronicowy plik pdf" + "70%" + dokumentacja media_resolution. Konsekwencja: część z tych 70% to artefakt pre-processingu, nie słabość modelu — a więc część wysiłku w prompt tuning idzie w próżnię. To otwiera pole na segmentację/cropy (osobne obrazy na okno) i podejście hybrydowe.

(Pozycje odrzucone z iteracji 1:)
- "PDF z programu do wycen jest wektorowy" — ZGADYWANIE, nie mina. Wchodzi jako pytanie TYP 1.
- "Rozdzielenie na trzy klasy otwierania to osobne zadania" — TYP 2 (nasza kompetencja), nie mina. Wchodzi jako propozycja na spotkaniu, nie w ofercie.
- "LayoutLM/DocLayout-YOLO to ślepa uliczka" — klient nie wymienił tych modeli, sami byśmy je wnieśli. To nie jest mina z jego briefu, to nasza wiedza. Zostaje na spotkanie, nie do oferty.

ODMOWA:
Nie pełna odmowa — punktowa korekta kierunku. Typ 5 (nieistniejąca funkcja/tryb): klient rozważa "fine-tuning modelu" na Gemini 3 Pro, gdzie ta operacja nie istnieje. Mechanizm: brak SFT dla 3.x Pro w API/Vertex. Konsekwencja: budżet i czas zaplanowany na coś niewykonalnego. Alternatywa: 3.5 Flash z SFT albo 2.5 Pro (z uwagą o wyłączaniu) albo open-weight poza Google. Ton: rzeczowy, nie negujemy briefu — akceptujemy 90% zakresu, korygujemy jeden punkt.

PYTANIA (3, wszystkie TYP 1):
1. **Jak liczycie te 70%?** Per rysunek, per pole (osobno kwatery, osobno kierunek otwierania), per dokument? — Bez tego nie da się zdefiniować "poprawy" ani ocenić, którą ścieżką iść. Inny problem przy 70% per pole, inny przy 70% per okno.
2. **Czy macie zbiór ground-truth — ręcznie zweryfikowane rysunki z poprawnymi etykietami?** — Rozstrzyga, czy fine-tuning jest w ogóle mierzalny i czy da się rzetelnie porównać rozwiązania. Bez termometru każda rekomendacja jest w ciemno.
3. **Czy PDF-y z programów do wycen są wektorowe, czy to skany?** — Warunkuje, czy dla tego kanału w ogóle potrzebny jest OCR, czy wystarczy parser geometrii i tabeli. Zmienia architekturę i wycenę docelową.

(Odrzucone pytania: o budżet — handlowe; o szczegóły materiałów — klient sam wyśle; o liczbę dokumentów/skali — nie zmienia rekomendacji dla 2-3h konsultacji.)

CO_ZLECENIE_MOWI:
- Budowa systemu analizy rysunków i dokumentów technicznych dla stolarki otworowej.
- Input: PDF-y z programów do wycen (rysunek + tabela, kilku stronicowe), rysunki architektów, odręczne szkice.
- Cel: wysoka dokładność na rysunku okna — liczba kwater, sposób otwierania, kierunek otwierania.
- Obecnie: Gemini 3 PRO + few-shots + szczegółowy prompt, ~70%.
- Rozważa: fine-tuning, pre-processing, segmentacja, bounding-box.
- Nie szuka wykonawcy. Chce 2-3 spotkania online (2-3h) + wskazanie rozwiązania.
- Prosi o: doświadczenie w podobnych projektach, propozycję rozwiązania, wycenę spotkań.
- Wybranym wyśle materiały.

CZEGO_NIE_MOWI:
- Czym liczy 70% (per co, na jakim zbiorze).
- Czy ma ground-truth.
- Czy PDF-y są wektorowe czy rastrowe.
- Skali (ile dokumentów, ile dziennie, produkcja czy POC).
- Czy rozważa zejście z Gemini 3 Pro (istotne wobec braku SFT dla 3.x Pro).
- Jakiego rzędu budżet po spotkaniach.
- Ilu kwater / jak złożone rysunki (choć to można wywnioskować z materiałów, które wyśle).

GRANICA_CIECIA:
Długość: krótka. Doświadczenie (2-3 zdania konkretu, nie CV) + jedna mina (fine-tuning Gemini 3 Pro — bo klient wprost wymienił) + jedna teza architektoniczna (routing po typie dokumentu, bo trzy różne dystrybucje w jednym pipeline) + wycena spotkań + 2 pytania (70% metryka, ground-truth). Trzecie pytanie (vector/raster) — na granicy; wrzuciłbym je, bo realnie zmienia architekturę, ale jeśli oferta robi się długa, to jest pierwsze do wycięcia. NIE oddajemy reszty diagnozy (limit 1120 tokenów, domain interference, YOLOv8, hybryda detektor+VLM) — to należy do płatnych spotkań. Głębokość: sygnał "wiemy, gdzie jest problem", nie "oto rozwiązanie".

RESEARCH_POTRZEBNY: NIE. Research z iteracji 1 wystarcza — dostarczył trzy twarde fakty potwierdzone źródłami. Dalszy research przed ofertą nie zmieni treści; materiały klienta i tak przyjdą po wyborze.

DECYZJE:
- DOPISAĆ w ofercie:
  - Wycena konkretna za 2-3h konsultacji (np. 1200-1500 PLN za całość, lub stawka 400-500 PLN/h × 3h = 1200-1500 PLN). Klarowne, więc liczba, nie widełki.
  - Doświadczenie w projektach VLM/OCR/dokumentów (bez zmyślania — jeśli brak wprost stolarki, to VLM na dokumentach technicznych / detekcja symboli).
  - Mina: "Jeśli planujecie fine-tuning Gemini 3 Pro — to nie jest obecnie możliwe; SFT dla rodziny 3.x Pro nie istnieje, alternatywy to 3.5 Flash albo model open-weight" (z zastrzeżeniem warunkowym).
  - Teza architektoniczna: trzy różne dystrybucje inputu (PDF z wyceny / rysunek architekta / szkic) w jednym pipeline = sufit dokładności. Routing po typie dokumentu jako pierwszy krok.
  - Krótka propozycja rozwiązania (klient wprost prosi) — na poziomie "co bym sprawdził na spotkaniu", nie pełny pipeline.
- ODPOWIEDZIEĆ: 
  - Tak, podejmuję się konsultacji, wycena X.
  - Zaproponować termin i formę (2-3 spotkania online).
- DOPYTAĆ:
  - Jak liczone jest 70% (per rysunek / per pole / per dokument)?
  - Czy jest ground-truth?
  - (opcjonalnie) Czy PDF-y z wycen są wektorowe czy rastrowe?
```