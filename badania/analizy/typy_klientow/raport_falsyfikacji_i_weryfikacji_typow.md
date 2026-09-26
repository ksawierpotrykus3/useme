# AUDYT FALSYFIKACYJNY I WERYFIKACJA PRAWDZIWOŚCI TAKSONOMII KLIENTÓW
## TEST ZGODNOŚCI Z BAZĄ 470 ZLECEŃ, WYKRYCIE BŁĘDÓW I TWARDA KOREKTA

> **Podstawa dowodowa:** 470 zleceń Useme ($N=470$), w tym 56 wygranych/odpisanych z pełną historią korespondencji na priv oraz 414 zamkniętych zleceń rynkowych.

---

## 1. WERDYKT OGÓLNY: CO JEST TWARDĄ PRAWDĄ, A CO BYŁO BŁĘDEM / NADINTERPRETACJĄ?

Taksonomia klientów po zderzeniu z twardymi danymi przeszła rygorystyczny test falsyfikacyjny. Wykazał on **3 kluczowe filary potwierdzone w 100%**, ale jednocześnie **obalił 3 istotne nadinterpretacje**, które mogłyby doprowadzić do błędnych decyzji automatycznego bota.

### Twarde Liczby z Bazy Danych ($N=470$):
* **Zlecenia z syndromem „Rescue / Sparzony”:** **57 zleceń (12.13% całego rynku)** – klienci wprost piszący o ucieczce dewelopera, dokończeniu rozgrzebanego kodu, poprawkach po partaczu lub audycie podejrzanego kodu.
* **Agencja / Software House / B2B Team:** **65 zleceń (13.83%)** – zlecenia na wsparcie zespołu, podwykonawstwo, stawki godzinowe, poszukiwanie seniorów/midów.
* **Zlecenia z oddelegowanym pracownikiem:** **20 zleceń (4.26%)** – wyraźne sygnały asystentki, księgowej lub pracownika działu piszącego w imieniu szefa/zarządu.
* **Zlecenia czysto Tech-Agnostic (zero IT żargonu):** **155 zleceń (33.0%)** – klienci opisujący wyłącznie proces biznesowy, niepodający ani jednej nazwy technologii.
* **Zlecenia „Szukam wspólnika / Equity za 0 zł”:** **8 zleceń (1.70%)** – skrajne oferty wizjonerów z budżetem 0–100 zł.

---

## 2. TRZY KLUCZOWE KOREKTY FALSYFIKACYJNE (USUNIĘTE BŁĘDY)

### ❌ BŁĄD 1: Traktowanie „Klienta Sparzonego / Rescue” jako osobnego typu branżowego
* **Co było błędem:** Przypisanie Klientowi Sparzonemu statusu „Osobnego Gatunku / Typu G”.
* **Twarda prawda z danych:** Te 57 zleceń (12.1% rynku) pochodzi ze WSZYSTKICH branż:
  * W ERP: Centrum Budowlane Kołcz (audyt wdrożenia Enova365 po poprzednikach),
  * W Mobile: TG Coders (dokończenie rozgrzebanej aplikacji w Kotlinie po programiście),
  * W Web/SaaS: Rafał W. (pilny audyt CTO czy kod Laravel nie jest „składakiem”),
  * W E-commerce: Arkadiusz (naprawa i aktualizacja PrestaShop po błędach).
* **Korekta architektoniczna:** **„Sparzony / Rescue” to nie typ, lecz MODYFIKATOR PSYCHOLOGICZNY (flaga `STAN = RESCUE`)**, który może nałożyć się na MŚP, E-commerce, Startup czy Agencję. Wymaga on natychmiastowego przełączenia narracji na: dekompozycję ryzyk, gwarancję audytu kodu, staging i transparentność, zamiast standardowej oferty wdrożeniowej.

### ❌ BŁĄD 2: Mitomania Startupowa – Iluzja Wysokich Budżetów („Phantom Leads”)
* **Co było błędem:** Przekonanie, że founderzy startupów na Useme to świetny rynek na oferty 15 000 – 34 000 zł, bo na priv wchodziły oferty: 34 000 zł (Adrian Cwiertnia, Mental Health), 15 000 zł (joaxx, Computer Vision), 14 000 zł (KZKujawska, SaaS screening), 10 000 zł (TG Coders, Kotlin).
* **Twarda prawda z danych transakcyjnych:** **ŻADNA z tych umów nie zakończyła się wpłatą depozytu (escrow) na Useme!** 
* Wszystkie te wątki miały zaledwie po 1–2 wiadomości lub urywały się w momencie, gdy Useme wymagało wpłacenia kaucji przez klienta.
* **Jedyna potwierdzona duża wpłata i wypłacony kontrakt w całej historii konta:** **Doktor Monika sp. z o.o. – 12 100,00 PLN netto** (11 083,52 PLN na rękę). Doktor Monika to NIE był marzyciel ze startupem, lecz **działający gabinet medyczny** rozwiązujący bolesną stratę finansową z pustych rezerwacji pacjentów.
* **Korekta architektoniczna:** Startup Founder na Useme ma status **WYSOKIEGO RYZYKA (Phantom Lead Alert)**. Bot nie może inwestować w niego nadmiernych zasobów; wycena musi żądać sztywnych kamieni milowych i wpłaty zaliczki do escrow przed rozpoczęciem jakichkolwiek prac.

