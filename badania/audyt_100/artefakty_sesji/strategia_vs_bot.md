# STRATEGIA vs BOT — Co Strategia Wymaga, a Czego Bot Nie Robi

> Przeczytałem **cały** katalog `badania/` — 4 stopnie pewności, 9 scenariuszy klientów, audyt falsyfikacyjny, 7 kroków schematu bota, filtry phantom leads, matrycę klient×tech — i porównałem z **każdą linijką kodu** w `kod/`.

---

## 🔴 KRYTYCZNE ROZBIEŻNOŚCI (strategia wyraźnie mówi X, bot robi Y)

### 1. Strategia: „Dual-Track — 33% rynku to tech-agnostic, zero żargonu IT"
**Bot: Nie rozróżnia ścieżek.**

- **Hipoteza 2.1** (80% pewności): 67% zleceń to inżynieria (precyzja stacku), 33% to tech-agnostic (zero żargonu, język rezultatu biznesowego).
- **Obalone Mity 3 i 7**: Wrzucenie żargonu IT do oferty dla klienta biznesowego = odrzucenie.
- **Kod**: `selekcja_zlecen.md` i `prompt_ai1.md` prowadzą AI do tiering (A/B) na bazie marży/technologii, ale **nie przekazują klasyfikacji Dual-Track dalej do generatora treści**. Agent 02a dostaje `tier` (A/B), ale nie dostaje flagi `ścieżka: inżynieria | biznes`, więc:
  - Nie ma mechanizmu, który mówi agentowi 02a: „ten klient nie wymienił żadnej technologii → pisz językiem rezultatu, zero skrótów IT".
  - Agent 08 waliduje format (190 słów, brak markdown, CTA), ale **nie waliduje spójności Dual-Track** — choć [krok_05_bramka_walidacji.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_05_bramka_walidacji.md#L15-L18) wprost wymienia „Test Spójności Dual-Track" jako obowiązek agenta 08.

**Zmiana w bocie**: Selekcjoner AI (slot prompt_ai1.md) powinien do werdyktu BIERZEMY dopisywać pole `"sciezka": "inzynieria" | "biznes"`. Agent 02a powinien dostawać to pole w kontekście i przełączać ton. Agent 08 powinien sprawdzać: „czy w ofercie do klienta biznesowego padł żargon IT?"

---

### 2. Strategia: „6 typów klientów + 3 modyfikatory psychologiczne"
**Bot: Nie widzi typów ani modyfikatorów.**

- Audyt falsyfikacyjny (`raport_falsyfikacji_i_weryfikacji_typow.md`) definiuje zweryfikowaną taksonomię:
  - **6 typów**: Tradycyjne MŚP/ERP, E-commerce, Agencja/SW House, Ekspert dziedzinowy, Tech-Agnostic, Quick Fix.
  - **3 modyfikatory**: RESCUE (12.1% rynku), DELEGOWANY PRACOWNIK (4.3%), PHANTOM STARTUP (2-3%).
- Audyt Red Team (`audyt_mocny_scenariusze_klientow.md`) mówi wprost: „Modyfikatory są mocniejsze niż profile podstawowe. Phantom Startup i Rescue powinny być **pierwszym filtrem**."
- **Kod**: Selekcjoner AI nie dostaje scenariuszy klientów. Dostaje `selekcja_zlecen.md` + `stack_i_filozofia.md`. Tworzy werdykt BIERZEMY/ODRZUCAM z Tier A/B, ale:
  - Nie klasyfikuje typu klienta (MŚP? Merchant? Ekspert?).
  - Nie wykrywa modyfikatorów (RESCUE? PHANTOM? DELEGOWANY?).
  - Agent 02a nie wie, czy pisze do magazyniera z Subiektem czy do lekarza z gabinetowym chaosem.

**Zmiana w bocie**: Selekcjoner powinien zwracać `"typ_klienta"` i `"modyfikatory": ["RESCUE"]` obok werdyktu. Generator 02a powinien dostawać odpowiedni scenariusz jako kontekst. Ale **nie dodawać 9 scenariuszy do promptu** — to rozdęłoby kontekst. Lepiej: selekcjoner klasyfikuje → chain_executor podczepialny kontekst dynamicznie.

---

### 3. Strategia: „Profil 04 (Ekspert dziedzinowy) = profil flagowy, jedyny potwierdzony duży win"
**Bot: Traktuje ekspertów tak samo jak resztę.**

- Doktor Monika 12 100 PLN — jedyna zweryfikowana duża transakcja — to typ E (Ekspert).
- Audyt Red Team: „Podniesiony do rangi profilu flagowego". 
- Poszlaka 3.4: ERP/Przemysł płacą „wysokie stawki bez negocjacji groszowych".
- **Kod**: Tier A dotyczy nisz technologicznych (scraping, CAD, Enova), ale **nie promuje ekspertów dziedzinowych** (lekarze, prawnicy, komornicy). Klinika medyczna szukająca systemu rezerwacji trafiłaby jako Tier B, bo „system rezerwacji" to nie jest słowo kluczowe fast-track.

**Zmiana w bocie**: Rozszerzyć definicję Tier A o sygnały eksperta dziedzinowego w `selekcja_zlecen.md` — słowa: gabinet, klinika, kancelaria, komornik, monitoring, RODO, dokumentacja medyczna.

---

### 4. Strategia: „Question CTA z opcjami A/B, nie prośba o call"
**Bot: Częściowo implementuje, ale nie waliduje typu pytania.**

- Fakt 1.5 (>95% pewności): Question CTA daje +26.4% response rate vs „zapraszam do kontaktu".
- Fakt 1.4: Oferta ma wywołać impuls do kliknięcia „Odpowiedz" — nie sprzedać cały projekt.
- Teoria „Pytanie w Środku": hipoteza, że pytanie wplecione w tok myślenia działa lepiej niż grzeczne CTA na końcu.
- **Kod**: `agent_02a_opis_oferty.md` wymaga Question CTA. Agent 08 waliduje obecność pytania. **Ale walidator nie sprawdza**:
  - Czy pytanie jest inżynierskie/architektoniczne (A/B o bazę danych) vs generyczne („Czy mogę pomóc?").
  - Czy odpowiada typowi klienta (tech-agnostic dostaje pytanie o architekturę DB → panika).

**Zmiana w bocie**: Walidator 08 powinien sprawdzać jakość CTA: dla tech-agnostic → pytanie o format danych/proces, dla inżyniera → pytanie o stack/architekturę. Plus: rozważyć test A/B „pytanie w środku" vs „CTA na końcu" z trackowaniem.

---

### 5. Strategia: „Obalony Mit 6 — Faza 1/PoC ma 0% konwersji"
**Bot: Kalkulator nadal ma logikę do Fazy 1.**

- Mit 6 (Stopień 4, pewność 0%): „Dzielenie projektu na Fazę 1 za 800 zł miało 0% konwersji".
- Audyt Red Team: „ZAKAZ samowolnego wyceniania małego MVP".
- **Kod**: `krok_03_kalkulacja_wyceny.md` mówi: „zakres ewidentnie wymaga 50 godzin pracy → podział na Faza 1 PoC". Ten zapis **wprost łamie obalony Mit 6**. Kod w `wycena_kalkulator.py` nie implementuje automatycznego dzielenia, ale prompt `mechanika_wyceniania.md` może to sugerować modelowi.

**Zmiana w bocie**: Usunąć wzmiankę o „Faza 1 PoC" z `krok_03_kalkulacja_wyceny.md` (to docs, nie kod, ale docs karmi prompty). W promptach: „Wyceniaj pełny zakres. Cięcie na MVP dopuszczalne WYŁĄCZNIE gdy (a) konkurencja pod zleceniem tak wycenia lub (b) klient wprost żąda fazowania".

---

## 🟡 ISTOTNE BRAKI (strategia zakłada, ale bot nie ma)

### 6. Strategia: „Czas złożenia oferty < 30 min od publikacji"
**Bot: Brak telemetrii czasu.**

- Hipoteza 2.5 (65% pewności): Oferty złożone w ciągu 15-30 min mają ~50% większą szansę na przeczytanie.
- **Kod**: `engine.py` nie loguje czasu od `detected_at` (kiedy zlecenie pojawiło się na Useme) do `data_wyslania` (kiedy oferta została złożona). Nie ma sposobu zmierzyć, czy ta hipoteza się potwierdza.

**Zmiana w bocie**: Logować `time_to_offer_s = data_wyslania - detected_at` do rekordu zlecenia. Priorytetyzować świeże zlecenia (< 1h) nad zalegające.

---

### 7. Strategia: „Poszlaka 3.5 — odpowiedź na priv < 15 minut = 3x konwersja"
**Bot: Zbieracz danych wyłączony, priv_engine istnieje ale nie jest zintegrowany.**

- `zbieracz_danych.py` ma `ZBIERACZ_AKTYWNY = False`.
- `priv_engine.py` (zrekonstruowany z bytecodu) ma pełną logikę 3-krokowego protokołu (Trojan Horse → Escrow → Domknięcie), ale:
  - Nie jest wywoływany z `engine.py`.
  - Nie ma promptu `agent_priv_responder.md` w repozytorium.
  - Brak alertów na telefon Ksawiera o nowej wiadomości.

**Zmiana w bocie**: Strategia mówi: „Wariant 1 — bot tylko składa ofertę, priv 100% ręczny Ksawier — jest aktualnym modelem domyślnym". Więc priv_engine jest na przyszłość. Ale **alert o nowej wiadomości** (push/webhook do telefonu) to zmiana o niskim koszcie i wysokim ROI wg poszlaki 3.5.

---

### 8. Strategia: „Filtr pułapek ogłoszeń — 5 typów zleceń-widm"
**Bot: Nie filtruje pułapek.**

- `filtr_pulapki_ogloszen.md` wymienia: ogłoszenia o pracę maskowane jako zlecenia, zbieranie wycen do dotacji, pośrednicy z podwójną marżą, „dokończenie po kimś" (2x wyższa wycena), aukcje z 80+ ofertami.
- **Kod**: Filtr anty-tłum odrzuca > 60 ofert (z wyjątkami fast-track). Ale **nie wykrywa**:
  - Ukrytych rekrutacji na etat (słowa: „na stałe", „etat", „ATS", „widełki").
  - Zleceń na zbieranie wycen do dotacji (język urzędowy, brak kontaktu).
  - Pośredników („zlecenie dla mojego klienta").

**Zmiana w bocie**: Dodać deterministyczne filtry w `engine.py` lub w prompt selekcjonera: „Odrzucaj zlecenia ze słowami: etat, ATS, na stałe, widełki godzinowe, dołączenie do zespołu". Selekcjoner AI już powinien to robić, ale warto wzmocnić explicite w `selekcja_zlecen.md`.

---

### 9. Strategia: „Audyt Red Team — brakuje mapy PROFIL → TECH"
**Bot: Brak dynamicznego podczepiania kontekstu technologicznego.**

- Red Team: „Bez tabeli mapowania PROFIL → KARTY TECH → SEKCJA SCENARIUSZA model AI sam musi zgadywać. To jest zaproszenie do halucynacji technicznej."
- **Kod**: Agent 02a dostaje cały kontekst statycznie (`jak_pisac_oferty.md`, `lore.md`, `portfolio_baza.md`, `mechanika_wyceniania.md`) — niezależnie od tego, czy pisze do ERP czy do scrapingu. Nie dostaje karty technologicznej.
- `badania/analizy/technologie/baza_wiedzy/` zawiera 16 kart tech (od WordPress po AI/LLM). **Żadna z nich nie jest podawana do promptu.**

**Zmiana w bocie**: Po klasyfikacji przez selekcjonera (typ + technologia), chain_executor powinien dynamicznie doczepiać odpowiednią kartę tech jako dodatkowy kontekst do agenta 02a. Np. zlecenie z Enova → dolinkować `tech_09_erp_enova_optima.md` (o ile taki istnieje, bo numery sugerują tech_13 = enova).

---

## 🟢 CO STRATEGIA MÓWI I BOT ROBI DOBRZE

| Reguła strategiczna | Implementacja w kodzie | Status |
|:---|:---|:---:|
| Max 190 słów, czysty tekst bez markdown | Agent 02a + walidator 08 | ✅ |
| Question CTA zamiast „zapraszam do kontaktu" | Prompt 02a + walidator 08 | ✅ |
| Stawka 90 zł/h, deterministyczny kalkulator | `wycena_kalkulator.py` L20-23 | ✅ |
| Min 7 dni w formularzu | `wycena_kalkulator.py` MIN_DNI=7 | ✅ |
| Blokada własnego profilu (wer13) | `engine.py` BLOCKED_AUTHORS | ✅ |
| Anty-powtórka Jaccarda per klient i globalnie | `ai_pipeline.py` L33-75 | ✅ |
| Research sieciowy (nie pisz ogólników) | Agent 01 + deepseek-v4-pro-search | ✅ |
| STOP file kill switch | `bezpieczenstwo.py` | ✅ |
| Sanity check efektywnej stawki > 85 zł/h | `wycena_kalkulator.py` L304-311 | ✅ |
| Nie obniżaj stawek przy dużej konkurencji | KOREKTY table (wszystkie ~1.0) | ✅ |
| Zakaz proponowania calli | Implicite w promptach | ✅ |
| Podpis „Pozdrawiam, Ksawier" | W prompcie 02a | ✅ |

---

## PRIORYTETYZACJA ZMIAN (wg wpływu na konwersję)

### P0: Natychmiastowe (wpływ na jakość każdej oferty)
1. **Dual-Track w selekcjonerze** — dodać `"sciezka": "inzynieria" | "biznes"` do werdyktu AI → przenieść do 02a → walidować w 08.
2. **Typologia klienta** — selekcjoner klasyfikuje typ (MŚP/Merchant/Ekspert/Quick Fix) → chain_executor podłącza scenariusz.
3. **Ekspert dziedzinowy = Tier A** — rozszerzyć fast-track o sygnały medyczne/prawne/księgowe.

### P1: Szybkie wzmocnienia (1-2h pracy)
4. **Filtry pułapek** — deterministyczne wykluczanie rekrutacji/dotacji w `engine.py`.
5. **Logowanie time_to_offer** — metryka czas od wykrycia do wysłania.
6. **Usunięcie wzmianki o Faza 1 PoC** z docs (łamie obalony Mit 6).

### P2: Architektura (wymagają dyskusji)
7. **Dynamiczne podczepianie kart TECH** do promptu 02a na podstawie klasyfikacji.
8. **Alert na telefon** o nowej wiadomości od klienta (webhook/Telegram/Pushover).
9. **Zbieracz danych** — decyzja: włączyć z HTTP API (bez Playwright DOM selektorów) czy poczekać.

---

## PYTANIA DO CIEBIE

1. **Dual-Track**: Czy selekcjoner AI (nothink) jest w stanie rzetelnie klasyfikować ścieżkę (inżynieria/biznes), czy powinien to robić model z myśleniem?
2. **Karty tech**: Czy 16 kart w `badania/analizy/technologie/baza_wiedzy/` jest aktualna i gotowa do wklejania jako kontekst? Czy trzeba je zrewidować?
3. **Priv_engine**: Ten moduł ma pełny kod (3-krokowy protokół). Brakuje mu promptu `agent_priv_responder.md`. Planujesz go dokończyć?
4. **Priorytet**: Z P0 zmian — od czego zaczynamy? Dual-Track? Typologia? Tier A dla ekspertów?
