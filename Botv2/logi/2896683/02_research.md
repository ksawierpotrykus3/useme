Oto ustalenia researchowe w zakresie wskazanym w dzienniku.

---

## 1. Limity Shopify Files i hosting wideo

**Fakty:**

Shopify Files (zakładka „Pliki" w panelu admina) ma twarde limity:
- **Obrazy:** max 20 MB, max 25 MP, formaty JPEG/PNG/WEBP/HEIC/GIF
- **Wideo (Files page):** max **1 GB**, max **10 minut**, rozdzielczość do 4K, formaty MOV/MP4/WEBM
- Shopify automatycznie transkoduje wideo do HLS (480p/720p/1080p) oraz MP4, ale **nie oferuje adaptacyjnego bitrate'u (ABR)** w odtwarzaczu natywnym

**Kluczowy problem dla tła strony głównej:** Plik 1 GB to maksimum, ale dla autoplay w tle na mobile nawet 10-20 MB jest zbyt dużym obciążeniem. Shopify Files **nie nadaje się** na duże wideo tła — nie ma CDN dedykowanego dla wideo, nie ma lazy loadingu ani poster frame'ów wbudowanych w system.

**Hosting zewnętrzny — ceny (2026):**

| Platforma | Model cenowy | Koszt orientacyjny |
|---|---|---|
| **Bunny Stream** | $0.005/GB delivered | ~$1.50–15/mies. przy małym ruchu |
| **Cloudflare Stream** | $5/1000 min streamowanych + $5/1000 min przechowywanych | ~$5.50–55/mies. |
| **Mux** | $1/1000 min encoded + storage | ~$11–110/mies. (droższy, developer-first) |

**Wniosek dla oferty:** Bunny Stream jest najtańszy przy dużym wolumenie, ale wymaga więcej pracy setupowej. Cloudflare Stream to złoty środek. Mux jest najdroższy, ale ma najlepsze API i analitykę. **Żadna z tych platform nie integruje się natywnie z Shopify** — wymaga customowego kodu Liquid/JS do osadzenia odtwarzacza i lazy loadingu.

---

## 2. Consent Mode v2 + Shopify Customer Privacy API

**Fakty:**

Consent Mode v2 wymaga **czterech sygnałów**: `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage` — każdy musi mieć wartość `granted` lub `denied`.

**Shopify NIE ma natywnego CMP.** Shopify dostarcza **Customer Privacy API** — warstwę, do której CMP *musi* pisać przez `Shopify.customerPrivacy.setTrackingConsent()`. Bez CMP, które wywołuje tę metodę, sygnały nie są propagowane do Google tagów.

**Czy natywna integracja Google & YouTube wystarczy?** Google wspiera: „If you're using the Google & YouTube app for conversion tracking and have set up your CMP, consent mode should work automatically". Ale **wymaga to wcześniej skonfigurowanego CMP** — sama aplikacja Google & YouTube nie zbiera zgód.

**Konsekwencja braku wdrożenia:** Google nie aktywuje modelowania konwersji dla ruchu EOG. Smart Bidding ma mniej sygnału, raportowany ROAS staje się „noisy".

**CMP — ceny (2026):**

| CMP | Darmowy plan | Płatny plan | Integracja z Shopify Customer Privacy API |
|---|---|---|---|
| **CookieYes** | 5 000 pageviews/mies., 1 domena | od $10/mies. (100K pageviews) | TAK |
| **Cookiebot** | ograniczony (50 podstron) | od ~€7–30/mies. w zależności od planu | TAK (Built for Shopify) |
| **Pandectes** | brak | ~$9–25/mies. | TAK, Google Certified CMP + IAB TCF v2.2 |

**Wniosek dla oferty:** Dla sklepu PL z kampaniami Google Ads **CMP jest obowiązkowe** — Shopify Customer Privacy API to tylko warstwa techniczna, nie zbiera zgód. CookieYes jest najtańszy z darmowym tierem, ale przy kampaniach Ads lepiej wybrać Google Certified CMP (Pandectes lub Cookiebot) dla pełnej zgodności z Consent Mode v2.

---

## 3. Aplikacje PL — InPost, płatności, faktury (koszty miesięczne)

### InPost (Paczkomaty)

| Aplikacja | Darmowy plan | Płatny plan |
|---|---|---|
| **InPost Paczkomaty ‑ Progus** | 5 zamówień/mies. | $9.99/mies. (150 zam.), $19.99/mies. (600 zam.), $49.99/mies. (2000 zam.) |
| **Paczkomaty InPost (Tale Commerce)** | brak | $19/mies. lub $192/rok (~$16/mies.) |

**Uwaga:** Wszystkie warianty działają na planach Basic i Grow. Koszt przesyłek InPost rozliczany osobno na podstawie umowy z InPost.

### Płatności PL

- **Shopify Payments** jest dostępne dla polskich sprzedawców i obsługuje karty, Shop Pay, Apple Pay, Google Pay, **BLIK oraz Przelewy24** natywnie
- **PayU** ma oficjalną aplikację Shopify
- **Przelewy24, Tpay, BlueMedia (Autopay)** wymagają instalacji zewnętrznych aplikacji i połączenia konta przez API
- Popularne KIP-y: Dotpay, PayU, PayLane, Tpay, Przelewy24, eCard, imoje, Adyen, Klarna

### Faktury

- **Fakturownia** — oficjalna integracja z Shopify dostępna w App Store
- Automatyzuje wystawianie faktur VAT, proform, paragonów, korekt, obsługuje B2B/B2C, wiele walut, zwroty
- **Cena:** brak w wynikach wyszukiwania — **niepotwierdzone**. Wymaga weryfikacji bezpośrednio w Shopify App Store.

---

## 4. Plany Shopify — ceny (2026)

| Plan | Cena roczna (mies.) | Cena miesięczna | Uwagi |
|---|---|---|---|
| **Basic** | $29/mies. | $39/mies. | 10 lokalizacji, 2.9% + 30¢ online |
| **Grow** (d. Shopify) | $79/mies. | $105/mies. | 2.7% + 30¢ online |
| **Advanced** | $299/mies. | $399/mies. | 2.5% + 30¢, lokalne店面 per market |
| **Plus** | od $2 300/mies. | od $2 300/mies. | Custom checkout, B2B, 200 lokalizacji |

**Ceny w PLN (orientacyjnie, wg Tale Commerce):** Shopify od 109 do 1630 PLN/mies., Plus od 2100 EUR.

**Co plan warunkuje (istotne dla odpowiedzi na pytanie klienta):**
- **Shopify Functions** i **checkout extensibility** — pełny dostęp wymaga planów wyższych niż Basic; na Basic ograniczone możliwości customizacji checkoutu
- **Shopify Plus** — jedyny plan z w pełni customizowalnym checkoutem (checkout.liquid)
- **Limity API** — rosną z planem, co wpływa na to, co da się zrobić natywnie vs. przez appkę

**Wniosek dla oferty:** Pytanie o plan Shopify jest zasadne — na Basic nie da się zrobić pełnej customizacji checkoutu, a klient chce kampanie Google Ads z konwersjami. Dla sklepu z 1 produktem i akcesoriami **Grow** ($79/mies. rocznie) prawdopodobnie wystarczy, ale **Plus** dopiero daje pełną kontrolę nad checkoutem.

---

## Podsumowanie luk / niepotwierdzone

| Pozycja | Status |
|---|---|
| Cena Fakturownia w Shopify App Store | **Niepotwierdzone** — nie znaleziono w wynikach |
| Cena Przelewy24/Tpay jako standalone app | **Niepotwierdzone** — wymaga weryfikacji w App Store |
| Czy Shopify Files obsługuje lazy loading natywnie | **Niepotwierdzone** — brak danych w wynikach |
| Dokładne limity API per plan | **Niepotwierdzone** — wymaga sprawdzenia w dokumentacji Shopify |