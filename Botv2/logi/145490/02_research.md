## 1. Stan e-commerce w Framer — krytyczne ograniczenia

**Framer nie ma natywnego sklepu.** To narzędzie design-first, które nie posiada wbudowanego koszyka, checkoutu ani zarządzania podatkami od sprzedaży globalnej. Framer oferuje integracje z Shopify (Framer Commerce) oraz zewnętrzne wtyczki (Stripe przez Axle, Dodo Payments), ale to nakładki, a nie natywny backoffice.

**Limity produktów w Framer są twarde i niskie:**
- Plan Basic: **100 pozycji** w kolekcji CMS (czyli produktów).
- Framer Commerce: plany od 12 USD/mies. dla **25 produktów**, do 40 USD/mies. dla **unlimited** — ale to limity samego pluginu, nie pełnego backoffice.
- Rekomendowany scenariusz: katalogi **poniżej 200 produktów**, sprzedaż kuratorowana, z Shopify jako backendem.

**Framer nie jest zbudowany do:** dużej skali magazynowej, złożonej logiki fulfillmentu, ani natywnego multi-language.

## 2. Stan e-commerce w Webflow — lepszy, ale wciąż ograniczony

**Limity produktów (stan aktualny):**
- Ecommerce Standard: **500 produktów** (wcześniej 500 łącznie z CMS; obecnie limity rozdzielone: 500 ecommerce + 2 000 CMS).
- Ecommerce Plus: **5 000 produktów** + 10 000 CMS.
- Ecommerce Advanced: **15 000 produktów** + 10 000 CMS.

**Płatności:** Webflow obsługuje wyłącznie **Stripe i PayPal** (plus Apple Pay/Google Pay przez Stripe). Brak natywnego wsparcia dla Przelewy24, iDEAL, BLIK.

**Kluczowe ograniczenia backoffice:**
- **2% opłaty transakcyjnej** na planie Standard; 0% na Plus/Advanced.
- **Brak natywnego odzyskiwania porzuconych koszyków**.
- **Brak integracji z API kurierów** (FedEx, UPS, USPS live rates) ani z systemami 3PL.
- **Sztywne pola checkoutu** — brak elastyczności w customizacji formularza zamówienia.

## 3. Alternatywy: WooCommerce i stack headless

**WooCommerce (WordPress):** pełna kontrola nad hostingiem, brak limitów produktów, elastyczność wtyczek, dojrzały ekosystem e-commerce. Wymaga jednak więcej pracy technicznej i utrzymania.

**Stack headless (Next.js + Stripe/Przelewy24 + Sanity/Shopify jako backend):** pełna kontrola nad animacjami i sklepem w jednym, bardzo szybkie ładowanie (LCP 0,8–1,2 s vs 2,5–4 s dla standardowego WooCommerce), ale **wysoki koszt deweloperski** i konieczność utrzymania przez zespół. Typowy stack: Next.js (SSR/SSG) + Shopify Storefront API lub Medusa + Sanity (CMS) + Stripe.

## 4. Compliance UE — czego brakuje w briefie

**Przycisk odstąpienia (Withdrawal Button):** Od **19 czerwca 2026** obowiązuje art. 11a dyrektywy 2011/83/UE (zmienionej dyrektywą 2023/2673). Sprzedawcy online do konsumentów UE **muszą** zapewnić elektroniczną funkcję odstąpienia, która:
- jest **widocznie wyeksponowana** na interfejsie,
- jest **łatwo dostępna**,
- działa **nieprzerwanie przez cały okres odstąpienia**,
- jest oznaczona etykietą **„Withdraw from contract here”** lub równoważnym jednoznacznym sformułowaniem.

Obowiązek dotyczy również sprzedawców spoza UE, jeśli targetują konsumentów w UE.

**Omnibus (historia cen):** Dyrektywa 2019/2161 wymaga, aby **każda obniżka ceny** była prezentowana wraz z **najniższą ceną z 30 dni poprzedzających obniżkę**. W Polsce obowiązuje od stycznia 2023; UOKiK może nałożyć karę do **10% rocznego przychodu**.

**Wniosek:** Brief klienta nie zawiera ani przycisku odstąpienia, ani mechanizmu śledzenia historii cen. To elementy, które trzeba dodać do zakresu — **nie pominąć**.

## 5. Rekomendacja technologii (z widełkami)

Mając na uwadze kombinację wymagań — **pełny sklep z backoffice + złożone animacje jako interaktywne elementy + CMS + szybkie ładowanie mobile + estetyka editorial** — rekomendujemy **WooCommerce (WordPress) jako bezpieczny kompromis** albo **stack headless (Next.js + Stripe/Przelewy24 + Sanity/Shopify backend)** dla maksymalnej kontroli.

**Widełki orientacyjne:**
- **WooCommerce:** 15 000–35 000 PLN (zależnie od liczby sekcji i integracji płatności).
- **Stack headless:** 40 000–80 000 PLN+ (wyższy koszt, ale pełna kontrola nad animacjami i sklepem).
- **Webflow:** 10 000–25 000 PLN (szybszy start, ale limity produktów i płatności).
- **Framer:** **nie rekomendujemy jako fundamentu sklepu** — chyba że asortyment to <200 produktów i klient akceptuje Shopify jako backend.

## 6. Pytania do klienta (2 krytyczne)

1. **Ile produktów ma być w sklepie i czy asortyment ma rosnąć w czasie?** Od tego zależy wybór platformy — Webflow ma twarde limity (500/5 000/15 000), a WooCommerce i headless nie mają ich wcale.
2. **Do kogo sprzedajesz (konsumenci UE / B2B / rynki poza UE) i jakimi metodami chcesz przyjmować płatności (Przelewy24, Stripe, PayPal, BLIK)?** To determinuje integracje i dobór elementów compliance (przycisk odstąpienia, Omnibus).

## 7. Potwierdzenie zakresu

**Tak, realizujemy e-commerce i płatności online** — zarówno w modelu WooCommerce, jak i headless. Pełny zakres: koszyk, checkout, płatności, zarządzanie produktami, cenami, dostępnością i zamówieniami.

**Niepotwierdzone:** dokładne stawki za integrację Przelewy24/BLIK w stacku headless (wymaga osobnej wyceny).