### ❌ BŁĄD 3: Iluzja Średnich Długości Wątków (Efekt Jednego Outliera)
* **Co było błędem:** Wniosek, że „Scraping & Boty generują średnio 63–78 wiadomości na priv, a ERP 12–15”.
* **Twarda prawda z danych:**
  * W Scrapingu średnią wywindował **jeden skrajny przypadek: smartcare (aż 373 wiadomości!)** z powodu żmudnej rejestracji aplikacji developerskiej w portalu OLX. Bez smartcare mediana w scrapingu to zaledwie **10–14 wiadomości**.
  * W ERP i B2B (Wiktoria Iwanow TopSolid 8.5k, Arkadiusz Presta 5.5k, Kołcz 5.5k) wątek priv z decyzyjnym klientem trwa zaledwie **1 do 2 wiadomości!** Klient MŚP/ERP nie chce czatować – zadaje jedno pytanie sprawdzające kompetencje i żąda umowy lub faktury.
* **Korekta architektoniczna:** Długi wątek na priv to rzadka anomalia (tylko 3 zlecenia na 56 miały >30 wiadomości). W 85% przypadków wygrana rozstrzyga się w **pierwszych 1–3 wiadomościach**!

---

## 3. OSTATECZNIE ZWERYFIKOWANA TAKSONOMIA (ZGODNA Z EMPIRIĄ)

Po usunięciu nadinterpretacji taksonomia składa się z **6 Rzeczywistych Typów Bazowych** oraz **Modyfikatorów Stanu**:

```
ZWERYFIKOWANA MATRYCA ZLECENIODAWCÓW (USEME):

[TYPY BAZOWE - SEKTOR I ORGANIZACJA]
1. TRADYCYJNE MŚP & ERP (29 zleceń | 17.2% WR | Budżet: 2 800 - 8 500 PLN | Wątek: 1-3 msgs)
   - Klient: Właściciel lub szef operacji. 
   - Cel: Magazyn, WZ, KSeF, ciągłość sprzedaży, brak przestojów.
   - Płatność: Bardzo pewna, faktura VAT, natychmiastowa po potwierdzeniu kompetencji.

2. E-COMMERCE MERCHANT (132 zlecenia | 11.4% WR | Budżet: 1 600 - 7 500 PLN | Wątek: 2-15 msgs)
   - Klient: Właściciel sklepu online (Shoper, Shopify, Presta, IdoSell).
   - Cel: Konwersja, koszyk, integracje kurierskie (DPD), automatyzacja stanów.
   - Płatność: Dojrzałe sklepy płacą stabilnie; dropshipperzy negocjują każdy grosz.

3. AGENCJA / SOFTWARE HOUSE (65 zleceń | 13.8% rynku | Budżet: 1 500 - 10 000 PLN | Wątek: 1-2 msgs)
   - Klient: PM w pożarze terminu lub szef agencji szukający podwykonawcy B2B.
   - Cel: Zrzucenie odpowiedzialności za dowiezienie modułu, uzupełnienie braków kadrowych.
   - Płatność: Bardzo szybka selekcja (1-2 pytania o repo/dostępność), czyste B2B.

4. EKSPERT DZIEDZINOWY / USŁUGI REGULOWANE (41 zleceń | 7.3% WR | Budżet: 2 500 - 12 100 PLN | Wątek: 5-25 msgs)
   - Klient: Lekarz (Doktor Monika), prawnik/komornik, szkoleniowiec, rzeczoznawca.
   - Cel: Eliminacja realnego bólu finansowego w gabinecie/kancelarii, RODO, autorski system.
   - Płatność: Najwyższy potwierdzony ticket gotówkowy (12 100 PLN), ale wymaga prowadzenia za rękę.

5. TECH-AGNOSTIC BIZNES (155 zleceń | 33.0% rynku | Budżet: 1 000 - 6 000 PLN | Wątek: 2-10 msgs)
   - Klient: Przedsiębiorca nietechniczny (usługi, produkcja, handel, nieruchomości).
   - Cel: „Ma działać samo”, połączenie dwóch programów, wyciągnięcie danych z Excela/Airtable.
   - Płatność: Średnia, zerowa tolerancja na żargon IT, kupuje gotowe rozwiązanie pudełkowe.

6. QUICK IT FIX & HOBBYSTA (57 zleceń | Budżet: 100 - 1 500 PLN | Wątek: 1-4 msgs)
   - Klient: Osoba prywatna lub mikro-firma z awarią na wczoraj (błąd 500, prosty skrypt).
   - Cel: Szybka łatka, naprawa błędu.
   - Płatność: Bardzo niska (często <500 zł), wysoka rotacja.

---

[MODYFIKATORY PSYCHOLOGICZNE NAKŁADANE NA DOWOLNY TYP]
⚡ MODYFIKATOR A: „SPARZONY / RESCUE” (57 zleceń w bazie = 12.1%)
   - Symptom: „poprzedni wykonawca”, „dokończenie kodu”, „audyt”, „porzucony projekt”.
   - Reakcja bota: Spokojna inżynierska diagnoza, staging, podział na małe transze (bez darmowej pracy i bez obwiniania klienta).

⚡ MODYFIKATOR B: „ODDELEGOWANY PRACOWNIK” (20 zleceń w bazie = 4.3%)
   - Symptom: „w imieniu szefa”, „właściciel prosił”, „nasza księgowa szuka”.
   - Reakcja bota: Przejrzysta oferta punktowa, którą pracownik może bez wstydu pokazać zarządowi.

⚡ MODYFIKATOR C: „PHANTOM STARTUP / WIZJONER” (8-15 zleceń = ~2-3%)
   - Symptom: „wspólnik techniczny”, „equity”, wysokie obietnice przy braku budżetu.
   - Reakcja bota: Rzetelna wycena pełnego zakresu. Zakaz samowolnego cięcia do „małego MVP” bez dokładnego warunku (warunek: konkurencja pod zleceniem również tak wycenia lub klient wprost wymaga fazowania).
```

