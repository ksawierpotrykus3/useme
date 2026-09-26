# STOPIEŃ 3: Poszlaki Niszowe (Pewność 20% – 40%)

> Kryterium kwalifikacji: Bardzo mała próba statystyczna ($n < 15$), pojedyncze wygrane Ksawiera, wysoka wariancja losowa ($\pm 25-40\%$). Dane te NIE są powtarzalnym lejkiem skali, lecz wskazówkami do dalszej obserwacji.

---

## POSZLAKA 3.1: Anomalia "TopSolid / CAD / CAM" (50% Win Rate)

- **Dane surowe**:
  - Liczba zleceń: $n = 2$.
  - Wygrane: 1.
  - Przegrane: 1.
  - Pozorny Win Rate: **50.00%**.
- **Ocena**:
  Brak jakiejkolwiek istotności statystycznej. Wynik to pojedyncze zlecenie, w którym specyficzna wiedza Ksawiera z zakresu skryptów dla obrabiarek/CAD trafiła na brak jakichkolwiek innych ofert na Useme.
- **Wniosek operacyjny**:
  Jeśli pojawi się zlecenie z hasłem CAD/CAM/TopSolid, bot wysyła ofertę w trybie VIP Fast-Track, ale nie wolno budować na tym prognoz finansowych.

---

## POSZLAKA 3.2: Nisza "VoIP / Asterisk / SIP" (40% Win Rate)

- **Dane surowe**:
  - Liczba zleceń: $n = 5$.
  - Wygrane: 2.
  - Przegrane: 3.
  - Pozorny Win Rate: **40.00%**.
- **Ocena**:
  Telefonia internetowa, centrale VoIP i integracje z bramkami SMS mają bardzo mało zgłoszeń od typowych web-developerów. 2 wygrane na 5 prób to obiecujący wynik, jednak próba $n=5$ oznacza margines błędu $\pm 35\%$.

---

## POSZLAKA 3.3: Integracje E-commerce Polskich Platform (IdoSell 33.3%, PrestaShop 11.8%)

- **Dane surowe**:
  - IdoSell: $n = 9$, wygrane = 3, **Win Rate = 33.33%**.
  - PrestaShop: $n = 17$, wygrane = 2, **Win Rate = 11.76%**.
  - Baselinker: $n = 4$, wygrane = 0, **Win Rate = 0.00%**.
- **Ocena**:
  IdoSell wykazuje wyższą skuteczność niż WooCommerce i Shopify, prawdopodobnie dlatego, że polscy sprzedawcy na IdoSell mają większe obroty i wyższe budżety na dedykowane integracje API niż mikro-sprzedawcy na darmowym WooCommerce.

---

## POSZLAKA 3.4: Systemy ERP i Przemysł (Enova365, Comarch Optima, Odoo)

- **Dane surowe**:
  - Enova365: $n = 3$, wygrane = 1 (Case CB Kołcz - 5500 PLN).
  - Comarch ERP / Optima: $n = 5$, wygrane = 1.
  - Odoo ERP: $n = 6$, wygrane = 1.
- **Ocena**:
  Klienci korporacyjni i przemysłowi rzadko zlecają na Useme, ale gdy to robią, płacą wysokie stawki bez negocjacji groszowych. Jednak częstotliwość pojawiania się tych zleceń to zaledwie 1-2 w miesiącu.

---

## POSZLAKA 3.5: Czas Reakcji na Wiadomości Priv (< 15 Minut)

- **Założenie**:
  Klient, który otrzymał odpowiedź w ciągu pierwszego kwadransa od zadania pytania na priv, ma 3-krotnie większe prawdopodobieństwo sfinalizowania umowy niż klient, który czekał 4 godziny.
- **Ocena**:
  Prawdopodobieństwo behawioralne wysokie, ale brak zautomatyzowanego pomiaru w obecnej wersji silnika (wymaga wdrożenia modułu asynchronicznego monitorowania powiadomień).
