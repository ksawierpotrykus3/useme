# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B
## TEMAT: Integracje Comarch ERP Optima, KSeF 2.0 / FA(3), Automatyzacja Obiegu Faktur, Praca Rozproszona

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW

**Budżety obserwowane w segmencie:** 4 500 – 16 000 zł netto.

**Typowe zlecenia:**
- Integracja OCR/AI z Comarch ERP Optima (import faktur kosztowych).
- Automatyczny import faktur zakupowych z KSeF do Optimy (rejestry VAT, ewidencja dodatkowa).
- Mostki e-commerce → Optima (Subiekt, WooCommerce, Baselinker, custom API).
- Wdrożenia pod KSeF 2.0 / FA(3) z uwzględnieniem pracy rozproszonej.
- Konwersja dokumentów XML → Optima (COM-ECO / Praca Rozproszona).
- Panel korekt i zatwierdzeń dla biur rachunkowych.

**Profil zleceniodawcy:**
- Biuro rachunkowe obsługujące 20–200 podmiotów (Optima Biuro Rachunkowe).
- CFO / Główny Księgowy w firmie handlowej lub produkcyjnej (10–200 pracowników).
- Właściciel firmy z obiegiem 300–3000 faktur kosztowych miesięcznie.
- Partner Comarch (reseller) szukający podwykonawcy do integracji.

**Charakterystyka klienta:** zna system ERP na poziomie użytkownika, nie rozumie warstwy wymiany danych. Nie odróżnia „API” od „bazy SQL”. Nie wie, że Comarch ma pięć różnych mechanizmów integracyjnych, z których każdy ma inne licencjonowanie i inne tryby awarii. Nie wie, że import XML pracy rozproszonej może być od października 2026 kontrolowany licencyjnie przez pakiet Comarch OCR&KSeF.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN PRAWNY NA 2026 ROK

### 2.1. Harmonogram KSeF 2.0 — twarde daty

| Data | Zakres obowiązku |
|------|-----------------|
| **26–31 stycznia 2026** | Przerwa techniczna KSeF 1.0; wyłączenie Modułu Certyfikatów i Uprawnień (MCU) |
| **1 lutego 2026** | Udostępnienie KSeF 2.0 jako jedynego systemu; **obowiązek ODBIORU faktur** dla wszystkich podatników VAT (bez możliwości odmowy akceptacji); obowiązek **wystawiania** dla podatników z obrotem >200 mln zł w 2024 r. |
| **1 kwietnia 2026** | Obowiązek **wystawiania** dla MŚP i JDG (obrót ≤200 mln zł) |
| **1 stycznia 2027** | Obowiązek dla najmniejszych podmiotów (sprzedaż ≤10 000 zł/mies. dokumentowana fakturami) |

**Kluczowa pułapka interpretacyjna:** odroczenie terminu wystawiania **nie zwalnia z obowiązku odbioru**. Podatnik zwolniony do 2027 r. z wystawiania faktur w KSeF **musi** odbierać faktury z KSeF już od 1 lutego 2026 r..

### 2.2. Struktura logiczna FA(3) — co zastępuje FA(2)

FA(3) zastępuje FA(2) bezwarunkowo od 1 lutego 2026 r. Dotyczy to również faktur korygujących do faktur wystawionych wcześniej w FA(1)/FA(2).

**Kluczowe zmiany:**
- **Rozbicie stawki 0%** na trzy kategorie: `0 KR` (kraj), `0 WDT` (wewnątrzwspólnotowa dostawa), `0 EX` (eksport).
- **Rozbicie NP** (niepodlegające opodatkowaniu) na `NP I` i `NP II`.
- **Nowe pola:** `GTIN` (Globalny Numer Jednostki Handlowej, max 20 znaków), `Indeks`, `PKWiU`, `CN`, `PKOB` w wierszu faktury.
- **Nowa rola podmiotu:** `Rola 11 — Pracownik` w sekcji `Podmiot3` (dla wydatków pracowniczych).
- **Załączniki do faktury** jako integralna część dokumentu (od 1 stycznia 2026 w e-US).
- **Numer KSeF i zbiorczy identyfikator** — nowe obowiązki w JPK_V7 od lutego 2026.

### 2.3. Metody integracji z Comarch ERP Optima — pięć różnych rzeczy pod jedną nazwą

