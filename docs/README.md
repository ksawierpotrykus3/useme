# docs/ — dokumentacja projektu useme_core

Ten folder opisuje **mechanikę i intencje** projektu. Nie zawiera liczb stanu (statusy, liczniki, daty "na dziś") — te żyją w kodzie i bazie.

## Jak sprawdzić aktualny stan (komendy, nie pliki)

```bash
# Status konfiguracji i flag
python -c "import sys; sys.path.insert(0,'kod'); import config; print(config.DRY_RUN, config.ZBIERACZ_AKTYWNY)"

# Liczba i statusy zleceń w bazie
# (zobacz pliki w badania/baza/<konto>/01_ofertowarka/*.json)

# Testy
cd kod; python -m pytest -q
```

## Struktura

| Folder/plik | Co zawiera |
|---|---|
| `architektura/` | Jak działa silnik: przepływ, wycena, selekcja |
| `referencje/` | Trwała wiedza o platformie Useme i operacjach |
| `STANDARD_DOKUMENTACJI.md` | Zasady trzymania porządku w docs |

## Zasady (skrót)

1. **Jedno źródło prawdy o liczbach** = kod (`config.py`, `wycena_kalkulator.py`). Dokumentacja cytuje, nie kopiuje.
2. **Zero liczników "na dziś"** w plikach .md.
3. **Każdy plik ma nagłówek** STATUS (AKTUALNE / PLAN / HISTORYCZNE).
4. **Jeden temat = jeden plik.**