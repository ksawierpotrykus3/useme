# USEME_CORE — MASTER PLIK (KOMPLETNA MAPA PROJEKTU)
**Ostatnia aktualizacja:** 24 września 2026

---

# AKTUALNY STATUS (na czym skończyliśmy)

## Co jest ZROBIONE:
1. ✅ Reorganizacja `badania/strategia/` — podział na 6 tematycznych podfolderów (01-06) + indeks README
2. ✅ **Migracja do `badania/baza/`** (24.09) — zlecenia/oferty/wiadomości w jednym miejscu: `badania/baza/<konto>/<podział>/`. Config i wszystkie skrypty zaktualizowane. Stare foldery (`historia_ofert_ksawiera/`, `kod/magazyn/`) zlikwidowane.
3. ✅ MASTER.md — ten plik, mapa całego projektu (zaktualizowana 24.09.2026)
4. ✅ Analiza konkurencji — 42 oferty + 6 wiadomości prywatnych od seniorów
5. ✅ Benchmark #1 (zlecenie #144890, AI/OCR/Optima):
   - Bot wygenerował ofertę (17 000 zł, 30 dni) → zanonimizowana jako "team-alpha"
   - DeepSeek V4 Pro: nasza oferta #2 (przegrała z ailone bo o 2k za droga)
   - Gemini 3.8 Flash: nasza oferta #1 (ZWYCIĘZCA)
   - Pełne reasoning traces zapisane w raw_logs/
6. ✅ Insight: liczba umów na Useme NIE koreluje z jakością (elita ma 0 umów)
7. ✅ Insight: 6/6 seniorów pisze na priv, nie składa ofert publicznych
8. ✅ Insight: kluczowy differentiator = znaleźć w briefie szczegół którego nikt nie zauważył

## Co TRZEBA ZROBIĆ (następne kroki, po kolei):
1. ⬜ **Kalibracja wyceny** — kalkulator powinien celować w ~14 500 zł zamiast 17k
   przy zleceniach "do negocjacji" blisko progu 15k (wniosek z benchmarku)
2. ⬜ **Benchmark #2** — wystawić zlecenie testowe w INNEJ niszy (BaseLinker/Subiekt)
   żeby sprawdzić które wzorce są uniwersalne a które specyficzne dla AI/OCR
3. ⬜ **Benchmark #3** — wystawić tanie zlecenie (landing/sklep 2-5k)
   żeby zobaczyć czy tani rynek rządzi się innymi prawami
4. ⬜ **Portfolio** — "Złota Ósemka" (8 projektów demo) nie jest zbudowana
   (plan w badania/strategia/plan_portfolio.md)
5. ⬜ **Zbieracz danych** — config.ZBIERACZ_AKTYWNY=False, nie wiemy jaki jest reply rate
6. ⬜ **Konto 2 (Maksymilian)** — cookies2.json nie istnieje, nie podpięte

## Uniwersalne wnioski z benchmarku (potwierdzone na 2 modelach):

### CO ODRZUCA KLIENTA (antywzorce — prawdopodobnie uniwersalne):
- Negowanie briefu ("nie rób n8n" gdy klient chce n8n)
- Absurdalna cena w obie strony (500 zł i 120 000 zł)
- Pchanie w telefon / "zdzwońmy się"
- 3 zdania bez konkretu
- Sprzedawanie abonamentu zamiast odpowiedzi na zlecenie
- Linki zewnętrzne / spam

### CO WYGRYWA (do potwierdzenia na kolejnych niszach):
- Znaleźć w briefie szczegół którego nikt nie zauważył (tu: ProfiPiek)
- Demo Guard / niski próg wejścia (test na 1 fakturze w 20 min)
- Ostrzeżenie o ukrytych kosztach (licencja Optimy 130 zł)
- Uczciwe "nie mam wdrożenia 1:1, ale sprawdzę"
- Etapowanie (pilot → reszta)
- Cena w budżecie klienta (nie za drogo, nie za tanio)

