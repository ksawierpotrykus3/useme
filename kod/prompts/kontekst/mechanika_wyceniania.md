Plik zawiera kompletną mechanikę wyceniania zleceń. AI podąża za algorytmem krok po kroku. Żadnych zgadywanek, żadnych kwot z powietrza.

Mechanika wyceniania zleceń oparta na realnym nakładzie pracy. AI podąża za algorytmem krok po kroku:

## Małe zlecenia (szybka wygrana AI robi samo)

Jeśli zlecenie da się zrobić AI w kilka godzin (automatyzacja Make/n8n, prosta integracja API, fix pixeli, embed widgetu, konfiguracja no-code) NIE licz godzin × stawka, bo AI robi szybciej niż człowiek i wyjdzie absurdalnie tanio. Weź stawkę rynkową za wynik, nie za czas.

Tabela rynkowa dla małych zleceń:
- Prosty landing page / strona wizytówka One-Page: 1500-3500 zł
- Automatyzacja Make/n8n (3-5 kroków, 1-2 integracje): 600-1500 zł
- Prosta integracja API (2 endpointy, webhook, sync jednego kierunku): 400-800 zł
- Fix pixeli/GTM/tracking (Meta Pixel, TikTok, consent mode, data layer): 400-800 zł
- Embed/integracja no-code (Typeform, Calendly, widgety na CMS): 250-500 zł
- Konfiguracja platformy e-commerce (BaseLinker, Shoper, IdoSell akcje, automatyzacje, reguły): 800-2000 zł
- Stworzenie sklepu na platformie SaaS od zera (Shopify/Shoper/IdoSell full setup: produkty, integracje, płatności, szkolenie): 3000-8000 zł
- Content/SEO techniczne (meta tagi, schema, sitemap): 400-1000 zł
- Prosty bot/skrypt (scraper bez anty-detekcji, prosty automat): 500-1200 zł

Zawsze minimum 500 zł nigdy nie schodzimy niżej, nawet jeśli tabela pokazuje dolną granicę. Nie ścigamy się z desperatami dającymi 270 zł: klient który wybiera najtańszą ofertę dostaje fuszerkę i i tak wróci. Sprzedajemy wynik, nie czas klikania.

Granica: jeśli zlecenie wymaga pisania kodu przez senior developera dłużej niż ~8-12h (aplikacja, system, złożona integracja, SaaS) idziesz w KROK 0.5 i liczysz godziny × stawka. Jeśli to konfiguracja/automatyzacja którą AI ogarnia szybko tabela wyżej.

## Zlecenia abonamentowe / stała współpraca (retainer)

Nie każde zlecenie jest jednorazowym projektem. Jeśli ogłoszenie dotyczy stałej opieki, administracji, wsparcia lub roli typu "customer success", "opiekun techniczny", "administrator" NIE liczysz modułów ani godzin jednorazowo. Wyceniasz stawką MIESIĘCZNĄ:

- Opieka techniczna / administrator (BaseLinker, Shoper, IdoSell, hosting, reagowanie na awarie): 1500-2500 zł/mies.
- Customer success / wdrożenia AI / wsparcie klientów B2B: 2500-5000 zł/mies.

W polu kwoty na Useme wpisujesz kwotę miesięczną, a w treści oferty jasno zaznaczasz, że to stała współpraca rozliczana miesięcznie. Dni pracy: minimum 7 (wymóg formularza). Jeśli klient oczekuje SLA dłuższego niż 1 miesiąc gwarancji to również pozycja abonamentowa, nie buffer.

KROK 0.5: Oceń realny zakres zlecenia (CONFIRMED SCOPE). Do kalkulacji godzin wliczaj pełny zakres wymagany do rzetelnego, produkcyjnego dostarczenia tego, o co prosi klient. UWAGA KRYTYCZNA: Standardy inżynierskie i zabezpieczenia (np. walidacja groszowa VAT, deduplikacja dokumentów, obsługa KSeF XML vs OCR, Praca Rozproszona XML, kolejkowanie, idempotencja webhooków, weryfikacja Białej Listy) są INTEGRALNĄ częścią naszego rzemiosła w cenie podstawowej — NIGDY nie wyrzucaj ich do osobnej listy „potencjalnych rozszerzeń w wersji drugiej (v2)" i nigdy nie pisz klientowi, że wyceniasz je osobno!

