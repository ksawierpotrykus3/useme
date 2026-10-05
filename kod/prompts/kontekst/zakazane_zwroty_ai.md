# Zakazane zwroty i konstrukcje — anty-AI

Ten plik jest wynikiem analizy liczbowej 180 ofert konkurencji z trzech zleceń testowych
(145285 Subiekt+BaseLinker, 145287 aplikacja mobilna, 144890 Comarch Optima OCR).
Nie jest to lista "brzydkich słów". To lista rzeczy, które **statystycznie zdradzają AI**
albo **nie wyróżniają nas na tle 60 innych ofert**.

Dwie listy. Lista A to rzeczy częste u konkurencji. Lista B to twarde AI-izmy.

---

## LISTA A: CZĘSTE U KONKURENCJI — NIE WYRÓŻNIAJĄ

To nie są błędy same w sobie. Problem w tym, że używa ich **każdy**. Jeśli napiszesz
"Dzień dobry" i "Pozdrawiam" jak wszyscy, jesteś jednym z 60. Jeśli musisz ich użyć,
użyj świadomie i nie buduj na nich wartości oferty.

Dane z korpusu (180 ofert, 3 zlecenia: 145285, 145287, 144890):

| Zwrot / konstrukcja | Wystąpienia | Uwaga |
|---|---|---|
| "Dzień dobry" jako otwarcie | ~113 | Standard. Nie jest zły, ale nie jest twój. |
| "Pozdrawiam" jako podpis | ~83 | Standard. |
| "mam doświadczenie", "posiadam doświadczenie" | ~37 | Ogólnik. Zakazany osobno w regułach (brak portfolio). |
| "realizowałem", "zrealizowałem", "budowałem", "stworzyłem" | ~12 | Ogólnik. |
| "posiadam", "posiadamy" | ~17 | Korporacyjne. |
| "zapewniam", "zapewniamy" | ~19 | Obietnica bez pokrycia. |
| "gwarantuję", "gwarantujemy" | ~4 | Tylko 30 dni rozruchowych. |
| "znam", "znamy" | ~13 | Puste. |
| "w pełni" | ~11 | Wata. |
| "profesjonalnie" | ~3 | Puste. |
| "kompleksowo", "rzetelnie" | 1-2 | Puste. |
| "solidnie", "skutecznie", "efektywnie" | 0-3 | Puste. |
| "indywidualne podejście", "nowoczesne rozwiązania", "najwyższa jakość" | 0 | Puste. |

**UWAGA — najczęstsze w 144890 (nie słowa, a FORMA):**
- Punktory od myślnika "-" na początku linii: **48 wystąpień**
- Etykiety z dwukropkiem w prozie ("Czas realizacji:", "Cena:"): **33 wystąpienia**
- Listy numerowane "1. 2. 3.": **26 wystąpień**

To znaczy, że konkurencja masowo używa formatowania dokumentacyjnego. U nas to jest
zakazane (Żelazne Zakazy pkt 8). To jest nasza realna przewaga, nie ozdoba.

**Zasada dla Listy A:** Jeśli zdanie da się skrócić, usuwając z niego zwrot z tej listy,
i nadal znaczy to samo — usuń zwrot. "Zapewniam, że dostarczę na czas" → "Dostarczę na czas".
"Mam doświadczenie w integracjach" → pokaż konkret zamiast deklaracji.

---

## LISTA B: DOSŁOWNIE WIDAĆ AI — ZAKAZ CAŁKOWITY

Te konstrukcje są rozpoznawalne natychmiast. Nie "brzmią trochę jak AI" — **są** AI.
Zakaz bez wyjątków, niezależnie od kontekstu i długości zlecenia.

### B1. Etykiety i nagłówki w środku prozy
Model uwielbia "porządkować" tekst etykietami. Człowiek tak nie mówi.
- "Dlaczego to ważne:"
- "Co proponuję:"
- "Kluczowa mina:"
- "Pytanie kwalifikujące:"
- "Na koniec:", "Podsumowując:", "Reasumując:"
- "Warto zauważyć, że", "Należy pamiętać, że", "Warto podkreślić, że"

Zasada: jeśli w tekście jest człon zakończony dwukropkiem, który nie jest naturalnym
wprowadzeniem do wyliczenia w rozmowie — wywal go. Zdanie ma płynąć.

### B2. Anonsowanie, co się zaraz zrobi
Model zapowiada swoje ruchy. Człowiek po prostu mówi.
- "Zanim jednak przejdę do...", "Zanim przejdę do..."
- "Chciałbym teraz omówić...", "Przejdźmy do..."
- "Na wstępie", "Tytułem wstępu", "Zacznijmy od..."

Zasada: usuń zapowiedź, zostaw treść. "Zanim jednak przejdę do SEO, jedna rzecz: ..."
→ "Jedna rzecz: ..." (a jeszcze lepiej bez "jedna rzecz").

### B3. Echo klienta
Model streszcza to, co klient napisał, i oddaje mu to z powrotem.
- "Pisze Pani o...", "Wspomina Pan, że...", "Jak Pan zauważył..."
- "Rozumiem, że zależy Państwu na..."
- Powtarzanie terminów z ogłoszenia bez dodania wartości.

