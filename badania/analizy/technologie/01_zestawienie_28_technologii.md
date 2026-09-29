# Zestawienie 28 Technologii Rynku Useme (Próba N=481)

> [!WARNING] Ostrzeżenie Metodologiczne dot. Wielkości Próby
> Dla technologii o wolumenie $n < 15$ zleceń, wskaźnik Win Rate obarczony jest wysokim błędem standardowym ($\pm 25-35\%$). Wyniki te stanowią **poszlaki badawcze**, a nie gwarantowane „złote strzały”. Jedyną grupą o pełnej istotności statystycznej ($n > 100$) jest **WordPress/WooCommerce ($n=108$)**, będący Czerwonym Oceanem (**6.5% Win Rate**).

---

## 1. Pełna Tabela Granularnych Technologii (Dane Empiryczne z `przelicz_baze.py`, N=481)

| Lp. | Technologia / Narzędzie | Wszystkie ($n$) | Wygrane | Przegrane | Win Rate (%) | Kategoria Próby |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | **WordPress / WooCommerce** | 108 | 7 | 101 | **6.5%** | Duża ($n \ge 50$) — Czerwony Ocean |
| 2 | **Laravel / PHP** | 46 | 5 | 41 | **10.9%** | Średnia ($15 \le n < 50$) |
| 3 | **Shopify / Liquid** | 31 | 4 | 27 | **12.9%** | Średnia ($15 \le n < 50$) |
| 4 | **React / Next.js** | 30 | 3 | 27 | **10.0%** | Średnia ($15 \le n < 50$) |
| 5 | **Python / Django / FastAPI** | 28 | 5 | 23 | **17.9%** | Średnia ($15 \le n < 50$) |
| 6 | **Bazy danych / SQL** | 28 | 2 | 26 | **7.1%** | Średnia ($15 \le n < 50$) |
| 7 | **DevOps / Docker / VPS** | 27 | 3 | 24 | **11.1%** | Średnia ($15 \le n < 50$) |
| 8 | **Make / n8n / Zapier** | 26 | 1 | 25 | **3.8%** | Średnia ($15 \le n < 50$) |
| 9 | **Computer Vision / OCR / AI** | 24 | 2 | 22 | **8.3%** | Średnia ($15 \le n < 50$) |
| 10 | **PrestaShop** | 24 | 3 | 21 | **12.5%** | Średnia ($15 \le n < 50$) |
| 11 | **Kotlin / Android Native** | 22 | 6 | 16 | **27.3%** | Średnia ($15 \le n < 50$) — Wysoka marża |
| 12 | **BaseLinker** | 21 | 1 | 20 | **4.8%** | Średnia ($15 \le n < 50$) |
| 13 | **Swift / iOS Native** | 20 | 4 | 16 | **20.0%** | Średnia ($15 \le n < 50$) — Wysoka marża |
| 14 | **Node.js / Express / Nest** | 17 | 1 | 16 | **5.9%** | Średnia ($15 \le n < 50$) |
| 15 | **Scraping (Selenium/Playwright/Bs4)** | 14 | 3 | 11 | **21.4%** | Mała ($n < 15$) — Poszlaka |
| 16 | **Figma / UI design** | 13 | 2 | 11 | **15.4%** | Mała ($n < 15$) — Poszlaka |
| 17 | **Shoper** | 10 | 1 | 9 | **10.0%** | Mała ($n < 15$) — Poszlaka |
| 18 | **Framer / Webflow** | 10 | 1 | 9 | **10.0%** | Mała ($n < 15$) — Poszlaka |
| 19 | **IdoSell (IAI)** | 9 | 3 | 6 | **33.3%** | Mała ($n < 15$) — Poszlaka e-commerce |
| 20 | **Subiekt (GT / nexo / Sfera)** | 9 | 1 | 8 | **11.1%** | Mała ($n < 15$) |
| 21 | **Enova365** | 7 | 2 | 5 | **28.6%** | Bardzo mała ($n \le 7$) |
| 22 | **Flutter / Dart** | 7 | 0 | 7 | **0.0%** | Bardzo mała ($n \le 7$) |
| 23 | **Vue / Nuxt** | 6 | 1 | 5 | **16.7%** | Bardzo mała ($n \le 6$) |
| 24 | **.NET / C#** | 6 | 0 | 6 | **0.0%** | Bardzo mała ($n \le 6$) |
| 25 | **VoIP / Asterisk / SIP** | 5 | 2 | 3 | **40.0%** | Bardzo mała ($n \le 5$) — Anomalia |
| 26 | **Comarch (Optima / XL)** | 5 | 0 | 5 | **0.0%** | Bardzo mała ($n \le 5$) |
| 27 | **React Native** | 3 | 0 | 3 | **0.0%** | Bardzo mała ($n \le 5$) |
| 28 | **TopSolid / CAD / CAM** | 2 | 1 | 1 | **50.0%** | Bardzo mała ($n \le 5$) — Anomalia |

---

## 2. Segment Tech-Agnostic (32.8% Całego Rynku)

Poza 28 technologiami wykryto kluczowy segment:
- **Liczba zleceń bez podanej technologii**: **158 zleceń na 481 (32.8% rynku)**.
- **Liczba wygranych zleceń w tym segmencie**: **17 wygranych**.
- **Win Rate w segmencie bez technologii**: **10.8%**.
- **Zasada bota**: Zakaz narzucania ciężkiego stacku i żargonu IT. Bot oferuje proste, bezobsługowe rozwiązanie biznesowe.
