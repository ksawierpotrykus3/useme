# BOT V2 — KROK 2: RESEARCH (plan szczegółowy)

> Status: plan roboczy. Data: 2026-10-05.
> Wejście: krok 1 (analiza) dał ZIELONE ŚWIATŁO, że istnieje pole do popisu, i wskazał ścieżkę (A/B/C).
> Research nie jest osobnym slotem z taśmy. Jest NARZĘDZIEM iteracji 2, uruchamianym świadomie i celowo.
> Uzasadnienia oparte na: teorii warstw, 31 realnych analizach ofert, błędach V1 (backfire).

---

## 0. Po co jest research

Research nie zbiera „amunicji do oferty". Nie buduje ściany faktów. Nie szuka materiału na pochwalenie się wiedzą.

**Research szuka PRAWDY O ŚWIECIE** — rzeczy, których klient może nie widzieć, a które wpływają na jego projekt.

Filozofia: świat i prawda istnieją niezależnie od tego, co myśli klient. Klient ma ograniczony obraz swojej sprawy. Zadanie researchu: znaleźć to, czego jego umysł nie widzi — a potem **zamienić podejrzenie w dowód, a dowód w konkretne zdanie** (albo w ciszę).

**Kluczowa zasada:** research ma potwierdzić albo ZABIĆ hipotezę z analizy. Nie „dokończyć na wszelki wypadek".

---

## 1. GDZIE research mieszka w pętli

