# PLAN NAPRAWY PROMPTÓW — propozycje zmian do akceptacji

> Dokument propozycji. NIC tu nie jest jeszcze wdrożone. Każda zmiana ma: plik, sekcję, stan obecny, propozycję, uzasadnienie i status decyzji (DO DECYZJI / GOTOWE).
> Źródło: 4 raporty subagentów (research, wycena, dopytanie, spójność) + analiza 12 sprzeczności.

---

## JAK CZYTAĆ

- **GOTOWE** — zmiana oczywista, nie wymaga Twojej decyzji, można wdrażać.
- **DO DECYZJI** — wymaga Twojego wyboru (kierunek projektowy), bo są 2+ sensowne opcje.
- Kolejność: najpierw Grupa A (realnie psuje oferty), potem B–E, na końcu F–G (dopieszczenie).

---

## GRUPA A — TRZY SZKODLIWE SPRZECZNOŚCI (najwyższy priorytet)

### A1. Etapy: agent_00 pozwala, mechanika zakazuje
**Pliki:** `generatory/agent_00_orchestrator.md` pkt 2 vs `kontekst/mechanika_wyceniania.md` KROK 9.5
**Obecnie:**
- agent_00: "Zaproponuj podział na etapy tylko wtedy, gdy projekt jest większy i wieloczęściowy"
- mechanika: "zakaz samowolnego dzielenia projektu na Fazę 1 / małe MVP, chyba że klient wprost w ogłoszeniu poprosił"

**Problem:** agent_00 autoryzuje etapy przy dużych projektach, mechanika je blokuje bez prośby klienta. Sprzeczne.

**Propozycja (GOTOWE):** Zostawić zakaz z mechaniki jako nadrzędny, poprawić agent_00 na:
> "Podział na etapy tylko wtedy, gdy klient SAM o to wprost poprosił w ogłoszeniu. Sam nie proponuj etapowania na siłę. Przy dużych projektach możesz wspomnieć, że chętnie rozłożysz pracę, ale decyzję zostaw klientowi."

**Uzasadnienie:** zakaz z mechaniki jest spójny z realiami wyceny (wycena pełnego zakresu, brak wypychania do wersji drugiej). agent_00 musi być z nim zgodny.

---

### A2. Zakończenie oferty: agent_08 wymaga pytania, agent_02a dopuszcza brak
**Pliki:** `walidatory/agent_08_weryfikacja_zasad.md` pkt 11 vs `generatory/agent_02a_opis_oferty.md` sekcja ZAKOŃCZENIE
**Obecnie:**
- agent_08: "Brak naturalnego pytania na końcu oferty → ZŁAMANE"
- agent_02a: zakończeniem może być "zaproszenie do rozmowy bez konkretnego zadania"

**Problem:** agent_08 odrzuca ofertę, którą agent_02a uznaje za poprawną. Bot wpada w pętlę poprawek, gdy nie ma o co pytać.

**Propozycja (DO DECYZJI):** Dwie opcje:
- **Opcja 1 (twardsza):** agent_02a ZAWSZE pisze pytanie; usuwamy "zaproszenie bez zadania". Ryzyko: bot pyta na siłę, gdy nie ma realnej luki.
- **Opcja 2 (zdrowsza):** agent_08 zmienia wymóg na: "Oferta kończy się pytaniem wynikającym ze zlecenia LUB, gdy klient dał wszystko, naturalnym zakończeniem bez pytania. Brak jakiegokolwiek zakończenia → ZŁAMANE."

**Moja rekomendacja:** Opcja 2. Bo gdy klient dał komplet informacji, pytanie na siłę brzmi jak desperacja (sprzeczne z filozofią agent_02a).

---

### A3. Merytoryka ZERO vs uzasadnienie ceny
**Pliki:** `generatory/agent_02a_opis_oferty.md` vs `kontekst/mechanika_wyceniania.md`
**Obecnie:**
- agent_02a: "W każdym innym przypadku: ZERO merytoryki"
- mechanika: "Dla zleceń które naturalnie wychodzą poniżej 500 zł uczymy się pisać oferty tak, żeby uzasadnić tę kwotę"

