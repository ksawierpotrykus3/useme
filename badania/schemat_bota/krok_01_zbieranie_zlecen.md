# KROK 1: Zbieranie Zleceń (Scraping i Monitorowanie Feedów)

Moduł odpowiedzialny za cykliczne pobieranie świeżych ogłoszeń z portalu Useme bez ryzyka blokad i awarii.

---

## 1. Monitorowanie Dostępności Useme (Watchdog)

Przed zainicjowaniem przeglądarki silnik uruchamia procedurę `czekaj_na_dostepnosc_useme()` ([`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py#L34-L56)):
- Wykonuje zapytania HTTP przez bibliotekę `curl_cffi` z impersonacją przeglądarki `chrome120`.
- W przypadku awarii serwerowej (błąd HTTP 503 "Oops!"), bot wstrzymuje wykonanie i ponawia próbę co 60 sekund (do 180 prób = 3 godziny).
- Zapewnia natychmiastowe wznowienie pracy w momencie, gdy portal powraca do działania.

---

## 2. Kategorie Monitorowane

Bot scrapuje dwie główne kategorie zleceń ([`kod/config.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/config.py)):
1. `programowanie-i-it`: https://useme.com/pl/jobs/category/programowanie-i-it,1/
2. `serwisy-internetowe`: https://useme.com/pl/jobs/category/serwisy-internetowe,55/

---

## 3. Przebieg Pobierania (Playwright BrowserDriver)

1. **Weryfikacja Sesji**:
   - `driver.check_logged_in(page)`: sprawdza obecność awatara użytkownika lub przycisku wylogowania.
   - Jeśli sesja wygasła, bot rzuca `AuthenticationRequiredError` i przerywa run dla danego konta.
2. **Pobieranie Listy Ogłoszeń**:
   - Wywołanie `driver.fetch_category_jobs(cat_key, should_stop_fn)`.
   - Paginacja zatrzymuje się w momencie, gdy napotka zlecenie istniejące już w magazynie (`storage.exists(jid)`).
3. **Pobranie Pełnych Detali (Enrichment)**:
   - Dla każdego nowo wykrytego zlecenia wywoływane jest `driver.fetch_job_details(url)`.
   - Zbierane dane: pełna treść ogłoszenia (`full_description`), autor (`author`, `author_id`), liczba dotychczas złożonych ofert (`offers_count`), budżet (`budget`), załączniki.
   - Status zlecenia w magazynie zostaje zaktualizowany na: `POBRANO_DETALE`.
