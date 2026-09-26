# useme_core — Mapa projektu

## Struktura katalogów

Root `useme_core/` zawiera trzy foldery: `kod/`, `docs/`, `badania/`.

### `kod/` — silnik bota (co się uruchamia)
- `engine.py`, `ai_pipeline.py`, `chain_executor.py`, `wycena_kalkulator.py`, `browser_driver.py`, `form_driver.py`, `storage.py`, `config.py`, `bezpieczenstwo.py`
- `kod/prompts/` — mózg AI (generatory, walidatory, kontekst)
- `kod/lab/` — testy laboratoryjne silnika
- `kod/tests/` — testy pytest
- `kod/tech/` — dokumentacja techniczna, cookies
- `kod/data/` — stany pipeline'ów zleceń
- `kod/debug/` — zrzuty ekranu z wysyłek

### `docs/` — dokumentacja projektu
- `MASTER.md` — pełna mapa projektu
- `CHANGELOG_REFORMY.md` — historia zmian
- `docs/info/` — plany, przepływ, lore, konta, struktura danych
- `docs/trae/` — reasoning i hipotezy (Trae AI)

### `badania/` — dane, analizy i strategia
- **`baza/`** — baza operacyjna (jedno źródło prawdy): `<konto>/<podział>/`
  - `ksawierpotrykus3/` — `01_ofertowarka/`, `02_przegrane/`, `03_odpisane/`, `_paczki_i_probki/`
  - `weronikabuchholc13/` — `04_moje_zlecenia/` (zlecenia testowe + oferty + wiadomości per zlecenie)
- **`rynek/`** — dane o rynku Useme: kategorie, snapshoty, scrapowane podstrony, `katalog_ofert/`, `profil/`
- **`skrypty/`** — skrypty Pythona do pobierania i analizowania danych
- **`strategia/`** — wiedza biznesowa (patrz `strategia/README.md`):
  - `00_rdzen_strategii/` — pliki operacyjne (kompendium, arsenal zamykania, strategia główna, plan portfolio, mystery shopping, lista zleceń)
  - `01_material_dowodowy/` … `06_system_bazy_klientow/` — materiały szczegółowe
  - `07_zrodla_unikalne/` — unikatowe źródła (profil, raport wywiadu, zasady pisania, lore)
  - `_archiwum/` — duplikaty i pliki historyczne

## Kontekst projektu
Ksawier Potrykus — freelancer na Useme.com, działa w duecie z Maksymilianem.
Specjalizacja: integracje ERP, automatyzacje, boty, konfiguratory 3D, e-commerce.
Cel: zwiększenie konwersji ofert w przedziale 3 000 — 25 000 PLN.