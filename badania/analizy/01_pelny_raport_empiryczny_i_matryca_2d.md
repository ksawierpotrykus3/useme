# Raport Inżynieryjny: Empiryczny Audyt 481 Zleceń na Useme (Stan po Synchronizacji)

> **Data aktualizacji:** 2026-09-28  
> **Próba badawcza:** **481 unikalnych zakończonych zleceń** z bazy `ksawierpotrykus3` (po dograniu 11 nowo zamkniętych ofert):  
> - **425 zleceń przegranych / nieodpisanych** ([`przegrane_pelne.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json) / `przegrane_pelne_416.json`)  
> - **56 zleceń wygranych / odpisanych** z pełną historią wiadomości ([`wygrane.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/03_odpisane/wygrane.json) / `wygrane_56.json`)  
> - Dodatkowo w `01_ofertowarka` zweryfikowano statusy 180 zleceń bota: **25 oznaczono jako `ZAMKNIETE_NIEODPISANE`** (pewna porażka), a **79 pozostaje w statusie `WYSLANO`** (w toku).  
> **Średni bazowy Win Rate bazy:** **11.64% (56 / 481)** *(wcześniej 11.91% przy N=470)*

---

## 1. Weryfikacja Danych i Ostrzeżenie Statystyczne (Błąd Małych Liczb)

### ❌ Krytyka Mitologii „Złotych Strzałów”
Wcześniejsze próby ogłaszania „złotych strzałów” (np. 33% czy 50% Win Rate w wąskich segmentach) są **błędem małych liczb (Law of Small Numbers)**.  
Przy łącznej liczbie 56 wygranych rozbitych na 28 technologii i 5 typów klientów, większość komórek zawiera zaledwie $n = 2$ do $n = 12$ zleceń:
* **TopSolid / CAD:** 1 wygrana na 2 zlecenia = 50.0% ($n=2$, czysta anegdota).
* **VoIP / SIP:** 2 wygrane na 5 zleceń = 40.0% ($n=5$, błąd marginesu $\pm 35\%$).
* **IdoSell:** 3 wygrane na 9 zleceń = 33.3% ($n=9$, wahanie o 1 klienta zmienia wynik o 11 punktów procentowych).

**Wniosek metodologiczny:** Wszelkie wskaźniki dla $n < 15$ należy traktować jako **wstępne hipotezy badawcze o wysokiej wariancji**, a nie żelazne reguły konwersji.

### ✅ Co JEST Twardym Faktem Statystycznym (Potwierdzonym na N=481)?
1. **WordPress / WooCommerce to Czerwony Ocean ($n = 108$, wcześniej $104$):**
   * Największy wolumen na Useme (22.5% wszystkich zleceń).
   * Zaledwie 7 wygranych na 108 prób = **6.5% Win Rate** (4 z 11 nowo zamkniętych porażek z września 2026 to znowu WordPress/WooCommerce: `#2892997`, `#2887326`, `#2887209`, `#2865617`!).
   * Twardy fakt: rynek zalany ofertami szablonowymi (20–38 ofert na ogłoszenie) i agresywnym dumpingiem cenowym.
2. **Dominacja Klientów Nietechnicznych ($n = 245$, 50.9% bazy):**
   * Ponad połowę całej bazy stanowią zlecenia pisane przez właścicieli firm i managerów bez wykształcenia IT (`TYP_A_BIZNESMEN_NIETECHNICZNY`, Win Rate **11.8%**).
3. **100% Konwersji Dzieje Się na Priv:**
   * Wszystkie 56 wygranych zleceń przeszło przez fazę wiadomości prywatnych. Żadne zlecenie nie zamknęło się bezpośrednio z samej oferty publicznej.

---

## 2. Twarde Metryki Porównawcze: Wygrane (56) vs Przegrane (425)

| Metryka | Wygrane (56) | Przegrane (425) | Delta Względna | Znaczenie Inżynieryjne |
|---|---:|---:|---:|---|
| **Question CTA (Pytanie diagnostyczne)** | **32.1%** | **24.9%** | **+28.9%** | **Główny czynnik konwersji na priv (delta wzrosła po dodaniu 11 porażek!)** |
| Call CTA („zdzwońmy się na 15 min”) | 33.9% | 36.7% | -7.6% | Przegrywa; budzi opór przed zobowiązaniem |
| Artifact CTA (link / próbka / screen) | 35.7% | 35.1% | +1.7% | Neutralne bez dopasowanego kontekstu |
| Direct priv CTA („napisz na priv”) | 10.7% | 10.8% | -0.9% | Słabe samo w sobie (musi wynikać z pytania) |
| Średnia liczba słów | 193.4 | 191.7 | +0.9% | Długość ~190 słów jest optymalna (elaboraty >400 słów z v5 przegrywały) |
| Gęstość technologiczna (Tech Density) | 1.80 | 1.62 | +11.1% | Precyzja terminologii lekko podbija autorytet |
| Mediana ceny ofertowej | 3 300 zł | 3 500 zł | -5.7% | Różnica pomijalna; cena w środku widełek nie jest blokadą |
| Średni deklarowany czas | 15.4 dni | 15.9 dni | -3.1% | Brak wpływu na decyzję klienta |

---

## 3. Rzeczywisty Rozkład Technologiczny (Pełny Granularny Skan N=481)

Skan regexowy wszystkich **481 zleceń** pod kątem 28 konkretnych technologii wykazał następujący zaktualizowany rozkład:

