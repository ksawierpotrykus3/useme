# useme_core — autonomiczny system ofertowania B2B

System wyszukiwania, wyceniania, generowania i składania ofert freelancerskich na **Useme.com**, zoptymalizowany pod zlecenia programistyczne i integracyjne (3 000 — 25 000 PLN).

Silnik oparty na architekturze **Human Voice v6**: naturalny język partnerski, bez szablonowości, dwuetapowe rozliczenie, zerowe ryzyko dla klienta (staging/backup/dry-run) i precyzyjne pytania operacyjne.

## Struktura repozytorium

```
useme_core/
├── kod/          # Silnik produkcyjny bota (engine, ai_pipeline, chain_executor, wycena_kalkulator,
│                 # audytor_lancuch, storage, browser_driver, form_driver, config, prompts, tests)
├── docs/         # Dokumentacja operacyjna (architektura silnika, referencje Useme, standard dokumentacji)
├── badania/      # Dane i analizy (baza zleceń, analizy empiryczne, audyt_100, teorie)
└── audyty/       # Auto-generowane raporty audytu 100-pkt pojedynczych ofert (output pokaz_audyt.py)
```

## Jak sprawdzić stan (komendy, nie pliki)

```bash
python kod/runner.py --dry-run        # uruchomienie w trybie próbnym (bez wysyłki)
pytest kod/tests -v                    # testy automatyczne
```

## Gdzie co jest

- **Jak działa silnik** → `docs/architektura/`
- **Wiedza o platformie Useme i operacjach** → `docs/referencje/`
- **Dane i analizy rynku** → `badania/`
- **Raporty z testów ofert** → `badania/audyt_100/`
- **Fakty, hipotezy i obalone mity** → `badania/teorie/`
- **Zasady dokumentacji** → `docs/STANDARD_DOKUMENTACJI.md`

## Konta

Ksawier Potrykus (właściciel) + Maksymilian (partner). Sesje przez pliki cookies (poza repozytorium).