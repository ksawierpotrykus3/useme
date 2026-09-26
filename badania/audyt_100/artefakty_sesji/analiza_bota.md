# Krytyczna Analiza Bota Useme — Co Zmienić i Dlaczego

> Przeczytałem **każdy plik** w `useme_core/kod/` i `prompts/`, `tech/`, skrypty badawcze. Poniżej moja krytyczna ocena — zgodnie z Twoim poleceniem **"nie ufaj ślepo plikom"**.

---

## TL;DR — 5 Najważniejszych Problemów

| # | Problem | Waga | Koszt naprawy |
|:--|:--------|:-----|:--------------|
| 1 | **6 z 7 walidatorów wyłączonych** — pipeline de facto nie waliduje | 🔴 Krytyczny | Niska (włączenie + poprawa promptów) |
| 2 | **Hardcoded data `"2026-09-21"` w engine.py:213** — bomba zegarowa | 🔴 Krytyczny | Minimalna |
| 3 | **Endpoint proxy: port 4571 vs dokumentacja 4570** — niespójność | 🟡 Średni | Konfiguracja |
| 4 | **Stawka 90 zł/h jest nadmiarowo zduplikowana ~15 razy** — false sense of control | 🟡 Średni | Refaktor |
| 5 | **Zbieracz danych wyłączony + selektory "NIEPOTWIERDZONE"** — martwy moduł | 🟡 Średni | Decyzja biznesowa |

---

## 🔴 Problemy Krytyczne

### 1. Pipeline walidacji jest MARTWY

[chain_config.json](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/chain_config.json) definiuje 10 slotów (3 generatory + 7 walidatorów). W rzeczywistości:

| Slot | Rola | Enabled? | Stan |
|:-----|:-----|:---------|:-----|
| 01 research | generator | ✅ | Działa |
| 02b wycena | generator | ✅ | Działa |
| 02a opis | generator | ✅ | Działa |
| 03 walidator_opisu | validator | ❌ | **3 linijki promptu** |
| 04 spojnosc | validator | ❌ | **3 linijki** |
| 05 ton_i_styl | validator | ❌ | **3 linijki** |
| 06 bledy_jezykowe | validator | ❌ | **3 linijki** |
| 07 kompletnosc | validator | ❌ | **3 linijki** |
| 08 weryfikacja_zasad | validator | ✅ | **Jedyny działający** |
| 20 ostatni_rzut_oka | validator | ❌ | **3 linijki** |

**Dlaczego to problem:**
- Masz rozbudowany system walidatorów w kodzie (`chain_executor.py` — retry logic, feedback loops, `_extract_feedback`, `POPRAW_WYCENA`/`POPRAW_OFERTA`), ale 6 z 7 walidatorów to **stuby z 3 linijkami**.
- Jedynym aktywnym walidatorem jest `08_weryfikacja_zasad`, który jest co prawda solidny (pełny prompt z regułami), ale robi robotę za 7 walidatorów naraz.
- System feedbacku (`POPRAW_OFERTA`, `POPRAW_WYCENA`) w `chain_executor.py` ma limit 2 rund poprawek — wystarczający, gdyby walidatory faktycznie coś robiły.

**Pytanie do Ciebie:** Czy te walidatory zostały specjalnie wyłączone (bo waliły false-positives / spowalniały pipeline / kosztowały tokeny), czy po prostu nie zostały dokończone?

---

### 2. Hardcoded data w engine.py — bomba zegarowa

