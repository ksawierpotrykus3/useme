# Plan: Meta-łańcuch wariantów ofert (2 konta)

Dokument opisuje docelowy system generowania ofert na podstawie ustaleń.
Cel: przez tydzień bez ręki zbierać dane o tym, które warianty ofert dostają odzew.

---

## 1. Założenia biznesowe

- Dwa konta Useme, każde z własnym cookie i własnym slotem sesji.
- Jedno zlecenie obsługiwane przez oba konta, ale rozłożone w czasie.
- Na jedno zlecenie powstają 2 różne oferty, po jednej na konto.
- Konta nie robią tego samego zlecenia w tym samym momencie.
- Wnioski wyciąga człowiek. System ma tylko dostarczyć porównywalne, nieprzypadkowe dane.

---

## 2. Kolejka i rozdzielenie zleceń

- Konto 1 bierze zlecenia od końca listy (najstarsze).
- Konto 2 bierze zlecenia od początku (najnowsze).
- Idą naprzeciw siebie i z czasem trafiają na te same zlecenia.
- Bramki:
  - Blokada: jedno zlecenie obsługuje naraz tylko jedno konto.
  - Minimalny odstęp czasowy: drugie konto czeka losowy odstęp po pierwszym.
- Rejestr przypisania: które zlecenie poszło już na które konto.

---

## 3. Role i losowanie (50/50 per zlecenie)

- Role NIE są przypisane do konta na stałe.
- Dla każdego zlecenia losuje się, które konto dostanie tryb konserwatywny, a które meta.
- Role zamieniają się co zlecenie.
- Konsekwencja: rejestr jest globalny i kluczowany po zleceniu, nie po koncie.

---

## 4. Dwa tryby swobody (jedna mechanika)

Ta sama mechanika w obu trybach. Różni się tylko zakres swobody mutacji.

### Tryb konserwatywny
- Trzyma się blisko sprawdzonej bazy.
- Własny, wąski rozkaz: klasyczna struktura, nie kombinuj.
- Mało mutacji, przewidywalny, to punkt odniesienia.

### Tryb meta
- Mocno mutuje, szuka wyróżników.
- Adres wariantu narzucany twardo (nie liczy, że model "się postara").

---

## 5. Osie wariacji

Oferta = szkielet (stały) + osie (losowane). Szkielet nigdy się nie mutuje.

### Szkielet (stały, nietykalny)
- Fakty o zleceniu, stack, twarde zasady stylu.
- Wspólny dla wszystkich wariantów.

### Warstwa A - Narracja
- Otwarcie: grzecznościowe / konkret / pytanie / nawiązanie do branży / nawiązanie do problemu.
- Struktura: ciągły akapit / 2-3 akapity / akapit + punkty / akapit + lista pytań.
- Ton: formalny / ludzki / rzeczowy / partnerski.
- Długość: losowana, ADEKWATNA do złożoności oferty, w OBU trybach.
  Nie "krótka vs długa" na sztywno. Proste zlecenie = wachlarz krótszych,
  duże zlecenie = wachlarz dłuższych. Losowanie w dopasowanym zakresie.
- Zakończenie: neutralne / wezwanie do kontaktu / konkretny krok.

### Warstwa B - Treść merytoryczna
- Argument ceny: wartość / szybkość / doświadczenie / zakres / jakość.
- Podejście: sam / mały zespół / etapami.
- Wyróżnik: brak / pytanie / mini-zakres / demo / konsultacja / pomysł na start.
- Dowód kompetencji: ogólne doświadczenie / podobne wdrożenie / detale stacku / referencja branżowa.

### Warstwa C - Relacja z klientem
- Perspektywa: ja / my / Ty i Twój cel.
- Poziom kontaktu: zdystansowany / bezpośredni / doradczy.
- Pewność siebie: ostrożna / zrównoważona / asertywna.

### Warstwa D - Forma sygnału
- Gęstość techniczna: laicko / mieszanie / technicznie.
- Język korzyści: funkcje / korzyści / jedno i drugie.

### Zasada liczby osi
- Mało osi, mało wartości na oś.
- Różnorodność odczuwalna dla klienta, ale powtarzalna statystycznie.
- Za dużo osi = każda oferta unikatem = brak porównania.

---

## 6. Twarde filtry (nie osie, zawsze stosowane)

- Brak em dash.
- Brak nawiasów.
- Brak tabelek.
- Głównie tekst, punkty tylko czasem i naturalnie.
- Zakaz słów-wytrychów AI.
- Zero formatowania markdown.

---

## 7. Wycena (osobna, kontrolowana oś)

- Jedna mechanika wyceny w obu trybach.
- Kwota pochodzi z deterministycznego kalkulatora (`wycena_kalkulator.py`), nie od modelu.
  Kalkulator JUŻ istnieje i jest podpięty w chain_executor (slot 02b -> policz_wycene -> formatuj_wynik).