## NIESPRAWDZONA TEORIA: Dwa typy klientów na Useme
- **Właściciel firmy** (piekarnia, mała firma) → wrzuca oferty do AI → AI filtruje → ogląda top 5
  → Nasz bot jest pod to zoptymalizowany (structured, comprehensive, keywords)
- **Pracownik w firmie** (PM, marketer) → czyta sam "po ludzku" → ocenia emocjonalnie
  → Nasza oferta może być za długa i za techniczna dla tego typu
- **Jak rozpoznać pracownika:** pełne imię + nazwisko + zdjęcie profilowe = często pracownik
  (właściciele małych firm częściej mają nick lub nazwę firmy)
- **Do zbadania:** czy da się rozpoznać typ klienta z briefu i dopasować długość/ton oferty

## Postęp budowania idealnej ofertowarki:
1. ✅ Bot działa — skanuje, selekcjonuje, generuje, wysyła (81 ofert wysłanych)
2. ✅ Prompt system gotowy — 4 generatory, 1 walidator, 6 plików kontekstu
3. ✅ Pierwszy benchmark — bot wygrywa z 95% ludzi (pozycja 1.5/42)
4. ✅ Analiza konkurencji — wiemy co robią seniorzy (priv, pytania, piloty)
5. ⬜ Kalibracja ceny — za drogo o 2k, trzeba poprawić próg 15k
6. ⬜ Benchmarki w innych niszach — potwierdzić co jest uniwersalne
7. ⬜ Wdrożyć wnioski do promptów — ProfiPiek-pattern (szukaj niszowego szczegółu)
8. ⬜ Portfolio — zero demo, zero case studies do pokazania
9. ⬜ Reply rate — nie wiemy ile klientów odpowiada (zbieracz wyłączony)

---
AI je selekcjonuje, wycenia i pisze ofertę, Playwright wypełnia formularz i wysyła.

## KTO
- **Ksawier Potrykus** — właściciel, profil Useme ID 608362
- **Maksymilian** — partner inżynieryjny (drugie konto w przygotowaniu)
- Profil Useme: 8 zrealizowanych umów, 0 sporów

## STAN MAGAZYNU (live, 23.09.2026)
| Kategoria | Zleceń | Wysłano | Nowe (czekają) | Inne |
|---|---|---|---|---|
| programowanie-i-it | 62 | 44 | 14 | 4 |
| serwisy-internetowe | 84 | 37 | 28 | 19 |
| **RAZEM** | **146** | **81** | **42** | **23** |

Wysłano łącznie 81 ofert. 42 zlecenia czekają na ofertę.

---

# ARCHITEKTURA BOTA

## Przepływ od początku do końca
```
1. Useme online?          → czekaj_na_dostepnosc_useme() (co 60s, max 3h)
2. Zbieracz danych        → zbieracz_danych.py (wyłączony — ZBIERACZ_AKTYWNY=False)
3. Scrapuj zlecenia       → browser_driver.py (Playwright + stealth, 2 kategorie)
4. Zapisz w bazie        → storage.py (badania/baza/<konto>/01_ofertowarka/<kategoria>/<job_id>.json)
5. Filtr anty-tłum        → odrzuć jeśli >60 ofert (chyba że VIP keyword)
6. AI selekcja            → ai_pipeline.py → deepseek-v4-pro-nothink
7. Pobierz detale         → browser_driver.py (pełny opis, autor)
8. AI łańcuch generowania:
   Slot 01: Research      → deepseek-v4-pro-search (fakty z sieci)
   Slot 02b: Wycena       → deepseek-v4-pro → wycena_kalkulator.py (deterministyczna)
   Slot 02a: Treść oferty → deepseek-v4-pro (z kontekstem lore + portfolio + research)
   Slot 08: Walidator     → deepseek-v4-pro (sprawdza reguły, PASS/FAIL)
9. Anty-powtórka          → Jaccard >70% = przepisz (max 2 próby)
10. Sanity check          → stawka efektywna >= 85 zł/h?
11. Globalne duplikaty    → Jaccard >75% z ofertami z ostatnich 7 dni
12. Wypełnij formularz    → form_driver.py (Playwright, headless=False)
13. Wyślij lub DRY_RUN    → engine.py (zrzut ekranu + potwierdzenie URL /finish)
14. Pacing anty-ban       → 25-40s między zleceniami, 18-25s między slotami AI
```

