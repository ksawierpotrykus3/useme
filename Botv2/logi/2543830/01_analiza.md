```
KWALIFIKOWALNOSC: TAK

TYP_ZLECENIA: doradcze (konsultacja 2-3 spotkania online, łącznie 2-3h + rekomendacja rozwiązania)

INTENCJA: doradcze (wprost: "Nie szukam wykonawcy")

DECYDENT_I_BOL: Osoba budująca produkt/system (founder/CTO/product owner w stolarce otworowej albo software house robiący to dla klienta z branży). Pisze językiem pół-technicznym — zna pojęcia (few-shots, fine-tuning, pre-processing, segmentation, bounding-box, Gemini 3 PRO), ale myli bounding z "bonding". Prawdopodobnie decydent techniczny lub blisko produktu. Ból: 70% dokładności na rysunkach blokuje wartość produktu — nie da się tego wypuścić na klienta. Chce wiedzieć, w którą gałąź inwestować czas/pieniądze, żeby nie przepalić 2 miesięcy na złą drogę.

WYKONALNE: TAK. Można zaproponować architekturę i wycenić spotkania.

POLE_DO_POPISU: JEST. Klient wprost zaprasza ("ewentualnie zaproponowanie rozwiązania"). Ma lukę widoczną już na poziomie opisu: jeden pipeline (Gemini 3 PRO + few-shots + prompt) próbuje obsłużyć trzy fundamentalnie różne typy inputu — PDF z programu do wycen, rysunek architekta, odręczny szkic. To nie jest problem modelu, to problem architektury.

SCIEZKA_MERYTORYKI: A (klient pyta wprost o propozycję) + B (mina architektoniczna z dowodem ze zlecenia)

MINY_I_CIEKAWOSTKI:
1. **Jeden model na trzy typy inputu.** Klient sam wymienia: PDF z wycen (rysunek + tabela), rysunki architektów, odręczne szkice. To trzy różne dystrybucje obrazu. Gemini 3 PRO + few-shots na całym miksie → sufit 70%. Nie da się wycisnąć więcej z jednego modelu, bo "optymalny prompt" dla skanu i dla wektorowego PDF-a wykluczają się. To jest mina z dowodem wprost ze zlecenia.
2. **PDF z programu do wycen to najprawdopodobniej PDF wektorowy.** Rysunek jest wektorem, tabela jest strukturą. Puszczanie tego przez VLM/OCR to marnowanie dokładności — na tym kanale można zejść do ~95-100% bez OCR, przez parsowanie geometrii i tabeli bezpośrednio z PDF-a. Dowód: "wyceny generowane przez programy do wycen — kilku stronicowy plik pdf z rysunkiem okna oraz tabelą informacyjną". (Założenie o wektorowości — sformułować warunkowo, zweryfikować pytaniem.)
3. **Rozdzielczość.** VLM (w tym Gemini) downsample'uje input do swojego limitu kafli/rozdzielczości. Rysunek okna z detalami kwater i kierunku otwierania na wielostronicowym PDF traci detale, zanim model w ogóle je zobaczy. Dlatego 70% może być artefaktem pre-processingu, nie modelu. Dowód: "kilku stronicowy plik pdf" + "70%".
4. **Trzy klasy otwierania vs jeden prompt.** Liczba kwater / sposób otwierania / kierunek otwierania to tak naprawdę trzy osobne zadania klasyfikacyjne na wycinku rysunku. Wrzucanie ich do jednego promptu obniża dokładność każdego z nich.

ODMOWA:
Typ 1 (brak kanału dostępu) — warunkowo. Jeśli klient planuje fine-tuning konkretnie Gemini 3 PRO, trzeba zweryfikować, czy Google w ogóle udostępnia tę operację na tym modelu (historycznie Pro nie był fine-tunowalny przez API, tylko Flash). To NIE wchodzi jako twierdzenie — wchodzi jako pytanie/uwaga. Reszta zakresu bez odmowy.

PYTANIA:
1. **Jak liczycie te 70%?** Per rysunek, per pole (osobno kwatery, osobno kierunek), per dokument? — Bez tego nie da się zdefiniować "poprawy" ani ocenić, którą ścieżką iść. Zmienia rekomendację: inny problem przy 70% per pole, inny przy 70% per okno.
2. **Czy macie zbiór ground-truth — ręcznie zweryfikowane rysunki z poprawnymi etykietami?** — To rozstrzyga, czy fine-tuning jest w ogóle mierzalny, czy wchodzimy w projekt bez termometru. Pytanie wykrywacz, nie wycenowe, ale fundamentalne dla rekomendacji.
3. **Czy PDF-y z programów do wycen są wektorowe, czy to skany?** — Warunkuje, czy na tym kanale w ogóle potrzebny jest OCR, czy wystarczy parser.

(Pytanie o budżet — odrzucone. Pytanie o szczegóły formatu materiałów — odrzucone, klient sam wyśle wybranym.)

CO_ZLECENIE_MOWI:
- Buduje system analizy rysunków i dokumentów technicznych dla stolarki otworowej (okna, drzwi, drzwi balkonowe).
- Input: PDF-y z programów do wycen (rysunek + tabela), rysunki architektów, odręczne szkice.
- Cel: wysoka dokładność analizy rysunku okna (kwatery, sposób otwierania, kierunek otwierania).
- Obecnie: Gemini 3 PRO + few-shots + szczegółowy prompt, ~70%.
- Rozważa: fine-tuning, pre-processing, segmentacja, bounding-box.
- Nie szuka wykonawcy. Chce 2-3 spotkania online, łącznie 2-3h + wskazanie rozwiązania.
- Prosi o wycenę spotkań i info o doświadczeniu. Wybranym wyśle materiały.

CZEGO_NIE_MOWI:
- Czym liczy 70% (per co? na jakim podzbiorze?).
- Czy ma ground-truth / test set.
- Czy PDF-y są wektorowe czy rastrowe.
- Skali (ile dokumentów, ile dziennie, docelowo).
- Czy to produkcja czy POC.
- Czy chce też wsparcia przy wdrożeniu, czy tylko wskazania kierunku.
- Jakiego rzędu budżet na "rozwiązanie" po spotkaniach.
- Czy "kilku stronicowy PDF" to 2 strony czy 40.

GRANICA_CIECIA:
Długość: krótko. Doświadczenie (2-3 zdania konkretu, nie CV) + jednozdaniowa synteza podejścia (sygnał "wiem, o czym mówicie") + wycena spotkań + 2 pytania. NIE pisać elaboratu technicznego w ofercie — klient jest pół-ekspertem, zweryfikuje, a jednocześnie jest to doradcze zlecenie na 2-3h, więc pełna diagnoza należy do płatnych spotkań, nie do oferty. Cienka granica: pokazać, że mamy w głowie architekturę, ale nie oddawać jej za darmo. Głębokość: jedna teza architektoniczna (routing po typie dokumentu), nie pełny pipeline.

RESEARCH_POTRZEBNY: TAK.
- Aktualna dostępność fine-tuningu Gemini 3 PRO przez API (i ewentualnie Vertex).
- Aktualne limity rozdzielczości / kafli Gemini 3 PRO dla inputu wizualnego.
- Czy na rynku są wyspecjalizowane modele do detekcji symboli architektonicznych (YOLO variants, document AI, LayoutLM itp.) — żeby mieć alternatywę do zaproponowania.
Po co: żeby nie postawić tezy, której klient nie może sfalsyfikować, i nie dać się złapać na szczegółach technicznych podczas spotkania.
```