- Model zwraca tylko strukturę (moduly, godziny, flagi), kalkulator liczy kwotę i dni.
- Ta sama struktura = zawsze ta sama cena (deterministycznie).
- Model przepisuje kwotę 1:1 z bloku [WYNIK_KONCOWY]. Zero halucynacji ceny.
- Twarda bramka: min. 500 zł, min. 7 dni.
- Dla dwóch ofert na to samo zlecenie: kwota IDENTYCZNA. Ta sama wycena na oba konta.

### 7a. Wycena i research wspólne dla obu kont
- Research liczony RAZ na zlecenie, podawany obu wariantom.
- Wycena liczona RAZ na zlecenie, podawana obu wariantom.
- Wycena ma się NIE zmieniać między ofertami. Obie oferty na to samo zlecenie
  dostają tę samą kwotę i te same dni.
- Różni się tylko treść oferty (osie), nigdy research ani wycena.

---

## 8. Wspólna pamięć (klucz do nierobienia się w kółko)

Ważne rozróżnienie:
- ADRES wariantu (osie) jest losowany PER OFERTA, nie per konto.
- REJESTR historii jest PER KONTO (co dane konto już wysłało).
- Dodatkowo rejestr per klient (jak w obecnym mechanizmie 1-kontowym).

Zapisuje:
- które zlecenie na które konto,
- adres oferty (osie),
- użyte fakty/amunicja (np. CVE, wtyczki).

Działanie:
- Drugie konto, zanim napisze, czyta ofertę pierwszego.
- Zakaz powtarzania nie tylko formy, ale i użytej amunicji.
- Drugie losowanie wymuszone na adres ortogonalny (świadomy kontrast).
- Kary za ostatnio użyte adresy w skali czasu (żeby tydzień nie był monotonny).

### 8a. Stan obecny (mechanizm 1-kontowy, już istnieje)
- `engine.py`: `find_by_author(author_id)` znajduje zlecenia tego samego klienta.
- Wstrzykuje `previous_offers` + `variation_seed` do job_detail.
- `ai_pipeline.py`: `_podobienstwo_jaccard` wykrywa zbyt podobny tekst, retry z `variation_seed + proby`.
- Testy: `_test_anty_powtorka.py`, `_test_integracja_pipeline.py`, `test_author_dedup.py`.

### 8b. Co rozszerzyć pod 2 konta
1. Klucz rejestru: obecnie po `author_id` (klient). Dodać wymiar per konto,
   żeby konto B wiedziało, co wysłało konto A.
2. `variation_seed` ma tylko 5 wartości (0-4) i jest deterministyczny
   (`hash(author_id + job_id)`). Zwiększyć liczbę wartości i dodać osie, nie tylko ton.
3. Jaccard łapie podobieństwo tekstu, ale nie amunicję. Dodać osobny wykrywacz
   powtórzonych faktów/argumentów (np. ten sam CVE w obu ofertach).

---

## 9. Meta-łańcuch - dwie role

1. Kurator różnorodności:
   - pilnuje, żeby warianty były różne w obrębie zlecenia i w czasie.
   - losuje adresy, nakłada kary za powtórki.

2. Strażnik szkieletu:
   - sprawdza, czy wariant nie złamał twardych zasad stylu i nie odpłynął od faktów.
   - wariant, który łamie zasady, wypada albo jest poprawiany.

---

## 10. Adres wariantu - pola

Adres jest losowany PER OFERTA (nie per konto). Obecny test miał tylko:
otwarcie, ton, struktura, wyróżnik. To za mało.

Docelowy adres zawiera:
- otwarcie,
- struktura,
- ton,
- długość (losowana, adekwatna do złożoności zlecenia, w obu trybach),
- liczba akapitów,
- wyróżnik: jest / nie ma,
- pytanie: jest / nie ma,
- zakaz powtarzania amunicji poprzednika (z rejestru).

Uwaga: adres ≠ rejestr. Adres jest per oferta. Rejestr (co już wysłano)
jest per konto oraz per klient.

---

## 11. Błędy wykryte w teście (do naprawy)

UWAGA: Punkt o zmyślonych kwotach był błędem MOJEGO TESTU, nie systemu.
Skrypt testowy wołał model bezpośrednio, omijając kalkulator. Właściwy łańcuch
(run_chain) już używa kalkulatora. Wniosek: testy meta muszą iść przez run_chain,
a nie przez bezpośrednie call_deepseek.

1. Konserwatywna nie była konserwatywna - brak własnego trybu. Naprawa: osobny wąski rozkaz.
2. Ceny rozjechane w teście (12000 / 29000 / 42000). Przyczyna: test omijał kalkulator.
   Naprawa: test przez run_chain, wspólny research i wycena dla obu wariantów.
