# GRANICE TEORII — pełny przegląd (36 zleceń)

> Źródło: analiza 4 rozmów + ~60-80 zleceń z bazy 01_ofertowarka.
> Data: 2026-10-04. Status: materiał do decyzji.

## Skala problemu

**36 zleceń na ~180 (ok. 20%) łamie teorię** w sposób, którego teoria nie umie obsłużyć.

| Kategoria | Liczba | Przykłady id |
|---|---|---|
| Klient wymaga portfolio/referencji | 13 | 145337, 144161, 143921, 144108, 144138, 144136, 144106, 144174, 144210, 144334, 144347, 143996, 143994 |
| Rekrutacja / stała współpraca / podwykonawstwo | 11 | 144199, 144185, 144044, 144107, 144038, 143959, 144002, 144252, 144347, 144136, 143994 |
| Narzucony format / egzamin wiedzy | 5 | 144161, 144165, 144120, 143996, 144138 |
| Skrajny budżet (jawny niski/wysoki) | 6 | 144256, 145337, 144154, 144069, 143891, 144001 |
| Ogólne, bez pola do wyceny | 3 | 144102, 144171, 143984 |
| Scam / patologia | 3 | 144010, 144256, 144199 |

## Sześć wniosków o granicach teorii

**1. Teoria jest teorią „drugiej wiadomości", nie „pierwszej oferty".**
Założenia (brak portfolio, brak callu, brak stawki godzinowej, jedna cena z widełkami) działają
tylko wtedy, gdy klient NIE narzuca formatu zgłoszenia. Gdy narzuca (144161, 144136, 144108,
144334), oferta przestaje być aktem komunikacji, a staje się testem rekrutacyjnym.

**2. Prawdziwym wyznacznikiem jest model relacji, a nie typ klienta.**
Teoria dzieli na techniczny/nietechniczny, doradca/wykonawca. Ale w bazie widać ostrzejszy podział:
jednorazowe zlecenie projektowe vs stała współpraca / podwykonawstwo / rekrutacja.
Tam gdzie to drugie (144185, 144038, 143959, 144002, 144347, 144252), cała aparatura
„widełki + dwa pytania + escrow" jest bezużyteczna, bo klient kupuje czas człowieka, nie projekt.

**3. „Nigdy portfolio" jest fałszywe jako zasada ogólna.**
Reguła wyszła z jednego zlecenia (145098) i została przeniesiona na cały system.
Ale 25% bazy to zlecenia, gdzie portfolio jest wymagane.
Rozróżnienie: portfolio tylko gdy klient JAWNIE o nie prosi albo gdy zlecenie jest rekrutacyjne.

**4. Reguła „widełki zawsze" nie działa przy jawnym budżecie.**
6 zleceń ma budżet w tabeli (100 zł / 5000 / 10000 / 50000 / 2000 USD).
Wtedy albo widełki są bez sensu (100 zł), albo wchodzą w konflikt z wyceną bota
(144154: budżet 5000 vs wycena 9000). Brak reguły „co robić, gdy kwota znana z góry".

**5. Reguła „zawsze pytaj o zakres" nie działa przy zleceniach bez zakresu.**
144102 (trener MariaDB, jedno zdanie), 143984 (system AI bez konkretów), 144171 (wszystko
oprócz budżetu). Tu pytania brzmią jak zgadywanie, a teoria sama mówi „zgadywanie to śmierć".
Paradoks: im mniej danych, tym teoria każe pytać, a im więcej pytań, tym bardziej brzmi jak AI.

**6. Teoria zakłada, że zlecenie jest wykonalne i opłacalne.**
W bazie są zlecenia, gdzie żadna strategia nie pomoże: 144199 (wymóg US-native, dyskwalifikacja
strukturalna), 144256 (100 zł), 144010 (scam). Brakuje etapu „sprawdź, czy w ogóle jest sens
składać ofertę". To brakujący klocek: **filtr kwalifikowalności** przed filtrem profilowania.

## Nowe przykłady warte uwagi (nie było ich w pierwszym przebiegu)

- **144161** | WooCommerce 1:1 z Figmy | BO: klient zadaje 3 pytania techniczne jako egzamin
  („które elementy będą najbardziej wymagające i jak je rozwiążesz, odpowiedzi ogólne odpadają").
  Merytoryka jest tu jedynym kryterium. Odwrotność „merytoryka zero".
- **144120** | System POS gastronomia | BO: w nagłówku „BEZ AI SLOOP" - klient wprost odrzuca
  AI-owe oferty. Sygnał, że nasz styl może być wykryty i odrzucony.
- **144165** | CNC Punch Software | BO: skrajna nisza, klient dostarcza własne programy,
  oczekuje modyfikacji nie diagnozy. Teoria „haczyków" nie działa.
- **144102** | trener MariaDB | BO: jedno zdanie, to rekrutacja trenera, nie zlecenie IT.
- **144199** | US based developer | BO: wymóg „US-native" - Ksawier tego nie spełnia.
  Zlecenie strukturalnie nie do wygrania, a bot i tak wysłał ofertę.

## Wniosek dla łańcucha

Przed całym łańcuchem potrzebny **detektor typu zlecenia / filr kwalifikowalności**:
- projekt jednorazowy (teoria działa)
- retainer / stała współpraca (inny tryb, brak deliverable)
- rekrutacja / podwykonawstwo (inny tryb, CV/stawka/dostępność)
- egzamin wiedzy (merytoryka obowiązkowa, nie opcjonalna)
- zlecenie bez zakresu (tryb czystego dopytania)
- scam / niewykonalne (odrzucić, nie pisać)

Od typu zależy tryb odpowiedzi. Bez tego teoria obsłuży ~80% rynku.