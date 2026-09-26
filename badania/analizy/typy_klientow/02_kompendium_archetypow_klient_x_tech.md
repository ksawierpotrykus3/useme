# KOMPENDIUM STRATEGICZNE: TYPOLOGIA I PROFILOWANIE NA USEME

Oparte na zweryfikowanym empirycznie audycie **470 zleceń** (56 wygranych z pełnymi wątkami na priv vs 414 przegranych) z bazy Ksawiera.

---

## 1. DWA GŁÓWNE ŚWIATY ZLECEŃ (PODWÓJNA ŚCIEŻKA)

Zlecenie na Useme należy w pierwszym kroku zakwalifikować do jednej z dwóch ścieżek:

### Ścieżka 1: Technologiczna (67% rynku, 315 zleceń)
* **Objaw:** Klient wprost wymienia stack (np. *„Laravel 10”*, *„Shopify Liquid”*, *„PrestaShop”*, *„Flutter”*, *„PostgreSQL”*).
* **Oczekiwanie klienta:** Szuka inżyniera, który zna ograniczenia danego frameworka i nie popsuje istniejącego środowiska.
* **Strategia w ofercie:** Natychmiastowe wejście w architekturę, wersję API i specyfikę stacku.
* **Haczyk na priv:** Pytanie o architekturę/repo (np. *„Czy ta integracja to natywny moduł czy zewnętrzny skrypt uderzający przez Webhooks?”*).

### Ścieżka 2: Wynikowa / Problemowa (33% rynku, 155 zleceń, 17 wygranych)
* **Objaw:** W ogłoszeniu **nie ma ani jednego słowa o technologii**. Klient pisze: *„Chcę automatyzację pobierania partnerów z Google Maps”*, *„Arkusz do kosztorysów domów”*, *„MVP platformy do screeningu”*, *„Skrypt do gry”*.
* **Oczekiwanie klienta:** Klient nie wie i nie obchodzi go, czy to będzie w Pythonie, n8n czy arkuszu Google. Chce konkretnego rezultatu biznesowego.
* **Strategia w ofercie:** Zero pouczania i zero żargonu IT. Propozycja najprostszego i najtańszego podejścia narzędziowego.
* **Haczyk na priv:** Pytanie o dane wejściowe i format wyniku (np. *„Czy te firmy z Google Maps mają trafiać do pliku Excel/CSV z numerami telefonów, czy bezpośrednio do Twojego CRM-a?”*).

---

## 2. TYPOLOGIA ZLECENIODAWCÓW (5 PROFILI)

### Profil A: Biznesmen Nietechniczny (50.4% rynku, 237 zleceń, WR: 12.2%)
* **Język:** Ból biznesowy, czas pracowników, błędy na magazynie, dławienie się zamówieniami.
* **Czego się boi:** Oszukania, ukrytych kosztów, zepsucia działającej firmy.
* **Czego NIE robić:** Nie zarzucać go żargonem architektonicznym ani coachingowymi formułkami.
* **Cel na priv:** Wytłumaczenie procesu po ludzku, potwierdzenie formatu danych wejściowych/wyjściowych i bezpieczne wdrożenie.

### Profil B: Tech Lead / CTO / PM Agencji (9.6% rynku, 45 zleceń, WR: 13.3%)
* **Język:** Ścisłe wymagania techniczne: Docker, Swagger, Clean Architecture, CI/CD, NFR.
* **Czego się boi:** Juniora udającego seniora, długu technologicznego, braku testów.
* **Czego NIE robić:** Żadnego marketingu, lania wody i obietnic „zrobimy wszystko”.
* **Cel na priv:** Partnerska rozmowa inżynier-inżynier, wgląd w repozytorium GitHub/GitLab, ustalenie kryteriów code review.