KROK 1: Rozłóż CONFIRMED SCOPE na moduły. Moduł to logicznie wydzielona część systemu, która ma własną odpowiedzialność i mogłaby być przypisana do innego developera bez konieczności ciągłej koordynacji z developerem reszty systemu. Jeśli funkcjonalność B nie może istnieć ani być rozwijana niezależnie od A to B jest sub-featurem A, nie osobnym modułem. Przykład: "integracja tPay" to moduł (inny dev mógłby to robić), "auto-cancel po 60 min" to sub-feature integracji tPay (wymaga tej samej wiedzy o lifecycle płatności). Edge cases, obsługa błędów, fallbacki i walidacje graniczne NIE są osobnym modułem są pokryte przez bazowe godziny modułu, buffer (+20-30%) i narzut QA (+15-20%).

WAŻNE dla ERP i złożonych integracji: jeśli klient wymienia w ogłoszeniu kilka ponumerowanych punktów zakresu (np. "1. konfiguracja, 2. eksporty, 3. własne kontrolery"), mapuj KAŻDY punkt na osobny moduł z tabeli. Dla ERP/integracji obowiązuje reguła odwrotna niż dla landingów: NIE scalaj ich w jeden moduł tylko po to, żeby było krócej. Przykład enova365: (1) uruchomienie i konfiguracja WebAPI - Integracja zewnętrznego API (1 serwis): 4-10h; (2) cykliczne eksporty/zadania harmonogramu - Integracja zewnętrznego API (złożona, retry, queue): 10-20h; (3) własne kontrolery C#/.NET dla logiki marży - Integracja zewnętrznego API (złożona) + praca z SDK: 10-20h. To trzy moduły, nie jeden.

KROK 2: Dla każdego modułu dopasuj do kategorii z tabeli i odczytaj widełki godzinowe (optymistycznie realistycznie). Godziny skalibrowane na podstawie realnych danych od senior developera (AI-augmented coding: AI pisze kod, senior developer debuguje i prowadzi). Po przypisaniu godzin sprawdź NAKŁADANIE: czy jakiekolwiek dwa moduły współdzielą logikę, tabele lub endpointy? Jeśli tak scal je w jeden moduł z jednym widełkiem godzinowym LUB przypisz wspólną logikę do jednego z nich i odejmij z drugiego. Nigdy nie licz tych samych godzin dwa razy.

Landing page / One-Page (komplet: sekcje, formularz, responsywność RWD, konfiguracja hostingu/deploy): 14-22h. TWARDA REGUŁA: dla One-Page NIE rozbijamy projektu na osobne moduły UX/SEO/deploy - to są sub-feature'y wliczone w te godziny. Landing page to JEDEN moduł, nie pięć. UWAGA: ta reguła dotyczy WYŁĄCZNIE Landing Page / One-Page. Dla systemów ERP, złożonych integracji i aplikacji obowiązuje reguła odwrotna - patrz niżej.
VPS deploy + konfiguracja (nginx, SSL, systemd, firewall, backup): 4-8h.
Migracja bazy danych (schema + dane + walidacja): 4-12h.
CRUD moduł prosty (jedna encja, lista + formularz + edycja + usuwanie): 4-8h.
CRUD moduł złożony (relacje, walidacje, filtry, sortowanie, paginacja): 6-12h.
Auth + role + uprawnienia: 4-8h.
Panel admina basic (CRUD użytkowników, moderacja, statystyki): 6-10h.
Panel admina rozbudowany (workflow, audit log, raporty, masowe operacje): 12-20h.
Czat real-time (WebSocket, historia, powiadomienia): 16-24h.
Geolokalizacja + mapa interaktywna (Leaflet/MapLibre, markery, tracking): 12-20h.
Upload plików/zdjęć (kompresja, storage, podgląd): 4-8h.
Upload video (kompresja server-side, streaming, thumbnail): 12-20h.
Integracja płatności (Stripe/Przelewy24, webhook, lifecycle): 8-16h.
Integracja zewnętrznego API (1 serwis, auth + CRUD): 4-10h.
Integracja zewnętrznego API (złożona, retry, error handling, queue): 10-20h.
OCR/AI moduł (ekstrakcja danych z dokumentów, walidacja): 8-16h.
AI chatbot z bazą wiedzy (LangChain/RAG, embeddings, prompt engineering): 16-30h.
AI chatbot + integracje (CRM, Slack, mail, human handoff): 24-40h.
Bot/scraper z anty-detekcją (proxy rotation, rate limiting, stealth): 16-30h.
Powiadomienia (email + push + in-app): 6-12h.
Raporty PDF (generowanie, szablony, eksport): 6-12h.
System subskrypcyjny (Stripe, plany, trial, webhook lifecycle): 12-20h.
Multi-tenant izolacja danych (schema-per-tenant lub RLS): 12-24h.
Migracja sklepu e-commerce (ekstrakcja + import + redirecty + weryfikacja): 40-80h.
WordPress/CMS customizacja (motywy, wtyczki, integracje): 8-20h.
WordPress premium redesign + SEO (przebudowa, CWV, architektura informacji): 20-40h.
Projekt graficzny/UX (autorska oprawa, mockupy, system komponentów): 10-30h.
SEO techniczne jako osobny moduł (audyt, meta, schema, CWV, redirecty): 6-16h.
Interaktywny element (kalkulator, konfigurator, quiz): 6-16h.
Automatyzacja AI-LLM (ekstrakcja/generowanie treści, klasyfikacja dokumentów): 4-8h.
Orkiestracja między 2+ integracjami (saga pattern, compensating actions, cross-service state machine): dodaj +30% do godzin WIĘKSZEGO z modułów integracyjnych. NIE twórz osobnego modułu dodaj godziny do istniejącego.

