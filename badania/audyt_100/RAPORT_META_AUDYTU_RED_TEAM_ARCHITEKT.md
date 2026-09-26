# BEZKOMPROMISOWY AUDYT RED-TEAM (ARCHITEKTURA + KONWERSJA B2B + STATYSTYKA 27 OFERT)

**Rola:** Principal Red-Team Architect & B2B Conversion Auditor  
**Przedmiot audytu:** Całość zmian w `useme_core` z sesji `2026-09-26`, kod produkcyjny (`engine.py`, `ai_pipeline.py`, `chain_executor.py`, `audytor_lancuch.py`, `wycena_kalkulator.py`, `config.py`, `zbieracz_danych.py`), prompty (`chain_config.json`, `agent_02a`, `agent_02b`, `agent_08`, `kryteria_audytu_100.md`, `portfolio_baza.md`) oraz pełny zbiór danych z 27 zleceń (`audyt_100_wyniki_27_ofert.json` i skrypty `run_audyt_100.py` / `run_audyt_wave2..5.py`).

---

## 1. WERDYKT GŁÓWNY I BILANS PUNKTACJI (SKALA 1–100 PKT)

> [!IMPORTANT]
> **KOŃCOWA OCENA RED-TEAM CAŁOŚCI REFORMY: `68 / 100 pkt`**  
> *(Suma punktów zdobytych `[+]`: **`+100 pkt`** potencjału bazowego -> Suma twardych potrąceń Red-Team `[-]`: **`-32 pkt`** = **`68 / 100 pkt`**)*

| Wymiar Audytu | Wynik | Maks. | Diagnoza w jednym zdaniu |
| :--- | :---: | :---: | :--- |
| **1. Integracja Produkcyjna i Spójność Kodu z Changelogiem** | **10 / 25** | 25 | `audytor_lancuch.py` **nie jest w ogóle wpięty w produkcję**, `priv_engine.py` **nie istnieje na dysku** (został tylko sierocy `.pyc`), a `CHANGELOG` przypisuje kodowi funkcje (`HARD_REJECT_PATTERNS`, `MAX_RISK_MULTIPLIER = 1.15`, `DNI_MIN = 3`), których w `config.py` i `wycena_kalkulator.py` **nie ma**. |
| **2. Jakość Promptów i Odporność na Overfitting** | **14 / 20** | 20 | Szkielet 4 akapitów, Dual-Track i zakaz „wersji drugiej” są świetne, ale `agent_02a_opis_oferty.md` został **przeuczony (overfitted)** literalnymi zdaniami z 27 testowanych zleceń (`DGX`, `NVFP4`, `LEX vs OpenLEX`, `Three.js r185 + PrestaShop`, `WAPRO MAG`, `RMA`). |
| **3. Wiarygodność B2B i Bezpieczeństwo Portfolio na Priv** | **14 / 20** | 20 | Projekty 1, 2, 5, 6 mają twarde pokrycie, ale **Projekt 8 i Projekt 9** to syntetyczne „worki wszystkich brakujących technologii z Fali 3–5” z bardzo szczegółowymi metrykami (`>15 000 sesji/dobę`, `99,2% GA4`, `>12 000 SKU WAPRO`), które przy **8 umowach na profilu Useme** stanowią minę weryfikacyjną na priv. |
| **4. Uczciwość Danych i Metodologia Statystyczna (27 ofert)** | **15 / 20** | 20 | Krzywa jakości realnie rośnie, ale statystyka zbiorcza miesza 7 starych ofert z cache’u `v4` (nigdy nieprzetestowanych w Zero-Shot po reformie), pomija selekcjoner `AI #1` (etykiety wpisano ręcznie w `WAVE_SPECS`) i zawiera **bug podwójnego odejmowania kar (`-24 pkt` zamiast `-12 pkt`)**. |
| **5. Obiektywizm Ewaluacji (Ryzyko Single-Model Judge)** | **15 / 15** | 15 | Ten sam model (`deepseek-v4-pro`) pisze ofertę i ją ocenia, patrząc w tę samą kartę `tech_XX`, co premiuje ekstremalne upychanie żargonu (tzw. *Lexical Mirroring*). |

---

## 2. ZA CO DODANO PUNKTY (`[+]` — Twarde Osiągnięcia Inżynierskie i Konwersyjne)