- **Iteracja 1 (analiza)** tylko ZGŁASZA zapotrzebowanie: „czy potrzebny research, jaki dokładnie i PO CO". Nie odpala go. Najpierw musi powstać dziennik myślenia z hipotezami.
- **Iteracja 2 (weryfikacja / pogłębienie)** to właściwe miejsce. Model patrzy na własne myślenie krytycznie („czy każda mina ma dowód, czy to domysł") i tu odpala research, żeby domysły zamienić w fakty albo je zabić.
- **Iteracja 3** korzysta z gotowego materiału przy decyzji DOPISAĆ / ODPOWIEDZIEĆ / DOPYTAĆ.

**Dlaczego nie w iteracji 1:** research przed dziennikiem myślenia = research na ślepo (nie wiem, czego szukać i po co). Research w weryfikacji = celowy, ograniczony do hipotez, z jasnym kryterium stopu.

---

## 2. BRAMKA: kiedy research się odpala, a kiedy NIE

### 2.1. Warunek wejściowy (bez niego zawsze OFF)
Krok 1 orzekł: **pole do popisu JEST** i wskazał konkretną ścieżkę A/B/C. Sam fakt „klient użył nazwy technologii" to NIE przesłanka. Nazwa bez procesu i bez pytania to za mało.

### 2.2. Przesłanki ON (wystarczy jedna)
- **A.** Klient WPROST pyta o coś, czego odpowiedź wymaga weryfikacji w świecie („czy X ma wsparcie", „co lepsze", „czy warto migrować").
- **B.** Widzę minę (podejrzewam, że klient może stracić), ale NIE mam na nią dowodu ze zlecenia. Research = próba zdobycia dowodu. Bez dowodu mina wypada, nie zostaje jako domysł.
- **C.** Wykryłem kandydata na ciekawostkę (data końca wsparcia, zmiana API, przepis, limit), która realnie wpływa na decyzję klienta i da się potwierdzić źródłem.
- **D.** Krok 1 (wykonalność) dał niepewność: nie wiem sam, czy to, o co prosi klient, jest wykonalne. Research sprawdza stan faktyczny.

### 2.3. Przesłanki OFF (research się NIE odpala)
- Krok 1 orzekł brak pola do popisu.
- Jedyne sygnały to gdybanie: „jeśli to jest X", „zwykle bywa", „prawdopodobnie" → to MOJE zgadywanie, nie zaproszenie do researchu.
- Klient użył nazwy technologii, ale nie opisał procesu i o nic nie pyta.
- Wiem sam z wiedzy własnej, a dowód jest już w treści zlecenia — research zbędny.
- Research miałby tylko „dodać merytoryki na siłę", żeby oferta była dłuższa.

**Zasada rozstrzygająca wątpliwości: OFF.** Brak researchu kosztuje mniej niż research na siłę (V1 już to spalił).

### 2.4. Wzorzec triggera z realnych danych
Research był potrzebny, gdy w zleceniu była **NAZWA systemu/platformy/technologii** (Booking, .NET, Tempo, TikTok, IdoSell, SAP) ALBO gdy **klient proponował rozwiązanie z ukrytym haczykiem** (import z banku, stawki konkurencji przez API, auto-publish na TikTok).

Research NIE był potrzebny przy: zleceniach emocjonalnych bez technologii (143916), prostych zakresach (144116, 144001), zleceniach widmo bez zakresu (144457, 144470), rolach miękkich (144044), scamach (144036, 144461).

---

## 3. CZEGO szuka research (konkret)

Research szuka prawdy w DWÓCH KIERUNKACH (oba istnieją obiektywnie):

### 3.1. Kierunek negatywny — MINY / HACZYKI
Co może klienta zabić albo narazić na stratę:
- **Wersje wsparcia i lifecycle** („.NET 8 kończy wsparcie XI 2026").
- **Licencje i regulacje prawne** („import z banku wymaga licencji AISP/PISP + KNF"; „licencje Tempo liczone od wszystkich użytkowników Jira").
- **Dostępność / brak API** („Booking nie ma publicznego API self-service"; „CapCut bez publicznego API").
- **Limity API** („API Shopera z limitami, nie oddaje wszystkiego"; limity IdoSell, Allegro).
- **Wymagania planów/wersji** („Structure i Gantt wymagają Jira Premium").
- **Specyfikacja sprzętowa** („KVM2 = 2 vCPU, 8 GB RAM, 4 agenty = OOM").
- **Zachowanie platform** („TikTok bez audytu publikuje prywatnie"; „llms.txt nieużywany przez Google").
- **Kanały integracji** (jaki SAP, przez co się łączymy — API/IDoc/RFC).
- **Formaty i standardy** (różne formaty feedów Ceneo/Google/Meta; 301 bez planu URL psuje indeks).

### 3.2. Kierunek pozytywny — CIEKAWOSTKI / OKAZJE
Co może projekt wzmocnić albo klienta ucieszyć:
- Lepsza, udowodniona alternatywa („import CSV zamiast API banku: dane, zero abonamentów, zero regulacji").
- Fakt, który realnie wzmacnia projekt i nie jest oczywisty.
- Zaczepienie do powiedzenia „widziałem ten schemat, kończy się tak" (doświadczenie, nie wykład).

### 3.3. Czego research NIE szuka
- Ogólnej merytoryki „o technologii", żeby zabrzmieć mądrze. To szum, każdy ma AI.
- **ROZWIĄZAŃ** — diagnoza, nie recepta. Research ma dać GDZIE i DLACZEGO groźne, nie JAK naprawić.
- Portfolio ani doświadczenia o sobie.
- Historii firmy klienta, KRS, NIP, LinkedIn — TYLKO to, co klient sam napisał. Badamy technologię, API, prawo, progi, limity. NIGDY życiorys klienta.

**Wynik researchu = konkretne zdanie-fakt + jego konsekwencja dla klienta („i co z tego").** Jeśli po fakcie nie umiem powiedzieć, co z niego dla klienta — fakt wypada.

---

## 4. REGUŁA DOWODU (fakt vs zgadywanie)

**Twarda reguła: bez dowodu fakt nie istnieje.**

### 4.1. Fakt z dowodem (może wejść dalej)
- Ma źródło: URL, cytat, nazwa dokumentu, data.
- Da się wskazać, skąd to wiem.
- Jest osadzony w treści zlecenia (zaczepienie): klient napisał X → w świecie jest fakt Y → dla niego znaczy Z.

### 4.2. Zgadywanie (STOP)
- Sygnały językowe: „jeśli", „zwykle", „prawdopodobnie", „zazwyczaj", „chyba", „mogłoby być".
- Wniosek z nazwy technologii bez potwierdzenia procesu.
- Fakt, którego nie umiem zweryfikować, ale „brzmi sensownie".
- Mina/alternatywa oparta tylko na „tak bywa w branży".

### 4.3. Procedura rozstrzygania (ślad w dzienniku)
1. Twierdzę coś → pytam: jaki mam na to dowód?
2. Dowód jest → zapisuję fakt + źródło + zaczepienie w zleceniu.
3. Dowodu nie ma → próbuję go zdobyć researchem.
4. Research nie dał dowodu → twierdzenie WYPADA. Nie zamieniam go w domysł z miękkim językiem.

### 4.4. Fakt vs doświadczenie
Surowy fakt brzmi jak Wikipedia (AI). Do oferty wchodzi jako doświadczenie („widziałem ten wyścig statusów, kończy się tak"), ale jego podstawa musi być tym samym udowodnionym faktem. Doświadczenie to FORMA, nie źródło.

### 4.5. Dowody z realnych danych (czego uczy backfire)
- „Pewna diagnoza przy zerowej wiedzy o kodzie" → nieodpisane (2897362, 2896500, 2891620).
- „Przyjmuję założenia robocze" przy braku danych → nieodpisane.
- Wniosek: research nie może udawać pewności, której nie ma.

---

## 5. JAK RESEARCH ŁĄCZY SIĘ Z MINAMI I CIEKAWOSTKAMI

To najważniejsze ogniwo. Research nie jest po to, żeby „coś wiedzieć" — jest po to, żeby **zamienić podejrzenie w dowód, a dowód w konkretne zdanie**.

### 5.1. Mina (zagrożenie = klient MUSI wiedzieć)
- W kroku 1 mina jest HIPOTEZĄ (bez dowodu nie wchodzi do oferty).
- Research: **albo udowodnić minę (fakt + źródło), albo ją zabić.**
- Udowodniona mina → wchodzi jako ostrzeżenie, które BOLI i ma zaczepienie w zleceniu.
- Nieudowodniona mina → wycięta. Bez dowodu to straszenie, nie diagnoza.

### 5.2. Ciekawostka (zwiększa ochotę, niekonieczna)
- Research potwierdza, czy ma realną wartość, czy jest oczywista.
- Oczywista ciekawostka wygląda sztucznie → wypada.
- Potwierdzona, konkretna → wchodzi tylko jeśli ma zaczepienie i mieści się w granicy cięcia.

### 5.3. Pary fakt → mina (realne przykłady)
| Research (fakt) | Mina w ofercie | Zlecenie |
|---|---|---|
| .NET 8 kończy wsparcie XI 2026 | „nowa apka na nim to migracja za kilka miesięcy" | 143891 |
| Import z banku wymaga AISP/PISP + KNF | „przy projekcie prywatnym praktycznie nie do przejścia" | 143891 |
| Booking bez publicznego API self-service | „realna droga to certyfikowany channel manager" | 143892 |
| Booking nie daje danych o innych obiektach | „tej usługi nie da się zrobić" | 143892 |
| API Shopera z limitami | „klienci, historia, stany siedzą w API, które ma limity" | 144210 |
| Brak 301 = utrata pozycji | „stracicie pozycje w Google z dnia na dzień" | 144210 |
| Tempo liczone od wszystkich userów Jira | „przy takiej skali robi się z tego konkretna kwota" | 144420 |
| TikTok bez audytu publikuje prywatnie | „zamiast obiecywać gruszki, zepniemy to inaczej" | 144249 |
| KVM2 = 2 vCPU/8 GB, 4 agenty = OOM | „cztery naraz to kolejkowanie i ryzyko wywalenia procesu" | 144275 |

### 5.4. Pary fakt → ciekawostka
| Research (fakt) | Ciekawostka | Zlecenie |
|---|---|---|
| CSV jako alternatywa dla API banku | „import CSV: dane, zero abonamentów, zero regulacji" | 143891 |
| Generowanie obrazów przez API jest tanie | „prawdziwa robota leży w kolejkach, obsłudze błędów" | 144969 |

**Wzór:** research daje FAKT → bot wybiera MINA (klient traci) czy CIEKAWOSTKA (klient zyskuje). Mina zawsze kończy się na SKUTKU, nie na instrukcji.

### 5.5. Zagrożenie vs ciekawostka (rozróżnienie)
- Zagrożenie = MUSI wiedzieć, inaczej strata. Priorytet, wchodzi pierwsze.
- Ciekawostka = miło wiedzieć. Wchodzi, jeśli miejsce i zaczepienie.
- **Nadmiar zagrożeń też jest błędem** — nie zasypujemy klienta problemami.

---

## 6. KIEDY RESEARCH PRZESADZIŁ (backfire z realnych danych)

To sekcja ostrzegawcza. Research, który przekroczy granicę, ZABIJA ofertę.

### 6.1. Pełna recepta zamiast diagnozy (dane!)
- „Pełna recepta krok po kroku: **68% nieodpisanych** vs ~30% odpisanych".
- Przykłady: 2897172 (Shoper — cała architektura), 2896427 (Presta B2B — trzy recepty + etapy), 2887274 (RAG + prompt injection + architektura, ~500 słów).
- Nasze backfire: 144165 (CNC — research dał „posortowanie linii cięcia po kącie, Micro-joint, przepisanie logiki" = recepta, nie diagnoza).

### 6.2. Research w zleceniu bez pola do popisu
- 144411 (SAP↔BaseLinker↔Shopify): research techniczny poszedł w ofertę jako wykład architektury, choć zlecenie miało twardy filtr doświadczeniowy. Research powinien zostać w filtrze kwalifikowalności, nie w ofercie.

### 6.3. Za dużo min naraz
- 144210 (Shoper→Shopify): 5 min w jednej ofercie (API limity, 301, feedy, abonament, historia zamówień). Ryzyko „insight + recepta".

### 6.4. Próg cięcia długości (twarde dane)
- **Nieodpisane = 300-600 słów. Odpisane = 100-250 słów.**
- Research, który pcha ofertę ponad 300 słów, jest podejrzany — to sygnał „insight + pełna recepta".

### 6.5. Reguła graniczna
> „Tease zamiast recepty: diagnoza kończy się na skutku, nie na kroku. Zamiast 'wymaga FORCE ROW LEVEL SECURITY i tenant context fails closed' → 'widziałem ten błąd, mam na to sposób, chętnie pokażę'."

---

## 7. KIEDY RESEARCH SIĘ KOŃCZY (wystarczy)

Trzy warunki stopu (wystarczy jeden — reszta to szum):

1. **Każda hipoteza z kroku 1 rozstrzygnięta:** mina ma dowód albo jest wycięta; alternatywa ma dowód albo wypada; pytanie klienta ma potwierdzoną odpowiedź.
2. **Nowe szukanie przestaje zmieniać decyzje.** Test: gdybym znalazł jeszcze jeden fakt, czy zmieniłby się wybór DOPISAĆ/ODPOWIEDZIEĆ/DOPYTAĆ albo wycena? Jeśli nie — stop.
3. **Dochodzę do granicy cięcia.** Dalsze fakty są już merytoryką ponad to, o co klient pytał — szumem. Stop.

**Dodatkowo:**
- Research nie ma limitu zapytań, ale ma limit UŻYTECZNOŚCI.
- Jeśli iteracja 2 uzna, że research nic nie zmienia — jest ANULOWANY, nie „dokończony na wszelki wypadek".
- Koniec researchu = dojrzały dziennik gotowy do iteracji 3. Research nie pisze oferty.

**Fallback:** gdy research nic nie znajdzie → zwraca `BRAK_ISTOTNYCH_FAKTOW` i NIC więcej. Pusta sekcja lepsza niż zmyślona. Nie wymyślamy faktów, żeby raport nie był pusty.

---

## 8. SKĄD czerpie (hierarchia źródeł)

1. **Zlecenie** — zawsze pierwsze i nadrzędne. Jeśli odpowiedź jest w treści, research zbędny (prymat ogłoszenia).
2. **Internet (WebSearch/WebFetch)** — fakty weryfikowalne: daty wsparcia, dokumentacja producenta, zmiany API, przepisy. Cel: zdobyć URL/cytat jako dowód.
3. **Materiał edukacyjny bota** (teoria warstw, lore, lekcje) — rozpoznawanie wzorców, min, zachowań. Nie źródło faktów technicznych, tylko rozumienia.
4. **Doświadczenie własne** — dopuszczalne jako podpowiedź GDZIE szukać, ale NIE jako dowód. „Pamiętam, że..." nie jest faktem, dopóki nie ma potwierdzenia.

---

## 9. OUTPUT researchu (forma)

Zwięzły raport w punktach, każdy fakt z:
- **co ustalono** (fakt),
- **źródło** (URL/cytat/data) albo oznaczenie „niepotwierdzone",
- **zaczepienie** w zleceniu (dlaczego to dotyczy TEGO klienta),
- **konsekwencja** („i co z tego") — mina czy ciekawostka.

Sekcje:
1. MINY I HACZYKI (zagrożenia).
2. CIEKAWOSTKI I RZECZY POMOCNE.
3. ALTERNATYWY (tylko z dowodem).
4. CENY RYNKOWE (jeśli znalezione — widełki dla freelancerów, nie agencji).

**Ślad w dzienniku:** dla każdego faktu — źródło + zaczepienie + dlaczego mina/ciekawostka. Dzięki temu w kroku 3 widać, DLACZEGO bot coś napisał albo przemilczał.

---

## 10. Zasady rządzące researchem (ściągawka)

1. Research odpala się TYLKO po zielonym świetle z analizy (pole do popisu + ścieżka A/B/C).
2. Sama nazwa technologii to NIE zaproszenie. Potrzebny proces albo pytanie.
3. Bez dowodu fakt nie istnieje. Research zamienia podejrzenie w dowód albo zabija hipotezę.
4. Research daje GDZIE i DLACZEGO groźne, nie JAK naprawić (diagnoza, nie recepta).
5. Nie badamy życiorysu klienta. Tylko technologia, prawo, API, limity, progi.
6. Maks. 2-3 miny na ofertę. Nadmiar zagrożeń to błąd.
7. Nie pchamy oferty ponad 300 słów researchem.
8. Research kończy się, gdy nowe fakty nie zmieniają decyzji.
9. Pustka lepsza niż zmyślony fakt. `BRAK_ISTOTNYCH_FAKTOW` to poprawny wynik.
10. Research nie pisze oferty. Dostarcza materiał i konsekwencje, reszta należy do iteracji 3.

---

## 11. Otwarte do dopracowania

1. Jak konkretnie formułować pytanie badawcze (nie „zbadaj temat", tylko konkret z zlecenia)?
2. Jak research łączy się z kartami tech (tech_01-16) — używać czy wyrzucić?
3. Czy research ma osobny limit czasu, czy tylko limit użyteczności?
4. Jak odróżnić „mina z dowodem" od „mina z wiedzy branżowej, którą mam w głowie"?