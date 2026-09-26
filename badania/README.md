# ARCHITEKTURA BADAWCZA USEME (Struktura 4 Stref)

Główne centrum wiedzy rynkowej, analiz statystycznych oraz mechaniki produkcyjnej systemu automatycznego ofertowania na Useme.

Projekt ofertowarki stanowi główne narzędzie przychodowe, dlatego struktura badawcza została sformalizowana w **4 odizolowane strefy inżynierskie**, eliminując amatorskie porady na rzecz twardych dowodów transakcyjnych.

---

## Przegląd 4 Stref Architektury

```
badania/
├── baza/               # [STREFA 1] Baza Surowa (nienaruszone JSON-y, zlecenia, kontrakty, wiadomości)
├── rynek/              # [STREFA 1] Surowy rynek Useme w podziałach na kategorie
│
├── analizy/            # [STREFA 2] Analizy i Badania Danych Empirycznych
│   ├── typy_klientow/  # Archetypy zleceniodawców, filtry pułapek, matryce behawioralne
│   ├── technologie/    # 28 nisz rynkowych, segment tech-agnostic (33%), wskaźniki Win Rate
│   ├── portfolio/      # Plan pozycjonowania, mystery shopping, zlecenia do wystawienia
│   ├── case_studies/   # Prawdziwe zlecenia Ksawiera (w tym Doktor Monika 12 100 PLN)
│   └── skrypty_i_narzedzia/ # Pythonowe skrypty audytujące i przeliczające bazę 470 zleceń
│
├── teorie/             # [STREFA 3] Teorie i Hipotezy (Klasyfikacja Stopni Pewności)
│   ├── 01_stopien_twarde_fakty.md      # Pewność >95% (Przelew z Useme, n >= 100, Question CTA)
│   ├── 02_stopien_hipotezy_robocze.md  # Pewność 60-80% (Dual-track 67/33, Mobile Native, Faza 1)
│   ├── 03_stopien_poszlaki_niszowe.md  # Pewność 20-40% (Mała próba n < 15: TopSolid, VoIP, ERP)
│   └── 04_stopien_obalone_mity.md      # Pewność 0% (Phantom leads 34k/15k, call 15 min, IT żargon)
│
└── schemat_bota/       # [STREFA 4] Schemat Działania Bota (Odzwierciedlenie kodu w kod/)
    ├── 00_ARCHITEKTURA_CALOSCI.md      # End-to-end maszyna stanów silnika bota
    ├── krok_01_zbieranie_zlecen.md     # Watchdog Useme HTTP 503, Playwright, feed IT & Serwisy
    ├── krok_02_selekcja_i_triage.md    # Filtr anty-tłum (>60), blokada własna, Selekcjoner AI
    ├── krok_03_kalkulacja_wyceny.md    # Kalkulator 90 zł/h, reguła min. 7 dni, seed per konto
    ├── krok_04_pipeline_generacji_ai.md# System slotów: Agent 01 -> Agent 02b -> Agent 02a
    ├── krok_05_bramka_walidacji.md     # Agent 08 Weryfikator Zasad, retry loop, anty-powtórka
    ├── krok_06_formularz_i_wysylka.md  # FormDriver Playwright, obsługa DRY_RUN, status WYSLANO
    └── krok_07_monitor_skrzynki_i_priv.md # Zbieracz danych, timeout, 3-krokowy protokół priv
```

---

## Tabela Zależności i Przepływu Wiedzy

| Strefa | Nazwa Strefy | Źródło Wejściowe | Przeznaczenie |
|:---:|:---|:---|:---|
| **Strefa 1** | **Baza Surowa** (`baza/`) | Scraper portalu, API Useme, historia kont | Nienaruszalny grunt faktograficzny (Single Source of Truth) |
| **Strefa 2** | **Analizy Danych** (`analizy/`) | Dane ze Strefy 1 (470 zleceń) | Agregacja, matryce popytu, segmentacja 28 nisz, studia przypadków |
| **Strefa 3** | **Teorie i Hipotezy** (`teorie/`) | Wnioski ze Strefy 2 + testy Ksawiera | Filtracja założeń wg 4 progów pewności przed dotknięciem kodu |
| **Strefa 4** | **Schemat Bota** (`schemat_bota/`) | Kod silnika w `../kod/` | Precyzyjna dokumentacja pipeline'u bota aktualizowana z biegiem czasu |

---

## Status Folderu `strategia/`
Dawny folder `badania/strategia/` (zawierający monolit i poradniki) został w całości zarchiwizowany i zastąpiony powyższym podziałem na Strefy 2, 3 i 4.