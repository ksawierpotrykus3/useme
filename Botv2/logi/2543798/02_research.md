## 1. Płatności online i terminale w Polsce

**Przelewy24 (P24)** to najpopularniejszy polski hub płatności online, agregujący karty, BLIK, przelewy bankowe i portfele. W kontekście POS udostępniany jest przez Mollie, Stripe, Adyen lub PayU. P24 działa jako hostowana strona płatności otwierana w widoku przeglądarki wewnątrz POS — klient wybiera BLIK, bank lub kartę, a po potwierdzeniu zamówienie zapisuje się z powrotem w systemie.

**BLIK** to dominująca metoda płatności mobilnej w Polsce — klient wpisuje 6-cyfrowy kod z aplikacji bankowej na stronie płatności, a cały proces trwa ok. 5 sekund.

**Porównanie prowizji (2026)** :
- **Przelewy24**: karty od 1,4% + 0,30 PLN, BLIK 0,79% (w abonamencie 50 PLN/mc)
- **PayU**: karty od 1,6% + 0,20 PLN, BLIK 0,99%, wypłata D+1
- **Stripe**: karty 1,4% + 0,25 EUR w UE, BLIK 1,4%, wypłata D+7
- **Tpay**: karty od 1,4%, BLIK 0,99%

Wszyscy krajowi operatorzy mają licencję KIP KNF, PCI DSS Level 1 i wypłaty D+1 po KYB. Dla typowego sklepu z dominującym BLIK-iem polskie KIP-y wychodzą taniej (koszt ~98–158 PLN przy 10 000 PLN obrotu/mc vs ~284 PLN u Stripe).

**Uwaga dla zlecenia**: żadne ze źródeł nie potwierdza integracji tych bramek z **terminalami fizycznymi** w trybie POS. Wszystkie opisane scenariusze to płatności online (hostowana strona, BLIK, przelew) — **niepotwierdzone** jest, czy i które z tych bramek oferują API do terminali stacjonarnych typu Ingenico/PAX.

---

## 2. API drukarek kuchennych / KDS

**KDS (Kitchen Display System)** to dedykowany ekran zastępujący papierowe tickety kuchenne, który stał się centralnym elementem nowoczesnej orkiestracji kuchni.

**Sposób integracji POS → KDS**: po zatwierdzeniu rachunku POS wysyła bon do drukarki kuchennej albo do systemu wyświetlania zamówień KDS. System automatycznie przypisuje pozycje do odpowiednich miejsc realizacji — kuchni gorącej, zimnej, pizzerii, baru lub cukierni — bez ręcznego przekazywania informacji między pracownikami.

**Kluczowe wymaganie rynkowe w Polsce**: integracja z API agregatorów dostaw (Pyszne.pl, Uber Eats, Glovo) jest obowiązkowym kryterium przetargowym — dostawcy bez natywnego wsparcia API dla tych platform są coraz częściej wykluczani z przetargów.

**Przykład integracji**: Insoft PC-Gastronom obsługuje drukarki/monitory kuchenne (KDS) i zarządza złożonymi zamówieniami stolikowymi; system jest kompatybilny z ponad 150 specjalistycznymi urządzeniami sprzętowymi. Restimo agreguje zamówienia z Uber Eats, Glovo, Wolt i przesyła je bezpośrednio do POS.

**Uwaga dla zlecenia**: zlecenie mówi o „WYŚLIJ na kuchnię/bar (ticket)”, ale **nie precyzuje**, czy istnieje już KDS/drukarka, z którą system ma się integrować. Źródła potwierdzają, że integracja KDS wymaga albo drukarki termicznej, albo ekranu KDS, albo API konkretnego dostawcy — bez tego zakres integracji pozostaje **niepotwierdzony**.

---

## 3. React Native vs Flutter dla POS na małych ekranach

**Udział w rynku (2026)**: Flutter ~46% wśród deweloperów cross-platform, React Native ~35%.

**Wydajność** — różnica jest obecnie nieznaczna dla typowych aplikacji biznesowych:

| Metryka | React Native (New Arch) | Flutter (Impeller) |
|---|---|---|
| Czas startu (zimny) | 800–1200 ms | 600–1000 ms |
| Spójność 60 fps | 95%+ | 98%+ |
| Rozmiar aplikacji (min) | 8–12 MB | 15–20 MB |
| Użycie pamięci (baza) | 40–60 MB | 50–70 MB |

Flutter ma lekką przewagę w animacjach i gwarantowanej spójności klatek, React Native daje mniejsze bundle i natywny wygląd UI per platforma.

**Rekomendacja z praktyki**: dla większości aplikacji biznesowych (systemy rezerwacji, e-commerce, narzędzia wewnętrzne) **React Native jest praktycznym wyborem w 2026** — większy ekosystem, JavaScript/TypeScript znany większości zespołów, łatwiejszy hiring. Flutter wygrywa, gdy **UI jest wyróżnikiem** — pixel-perfect spójność iOS/Android, zaawansowane animacje na średniej klasy urządzeniach.

**Przypadek POS**: zbudowano aplikację POS dla eventów (Booxos) na Flutterze w 4 tygodnie — QR login, katalog produktów, Tap to Pay, paragony cyfrowe, jedna codebase na iOS i Android. **Native wygrywa**, gdy aplikacja wymaga głębokiego SDK sprzętowego (skanery przemysłowe, czytniki kart z certyfikowanym firmware) lub certyfikacji płatniczej na poziomie OS.

**Uwaga dla zlecenia**: jeśli POS ma integrować się z **terminalami płatniczymi fizycznymi** (certyfikowanymi PCI PTS), może to wymusić podejście natywne lub hybrydowe — cross-platform może nie obsłużyć SDK producenta terminala. To **niepotwierdzone** w źródłach, ale wynika z warunków brzegowych opisanych powyżej.

---

## Wnioski dla zlecenia (tylko diagnoza, nie recepta)

1. **Płatności**: polskie bramki (P24, PayU) mają dojrzałe API online, ale **nie ma potwierdzenia integracji z terminalami fizycznymi** w trybie POS. Split payment częściowy (jak w zleceniu) wymaga własnego silnika rozliczeniowego — żadna bramka nie oferuje tego „z pudełka”.
2. **KDS**: rynek wymaga integracji z API agregatorów (Pyszne, Uber Eats, Glovo) jako standardu. Zlecenie mówi „menu jak delivery” — to **może** oznaczać potrzebę integracji z tymi platformami, ale zlecenie tego wprost nie mówi.
3. **Technologia**: React Native jest praktyczniejszy dla zespołów JS/React i szybszego prototypowania; Flutter daje spójniejszy UI na małych ekranach. Wybór zależy od tego, czy POS musi integrować się z fizycznymi terminalami płatniczymi (wtedy potencjalnie native/hybryda).