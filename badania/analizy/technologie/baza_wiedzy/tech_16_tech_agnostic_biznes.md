# KARTA WIEDZY STRATEGICZNEJ BOTA OFERTOWEGO USEME

## TEMAT: Obsługa Segmentu Tech-Agnostic — Zlecenia bez Podanej Technologii

**Wersja:** 1.0 | **Data aktualizacji:** 2026 | **Klasyfikacja:** Wewnętrzna baza wiedzy bota ofertowego

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW

### 1.1. Wolumen i pozycja segmentu

Segment tech-agnostic obejmuje 155 zleceń w przebadanym wolumenie, co stanowi 33% całego rynku Useme. To największy pojedynczy segment pod względem liczby zapytań — wyprzedza zlecenia z jawnie określoną technologią (React, Python, WordPress) oraz zlecenia czysto kreatywne (grafika, copywriting).

### 1.2. Charakterystyka budżetowa

| Parametr | Wartość |
|---|---|
| Widełki budżetowe | 1 500 – 7 000 zł |
| Mediana | ok. 3 500 – 4 200 zł |
| Średnia stawka programistyczna na Useme (2025/2026) | 5 014 zł za projekt |
| Średnia stawka tworzenia aplikacji | 3 974 zł |
| Średnia stawka usług IT | 3 995 zł |
| Średnia stawka UX/UI | 3 656 zł |

Dane bazowe: Useme, raport stawek 2025/2026.

Budżet 1 500 – 7 000 zł lokuje się **poniżej średniej programistycznej** (5 014 zł), ale **powyżej średniej copywritingowej** (1 576 zł) i **marketingu ogólnego** (2 426 zł). Oznacza to, że klient tech-agnostic jest gotów zapłacić za **rozwiązanie problemu**, nie za godziny programistyczne.

### 1.3. Profil zleceniodawcy

- **Typ:** Właściciel małej firmy (1–20 osób), manager operacyjny, osoba prowadząca jednoosobową działalność.
- **Wiedza techniczna:** Zerowa lub minimalna. Nie odróżnia frontendu od backendu, nie zna pojęć „API”, „deployment”, „stack”.
- **Motywacja:** Bolączka operacyjna — powtarzalna czynność, która zjada godziny, błędy ludzkie w danych, brak dostępu do informacji w czasie rzeczywistym.
- **Sposób myślenia:** Myśli kategoriami „co zyskam”, nie „jak to działa”. Decyzję zakupową podejmuje emocjonalnie, a następnie racjonalizuje.
- **Kanał komunikacji:** Wyłącznie pisemny na priv (Useme). Nie proponować rozmów telefonicznych ani wideo.

### 1.4. Dlaczego ten segment jest kluczowy dla bota

Klient tech-agnostic:
- Nie porównuje technologii, bo jej nie zna — porównuje **efekt końcowy** i **poczucie bezpieczeństwa**.
- Jest bardziej lojalny wobec wykonawcy, który „mówi po ludzku”.
- Rzadziej negocjuje stawkę, jeśli oferta jest oparta na rezultacie, a nie na godzinach.
- Częściej wraca z kolejnymi zleceniami — automatyzacja jednego procesu rodzi potrzebę kolejnych.


## 2. ZASADY PSYCHOLOGICZNE I JĘZYKOWE

### 2.1. Kategoryczny zakaz żargonu programistycznego

**Zakazane słowa i frazy w ofercie dla segmentu tech-agnostic:**

| Zakazane | Zamiast tego |
|---|---|
| API | „program łączy się z Twoim systemem” |
| Backend / Frontend | „część programu widoczna dla Ciebie / część działająca w tle” |
| Deployment | „uruchomienie u Ciebie na komputerze” |
| Stack technologiczny | „narzędzia, na których to zbuduję” |
| Endpoint | „adres, pod który program wysyła zapytanie” |
| CRUD | „dodawanie, edytowanie, usuwanie danych” |
| Docker / Kubernetes | (nigdy nie wymieniać — to nie jest informacja dla klienta) |
| CI/CD | „automatyczne wdrażanie poprawek” |
| Repozytorium / Git | „miejsce, w którym trzymam wersje programu” |

