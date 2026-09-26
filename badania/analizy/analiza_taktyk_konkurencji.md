# Analiza konkurencji — co robi elita, czego nie robi reszta

Źródło danych: 30 ofert publicznych + 4 wiadomości prywatne pod zleceniem testowym #144890.
Data analizy: 23 września 2026.

## TECHNIKA 1 — Otwieranie problemem klienta, nie sobą

90% oferentów otwiera ofertę słowami o sobie:
- "Dzień dobry, zajmuję się automatyzacją od 6 lat..."
- "Chętnie podejmiemy się zaprojektowania..."
- "Mogę przygotować automatyzację..."

Elita otwiera problemem, o którym klient nie wie:
- ailone: "Zanim odpowiem na Państwa trzy pytania, jedna rzecz, która zmienia projekt na korzyść. KSeF zamiast OCR tam, gdzie się da."
- skalownia: "Najdroższy w takim procesie jest dokument odczytany błędnie i wpuszczony dalej bez zatrzymania."
- Adam K na priv: "Przy Waszym punkcie 3, o weryfikacji sum, trzeba od razu ustalić, co automat robi z różnicą kilku groszy."

Klient czyta to i myśli: "ten gość wie więcej ode mnie o moim własnym problemie." I to jest moment, w którym zaufanie się buduje.

ZASADA: Pierwsze 2-3 zdania oferty muszą mówić o problemie klienta, nie o Tobie.


## TECHNIKA 2 — Mówienie klientowi czegoś, czego klient NIE WIE

Trzy "złote argumenty" z badania, które zna mniej niż 15% oferentów:

ARGUMENT KSeF (tylko 4 z 28 oferentów):
Od lutego 2026 faktury od polskich podatników VAT trafiają do KSeF jako ustrukturyzowany XML. Optima po skonfigurowaniu uprawnień pobiera je sama. Budowanie OCR dla tych faktur to marnowanie budżetu — dane są bezbłędne u źródła. OCR i model wizyjny AI rezerwujemy wyłącznie dla WZ, zamówień i faktur zagranicznych.

ARGUMENT ZAOKRĄGLEŃ VAT (tylko ailone + Adam K na priv):
Ustawa o VAT dopuszcza dwa sposoby liczenia podatku: od każdej pozycji osobno lub od sumy stawek w podsumowaniu. Trzy pozycje po 10 groszy netto przy 23% — te dwa sposoby dają legalne rozbieżności rzędu 1-2 groszy. Sztywna walidacja "co do grosza" odrzuci poprawne faktury.
Przykład liczbowy Adama K: 3 x 0,10 zł netto x 23% = 0,06 zł VAT od pozycji vs 0,07 zł VAT od sumy.

ARGUMENT DEDUPLIKACJI (tylko ailone + Adam K na priv):
Dokumenty spływają z trzech wejść — skaner, mail, pracownicy w terenie. Ta sama faktura potrafi wpłynąć dwiema drogami. Klucz: NIP dostawcy + numer dokumentu.

ZASADA: Każda oferta musi zawierać minimum 1 konkretny insight techniczny lub biznesowy, którego klient nie zna.


## TECHNIKA 3 — Rozbijanie ceny na moduły

Jak wycenia rzemieślnik:
"4 500 zł, 7 dni pracy."
Skąd ta kwota? Klient nie wie. Nie może porównać. Nie rozumie za co płaci.

Jak wycenia elita:
sunoger (14 580 zł rozbite na 8 modułów):
  Moduł 1: Instalacja n8n na serwerze — 1 080 zł
  Moduł 2: Pobieranie dokumentów — 1 260 zł
  Moduł 3: Odczyt AI i klasyfikacja — 3 240 zł
  Moduł 4: Walidacja i obsługa wyjątków — 1 620 zł
  Moduł 5: Nazewnictwo i archiwum — 720 zł
  Moduł 6: Integracja z Comarch Optima — 2 880 zł
  Moduł 7: Testy na rzeczywistych dokumentach — 2 160 zł
  Moduł 8: Opieka powdrożeniowa 30 dni — 1 620 zł

krmob (14 900 zł = 124 roboczogodziny x 120 zł/h):
  analiza procesu i architektura — 8 h
  konfiguracja n8n i środowiska — 10 h
  Google Drive i e-mail — 10 h
  OCR i przygotowanie skanów — 22 h
  ekstrakcja danych i klasyfikacja — 20 h
  walidacja matematyczna i biznesowa — 12 h
  workflow błędów i archiwizacja — 8 h
  integracja z Comarch Optima — 18 h
  testy na dokumentach firmy — 10 h
  wdrożenie i dokumentacja — 6 h

ZASADA: Przy wycenach powyżej 5 000 zł — zawsze rozbijaj na moduły lub roboczogodziny.


## TECHNIKA 4 — Gwarancje, których nikt nie daje

Standardowa oferta: "krótki okres wsparcia" albo nic.

