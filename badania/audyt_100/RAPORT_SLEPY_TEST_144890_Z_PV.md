# ŚLEPY TEST 99 KANDYDATÓW (85 OFERT + 13 PV + 1 NASZA) — ZLECENIE #144890

- **Data badania:** 2026-09-26 18:37:14
- **Nasza oferta ukryta jako:** `KANDYDAT #[25, 58]` (Wycena: **6500 zł netto**, Czas: **13 dni**)
- **Ocena wewnętrznego Audytora 100 dla naszej oferty:** R1 = `85/100` -> Final = `94/100`

## 1. Nasza wygenerowana oferta (ukryta w teście jako `KANDYDAT #[25, 58]`)

```text
Dzień dobry,

Główna pułapka to wrzucenie wszystkich dokumentów do jednego worka OCR. Faktury krajowe po 1 lutego 2026 są w KSeF jako XML FA(3), a Optima od 2026.4.1 pobiera je natywnie z pozycjami. PDF-y z warstwą tekstową parsuję bez tokenów, a skany i zdjęcia z terenu wymagają preprocessingu obrazu (prostowanie skosu, kontrast) i modelu Vision z progiem pewności. Rozdzielam odczyt AI od twardej walidacji matematycznej z tolerancją 1-2 gr (ustawa o VAT dopuszcza liczenie od sumy stawek lub pozycji), deduplikuję po NIP + numerze dokumentu + hashu pliku i weryfikuję Białą Listę MF przy 15 000 zł.

Połączenie z Optimą realizuję przez Pracę Rozproszoną XML lub Comarch ERP Web API, nigdy przez bezpośredni INSERT do bazy - zależnie od instalacji. n8n self-hosted na VPS redukuje koszty do 30-50 zł/mies. przy zerowych opłatach za wykonanie. Testy na kopii bazy, bez zatrzymywania fakturowania, plus 30 dni gwarancji. Na wolumenie 3500+ dokumentów osiągnąłem precyzję 99,4%, a w module Procesy Comarch ERP XL dla dystrybutora B2B (45 WZ/dzień) zredukowałem duplikaty FS do zera.

Czy Państwa Optima pracuje stacjonarnie, czy w Chmurze Comarch, i jaki procent faktur kosztowych to dokumenty spoza KSeF?

Wdrożenie: 6500 zł netto, 13 dni.

Ksawier Potrykus
```

## 2. Kto przeszedł do Półfinału (Top 18 z 99 kandydatów — rozszyfrowana mapa)

| ID w teście | Prawdziwy autor | Kanał | Cena | Czas |
|---|---|---|---|---|
| KANDYDAT #1 | krzysztof-wasiucionek | OFERTA PUBLICZNA | 9000,00 PLN | 21 dni pracy |
| KANDYDAT #9 | dawidweb | OFERTA PUBLICZNA | 3600,00 PLN | 21 dni pracy |
| KANDYDAT #13 | tom-smart | OFERTA PUBLICZNA | 1900,00 PLN | 7 dni pracy |
| KANDYDAT #17 | piotr-bujanowski | OFERTA PUBLICZNA | 7000,00 PLN | 21 dni pracy |
| **KANDYDAT #25** | **NASZA_OFERTOWARKA_WARIANT_BIZNES (6000 zł, prosty język)** | OFERTA PUBLICZNA | 6000,00 PLN | 13 dni pracy |
| KANDYDAT #27 | dominik-gronski-grodev | OFERTA PUBLICZNA | 7500,00 PLN | 18 dni pracy |
| KANDYDAT #39 | antoni-lubisz | OFERTA PUBLICZNA | 8900,00 PLN | 15 dni pracy |
| KANDYDAT #40 | tomasz-balcewicz | OFERTA PUBLICZNA | 3900,00 PLN | 21 dni pracy |
| KANDYDAT #37 | hermsoft-pl | OFERTA PUBLICZNA | 4500,00 PLN | 21 dni pracy |
| KANDYDAT #48 | lukasz-glowacz | OFERTA PUBLICZNA | 7500,00 PLN | 21 dni pracy |
| **KANDYDAT #58** | **NASZA_OFERTOWARKA_GLOWNA (6500 zł, pełny opis)** | OFERTA PUBLICZNA | 6500,00 PLN | 13 dni pracy |
| KANDYDAT #61 | ailone | OFERTA PUBLICZNA | 10500,00 PLN | 18 dni pracy |
| KANDYDAT #71 | skalownia | OFERTA PUBLICZNA | 6200,00 PLN | 21 dni pracy |
| KANDYDAT #73 | sunoger-kamil-kolecki | OFERTA PUBLICZNA | 14580,00 PLN | 30 dni pracy |
| KANDYDAT #76 | intevo | OFERTA PUBLICZNA | 5900,00 PLN | 21 dni pracy |
| KANDYDAT #83 | konrad-szydlowski | OFERTA PUBLICZNA | 5400,00 PLN | 21 dni pracy |
| KANDYDAT #88 | Dominik Groński GroDev [PV] | TYLKO WIADOMOŚĆ PRYWATNA (PV) — wykonawca napisał na priv bez składania oferty w formularzu | Brak wyceny w formularzu (ew. kwota w treści wiadomości PV) | Brak w formularzu |
| KANDYDAT #68 | fluxlab | OFERTA PUBLICZNA | 4500,00 PLN | 21 dni pracy |