### 2.2. Język rezultatu biznesowego — zasada nadrzędna

Każde zdanie w ofercie musi odpowiadać na jedno z pytań klienta:

1. **Co to dla mnie robi?**
2. **Jak to wygląda, gdy już działa?**
3. **Co się stanie, gdy Cię zabraknie?**

**Wzorce językowe do stosowania:**

- „Program działa w tle — jednym kliknięciem.”
- „Otwierasz komputer, na pulpicie jest ikona. Klikasz. Program robi resztę.”
- „Dane same trafiają tam, gdzie powinny — bez przepisywania.”
- „Oszczędzasz X godzin tygodniowo, które teraz zajmuje ręczne kopiowanie.”
- „Dostajesz plik, który możesz otworzyć w Excelu i wysłać do księgowej.”

**Wzorce językowe do eliminacji:**

- „Zbuduję REST API w FastAPI z Postgresem.”
- „Wdrożę kontener Dockerowy na VPS.”
- „Użyję Reacta z TypeScriptem.”
- „Zintegruję się z zewnętrznym endpointem.”

### 2.3. Zasada „trzech warstw komunikatu”

| Warstwa | Zawartość | Przykład |
|---|---|---|
| **Warstwa 1: Rezultat** | Co klient zobaczy i poczuje | „Faktury z maila same trafiają do Excelа.” |
| **Warstwa 2: Proces** | Jak to będzie wyglądało krok po kroku | „Najpierw pokażesz mi, jak to robisz teraz. Potem zbuduję program, który to przejmie. Na końcu dostaniesz ikonę na pulpicie.” |
| **Warstwa 3: Zabezpieczenie** | Co się stanie po zakończeniu współpracy | „Dostaniesz pełną dokumentację i nagranie, jak to obsługiwać. Program nie wymaga mnie do działania.” |


## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA NIETECHNICZNEGO

### 3.1. Strach przed konsolą tekstową

**Diagnoza:** Klient nietechniczny kojarzy „programowanie” z czarnym oknem, w którym trzeba wpisywać komendy. Ten obraz wywołuje paraliż decyzyjny — klient boi się, że nie będzie umiał obsługiwać tego, co dostanie.

**Konsekwencja dla oferty:** Nigdy nie wspominać o terminalu, wierszu poleceń, skryptach uruchamianych z konsoli. **Każde rozwiązanie musi mieć interfejs graficzny** — ikonę, przycisk, okno.

**Lek na strach w ofercie:** „Nie będziesz musiał nic wpisywać. Program uruchamia się tak samo jak przeglądarka — klikasz ikonę i działa.”

### 3.2. Strach przed zniknięciem programisty

**Diagnoza:** Klient nietechniczny boi się, że po zapłacie wykonawca zniknie, a on zostanie z „czymś, co nie działa i nikt tego nie naprawi”. To strach głębszy niż obawa o cenę.

**Konsekwencja dla oferty:** Każda oferta musi zawierać **element trwałego zabezpieczenia** — nie w formie ogólnika, ale konkretu:
- „Dostaniesz nagranie wideo, jak obsługiwać program.”
- „Kod i dokumentacja zostaną przekazane na Twoją własność.”
- „Program będzie działał na Twoim komputerze bez mojego udziału.”

### 3.3. Strach przed „technicznym bełkotem”

**Diagnoza:** Klient obawia się, że nie zrozumie tego, co wykonawca do niego pisze, i że zostanie „zagadany”. Reakcją obronną jest wybór oferty, która brzmi **najprościej** — nawet jeśli jest droższa.

**Konsekwencja dla oferty:** Każda oferta musi być **czytelna dla osoby bez wykształcenia technicznego**. Test: czy osoba po liceum, prowadząca sklep, zrozumie każde zdanie? Jeśli nie — przepisać.

### 3.4. Prawdziwy ból operacyjny i „Brudne Dane z Życia" (OBOWIĄZKOWY KONKRET BEZ ŻARGONU)

