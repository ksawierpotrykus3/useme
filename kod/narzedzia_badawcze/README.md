# Narzędzia Badawcze i Synchronizacyjne (`kod/narzedzia_badawcze/`)

Przybornik stałych, wielokrotnego użytku narzędzi CLI podzielony na **Dwa Światy** oraz **Audyt i Diagnostykę Silnika** (zgodnie z wyrokami Izby Segregacji #9–#16).

---

## 🚀 Szybki Start — Jedna Komenda do Wszystkiego

```bash
# Synchronizacja z Useme + przeliczenie statystyk obu światów:
python kod/narzedzia_badawcze/aktualizuj_wszystko.py

# Tylko przeliczenie lokalnych statystyk i macierzy (bez zapytań sieciowych do Useme):
python kod/narzedzia_badawcze/aktualizuj_wszystko.py --tylko-statystyki

# Pełna synchronizacja + przeliczenie statystyk + Audyt AI przez lokalny serwer DeepSeek (port 4571):
python kod/narzedzia_badawcze/aktualizuj_wszystko.py --ai
```

---

## 🌍 Świat 1: Zleceniodawca / Mystery Shopping (`swiat_1_zleceniodawca/`)
Operuje na koncie zleceniodawcy (`weronikabuchholc13`, `cookies_zleceniodawca.json`) oraz bazie zlecenia `#144890`:

1. **[`sync_zlecenie.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_1_zleceniodawca/sync_zlecenie.py)**
   - Przyrostowo pobiera nowe oferty publiczne i wątki prywatne (PV) bez utraty istniejących rekordów.
   - Zapisuje `oferty_publiczne.json` (oraz kompatybilne `oferty_publiczne_30.json`), `wiadomosci_prywatne_pelne.json` i `raport_wiadomosci_prywatnych_zleceniodawcy.md`.
2. **[`przelicz_statystyki.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_1_zleceniodawca/przelicz_statystyki.py)**
   - Przelicza rozkłady cen, dni, długości, umów i wzmianek technologicznych/taktycznych (`analiza_cech_konkurencji.json`).
   - Synchronizuje podzielone paczki tekstów w `laboratorium_modeli/03_DANE_REFERENCYJNE/zlecenie_144890/`.
3. **[`audyt_nowych_ai.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_1_zleceniodawca/audyt_nowych_ai.py)**
   - Ocenia przyrostowo nowe oferty i wątki PV przez lokalny serwer DeepSeek (`http://127.0.0.1:4571`) oczami Klienta oraz Łowcy Zagrywek Psychologicznych.

---

## 🛠️ Świat 2: Wykonawca / Ofertowarka (`swiat_2_wykonawca/`)
Operuje na koncie wykonawcy (`ksawierpotrykus3`, `cookies.json`) oraz bazach `01_ofertowarka`, `02_przegrane`, `03_odpisane`:

1. **[`sync_konto.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_2_wykonawca/sync_konto.py)**
   - Sprawdza powiadomienia (`/pl/notifications/nots/`) oraz zamknięte oferty (`/pl/dashboard/offers/closed/`).
   - Dopisuje nowe zamknięte oferty do `02_przegrane/przegrane_pelne.json` (oraz `przegrane_pelne_416.json`) z zachowaniem wszystkich dotychczasowych rekordów.
   - Przenosi zlecenia w `01_ofertowarka/` ze statusu `WYSLANO` ("niewiadome") do `ZAMKNIETE_NIEODPISANE` ("nieodpisane / pewna porażka") lub `ODPOWIEDZ_KLIENTA`.
2. **[`przelicz_baze.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_2_wykonawca/przelicz_baze.py)**
   - Przelicza na żywo wszystkie statystyki dla aktualnej liczby $N$ zleceń (obecnie $425 + 56 = 481$):
     - `badania/analizy/01_dane_empiryczne.json` (oraz `01_dane_empiryczne_470.json`)
     - `badania/analizy/technologie/02_matryca_granularna_technologie_i_unmatched.json`
     - `badania/analizy/typy_klientow/02_matryca_2d_klient_x_tech.json`
     - `badania/analizy/03_analiza_zlecen_niewyslanych_selekcja.json`
3. **[`sekcja_porazek_ai.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/swiat_2_wykonawca/sekcja_porazek_ai.py)**
   - Wykonuje Sekcję Porażek (Failure Alchemy) przez `http://127.0.0.1:4571` dla nowo zamkniętych ofert i generuje `RAPORT_SEKCJA_PORAZEK_OFERTOWARKI.md`.

---

## 🔍 Audyt i Diagnostyka Silnika (`audyt_i_diagnostyka/`)
Zawiera pomocnicze skrypty diagnostyczne i historyczne ekstraktory przeniesione z głównego katalogu `kod/` oraz `kod/lab/` (m.in. `engine_audit.py`, `deep_audit.py`, `pokaz_audyt.py`, `weryfikuj_konkurencje_48h.py`, `check_budgets.py`, `check_crm_leaks.py`, `check_mobile.py`).