**Problem:** jedna reguła każe milczeć, druga każe pisać uzasadnienie ceny. Konflikt przy tanich zleceniach.

**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja STRUKTURA:
> "Wyjątek od ZERO merytoryki: gdy kwota jest niska (poniżej 1000 zł) albo mocno odbiega od tego, co klient mógłby oczekiwać, masz prawo i obowiązek uzasadnić ją jednym zdaniem. Nie architekturą, tylko zakresem: co dokładnie wchodzi w cenę. To nie jest merytoryka, to wyjaśnienie wartości."

**Uzasadnienie:** godzi dwie reguły bez łamania "ZERO merytoryki" w normalnych przypadkach.

---

## GRUPA B — WSPÓLNY KONTRAKT PRZEKAZANIA (fundament spójności)

### B1. Orchestrator planuje merytorykę przed researchem
**Plik:** `generatory/agent_00_orchestrator.md` pkt 2 "CO PASUJE DO TEGO ZLECENIA"
**Obecnie:** agent_00 każe zaplanować "które 1 lub 2 konkrety merytoryczne warto poruszyć" — ale działa PRZED agent_01, więc nie zna jeszcze min.
**Problem:** plan merytoryczny powstaje w ciemno. Research przynosi minę, której orchestrator nie widział.

**Propozycja (DO DECYZJI):** Dwie opcje:
- **Opcja 1:** Przenieść agent_01 (research) PRZED agent_00. Orchestrator widzi miny i planuje z nimi.
- **Opcja 2:** Zmienić rolę agent_00 — niech planuje tylko "co ZABLOKOWAĆ" i "o co klient pyta", a decyzję "co dopisać" odda agentowi_02a, który dostaje research.

**Moja rekomendacja:** Opcja 2. Mniejsza zmiana, agent_00 i tak jest "reżyserem blokad", nie "planistą merytoryki".

---

### B2. Wycena odcięta od narracji
**Pliki:** `generatory/agent_02b_wycena_dni.md` → `generatory/agent_02a_opis_oferty.md`
**Obecnie:** 02b liczy moduły i flagi, ale 02a nie wie, dlaczego wyszła taka kwota. Pisarz dostaje tylko `[WYNIK_KONCOWY]`.
**Problem:** brak związku "co klient napisał → ile to kosztuje → jak to opisujemy".

**Propozycja (GOTOWE):** Dodać do agent_02a sekcję "JAK WPIĄĆ WYCENĘ":
> "Dostajesz z 02b pole `uzasadnienie` i flagi. Jeśli cena jest pod 1000 zł albo mocno odbiega od rynku, wpleć jedno zdanie wyjaśnienia (patrz A3). W pozostałych przypadkach nie tłumacz ceny — po prostu ją podaj."

---

### B3. Pytania z mechaniki KROK 11 nie trafiają do agent_02a
**Pliki:** `kontekst/mechanika_wyceniania.md` KROK 11 → `generatory/agent_02a_opis_oferty.md`
**Obecnie:** mechanika ma gotowe pytania per typ zlecenia ("Ile SKU?", "W jakim formacie pliki?"), ale agent_02a ich nie zna.
**Problem:** wiedza o dobrych pytaniach zostaje w mechanice, pisarz wymyśla od zera.

**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja ZAKOŃCZENIE:
> "Masz pulę dobrych pytań z mechaniki wyceniania (KROK 11). To PULA DO WYBORU, nie lista do wypełnienia. Wybierz JEDNO najważniejsze dla tego zlecenia. Reszta zostaje na rozmowę priv."

---

## GRUPA C — LIMIT PYTAŃ I DEFINICJA "NAJWAŻNIEJSZE"

### C1. Brak limitu pytań
**Plik:** `generatory/agent_02a_opis_oferty.md` sekcja ZAKOŃCZENIE
**Obecnie:** "pytanie wynikające ze zlecenia" (liczba pojedyncza, ale nie twardy limit). Dowód: oferta 144737 zadała 4 pytania.
**Propozycja (GOTOWE):** Dopisać twardy limit:
> "Maksymalnie JEDNO pytanie CTA w ofercie publicznej. Jeśli widzisz kilka luk, wybierz tę, która najbardziej zmienia zakres lub wycenę. Resztę zadaj w wiadomości prywatnej albo zostaw na później."

