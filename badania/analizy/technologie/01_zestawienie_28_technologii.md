# Zestawienie 28 Technologii Rynku Useme (Próba N=470)

> [!WARNING] Ostrzeżenie Metodologiczne dot. Wielkości Próby
> Dla technologii o wolumenie $n < 15$ zleceń, wskaźnik Win Rate obarczony jest wysokim błędem standardowym ($\pm 25-35\%$). Wyniki te stanowią **poszlaki badawcze**, a nie gwarantowane "złote strzały". Jedyną grupą o pełnej istotności statystycznej ($n > 100$) jest **WordPress/WooCommerce**, będący Czerwonym Oceanem.

---

## 1. Pełna Tabela Granularnych Technologii (Dane Empiryczne)

| Lp. | Technologia / Narzędzie | Wszystkie ($n$) | Wygrane | Przegrane | Win Rate (%) | Kategoria Próby |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| 1 | **WordPress / WooCommerce** | 104 | 7 | 97 | **6.73%** | Duża ($n \ge 50$) - Czerwony Ocean |
| 2 | **Laravel / PHP** | 44 | 5 | 39 | **11.36%** | Średnia ($15 \le n < 50$) |
| 3 | **Shopify / Liquid** | 31 | 4 | 27 | **12.90%** | Średnia ($15 \le n < 50$) |
| 4 | **React / Next.js** | 30 | 3 | 27 | **10.00%** | Średnia ($15 \le n < 50$) |
| 5 | **Python / Django / FastAPI** | 27 | 5 | 22 | **18.52%** | Średnia ($15 \le n < 50$) |
| 6 | **DevOps / Docker / VPS** | 27 | 3 | 24 | **11.11%** | Średnia ($15 \le n < 50$) |
| 7 | **Bazy danych / SQL** | 27 | 2 | 25 | **7.41%** | Średnia ($15 \le n < 50$) |
| 8 | **Make / n8n / Zapier** | 26 | 1 | 25 | **3.85%** | Średnia ($15 \le n < 50$) |
| 9 | **Scraping / Playwright / BS4** | 24 | 3 | 21 | **12.50%** | Średnia ($15 \le n < 50$) |
| 10 | **Kotlin / Android Native** | 22 | 6 | 16 | **27.27%** | Średnia ($15 \le n < 50$) - Wysoka marża |
| 11 | **Flutter / Dart** | 20 | 4 | 16 | **20.00%** | Średnia ($15 \le n < 50$) - Wysoka marża |
| 12 | **PrestaShop** | 17 | 2 | 15 | **11.76%** | Średnia ($15 \le n < 50$) |
| 13 | **Google Sheets / AppScript** | 15 | 2 | 13 | **13.33%** | Średnia ($15 \le n < 50$) |
| 14 | **Vue.js / Nuxt** | 13 | 1 | 12 | **7.69%** | Mała ($n < 15$) - Poszlaka |
| 15 | **Node.js / Express / NestJS** | 12 | 2 | 10 | **16.67%** | Mała ($n < 15$) - Poszlaka |
| 16 | **C# / .NET** | 10 | 1 | 9 | **10.00%** | Mała ($n < 15$) - Poszlaka |
| 17 | **IdoSell** | 9 | 3 | 6 | **33.33%** | Mała ($n < 15$) - Poszlaka e-commerce |
| 18 | **AI / OpenAI / LLM** | 9 | 1 | 8 | **11.11%** | Mała ($n < 15$) - Poszlaka |
| 19 | **Swift / iOS Native** | 8 | 1 | 7 | **12.50%** | Mała ($n < 15$) - Poszlaka |
| 20 | **Odoo ERP** | 6 | 1 | 5 | **16.67%** | Mała ($n < 15$) - Poszlaka |
| 21 | **VoIP / Asterisk / SIP** | 5 | 2 | 3 | **40.00%** | Bardzo mała ($n \le 5$) - Anomalia |
| 22 | **Comarch ERP / Optima** | 5 | 1 | 4 | **20.00%** | Bardzo mała ($n \le 5$) - Poszlaka |
| 23 | **Baselinker** | 4 | 0 | 4 | **0.00%** | Bardzo mała ($n \le 5$) |
| 24 | **Enova365** | 3 | 1 | 2 | **33.33%** | Bardzo mała ($n \le 5$) - Pojedynczy case |
| 25 | **TopSolid / CAD / CAM** | 2 | 1 | 1 | **50.00%** | Bardzo mała ($n \le 5$) - Anomalia |
| 26 | **C++ / Qt** | 2 | 0 | 2 | **0.00%** | Bardzo mała ($n \le 5$) |
| 27 | **Allegro API** | 2 | 0 | 2 | **0.00%** | Bardzo mała ($n \le 5$) |
| 28 | **Subiekt GT / Nexo** | 2 | 0 | 2 | **0.00%** | Bardzo mała ($n \le 5$) |

---

## 2. Segment Tech-Agnostic (33% Całego Rynku)

Poza 28 technologiami wykryto kluczowy segment:
- **Liczba zleceń bez podanej technologii**: 155 zleceń (33.0% rynku).
- **Liczba wygranych zleceń w tym segmencie**: 17 wygranych.
- **Win Rate w segmencie bez technologii**: 10.97%.
- **Charakterystyka**: Klienci pytają o "pozyskanie bazy firm", "skrypt do wystawiania ogłoszeń", "bota do gry", "system rezerwacji", "przeliczenie arkuszy Excel".
- **Zasada bota**: Zakaz narzucania stacku (React/FastAPI). Bot oferuje proste, bezobsługowe rozwiązanie biznesowe.

---

## 3. Podział Strategiczny dla Bota

1. **Czerwony Ocean (WordPress $n=104$, Win Rate 6.7%)**:
   - Skrajna konkurencja cenowa.
   - Wymóg: Ofertowanie tylko z wyższym filtrem budżetowym lub pomijanie zleceń o budżetach < 500 PLN.
2. **Technologie o Stabilnym Wolumenie i Umiarkowanym Win Rate (Python, Laravel, Shopify, React, Scraping)**:
   - Wolumen od 20 do 45 zleceń, Win Rate 10–19%.
   - Główny chleb powszedni bota. Wymagają technicznego pytania diagnostycznego (Question CTA).
3. **Mobilne Technologie Natywne (Kotlin $n=22$ / WR 27.3%, Flutter $n=20$ / WR 20%)**:
   - Wyższy próg wejścia eliminuje konkurencję amatorską.
   - Bardzo dobra responsywność zleceniodawców.
4. **Nisze Mikro (TopSolid, VoIP, IdoSell, Enova365)**:
   - Bardzo wysoki Win Rate pozorny wynikający z $n \le 9$.
   - Traktowane jako okazje (Fast-Track), ale nie podstawa planowania przychodów.
