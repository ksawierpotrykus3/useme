# Skrypty i Narzędzia Analityczne Strefy 2

Katalog zawiera dedykowane skrypty w języku Python służące do przetwarzania surowych danych Useme, audytu statystycznego, badania archetypów klientów, generowania elitarnej bazy wiedzy oraz matematycznej weryfikacji pokrycia rynku.

---

## 1. Kategorie Narzędzi

### A. Narzędzia Weryfikacyjne i Dowodowe (Bieżące / Produkcyjne)
* [`weryfikuj_pokrycie_100.py`](file:///badania/analizy/skrypty_i_narzedzia/weryfikuj_pokrycie_100.py) – **Dowód 100% pokrycia rynku**: sprawdza każde z 343 zleceń inżynieryjnych poza stronami WWW z bazy empirycznej $N=470$ i przypisuje je deterministycznie do kart `tech_01` – `tech_16`. Zwraca wskaźnik pokrycia 100.0% ($0$ zleceń osieroconych).
* [`skrypt_audyt_470.py`](file:///badania/analizy/skrypty_i_narzedzia/skrypt_audyt_470.py) – Główny audytor zbioru danych $N=470$: analizuje statusy (56 wygranych/odpisanych, 414 zamkniętych/przegranych), budżety, mediany i rozkłady.
* [`weryfikacja_danych.py`](file:///badania/analizy/skrypty_i_narzedzia/weryfikacja_danych.py) – Walidator integralności plików JSON i spójności identyfikatorów zleceń.
* [`aktualizuj_wygrane_56.py`](file:///badania/analizy/skrypty_i_narzedzia/aktualizuj_wygrane_56.py) – Narzędzie aktualizujące metadane 56 wygranych transakcji (treści wiadomości, escrow).

### B. Głęboka Analiza Rynku i Klientów (Matryce 2D)
* [`skrypt_klient_x_tech.py`](file:///badania/analizy/skrypty_i_narzedzia/skrypt_klient_x_tech.py) – Generuje dwuwymiarową matrycę przecięcia: Archetypy Klientów $\times$ Technologie.
* [`gleboka_typologia_klientow.py`](file:///badania/analizy/skrypty_i_narzedzia/gleboka_typologia_klientow.py) – Segmentacja behawioralna zleceniodawców (Tradycyjne MŚP, E-commerce, Startup Founder, Agencja, Quick-Fix, itp.).
* [`profiler_zleceniodawcow.py`](file:///badania/analizy/skrypty_i_narzedzia/profiler_zleceniodawcow.py) – Profilowanie zachowań decyzyjnych, elastyczności cenowej i wrażliwości na żargon.
* [`generuj_profile_porownanie.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_profile_porownanie.py) – Zestawienie porównawcze cech zleceń wygranych vs odrzuconych.
* [`zapisz_typologie.py`](file:///badania/analizy/skrypty_i_narzedzia/zapisz_typologie.py) – Eksport struktur typologii do formatów JSON i Markdown.

### C. Łańcuchy Rozumowania AI i Generator Bazy Wiedzy
* [`krytyczny_red_team_audyt.py`](file:///badania/analizy/skrypty_i_narzedzia/krytyczny_red_team_audyt.py) – Uruchamia bezwzględny audyt krytyczny Red Team weryfikujący taktyki rynkowe, mechanikę priv vs public oraz eliminujący nadmiarowy overengineering.
* [`uruchom_mocny_lancuch_grupowy.py`](file:///badania/analizy/skrypty_i_narzedzia/uruchom_mocny_lancuch_grupowy.py) – Wykonuje łańcuchy wielodomenowe generujące 4 Syntezy Bojowe (`synteza_bojowa_01` – `04`).
* [`eksploruj_dzwignie_psychologia_wyceny.py`](file:///badania/analizy/skrypty_i_narzedzia/eksploruj_dzwignie_psychologia_wyceny.py) – Eksplorator dźwigni psychologicznych, struktur autorytetu i strategii wycen.
* [`generuj_elitarne_karty_technologiczne.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_elitarne_karty_technologiczne.py) – Generator kart ERP i Scrapingu (`tech_01` do `tech_04`).
* [`generuj_blok_1_mobile.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_blok_1_mobile.py) – Generator kart Mobile i VoIP (`tech_05` do `tech_07`, `tech_12`).
* [`generuj_blok_2_devops_backend.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_blok_2_devops_backend.py) – Generator kart DevOps, SQL, Node.js i .NET (`tech_08` do `tech_11`).
* [`generuj_reszte_bazy_wiedzy.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_reszte_bazy_wiedzy.py) – Generator kart Enova365/Odoo, Apps Script, AI/RAG oraz Tech-Agnostic (`tech_13` do `tech_16`).
* [`generuj_pojedyncza_karte.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_pojedyncza_karte.py) – Skrypt pomocniczy do precyzyjnego generowania pojedynczej karty.
* [`uruchom_lancuch_analizy.py`](file:///badania/analizy/skrypty_i_narzedzia/uruchom_lancuch_analizy.py) – Wczesny skrypt do testów sekwencyjnego promptingu.
* [`generuj_granularna_baze.py`](file:///badania/analizy/skrypty_i_narzedzia/generuj_granularna_baze.py) – Pierwsza wersja generatora matrycy technologicznej.

### D. Archiwum
* `stare_skrypty/` – Archiwum wczesnych skryptów zwiadowczych, crawlerów i parserów HTML z początkowego etapu pozyskiwania danych.
