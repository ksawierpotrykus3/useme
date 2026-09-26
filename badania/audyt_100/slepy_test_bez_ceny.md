Poniżej ranking wyłącznie po treści, sposobie myślenia, zaufaniu i naturalności. Kwoty, terminy i liczby umów pomijam całkowicie — nawet jeśli przewijają się w wiadomościach, nie mają wpływu na ocenę.

## Ranking 1–10

1. **A — Antoni, AppWave**
2. **I — bez podpisu**
3. **B — Mariusz, ailone**
4. **C — Łukasz**
5. **E — Dominik, grodev.pl**
6. **D — Dawid**
7. **F — Adam**
8. **G — bez podpisu**
9. **H — Arek**
10. **J — bez podpisu**

---

### 1. A — Antoni, AppWave

**Co robi świetne wrażenie:**
To jedyna wiadomość, która od razu nie sprzedaje „OCR do wszystkiego”, tylko przebudowuje zakres: KSeF, Optima 2026.4.1, faktury krajowe, WZ, zamówienia, faktury zagraniczne, zdjęcia z terenu. Antoni rozumie, że problem nie polega na „przepuszczeniu PDF przez AI”, tylko na tym, co ma sens automatyzować, a co już jest w systemie. Do tego konkret: hash pliku, deduplikacja, osobny klucz tylko do czytania KSeF, model zostawia puste pola zamiast zgadywać, walidacja sum robiona kodem, nie przez AI, tolerancja groszowa, Biała Lista VAT, 15 000 zł, karty towarów w Optimie, import XML, brak bezpośredniego pisania do bazy, test na kopii. To jest język człowieka, który realnie robił takie wdrożenia albo je głęboko przeanalizował. Etapowanie, płatność za odebrany etap i pytanie o trudne dokumenty budują zaufanie.

**Co może niepokoić / jest słabsze niż ideał:**
Wiadomość jest bardzo dopracowana, momentami aż „produktowa”. Link do artefaktu i prototypu trzeba zweryfikować, bo ładny link nie zastąpi działającego wdrożenia. Ale merytorycznie i komunikacyjnie to lider.

---

### 2. I — bez podpisu

**Co robi świetne wrażenie:**
Bardzo mocny, gęsty technicznie głos. Trafia w KSeF, XML FA(3), Optimę 2026.4.1, rozdzielenie OCR od walidacji, tolerancję 1–2 gr, deduplikację po NIP + numerze + hashu, Białą Listę przy 15 000 zł, Pracę Rozproszoną XML lub Comarch ERP Web API, zakaz bezpośredniego INSERT do bazy, testy na kopii. Do tego konkretne doświadczenie: 3500+ dokumentów, 99,4% precyzji, Comarch ERP XL, 45 WZ dziennie. To brzmi jak ktoś, kto naprawdę siedzi w temacie dokumentów i Comarchu.

**Co brzmi gorzej niż u lidera:**
Styl jest telegramowy, bardzo techniczny, miejscami zimny. Dla nietechnicznego właściciela firmy to może być ściana pojęć. Brakuje trochę ludzkiego „jak to będzie wyglądać u Was” i większego rozpisania WZ/zamówień. Merytorycznie jest blisko A, ale A wygrywa przystępnością i poczuciem partnerstwa.

---

### 3. B — Mariusz, ailone

**Co robi świetne wrażenie:**
Bardzo dobre rozpoznanie KSeF jako źródła pewnych danych. Nie sprzedaje OCR tam, gdzie nie trzeba. Świetnie łapie ryzyko duplikatu: ta sama faktura z KSeF i ze skanu wrzuconego z przyzwyczajenia. Do tego weryfikacja NIP + numer dokumentu, tolerancja VAT przy zaokrągleniach, preprocessing obrazu, model widzący stronę, walidacja sum jako detektor błędów. Ma też sekcję „ryzyko, które przewiduję” — to buduje zaufanie, bo nie udaje, że wszystko będzie proste.