---

### C2. Brak definicji "najważniejsze"
**Plik:** `generatory/agent_02a_opis_oferty.md`
**Obecnie:** "bez czego nie da się ruszyć" — dobre, ale nieostre przy 5 lukach.
**Propozycja (GOTOWE):** Dopisać definicję:
> "Najważniejsze pytanie to takie, którego brak odpowiedzi uniemożliwia podanie wiążącej kwoty albo rozpoczęcie pracy. Jeśli dwie luki wydają się równie ważne, wybierz tę, która bardziej zmienia wycenę."

---

### C3. Wyciek calli mimo zakazu
**Pliki:** `generatory/agent_02a_opis_oferty.md` zakaz #7, `walidatory/agent_08` WYMIAR C
**Obecnie:** zakaz #7 zabrania calli, ale 7 z 9 realnych ofert kończy się "zdzwońmy się".
**Problem:** zakaz jest, egzekucji nie ma. Walidator tego nie łapie.

**Propozycja (GOTOWE):** Wzmocnić agent_08 pkt 11:
> "Propozycja rozmowy telefonicznej, calla, spotkania online, Google Meet, Zoom lub wideokonferencji (o ile klient sam tego nie zażądał) → ZŁAMANE z karą -20 pkt. Dotyczy każdej formy: 'zdzwońmy się', 'umówmy się na rozmowę', 'krótki call', 'spotkanie online'."

---

## GRUPA D — BRAMKA RESEARCHU

### D1. Wewnętrzna sprzeczność listy ON/OFF
**Plik:** `generatory/agent_01_research.md` CZĘŚĆ A
**Obecnie:** lista ON ma "duże, złożone zlecenie z realnym budżetem", lista OFF ma "dał materiały i wie dokładnie czego chce". Duże zlecenie z materiałami nie wiadomo, którą listę wybiera.
**Propozycja (GOTOWE):** Dodać priorytet:
> "Gdy zlecenie spełnia kryterium z OBU list jednocześnie, rozstrzyga obecność procesu albo pytania. Jeśli klient opisał proces lub zadał pytanie → ON. Jeśli tylko dał materiały i wie czego chce, bez opisu procesu i bez pytania → OFF. Sama duża skala i budżet to za mało na ON."

---

### D2. quick_fix nieobsłużony w bramce
**Plik:** `generatory/agent_01_research.md` CZĘŚĆ A
**Obecnie:** bramka nie ma kategorii "awaria / konkretny błąd produkcyjny". Quick_fix spłaszcza się do "2 zdania" → OFF.
**Propozycja (GOTOWE):** Dodać do listy ON:
> "Zgłoszenie konkretnej awarii lub błędu produkcyjnego (np. 'błąd 500', 'skrypt pada', 'system nie działa po aktualizacji'). Nawet krótkie, bo konkret błędu to zaproszenie do researchu znanych przyczyn i regresji."

---

### D3. "Nazwa technologii to nie zaproszenie" ucina obiektywne miny
**Plik:** `generatory/agent_01_research.md` CZĘŚĆ A
**Obecnie:** "sama nazwa technologii to NIE jest zaproszenie do merytoryki. Nazwa bez procesu i bez pytania to za mało."
**Problem:** "Chcę scraping z Allegro, 800 zł" → OFF → bot nie powie o anty-scrapingu, choć to obiektywna mina znana dla tej technologii.
**Propozycja (GOTOWE):** Dodać wyjątek:
> "Wyjątek od tej zasady: jeśli technologia z ogłoszenia ma OBIEKTYWNĄ, powszechnie znaną minę niezależną od procesu klienta (np. brak oficjalnego API Allegro, anty-scraping, rate-limit, wymóg licencji), research może być ON nawet bez opisu procesu. Mina obiektywna to nie zgadywanie."

---

### D4. ON przy procesie bez potencjału na merytorykę
**Plik:** `generatory/agent_01_research.md` CZĘŚĆ A
**Obecnie:** "opisał swój proces" → ON, nawet gdy proces jest rutynowy i nie ma min.
**Propozycja (GOTOWE):** Dopisać:
> "Opisany proces to zaproszenie do researchu tylko wtedy, gdy proces ma potencjał na minę, alternatywę albo realne pytanie. Proces rutynowy, bez haczyka, nie wymaga researchu — możesz zwrócić BRAK_ISTOTNYCH_FAKTOW nawet przy ON."

