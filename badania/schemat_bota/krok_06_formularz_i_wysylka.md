# KROK 6: Wypełnienie Formularza i Wysyłka (Playwright FormDriver)

Moduł automatyzacji interfejsu webowego Useme odpowiedzialny za bezbłędne złożenie oferty na portalu.

---

## 1. Architektura FormDriver ([`kod/form_driver.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/form_driver.py))

FormDriver operuje w kontekście przeglądarki Playwright z zachowaniem ciasteczek sesyjnych danego konta.

### Główne etapy:
1. **Nawigacja do formularza zlecenia**:
   - URL: `https://useme.com/pl/jobs/{job_id}/` (lub bezpośredni URL zlecenia).
   - Kliknięcie przycisku *"Złóż ofertę"* / *"Dodaj ofertę"*.
2. **Wypełnienie pól formularza**:
   - Pole kwoty netto: wpisanie `proposal.wycena` (np. 1500).
   - Pole liczby dni roboczych: wpisanie `proposal.dni` (minimum 7 dni).
   - Pole opisu oferty: wklejenie sformatowanego tekstu z zachowaniem podziału na akapity.
3. **Zarządzanie Trybem DRY-RUN vs LIVE**:
   - W trybie `DRY_RUN = True`: FormDriver wypełnia pola, wykonuje zrzut ekranu (screenshot) do folderu `debug/`, po czym zamyka stronę **bez kliknięcia przycisku finalnego**. Status: `PRZYGOTOWANA`.
   - W trybie `DRY_RUN = False`: FormDriver klika przycisk zatwierdzający, weryfikuje komunikat sukcesu (*"Twoja oferta została złożona"*), rejestruje status: `WYSLANO` oraz zapisuje dokładny znacznik czasu ISO `data_wyslania`.

---

## 2. Obsługa Błędów i Zabezpieczenia

1. **Wygasłe Ciasteczka Sesji (HTTP 401/403)**:
   - Zgłoszenie `AuthenticationRequiredError`.
   - Natychmiastowe przerwanie pracy dla danego konta, powiadomienie w logach i przejście do kolejnego konta lub zatrzymanie.
2. **Blokada Podwójnej Wysyłki per Konto**:
   - Metoda `storage.czy_konto_juz_oferowalo(job_id, konto_id)` uniemożliwia złożenie dwóch ofert z tego samego konta na to samo ogłoszenie.
3. **Naturalne Odstępy Czasowe (Anty-Ban)**:
   - Po każdej udanej wysyłce w trybie live silnik stosuje losową pauzę (`MIN_DELAY_BETWEEN_OFFERS_S`), symulując naturalny czas pisania oferty przez człowieka.
4. **Licznik Dzienny**:
   - Rejestracja liczby wysłanych ofert w module [`bezpieczenstwo.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/bezpieczenstwo.py).
