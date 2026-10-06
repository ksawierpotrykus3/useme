## Research: soft4fx.com – ustalenia

### 1. Technologia i struktura

**PHP – potwierdzone.** Adresy podstron kończą się na `.php` (index.php, contact.php, pricing.php, download.php, affiliate-program.php, tutorials-mt4.php, tutorials-mt5.php, privacy-policy.php, reset-activations.php). Brak śladów frameworka (Laravel, Symfony) ani CMS (WordPress) – wygląda na **własny kod PHP**. W nagłówku HTML ładowane są trzy pliki CSS (`variables.css`, `fix.css`, `custom.css`), co sugeruje autorski system stylów, a nie gotowy szablon.

**Strona ma już responsywność w meta viewport** (`<meta name="viewport" content="width=device-width, initial-scale=1.0">`), ale to nie znaczy, że layout faktycznie jest mobilny – sam tag to tylko deklaracja.

### 2. Formularz kontaktowy – już istnieje

Na `contact.php` jest sekcja **„Ask a Question”** z akceptacją polityki prywatności („By sending this message, you accept our privacy policy”). Nie ma informacji o zabezpieczeniach antyspamowych ani o tym, czy formularz działa (nie udało się zweryfikować backendu). Klient pisze „Wymagane funkcje: formularz kontaktowy”, co może oznaczać, że **obecny formularz nie działa lub klient o nim nie wie** – to potencjalna mina: zlecenie może być częściowo już zrealizowane.

### 3. PayPro – potwierdzone, ale nie na stronie transakcyjnej

PayPro Global jest wymieniony w **polityce prywatności** jako procesor płatności i operator programu afiliacyjnego. Klient nie podaje numerów kart – dane płatnicze zbiera wyłącznie PayPro Global na swojej stronie. To oznacza, że **integracja z PayPro jest zewnętrzna** i nie wymaga modyfikacji przy redesignie – wystarczy nie zepsuć linków/ścieżki przekierowania.

### 4. Dostępne materiały

- **Logo:** `img/brand/logoBlack.svg` – istnieje, w formacie wektorowym (SVG).
- **Screenshoty:** strona zawiera liczne zrzuty ekranu z symulatora (sekcje „How Forex Simulator Works”, „Great features” itd.) – są wbudowane w treść, więc klient ma źródła.
- **Treści:** wszystkie sekcje są na stronie (opis produktu, FAQ, tutoriale) – do zachowania.

### 5. Miny i ciekawości (potwierdzone)

- **Własny PHP bez frameworka** – redesign może oznaczać pracę na „gołym” PHP, co utrudnia separację logiki od widoku. Jeśli struktura kodu jest splątana, zakres może wzrosnąć z „warstwy prezentacji” na „przebudowę widoków”.
- **Formularz już istnieje** – ryzyko, że klient oczekuje naprawy, a nie budowy od zera; warto dopytać, co konkretnie nie działa.
- **PayPro Global jest zewnętrzny** – nie ma potrzeby integracji po stronie soft4fx.com; wystarczy zachować linki do koszyka/płatności. Brak wzmianki o PayPro na stronie głównej czy cenniku (prawdopodobnie przekierowanie następuje dopiero przy zakupie).
- **Brak cookies** – strona deklaruje, że nie używa cookies, co upraszcza kwestie RODO przy formularzu.

### 6. Czego nadal nie wiadomo (do dopytania)

- Czy obecny formularz kontaktowy **działa** (backend, wysyłka e-mail).
- Ile **podstron** obejmuje responsywność (widoczne min. 9–10 plików .php).
- Czy klient ma **dostęp do kodu** i repozytorium.
- Czy PayPro ma być **modyfikowane** (np. nowy product box z linkiem do koszyka).