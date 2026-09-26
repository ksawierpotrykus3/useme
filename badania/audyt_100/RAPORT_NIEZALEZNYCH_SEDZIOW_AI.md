# RAPORT NIEZALEŻNYCH SĘDZIÓW AI (BEZ SZTUCZNYCH PROMPTÓW)
**Data badania:** 2026-09-26  
**Zlecenie:** Automatyzacja obiegu faktur i dokumentów kosztowych (#144890)  
**Cel:** Sprawdzenie, jak modele AI (oceniające surowym promptem klienta biznesowego) oceniają oferty oraz jak interpretują dylemat: "Oferta z gotową architekturą vs Zadawanie pytań".

---

## 1. OCENA SĘDZIEGO 1: DeepSeek-Reasoner (Model Wnioskujący / R1)
*Model pracujący z łańcuchem myślenia (Chain of Thought), weryfikujący logikę biznesową i architektoniczną.*

Cześć. Po ludzku: **najlepsze oferty to B i A**. C wygląda jak skrócona wersja oferty A, podpisana tym samym nazwiskiem, więc traktuję ją jako co najmniej dziwną powtórkę. D jest uczciwy, ale nie wdrażał n8n produkcyjnie. E nie złożył oferty, tylko zadał pytanie. F jest zdecydowanie za tani i za mglisty jak na projekt, który dotyka księgowości.

I najważniejsze: dziś jest wrzesień 2026. **KSeF już działa**. Kto tego nie uwzględnia, ten albo jest do tyłu, albo chce Ci wcisnąć OCR do faktur, które i tak przychodzą jako dane XML. To podnosi koszty i ryzyko. Dlatego A, B, C i E zyskują, a D i F tracą.

## 1. Które oferty są najlepsze?

**Najlepsze: B i A.**

- **B (Antoni, AppWave)** – najbardziej kompletna oferta. Widzi KSeF, rozdziela faktury z KSeF od reszty, zna import XML do Optimy, mówi wprost: żadnego bezpośredniego pisania do bazy, testy na kopii, mapowanie towarów, 50 dokumentów testowych, jasne etapy. Cena za pełny zakres: 11 500 zł netto. To rozsądne.
- **A (Ksawier Potrykus)** – bardzo mocna merytorycznie oferta. Ma bezpośrednie doświadczenie z Comarch ERP, wie o KSeF, o Białej Liście, o tolerancjach VAT, o mapowaniu kartotek. Cena 9 800 zł netto za całość. Minus: **ten sam Ksawier podpisał też ofertę C za 6 500 zł i 13 dni** – to trzeba wyjaśnić, bo wygląda na bałagan.
- **C** – to prawdopodobnie ta sama osoba co A. Oferta krótsza, tańsza, ale bez rozwinięcia. Jeśli to naprawdę ta sama firma i honoruje 6 500 zł za ten sam zakres, to może być okazja. Ale na razie to czerwona flaga, nie oferta.
- **D** – uczciwy. Sam mówi, że n8n nie wdrażał produkcyjnie. Ma dobre podejście do Optimy, ale nie wspomina KSeF. Jako rezerwa – tak. Jako główny wykonawca – ryzyko.
- **E** – zadał dobre pytanie o KSeF, ale nie dał ceny ani terminu. To nie jest oferta.
- **F** – 3 600 zł netto za pełne wdrożenie, OCR, AI, import do Optimy i opiekę? Za takie pieniądze albo tego nie dowiezie, albo zrobi byle jak, albo później doliczy koszty. Do tego nie wie, jaki format przyjmie Twoja Optima. To jest proszenie się o problem z księgowością.

## 2. Kandydat E – profesjonalne czy strata czasu?

Pytanie o KSeF jest **mądre i potrzebne**. Gdyby zadał je przed złożeniem oferty w normalnym procesie sprzedaży, to byłby plus.

Ale w odpowiedzi na ogłoszenie, gdzie prosisz wprost o ofertę, **samo pytanie to za mało**. Profesjonalnie powinno to wyglądać tak:

> „Czy faktury są już w KSeF? Jeśli tak, proponuję zakres X za Y zł, a jeśli nie – zakres Z za W zł. Termin: ...”

On tego nie zrobił. Więc jako oferta – strata czasu. Jako potencjalny wykonawca – możesz odpisać: „Tak, KSeF działa. Przyślij ofertę z uwzględnieniem tego.” Jeśli wtedy przyśle konkret, można go brać pod uwagę. Na dziś nie ma czego porównywać.

## 3. Czy długie oferty A i B to strzelanie na oślep?

Nie. Wręcz przeciwnie.

W automatyzacji dokumentów **diabeł siedzi w szczegółach**. Ktoś, kto pisze dużo i wymienia konkrety:

- KSeF,
- brak bezpośredniego INSERT do bazy Optimy,
- import XML / Praca Rozproszona,
- mapowanie towarów, żeby nie zaśmiecić kartotek,
- testy na kopii bazy,
- kontrola sum i tolerancji VAT,
- deduplikacja,
- Biała Lista przy 15 000 zł,

ten najprawdopodobniej **wie, gdzie są miny**. To nie jest strzelanie. To jest pokazanie, że rozumie projekt.

Ale jest jedno „ale”: jeśli ktoś zakłada za dużo bez pytania o Twoją instalację Optimy, wersję, wolumen dokumentów i to, czy Optima jest stacjonarna czy w chmurze – to też jest ryzyko. Dlatego A i B na końcu pytają o rzeczy albo proponują rozmowę. To dobry znak. Złym znakiem byłby długi tekst bez pytań i bez propozycji testu na Twoich dokumentach.

## 4. Ranking od 1 do 6

**1. B – Antoni, AppWave**  
Najbardziej kompletna, uporządkowana oferta. KSeF, n8n, Optima, testy, etapy, jasna cena. Ma prototyp i proces. Jedyne zastrzeżenie: pełny zakres 11 500 zł netto, ale to i tak sensowne za projekt dotykający księgowości.

**2. A – Ksawier Potrykus**  
Bardzo mocny technicznie, z doświadczeniem w Comarch. Cena 9 800 zł netto za całość. Gdyby nie bałagan z ofertą C pod tym samym nazwiskiem, mógłby być nr 1. Wyjaśnij to z nim natychmiast.

**3. C – Ksawier Potrykus (prawdopodobnie ta sama osoba co A)**  
Ta sama wiedza, niższa cena, ale krótka i sprzeczna z ofertą A. Jeśli to pomyłka – traktuj razem z A. Jeśli nie – żądaj wyjaśnienia, która oferta jest wiążąca.

**4. D – Dominik, grodev.pl**  
Uczciwy. Mówi wprost, że n8n nie wdrażał produkcyjnie. Ma dobre instynkty przy Optimie, ale brak KSeF i brak doświadczenia w n8n to za duże ryzyko na głównego wykonawcę. Dobra rezerwa.

**5. E – bez ceny i terminu**  
Dobre pytanie, zero oferty. Nie da się go wybrać, bo nie wiadomo, co, za ile i kiedy. Odpisz mu i zobacz, czy złoży konkret.

**6. F – 3 600 zł netto**  
Najtańszy i najbardziej ryzykowny. Nie zna formatu importu do Twojej Optimy, nie wspomina KSeF, portfolio nie pasuje. Za 3 600 zł nie da się bezpiecznie wdrożyć automatyzacji, która dotyka faktur, WZ, zamówień i księgowości. To nie oszczędność, to potencjalny koszt.

## Co bym zrobił na Twoim miejscu

1. **Napisz do Ksawiera (A/C)**: „Czy A i C to ta sama oferta? Która jest wiążąca? Proszę o wyjaśnienie różnicy w cenie i terminie.”
2. **Umów 45 minut z B i A.** Nie z całą szóstką. Szkoda czasu.
3. **Daj im 3 najgorsze dokumenty**: jedną fakturę z maila, jeden skan ze skanera, jedno zdjęcie od kierowcy. Niech pokażą, co odczytają.
4. **Zapytaj wprost o KSeF, import do Optimy, testy na kopii bazy i mapowanie towarów.**
5. **Wybierz tego, kto nie boi się testu na kopii bazy i nie obiecuje cudów za 3 600 zł.**

Jeśli mam wskazać jednego: **B na pierwsze miejsce, A na drugie, z zastrzeżeniem wyjaśnienia C.** Różnica 1–2 tys. zł przy projekcie, który ma chronić Twoją księgowość, nie powinna być głównym kryterium.

---

## 2. OCENA SĘDZIEGO 2: DeepSeek-Chat (Standardowy Model Konwersacyjny)
*Model odpowiadający w roli doradcy biznesowego / pragmatycznego przedsiębiorcy.*

Po ludzku: **nie wybieraj najtaniej**. W tym projekcie najważniejsze są dwie rzeczy: **bezpieczne wprowadzanie danych do Optimy** i **niepłacenie za OCR tam, gdzie dane już są w KSeF**. Kto to rozumie, ten jest w grze. Kto tego nie widzi, będzie się uczył na Twojej księgowości.

**Uwaga na start:** Kandydat A i C podpisali się jako **Ksawier Potrykus** i podają to samo doświadczenie. To może być ta sama osoba. Jeśli tak, to nie masz 6 ofert, tylko 5. Nie traktuj C jako osobnego kandydata, dopóki nie wyjaśnisz, czemu raz wycenia 9 800 zł, a raz 6 500 zł.

---

## 1. Które oferty są najlepsze i dlaczego?

Najlepsi moim zdaniem to **A i B**. Reszta jest albo niepełna, albo ryzykowna.

**Kandydat A — bardzo mocny.**
- Rozumie KSeF i to, że część faktur nie powinna w ogóle przechodzić przez OCR.
- Mówi wprost: **żadnego INSERT do bazy Optimy**. To jest kluczowe. Kto proponuje pisanie bezpośrednio do bazy, tego bym odprawił.
- Zna pracę rozproszoną XML / Comarch ERP Web API.
- Wie, że największy problem to mapowanie towarów, żeby nie nabić bałaganu w kartotece.
- Testy na kopii bazy, etapowanie, 30 dni asysty, 12 miesięcy gwarancji na błędy.
- Cena 9 800 zł netto za całość wygląda rozsądnie jak za pełny zakres.

**Kandydat B — też bardzo dobry, ale drożej za pełny zakres.**
- Software house, nie pojedynczy człowiek. To plus przy większym wdrożeniu.
- Też rozumie KSeF, n8n, XML, brak INSERT, mapowanie towarów, testy na kopii.
- Ma etapy i konkretny podział prac.
- Minus: pełny zakres z importem WZ i zamówień to u niego **11 500 zł**, czyli drożej niż A. Za 8 900 zł masz tylko etap 1+2, a import WZ/zamówień jest dopiero w etapie 3.

**Kandydat C — dobre technicznie, ale za krótkie i ten sam podpis co A.**
Jeśli to naprawdę inna osoba, to jest to tańsza wersja A. Ale oferta jest zbyt skrótowa, brakuje etapów i szczegółów. Jeśli to ten sam Ksawier, to nie jest osobna oferta, tylko ten sam wykonawca z inną ceną.

**Kandydat D — uczciwy, ale nie na pierwszy ogień.**
- Ma dobre ostrzeżenie: sprawdź, czy Twoja licencja Optimy obejmuje pracę rozproszoną.
- Rozumie, że nie wolno pisać do bazy bezpośrednio.
- Ale sam przyznaje: **n8n nie wdrażał produkcyjnie**.
- Do tego w ogóle nie wspomina KSeF. To duże przeoczenie w 2026 roku.
- Nadaje się jako backup, ale nie jako pierwszy wybór.

**Kandydat E — to nie oferta, tylko pytanie.**
Merytorycznie bardzo ważne pytanie o KSeF. Ale nie ma ceny, terminu, zakresu. Nie da się go wybrać.

**Kandydat F — najtaniej, ale najbardziej ryzykownie.**
- 3 600 zł za pełne wdrożenie z Optimą to nierealnie mało.
- Nie wspomina KSeF.
- Sam pisze, że format importu do Optimy to „główna niewiadoma projektu”. Czyli wycenia, nie wiedząc, co ma zrobić.
- Doświadczenie z feedów Midocean/PF Concept to nie to samo co faktury, WZ, zamówienia i Optima.

---

## 2. Kandydat E — profesjonalizm czy strata czasu?

**To jest profesjonalne pytanie, ale nie jest to pełna oferta.** Facet zadał najważniejsze pytanie: czy faktury już spływają z KSeF. Jeśli tak, to połowa OCR-u jest bez sensu i można zaoszczędzić kupę kasy.

Ale na Useme oferta bez ceny i terminu to nie oferta. Możesz mu odpowiedzieć i poprosić o konkretną wycenę. Jeśli ją przyśle i będzie merytoryczna, można go rozważyć. Na dziś nie ma go jak wybrać, bo nie wiesz, ile chce i kiedy to zrobi.

---

## 3. Czy A i B dużo piszą, bo strzelają na oślep?

Nie. **Długość sama w sobie nic nie znaczy, ale w ich przypadku to nie jest lanie wody.**

A i B piszą dużo, bo ten projekt ma dużo pułapek:
- KSeF,
- różne typy dokumentów,
- skany ze skanera vs PDF z mailem,
- zdjęcia od kierowców,
- walidacja matematyczna,
- Biała Lista,
- mapowanie towarów,
- import do Optimy,
- testy na kopii bazy.

Oni te pułapki nazywają. To dobrze.

Strzelanie na oślep to raczej **F**, który podaje cenę, a potem mówi, że nie wie, jaki format importu przyjmie Optima. Albo ktoś, kto proponuje INSERT do bazy, bo nie zna Optimy. A i B raczej wiedzą, o czym mówią.

---

## 4. Ranking od 1 do 6

1. **Kandydat A** — najlepszy stosunek wiedzy o Optimie, KSeF, bezpieczeństwa i ceny. Ma doświadczenie z Comarch, etapy, testy na kopii, brak INSERT. Zastrzeżenie: wyjaśnij, czy C to ta sama osoba i czemu jest inna cena.

2. **Kandydat B** — bardzo mocny, software house, przejrzyste etapy, też bezpieczne podejście. Ale pełny zakres z importem WZ/zamówień drożej: 11 500 zł. Wybierz, jeśli wolisz firmę i proces, a różnica ceny nie boli.

3. **Kandydat C** — jeśli to osobna oferta, to dobry merytorycznie i tani. Ale zbyt skrótowy i podpisany tym samym nazwiskiem co A. Traktuj jako „tańsza wersja A do wyjaśnienia”, nie jako pewniaka.

4. **Kandydat D** — uczciwy, zna temat od strony AI/API, ale nie wdrażał n8n produkcyjnie i nie wspomina KSeF. Dobry jako backup albo do mniejszego, prostszego projektu.

5. **Kandydat E** — nie oferta, tylko pytanie. Merytorycznie cenne, ale bez ceny i terminu nie da się wybrać. Odpisz mu i poproś o pełną wycenę.

6. **Kandydat F** — najtaniej, ale najbardziej ryzykownie. Za 3 600 zł nie dowiezie pełnego wdrożenia z Optimą bez niespodzianek. Brak KSeF, nieznany format importu, doświadczenie nieadekwatne.

---

## Co bym zrobił na Twoim miejscu

Wybrałbym **A**, ewentualnie **B**, jeśli wolisz software house. Zanim podpiszesz, dopytaj:
- czy Optima jest stacjonarna czy w chmurze,
- czy licencja obejmuje pracę rozproszoną / API,
- czy KSeF jest już skonfigurowany,
- ile dokumentów miesięcznie przetwarzacie,
- czy import WZ i zamówień jest w cenie,
- czy testy na kopii bazy i 50 dokumentach są w cenie,
- co dokładnie obejmuje 30 dni asysty i 12 miesięcy gwarancji,
- czy kod, scenariusze n8n i instrukcje przechodzą na Ciebie.

Płać etapami i odbieraj po testach. Nie płać całości z góry. I nie wybieraj F tylko dlatego, że jest najtańszy — w tym projekcie taniość może Cię kosztować więcej niż różnica w cenie.

---