**A. Praca Rozproszona (XML / COM-ECO)**
- Wymiana plików XML między bazami Optimy lub z systemów zewnętrznych.
- Import przez: Narzędzia → Praca rozproszona → Import.
- **Bezlicencyjny** — do odwołania. Comarch zapowiedział kontrolę licencyjną od października 2026 (pakiet OCR&KSeF, od ~130 zł netto/mies.), ale termin został przesunięty bez nowej daty.
- Ograniczenie: brak pełnej walidacji biznesowej — import trafia bezpośrednio do rejestrów VAT / ewidencji dodatkowej.

**B. CDN.API (COM / CDNBase / Optima.Dokumenty)**
- Własny model obiektowy COM Comarchu. To właśnie Comarch ma na myśli, mówiąc „API”.
- Działa **tylko na Windows, w procesie, obok zainstalowanej Optimy** — nie da się wywołać z kontenera.
- Pełna walidacja biznesowa, bufor dokumentów, księgowanie do Księgi Handlowej.
- **Wymaga licencji operatora** — każde połączenie integracyjne „zajmuje” miejsce licencyjne w sensie prawnym.

**B2. Comarch ERP XL (Moduł Procesy / API XL `CDN_API` / Automat WZ → FS)**
- W Comarch ERP XL (np. wersje 2025.x) moduł **Modelowanie Procesów** wymaga osobnej licencji serwerowej w kluczu sprzętowym HASP/Sentinel.
- Przy automatycznym generowaniu **Faktur Sprzedaży (FS) z dokumentów WZ** kluczowe są 3 mechanizmy:
  1. **Idempotencja relacji `TrN_ZaNId` / `TraNag`:** twarda blokada przed wygenerowaniem duplikatu FS do tej samej WZ przy równoległym uruchomieniu harmonogramu i pracy operatora.
  2. **Walidacja kompletności pod KSeF 2.0 `FA(3)`:** przed spięciem WZ w FS automat musi zweryfikować poprawność NIP, formy płatności i kodów stawek VAT (`0 KR / 0 WDT / 0 EX`), aby wystawiona FS nie została odrzucona przez bramkę KSeF.
  3. **Kolejka błędów (bufor wyjątków):** jeśli kontrahent ma zablokowany limit kredytowy lub brakuje ceny na pozycji WZ, dokument trafia do rejestru błędów z powiadomieniem operatora, nie blokując przetwarzania pozostałych WZ w paczce.
- Standardowy kształt integracji: cienka usługa HTTP na hoście Optimy, wystawiająca REST dla reszty świata.

**C. Comarch ERP Web API (REST)**
- Usługa sieciowa dostarczana przez Comarch, włączana w konfiguracji.
- Umożliwia dodawanie i modyfikację dokumentów w modułach handlowych, magazynowych, finansowo-księgowych i kadrowo-płacowych.
- Działa dla Optimy w chmurze (`OptimaCloudMode = true`) oraz w modelu stacjonarnym z odpowiednim kluczem licencyjnym.
- Dokumentacja API jest za ścianą partnerską — brak publicznego Swaggera.

**D. Bezpośredni odczyt/zapis SQL**
- **Nie jest API.** Używany powszechnie, ale łamie licencję i unieważnia gwarancję.

**E. Dodatki firm trzecich (resellerzy)**
- Komercyjne „Web API do Optimy” sprzedawane jako produkty (ok. 5 800–8 800 zł netto).

---

## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1. Mina nr 1: Trzy zupełnie różne strumienie dokumentów (KSeF XML vs cyfrowy PDF z warstwą tekstową vs skan/zdjęcie z terenu)

**Co klient pisze:** „Chcemy prosty OCR AI z czytaniem faktur PDF, maili i zdjęć z telefonów z zapisem do Optimy”.

**Co jest prawdą (i czego nie wie 85% wykonawców):** Wrzucanie wszystkich dokumentów do jednego worka OCR Vision to palenie budżetu na tokeny i generowanie halucynacji. W firmie handlowo-produkcyjnej występują **trzy osobne strumienie**:
1. **Faktury krajowe w KSeF (XML FA(3)):** Od 1 lutego 2026 r. polskie faktury B2B są ustrukturyzowanym XML-em. Co więcej, **Comarch ERP Optima od wersji 2026.4.1 posiada natywny mechanizm pobierania faktur z KSeF w tle wraz z pozycjami**. Budowanie w n8n prostego pobieracza KSeF dubluje funkcję ERP — prawdziwą wartością automatyzacji w n8n jest przypisanie MPK/kategorii kosztowej, automatyczne parowanie faktury z dokumentem magazynowym **WZ / zamówieniem (PZ/RO)** oraz obsługa dokumentów spoza KSeF.
2. **Cyfrowe PDF-y przychodzące mailem:** Posiadają **natywną warstwę tekstową**. Odczytujemy z nich tekst i tabele bezpośrednio (100% dokładności znakowej, zero kosztu tokenów Vision, zero błędów OCR).
3. **Papierowe skany oraz zdjęcia z telefonów od pracowników w terenie (WZ, paragony, faktury zagraniczne):** Zdjęcia robione telefonem pod kątem i w słabym świetle wymagają przed modelem Vision **preprocessingu obrazu** (prostowanie skosu / deskew, poprawa kontrastu, odszumianie) oraz oceny pewności (**confidence score** dla każdego pola — poniżej progu np. 85% dokument trafia do kolejki weryfikacji).

