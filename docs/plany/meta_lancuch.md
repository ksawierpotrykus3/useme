# PLAN: Meta-lancuch wariantow ofert (2 konta)
**STATUS: PLAN** (pomysl, nie wdrozone w calosci)

Cel: przez tydzien bez reki zbierac dane, ktore warianty ofert dostaja odzew.

---

## 1. Zalozenia
- Dwa konta Useme, kazde z wlasnym cookies i slotem sesji.
- Jedno zlecenie obslugiwane przez oba konta, rozlozone w czasie.
- Na jedno zlecenie powstaja 2 rozne oferty (po jednej na konto).
- Konta nie robia tego samego zlecenia w tym samym momencie.
- Wnioski wyciaga czlowiek. System dostarcza porownywalne, nieprzypadkowe dane.

## 2. Kolejka i rozdzielenie
- Konto 1 bierze od konca listy (najstarsze), konto 2 od poczatku (najnowsze).
- Bramki: jedno zlecenie naraz tylko jedno konto; drugie konto czeka losowy odstep.
- Rejestr przypisania: ktore zlecenie na ktore konto.

## 3. Role (losowane 50/50 per zlecenie)
- Role NIE sa przypisane do konta na stale — losowane per zlecenie, zamieniane co zlecenie.
- Rejestr globalny, kluczowany po zleceniu.

## 4. Dwa tryby swobody (jedna mechanika)
- **Konserwatywny:** blisko sprawdzonej bazy, waski rozkaz, malo mutacji, punkt odniesienia.
- **Meta:** mocno mutuje, szuka wyroznikow, adres wariantu narzucany twardo.

## 5. Osie wariacji
Oferta = szkielet (staly) + osie (losowane). Szkielet nigdy sie nie mutuje.
- **Szkielet (nietykalny):** fakty o zleceniu, stack, twarde zasady stylu.
- **Warstwa A - Narracja:** otwarcie, struktura (akapit/punkty), ton, dlugosc (losowana adekwatnie do zlozonosci), zakonczenie.
- **Warstwa B - Tresc:** argument ceny, podejscie, wyroznik, dowod kompetencji.
- **Warstwa C - Relacja:** perspektywa, poziom kontaktu, pewnosc siebie.
- **Warstwa D - Forma:** gestosc techniczna, jezyk korzysci.
- **Zasada:** malo osi, malo wartosci na os. Roznorodnosc odczuwalna, ale powtarzalna statystycznie.

## 6. Twarde filtry (zawsze)
Brak em-dash, brak nawiasow, brak tabelek, glownie tekst, zakaz slow-wytrychow AI, zero markdownu.

## 7. Wycena (wspolna dla obu kont)
- Kwota z deterministycznego kalkulatora, nie od modelu.
- Research i wycena liczone RAZ na zlecenie, podawane obu wariantom.
- Obie oferty na to samo zlecenie dostaja IDENTYCZNA kwote i dni. Rozni sie tylko tresc.

## 8. Pamiec (klucz do nierobienia sie w kolko)
- ADRES wariantu (osie) losowany PER OFERTA.
- REJESTR historii PER KONTO + per klient.
- Drugie konto czyta oferte pierwszego, zakaz powtarzania formy i "amunicji" (faktow/CVE).

## 9. Bariera architektoniczna (fundament)
Aby research i wycena byly wspolne, trzeba rozdzielic lancuch na:
- ETAP WSPOLNY: slot 01 (research) + slot 02b (wycena) — raz na zlecenie.
- ETAP PER OFERTA: slot 02a (tresc) + walidator 08 — osobno dla kazdej oferty.
Wymaga: run_chain(..., stop_after="02b") + run_chain(..., injected_context={...}).

## 10. Kolejnosc wdrozenia
1. (A) Rozdzielenie lancucha na wspolny i per-oferta — FUNDAMENT.
2. (B) Warstwa kont (multi-account).
3. (C) Rejestr per konto (rozszerzenie anty-powtorki).
4. (D) Rozszerzenie adresu wariantu i variation_seed.
5. (E) Wykrywacz powtorzonej amunicji (obok Jaccarda).
6. (F) Osobny tryb konserwatywny.
7. (G) Kolejka, blokada, odstep czasowy.
8. (H) Losowanie 50/50 rol per zlecenie.
9. (I) Test na zywym zleceniu.

Zaleznosci: A jest fundamentem; C zalezy od B; D/E/F rownolegle po A; G/H zaleza od B i C; I na koncu.
Zasada: wszystko musi dzialac wstecznie zgodnie dla 1 konta. Wielokonto = rozszerzenie, nie zamiennik.

## 11. Co juz istnieje
- wycena_kalkulator.py (policz_wycene + formatuj_wynik), podpiety w chain_executor.py (slot 02b).
- Anty-powtorka per KLIENT: storage.find_by_author + engine.py (previous_offers, variation_seed) + ai_pipeline._podobienstwo_jaccard.
- BrowserDriver(cookies_path=...) i FormDriver(context=...) przyjmuja parametry.
- Checkpointy lancucha w storage.
- Multi-account: config.ACCOUNTS + aktywne_konta().