1. **`[+22 pkt]` Architektura Dual-Track (`inzynieria` vs `biznes`) + Karta `tech_16` i 9 Scenariuszy Psychologicznych (`chain_executor.py:341-405`, `agent_02a_opis_oferty.md:23-37`):**
   - Rozdzielenie języka komunikacji na ścieżkę techniczną (Killshot architektoniczny w pierwszych 2 zdaniach) oraz biznesową (zakaz żargonu IT, „narzędzie w pudełku”, nazywanie po ludzku 2–3 życiowych wyjątków w „brudnych danych” klienta, np. mieszania `cm/mm` czy cytowanych wątków mailowych) rozwiązuje największy problem konwersji B2B na Useme.
   - Twardy routing w `_resolve_tech_cards()` (`chain_executor.py:404-405`): dla `sciezka == "biznes"` lub `typ_klienta == "tech_agnostic"` slot `02a` dostaje wyłącznie `["tech_16"]`, co fizycznie odcina model od kopiowania żargonu z kart `tech_01..15`.
2. **`[+18 pkt]` Dynamiczny Selektor i Sanitizer 16 Kart Wiedzy (`_resolve_tech_cards` + `_format_tech_card_for_slot` w `chain_executor.py:394-525`):**
   - Wycinanie z kart wiedzy Sekcji 1 (statystyki rynkowe) i Sekcji 6 (tabele wycen wielowariantowych i diagramy ASCII) przed wstrzyknięciem do `02a` oraz zamiana tabel Markdown `| A | B |` na czysty tekst bez `**` i bez `—` wyeliminowały plagę kopiowania wariantów cenowych i formatowania tabelarycznego do ofert.
   - Deterministyczna sanitacja wyjścia `02a` (`chain_executor.py:847-855`) czyści długie pauzy (`—`/`–`), gwiazdki `**`, etykiety z promptu (`Pytanie kwalifikujące:`, `Kluczowa mina:`), słowo-wytrych `kompleksowego` oraz hedging (`według mojej wiedzy`).
3. **`[+16 pkt]` Eliminacja Antywzorców Konwersyjnych B2B w `agent_02a_opis_oferty.md` i `jak_pisac_oferty.md`:**
   - Bezwzględny zakaz „Wersji Drugiej wycenianej osobno” (wszystkie mechanizmy odpornościowe wchodzą w cenę bazową).
   - Zastąpienie darmowego mielenia plików klienta i recytowania wewnętrznego regulaminu (*„To czysta próbka techniczna na danych testowych…”*) zasadą **Sandbox-First** (praca na kopii bazy / środowisku testowym bez ryzyka dla produkcji) + **30 dni gwarancji rozruchowej na własny kod**.
   - Twarde limity długości (`75–105 słów` dla zleceń `< 3 000 zł`, `145–195 słów` dla `>= 3 000 zł`), które wymuszają gęstość informacyjną.
4. **`[+15 pkt]` Urealnienie Kalkulatora Wycen (`wycena_kalkulator.py:20-45, 256-274`) i Zasada Anty-Dumpingowa:**
   - Ujednolicenie stawki godzinowej do sztywnych **`90 zł/h`** (`STAWKA_EFEKTYWNA = 90`) w całym systemie.
   - Obniżenie mnożników ryzyka w `policz_wycene()` (`brak_specyfikacji` z `1.30` na `1.05`; `ograniczenia_api` z `1.25` na `1.05` gdy istnieje już moduł API lub `1.15` gdy go brak; `real_time` z `1.20` na `1.10`), co zbiło zawyżone wyceny integracji ERP (np. `#144890` z `17 500 zł` do rynkowych `9 500 zł`).
   - Usunięcie mnożników dumpingowych `0.85` przy dużej konkurencji w `KOREKTY` (`wycena_kalkulator.py:37-45`).
5. **`[+15 pkt]` Architektura Niezależnego Audytora 1–100 (`audytor_lancuch.py` + `kryteria_audytu_100.md`):**
   - Połączenie deterministycznego pre-audytu w Pythonie (`deterministic_pre_audit()`) z ustrukturyzowaną matrycą 5 wymiarów (`A–E`) wymagającą cytatów dla każdego `[+]` i `[-]` pozwoliło precyzyjnie zdiagnozować błędy generatora w trakcie 5 fal testowych.
   - Zabezpieczenie `if score_r2 >= score_r1` w skryptach falowych uchroniło 5 z 27 ofert przed regresją w Rundzie 2 (`#144951`, `#2586109`, `#139571`, `#144249`, `#2643264`).