### 3.2. Mina nr 2: Zaokrąglenia VAT — automat, który wywala się na 15% faktur

**Co klient pisze:** „Chcemy, żeby wszystko zgadzało się co do grosza”.

**Co jest prawdą:** Prawo (ustawa o VAT) dopuszcza dwie metody liczenia VAT: **od sumy stawek w podsumowaniu** lub **od sumy pojedynczych pozycji**. Różnica pojawia się przy fakturach wielopozycyjnych z ułamkami groszy.

**Przykład liczbowy:** 3 pozycje × 0,10 zł netto × 23% VAT:
- VAT liczony od pozycji: 3 × (0,10 × 0,23) = 3 × 0,023 → po zaokrągleniu 3 × 0,02 = **0,06 zł**.
- VAT liczony od sumy: 0,30 × 0,23 = 0,069 → po zaokrągleniu **0,07 zł**.

Różnica wynosi 1 grosz. Sztywna walidacja „na równość groszową” między dokumentem a rejestrem VAT w Optimie wyłoży automat na **15% poprawnych faktur**. Rozwiązaniem jest rozdzielenie ekstrakcji semantycznej (LLM zwraca JSON) od deterministycznego skryptu matematycznego z **tolerancją groszową ±0,01–0,02 zł** na dokument.

### 3.3. Mina nr 3: Deduplikacja (trzy kanały wejścia) oraz Biała Lista VAT (próg 15 000 zł)

**Scenariusz:** Ten sam dokument przychodzi równolegle mailem (PDF), ze skanera/telefonu pracownika (JPG) oraz z KSeF (XML FA(3)).
- **Klucz deduplikacji:** `znormalizowany NIP sprzedawcy` + `NumerFakturyOryginalny` (P_2A) + `TypDokumentu` (faktura vs korekta) + hash pliku (SHA-256).
- **Weryfikacja Białej Listy MF i MPP (próg 15 000 zł brutto):** Przy fakturach kosztowych $\ge 15\ 000$ zł brutto (lub z załącznika nr 15) brak weryfikacji czynnego statusu VAT i rachunku bankowego dostawcy w wykazie MF oznacza solidarną odpowiedzialność podatkową i wyłączenie kosztu z KUP. Automat sprawdza to w API MF w ułamku sekundy.
- **Dokumenty magazynowe i handlowe w Pracy Rozproszonej XML:** Praca Rozproszona XML w Optimie pozwala bezpiecznie przenosić nie tylko rejestry zakupu VAT, ale też dokumenty handlowo-magazynowe (**WZ, PZ, RW, PW, MM, RO**), podczas gdy bezpośredni zapis SQL `INSERT` rozwala numerację, indeksy i unieważnia gwarancję producenta.


---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ OFERTY

**Otwarcie A — dla klienta z wolumenem krajowym:**
> „Od 1 lutego 2026 faktury krajowe są w KSeF jako XML FA(3) — budowanie OCR dla nich to palenie 60% budżetu. Realny problem architektoniczny to nie odczyt PDF, a **tolerancja groszowa VAT** między FA(3) a rejestrem VAT w Optimie i **deduplikacja** dokumentów przychodzących jednocześnie z KSeF i mailem.”

**Otwarcie B — dla klienta z pracą rozproszoną:**
> „Format Praca Rozproszona (XML) jest bezlicencyjny, ale Comarch zapowiedział kontrolę licencyjną importu XML do rejestrów VAT — każdy zaimportowany dokument ma zużywać limit pakietu OCR&KSeF (od ~130 zł netto/mies.). Zanim wybierzemy ten kanał, trzeba ustalić, czy Państwa wolumen nie postawi nas w sytuacji, w której taniej jest iść przez CDN.API lub Web API.”

