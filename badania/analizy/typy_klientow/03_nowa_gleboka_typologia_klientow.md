# POGŁĘBIONA TYPOLOGIA ZLECENIODAWCÓW NA USEME (AUDYT 470 ZLECEŃ)

> **Podstawa empiryczna:** 470 zleceń (56 wygranych z pełną historią wiadomości vs 414 przegranych) z bazy `ksawierpotrykus3`.

---

## 1. CO NOWEGO WYKAZAŁ POGŁĘBIONY ŁAŃCUCH?

Wcześniejszy podział sztucznie upchnął ponad 50% rynku w jeden abstrakcyjny worek *„Biznesmen Nietechniczny”*. 
Głęboka analiza semantyczna i behawioralna całej bazy wykazała, że zleceniodawcy dzielą się na **8 wyraźnych person biznesowych**, różniących się budżetem, czasem decyzyjnym i zachowaniem na priv:

| Persona | Liczba Zleceń | Wygrane | Win Rate | Śr. / Maks Wiadomości Priv | Profil Budżetowy |
|---|---:|---:|---:|---:|---|
| **1. E-commerce Merchant (Sklepy online)** | 132 | 15 | 11.4% | 16.2 (maks 173) | 1 600 – 7 500 PLN |
| **2. Niszowe R&D / Integracje i Boty** | 121 | 13 | 10.7% | 34.0 (maks 373) | 300 – 14 500 PLN |
| **3. Startup Founder / Nowe MVP** | 53 | 9 | **17.0%** | **9.6** (maks 35) | **6 000 – 34 000 PLN** |
| **4. Quick IT Fix (Małe zlecenia / błędy)** | 50 | 5 | 10.0% | 7.2 (maks 20) | 400 – 7 500 PLN |
| **5. Ekspert Dziedzinowy (Usługi / Edukacja)** | 41 | 3 | 7.3% | **24.7** (maks 70) | 2 500 – 6 500 PLN |
| **6. Agencja / Software House (B2B)** | 37 | 4 | 10.8% | 9.5 (maks 21) | 1 500 – 16 000 PLN |
| **7. Tradycyjne MŚP / Przemysł / ERP** | 29 | 5 | **17.2%** | 12.8 (maks 53) | **2 800 – 8 500 PLN** |
| **8. Gamer / Hobbysta / Zlecenie Prywatne** | 7 | 2 | 28.6% | 15.5 (maks 23) | ~400 PLN |

---

## 2. SZCZEGÓŁOWA CHARAKTERYSTYKA PERSON

### 🚀 Persona A: Startup Founder / Nowe MVP (Pozorne Zwycięstwa vs Realna Kasa)
* **Wolumen:** 53 zlecenia | **Odpisane oferty:** 9 zleceń (17.0% wskaźnik odpowiedzi na priv).
* **UWAGA KRYTYCZNA (Phantom Leads):** Chociaż na priv wchodziły oferty o wysokich stawkach (34 000 zł Mental Health, 15 000 zł Computer Vision, 14 000 zł SaaS screening, 10 000 zł Kotlin), **żadna z nich nie została opłacona i sfinalizowana na Useme**. Founderzy często badają rynek, szukają darmowego CTO lub nie mają zabezpieczonego finansowania na escrow.

---

### 🩺 Persona B: Działający Biznes Usługowy / Klinika (Złoty Case Study: Doktor Monika)
* **ZŁOTA WYGRANA I POTWIERDZONA WYPŁATA:** Umowa z **Doktor Monika sp. z o.o.** (Utworzono: 30.04.2026, Wypłacono: 22.06.2026).
  * **Kwota na fakturze:** **12 100,00 PLN netto** (14 883,00 PLN brutto).
  * **Wypłacono wykonawcy na rękę:** **11 083,52 PLN**.
* **Dlaczego ten klient realnie zapłacił 12,1k, a founderzy 34k odpadli?**
  1. **Realny ból finansowy działającej firmy:** Gabinet medyczny (4 lekarzy, docelowo 10, tysiące pacjentek) tracił realne tysiące złotych przez „puste, nieopłacone rezerwacje” blokujące lekarzy w Calendly.
  2. **Profesjonalna specyfikacja:** Klient nie pisał mglistych wizji, lecz załączył konkretny PDF (`REZERWACJE_DOKTOR_MONIKA.pdf`) z rozrysowanymi ekranami.
  3. **Anty-spamowy filtr:** Klient wprost napisał: *„Czego nie chcę: szablonowych ofert, pytań bez analizy PDF, wycen renegocjowanych później, odpowiedzi z ChatGPT”*.
  4. **Zwycięska inżynieria Ksawiera:** Odpowiedź punkt po punkcie na każdy ekran PDF, wdrożenie *Pessimistic Locking* (ochrona przed double-bookingiem), *Rate Limiting na SMSAPI* oraz *Odwrócona Logika Rezerwacji* (lock w bazie -> webhook Tpay -> dopiero uderzenie w API Calendly).
  5. **Twarde warunki:** 12 100 zł fix-price, 4 tygodnie, staging, 1 miesiąc asysty powdrożeniowej.

---