## Kluczowe parametry
| Parametr | Wartość | Plik |
|---|---|---|
| Model AI (research) | deepseek-v4-pro-search | chain_config.json |
| Model AI (wycena/oferta) | deepseek-v4-pro | chain_config.json |
| Model AI (selekcja) | deepseek-v4-pro-nothink | ai_pipeline.py |
| Proxy AI | http://127.0.0.1:4571 | chain_executor.py |
| Max ofert/kategorię | 40 | config.py |
| Max konkurentów (filtr) | 60 | config.py |
| Max czas runu | 180 min (3h) | config.py |
| Max długość opisu | 6000 znaków | config.py |
| Min kwota | 500 zł | wycena_kalkulator.py |
| Min dni pracy | 7 | config.py |
| Stawka Tier B | 100 zł/h (pasmo 90-110) | wycena_kalkulator.py |
| Stawka Tier A | 110 zł/h | wycena_kalkulator.py |
| Limit Useme | 21 ofert/dzień | selekcja_zlecen.md |
| DRY_RUN | False (live!) | config.py |
| HEADLESS | False (widoczna przeglądarka) | config.py |
| Przeglądarka | Chromium + playwright-stealth | browser_driver.py |
| Konta aktywne | 1 (Ksawier), konto 2 przygotowane | config.py |

---

# MECHANIKA WYCENY (DETERMINISTYCZNA)

AI nie liczy ceny. AI ocenia zakres i zwraca moduły/godziny → Python liczy cenę.

## Ścieżki wyceny
- **Małe zlecenie** (<8-12h pracy): stała kwota rynkowa (min 500 zł), 7 dni
- **Retainer** (stała współpraca): 1 500–5 000 zł/mies
- **Projekt**: moduły → godziny → bufor (+20-30%) → testy (+15%) → mnożniki ryzyka → stawka × godziny → zaokrąglenie

## Mnożniki ryzyka (cap łączny: ×1.8)
| Mnożnik | Wartość |
|---|---|
| Brak specyfikacji | ×1.3 |
| Figma + specyfikacja (rabat) | ×0.9 |
| Ograniczenia API | ×1.25 |
| Real-time (WebSocket) | ×1.2 |
| System do przepisania | ×1.15 |

## Kotwica budżetu klienta
- Budżet jawny > cena bazowa → celuj w 85% budżetu (cap 1.4× bazy)
- Budżet jawny < cena bazowa → nie schodź poniżej rentowności, proponuj MVP
- Budżet 50–250 zł → kontekstowo: stawka godzinowa lub mikrozadanie min 500 zł

## Zaokrąglanie
- Do 2 000 zł: do 50 zł
- 2 000–10 000 zł: do 500 zł
- Powyżej 10 000 zł: do 1 000 zł

## Sanity check
Jeśli efektywna stawka (kwota ÷ godziny) spadnie poniżej 85 zł/h → SANITY_BLOK.

---

# SELEKCJA ZLECEŃ (CO BIERZEMY, CO ODRZUCAMY)

## TIER A — priorytet (wysokie marże)
Aplikacje mobilne (Kotlin, Flutter, iOS), .NET/C#, ERP/KSeF/FinTech, boty/scraping
z anty-detekcją, AI/LLM/n8n/RAG, konfiguratory 3D Three.js, systemy rezerwacji

## TIER B — bierzemy
Dedykowane sklepy (Shopify, IdoSell, WooCommerce), aplikacje webowe, integracje API,
zlecenia ogólne z niepełną specyfikacją

## TIER C — odrzut
Marketing (Google/Meta Ads), praca biurowa bez kodu, szkolenia, mechanika CNC Punch,
malware/czyszczenie wirusów, WordPress/Elementor z budżetem <1000 zł i >25 ofert

## VIP Fast-Track (ignoruje filtr anty-tłum)
ai, llm, n8n, make, baselinker, konfigurator, three.js, webgl, idosell, ksef, erp,
scraping, ocr, topsolid, cnc, cad

