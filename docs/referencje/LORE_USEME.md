# LORE USEME — mechanika platformy
**STATUS: AKTUALNE** (wiedza trwala; bez dat "stan na")

Useme to polska platforma freelancerska: zleceniodawcy publikuja zlecenia, wykonawcy wysylaja oferty, platforma pobiera prowizje od zrealizowanych zlecen.

## Przegladanie i struktura URL
- Sciezka: Jobs -> "Znajdz zlecenie" -> kategoria -> lista (najnowsze na gorze).
- URL kategorii: https://useme.com/pl/jobs/category/NAZWA_KATEGORII,ID_LICZBOWE/
- Uwaga: liczbowe ID kategorii moze sie zmieniac. Nazwa kategorii jest stala. Nie zakladac stalosci ID.
- Monitorowane kategorie: "Programowanie i IT", "Serwisy i strony internetowe".

## Zabezpieczenia
- Cloudflare — JavaScript challenge przy wejsciu.
- Turnstile — CAPTCHA Cloudflare przy logowaniu.
- Wniosek operacyjny: tryb widocznej przegladarki (headless=False) + wazne cookies otwiera formularz bez blokady Turnstile. Tryb headless byl blokowany.

## Logowanie
- Logowanie przez cookies sesji (sessionid + csrftoken), nie przez formularz.
- cookies.json jest NIEZBEDNY do bycia zalogowanym (wysylka, pelne dane).
- Cookies trzymane poza repozytorium (.gitignore).

## Limity i niepewnosci
- Prawdopodobny limit ofert na jednego zleceniodawce/zlecenie — niepotwierdzony, wymaga testu.
- Rotacja kont — mechanizm wielokontowy istnieje (osobne pliki cookies per konto).