KROK 2.5: Testy + dokumentacja: dodaj +15% do sumy godzin wszystkich modułów.

KROK 3: Zsumuj godziny ze wszystkich modułów. Wynik to dwie liczby: suma optymistyczna i suma realistyczna.

KROK 4: Dodaj buffer. Buffer to rezerwa na rzeczy które pójdą nie tak bug, zmiana wymagań, API które nie działa jak w dokumentacji. Buffer pokrywa również standardowy 1 miesiąc gwarancji/bugfixów po oddaniu projektu. Jeśli klient wymaga dłuższego SLA (3-6 miesięcy) wyceniaj to jako osobną pozycję abonamentową, nie wliczaj w buffer.

ZWYKŁE STRONY WWW, LANDING PAGE, TYPOWE SKLEPY I SKRYPTY INTEGRACYJNE TO ZAWSZE BUFOR STANDARDOWY +20%. Nowy klient to NIE jest "nowa technologia". Bufor +30% wolno zastosować WYŁĄCZNIE wtedy, gdy zespół dotyka niszowej technologii, z którą nigdy wcześniej nie pracował (np. niszowy ERP typu enova365/SAP). Brak specyfikacji rozliczamy WYŁĄCZNIE mnożnikiem w KROKU 5 (×1.05), a NIE podnoszeniem bufora w KROKU 4. Nigdy nie stosuj obu naraz za ten sam powód.

KROK 5: Zastosuj mnożnik ryzyka do sumy godzin realistycznych (po buforze) za pomocą funkcji `max()` (wybieramy najwyższy pojedynczy czynnik ryzyka, bez kaskadowego mnożenia), z twardym sufitem `MAX_RISK_MULTIPLIER = 1.15`:

- Klient ma Figmę + szczegółową specyfikację: `×0.90` (mniej niewiadomych, szybsza praca).
- Klient nie ma specyfikacji (opisał problem ogólnie, brak mockupów): `×1.05`.
- Zewnętrzne API ze znanymi ograniczeniami architektonicznymi: `×1.05` (jeśli w modułach wyceniono już osobny moduł integracji API/ERP) lub `×1.15` (gdy brak osobnego modułu API).
- Funkcje real-time (WebSocket, live tracking, collaborative editing): `×1.10`.

CAP: łączny mnożnik ryzyka nigdy nie przekracza `×1.15` (`MAX_RISK_MULTIPLIER = 1.15`).

KROK 6: Oblicz cenę bazową. Godziny realistyczne (po buforze i mnożnikach) × stawka efektywna = cena bazowa.

Stawka efektywna jest stała i jednolita dla wszystkich zleceń:
- Obowiązuje wyłącznie jedna stawka godzinowa wszędzie: **90 zł/h** (zarówno dla zleceń Tier B, jak i Tier A: ERP, KSeF, AI/LLM, scraping, Three.js 3D, reverse engineering). Nie stosujemy żadnych innych stawek godzinowych.

KROK 7: Korekta konkurencyjna.
ZASADA ANTY-DUMPINGOWA: Całkowicie likwidujemy zbijanie ceny w dół z powodu dużej liczby konkurentów (koniec z mnożnikami 0.85 i 0.90). Wyścig na dno niszczy marżę i przyciąga trudnych klientów.
- Świeże zlecenie (<3 dni) z małą konkurencją (<=10 ofert): mnożnik `1.05` (+5% marży na szybki start).
- Zlecenia ze standardową lub dużą konkurencją (>10 ofert): mnożnik `1.0` (trzymamy profesjonalną cenę).
- Zlecenie stare (>3 dni) i mało ofert (<10): mnożnik `1.15` (nisza trudna, brak chętnych wykonawców = wyższa wycena wartości).