---

# REGUŁY PISANIA OFERT (CZARNA LISTA)

1. ZERO szablonów — każda oferta unikalna
2. ZERO coachingu — zakaz "Doskonale rozumiem, że..."
3. ZERO obcych case study — zakaz wklejania faktur do zlecenia FinTech (Łoże Prokrustesa)
4. ZERO over-engineeringu — zakaz mikroserwisów i Redis do poprawki CSS
5. ZERO korpomowy — zakaz "kompleksowe rozwiązanie", "synergia", "innowacyjny"
6. ZERO straszenia regulacjami — zakaz RODO/KSeF bez związku ze zleceniem
7. ZERO tanich chwytów — zakaz "prototyp w 15 min na telefon" przy 20k zł
8. ZERO LinkedInowego CTA — zakaz "Zdzwońmy się na 15 minut" (81% przegranych!)
9. ZERO anonimowego podpisu — zawsze "Ksawier Potrykus"
10. Język 1:1 — angielski do angielskiego, polski do polskiego
11. Formatowanie Useme — czysty tekst, zero markdown, zero list z myślnikami
12. Stawka max 110 zł/h — zawsze podawaj gdy klient prosi

## CTA sytuacyjne (zamykanie)
- Do ~5k zł: "Napisz to zgadamy się co do szczegółów" / "Podeślij pliki na priv"
- 5k–15k zł: wybór klienta (priv lub rozmowa)
- Powyżej 15k zł: krótka rozmowa z podglądem ekranu

## Demo Guard (próbka techniczna)
AI proponuje demo tam, gdzie to ma sens (np. "prześlij 1 fakturę, w 20 min odsyłam JSON").
Zawsze na danych testowych / wideo / podgląd ekranu.
BEZWZGLĘDNY ZAKAZ oddawania kodu produkcyjnego przed escrow Useme.

## Anty-powtórka
Jeśli ten sam klient dostał już od nas ofertę → porównanie Jaccarda:
- >70% podobieństwa → przepisz (max 2 próby, inny variation_seed 0-4)
- Globalnie >75% podobieństwa do dowolnej oferty z 7 dni → ostrzeżenie o spadku unikalności

---

# PORTFOLIO (CO BOT MOŻE WKLEJAĆ)

## TIER 1 (80% rynku Useme)
1. **AI Document Pipeline** — OCR/n8n, walidacja VAT co do grosza, KSeF XML, 3500+ docs, 99.4%
2. **API Integration Engine** — BaseLinker/Allegro/Shopify, Leaky Bucket, Redlock, idempotencja
3. **Scraping Engine** — bypass WAF/Cloudflare, TLS JA4, detekcja <3:40, skuteczność 99.8%

## TIER 2 (nisze 4.5–25k zł)
4. **Konfigurator 3D** — Three.js/WebGL, Draco (-92% waga), 60 FPS iOS, eksport CNC G-code
5. **Panel B2B** — IdoSell/Shopify, cenniki hurtowe, NIP w GUS/VIES
6. **System rezerwacji** — PostgreSQL SELECT FOR UPDATE, Stripe Connect, zero kolizji 18 mies.

## Social proof
Rekomendacja Dominika Łyżwy (Prezes Kliniki Doktor Monika): "głębokie zrozumienie procesów
biznesowych, wyłapywanie luk architektonicznych, dostarczenie technologii i spokoju".

---

# STATYSTYKI Z AUDYTÓW

## Definicje
- **Wygrana** = klient ODPISAŁ na naszą ofertę (nie oznacza podpisanej umowy!)
- **Przegrana** = klient NIE odpisał (cisza / zlecenie zamknięte bez nas)

## 56 wygranych ofert (= klient odpisał)
- Średnia cena: 5 273 zł (mediana 3 400 zł)
- Top: 34k (Mental Health), 16k (Subiekt nexo), 15k (CV bot)
- Wzorzec wygrywający: hook z problemem → proof of competence → mały pierwszy krok → 21-30 dni wsparcia

