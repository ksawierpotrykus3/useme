# Raport Inżynieryjny: Empiryczny Audyt 470 Zleceń na Useme

> **Data audytu:** 2026-09-25  
> **Próba badawcza:** 470 unikalnych zleceń z bazy `ksawierpotrykus3`  
> - 414 zleceń przegranych (`przegrane_pelne_416.json`)  
> - 56 zleceń wygranych / odpisanych z pełną historią wiadomości (`wygrane_56.json`)  
> **Średni bazowy Win Rate bazy:** 11.91% (56 / 470)

---

## 1. Weryfikacja Danych i Ostrzeżenie Statystyczne (Błąd Małych Liczb)

### ❌ Krytyka Mitologii „Złotych Strzałów”
Wcześniejsze próby ogłaszania „złotych strzałów” (np. 33% czy 50% Win Rate w wąskich segmentach) są **błędem małych liczb (Law of Small Numbers)**. 
Przy łącznej liczbie 56 wygranych rozbitych na 28 technologii i 5 typów klientów, większość komórek zawiera zaledwie $n = 2$ do $n = 12$ zleceń:
* **TopSolid / CAD:** 1 wygrana na 2 zlecenia = 50.0% ($n=2$, czysta anegdota).
* **VoIP / SIP:** 2 wygrane na 5 zleceń = 40.0% ($n=5$, błąd marginesu $\pm 35\%$).
* **IdoSell:** 3 wygrane na 9 zleceń = 33.3% ($n=9$, wahanie o 1 klienta zmienia wynik o 11 punktów procentowych).

**Wniosek metodologiczny:** Wszelkie wskaźniki dla $n < 15$ należy traktować jako **wstępne hipotezy badawcze o wysokiej wariancji**, a nie żelazne reguły konwersji.

### ✅ Co JEST Twardym Faktem Statystycznym?
1. **WordPress / WooCommerce to Czerwony Ocean ($n = 104$):**
   * Największy wolumen na Useme (22.1% wszystkich zleceń).
   * Zaledwie 7 wygranych = **6.7% Win Rate** (prawie połowa średniej rynkowej).
   * Twardy fakt: rynek zalany ofertami szablonowymi i agresywnym dumpingiem cenowym.
2. **Dominacja Klientów Nietechnicznych ($n = 237$):**
   * **50.4% całej bazy** stanowią zlecenia pisane przez właścicieli firm i managerów bez wykształcenia IT.
3. **100% Konwersji Dzieje Się na Priv:**
   * Wszystkie 56 wygranych zleceń przeszło przez fazę wiadomości prywatnych (wątki po 373, 173, 53 wiadomości). Żadne zlecenie nie zamknęło się bezpośrednio z samej oferty publicznej.

---

## 2. Twarde Metryki Porównawcze: Wygrane vs Przegrane

| Metryka | Wygrane (56) | Przegrane (414) | Delta Względna | Znaczenie Inżynieryjne |
|---|---:|---:|---:|---|
| **Question CTA (Pytanie diagnostyczne)** | **32.1%** | **25.4%** | **+26.4%** | **Główny czynnik konwersji na priv** |
| Call CTA („zdzwońmy się na 15 min”) | 33.9% | 35.7% | -5.0% | Przegrywa; budzi opór przed zobowiązaniem |
| Direct priv CTA („napisz na priv”) | 10.7% | 9.4% | +13.8% | Słabe samo w sobie (musi wynikać z pytania) |
| Średnia liczba słów | 193.4 | 187.7 | +3.0% | Długość jest neutralna (~190 słów to standard) |
| Gęstość technologiczna (Tech Density) | 1.8 | 1.6 | +12.5% | Precyzja terminologii lekko podbija autorytet |
| Mediana ceny ofertowej | 3 300 zł | 3 500 zł | -5.7% | Różnica pomijalna; cena nie jest głównym filtrem |
| Średni deklarowany czas | 15.4 dni | 15.7 dni | -1.9% | Brak wpływu na decyzję klienta |

---

## 3. Rzeczywisty Rozkład Technologiczny (Pełny Granularny Skan)

Skan regexowy wszystkich 470 zleceń pod kątem 28 konkretnych technologii wykazał następujący rozkład:

| Granularna Technologia | Liczba Zleceń ($n$) | Wygrane | Win Rate | Istotność Próby |
|---|---:|---:|---:|---|
| **WordPress / WooCommerce** | 104 | 7 | 6.7% | Bardzo wysoka ($n>100$) |
| **Laravel / PHP** | 44 | 5 | 11.4% | Wysoka ($n>40$) |
| **Shopify / Liquid** | 31 | 4 | 12.9% | Średnia |
| **React / Next.js** | 30 | 3 | 10.0% | Średnia |
| **Python / Django / FastAPI** | 27 | 5 | 18.5% | Średnia |
| **DevOps / Docker / VPS** | 27 | 3 | 11.1% | Średnia |
| **Bazy danych / SQL** | 27 | 2 | 7.4% | Średnia |
| **Make / n8n / Zapier** | 26 | 1 | 3.8% | Średnia (niska skuteczność) |
| **Computer Vision / OCR / AI** | 24 | 2 | 8.3% | Średnia |
| **PrestaShop** | 23 | 3 | 13.0% | Średnia |
| **Kotlin / Android native** | 22 | 6 | 27.3% | Średnia ($n=22$) |
| **Swift / iOS native** | 20 | 4 | 20.0% | Średnia ($n=20$) |
| **BaseLinker** | 20 | 1 | 5.0% | Średnia |
| **Node.js / Express / Nest** | 16 | 1 | 6.2% | Niska |
| **Scraping (Selenium/Playwright/Bs4)** | 14 | 3 | 21.4% | Niska |
| **Figma / UI design** | 13 | 2 | 15.4% | Niska |
| **Shoper** | 10 | 1 | 10.0% | Niska |
| **Framer / Webflow** | 10 | 1 | 10.0% | Niska |
| **IdoSell (IAI)** | 9 | 3 | 33.3% | Bardzo niska (wysoka wariancja) |
| **Subiekt (GT / nexo / Sfera)** | 8 | 1 | 12.5% | Bardzo niska |
| **Enova365** | 7 | 2 | 28.6% | Bardzo niska |
| **Flutter / Dart** | 7 | 0 | 0.0% | Bardzo niska |
| **Vue / Nuxt** | 6 | 1 | 16.7% | Bardzo niska |
| **.NET / C#** | 6 | 0 | 0.0% | Bardzo niska |
| **VoIP / Asterisk / SIP** | 5 | 2 | 40.0% | Bardzo niska |
| **Comarch (Optima / XL)** | 4 | 0 | 0.0% | Bardzo niska |
| **React Native** | 3 | 0 | 0.0% | Bardzo niska |
| **TopSolid / CAD / CAM** | 2 | 1 | 50.0% | Czysto anegdotyczna ($n=2$) |

---

## 4. Odkrycie Kluczowe: 155 Zleceń (33.0% Rynku) Bez Podanej Technologii

Aż **155 na 470 zleceń** w tytule i opisie **nie zawiera żadnej konkretnej nazwy technologii**.
Z tej puli wygrano **17 zleceń** (Win Rate: **11.0%**), co stanowi **30.4% wszystkich Twoich wygranych**.

### Przykłady wygranych zleceń bez podanej technologii:
* **14 000 zł** – *MVP aplikacji webowej do screeningu danych względem list referencyjnych*
* **8 500 zł** – *Wykonanie UI bota do przenoszenia danych z portalu do Wapro*
* **7 000 zł** – *Aplikacja mobilna ogłoszenia (w stylu TikTok)*
* **6 500 zł** – *Testy ABCDE i integracja z istniejącą platformą edukacyjną*
* **6 500 zł** – *Rozwój projektu zbudowanego w Bubble*
* **4 200 zł** – *Wykonanie połączenia oprogramowania PMS (recepcji hotelu) z Booking.com*
* **3 500 zł** – *System rezerwacji terminów dla psychologów*
* **3 300 zł** – *Zlecę analizę forensic dysku systemowego Windows (serwer)*
* **2 500 zł** – *Zlecenie: Automatyzacja testu online (quiz diagnostyczny dla liderów)*
* **2 500 zł** – *Automatyzacja pozyskiwania partnerów z Google Maps*
* **2 400 zł** – *Bitrix - wdrożenie*
* **2 300 zł** – *Airtable Consultancy*
* **1 500 zł** – *Stworzenie arkusza kalkulacyjnego do tworzenia kosztorysów*
* **1 200 zł** – *Usunięcie danych posprzedażowych z zewnętrznych serwisów internetowych*
* **600 zł** – *Audyt strony + poprawa UX*
* **400 zł** – *Szybka akcja gangsters.pl (skrypt do gry)*
* **400 zł** – *Walka z bossem pokewars (skrypt do gry)*

### Strategiczny Wniosek: Dwie Równoległe Ścieżki
Rynek Useme dzieli się na dwa zupełnie odmienne światy:
1. **Ścieżka Technologiczna (67% rynku):**
   * Klient podaje stack (np. *„Szukam programisty Laravel 10 / Vue 3”*).
   * Strategia: precyzja inżynierska, wersje bibliotek, zapytania o architekturę i repozytorium.
2. **Ścieżka Wynikowa / Problemowa (33% rynku):**
   * Klient nie wie, czym to zrobić (chce leadów, arkusza, MVP, bota do gry, rezerwacji terminów).
   * Strategia: zero żargonu, propozycja najprostszego i najtańszego narzędzia pod jego cel biznesowy.

---

## 5. Podsumowanie Wdrożeniowe do Silnika

1. **Wyeliminować sztuczne 6 worków:** Zastąpić je granularnym katalogiem 28 technologii oraz flagą `IS_TECH_AGNOSTIC`.
2. **Usunąć pojęcie „złotych strzałów”:** W generatorach nie wolno zakładać, że niszowe technologie gwarantują wygraną.
3. **Wdrożyć Question CTA dopasowane do ścieżki:**
   * Jeśli zlecenie ma stack -> pytanie o architekturę / wersję API.
   * Jeśli zlecenie jest bez stacku -> pytanie o format danych wejściowych i cel biznesowy.