3. Ta sama długość tekstu. Naprawa: losowanie długości adekwatnej do zlecenia.
4. Ten sam hook/amunicja we wszystkich. Naprawa: zakaz powtarzania amunicji.
5. Meta B dostała tylko 1500 znaków poprzedniej oferty. Naprawa: cała oferta w kontekście.
6. Zakazy bez alternatywy działają słabo. Naprawa: zawsze podawać konkretny kierunek.

---

## 12. Kolejność wdrożenia

Stan wyjściowy: mechanizm anty-powtórki dla 1 konta już istnieje
(engine.py + ai_pipeline.py + testy). Rozbudowujemy go, nie piszemy od zera.

1. Research i wycena: liczone RAZ na zlecenie i współdzielone przez oba warianty
   (kalkulator już istnieje i jest podpięty, trzeba tylko zagwarantować wspólne źródło).
2. Rozbudować rejestr: dodać wymiar per konto obok per klient.
3. Rozszerzyć adres wariantu o długość, liczbę akapitów, flagi wyróżnika i pytania.
4. Rozszerzyć `variation_seed` (obecnie tylko 0-4) i dodać osie poza tonem.
5. Dodać wykrywacz powtórzonej amunicji obok Jaccarda.
6. Napisać osobny tryb konserwatywny (wąski rozkaz).
7. Dodać rozdzielenie kolejki (od końca / od początku) + blokadę + odstęp czasowy zależny
   od wieku zlecenia i liczby ofert.
8. Dodać losowanie 50/50 ról per zlecenie.
9. Powtórzyć test na tym samym zleceniu 143764 i porównać z obecnym wynikiem.

---

## 13. Do usunięcia (pliki tymczasowe)

- _meta_ab_test.py
- _meta_ab_result.txt
- _meta_ab_log.txt

---

## 14. Stan projektu po pełnym przeglądzie (co jest, czego brak)

### 14a. Co JUŻ istnieje (rozbudowujemy, nie piszemy od zera)
- `wycena_kalkulator.py` -> `policz_wycene` + `formatuj_wynik`. Podpięty w `chain_executor.py` (slot 02b).
- Mechanizm anty-powtórki per KLIENT: `storage.find_by_author` + `engine.py` (previous_offers, variation_seed) + `ai_pipeline._podobienstwo_jaccard` (retry z wymus_inny_styl).
- `BrowserDriver(cookies_path=...)` - już przyjmuje ścieżkę cookies jako parametr.
- `FormDriver(context=...)` - już przyjmuje kontekst przeglądarki jako parametr.
- `cortex_bridge.Chain` - raportowanie kroków do Cortexa, obsługa parent_id.
- Checkpointy łańcucha w `storage` (save/load/clear_checkpoint).
- Walidator 08 (włączony), reszta walidatorów wyłączona.

### 14b. Czego BRAKUJE (do zbudowania)
- ZERO obsługi wielu kont. `engine.py` tworzy jeden `BrowserDriver` z jednym `config.COOKIES_PATH`.
- `run_chain` robi CAŁY łańcuch (01 -> 02b -> 02a -> 08) naraz. Nie da się współdzielić researchu i wyceny między dwiema ofertami.
- `find_by_author` kluczuje po kliencie, nie ma wymiaru per konto.
- `variation_seed` ma 5 wartości i jest deterministyczny (hash(author_id + job_id)).
- Brak rejestru wysłanych ofert z przypisaniem do konta.
- Brak blokady zlecenia (które konto aktualnie obsługuje).
- Brak wykrywacza powtórzonej amunicji (Jaccard łapie tylko słowa).

### 14c. BARIERA ARCHITEKTONICZNA (kluczowa)
Aby research i wycena były wspólne dla obu kont, trzeba rozdzielić łańcuch na:
- ETAP WSPÓLNY: slot 01 (research) + slot 02b (wycena) -> liczony RAZ na zlecenie.
- ETAP PER OFERTA: slot 02a (treść) + walidator 08 -> liczony osobno dla każdej oferty.

Dziś `run_chain` tego nie potrafi. Trzeba dodać tryb częściowy (np. `run_chain(..., stop_after="02b")`
albo osobna funkcja `run_shared_context(job)` zwracająca {research, wycena_dni}), a potem
`run_chain(..., injected_context={research, wycena_dni, variation_seed, ...})` dla samych ofert.

To jest fundament pod całą resztę. Bez tego nie da się zagwarantować identycznej wyceny na oba konta.

---

## 15. Plan wykonania (kolejność, zależności, pliki)