---

## 4. WERYFIKACJA CROSS-TECH: CZY RÓŻNICE TECHNOLOGICZNE SĄ PRAWDZIWE?

Audyt potwierdza: **Różnice psychologiczne i decyzyjne między technologiami są w 100% prawdziwe i wynikają z natury ryzyka biznesowego:**

1. **ERP & B2B (Optima, Subiekt, Enova)**:
   * **Ryzyko:** Paraliż fiskalno-magazynowy. Błąd w kodzie = kary z urzędu skarbowego lub zablokowanie wysyłki towaru.
   * **Tolerancja na żargon IT:** Zerowa. Klient wymaga terminologii księgowej (WZ, ZK, FA(3), KSeF, rejestr VAT).
   * **Decyzyjność:** 1–2 wiadomości konkretu. Jeśli widzi, że znasz system – bierze.

2. **Web Scraping & Boty (Cloudflare, Antyboty, API)**:
   * **Ryzyko:** Wykrycie, zablokowanie IP, utrata konta, zmiana layoutu strony.
   * **Tolerancja na żargon IT:** Bardzo wysoka (JA4, emulacja TLS, cURL-impersonate, proxy residential).
   * **Decyzyjność:** Wymaga dowodu skuteczności i dostrajania do żywego portalu.

3. **Tech-Agnostic (33% rynku)**:
   * **Ryzyko:** Przepłacenie za skomplikowany system, którego nikt w firmie nie ogarnie.
   * **Tolerancja na żargon IT:** Alergiczna. Wszelkie wzmianki o frameworkach i bazach danych obniżają szanse na odpowiedź.
   * **Decyzyjność:** Wolniejsza, wymaga zbudowania bezpieczeństwa w języku czystego zysku operacyjnego.

---

## 5. PODSUMOWANIE DLA SYSTEMU BOTA (`kod/`)

1. Bot **nie może** tworzyć 20 sztucznych szablonów pod drobne podgrupy.
2. Bot operuje na **6 Zweryfikowanych Typach Bazowych** + nakłada **Modyfikator RESCUE** (gdy widzi ślady po ucieczce dewelopera) oraz **Modyfikator DELEGATED** (gdy pisze pracownik).
3. Bot nie marnuje czasu na puste dyskusje o equity z marzycielami – wycenia normalnie zakres zlecenia zgodnie z rynkiem. **Nie ma miejsca na samowolne wycenianie „małego MVP”**, chyba że inni wykonawcy pod tym zleceniem tak robią (benchmark) lub klient wprost tego zażądał. W przeciwnym razie wyceniamy całość.