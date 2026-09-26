# KROK 7: Monitor Skrzynki i Protokół Priv (Od Zgłoszenia do Escrow)

Moduł telemetrii i konwersji odpowiedzialny za wykrywanie odpowiedzi zleceniodawców oraz prowadzenie wątku prywatnego aż do wpłaty zaliczki/escrow na Useme.

---

## 1. Zbieracz Danych Zwrotnych ([`kod/zbieracz_danych.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/zbieracz_danych.py))

Przed każdym nowym runem lub w dedykowanym cyklu silnik uruchamia procedurę `uruchom_zbieranie()`:
1. Pobiera wszystkie zlecenia o statusie `WYSLANO`.
2. Sprawdza wiek oferty: jeśli minął określony czas (`TIMEOUT_DNI`, np. 7 dni), sprawdza skrzynkę odbiorczą Useme.
3. Wywołuje metody BrowserDriver:
   - `driver.sprawdz_skrzynke(author_id, data_wyslania)`: sprawdza, czy pojawiła się nowa wiadomość od zleceniodawcy.
   - `driver.sprawdz_powiadomienia(job_id, job_title)`: sprawdza status odrzucenia lub wyboru oferty.
4. Aktualizuje status zlecenia w magazynie:
   - `PROZNIA`: brak jakiejkolwiek reakcji zleceniodawcy po upływie timeoutu.
   - `ODPOWIEDZ` / `WATEK_PRIV`: klient odpisał, otwarto wątek negocjacyjny.

---

## 2. 3-Krokowy Protokół Konwersji na Priv

Gdy zleceniodawca odpowie na ofertę, Ksawier (lub asystent priv) stosuje deterministyczny protokół 3 kroków:

### Krok 1: Trojan Horse (Żądanie Konkretnego Artefaktu)
- **Cel**: Wyeliminowanie "marzycieli" i wymuszenie zaangażowania klienta.
- **Działanie**: Zamiast ogólnej rozmowy prosimy o plik lub dostęp techniczny:
  - *"Żeby precyzyjnie potwierdzić czas realizacji, podeślij proszę przykładowy plik z danymi wejściowymi (lub schemat bazy/link do API)."*
- **Filtr Phantom Leads**: Jeśli klient nie posiada żadnych danych, specyfikacji ani dostępu, a jedynie "ogólną ideę", zostaje natychmiast zweryfikowany pod kątem budżetu.

### Krok 2: Odcięcie Ryzyka przez Depozyt Escrow Useme i Demo Guard
- **Cel**: Zapewnienie klienta o bezpieczeństwie bez sztucznego rozbijania projektu na niechciane mikrozlecenia (falsyfikacja: Mit 6 wykazał 0% konwersji na płatne etapy PoC).
- **Działanie**:
  - Klient Useme oczekuje pewnego siebie inżyniera, który rozwiąże problem kompleksowo.
  - Wyjaśniamy mechanikę depozytu: *"Środki trafiają do bezpiecznego depozytu Useme i są uwalniane dopiero po Twojej akceptacji i testach na stagingu – niczym nie ryzykujesz"*.
  - Jeśli klient ma wątpliwości technologiczne, stosujemy **Demo Guard**: szybki test na danych próbnych klienta (np. sparsowanie 1 próbki pliku, test webhooka w 20 minut na danych testowych) przed kliknięciem umowy. Zero wydawania kodu produkcyjnego przed escrow.

### Krok 3: Domknięcie Umowy i Wpłata Escrow na Useme
- **Zasada żelazna**: **Ani jedna linijka kodu produkcyjnego nie powstaje przed zaksięgowaniem środków w escrow Useme**.
- Po akceptacji warunków Ksawier generuje umowę przez interfejs Useme.
- Po otrzymaniu powiadomienia *"Zleceniodawca wpłacił środki"* rozpoczyna się właściwa realizacja.