---

## GRUPA E — MOSTEK "WARUNKOWOŚĆ = PYTANIE, NIE WIDEŁKI"

### E1. Brak zdania łączącego wycenę warunkową z pytaniem CTA
**Pliki:** `generatory/agent_02a_opis_oferty.md`, `walidatory/agent_08`
**Obecnie:** prompty zakazują widełek cenowych (słusznie), ale nie mówią wprost "warunkowość wyrażaj pytaniem".
**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja STRUKTURA:
> "Wycena jest jedna, konkretna kwota. Warunkowość wyceny komunikujesz PYTANIEM, nigdy widełkami ceny. Gdy pytasz o brakujący parametr, powiedz wprost, od czego zależy cena: 'od tego zależy, czy zmieścimy się w X czy potrzebne będzie Y'. Ale nadal podaj jedną kwotę, nie widełki."

---

## GRUPA F — ZA SZTYWNE REGUŁY

### F1. Licznik "ludzkich akcentów"
**Plik:** `walidatory/agent_08` pkt 13
**Obecnie:** "więcej niż 2-3 wyraźne ludzkie akcenty → ZŁAMANE"
**Problem:** brzmi jak teatr kontroli nad teatrem, sprzeczne z filozofią "naturalność to brak sztuczności".
**Propozycja (DO DECYZJI):**
- **Opcja 1:** Usunąć licznik, zostawić tylko test "wzorzec bez triggera to teatr".
- **Opcja 2:** Zmienić na miękki sygnał: "Jeśli oferta ma wrażenie przesytu ludzkimi wtrąceniami, wskaż do redukcji — ale nie odrzucaj z tego powodu".

**Moja rekomendacja:** Opcja 1. Licznik jest sprzeczny z duchem promptu.

---

### F2. Absolutny zakaz nawiasów
**Pliki:** `generatory/agent_02a` zakaz #2, `walidatory/agent_08` pkt 2
**Obecnie:** zero nawiasów, kara -20 pkt za jeden.
**Problem:** w zleceniach technicznych "KSeF (XML)" jest naturalne, zakaz zmusza do "KSeF w wersji XML".
**Propozycja (DO DECYZJI):**
- **Opcja 1:** Zostawić absolutny zakaz (spójny, prosty do walidacji).
- **Opcja 2:** Dopuścić nawiasy WYŁĄCZNIE wokół skrótów technicznych (max 1-2 w ofercie), reszta zakazana.

**Moja rekomendacja:** Opcja 1. Zakaz jest spójny i prosty, a "KSeF w wersji XML" da się napisać naturalnie.

---

### F3. Wymuszone pytanie na końcu (powiązane z A2)
**Plik:** `walidatory/agent_08` pkt 11
**Propozycja:** Rozwiązane w A2.

---

### F4. "Merytoryka ZERO" + "ZERO nazw bibliotek" nakładają się
**Plik:** `generatory/agent_02a_opis_oferty.md` sekcja MERYTORYKA + JAK PODAWAĆ MERYTORYKĘ
**Obecnie:** trzy zakazy nakładają się i uniemożliwiają odpowiedź na pytanie techniczne bez nazwania technologii.
**Propozycja (DO DECYZJI):**
- **Opcja 1:** Złagodzić "ZERO nazw bibliotek" na "nazwy bibliotek tylko gdy klient sam je wymienił albo są niezbędne do odpowiedzi na jego pytanie".
- **Opcja 2:** Zostawić jak jest, ale dopisać wyjątek: "Gdy klient zadał pytanie techniczne wprost, odpowiedź może zawierać nazwy technologii, bo inaczej odpowiedź jest wymijająca".

**Moja rekomendacja:** Opcja 2. Mniejsza zmiana, nie łamie zasady "merytoryka domyślnie ZERO".

---

