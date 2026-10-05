# STOPIEŃ 3: Poszlaki Niszowe (Pewność 20% – 40%)

> Kryterium kwalifikacji: Bardzo mała próba statystyczna ($n < 15$), pojedyncze wygrane Ksawiera, wysoka wariancja losowa ($\pm 25-40\%$). Dane te NIE są powtarzalnym lejkiem skali, lecz wskazówkami do dalszej obserwacji.

---

## POSZLAKA 3.1: Anomalia "TopSolid / CAD / CAM" (50% Win Rate)

- **Dane surowe**:
  - Liczba zleceń: $n = 2$.
  - Wygrane: 1.
  - Przegrane: 1.
  - Pozorny Win Rate: **50.00%**.
- **Ocena**:
  Brak jakiejkolwiek istotności statystycznej. Wynik to pojedyncze zlecenie, w którym specyficzna wiedza Ksawiera z zakresu skryptów dla obrabiarek/CAD trafiła na brak jakichkolwiek innych ofert na Useme.
- **Wniosek operacyjny**:
  Jeśli pojawi się zlecenie z hasłem CAD/CAM/TopSolid, bot wysyła ofertę w trybie VIP Fast-Track, ale nie wolno budować na tym prognoz finansowych.

---

## POSZLAKA 3.2: Nisza "VoIP / Asterisk / SIP" (40% Win Rate)

- **Dane surowe**:
  - Liczba zleceń: $n = 5$.
  - Wygrane: 2.
  - Przegrane: 3.
  - Pozorny Win Rate: **40.00%**.
- **Ocena**:
  Telefonia internetowa, centrale VoIP i integracje z bramkami SMS mają bardzo mało zgłoszeń od typowych web-developerów. 2 wygrane na 5 prób to obiecujący wynik, jednak próba $n=5$ oznacza margines błędu $\pm 35\%$.

---

## POSZLAKA 3.3: Integracje E-commerce Polskich Platform (IdoSell 33.3%, PrestaShop 11.8%)

- **Dane surowe**:
  - IdoSell: $n = 9$, wygrane = 3, **Win Rate = 33.33%**.
  - PrestaShop: $n = 17$, wygrane = 2, **Win Rate = 11.76%**.
  - Baselinker: $n = 4$, wygrane = 0, **Win Rate = 0.00%**.
- **Ocena**:
  IdoSell wykazuje wyższą skuteczność niż WooCommerce i Shopify, prawdopodobnie dlatego, że polscy sprzedawcy na IdoSell mają większe obroty i wyższe budżety na dedykowane integracje API niż mikro-sprzedawcy na darmowym WooCommerce.

---

## POSZLAKA 3.4: Systemy ERP i Przemysł (Enova365, Comarch Optima, Odoo)

- **Dane surowe**:
  - Enova365: $n = 3$, wygrane = 1 (Case CB Kołcz - 5500 PLN).
  - Comarch ERP / Optima: $n = 5$, wygrane = 1.
  - Odoo ERP: $n = 6$, wygrane = 1.
- **Ocena**:
  Klienci korporacyjni i przemysłowi rzadko zlecają na Useme, ale gdy to robią, płacą wysokie stawki bez negocjacji groszowych. Jednak częstotliwość pojawiania się tych zleceń to zaledwie 1-2 w miesiącu.

---

## POSZLAKA 3.5: Czas Reakcji na Wiadomości Priv (< 15 Minut)

- **Założenie**:
  Klient, który otrzymał odpowiedź w ciągu pierwszego kwadransa od zadania pytania na priv, ma 3-krotnie większe prawdopodobieństwo sfinalizowania umowy niż klient, który czekał 4 godziny.
- **Ocena**:
  Prawdopodobieństwo behawioralne wysokie, ale brak zautomatyzowanego pomiaru w obecnej wersji silnika (wymaga wdrożenia modułu asynchronicznego monitorowania powiadomień).

---

## POSZLAKA 3.6: Farma treści AI pod SEO (143289)