6. **`[+14 pkt]` Weryfikowalny Skok Jakości Zero-Shot w Falach 4–5 oraz Pokrycie Testami Jednostkowymi (`test_bot_audit.py`, `test_strategia_dual_track.py`):**
   - Na zupełnie nowych zleceniach w Falach 4–5 generator osiągnął w **Rundzie 1 (Zero-Shot, bez udziału Sędziego)** wyniki **`92–97 / 100 pkt`** w 7 z 8 zleceń (`#133275`: 97, `#143979`: 96, `#2749617`: 94, `#144077`: 93, `#2695589`: 92, `#2643264`: 92, `#144249`: 92).

---

## 3. ZA CO ODJĘTO PUNKTY (`[-]` — Bezlitosna Lista Błędów, Luk Produkcyjnych i Przekłamań w Danych)

### OBSZAR 1: Krytyczne Luki Integracji Produkcyjnej (`-15 pkt`)

* **`[-6 pkt]` `audytor_lancuch.py` NIE JEST WPIĘTY W PRODUKCJĘ (`engine.py` / `ai_pipeline.py` / `chain_executor.py` / `chain_config.json`):**
  - Produkcyjny bot (`engine.py:396` -> `ai_pipeline.py:276` -> `chain_executor.py:632`) uruchamia wyłącznie sloty z `kod/prompts/chain_config.json` (`01 -> 02b -> 02a -> 08`).
  - Żaden plik produkcyjny nie importuje `audytor_lancuch.py`! Ani `deterministic_pre_audit()`, ani `evaluate_offer_100()`, ani `regenerate_from_judge_feedback()`, ani `kryteria_audytu_100.md` nie uruchamiają się podczas działania bota produkcyjnego.
  - Docstring `audytor_lancuch.py:18` opisuje funkcję `run_adversarial_loop`, a `CHANGELOG:118` wymienia funkcję `audit_and_refine_100()` — żadna z tych dwóch funkcji nie istnieje jeszcze w `audytor_lancuch.py` (pętla naprawcza była w skryptach `run_audyt_wave1..5.py`).

* **`[-4 pkt]` Brak `priv_engine.py` (na dysku został tylko sierocy `.pyc`!) — Ślepota Bota po Odpowiedzi Klienta na Priv:**
  - Plik `kod/priv_engine.py` nie istnieje w repozytorium (został tylko skompilowany artefakt `kod/__pycache__/priv_engine.cpython-313.pyc`).
  - Gdy klient odpowie na nasze chirurgiczne pytanie kwalifikujące na priv, w systemie nie ma modułu konwersacyjnego, który odczytałby zapisane w `storage` metadane (`sciezka`, `typ_klienta`, `karta_tech`, `portfolio_baza.md`) i przygotował spójną odpowiedź domykającą sprzedaż.

* **`[-5 pkt]` Rozjazdy między `CHANGELOG` a Rzeczywistym Kodem (`config.py`, `wycena_kalkulator.py`, `mechanika_wyceniania.md`):**
  1. W `kod/config.py` jest `TRAP_KEYWORDS`, ale pre-filtr Czerwonego Oceanu znajduje się w `engine.py` / `ai_pipeline.py` — przy timeoucie `AI #1` (`ai_pipeline.py:194-196`) fallback przepuszcza wszystkie oferty bez odfiltrowania WordPress/SEO/Canva.
  2. W `wycena_kalkulator.py`:
     - `CAP_MNOZNIKOW = 1.8` (linia 27), a dla zleceń `retainer` (`linie 189-193`) nadal działają stare mnożniki `m *= 1.3` i `m *= 1.25`.
     - `MIN_DNI = 7` (linia 29, zgodnie z wymogiem formularza Useme `config.py:79`), przez co w `#2695589` kalkulator zwrócił `7 dni`, ale model w tekście oferty napisał `4 dni robocze`.
     - W `kod/prompts/kontekst/mechanika_wyceniania.md:83-91` nadal widnieją stare mnożniki tekstowe (`×1.3`, `×1.25`, `×1.2`).
  3. W `engine.py:404-413` brak blokady wysyłki, gdy `kwota_zgodna == False`. Ponadto w `chain_config.json:38-113` wisi 6 wyłączonych slotów (`03..07`, `20`).

