**Uwaga wstępna:** bez podania adresu URL strony, hostingu i listy wtyczek nie można zweryfikować realnej prędkości, konfiguracji cache ani tego, co dokładnie blokuje wydajność. Poniżej ogólne ustalenia z researchu, które diagnozują *gdzie* i *dlaczego* mogą pojawić się problemy — nie recepty.

---

## 1. RODO / consent (formularz, oddzwanianie, czat)

**Gdzie groźne:** każdy nowy kanał kontaktu zbiera dane osobowe (imię, telefon, e-mail, IP, metadane połączeń). Bez zgód i klauzul informacyjnych wdrożenie tych funkcji może naruszać RODO oraz ePrivacy.

**Dowody:**
- Formularz kontaktowy: przetwarzanie danych wymaga podstawy z art. 6 ust. 1 lit. a RODO (zgoda) w związku z pytaniem/zgłoszeniem; zgodę można wycofać w każdym momencie. Zgoda marketingowa musi być opcjonalna i niezaznaczona domyślnie.
- Callback widget (np. Zadarma): ustawia cookies (`zd_session`, `zd_visitor` itd.), zbiera numer telefonu, IP, User Agent, metadane połączeń, opcjonalnie nagranie audio. Cookies widgetu wymagają uprzedniej zgody na podstawie art. 5(3) ePrivacy; nagrywanie rozmów regulowane odrębnie (w większości jurysdykcji UE wymagana zgoda wszystkich stron). Widget podlega też art. 13 ePrivacy, gdy callback służy do sprzedaży, której użytkownik nie zażądał.
- Czat: integracja live chat wymaga poinformowania użytkownika o przetwarzaniu danych i wyboru narzędzi spełniających normy prawne.

**Niepotwierdzone:** czy obecna strona ma już politykę prywatności, zgody i umowy z dostawcami (DPA) — to wymaga weryfikacji po URL i nazwach narzędzi.

---

## 2. Wydajność: Elementor + hosting + wtyczki

**Gdzie groźne:** wolne działanie strony to zwykle kombinacja: wolny hosting (współdzielony serwer bazy danych), brak cache obiektowego, zbyt wiele wtyczek/rozszerzeń Elementora i nieoptymalne obrazy. Sam Elementor nie jest jedynym winowajcą.

**Dowody:**
- Elementor dodaje CSS i JavaScript; na nieoptymalizowanej stronie narzut jest zauważalny. Na stronie z dobrym hostingiem, cache i sensowną obsługą obrazów różnica jest niewielka. WordPress sam przetwarza każdy request (PHP), a „bloated theme” i stos niepotrzebnych wtyczek spowalniają niezależnie od buildera.
- Hosting współdzielony (np. Bluehost) bywa „underprovisioned” dla bazy danych; buffer pool może być w 97% pełny. Połączenie „elementor + Bluehost” nie jest dobre dla wysokiej wydajności.
- Cache dla Elementora: wtyczki takie jak EmiCache deklarują bycie zbudowanym pod Elementor i WooCommerce — obsługują full-page cache, minifikację, lazy load, WebP, critical CSS, CDN i Core Web Vitals. Elementor sam oferuje wewnętrzne opcje cache (element cache, generowanie CSS/JS w Advanced), które mogą istotnie obniżyć TTFB.

**Niepotwierdzone:** jaki jest obecny hosting, wtyczki cache, TTFB, LCP i rozmiar bazy — do sprawdzenia po URL i dostępie do panelu.

---

## 3. „Gotowy kod do funkcji oddzwaniania” — snippet, wtyczka czy SaaS?

**Gdzie groźne:** nie wiadomo, czy klient ma na myśli snippet do wklejenia, wtyczkę WordPress czy zewnętrzny widget SaaS. Od tego zależą koszty, licencje, limity API i zgodność z RODO.

**Dowody:**
- Widgety callback (np. Zadarma, Genesys, Medallia) to zewnętrzne usługi z API, tokenami dostępu i politykami kontroli dostępu; mogą wymagać kluczy API i generować koszty oraz metadane poza UE.
- Zadarma jako przykład: infrastruktura kontrolna w UE, ale media połączeń mogą przechodzić przez punkty w Azji/USA — łańcuch operatorów przetwarza numer dzwoniącego, numer docelowy i czas trwania jako metadane telekomunikacyjne; trzeba to udokumentować w polityce prywatności.
- Są też wtyczki WordPress do callbacków z wbudowaną zgodą RODO (checkbox z linkiem do polityki prywatności, walidacja po stronie klienta i serwera).

**Niepotwierdzone:** co dokładnie klient posiada (snippet/wtyczka/SaaS), jaki to dostawca, jaki model rozliczeniowy i czy przetwarza dane poza EOG.

---

## 4. „Wersja mobilna” — responsywność vs osobna strona

**Gdzie groźne:** w WordPress + Elementor standardem jest responsywność (jedna strona, różne breakpointy). Osobna wersja mobilna (subdomena, `m.`) to zwykle gorsza droga — więcej pracy, problemy z SEO i utrzymaniem.

**Dowody:**
- Elementor ma wbudowany tryb responsywny: przełączanie między desktop/tablet/mobile w edytorze, niezależne style, widoczność sekcji i kontrolki responsywne.
- Standardową metodą tworzenia stron mobilnych jest dziś jedna wersja responsywna, a nie osobna strona mobilna. Osobna wersja wymaga pluginów typu WPtouch i dodatkowej infrastruktury.
- Przy mobile-first indexingu Google, jeśli strona ma osobną wersję mobilną, trzeba pilnować spójności treści i linków.

**Wniosek:** jeśli klient mówi „wymagane funkcje wersja mobilna”, prawdopodobnie chodzi o responsywność, którą Elementor obsługuje natywnie. Osobna wersja mobilna to potencjalna mina kosztowa i SEO.

---

## Podsumowanie diagnozy (GDZIE i DLACZEGO groźne)

| Obszar | Gdzie groźne | Dlaczego |
|---|---|---|
| RODO | formularz, callback, czat | zbierają dane osobowe i metadane; wymagają zgód, klauzul, DPA, czasem CMP |
| Wydajność | hosting + wtyczki + Elementor | współdzielony hosting i brak cache obniżają TTFB; Elementor dodaje CSS/JS, ale nie jest jedynym winowajcą |
| „Gotowy kod” | nieznany dostawca callbacku | może być snippet, wtyczka lub SaaS z API, licencją i limitami; dane mogą wychodzić poza EOG |
| Wersja mobilna | rozumienie „osobnej wersji” | WordPress/Elementor domyślnie daje responsywność; osobna wersja to zwykle gorsza droga |

**Czego nie potwierdzam:** konkretnych liczb dotyczących prędkości, konwersji, ruchu, hostingu, wtyczek i budżetu — brak URL i danych po stronie klienta.