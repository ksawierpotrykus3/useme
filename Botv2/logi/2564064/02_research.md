## 1. Shopify Payments w Polsce

**Shopify Payments jest dostępny w Polsce** – od marca 2025 roku dołączył do 15 nowych krajów europejskich, w tym Polski.

**Kluczowe ograniczenie:** W ramach Shopify Payments **Przelewy24 działa wyłącznie w sklepach, które aktywowały je wcześniej. Nowe sklepy nie mogą już włączyć P24 przez Shopify Payments.**

**Dostępne metody lokalne w Polsce (2026):** BLIK, Klarna, MobilePay, TWINT – włączane ręcznie w ustawieniach płatności. BLIK przez Shopify Payments jest tańszy od kart.

**Ważne:** Shopify Payments w Polsce obsługuje wyłącznie sprzedaż online – nie działa z Shopify POS (płatności stacjonarne).

---

## 2. Foxy.io – obsługa Przelewy24/BLIK

**Potwierdzone:** Foxy.io obsługuje BLIK oraz Przelewy24 (P24) przez integrację z PayPal Commerce. Pełna lista obsługiwanych metod: Venmo, PayPal Credit, Bancontact, **BLIK**, eps, iDEAL, MyBank, **Przelewy24 (P24)**, Trustly – dostępność zależy od kraju.

**Ograniczenie:** Foxy.io to hosted checkout dla subskrypcji/digital – nie jest standardową bramką dla fizycznych produktów na Shopify. Brak natywnej integracji z Shopify dla śledzenia wysyłki – wymaga integracji przez zewnętrzne systemy (np. OrderDesk).

---

## 3. Najszybsze motywy Shopify (2026)

**Dawn (darmowy, oficjalny Shopify):**
- Najszybszy i najczęściej aktualizowany darmowy motyw – flagowy motyw Shopify, referencyjna implementacja wszystkich funkcji Online Store 2.0.
- ~30KB JavaScript, wynik PageSpeed na mobile 92+, ok. 17 typów sekcji.
- **Wada:** bardzo podstawowy design – wymaga dużej customizacji, by nie wyglądał generycznie; mało wbudowanych sekcji w porównaniu do płatnych motywów.

**Minimalin (płatny, TemplateMonster):**
- Zbudowany na Shopify Online Store 2.0, skoncentrowany na wydajności, minimalistyczny design z zaawansowaną funkcjonalnością eCommerce.
- Zoptymalizowana struktura zapewnia szybki czas ładowania, responsywność i płynne zakupy na wszystkich urządzeniach.
- Zawiera: zaawansowane filtrowanie, wyszukiwanie predykcyjne, mega menu, szybki podgląd, listę życzeń, rekomendacje produktów, integrację z newsletterem, obsługę wielu walut i języków.

**Inne szybkie motywy (2026):** Streamline, Warehouse, Avenue, Motion, Capital, Story.

---

## 4. Przelewy24 / PayU – prowizje i czas weryfikacji

### Prowizje (2026)

| Metoda | Przelewy24 | PayU |
|---|---|---|
| BLIK | 0,79% (abonament) – 1,9% | 0,99% – 1,4% |
| Karty | od 1,5% | od 1,6% |
| Szybkie przelewy | ok. 1% | – |

Źródła: 

Obie bramki mają **gotowe wtyczki do Shopify** – różnice w łatwości wdrożenia bywają minimalne.

**Ukryty koszt:** Każda zewnętrzna bramka (Przelewy24/PayU) oznacza **dodatkową prowizję Shopify** naliczaną oprócz prowizji samej bramki.

### Czas weryfikacji

| Bramka | Standardowy czas weryfikacji |
|---|---|
| **Przelewy24** | do 48 godzin roboczych (8:00–16:00); braki w dokumentach wydłużają termin |
| **PayU** | od kilku godzin do maksymalnie 3 dni roboczych |

**Ostrzeżenie:** Weryfikacja Przelewy24 może trwać znacznie dłużej niż deklarowane 48h – jeden z merchantów raportował **4 tygodnie oczekiwania** na weryfikację vendora, co uniemożliwiło rozpoczęcie sprzedaży.

**Czas integracji technicznej:** Przelewy24 – 1–2 dni; PayU – 1–3 dni; Stripe – 0,5–2 dni.

**Czas realizacji wypłat:** PayU – do 10 dni dla przelewów, 5 dni dla BLIK/kart; Przelewy24 – płatność autoryzowana natychmiast po weryfikacji w bankowości mobilnej.

---

## Wnioski dla zlecenia

1. **Shopify Payments w Polsce NIE obsłuży Przelewy24 dla nowego sklepu** – jeśli klient chce P24, musi użyć zewnętrznej bramki (Przelewy24 lub PayU), co wiąże się z dodatkową prowizją Shopify.
2. **Foxy.io obsługuje P24/BLIK**, ale jest to checkout dla subskrypcji/digital – nie jest to rozwiązanie dla fizycznych produktów na Shopify.
3. **Dawn jest najszybszym darmowym motywem** (92+ PageSpeed mobile), ale wymaga customizacji; Minimalin to płatna alternatywa z lepszym designem out-of-the-box.
4. **Czas weryfikacji Przelewy24 może zaskoczyć** – deklarowane 48h to minimum, a realnie może trwać tygodniami.