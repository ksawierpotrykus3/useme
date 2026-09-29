# ARCHITEKTURA SILNIKA — przepływ E2E
**STATUS: AKTUALNE** | Wartości liczbowe żyją w kod/config.py i kod/wycena_kalkulator.py.

---

## 1. Przepływ E2E
```
1.  Watchdog Useme         -> czekaj_na_dostepnosc_useme()
2.  Zbieracz danych        -> zbieracz_danych.py (flaga ZBIERACZ_AKTYWNY)
3.  Scrapuj zlecenia       -> browser_driver.py (Playwright + stealth, 2 kategorie)
4.  Zapisz w bazie         -> storage.py (badania/baza/<konto>/01_ofertowarka/<kategoria>/<job_id>.json)
5.  Filtr anty-tlum        -> odrzuc jesli > MAX_COMPETITOR_LIMIT ofert (chyba ze VIP keyword)
6.  AI selekcja            -> ai_pipeline.py (model selektora w chain_config.json)
7.  Pobierz detale         -> browser_driver.py (pelny opis, autor)
8.  AI lancuch generowania:
    Slot 01  Research      -> model search (fakty z sieci)
    Slot 02b Wycena        -> model + wycena_kalkulator.py (deterministyczna)
    Slot 00  Orchestrator  -> plan strategii + zakazy kontekstowe
    Slot 02a Tresc oferty  -> model (Dual-Track: oferta + priv)
    Slot 08  Walidator     -> audytor_lancuch.py (sedzia 1-100 + Sedzia Zdrowego Rozsadku)
9.  Anty-powtorka          -> Jaccard > PROG_PODOBNOSCI = przepisz (max 2 proby)
10. Globalne duplikaty     -> Jaccard > PROG_PODOBNOSCI_GLOBALNY z ostatnich 7 dni
11. Sanity check           -> stawka efektywna >= MIN_STAWKA_GODZINOWA?
12. Wypelnij formularz     -> form_driver.py (Playwright)
13. Wyslij lub DRY_RUN     -> engine.py (zrzut ekranu + potwierdzenie)
14. Pacing anty-ban        -> INTER_JOB_DELAY_RANGE / INTER_SLOT_DELAY_RANGE
```

## 2. Gdzie zyja parametry (NIE kopiowac wartosci do docs)
| Parametr | Zrodlo |
|---|---|
| Modele AI, proxy | kod/chain_config.json |
| Max ofert/kategorie, max konkurenci, limity | kod/config.py |
| Progi Jaccard, anty-powtorka | kod/ai_pipeline.py |
| Stawka, mnozniki, sanity check, min kwota | kod/wycena_kalkulator.py |
| Prog audytu 1-100 | kod/config.py (AUDYTOR_100_TARGET_SCORE) |
| Tryb DRY_RUN, tryb headless | kod/config.py |

## 3. Moduly silnika
| Modul | Rola |
|---|---|
| engine.py | petla orkiestracji (pobranie -> triaz -> wycena -> AI -> walidacja -> wysylka) |
| runner.py | punkt wejscia CLI (--dry-run, --single, --headless) |
| ai_pipeline.py | selekcja AI, generowanie ofert, anty-powtorka, walidacja kwoty |
| chain_executor.py | klient LLM (sloty z chain_config.json, SSE, retry, watchdog) |
| audytor_lancuch.py | sedzia 1-100 + Sedzia Zdrowego Rozsadku + auto-refine |
| wycena_kalkulator.py | deterministyczny kalkulator wycen |
| storage.py | baza stanu, deduplikacja, checkpointy, zapis atomowy |
| browser_driver.py | Playwright + stealth, scraping listy i detali |
| form_driver.py | wypelnianie formularza oferty (DRY_RUN/live) |
| bezpieczenstwo.py | kill switch (STOP), RunLimiter |
| config.py | centralna konfiguracja |