### F5. Binarna flaga `brak_specyfikacji`
**Pliki:** `generatory/agent_02b_wycena_dni.md`, `kontekst/mechanika_wyceniania.md` KROK 5
**Obecnie:** flaga true/false. "Częściowe" (proces + brak 2-3 parametrów) wpada w tę samą kategorię co "kompletne" albo "otwarte".
**Propozycja (DO DECYZJI):**
- **Opcja 1:** Rozszerzyć na trzystanową: `kompletna` / `czesciowa` / `otwarta` z mnożnikami ×0.90 / ×1.0 / ×1.05.
- **Opcja 2:** Dodać drugą flagę `specyfikacja_czesciowa` z osobnym mnożnikiem.

**Moja rekomendacja:** Opcja 1. Czystsze.

---

## GRUPA G — POZOSTAŁE SPRZECZNOŚCI (niższy priorytet)

### G1. Portfolio: trzy różne reżimy w trzech plikach
**Pliki:** `agent_00`, `agent_02a` zakaz #5, `jak_pisac_oferty` pkt 5
**Propozycja (GOTOWE):** Ujednolicić: "Jeśli klient wprost pyta o portfolio, odpowiedz jednym zdaniem: nie mamy publicznego portfolio. W żadnym innym wypadku nie wspominaj o portfolio ani doświadczeniu."

### G2. Kto liczy: AI vs kalkulator
**Pliki:** `agent_02b`, `mechanika_wyceniania` KROK 9.5
**Propozycja (GOTOWE):** Ujednolicić granicę: "AI rozpoznaje zlecenie, dobiera moduły i flagi. Kalkulator liczy kwotę. Decyzję o wariancie A/B dla budżetów 50-250 zł podejmuje AI (agent_02b), kalkulator tylko wykonuje." Dopisać w obu plikach.

### G3. "Tylko JSON" vs "pokaż rozbicie właścicielowi"
**Pliki:** `agent_02b`, `mechanika_wyceniania` KROK 10.6
**Propozycja (GOTOWE):** Dopisać w mechanice: "Rozbicie kalkulatora jest logowane automatycznie przez kod, nie przez agenta. Agent_02b zwraca tylko JSON."

### G4. Koszty serwera: agent_00 zabrania, mechanika podnosi cenę
**Pliki:** `agent_00`, `agent_02b` flaga `ograniczenia_api`
**Propozycja (GOTOWE):** Dopisać w agent_00: "Koszty API mogą wpłynąć na cenę (flaga `ograniczenia_api`), ale w ofercie wspominasz o nich TYLKO gdy klient sam pyta o koszty albo gdy są istotne dla jego decyzji."

### G5. Duplikat sekcji DŁUGOŚĆ w agent_02a
**Plik:** `generatory/agent_02a_opis_oferty.md`
**Propozycja (GOTOWE):** Usunąć duplikat, zostawić jedną wersję.

### G6. Diagnoza, nie recepta vs moduły w mechanice
**Pliki:** `agent_02a`, `mechanika_wyceniania` KROK 1
**Propozycja (GOTOWE):** Nie zmieniać — to napięcie, nie sprzeczność. Dopisać w agent_02a: "Moduły z wyceny są wewnętrzne. W ofercie mówisz o nich językiem korzyści, nie nazwami modułów."

---

## PODSUMOWANIE DECYZJI DO PODJĘCIA

| # | Decyzja | Opcje | Moja rekomendacja |
|---|---|---|---|
| A2 | Zakończenie bez pytania | twarde / miękkie | miękke |
| B1 | Kolejność agent_01 vs 00 | przenieść / zmienić rolę 00 | zmienić rolę 00 |
| F1 | Licznik ludzkich akcentów | usunąć / złagodzić | usunąć |
| F2 | Zakaz nawiasów | zostawić / dopuścić techniczne | zostawić |
| F4 | Nazwy bibliotek przy pytaniu | złagodzić / wyjątek | wyjątek |
| F5 | Flaga specyfikacji | trzystanowa / druga flaga | trzystanowa |

**Zmiany GOTOWE (bez decyzji):** A1, A3, B2, B3, C1, C2, C3, D1, D2, D3, D4, E1, G1, G2, G3, G4, G5, G6.

**Zmiany DO DECYZJI:** A2, B1, F1, F2, F4, F5.