### KROK A - Rozdzielenie łańcucha na wspólny i per-oferta (FUNDAMENT)
Pliki: `chain_executor.py`, `ai_pipeline.py`.
1. Dodać do `run_chain` parametr `stop_after` (np. "02b") - przerwij po wycenie.
2. Dodać parametr `injected_context` - wstrzyknij gotowe {research, wycena_dni} zamiast liczyć.
3. Dodać `run_shared_context(job)` -> zwraca {research, wycena_dni, kwota, dni}.
4. `SlotChainAIPipeline.generate_proposal` rozbić na:
   - `prepare_context(job)` -> shared,
   - `generate_variant(job, context, adres)` -> pojedyncza oferta.
Efekt: research i wycena liczone raz, obie oferty dostają identyczne.

### KROK B - Warstwa kont (multi-account)
Pliki: `config.py`, `browser_driver.py`, `form_driver.py`, `engine.py`.
1. `config.py`: zamiast jednego COOKIES_PATH -> lista kont [{id, nazwa, cookies_path}].
2. `BrowserDriver`: już przyjmuje cookies_path - wystarczy tworzyć osobny driver per konto.
3. Dodać slot sesji per konto (osobny BrowserContext).
4. `engine.py`: pętla po kontach zamiast jednego drivera.
Uwaga: zachować zgodność wsteczną - jedno konto nadal ma działać.

### KROK C - Rejestr per konto (rozszerzenie anty-powtórki)
Pliki: `storage.py`, `engine.py`.
1. Rozszerzyć rekord zlecenia o pole `konto` (które konto wysłało) i `adres` (osie wariantu).
2. Dodać `find_by_account(konto)` - co dane konto już wysłało (przecięcie z find_by_author).
3. Przy generowaniu oferty: previous_offers = suma (per klient + per konto) z tego samego zlecenia.
4. Zapisywać adres wariantu przy wysyłce.

### KROK D - Rozszerzenie adresu wariantu i variation_seed
Pliki: `engine.py`, `ai_pipeline.py`, `prompts/generatory/agent_02a_opis_oferty.md`.
1. Zwiększyć variation_seed (np. 0-19) i dodać osie poza tonem.
2. Adres = słownik: {otwarcie, struktura, ton, dlugosc, akapity, wyroznik, pytanie}.
3. Dopisać do promptu 02a twarde sterowanie długością (losowaną, adekwatną do zlecenia).
4. Wstrzykiwać pełny adres do job_detail.

### KROK E - Wykrywacz powtórzonej amunicji
Pliki: `ai_pipeline.py` (obok `_podobienstwo_jaccard`).
1. Wyciągać z oferty "użyte fakty" (np. CVE, nazwy wtyczek, kwoty rynkowe).
2. Porównywać z amunicją previous_offers; jeśli pokrycie > próg -> retry z zakazem.
3. Wstrzykiwać do promptu listę "NIE UŻYWAJ TYCH FAKTÓW".

### KROK F - Tryb konserwatywny
Pliki: `prompts/generatory/agent_02a_opis_oferty.md` (lub osobny plik), `ai_pipeline.py`.
1. Wąski rozkaz: klasyczna struktura, bez kombinowania.
2. Adres konserwatywny = stały, blisko bazy.
3. Adres meta = szeroki, z mutacjami.

### KROK G - Kolejka, blokada, odstęp czasowy
Pliki: `engine.py`, `storage.py`, `config.py`.
1. Rozdzielenie: konto 1 od końca listy, konto 2 od początku.
2. Blokada zlecenia (flaga "w_obrobce" + timeout zwolnienia).
3. Odstęp czasowy zależny od wieku zlecenia i liczby ofert (nie stały).

### KROK H - Losowanie 50/50 ról per zlecenie
Pliki: `engine.py`.
1. Dla każdego zlecenia losować, które konto = konserwatywne, które = meta.
2. Role zamieniają się co zlecenie.

### KROK I - Test na żywym zleceniu
Pliki: nowy `_meta_ab_test.py` (poprawiony, przez `run_chain`).
1. Odpalić przez `run_chain`, nie przez gołe `call_deepseek`.
2. Sprawdzić: identyczna wycena na oba warianty, inna treść, inna długość, inna amunicja.
3. Porównać z obecnym wynikiem z sekcji 11.

### Zależności między krokami
- KROK A jest fundamentem - bez niego B-I nie mają sensu dla wspólnej wyceny.
- KROK C zależy od B (potrzebna warstwa kont).
- KROK D, E, F można robić równolegle po A.
- KROK G, H zależą od B i C.
- KROK I na końcu, po A-H.

### Zasada nadrzędna dla wszystkich kroków
Wszystko musi działać wstecznie zgodnie dla 1 konta. Wielokonto to rozszerzenie,
nie zamiennik. Obecne testy (`_test_anty_powtorka.py`, `_test_integracja_pipeline.py`)
muszą dalej przechodzić.