Zasada: każde zdanie musi wnosić informację, której klient jeszcze nie ma. Jeśli jego
treść występuje też w opisie zlecenia — wytnij.

### B4. Coaching i sztuczna empatia
- "Doskonale rozumiem", "Rozumiem doskonale"
- "Czytam Twoje ogłoszenie i widzę, że..."
- "Prowadzenie firmy to przede wszystkim..."
- "Przyznam szczerze", "Nie ukrywam", "Mówiąc wprost"

Zasada: zero. Nie komentujemy klienta, nie współodczuwamy. Mówimy o sprawie.

### B5. Kapitulacja i wycofanie
Model chce być "uczciwy" i "nie nachalny", więc się wycofuje.
- "Jeśli to za mało, rozumiemy."
- "Jeśli to nie pasuje, proszę o informację."
- "Rozumiem, jeśli wybierze Pan inną ofertę."
- "Mam nadzieję, że to pomoże."

Zasada: zdanie, które brzmi jak rezygnacja, wywal całe. Jeśli przyznajesz brak (skromność),
obok MUSI stać konkret z tego zlecenia, który go zastępuje. Bez konkretu — wywal całe zdanie.

### B6. Konstrukcje-szkielety
Powtarzalne matryce zdaniowe, które model uwielbia:
- "Nie X, ale Y" — jako ozdobnik, nie jako realny kontrast (27 wystąpień w 60 ofertach)
- "Zamiast X proponuję Y" — gdy X jest oczywisty
- "Jeśli X, to Y" — jako wypełniacz (29 wystąpień)
- "To nie jest X. To jest Y."
- "Nie chodzi o X. Chodzi o Y."

Zasada: jeśli konstrukcja jest ozdobą, a nie realnym kontrastem — przepisz na zwykłe zdanie.
Test: czy da się to samo powiedzieć bez matrycy? Jeśli tak, mów bez.

### B7. Em-dash i pauza
Znak `—` to najczęstszy marker AI w polskim tekście. W korpusie 85 wystąpień
w jednym zbiorze (145287), gdy w drugim (145285) tylko 5. To znaczy, że konkurencja
używa go masowo, a my mamy zakaz (Żelazne Zakazy pkt 1).
- `—` em-dash
- `–` półpauza
- ` - ` dywiz w spacjach

Zasada: zero. Zdania łączymy przecinkami, kropkami, spójnikami.

### B8. Formatowanie dokumentacyjne
- Listy numerowane `1. 2. 3.` (28 z 60 ofert w 145287)
- Punktory `-`, `•`, `*` (35 z 60 ofert w 145287)
- Nagłówki markdown `#`, `##`
- Tabele `|`
- Pogrubienia `**`

Zasada: zero. Piszemy prozą. Jeśli coś jest listą, ujmujemy to w zdaniu.

### B9. Wewnętrzny żargon, który wyciekł z promptu
Formułki z naszych własnych promptów, które nie mają sensu dla klienta.
- "Obaj robimy to, czego wymaga zlecenie."
- "Robimy to, czego wymaga zlecenie."
- "Działamy w duecie."

Zasada: jeśli zdanie nie znaczy nic dla klienta bez znajomości naszego promptu — wywal.

---

## SKROMNOŚĆ: NIE POSTAWA, LECZ BILANS

Skromność nie jest kategorią samą w sobie. Jest **uczciwym bilansem: czego nie mamy —
i co konkretnie to zastępuje.** Jeśli druga strona bilansu jest pusta albo jest cechą
charakteru ("jesteśmy uczciwi", "zależy nam"), to nie jest bilans — to skarga.
Wtedy wywalamy całe zdanie, nie tylko skromność.

Test:
> Jeśli w zdaniu jest przyznanie braku — znajdź obok konkret, który go zastępuje.
> Jeśli obok stoi: cecha charakteru, nastrój, albo nic — wywal całe zdanie.

Przykłady z korpusu (działają):
- "Nie mamy portfolio, ale możemy pokazać, jak podchodzimy do audytu." → konkret jest.
- "Uczciwie: aplikacji w sklepie nie mam. Zrobiłem Tapebook, działa offline." → konkret jest.
- "Jeśli to za mało, rozumiemy." → nic obok → wywal całe.

---

## TEST KOŃCOWY (do wykonania po napisaniu oferty)

Przeczytaj gotowy tekst i zadaj sobie trzy pytania:

1. Czy którekolwiek zdanie da się skrócić, usuwając z niego zwrot z Listy A?
   Jeśli tak, usuń.
2. Czy w tekście jest cokolwiek z Listy B? Jeśli tak, przepisz.
3. Czy któreś zdanie brzmi jak coś, co napisałoby inne AI?
   Jeśli tak, oferta jest do wymiany.

---

## SKĄD TE DANE

Analiza liczbowa 180 ofert z trzech zleceń testowych konta weronikabuchholc13
(04_moje_zlecenia). Liczone maszynowo (subagenty), nie z pamięci. Pełne raporty
w badaniach. Wnioski jakościowe z rozmowy z Ksawierem o tym, dlaczego skromność
bez konkretu brzmi źle i jak odróżnić "skromność z zamiennikiem" od "kapitulacji".