**Co brzmi gorzej niż u lidera:**
Poważny zgrzyt: najpierw mówi, że wszystko zostaje u klienta, a potem „formalnie proponuję licencję, bo uniwersalne komponenty muszę zostawić po swojej stronie”. To nie musi być złe, ale wymaga jasnego wyjaśnienia. U A ten temat jest czystszy: scenariusze, konfiguracja i instrukcje są klienta. B jest bardzo dobry, ale ta sprzeczność obniża zaufanie.

---

### 4. C — Łukasz

**Co robi świetne wrażenie:**
Bardzo dojrzała architektura: n8n jako orkiestracja, a obok własny serwis w Pythonie do OCR, ekstrakcji i walidacji. Łukasz rozumie, że n8n do samego spinania jest świetne, ale trudne OCR i walidacja w węzłach bywają koszmarem utrzymaniowym. Ma doświadczenie z Comarch Optima, Insert GT i Symfonią, własny system BusiKM dla firm transportowych, gdzie zdjęcia paragonów są gorsze niż tutaj. Prosi o 3–5 najgorszych dokumentów i mówi wprost, że powie, czy da się automatyzować, czy nie. To bardzo uczciwe.

**Co brzmi gorzej niż u lidera:**
Nie wspomina KSeF ani razu. Przy 2026 roku to duża luka. Może to wynikać z tego, że odpowiadał tylko na dwa pytania z ogłoszenia, ale dla właściciela firmy to sygnał, że nie przeprojektował zakresu tak jak A, B, G czy I. Poza tym proponuje własny serwis w Pythonie — to może być dobre, ale dla nietechnicznego przedsiębiorcy mniej przejrzyste niż czyste n8n + import.

---

### 5. E — Dominik, grodev.pl

**Co robi świetne wrażenie:**
Bardzo uczciwy. Odradza bezpośredni zapis do bazy Optimy i wyjaśnia dlaczego: numeracja, powiązania, rejestry VAT, utrata wsparcia. Mówi o pracy rozproszonej, licencjonowaniu, XML. W OCR rozdziela PDF z warstwą tekstową od prawdziwych skanów, używa modelu widzącego obraz, a walidację robi kodem, nie modelem. Dodaje uwagę o przetwarzaniu danych w UE. I najważniejsze: przyznaje, że n8n nie wdrażał produkcyjnie. To szczere.

**Co brzmi gorzej niż u lidera:**
Właśnie to przyznanie jest jednocześnie cnotą i ryzykiem. Przy zleceniu, gdzie n8n jest wymagane, brak produkcyjnego doświadczenia w n8n to realny minus. Merytorycznie broni się świetnie, ale nie ma takiego poczucia „robiłem dokładnie to”.

---

### 6. D — Dawid

**Co robi świetne wrażenie:**
Krótko, konkretnie, bez ściemy. Dwutorowo OCR + model AI, stała struktura, walidacja sum, NIP z cyfrą kontrolną, folder weryfikacji, import przez plik wymiany, n8n na własnym serwerze. Pyta o wolumen i czy import ma iść do rejestru VAT, czy dokumentów magazynowych. To dobre pytania.

**Co brzmi gorzej niż u lidera:**
Sam przyznaje, że format i moduł Optimy to „główna niewiadoma”. To uczciwe, ale u lidera ta niewiadoma jest już rozpisana na warianty. Portfolio o feedach Midocean i PF Concept jest mniej podobne do dokumentów OCR niż BusiKM czy KSEBridge. Brakuje głębi przy WZ i zamówieniach.

---

### 7. F — Adam

**Co robi świetne wrażenie:**
Dobrze łapie tolerancję VAT i podaje konkretny przykład groszowych różnic. Ma link do deduplikacji, rozumie ryzyko powtórnego przetworzenia, pyta o KSeF. Styl jest rzeczowy, asynchroniczny, bez przesadnego marketingu.