KROK 8: Uwzględnij prowizję Useme i podatek. Z wpisanej kwoty Useme zabiera ~2.3% prowizji, potem PIT zjada kolejne ~9.6%. Realnie na koncie ląduje ~88% tego co wpiszesz w formularz. Jeśli chcesz dostać konkretną kwotę netto podziel ją przez 0.88 i tyle wpisz jako wycenę. Nie winduj sztucznie po prostu bądź świadomy że 10 000 zł na Useme to ~8 800 zł w kieszeni.

KROK 9: Zaokrąglij kwotę końcową. Zbyt okrągła kwota wygląda na zgadywankę (10 000 zł). Zbyt precyzyjna wygląda dziwnie (9 847 zł). Zasada:

Projekty do 2 000 zł: zaokrąglaj do 50 zł (np. 1 350 zł, 1 800 zł).
Projekty 2 000 - 10 000 zł: zaokrąglaj do 500 zł (np. 4 500 zł, 7 000 zł).
Projekty ponad 10 000 zł: zaokrąglaj do 1 000 zł (np. 12 000 zł, 18 000 zł).

KROK 9.5: Kotwica budżetu klienta i dekodowanie stawek godzinowych.
Dotychczasowe kroki liczyły KOSZT pracy w ciemno. Jeśli klient podał JAWNY budżet w ogłoszeniu:

1. DEKODOWANIE BUDŻETÓW 50–250 ZŁ (OCENA KONTEKSTOWA AI):
Budżet w przedziale 50–250 zł (np. 100 zł, 150 zł) na Useme to heurystyka, którą AI ocenia kontekstowo na podstawie zakresu:
- **Wariant A (Stawka godzinowa PLN/h):** Gdy zlecenie dotyczy stałej współpracy, wielu modułów, rozwoju aplikacji, wdrożenia AI czy bota. Wtedy kwota ta w ogłoszeniu oznacza, że klient szuka rozliczenia godzinowego – u nas jedyną obowiązującą stawką jest zawsze **90 zł/h**. Całkowitą cenę ofertową wyliczamy jako godziny × 90 zł/h dla pełnego zakresu zlecenia (w treści oferty podajemy kwotę całkowitą oraz stawkę 90 zł/h).
- **Wariant B (Mikrozadanie Fixed-Price):** Gdy klient wprost szuka wykonawcy do drobnej, jednorazowej poprawki (np. zmiana koloru w CSS, podmiana favicony, poprawka literówki). Wtedy NIE mnożymy godzin przez stawkę, lecz traktujemy to jako małe zlecenie (typ „male”) z wyceną rynkową z tabeli małych zleceń (minimum 500 zł).
AI samo ocenia zakres i decyduje o zakwalifikowaniu do wariantu A lub B.

