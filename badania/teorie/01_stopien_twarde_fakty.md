# STOPIEŃ 1: Twarde Fakty (Pewność > 95%)

> Kryterium kwalifikacji: Twarde fakty transakcyjne (zweryfikowany przelew bankowy/escrow z Useme), statystyczna istotność wolumenowa ($n \ge 100$), lub 100% deterministyczna mechanika platformy.

---

## FAKT 1.1: Doktor Monika to Jedyny Zweryfikowany Wysoki Kontrakt Zrealizowany i Wypłacony

- **Dane transakcyjne**:
  - Zleceniodawca: Doktor Monika sp. z o.o. (NIP: 5833446979).
  - Wartość umowy Useme: **12 100,00 PLN netto** (14 883,00 PLN brutto).
  - Wypłata na konto wykonawcy: **11 083,52 PLN netto**.
  - Data wypłaty: **22.06.2026**.
  - Przedmiot: Dedykowany system rezerwacji medycznej (odwrócona logika Calendly + Tpay, pesymistyczne blokowanie slotów SQL, SMS rate-limit).
- **Wniosek strategiczny**:
  Prawdziwe, wysokie pieniądze na Useme pochodzą z **działających, zarabiających biznesów** (kliniki, kancelarie, e-commerce, hurtownie) rozwiązujących problem blokujący ich operacje, a NIE z pomysłów startupowych.

---

## FAKT 1.2: 90% "Odpisanych" Zleceń NIE Jest Wygranymi

- **Dowód empiryczny**:
  Analiza 56 rekordów w folderze `03_odpisane` oraz deklaracja Ksawiera: około 90% zleceniodawców, którzy odpowiedzieli na ofertę na Useme, **nigdy nie doszło do podpisania umowy i wpłaty escrow**.
- **Przykłady fałszywych wygranych (Phantom Leads)**:
  - Startup Zdrowie Psychiczne: wycena 34 000 PLN (klient zniknął po wymianie 3 wiadomości, brak budżetu inwestorskiego).
  - Generator CV: wycena 15 000 PLN (pomysłodawca chciał "przegadać wizję", brak środków).
  - SaaS B2B: wycena 14 000 PLN (poszukiwanie darmowej konsultacji architektonicznej).
- **Wniosek strategiczny**:
  Bot ofertowy **nie może optymalizować się pod sam wskaźnik odpowiedzi (Response Rate) ze strony marzycieli startupowych**. Metryką sukcesu jest przejście do płatnego etapu (Faza 1 / Escrow).

---

## FAKT 1.3: WordPress to Bezwzględny Czerwony Ocean

- **Dane statystyczne**:
  - Całkowita liczba zleceń: $n = 104$ (22.1% całego rynku w bazie).
  - Wygrane: 7 zleceń.
  - Przegrane: 97 zleceń.
  - **Win Rate: 6.73%** (najniższy wśród wszystkich popularnych technologii).
- **Przyczyna**:
  Ogromny napływ tanich wykonawców, agencji masowych oraz freelancerów licytujących w dół za 100-300 PLN.
- **Wniosek strategiczny**:
  Składanie generycznych ofert na WordPress to marnowanie zasobów API i limitów konta. WordPress jest dopuszczalny tylko przy zleconym dedykowanym kodzie (wtyczka, custom API, integracja ERP) z budżetem > 1500 PLN.

---

## FAKT 1.4: Żadna Oferta Nie Domyka Się w Treści Publicznej Useme

- **Mechanika platformy**:
  Treść oferty na Useme jest widoczna wyłącznie dla zleceniodawcy. Jej jedyną funkcją jest **otwarcie prywatnego wątku komunikacyjnego (priv)**.
- **Wniosek strategiczny**:
  Próba "sprzedania całego projektu i opisania 50 kroków w treści oferty" jest błędem. Oferta ma wywołać impuls do kliknięcia "Odpowiedz" i zadania pytania Ksawierowi.

---

## FAKT 1.5: Question CTA Zwiększa Wskaźnik Odpowiedzi o +26.4%

- **Dowód testowy**:
  Oferty kończące się pytaniem decyzyjnym (architektonicznym rozwidleniem) uzyskują o 26.4% wyższy wskaźnik otwarcia dyskusji niż oferty kończące się formułą *"Zapraszam do kontaktu / zdzwońmy się"*.
- **Dlaczego to działa**:
  Zleceniodawca nie musi zastanawiać się, co odpisać – dostaje gotowe pytanie A lub B dotyczące jego własnego biznesu.

---

## FAKT 1.6: Czysty Format Tekstowy Bez Stylizacji Markdown

- **Format wiadomości Useme**:
  Wiadomości na Useme renderowane są w prostym formularzu tekstowym.
  - Zakaz stosowania pogrubień markdown (`**tekst**`), nagłówków (`###`) oraz list myślnikowych (`- `). Wyglądają jak wygenerowane maszynowo przez bota.
  - Wymóg: Krótkie akapity (2-3 zdania), naturalny ton inżynierski, podpis `"Pozdrawiam, Ksawier"`.

---

## FAKT 1.7: Zakaz Udawania Mowy Przez Tekst (AI Pretend-Speech)

- **Doświadczenie rynkowe i analiza konkurencji**:
  Wszelkie próby udawania potocznej mowy w tekście (sztuczne dopiski P.S. o AI, teatralne westchnienia typu „Przyznam szczerze”, cyniczne odwracanie ról „to ja wybieram Ciebie”) są natychmiast rozpoznawane przez zleceniodawcę jako tani, żenujący trik.
- **Żelazna zasada**:
  Żaden z topowych wykonawców z badania rynku nie stosuje takich chwytów. Oferta musi brzmieć jak profesjonalna, konkretna notatka inżynierska skupiona wyłącznie na problemie technicznym klienta.