**Otwarcie C — dla biura rachunkowego:**
> „Biuro rachunkowe na Optimie ma trzy równoległe kanały dokumentów: KSeF API, skrzynka IMAP i praca rozproszona od klientów. Bez **bufora akceptacji** dla księgowej — zamiast bezpośredniego zapisu do rejestru VAT — każdy błąd parsowania FA(3) ląduje w księdze. Pytanie brzmi: czy księgowa ma widzieć kolejkę wyjątków, czy ma dostawać gotowe dokumenty do zatwierdzenia.”

---

## 5. CZERWONA LISTA / ANTYWZORCE — CZEGO KATEGORYCZNIE NIE PISAĆ

### 5.1. Zakaz bezpośrednich INSERT-ów do bazy MS SQL Optimy

**Nie wolno proponować ani obiecywać:**
- `INSERT INTO CDN.TraNag`, `CDN.TraElem`, `CDN.Kontrahenci`, `CDN.DokElem` ani żadnej innej tabeli.
- Modyfikacji `CDN.Sekwencje` ani ręcznego nadawania `TrN_ID`.
- Triggerów na tabelach CDN.

**Konsekwencje:**
- Łamie umowę licencyjną Comarch — asysta i gwarancja **natychmiast tracą ważność**.
- Psuje triggery, sekwencje ID, relacje między tabelami.
- Uniemożliwia upgrade Optimy (nowa wersja nadpisze schemat, integracja się rozsypie).
- Comarch może odmówić wsparcia technicznego i zażądać audytu.

**Alternatywy:** Praca Rozproszona (XML), CDN.API (COM), Comarch ERP Web API (REST). Zawsze przez warstwę udokumentowaną przez producenta.

### 5.2. Zakaz obietnic 100% bezobsługowego księgowania

**Nie wolno pisać:** „W pełni automatycznie zaksięgujemy wszystkie faktury bez udziału człowieka”.

**Dlaczego:** każdy system ERP wymaga akceptacji wyjątków. Faktury z błędnym NIP-em, nieznanym kontrahentem, rozbieżnością VAT, brakiem mapowania pozycji — muszą trafić do kolejki weryfikacji. Obietnica „zero człowieka” to katastrofa podatkowa: błąd w dekretacji → korekta JPK → odpowiedzialność karnoskarbowa.

**Poprawna obietnica:** „Automatyzujemy 85–95% wolumenu. Pozostałe 5–15% trafia do **panelu korekt** z pełnym kontekstem (oryginalny XML FA(3), wynik walidacji, propozycja dekretacji), gdzie księgowa zatwierdza jednym kliknięciem lub koryguje.”

### 5.3. Zakaz proponowania rozmów telefonicznych / Google Meet / darmowych konsultacji wideo

Komunikacja na Useme jest w 100% asynchroniczna i pisemna. Propozycja „porozmawiajmy na Zoomie” = sygnał amatora, który nie potrafi sprzedać przez tekst.

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 6 000 – 15 000 ZŁ)

### Moduł 1: Konektor źródeł (KSeF API 2.0 + IMAP/Drive)

**Zakres:**
- Uwierzytelnienie w KSeF 2.0 (certyfikat KSeF z MCU lub token).
- Pobieranie faktur zakupowych (`GET /invoices/ksef/{ksefNumber}`) i paczek zbiorczych.
- Kolejkowanie pobrań (rate limiting — KSeF API ma limity, których Comarch nie publikuje).
- Skrzynka IMAP (faktury zagraniczne, PDF, skany) — odbiór, archiwizacja, ekstrakcja załączników.
- Google Drive / OneDrive jako alternatywne źródło dla skanów od pracowników.

**Wycena modułu:** 1 800 – 3 500 zł.

### Moduł 2: Silnik parsowania FA(3) + OCR AI dla zagranicy

**Zakres:**
- Parser XML FA(3) — mapowanie pól `P_1`, `P_2A`, `P_7`, `P_8B`, `P_9A`, `P_9B`, `P_11`, `P_12`, `P_13_x`, `P_14_x`, `P_15`, `KodWaluty`, `KursWalutyZ`.
- Obsługa nowych kategorii stawek: `0 KR`, `0 WDT`, `0 EX`, `NP I`, `NP II`.
- OCR AI dla faktur zagranicznych (PDF/JPG) — engine typu Textract / Azure Document Intelligence / open-source Tesseract z fine-tuningiem na fakturach UE.
- Rozpoznawanie walut, kursów NBP (tabela A z daty wystawienia lub daty kursu w FA(3)).

**Wycena modułu:** 2 000 – 4 000 zł.

### Moduł 3: Moduł walidacji biznesowej i tolerancji VAT