Elita:
- krmob: 12 MIESIĘCY GWARANCJI NA KOD — jedyny na rynku
- marcin-korolko: 3 miesiące gwarancji, mierzalne kryteria odbioru etapu
- sunoger/bartoszb/skalownia/ailone: 30 dni asysty powdrożeniowej wliczone w cenę
- marcin-korolko: precyzyjne wyliczenie kosztów tokenów — Claude Haiku: 17 zł za 1000 stron

Retainery po wdrożeniu (stała opieka):
- marek-pastuszczak: 400 zł/miesiąc
- bartoszb: 500 zł/miesiąc
- skalownia: od 600 zł/miesiąc
- krmob: 120 zł/h (bank godzin)

ZASADA: Zawsze podawaj konkretną gwarancję — ile dni/miesięcy, co obejmuje.


## TECHNIKA 5 — Mówienie wprost czego NIE umiesz

Paradoksalnie buduje zaufanie bardziej niż przechwałki.

skalownia: "Z Comarchem pracowałem po stronie XL, nie Optimy, więc most zaczynam od sprawdzenia u Państwa, zamiast obiecywać gotową ścieżkę."

marek-pastuszczak: "Uczciwie: automatyzacji obiegu faktur nie wdrażałem dotąd komercyjnie — opisany wyżej sposób postępowania jest tym, co realnie zrobię, a etap pierwszy pozwoli Państwu to zweryfikować małym kosztem."

daniel-michalek: "Nie chcę deklarować portfolio 1:1 z Optimą, którego nie mogę udokumentować. Zamiast tego proponuję na początku krótki test na kilku zanonimizowanych dokumentach."

Klient myśli: "Skoro mówi wprost że czegoś nie robił, to reszta musi być prawda."

ZASADA: Jeśli nie masz doświadczenia w konkretnej technologii — powiedz to i zaproponuj test/etap próbny.


## TECHNIKA BONUSOWA — Co robili seniorzy na priv (i dlaczego to najwyższy poziom)

4 seniorów (Adam K, Kamil Wojtulewicz, Konrad Szydłowski, Adam Wolski) NIE złożyli oferty publicznej. Zamiast tego:

1. PYTALI zamiast strzelać ceną — żaden nie podał kwoty bez informacji o wersji Optimy, wolumenie dokumentów, próbce skanów.

2. KWALIFIKOWALI klienta — Konrad: "zanim złożę ofertę, jedno pytanie, bo od niego zależy połowa zakresu." To odwrócenie dynamiki: to freelancer decyduje czy chce ten projekt, nie klient.

3. PISALI ASYNCHRONICZNIE — Adam K: "Piszę asynchronicznie, na pytania odpowiem tutaj w wątku." Zero presji, zero nachalności.

4. DZIELILI SIĘ WIEDZĄ ZA DARMO — Adam K wyjaśnił problem zaokrągleń VAT z przykładem liczbowym. Konrad wyjaśnił że KSeF eliminuje potrzebę OCR. To reguła wzajemności Cialdiniego w czystej postaci.

ZASADA: Najwyższy poziom sprzedaży na Useme to NIE składanie oferty publicznej — to napisanie prywatnej wiadomości z pytaniami kwalifikującymi i jednym insightem za darmo.


## ANTYWZORCE — Czego absolutnie nie robić

1. NIE pisz "chętnie pomogę" — puste, generyczne, mówi każdy
2. NIE otwieraj od siebie — "zajmuję się X od Y lat" nikogo nie obchodzi
3. NIE kopiuj treści zlecenia — klient widzi to natychmiast
4. NIE proponuj bezpośredniego zapisu do SQL Optimy — to błąd architektoniczny
5. NIE wrzucaj numeru telefonu — łamie regulamin Useme, wygląda desperacko
6. NIE żądaj 36 000 zł w 707 znakach — to nie jest pewność siebie, to nonsens
7. NIE testuj na 3 dokumentach — to naiwność produkcyjna (kamil-dus)
8. NIE pytaj klienta o rzeczy, które podał w ogłoszeniu

## INSIGHT: LICZBA UMÓW NIE KORELUJE Z JAKOŚCIĄ

Dane z 36 ofert pod zleceniem #144890:
- 18 oferentów z 0 umów — tam są WSZYSCY najlepsi (ailone, dso-it, intevo, marek-pastuszczak,
  marcin-korolko, dawid-braun). Średnio 2 553 znaków, merytoryczne, z insightami.
- 7 oferentów z 6+ umów — śmieci lub kosmiczne ceny (pixelpulse 120k, ofylypczuk 1k dumping).
  Średnio 1 355 znaków, generyczne.

Liczba umów na Useme mówi że ktoś dużo klikał, nie że jest dobry.
Najlepsi prawdopodobnie prowadzą rozliczenia poza platformą lub traktują Useme jako kanał lead-gen.