| Granularna Technologia | Liczba Zleceń ($n$) | Wygrane | Win Rate | Istotność Próby |
|---|---:|---:|---:|---|
| **WordPress / WooCommerce** | 108 | 7 | **6.5%** | Bardzo wysoka ($n>100$) — Czerwony Ocean |
| **Laravel / PHP** | 46 | 5 | **10.9%** | Wysoka ($n>40$) |
| **Shopify / Liquid** | 31 | 4 | **12.9%** | Średnia |
| **React / Next.js** | 30 | 3 | **10.0%** | Średnia |
| **Python / Django / FastAPI** | 28 | 5 | **17.9%** | Średnia |
| **Bazy danych / SQL** | 28 | 2 | **7.1%** | Średnia |
| **DevOps / Docker / VPS** | 27 | 3 | **11.1%** | Średnia |
| **Make / n8n / Zapier** | 26 | 1 | **3.8%** | Średnia (niska skuteczność w starym stylu) |
| **Computer Vision / OCR / AI** | 24 | 2 | **8.3%** | Średnia |
| **PrestaShop** | 24 | 3 | **12.5%** | Średnia |
| **Kotlin / Android native** | 22 | 6 | **27.3%** | Średnia ($n=22$) |
| **Swift / iOS native** | 20 | 4 | **20.0%** | Średnia ($n=20$) |
| **BaseLinker** | 21 | 1 | **4.8%** | Średnia |
| **Node.js / Express / Nest** | 17 | 1 | **5.9%** | Średnia |
| **Scraping (Selenium/Playwright/Bs4)** | 14 | 3 | **21.4%** | Niska |
| **Figma / UI design** | 13 | 2 | **15.4%** | Niska |
| **Shoper** | 10 | 1 | **10.0%** | Niska |
| **Framer / Webflow** | 10 | 1 | **10.0%** | Niska |
| **IdoSell (IAI)** | 9 | 3 | **33.3%** | Bardzo niska (wysoka wariancja) |
| **Subiekt (GT / nexo / Sfera)** | 9 | 1 | **11.1%** | Bardzo niska |
| **Enova365** | 7 | 2 | **28.6%** | Bardzo niska |
| **Flutter / Dart** | 7 | 0 | **0.0%** | Bardzo niska |
| **Vue / Nuxt** | 6 | 1 | **16.7%** | Bardzo niska |
| **.NET / C#** | 6 | 0 | **0.0%** | Bardzo niska |
| **VoIP / Asterisk / SIP** | 5 | 2 | **40.0%** | Bardzo niska |
| **Comarch (Optima / XL)** | 5 | 0 | **0.0%** | Bardzo niska (doszło `#2868642`) |
| **React Native** | 3 | 0 | **0.0%** | Bardzo niska |
| **TopSolid / CAD / CAM** | 2 | 1 | **50.0%** | Czysto anegdotyczna ($n=2$) |

---

## 4. Rynek Bez Podanej Technologii (Unmatched): 158 Zleceń (32.8% Rynku)

Aż **158 na 481 zleceń (32.8%)** w tytule i opisie **nie zawiera żadnej konkretnej nazwy technologii**.  
Z tej puli wygrano **17 zleceń** (Win Rate: **10.8%**), co stanowi **30.4% wszystkich wygranych**.

---

## 5. Macierz 2D: Typ Klienta × Archetyp Technologiczny (N=481)

### Rozkład według Typu Klienta:
- **`TYP_A_BIZNESMEN_NIETECHNICZNY`:** 245 zleceń | 29 wygranych | **11.8% Win Rate**
- **`TYP_C_ECOMMERCE_MANAGER`:** 96 zleceń | 10 wygranych | **10.4% Win Rate**
- **`TYP_D_STARTUPOWIEC_MVP`:** 51 zleceń | 6 wygranych | **11.8% Win Rate**
- **`TYP_B_TECH_LEAD_CTO_PM`:** 46 zleceń | 6 wygranych | **13.0% Win Rate**
- **`TYP_E_QUICK_FIX`:** 43 zlecenia | 5 wygranych | **11.6% Win Rate**

### Rozkład według Archetypu Technologicznego:
- **`TECH_3_ECOMMERCE_CMS`:** 162 zlecenia | 15 wygranych | **9.3% Win Rate**
- **`TECH_2_AUTOMATYZACJE_BOTY_SCRAPING`:** 115 zleceń | 15 wygranych | **13.0% Win Rate**
- **`TECH_6_LEGACY_INNE`:** 96 zleceń | 11 wygranych | **11.5% Win Rate**
- **`TECH_1_ERP_CAD_SYSTEMY`:** 54 zlecenia | 6 wygranych | **11.1% Win Rate**
- **`TECH_5_WEB_APPS_SAAS`:** 30 zleceń | 3 wygrane | **10.0% Win Rate**
- **`TECH_4_MOBILE_APPS`:** 24 zlecenia | 6 wygranych | **25.0% Win Rate**

Pełna Sekcja Porażek (Failure Alchemy) dla 11 nowo zamkniętych ofert jest generowana dynamicznie skryptem `kod/narzedzia_badawcze/swiat_2_wykonawca/sekcja_porazek_ai.py` do pliku `badania/analizy/RAPORT_SEKCJA_PORAZEK_OFERTOWARKI.md` (plik powstaje po uruchomieniu skryptu).