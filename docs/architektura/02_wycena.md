# MECHANIKA WYCENY (DETERMINISTYCZNA)
**STATUS: AKTUALNE** | Implementacja: kod/wycena_kalkulator.py (zrodlo prawdy liczb).

---

## 1. Zasada nadrzedna
AI NIE LICZY CENY SAMODZIELNIE. Agent 02b ocenia zakres i zwraca strukture (moduly, szacowane godziny, flagi ryzyka). Python w wycena_kalkulator.py deterministycznie wylicza kwote, dni i zaokraglenia.

## 2. Sciezki wyceny
- **Male zlecenie** (typ="male"): stala kwota rynkowa z twarda podloga MIN_KWOTA i MIN_WORK_DAYS.
- **Retainer** (typ="retainer"): widełki miesięczne dla opieki technicznej / customer success (RETAINER_WIDEŁKI), z korekta ryzyka max().
- **Projekt godzinowy** (typ="projekt"): suma godzin modulow (cap dla czystego landingu) -> testy/dokumentacja (narzut) -> bufor (standard / nowa technologia) -> mnoznik ryzyka -> stawka -> korekta konkurencyjna -> kotwica budzetu -> zaokraglenie psychologiczne.

## 3. Mnozniki ryzyka (max(), twardy sufit MAX_RISK_MULTIPLIER)
Zamiast kaskadowego mnozenia — wybierany jest najwyzszy pojedynczy mnoznik z twardym sufitem ("zero kaskady").

| Flaga | Mnoznik |
|---|---|
| figma_w_ogloszeniu (gotowe makiety = rabat) | ×0.90 |
| brak_specyfikacji | ×1.05 |
| real_time (WebSocket/streaming) | ×1.10 |
| ograniczenia_api (API jako osobny modul) | ×1.05 |
| ograniczenia_api (brak modulu API) | ×1.15 |
| Twardy sufit | = MAX_RISK_MULTIPLIER |

## 4. Korekta konkurencyjna i kotwica budzetu
- Brak dumpingu przy duzej konkurencji — brak obnizek przy duzej liczbie ofert.
- Premia marzowa przy malej konkurencji (i dodatkowo dla zlecen starszych niz 3 dni).
- Kotwica budzetu jawnego: jesli budzet > cena po korekcie — kalkulator celuje w % budzetu klienta z twardym sufitem mnoznikowym (ochrona przed szokiem cenowym). Male budzety (przedzial stawki) sa rozpoznawane jako deklarowana stawka godzinowa klienta, nie budzet calosci.

## 5. Sanity check
W projektach godzinowych, jesli po korektach efektywna stawka (kwota / godziny_real) spadnie ponizej MIN_STAWKA_GODZINOWA, kalkulator podnosi ostrzezenie blokujace (SANITY_BLOK).