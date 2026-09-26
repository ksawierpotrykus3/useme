# Useme Core — Autonomiczny System Ofertowania B2B

System automatycznego wyszukiwania, wyceniania, generowania i składania ofert freelancerskich na platformie **Useme.com**, zoptymalizowany pod kątem maksymalnej konwersji w zleceniach programistycznych i integracyjnych (3 000 — 25 000 PLN).

Silnik bazuje na architekturze **Human Voice v6** — generowaniu ofert inżynierskich pozbawionych sztucznego szablonowości, z naturalnym językiem partnerskim, dwuetapowym rozliczeniem za efekt, zerowym ryzykiem dla klienta (staging/backup/dry-run) oraz precyzyjnymi pytaniami operacyjnymi.

---

## 📁 Struktura Repozytorium

```
useme_core/
├── kod/                       # Silnik produkcyjny bota
│   ├── engine.py              # Główna pętla orkiestracji (pobranie -> triaż -> wycena -> AI -> wysyłka)
│   ├── runner.py              # Punkt wejścia CLI z flagami (--dry-run, --single, --headless)
│   ├── ai_pipeline.py         # Zarządzanie łańcuchem promptów AI i bramkami jakości
│   ├── chain_executor.py      # Klient modeli LLM (DeepSeek / Gemini / OpenRouter)
│   ├── wycena_kalkulator.py   # Deterministyczny kalkulator stawek i podziału na etapy
│   ├── audytor_lancuch.py     # 100-punktowy sędzia jakości ofert i moduł auto-refine
│   ├── storage.py             # Baza stanu, unikanie duplikatów i historia wysyłek
│   ├── browser_driver.py      # Sterownik Playwright / przeglądarka z obsługą sesji
│   ├── form_driver.py         # Automatyczne wypełnianie i submission formularzy Useme
│   ├── bezpieczenstwo.py      # Kontrola limitów, budżetów i blokad anty-ban
│   ├── prompts/               # Mózg AI (generatory, walidatory, baza dowodowa)
│   │   ├── generatory/        # agent_01_research, agent_02a_opis_oferty (v6), agent_02b_wycena
│   │   ├── kontekst/          # jak_pisac_oferty, portfolio_baza, lore, stack_i_filozofia
│   │   └── walidatory/        # agent_03..agent_08 (styl, spójność, reguły bezpieczeństwa)
│   ├── tests/                 # 45 automatycznych testów jednostkowych i integracyjnych
│   └── lab/                   # Archiwum historycznych testów i eksperymentów z formularzem
│
├── badania/                   # Centrum badawczo-analityczne i mystery shopping
│   ├── audyt_100/             # Kompleksowy audyt 100 zleceń, turnieje AI i raporty
│   │   ├── README.md          # Indeks wszystkich 12 raportów, skryptów i zbiorów danych
│   │   ├── RAPORT_*.md        # Raporty z turniejów sędziowskich, ślepych testów i psychologii
│   │   ├── lab_*.py           # Skrypty laboratoryjne (Gemini, DeepSeek R1, 4 różne domeny)
│   │   └── wyniki_*.json      # Surowe dane ewaluacyjne i benchmarki
│   ├── baza/                  # Surowe dane z rynku (mystery shopping, zamknięte wątki)
│   ├── schemat_bota/          # 8 szczegółowych dokumentów architektury technicznej
│   ├── strategia/             # Wytyczne biznesowe, psychologia konwersji i zamykanie
│   └── teorie/                # Udokumentowane fakty, hipotezy i obalone mity o Useme
│
└── docs/                      # Dokumentacja operacyjna projektu
    ├── MASTER.md              # Globalna mapa systemu
    ├── CHANGELOG_REFORMY.md   # Dziennik ewolucji systemu
    ├── info/                  # Szczegóły kont, flow i lore
    └── trae/                  # Dokumentacja analityczna Trae AI
```

---

## 🚀 Uruchomienie Bota

### 1. Wymagania wstępne
- Python 3.11+
- Playwright zainstalowany i zainicjalizowany (`playwright install chromium`)
- Uruchomiony lokalny proxy LLM (`gemini_proxy` na porcie 8045 lub `deepseek-proxy` na porcie 4571)

### 2. Logowanie do Useme
Przed pierwszym uruchomieniem bota należy zapisać sesję przeglądarki:
```bash
python kod/login_useme.py
# lub użyj: kod/login_useme.bat
```

### 3. Uruchomienie w trybie próbnym (Dry-Run — bezpieczny, bez wysyłania)
```bash
python kod/runner.py --dry-run
```

### 4. Uruchomienie produkcyjne
```bash
python kod/runner.py
# lub użyj: kod/start.bat
```

---

## 🧪 Testy Jakości i Bezpieczeństwa

Wszystkie kluczowe moduły objęte są pakietem testów automatycznych:
```bash
pytest kod/tests -v
```
Aktualny stan testów: **45/45 zdanych (100% pass)** w ~3.1 sekundy.

---

## 🏆 Kluczowe Osiągnięcia Architektury (Human Voice v6)

W toku rygorystycznych badań laboratoryjnych (`badania/audyt_100/`) zweryfikowano:
1. **Zwycięstwo w Turnieju Sędziowskim**: Nowy styl generatora zajął **1. miejsce** w ocenach niezależnych sędziów AI (*Gemini 3.8 Flash*, *DeepSeek-Chat* oraz *DeepSeek R1*), pokonując topowych rynkowych freelancerów (w tym Antoniego).
2. **Uniwersalność Międzydomenowa**: Średnia ocena **86.3 / 100** w 4 skrajnie różnych domenach (WebGL 3D, BaseLinker, integracje Notion VoIP, przemysłowy CNC w języku angielskim).
3. **Złota Zasada Pytań Operacyjnych**: Zamiast irytować klientów pytaniami z bezradności na wstępie, bot proponuje kompletną architekturę i zadaje jedno precyzyjne pytanie wdrożeniowe.
4. **Hak Darmowej Próbki (Risk-Free Dry-Run)**: Bezpłatne sprawdzenie 1–3 plików/przypadków bez dotykania produkcyjnej bazy danych gwarantuje natychmiastowe przejście do rozmowy na priv.