- **Cytat**: „opis każdej stacji do wprowadzenia poprzez API CHATGPT albo ręcznie" + „BLOG … automatycznie przerabiane teksty poprzez API CHATGPT".
- **Interpretacja**: nacisk na automatyczną generację treści pod tysiące podstron = farma treści pod SEO, nie realny serwis. Ryzyko pracy przy projekcie o wątpliwej wartości biznesowej i reputacyjnej.
- **Dowody obserwacyjne**: $n = 1$ (143289).
- **Źródło**: subagent analiza 143289.
- **Powiązane**: typ `spekulacyjny_niedopasowany_budzet`.

---

## POSZLAKA 3.7: Pośrednik na Useme — sygnały, zaniżanie budżetu, podwójna rola (143698, KARTS)

- **Cytat**: „dla strony mojego klienta" (143698).
- **Interpretacja**: zwroty „mój klient", „dla naszego klienta" = pośrednik szuka podwykonawcy, często z marżą w dół ceny. Firma designu (KARTS: 143507, 143275, 143548, 143562, 143652) bywa jednocześnie zleceniodawcą i wykonawcą. Wariant: pośrednik zaniża budżet, bo sam chce zarobić.
- **Dowody obserwacyjne**: $n \ge 2$ (143698, KARTS jako seria).
- **Źródło**: subagent analiza 143698 + obserwacja serii KARTS.
- **Powiązane**: typ `spekulacyjny_niedopasowany_budzet`, `firmowy_wymagajacy`.

---

## POSZLAKA 3.8: Część „zleceń" to zbieranie wycen pod dofinansowanie lub przetarg (143618, 143507, 143344)

- **Interpretacja**: formalny język urzędowy, prośba o wycenę modułową, brak budżetu = dokument do wniosku o dofinansowanie. Wariant: szczegółowy brief z pytaniem o wycenę modułową to zbieranie danych do przetargu, nie realny projekt.
- **Dowody obserwacyjne**: $n = 3$ (143618 ARR ARES, 143507 KARTS, 143344 patrykb).
- **Źródło**: subagent analizy 143618, 143344.
- **Powiązane**: typ `firmowy_wymagajacy`.

---

## POSZLAKA 3.9: „Możliwa dalsza współpraca" to często hak na obniżenie stawki (143652)

