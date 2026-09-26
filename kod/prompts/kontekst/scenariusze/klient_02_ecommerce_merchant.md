# PROFIL OPERACYJNY KLIENTA: E-COMMERCE MERCHANT (ecommerce)

## 1. Minimum Operacyjne (Kim jest i czego się boi)
- **Kto to jest:** Właściciel działającego sklepu internetowego (IdoSell, Shopify, PrestaShop, Shoper, WooCommerce + BaseLinker), obsługujący od kilkudziesięciu do kilkuset zamówień dziennie (często z kanałem B2B/hurtowym).
- **Główny lęk:** Prace na żywym sklepie powodujące spadek konwersji lub wywalenie koszyka w szczycie sprzedaży, nadsprzedaż towaru (overselling), zablokowanie API przez limity zapytań (429 Rate Limit), wyciek cen hurtowych B2B do detalu.
- **Stosunek do ceny:** Myśli zwrotem z inwestycji (ROI) — jeśli naprawa koszyka lub automatyzacja BaseLinkera oszczędza czas pakowaczy lub ratuje porzucone koszyki, akceptuje rynkową stawkę.

## 2. Konkret, który MUSI paść w ofercie
- **Gwarancja pracy na stagingu / kopii roboczej:** Jasno zaznacz, że żadne zmiany nie są wgrywane na żywy sklep przed przetestowaniem ścieżki zakupowej.
- Używaj pojęć e-commerce: **mapowanie pól/atrybutów, synchronizacja stanów i cen, cenniki hurtowe B2B, webhooki vs cron, obsługa rate-limitów API, kurierzy (InPost/DPD), koszyk i checkout, PageSpeed / LCP**.
- Jeśli zlecenie dotyczy integracji katalogu XML/CSV/API, możesz zaproponować próbkę (Demo Guard): przetestowanie mapowania na próbce 10–20 produktów.

## 3. Czego kategorycznie UNIKAĆ
- Zakaz bagatelizowania problemu słowami „to proste, zrobię w chwilę" — właściciel sklepu wie, że na żywej bazie z tysiącami SKU nic nie jest trywialne.
- Zakaz proponowania ciężkiej infrastruktury (mikroserwisy, Kubernetes) do modułu sklepowego lub integracji BaseLinker.

## 4. Konstrukcja Question CTA (na koniec oferty)
Zadaj konkretne pytanie o parametry sklepu lub poproś o artefakt (Trojan Horse):
- o przykładowy plik XML/CSV od dostawcy lub strukturę wariantów SKU,
- czy synchronizacja stanów ma działać w czasie rzeczywistym po webhooku zamówienia, czy cyklicznie (cron), oraz ile SKU obejmuje baza.
