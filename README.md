# useme_core — autonomiczny system ofertowania B2B

System wyszukiwania, wyceniania, generowania i skladania ofert freelancerskich na **Useme.com**, zoptymalizowany pod zlecenia programistyczne i integracyjne (3 000 — 25 000 PLN).

Silnik oparty na architekturze **Human Voice v6**: naturalny jezyk partnerski, bez szablonowosci, dwuetapowe rozliczenie, zerowe ryzyko dla klienta (staging/backup/dry-run) i precyzyjne pytania operacyjne.

## Struktura repozytorium

```
useme_core/
├── kod/          # Silnik produkcyjny bota (engine, ai_pipeline, chain_executor, wycena_kalkulator,
│                 # audytor_lancuch, storage, browser_driver, form_driver, config, prompts, tests)
├── badania/      # Dane i analizy (baza zlecen, typy klientow, technologie, case studies)
├── teorie/       # Fakty, hipotezy i obalone mity o Useme
├── audyty/       # Audyty ofert (dane historyczne)
└── docs/         # Dokumentacja operacyjna (architektura, referencje, plany, historia)
```

## Jak sprawdzić stan (komendy, nie pliki)

```bash
python kod/runner.py --dry-run        # uruchomienie w trybie probnym (bez wysylki)
pytest kod/tests -v                    # testy automatyczne
```

## Gdzie co jest

- **Jak działa silnik** → `docs/architektura/`
- **Wiedza o platformie Useme** → `docs/referencje/`
- **Pomysły i plany** → `docs/plany/`
- **Historia (post-mortem, reformy)** → `docs/historia/`
- **Dane i analizy rynku** → `badania/`
- **Zasady dokumentacji** → `docs/STANDARD_DOKUMENTACJI.md`

## Konta
Ksawier Potrykus (wlasciciel) + Maksymilian (partner inzynieryjny). Sesje przez pliki cookies (poza repozytorium).