---

### OBSZAR 2: Prompt Overfitting vs Generalizacja (`-6 pkt`)

* **`[-6 pkt]` Przeuczenie (Overfitting) `agent_02a_opis_oferty.md` i `audytor_lancuch.py` pod Konkretne Zlecenia z Próby 27 Ofert:**
  - Do głównego promptu systemowego `02a` wpisano literalne przykłady z konkretnych zadań z testu 27 ofert (`kancelaria prawna na DGX`, `NVFP4`, `QLoRA`, `BLoC`, `LEX vs OpenLEX`, `Three.js r185 + PrestaShop`, `WAPRO MAG`, `RMA`), zamiast trzymać w `02a` wyłącznie reguły uogólnione, a przykłady domenowe w kartach `tech_01..16`.

---

### OBSZAR 3: Ryzyko Wiarygodności Portfolio na Priv (`-5 pkt`)

* **`[-5 pkt]` Syntetyczne Konglomeraty w `portfolio_baza.md` (`Projekt 8` i `Projekt 9` oraz dopiski w `Projekt 1`) vs Publiczny Profil Useme (`8 zrealizowanych umów`):**
  - Na profilu Useme widnieje `8 zrealizowanych umów`, podczas gdy `Projekt 8` i `Projekt 9` zawierają szczegółowe metryki (`>15 000 sesji/dobę`, `99,2% GA4`, `>12 000 SKU WAPRO`, `45 WZ/dzień w Comarch XL`) bez adnotacji, że są to wdrożenia zespołu realizowane w bezpośrednich kontraktach B2B poza Useme (objętych NDA).

---

### OBSZAR 4: Uczciwość Statystyczna i Błędy Metodologiczne w Danych z 27 Ofert (`-6 pkt`)

* **`[-2 pkt]` Fala 1 (`runda_1` dla 7 ofert) w `audyt_100_wyniki_27_ofert.json` pochodzi ze starego `wyniki_live_v4.json` sprzed reformy:**
  - Gdy rozbijemy dane uczciwie według chronologii fal:
    - **Fala 1 (7 ofert ze starego `v4` sprzed reformy):** Średnia R1 = **`67,6 / 100`** (`41..93`).
    - **Fale 2–3 (12 ofert w trakcie iteracyjnej kalibracji):** Średnia R1 = **`85,2 / 100`** (`63..97`).
    - **Fale 4–5 (8 nowych ofert na dojrzałym systemie):** Średnia R1 = **`90,6 / 100`** (mediana **`92,0 / 100`**, przedział `81..96`).
* **`[-2 pkt]` Pominięcie Klasyfikatora `AI #1` (`filter_offers`) w skryptach falowych (`WAVE_SPECS` wpisane ręcznie).**
* **`[-2 pkt]` Bug Podwójnego Odejmowania Kar (`-24 pkt` zamiast `-12 pkt`) w `audytor_lancuch.py:278-286` oraz rozjazd progów słów (`120/225` w `audytor_lancuch.py` vs `110/205` w `02a`).**

---

### OBSZAR 5: Ślepe Plamki Sędziego (Single-Model Echo Chamber: `deepseek-v4-pro` ocenia `deepseek-v4-pro`)
1. **Komora Echa Słownikowego (*Lexical Mirroring / Keyword Stuffing Bias*)**: Sędzia nagradza maksymalną notą (`98–99/100`) oferty, które w 195 słowach upchną jak najwięcej haseł z karty wiedzy (`#144077`).
2. **Brak weryfikacji halucynacji domenowych spoza karty wiedzy** (np. obietnica eksportu XML w zamkniętych programach okiennych `WinCon/Liczokno` bez zastrzeżenia licencyjnego).
3. **Ślepota na drobne niespójności liczbowe**: W `#2695589` Sędzia przeoczył rozjazd `DNI: 7` (kalkulator) vs `4 dni robocze` (tekst), a w `#144077` przeoczył widełki `retainer 1500-2500 zł/mies.`.