## 414 zamkniętych ofert (= zakończone; część to wygrane)
- Pełna baza: badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json
- Skrócona wersja (16 z audytem): badania/baza/ksawierpotrykus3/02_przegrane/przegrane_16.json
- Uwaga: 414 Twoich zamkniętych ofert; część z nich pokrywa się z wygranymi (klient odpisał). Wszystkie 42/42 strony pobrane.
- Uwaga: nazwa `przegrane_pelne_416.json` jest myląca — to nie „cudze oferty", to Twoje zamknięte.

## Szczegółowy audyt 16 przegranych (próbka z 416)
- Średnia cena w tych 16: 9 447 zł (prawie 2× wyższe niż wygrane!)
- 87.5% call spam, 81.2% "15 minut", 56.2% "dwuosobowy zespół", 0% podpisu
- Wzorzec przegrywający: pouczanie, price shock, nieczytanie briefu, straszenie regulacjami

## Mystery shopping (zlecenia testowe jako zleceniodawca)
- **Zlecenie #1 DONE:** #144890 "Automatyzacja obiegu faktur" (AI/OCR/Optima)
  - **42 oferty** (41 publicznych + 1 nasza zanonimizowana jako "team-alpha")
  - **6 wiadomości prywatnych od seniorów** (ŻADEN nie złożył oferty publicznej!):
    1. Adam K — zaokrąglenia VAT, deduplikacja NIP+nr, KSeF eliminuje OCR, GitHub
    2. Kamil Wojtulewicz — etapowe, OCR z confidence score, pytania o Optimę
    3. Konrad Szydłowski — KSeF od 1.02.2026, oferta publiczna 5 400 zł
    4. Adam Wolski — próbka dokumentów, format wymiany, architektura
    5. Bartłomiej Drożyński (Clever Future Company) — brak wdrożenia OCR-Optima, uczciwie, etap testowy
    6. UTIS — pilot 1 500 zł za 20 faktur, Allegro integracje, CSV/JSON
  - Analiza: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/ANALIZA_KONKURENCJI.md
- **5 kolejnych zleceń GOTOWYCH do wysłania** (badania/strategia/mystery_shopping.md)

## WYNIKI BENCHMARKU #144890 (ślepy test na 2 modelach)

Nasza oferta (bot, 17 000 zł) oceniona jako "team-alpha" wśród 42 ofert:

| Model | Pozycja naszej oferty | Zwycięzca |
|---|---|---|
| Gemini 3.8 Flash | **#1 ZWYCIĘZCA** | team-alpha (MY!) |
| DeepSeek V4 Pro | **#2 runner-up** | ailone (10 500 zł, tańszy) |

**Średnia pozycja: 1.5 / 42 ofert!**

Co wygrało: ProfiPiek (niszowy system klienta — jedyni którzy go zauważyli),
ostrzeżenie o koszcie licencji Optimy, Demo Guard.

Co przegrało: -2 000 zł za drogo (17k vs mentalny budżet 15k). Gdyby bot dał
14 500 zł → 1. miejsce na OBU modelach.

Pełne raporty: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/ocena_klienta/

---

# BENCHMARK OFERT (ślepy test na wielu AI)

## Idea
1. Wystawiamy zlecenie testowe → zbieramy oferty konkurencji
2. Bot generuje NASZĄ ofertę (DRY RUN, nie wysyła)
3. Anonimizujemy naszą ofertę i wrzucamy do puli
4. Każdy model AI dostaje TEN SAM prompt i ocenia oferty jako KLIENT
5. Zbieramy: kto wygrał, dlaczego, co odpadło, czego brakowało
6. Powtarzamy na wielu modelach → wyciągamy UNIWERSALNE wzorce
7. Wzorce → aktualizacja promptów bota (zamknięcie pętli)

## Pliki
- badania/PROMPT_OCENA_KLIENTA.md — uniwersalny prompt ewaluatora
- badania/PLAN_BENCHMARK_OFERT.md — pełny plan z krokami i strukturą
- badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_*/ocena_klienta/ — wyniki per model per zlecenie
- badania/RAPORT_ZBIORCZY.md — wnioski cross-model (planowany, jeszcze nie istnieje)

