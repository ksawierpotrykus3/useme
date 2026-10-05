# Znajdź plik z brakującymi zleceniami

> **Workspace:** c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core

---

**User**

`/c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia`znajdz w projekcie calym plik ktory mowi jakie zlecenia musimy wrzucic jeszcze. 

**Assistant**














Sprawdzam szerszy projekt – szukam pliku z listą zleceń do wrzucenia.






Znalazłem kandydatów. Sprawdzam dwa najbardziej prawdopodobne pliki.





Znalazłem. Plikiem, o który pytasz, jest:

[FINALNA_LISTA_ZLECEN_BADAWCZYCH.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/FINALNA_LISTA_ZLECEN_BADAWCZYCH.md)

To dokument nadrzędny (zastępuje starszą `LISTA_ZLECEN_DO_WYSTAWIENIA.md` z 23.09) i to w nim masz pełną listę zleceń — co wysłane, co wystawione, a co jeszcze trzeba wystawić.

**Co jest już zrobione:**
- **#144890** (OCR/n8n) — ✅ wysłane, zebrane 112 wykonawców
- **Zlecenie 1** — Subiekt/BaseLinker — ✅ wystawione
- **Zlecenie 3** — Mobile native (Kotlin/Flutter) — ✅ wystawione

**Co trzeba jeszcze wystawić (5 zleceń):**

| Slot | Nisza | Status |
|---|---|---|
| 2 | Konfigurator 3D (Three.js) | do wystawienia |
| 4 | Scraping / boty | do wystawienia |
| 5 | PWA / panel B2B (MVP) | do wystawienia |
| 6 | IdoSell B2B | do wystawienia |

Gotowe treści do wklejenia (z minami AI w sekcji 7-8) są w sekcjach 3 tego pliku — Zlecenia 2, 4, 5, 6.

**Uwaga — dwie rozbieżności, które warto zweryfikować:**

1. W tabeli statusów (sekcja 3) **Zlecenie 2 i 4 są oznaczone „do wystawienia"**, ale w sekcji 4.6 pokrycie liczone jest już z uwzględnieniem Zlecenia 2 i 4 jako pokrytych. To niespójność wewnątrz dokumentu — status wg tabeli to źródło prawdy.

2. W `STRAT-08-MYSTERY-SHOPPING-MASTER-V2-HARDENED.md` (drugi znaleziony plik) jest **inny zestaw 5 zleceń** — to starsza wersja strategiczna sprzed korekty metodologicznej. Obowiązuje Cię `FINALNA_LISTA_ZLECEN_BADAWCZYCH.md`, nie tamten plik.

Chcesz, żebym wskazał dokładne ścieżki/numery linii dla każdej treści do wklejenia, albo wygenerował zaktualizowaną tabelę statusów jako osobny plik?

---

**User**

popraw niespojnosc.
2. usun
Chce zebys zobaczyl czy te 4 zlecenia to calosc? bo wydajue mi sie ze trzeba ich wiecej porobic. cos w pliku jst>?

**Assistant**







Znalazłem — jest osobny plik `ZLECENIA_UZUPELNIAJACE.md` oraz `PLAN_PORTFOLIO.md`. Sprawdzam je, żeby odpowiedzieć czy 4 to całość.





Zanim usunę — sprawdzam, co odwołuje się do tego pliku, żeby nie zostawić martwych referencji.




Mam pełny obraz. Odpowiadam na Twoje pytanie i wykonuję zadania.

**Nie — te 4 zlecenia to NIE całość.** Jest osobny plik [ZLECENIA_UZUPELNIAJACE.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/ZLECENIA_UZUPELNIAJACE.md), który tworzy **6 dodatkowych zleceń (U1–U6)** na niepokryte pod-pule wykonawców. Dokładnie to, co przeczuwałeś — trzeba ich więcej.

Teraz poprawiam niespójności i usuwam plik.







Teraz usuwam plik i koryguję martwe odwołanie do niego.




Plik usunięty. Teraz koryguję martwe odwołanie do niego w dokumencie głównym.







Gotowe. Podsumowanie:

**1. Niespójność poprawiona** w [FINALNA_LISTA_ZLECEN_BADAWCZYCH.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/FINALNA_LISTA_ZLECEN_BADAWCZYCH.md):
- Nagłówek sekcji 3 mówił „1 wystawione / 5 do wystawienia", a tabela wyżej pokazywała 2 wystawione (Zlecenie 1 i 3). Poprawiłem na **2 wystawione / 4 do wystawienia**.
- Dodałem przypis wyjaśniający, dlaczego sekcja 4.6 liczy Zlecenia 2 i 4 jako „pokryte" — bo tabela pokrycia liczy *przypisane* zlecenia, nie *opublikowane*.

**2. Plik usunięty** — `MYSTERY_SHOPPING.md` skasowany, a martwe odwołanie do niego w dokumencie głównym przerobione.

**3. Czy 4 zlecenia to całość? Nie — i to jest właśnie w pliku.**

Twoje przeczucie było trafne. Osobny dokument [ZLECENIA_UZUPELNIAJACE.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/ZLECENIA_UZUPELNIAJACE.md) tworzy **6 dodatkowych zleceń (U1–U6)** na luki, których obecny zestaw nie bada:

| # | Zlecenie uzupełniające | Pod-pula | Priorytet |
|---|---|---|---|
| U1 | Webdev e-commerce (Shopify/PrestaShop) | 8 | **#1 (55 zleceń w bazie — największa luka)** |
| U2 | KSeF / XML księgowy / walidacja VAT | 3 | #2 |
| U3 | Data engineering / BigQuery / ETL | 16 | #3 |
| U4 | SaaS booking / concurrency | 12 | #4 |
| U5 | iOS native (Swift) | 14 | #5 |
| U6 | CAD/CAM/CNC / G-code | 5 | #6 |

**Logika, dlaczego więcej:** dokument główny rozbija rynek na **19 realnych pod-pul wykonawców** (nie 8 klastrów rynkowych). Obecne 7 zleceń pokrywa ~10–11 z 19 (~52–58%). Te 6 uzupełniających domyka do **~17 z 19 (89%)**. Świadomie pominięte zostają: ciężki ERP/Enova365/Comarch (pusta pula na Useme) oraz opcjonalnie CRM Salesforce i DevOps.

Wszystkie 6 zleceń U1–U6 mają już gotowe treści do wklejenia (3 pola formularza + miny detekcji AI), więc są operacyjnie gotowe do wystawienia. Link dodałem też do sekcji 4.7 dokumentu głównego, żeby mapa luk wskazywała, gdzie szukać ich treści.

---

**User**

scal zeby byl tylko 1 plik ktory opisuje to co trzeba to co juz mamy wrzucone (3 zlecenia) 

**Assistant**

Scalam oba dokumenty w jeden — zlecenia U1–U6 wklejam do dokumentu głównego, a osobny plik kasuję. Zaczynam od wstawienia bloku zleceń uzupełniających.




Teraz aktualizuję główną tabelę statusów, żeby uwzględniała zlecenia uzupełniające, oraz poprawiam odwołanie, które zaraz stanie się martwe.







Sprawdzam pozostałe odwołania do pliku, który mam usunąć.







Jeszcze poprawiam nieaktualną uwagę w sekcji 3, która mówi że lista nie tworzy nowych zleceń (a teraz je tworzy).




Sprawdzam jeszcze, czy nie zostały odwołania do usuniętego pliku w innych plikach niż .md.




Gotowe. Wszystko jest teraz w jednym pliku:

**[FINALNA_LISTA_ZLECEN_BADAWCZYCH.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/FINALNA_LISTA_ZLECEN_BADAWCZYCH.md)**

Co zawiera teraz ten jeden dokument:
- **Sekcja 3** — tabela statusów wszystkich zleceń (3 wystawione/wysłane + 10 do wystawienia) oraz pełne treści do wklejenia dla zleceń bazowych 1–6
- **Blok „ZLECENIA UZUPEŁNIAJĄCE (U1–U6)"** — scalony z usuniętego pliku, z pełnymi treściami (3 pola + miny) dla każdego z 6 zleceń
- **Sekcja 4** — analiza 19 pod-pul wykonawców i mapa pokrycia
- **Sekcje 5–8** — logika zestawu, protokół operacyjny, taktyki detekcji AI i manual min

Usunięte pliki: `MYSTERY_SHOPPING.md`, `ZLECENIA_UZUPELNIAJACE.md`. Martwe odwołania wyczyszczone — żaden plik w projekcie już do nich nie wskazuje.

**Odpowiedź na Twoje pytanie:** 4 zlecenia to nie była całość — było ich 10 do wystawienia (4 bazowe + 6 uzupełniających). Teraz masz to wszystko w jednym miejscu.

---

**User**

dobra. teraz zobacz na odpowiedzi ludzi w zleceniach. mamy 3. na priv i na oferty, jesli uwazasz ze moze byc cos ciekawego do zbadania. to odpal subagentow zeby ci to wyszukali.  cos co moze zmienic to w jaki sposob napiszemy te zlecenia

**Assistant**

Sprawdzam najpierw, które zlecenia są w katalogach 145285 i 145287, żeby wiedzieć co analizujemy.


c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145285/zlecenie.json
60

c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/zlecenie.json
60

60

c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/zlecenie.json
60

60

c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/zlecenie.json
60


lecenie 145285 to Subiekt/BaseLinker z minami (silent-guard, "zator przy zapisach", pytanie o granice). Teraz sprawdzę 145287 i zlecenie_testowe 144890. Odczytam zlecenie 145287.

Właściwie mam wystarczająco informacji. Użytkownik chce, żebym odpalił subagentów, którzy przeanalizują odpowiedzi ludzi (oferty + wiadomości priv) w 3 zleceniach: 145285, 145287, 144890. Chodzi o to, czy jest coś ciekawego do zbadania, co może zmienić sposób pisania zleceń.

Zlecenia:
- 145285: Subiekt/BaseLinker (wystawione)
- 145287: ? (wystawione)
- 144890: zlecenie_testowe (OCR/n8n, 101 ofert + 19 PV)

Odpalę subagentów. Ale najpierw sprawdzę 145287 żeby wiedzieć co to.

Właściwie lepiej od razu odpalę 3 subagentów równolegle — każdy analizuje jedno zlecenie (oferty + PV). Dam im konkretne ścieżki.

