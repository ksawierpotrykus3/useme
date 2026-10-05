# BOT V2 — TEST PLANU NA REALNEJ BAZIE (wyniki)

> Status: wyniki testu. Data: 2026-10-05.
> Testowane: plan kroku 1 (analiza) + kroku 2 (research) na realnych zleceniach z magazynu.
> Zakres: ~70 zleceń (36 z programowanie-i-it, 25 z serwisy-internetowe, 3 zlecenia testowe z ofertami konkurencji).
> Werdykt: PLAN NIE DZIAŁA NA 100%. Jest dobrą filozofią, ale ma dziury jako procedura.

---

## 1. WYNIK LICZBOWY (próbka 36 zleceń z IT)

- ✅ Plan przechodzi bez problemu: **15 (42%)** — realne, konkretne projekty z nazwą technologii i opisem procesu.
- 🟡 Przechodzi niejednoznacznie: **11 (31%)** — potrzebna decyzja człowieka, plan sam nie rozstrzyga.
- ❌ Plan się wykłada: **10 (28%)** — brak kategorii, brak procedury, brak filtra.

---

## 2. GDZIE PLAN ZAWIÓDŁ — 7 LUK

### LUKA 1 — NIEAKTUALNA (błąd subagenta: pomieszał konteksty)
**Weryfikacja użytkownika:** Subagent pomylił dwa konta.
- `ksawierpotrykus3` = konto, na którym WYSTAWIAmy oferty. Widzimy TYLKO ogłoszenie z listy. Opis ogłoszenia to cały materiał. Żadnego priv, korespondencji, załączników przed wysłaniem oferty.
- `weronikabuchholc13` = konto BADAWCZE, na którym WYSTAWIAMy zlecenia i zbieramy oferty konkurencji. Tu są priv, załączniki, wątki — ale to NIE nasz bot ofertujący.

ProfiPiek i „deep-sync" były w korespondencji konta badawczego. Bot ofertujący ich nie zobaczy i nie musi.
**Skutek:** luka nieprawdziwa. Krok 1 słusznie operuje na samym ogłoszeniu.
**Fix:** brak. (Uwaga na przyszłość: testy muszą jasno rozdzielać kontekst „wystawiamy ofertę" vs „zbieramy oferty".)

### LUKA 2 — Bramka researchu zbyt ostro odcina nazwy bez procesu
**Dowód:** W #144890 klient napisał tylko „Comarch Optima" jako system docelowy (nazwa bez pełnego procesu). Plan dałby OFF — a research Optimy dał 2 kluczowe miny zwycięskiej oferty (koszt licencji, ograniczenia XML).
**Skutek:** tracimy miny ścieżki B oparte na nazwie systemu.
**Fix:** dodać przesłankę ON: „Klient wymienił NAZWĘ systemu docelowego (ERP, platformy, integracji) → research podstawowy (koszty licencji, ograniczenia API, dostępność modułów)".