**Co brzmi gorzej niż u lidera:**
To bardziej głos w dyskusji niż pełna oferta. „Sam rdzeń, bez zapisu do Optimy” — czyli część najważniejsza dla klienta zostaje na później. Brakuje doświadczenia dokumentowego podobnego do tego zlecenia. Jest sensowny, ale nie przyciąga tak jak A, I, B czy C.

---

### 8. G — bez podpisu

**Co robi świetne wrażenie:**
Zadaje jedno z najważniejszych pytań: czy faktury kosztowe od polskich dostawców są już pobierane w Optimie z KSeF. To realnie zmienia połowę zakresu. Widać, że nie chce sprzedawać OCR bez sensu. Krótko, naturalnie, merytorycznie.

**Co brzmi gorzej niż u lidera:**
To nie jest oferta, tylko pytanie przed ofertą. Nie pokazuje doświadczenia, planu, podejścia do skanów, WZ, zamówień, importu. Jako wiadomość na czacie — dobra. Jako kandydat do pracy — niepełny.

---

### 9. H — Arek

**Co robi świetne wrażenie:**
Ma KSEBridge, czyli projekt okołofakturowy i KSeF. Proponuje n8n, OCR + AI, niezależny moduł obliczeniowy, folder weryfikacji, deduplikację, zmianę nazw, archiwizację. Zadaje dużo pytań o wersję Optimy, moduły, wolumen, EAN, rejestr VAT.

**Co brzmi gorzej niż u lidera:**
Brzmi jak szablon. Dużo pytań, mało konkretów: jak dokładnie połączy się z Optimą, jak rozwiąże karty towarów, jak przetestuje, co już robił z n8n. Pytania są dobre, ale brakuje planu i dowodów. Wygląda jak ktoś, kto dopiero chce zdiagnozować projekt, a nie ktoś, kto już ma przemyślane rozwiązanie.

---

### 10. J — bez podpisu

**Co robi świetne wrażenie:**
Rozumie bałagan dokumentów: krzywe skany, NIP ze spacjami, rozjechane kolumny, potrzeba tolerancji groszowej, folder weryfikacji, wideo-instrukcje. To wszystko jest poprawne.

**Co brzmi gorzej niż u lidera:**
Ton jest zbyt sprzedażowy: „typowy bałagan”, „program sam odczyta”, „skrócę obsługę o 85%”. Deklaracja „gotowy node n8n do Optima REST API” brzmi podejrzanie, bo Optima REST API nie jest oczywistym, uniwersalnym rozwiązaniem w każdej instalacji. Do tego claim 3500+ dokumentów i 99,4% wygląda jak wklejony skądinąd. Brakuje pokory i konkretu. Najmniej chciałbym na tej podstawie rozmawiać.

---

## Dlaczego nr 1 to A — Antoni

A wygrywa, bo łączy trzy rzeczy, których brakuje większości:

1. **Myślenie biznesowe, nie tylko techniczne.** Nie sprzedaje OCR do faktur, które i tak przyjdą z KSeF. Przebudowuje zakres tak, żeby klient nie płacił za automatyzowanie czegoś, co Optima już umie.
2. **Głębokie zrozumienie Optimy i ryzyk.** Import XML, brak bezpośredniego zapisu do bazy, karty towarów, dopasowanie pozycji, test na kopii, KSeF, Biała Lista, 15 000 zł. To są szczegóły, które pokazują, że ktoś myślał o wdrożeniu, a nie tylko o demonstracji AI.
3. **Ludzki, partnerski ton.** Mówi po polsku, nie zasypuje żargonem, etapuje, pyta o trudne dokumenty i wolumen, proponuje rozmowę. Brzmi jak człowiek, z którym można się dogadać, a nie jak generator ofert.

I jest blisko merytorycznie do kandydata I, ale I jest zimny i techniczny. B ma świetne ryzyka, ale zgrzyt licencyjny. C jest bardzo dobry, ale pominął KSeF. E jest uczciwy, ale nie wdrażał n8n produkcyjnie. Reszta ma albo mniejszą głębię, albo zbyt dużo marketingu. Dlatego nr 1 to A.