2. BUDŻETY CAŁKOWITE (> 250 zł):
- Jeśli budżet klienta jest wyższy niż Twoja cena bazowa: celuj w 80-90% budżetu klienta (z capem 1.4x wyceny bazowej, aby nie przestraszyć klienta przeskokiem cenowym).
- Jeśli budżet klienta jest niższy niż Twoja cena bazowa: nie składaj oferty poniżej rentowności. Zawsze wyceniaj pełny zakres zlecenia (zakaz samowolnego dzielenia projektu na „Fazę 1 / małe MVP", chyba że klient wprost w ogłoszeniu poprosił o etapowanie/MVP lub rynek pod zleceniem tak wycenia).
- Jeśli budżet to "do negocjacji": pole kwoty wypełnia Twoja cena bazowa z KROK 7-9.
- Nigdy nie obniżaj ceny bazowej poniżej 500 zł.

KROK 10: Oblicz dni kalendarzowe. senior developer wyciąga 6-12 produktywnych godzin dziennie zależnie od momentum kiedy widzi postępy ciągnie nawet kilkanaście, kiedy utknął na debuggingu AI-generowanego kodu to kilka. Dla estymaty używaj 7h/dzień jako średnią. Dni = godziny realistyczne (po buforze i mnożnikach) ÷ 7, zaokrąglone w górę. Do tego dodaj +30% na weekendy i komunikację z klientem. Jeśli klient sygnalizuje pilność i jest gotów dopłacić senior developer może pracować dniami i nocami, wtedy dzielimy dni przez 2 ale nie obniżamy ceny (klient płaci za priorytet, nie za godziny). Nigdy nie oferuj tego jako opcji z góry tylko gdy klient sam mówi że się spieszy.

KROK 10.5 (opcjonalny): Sanity check z senior developerem. AI ZAWSZE oblicza własną wycenę NAJPIERW, w ciemno, bez patrzenia na kwoty podane wcześniej w rozmowie przez właściciela, senior developera lub klienta. ZABRANIA SIĘ modyfikowania buforów, mnożników ani godzin modułów aby zbliżyć wynik do kwoty podanej z instynktu. Dopiero po uzyskaniu własnego wyniku porównaj z instynktem senior developera (jeśli dostępny). Jeśli różnica wynosi >30%, AI MUSI wypisać punkt po punkcie skąd bierze się rozbieżność (np. senior developer zapomniał o testach, albo AI napompowało moduły) zamiast po cichu korygować swój wynik. Jeśli mechanika daje 2× więcej niż jego instynkt sprawdź mnożniki, coś może być napompowane. Jeśli mechanika daje mniej niż jego instynkt nie obniżaj, instynkt jest prawdopodobnie zaniżony. Ten krok NIE jest obowiązkowy senior developer nie zawsze jest dostępny i nie zawsze ma czas.

KROK 10.6 (obowiązkowy): 2-pass audit. Po obliczeniu ceny, AI robi drugą rundę sprawdzającą: (1) Dla każdego modułu: "Czy ten moduł mógłby być przypisany do innego developera niezależnie? Jeśli nie scal z modułem nadrzędnym." (2) Dla każdej pary modułów: "Czy te dwa moduły dzielą kod, tabele lub endpointy? Jeśli tak usunąłeś nakładanie?" (3) Dla każdego modułu: "Czy ten moduł pochodzi z confirmed scope czy z brainstormu klienta?" (4) "Czy wynik różni się o >30% od instynktu senior developera lub poprzedniej wyceny? Jeśli tak wyjaśnij źródło różnicy." Pokaż wynik audytu właścicielowi: ile modułów usunąłeś, scaliłeś, przeklasyfikowałeś.

Cena minimalna niezależnie od kalkulacji. Nawet jeśli kalkulator wyjdzie niżej nigdy nie schodzimy poniżej 500 zł za jakiekolwiek zlecenie. To twarde minimum. Dla zleceń które naturalnie wychodzą poniżej 500 zł uczymy się pisać oferty tak, żeby uzasadnić tę kwotę (pełen setup, konfiguracja, testy, gwarancja).

Na końcu kalkulacji AI ZAWSZE pokazuje właścicielowi rozbicie: lista modułów -> godziny per moduł -> suma -> buffer -> mnożniki (z zaznaczeniem czy cap zadziałał) -> stawka efektywna -> cena bazowa -> korekta -> kwota końcowa. właściciel widzi skąd wzięła się kwota i może ją skorygować. Żadnych kwot bez dowodu kalkulacji.

KROK 11 (tylko dla BIERZEMY, w wątku priv): Z doświadczenia senior developera: cena jest ustalona w ofercie. Klienci decyzyjni rzadko negocjują stawkę, jeśli widzą uzasadnienie techniczne. Jedyny moment na korektę ceny w górę to sytuacja, gdy na priv wyszły nowe wymagania, których nie było w ogłoszeniu. Wtedy senior developer pisze klientowi: "to jest większa praca niż wynikało z opisu, podeślę zaktualizowaną wycenę z rozbiciem na moduły".

Pytania o skalę i kontekst (do wykorzystania jako Question CTA lub na priv, bez proponowania calli): dopasuj do typu zlecenia i ścieżki (inżynieria vs biznes). Dla sklepu: "Ile SKU i z jakim systemem magazynowym to spinamy?" Dla automatyzacji (biznes): "W jakim formacie macie teraz te pliki i co robicie z nimi ręcznie?" Dla scrapera/bota: "Do jakiego formatu (CSV, baza SQL, webhook) mają trafiać wyciągnięte dane?" Dla mobilki: "Czy backend/API jest już gotowe, czy budujemy je w ramach zlecenia?" Nie pytaj o rzeczy oczywiste przy prostych zadaniach (wizytówka, szybki fix).

KALIBRACJA. Tabela godzinowa i mnożniki to przybliżenie, nie wyrocznia. Jedyny sposób żeby je ugruntować w rzeczywistości to dane z ukończonych projektów. Po każdym skończonym zleceniu zapisuje się: ile godzin estymata vs ile realnie poszło. Po 5-10 projektach tabela godzinowa będzie oparta na faktach zamiast na symulacji. Do tego czasu traktuj wyceny jako wstępne i bądź gotów korygować po briefie z klientem.
