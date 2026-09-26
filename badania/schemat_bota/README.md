# STREFA 4: Schemat Działania Bota (Stan Faktyczny i Kroki Pipeline)

Strefa 4 odzwierciedla w sposób modularny i deterministyczny **aktualny stan produkcyjny kodu silnika bota** znajdującego się w katalogu [`kod/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/).

Jest to przestrzeń przeznaczona do stopniowej aktualizacji w miarę rozwoju kodu silnika, dodawania nowych modułów i optymalizacji konwersji.

---

## 1. Wykaz Kroków Produkcyjnych Bota

| Krok | Plik Dokumentacji | Główny Plik Kodu | Odpowiedzialność |
|:---:|:---|:---|:---|
| **00** | [`00_ARCHITEKTURA_CALOSCI.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/00_ARCHITEKTURA_CALOSCI.md) | [`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py) | Całościowy diagram stanu, pętla wielokontowa, obsługa limitów |
| **01** | [`krok_01_zbieranie_zlecen.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_01_zbieranie_zlecen.md) | [`kod/browser_driver.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/browser_driver.py) | Watchdog Useme HTTP 503, scraping IT & Serwisy, pobieranie detali |
| **02** | [`krok_02_selekcja_i_triage.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_02_selekcja_i_triage.md) | [`kod/ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py) | Filtr anty-tłum (>60), blokada własnego profilu, Selekcjoner AI (Tier A/B) |
| **03** | [`krok_03_kalkulacja_wyceny.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_03_kalkulacja_wyceny.md) | [`kod/wycena_kalkulator.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/wycena_kalkulator.py) | Stawka bazowa 90 PLN/h, reguła min. 7 dni, seed losowania per oferta |
| **04** | [`krok_04_pipeline_generacji_ai.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_04_pipeline_generacji_ai.md) | [`kod/chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py) | Agent 01 Research -> Agent 02b Wycena -> Agent 02a Opis z Question CTA |
| **05** | [`krok_05_bramka_walidacji.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_05_bramka_walidacji.md) | [`kod/chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py) | Agent 08 Weryfikator Zasad, pętla retry_from_02a, anty-powtórka Jaccarda |
| **06** | [`krok_06_formularz_i_wysylka.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_06_formularz_i_wysylka.md) | [`kod/form_driver.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/form_driver.py) | Playwright form automation, obsługa DRY_RUN, rejestracja statusu WYSLANO |
| **07** | [`krok_07_monitor_skrzynki_i_priv.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/schemat_bota/krok_07_monitor_skrzynki_i_priv.md) | [`kod/zbieracz_danych.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/zbieracz_danych.py) | Polling skrzynki Useme, filtr phantom leads, 3-krokowy protokół domykania escrow |

---

## 2. Zasady Utrzymania i Aktualizacji

1. Wszelkie zmiany w architekturze bota muszą być najpierw zweryfikowane w Strefie 2 (analizy danych) lub Strefie 3 (teorie i hipotezy).
2. Po zmianie kodu w `kod/` odpowiedni plik w Strefie 4 musi zostać zaktualizowany, aby zachować 100% zgodność dokumentacji z rzeczywistym działaniem programu.
