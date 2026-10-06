## Diagnoza min i ryzyk

### 1. Anolla — brak natywnej integracji z Squarespace

**Fakt:** Anolla udostępnia embedowalne widgety i generator przycisków „Book Now” z kodem HTML do wklejenia. W planie Free Anolla zawiera „Add booking widget to your website”, a wśród funkcji wymieniane są „Embeddable web widgets for portals and third-party sites”.

**Dlaczego groźne:** Klient pisze „preferowana Anolla” i traktuje to jako integrację. W rzeczywistości rezerwacja dzieje się **po stronie Anolla** (widget/iframe), a nie wewnątrz Squarespace. Nie ma natywnego połączenia typu synchronizacja kalendarza czy automatyczne mapowanie formularzy. Jeśli klient oczekuje, że rezerwacja będzie „wbudowana” w SQS na poziomie systemowym — to nie zadziała. Wchodzi jako embed przez Code Block lub Code Injection, co wymaga planu Business (jest) i nie daje pełnej kontroli nad wyglądem ani danymi po stronie SQS.

### 2. Weglot — dodatkowy abonament poza budżetem projektu

**Fakt:** Squarespace nie ma natywnej wielojęzyczności w 2026 r. — dostępne są tylko Weglot, metoda ręczna (duplikaty stron) lub widget Google Translate. Weglot kosztuje od ~15 €/mies. za 1 język i 10 000 słów, 29 €/mies. za 3 języki. Tłumaczenie URL-i i pełne SEO wymaga planu Pro za 79 €/mies.. W niższych planach tłumaczenie odbywa się przy ładowaniu strony i nie jest indeksowane przez Google w sposób umożliwiający pełne SEO.

**Dlaczego groźne:** Klient pisze „Weglot lub natywne SQS” — sugeruje, że traktuje oba jako równoważne. Nie są. „Natywne SQS” nie istnieje. Weglot to **stały miesięczny koszt abonamentowy**, który nie jest częścią budżetu projektu (3000–4500 PLN jednorazowo). Przy 3 językach (PL/EN/IT) i stronie z tekstami PL/EN/IT gotowymi do wdrożenia, sam Weglot pochłonie 29 €/mies. w planie Business, a przy potrzebie indeksowania URL-i — 79 €/mies. To zmienia ekonomię projektu: klient płaci za Squarespace Business + Weglot Pro, a budżet freelancera nie pokrywa tego kosztu.

### 3. Squarespace Scheduling jako alternatywa — ograniczenia funkcjonalne

**Fakt:** Squarespace Scheduling (oparty na Acuity) oferuje integrację z Google Analytics, Stripe, Zapier, Zoom, a także obsługę subskrypcji, kart podarunkowych i pakietów. Nie ma jednak natywnego połączenia z Anolla — to dwa odrębne systemy.

**Dlaczego groźne:** Jeśli klient wybierze Squarespace Scheduling zamiast Anolla, traci ekosystem Anolla (AI, IoT, marketplace). Jeśli zostanie przy Anolla — traci natywną integrację SQS. Nie ma rozwiązania „wszystko w jednym”. Wybór jednego systemu rezerwacji wyklucza drugi. Dla B2B team buildingów, gdzie klient chce logotypy, case studies i formularz, system rezerwacji może być mniej krytyczny — ale dla B2C warsztatów i „Gnam Gnam” prywatnego szefa kuchni rezerwacja online jest kluczowa.

### 4. Plan Business — potwierdzenie dostępu do Code Injection i Custom CSS

**Fakt:** Code Injection jest dostępny wyłącznie w planach Business i Commerce; Personal go nie ma. Custom CSS jest dostępny w każdym planie przez Design > Custom CSS. Page Header Code Injection wymaga planu Core (dawniej Business) lub wyższego.

**Dlaczego groźne:** To akurat **nie jest mina** — plan Business, który klient ma opłacony, w pełni pokrywa potrzeby Code Injection (dla embedów Anolla, GA4, Meta Pixel) oraz Custom CSS. Brak blokady technicznej. Ryzyko leży wyłącznie po stronie Anolla i Weglot, nie po stronie planu Squarespace.

---

**Podsumowanie:** Dwie realne miny — Anolla jako embed (nie integracja) i Weglot jako stały koszt miesięczny poza budżetem projektu. Reszta (plan Business, Custom CSS, Code Injection) nie stanowi bariery.