### Profil C: E-commerce Manager (20.0% rynku, 94 zlecenia, WR: 10.4%)
* **Język:** Koszyk, konwersja, szybkość sklepu, BaseLinker, marketplace'y, hurtownie.
* **Czego się boi:** Spadku sprzedaży, problemów z płatnościami (Klarna/Stripe), spowolnienia strony.
* **Czego NIE robić:** Nie proponować armaty na muchę (drogich dedykowanych systemów tam, gdzie wystarczy lekki skrypt w Liquid).
* **Cel na priv:** Prośba o link do sklepu/stagingu, wskazanie natychmiastowej optymalizacji, bezpieczne wdrożenie bez przestojów.

### Profil D: Startupowiec / Pomysłodawca MVP (10.9% rynku, 51 zleceń, WR: 11.8%)
* **Język:** Wizja „nowej platformy”, szuka „partnera technologicznego”, emocje i duże plany.
* **Czego się boi:** Przepalenia całego budżetu na discovery w drogim software housie.
* **Czego NIE robić:** Nie wchodzić w jałowe dyskusje o equity/partnerstwie ani nie stosować samowolnego obcinania zakresu do „taniego MVP”.
* **Cel na priv:** Rzetelna wycena pełnego zakresu zlecenia w stawkach rynkowych. Wycena małego MVP / etapowa jest dopuszczalna WYŁĄCZNIE wtedy, gdy: (a) inni wykonawcy pod zleceniem również tak wyceniają (benchmark rynkowy), LUB (b) klient wprost zażądał fazowania/MVP w treści ogłoszenia.

### Profil E: Zadaniowiec Quick-Fix (9.1% rynku, 43 zlecenia, WR: 11.6%)
* **Język:** Krótki (1-2 zdania), „na wczoraj”, błąd 500, padnięty skrypt, szybki bot.
* **Czego się boi:** Przeciągania w czasie, licytacji stawek, niekończących się pytań i calli.
* **Czego NIE robić:** Nie pisać elaboratów ani nie zapraszać na „15-minutowe calle”.
* **Cel na priv:** Natychmiastowa prośba o log/screenshot, 15 minut na weryfikację i szybkie escrow.

---

## 3. RZECZYWISTOŚĆ STATYSTYCZNA TECHNOLOGII

* **WordPress / WooCommerce ($n = 104$, WR: 6.7%):** Czerwony ocean. Wysoka konkurencja i niska marża. Wygrywa tylko precyzyjne odcięcie się od instalatorów wtyczek i wskazanie konkretnego kodu PHP/JS/CSS.
* **Zlecenia Niszowe ($n < 15$, np. TopSolid, VoIP, IdoSell, Enova, Sfera):** Z powodu małej próby nie wolno ich traktować jako pewników. To segmenty o wysokiej wartości jednostkowej, gdzie liczy się bezwzględne potwierdzenie kompetencji (np. posiadanie licencji/środowiska testowego).

---

## 4. PROTOKÓŁ 3 KROKÓW NA PRIV (ZAMYKANIE ZLECENIA)

Gdy klient odpowie na Question CTA z oferty publicznej:

1. **Krok 1: Żądanie Artefaktu (Plik / Link / Dostęp)**
   * Poproś o konkret: plik XML/CSV/JSON, link do sklepu/Figmy, log błędu lub zaproszenie do repozytorium.
   * *Przesłanie materiałów przez klienta to punkt zwrotny – psychologicznie wybrał Ciebie do realizacji.*

2. **Krok 2: Odcięcie Ryzyka i Twarda Specyfikacja**
   * Klient boi się utraty kontroli nad budżetem i zniknięcia wykonawcy.
   * Przedstawienie transparentnej wyceny pełnego zakresu (lub etapowej, jeśli spełniony jest warunek: bezpośrednie żądanie klienta lub benchmark konkurencji).
   * Podanie twardego terminu i specyfikacji dostarczanych artefaktów.

3. **Krok 3: Domykanie Escrow Useme**
   * *„Wystawiam dedykowaną umowę na Useme na uzgodniony zakres. Środki wpłacasz na bezpieczny rachunek powierniczy escrow – są zablokowane do Twojego odbioru. Po odbiorze Useme wystawia fakturę VAT, a ja przekazuję kod.”*