### LUKA 3 — Brak detektora „terminu spoza świata"
**Dowód:** „silent-guard" (#145285) i „deep-sync" (#145287) — terminy, których NIE MA w dokumentacji dostawców. Elita konkurencji je rozbroiła (DAVIDO: „nie znam w Subiekcie trybu silent-guard"; ensomedia: „nazwy deep-sync nie znam jako gotowego mechanizmu").
**Skutek:** nie reagujemy na wymyślone terminy, które są okazją do pokazania kompetencji.
**Fix:** reguła — jeśli klient użył nazwy mechanizmu/trybu, której nie ma w dokumentacji systemu → sygnał do research + pytania.

### LUKA 4 — Pytanie 7 wycina pytania, które nie zmieniają wyceny
**Dowód:** Pytanie o „silent-guard" NIE zmieniało wyceny, a było kluczem pokazania kompetencji (DAVIDO, Ziemniaqs, Volodymyr wszyscy o to pytali).
**Skutek:** tracimy pytania-wykrywacze, które budują wiarygodność.
**Fix:** rozdzielić pytania na dwa typy: (a) wycenowe (są), (b) **pytania-wykrywacze** („co u Was znaczy X?") — budują diagnozę.

### LUKA 5 — Zero kalibracji ceny
**Dowód:** #144890 — nasza v6 17 000 zł przegrała u DeepSeeka z 10 500 zł. Zwycięska nowa wersja: 9 800 zł. Budżet jawny vs wycena to dziura krytyczna (144154: budżet 5000, V1 wycenił 9000).
**Skutek:** cena to czynnik przegranej, a plan jej nie dotyka.
**Fix:** reguła dla budżetu jawnego: „budżet X → widełki [0.9X, 1.2X] albo odrzucamy albo fazujemy". (Do rozstrzygnięcia — open question #2 kroku 1.)

### LUKA 6 — Nie łapie „ukrytego ryzyka projektowego" bez nazwy technologii
**Dowód:** #145287 — klient NIE napisał o konflikcie synchronizacji offline, a Kacper Zdziebło zrobił z tego główny argument („co się dzieje, gdy pracownik wypełnia formularz bez zasięgu, a ktoś inny zmienia ten sam rekord"). To ryzyko KLASOWE (każda apka offline-first je ma), nie nazwa technologii.
**Skutek:** przegapiamy najbardziej wartościowe miny.
**Fix:** dodać do kroku 2 listę **ryzyk klasowych per typ zlecenia** (mobile offline = konflikt synchronizacji; OCR faktur = tolerancja groszy VAT; sync magazynów = sprzedaż widmo) — niezależnie od tego, czy klient je wymienił.

### LUKA 7 — P3 „prawdziwy ból" zakłada, że ból jest w opisie
**Dowód:** #145285 — prawdziwy ból = „sprzedaż towaru, którego nie ma na stanie" (widmo), a nie „synchronizacja". Plan by to złapał tylko dlatego, że klient to napisał.
**Skutek:** gdy klient nie nazwie bólu, nie znajdziemy go.
**Fix:** szukać bólu biznesowego aktywnie, także poza dosłownym opisem (połączenie z luką 6).

---

## 3. NOWE KATEGORIE ZLECEŃ (plan ich NIE przewidział)

1. **Awaria scrapowania** (144514, 144520) — `full_description` pusty, URL = useme.com. V1 wysłał oferty „w ciemno" z `short_desc`.
2. **Phantom lead / equity / wspólnik techniczny** (145033) — „szukam CTO za udziały". V1 wycenił na 18000 zł!
3. **Rekrutacja pod przykrywką** (144044, 144045, 144199, 144318, 144457) — lista wymagań jak w CV, „CV + stawka godzinowa", filtry US-native.
4. **Tester / QA / pentest** (144434, 144599) — usługa poza devem, wymóg CEH/OSCP.
5. **Usługa nie-IT w kategorii IT** (144461 — księgowy enova365) — plan krok 2 fałszywie zaklasyfikował jako scam.
6. **Praca dla innej profesji** (145153 — redesign grafiki).
7. **Czerwony ocean** (144774 — WordPress/WooCommerce „dla mas").
8. **Własny profil / konkurencja** (144890 — status ODRZUCONA_WLASNY_PROFIL).
9. **Twardy filtr doświadczeniowy branżowy** (144411, 144737 — „musisz mieć wdrożenia WAPRO/BaseLinker").
10. **Egzamin wiedzy z twardą listą pytań** (144411, 144737, 144748, 144318) — klient nie pyta „jak to zrobisz", tylko „opisz 1-3 wdrożenia, odpowiedz na 7 punktów".

---

## 4. P0 „KWALIFIKOWALNOŚĆ" TRZEBA ROZBIĆ NA PODTYPY

Plan mówi „TAK/NIE". Realnie jest co najmniej **7 różnych typów odrzuceń**:
1. phantom/equity (145033),
2. rekrutacja pod przykrywką (144045, 144199, 144457),
3. twardy filtr certyfikacyjny (144599 — CEH/OSCP),
4. twardy filtr doświadczeniowy branżowy (144411, 144737),
5. praca dla innej profesji (144434, 144461, 145153),
6. czerwony ocean (144774),
7. własny profil (144890),
8. **awaria danych wejściowych** (144514, 144520 — pusty `full_description`).

Każdy typ ma INNY sygnał i INNĄ decyzję. Wrzucanie ich do jednego worka „NIE" to błąd.

---

## 5. CO POTWIERDZIŁO SIĘ JAKO MOCNA STRONA PLANU

1. **Bramka dowodu (krok 2 sekcja 4)** — spójna z danymi (68% nieodpisanych miało pełną receptę).
2. **Rozdzielenie diagnoza vs recepta** — potwierdzone: oferta `dso-it` (15 000 zł, 4215 znaków, 12 kroków) nie weszła do shortlisty, a zwycięska była diagnozą z zaczepieniem.
3. **Ścieżka B (mina)** działa na #145285 — plan słusznie traktuje ostrzeżenie o „silent-guard" jako hipotezę; research ją zabija.
4. **Ścieżka C (alternatywa)** — „Sfera zamiast INSERT SQL" złapane.
5. **Rozpoznawanie egzaminu wiedzy, retainer, phantom** — plan ma je na liście typów.

---

## 6. REKOMENDACJE PRZED KROKIEM 3

1. **Dodać detektor awarii danych wejściowych:** pusty `full_description` lub URL = useme.com → P0 = NIE, przerwij (re-scrape).
2. **Rozbić P0 na 8 podtypów odrzuceń** z osobnymi sygnałami.
3. **Dopisać do listy typów zleceń:** tester/QA/pentest, egzamin wiedzy, praca poza devem, czerwony ocean, phantom/equity, własny profil, twardy filtr doświadczeniowy/certyfikacyjny, awaria scrapowania.
4. **Domknąć budżet jawny vs wycena** (open question #2 kroku 1).
5. **Dodać wejście „poza ogłoszeniem"** (PV, załączniki, korespondencja).
6. **Zmiękczyć bramkę research OFF** o nazwę systemu docelowego.
7. **Dodać detektor „terminu spoza świata".**
8. **Dodać ryzyka klasowe per typ zlecenia.**
9. **Rozdzielić pytania na wycenowe i wykrywacze.**

---

## 7. MATERIAŁ: LISTY ZWROTÓW AI I WZORCÓW LUDZKICH (do wpięcia)

### 7a. Twarde zakazy (checker automatyczny)
1. Zakaz `—`, `–`, ` - ` — łączyć przecinkami/kropkami/spójnikami.
2. Zakaz nawiasów `(` `)`.
3. Zakaz markdown: `#`, `**`, `|`, tabele.
4. Zakaz wypunktowań: `-`, `•`, `*`, listy `1. 2. 3.` na początku linii.
5. Zakaz etykiet z dwukropkiem w prozie („Dlaczego to ważne:", „Kluczowa mina:").
6. Zakaz otwarcia „Dzień dobry" / podpisu „Pozdrawiam" (standard 113x/83x, brak wyróżnika).
7. Zakaz blacklisty B1-B9 (etykiety, anonsowanie, echo klienta, coaching/empatia, kapitulacja, szkielety „Nie X, ale Y", żargon promptowy).
8. Gwarancja tylko 30 dni.
9. Stawka godzinowa tylko 90 zł/h.
10. Zakaz słów „inżynier", „tandem inżynierski".
11. Zakaz propozycji wideo/telefonu/calli (bez prośby klienta).
12. Kwota/dni zgodne z `[WYNIK_KONCOWY]`.
13. Zakaz „Przyznam szczerze" / „Nie ukrywam".

### 7b. Miękkie wzorce ludzkie (LLM-guided, nie checker)
- Macierz powtarzalność × sens: A (standard branży), B (wata — wywalać), C (dziwactwo — nie naśladować), **D (ZŁOTO — naśladować mechanizm)**.
- Max **1-2 wzorce D na ofertę**, każdy z realnym triggerem w zleceniu.
- Wzorzec bez triggera = ZABLOKOWANY (teatr).
- Skromność = bilans: brak + konkret zamiennik z tego zlecenia.
- Kopiujesz MECHANIZM, nie cytat.
- Brak pasującego wzorca = sucha oferta, zero doklejania.

### 7c. Wzorce D (mechanizmy, nie cytaty)
D1 anegdota o usterce, D2 mikroprzykład co do grosza, D3 bug operacyjny z praktyki, D4 przyznanie braku + konkret, D6 szczegół wizualny, D8 metafora ożywiająca system, D9 pytanie decyzyjne przed ofertą, D10 jawna rezygnacja z marży, D15 humanizacja procesu, D16 sekcja ryzyka z inicjatywy, D17 konkretna liczba zamiast obietnicy, D21 zaprzeczenie własnej obietnicy („zero opóźnień nie istnieje"), D24 rekomendacja konkurencyjnej technologii wbrew sobie, D27 przyznanie braku portfolio z zamiennikiem.

### 7d. Sprzeczności do rozstrzygnięcia
1. **Nawiasy vs D12** (samokorekta w nawiasie) → D12 dozwolone TYLKO jako myślenie na głos BEZ nawiasu.
2. **Em-dash w cytatach korpusu** → zakaz dotyczy NASZEGO tekstu, nie ilustracji.
3. **„Dzień dobry"** A vs B → dla V2 traktować jako B (wywalać).
4. **Literówki D5/D14/D19/D30** → oznaczyć jako „rozpoznawać, NIE naśladować".
5. **Praca w duecie** → nie umieszczać w ofercie wcale (klient widzi profil).

---

## 8. STAN PO TEŚCIE

Plan kroku 1 i 2 wymaga **poprawek przed krokiem 3**. Najpilniejsze:
- P0 na 8 podtypów,
- 10 nowych kategorii zleceń,
- wejście „poza ogłoszeniem",
- bramka researchu (nazwa systemu),
- ryzyka klasowe,
- budżet jawny.

Listy zwrotów AI i wzorców ludzkich są gotowe do wpięcia (sekcja 7).