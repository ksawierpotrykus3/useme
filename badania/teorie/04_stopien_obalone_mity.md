# STOPIEŃ 4: Obalone Mity i Fałszywe Założenia (Pewność 0% / Falsyfikacja)

> Kryterium kwalifikacji: Tezy, które zostały obalone przez twarde fakty transakcyjne, bezpośrednią weryfikację zleceń przez Ksawiera lub negatywne wyniki testów empirycznych.

---

## MIT 1: "Wysokie Wyceny Startupowe (34k, 15k) to Wygrane Kontrakty"

- **Mit**:
  Wcześniejsze raporty traktowały oferty na 34 000 PLN (Startup Zdrowie Psychiczne), 15 000 PLN (Generator CV) i 14 000 PLN (SaaS B2B) jako "sukcesy ofertowarki i wygrane w portfolio".
- **Falsyfikacja empiryczna**:
  Ksawier jednoznacznie zweryfikował, że **żadna z tych ofert nie doszła do skutku**. Klienci ci odpisali, zadali kilka pytań, po czym zniknęli bez wpłaty choćby złotówki na Useme.
- **Konsekwencja operacyjna**:
  Całkowity zakaz targetowania bota na "wielkie wizje startupowe bez budżetu". Jedynym realnym wysokim kontraktem z wpłatą był **Doktor Monika (12 100 PLN)** – działająca klinika medyczna.

---

## MIT 2: "Najlepszy Call To Action to Propozycja Rozmowy / Zdzwonienia Się (Call 15 Minut)"

- **Mit**:
  Kończenie oferty formułą: *"Zaproponuj termin na 15-minutowy call na Google Meet, żeby omówić szczegóły"*.
- **Falsyfikacja empiryczna**:
  Zleceniodawcy Useme szukają freelancerów właśnie po to, by załatwić sprawę **asynchronicznie i bez konieczności umawiania rozmów wideo**. Prośba o calla w pierwszej wiadomości:
  1. Wymaga od klienta otwarcia kalendarza i wyboru terminu (wysoki wysiłek poznawczy).
  2. Budzi obawę przed nachalną prezentacją handlową.
  3. Obniża wskaźnik otwarcia dyskusji o ponad 20% względem Question CTA.
- **Konsekwencja operacyjna**:
  Zakaz proponowania calli w pierwszej ofercie. Zawsze zadajemy precyzyjne pytanie inżynierskie lub biznesowe z dwiema opcjami A/B.

---

## MIT 3: "Każdy Zleceniodawca Chce Usłyszeć Propozycję Nowoczesnego Stacku (React, Docker, Microservices)"

- **Mit**:
  Każda oferta powinna popisywać się zaawansowanym stackiem technologicznym, architekturą chmurową i konteneryzacją.
- **Falsyfikacja empiryczna**:
  Aż **33% rynku (155 zleceń)** to klienci biznesowi (tech-agnostic), którzy nie mają pojęcia, czym jest Docker czy Next.js. Wrzucenie żargonu IT w ofercie dla tego segmentu skutkuje natychmiastowym poczuciem zagubienia u klienta i odrzuceniem oferty jako "zbyt skomplikowanej i za drogiej".
- **Konsekwencja operacyjna**:
  Klasyfikator Dual-Track w silniku: jeśli zlecenie nie ma tagów technicznych, bot ma bezwzględny zakaz używania skrótów i nazw bibliotek.

---

## MIT 4: "Masowa Wysyłka Generycznych Ofert (Spray & Pray) z Myślnikami Zapewni Dochód"

- **Mit**:
  Wystarczy generować 50-100 ofert dziennie z listą wypunktowanych cech (*"Dlaczego warto mnie wybrać: 1. Doświadczenie, 2. Terminowość..."*).
- **Falsyfikacja empiryczna**:
  Tego typu oferty wpadają wprost do Czerwonego Oceanu WordPressa (Win Rate 6.7%) i są natychmiast rozpoznawane jako spam przez algorytm i ludzi.
- **Konsekwencja operacyjna**:
  Maksymalny limit 190 słów, czysty tekst bez bulletpointów, zakaz markdowna, obowiązkowy research sieciowy klienta (Agent 01).

---

## MIT 5: "O Wygranej na Useme Decyduje Wyłącznie Najniższa Cena"

- **Mit**:
  Aby wygrywać na Useme, trzeba licytować po 100-300 PLN i zaniżać stawkę godzinową.
- **Falsyfikacja empiryczna**:
  Case Doktor Monika (12 100 PLN netto) wygrał z konkurentami oferującymi wykonanie "za 2 000 PLN w WordPressie". Klient wybrał Ksawiera, ponieważ Ksawier wskazał błąd wyścigu (race condition) przy rezerwacjach i zaproponował blokowanie pesymistyczne slotów SQL oraz rate-limit SMS. Klient biznesowy płaci za **bezpieczeństwo i brak przestoju**, a nie za najtańszy kod.

---

## MIT 6: "Dzielenie Projektu na Fazę 1 / Mały Etap Zapewnia Konwersję"

- **Mit**:
  Rozbijanie dużych zleceń na "Płatne PoC / Etap 1 za 800 zł" rzekomo usuwa opór psychologiczny i automatycznie domyka klienta.
- **Falsyfikacja empiryczna (Praktyka Ksawiera)**:
  W realnych testach Ksawiera taka propozycja miała **0% konwersji**. Klienci z Useme albo chcą mieć sprawę rozwiązaną całościowo i widzieć pewnego siebie inżyniera, albo traktują propozycję etapu wstępnego jako brak wiary wykonawcy we własne możliwości.
- **Konsekwencja operacyjna**:
  Nie traktować Fazy 1 jako uniwersalnej zasady. Jeśli klient chce całości, ofertujemy całość z zabezpieczeniem płatności w escrow Useme.

---

## MIT 7: "Wyróżnianie Się w Hooku Przez Wytykanie Innym Używania AI"

- **Mit**:
  Wpisanie w pierwszym zdaniu: *"Większość ofert, które Pan dostał, wygenerowało AI, ja natomiast piszę osobiście..."*.
- **Falsyfikacja empiryczna**:
  To stary, oklepany schemat (generowany dawniej m.in. przez Gemini), który brzmi równie sztucznie i pretensjonalnie jak sam spam AI. Klient szuka rozwiązania swojego problemu, a nie narzekania na konkurencję.

---

## MIT 8: "Cyniczne Odwracanie Ról ('To Ja Wybieram Ciebie')"

- **Mit**:
  Pisanie z pozycji wyższości (*"Wybieram tylko najciekawsze projekty, nie pracuję z każdym"*).
- **Falsyfikacja empiryczna**:
  Gdy 10 wykonawców zaczyna kopiować ten sam pseudocoachingowy ton, zleceniodawca czuje fałsz i arogancję. Wygrywa rzeczowy, profesjonalny inżynier bez taniej manipulacji.