- **Cytat**: „możliwa dalsza współpraca" (143652, Albert — Shopify).
- **Interpretacja**: obietnica ciągłości bez konkretów = klasyczny mechanizm presji na niższą cenę teraz („pierwsze zlecenie taniej, potem się odbijemy").
- **Dowody obserwacyjne**: $n = 2$ (143652, 143562).
- **Źródło**: subagent analiza 143652.
- **Powiązane**: typ `lakoniczny_minimalista`, `indywidualny_mikro_budzet`.

---

## POSZLAKA 3.10: Instytucjonalny-pilotażowy — konkretny budżet + szkolenie = pilotaż pod większy projekt (143924)

- **Cytat**: „Zlecenie obejmuje wdrożenie, testy, instrukcję oraz szkolenie prowadzących."
- **Interpretacja**: pełny cykl wdrożeniowy z dokumentacją i szkoleniem przy realistycznym budżecie sugeruje pilotaż — jeśli się sprawdzi, klient wróci z kolejnymi modułami. Warto traktować jako wejście do relacji długoterminowej.
- **Dowody obserwacyjne**: $n = 1$ (143924).
- **Źródło**: subagent analiza 143924.
- **Powiązane**: typ `swiadomy_wymagajacy`.

---

## POSZLAKA 3.11: Wewnętrzne wsparcie techniczne = zleceniodawca celowo zawęża odpowiedzialność wykonawcy (143287)

- **Cytat**: „my odpowiadamy za ogarnięcie integracji po stronie naszego CRM / Manago AI. Wykonawca tylko wysyła ustrukturyzowane dane."
- **Interpretacja**: klient ma własnych programistów i celowo odcina kosztowny zakres — to przygotowanie, ale i kontrola kosztów. Wyceniaj tylko to, co naprawdę do Ciebie należy; nie rozszerzaj zakresu z własnej inicjatywy.
- **Dowody obserwacyjne**: $n = 1$ (143287).
- **Źródło**: subagent analiza 143287.
- **Powiązane**: typ `swiadomy_wymagajacy`.

---

## POSZLAKA 3.12: Duża liczba ofert przy ogólnikowym opisie = sondowanie ceny lub ankietyzacja rynku

- **Interpretacja**: im prostsze zadanie i więcej ofert, tym większa presja na niską cenę. Przy 100+ ofertach to często ankietyzacja rynku, nie realny projekt. Sygnał do odpuszczenia lub wejścia wyłącznie z ceną bardzo konkurencyjną.
- **Dowody obserwacyjne**: $n = 4$ (143308 — 150 ofert, 143618 — 103, 143562 — 50, 143652 — 48).
- **Źródło**: subagent analiza rozkładu ofert.
- **Powiązane**: typ `lakoniczny_minimalista`, `indywidualny_mikro_budzet`, `firmowy_wymagajacy`.

---

## POSZLAKA 3.13: „Dokończenie po kimś" to osobna kategoria ryzyka (143548)

- **Interpretacja**: przejmowanie cudzego kodu bez repo/dokumentacji = ryzyko ukrytych błędów. Wyceniaj z zapasem, nigdy nie obiecuj ceny „jak za nowy projekt".
- **Dowody obserwacyjne**: $n \ge 1$ (143548 EVERWOOD — zaawansowana wtyczka, „co wymaga dokończenia").
- **Źródło**: subagent analiza 143548.
- **Powiązane**: typ `ekspert_egzekucyjny`, modyfikator `rescue`.

---

> Poniższe poszlaki pochodzą z odzyskanego zbioru `_odzyskane/wiedza_biznesowa/notatki_i_teorie/teorie.md` (scalenie 2026-09-30). Wszystkie mają małą próbę ($n = 1$–3), więc metodologicznie należą do Stopnia 3.

## POSZLAKA 3.14: Ludzie używają AI do oceniania ofert AI
- **Cytat/teza**: przy 50+ ofertach zleceniodawcy wrzucają oferty do AI, żeby wybrało najlepsze. Oferta musi być zoptymalizowana pod ocenę AI.
- **Interpretacja**: proste zdania, słowa kluczowe z opisu, bez ozdobników, jasna deklaracja, konkretne liczby.
- **Dowody obserwacyjne**: $n = 0$ (teoria metody, wymaga testu).
- **Źródło**: korekta użytkownika 2026-09-09.
- **Powiązane**: teorie metody.

---

## POSZLAKA 3.15: Monolit może być optimum, a metodyka anty-monolitu może być błędna
- **Teza**: dominująca strategia to baseline, nie optimum. Sama metodyka szukania lepszych strategii jest nieprzetestowana.
- **Interpretacja**: możliwe, że nie da się rozbić oferty na komponenty; monolit jest optimum, a błąd atrybucji nigdy nie wystąpi.
- **Dowody obserwacyjne**: $n = 0$ (teoria metody).
- **Źródło**: korekta użytkownika 2026-09-09.
- **Powiązane**: teorie metody.

---

## POSZLAKA 3.16: Długość opisu nie zawsze koreluje z wielkością zakresu
- **Źródło**: 143750 (Notion, 1 zdanie, duży CRM), 143747 (SQL, 1 zdanie, infrastruktura).
- **Interpretacja**: jedno zdanie może kryć duży projekt; zawsze doprecyzować przed wyceną.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `lakoniczny_minimalista`.

---

## POSZLAKA 3.17: Lakoniczność + „do negocjacji" = delegacja całości na wykonawcę
- **Źródło**: 143750 (Adam — Notion CRM), 143355 (Jacek — sklep zoo).
- **Interpretacja**: klient nie chce specyfikować, oczekuje, że wykonawca zgadnie zakres.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `lakoniczny_minimalista`.

---

## POSZLAKA 3.18: Firma może pisać emocjonalnie i kreatywnie, nie tylko formalnie
- **Źródło**: 143916 (Perca — landing page, „porwie nas i klientów :)").
- **Interpretacja**: formalny ≠ firmowy; liczy się ton i oczekiwany efekt.
- **Dowody obserwacyjne**: $n = 1$.
- **Powiązane**: typ `firmowy_emocjonalny`.

---

## POSZLAKA 3.19: Świadomy klient indywidualny potrafi mieć mentalność korporacyjną (twarde MUST HAVE)
- **Źródło**: 143994 (Aleksandra — Google Ads, „MUST HAVE!").
- **Interpretacja**: osoba prywatna może stawiać warunki jak firma; odpowiedź musi być dopasowana do briefu.
- **Dowody obserwacyjne**: $n = 1$.
- **Powiązane**: typ `swiadomy_wymagajacy`.

---

## POSZLAKA 3.20: Ekspert-egzekucyjny nie chce edukacji, tylko wykonania z autonomią
- **Źródło**: 143665 (Michał — SEO Litwa), 144045 (kodiwo — WordPress).
- **Interpretacja**: odrzuca półprodukty; proponować metodę i jakość, nie podstawy.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `ekspert_egzekucyjny`.

---

## POSZLAKA 3.21: Ogłoszenie o pracę bywa maskowane jako zlecenie freelancerskie
- **Źródło**: 143650 (Dialog Key), 143318 (Bruno Prusaczyk), 143767 (Aethon AI Labs).
- **Interpretacja**: link do zewnętrznego ATS lub sekcja „How to Apply" = rekrutacja, nie projekt.
- **Dowody obserwacyjne**: $n = 3$.
- **Powiązane**: typ `rekrutacyjny_pod_przykrywka`.

---

## POSZLAKA 3.22: Ekspercki opis może iść w parze z rażąco zaniżonym budżetem
- **Źródło**: 143589 (MERN, 10k USD), 143318 (AI senior, $2000/mies.).
- **Interpretacja**: im większy rozjazd wymagania/budżet, tym mniejsze szanse na realny projekt.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `spekulacyjny_niedopasowany_budzet`.

---

## POSZLAKA 3.23: Firma może stawiać twarde wymagania przy zerowej specyfikacji produktu
- **Źródło**: 143273 (KARTS DESIGN iOS), 143274 (KARTS DESIGN R&D).
- **Interpretacja**: referencje jako filtr wejścia, a sam projekt nieopisany — to selekcja, nie brief.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `firmowy_wymagajacy`, `lakoniczny_minimalista`.

---

## POSZLAKA 3.24: Zlecenie wymagające fizycznej obecności tworzy osobny segment
- **Źródło**: 143823 (konfiguracja MikroTik, Łódź on-site).
- **Interpretacja**: twarda lokalizacja + mała pula ofert = inna dynamika niż typowy fix zdalny.
- **Dowody obserwacyjne**: $n = 1$.
- **Powiązane**: potencjalny typ `lokalny_fizyczny_fix`.

---

## POSZLAKA 3.25: Startup szuka „partnera-lidera", nie wykonawcy
- **Źródło**: 143767 (Aethon AI Labs — „nie szukamy wykonawcy do prostego kodowania").
- **Interpretacja**: milestone-based + wizja bez konkretów = ryzyko niestabilnych płatności.
- **Dowody obserwacyjne**: $n = 1$.
- **Powiązane**: typ `ekspert_egzekucyjny`, `rekrutacyjny_pod_przykrywka`.

---

## POSZLAKA 3.26: Rekrutera pod przykrywką rozpoznaje się po kombinacji 5 sygnałów
- **Źródło**: 143650, 143318, 143767.
- **Interpretacja**: 1 sygnał = podejrzenie, 2–3 = prawdopodobne, 4–5 = pewne. Sygnały: (1) cel to etat/kontrakt, (2) link do zewnętrznego ATS/portalu (najsilniejszy), (3) struktura HR (Responsibilities/Qualifications/How to Apply), (4) wymagania jak do etatu, (5) ton rekrutera.
- **Dowody obserwacyjne**: $n = 3$.
- **Powiązane**: typ `rekrutacyjny_pod_przykrywka`.

---

## POSZLAKA 3.27: Wysoki próg wejścia (raport, referencje) to filtr jakości, nie zła wola
- **Źródło**: 143681 (przegląd techniczny — wymóg zanonimizowanego raportu), 143721 (enova — 2 referencje + pytanie techniczne).
- **Interpretacja**: to nie pułapka — ekspert chce sprawdzić warsztat przed oddaniem projektu.
- **Dowody obserwacyjne**: $n = 2$.
- **Powiązane**: typ `swiadomy_wymagajacy`, `ekspert_egzekucyjny`.

---

## POSZLAKA 3.28: Edukacyjny-lękowy — motywacją jest uniknięcie katastrofy, nie produkt
- **Cytat**: „Wiec potrzebuje domenę skonfigurować aby mi skrzynki e-mail nie sparaliżowało."
- **Interpretacja**: prawdziwy priorytet to ciągłość skrzynek firmowych, nie strona; klient boi się zepsuć coś, co działa — trzeba zarządzać lękiem, nie tylko technologią.
- **Dowody obserwacyjne**: $n = 1$ (143904).
- **Powiązane**: typ `swiadomy_edukacyjny`.

---

## POSZLAKA 3.29: Lakoniczny-biznesowy — zna cel, nie zna mechanizmu („chyba" otwiera pole)
- **Cytat**: „Zlecę konfigurację przez API chyba."
- **Interpretacja**: klient zna nazwy narzędzi i efekt (transkrypcje→CRM), ale nie wie JAK; słowo „chyba" = otwarty na alternatywę no-code (n8n/Zapier), a nie na programowanie.
- **Dowody obserwacyjne**: $n = 1$ (143981).
- **Powiązane**: typ `lakoniczny_minimalista`.

---

## POSZLAKA 3.30: Przejmowanie kodu AI — „Powstał w Lovable" = refaktoryzacja, nie rozwój
- **Cytat**: „System jest już zbudowany i działa. Powstał w Lovable, kod jest w React/TypeScript, backend oparty jest o Supabase."
- **Interpretacja**: kod generowany AI bywa niespójny i bez testów — pod „dalszym rozwojem" kryje się potrzeba refaktoryzacji; wyceniaj z zapasem na zrozumienie cudzego kodu.
- **Dowody obserwacyjne**: $n = 1$ (143861).
- **Powiązane**: typ `ekspert_egzekucyjny`, `dokończenie po kimś`.

---

## POSZLAKA 3.31: „Umowa na część etatu" pod pozorem freelancera = fałszywe B2B
- **Cytat**: „rozliczenie przez Useme lub umowa na część etatu".
- **Interpretacja**: klient chce stałej dyspozycyjności i zaangażowania pracownika, ale bez ZUS/urlopów; sygnał fałszywego B2B — wyceniaj czas dyspozycyjności, nie tylko zadania.
- **Dowody obserwacyjne**: $n = 1$ (143325).
- **Powiązane**: typ `firmowy_wymagajacy`, `rekrutacyjny_pod_przykrywka`.

---

## POSZLAKA 3.32: Marketingowy wariant rekrutacyjny — emoji + „cykliczne zlecenia" bez konkretu
- **Cytat**: „Świetnie się składa" + „Cykliczne zlecenia… Projekty o różnej skali" + „Wymagane funkcje: W zależności od zlecenia".
- **Interpretacja**: to budowanie bazy wykonawców przez agencję, nie konkretne zlecenie; obietnice stałej pracy bez briefu przyciągają masowo, ale realne zlecenia mogą być niskomarżowe lub nigdy nie nadejść.
- **Dowody obserwacyjne**: $n = 1$ (143314).
- **Powiązane**: typ `rekrutacyjny_pod_przykrywka`.