### 🏭 Persona B: Tradycyjne MŚP / Przemysł / Operacje ERP (17.2% WR)
* **Wolumen:** 29 zleceń | **Twoje Wygrane:** 5 zleceń.
* **Poziom biletów:** 2 800 – 8 500 zł (TopSolid CNC, UI bot Wapro Kaper, Enova, Make-InFakt).
* **Zachowanie na priv:** Średnio 12.8 wiadomości.
* **Profil:** Właściciel fabryki, hurtowni, firmy produkcyjnej. Zmaga się z realnym tarciem operacyjnym: synchronizacja maszyn CNC, fakturowanie, blokady bazy danych, eksporty do ERP.
* **Klucz do wygranej:** Przewaga inżynierska. 95% freelancerów na Useme robi strony WWW i nie ma pojęcia o API TopSolid czy Sferze nexo. Wejście z konkretnym rozwiązaniem translacji danych natychmiast eliminuje konkurencję.

---

### 🛒 Persona C: E-commerce Merchant (11.4% WR)
* **Wolumen:** 132 zlecenia (największy pojedynczy rynek komercyjny) | **Twoje Wygrane:** 15 zleceń.
* **Poziom biletów:** 1 600 – 7 500 zł (Shopify, PrestaShop, IdoSell, BaseLinker).
* **Zachowanie na priv:** Średnio 16.2 wiadomości (rekord: **173 wiadomości**!).
* **Profil:** Właściciel sklepu online. Żyje konwersją, koszykiem, szybkością strony i integracjami z hurtowniami.
* **Klucz do wygranej:** Zapewnienie, że wdrożenie odbędzie się na środowisku stagingowym bez ryzyka dla sprzedaży live. Wymaga cierpliwości w testach koszyka.

---

### ⚙️ Persona D: Niszowe R&D / Integracje i Boty (10.7% WR)
* **Wolumen:** 121 zleceń | **Twoje Wygrane:** 13 zleceń.
* **Poziom biletów:** 300 – 14 500 zł (Wtyczki Chrome 14.5k, System medyczny 12.1k, Booking PMS 4.2k, VoIP/SIP 3.5k, OLX bot).
* **Zachowanie na priv:** Średnio **34.0 wiadomości** (rekord: **373 wiadomości**!).
* **Profil:** Klienci szukający nietypowych rozwiązań (reverse engineering API, ekstrakcja danych, telefonia VoIP, streaming IPTV, scrapery z obejściem Cloudflare).
* **Klucz do wygranej:** Wykazanie, że rozumiesz mechanizmy niskopoziomowe (Headless browsers, protokoły SIP/RTP, sesje i captche). Długie wątki wynikają z konieczności precyzyjnego dostrajania scrapera do zmian w serwisach zewnętrznych.

---

### 🩺 Persona E: Ekspert Dziedzinowy / Edukacja / Usługi (7.3% WR)
* **Wolumen:** 41 zleceń | **Twoje Wygrane:** 3 zlecenia.
* **Poziom biletów:** 2 500 – 6 500 zł (System dla psychologów, Quiz diagnostyczny dla liderów, Testy ABCDE).
* **Zachowanie na priv:** Średnio **24.7 wiadomości** (maks: 70 wiadomości).
* **Profil:** Psycholog, edukator, trener biznesu, rzeczoznawca. Całkowicie nietechniczny, pełen obaw, potrzebuje intensywnego prowadzenia za rękę.
* **Klucz do wygranej:** Najniższy współczynnik wygranych (7.3%) przy największym nakładzie czasu na priv. Wymaga prostego języka, cierpliwości i proponowania gotowych narzędzi (np. Typeform/Airtable/Make) zamiast programowania od zera.

---

### 🏢 Persona F: Agencja / Software House (10.8% WR)
* **Wolumen:** 37 zleceń | **Twoje Wygrane:** 4 zlecenia.
* **Poziom biletów:** 1 500 – 16 000 zł (Subiekt Sfera 16k, Arkusze 1.5k, Wdrożenie CRM 2.2k).
* **Zachowanie na priv:** Średnio **9.5 wiadomości**.
* **Profil:** PM lub CTO szukający podwykonawcy na zlecenie B2B lub do wsparcia zespołu.
* **Klucz do wygranej:** Zero marketingu. Pytanie o repo, stack, środowiska i kryteria akceptacji.

---

## 3. IMPLIKACJE DLA GENERATORÓW PROMPTÓW

1. **Eliminacja sztywnego podziału na 5 etykiet:** Silnik kwalifikacji musi rozpoznawać 8 powyższych person.
2. **Kwalifikacja pod kątem tarcia na priv:**
   * Do **Foundera MVP** i **Tradycyjnego MŚP** piszemy twardo, architektonicznie, dążąc do szybkiego zamknięcia (wysokie ROI).
   * Do **Eksperta Dziedzinowego** piszemy z dużą empatią procesową, bo wymaga on wieloetapowego budowania zaufania.
3. **Flaga `HIGH_TICKET_ALERT`:** Jeśli zlecenie dotyczy budowy nowego MVP lub automatyzacji procesów w firmie produkcyjnej, wyceny w rubryce ofertowej powinny celować w przedział **8 000 – 35 000 zł**, bo dane empiryczne dowodzą, że w tych segmentach wygrywasz z najwyższymi stawkami.