## Modele do testowania
DeepSeek V4 Pro, Claude Sonnet/Opus, GPT-4o, Gemini 2.5 Pro, Llama 405B

## Status
| Zlecenie | Oferty | Nasza oferta | Oceny AI |
|---|---|---|---|
| #144890 (AI/OCR) | 36 ✅ | ⬜ do wygenerowania | ⬜ |
| #2-5 | ⬜ do wystawienia | ⬜ | ⬜ |

---

# MAPA PLIKÓW

> **Struktura fizyczna (stan 24.09.2026):** root `useme_core/` zawiera TYLKO trzy foldery: `kod/`, `docs/`, `badania/`. Wszystko poniżej jest w jednym z nich.

## kod/ — silnik bota (co się uruchamia)

### kod/ (root silnika)
| Plik | Rola |
|---|---|
| engine.py | Główny koordynator — cały cykl życia oferty |
| ai_pipeline.py | Selekcja AI + generowanie propozycji + anty-powtórka |
| chain_executor.py | Wykonawca łańcucha slotów AI (research → wycena → treść → walidacja) |
| wycena_kalkulator.py | Deterministyczny kalkulator cen (Python, nie AI) |
| browser_driver.py | Playwright + stealth, scraping list i detali |
| form_driver.py | Wypełnianie i wysyłanie formularza oferty |
| storage.py | Magazyn JSON, deduplikacja, checkpointy, atomowy zapis |
| config.py | Konfiguracja: konta, kategorie, flagi, limity, pacing |
| bezpieczenstwo.py | Kill switch (plik STOP), dzienny licznik ofert |
| zbieracz_danych.py | Weryfikator odpowiedzi klientów (wyłączony) |
| segreguj_oferty.py | Segregator bazy 416 zamkniętych ofert do Markdown |
| pobierz_*.py | Pobieracze: wygrane, przegrane, wiadomości, zamknięte 416, dane badawcze |
| generuj_mega_paczke.py, przygotuj_paczke_ai.py | Budowa paczek danych dla AI |
| runner.py, login_useme.py, weryfikuj_konkurencje_48h.py | Uruchamianie, logowanie, weryfikacja |

### kod/prompts/ — mózg AI
| Plik | Rola |
|---|---|
| chain_config.json | Konfiguracja łańcucha slotów (kolejność, modele, zależności) |
| generatory/prompt_ai1.md | Selekcjoner (BIERZEMY / ODRZUT / TIER) |
| generatory/agent_01_research.md | Research sieciowy (fakty, API, prawo) |
| generatory/agent_02b_wycena_dni.md | Wycena: moduły + godziny → JSON dla kalkulatora |
| generatory/agent_02a_opis_oferty.md | Generator treści oferty |
| walidatory/agent_08_weryfikacja_zasad.md | Główny walidator (14 punktów kontrolnych) |
| walidatory/agent_03-07,20 | Wyłączone, zintegrowane w agent_08 |
| kontekst/mechanika_wyceniania.md | 12-krokowy algorytm wyceny |
| kontekst/jak_pisac_oferty.md | Czarna lista błędów dyskwalifikujących |
| kontekst/lore.md | Kim jesteśmy, kompetencje, social proof |
| kontekst/portfolio_baza.md | Case studies do wklejania (z regułą dopasowania) |
| kontekst/selekcja_zlecen.md | Kryteria TIER A/B/C |
| kontekst/stack_i_filozofia.md | Technologie i filozofia sprzedaży |

### badania/baza/ — live baza zleceń (dawniej kod/magazyn/)
| Katalog | Co zawiera |
|---|---|
| ksawierpotrykus3/01_ofertowarka/programowanie-i-it/ | Zlecenia IT (62 pozycje, statusy pipeline) |
| ksawierpotrykus3/01_ofertowarka/serwisy-internetowe/ | Zlecenia serwisowe (84 pozycje) |
| ksawierpotrykus3/01_ofertowarka/.checkpoints/ | Checkpointy stanu |
| ksawierpotrykus3/02_przegrane/ | Zamknięte bez odpowiedzi (nots/) |
| ksawierpotrykus3/03_odpisane/ | Klient odpisał (mesg/) |
| weronikabuchholc13/04_moje_zlecenia/ | Zlecenia testowe + oferty + wiadomości |

