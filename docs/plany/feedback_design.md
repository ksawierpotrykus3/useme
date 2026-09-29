# PROJEKT: feedback.py — jeden plik do zbierania feedbacku
**STATUS: PLAN / DO ZATWIERDZENIA**

## Podział odpowiedzialności
- **Ofertowarka (engine.py) JUŻ ZAPISUJE** i tego NIE ruszamy:
  - wszystkie zlecenia w 2 kategoriach
  - wszystkie moje wysłane oferty (na jakie zlecenia)
- **feedback.py zbiera TYLKO 3 rzeczy:**
  1. Wiadomości prywatne
  2. Porażki
  3. Zlecenia, które sam WRZUCIŁEM (posted) — per konto

## Komenda
```
python kod/feedback.py --konto konto2 --wiadomosci --z-ofert
python kod/feedback.py --konto konto2 --wiadomosci --ze-zlecen
python kod/feedback.py --konto konto1 --porazki
python kod/feedback.py --konto konto2 --wrzucone
python kod/feedback.py --konto all --wszystko
```

## Flagi (tylko te, nic więcej)
| Flaga | Co robi |
|---|---|
| `--konto konto1\|konto2\|all` | Które konto (all = iteruje config.ACCOUNTS) |
| `--wiadomosci` | Zbiera wiadomości prywatne |
| `--z-ofert` | (pod-flaga) tylko wiadomości od ofert; ODRZUCA te, co odpisali na moje zlecenie |
| `--ze-zlecen` | (pod-flaga) tylko wiadomości dot. zleceń które sam wstawiłem |
| `--porazki` | Scrap porażek aż do znanego rekordu |
| `--wrzucone` | Zapisuje moje WRZUCONE zlecenia (posted) do bazy |
| `--dry-run` | Nic nie zapisuje, pokazuje co znalazł |

## Cookies — prosty komunikat
Na starcie feedback.py sprawdza plik cookies dla danego konta.
Jeśli BRAK:
```
[BŁĄD] Brak cookies dla konto2 (tech/cookies2.json).
       Sesja wygasła lub nie zalogowano. Wrzuć świeży plik cookies i uruchom ponownie.
```
AI widzi to od razu i prosi użytkownika o cookies. Zero zgadywania.

## Rozróżnianie wiadomości (z-ofert vs ze-zlecen)
W bazie MAMY już tytuły:
- moich wysłanych ofert (01_ofertowarka)
- moich wstawionych zleceń (04_moje_zlecenia)

Wiadomość ma "Dotyczy: <tytuł>". Dopasowujemy tytuł do jednej z tych dwóch baz:
- pasuje do mojej wysłanej oferty → `--z-ofert`
- pasuje do mojego wstawionego zlecenia → `--ze-zlecen`

To proste, bo tytuły już są w bazie. Nic nie trzeba zgadywać.

## Struktura folderów per konto (ujednolicona, dowolna liczba kont)
```
badania/baza/<konto>/
├── 01_ofertowarka/      # (ofertowarka) zlecenia, na które wysłałem ofertę
├── 02_przegrane/        # (feedback --porazki) porażki
├── 03_odpisane/         # wygrane/odpisane
├── 04_moje_zlecenia/    # (feedback --wrzucone) MOJE wstawione zlecenia + oferty pod nimi
├── 05_kontakty.json     # (feedback --wiadomosci) rejestr wszystkich, którzy pisali
└── marker.json
```

## 05_kontakty.json — rejestr kontaktów (naprawia bug "dr Monika")
Klucz = user_id. Nigdy nie usuwamy kontaktu, tylko scalamy.
- Nowa wiadomość dopisuje wątek, nie kasuje starych.
- Brak kontekstu → `zrodlo=bez_kontekstu`, ale kontakt ZOSTAJE.
- Przy każdym uruchomieniu próbujemy ponownie dopasować (mogą dojść nowe dane).

```json
{
  "12345": {
    "user_id": "12345",
    "author_name": "Naviproject",
    "zrodlo": "offer | job | bez_kontekstu",
    "watki": [ { "thread_id": "999", "subject": "...", "messages": [...] } ],
    "liczba_wiadomosci": 6,
    "pierwszy_kontakt": "...", "ostatni_kontakt": "..."
  }
}
```

## Porażki (--porazki)
1. Scrapuj /pl/dashboard/offers/closed/ strona po stronie.
2. STOP gdy trafisz offer_id który JUŻ jest w bazie.
3. Nowe → pobierz detale, dopisz do 02_przegrane/.
4. Zmapuj job_id → przenieś status w 01_ofertowarka. Dane już są.

## Wrzucone (--wrzucone)
1. Scrapuj moje wystawione zlecenia (/pl/my-jobs/).
2. Zapisz do 04_moje_zlecenia/<job_id>/ (opis + oferty konkurencji pod nim).
3. Bez tego ręcznie dodawałbyś zlecenia do bazy.

## Konto 2
Konto 2 to NIE Maksymilian. To konto testowe/zleceniodawcy (weronikabuchholc13).
Config.py ma błędny podpis "Maksymilian" — do poprawy.

## Po wdrożeniu usuwamy
sync_zlecenie.py, sync_konto.py, zbieracz_danych.py, aktualizuj_wszystko.py,
przelicz_*, audyt_*_ai, sekcja_porazek_ai, audyt_i_diagnostyka/ (~20 skryptów).

## Zasada dla AI
Użytkownik mówi "odpal feedback". AI uruchamia, czyta log. Jeśli brak cookies — od razu prosi o plik.