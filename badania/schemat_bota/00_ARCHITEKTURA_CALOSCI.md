# ARCHITEKTURA GŁÓWNA SILNIKA BOTA (Stan Produkcyjny)

Niniejszy dokument przedstawia całościowy schemat działania produkcyjnego silnika bota zlokalizowanego w katalogu [`kod/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/).

---

## 1. Diagram Przepływu Danych (End-to-End State Machine)

```mermaid
flowchart TD
    Start(["Start Runu: engine.py"]) --> Watchdog["Watchdog Useme: czekaj_na_dostepnosc_useme()"]
    Watchdog --> KillSwitch{"Plik STOP lub Limit Czasu?"}
    KillSwitch -- Tak --> StopRun(["Zatrzymanie Silnika"])
    KillSwitch -- Nie --> AccountsLoop["Iteracja po Kontach (Multi-Account Cookies)"]

    subgraph Krok1_2 ["Krok 1 & 2: Zbieranie"]
        AccountsLoop --> FetchFeed["BrowserDriver: Pobranie z Kategori: IT i Serwisy"]
        FetchFeed --> DedupStore["Magazyn (Storage): Filtrowanie Duplikatów"]
        DedupStore --> FetchDetails["Pobranie Pełnych Detali (Full Description)"]
    end

    subgraph Krok3 ["Krok 3: Selekcja i Triage"]
        FetchDetails --> FilterCrowd["Filtr Anty-Tłum (> 60 ofert) + Blokada Własnego Profilu"]
        FilterCrowd --> AI_Selector["Selekcjoner AI (deepseek-v4-pro-nothink)"]
        AI_Selector --> TierSort["Sortowanie Kolejki: Tier A (Nisze) -> Tier B"]
    end

    subgraph Krok4_5 ["Krok 4 & 5: Generacja i Walidacja AI"]
        TierSort --> Agent01["Agent 01: Research Sieciowy (deepseek-v4-pro-search)"]
        Agent01 --> Agent02b["Agent 02b: Wycena i Liczba Dni (kalkulator 90 zł/h, min. 7 dni)"]
        Agent02b --> Agent02a["Agent 02a: Treść Oferty (Question CTA, podpis 'Ksawier')"]
        Agent02a --> Agent08["Agent 08: Bramka Walidatora Zasad (Weryfikacja rygorystyczna)"]
        Agent08 -- "FAIL: Feedback POPRAW" --> Agent02a
        Agent08 -- "PASS" --> SanityCheck{"Sanity-Check Wyceny & Anty-Powtórka Jaccarda"}
    end

    subgraph Krok6 ["Krok 6: Wysyłka"]
        SanityCheck -- "PASS" --> FormDriver["FormDriver: Wypełnienie Formularza Useme (Playwright)"]
        SanityCheck -- "FAIL" --> SanityBlock["Status: SANITY_BLOK"]
        FormDriver --> SaveSuccess["Zapis Statusu WYSLANO + Timestamp"]
    end

    subgraph Krok7 ["Krok 7: Telemetria i Priv"]
        SaveSuccess --> Zbieracz["Zbieracz Danych: Polling Skrzynki i Monitor Zleceniodawców"]
        Zbieracz --> PrivEngine["Protokół Priv: Odpowiedź < 15 min, Żądanie Artefaktu, Escrow + Demo Guard"]
    end
```

---

## 2. Kluczowe Komponenty Systemowe

| Komponent | Plik Źródłowy | Rola i Odpowiedzialność |
|:---|:---|:---|
| **Silnik Koordynacyjny** | [`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py) | Główna pętla wykonawcza, multi-account, limity czasu, obsługa wyjątków |
| **Sterownik Przeglądarki** | [`kod/browser_driver.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/browser_driver.py) | Playwright, zarządzanie kontekstem sesji, ciasteczka, omijanie Cloudflare |
| **Magazyn Danych** | [`kod/storage.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/storage.py) | Lokalna baza JSON, deduplikacja per zlecenie i per konto, checkpointy |
| **Łańcuch AI** | [`kod/ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py) | Izolowana warstwa AI, interfejs `filter_offers` oraz `generate_proposal` |
| **Egzekutor Slotów** | [`kod/chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py) | Sekwencyjne odpalanie agentów AI, pętla retry, parsowanie tagów i JSON |
| **Sterownik Formularza** | [`kod/form_driver.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/form_driver.py) | Automatyczne wpisywanie stawek, dni i treści na Useme, obsługa błędów sesji |
| **Zbieracz Informacji Zwrotnej**| [`kod/zbieracz_danych.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/zbieracz_danych.py) | Weryfikacja skrzynki Useme, sprawdzanie czy minął timeout, aktualizacja statusów |