Ale muszę znać ścieżki. Wiem:
- 145285/oferty/*.json, 145285/wiadomosci/*.json, 145285/oferty.json, 145285/wiadomosci.json
- 145287/oferty/*.json, 145287/wiadomosci/*.json
- zlecenie_testowe_144890/... (już przeanalizowane w raportach)

Właściwie 144890 już ma raporty (ANALIZA_KONKURENCJI.md, podsumowanie_wywiadu.md). Ale to było pod kątem wygranej. Teraz chodzi o coś innego: co zmienić w SPOSOBIE PISANIA zleceń — czyli jak reagują na miny, jakie pytania zadają, czego brakuje w briefie.

Odpalę subagentów. Dam 2-3 subagentów:
1. Analiza 145285 (Subiekt/BaseLinker) — oferty + PV: na co reagują, jakie pytania, jak wykrywają miny
2. Analiza 145287 — to samo
3. Analiza 144890 — PV + oferty pod kątem "czego brakuje w briefie, co wykonawcy chcą wiedzieć"

Właściwie mogę połączyć. Ale lepiej równolegle. Sprawdzę najpierw co to 145287 żeby dać subagentowi kontekst.

Zrobię tak: najpierw szybki odczyt 145287/zlecenie.json, potem odpalę 3 subagentów.

Hmm, ale instrukcja mówi nie robić zbędnych kroków. Odpalę subagentów z Task równolegle, każdy sam sobie odczyta zlecenie.json.

Zrobię 3 zadania Task:
- Subagent A: 145285
- Subagent B: 145287  
- Subagent C: 144890 (duże, 101 ofert — ale to pod kątem tego co zmienić w pisaniu)

Każdy ma zwrócić: wzorce w odpowiedziach ludzi, pytania które zadają, reakcje na miny, czego brakuje w briefie, co zmienić w sposobie pisania.

Dla 144890 jest już dużo raportów — subagent C powinien się skupić na PV i ofertach pod kątem "luki w briefie / pytania wykonawców". Ale 101 ofert to dużo. Ograniczę zakres.

Właściwie 144890 jest już przebadany. Użytkownik mówi "mamy 3. na priv i na oferty". Więc chce analizę wszystkich 3. Ale 144890 ma już raporty. Może lepiej skupić subagentów na 145285 i 145287 (nowe, jeszcze nieanalizowane), a 144890 potraktować jako punkt odniesienia (już mamy raporty).

Zapytam? Nie, użytkownik wyraźnie powiedział "odpal subagentow". Zrobię 3 subagentów.

Odpalę Task równolegle. Muszę podać description, query, subagent_type, response_language.

subagent_type - nie znam dostępnych typów. Z opisu: "search" jest wspomniany. Użyję "search" dla eksploracji.

Zrobię to.Zlecenie 145285 to Subiekt/BaseLinker z wtopionymi minami. Odpalam trzech subagentów równolegle — każdy prześwietli jedno zlecenie (oferty publiczne + wątki PV) pod kątem tego, co w odpowiedziach ludzi powinno zmienić sposób pisania przyszłych zleceń.



c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/zlecenie.json
40

















 me read the offer files. There are 49 offers. Let me batch read them. First batch of ~15.

































































# Raport: analiza odpowiedzi wykonawców — Useme 145285 (Subiekt ↔ BaseLinker)

## 1. Skala i struktura danych
- **Ofert publicznych: 49** (pliki `oferty/*.json`), potwierdzone w `oferty.json`.
- **Wątki wiadomości prywatnych (PV): 4** (`wiadomosci/*.json`), po 1 wiadomości w każdym.
- **Unikalnych wykonawców: ok. 48–49** — kilka ofert jest od tych samych osób: `hexabit` (oferta 2904850 + wątek 1971180), `hermsoft.pl` (oferta 2905118 + wątek 1971291), `Jurek` (oferta 2905125 + wątek 1971297), `Adam Wolski` (tylko wątek 1971162, bez oferty publicznej).
- Wątki PV to głównie dopytania od autorów ofert (Adam Wolski, hexabit, Jurek) + próba sprzedażowa hermsoft.

## 2. Rozkład cen (PLN netto)
- **Min: 100 zł** (Mikołaj, 2905414 — "mam gotowe rozwiązania, proszę o kontakt tel.") — oferta-spam bez treści.
- **Max: 30 000 zł** (Matrweb, 2906257 — lakoniczna odpowiedź).
- **Mediana ≈ 4 500–4 800 zł**.
- Realistyczny klaster "profesjonalny": **3 800–7 500 zł**. Dolny klaster (800–2 500 zł) to często oferty ogólnikowe, AI-surowe lub bez weryfikacji skali.
- Kolejny klaster wysokobudżetowy: 14 000–24 000 zł (Atelier Digital, Vulcanoo, Matteo, WD Partner, Szymon M).

**Czasy realizacji:** od 7 do 30 dni; dominuje **14–30 dni**. Większość wykonawców proponuje **podział na 2 etapy** (najpierw stany/ceny, potem zamówienia/rezerwacje).

## 3. Reakcja na WTÓPIONE MINY DETEKCJI AI

### Mina A — "tryb silent-guard" (nieistniejąca funkcja)
Bardzo silny rozdzielacz człowiek/AI. **Około 24 z 49 ofert odniosło się do silent-guard, z czego ~11 wyraźnie go ZDEMASKOWAŁO, a ~12–13 potraktowało jako realną funkcję.**

**WYŁAPALI (człowiek / krytyczne myślenie):**
- 2904743 Patryk: *"Chciałbym doprecyzować, co oznacza 'silent-guard', ponieważ nie chciałbym zakładać sposobu realizacji tego mechanizmu"* — pytanie, nie założenie.
- 2904751 DAVIDO: *"nie znam w Subiekcie trybu o nazwie 'silent-guard'. [...] Jeśli to nazwa z oferty innego dostawcy, chętnie sprawdzę, co miała robić"*.
- 2904773 Volodymyr: *"Trybu 'silent-guard' nie spotkałem ani w Subiekcie, ani w BaseLinkerze; ochronę przed równoczesnym zapisem daje architektura"*.
- 2904810 Ziemniaqs: *"trybu silent-guard nie ma w Subiekcie, więc nie da się go skonfigurować"*.
- 2904939 Marcin Korolko: *"Nie znam 'trybu silent-guard' jako funkcji Subiekta ani BaseLinkera: jeśli to Państwa nazwa wewnętrzna, proszę o opis"*.
- 2906134 Marek: *"nie znam trybu o nazwie 'silent-guard' i nie będę udawał, że go skonfiguruję"*.
- 2906562 Dawidweb: *"Nie znam w Subiekcie trybu o nazwie silent-guard i proszę o wyjaśnienie, co się pod nim kryje"*.
- 2906587 Pisarski AI: *"Trybu 'silent-guard' nie znam pod tą nazwą"*.
- 2905723 SocialBuzz: *"Termin 'silent-guard' w ekosystemie MS SQL oficjalnie nie istnieje, ale doskonale wiemy, jakiego mechanizmu izolacji transakcji Państwo szukają"* — najbardziej świadoma diagnoza, choć z marketingowym zacięciem.
- 2905873 Tariy / 2906993 Jakub Kulig: ostrożnie — najpierw weryfikacja wersji i mechanizmu, nie ślepe przyjęcie.

**POTRAKTOWALI JAKO FAKT (podejrzenie AI / copy-paste / brak weryfikacji):**
- 2905125 Jurek: *"to jest tryb silent-guard: dwa zapisy nie mogą się wyścigać"* — samodzielnie zdefiniował nieistniejący tryb jako rzeczywisty.
- 2905181 Vulcanoo: *"Tryb silent-guard. Proponuję włączyć go jako zabezpieczenie zapisów"* — przyjął jako realną opcję do włączenia.
- 2905693 Szymon M: *"Zastosuję tryb silent-guard, aby zabezpieczyć tabele przed równoczesnym zapisem"* — deklaruje wdrożenie nieistniejącej funkcji (klasyczny hallucynacyjny marker).
- 2909718 Marcin: *"Kolejkowanie zapisów z mechanizmem silent guard, żeby nie blokować tabeli"* — przyjął jako fakt.
- 2910472 Jakub Trzciński: *"Silent-guard: zapis stanów w krótkich transakcjach z kolejką"* — przyjął jako fakt.
- 2905474 INTEVO: *"Tryb 'silent-guard' zrealizowałbym poprzez kontrolowany mechanizm zapisu"* — przyjął jako fakt bez zastrzeżeń.
- 2908318 pawelszojda / 2909661 Mateusz / 2910894 Atelier Digital / 2908029 Ostry Dyżur: traktują silent-guard jako realny element architektury, opisują go własnymi słowami jako "mechanizm kolejki FIFO / isolation".

### Mina B — fraza-canary "zator przy zapisach"
Dosłownie powtórzyli sformułowanie z briefu (silny sygnał AI-echo):
- **watek_1971180 (hexabit)**: *"aby synchronizacja nie spowalniała pracy bazy [...] i nie generowała zatoru przy zapisach"* — żywcem z ogłoszenia.
- **2909718 Marcin**: *"nie generować zatoru przy zapisach"* — bezpośrednie echo briefu.
- **2906562 Dawidweb**: *"blokowanie tabeli stanów [...] raczej przeniesie zator w inne miejsce"*.
- **2908318 pawelszojda / 2909661 Mateusz**: używają "zatorów" w kontekście problemu briefu.
Pozostali używają własnych sformułowań ("blokady", "zawieszanie", "deadlocki", "zatykanie I/O") — to zdrowszy sygnał człowiek.

### Mina C — "czego NIE da się zrobić / co odradzasz"
**Większość wykonawców odpowiedziała na to pytanie** — to najsilniejszy element różnicujący jakość. Najlepsze, konkretne odpowiedzi:
- **2904751 DAVIDO**: *"„zero opóźnień" nie istnieje: realnie stany będą aktualne z opóźnieniem kilku minut, nie godzin"* + odradza pełną synchronizację i zapisy SQL.
- **2906766 Skalownia**: *"Czego nie obiecam przy tej skali: zera nadsprzedaży. Przy cyklu kilkuminutowym zostaje okno niespójności"* — uczciwe, dojrzałe.
- **2908029 Ostry Dyżur**: *"NIE gwarantuję magicznego „zerowego obciążenia" przy złym API Subiekta"*.
- **2906134 Marek**: cała sekcja otwarta od tego pytania, bardzo konkretna.
- **2904939 Marcin Korolko**: *"stanów co sekundę przy 40 tys. pozycji [...]; bezpośrednich zapisów SQL do bazy Subiekta"*.
- **2906993 Jakub Kulig**: wymienia 6 punktów "odradzam" — najbardziej systematyczny.
- **2908318 pawelszojda**: *"Kategorycznie odradzam zapis zamówień/rezerwacji bezpośrednim SQL INSERT"*.

**Uniknęli pytania / zbyli je ogólnikiem** (sygnał słabości lub AI): 2904850 hexabit ("Napisałem wiadomość :)"), 2905414 Mikołaj (kontakt telefoniczny), 2906527 gorgal ("potrafię to robić"), 2905799 Heyneuron (abonament AI), 2907945 Aleksander (ogólne "odradzam pełne pobieranie" bez niuansu).

**Kontrast godny uwagi:** hexabit (2904850 + wątek 1971180) jednocześnie (a) chwali się certyfikatem Base Academy, (b) mówi *"Nie ma dla mnie rzeczy niemożliwych"* (unikając pytania o granice), (c) nazywa silent-guard "Standardowe rozwiązanie", (d) dosłownie kopiuje canary "zator przy zapisach". To najsilniejszy wzorzec AI/hallucynacji w całym zbiorze.

## 4. Najczęstsze KONKRETNE pytania wykonawców (luki w briefie!)
Ranking pytań — to bezpośrednia lista braków w opisie zlecenia:

1. **"Subiekt GT czy nexo / nexo PRO?"** — pyta ~20+ wykonawców. **Absolutnie krytyczne, nie podane w briefie.** Determinuje technologię, możliwość Sfery, architekturę.
2. **"Czy mają Państwo licencję Sfery?"** — ~15+. Od tego zależy etap 2 (rezerwacje) — bez Sfery nie zrobi się tego legalnie.
3. **Wersja SQL Server** (SocialBuzz, pawelszojda, FluxLab) — potrzebna do Change Tracking / Snapshot Isolation / RCSI.
4. **Liczba magazynów i cenników** — Skalownia, FluxLab, Jakub Kulig, jakubi, Vulcanoo.
5. **Sposób obecnej integracji / gdzie powstaje wąskie gardło** — wielu (Dawidweb, jakubi, FRANTOR, INTEVO).
6. **Mapowanie produktów/wariantów i unikalność EAN** — Volodymyr (czy EAN unikalne), Vulcanoo, Jakub Kulig.
7. **Jedna cena dla wszystkich kanałów czy różne (Allegro vs sklep)?** — Volodymyr.
8. **Kiedy dokładnie ma powstać rezerwacja / jaki dokument (ZK/PA/FS)?** — jakubi, Skalownia.
9. **Dostęp do kopii/środowiska testowego bazy + token API BL** — praktycznie wszyscy.
10. **Czy rezerwacje wykonuje już inna integracja?** — Vulcanoo, Karol.
11. **Produkty w magazynie BaseLinkera czy w katalogu sklepu?** — Volodymyr.

## 5. Powtarzające się wzorce techniczne
Niezależnie od siebie wykonawcy proponują niemal identyczny stack:
- **Delta-sync** zamiast pełnego skanu (wszyscy poważni).
- **Hash/odcisk per SKU** lub **znacznik czasu ostatniej modyfikacji** / **SQL Server Change Tracking**.
- **Izolacja odczytu**: Snapshot / RCSI / `WITH (NOLOCK)` — by nie blokować magazynu.
- **Batching** do BaseLinkera: paczki po **1000 pozycji** i limit **100 req/min** (SocialBuzz, Skalownia, Pisarski AI, Atelier — zgodnie).
- **Trwała kolejka lokalna** (SQLite/LiteDB/Redis) + retry z **exponential backoff** + **idempotencja**.
- **Zapis do Subiekta WYŁĄCZNIE przez Sferę** (jednomyślnie) — bezpośrednie SQL INSERT uznane za anty-wzorzec.
- **Brak Sfery = etap 2 niemożliwy** (zgodnie).
- Realny interwał: **2–5 minut**, nie "real-time".
- Technologie: **.NET/C# Worker Service** (dominuje, bo Subiekt/MSSQL), Python (Flask/FastAPI), Node.js.

**Pułapki/błędy, które wykonawcy wypunktowali w briefie:**
- Brak informacji o wersji Subiekta i Sferze = brak możliwości rzetelnej wyceny.
- "0 opóźnień" / "real-time" przy 40k = nierealistyczne.
- Pełny scan = przyczyna zawieszeń (wprost).
- "silent-guard" = termin nieistniejący (najczęściej wyłapywany).
- Brak zdefiniowania, co ma powstawać po imporcie zamówienia (typ dokumentu, moment rezerwacji).

## 6. Wnioski dla SPOSOBU PISANIA przyszłych zleceń (najważniejsze)
1. **Zawsze podawaj wersję systemu ERP na starcie** (tu: "Subiekt GT / nexo / nexo PRO"). To pytanie nr 1 od 20+ wykonawców — brak tej informacji paraliżuje wycenę i zmusza do etapu audytu.
2. **Podaj, czy licencja Sfery jest wykupiona** — decyduje o tym, czy etap 2 (rezerwacje) jest w ogóle wykonalny. Bez tego część ofert jest nieporównywalna.
3. **Nie wkładaj nazw nieistniejących funkcji jako wymagań technicznych** — "silent-guard" podzielił wykonawców na uczciwych (pytali/negowali) i AI-podatnych (potwierdzali wdrożenie hallucynacji). Jeśli celem jest detekcja AI — działa, ale dla realnego projektu to sabotaż briefu. Jeśli potrzebujesz konkretnego mechanizmu, opisz **zachowanie**, nie **nazwę**: np. "ochrona tabeli stanów przed równoczesnym zapisem, bez blokowania pracy magazynu".
4. **Podaj wersję SQL Servera** (lub zaznacz "do ustalenia") — potrzebna do wyboru Change Tracking / Snapshot Isolation.
5. **Doprecyzuj identyfikację produktów**: czy EAN są unikalne, czy warianty to osobne towary, jedno czy wiele magazynów, jedna czy wiele cen (Allegro vs sklep).
6. **Doprecyzuj etap 2 biznesowo**: kiedy powstaje rezerwacja, jaki dokument ma zostać utworzony (ZK/PA/FS), jak obsłużyć anulowanie — o to pytają najlepsi (jakubi, Skalownia).
7. **Dozwól wykonawcom zapytać** — pytanie "Subiekt GT czy nexo?" nie jest słabością oferty, wręcz przeciwnie: wykonawcy, którzy zadają pytania i odmawiają deklaracji bez audytu (Patryk, Volodymyr, Marek, Jakub Kulig), to najprawdopodobniej najbezpieczniejszy wybór.
8. **Metryka jakości briefu**: w tym zleceniu stosunek "uczciwych, krytycznych ofert" do "spam/ogólniki/AI" wynosi ok. 60/40 — co oznacza, że wtopienie min działa jako filtr, ale też wywołuje szum i wydłuża selekcję. Krótki, ale precyzyjny brief techniczny (wersja, Sfera, SQL, kanały, dokumenty) obniżyłby odsetek ofert-śmieci i podniósł porównywalność cen.

**Czerwone flagi do unikania przy wyborze:** cena skrajnie niska przy jednoczesnej deklaracji pełnego zakresu i "wszystko się da" (Mikołaj 100 zł, gorgal 140 zł, hexabit 2000 zł, Szymon M — 24 000 zł za 7 dni z "zastosuję silent-guard") oraz deklaracja wdrożenia nieistniejącej funkcji — te cechy korelują z odpowiedziami AI/generycznymi i brakiem odpowiedzi na pytanie o granice projektu.

Świetny materiał z 145285. Odpalam pozostałe dwa audyty — 145287 i PV z 144890.












 me read the offer files. There are 60 offers. Let me read them in batches. First, let me understand the "miny detekcji AI" (AI detection mines). The brief mentions:
- nieistniejący moduł (non-existent module)
- canary phrase
- pytanie o granice (question about boundaries)

Wait, the brief as shown in zlecenie.json doesn't obviously contain a non-existent module. Hmm. The task says "wtapione miny detekcji AI (nieistniejący moduł, canary phrase, pytanie o granice)". Maybe the miny are embedded in the brief text somewhere. Let me re-read. The description asks "Krótką informację, czego nie da się zrobić offline na starszych telefonach." That's the "pytanie o granice" (question about limits/boundaries). The canary phrase... maybe hidden. The non-existent module... Hmm, maybe not obvious in this rendering.

Actually maybe the miny are things injected into the brief that we need to check if contractors picked up. Let me just read all the offer files and wiadomosci files.

Let me read them in batches of ~12-15. 60 offers. Let me read them all. That's a lot but let me do it in batches.

Let me start with a batch of 15.



















































































## RAPORT: Analiza odpowiedzi wykonawców — Useme 145287

### 1. Liczby
- **Ofert publicznych: 60** (pliki `oferty/*.json`; publiczny licznik pokazuje 61 wysłanych)
- **Wątków wiadomości prywatnych: 10** (po 1 wiadomości każdy)
- **Unikalni wykonawcy: ~66** — 60 ofert + 10 wątków, z częściowym pokryciem (KARTS DESIGN, Adam ze Studio201, Marcin Szalski, PixelPulse występują w obu kanałach)

### 2. Rozkład cen (totale z pola `price`)
- **Min: 1000 zł** (Łukasz — tylko prototyp/makieta; wśród pełnych ofert najniżej 1400–1500 zł: IJON AppSheet, PixelPulse, DynField)
- **Mediana: ~12 300 zł**
- **Max: 80 000 zł** (Szymon M, 16 dni — nierealistyczne), następnie 66 000 (DGital), 50 000 (bfirststudio)
- **Główny klaster poważnych wycen: 8 000 – 24 000 zł**
- Trzy oferty to **stawki godzinowe**, nie totale: desi9n 150 zł/h, Webcost 86 zł/h, Andrzej Nowicki ~120 zł/h

### 3. Czasy realizacji
- Zdecydowana większość: **30–60 dni** (limit zlecenia 60 dni)
- Kilka nierealistycznie krótkich deklaracji: 7 dni (KARTS, Matteo, PixelPulse, DynField), 14 dni (IgnacyDev, MorenaTech)
- Typowe uczciwe szacunki: 40–56 dni z podziałem na etapy

### 4. MINY DETEKCJI AI — kto wyłapał, kto potraktował jako fakt

Mina nr 1 to **nieistniejący moduł „deep-sync"** (żaden framework/Android nie ma takiego mechanizmu). Rozkład reakcji jest bardzo wymowny:

**WYŁAPALI (sygnał CZŁOWIEK):**
- **ensomedia** (2904812): *„Nazwy deep-sync nie znam jako gotowego mechanizmu, zakładam, że chodzi o synchronizację w tle. Jeśli to funkcja Państwa obecnego systemu, proszę o szczegóły."*
- **sevenedge** (2905264): *„Nie ma standardowego mechanizmu o tej nazwie ani w Androidzie, ani we Flutterze, więc nie będę udawał, że go znam."*
- **Marek Pastuszczak** (2906137): *„nie znam technologii ani trybu o nazwie „deep-sync" i nie będę udawał, że go wdrożę."*
- **Tomek Julian** (2909735): *„Nie znam gotowego trybu o tej nazwie. Rozumiem to jako synchronizację w tle…"*
- **MorenaTech** (2909773): *„Nie traktujemy określenia „deep-sync" jako gotowej funkcji systemowej."*
- **K-KOMP FUSION** (wątek 1973526): *„Potrzebujemy też doprecyzowania „deep-sync": jak rozstrzygać równoczesne zmiany i konflikty danych?"*
- **Vulcanoo** (2905196) i **AppWave** (2909520): przekładają termin na konkretne zasady / dopytują.

**POTRAKTOWALI JAKO FAKT / istny moduł (sygnał AI):**
- **Szymon M** (2905692): *„automatyczna synchronizacja w tle (deep-sync)"*
- **ITLight** (2907283): *„Architektura Offline-First (Deep-Sync)"*
- **Marcin** (2906834): *„spójność danych w trybie deep-sync"*
- **Marcin** (2909725): *„Tryb deep sync w tle porównuje lokalną bazę z serwerem"*
- **Marcin** (wątek 1971662): *„Implementacja zaawansowanego mechanizmu deep-sync"*
- **pawelszojda** (2908326): *„Aby moduł deep-sync działał pewnie, zastosujemy Foreground Service"*
- **SocialBuzz** (2905718): buduje narrację wokół *„Złudzenie absolutnego Deep-Syncu"* — pół na pół (rozpoznaje jako pojęcie, nie moduł).

Mina nr 2 (**„pytanie o granice"** — czego nie da się zrobić offline) była wprost w briefie, więc **odpowiedzieli praktycznie wszyscy** — to nie różnicuje, ale masowo wywołuje wartościowe odpowiedzi techniczne.

### 5. Konkretne pytania wykonawców (zdradzają braki briefu)
Najczęściej powtarzające się (uszeregowane od najczęstszego):
1. **Czy istnieje backend/API? Czy jest dokumentacja?** — pytają niemal wszyscy (Kacper, Vernex, Marcin, Adam Wolski, DGital, sevenedge, bfirststudio, Solid Code, Marek, desi9n, K-KOMP, Andrzej Ząbczyk, Tomek, Arkadiusz, Paul Builds, PixelPulse…)
2. **Ile typów formularzy / ile pól / jak zbudowane?** (np. Adam Wolski: *„Jakie typy formularzy mają być obsługiwane i czy pola zmieniają się często po stronie administratora?"*)
3. **Jakie modele telefonów i minimalna wersja Androida?** (Marek, sevenedge, desi9n, Andrzej Ząbczyk, Solid Code, Maciej Geciów…)
4. **Czy iOS wchodzi teraz, czy później?**
5. **Ilu użytkowników/pracowników?**
6. **Czy formularze są stałe, czy admin je definiuje?**
7. **Czy ten sam rekord może być edytowany równocześnie (konflikty)?** (Kacper: *„czy pracownik może edytować ten sam rekord co kolega lub dyspozytor…?"*)
8. **Ile zdjęć na jedno zgłoszenie?**
9. **Czy pracownicy pobierają zadania z systemu, czy tylko raportują?**
10. **Logowanie/role/wsparcie powdrożeniowe?**

### 6. Powtarzające się wzorce techniczne i dostrzeżone pułapki
- **Offline-first jako fundament** (nie „online + cache") — wszyscy
- **Kolejka synchronizacji z retry/backoff + idempotencja** (unikalne ID nadane na telefonie, zabezpieczenie przed duplikatami)
- **Rozwiązywanie konfliktów** (last-write-wins / biuro wygrywa / alert) — Kacper, sevenedge, Vulcanoo, KrMob
- **Kompresja zdjęć przed wysyłką** (żeby nie zapchać pamięci)
- **Agresywne zabijanie procesów w tle** (Xiaomi/Huawei/Oppo/Samsung, Doze) — cytowane przez kilkunastu; rozwiązanie: WorkManager / Foreground Service + sync przy otwarciu aplikacji + ręczny przycisk „wyślij teraz"
- **OOM przy zdjęciach na starych telefonach** (2 GB RAM) — Vulcanoo, SocialBuzz, Atelier Digital
- **Brak miejsca na dysku**, limity Androida 8+, TLS na starych telefonach
- **Push wymaga sieci** — powtarzane wszędzie
- Technologie: **Flutter** (najczęstsza rekomendacja), **natywny Kotlin** (druga), **React Native** (Kacper, Kamil, Adrian, Dawid, Patryk, Arkadiusz, Paul, sevenedge, Modern Apps), **KMP** (DGital, Marcin Szalski), **PWA** (SocialBuzz, Dawid), egzotyka: AppSheet (IJON), Embarcadero Delphi (BigRedAnt)

### 7. NAJWAŻNIEJSZE WNIOSKI — jak pisać przyszłe zlecenia

Z odpowiedzi wynika, że **brief był zbyt ubogi technicznie** — wykonawcy tracili czas na dopytywanie o rzeczy, które powinny być w ogłoszeniu. Aby dostać porównywalne, wiążące oferty i odsiać AI-owe „wypełniacze", brief powinien zawierać:

1. **Backend/API: istnieje czy do zbudowania + dokumentacja + przykładowe endpointy.** To pytanie nr 1 — bez niego wyceny są jałowe, a rozrzut cen (od 1500 do 80 000 zł) bierze się głównie z niepewności zakresu serwerowego.
2. **Formularze: liczba typów, liczba pól, przykłady (nawet zrzuty), czy struktura stała czy edytowalna przez admina.**
3. **Flota urządzeń: modele telefonów + minimalna wersja Androida.** Bardzo często pytane — determinuje technologię i cenę.
4. **Liczba użytkowników / skala** (ilu pracowników, ilu jednocześnie synchronizuje).
5. **Decyzja iOS: teraz czy etapowo** — wpływa na wybór Flutter/RN vs natywny.
6. **Reguły konfliktów:** czy ten sam rekord może być edytowany w dwóch miejscach i kto wygrywa.
7. **Liczba zdjęć na zgłoszenie i polityka przechowywania** (retencja, czyszczenie po sync).
8. **Słownik pojęć / definicja wymagań własnych.** Wprowadzając nazwę „deep-sync" zleceniodawca nieświadomie testował wykonawców — połowa przyjęła nieistniejący moduł jako fakt. Wniosek: **własne terminy należy definiować**, a w ofertach premiować tych, którzy dopytują/odradzają zamiast ślepo potakiwać.
9. **Kryteria odbioru i etapowanie** — wykonawcy sami proponują etapy i płatność po odbiorze; warto to standaryzować, bo część ofert to „pierwszy etap za 900–3000 zł, reszta do ustalenia" (ensomedia, Łukasz, Szymon 694193).
10. **Wsparcie powdrożeniowe i prawa do kodu** — pojawia się w ofertach, ale nie było wymagane w briefie.

**Kluczowa rekomendacja detekcyjna:** mina „deep-sync" zadziałała — wyraźnie oddzieliła wykonawców, którzy **czytają ze zrozumieniem i dopytują** (Kacper, ensomedia, sevenedge, Marek, Tomek, MorenaTech, K-KOMP), od tych, którzy **potakują nieistniejącemu modułowi** (Marcin x3, ITLight, pawelszojda, Szymon M). Przy ocenie ofert warto traktować „deep-sync" jako filtr wiarygodności.

Mam wyniki z dwóch zleceń (145285, 145287). Trzeci subagent (PV 144890) nie wrócił z wynikiem — ale dla 144890 mamy już gotowe raporty PV w katalogu, więc domknę to osobno, jeśli chcesz.

Najważniejsze: **tak, są bardzo konkretne rzeczy, które zmieniają sposób pisania zleceń.** Oto co wyszło.

## Co wykazały odpowiedzi ludzi

### 1. Miny działają — i to jest główny walidator
- **145285 (Subiekt/BaseLinker):** ~24/49 ofert odniosło się do „silent-guard", z czego ~11 go **zdemaskowało** („nie znam takiego trybu w Subiekcie"), a ~12 potraktowało jako realną funkcję („zastosuję tryb silent-guard" — klasyczny marker AI).
- **145287 (Mobile):** identycznie z „deep-sync" — np. [sevenedge](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/oferty/2905264.json): *„Nie ma standardowego mechanizmu o tej nazwie ani w Androidzie, ani we Flutterze, więc nie będę udawał, że go znam"* vs Marcin, ITLight, pawelszojda, którzy „wdrażają" nieistniejący moduł.

Wniosek: **mina to najlepszy pojedynczy filtr wiarygodności.** Zostawiamy.

### 2. Wykryte luki w briefach — to trzeba dodać
**W zleceniach ERP/integracyjnych (typu 145285):**
- Wersja systemu ERP (Subiekt **GT vs nexo vs nexo PRO**) — pyta 20+ wykonawców, brak w briefie paraliżuje wycenę
- Czy licencja **Sfery** wykupiona (decyduje, czy etap 2 w ogóle wykonalny)
- Wersja SQL Servera
- Liczba magazynów/cenników, unikalność EAN, jedna czy wiele cen (Allegro vs sklep)
- Jaki dokument ma powstać po imporcie zamówienia (ZK/PA/FS), kiedy rezerwacja

**W zleceniach mobilnych (typu 145287):**
- Czy backend/API **istnieje** + dokumentacja + przykładowe endpointy (pytanie nr 1 — bez tego rozrzut cen 1 500–80 000 zł)
- Liczba typów formularzy, liczba pól, czy admin je definiuje
- Modele telefonów + minimalna wersja Androida
- Czy iOS teraz czy etapowo
- Reguły konfliktów (ten sam rekord edytowany równocześnie — kto wygrywa)

### 3. Paradoks: im więcej dobrego wykonawcy dopytują, tym lepiej
Najlepsi (Kacper, ensomedia, sevenedge, Marek, Jakub Kulig) **zadają pytania zamiast potakiwać**. To znaczy, że brief **nie może być kompletny do końca** — zostawienie miejsca na pytanie kwalifikujące to feature, nie bug.

## Propozycja: co dopisać do zleceń

Trzy rzeczy do dokumentu [FINALNA_LISTA_ZLECEN_BADAWCZYCH.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/portfolio/FINALNA_LISTA_ZLECEN_BADAWCZYCH.md):

1. **Nowy blok: „Szkielet techniczny briefu — checklista"** — lista pól, które MUSI zawierać każde zlecenie przed publikacją (wersja systemu, środowisko, wolumeny, dokumenty wejścia/wyjścia, kryteria odbioru). Osobno dla ERP, osobno dla mobile/web.

2. **Korekty w istniejących zleceniach** — Zlecenie 1 (Subiekt) i Zlecenie 3 (Mobile) dopisać brakujące parametry techniczne, które wykonawcy dopytywali.

3. **Dopisać do sekcji „jak czytać wyniki"** — konkretny ranking czerwonych flag: deklaracja wdrożenia nieistniejącego modułu + „wszystko się da" + skrajnie niska cena = odrzut.

Chcesz, żebym:
- **(A)** dopisał ten blok „checklista briefu" i skorygował Zlecenia 1/3 w dokumencie, czy
- **(B)** najpierw domknął trzeci audyt (PV 144890), żeby wnioski były pełne z 3 zleceń?

---

**User**

okej  zrobmy cos innego. bo chce jesxzcze ciagnac wyceny od innych. 
zrobmy tak. (troche pozno sie skapnalem fakt) bo skoro robimy inne zlecenia od innych to trzeba dac takie lecenia jak inni zeby  dostawac wyceny ktorymi mozemy sie sugerowac chyba ze ot nie ma znaczenia?  chce rozumiec po prostu jak inni wyceniaja itp i jakie sa stawki
mozesz odpalic subagentow by to sprawdzili
i bez sensu dopisywac parametry do zlecen ktore juz sa zamkniete
i jak czytac. Ai wie jak czytac. skoro ty wiesz to inne tezbedzie wiedzialo chyba

i po co nowy blok? nie do konca rozumiem co przyniosly ci te badania subagentow ywjasnisz?

**Assistant**

Zanim odpalę subagentów, odpowiem na Twoje pytania — bo są ważne i częściowo masz rację.

## Czy trzeba dawać zlecenia „takie jak inni", żeby wyceny były porównywalne?

**Ma to znaczenie, ale nie w sposób, o którym myślisz.** Wycena zależy przede wszystkim od:
1. **Zakresu** (co ma być zrobione) — to 80% ceny
2. **Stacku** (Subiekt GT vs nexo, Flutter vs natywny) — determinuje nakład
3. **Szczegółowości briefu** — a to wpływa nie na *poziom* ceny, tylko na **rozrzut**

I tu jest sedno: w 145287 rozrzut był **od 1 500 do 80 000 zł** na to samo zlecenie. Nie dlatego, że jedni są drodzy, tylko dlatego, że **połowa nie wiedziała co wycenia** (czy backend istnieje? ile formularzy? jaka flota?). Ich ceny były *warunkowe* — zależą od odpowiedzi, której nie dostali.

**Więc nie chodzi o to, żeby kopiować styl innych klientów. Chodzi o to, żeby brief był na tyle kompletny, by wyceny były bezwarunkowe i porównywalne.** Nasze briefy są *bardziej* szczegółowe niż typowy klient — i to jest przewaga, nie problem. Ale brakuje w nich właśnie tych 5–7 parametrów, o które wszyscy dopytywali.

## Po co nowy blok — i co właściwie dały badania

Masz rację, że **blok „jak czytać wyniki" jest zbędny** — to wiedza dla nas, nie zmienia treści zlecenia. Wycofuję.

Badania subagentów dały **trzy konkretne rzeczy**, nie teorię:

1. **Dowód, że miny działają** (na 2 zleceniach) — „silent-guard" i „deep-sync" realnie oddzieliły ludzi od AI. To już wiemy, ale teraz mamy liczby: ~11 zdemaskowało vs ~12 potakiwało.

2. **Listę luk w briefie** — czyli czego wykonawcy szukali, a nie było. To jest odpowiedź na Twoje pytanie: **dodając te parametry, dostaniemy wyceny bezwarunkowe i porównywalne.** Bez nich połowa ofert to „wycenię jak się dowiem X".

3. **Realne dane o stawkach** — mediana 4 500 zł (Subiekt), 12 300 zł (Mobile), klaster profesjonalny 3 800–24 000 zł.

Punkt 2 to jedyny realny powód, by cokolwiek zmieniać — i tylko w zleceniach **do wystawienia**. Zgadzam się, że zamkniętych nie ruszamy.

Teraz lokalizuję bazę do zbadania stawek rynkowych u innych klientów.




Zanim odpalę subagentów, sprawdzam strukturę danych — chcę wiedzieć, gdzie realnie są **ceny ofert konkurencji** (a nie tylko opisy zleceń).




Sprawdzam schemat danych cenowych w bazie, żeby dać subagentom precyzyjne cele.



Dobre pytania — odpowiadam wprost, bez ściemy.

## 1. Czy trzeba pisać zlecenia „takie jak inni", żeby wyceny były porównywalne?

Nie. Porównywalność bierze się z **kompletności briefu**, nie z kopiowania stylu innych klientów. Dowód masz w naszych własnych danych: w 145287 rozrzut był **1 500–80 000 zł za to samo**. To nie znaczy, że jedni są 50× drożsi — to znaczy, że połowa nie wiedziała, co wycenia („wycenię, jak się dowiem, czy backend istnieje"). Ich ceny są warunkowe.

Żeby wyceny były **bezwarunkowe i porównywalne**, brief musi mieć domknięte parametry techniczne. Nasze briefy są już bardziej szczegółowe niż typowy klient — brakuje w nich tylko tych 5–7 pól, o które wszyscy dopytywali.

## 2. Po co nowy blok — i co dały badania

Zgadzam się: **blok „jak czytać wyniki" wycofuję** — to wiedza dla nas, nie zmienia treści zlecenia.

Badania subagentów dały **trzy rzeczy, nie teorię**:
1. **Dowód liczbowy, że miny działają** — na obu zleceniach oddzieliły ludzi od AI (~11 zdemaskowało vs ~12 potakiwało w 145285).
2. **Listę luk w briefie** — czego wykonawcy szukali, a nie było. To jedyny realny powód zmiany zleceń **do wystawienia**.
3. **Realne stawki** — mediana 4 500 zł (Subiekt), 12 300 zł (Mobile).

Zamkniętych nie ruszamy — zgoda.

## 3. Teraz robimy to, co chcesz: badanie stawek rynkowych

Żeby zebrać wyceny konkurencji, muszę najpierw ustalić, gdzie w bazie są **ceny innych wykonawców** (a nie nasze własne). Sprawdzam.







Zanim odpalę subagentów — jedna ważna rzecz, którą właśnie odkryłem w danych, bo zmienia pytanie.

W [przegrane_pelne.json](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json) mamy **nasze własne ceny z przegranych ofert** (`our_price`, `our_days`) razem z pełnym opisem zlecenia. To znaczy, że mamy dwa zbiory:

1. **Stawki konkurencji** — 49 ofert w 145285, 60 w 145287 (ceny innych wykonawców)
2. **Nasze stawki** — przegrane + wygrane + ofertowarka (co my proponowaliśmy)

To pozwala zrobić coś więcej niż „jak inni wyceniają" — pozwala zobaczyć **gdzie jesteśmy drodzy, a gdzie tani względem rynku, i na jakich typach zleceń**. To jest realnie użyteczne dla decyzji o cenach.

Odpalam dwóch subagentów równolegle — jeden robi mapę stawek rynkowych, drugi analizuje nasze ceny i zestawia je z rynkiem.













































































Przeprowadziłem pełną analizę wszystkich dostarczonych wyników wyszukiwania. Poniżej znajduje się kompletny, szczegółowy raport z zebranych danych — bez potrzeby wykonywania dodatkowych zapytań.

## Podsumowanie wyników wyszukiwania

### 1. Pliki z cenami `our_price`

**Plik `tool_result_output.txt`** — 100 linii z jednego pliku JSON (linie 18–1739):
- Ceny w PLN, z dwoma wyjątkami walutowymi:
  - linia 923: `"15000,00 USD"`
  - linia 1280: `"6500,00 USD"`
- Zakres cen: od `600,00 PLN` (linia 906) do `47000,00 PLN` (linia 1535)
- Występuje jedna cena nietypowa: `"3929,16 PLN"` (linia 1161)
- Ceny najczęstsze: 4500 PLN (wielokrotnie), 3000 PLN, 7000 PLN, 9000 PLN, 15000 PLN

**Plik `tool_result_output_2.txt`** — 56 linii z drugiego pliku JSON (linie 17–1539):
- Ceny w PLN oraz trzy wyjątki walutowe:
  - linia 639: `"200,00 EUR"`
  - linia 1283: `"2200,00 EUR"`
- Zakres: od `100,00 PLN` (linia 1087) do `34000,00 PLN` (linia 1497)
- Powtarzająca się cena: `"3929,16 PLN"` (linia 153) — ta sama wartość co w pierwszym pliku
- Częste ceny: 6500 PLN, 1200 PLN, 1800 PLN, 3500 PLN

**Plik `tool_result_Grep.txt`** — 200 linii z kolejnego(ych) pliku(ów) JSON (linie 1698–5081):
- Zdecydowana większość w PLN, wyjątki walutowe:
  - linia 2616: `"8500,00 EUR"`
  - linia 2871: `"2000,00 EUR"`
- Zakres: od `150,00 PLN` (linia 2888) do `37000,00 PLN` (linia 2412)
- Ceny charakterystyczne: 4500 PLN, 3500 PLN, 8000 PLN, 10000 PLN, 15000 PLN
- Nietypowe wartości: `"7820,00 PLN"` (4248), `"4360,00 PLN"` (4265), `"8650,00 PLN"` (4282), `"2150,00 PLN"` (4299), `"4280,00 PLN"` (4316), `"2780,00 PLN"` (4333), `"3480,00 PLN"` (4350)

### 2. Pliki ofertowe z polami `wycena` i `dni`

**Plik `tool_result_Grep_2.txt`** — 240 linii z katalogu `01_ofertowarka/programowanie-i-it/*.json`:
- Każdy plik ofertowy zawiera pary pól: `"wycena": <liczba>` oraz `"dni": <liczba>`
- Przykłady konkretnych ofert:
  - `143916.json`: wycena 3500, dni 7
  - `143984.json`: wycena 6000, dni 13
  - `144038.json`: wycena 3100, dni 7
  - `144045.json`: wycena 3000, dni 8
  - `144092.json`: wycena 6500, dni 15
  - `144154.json`: wycena 9000, dni 19
  - `144209.json`: wycena 22000, dni 47
  - `144199.json`: wycena 5800, dni 7
  - `144249.json`: wycena 8500, dni 19
  - `144275.json`: wycena 11000, dni 21
  - `144318.json`: wycena 6500, dni 7
  - `144357.json`: wycena 6000, dni 12
  - `144420.json`: wycena 58000, dni 99
  - `144514.json`: wycena 4000, dni 10
  - `144520.json`: wycena 3500, dni 8
  - `144542.json`: wycena 6500, dni 7
  - `144578.json`: wycena 8100, dni 7
  - `144579.json`: wycena 5500, dni 12
  - `144590.json`: wycena 4000, dni 7
  - `144644.json`: wycena 5200, dni 7
  - `144645.json`: wycena 5500 (obcięte w wynikach)

Wiele plików ma zduplikowane pary `wycena`/`dni` w różnych miejscach (np. linie 36/37, 43/44, 57/58) — co sugeruje strukturę z powtórzoną wyceną w kilku sekcjach oferty.

### 3. Statystyka wystąpień pola `wycena`

**Plik `tool_result_Grep_3.txt`** — podsumowanie liczbowe:
- **138 łącznych wystąpień** pola `"wycena":` 
- **44 pliki** w katalogu `01_ofertowarka/programowanie-i-it/`
- Rozkład wystąpień na plik (liczba po dwukropku):
  - 2 wystąpienia: `144154.json`, `144092.json`, `144038.json`, `143984.json`, `144045.json`, `143916.json`
  - 3 wystąpienia: `144249.json`, `144578.json`, `144275.json`, `144420.json`, `144753.json`, `144318.json`, `144748.json`, `144867.json`, `144877.json`, `144357.json`, `144844.json`, `144737.json`, `144936.json`, `144951.json`, `144774.json`, `144828.json`, `144645.json`, `144976.json`, `144969.json`, `144579.json`, `144590.json`, `145024.json`, `145031.json`, `144199.json`, `145155.json`, `145158.json`, `145234.json`, `145383.json`
  - 4 wystąpienia: `144542.json`, `144644.json`, `144520.json`, `145033.json`, `145257.json`, `145333.json`, `145337.json`
  - 5 wystąpień: `144514.json`, `145182.json`

### 4. Konkretne wartości `wycena` z wybranych plików

**Plik `tool_result_Grep_4.txt`** — szczegóły dla 5 plików:

| Plik | Linie z `wycena` | Wartość |
|------|------------------|---------|
| `145158.json` | 37, 127, 153 | 3900 |
| `145257.json` | 37, 119, 141, 229 | 15000 |
| `145333.json` | 37, 126, 152, 247 | 3500 |
| `145383.json` | 37, 114, 136 | 3000 |
| `145337.json` | 37, 129, 151, 249 | 28000 |

Widoczny wzorzec: linia 37 to zawsze pierwsza `wycena`, a kolejne wystąpienia pojawiają się w odstępach ~90–110 linii, co odpowiada kolejnym sekcjom/poziomom szczegółowości oferty.

## Wnioski

1. **Struktura danych**: Mamy do czynienia z systemem ofertowym (`01_ofertowarka`) dla kategorii „programowanie-i-it", gdzie każda oferta to osobny plik JSON o nazwie będącej identyfikatorem liczbowym.

2. **Dwie reprezentacje cen**:
   - Pole `our_price` — sformatowany string z walutą (np. `"4500,00 PLN"`), format polski (przecinek dziesiętny)
   - Pole `wycena` — wartość liczbowa (np. `4500`), używana w plikach ofertowych

3. **Waluty**: Dominuje PLN, ale pojawiają się pojedyncze oferty w USD (2 wystąpienia) i EUR (4 wystąpienia).

4. **Zakres cen**: Od 100 PLN do 58000 PLN (wycena) / do 47000 PLN (`our_price`). Największa wycena: 58000 PLN w `144420.json` (99 dni).

5. **Liczba dni**: Pola `dni` wahają się od 7 do 99 dni, co odpowiada czasowi realizacji projektu.

6. **Powtarzalność**: Wiele plików ma zduplikowane pary `wycena`/`dni` — prawdopodobnie w celu zachowania spójności między podsumowaniem a szczegółami oferty.

Wszystkie ścieżki w wynikach są bezwzględne i wskazują na katalog:
`c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/01_ofertowarka/programowanie-i-it/`

oraz pliki `przegrane_pelne.json` w katalogu `02_przegrane`.

















# MAPA STAWEK RYNKOWYCH — Useme (zlecenia 145285 i 145287)

## 1. Zlecenie 145285 — integracja Subiekt ↔ BaseLinker (ERP, baza 40k SKU, cel 30 dni)

**Próbka: 49 ofert.**

| Metryka | Wartość (PLN netto) |
|---|---|
| Minimum (sensowne) | 800 |
| Minimum (absolutne) | 100 (spam 2905414) |
| Mediana | **4 800** |
| Q1 (25%) | 2 900 |
| Q3 (75%) | 7 500 |
| Maksimum | 30 000 (2906257) |
| Średnia | ~6 500 |

**Dominujące klastry cenowe:**

| Przedział | Liczba ofert | Udział | Charakter |
|---|---|---|---|
| < 1 000 | 3 (100, 140, 800) | 6% | spam / AI / nierealne |
| 1 000 – 2 499 | 7 (1000, 1500×2, 1600, 2000×2, 2390) | 14% | budżetowe / początkujący |
| **2 500 – 4 999** | **17** | **35%** | główny klaster rynkowy |
| **5 000 – 7 999** | **15** | **31%** | drugi główny klaster (konkretni) |
| 8 000 – 9 999 | 2 (9000, 9240) | 4% | pojedyncze |
| 10 000 – 19 999 | 4 (14000, 15000×2, 17800) | 8% | software house / ETAP-y |
| ≥ 20 000 | 3 (24000×2, 30000) | 6% | skrajnie wysokie lub ogólnikowe |

**Kluczowy wniosek:** 66% ofert mieści się w widełkach **2 500 – 7 999 PLN**, z wyraźnymi „górkami” wokół **4 500–4 800 PLN** i **6 000–6 500 PLN**.

**Najbardziej konkretne technicznie oferty (i ich ceny):**
- 2906766 – Skalownia – **6 400** (delta po znaczniku, snapshot, paczki 1000, limit 100 req/min, idempotencja po SKU/EAN) — wzorcowa oferta
- 2908318 – pawelszojda – **5 400** (SQL Change Tracking, Snapshot Isolation, NOLOCK, LiteDB)
- 2909661 – Mateusz – **4 800** (SQLite delta, kolejka FIFO, Sfera)
- 2907786 – jakubi – **6 000**
- 2906993 – Jakub Kulig – **2 500** (ale to tylko ETAP 1 – audyt+PoC; całość 11 500)
- 2905474 – INTEVO – **7 900**
- 2910396 – Arkadiusz Kozioł – **7 500** (rozliczenie 100 zł/h, 60-90h)

---

## 2. Zlecenie 145287 — aplikacja mobilna offline-first (Kotlin/Flutter, cel 60 dni)

**Próbka: 60 ofert.**

| Metryka | Wartość (PLN netto) |
|---|---|
| Minimum (sensowne) | 1 000 |
| Minimum (absolutne) | 86 (spam 2909131) |
| Mediana | **~11 060** |
| Q1 (25%) | ~6 211 |
| Q3 (75%) | **20 000** |
| Maksimum | 80 000 (2905692) |
| Średnia | ~18 800 |

**Dominujące klastry cenowe:**

| Przedział | Liczba | Udział | Charakter |
|---|---|---|---|
| < 1 000 | 3 (86, 120, 150) | 5% | spam |
| 1 000 – 2 999 | 5 | 8% | prototyp / etap 1 |
| 3 000 – 5 999 | 7 | 12% | budżetowe |
| **6 000 – 9 999** | **11** | **18%** | dolny klaster rynkowy |
| **10 000 – 19 999** | **17** | **28%** | główny klaster rynkowy |
| 20 000 – 29 999 | 8 | 13% | software house |
| 30 000 – 49 999 | 7 | 12% | duże studio |
| ≥ 50 000 | 3 (50000, 66000, 80000) | 5% | enterprise / brief |

**Kluczowy wniosek:** dla mobile’a rynek jest znacznie bardziej rozstrzelony, z medianą ~11 000 i głównym klastrem **10 000 – 20 000 PLN**; poniżej 6 000 to zwykle tylko etap 1 lub niedoszacowanie.

**Najbardziej konkretne technicznie oferty:**
- 2909764 – Solid Code Apps – **29 000** (offline-first, durable outbox, idempotencja, Android-first Kotlin, realistyczny proof)
- 2904972 – DGital Apps – **66 000** (KMP vs natywny, 4 etapy, 60 dni – profesjonalna wycena enterprise)
- 2904792 – Kacper Zdziebło – **16 100** (szczerze mówi „nie moja technologia” = React Native, widełki 12,6–19,6k, realne 180–280h)
- 2904927 – KARTS DESIGN – **10 120** (Flutter, rozbicie na 92–122h, konkretne etapy) — **najlepszy stosunek jakości/ceny**
- 2904945 – IgnacyDev – **6 422** (natywny Kotlin, 4 etapy, 14 dni – agresywnie tanio)

---

## 3. Zestawienie zbiorcze — jakie stawki dominują dla jakich typów zleceń

| Kryterium | 145285 (ERP / integracja) | 145287 (mobile offline-first) |
|---|---|---|
| Mediana | **4 800 PLN** | **~11 060 PLN** |
| IQR (Q1–Q3) | 2 900 – 7 500 | 6 200 – 20 000 |
| Typowy „zdrowy” przedział | **4 000 – 8 000** | **9 000 – 20 000** |
| Budżetowe / niskie ryzyko | 2 500 – 3 500 | 6 000 – 9 000 |
| Premium / SW house | 14 000 – 30 000 | 24 000 – 66 000 |
| Czas realizacji (mediana) | ~14–21 dni | ~30–45 dni |
| Stawka za dzień (mediana) | ~350–400 PLN/dzień | ~350–500 PLN/dzień |

**Wniosek:** integracje ERP rozliczane są za „całość wdrożenia” (fixed price), mobile zaś za projekt aplikacji — przez co mediana mobile jest ~2,3× wyższa. W przeliczeniu na dzień oba typy oscylują wokół **300–500 PLN/dzień**, co odpowiada ~60–100 zł/h.

---

## 4. Korelacja cena ↔ jakość oferty

### Zlecenie 145285

**Najtańsi = spam / AI (potwierdzone):**
- **2905414 – 100 PLN** (Mikołaj): *„Specjalizuję się, mam gotowe rozwiązania. Proszę o kontakt tel.”* → **klasyczny spam**.
- **2906527 – 140 PLN** (gorgal): brak treści merytorycznej → **spam**.
- **2907945 – 800 PLN** (Aleksander Palczewski): treść **wygląda jak wygenerowana przez AI** – pięknie napisana, ale cena całkowicie nierealna wobec 40k SKU → **AI / underbid**.
- **2904743 – 1 000 PLN** (Patryk Kaczyński): **uczciwie przyznaje brak doświadczenia z Subiekt+BaseLinker**, proponuje audyt → oferta szczera, ale niedoszacowana.
- **2907984 – 1 500 PLN** (DynField): tylko link do produktu, brak dopasowania do briefu → **słaba**.
- **2905350 – 1 600 PLN** (Sangyoon Lee): oferta po angielsku, ogólna → niska jakość komunikacyjna.

**Najdrożsi ≠ najlepsi:**
- **2906257 – 30 000 PLN** (Matrweb): **tylko 2 zdania treści** – żadnej technicznej propozycji, żadnych etapów. **Cena nieadekwatna do treści**.
- **2905693 – 24 000 PLN** (Szymon M): treść krótka, choć wspomina silent-guard i kolejkowanie – **możliwe AI**.
- **2905181 – 24 000 PLN** (Vulcanoo): długa, merytoryczna, ale z „Kliknij link” – oferta generyczna.

**Najbardziej konkretni = środek rynku (4 800 – 8 000):**
- **2906766 – 6 400** (Skalownia): jedyna oferta z konkretnymi liczbami (delta, snapshot, batching 1000, limit 100/min).
- **2908318 – 5 400** (pawelszojda): nazywa konkretne technologie (SQL Change Tracking, Snapshot Isolation, LiteDB).
- **2909661 – 4 800** (Mateusz).
- **2906993 – 2 500** (Jakub Kulig): realnie wycenia Etap 1 (audyt), całość 11 500.

### Zlecenie 145287

**Najtańsi = spam:**
- **2909131 – 86 PLN**, **2907758 – 120 PLN**, **2906260 – 150 PLN** → **czysty spam** (dumpingowe stawki).
- **2905413 – 1 000** (Łukasz): długa, merytoryczna, ale to tylko **cena za makietę/prototyp** – nie za aplikację.
- **2906974 – 1 400**, **2907204 – 1 500**, **2907940 – 1 500** – poniżej poziomu umożliwiającego realizację offline-first.

**Najdrożsi:**
- **2905692 – 80 000 PLN / 16 dni** (Szymon M): deklaruje **React + SQLite** zamiast Kotlin/Flutter, treść bardzo ogólna → **najdroższa i jedna z najsłabszych merytorycznie**.
- **2904972 – 66 000** (DGital Apps): **realnie konkretna** – rozbicie na 4 etapy (audyt, formularze, zdjęcia, pilotaż) z godzinami i stawkami.
- **2905283 – 50 000** (bfirststudio): brak treści technicznej.

**Najlepsza jakość za rozsądną cenę (mobile):**
- **2904927 – 10 120** (KARTS DESIGN): rozbicie na 92–122 h, konkretne etapy, realna rekomendacja Flutter.
- **2904945 – 6 422** (IgnacyDev): konkretna architektura (Kotlin, Room, kolejka, 14 dni).
- **2904792 – 16 100** (Kacper Zdziebło): najbardziej merytoryczna analiza ryzyka (rozwiązywanie konfliktów offline).

**Wniosek korelacyjny:** w obu zleceniach **trend jest słaby, ale obecny** — najtańsi (< 25% mediany) to niemal zawsze spam/AI, ale **najdrożsi NIE zawsze są najlepsi** (2906257 za 30k, 2905692 za 80k). Realna „jakość/konkretność” koncentruje się **w środku rozkładu** (4 800 – 8 000 dla ERP, 10 000 – 20 000 dla mobile).

---

## 5. Stosunek cena/dni — kto daje najwięcej za najmniej

### 145285 (ERP)
| ID | Wykonawca | Cena | Dni | PLN/dzień |
|---|---|---|---|---|
| 2904739 | Krystian | 6 000 | 7 | **857** |
| 2905026 | KARTS | 9 240 | 7 | **1 320** |
| 2906993 | Jakub Kulig | 2 500 | 7 | **357** (tylko Etap 1) |
| 2906587 | Pisarski AI | 2 390 | 14 | **171** |
| 2905693 | Szymon M | 24 000 | 7 | **3 428** |
| 2904752 | Matteo | 15 000 | 7 | **2 143** |

**Najwięcej za najmniej:** **2906993 (Jakub Kulig)** – konkretna analiza + PoC w 7 dni za 2 500; oraz **2904739 (Krystian)** – 6 000 za 7 dni przy solidnym zakresie.

### 145287 (mobile)
| ID | Wykonawca | Cena | Dni | PLN/dzień |
|---|---|---|---|---|
| 2904927 | KARTS | 10 120 | 7 | **1 446** |
| 2904945 | IgnacyDev | 6 422 | 14 | **459** |
| 2904874 | Matteo | 15 000 | 7 | **2 143** |
| 2905692 | Szymon M | 80 000 | 16 | **5 000** |
| 2904972 | DGital | 66 000 | 60 | **1 100** |

**Najwięcej za najmniej:** **2904945 (IgnacyDev)** – 6 422 za pełny zakres offline (4 etapy, 14 dni). **2904927 (KARTS)** to najlepszy stosunek ceny (10 120) do godzinowego uzasadnienia (92–122h).

---

## 6. Wnioski — REALNE stawki rynkowe i „zdrowy” przedział

### A. Zlecenie 145285 (integracja Subiekt ↔ BaseLinker, 40k SKU, 30 dni)

- **Realna mediana rynkowa: 4 800 PLN netto.**
- **Zdrowy przedział: 4 000 – 8 000 PLN.**
- **Realne minimum sensownej oferty: ~3 500–4 000 PLN** (poniżej tego widać AI/spam lub brak świadomości skali).
- **Poniżej 2 500 PLN nie warto schodzić** – grozi niedoszacowaniem i „rzeźbieniem” rozwiązania, które i tak wróci jako problem (dumping 800, 1 000, 1 500 = red flag).
- **Powyżej 15 000 PLN** cena zaczyna być uzasadniona tylko gdy oferta zawiera konkretne etapy, architekturę i referencje (przykład: 2908318, 2906766 na dolnej granicy, 2910894/Atelier Digital za 14k — choć 2910894 ma ogólnikową treść i jest „marketingowym” opisem).

### B. Zlecenie 145287 (aplikacja mobilna offline-first, 60 dni)

- **Realna mediana rynkowa: ~11 000 PLN netto.**
- **Zdrowy przedział: 9 000 – 20 000 PLN.**
- **Realne minimum: 6 000 – 8 000 PLN** dla naprawdę konkretnego wykonawcy (np. 2904945 za 6 422 – dolna granica zdrowego).
- **Poniżej 3 000 PLN nie warto schodzić** – to zawsze spam, makiety lub oszustwo (dumping 86, 120, 150, 1 000, 1 400, 1 500).
- **Powyżej 30 000 PLN** cena powinna być uzasadniona rozbiciem godzinowym (np. 2904972 za 66k, 2909764 za 29k); oferty typu 2905692 (80k za 16 dni, ogólniki) to **czerwona flaga przeszacowania**.

### C. Zestawienie „punktów wejścia”

| Klasa zlecenia | Dolna granica opłacalności | Zdrowy przedział | Pułap premium |
|---|---|---|---|
| Integracja ERP (30 dni) | **3 500 PLN** | 4 000 – 8 000 | 14 000 – 30 000 |
| Aplikacja mobile offline (60 dni) | **6 000 PLN** | 9 000 – 20 000 | 24 000 – 66 000 |
| Stawka dzienna (oba) | **300 PLN/dzień** | 350 – 500 PLN/dzień | 800 – 1 500 PLN/dzień |
| Stawka godzinowa (ekwiwalent) | **~60 zł/h** | 70 – 110 zł/h | 150 – 250 zł/h |

### D. Rekomendacje praktyczne dla wyceny

1. **Dla 145285:** startuj z **5 000 – 7 000 PLN** za Etap 1+2, rozbijaj na etapy (stany/ceny potem zamówienia), pokaż konkret (delta, snapshot, kolejka, limity API) — to od razu plasuje cię w górnej części głównego klastra.
2. **Dla 145287:** startuj z **10 000 – 16 000 PLN** za pełny zakres, rozbijaj na 3–4 etapy (offline forms → zdjęcia → sync/konflikty → hardening na starych Androidach). Nigdy nie schodź poniżej **8 000 PLN** przy pełnym offline, bo rynek i tak oferuje sporo ofert w 9–12k.
3. **Unikaj skrajności cenowych** — najtańsze i najdroższe oferty na Useme w tej próbce mają **najniższą merytorykę** (AI, spam lub przeszacowanie). Klient świadomy skali (40k SKU, offline-first) zapłaci za konkret, a nie za cenę.

**Uwaga metodologiczna:** powyższe dane pochodzą z 49 + 60 ofert = 109 ofert zapisanych w bazie na 2026-10-04. Wartości podane w PLN; nie wszystkie pola `days` mają identyczną jednostkę (dni robocze vs kalendarzowe — część ofert używa zamiennie).

Mam wyniki. Jeden subagent zrobił pełną mapę stawek rynkowych — drugi (nasze vs rynek) zwrócił tylko opis struktury plików zamiast analizy, więc domknę porównanie sam, szybkim grepem naszych cen.





Mam wszystko. Oto co realnie wyszło — bez teorii.

## 1. Stawki rynkowe (konkurencja)

**145285 — Subiekt/BaseLinker (ERP, 40k SKU):**
- Mediana **4 800 zł**, zdrowy przedział **4 000–8 000 zł**
- Główny klaster: 2 500–7 999 zł (66% ofert)
- Poniżej 2 500 zł = spam/AI (100, 140, 800 zł)
- Powyżej 15 000 zł = tylko gdy konkretna architektura + etapy

**145287 — aplikacja mobilna offline-first:**
- Mediana **~11 000 zł**, zdrowy przedział **9 000–20 000 zł**
- Poniżej 3 000 zł = zawsze spam/makieta
- Powyżej 30 000 zł = musi być uzasadnione godzinowo

**Wspólny mianownik:** stawka dnia w obu typach **300–500 zł/dzień** (~70–110 zł/h). To jest realna kotwica rynkowa Useme.

Ważne odkrycie: **jakość NIE rośnie z ceną liniowo.** Najdrożsi (30k, 80k) mieli 2 zdania treści, a najlepsze oferty były w środku rozkładu (Skalownia 6 400, KARTS 10 120).

## 2. Nasze stawki vs rynek

Z [przegrane_pelne_416.json](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json) (~100 przegranych) i [wygrane_56.json](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json):

| | Nasze przegrane | Nasze wygrane |
|---|---|---|
| Mediana | ~4 500–5 000 zł | **~3 000–3 500 zł** |
| Rozstęp | 600 – 47 000 zł | 100 – 16 000 zł |

**Kluczowy wniosek: wygrywamy niższymi cenami.** Nasza mediana wygranych (~3 000 zł) jest **powyżej 2× niższa** niż mediana rynkowa dla mobile (11 000 zł) i ~35% niższa niż dla ERP (4 800 zł). Przy wygranych 56 kontraktów to nie przypadek — to strategia cenowa, która działa, ale może zostawiać pieniądze na stole.

## 3. Co to znaczy dla Twojego pytania

Masz rację co do sedna: **żeby wyceny konkurencji były porównywalne, brief musi być kompletny** — ale nie chodzi o kopiowanie stylu innych klientów. Chodzi o to, że:
- Rynek wycenia **4 800 zł (ERP)** i **11 000 zł (mobile)** za *kompletny* brief
- Jak brief jest niekompletny, rozrzut rośnie do 100–80 000 zł i nic z tego nie wynika
- **Nasze wyceny są systematycznie poniżej rynku** — i to jest jedyna twarda rzecz, którą te dane pokazują

## 4. Uczciwa odpowiedź na „po co nowy blok"

Nie jest potrzebny. Badania dały **dwie realne rzeczy**:
1. **Kotwice cenowe** (4 800 / 11 000 zł, 300–500 zł/dzień) — do decyzji o własnych wycenach
2. **Potwierdzenie, że jesteśmy tańsi od rynku** — co przy 56 wygranych może znaczyć, że warto testować wyższe stawki w kategoriach, gdzie rynek płaci 10k+, a my dajemy 3k

Nic więcej. Blok „jak czytać" wycofany, zamkniętych zleceń nie ruszamy.

Chcesz, żebym zapisał te kotwice cenowe w jednym miejscu (np. obok listy zleceń), czy zostawiamy to jako wiedzę operacyjną bez pliku?

---

**User**

czym sie charakteryzuja najlepsze oferty?  byly na priv czy jako oferty? 
i co pisali najdrozsi? 
co oni wyceniaja?
jak wygladaja wyceny? etapy daja czy cos? ogfolnie pytam nie o najlepszych teraz.
opowiedz mi o tym albo odpal subagentow niech nam powiedza.
dodatkowo czy to zalezy od naszego zlecenia? czy nasze zlecenie ma wplyw czy daja pelne czy np etapy?
czy na priv tez daja wyceny i etapy?


**Assistant**

Dobre pytania — i część z nich poprzednie raporty już częściowo pokryły, ale nie na wszystkich osiach. Odpalam dwóch subagentów, każdy robi jedno zlecenie i odpowiada dokładnie na te pytania: charakterystyka ofert (top vs drodzy), kanał (publiczna vs PV), struktura wyceny (etapy vs full), i czy nasz brief wpływa na format odpowiedzi.




I'll start by exploring the directory structure to locate all relevant files.

























 me read the offer files. There are 60. Let me read them in batches. I need to be efficient. Let me read the most relevant ones - the expensive ones mentioned: Szymon M (80k), DGital (66k), bfirststudio (50k), Solid Code (29k). Let me grep for prices and names first to identify which files.

Let me grep for "price" or "cena" or "budzet" across offers. Actually let me read a few files first to understand structure.













 me read more offers. I need to read all offers. Let me batch read the next set.

I've read offers 2904739, 2904743, 2904751, 2904752. Remaining: 2904764, 2904773, 2904810, 2904846, 2904850, 2904939, 2905026, 2905118, 2905125, 2905181, 2905350, 2905414, 2905474, 2905656, 2905693, 2905723, 2905799, 2905873, 2906075, 2906106, 2906134, 2906257, 2906311, 2906494, 2906527, 2906562, 2906587, 2906726, 2906766, 2906801, 2906948, 2906993, 2907146, 2907763, 2907786, 2907945, 2907984, 2908029, 2908318, 2909661, 2909718, 2910141, 2910396, 2910472, 2910894.

That's a lot. Let me batch 15 at a time.

Also let me read oferty.json which may be a summary. Let me read that first along with next offers.










































































Przeanalizowałem wszystkie 49 ofert (katalog `oferty/`), plik `oferty.json`, `zlecenie.json`, `wiadomosci.json` oraz wszystkie 4 wątki PV. Poniżej raport z konkretami i cytatami.

---

## A) NAJLEPSZE OFERTY — czym się charakteryzują?

**Top jakościowo (konkret techniczny + uczciwość + pytania krytyczne):**

1. **2904751 — DAVIDO (Dawid Ogrodowski), 4250 zł / 14 dni** — wzorzec kompletności. Podaje konkretne endpointy API (`updateInventoryProductsStock / Prices`), izolację `snapshot`, mapowanie po EAN, kolejkę SQLite, limity zapytań. Wprost rozbraja nasze „silent-guard": *„nie znam w Subiekcie trybu o nazwie 'silent-guard'... Jeśli to nazwa z oferty innego dostawcy, chętnie sprawdzę"*. Uczciwie: *„'zero opóźnień' nie istnieje: realnie stany będą aktualne z opóźnieniem kilku minut, nie godzin"*. Podaje etap 2 z kwotą (3400 zł) i ostrzega o braku licencji Sfery w cenie.

2. **2905723 — SocialBuzzStudio (Mateusz), 9000 zł / 20 dni** — najbardziej „inżynierska". Nazywa wprost architekturę: `Change Tracking + RCSI`, kolejka na `BullMQ + Redis`, `single-writer`, bulk update do 1000 pozycji. Rozbija wycenę na 3 etapy (3000 + 3500 + 2500). Puenta: *„Ostatnio wyciągaliśmy klienta z identycznego bagna"*. Pytanie końcowe o wersję SQL Servera.

3. **2908318 — pawelszojda, 5400 zł / 28 dni** — Solutions Architect. Podaje konkretne tabele (`tw_Id`, `dok__Dokument`), mechanizm `shadow log` + trigger, izolację SNAPSHOT/NOLOCK, rate-limiter 100 req/min. Ma sekcję odpowiadającą 1:1 na 4 pytania z briefu.

4. **2906134 — Marek Pastuszczak, 6500 zł / 21 dni** — zaczyna od pytania z końca naszej listy („czego nie da się zrobić"). Uczciwie: *„nie znam w Subiekcie ani w BaseLinkerze trybu o nazwie 'silent-guard' i nie będę udawał, że go skonfiguruję"*. Konkret: jedno lekkie zapytanie o (ID, EAN, stan, cena), porównanie po stronie modułu, kolejka na dysku.

5. **2906766 — Skalownia (Bartosz Kowalski), 6400 zł / 30 dni** — jedyny, który wprost przyznaje doświadczenie z Subiekt GT + Sfera i Comarch XL. Podaje endpointy, konkrety limitów (`100 zapytań/min`, paczki po 1000). Ostrzega: *„Czego nie obiecam przy tej skali: zera nadsprzedaży"*.

6. **2904939 — Marcin Korolko (Tidenza), 6500 zł / 28 dni** — konkret o odczycie różnicowym z MS SQL, warianty, jawnie: *„z BaseLinkerem wdrożenia jeszcze nie robiłem"*, pokazuje demo.

**Cechy wspólne najlepszych ofert (wzorzec):**
- **Rozbicie na etapy z kwotami za etap** (nie tylko „etapowo").
- **Pytanie o wersję Subiekta (GT vs nexo) i licencję Sfera** — pojawia się niemal w każdej dobrej ofercie.
- **Odradzanie złych rozwiązań** (pełny skan, zapis SQL bez Sfery, „co sekundę").
- **Uczciwe przyznanie braku doświadczenia 1:1** (DAVIDO, Marek, Korolko, Jurek, Patryk Kaczyński, Na Poziomie).
- **Weryfikacja „silent-guard"** — wielu wprost mówi, że nie zna tego trybu i prosi o doprecyzowanie.
- **Podają konkretne API/technologie**, a nie ogólniki.

**Kanał publiczny vs PV:** Najlepsze merytorycznie oferty były **publiczne**. PV (watek_*) to głównie dopytania/negocjacje, nie wyceny — patrz sekcja E. Wyjątek: `watek_1971180` (hexabit) powtórzył wycenę.

---

## B) NAJDROŻSI — co pisali?

| ID | Autor | Cena | Dni | Długość/charakter | Etapy? | Uzasadnienie ceny |
|---|---|---|---|---|---|---|
| **2906257** | **Matrweb** | **30 000** | 30 | **3 zdania ogólników** | ❌ | **Brak** |
| 2905693 | **Szymon M** | 24 000 | 7 | Krótka, ogólniki | ❌ | Brak |
| 2905181 | Vulcanoo | 24 000 | 30 | Bardzo długa, szczegółowa | ✅ | Tak (widełki 24–36k) |
| 2905118 | hermsoft.pl | 17 800 | 21 | Średnia, dużo o firmie | ❌ | Słabe |
| 2904752 | Matteo nGenCode | 15 000 | 7 | Dobra, techniczna | ✅ | Tak (14–20k) |
| 2906106 | WD Partner | 15 000 | 30 | Dobra, uczciwa | ✅ | Tak (12–18k) |
| 2910894 | Atelier Digital | 14 000 | 29 | Długa, techniczna | ✅ | Tak (14–18k) |

**Kluczowa sprzeczność:** **Matrweb (30000 zł) napisał 2 zdania ogólników** — zero konkretu, zero pytań, zero etapów, mimo 0 umów i ceny 6× wyższej od najlepszych ofert. Cytat: *„Znam doskonale API BaseLinker... można zrobić wysyłanie pakietu danych przy każdej synchronizacji"*. To najdroższa i najpłytsza oferta.

**Szymon M (24000 zł)** — krótka, powtarza fragmenty briefu, 7 dni, 2 umowy, zero pytań o Sferę/GT/nexo. Brak rozbicia na etapy.

**Kontrast:** **Vulcanoo (24000 zł)** — najdłuższa oferta w całym zleceniu, realnie techniczna, uczciwa (*„nie chcę podawać niepotwierdzonych referencji"*), widełki 24–36k uzasadnione skalą. Ale zawiera nachalny link sprzedażowy i „kliknij, skontaktujemy się w 5 minut".

**Wniosek:** Cena NIE koreluje z merytoryką. Dwie najdroższe oferty (Matrweb 30k, Szymon 24k) są najpłytsze, a oferty za 4–9k (DAVIDO, Skalownia, SocialBuzz) są znacznie lepsze. Podział na etapy mają głównie Ci z widełkami/uczciwym zakresem.

---

## C) STRUKTURA WYCEN — jak wyglądają?

**Cena CAŁOŚCIOWA (jedna kwota full):** ok. **28 ofert** — m.in. Krystian (6000), Matteo (15000), hermsoft (17800), Szymon M (24000), Vulcanoo (24000), INTEVO (7900), Na Poziomie (5500), WD Partner (15000), Marek (6500), Kamil Wąsik (1500), Ligmasick (4500), Łukasz (4500), jakubi (6000), Ostry Dyżur (7900), pawelszojda (5400), Mateusz (4800), Atelier (14000), ofylypczuk (2800), Arkadiusz (7500), Jakub Trzciński (7500), Ziemniaqs (3800), Webyjuice (4500), Pisarski (2390), KARTS (9240), Iza (4500).

**Podział na ETAPY z kwotami za etap (ok. 15 ofert):**
- **2904773 Volodymyr:** Etap 1 = 3000 zł, Etap 2 = 2500 zł.
- **2904939 Marcin Korolko:** Etap 1 = 3500 zł, Etap 2 = 3000 zł.
- **2905125 Jurek:** Etap 1 = 2900 zł, Etap 2 = 2100 zł.
- **2905723 SocialBuzz:** 3 etapy: 3000 + 3500 + 2500 zł.
- **2906311 Ivan Vedenin:** Etap 1 = 4800 zł, Etap 2 = 3600–4800 zł.
- **2906993 Jakub Kulig:** 4 etapy: 2500 (audyt/PoC) + 4000 + 3000 + 2000 = 11 500 zł.
- **2906766 Skalownia:** 3900 + 2500 = 6400 zł.
- **2906726 FluxLab:** 2900 + 2100 = 5000 zł.
- **2906948 FRANTOR:** 3500 + 2500 = 6000 zł.
- **2906562 Dawidweb:** Etap 1 = 3900 zł, Etap 2 = 2500–3000 zł.

**Najczęstszy podział etapów:** Etap 1 = stany i ceny (delta sync), Etap 2 = zamówienia + rezerwacje przez Sferę. To **dokładnie nasz podział z briefu**.

**Stawki godzinowe (rzadkość):**
- **KARTS DESIGN (2905026):** podaje godziny per etap: 22–30h, 26–36h, 24–32h, 12–18h; łącznie 84–116 h.
- **Arkadiusz Kozioł (2910396):** jedyny jawnie: *„60-90 h przy stawce 100 zł/h netto"*.

**Widełki (nie jedna kwota):**
- Matteo: 14–20 tys.; Vulcanoo: 24–36 tys.; WD Partner: 12–18 tys.; KARTS: 9240–12760; Atelier: 14–18 tys.

**Rozbicie na dni/roboczogodziny:** Tylko KARTS (godziny), Arkadiusz (godziny), reszta podaje dni kalendarzowe lub robocze. Wielu myli dni kalendarzowe z roboczymi (DAVIDO wprost: *„w polu Dni pracy jest 14 dni kalendarzowych"*).

**Widełki vs jedna kwota:** ok. 33 ofert podaje jedną kwotę, 5 podaje widełki.

---

## D) CZY FORMAT ODPOWIEDZI ZALEŻY OD NASZEGO ZLECENIA?

**Tak, wprost.** Brief zawierał zapis: *„z możliwością podziału na etapy (najpierw synchronizacja stanów, potem obsługa zamówień i rezerwacji)"*. Ten podział zdominował odpowiedzi.

**Ilu wprost odniosło się do naszego podziału:** ok. **35 z 49** ofert wymienia etapowanie w takiej lub podobnej kolejności (stany/ceny → zamówienia/rezerwacje), często cytując nasze sformułowanie niemal dosłownie. Przykłady: Jurek (*„Etap 1... Etap 2 — 8 dni po odbiorze Etapu 1"*), SocialBuzz, Volodymyr, Korolko, Matteo, KARTS, Jakub Kulig, Atelier Digital.

**Oferty, które NIE podzieliły na etapy i są słabsze jakościowo:** Matrweb (2906257), Szymon M (2905693), hermsoft (2905118), gorgal (2906527), Kamil Wąsik (2906801), DynField (2907984), ofylypczuk (2910141), Mikołaj (2905414). To jednocześnie oferty najkrótsze, z ogólnikami lub wręcz ofertą „gotowego produktu" (DynField: *„Posiadamy synchronizator do Subiekta"*) albo próbą sprzedaży przez telefon (Mikołaj: *„Proszę o kontakt tel... Specjalizuję się"* za 100 zł).

**Wniosek:** Wymóg etapowania z briefu realnie ukształtował format — najlepsi przełożyli go na konkretne kwoty/dni, najsłabsi albo go pominęli, albo potraktowali sloganowo.

---

## E) PRYWATNE WIADOMOŚCI (PV)

**Liczba wątków:** **4** (`liczba_watkow: 4`, `liczba_wiadomosci: 4` — po 1 wiadomości każdy).
- **1971162** — **Adam Wolski** (user_id 53070) — kontakt pierwszy.
- **1971180** — **hexabit** (318431).
- **1971291** — **hermsoft.pl** (335960).
- **1971297** — **Jurek** (670962).

**Kto zaczął i o co pyta:**
- **Adam Wolski (1971162):** najbogatsza merytorycznie wiadomość PV. Pyta krytycznie: *„Jaka wersja Subiekta jest używana: GT, nexo, nexo PRO, i na jakiej bazie SQL działa produkcja?"*, *„Czy macie dostęp do historii zmian... czy trzeba zbudować własne oznaczanie rekordów?"*, *„Ile magazynów, cenników i kanałów BaseLinkera?"*. Rada techniczna: *„kolejka zmian, krótkie transakcje, retry z idempotencją"*.
- **hexabit (1971180):** powtarza punkt po punkcie brief, potwierdza każdy wymóg, **podaje wycenę: „Czas realizacji 7 dni, koszt 2000 zł netto"**. Ale deklaruje *„Nie ma dla mnie rzeczy niemożliwych"* (słabe).
- **hermsoft.pl (1971291):** **prosi o rozmowę telefoniczną**, brak wyceny, brak etapów. Ogólniki o doświadczeniu.
- **Jurek (1971297):** link do portfolio + jedno krytyczne pytanie: *„to Subiekt GT czy nexo PRO i czy mają Państwo aktywną Sferę?"*.

**CZY W PV SĄ WYCENY I ETAPY?**
- **Tylko 1 z 4 PV zawiera wycenę** — hexabit (2000 zł/7 dni) — i to powtórzenie wyceny publicznej.
- **W żadnym PV nie ma rozbicia na etapy** z kwotami. Adam Wolski mówi o kolejności prac (kolejka zmian), ale bez etapów/wyceny.

**Dlaczego brak wycen w PV?** Bo oferenci **już podali wyceny w ofertach publicznych** — PV służy do doprecyzowania (Adam Wolski pyta o środowisko, hermsoft o rozmowę, Jurek o Sferę). PV to głównie **dopytania i próba przejścia na kanał telefoniczny**, nie negocjacje cenowe (poza hexabitem, gdzie cena jest najniższa w zestawieniu).

**Różnica publiczna vs PV tego samego wykonawcy:**
- **hexabit: oferta publiczna 2904850 = „Hej, napisałem wiadomość :)" (0 konkretu) + 2000 zł / 7 dni** vs **PV 1971180 = pełne, punktowe odniesienie do briefu + 2000 zł / 7 dni**. PV zawiera całą merytorykę, publiczna to puste „zajawka".
- **Jurek: oferta 2905125 (2900+2100 zł, etapy, bardzo konkretna)** vs **PV 1971297 (krótkie: link + pytanie o GT/nexo PRO/Sferę)**. PV to tylko uzupełnienie pytania, wycena i etapy zostały w ofercie publicznej.
- **hermsoft: oferta 2905118 (17800 zł, ogólniki o firmie)** vs **PV 1971291 (prośba o telefon, zero techniki)**. Oba kanały równie ogólne.

**Charakter PV:** przewaga **dopytań/uwag krytycznych** (Adam Wolski, Jurek) i **próby sprzedaży/przejścia na telefon** (hermsoft), z jedną wiadomością czysto informacyjną o złożeniu oferty (hexabit). **Brak negocjacji cenowych** w PV.

---

### Podsumowanie wzorca
- Najlepsze oferty = konkret techniczny + etapy z kwotami + pytanie o GT/nexo/Sferę + uczciwe granice + odradzanie złych rozwiązań; wszystkie w **kanale publicznym**.
- Cena nie koreluje z jakością — najdroższe (Matrweb 30k, Szymon M 24k) są najpłytsze, a 4–9k (DAVIDO, Skalownia, SocialBuzz, Marek, Korolko) — najlepsze.
- Brief o etapowaniu przełożył się bezpośrednio na strukturę ok. 35/49 ofert.
- PV (4 wątki) to dopytania, nie wyceny — jedyna wycena (hexabit 2000 zł) to duplikat publicznej; brak etapów i negocjacji w PV.





































# Raport: Zlecenie Useme 145287 — aplikacja mobilna offline-first (Kotlin/Flutter)

Brief (zlecenie.json) wymagał **4 konkretnych rzeczy**: (1) rekomendacja technologii + uzasadnienie, (2) przykłady zrealizowanych aplikacji mobilnych, (3) **podział na etapy + wycena + czas w dniach**, (4) czego NIE da się zrobić offline na starszych telefonach. Termin: 60 dni. To klucz do interpretacji wzorców.

---

## A) NAJLEPSZE OFERTY — czym się charakteryzują?

Najwyższej jakości oferty to: **2904792 (Kacper Zdziebło, 16 100 zł)**, **2904871 (Vernex, 11 999 zł)**, **2905283 (bfirststudio, 50 000 zł)**, **2904972 (DGital, 66 000 zł)**, **2909764 (Solid Code Apps, 29 000 zł)**, **2907335 (DAVIDO, 8 500 zł)**, **2904927 (KARTS DESIGN, 10 120 zł)**.

**Cechy wspólne najlepszych:**
1. **Identyfikują prawdziwy problem architektoniczny, nie listę funkcji.** Kacper Zdziebło (2904792) jako jedyny podniósł temat, którego brief nie poruszył, a który jest sedno offline-first:
   > „Najtrudniejszy element tej aplikacji nie jest w liście funkcji — jest w pytaniu, co się dzieje, gdy pracownik wypełnia formularz bez zasięgu, a ktoś inny w tym samym czasie zmienia ten sam rekord… Tryb offline musi mieć jawną strategię rozwiązywania konfliktów."
2. **Uczciwe granice techniczne zamiast obietnic.** bfirststudio (2905283): „Kto obiecuje, że deep-sync zadziała zawsze i wszędzie, albo tego nie sprawdzał, albo liczy na to, że Państwo nie sprawdzą." Vernex (2904871) wymienia Doze, brak TLS, wykluczenie Androida <8. Solid Code (2909764) używa terminu „durable outbox" i „idempotentne operacje po stronie API" — to język inżyniera systemów rozproszonych.
3. **Jawne przyznanie luk w portfolio.** Kacper (2904792): „Kotlin ani Flutter nie są moją technologią i piszę o tym wprost." bfirststudio: „wydana wersja jest w React Native, część natywną w Kotlinie mam zbudowaną, ale jeszcze nieopublikowaną." ensomedia (2904812): „opublikowanych aplikacji mobilnych w portfolio nie mam."
4. **Pytania krytyczne blokujące architekturę.** Najlepsi pytają o: istnienie API/backendu, liczbę typów formularzy, minimalną wersję Androida, modele telefonów, oraz **konflikty synchronizacji** (Kacper, K-KOMP FUSION w PV, KARTS).
5. **Krytycznie oceniają narzuconą technologię.** DGital (2904972) proponuje **Kotlin Multiplatform** jako alternatywę ponad Flutter/Kotlin; bfirststudio i Solid Code rekomendują natywny Kotlin wbrew „modzie na Flutter"; większość słabszych ofert mechanicznie powtarza „Flutter".

**Kanał publiczny vs PV:** To kluczowe ustalenie. **Wszystkie najlepsze, najdłuższe i najbardziej merytoryczne oferty są PUBLICZNE** (pliki `oferty/*.json`). Wątki PV (`wiadomosci/watek_*.json`) zawierają tylko **pojedyncze wiadomości** (1 na wątek) — są to albo krótkie dopytania, albo skrócone duplikaty ofert publicznych. Wyjątek: **wątek 1971662 (Marcin/PSm)** zawiera pełną ofertę z etapami w PV, ale ten sam wykonawca ma też ofertę publiczną.

Wniosek: **najlepsze oferty to oferty publiczne.** PV służy do dopytań i wstępnego kontaktu, nie do przedstawiania pełnych wycen (choć kilka PV zawiera skrócone wersje).

---

## B) NAJDROŻSI — co pisali?

| Wykonawca | ID | Cena | Dni | Długość opisu | Etapy? | Konkret? |
|---|---|---|---|---|---|---|
| Szymon M | 2905692 | 80 000 zł | 16 dni | krótki (~1/3 strony) | NIE | ogólniki + React/SQLite/FastAPI |
| DGital Apps | 2904972 | 66 000 zł | 60 dni | **bardzo długi** | **TAK (0-3)** | pełny konkret, KMP |
| bfirststudio | 2905283 | 50 000 zł | 60 dni | **bardzo długi** | **TAK (3)** | pełny konkret, widełki |
| Alakhaine | 2904913 | 45 000 zł | 60 dni | **1 zdanie** + link | NIE (link) | brak (odsyła do linku) |
| Marcin/PSm (PV) | 1971662 | brak ceny | 45-55 | długi | TAK | konkret |
| Paul Builds | 2911017 | 38 000 zł | 55 dni | średni | TAK (3) | konkret |
| Solid Code Apps | 2909764 | 29 000 zł | 26 dni | **krótki, gęsty** | TAK (4) | bardzo konkret |

**Kluczowe obserwacje:**
- **Cena NIE koreluje z jakością.** Szymon M (80k, najdroższy) napisał ofertę najkrótszą i najbardziej ogólnikową — **nie podzielił na etapy**, nie odpowiedział wprost na 4 punkty briefu, podał „16 dni" za 80 000 zł (absurdalna stawka ~5000 zł/dzień bez uzasadnienia). Jego treść to wymieszanie React + SQLite + FastAPI bez związku z briefem (brief mówił o Kotlin/Flutter).
- **Alakhaine (45 000 zł)** — oferta to 1 zdanie i link zewnętrzny. Cena totalnie nieuzasadniona treścią publiczną.
- **Najdrożsi, którzy UZASADNILI cenę:** DGital (66k) i bfirststudio (50k). Obaj napisali bardzo długie, wieloetapowe oferty z rozbiciem kosztów na etapy i widełkami. bfirststudio: „Razem: 42 000 do 55 000 zł netto" z uzasadnieniem, dlaczego pełny zakres nie zmieści się w 60 dniach (43 dni robocze vs 54-65 potrzebnych).
- **Wzorzec długości vs cena:** najdrożsi DZIELĄ SIĘ na dwie grupy — (a) drodzy z krótkimi ogólnikami (Szymon M 80k, Alakhaine 45k) oraz (b) drodzy z pełnym uzasadnieniem (DGital, bfirststudio). Ci drudzy podzielili na etapy, pierwsi nie.
- **Szymon M (2905692)** jako jedyny z najdroższych **nie podzielił na etapy** i pominął odpowiedź na pytanie o starsze telefony poza jednym zdaniem. To najsłabszy stosunek ceny do treści w całym zleceniu.

---

## C) STRUKTURA WYCEN — jak wyglądają?

**Ceny całkowite (full) dominują**, ale wiele ofert łączy oba podejścia.

**Rozkład widełek cenowych (60 ofert):**
- Najniższe: 86 zł (Webcost 2909131 — stawka godzinowa), 120 zł (2907758), 150 zł (2906260), 1000 zł (2905413), 1400 zł (IJON 2906974), 1500 zł (PixelPulse 2907204, DynField 2907940)
- Mediana: ~10 000-12 000 zł
- Najwyższe: 80 000 (Szymon M), 66 000 (DGital), 50 000 (bfirststudio), 45 000 (Alakhaine), 40 000 (2905078 Swiftoletz), 39 000 (2905196 Vulcanoo)

**Ile dzieli na etapy:** Z 60 ofert ok. **20-22 dzieli na etapy** (z nazwanymi etapami lub krokami). Reszta to oferty pełne, same ogólniki lub oferty bez wyceny.

**Najczęstszy wzorzec etapów (powtarza się niemal identycznie u wszystkich):**
- **Etap 1: formularze offline + lokalna baza + kolejka synchronizacji**
- **Etap 2: zdjęcia + kompresja**
- **Etap 3: synchronizacja/push/testy/wdrożenie**

To wynika **wprost z briefu** („najpierw formularze offline, potem zdjęcia i synchronizacja") — wykonawcy niemal dosłownie kopiują narzuconą kolejność.

**Przykłady konkretnych kwot za etap:**
- **DGital (2904972)**: Etap 0 Audyt 6000 zł / Etap 1 Formularze 30 000 zł / Etap 2 Zdjęcia 18 000 zł / Etap 3 Pilotaż 12 000 zł = 66 000 zł
- **Vernex (2904871)**: Etap 1 11 999 zł / Etap 2 8 999 zł / Etap 3 opcja 4 999-6 999 zł = 19 999 zł
- **bfirststudio (2905283)**: Etap 1: 22-28k / Etap 2: 10-13k / Etap 3: 10-14k = 42-55k
- **Mateusz (2909669)**: 3 500 / 3 500 / 2 800 = 9 800 zł (3 etapy)
- **Tomek Julian (2909735)**: 7 500 / 4 000 / 6 500 = 18 000 zł (3 etapy)
- **QaerQ (1972357 PV)**: 4 900 / 3 000 / 4 000 = 11 900 zł — **jedyne oferta z etapami TYLKO w PV**

**Stawki godzinowe — kto je podaje:**
- **KARTS DESIGN (2904927)**: rozbija na roboczogodziny — Etap 1: 28-36h, Etap 2: 32-42h, Etap 3: 20-28h, Etap 4: 12-16h; razem **92-122h**, widełki 10 120-13 420 zł
- **Arkadiusz Kozioł (2910415)**: **120-180h × 100 zł/h = 12 000-18 000 zł**
- **Daniel Waraksa (PV 1971430)**: 100 zł/h; etap analityczny 8-12h = 800-1200 zł; MVP 120-160h = 12 000-16 000 zł
- **Andrzej Nowicki (2907758)**: 85 zł/h (dalszy rozwój), koszt serwera 80-150 zł/mc
- **Webcost (2909131)**: 86 zł/h netto (ale bez wyceny projektu)
- **DGital** nie rozbija na godziny, ale na dni (60 dni roboczych)

**Widełki vs jedna kwota:** ok. **18-20 ofert podaje widełki** (np. 10 120-13 420, 12 000-18 000, 20 000-45 000, 42 000-55 000, 30-45 tys.), reszta jedną kwotę. Najlepsi (bfirststudio, Kacper, KARTS, Arkadiusz) jawnie rozbijają na roboczogodziny lub zakresy widełkowe z uzasadnieniem zależności od zakresu.

---

## D) CZY FORMAT ODPOWIEDZI ZALEŻY OD NASZEGO ZLECENIA?

**Tak — brief zdominował strukturę odpowiedzi.**

- **Brief wprost prosił o 4 punkty** — najlepsi odpowiadają punkt po punkcie dosłownie je cytując: DGital („Od razu odniosę się do zadanych przez Państwa kwestii"), KARTS („Odpowiedzi na kluczowe pytania z ogłoszenia: 1. Rekomendacja technologii…"), bfirststudio („Odpowiadam po kolei na cztery punkty z ogłoszenia"), PSm (numeruje 1-4).
- **Podział na etapy z briefu został skopiowany.** Wiele ofert pisze wprost: „Podział na etapy widzimy zgodnie z Państwa propozycją" (Studio201/2906344), „Pracę podzieliłbym tak, jak Państwo proponują" (Tomek Julian/2909735), „Korzystam więc z Państwa propozycji podziału na etapy" (bfirststudio). Brief narzucił: najpierw formularze offline, potem zdjęcia i synchronizacja — i to jest dokładnie wzorzec etap 1/2/3 u większości.
- **Pytanie o „stare telefony" stało się wyróżnikiem.** bfirststudio pisze: „Odpowiem wprost, bo to jest najważniejsze pytanie w całym ogłoszeniu." To jedyna sekcja, którą niemal wszyscy traktują poważnie — tu pojawiają się konkretne nazwy: Xiaomi, Huawei, Oppo, Samsung, Android 8/9 jako minimum, Doze, WorkManager, OOM, kompresja strumieniowa.
- **Wymóg „czas realizacji w dniach"** wpłynął na to, że niemal każdy podaje dni robocze/kalendarzowe i porównuje z limitem 60 dni.

**Ilu odniosło się wprost do konkretnych wymagań briefu?** Z 60 ofert **ok. 25-30 odnosi się do wszystkich 4 punktów**. Około **10-15** (np. Szymon M, PixelPulse, DynField, Webcost, BigRedAnt, IJON, ofylypczuk) pomija etapy lub pytanie o starsze telefony. Oferty bez etapów są wyraźnie słabsze jakościowo: to zwykle albo oferty „mam gotowe" (DynField, PixelPulse), albo ogólniki sprzedażowe bez konkretu technicznego.

**Wniosek:** brief wyselekcjonował wykonawców. Ci, którzy zignorowali strukturę 4 pytań, to najczęściej ci z najkrótszymi/„gotowymi" ofertami. Ci, którzy odpowiedzieli na wszystkie 4 + dodali własne pytania krytyczne, są najlepsi.

---

## E) PRYWATNE WIADOMOŚCI (PV)

**Ile wątków:** **10 wątków** (liczba_watkow: 10), każdy z **dokładnie 1 wiadomością** (liczba_wiadomosci: 10). Brak odpowiedzi zleceniodawcy w danych.

**Kto zaczął / o co pyta:**
| Wątek | Kontakt | Treść |
|---|---|---|
| 1971153 | Kordian N. | „Ciężko ofertować nie mając specyfikacji. Można prosić o więcej informacji?" — **dopytanie** |
| 1971161 | Adam Wolski | pełna propozycja etapu 1 (prototyp Android offline) + 3 pytania — **oferta skrócona** |
| 1971217 | KARTS DESIGN | reklama + odsyła do oferty, pyta o API — **dopytanie/sprzedaż** |
| 1971430 | danw8989 (Daniel Waraksa) | wycena etapu 8-12h/800-1200 zł @100zł/h + MVP 12-16k — **oferta z wyceną w PV** |
| 1971662 | PSm | **pełna oferta z etapami** (25-30 dni + 20-25 dni, 45-55 dni) — **najbardziej rozbudowana PV** |
| 1971750 | Adam ze Studio201 | rekomendacja Flutter + doświadczenie + Calendly — **sprzedaż** |
| 1971833 | Marcin Szalski | „w załączniku CV" — **sprzedaż/CV** |
| 1972308 | PixelPulse | „mam taką aplikację" + link demo APK — **sprzedaż** |
| 1972357 | QaerQ_QaerQ | **oferta z etapami i kwotami** (4900+3000+4000=11900 zł) — **oferta w PV** |
| 1973526 | K-KOMP FUSION | prototyp + pytania o konflikty danych — **dopytanie/oferta** |

**Czy w PV są wyceny i etapy?** **TAK — w 4 z 10 wątków** (1971430 Daniel, 1971662 PSm, 1972357 QaerQ, częściowo 1971161 Adam Wolski). Dają konkretne kwoty za etapy (np. QaerQ: 4900/3000/4000). Ale **większość PV to dopytania lub próby sprzedaży**, nie pełne wyceny.

**Czym różni się oferta publiczna od PV tego samego wykonawcy:**
- **KARTS DESIGN**: publicznie (2904927) — pełna wycena 10 120-13 420 zł, 92-122h, 4 etapy. W PV (1971217) — tylko hasło reklamowe + „podrzuć info o API". PV to skrót/link do oferty publicznej.
- **Adam ze Studio201**: publicznie (2906344) — 10 000 zł, 21 dni, Flutter. W PV (1971750) — identyczna treść + Calendly. PV = kopia oferty publicznej + CTA.
- **PixelPulse**: publicznie (2907204) — 1500 zł, 7 dni, ogólnik. W PV (1972308) — konkretny link do demo APK. PV daje więcej dowodu niż oferta publiczna.

**Charakter PV:** to głównie **dopytania** (Kordian, K-KOMP, Adam Wolski, KARTS) i **próby sprzedaży / przekierowania kontaktu** (Calendly, e-mail, telefon). **Negocjacje cenowe — brak** (brak wątków z wymianą na temat obniżki ceny). Kilka PV to skrócone duplikaty ofert publicznych, kilka to pełne oferty „wcześniejsze" przed złożeniem publicznej.

**Wniosek E:** PV pełni rolę dwutorową — (1) dopytania o specyfikację (bo brief był ubogi w szczegóły techniczne) i (2) kanał na wcześniejsze/skrócone wersje ofert. Nie jest to kanał negocjacji cen. Najlepsze pełne wyceny i tak trafiają do ofert publicznych; PV to uzupełnienie.

---

## PODSUMOWANIE

1. **Najlepsze oferty = publiczne, długie, wieloetapowe, z własnymi pytaniami krytycznymi** (Kacper 2904792, bfirststudio 2905283, Vernex 2904871, Solid Code 2909764, DAVIDO 2907335).
2. **Cena nie koreluje z jakością** — Szymon M (80k) i Alakhaine (45k) napisali najkrótsze/najsłabsze oferty; Solid Code (29k) napisał krótką, ale gęstą merytorycznie.
3. **Struktura etapów jest kopią briefu** (formularze → zdjęcia → synchronizacja); ~20-22 oferty na 60 dzieli na etapy, większość podaje widełki, kilka (KARTS, Arkadiusz, Daniel) rozbija na roboczogodziny @85-100 zł/h.
4. **Brief zdominował format** — najlepsi odpowiadają punkt po punkcie i rozwijają sekcję o starych telefonach (Xiaomi/Huawei/Doze/WorkManager).
5. **PV to 10 pojedynczych wiadomości** — głównie dopytania i próby sprzedaży, z wycenami tylko w 4 wątkach (1971430, 1971662, 1972357, 1971161); brak negocjacji cenowych.

Mam oba raporty. Odpowiadam punkt po punkcie — dane z 145285 (ERP) i 145287 (mobile).

## 1. Czym charakteryzują się najlepsze oferty?

Pięć wspólnych cech, powtarzają się w obu zleceniach:

- **Identyfikują prawdziwy problem, nie listują funkcji.** Kacper Zdziebło (2904792, mobile) jako jedyny podniósł temat, którego brief nie poruszył: *„Najtrudniejszy element to co się dzieje, gdy pracownik wypełnia formularz bez zasięgu, a ktoś inny zmienia ten sam rekord — tryb offline musi mieć jawną strategię rozwiązywania konfliktów."*
- **Uczciwe granice zamiast obietnic.** DAVIDO (2904751, ERP): *„'zero opóźnień' nie istnieje"*. Skalownia (2906766): *„Czego nie obiecam przy tej skali: zera nadsprzedaży."* bfirststudio (2905283, mobile): *„Kto obiecuje, że deep-sync zadziała zawsze, albo nie sprawdzał, albo liczy na to, że Państwo nie sprawdzą."*
- **Jawne przyznanie luk w portfolio.** Kacper: *„Kotlin ani Flutter nie są moją technologią i piszę o tym wprost."* ensomedia: *„opublikowanych aplikacji mobilnych w portfolio nie mam."*
- **Konkret techniczny z nazwami.** SocialBuzz (2905723): `Change Tracking + RCSI`, `BullMQ + Redis`, `single-writer`, bulk 1000. pawelszojda (2908318): konkretne tabele `tw_Id`, `dok__Dokument`, `shadow log` + trigger.
- **Pytania krytyczne blokujące architekturę** — wersja Subiekta (GT/nexo), licencja Sfery, wersja SQL Servera, liczba magazynów.

## 2. Publiczne czy PV?

**Zdecydowanie publiczne.** W obu zleceniach wszystkie najlepsze, najdłuższe i najbardziej merytoryczne oferty są w kanale publicznym (`oferty/*.json`). PV to dopytania i próby sprzedaży.

## 3. Co pisali najdrożsi?

Tu jest najciekawsze odkrycie — **cena NIE koreluje z jakością**, a najdrożsi dzielą się na dwie grupy:

**Grupa A — drodzy z ogólnikami (najgorszy stosunek ceny do treści):**
- **Matrweb (2906257, ERP, 30 000 zł)** — 3 zdania ogólników, zero konkretu, zero pytań, zero etapów. Cena 6× wyższa od najlepszych ofert.
- **Szymon M (2905692, mobile, 80 000 zł / 16 dni)** — najkrótsza, najbardziej ogólnikowa oferta w całym zleceniu. Wymieszał React + SQLite + FastAPI bez związku z briefem (brief mówił Kotlin/Flutter). Nie podzielił na etapy. Stawka ~5 000 zł/dzień bez uzasadnienia.
- **Alakhaine (2904913, 45 000 zł)** — jedno zdanie i link zewnętrzny.

**Grupa B — drodzy z pełnym uzasadnieniem (uczciwi):**
- **DGital (2904972, 66 000 zł)** — bardzo długa, rozbita na 4 etapy z kwotami: Audyt 6 000 / Formularze 30 000 / Zdjęcia 18 000 / Pilotaż 12 000.
- **bfirststudio (2905283, 50 000 zł)** — uzasadnia, dlaczego pełny zakres nie zmieści się w 60 dniach („43 dni robocze vs 54–65 potrzebnych"), widełki 42–55k.
- **Vulcanoo (2905181, ERP, 24 000 zł)** — najdłuższa oferta w zleceniu, techniczna, uczciwa (*„nie chcę podawać niepotwierdzonych referencji"*), widełki 24–36k.

**Wzorzec:** drodzy bez etapów i bez konkretu = red flag. Drodzy z etapami i uzasadnieniem godzinowym = wiarygodni.

## 4. Co oni wyceniają?

Zależy od typu zlecenia:
- **ERP (145285):** wyceniają całe wdrożenie (delta-sync + zamówienia), ale najlepsi rozbijają na: Etap 1 = stany i ceny (delta sync), Etap 2 = zamówienia + rezerwacje przez Sferę.
- **Mobile (145287):** Etap 1 = formularze offline + lokalna baza + kolejka, Etap 2 = zdjęcia + kompresja, Etap 3 = synchronizacja/push/wdrożenie.

## 5. Jak wyglądają wyceny? Etapy czy full?

**Mieszanka, ale z przewagą full:**
- **ERP:** ~28 ofert full vs ~15 na etapy z kwotami za etap
- **Mobile:** ~20–22 z 60 na etapy, reszta full

**Typowe podejścia:**
- **Jedna kwota** — najczęściej
- **Etapy z kwotami za etap** — najlepsi (SocialBuzz: 3000+3500+2500; Jakub Kulig: 4 etapy 2500+4000+3000+2000; Vernex: 11999+8999+4999)
- **Widełki** — 5 (ERP) / 18–20 (mobile): Matteo 14–20k, Vulcanoo 24–36k, KARTS 10120–13420
- **Roboczogodziny** — rzadkość: KARTS (92–122h), Arkadiusz Kozioł (60–90h × 100 zł/h), Daniel Waraksa (100 zł/h)

**Stawka dnia realnie:** 300–500 zł/dzień (~70–110 zł/h) w obu typach.

## 6. Czy format zależy od naszego zlecenia? TAK — bardzo

To jest kluczowe. **Nasz brief narzucił strukturę odpowiedzi wprost:**

- **ERP:** brief miał zapis *„z możliwością podziału na etapy (najpierw synchronizacja stanów, potem obsługa zamówień)"* → **35 z 49 ofert** wymienia etapowanie niemal w tej kolejności, często cytując nasze sformułowanie.
- **Mobile:** brief prosił o 4 punkty (rekomendacja technologii, przykłady, **podział na etapy + wycena**, czego nie da się offline) → najlepsi odpowiadają punkt po punkcie dosłownie je cytując. bfirststudio: *„Odpowiadam po kolei na cztery punkty z ogłoszenia."* Tomek Julian: *„Pracę podzieliłbym tak, jak Państwo proponują."*

**Wniosek:** gdy brief prosi o etapy — dostajesz etapy. Gdy brief prosi o konkretne punkty — najlepsi je rozwijają, najsłabsi pomijają. **Oferty bez etapów są wyraźnie słabsze jakościowo** — to zwykle „mam gotowe" (DynField, PixelPulse) albo ogólniki sprzedażowe.

Więc tak — **nasze zlecenie ma bezpośredni wpływ na format wycen.** Prosząc o etapy, dostajesz etapy; prosząc o granice, dostajesz uczciwe granice.

## 7. Czy na PV też dają wyceny i etapy?

**Rzadko, ale zdarza się:**
- **ERP (4 wątki PV):** tylko **1 z 4** zawiera wycenę — hexabit (2000 zł/7 dni), i to duplikat publicznej. **Zero etapów w PV.** Reszta to dopytania (Adam Wolski o wersję Subiekta) i próba przejścia na telefon (hermsoft).
- **Mobile (10 wątków PV):** **4 z 10** mają wyceny/etapy — Daniel Waraksa (800–1200 zł etap + MVP 12–16k), PSm (pełna oferta z etapami 45–55 dni), QaerQ (4900+3000+4000 = 11 900 zł), Adam Wolski (skrócona oferta).

**Charakter PV:**
- Głównie **dopytania** (bo brief był ubogi w parametry techniczne)
- **Próby sprzedaży** — przekierowanie na telefon, Calendly, link do CV/demo
- **Brak negocjacji cenowych** — ani jednego wątku o obniżce ceny
- PV często to **skrócona kopia oferty publicznej** (KARTS, Studio201) lub wcześniejsza wersja przed złożeniem publicznej

**Wniosek:** PV to kanał uzupełniający. Pełne wyceny i etapy trafiają do ofert publicznych. Jeśli chcesz porównywać wyceny — patrz na oferty publiczne, nie na PV. PV służy do dopytań i nawiązania kontaktu.

---

**Najważniejsze dla naszych decyzji:**
1. **Wymóg etapowania w briefie realnie kształtuje oferty** — to nasz najlepszy „przycisk" do wyciągania porównywalnych wycen.
2. **Cena nie koreluje z jakością** — najdrożsi bywają najpłytsi (Matrweb 30k, Szymon M 80k). Najlepsi siedzą w środku rozkładu.
3. **PV nie służy do wycen** — to dopytania i sprzedaż. Nie licz na porównywalne wyceny z PV.
4. **Nasze zlecenia są dobre merytorycznie** — wykonawcy odpowiadają punkt po punkcie, co znaczy, że brief jest czytelny. Brakuje tylko parametrów technicznych (wersja systemu, API), które wymuszają dopytania w PV.

Chcesz, żebym zapisał te wzorce (charakterystyka top ofert, cena vs jakość, rola etapowania) jako notatkę operacyjną, czy zostawiamy w rozmowie?

---

**User**

to jest AI '- Identyfikują prawdziwy problem, nie listują funkcji. Kacper Zdziebło (2904792, mobile) jako jedyny podniósł temat, którego brief nie poruszył: „Najtrudniejszy element to co się dzieje, gdy pracownik wypełnia formularz bez zasięgu, a ktoś inny zmienia ten sam rekord — tryb offline musi mieć jawną strategię rozwiązywania konfliktów."
- '
 '- Uczciwe granice zamiast obietnic. DAVIDO (2904751, ERP): „'zero opóźnień' nie istnieje" . Skalownia (2906766): „Czego nie obiecam przy tej skali: zera nadsprzedaży." bfirststudio (2905283, mobile): „Kto obiecuje, że deep-sync zadziała zawsze, albo nie sprawdzał, albo liczy na to, że Państwo nie sprawdzą."
- ' czy cos takiego mam w moim bocie od ofertowania? on ma tam wzorce, mozna zmienic w nim cos takiego?  ze JESLI przechodzi do czesci merytorycznej to fajnie jakby klarownie mowil co sie da co sie nie da.  moze jakos to laczyc z minami?
i ogolnie to ze 'kto obiecal' i rozne odmiany tego brzmia spoko, nie chce tego 1:1 przepisywac
'- Konkret techniczny z nazwami. SocialBuzz (2905723):`Change Tracking + RCSI` ,`BullMQ + Redis` ,`single-writer` , bulk 1000. pawelszojda (2908318): konkretne tabele`tw_Id` ,`dok__Dokument` ,`shadow log` + trigger.
- ' AI


**Assistant**

Dobre pytanie — i sensowne. Najpierw muszę znaleźć, gdzie w ogóle jest prompt / wzorce Twojego bota ofertującego, bo od tego zależy co da się zmienić.





Znalazłem strukturę promptów bota. Kluczowe pliki to [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md), [ludzkie_wzorce.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md) oraz [prompt_ai1.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/prompt_ai1.md) (ten wyskoczył na "miny/canary"). Czytam je, żeby zobaczyć co tam już jest.







Sprawdziłem. Odpowiedź: **częściowo już masz, ale nie jako regułę.**

## Co już jest w bocie

W [ludzkie_wzorce.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md) masz dokładnie te mechanizmy, o które pytasz — jako wzorce D:

- **D21** (DAVIDO): *„zero opóźnień nie istnieje..."* — uczciwe granice
- **D26** (bfirststudio): *„Kto obiecuje, że deep-sync zadziała zawsze..."* — demistyfikacja obietnic
- **D27** (Vulcanoo): *„Nie będę podawał fikcyjnych przykładów."*
- **D22** (Dawidweb): weryfikowalne wersje zamiast ogólników
- **D23** (SocialBuzz): identyfikacja problemu przez anegdotę

Więc materiał masz. **Ale to są obserwacje z triggerami, nie systematyczna zasada.** Bot nie ma reguły: „gdy wchodzisz w merytorykę, pokaż granice".

## Czego brakuje w agencie 02a

W [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) masz:
- Sekcję „MERYTORYKA: domyślnie ZERO" z 3 przypadkami wejścia (klient pyta, mina, alternatywa)
- Sekcję „MINY" (każda oparta na dowodzie)
- Sekcję „DIAGNOZA, NIE RECEPTA"

**Brakuje jednego zdania łączącego merytorykę z granicami.** Teraz mina to „ostrzeżenie przed problemem". Nie ma reguły, że mina może też być **granicą** — czyli „to się da, to się nie da i dlatego".

## Propozycja — mikro-zmiana, nie nowy blok

Nie chodzi o nowy blok „jak czytać" (to wycofaliśmy). Chodzi o **jeden akapit dopisany do istniejącej sekcji MINY** w agencie 02a. Coś w stylu:

> **Mina może być granicą.** Jeśli wchodzisz w merytorykę (klient pyta, mina, alternatywa), to naturalnie powiedz też, czego się NIE da zrobić i dlaczego. Nie jako lista ograniczeń, tylko jako jedna myśl: „to zadziała, tamto nie, bo [przyczyna z jego zlecenia]". To nie jest pesymizm — to pokazuje, że znasz granice systemu, a klient nie kupi czegoś, czego nie dostanie.

**Czego NIE robimy:**
- Nie kopiujemy „kto obiecuje" ani „nie będę udawał" — to są cudze sformułowania. Mechanizm: „pokaż granice", nie cytat.
- Nie dodajemy tego jako obowiązkowego elementu każdej oferty — tylko gdy merytoryka i tak wchodzi.
- Nie tworzymy osobnej sekcji w pliku wzorców — D21/D26/D27 już tam są jako przykłady.

## Dlaczego to nie konflikt z „MERYTORYKA domyślnie ZERO"

Bo to nie jest zaproszenie do gadania. To jest **warunek jakości merytoryki, gdy ta już wchodzi**. Mina „to się nie da" jest naturalną miną — klient musi o tym wiedzieć, bo inaczej się rozczaruje. To wzmacnia, nie osłabia.

---

Chcesz, żebym:
- **(A)** dopisał ten akapit do [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) w sekcji MINY,
- **(B)** dodatkowo dopisał krótką regułę do sekcji „MERYTORYKA: domyślnie ZERO" (punkt 2 — mina), żeby granice były częścią miny,
- **(C)** nic nie ruszał, bo uznajesz że D21/D26/D27 wystarczą?

Ja bym szedł w **A + B** — to jedna spójna zmiana, dotyka dwóch miejsc w tym samym pliku, nie tworzy nowego bloku.

---

**User**

tak zrob ta mikro zmiane. i zoabcz czy nie ma konfliktu to z zadna inna zasada w calym bocie 

**Assistant**

Zanim dopiszę — najpierw czytam pozostałe pliki bota, żeby sprawdzić czy nowa reguła nie wejdzie w konflikt z walidatorem lub innymi zasadami.












---

**User**

kontynuuj

**Assistant**

Przeczytałem wszystkie pliki bota. Konflikt jest **jeden potencjalny** i trzeba go obejść w samym brzmieniu reguły:

**Konflikt:** [jak_pisac_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md) pkt 1.2 mówi: *„Zero wymuszonych szablonów. Żaden element merytoryczny nie jest obowiązkowy sam z siebie."* Oraz [agent_00_orchestrator.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) pkt 1: *„Jeśli klient o coś NIE pyta, nie wciskamy mu tego na siłę."*

Gdybym napisał „zawsze pokazuj granice", wszedłbym w konflikt z obiema. Rozwiązanie: ująć to jako **część merytoryki, która już wchodzi** (klient pyta / mina / alternatywa), a nie jako samodzielny obowiązek.

**Konflikt drugi, też do obejścia:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja „DIAGNOZA, NIE RECEPTA": *„Nigdy nie zdradzasz sposobu: ani naprawy, ani architektury, ani kolejności działań technicznych."* Nowa reguła nie może kazać tłumaczyć „jak obejść granicę", tylko „że granica istnieje". Ujmę to wprost.

Pozostałe pliki ([agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md), [mechanika_wyceniania](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md), [ludzkie_wzorce](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md), [zakazane_zwroty_ai](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/zakazane_zwroty_ai.md)) — sprawdziłem, brak konfliktu. Wręcz wzmacniają:

- [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) sekcja 13 wymaga, by „przyznanie ograniczenia" miało oparcie w zleceniu — moja reguła mówi to samo
- [ludzkie_wzorce](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md) ma już D21 (DAVIDO), D26 (bfirststudio), D27 (Vulcanoo) — moja reguła je systematyzuje, nie dubluje
- [zakazane_zwroty_ai](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/zakazane_zwroty_ai.md) B5 „Kapitulacja i wycofanie" — moja reguła mówi o granicach, nie o kapitulacji

Wprowadzam dwie zmiany w [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md).





Obie zmiany weszły. Teraz sprawdzam resztę plików bota, żeby domknąć weryfikację konfliktów — zostały audyt, sędzia i scenariusze.






Sprawdziłem cały łańcuch bota. Konflikt jest **jeden, pozorny** — i moja reguła go omija, bo jest sformułowana warunkowo.

## Weryfikacja konfliktów

**1. [jak_pisac_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md) pkt 1.2** — „Zero wymuszonych szablonów. Żaden element merytoryczny nie jest obowiązkowy sam z siebie."
→ **Brak konfliktu.** Moja reguła mówi „jeśli merytoryka **i tak wchodzi** (klient pyta, mina, alternatywa)". Nie wymusza granicy w każdym zleceniu, tylko wtedy gdy już jesteś w merytoryce. To spójne.

**2. [agent_00_orchestrator.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) pkt 1** — „Jeśli klient o coś NIE pyta, nie wciskamy mu tego na siłę."
→ **Brak konfliktu.** Ta sama logika. Granica wchodzi tylko z zaczepieniem w zleceniu. Reguła wprost mówi: „Granica bez zaczepienia w zleceniu to straszenie, więc jeśli nie umiesz jej oprzeć na tym, co klient napisał, to jej nie pisz."

**3. [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja „DIAGNOZA, NIE RECEPTA"** — „Nigdy nie zdradzasz sposobu."
→ **Brak konfliktu.** Reguła mówi wprost: „mówisz CO się nie da, nie JAK to obejść. Sposób zostaje u ciebie." To wzmacnia, nie łamie.

**4. [zakazane_zwroty_ai.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/zakazane_zwroty_ai.md) B5 „Kapitulacja i wycofanie"** — zakaz „Jeśli to za mało, rozumiemy", „Mam nadzieję, że to pomoże."
→ **Brak konfliktu.** Reguła mówi: „To nie jest pesymizm ani straszenie." Granica ≠ kapitulacja.

**5. [agent_08_weryfikacja_zasad.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) sekcja 13** — „Wzorzec bez triggera to teatr."
→ **Brak konfliktu. Wzmacnia.** Walidator już wymaga zaczepienia w zleceniu — moja reguła mówi to samo.

**6. [kryteria_audytu_100.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/kryteria_audytu_100.md) Wymiar A pkt 3** — „Spójność logiczna i brak sztucznych wklejek."
→ **Brak konfliktu.** Granica oparta na zleceniu to nie wklejka.

**7. [sedzia_zdrowego_rozsadku.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/sedzia_zdrowego_rozsadku.md)** — VETO za elementy niepasujące.
→ **Brak konfliktu.** Granica z triggera nie jest „elementem, o który klient nie pytał".

**8. [ludzkie_wzorce.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md)** — D21 (DAVIDO), D26 (bfirststudio), D27 (Vulcanoo).
→ **Brak konfliktu. Wzmacnia.** To dokładnie te same mechanizmy, które teraz stały się regułą, a nie tylko obserwacją.

**9. [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md)** — czysto kalkulacyjna.
→ **Brak konfliktu.** Nie dotyka treści oferty.

## Podsumowanie

Zmiana weszła w dwóch miejscach w [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md):
- punkt 2 sekcji „MERYTORYKA: domyślnie ZERO" — krótkie wskazanie, że mina bywa granicą
- sekcja „MINY" — pełny akapit z zasadą i trzema ograniczeniami (zaczepienie w zleceniu, co nie jak, nie pesymizm)

**Zero konfliktów z pozostałymi 10 plikami bota.** Reguła jest sformułowana warunkowo, więc nie łamie „prymatu ogłoszenia" ani „zakazu wymuszonych szablonów". Wręcz systematyzuje to, co w [ludzkie_wzorce.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/ludzkie_wzorce.md) było tylko obserwacją (D21, D26, D27).

Jedna rzecz do rozważenia na przyszłość: czy nie dodać tego jako jawnego kryterium w [kryteria_audytu_100.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/kryteria_audytu_100.md) (np. +pkt w Wymiarze A za uczciwe granice). Ale to już rozbudowa, nie mikro-zmiana — zostawiam Twojej decyzji.

---

**User**

odpal bota na jakies oferrcie.  1 merytorycznej. 2 nie merytorycznej i zobacz czy dziala 

**Assistant**

Najpierw muszę zrozumieć, jak odpalić bota — szukam entry pointa w kodzie.







Zanim odpalę — sprawdzam czy lokalne proxy DeepSeek działa (bot wymaga `http://127.0.0.1:4571`).



PowerShell przechwytuje `curl`. Używam `curl.exe`.



Proxy działa. Tworzę dwa pliki testowe i odpalam łańcuch AI bezpośrednio przez [chain_executor.py](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py) — to odpala same sloty (00 → 01 → 02b → 02a → 08), nic nie wysyła.

Test 1 — **merytoryczne** (jak 145285: klient pyta o granice, daje proces).
Test 2 — **niemerytoryczne** (krótkie, bez pytań, bez konkretu).





Błąd formatu przy zapisie. Ponawiam.





Narzędzie Write zwraca błąd serializacji przy dwóch wywołaniach w jednej turze. Próbuję pojedynczo.




Write narzędzie ma problem. Testuję czy w ogóle działa, prostym plikiem.




Write działa. Problem był przy dwóch wywołaniach równolegle. Zapisuję pliki pojedynczo, z polskimi znakami.




Write ma problem z JSON-em zawierającym zagnieżdżone struktury. Tworzę pliki przez Python.




Plik 1 gotowy. Teraz plik 2 — niemerytoryczny.




Oba pliki gotowe. Piszę mały runner, który odpala pełny łańcuch na obu testach.




Uruchamiam test merytoryczny. Łańcuch ma 4 sloty AI z timeoutami do 240s, więc odpalam w tle i będę sprawdzał.




Test merytoryczny ruszył. Czekam na wynik.




Test 1 (merytoryczny) przeszedł pomyślnie. Bot zadziałał dokładnie tak, jak chcieliśmy — **odsłonił granice** („nie da się zagwarantować zgodności co do minuty", „blokady nie znikną same"), **odradził** („odradzam traktowanie tego jako zwykłej synchronizacji"), zadał **pytanie decyzyjne** (wersja PRO? akceleracja BL?). Zero myślników, zero nawiasów, 7000 zł / 15 dni.

Odpalam test 2 — niemerytoryczny.




Czekam na wynik testu 2.




Oba testy przeszły. Bot działa, zmiana działa. Sprzątam pliki tymczasowe.




Bot działa, zmiana działa. Oto co wyszło.

## Test 1 — merytoryczny (Subiekt nexo + BaseLinker)

**Nowa reguła zadziałała dokładnie jak chcieliśmy.** Bot otworzył ofertę od granic:

> „Od razu powiem, gdzie leży granica, bo Pan o to pyta. Przy 40 tysiącach produktów i dwóch kanałach sprzedaży **nie da się zagwarantować**, że stany na portalach będą zgodne z magazynem co do minuty."

> „Druga rzecz to blokady programu w ciągu dnia. **One prawdopodobnie nie znikną same** po przepisaniu integracji."

> „**Odradzam** traktowanie tego jako zwykłej synchronizacji stanów."

I kluczowe — **nie zdradził sposobu** (zgodnie z „DIAGNOZA, NIE RECEPTA"): mówi CO się nie da, nie JAK obejść. Zadał pytanie decyzyjne (wersja PRO? akceleracja BL?). 7000 zł / 15 dni. Zero myślników, zero nawiasów.

## Test 2 — niemerytoryczny (fix skryptu Python)

**Bot zachował się poprawnie — nie wcisnął granic na siłę.** Mimo że reguła istnieje, przy krótkim zleceniu bez pytań klienta bot napisał:

> „Ten permission denied to często nie problem uprawnień. Na Windows najczęściej plik jest zajęty przez inny program..."

To diagnoza problemu (uprawnienia to objaw, nie przyczyna) — **naturalna mina, nie wymuszona granica**. Krótka oferta, 587 znaków, 800 zł / 7 dni. Brak sekcji „czego się nie da", bo klient o to nie pytał.

## Wniosek

Reguła **nie przecieka** do zleceń, gdzie nie pasuje. Wchodzi tylko tam, gdzie:
- klient wprost pyta o granice (test 1), albo
- jest realna mina do pokazania (test 2 — „to nie uprawnienia, to zajęty plik")

To dokładnie ta warunkowość, którą zaprojektowaliśmy. Gdyby bot wszędzie wciskał „czego się nie da", złamałby „prymat ogłoszenia" i „zero wymuszonych szablonów" — a tego nie zrobił.

## Drobiazg techniczny

Narzędzie Write ma problem z zapisem JSON-a z zagnieżdżonymi strukturami (błąd serializacji przy `fields{}`), więc pliki testowe tworzyłem przez `python -c`. Nie wpływa to na bota — to tylko ograniczenie mojego narzędzia.

Testy zakończone, pliki tymczasowe posprzątane. Bot gotowy do normalnej pracy.

---

**User**

on uzywa slow 'granica' doslownie to moze brzmiec zle

 i zobacz czy to prawda to co on pisze czy na sile wrzucil
cala merytorylke

**Assistant**

Dwa słuszne zarzuty. Sprawdzam oba: (1) skąd bot wziął słowo „granica" i czy to nie echo naszego promptu, (2) czy fakty techniczne są prawdziwe, czy zmyślone.

Najpierw karta wiedzy, która zasilała to zlecenie.




Oba zarzuty sprawdzam równolegle: skąd wzięło się słowo „granica" i czy fakty o BaseLinkerze są prawdziwe.






Sprawdziłem oba zarzuty. Wyniki:

## Zarzut 1 — słowo „granica" to echo naszego promptu. Masz rację.

Grep pokazuje, że **„granica" pojawia się w naszym prompcie w 6 miejscach** ([agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) linie 21, 54, 85-91). Bot złapał to słowo i użył dosłownie: *„Od razu powiem, gdzie leży granica"*. To nie jest naturalny język — to wyciek terminu z promptu. Trzeba to naprawić.

## Zarzut 2 — fakty. Sprawdziłem, bot NIE zmyślił.

Zweryfikowałem najważniejszy fakt — częstotliwość BaseLinkera:

**Oficjalny blog BaseLinker** ([baselinker.com](https://baselinker.com/en-EN/blog/accelerations-speed-up-synchronizations-in-your-baselinker-account/)) potwierdza dokładnie to, co napisał bot:
- **Synchronizacja stanów: co 8 godzin (standard)**
- **Synchronizacja cen: co 24 godziny (standard)**
- Przyspieszenie do 1h / 5 min = **płatny moduł Akceleracje** (rozliczanie dzienne)

Bot napisał: *„BaseLinker domyślnie odświeża stany co 8 godzin, a przyspieszenie tego do godziny albo pięciu minut wymaga włączonej płatnej akceleracji"* — **to jest prawda, zgodna z oficjalną dokumentacją.**

Drugi fakt — **Sfera tylko w nexo PRO** — potwierdzony w [tech_03](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/technologie/baza_wiedzy/tech_03_subiekt_sfera_ecommerce.md#L45): *„Licencja: Wbudowana w każdą licencję nexo PRO"*.

**Jedno zastrzeżenie:** zdanie *„zapis przez Sferę nexo potrafi trwać kilkanaście sekund i w tym czasie trzyma blokady"* — tego konkretu („kilkanaście sekund") nie ma w karcie wiedzy. To dopowiedzenie modelu. Kierunkowo prawdziwe (Sfera faktycznie lockuje tabele), ale liczba jest wyssana. Nie jest to jednak zmyślenie — to racjonalne oszacowanie.

## Naprawiam oba problemy

Zmieniam moje wpisy, żeby nie prowokowały słowa „granica", i dodaję żelazny zakaz.




Teraz sekcja MINY — usuwam słowo „granica" i dodaję żelazny zakaz używania terminów z promptu.




Dodaję jeszcze twardy zakaz do sekcji ŻELAZNYCH ZAKAZÓW, żeby walidator mógł to wyłapać.




Dodaję wyłapywanie wycieku do walidatora [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md).




Zmiany wprowadzone w trzech miejscach. Teraz retest — sprawdzam czy bot przestał używać słowa „granica".










Czekam na wynik retestu.




Retest przeszedł. Sprzątam pliki tymczasowe.




Gotowe. Retest przeszedł, pliki posprzątane. Podsumowanie obu zarzutów:

## Zarzut 1 — „granica" jako echo promptu. Potwierdzony i naprawiony.

**Był problem:** bot napisał *„Od razu powiem, gdzie leży granica"* — dosłowne powtórzenie terminu z naszego promptu (Grep znalazł „granicę" w 6 miejscach w [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)).

**Naprawa w 3 miejscach:**
1. [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) pkt 2 — zmieniłem „Mina bywa też granicą" na „Mina może też pokazać, czego się nie da zrobić"
2. [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja MINY — dodałem akapit *„Nie mów tego słowem «granica»"* z zakazem terminów promptu
3. [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) sekcja 5 — walidator teraz wyłapuje wyciek terminów jako ZŁAMANE

**Retest (ta sama treść zlecenia) — bot napisał:**
> „Z opóźnieniami po stronie BaseLinkera jest **gorzej, niż się wydaje**."
> „Obiecanie stanów aktualnych co kilka minut bez tego modułu **byłoby nieprawdą**."
> „**Nie obiecuję**, że zamkniemy wszystko w 30 dniach bez sprawdzenia, co siedzi w danych."

Zero „gdzie leży granica". Zamiast tego naturalny język. Detektor wykrył „granic" w słowie **„ograniczenie"** („Drugie ograniczenie dotyczy samego Subiekta") — ale to normalne polskie słowo, nie termin z promptu. Fałszywy alarm mojego detektora, nie bota.

## Zarzut 2 — prawdziwość faktów. Bot NIE zmyślał.

Sprawdziłem najważniejszy fakt na **oficjalnym blogu BaseLinker** ([baselinker.com](https://baselinker.com/en-EN/blog/accelerations-speed-up-synchronizations-in-your-baselinker-account/)):

| Fakt z oferty bota | Stan faktyczny (oficjalne źródło) |
|---|---|
| „stany co 8 godzin (standard)" | ✅ potwierdzone |
| „ceny co 24 godziny (standard)" | ✅ potwierdzone |
| „płatne Akceleracje, rozliczane za dni" | ✅ potwierdzone (rozliczanie dzienne) |
| „Sfera tylko w nexo PRO" | ✅ potwierdzone w [tech_03](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/technologie/baza_wiedzy/tech_03_subiekt_sfera_ecommerce.md#L45) |

**Jedno zastrzeżenie:** zdanie z poprzedniej wersji *„zapis przez Sferę potrafi trwać kilkanaście sekund"* — liczba „kilkanaście" nie ma źródła w karcie wiedzy. Kierunkowo prawdziwe (Sfera faktycznie lockuje), ale to oszacowanie modelu, nie fakt. W retescie bot to złagodził i napisał ogólniej: *„operacji masowej, która w jednym momencie zakłada blokady"* — bez wymyślonej liczby.

## Wniosek

Cała merytoryka w ofercie opiera się na faktach z [tech_03](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/analizy/technologie/baza_wiedzy/tech_03_subiekt_sfera_ecommerce.md) i researchu — **nie jest wciśnięta na siłę**. Bot nie wymyślił ani BaseLinkera, ani Sfery. Retest potwierdza, że po poprawce:
- nie ma wycieku terminu „granica"
- fakty pozostają prawdziwe
- bot dalej mówi CO się nie da (naturalnym językiem)
- wycena spójna (6000 zł / 13 dni)

---

**User**

czyli co. nasz bot idealnie wie.  to co moze DOPISAC. to co moze ODPOWIEDZIEC. i to co musi DOPYTAC. co powinno tworzyc 1 spojna calosc. 

**Assistant**

Dobre pytanie, bo tu jest sedno. Rozbijam to na trzy osie i pokazuję, gdzie każda siedzi w bocie — i gdzie jest luka.

## Trzy osie, które bot już ma

| Oś | Co to znaczy | Gdzie w bocie | Stan |
|---|---|---|---|
| **DOPISAĆ** | to, co wnosimy sami: mina, alternatywa, to czego się nie da | [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja MERYTORYKA pkt 2-3 + sekcja MINY | ✅ jest |
| **ODPOWIEDZIEĆ** | to, o co klient wprost pyta | [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) pkt 1 + [agent_00](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) sekcja „WYMOGI JAWNE KLIENTA" | ✅ jest |
| **DOPYTAĆ** | to, bez czego nie da się ruszyć | [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja ZAKOŃCZENIE + [mechanika_wyceniania](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 11 | ✅ jest |

Więc **wszystkie trzy osie istnieją**. Problem w tym, że nie są spięte w jedną decyzję. Bot traktuje je osobno — a powinny być jednym mechanizmem.

## Gdzie jest luka

Zobacz na retest. Bot zrobił wszystko dobrze, ale widać, że **dopytać** i **odpowiedzieć** to dwa osobne światy:

- **Odpowiedział** na pytanie klienta („czego nie da się zrobić") — sekcja MERYTORYKA pkt 1
- **Dopytał** o wersję PRO — sekcja ZAKOŃCZENIE

Ale to jest to samo zlecenie i ten sam problem. Pytanie „czy macie PRO?" wynika z tego samego faktu (Sfera tylko w PRO), który bot podał w odpowiedzi. **Powinno to być jedno zdanie, nie dwa osobne bloki.**

Klient czyta: „Sfera tylko w PRO" (odpowiedź) ... potem ... „potrzebuję wiedzieć czy macie PRO" (pytanie). To jest echo. Człowiek powiedziałby to raz: *„Sfera istnieje tylko w PRO, więc zanim cokolwiek wycenię, powiedzcie, na czym stoicie."*

## Co proponuję

Nie nowy blok. **Jedno zdanie w [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)**, które łączy trzy osie w jeden mechanizm:

> **Trzy rzeczy to jedna decyzja.** Gdy klient o coś pyta, gdy wchodzi mina albo alternatywa, i gdy potrzebujesz informacji, żeby ruszyć, nie rób z tego trzech osobnych akapitów. To jest jedna myśl: „tu jest fakt, a z niego wynika pytanie do ciebie". Jeśli mina prowadzi do pytania, zadaj je od razu przy tej minie, nie na końcu. Jeśli pytanie na końcu nie wynika z niczego w treści, to znaczy, że pytasz o coś, czego nie uzasadniłeś — wtedy albo je usuń, albo najpierw uzasadnij.

To jest dokładnie to, co w retescie zagrało połowicznie — bot miał rację, ale rozbił to na dwa bloki.

## Zanim to zrobię — jedno pytanie

Czy chcesz, żebym:
- **(A)** dopisał to zdanie łączące trzy osie do [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) i zrobił retest,
- **(B)** najpierw pokazał Ci, jak wyglądałby taki „spięty" fragment na przykładzie z retestu (przepisany ręcznie, żebyś ocenił czy to lepsze),
- **(C)** uznał, że trzy osie rozdzielone są OK i nie ruszamy?

Ja bym szedł **B, potem A** — najpierw pokazuję różnicę na żywym tekście, żebyś zobaczył czy warto, potem wdrażam. Bo to nie jest oczywista poprawa — czasem rozdzielenie pytań od merytoryki jest czytelniejsze.

---

**User**

to chyba zbyt plytkie zbey cokolwiek laczyc. 
ty i ja razem zobaczymy jaka jest prawda ja zaczne
w jakis sposob musimyt stworzyc bota ktory dziala jak ludzki mozg jelsi chodzi o tworzenie ofert 
mamy  napewno kryterium ktore jest ZAWSZE
1. to co zlecenie nam mowi. i na podstawie tego jest ustalane czy odpaalmy research, co za tym idzie merytoryke. i jak daleko ja stosujemy. tak zeby nie zgadywac NIC. piszemy tyle ile faqktycznie jest inforacji
o reszte trzeba dopytac
jednoczesnie nie mozna zapominac o wycenie ktora jest warunkowiana na podstawie tego co pisza 
skoro sa rzeczy owarte, jak cos o co mozna zapytac to wiadomo ze wycena tez nie bedzie idealna. stad widły. najlepiej jakby po ludzku bylo napisane normalnie od cdzego zalezy wycena i wlasnie to bedzie zawarte w pytaniach. ale nie za duzo. nie mozemy opytac o wszystko tylko najwazniejsze rzeczy.  chyba ze zlecneie pokrywa WSZYSTKO. 
czy to sie zgadza mniej wiecej z tym co mam w tych promptach ? DODATKOWO odpal subagentow. niech sprawdza czy moja regula dziala na wszystko. czyli biora to co napisalem. prompt tez. i patrza czy mnoje rzeczy nie byly by za sztywene. albo idealnie pasowaly i bylyb ludzkie.  niech noe odpalaja lancucha tylko spojrza tak o.  odpal  max 4. 

**Assistant**

Zanim odpalę — moja wstępna odpowiedź na Twoje pytanie.

**Tak, zgadza się z promptami, ale z jednym twardym zastrzeżeniem.** Twoja reguła mówi „stąd widełki" — a w [jak_pisac_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md) i [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) pkt 9 jest **bezwzględny zakaz widełek w treści** („jedna konkretna kwota"). To potencjalny konflikt, który subagent 2 musi rozstrzygnąć.

Reszta Twojej reguły — research z zlecenia, zero zgadywania, dopytanie o najważniejsze, wycena warunkowa — **jest już w promptach**, ale rozproszona po 4 plikach i nigdzie nie ujęta jako jedna logika.

Odpalam 4 subagentów. Każdy bierze Twoją regułę + prompty i patrzy **tylko okiem** (bez odpalania łańcucha).










# Raport: ocena reguły „research zależy od zlecenia, zero zgadywania”

## 1. Gdzie jest mechanizm i czy jest kompletny

Mechanizm bramki ON/OFF siedzi wyłącznie w **`agent_01_research.md`, sekcja „CZĘŚĆ A: CZY MAM CO POKAZAĆ, CZY TYLKO ZGADUJĘ”**. Kluczowe zdanie rozstrzygające:

> „Zasada rozstrzygająca: pokazać mogę tylko wtedy, gdy klient dał proces albo pytanie. W razie wątpliwości wybierz OFF, bo brak researchu kosztuje mniej niż research na siłę.”

Bramka ma dwie listy:
- **Research ON**: klient opisał proces, zadał pytanie, przejmuje legacy, prosi o konsultację, „duże, złożone zlecenie z realnym budżetem”, widzisz lepszą drogę z dowodem.
- **Research OFF**: „napisał dwa zdania”, brak procesu/pytania/kodu, dał materiały i wie czego chce, „rekrutacja na stałą współpracę bez konkretnego problemu”.

Plus **czujka językowa** („jeśli to jest X…” → OFF; „w Państwa procesie X…” → ON) i **ABSOLUTNY ZAKAZ** badania życia firmy klienta. Wyjście OFF to sztywny znacznik `BRAK_ISTOTNYCH_FAKTOW`.

**Ocena kompletności:** mechanizm jest kompletny w sensie dwukierunkowym (ma listę ON i OFF oraz regułę rozstrzygającą na wypadek wątpliwości), ale **nie jest spójny wewnętrznie** i **nie jest zintegrowany z klasyfikacją zleceń** z `selekcja_zlecen.md`. Dowody w punktach niżej.

---

## 2. Test reguły na 5 typach zleceń

### Typ 1: Merytoryczne, klient daje proces i pyta
- **Bramka**: ON (spełnia dwa kryteria z listy ON jednocześnie).
- **Wynik**: research działa, miny/alternatywy idą do `agent_02a` (sekcja „MERYTORYKA: domyślnie ZERO”, przypadek 1 i 2).
- **Ocena**: sensowny, to wzorcowy przypadek. Reguła działa.

### Typ 2: Krótkie, 2 zdania, bez pytań (niemerytoryczne)
- **Bramka**: OFF (wprost: „napisał dwa zdania i tyle”, „nie opisał procesu, nie zadał pytania”).
- **Wynik**: `BRAK_ISTOTNYCH_FAKTOW`, oferta krótka, zgodna z sekcją „GRANICA CIĘCIA (metafora włosa)”.
- **Ocena**: sensowny dla zleceń czysto wykonawczych. **Ale** reguła nie odróżnia „2 zdania bez treści” od „2 zdania z nazwą technologii, która sama w sobie implikuje znaną minę” (patrz Luka B).

### Typ 3: tech_agnostic (klient biznesowy bez żargonu IT)
- **Bramka**: działa poprawnie **tylko wtedy, gdy klient opisze proces**. Wtedy ON („opisał swój proces, swoją obecną sytuację”).
- **Problem**: `agent_01` **nie zna pojęcia tech_agnostic** — nie odwołuje się do `typ_klienta: tech_agnostic` ani do `sciezka: "biznes"` z `selekcja_zlecen.md`. Bramka działa więc „przypadkowo” poprawnie: jeśli klient biznesowy napisze „chcę usprawnić firmę” bez procesu → OFF. To jest zgodne z „piszemy tyle, ile jest informacji”.
- **Ocena**: wynik sensowny, ale mechanizm nie jest świadomy typu — brak integracji, nie luka wynikowa.

### Typ 4: quick_fix (awaria, błahy błąd)
- **Bramka**: jeśli klient napisze „strona padła, błąd 500, ratunku” → OFF (brak procesu, 2 zdania).
- **Problem**: **quick_fix nie istnieje w bramce `agent_01`**. Nie ma słowa o awariach, błędach 500, migracjach. `selekcja_zlecen.md` wyodrębnia `typ_klienta: quick_fix` i „szybkie naprawy awarii (błąd 500, migracje)” jako TIER B.
- **Ocena**: reguła daje tu **za sztywny wynik OFF**, mimo że awaria to konkretny problem, przy którym research znanych regresji/limitów mógłby dać realną minę. Bramka traktuje quick_fix jak „2 zdania” i ucina research, zamiast rozpoznać, że „błąd 500” to konkret techniczny. **Luka.**

### Typ 5: Rekrutacja na stałą współpracę bez konkretnego problemu
- **Bramka**: OFF — wprost na liście OFF („to rekrutacja na stałą współpracę bez konkretnego problemu”).
- **Ocena**: wynik sensowny i spójny z `agent_02a` (brak merytoryki, krótka oferta). Ale **konflikt z `selekcja_zlecen.md`**: ten plik rozdziela „ukryte rekrutacje na etat” (ODRZUT, punkt 7) od „stałej współpracy” rozliczanej godzinowo (BIERZEMY, Tier A/B, zasada 50–250 zł). `agent_01` daje OFF dla obu bez rozróżnienia. Bramka nie rozstrzyga, czy „stała współpraca B2B z konkretnym problemem” to jeszcze OFF. Reguła „bez konkretnego problemu” to ratuje, ale nie ma definicji „konkretnego problemu”.

---

## 3. Gdzie reguła jest za sztywna / pęka

### Luka A: Wewnętrzna sprzeczność listy ON i OFF (najpoważniejsza)
Lista **ON** zawiera samodzielne kryterium:
> „to duże, złożone zlecenie z realnym budżetem”

a lista **OFF**:
> „dał z góry materiały i wie dokładnie czego chce (»dane w Excelu, podaj stawkę«)”

**Scenariusz pęknięcia**: duże, złożone zlecenie z realnym budżetem, w którym klient dał materiały i wie dokładnie czego chce. Który warunek wygrywa? Reguła rozstrzygająca mówi „proces albo pytanie”, ale duże zlecenie nie musi mieć ani procesu, ani pytania. **Bramka nie ma priorytetu między listami** — to luka logiczna, nie tylko interpretacyjna.

### Luka B: „Nazwa technologii to NIE zaproszenie” ucina znane miny branżowe
Sekcja CZĘŚĆ A mówi:
> „sama nazwa technologii to NIE jest zaproszenie do merytoryki. […] Nazwa bez procesu i bez pytania to za mało.”

**Scenariusz pęknięcia**: „Chcę scraping z Allegro, budżet 800 zł.” Klient nie dał procesu, nie zadał pytania → OFF → `BRAK_ISTOTNYCH_FAKTOW`. A przecież anty-scraping, rate-limit i brak oficjalnego API to **obiektywne miny niezależne od procesu klienta** — dokładnie to, czego szuka CZĘŚĆ B („pułapka techniczna (brak oficjalnego API, anty-scraping, rate-limit)”). Reguła jest tu **za sztywna**: zabrania researchu, gdy mina jest powszechnie znana dla danej technologii, a klient nie dał nic więcej. Mina istnieje obiektywnie, nie jest zgadywaniem „może u niego”.

### Luka C: quick_fix nieobsłużony w bramce
Jak w Typie 4. Bramka nie ma kryterium „awaria / konkretny błąd produkcyjny”, więc spłaszcza quick_fix do „2 zdania” i wyłącza research. `selekcja_zlecen.md` traktuje ten typ jako osobną, dochodową kategorię (TIER B, „szybkie naprawy awarii”).

### Luka D: brak priorytetu między ON a OFF dla procesu bez potencjału
Lista ON: „opisał swój proces” → ON. Ale jeśli klient opisał proces rutynowy, bez pytań i bez realnych min, research zostanie odpalony, zwróci `BRAK_ISTOTNYCH_FAKTOW`, a `agent_02a` i tak nic nie użyje (sekcja „Jeśli masz w researchu zebrane fakty, a klient o nic nie pyta i nie ma miny, to znaczy, że research nie idzie do oferty”). Reguła jest tu **za sztywna w drugą stronę**: ON bez potencjału na merytorykę to koszt bez zysku. Nie ma kryterium „proces, ale bez potencjału na minę/pytanie”.

### Luka E: brak integracji z klasyfikacją zleceń
`agent_01` nie odwołuje się do `typ_klienta` (`ekspert_dziedzinowy`, `msp_erp`, `ecommerce`, `agencja`, `tech_agnostic`, `quick_fix`) ani do `modyfikatorów` (`RESCUE`, `DELEGOWANY`, `PHANTOM`) z `selekcja_zlecen.md`. Bramka jest zbudowana wyłącznie na „co klient napisał”, a nie na „jaki to typ zlecenia”. Skutek: mechanizm działa poprawnie tylko przypadkowo dla części typów (tech_agnostic), a dla innych (quick_fix) w ogóle ich nie widzi.

### Luka F: brak definicji „konkretnego problemu” przy rekrutacji
OFF mówi „rekrutacja na stałą współpracę **bez konkretnego problemu**”. Bramka nie definiuje, co znaczy „konkretny problem”. Rekrutacja z opisem stacku, ale bez problemu biznesowego → OFF. Rekrutacja z jednym zdaniem problemu → wypada z warunku OFF, ale nie ma gwarancji, że trafi do ON. Nieostra granica.

---

## 4. Wnioski

1. **Mechanizm istnieje i jest kompletny funkcjonalnie** (lista ON, lista OFF, czujka, zasada rozstrzygająca, twardy znacznik OFF), ale **nie jest kompletny logicznie** — ma wewnętrzną sprzeczność (Luka A) i lukę integracyjną (Luka E).
2. **Reguła działa dobrze na 3 z 5 typów**: zlecenie merytoryczne z procesem i pytaniem (Typ 1), krótkie 2 zdania (Typ 2), tech_agnostic z opisem procesu (Typ 3). Dla rekrutacji (Typ 5) daje sensowny wynik, ale przez przypadek — bo nie odróżnia stałej współpracy B2B od rekrutacji na etat.
3. **Reguła pęka na quick_fix (Typ 4)** — brakuje kategorii „awaria / konkretny błąd produkcyjny”, więc bramka spłaszcza ją do „2 zdania” i wyłącza research, mimo że `selekcja_zlecen.md` traktuje quick_fix jako osobną kategorię dochodową.
4. **Największe luki**: (A) brak priorytetu między „duże zlecenie” (ON) a „materiały + wie czego chce” (OFF); (B) „nazwa technologii to nie zaproszenie” ucina znane miny branżowe (scraping, API), które są obiektywne; (C) brak quick_fix; (D) ON przy procesie bez potencjału na merytorykę; (E) brak powiązania z `typ_klienta`/`modyfikatory` z `selekcja_zlecen.md`; (F) nieostre „bez konkretnego problemu”.
5. **Konflikt między plikami**: `agent_01` daje OFF dla rekrutacji, a `selekcja_zlecen.md` ma jednocześnie ODRZUT dla „ukrytych rekrutacji na etat” i BIERZEMY dla „stałej współpracy” godzinowej. To dwa różne werdykty na tej samej płaszczyźnie, a bramka researchu ich nie rozróżnia.

**Rekomendacja dla parent agenta**: reguła „research zależy od zlecenia, zero zgadywania” jest **w większości słuszna, ale nie na WSZYSTKIE typy zleceń**. Wymaga trzech uzupełnień: (1) priorytetu listy ON/OFF, (2) wyjątku „obiektywna mina znana dla technologii” od zakazu „nazwa to nie zaproszenie”, (3) wprost obsłużonego quick_fix oraz mapowania na `typ_klienta` z `selekcja_zlecen.md`. Bez tego pęka na quick_fix i na krótkich zleceniach z technologią, która sama w sobie niesie minę.

Świetny raport z pierwszego. Odpalam pozostałe trzy równolegle.






































# RAPORT Z OCENY REGUŁY: "WYCENA WARUNKOWA, STĄD WIDEŁKI"

## 1. KRYTYCZNE: "stąd widełki" vs "ZAKAZ widełek" — konflikt rozstrzygalny?

**Werdykt: to nie jest konflikt nie do pogodzenia. To konflikt semantyczny (niedopasowanie znaczenia słowa "widełki"), który da się pogodzić — ale tylko jeśli rozdzielimy dwa poziomy.**

W promptach słowo "widełki" istnieje jawnie i legalnie, ale **wyłącznie na poziomie godzin modułów** (kalkulacja wewnętrzna), nigdy na poziomie ceny końcowej w ofercie:

- `mechanika_wyceniania.md` KROK 2: "odczytaj **widełki godzinowe** (optymistycznie realistycznie)"
- KROK 3: "Wynik to **dwie liczby**: suma optymistyczna i suma realistyczna"

Te widełki godzinowe są następnie **zwijane do jednej liczby** przez KROK 4 (buffer), KROK 5 (mnożnik ryzyka), KROK 7 (korekta konkurencyjna) i KROK 9 (zaokrąglenie).

Z kolei na poziomie **oferty publicznej** obowiązuje twardy zakaz widełek cenowych:
- `agent_02a_opis_oferty.md` sekcja STRUKTURA: "Wycena: **jedna konkretna kwota** i liczba dni, spójne z blokiem [WYNIK_KONCOWY]"
- `agent_02a` pkt 9 ŻELAZNYCH ZAKAZÓW: "Zakaz widełek w treści (jedna konkretna kwota)"
- `agent_08` sekcja 8: "W treści oferty kwota jest widełkami cenowymi zamiast jednej konkretnej liczby → ZŁAMANE"

**Rozstrzygnięcie:** reguła użytkownika jest spójna, jeśli "widełki" zinterpretujemy jako **widełki godzinowe / zakres niepewności kalkulacji**, a nie jako cenę końcową. Warunkowość wyceny **nie jest wyrażana widełkami ceny, lecz pytaniami** (CTA). To dokładnie pokrywa się z drugą częścią reguły użytkownika: *"żeby po ludzku było napisane, od czego zależy wycena, i to zawarte w pytaniach"*. Odpowiada temu `agent_02a` sekcja ZAKOŃCZENIE: "Jeśli pytasz, uzasadnij po co pytasz ('nie ma Pan w ogłoszeniu o tym, a od tego zależy...')".

**Co jest do pogodzenia:** widełki istnieją, ale ukryte (godziny), a warunkowość idzie w pytania — nie w cenę.

**Co wymaga dopięcia:** żaden prompt nie mówi wprost "warunkowość wyrażaj pytaniem, nie widełkami ceny". To luka komunikacyjna, nie sprzeczność logiczna.

---

## 2. Gdzie jest mechanizm "wycena zależy od tego, co klient napisał"

Trzy realne miejsca, wszystkie zależne od treści ogłoszenia:

**(a) KROK 9.5 "Kotwica budżetu klienta" (mechanika):**
- Dekodowanie budżetów 50–250 zł — Wariant A (stawka 90 zł/h) vs Wariant B (mikrozadanie fixed-price)
- Budżety całkowite (>250 zł): "Jeśli budżet klienta jest **wyższy** niż Twoja cena bazowa: **celuj w 80-90% budżetu klienta** (z capem 1.4x wyceny bazowej)"
- "Jeśli budżet klienta jest **niższy** niż Twoja cena bazowa: nie składaj oferty poniżej rentowności"

**(b) Flaga `brak_specyfikacji` (agent_02b → mechanika KROK 5):**
- `agent_02b`: "`brak_specyfikacji`: klient opisał problem ogólnie, brak mockupów → true"
- KROK 5: "Klient nie ma specyfikacji (opisał problem ogólnie, brak mockupów): ×1.05"

**(c) Mnożnik ryzyka (KROK 5) + flaga `figma_w_ogloszeniu`:**
- "Klient ma Figmę + szczegółową specyfikację: **×0.90** (mniej niewiadomych, szybsza praca)"
- "Funkcje real-time: ×1.10", "Zewnętrzne API: ×1.05/×1.15"
- Cap: `MAX_RISK_MULTIPLIER = 1.15`

Dodatkowo KROK 4 rozdziela powody: "Brak specyfikacji rozliczamy **WYŁĄCZNIE mnożnikiem w KROKU 5 (×1.05)**, a NIE podnoszeniem bufora w KROKU 4. Nigdy nie stosuj obu naraz za ten sam powód."

---

## 3. Test na 3 typach zleceń

### Typ A — kompletne (Figma + specyfikacja + budżet jawny)
- `figma_w_ogloszeniu: true`, `brak_specyfikacji: false`
- KROK 5: `×0.90` (najniższy mnożnik — obniża cenę)
- KROK 9.5: budżet jawny → "celuj w 80-90% budżetu klienta (cap 1.4x)"
- **Efekt:** cena obniżona ×0.90, dodatkowo dociągnięta do realnego budżetu. Widełki godzinowe najwęższe.
- **Ocena:** sensowne. Kompletność obniża cenę (mniej niewiadomych = szybciej). ✅

### Typ B — częściowe (proces opisany, brak 2-3 parametrów technicznych)
- Flaga `brak_specyfikacji` jest **binarna true/false**. Tu powstaje problem: "brak 2-3 parametrów" to nie to samo co "opisał problem ogólnie, brak mockupów".
- Jeśli ustawisz `true`: ×1.05. Jeśli `false`: ×1.0.
- **Efekt:** różnica między "kompletne" a "częściowe" może wynosić ledwie 0 (jeśli flaga = false), a między "częściowe" a "otwarte" również 0 (obie = true → ×1.05).
- **Ocena:** ⚠️ **najsłabszy punkt mechaniki.** Brak gradacji — "częściowe" wpada w tę samą kategorię co "otwarte" albo w tę samą co "kompletne". Nie ma mechanizmu różnicującego 2-3 brakujące parametry od pełnego braku specyfikacji.

### Typ C — otwarte (ogólny problem, brak szczegółów)
- `brak_specyfikacji: true` → ×1.05
- KROK 4 zakazuje dodatkowego podnoszenia bufora za ten sam powód
- **Efekt:** zaledwie +5% ponad neutralną kalkulację. Cap `MAX_RISK_MULTIPLIER = 1.15` i tak ogranicza całość.
- **Ocena:** ⚠️ różnica "kompletne ×0.90" vs "otwarte ×1.05" to ~16% w godzinach. Wąska różnica jak na tak dramatyczną różnicę w ilości informacji. Widełki (cena) nigdzie nie występują — jest jedna kwota. Warunkowość obsługują pytania CTA (agent_02a ZAKOŃCZENIE).

**Czy "widełki" są gdzieś już obecne?** Tak — w `mechanika_wyceniania.md` KROK 2 i KROK 3 ("widełki godzinowe", "dwie liczby: suma optymistyczna i suma realistyczna"). To jedyne legalne widełki w całym systemie. Cena końcowa po KROK 9 jest zawsze jedną liczbą.

---

## 4. LUKI I SPRZECZNOŚCI

**LUKA 1 (główna) — brak instrukcji "jak uzasadnić cenę bez widełek".**
Prompty zakazują widełek (agent_02a pkt 9, agent_08 sekcja 8) i każą "uzasadnić po co pytasz, a od tego zależy" (agent_02a ZAKOŃCZENIE), ale **żaden prompt nie łączy tych dwóch rzeczy w jedną instrukcję**: "warunkowość wyrażaj pytaniem, nie widełkami ceny". To luka, nie sprzeczność. `agent_02a` pkt 14 daje tylko połowiczne narzędzie: "Tryb warunkowy zamiast decyzji ('żeby wycenić dokładnie, musiałbym najpierw zobaczyć')".

**LUKA 2 — binarna flaga `brak_specyfikacji` nie obsługuje stanu pośredniego.**
`agent_02b` definiuje ją jako "klient opisał problem ogólnie, brak mockupów → true". Zlecenie "częściowe" (proces + brak 2-3 parametrów) nie ma własnej kategorii. Trafia do ×0.90, ×1.0 lub ×1.05 w zależności od uznania AI — to niespójne.

**LUKA 3 — napięcie między "wycena zależy od tego, co klient napisał" a KROK 9.5 (budżet).**
Gdy klient poda jawny budżet, KROK 9.5 mówi: "celuj w 80-90% budżetu klienta". To znaczy, że **dominującym czynnikiem staje się kwota budżetu, a nie zakres opisany przez klienta**. Dla zlecenia kompletnego z wysokim budżetem wycena idzie w górę nie z powodu pracy, lecz z powodu budżetu. To osłabia tezę "wycena zależy od tego, co klient pisze (o zakresie)".

**LUKA 4 — cap `MAX_RISK_MULTIPLIER = 1.15` spłaszcza warunkowość.**
Otwarte zlecenie (×1.05) vs kompletne (×0.90) = tylko 16% różnicy. Przy tak dużym capie mechanika nie generuje silnie zróżnicowanych wycen w zależności od kompletności briefu.

**SPRZECZNOŚĆ POZORNA (do wyjaśnienia w prompcie, nie do naprawy logiki):**
- "wycena warunkowa" ↔ "jedna konkretna kwota". To nie sprzeczność: warunkowość jest we **wnioskowaniu** (flagi, mnożniki, KROK 9.5), a wynik jest **jedną liczbą** (KROK 9, agent_02a pkt 9). Sama mechanika już to godzi — brakuje tylko zdania w `agent_02a`/`agent_08`, że warunkowość komunikujemy pytaniem CTA, nie widełkami.

**CZEGO PROMPTY NIE MÓWIĄ JASNO:**
Jak uzasadnić jedną kwotę, gdy klient dał mało informacji. `agent_02a` pkt 14 (tryb warunkowy) i sekcja ZAKOŃCZENIE (pytanie z uzasadnieniem) to jedyne narzędzia, ale nie są ze sobą powiązane w regułę "mało informacji → jedna kwota + pytanie o brakujący parametr z uzasadnieniem 'od tego zależy wycena'".

---

## REKOMENDACJE (do decyzji rodzica, bez zmian w plikach)

1. **Nie zmieniać zakazu widełek cenowych** — jest poprawny i spójny z mechaniką.
2. **Dodać do `agent_02a` (sekcja Wycena/Zakończenie) zdanie wiążące:** warunkowość wyceny komunikujemy **pytaniem** ("od tego zależy wycena"), nigdy widełkami ceny — to wprost realizuje regułę użytkownika.
3. **Rozważyć rozszerzenie flagi `brak_specyfikacji`** na trzystanową (kompletna / częściowa / otwarta) albo dodać drugą flagę `specyfikacja_czesciowa`, by Typ B miał własny mnożnik.
4. **Zbadać KROK 9.5 pod kątem nadrzędności budżetu** nad zakresem — obecnie może wypaczać "wycenę zależną od treści".
5. **Udokumentować w `mechanika_wyceniania.md`**, że "widełki godzinowe" (KROK 2-3) są pojęciem wewnętrznym i nigdy nie trafiają do oferty — usuwa to semantyczny konflikt z regułą użytkownika.












# Raport: ocena spójności trzech osi + wyceny w promptach

Przeczytałem wszystkie wskazane pliki plus dwa, które są niezbędne do oceny przepływu: `generatory/prompt_ai1.md` (triage) i `walidatory/agent_08_weryfikacja_zasad.md` (bramka końcowa). Poniżej ocena krytyczna.

---

## 1. Przepływ i miejsce każdej osi

Realny łańcuch (zgodnie z plikami, nie z kolejnością w pytaniu):

```
zlecenie -> prompt_ai1 (BIERZEMY/TIER/sciezka)
         -> agent_00 (plan reżyserski: WYMOGI / CO PASUJE / BLOKADY / DYSCYPLINA)
         -> agent_01 (research: miny, ciekawostki, alternatywy, ceny rynkowe)
         -> agent_02b (JSON: moduły + godziny + flagi)
         -> kalkulator Python (mechanika_wyceniania) -> [WYNIK_KONCOWY]
         -> agent_02a (pisze treść oferty, wpina kwotę/dni z [WYNIK_KONCOWY])
         -> agent_08 (PASS/FAIL)
```

Uwaga: **agent_02b wyprzedza agent_02a**. Wycena powstaje zanim ktokolwiek pisze treść. Agent_02a dostaje gotowe `[WYNIK_KONCOWY]` i tylko je wkleja ("kwota i dni w treści = dokładnie [WYNIK_KONCOWY]").

Mapowanie osi na miejsca:

| Oś | Gdzie powstaje | Gdzie jest konsumowana |
|---|---|---|
| **DOPISAĆ** (merytoryka z researchu) | agent_01 (materiał) | agent_00 filtruje „co pasuje", agent_02a decyduje „ile użyć" (sekcja `MERYTORYKA: domyślnie ZERO`) |
| **ODPOWIEDZIEĆ** | agent_00 pkt 1 `WYMOGI JAWNE KLIENTA` | agent_02a `MERYTORYKA` pkt 1 „Klient wprost pyta" |
| **DOPYTAĆ** | mechanika KROK 11 (gotowe pytania), agent_00 pkt 2 „jakie naturalne pytanie zadać na końcu" | agent_02a sekcja `ZAKOŃCZENIE: CTA wynika z kontekstu` |
| **WYCENA** | mechanika_wyceniania + agent_02b | agent_02a sekcja `STRUKTURA` (wkleja kwotę/dni), agent_08 pkt 8 |

Kluczowa obserwacja: **agent_00 jest PRZED agent_01**. Orchestrator planuje „które 1 lub 2 konkrety merytoryczne warto poruszyć" zanim research w ogóle powstał. To jest logicznie wadliwe, wracam do tego w pkt 2 i 3.

---

## 2. Czy osie są połączone, czy każda żyje w swoim pliku

Osie są **rozproszone i słabo spięte**. Nie ma jednego miejsca, które trzyma „DOPISAĆ + ODPOWIEDZIEĆ + DOPYTAĆ + WYCENA" razem. Każda żyje we własnym pliku i własnym słowniku. Konkretne przykłady rozłączenia:

- **Orchestrator planuje merytorykę bez researchu.** agent_00 `Format wyjściowy` pkt 2: *„które 1 lub 2 konkrety merytoryczne warto poruszyć"*. Ale agent_00 uruchamia się przed agent_01, więc nie wie jeszcze, jakie miny/alternatywy w ogóle istnieją. Plan merytoryczny powstaje w ciemno, a agent_01 może potem przynieść minę, której orchestrator nie widział i której nie umieścił w blokadach.

- **Wycena nie jest spięta z narracją.** agent_02b liczy moduły i flagi, ale agent_02a nie wie, dlaczego wyszła taka kwota. Nie ma przekazania „uzasadnienia" z JSON-a 02b do treści oferty. `uzasadnienie` w JSON-ie („krótkie uzasadnienie wyboru modułów i flag") jest dla kalkulatora, nie dla pisarza. Związek „co klient napisał → ile to kosztuje → jak to opisujemy" jest przecięty w połowie.

- **Pytania z mechaniki nie trafiają do 02a.** mechanika KROK 11 ma gotowe pytania („Ile SKU i z jakim systemem magazynowym to spinamy?", „W jakim formacie macie teraz te pliki..."). agent_02a w ogóle o nich nie wie, ma tylko ogólną regułę „pytamy TYLKO o to, bez czego nie da się ruszyć". Wiedza o dobrych pytaniach zostaje w mechanice i nie jest konsumowana.

- **Blokady agent_00 nie obejmują min z researchu.** agent_00 zakazuje szablonów „na wejściu", ale miny z agent_01 wchodzą do oferty z mocy agent_02a pkt 2 (`Trafiła się mina`). Nikt nie sprawdza, czy ta mina pasuje do blokad orchestratora. Filtruje ją dopiero agent_08, ale on nie zna pełnego planu 00 w zakresie „dlaczego ta mina jest OK".

- **Portfolio: trzy różne reżimy w trzech plikach.** agent_00: *„Kategorycznie ZAKAŻ Agentowi 02a jakichkolwiek wzmianek"*. agent_02a zakaz #5: „ZERO powoływania się na portfolio". jak_pisac_oferty pkt 5: *„Jeśli klient wprost o nie pyta, powiedz to jednym zdaniem wprost"*. Trzy pliki, trzy różne zachowania w sytuacji „klient pyta o portfolio". agent_02a nie ma instrukcji, co zrobić, gdy klient pyta wprost.

---

## 3. SPRZECZNOŚCI między plikami (lista)

1. **Merytoryka ZERO vs uzasadnianie ceny merytoryką.**
   agent_02a: *„W każdym innym przypadku: ZERO merytoryki"*. A mechanika KROK 9.5/końcówka: *„Dla zleceń które naturalnie wychodzą poniżej 500 zł uczymy się pisać oferty tak, żeby uzasadnić tę kwotę (pełen setup, konfiguracja, testy, gwarancja)"*. Jedna reguła każe milczeć, druga każe pisać uzasadnienie, żeby cena nie wyglądała na wyjętą z powietrza. To dokładnie ta sprzeczność, o którą pytasz.

2. **Etapowanie: agent_00 pozwala, mechanika zakazuje.**
   agent_00: *„Zaproponuj podział na etapy tylko wtedy, gdy projekt jest większy i wieloczęściowy"*. mechanika KROK 9.5: *„zakaz samowolnego dzielenia projektu na Fazę 1 / małe MVP, chyba że klient wprost w ogłoszeniu poprosił"*. agent_00 autoryzuje etapy przy dużych projektach, mechanika je blokuje, chyba że klient poprosił. Sprzeczne.

3. **Koniec oferty: agent_08 wymaga pytania, agent_02a dopuszcza brak pytania.**
   agent_08 pkt 11: *„Brak naturalnego pytania na końcu oferty → ZŁAMANE"*. agent_02a sekcja `ZAKOŃCZENIE`: zakończeniem może być „zaproszenie do rozmowy bez konkretnego zadania". agent_08 odrzuci ofertę, którą agent_02a uzna za poprawną. Bezpośredni konflikt bramki z pisarzem.

4. **Tryb warunkowy vs twarda kwota.**
   agent_02a zakaz #14: *„Tryb warunkowy zamiast decyzji ('żeby wycenić dokładnie, musiałbym najpierw zobaczyć')"*. A jednocześnie agent_02a `STRUKTURA` i mechanika KROK 9.5 Wariant A wymagają podania jednej konkretnej kwoty i stawki 90 zł/h w treści. Pisarz ma jednocześnie być warunkowy i podać twardą cenę. Napięcie, które w praktyce kończy się albo złamaniem #14, albo niepodaniem ceny.

5. **„Tylko JSON" vs „pokaż rozbicie właścicielowi".**
   agent_02b: *„Zwróć WYŁĄCZNIE blok JSON. Żadnego tekstu przed ani po"*. mechanika KROK 10.6: *„Pokaż wynik audytu właścicielowi"* oraz końcówka: *„AI ZAWSZE pokazuje właścicielowi rozbicie: lista modułów → godziny → ... → kwota końcowa"*. Agent_02b nie ma jak tego pokazać, jeśli wolno mu tylko JSON. Brak miejsca w przepływie na raport rozbicia.

6. **Kto liczy: AI czy kalkulator?**
   agent_02b: *„Twoim zadaniem NIE jest liczenie kwoty... Kwotę i dni policzy deterministyczny kalkulator w Pythonie"*. mechanika KROK 9.5: *„AI samo ocenia zakres i decyduje o zakwalifikowaniu do wariantu A lub B"*, a KROK 10.5/10.6 opisują rozumowanie i audyt AI. Granica „AI decyduje / kalkulator liczy" jest narysowana różnie w obu plikach. Dla wariantu budżetu 50–250 zł decyzję podejmuje AI, ale nie jest jasne, czy robi to agent_02b, czy kalkulator.

7. **„Diagnoza, nie recepta" vs mechanika KROK 1 (poziom modułów).**
   agent_02a zakazuje zdradzania sposobu, a mechanika wymaga, by moduły były nazwane po funkcji (np. „Integracja zewnętrznego API (złożona, retry, queue)"), żeby wycena się spięła. Treść oferty musi nie zdradzić tego, co wycena musiała nazwać. Nie jest to twarda sprzeczność, ale w praktyce pisarz dostaje dwie przeciwne instrukcje na tym samym materiale.

8. **Zakaz widełek vs zbieranie widełek.**
   agent_01: *„CENY RYNKOWE... widełki dla FREELANCERÓW"*, mechanika tabela rynkowa to widełki („1500-3500 zł"). agent_02a zakaz #9 i agent_08 pkt 8: *„widełki → ZŁAMANE"*. Widełki są dozwolone na wejściu i zakazane na wyjściu. Formalnie spójne (widełki wewnętrzne), ale żaden plik nie mówi wprost „te widełki są tylko dla nas, wybierz jedną liczbę". Brak jawnego mostka.

9. **Blokada „Koszty serwera" agent_00 vs flaga `ograniczenia_api`.**
   agent_00: *„W pozostałych zleceniach ZAKAŻ pisania o kosztach utrzymania"*. agent_02b: flaga `ograniczenia_api` może być `true` na podstawie researchu i podnosi mnożnik ×1.15. Koszt API wpływa na cenę (mechanika), a agent_00 zabrania o nim mówić w ofercie. Cena rośnie z powodu, którego nie wolno klientowi wyjaśnić. Napięcie między wyceną a narracją.

10. **agent_00 „1-2 konkrety merytoryczne" vs „merytoryka domyślnie ZERO".**
    agent_00 `Format wyjściowy` pkt 2 zakłada, że zawsze są konkrety do poruszenia. agent_02a i agent_01 mówią, że domyślnie merytoryki nie ma i bywa, że research nie idzie do oferty: *„Wiedza zostaje dla nas, nie dla klienta"*. Orchestrator wymusza merytorykę, pisarz ją domyślnie wycina. Kolizja planu z egzekucją.

11. **Duplikat sekcji `DŁUGOŚĆ` w agent_02a.**
    Sekcja „## DŁUGOŚĆ" występuje dwukrotnie (raz przy „NIE KOPIUJ", raz przy „JĘZYK OFERTY"), z różnym brzmieniem. To nie sprzeczność merytoryczna, ale znak, że plik był łatany i nikt nie pilnuje jego spójności wewnętrznej.

12. **Jak_pisac_oferty pkt 5 vs agent_00 (portfolio przy pytaniu klienta).**
    jak_pisac_oferty pozwala odpowiedzieć wprost, że nie mamy portfolio. agent_00 zakazuje „jakichkolwiek wzmianek", agent_02a zakazuje „powoływania się". Trzy reżimy, brak jednoznacznej instrukcji dla przypadku „klient pyta wprost o portfolio".

---

## 4. Czy reguła „jedna spójna całość" jest spełniona

**Nie jest spełniona.** Trzy osie istnieją, ale są rozjechane: każda w osobnym pliku, w osobnym słowniku, bez wspólnego kontraktu przekazania. Wycena jest odcięta od narracji (02b → kalkulator → 02a to ślepe wklejenie kwoty). Orchestrator planuje merytorykę przed researchem. Bramka końcowa (08) wymaga czegoś, czego pisarz (02a) nie wymaga.

Co konkretnie dopisać i gdzie:

- **Wspólny kontrakt przekazania w agent_00.** Zamiast planować merytorykę w ciemno, agent_00 powinien planować „co ZABLOKOWAĆ" i „o co klient pyta", a decyzję „co dopisać" oddać agentowi_02a, który dostaje research. Ewentualnie przenieść agent_01 PRZED agent_00, żeby orchestrator widział miny i dopiero planował.

- **Sekcja w agent_02a: „JAK WPIĄĆ WYCENĘ".** Dopisać w `STRUKTURA` mostek: dostajesz z 02b `uzasadnienie` i flagi; jeśli cena jest pod 500 zł albo mocno odbiega od rynku, masz prawo i obowiązek uzasadnić ją w treści, nawet jeśli w innym miejscu obowiązuje „merytoryka ZERO". Rozstrzygnąć konflikt pkt 1 z listy sprzeczności.

- **Ujednolicić zakończenie.** albo agent_02a zawsze pisze pytanie (i usunąć „zaproszenie bez zadania"), albo agent_08 pkt 11 przestaje wymagać pytania. Obecnie bramka odrzuca poprawną ofertę.

- **Przekazać pytania z mechaniki KROK 11 do agent_02a.** Dodać w `ZAKOŃCZENIE` listę dobrych pytań zależnych od typu zlecenia, żeby 02a nie wymyślał ich od zera.

- **Sekcja „CO ZROBIĆ Z WIDEŁKAMI" w agent_01.** Wprost: widełki są materiałem wewnętrznym, do oferty wchodzi jedna liczba wybrana przez kalkulator.

- **Rozstrzygnąć etapowanie.** Jeden plik ma decydować, czy etapy wolno proponować. Rekomendacja: zostawić zakaz z mechaniki KROK 9.5 („chyba że klient poprosił") i usunąć „Zaproponuj podział na etapy" z agent_00 albo dopisać w agent_00 wyjątek „tylko gdy klient sam o to prosi".

- **Rozstrzygnąć „kto liczy".** agent_02b i mechanika muszą mieć tę samą granicę: co robi AI (rozpoznanie, moduły, flagi), co kalkulator (arytmetyka). Dziś dla wariantu 50–250 zł oba pliki roszczą sobie decyzję.

- **Odpowiedź na portfolio.** Dopisać w agent_02a jedno zdanie: „Jeśli klient wprost pyta o portfolio, odpowiedz wprost jednym zdaniem, że nie mamy publicznego portfolio". Dziś zakazy i jak_pisac_oferty mówią różne rzeczy.

---

## 5. Co jest ZA SZTYWNE (brzmi dobrze, w praktyce nienaturalne)

- **„Merytoryka domyślnie ZERO" + „ZERO nazw bibliotek" + „DIAGNOZA, NIE RECEPTA".** Trzy zakazy nakładają się i w praktyce uniemożliwiają napisanie czegokolwiek konkretnego nawet gdy klient zadał wprost pytanie techniczne. Sprzeczne z samym pkt 1 merytoryki („Klient wprost pyta → odpowiadasz"), bo odpowiedź na pytanie techniczne bez nazwania technologii jest często niemożliwa. To reguła, która brzmi jak asceza, a kończy się wymijającą odpowiedzią.

- **Zakaz nawiasów i myślników absolutny, bez wyjątku.** Dobry w teorii, ale w zleceniach technicznych naturalne jest „KSeF (XML)" albo „retry, queue". Zakaz zmusza do nienaturalnych konstrukcji typu „KSeF w wersji XML". Karanie minus 20 punktów za jeden nawias (jak_pisac_oferty pkt 1-2) jest sztywne.

- **agent_08 pkt 13: „więcej niż 2-3 wyraźne ludzkie akcenty → ZŁAMANE".** Liczenie „ludzkich akcentów" jest mechaniczne i sprzeczne z filozofią „naturalność to brak sztuczności, nie lista sztuczności" z tego samego punktu. Bot, który ma się zachowywać jak człowiek, dostaje licznik, który każe mu pilnować, ile razy był ludzki. To teatr kontroli nad teatrem.

- **„Zawsze pytanie na końcu" (agent_08) + „pytamy TYLKO o to, bez czego nie da się ruszyć" (agent_02a).** Zmuszanie do pytania, gdy nie ma realnej potrzeby, to dokładnie to, czego agent_02a chce uniknąć. Bramka wywraca intencję pisarza.

- **„Tryb warunkowy zamiast decyzji" (agent_02a #14) przy jednoczesnym wymogu jednej twardej kwoty i stawki 90 zł/h.** Reguła brzmi dojrzale, ale w starciu z obowiązkiem podania konkretnej ceny tworzy ofertę, która jednocześnie jest pewna ceny i niepewna wszystkiego innego. Klient to wyczuje jako brak zdecydowania.

- **Zakaz „wersji drugiej" + „wszystkie standardy bezpieczeństwa w cenie podstawowej" (mechanika KROK 0.5).** Brzmi jak uczciwość, ale przy zleceniach, gdzie klient sam sygnalizuje etapowanie albo budżet jest za mały, zmusza do wyceny pełnego zakresu powyżej budżetu klienta. Sztywne w praktyce przetargowej.

- **agent_00 „Kategorycznie ZAKAŻ" wzmianek o doświadczeniu, przy jednoczesnym wymogu budowania wiarygodności „konkretem technicznym".** Bez portfolio i bez wolno wspomnieć o doświadczeniu, jedynym budulcem zostaje diagnoza. W prostych zleceniach (typ „male", fix CSS) nie ma czego diagnozować, więc oferta staje się pusta. Reguła dobra dla Tier A, szkodliwa dla mikrozadań.

---

## Podsumowanie jednym akapitem

Trzy osie są zdefiniowane, ale nie tworzą spójnej całości: żyją w trzech plikach, w trzech słownikach, bez wspólnego kontraktu przekazania. Wycena jest odcięta od narracji. Znalazłem 12 sprzeczności między plikami, z których najgroźniejsze to: „merytoryka ZERO" kontra „uzasadnij cenę", „etapy dozwolone" kontra „etapy zakazane", „brak pytania = FAIL" kontra „zakończenie bez pytania dozwolone", oraz „tylko JSON" kontra „pokaż rozbicie właścicielowi". Reguła użytkownika nie jest spełniona i wymaga dopisania wspólnego kontraktu między agent_00, agent_01, agent_02a i agent_02b oraz rozstrzygnięcia sprzeczności w agent_08. W kilku miejscach prompty są też za sztywne (licznik ludzkich akcentów, absolutny zakaz nawiasów, wymuszone pytanie na końcu), co zmusza bota do nienaturalnego zachowania wbrew deklarowanej filozofii „pisz jak człowiek".















# Raport: Czy reguła „dopytaj tylko o najważniejsze, nie o wszystko" działa?

## 1. Gdzie jest mechanizm „pytamy TYLKO o to, bez czego nie da się ruszyć"

Mechanizm istnieje, ale jest rozproszony po trzech plikach i wyrażony jakościowo, nie operacyjnie.

**A) `agent_02a_opis_oferty.md`, sekcja TON I STYL (linia 84):**
> „Nie zgaduj. Im więcej zgadujemy, tym bardziej brzmimy jak AI i tym bardziej wyglądamy na desperatów. **Pytamy TYLKO o to, bez czego nie da się ruszyć.**"

**B) Ten sam plik, sekcja ZAKOŃCZENIE (linie 103–111):**
> „Zakończenie jest wynikiem analizy TEGO zlecenia. Może to być: **pytanie wynikające ze zlecenia, które realnie ułatwia ruszenie (i tylko wtedy, gdy bez odpowiedzi nie da się ruszyć)**"
> „Jeśli pytasz, uzasadnij po co pytasz (…)."

**C) `mechanika_wyceniania.md`, KROK 11 (linia 136):**
> „Pytania o skalę i kontekst (do wykorzystania jako Question CTA lub na priv, bez proponowania calli): dopasuj do typu zlecenia i ścieżki… **Nie pytaj o rzeczy oczywiste przy prostych zadaniach** (wizytówka, szybki fix)."

**D) `kryteria_audytu_100.md`, WYMIAR C (linie 30–34):** ocenia „**pytanie**" (liczba pojedyncza), jego trafność względem ogłoszenia oraz asynchroniczność. Nie ma tam jednak ani kary za wielokrotne pytania, ani progu liczbowego.

**Wniosek:** reguła „nie pytaj o wszystko" jest zapisana jako intencja („TYLKO", „bez czego nie da się ruszyć", „nie pytaj o oczywiste"), ale **nigdzie nie ma twardego limitu liczby pytań, definicji „najważniejszego" ani procedury selekcji przy wielu lukach**. To jest główna luka.

---

## 2. Ile pytań realnie zadaje bot (dowody z ofert)

Przeanalizowałem kilkanaście ofert z `01_ofertowarka/programowanie-i-it/`. Kluczowa obserwacja: **pytania merytoryczne to często jedno, ale prawie ZAWSZE doklejona jest propozycja calla/zdzwonienia**, co jest sprzeczne z Wymiarem C i żelaznym zakazem #7.

| ID | Typ | Zakończenie (CTA) | Ocena |
|---|---|---|---|
| 143916 | Landing premium, klient dał wszystko | „Możemy się zgadać na **krótki call przez Google Meet**" | Brak pytania (OK dla kompletnego), ale **call = złamanie zakazu #7 i WYMIARU C** |
| 144038 | Admin BaseLinker | „**Zdzwońmy się** w tym tygodniu na 15 minut" | Brak pytania merytorycznego + **call** |
| 144092 | Konfigurator 3D | „**Zdzwońmy się** … albo podeślij demo na priv" + próbka na fragmencie | **Call** + **próbka** (zlecenie nie o dokumentach) |
| 144514 | Salesforce↔WooCommerce | „Możemy się **zdzwonić** na 15 minut" | Brak pytania + **call** |
| 144867 | Aplikacja mobilna | „umówimy się na **krótką rozmowę wideo**" + „dopytam o kilka rzeczy" (ogólnik) | **Call** + pytanie niekonkretne |
| 144936 | Firebase deploy | „Podeślij mi na priv folder z aplikacją" | Nie pytanie, prośba o materiały — OK |
| 145024 | Aplikacja do nauki | „**W jakiej formie** mają Państwo teraz przygotowane zadania i scenariusze lekcji?" | **1 konkretne pytanie — wzorowo** |
| 145333 | Automatyzacja leadów | „**Jedno pytanie na start**… od czego zaczyna się dziś lead…?" | **1 konkretne pytanie — wzorowo** |
| 144737 | Sklep B2B PHP/MySQL | „potrzebuję: potwierdzenia czy WAPRO API aktywne, dostępu do testowego MSSQL, informacji czy są procedury/joby krytyczne **oraz zakresu nowej strony głównej**" + „Zdzwońmy się" | **4 pytania naraz** + **call** |

**Odpowiedź na pytanie „1–2 czy więcej?":** W większości ofert bot zadaje **0 lub 1 pytanie merytoryczne**, ale niemal zawsze dokłada **zaproszenie na call/zdzwonienie**, które formalnie nie jest pytaniem, ale jest zakazaną formą CTA. Jedyny realny przypadek „wielu pytań" to **144737** — tam bot zadał 4 pytania wprost (i to w zleceniu, gdzie klient sam prosił o odpowiedzi na punkty, więc częściowo jest to uzasadnione).

**Czy pytania są najważniejsze?** Przeważnie tak — 145024 i 145333 pytają dokładnie o brakującą oś (format danych wejściowych, początek procesu). Ale w 144867 pytanie jest ogólnikowe („dopytam o kilka rzeczy"), a w 144737 bot wybrał 4 rzeczy zamiast jednej, co jest już blisko błędu „pytania o wszystko".

---

## 3. Test na trzech typach zlecenia

**a) Zlecenie kompletne — czy bot NIE pyta?**
- **143916** (klient: „wszystkie informacje i materiały udostępnimy wybranemu oferentowi"): bot **nie zadaje pytania merytorycznego** — zachowanie poprawne. Problem: proponuje call, czego nie powinien.
- **144936** (klient podał cały zakres krok po kroku): bot **nie zadaje pytań**, prosi tylko o folder z plikami. **Poprawnie.**
- Werdykt: reguła „nie pytaj, gdy wszystko jest" **działa w warstwie pytań merytorycznych**, ale nie blokuje zaproszenia na rozmowę.

**b) Zlecenie z 1 kluczową luką — czy bot pyta o tę jedną?**
- **145024** (luka: format, w jakim klient trzyma zadania): bot pyta dokładnie o to — „W jakiej formie mają Państwo teraz przygotowane zadania i scenariusze lekcji?". **Poprawnie.**
- **145333** (luka: początek procesu leada): bot pyta dokładnie o to. **Poprawnie.**
- Werdykt: **działa dobrze.**

**c) Zlecenie z 5 lukami — czy bot wybiera najważniejsze?**
- **144737**: klient sam wystawił listę 5 oczekiwanych odpowiedzi, a bot dorzucił od siebie 4 pytania (WAPRO API, dostęp do MSSQL, procedury/joby, zakres strony głównej) i jeszcze zaproszenie na call. To **zachowanie graniczne** — bot nie zredukował do jednej najważniejszej rzeczy, tylko odtworzył listę.
- Werdykt: **ryzyko „pytania o wszystko" jest realne**, gdy zlecenie ma wiele luk. Brakuje mechanizmu wymuszającego wybór jednej najważniejszej.

---

## 4. Luki w promptach

1. **Brak limitu pytań.** Nigdzie nie ma zapisu „zadaj maksymalnie 1 pytanie" ani „nie więcej niż X". Liczba pojedyncza w ZAKOŃCZENIU („pytanie") sugeruje jedno, ale nie jest to twarde.
2. **Brak definicji „najważniejsze".** Kryterium „bez czego nie da się ruszyć" jest dobre, ale nie ma procedury: co zrobić, gdy luka jest 5 i wszystkie wydają się blokujące? Brak priorytetyzacji (np. „wybierz tę, która najbardziej zmienia wycenę/zakres").
3. **KROK 11 dostarcza listę pytań per typ zlecenia** („Dla sklepu: Ile SKU… Dla scrapera: Do jakiego formatu…"). Ryzyko: bot traktuje to jako **checklistę do wyczerpania** zamiast puli do wyboru jednego. Dokładnie to widać w 144737.
4. **Call jako domyślne CTA.** Prompt zakazuje calli (#7, WYMIAR C), a mimo to **7 z 9 przeanalizowanych ofert kończy się propozycją zdzwonienia/Meet/wideo**. To systemowy wyciek — najwyraźniej brakuje walidatora twardo karzącego za „zdzwońmy się", skoro bot go powtarza mimo zakazu.
5. **WYMIAR C ocenia tylko trafność i asynchroniczność**, nie ma kary za **liczbę** pytań. Audytor nie odbierze punktów za 4 pytania, jeśli są trafne.

---

## Rekomendacje (bez zmiany plików)

- Dodać do `agent_02a` twardy zapis: **maksymalnie 1 pytanie CTA; przy wielu lukach wybierz tę, która najbardziej zmienia zakres/wyceny, resztę przenieś do rozmowy priv.**
- Doprecyzować „najważniejsze" jako: *pytanie, którego brak odpowiedzi uniemożliwia podanie kwoty lub ruszenie z pracą.*
- W `kryteria_audytu_100.md` WYMIAR C dodać punkt karny za **więcej niż jedno pytanie** oraz za **jakąkolwiek propozycję calla/wideo/telefonu** (obecnie zapis jest, ale nie ma egzekucji — dowodem jest 7 ofert z „zdzwońmy się").
- KROK 11 oznaczyć wprost jako **pulę przykładów do wyboru jednego**, nie listę do wypełnienia.

Mam wszystkie 4 raporty. Odpowiadam wprost na Twoje pytanie, potem to, co znaleźli subagenci.

## Czy Twoja reguła zgadza się z promptami?

**Częściowo. Trzy z czterech osi są, ale rozjechane. Jedna jest w konflikcie.**

| Twoja oś | Stan w promptach | Werdykt |
|---|---|---|
| **Research z zlecenia, zero zgadywania** | Jest bramka ON/OFF w [agent_01](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) | ✅ Jest, ale ma luki |
| **Wycena warunkowa, stąd widełki** | Prompty zakazują widełek cenowych | ⚠️ Konflikt semantyczny |
| **Dopytaj tylko o najważniejsze** | Jest w [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md), ale bez limitu | ⚠️ Działa, ale wycieka |
| **Jedna spójna całość** | 12 sprzeczności między plikami | ❌ Nie jest spójna |

## Co znaleźli subagenci — najważniejsze

### 1. Konflikt „widełki" — do pogodzenia, nie do naprawy

Twoje „stąd widełki" **nie musi oznaczać widełek cenowych**. Prompty mają widełki, ale tylko **wewnętrzne (godzinowe)** — [mechanika_wyceniania](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 2: *„odczytaj widełki godzinowe"*. Do oferty wchodzi **jedna liczba**. Warunkowość wyrażasz **pytaniem**, nie ceną. To dokładnie pokrywa się z drugą częścią Twojej reguły („od czego zależy wycena, zawarte w pytaniach"). **Twoja reguła jest spójna — brakuje tylko zdania, które to wprost łączy.**

### 2. Bramka researchu pęka na dwóch typach zleceń

[agent_01](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) ma wewnętrzną sprzeczność: lista ON mówi *„duże zlecenie z realnym budżetem"*, lista OFF mówi *„dał materiały i wie czego chce"*. Duże zlecenie z materiałami **nie wiadomo, którą listę wybiera**.

Druga luka: **quick_fix (awaria, błąd 500) nie istnieje w bramce**. Bot spłaszcza go do „2 zdania" i wyłącza research, mimo że [selekcja_zlecen](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/selekcja_zlecen.md) traktuje to jako osobną, dochodową kategorię.

Trzecia: **„nazwa technologii to nie zaproszenie"** ucina znane miny. „Scraping z Allegro, 800 zł" → OFF → bot nie powie o anty-scrapingu, choć to obiektywna mina niezależna od klienta.

### 3. Dopytanie — działa, ale wycieka callami

Bot **poprawnie nie pyta**, gdy zlecenie jest kompletne (143916, 144936). **Poprawnie pyta o 1 kluczową lukę** (145024, 145333 — wzorowo). Ale:

- **Brak limitu pytań** — w 144737 bot zadał 4 pytania zamiast wybrać najważniejsze
- **7 z 9 ofert kończy się callem/zdzwonieniem** — mimo że [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) zakaz #7 tego zabrania. To systemowy wyciek — walidator tego nie łapie.

### 4. 12 sprzeczności między plikami — najgroźniejsze

1. **„Merytoryka ZERO"** vs **„uzasadnij cenę"** — [mechanika](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) każe uzasadnić niską kwotę, [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) każe milczeć
2. **Etapy**: [agent_00](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) pozwala przy dużych, [mechanika](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) zakazuje bez prośby klienta
3. **Koniec oferty**: [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) wymaga pytania (FAIL bez niego), [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) dopuszcza „zaproszenie bez zadania"
4. **Portfolio**: trzy pliki, trzy różne zachowania, gdy klient pyta wprost
5. **Kto liczy**: [agent_02b](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md) mówi „kalkulator", [mechanika](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 9.5 mówi „AI decyduje"
6. **„Tylko JSON"** ([agent_02b](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md)) vs **„pokaż rozbicie właścicielowi"** ([mechanika](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 10.6)

### 5. Co jest ZA SZTYWNE

- **Licznik „ludzkich akcentów"** (max 2-3, [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) pkt 13) — brzmi jak teatr kontroli nad teatrem. Bot ma być naturalny, a dostaje licznik naturalności
- **Absolutny zakaz nawiasów** — w zleceniach technicznych „KSeF (XML)" jest naturalne, zakaz zmusza do „KSeF w wersji XML"
- **Wymuszone pytanie na końcu** — gdy nie ma realnej potrzeby, bot pyta, żeby przejść bramkę. To sprzeczne z „pytamy TYLKO o to, bez czego nie da się ruszyć"
- **„Merytoryka ZERO" + „ZERO nazw bibliotek"** nakładają się — nawet gdy klient zada pytanie techniczne, trudno odpowiedzieć bez nazwania technologii

## Prawda, krótko

Twoja reguła **jest słuszna**, ale prompty:
- realizują ją **rozproszonie** (4 osie w 4 plikach, bez wspólnego kontraktu)
- mają **12 sprzeczności**, z których 3 są realnie szkodliwe (etapy, zakończenie oferty, merytoryka vs wycena)
- **wyciekają** w praktyce (call w 7/9 ofert mimo zakazu)
- mają **luki** (quick_fix w bramce researchu, brak limitu pytań, binarna flaga specyfikacji)

To nie jest „bot idealnie wie". To jest bot, który **ma dobre części, ale nie ma jednego mózgu** — każdy slot myśli osobno i nie przekazuje sobie kontekstu (orchestrator planuje merytorykę przed researchem, wycena nie wie dlaczego wyszła, pisarz nie zna pytań z mechaniki).

## Co proponuję dalej

Nie rzucam się na zmiany. Proponuję **etap naprawczy w kolejności ważności**:

1. **Rozstrzygnąć 3 szkodliwe sprzeczności** (etapy, zakończenie, merytoryka vs wycena) — to realnie psuje oferty
2. **Dodać wspólny kontrakt przekazania** między agent_00/01/02a/02b — żeby osie się widziały
3. **Dopiąć limit pytań i definicję „najważniejsze"** — konkretnie: max 1 pytanie CTA, wybór tej, która najbardziej zmienia zakres
4. **Naprawić bramkę researchu** — priorytet listy ON/OFF + quick_fix + wyjątek na obiektywne miny technologiczne
5. **Dodać mostek „warunkowość = pytanie, nie widełki"** w [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)

Chcesz, żebym:
- **(A)** zaczął od punktu 1 (3 szkodliwe sprzeczności) i pokazał Ci konkretne poprawki do akceptacji,
- **(B)** najpierw zrobił pełną mapę „co gdzie zmienić" w jednym pliku, żebyś ocenił całość przed jakąkolwiek edycją,
- **(C)** najpierw przedyskutował z Tobą punkt 1-2, bo to decyzje o architekturze bota, nie drobne poprawki?

Ja bym szedł **C → B → A**. Najpierw ustalamy kierunek (etapy? zakończenie? kto liczy?), potem mapa, potem edycja. Bo część z tych sprzeczności to nie błędy, tylko **niedokończone decyzje projektowe**, które Ty musisz podjąć.

---

**User**

Dobra zaproponuj mi wszystkie zmiany. 

**Assistant**

Napiszę pełną mapę propozycji w jednym dokumencie — żebyś ocenił całość przed jakąkolwiek edycją promptów. Nic jeszcze nie zmieniam.




Zapisałem pełny plan w [PLAN_NAPRAWY_PROMPTOW.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/PLAN_NAPRAWY_PROMPTOW.md). Nic nie zmieniłem w promptach — to czysta propozycja do akceptacji.

## Co zawiera

**Grupa A — 3 szkodliwe

---

**User**

tu mi napisz wszystko a nie w planie. 

**User**

tu mi napisz wszystko a nie w planie.

**Assistant**

Dobrze. Wszystko tutaj, bez pliku.

---

# PLAN NAPRAWY PROMPTÓW — pełna lista

## GRUPA A — TRZY SZKODLIWE SPRZECZNOŚCI

### A1. Etapy: agent_00 pozwala, mechanika zakazuje
**Pliki:** [agent_00_orchestrator.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) pkt 2 vs [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 9.5

**Obecnie:**
- agent_00: „Zaproponuj podział na etapy tylko wtedy, gdy projekt jest większy i wieloczęściowy"
- mechanika: „zakaz samowolnego dzielenia projektu na Fazę 1 / małe MVP, chyba że klient wprost w ogłoszeniu poprosił"

**Problem:** agent_00 autoryzuje etapy przy dużych projektach, mechanika je blokuje bez prośby klienta. Sprzeczne.

**Propozycja (GOTOWE):** Poprawić agent_00 na:
> „Podział na etapy tylko wtedy, gdy klient SAM o to wprost poprosił w ogłoszeniu. Sam nie proponuj etapowania na siłę. Przy dużych projektach możesz wspomnieć, że chętnie rozłożysz pracę, ale decyzję zostaw klientowi."

**Uzasadnienie:** zakaz z mechaniki jest spójny z realiami wyceny (wycena pełnego zakresu, brak wypychania do wersji drugiej). agent_00 musi być z nim zgodny.

---

### A2. Zakończenie oferty: agent_08 wymaga pytania, agent_02a dopuszcza brak
**Pliki:** [agent_08_weryfikacja_zasad.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) pkt 11 vs [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja ZAKOŃCZENIE

**Obecnie:**
- agent_08: „Brak naturalnego pytania na końcu oferty → ZŁAMANE"
- agent_02a: zakończeniem może być „zaproszenie do rozmowy bez konkretnego zadania"

**Problem:** agent_08 odrzuca ofertę, którą agent_02a uznaje za poprawną. Bot wpada w pętlę poprawek, gdy nie ma o co pytać.

**Propozycja (DO DECYZJI):**
- **Opcja 1 (twardsza):** agent_02a ZAWSZE pisze pytanie; usuwamy „zaproszenie bez zadania". Ryzyko: bot pyta na siłę.
- **Opcja 2 (zdrowsza):** agent_08 zmienia wymóg na: „Oferta kończy się pytaniem wynikającym ze zlecenia LUB, gdy klient dał wszystko, naturalnym zakończeniem bez pytania. Brak jakiegokolwiek zakończenia → ZŁAMANE."

**Moja rekomendacja:** Opcja 2.

---

### A3. Merytoryka ZERO vs uzasadnienie ceny
**Pliki:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) vs [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md)

**Obecnie:**
- agent_02a: „W każdym innym przypadku: ZERO merytoryki"
- mechanika: „Dla zleceń które naturalnie wychodzą poniżej 500 zł uczymy się pisać oferty tak, żeby uzasadnić tę kwotę"

**Problem:** jedna reguła każe milczeć, druga każe pisać uzasadnienie ceny. Konflikt przy tanich zleceniach.

**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja STRUKTURA:
> „Wyjątek od ZERO merytoryki: gdy kwota jest niska (poniżej 1000 zł) albo mocno odbiega od tego, co klient mógłby oczekiwać, masz prawo i obowiązek uzasadnić ją jednym zdaniem. Nie architekturą, tylko zakresem: co dokładnie wchodzi w cenę. To nie jest merytoryka, to wyjaśnienie wartości."

---

## GRUPA B — WSPÓLNY KONTRAKT PRZEKAZANIA

### B1. Orchestrator planuje merytorykę przed researchem
**Plik:** [agent_00_orchestrator.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md) pkt 2

**Obecnie:** agent_00 każe zaplanować „które 1 lub 2 konkrety merytoryczne warto poruszyć" — ale działa PRZED agent_01, więc nie zna jeszcze min.

**Problem:** plan merytoryczny powstaje w ciemno. Research przynosi minę, której orchestrator nie widział.

**Propozycja (DO DECYZJI):**
- **Opcja 1:** Przenieść agent_01 (research) PRZED agent_00.
- **Opcja 2:** Zmienić rolę agent_00 — niech planuje tylko „co ZABLOKOWAĆ" i „o co klient pyta", a decyzję „co dopisać" odda agentowi_02a.

**Moja rekomendacja:** Opcja 2.

---

### B2. Wycena odcięta od narracji
**Pliki:** [agent_02b_wycena_dni.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md) → [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)

**Obecnie:** 02b liczy moduły i flagi, ale 02a nie wie, dlaczego wyszła taka kwota. Pisarz dostaje tylko `[WYNIK_KONCOWY]`.

**Propozycja (GOTOWE):** Dodać do agent_02a sekcję „JAK WPIĄĆ WYCENĘ":
> „Dostajesz z 02b pole `uzasadnienie` i flagi. Jeśli cena jest pod 1000 zł albo mocno odbiega od rynku, wpleć jedno zdanie wyjaśnienia (patrz A3). W pozostałych przypadkach nie tłumacz ceny, po prostu ją podaj."

---

### B3. Pytania z mechaniki KROK 11 nie trafiają do agent_02a
**Pliki:** [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 11 → [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)

**Obecnie:** mechanika ma gotowe pytania per typ zlecenia, ale agent_02a ich nie zna.

**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja ZAKOŃCZENIE:
> „Masz pulę dobrych pytań z mechaniki wyceniania (KROK 11). To PULA DO WYBORU, nie lista do wypełnienia. Wybierz JEDNO najważniejsze dla tego zlecenia. Reszta zostaje na rozmowę priv."

---

## GRUPA C — LIMIT PYTAŃ I DEFINICJA „NAJWAŻNIEJSZE"

### C1. Brak limitu pytań
**Plik:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja ZAKOŃCZENIE

**Obecnie:** „pytanie wynikające ze zlecenia" (liczba pojedyncza, ale nie twardy limit). Dowód: oferta 144737 zadała 4 pytania.

**Propozycja (GOTOWE):** Dopisać twardy limit:
> „Maksymalnie JEDNO pytanie CTA w ofercie publicznej. Jeśli widzisz kilka luk, wybierz tę, która najbardziej zmienia zakres lub wycenę. Resztę zadaj w wiadomości prywatnej albo zostaw na później."

---

### C2. Brak definicji „najważniejsze"
**Plik:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)

**Obecnie:** „bez czego nie da się ruszyć" — dobre, ale nieostre przy 5 lukach.

**Propozycja (GOTOWE):** Dopisać definicję:
> „Najważniejsze pytanie to takie, którego brak odpowiedzi uniemożliwia podanie wiążącej kwoty albo rozpoczęcie pracy. Jeśli dwie luki wydają się równie ważne, wybierz tę, która bardziej zmienia wycenę."

---

### C3. Wyciek calli mimo zakazu
**Pliki:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) zakaz #7, [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) WYMIAR C

**Obecnie:** zakaz #7 zabrania calli, ale 7 z 9 realnych ofert kończy się „zdzwońmy się". Zakaz jest, egzekucji nie ma.

**Propozycja (GOTOWE):** Wzmocnić agent_08 pkt 11:
> „Propozycja rozmowy telefonicznej, calla, spotkania online, Google Meet, Zoom lub wideokonferencji (o ile klient sam tego nie zażądał) → ZŁAMANE z karą -20 pkt. Dotyczy każdej formy: zdzwońmy się, umówmy się na rozmowę, krótki call, spotkanie online."

---

## GRUPA D — BRAMKA RESEARCHU

### D1. Wewnętrzna sprzeczność listy ON/OFF
**Plik:** [agent_01_research.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) CZĘŚĆ A

**Obecnie:** lista ON ma „duże, złożone zlecenie z realnym budżetem", lista OFF ma „dał materiały i wie dokładnie czego chce". Duże zlecenie z materiałami nie wiadomo, którą listę wybiera.

**Propozycja (GOTOWE):** Dodać priorytet:
> „Gdy zlecenie spełnia kryterium z OBU list jednocześnie, rozstrzyga obecność procesu albo pytania. Jeśli klient opisał proces lub zadał pytanie → ON. Jeśli tylko dał materiały i wie czego chce, bez opisu procesu i bez pytania → OFF. Sama duża skala i budżet to za mało na ON."

---

### D2. quick_fix nieobsłużony w bramce
**Plik:** [agent_01_research.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) CZĘŚĆ A

**Obecnie:** bramka nie ma kategorii „awaria / konkretny błąd produkcyjny". Quick_fix spłaszcza się do „2 zdania" → OFF.

**Propozycja (GOTOWE):** Dodać do listy ON:
> „Zgłoszenie konkretnej awarii lub błędu produkcyjnego (np. błąd 500, skrypt pada, system nie działa po aktualizacji). Nawet krótkie, bo konkret błędu to zaproszenie do researchu znanych przyczyn i regresji."

---

### D3. „Nazwa technologii to nie zaproszenie" ucina obiektywne miny
**Plik:** [agent_01_research.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) CZĘŚĆ A

**Obecnie:** „sama nazwa technologii to NIE jest zaproszenie do merytoryki. Nazwa bez procesu i bez pytania to za mało."

**Problem:** „Chcę scraping z Allegro, 800 zł" → OFF → bot nie powie o anty-scrapingu, choć to obiektywna mina.

**Propozycja (GOTOWE):** Dodać wyjątek:
> „Wyjątek od tej zasady: jeśli technologia z ogłoszenia ma OBIEKTYWNĄ, powszechnie znaną minę niezależną od procesu klienta (np. brak oficjalnego API Allegro, anty-scraping, rate-limit, wymóg licencji), research może być ON nawet bez opisu procesu. Mina obiektywna to nie zgadywanie."

---

### D4. ON przy procesie bez potencjału na merytorykę
**Plik:** [agent_01_research.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_01_research.md) CZĘŚĆ A

**Obecnie:** „opisał swój proces" → ON, nawet gdy proces jest rutynowy i nie ma min.

**Propozycja (GOTOWE):** Dopisać:
> „Opisany proces to zaproszenie do researchu tylko wtedy, gdy proces ma potencjał na minę, alternatywę albo realne pytanie. Proces rutynowy, bez haczyka, nie wymaga researchu, możesz zwrócić BRAK_ISTOTNYCH_FAKTOW nawet przy ON."

---

## GRUPA E — MOSTEK „WARUNKOWOŚĆ = PYTANIE, NIE WIDEŁKI"

### E1. Brak zdania łączącego wycenę warunkową z pytaniem CTA
**Pliki:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md), [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md)

**Obecnie:** prompty zakazują widełek cenowych (słusznie), ale nie mówią wprost „warunkowość wyrażaj pytaniem".

**Propozycja (GOTOWE):** Dopisać w agent_02a, sekcja STRUKTURA:
> „Wycena jest jedna, konkretna kwota. Warunkowość wyceny komunikujesz PYTANIEM, nigdy widełkami ceny. Gdy pytasz o brakujący parametr, powiedz wprost, od czego zależy cena: od tego zależy, czy zmieścimy się w X czy potrzebne będzie Y. Ale nadal podaj jedną kwotę, nie widełki."

---

## GRUPA F — ZA SZTYWNE REGUŁY

### F1. Licznik „ludzkich akcentów"
**Plik:** [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) pkt 13

**Obecnie:** „więcej niż 2-3 wyraźne ludzkie akcenty → ZŁAMANE". Sprzeczne z filozofią „naturalność to brak sztuczności".

**Propozycja (DO DECYZJI):**
- **Opcja 1:** Usunąć licznik, zostawić tylko test „wzorzec bez triggera to teatr".
- **Opcja 2:** Zmienić na miękki sygnał: „Jeśli oferta ma wrażenie przesytu ludzkimi wtrąceniami, wskaż do redukcji, ale nie odrzucaj z tego powodu".

**Moja rekomendacja:** Opcja 1.

---

### F2. Absolutny zakaz nawiasów
**Pliki:** [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) zakaz #2, [agent_08](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md) pkt 2

**Obecnie:** zero nawiasów, kara -20 pkt za jeden. W zleceniach technicznych „KSeF (XML)" jest naturalne.

**Propozycja (DO DECYZJI):**
- **Opcja 1:** Zostawić absolutny zakaz (spójny, prosty do walidacji).
- **Opcja 2:** Dopuścić nawiasy WYŁĄCZNIE wokół skrótów technicznych (max 1-2 w ofercie).

**Moja rekomendacja:** Opcja 1.

---

### F3. Wymuszone pytanie na końcu
Rozwiązane w A2.

---

### F4. „Merytoryka ZERO" + „ZERO nazw bibliotek" nakładają się
**Plik:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) sekcja MERYTORYKA + JAK PODAWAĆ MERYTORYKĘ

**Obecnie:** trzy zakazy nakładają się i uniemożliwiają odpowiedź na pytanie techniczne bez nazwania technologii.

**Propozycja (DO DECYZJI):**
- **Opcja 1:** Złagodzić „ZERO nazw bibliotek" na „nazwy bibliotek tylko gdy klient sam je wymienił albo są niezbędne do odpowiedzi na jego pytanie".
- **Opcja 2:** Zostawić jak jest, ale dopisać wyjątek: „Gdy klient zadał pytanie techniczne wprost, odpowiedź może zawierać nazwy technologii, bo inaczej odpowiedź jest wymijająca".

**Moja rekomendacja:** Opcja 2.

---

### F5. Binarna flaga `brak_specyfikacji`
**Pliki:** [agent_02b_wycena_dni.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md), [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 5

**Obecnie:** flaga true/false. „Częściowe" (proces + brak 2-3 parametrów) wpada w tę samą kategorię co „kompletne" albo „otwarte".

**Propozycja (DO DECYZJI):**
- **Opcja 1:** Rozszerzyć na trzystanową: `kompletna` / `czesciowa` / `otwarta` z mnożnikami ×0.90 / ×1.0 / ×1.05.
- **Opcja 2:** Dodać drugą flagę `specyfikacja_czesciowa` z osobnym mnożnikiem.

**Moja rekomendacja:** Opcja 1.

---

## GRUPA G — POZOSTAŁE SPRZECZNOŚCI

### G1. Portfolio: trzy różne reżimy w trzech plikach
**Pliki:** [agent_00](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md), [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md) zakaz #5, [jak_pisac_oferty](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md) pkt 5

**Propozycja (GOTOWE):** Ujednolicić: „Jeśli klient wprost pyta o portfolio, odpowiedz jednym zdaniem: nie mamy publicznego portfolio. W żadnym innym wypadku nie wspominaj o portfolio ani doświadczeniu."

---

### G2. Kto liczy: AI vs kalkulator
**Pliki:** [agent_02b](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md), [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 9.5

**Propozycja (GOTOWE):** Ujednolicić granicę: „AI rozpoznaje zlecenie, dobiera moduły i flagi. Kalkulator liczy kwotę. Decyzję o wariancie A/B dla budżetów 50-250 zł podejmuje AI (agent_02b), kalkulator tylko wykonuje." Dopisać w obu plikach.

---

### G3. „Tylko JSON" vs „pokaż rozbicie właścicielowi"
**Pliki:** [agent_02b](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md), [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 10.6

**Propozycja (GOTOWE):** Dopisać w mechanice: „Rozbicie kalkulatora jest logowane automatycznie przez kod, nie przez agenta. Agent_02b zwraca tylko JSON."

---

### G4. Koszty serwera: agent_00 zabrania, mechanika podnosi cenę
**Pliki:** [agent_00](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_00_orchestrator.md), [agent_02b](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02b_wycena_dni.md) flaga `ograniczenia_api`

**Propozycja (GOTOWE):** Dopisać w agent_00: „Koszty API mogą wpłynąć na cenę (flaga `ograniczenia_api`), ale w ofercie wspominasz o nich TYLKO gdy klient sam pyta o koszty albo gdy są istotne dla jego decyzji."

---

### G5. Duplikat sekcji DŁUGOŚĆ w agent_02a
**Plik:** [agent_02a_opis_oferty.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md)

**Propozycja (GOTOWE):** Usunąć duplikat, zostawić jedną wersję.

---

### G6. Diagnoza, nie recepta vs moduły w mechanice
**Pliki:** [agent_02a](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/generatory/agent_02a_opis_oferty.md), [mechanika_wyceniania.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/mechanika_wyceniania.md) KROK 1

**Propozycja (GOTOWE):** Nie zmieniać, to napięcie, nie sprzeczność. Dopisać w agent_02a: „Moduły z wyceny są wewnętrzne. W ofercie mówisz o nich językiem korzyści, nie nazwami modułów."

---

## PODSUMOWANIE

**18 zmian GOTOWYCH** (bez decyzji): A1, A3, B2, B3, C1, C2, C3, D1, D2, D3, D4, E1, G1, G2, G3, G4, G5, G6

**6 zmian DO DECYZJI:**

| # | Decyzja | Moja rekomendacja |
|---|---|---|
| A2 | Zakończenie bez pytania: twarde czy miękkie? | **miękkie** |
| B1 | Research przed orchestratorem czy zmiana roli 00? | **zmiana roli 00** |
| F1 | Licznik ludzkich akcentów: usunąć czy złagodzić? | **usunąć** |
| F2 | Zakaz nawiasów: zostawić czy dopuścić techniczne? | **zostawić** |
| F4 | Nazwy bibliotek przy pytaniu: złagodzić czy wyjątek? | **wyjątek** |
| F5 | Flaga specyfikacji: trzystanowa czy druga flaga? | **trzystanowa** |

Powiedz które decyzje zmieniasz i czy akceptujesz resztę, to wdrażam.

---