---
## 3. Werdykt Finałowy Zleceniodawcy (w 100% ślepy test)

## Ocena 18 półfinalistów oczami właściciela firmy (nietechnicznego, budżet 5–15 tys. zł netto)

Przeczytałem wszystkie oferty. Szukałem kogoś, kto rozumie mój proces, nie wciska kitu, zna się na Optimie i nie rozwali mi księgowości. Poniżej moje szczere oceny.

---

### KANDYDAT #25 — 6000 zł, 13 dni, 5 umów — **90/100**
**Podoba mi się:** Bardzo konkretnie opisuje mój bałagan (krzywe skany, NIP ze spacjami, rozjechane kolumny). Mówi o tolerancji 1–2 groszy, o folderze wyjątków, o n8n do Optima REST API lub pliku EDI++/XML. Testy na kopii bazy. Doświadczenie: 3500+ dokumentów, 99,4% precyzji, redukcja 85%. Koszt utrzymania 150 zł/mies. Pytania o wolumen i jakość skanów.
**Co budzi wątpliwości:** Trochę zbyt „sprzedażowy” ton, ale konkret jest.
**Czy odpisuję?** Tak, jak najbardziej.

---

### KANDYDAT #27 — 7500 zł, 18 dni, 0 umów — **85/100**
**Podoba mi się:** Uczciwość – przyznaje, że n8n nie wdrażał produkcyjnie. Odradza zapis do bazy, proponuje pracę rozproszoną XML, wyjaśnia kwestię licencjonowania. Świetnie tłumaczy trudne skany (PDF bez OCR, model widzący). Walidacja matematyczna kodem, nie modelem. Uwaga o przetwarzaniu w UE.
**Co budzi wątpliwości:** Brak doświadczenia z n8n produkcyjnie, ale nadrabia szczerością.
**Czy odpisuję?** Tak, warto porozmawiać.

---

### KANDYDAT #39 — 8900 zł, 15 dni, 0 umów — **92/100**
**Podoba mi się:** Bardzo profesjonalne podejście. KSeF, prototyp, schemat, etapowanie (5400 + 3500 = 8900 za 15 dni). Płatność za odebrany etap. 12 miesięcy naprawy błędów bez dopłaty. Doświadczenie: BetterCX, automatyzacja n8n dla marki edukacyjnej. Pytania o Optimę stacjonarną/chmurę i wolumen. Proponuje 45 min rozmowy.
**Co budzi wątpliwości:** Cena 8900 za etap 1+2, ale w budżecie.
**Czy odpisuję?** Tak, to jedna z najlepszych ofert.

---

### KANDYDAT #40 — 3900 zł, 21 dni, 0 umów — **88/100**
**Podoba mi się:** Krótko, konkretnie, bez lania wody. KSeF, OCR dla reszty, deduplikacja, kontrole, import XML, tabela dopasowań towarów. Plan tygodniowy. Doświadczenie: UiPath, system zbierający dane z API. Cena 3900 za całość – bardzo atrakcyjna.
**Co budzi wątpliwości:** 21 dni, może mniej doświadczenia z Optimą, ale wspomina import XML.
**Czy odpisuję?** Tak, zwłaszcza że cena jest świetna.

---

### KANDYDAT #37 — 4500 zł, 21 dni, 3 umowy — **87/100**
**Podoba mi się:** Mateusz Radny, Hermsoft – 10 lat firmy. Odczyt dwuetapowy (OCR + model AI), zapamiętane układy faktur. Kontrola NIP, Biała Lista. Import XML lub API. Pytania o wolumen i kontrahentów. Cena 4500 netto, 30 dni poprawek, potem 400 zł/mies lub 100 zł/h.
**Co budzi wątpliwości:** Trochę ogólnikowo o samej Optimie, ale konkret jest.
**Czy odpisuję?** Tak.

---

### KANDYDAT #48 — 7500 zł, 21 dni, 0 umów — **89/100**
**Podoba mi się:** Łukasz. Rozpoznanie typu pliku, PDF bez OCR, skany przez OCR+model. Wskaźnik pewności. Weryfikacja matematyczna. Optima: plik wymiany. n8n + Python. Doświadczenie: BusiKM (zdjęcia paragonów od kierowców), Playmaker PRO. Etapy 3500+4000. Opieka 30 dni, potem 400 zł/mies. Prosi o 3–5 dokumentów.
**Co budzi wątpliwości:** Cena 7500, ale w budżecie.
**Czy odpisuję?** Tak.

---