[engine.py:213](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py#L213):
```python
and scraped_at >= "2026-09-21"
```

To filtruje zlecenia z magazynu, które mogą być dodane do kolejki selekcji. Ta data jest **wpisana na sztywno** — za kilka tygodni wszystkie "stare" zlecenia z magazynu będą dawno po tej dacie, ale jeśli kiedyś zmienisz coś w strukturze dat, ta linia cicho ominie zlecenia. 

**Co powinno być:** relatywna data, np. `datetime.now() - timedelta(days=7)` lub parametr w `config.py`.

---

### 3. Endpoint proxy: 4571 vs 4570

**Dokumentacja** ([AI_INTEGRACJA.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tech/AI_INTEGRACJA.md), [TECH_STACK.md](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/tech/TECH_STACK.md)):
```
http://localhost:4570/v1
```

**Kod** ([chain_executor.py:44](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py#L44)):
```python
DEEPSEEK_API_URL = "http://127.0.0.1:4571/v1/chat/completions"
```

Dokumentacja mówi 4570, kod używa 4571. Jedno z nich jest stale, drugie jest notatką historyczną. Ale ktoś czytający dokumentację (albo AI) dostanie sprzeczną informację.

**Pytanie do Ciebie:** Który port jest aktualny? I czy port powinien być w `config.py` zamiast zahardcodowany?

---

## 🟡 Problemy Strukturalne

### 4. Stawka 90 zł/h powtórzona 15+ razy

W [wycena_kalkulator.py](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py#L20-L23):
```python
STAWKA_EFEKTYWNA = 90
STAWKA_TIER_A = 90
STAWKA_MIN = 90
STAWKA_MAX = 90
```

Plus komentarze w promptach powtarzają "90 zł/h" wielokrotnie. Plus linia 170:
```python
stawka = STAWKA_EFEKTYWNA  # ta linia NADPISUJE wszystko powyżej!
```

Linie 162-170 to **martwy kod** — cała logika `if is_tier_a / elif stawka_godzinowa_klienta / else` jest na końcu **nadpisana** przez linia 170 `stawka = STAWKA_EFEKTYWNA`. Funkcja `wylosuj_stawke()` i `stawka_dla_oferty()` losują z zakresu `randint(90, 90)` — czyli zawsze 90. Offset jest zawsze 0.

**Dlaczego to problem:** To wygląda jak pozostałość po planach dynamicznej stawki, które zostały porzucone. Ale zamiast usunąć stary kod, dodano linie overridujące. Efekt: ktoś (lub AI modyfikujący kod) myśli że stawka jest konfigurowalna, a naprawdę jest zamrożona.

**Sugestia:** Uprość do jednej stałej `STAWKA = 90` i usuń martwą logikę.

---

### 5. Korekta konkurencyjna nie obniża — wszystkie mnożniki to 1.0

[wycena_kalkulator.py:37-44](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py#L37-L44):
```python
KOREKTY = [
    (0, 1, 20, None, 1.0),    # swieze do 24h, >=20 ofert
    (0, 1, 0, 20, 1.0),       # swieze do 24h, <20
    (1, 3, 20, None, 1.0),    # 1-3 dni, >=20
    (1, 3, 0, 20, 1.0),       # 1-3 dni, <20
    (3, None, 0, 10, 1.15),   # >3 dni, <10 (marża)
    (3, None, 10, 30, 1.0),   # >3 dni, 10-30
    (3, None, 30, None, 1.0), # >3 dni, >30 — USUNIĘTO DUMPING
]
```

Komentarz mówi "USUNIĘTO DUMPING" — prawie wszystkie mnożniki to `1.0`. Jedyna wyjątkowa sytuacja to `1.15x` (zlecenie >3 dni, <10 ofert). Cała ta tablica jest prawie no-op.

**To nie jest "błąd"** — to świadoma decyzja ("stop wyścigowi na dno"). Ale jeśli konkurencyjność cenowa nie jest celem, to **cała tablica KOREKTY i funkcja `_korekta_konkurencyjna()` mogą być usunięte** i zastąpione stałym `1.0`.

---

### 6. `ZBIERACZ_AKTYWNY = False` + selektory "NIEPOTWIERDZONE"

[config.py:143](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/config.py#L137-L143):
```python
# UWAGA: selektory DOM w BrowserDriver.sprawdz_skrzynke / sprawdz_powiadomienia
# sa NIEPOTWIERDZONE na realnym DOM Useme [...]
# Na czas nieobecnosci (wakacje) trzymamy zbieracz WYLACZONY
ZBIERACZ_AKTYWNY = False
```

Zbieracz danych (weryfikacja odpowiedzi klienta) jest wyłączony. Komentarz mówi "na czas wakacji", ale selektory DOM nie były nigdy potwierdzone. To znaczy, że:
- Bot wysyła oferty, ale **nie wie, czy ktoś odpisał**.
- Cały feedback loop (Faza 2 z `DOKUMENTACJA_EKSPANSJI.md`) nie istnieje.

**Pytanie do Ciebie:** Czy zbieracz powinien wrócić? Czy macie ręczny sposób na śledzenie odpowiedzi?

---

## 🟢 Co Działa Dobrze (obiektywnie)

### Solidna architektura bezpieczeństwa
- **Kill switch** (`STOP` file) — sprawdzany w wielu punktach pipeline'u
- **Twardy limit czasu** (`MAX_RUN_MINUTES = 180`)
- **Circuit breaker** w `chain_executor.py` (max kroków + wall-clock watchdog 600s)
- **Atomowy zapis** (`atomic_write_json`) — ochrona przed 0KB plikami
- **Checkpointy** — wznawianie po przerwaniu
- **Blokada własnego profilu** (`wer13`) — sprawdzana w 4 różnych miejscach
- **DRY_RUN** z dowodami (zrzuty ekranu)
- **Sanity check** efektywnej stawki (nie pozwala na zaniżenie poniżej 85 zł/h)
- **Anti-repeat** (Jaccard similarity per klient + globalnie)

### Hybrydowa architektura wyceny
Podział na:
1. **Model AI** (agent 02b) → struktura JSON (moduły, godziny, flagi)
2. **Deterministyczny kalkulator Python** → kwota + dni

To jest mocne — model nie "wymyśla" ceny, tylko dostarcza rozbicie, a Python liczy. To eliminuje halucynacje cenowe.

### Dojrzały system scrapingu
- `BrowserDriver` z obsługą Cloudflare (headless=False fallback)
- `FormDriver` z nadpisywaniem draftów, obsługą rich-text edytora, dwuetapową weryfikacją wysyłki
- Deduplikacja per konto (konto1 i konto2 mogą wysłać ofertę na to samo zlecenie niezależnie)

---

## 🔍 Sprzeczności Dokumentacja vs Kod

| Temat | Dokumentacja mówi | Kod robi | Ocena |
|:------|:-------------------|:---------|:------|
| Port proxy | 4570 | 4571 | ⚠️ Niespójność |
| Model selekcji | `deepseek-v4-pro` | `deepseek-v4-pro-nothink` | 🟢 Nothink to lepsza decyzja (szybkość) — ale docs nieaktualne |
| Walidatory 03-07 | "Opcjonalne, domyślnie disabled" | Stuby 3-liniowe, nigdy nie były prawdziwe | 🟡 Docs sugerują gotowość, kod mówi co innego |
| `Camoufox/Firefox` | `TECH_STACK.md`: "❌ nie jako główny stack" | `turnstile_solver.py` importuje `AsyncCamoufox` | 🟡 Solver istnieje, docs mówią "nie" |
| Stawki AI | `AI_INTEGRACJA.md`: "110 PLN/h, 95 PLN/h" | Kalkulator: zawsze 90 PLN/h | 🟡 Docs z testów, kalkulator to source of truth |
| Dwuetapowy AI | `AI_INTEGRACJA.md`: "AI #1 + AI #2" | Teraz: AI selekcja + 3-slotowy łańcuch (research + wycena + opis) + walidator | 🟢 Kod ewoluował, docs nie |

---

## 📋 Proponowane Zmiany (do dyskusji)

### Priorytet 1 — Quick Wins (1-2h)

1. **Zamień hardcoded datę** `"2026-09-21"` na `(datetime.now() - timedelta(days=7)).isoformat()[:10]`
2. **Przenieś port proxy** do `config.py` jako `DEEPSEEK_API_URL`
3. **Uprość stawkę** — usuń martwy kod w `wycena_kalkulator.py` (linie 58-77, 162-169), zostaw jedną stałą

### Priorytet 2 — Architektura (4-8h)

4. **Zdecyduj co z walidatorami 03-07:**
   - Opcja A: Usuń stuby i tabelę w chain_config (jeśli agent_08 wystarczy)
   - Opcja B: Napisz prawdziwe prompty i włącz 2-3 najważniejsze (np. 04_spojnosc + 06_bledy_jezykowe)
5. **Zaktualizuj dokumentację techniczną** — `AI_INTEGRACJA.md` i `TECH_STACK.md` są z epoki testów, nie odzwierciedlają aktualnego stanu
6. **Zdecyduj co ze zbieraczem** — albo napraw selektory i włącz, albo wywal komentarz "na czas wakacji"

### Priorytet 3 — Ulepszenia (opcjonalne)

7. **Dodaj metryki** — ile ofert wysłano, ile odpowiedzi, response rate (teraz zbieracz jest wyłączony, więc nie ma żadnych metryk)
8. **Refaktor `engine.py`** — linie 193-225 (szukanie "zalegających" zleceń z magazynu) to 30 linii zagnieżdżonego kodu, które duplikują logikę z liniami 267-292. To powinno być w Storage
9. **`turnstile_solver.py` (1533 linie)** — ten plik pochodzi z innego projektu (Cardmarket — komentarze wprost mówią "cardmarket.com"). Czy jest w ogóle używany przez useme_core? Jeśli nie — wywal
10. **Korekta konkurencyjna** — albo zrób z niej prawdziwy mechanizm, albo usuń (teraz to tablica samych `1.0`)

---

## Pytania Do Ciebie

1. **Walidatory 03-07**: Wyłączone specjalnie (zbyt wolne / drogie / false positives) czy po prostu niedokończone?
2. **Port proxy 4570 vs 4571**: Który jest aktualny?
3. **Zbieracz danych**: Macie ręczne śledzenie odpowiedzi klientów? Czy ta informacja jest w ogóle potrzebna?
4. **Turnstile solver**: Czy jest używany przez bota czy to martwy import z Cardmarket?
5. **Stawka 90 zł/h**: Czy planujecie kiedykolwiek wrócić do dynamicznej stawki, czy na stałe 90?
6. **Ile ofert dziennie wysyła bot realnie?** (Pytam, bo nie ma żadnych metryk ani logów sukcesu — nie wiem czy bot jest efektywny)