### kod/lab/ — testy laboratoryjne
| Katalog | Co zawiera |
|---|---|
| test01-test17/ | Testy silnika (connect, parse, AI, formularz, scraping) |
| test_results/ | Wyniki testów w Markdown |
| archiwalne_testy/ | Stare testy porównawcze (DeepSeek vs Gemini) |
| *.py (root lab) | 20+ skryptów audytowych (analiza_551, cluster_369, deep_audit) |

### kod/tests/ — testy pytest
13 modułów testowych (40 testów, 4.65s, 100% PASS): anty-powtórka, dedup, bezpieczeństwo, kalkulator, multi-konto.

### kod/tech/ — dokumentacja techniczna
AI_INTEGRACJA, AI_LANCUCH, TECH_STACK, LOGIKA_ITERACJI, DOKUMENTACJA_EKSPANSJI, cookies sesyjne, turnstile_solver.py.

### kod/data/, kod/debug/
| Katalog | Co zawiera |
|---|---|
| data/pipelines/ | 57 stanów pipeline'ów zleceń (useme-job-*) |
| debug/ | Zrzuty ekranu z wysyłek (proof screenshots) |

---

## docs/ — dokumentacja projektu (jak działa system)

### docs/ (root)
| Plik | Rola |
|---|---|
| MASTER.md | Ten plik — mapa projektu |
| README.md | Opis projektu |
| CHANGELOG_REFORMY.md | Historia zmian struktury |
| PLAN_meta_lancuch.md | Plan łańcucha meta |

### docs/info/
| Plik | Rola |
|---|---|
| PROJEKT_PLAN.md | Plan projektu |
| PRZEPLYW.md | Opis przepływu bota |
| LORE_USEME.md | Lore platformy Useme |
| DANE_OFERT.md | Struktura danych ofert (lista + szczegóły) |
| KONTA.md | Informacje o kontach |

### docs/trae/
| Plik | Rola |
|---|---|
| 00_REASONING.md | Reasoning AI |
| 01_DIAGNOZA.md | Diagnoza stanu |
| 02_HIPOTEZY_100.md | 100 hipotez |
| 03_PLAN_ODZYSKANIA_OFERT.md | Plan odzyskiwania ofert |
| 04_ANEKS_ZALOZENIA.md | Założenia |
| 05_TRESC_I_WYCENA_100_HIPOTEZ.md | Treść i wycena hipotez |

---

## badania/ — dane, analizy i strategia

### badania/baza/ — baza operacyjna (jedno źródło prawdy, patrz badania/baza/README.md)
Struktura: `<konto>/<podział>/`.

| Konto | Podziały |
|---|---|
| ksawierpotrykus3/ | `01_ofertowarka/` (zlecenia bota: odrzucone+wysłane), `02_przegrane/` (nots/), `03_odpisane/` (mesg/), `_paczki_i_probki/` |
| weronikabuchholc13/ | `04_moje_zlecenia/` (zlecenia testowe + oferty + wiadomości per zlecenie) |

Mapowanie skryptów: `kod/engine.py` → `01_ofertowarka/`, `kod/pobierz_przegrane.py` → `02_przegrane/`, `kod/pobierz_wygrane.py` → `03_odpisane/`, `kod/pobierz_oferty_zleceniodawcy.py` → `04_moje_zlecenia/`.

### badania/rynek/ — dane surowe (rynek)
| Katalog | Co zawiera |
|---|---|
| archiwum/ | Scrap Useme: strona.html + zlecenie.json + zlecenie.txt |
| it/, serwisy/ | Bieżące kategorie |
| katalog_ofert/ | Oferty obrobione do Markdown (01_aplikacje_webowe itd.) |
| profil/ | Profil Useme ID 608362 (raw.html + tekst 1do1) |

### badania/skrypty/ — skrypty analityczne
27 skryptów analitycznych (.py) + checkpointy.