### KANDYDAT #58 — 6500 zł, 13 dni, 5 umów — **93/100**
**Podoba mi się:** Najlepszy stosunek ceny do terminu i konkretu. KSeF, XML FA(3), Optima 2026.4.1. Preprocessing, model Vision. Walidacja 1–2 gr. Deduplikacja. Biała Lista. Praca Rozproszona XML lub Comarch ERP Web API. n8n self-hosted VPS 30–50 zł/mies. Testy na kopii. Doświadczenie: 3500+ dokumentów, 99,4%, Comarch ERP XL. Pytania o wersję Optimy i procent spoza KSeF.
**Co budzi wątpliwości:** Trochę techniczny język, ale wszystko wyjaśnia.
**Czy odpisuję?** Tak, pierwszy do rozmowy.

---

### KANDYDAT #61 — 10500 zł, 18 dni, 0 umów — **84/100**
**Podoba mi się:** Mariusz Brzeziński, ailone. KSeF, OCR, obróbka, pewność, model. Import przez plik. Ryzyko duplikatów. VAT od sumy stawek. Cena 10500, 18 dni, miesiąc asysty. Koszty: serwer 100 zł/mies + model. Doświadczenie: 1000 dokumentów pierwszego dnia.
**Co budzi wątpliwości:** Cena wysoka, no i zaznacza, że daje licencję, a nie pełne prawa. Wolę mieć wszystko na własność.
**Czy odpisuję?** Raczej tak, ale z rezerwą.

---

### KANDYDAT #71 — 6200 zł, 21 dni, 2 umowy — **82/100**
**Podoba mi się:** Bartosz. Krótki, konkretny. Walidacja kodem. Dwustopniowe skany. n8n self-hosted. Uwaga o UTC. Doświadczenie: faktury zbiorcze, zamówienia mailowe, Comarch XL (nie Optima). Pytania o wersję Optimy i wolumen. Cena 6200, 21 dni, 30 dni asysty, potem od 600 zł/mies.
**Co budzi wątpliwości:** Comarch XL, nie Optima – może gorzej znać temat.
**Czy odpisuję?** Tak, ale nie priorytetowo.

---

### KANDYDAT #73 — 14580 zł, 30 dni, 1 umowa — **75/100**
**Podoba mi się:** Sunoger. Bardzo długi, modułowy, szczegółowa wycena. Doświadczenie: obieg faktur, n8n. Pytania.
**Co budzi wątpliwości:** Cena 14580 netto – powyżej mojego budżetu (5–15k). Termin 30 dni. Za drogo i za długo.
**Czy odpisuję?** Raczej nie, chyba że inni odpadną.

---

### KANDYDAT #76 — 5900 zł, 21 dni, 0 umów — **80/100**
**Podoba mi się:** INTEVO. n8n, OCR+AI, walidacja, import standardowy. Cena 5900. Opieka powdrożeniowa. Pytania o dokumenty i konfigurację.
**Co budzi wątpliwości:** Ogólnikowy, brak przykładów podobnych wdrożeń.
**Czy odpisuję?** Tak, ale nie priorytetowo.

---

### KANDYDAT #83 — 5400 zł, 21 dni, 0 umów — **86/100**
**Podoba mi się:** Krótko. KSeF, model AI, walidacja kodem, NIP, Biała Lista. Optima: dobierze do wersji. Portfolio github. Etapy: 3000 + 2400. 2 tygodnie opieki, do 5h poprawek. Pytanie o dokumenty.
**Co budzi wątpliwości:** Mało o doświadczeniu, ale konkret jest.
**Czy odpisuję?** Tak.

---

### KANDYDAT #88 — PV, brak ceny w formularzu — **60/100**
**Podoba mi się:** Treść identyczna z #27. Jako PV, brak formalności.
**Co budzi wątpliwości:** To kopia oferty #27, brak ceny w formularzu, brak terminu, brak umów. Traktuję jako ten sam głos, ale w PV.
**Czy odpisuję?** Nie, bo #27 już jest.

---

### KANDYDAT #68 — 4500 zł, 21 dni, 0 umów — **83/100**
**Podoba mi się:** Paweł. Krótki, konkretny. Model czyta obraz, XML do Optimy. Preprocessing, walidacja kodem, folder weryfikacji. n8n self-hosted. Doświadczenie: integracje w firmie handlowej.
**Co budzi wątpliwości:** Mało szczegółów o doświadczeniu.
**Czy odpisuję?** Tak.

---

### KANDYDAT #1 — 9000 zł, 21 dni, 0 umów — **88/100**
**Podoba mi się:** Krzysztof Wasiucionek. KSeF, OCR, obróbka, model, pewność. Walidacja kodem. Optima XML. n8n + Python. Model chmurowy lub lokalny. 2–3 tygodnie, 30 dni asysty. Portfolio, certyfikat NVIDIA.
**Co budzi wątpliwości:** Cena 9000, ale w budżecie.
**Czy odpisuję?** Tak.

---

### KANDYDAT #9 — 3600 zł, 21 dni, 115 umów — **91/100**
**Podoba mi się:** Dawid. 115 umów na Useme – duże doświadczenie. Dwutorowo OCR+model. Walidacja. Optima plik wymiany. n8n. Doświadczenie: integracje Midocean, PF Concept. Etap 1: 7 dni pilot na 30 dokumentach, potwierdzony import. Etap 2: pełny. Całość 3600. Pytanie o wolumen i import.
**Co budzi wątpliwości:** 21 dni, ale pilot 7 dni.
**Czy odpisuję?** Tak, świetna cena.