Oferta na ścieżce biznesowej NIE MOŻE składać się wyłącznie z gładkich obietnic („program zrobi wszystko sam jednym kliknięciem"). Żeby klient poczuł, że naprawdę znasz jego branżę, **musisz nazwać po ludzku 2–3 życiowe wyjątki i bałagan w danych, z którym on walczy na co dzień**:

| Branża / Proces | Brudne przypadki z życia (nazwij je prostym językiem w ofercie!) | Jak opisujesz rozwiązanie po ludzku |
|---|---|---|
| **Zamówienia na wymiar z Allegro / E-commerce / Stolarnia / Drukarnia** | Kupujący piszą wymiary w wiadomościach jak chcą: jeden podaje w `cm` (`100x50 cm`), drugi w `mm` (`1000x500 mm`), trzeci pisze słownie „dwie długie krawędzie oklejone, jedna krótka bez okleiny" albo zapomina podać kolor płyty czy kierunek usłojenia. | „Program sam przelicza centymetry na milimetry pod wymiar produkcyjny, rozpoznaje opis oklejania obrzeży, a jeśli klient zapomniał podać wymiaru lub koloru — od razu podświetla takie zamówienie do wyjaśnienia, zanim trafi na halę." |
| **Bot do maili firmowych / Obsługa zapytań klientów** | Klienci odpisują w długich wątkach pełnych cytowań starych wiadomości, stopki firmowej albo dorzucają załącznik (zdjęcie, PDF z zamówieniem). Przy nietypowym pytaniu zwykły bot potrafi zmyślić odpowiedź lub obiecać rabat, którego nie ma. | „Program oddziela nowe pytanie klienta od starej historii maila i podpisów, odczytuje treść załączników PDF, a gdy pytanie wykracza poza Wasze FAQ lub cennik — nie zgaduje, tylko przygotowuje szkic z wyraźnym oznaczeniem dla pracownika." |
| **Łączenie dwóch programów biurowych / Telefonia / CRM (np. CloudTalk, Notion, Pipedrive)** | Niższy pakiet abonamentowy blokuje dostęp do danych (np. brak transkrypcji w tańszym planie), albo jeden z systemów chwilowo nie odpowiada i notatka z rozmowy handlowca przepada lub zapisuje się podwójnie. | „Sprawdzamy od razu ograniczenia Waszego pakietu abonamentowego. Jeśli drugi program chwilowo nie odpowiada, rozmowa czeka w bezpiecznej kolejce w tle i dopisuje się automatycznie po powrocie połączenia, bez ryzyka zgubienia notatki lub duplikatów." |
| **Przepisywanie faktur, cenników i raportów do Excela** | Różne układy tabel od różnych dostawców, spacje i myślniki w numerach NIP, pomylone kolumny netto/brutto, zduplikowane pozycje z poprzedniego dnia. | „Program sam ujednolica układ kolumn, czyści numery NIP ze zbędnych znaków, sprawdza czy kwoty netto i brutto się zgadzają i pilnuje, żeby żaden dokument nie wpisał się dwa razy." |


## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

### 4.1. Zasada otwarcia

**Pierwsze 2 zdania oferty muszą opisywać stan docelowy — nie metodę, nie technologię, nie Twoje doświadczenie.**

Klient tech-agnostic czyta ofertę jak ogłoszenie o pracę: szuka potwierdzenia, że **ty rozumiesz jego problem** i **wiesz, jak będzie wyglądało rozwiązanie**.

### 4.2. Gotowe wzorce otwarć (do bezpośredniego użycia)

**Wzorzec A — Automatyzacja przepisywania danych:**
> „Wyobraź sobie, że faktury z maila same trafiają do Twojego Excela — bez przepisywania, bez błędów, bez siedzenia po godzinach. Program, który to robi, działa w tle i uruchamia się jednym kliknięciem.”

**Wzorzec B — Synchronizacja danych:**
> „Dane w Twoim sklepie i magazynie zawsze się zgadzają — bez ręcznego poprawiania. Program łączy oba systemy i aktualizuje wszystko automatycznie, gdy tylko pojawi się zmiana.”

**Wzorzec C — Raportowanie:**
> „Raport, który teraz zajmuje Ci godzinę w piątek, będzie gotowy w 10 sekund — jednym kliknięciem. Dostajesz plik, który możesz od razu wysłać dalej.”

**Wzorzec D — Powtarzalne maile:**
> „Maile do klientów wysyłają się same — w odpowiednim momencie, z właściwą treścią. Program pilnuje terminów i nie wymaga od Ciebie pamiętania o niczym.”

### 4.3. Czego nie umieszczać w pierwszych 2 zdaniach

- Swojego imienia i nazwiska (to miejsce jest w profilu).
- Lat doświadczenia.
- Nazw technologii.
- Pytań (pytania idą w środku analizy).
- Ceny (cena idzie w module wyceny).

### 4.4. Struktura pierwszych 2 zdań — schemat

```
[Stan docelowy: co klient zobaczy/poczuje] + [Mechanizm działania w języku laika: jak to będzie działać]
```

**Przykład rozwinięty:**
> „Przestaniesz przepisywać dane z faktur — będą same trafiać tam, gdzie powinny. Program działa w tle, uruchamiasz go ikoną na pulpicie, a on robi resztę: czyta dokument, wyciąga to, co ważne, i wpisuje do Excela.”


## 5. CZERWONA LISTA / ANTYWZORCE

### 5.1. Antywzorce w warstwie treści

| Antywzorzec | Dlaczego zabija ofertę |
|---|---|
| „Używam React, FastAPI, Postgres” | Klient nie wie, co to znaczy. Brzmi jak próba onieśmielenia. |
| „Mam 5 lat doświadczenia w programowaniu” | Klient nie kupuje doświadczenia — kupuje rozwiązanie problemu. |
| „Zbuduję REST API z endpointami” | Zero informacji o tym, co to da klientowi. |
| „Wdrożę na serwerze VPS z Dockerem” | Klient nie wie, co to VPS ani Docker. |
| „Proponuję spotkanie na Google Meet” | Zasada kanału: wyłącznie pisemnie na priv. |
| „To zależy od wielu czynników” | Brak konkretu = brak zaufania. |
| „Mogę to zrobić za X zł” bez rozbicia | Ryczałt bez modułów wywołuje opór. |

### 5.2. Antywzorce w warstwie pytań

| Antywzorzec | Poprawna alternatywa |
|---|---|
| „Jaki system operacyjny?” | „Na czym teraz pracujesz — Windows czy Mac?” |
| „Czy masz API?” | „Czy program, z którego korzystasz, ma możliwość eksportu danych?” |
| „Jaki masz stack?” | (Nigdy nie zadawać tego pytania) |
| „Czy znasz Pythona?” | (Nigdy nie zadawać tego pytania) |

### 5.3. Antywzorce w warstwie wizualnej i formatowania

- **Ściana tekstu bez akapitów** — klient nietechniczny przestaje czytać po 3 linijkach.
- **Brak nagłówków** — oferta musi mieć widoczne sekcje.
- **Tabele techniczne** — nie umieszczać specyfikacji technicznej w ofercie.
- **Emotikony w nadmiarze** — maksymalnie 1–2 na całą ofertę, wyłącznie dla oznaczenia sekcji.

### 5.4. Czerwone flagi po stronie klienta

| Sygnał | Ryzyko | Reakcja |
|---|---|---|
| „Potrzebuję tego na wczoraj” | Presja czasu = brak możliwości rzetelnego wdrożenia | Zaproponować etapowy zakres z jasnym terminem pierwszego modułu |
| „Mam już kogoś, kto to zaczął” | Ryzyko długu technicznego, konfliktu | Zapytać o zakres poprzedniej pracy i dostęp do kodu |
| „Nie wiem, czego dokładnie potrzebuję” | Brak zdefiniowanego problemu | Zaproponować krótki audyt/diagnozę jako pierwszy moduł |
| „Czy to będzie działać na moim komputerze?” | Brak zaufania do trwałości rozwiązania | Wzmocnić sekcję zabezpieczenia posprzedażowego |


## 6. PRODUKCYJNA ARCHITEKTURA WDROŻENIA BIZNESOWEGO

### 6.1. Zasada rozbicia wyceny

Wycena **nigdy nie jest ryczałtowa**. Klient tech-agnostic musi widzieć, za co płaci w każdym module. Ryczałt wywołuje pytanie „dlaczego tak drogo?”. Moduły wywołują pytanie „co dostanę w module 2?”.

### 6.2. Moduły wdrożenia (widełki 2 500 – 6 500 zł)

**MODUŁ 1: Diagnoza i projekt rozwiązania** | 400 – 800 zł
- Cel: zrozumienie, jak klient pracuje teraz, i zaprojektowanie programu „pod niego”.
- Co klient dostaje: prosty opis na piśmie, co program będzie robił i jak będzie wyglądał.
- Czas: 1–2 dni.
- Ryzyko dla klienta: minimalne — to etap, na którym można się wycofać.

**MODUŁ 2: Budowa rdzenia programu** | 1 200 – 3 200 zł
- Cel: zbudowanie działającego mechanizmu, który wykonuje główną czynność.
- Co klient dostaje: program, który już działa — można go przetestować na prawdziwych danych.
- Czas: 3–7 dni.
- Ryzyko dla klienta: średnie — widzi pierwszy rezultat.

**MODUŁ 3: Interfejs i wygoda obsługi** | 500 – 1 200 zł
- Cel: dodanie ikony na pulpit, okna programu, przycisku „uruchom”.
- Co klient dostaje: program, który obsługuje się jednym kliknięciem — bez konsoli, bez wpisywania komend.
- Czas: 1–3 dni.
- Ryzyko dla klienta: niskie — widzi, że to będzie łatwe w obsłudze.

**MODUŁ 4: Testy na prawdziwych danych i poprawki** | 400 – 800 zł
- Cel: sprawdzenie, czy program działa na rzeczywistych plikach klienta.
- Co klient dostaje: pewność, że program nie wysypie się na jego danych.
- Czas: 1–2 dni.
- Ryzyko dla klienta: minimalne.

**MODUŁ 5: Przekazanie, nagranie instruktażowe i zabezpieczenie** | 300 – 500 zł
- Cel: klient zostaje samodzielny — nie jest zależny od wykonawcy.
- Co klient dostaje: nagranie wideo „jak to obsługiwać”, plik z programem, krótką instrukcję na piśmie.
- Czas: 1 dzień.
- Ryzyko dla klienta: zerowe — to moment, w którym czuje się bezpiecznie.

### 6.3. Tabela decyzyjna — kiedy który moduł

| Budżet klienta | Rekomendowany zakres | Moduły |
|---|---|---|
| 1 500 – 2 500 zł | Minimalny | 1 + 2 (uproszczony) + 5 |
| 2 500 – 4 000 zł | Standardowy | 1 + 2 + 3 + 5 |
| 4 000 – 5 500 zł | Rozszerzony | 1 + 2 + 3 + 4 + 5 |
| 5 500 – 7 000 zł | Kompletny | Wszystkie + moduł dodatkowy (np. integracja z drugim systemem) |

### 6.4. Kontekst rynkowy dla wyceny

Dla porównania: wdrożenie automatyzacji jednego procesu w małej firmie w Polsce kosztuje w 2026 roku od 3 000 do 15 000 zł jednorazowo. Wycena 2 500 – 6 500 zł mieści się w **dolnej połowie widełek rynkowych** — to argument, że oferta jest konkurencyjna, a jednocześnie uczciwie wyceniona.

Średnia wartość projektu programistycznego na Useme to ponad 5 000 zł. Nasza wycena dla segmentu tech-agnostic **nie odbiega od średniej rynkowej**, ale jest **lepiej uzasadniona** — przez rozbicie na moduły.


## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE DLA KLIENTA BIZNESOWEGO

### 7.1. Zasada zadawania pytań

Pytania kwalifikujące umieszcza się **w środku analizy oferty** — po opisaniu rezultatu, ale przed wyceną. Cel: **zmusić klienta do natychmiastowego odpisania na priv** i wejścia w tryb dialogu.

Pytania muszą być:
- **Zamknięte w formie** (klient może odpowiedzieć krótko), ale **otwarte w treści** (odpowiedź ujawnia kontekst).
- **Zrozumiałe bez wiedzy technicznej.**
- **Maksymalnie 2–3 pytania na ofertę** — więcej wywołuje przeciążenie.

### 7.2. Gotowe zestawy pytań (do wyboru w zależności od typu zlecenia)

**Zestaw A — dla zleceń automatyzacji przepisywania danych:**

1. „Ile czasu zajmuje Ci teraz ręczne przepisywanie danych — godzina dziennie, kilka godzin w tygodniu?”
2. „Czy dane, które przepisujesz, mają zawsze taki sam format, czy zdarzają się wyjątki?”
3. „Czy program, z którego teraz korzystasz, pozwala na eksport danych do pliku Excel/CSV?”

**Zestaw B — dla zleceń synchronizacji między systemami:**

1. „Z jakich programów teraz korzystasz — czy oba działają na tym samym komputerze, czy w przeglądarce?”
2. „Co się dzieje teraz, gdy dane się nie zgadzają — kto to poprawia i ile to zajmuje?”
3. „Czy dane muszą być aktualizowane natychmiast, czy wystarczy raz dziennie?”

**Zestaw C — dla zleceń raportowania:**

1. „Jak często potrzebujesz raportu — codziennie, co tydzień, raz w miesiącu?”
2. „Co dokładnie zawiera raport — jakie kolumny, jakie podsumowania?”
3. „Komu wysyłasz raport i w jakiej formie — plik Excel, PDF, wiadomość mailowa?”

**Zestaw D — dla zleceń ogólnych (bez sprecyzowanego typu):**

1. „Która czynność w Twojej pracy zajmuje najwięcej czasu i jest najbardziej powtarzalna?”
2. „Czy korzystasz z komputera z systemem Windows, czy pracujesz głównie w przeglądarce?”
3. „Kiedy program będzie gotowy — czy chcesz go uruchamiać na swoim komputerze, czy ma działać w tle bez Twojej obecności?”

### 7.3. Czego nie umieszczać w pytaniach

- Nazw technologii („Czy masz API?”, „Jaki masz system operacyjny?”).
- Pytań o budżet wprost („Ile możesz zapłacić?”) — budżet wynika z zakresu.
- Pytań o termin, jeśli nie zaproponowano jeszcze modułów.
- Pytań, na które klient nie zna odpowiedzi („Czy dane są w formacie JSON?”).

### 7.4. Mechanizm psychologiczny

Pytania kwalifikujące działają na zasadzie **„przerwy w monologu”**. Klient tech-agnostic czyta ofertę pasywnie — dopóki nie natrafi na pytanie. Pytanie **wymusza aktywność**: musi przetworzyć odpowiedź, wrócić do swojego komputera, sprawdzić, jak coś działa. To buduje zaangażowanie.

Dodatkowo: pytania pokazują, że **wykonawca myśli o kliencie jako o partnerze**, a nie jako o „zleceniodawcy, któremu się coś zbuduje”. To różnica między ofertą, która wygrywa, a ofertą, która ginie w tłumie.

---

## PODSUMOWANIE OPERACYJNE DLA BOTA

| Element | Zasada kluczowa |
|---|---|
| **Otwarcie** | 2 zdania o stanie docelowym, zero żargonu, zero doświadczenia |
| **Język** | Rezultat biznesowy, ikona na pulpicie, jeden klik |
| **Strach klienta** | Adresować konsolę („nie będziesz musiał nic wpisywać”) i zniknięcie („dostaniesz nagranie i dokumentację”) |
| **Antywzorce** | Zero stacku, zero pytań technicznych, zero rozmów wideo |
| **Wycena** | Moduły: diagnoza → rdzeń → interfejs → testy → przekazanie |
| **Pytania** | 2–3 chirurdzy w środku analizy, język formatu i wygody |
| **Kanał** | Wyłącznie pisemnie na priv Useme |

**Cel nadrzędny:** Klient tech-agnostic nie kupuje kodu. Kupuje **spokój, oszczędność czasu i pewność, że program będzie działał, gdy wykonawca zniknie z horyzontu**. Oferta, która to komunikuje, wygrywa.