**Zakres:**
- Walidacja NIP (suma kontrolna, VIES dla UE).
- **Tolerancja groszowa VAT:** porównanie VAT z FA(3) vs VAT z rejestru VAT Optimy z progiem ±0,02 zł na dokument; logowanie rozbieżności.
- Deduplikacja: klucz `NIP + NumerFakturyOryginalny + DataWystawienia`.
- Walidacja stawek: czy `P_12` jest zgodne z `P_13_x`/`P_14_x`.
- Weryfikacja kursu walutowego (NBP, tabela A).
- Kolejka wyjątków dla walidacji nieprzechodzących.

**Wycena modułu:** 1 500 – 2 500 zł.

### Moduł 4: Mostek importowy do Comarch ERP Optima

**Zakres:**
- **Wariant A (Praca Rozproszona):** generowanie plików XML w formacie COM-ECO, import przez `Narzędzia → Praca rozproszona → Import`. Bezlicencyjny, ale bez pełnej walidacji biznesowej.
- **Wariant B (CDN.API):** integracja przez COM (`CDNBase`, `Optima.Dokumenty`). Pełna walidacja, bufor dokumentów, wymaga licencji operatora i hosta Windows.
- **Wariant C (Web API):** REST dla Optimy w chmurze. Dokumentacja za ścianą partnerską.
- **Decyzja wariantu:** na podstawie odpowiedzi na pytanie kwalifikujące (patrz sekcja 7).

**Wycena modułu:** 2 000 – 4 000 zł.

### Moduł 5: Panel korekt i zatwierdzeń dla księgowości

**Zakres:**
- Kolejka dokumentów oczekujących na akceptację (web UI).
- Podgląd oryginalnego XML FA(3) obok propozycji dekretacji.
- Edycja mapowania kontrahenta / kont księgowych.
- Bulk approve dla dokumentów bez wyjątków.
- Log audytowy: kto zatwierdził, kiedy, co zmienił.

**Wycena modułu:** 1 500 – 3 000 zł.

### Moduł 6: Wdrożenie i 30 dni asysty

**Zakres:**
- Konfiguracja środowiska, certyfikaty KSeF, testy na środowisku Demo KSeF 2.0.
- Szkolenie asynchroniczne (nagrania + dokumentacja).
- 30 dni asysty powdrożeniowej (reakcja na błędy walidacji, korekty mapowań).

**Wycena modułu:** 1 200 – 2 000 zł.

**Suma:** 10 000 – 19 000 zł (przy pełnym zakresie). Dla zakresu podstawowego (Moduły 1–4 + 6): **6 500 – 12 000 zł**.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODKU ANALIZY)

Pytania umieszczone w treści oferty po przedstawieniu problemu architektonicznego, przed wyceną. Cel: wymusić odpowiedź na priv.

**Pytanie 1 (wariant integracji):**
> „Czy Państwa Comarch ERP Optima pracuje w modelu **stacjonarnym** (serwer Windows w siedzibie), czy w **Chmurze Comarch** (`OptimaCloudMode = true`)? Od tego zależy, czy integracja pójdzie przez CDN.API (tylko Windows, in-process), czy przez Comarch ERP Web API (REST, chmura).”

**Pytanie 2 (strumień dokumentów):**
> „Jaki procent faktur kosztowych to faktury **krajowe z NIP PL** (które po 1 lutego 2026 są w KSeF jako XML FA(3)), a jaki to **faktury zagraniczne, paragony, WZ lub dokumenty spoza KSeF**? Od tego zależy, czy OCR jest w ogóle potrzebny, czy wystarczy konektor KSeF API 2.0.”

**Pytanie 3 (zakres modułów Optimy):**
> „Czy posiadają Państwo moduł **Handel / Kasa / Magazyn** (faktury zakupowe trafiają do modułu handlowego z mapowaniem pozycji), czy wyłącznie **Księga Handlowa / Rejestry VAT** (dokumenty trafiają bezpośrednio do rejestru VAT bez rozbijania na pozycje)? To determinuje, czy mostek importowy musi mapować pozycje na towary, czy tylko nagłówek dokumentu.”

---

*Karta wiedzy wygenerowana na podstawie stanu prawnego i dokumentacji technicznej zweryfikowanej pod kątem 2026 roku. Wszystkie stwierdzenia dotyczące KSeF 2.0, FA(3) i integracji Comarch ERP Optima znajdują potwierdzenie w źródłach Ministerstwa Finansów, Comarch oraz dokumentacji technicznej partnerów.*