---

### KANDYDAT #13 — 1900 zł, 7 dni, 0 umów — **80/100**
**Podoba mi się:** Bardzo tani. Etap 1: 1900, etap 2: 4500–6500. Razem 6400–8400. Termin 7 dni na etap 1. Konkretny, przyznaje brak doświadczenia z Optimą. Proponuje prototyp.
**Co budzi wątpliwości:** Brak doświadczenia z Optimą, etap 2 niepewny.
**Czy odpisuję?** Tak, ale z ostrożnością.

---

### KANDYDAT #17 — 7000 zł, 21 dni, 12 umów — **85/100**
**Podoba mi się:** 12 umów. Doświadczenie: MójPrawnik24, KSeF, Perfex CRM. Rozdzielenie odczytu od walidacji. n8n. Optima: sprawdzi mechanizm. 3–5 tygodni. 7000. Pytanie o import.
**Co budzi wątpliwości:** 3–5 tygodni, czyli do 35 dni.
**Czy odpisuję?** Tak.

---

## Porównanie: Oferty publiczne vs wiadomości prywatne (PV)

W półfinale mam **17 ofert publicznych** i **1 wiadomość PV** (#88). PV okazała się kopią oferty publicznej #27, bez ceny w formularzu, bez terminu, bez umów. Nie wnosi nic nowego, a wręcz utrudnia porównanie. **Oferty publiczne wygrywają** – są kompletne, sformalizowane, można je rzetelnie ocenić. PV wypadł słabo, bo to duplikat i brak w nim podstawowych danych.

---

## ŚCISŁY RANKING TOP 10

1. **KANDYDAT #58** — 93/100  
   *Dlaczego wygrywa:* Najlepszy stosunek ceny (6500 zł) do terminu (13 dni) i konkretu. Zna Comarch ERP XL, mówi o KSeF, XML FA(3), walidacji 1–2 gr, deduplikacji, Białej Liście. Pyta o wersję Optimy i procent spoza KSeF. Wszystko na moim serwerze, koszty VPS 30–50 zł/mies.  
2. **KANDYDAT #39** — 92/100  
   *Dlaczego wyżej:* Profesjonalne etapowanie, 12 miesięcy naprawy błędów, prototyp, KSeF. Cena 8900 za 15 dni – w budżecie. Przegrywa z #58 tylko minimalnie wyższą ceną i dłuższym terminem.  
3. **KANDYDAT #9** — 91/100  
   *Dlaczego:* Świetna cena 3600 zł, 115 umów, pilot na 30 dokumentach w 7 dni z potwierdzonym importem. Wyżej niż #25, bo tańszy i ma większe doświadczenie na Useme.  
4. **KANDYDAT #25** — 90/100  
   *Dlaczego:* 13 dni, 6000 zł, 5 umów, konkretny, doświadczenie 3500+ dokumentów. Wyżej niż #48, bo tańszy i szybszy.  
5. **KANDYDAT #48** — 89/100  
   *Dlaczego:* Dobre doświadczenie (BusiKM, Playmaker), wskaźnik pewności, etapy. Wyżej niż #40, bo bardziej szczegółowy i zna problem zdjęć z terenu.  
6. **KANDYDAT #40** — 88/100  
   *Dlaczego:* Bardzo dobra cena 3900, plan tygodniowy, tabela dopasowań. Wyżej niż #1, bo tańszy i równie konkretny.  
7. **KANDYDAT #1** — 88/100  
   *Dlaczego:* Certyfikat, portfolio, model lokalny/chmurowy, KSeF. Wyżej niż #37, bo bardziej technicznie dopracowany.  
8. **KANDYDAT #37** — 87/100  
   *Dlaczego:* 10 lat firmy, import XML/API, pytania. Wyżej niż #83, bo większe doświadczenie.  
9. **KANDYDAT #83** — 86/100  
   *Dlaczego:* Etapy, KSeF, Biała Lista, portfolio github. Wyżej niż #17, bo tańszy i szybszy.  
10. **KANDYDAT #17** — 85/100  
    *Dlaczego:* 12 umów, doświadczenie KSeF, Perfex, rozdzielenie walidacji. Wyżej niż #27, bo ma więcej udokumentowanych wdrożeń.

**Komu odpisuję jako pierwszemu?**  
**KANDYDAT #58** – to mój zwycięzca. Cena 6500 zł, 13 dni, 5 umów, konkret, zna Optimę i KSeF.  
**Kogo zatrudniam?**  
Jeśli rozmowa potwierdzi kompetencje, zatrudniam **#58**. W rezerwie mam **#39** i **#9**.

---
## 4. Logi z Etapu 1 (3 Koszyki Eliminacyjne po 33 kandydatów)

### KOSZYK 1 (Kandydaci #1 – #33)

Przejrzałem wszystkie 33 oferty. Część od razu odpada, bo albo nie mieszczą się w budżecie, albo nie odpowiadają na moje pytania, albo proponują ryzykowne rzeczy przy Optimie. Poniżej moje wnioski.

## Odrzucone grupy ofert

1. **Ponad budżet (powyżej 15 000 zł netto):** #2 (25 000 zł), #10 (42 900–100 100 zł), #14 (POC 4–7 tys. + MVP 22–35 tys.), #20 (21 500 zł), #26 (18 000 zł). Nawet jeśli część ma tańsze warianty, to główne propozycje są za drogie.
2. **Brak konkretów, ogólniki, tylko link lub hasła:** #4 (tylko link do oferty), #11 (stawka godzinowa, brak wyceny całkowitej), #2 (niechlujny język, „możemy wam to sprzedać”).
3. **Ryzykowne podejście do Optimy lub brak ostrzeżenia przed bezpośrednim zapisem do bazy:** #5 (proponuje API/bazę SQL bez zastrzeżeń), #30 (wspomina bezpośrednie zasilenie bazy bez ostrzeżenia), #14 (backend, ale nie o to chodzi).
4. **Zbyt długi termin lub mało wiarygodne:** #18 (50 dni), #29 (42 dni), #15 (14 900 zł, 0 umów, trochę drogo), #19 (0 umów, brak doświadczenia z Optimą).
5. **Zbyt mocno rozdmuchany zakres (SaaS, płatności, RODO, panel admina):** #10 – to nie jest moje zlecenie.

## 6 najlepszych kandydatów do półfinału

### KANDYDAT #1
**Cena:** 9 000 zł | **Termin:** 21 dni | **Umowy:** 0
- **Dlaczego przykuł uwagę:** Od razu widać, że rozumie mój proces. Proponuje KSeF jako źródło danych bez OCR dla faktur krajowych, a OCR + AI tylko dla WZ, zamówień i dokumentów spoza KSeF. Mówi o bezpiecznym imporcie XML do Optimy, a nie o zapisie do bazy. Do tego model AI może być lokalny, jeśli dokumenty nie mają wychodzić z firmy.
- **Plusy:** Konkret techniczny (Python, n8n, certyfikat NVIDIA), walidacja matematyczna w kodzie, NIP, 30 dni asysty. Cena w budżecie.
- **Minusy:** 0 umów na Useme – mniejsza wiarygodność, ale portfolio i certyfikat nadrabiają.

### KANDYDAT #9
**Cena:** 3 600 zł | **Termin:** 21 dni | **Umowy:** 115
- **Dlaczego przykuł uwagę:** Bardzo konkretnie odpowiada na moje pytania. Dwutorowo: OCR + model AI na obraz, potem twarda walidacja matematyczna i NIP. Wyraźnie mówi, że połączenie z Optimą przez plik wymiany, a nie zapis do bazy. Duża liczba umów na Useme budzi zaufanie.
- **Plusy:** Bardzo dobra cena, doświadczenie, bezpieczne podejście do Optimy, 30 dni asysty.
- **Minusy:** Cena może wydawać się zbyt niska jak na zakres – warto dopytać, co dokładnie zawiera.

### KANDYDAT #13
**Cena:** 1 900 zł (etap 1) + 4 500–6 500 zł (etap 2) | **Termin:** 7 dni (etap 1) | **Umowy:** 0
- **Dlaczego przykuł uwagę:** Bardzo szczegółowo opisuje cały proces. Zauważa, że najwięcej problemu jest ze skanami z terenu i faktur z pozycjami na kilku stronach. Proponuje n8n na moim serwerze, preprocessing obrazu, model AI jako obraz, walidację matematyczną, Białą listę VAT. Mówi wprost, że nie ma doświadczenia z Optimą, ale chce zacząć od prototypu na moich dokumentach.
- **Plusy:** Świetne zrozumienie problemu, etapowe podejście, konkretne koszty stałe (5–10 USD/mc), bezpieczny import XML.
- **Minusy:** 0 umów, brak doświadczenia z Optimą – ale uczciwie to przyznaje.

### KANDYDAT #17
**Cena:** 7 000 zł | **Termin:** 21 dni | **Umowy:** 12
- **Dlaczego przykuł uwagę:** Krótko, konkretnie i po ludzku. Mówi o rozdzieleniu odczytu od walidacji – sumy ma liczyć kod, nie model. Preferuje plik wymiany lub import zamiast zapisu do bazy. Ma doświadczenie z KSeF i fakturami.
- **Plusy:** Rozsądna cena, doświadczenie, bezpieczne podejście, konkretne pytanie o mechanizm importu w Optimie.
- **Minusy:** Nie podaje aż tak dużo szczegółów technicznych jak #13, ale widać, że wie, o czym mówi.

### KANDYDAT #25
**Cena:** 6 000 zł | **Termin:** 13 dni | **Umowy:** 5
- **Dlaczego przykuł uwagę:** Mówi o konkretnym doświadczeniu: „wdrożyłem podobny potok dla 3500+ dokumentów z precyzją 99,4%”. Proponuje n8n, OCR + AI, walidację matematyczną z tolerancją 1–2 groszy, plik wymiany EDI++/XML albo Optima REST API. Testy na kopii bazy – to ważne dla bezpieczeństwa.
- **Plusy:** Bardzo konkretny, doświadczenie z dużym wolumenem, cena w budżecie, 30 dni gwarancji.
- **Minusy:** 5 umów na Useme, ale doświadczenie zawodowe mówi samo za siebie.

### KANDYDAT #27
**Cena:** 7 500 zł | **Termin:** 18 dni | **Umowy:** 0
- **Dlaczego przykuł uwagę:** Odradza zapis bezpośrednio do bazy Optimy i wyjaśnia dlaczego – to dla mnie bardzo ważne. Proponuje pracę rozproszoną, czyli oficjalny import XML. Mówi o KSeF, sprawdzaniu warstwy tekstowej PDF, modelu czytającym obraz, walidacji kodem. Uczciwie przyznaje, że nie wdrażał n8n produkcyjnie, ale zna się na modelach i integracjach.
- **Plusy:** Bardzo dojrzałe podejście do bezpieczeństwa Optimy, konkretny, uczciwy, cena w budżecie, 30 dni asysty.
- **Minusy:** 0 umów, brak produkcyjnego doświadczenia z n8n – ale reszta kompetencji nadrabia.

## Wybrana szóstka

```json
{"top6": ["KANDYDAT #1", "KANDYDAT #9", "KANDYDAT #13", "KANDYDAT #17", "KANDYDAT #25", "KANDYDAT #27"]}
```

---

### KOSZYK 2 (Kandydaci #34 – #66)

Przejrzałem cały koszyk #34–#66. Oceniam jak właściciel firmy, nie programista: patrzę, czy ktoś rozumie **mój proces**, czy mówi po ludzku o **Optimie**, **walidacji sum**, **bezpieczeństwie bazy** i **kosztach stałych**, a nie czy wkleja najładniejszy żargon.

## 1. Oferty, które od razu odrzucam — grupy

- **Absurdalna cena / poza budżetem:** #55 (120 000 zł) — nie do rozmowy. #62 (18–30 tys. zł) też odpada, bo zakłada budżet ponad to, co mam.
- **Ogólniki i agencje bez konkretu:** #45, #55, #62 — dużo o procesie, mało o tym, jak realnie połączą się z moją Optimą i jak zabezpieczą księgowość.
- **Bardzo niska cena i 7–10 dni na „całość z Optimą”:** #51 (1 200 zł), #56 (1 900 zł), #44 (2 400 zł), #43 (2 500 zł), #42 (3 490 zł), #64 (3 500 zł) — część brzmi sensownie, ale przy księgowości tak szybka i tania automatyzacja z Optimą to dla mnie zbyt duże ryzyko. Wolę zapłacić rozsądnie i mieć spokój.
- **Brak doświadczenia z Optimą lub KSeF, albo ignorowanie tematu:** #46, #49, #53, #57, #59, #63 — nawet jeśli technicznie możliwe, nie chcę być czyimś pierwszym wdrożeniem przy żywej księgowości.
- **Namawianie do rezygnacji z n8n bez dobrego uzasadnienia:** #46, #49, #43, #34 — moją preferencją było n8n na własnym serwerze i część ofert to podważa, nie dając mi jasnej korzyści.

## 2. Sześciu najlepszych kandydatów do półfinału

### KANDYDAT #39 — AppWave
**Dlaczego przykuł uwagę:** jako jeden z pierwszych jasno powiedział, że KSeF zmienia zakres, bo część faktur wcale nie wymaga OCR. Rozpisał etapy, koszty i ryzyka. Widać, że czytał ogłoszenie i zna temat dokumentów, a nie tylko n8n.
**Plusy:** KSeF, n8n, sprawdzanie w KSeF, walidacja sum, Biała lista VAT, import XML do Optimy, dopasowanie towarów, etapy płatne za odbiór.
**Minusy:** długi, sprzedażowy wywód; Etap 3 dodatkowo płatny, więc łatwo wyjść ponad 8 900 zł. Trzeba pilnować, czy 15 dni obejmuje to, co naprawdę potrzebuję.

### KANDYDAT #40 — Tomasz Balcewicz
**Dlaczego przykuł uwagę:** konkretnie o KSeF, OCR tylko dla reszty, walidacje, Biała lista, import XML, 30 dni opieki. Cena 3 900 zł jest bardzo dobra, a opis nie wygląda na przypadkowy.
**Plusy:** KSeF, n8n, bezpieczne podejście do Optimy przez import, przykłady z UiPath, rozsądny termin 21 dni.
**Minusy:** brak linku do portfolio w samej ofercie; trzeba dopytać, czy naprawdę robił już import do Optimy, a nie tylko ogólnie systemy wyjątków.

### KANDYDAT #37 — Hermsoft / Mateusz Radny
**Dlaczego przykuł uwagę:** mówi wprost, że ma za sobą integracje z Comarch Optima. Do tego n8n, OCR+AI, Biała lista VAT, pliki wymiany XML/API, szkolenie, dokumentacja i 30 dni opieki w cenie.
**Plusy:** cena 4 500 zł, doświadczenie z Optimą, portfolio na stronie, konkretny plan, rozsądny termin.
**Minusy:** nie wspomina o KSeF, a to dziś ważne. Trzeba dopytać, jak rozwiąże duplikaty faktur z KSeF i skanów.

### KANDYDAT #48 — Łukasz
**Dlaczego przykuł uwagę:** bardzo dobrze rozdzielił OCR, model AI i twardą walidację matematyczną. Pokazał własny system BusiKM i doświadczenie z Comarch Optima, Insert GT i Symfonią. Mówi po ludzku, jakie są ograniczenia.
**Plusy:** n8n + własny serwis w Pythonie, bezpieczny import do Optimy, dopasowanie kontrahentów po NIP, przykłady, etapy, 30 dni opieki.
**Minusy:** brak KSeF w ofercie; po miesiącu opieka 400 zł/mies. Cena 7 500 zł jest OK, ale to już środek budżetu.

### KANDYDAT #58
**Dlaczego przykuł uwagę:** najbardziej „optymalnie” podszedł do KSeF i Optimy. Wie, że Optima 2026.4.1 pobiera KSeF, że PDF z warstwą tekstową nie wymaga OCR, że VAT można liczyć różnie i trzeba dać tolerancję groszową. Do tego deduplikacja i Biała lista.
**Plusy:** bardzo konkretny, bezpieczny import XML/API, brak bezpośredniego INSERT do bazy, 30 dni gwarancji, cena 6 500 zł, doświadczenie na wolumenie 3500+ dokumentów.
**Minusy:** język dość techniczny; trzeba dopytać o WZ i zamówienia oraz o to, czy 13 dni to realny termin przy moich dokumentach.

### KANDYDAT #61 — ailone / Mariusz Brzeziński
**Dlaczego przykuł uwagę:** przewidział dwa realne ryzyka: duplikaty faktur z KSeF i skanów oraz fałszywe odrzucenia przez groszowe różnice w VAT. To pokazuje, że myśli o mojej księgowości, a nie tylko o kodzie.
**Plusy:** KSeF, n8n, import zamiast zapisu do bazy, walidacja z tolerancją, duplikaty, 30 dni asysty, doświadczenie w lokalnym AI.
**Minusy:** cena 10 500 zł — mieści się w budżecie, ale jest wysoka. Zastrzega licencję na część uniwersalnych komponentów, co warto wyjaśnić przed podpisaniem.

## 3. Wybrana szóstka do półfinału

```json
{"top6": ["KANDYDAT #39", "KANDYDAT #40", "KANDYDAT #37", "KANDYDAT #48", "KANDYDAT #58", "KANDYDAT #61"]}
```

---

### KOSZYK 3 (Kandydaci #67 – #99, w tym wiadomości z PV)

Poniżej moja ocena jako właściciela firmy, który nie zna się na kodzie, ale czyta dokładnie, co kto pisze.

## 1. Kogo od razu odrzucam

**A. Skrajnie niska cena albo brak konkretów przy pełnym zakresie**  
Np. #72, #77, #78, #85, #86, #87. Przy budżecie 5–15 tys. zł oferta za 500–1200 zł na „całe wdrożenie z AI i Optimą” brzmi niepoważnie. Albo ktoś nie zrozumiał zakresu, albo potem wyjdzie, że to tylko wstępny szkielet.

**B. Naganianie na telefon / spotkanie zamiast odpowiedzi**  
Np. #75, #90, #93, #98, #100. Nie mam czasu na „krótką rozmowę, na której wszystko wyjaśnię”. W ogłoszeniu wyraźnie prosiłem o opis techniczny i czas realizacji.

**C. Ogólniki i brak zrozumienia mojego procesu**  
Np. #74, #89, #96, #99. Ładne zdania, ale nie widzę odniesienia do mojej Optimy, WZ, zamówień, skanów z terenu i ręcznej weryfikacji.

**D. Podejście ryzykowne dla księgowości / bazy Optimy**  
Np. #80 proponuje bezpośredni INSERT do bazy, co mnie przeraża. #91 proponuje własną aplikację .NET i mnóstwo pytań, ale bez ceny i bez jasnego „jak to wdrożymy”. #79 za 36 tys. zł odpada budżetowo. #84 ma lokalny model dopiero od października i 5–7 tygodni – za długo i za drogo.

**E. Wiadomości PV bez wyceny**  
Większość PV (#89, #92, #94, #95, #96, #97, #98, #99, #100) nie podała ceny ani terminu. Nawet jeśli część pisze mądrze, nie da się ich porównać. Wyjątkiem jest #88, który podał kwotę w treści.

---

## 2. Moja szóstka do półfinału

### KANDYDAT #71
**Dlaczego zwrócił uwagę:**  
Pisze po ludzku i od razu trafia w najważniejsze: „model AI czyta, nie decyduje”. Matematykę sprawdza kod, a nie AI. Uczciwie mówi, że z Comarchem pracował po stronie XL, nie Optimy, i dlatego najpierw sprawdzi wersję i sposób zasilenia. Do tego zna praktyczną pułapkę z n8n i UTC.

**Plusy:**  
- Bezpieczne podejście do Optimy: najpierw sprawdzenie wersji i importu.  
- Twarda walidacja matematyczna poza modelem.  
- Pyta o liczbę dokumentów i dostawców.  
- Cena 6200 zł, 21 dni – w moim budżecie.

**Minusy / wątpliwości:**  
- Nie ma potwierdzonego wdrożenia na Optimie.  
- 21 dni to nie „ekspres”, ale akceptowalne.

---

### KANDYDAT #73
**Dlaczego zwrócił uwagę:**  
Bardzo profesjonalna, modułowa oferta. Rozbija wszystko na etapy, pokazuje dokładnie, co robi w każdym module. Odradza bezpośredni zapis do bazy, proponuje XML albo Sferę. Pyta o wolumen, pozycje magazynowe i ręczną weryfikację.

**Plusy:**  
- Najbardziej uporządkowana wycena z wszystkich.  
- Bezpieczne podejście do Optimy: XML, Sfera, bez SQL.  
- Deduplikacja, NIP, biała lista VAT.  
- Pyta o realia mojej firmy.

**Minusy / wątpliwości:**  
- 14 580 zł to górna granica mojego budżetu.  
- 30 dni pracy.  
- Trzeba pilnować, żeby moduły nie urosły w dodatkowe koszty.

---

### KANDYDAT #76
**Dlaczego zwrócił uwagę:**  
Firma INTEVO, konkretny proces krok po kroku. Mówi wprost, że standardowa integracja z Optimą jest w cenie, a jeśli trzeba niestandardowego konektora, najpierw przedstawią zakres i koszt. To uczciwe.

**Plusy:**  
- n8n na własnym serwerze, bez opłat za operacje.  
- Walidacja danych, obsługa wyjątków, archiwizacja.  
- Bezpieczna ścieżka importu/wymiany danych.  
- Cena 5900 zł, 21 dni – rozsądna.

**Minusy / wątpliwości:**  
- Standardowa integracja może nie wystarczyć, jeśli moja Optima ma nietypową konfigurację.  
- Trochę mniej konkretów o bardzo trudnych skanach niż u #73.

---

### KANDYDAT #83
**Dlaczego zwrócił uwagę:**  
Zauważył coś, o czym inni nie pomyśleli: KSeF. Faktury od polskich dostawców można pobrać bez OCR, a OCR zostawić dla WZ, zamówień, faktur zagranicznych i małych dostawców. To może realnie obniżyć koszty.

**Plusy:**  
- Inteligentne rozdzielenie strumieni: KSeF vs reszta.  
- Walidacja matematyki kodem, NIP, biała lista VAT.  
- Etapowanie: 3000 zł + 2400 zł = 5400 zł.  
- 21 dni, w budżecie.

**Minusy / wątpliwości:**  
- Zakłada, że KSeF jest u mnie wdrożony lub będzie. Muszę to potwierdzić.  
- Jeśli KSeF nie działa, zakres i koszt mogą się zmienić.

---

### KANDYDAT #88
**Dlaczego zwrócił uwagę:**  
To wiadomość PV, ale bardzo konkretna. Odradza zapis do bazy Optimy, tłumaczy, dlaczego to niebezpieczne. Rozróżnia PDF z warstwą tekstową od skanów. Mówi, że walidację matematyczną robi kodem, nie modelem. Uczciwie przyznaje, że n8n nie wdrażał produkcyjnie, ale zna się na odczycie dokumentów i integracjach.

**Plusy:**  
- Bardzo dojrzałe podejście do bezpieczeństwa Optimy.  
- Świadomość licencjonowania pracy rozproszonej.  
- Walidacja kodem, obsługa wyjątków, dane w UE.  
- 7500 zł + VAT, 18 dni.

**Minusy / wątpliwości:**  
- Tylko PV, bez oferty w formularzu.  
- Brak produkcyjnego doświadczenia z n8n.  
- Trzeba samemu potwierdzić licencję na pracę rozproszoną.

---

### KANDYDAT #68
**Dlaczego zwrócił uwagę:**  
Krótko, prosto i bez żargonu. Od razu mówi: trudne skany idą do modelu czytającego obraz, nie do zwykłego OCR. Z Optimą łączy się plikiem XML, nie zapisem do bazy. Matematykę sprawdza kod. Po wdrożeniu przez miesiąc poprawia to, co wyjdzie w praktyce.

**Plusy:**  
- Normalny język, zrozumiały dla mnie.  
- Bezpieczny import XML.  
- Walidacja matematyczna i folder ręcznej weryfikacji.  
- Cena 4500 zł, 21 dni – dobra relacja ceny do zakresu.  
- Ma doświadczenie w integracjach w firmie handlowej.

**Minusy / wątpliwości:**  
- Mniej szczegółów o wersji Optimy i wolumenie dokumentów.  
- Nie pyta o tyle rzeczy co #73 czy #88, więc wycena może wymagać doprecyzowania.

---

## 3. Wybrana szóstka

```json
{"top6": ["KANDYDAT #71", "KANDYDAT #73", "KANDYDAT #76", "KANDYDAT #83", "KANDYDAT #88", "KANDYDAT #68"]}
```

---