### badania/strategia/ — wiedza biznesowa (patrz strategia/README.md)
| Katalog / plik | Co zawiera |
|---|---|
| STRATEGIA_GLOWNA.md | Kompletna strategia: anatomia rynku, wzorzec oferty, gotowa oferta |
| kompendium_195kb.md | 195KB kompendium (profil, 9 archetypów, 9 case studies, Red Team) |
| arsenal_zamykania.md | Wzorce zamykania dla 4 grup popytu |
| mystery_shopping.md | 5 gotowych zleceń badawczych do wysłania |
| lista_zlecen_badawczych.md | Wzorce zleceń 1:1 z bazy Useme |
| plan_portfolio.md | "Złota Ósemka" — 8 projektów demo do zbudowania |
| 01_material_dowodowy/ | 12 wygranych ofert + 8 audytów |
| 02_fundamenty_psychologiczne/ | Psychologia konwersji, CTA, reguły techniczne tekstu |
| 03_matryca_decyzyjna_i_klientow/ | TIER-y, 9 typów klientów, 7 strategii ofert |
| 04_rejestr_hipotez_i_falsyfikacji/ | 11 audytów: hipotezy, red team, kronika zmian |
| 05_portfolio_i_case_studies/ | Kompletny pakiet portfolio B2B |
| 06_system_bazy_klientow/ | Zasady systemu zbierania wiedzy (README, track, szablony) |
| 07_zrodla_unikalne/ | 14 plików źródłowych kompendium |

# WYNIKI BENCHMARKU OFERT (ŚLEPY TEST AI — ZLECENIE #144890)

Przeprowadzono ślepy test ewaluacyjny 42 ofert (41 konkurentów z Useme + 1 anonimowa oferta naszego bota jako `team-alpha` na pozycji #13) na dwóch niezależnych modelach AI (`DeepSeek V4 Pro` i `Gemini 3.8 Flash Thinking`):

- 🏆 **Gemini 3.8 Flash Thinking:** **1. MIEJSCE (ZWYCIĘZCA — OFERTA AKCEPTOWANA)**
  - Przeważyło: dostrzeżenie braku publicznego API w ProfiPiek (MS SQL), ostrzeżenie przed licencjami Comarch Optima oraz propozycja **Demo Guard** (test na 1 fakturze w 20-30 min).
- 🥈 **DeepSeek V4 Pro:** **2. MIEJSCE (TOP SHORTLIST / RUNNER-UP)**
  - Uznana za bezwzględnie najlepszą technicznie i merytorycznie („poziom doradcy, nie wykonawcy”). Jedyny powód wyboru konkurenta (#16 ailone za 10.5k): cena bota (17k) była lekko powyżej mentalnego budżetu 15k.
- 📊 **Średnia pozycja:** **1.5 na 42 oferty** (pełne logi i raporty w `badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/ocena_klienta/`).

---

# CO DALEJ — OTWARTE KWESTIE

1. **Zbieracz danych wyłączony** — nie wiemy jaki jest reply rate (ile klientów odpowiada).
   config.ZBIERACZ_AKTYWNY = False. Wymaga weryfikacji selektorów DOM.

2. **Konto 2 (Maksymilian) niepodpięte** — cookies2.json nie istnieje. Silnik gotowy
   na multi-account, ale drugie konto nie jest aktywne.

3. **Portfolio nie istnieje** — "Złota Ósemka" (8 projektów demo) jest zaplanowana
   w plan_portfolio.md, ale żaden projekt nie jest zbudowany.

4. **Mystery shopping / Benchmark** — Zlecenie #144890 (faktury/OCR) w pełni przebadane i zbenchmarkowane (41 ofert + 6 wątków priv, wygrana bota w ślepym teście). 4 kolejne gotowe do wystawienia (BaseLinker, 3D, scraping, B2B).

5. **Kalibracja cenowa Slotu 02b** — Wdrożenie wniosku z benchmarku: przy budżetach „Do negocjacji” trzymać kwotę poniżej psychologicznego progu 15k (np. 14 500 – 14 900 zł) lub proponować rozbicie na pilot (3.5k) + wdrożenie (11.5k).
