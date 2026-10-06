# 📊 DRUGA ANALIZA — Ocena przepływu AI i realizmu wycen
# Data: 2026-10-05
# Źródło: zewnętrzna recenzja (nie benchmark rynkowy, ocena z doświadczenia)
# Zakres: 34 pliki

============================================================
## WERDYKT OGÓLNY
============================================================

- Realistyczne (±20%): ~20 z 34 — głównie małe/średnie projekty WP, Shopify, integracje do ~10 tys. zł
  (np. #2523916, #2523493, #2638274, #2646530, #2709431, #2797272, #2871273, #2735493)
  #2624700 (35–50 tys.) też dobrze trafiony — arbiter słusznie odrzucił najniższy głos.
- Zaniżone: ~9 — im większy lub bardziej specjalistyczny projekt, tym większe zaniżenie.
- Zbyt szerokie, żeby coś znaczyły: 3 (#2546694, #2630208, #2559405)
- Definitywnych wycen: 0 z 34 — PROBLEM PROJEKTOWY, bo część zleceń jest dobrze zdefiniowana
  (np. #2797272, #2896683)

============================================================
## SZCZEGÓŁOWA TABELA ROZBIEŻNOŚCI
============================================================

| Zlecenie | Final bota | Ocena recenzenta | Powód |
|----------|-----------|-----------------|-------|
| #2543830 Konsultacja AI/OCR | 600–800 | Zaniżone ~3× (1,5–3 tys.) | Etap 03 wyszedł na 1200–1500, rada zbiła do 600–800 przez "klient porówna z rynkiem". Wycenia się tu wiedzę, nie godziny. |
| #2705780 Bilety MVP | 35–50 tys. | Zaniżone (45–65 tys.) | Marketplace PSP, KYC, zwroty, PWA check-in, panel admina i e-maile. Dwa modele dawały 40–55 tys. |
| #2628151 PWA + Supabase | 20–28 tys. | Zaniżone (26–36 tys. za pełny zakres) | Rada sama napisała, że pełny zakres to 260–400 h. Dolne 20 tys. dotyczyło okrojonego MVP, a oferta sprzedaje je jako pełny zakres. |
| #2526974 Portal Wiedeń | 8–12 tys. | Zaniżone (12–18 tys.) | Nowy design, UGC, i18n, CMP/TCF, Impressum, AdSense, newsletter. Plus niewspomniane licencje wtyczek The Events Calendar/Community Events. |
| #2868640 Strona TSL | 15–22 tys. | Zaniżone (20–28 tys.) | Premium UX/UI i identyfikacja od zera, własny motyw, mapa, HubSpot, PL/EN. |
| #2630780 Squarespace | 4–4,5 tys. | Zaniżone (5–6 tys.) | Model C sam policzył 60–70 h, a potem zszedł do 4300, bo "górna granica Twojego budżetu". |
| #2521698 CRM Power Apps | 14–22 tys. | Dolna za niska | Agregacja maili przez Graph, dopasowanie do klientów, Dataverse, role, traceability. |
| #2566145 Presta 1.6→8 | 8–14 tys. | Dolna za niska (10–16 tys.) | Moduły, szablon, migracja i 301 bez znanego wolumenu. |
| #2551600 n8n | 18–30 tys. | Górna za niska | Dwa modele dawały 36–40 tys. |
| #2546694 Scraper APK | 4,5–12 tys. | Szerokość 2,7× | Dla klienta bezużyteczne bez wariantów. |
| #2630208 Strona/sklep | 5,5–22 tys. | Szerokość 4× | Dwa osobne produkty w jednym przedziale. Oferta słusznie dzieli to na prezentacyjną i sklep. |

============================================================
## STRUKTURALNE PRZYCZYNY SŁABEJ WYCENY
============================================================

### 1. Jedna stawka 90 zł/h dla wszystkiego
Konsulting AI, Java/Spring i offline PWA dostają tę samą stawkę co Divi.
Model B w #2628151 sam pisze, że to "niskie dla Java+React".
Przy konsultingu cennik godzinowy w ogóle nie oddaje wartości.

### 2. Cztery razy ten sam model
Rozrzut między głosami to często 2–4×:
- #2546694: 2,2–22 tys.
- #2526974: 6–18 tys.
- #2630208: 3,6–36 tys.
To sygnał niskiej pewności, który arbiter zamienia w gładki przedział i ukrywa.

### 3. Autokrytyka pyta o złą rzecz
Runda 2 sprawdza "czy nie zgadłeś" (treść oferty), a nie przelicza zadań od zera.
Efekt: ruch w losową stronę. Rada często "koryguje" w górę lub w dół bez nowej rozpiski godzin.

### 4. Kotwiczenie na budżecie klienta
Modele dostają budżet i się do niego dopasowują.
Przykład: "trzymam górną granicę Twojego budżetu" w #2630780.
Estymacja i strategia cenowa powinny być rozdzielone.

### 5. Brak kalibracji na faktycznych godzinach
Nikt nie sprawdza, ile podobne projekty zajęły naprawdę.
Brakuje narzutu na komunikację i poprawki.
Brakuje bufora ryzyka dla ceny stałej.

============================================================
## CICHY DRYF LICZB PO RADZIE
============================================================

Po arbitrze liczby zmieniają się bez śladu i prawie zawsze W DÓŁ:

### Zaokrąglanie dolnej granicy w dół:
- #2512751: z 3700–5200 na 3500–5000
- #2523916: z 3200–4200 na 3000–4000
- #2581512: z 2700 na 2500

### Składniki oferty niższe niż składniki rady:
- #2512751: LP 2600–3400 (rada 2700–3800), Ads 900–1600 (rada 1200–1600)

### Rozjazd między rekordem a arbitrem:
- #2630054: arbiter dał 270–360 zł i 1–3 dni, w rekordzie jest 500–500 zł i 7–7 dni.
  Uzasadnienie opisuje inne liczby niż rekord.

### Podłoga 7 dni:
Wycena 2–5 dni (#2646530, #2638274, #2709431) ląduje jako "7-7", a oferta pisze "5–7" lub "3–5".

### Literówka w kluczu:
`od_czego_zalea` w #2543798 dała pustą listę zależności. Nikt tego nie walidował.

### Zagubiony etap:
"uwaga_etap1" w #2551600 (moduł 2700–3200 zł) nie trafia do rekordu.
Oferta mówi, że moduł "mieści się w budżecie 2890", choć widełki rady i głos B (3000–4000) temu przeczą.

### Niespójność jednostek:
- #2896683: 20–30 dni, a oferta pisze 3–4 tygodnie (kalendarzowo)
- #2871300: 14–25 dni, a oferta pisze 3–5 tygodni (robocze)

### Netto vs brutto:
Klienci piszą "brutto" (#2628151, #2630780), a oferty są w netto. Nic tego nie normalizuje.

============================================================
## PĘTLA VETO PSUJE WYCENY I FAKTY
============================================================

Sędzia często dopisuje fakty spoza ogłoszenia, a potem przepisywanie traktuje je jako prawdę:

### Wymyślone budżety:
- #2572013: sędzia wymyślił "budżet 5750 zł netto". Finalna oferta mówi klientowi
  "mieścisz się w swoim budżecie", choć w ogłoszeniu jest "Do negocjacji".

### Wymyślone wyceny:
- #2637922 i #2630780: sędzia wymyślił wycenę "900 zł / 7 dni" i nagłówek "4250".
  Weryfikacja fałszywych zarzutów zadziałała, ale kosztowała dwie rundy.

### Veto wymusza cenę poniżej kosztu:
- #2628174: oferta obiecuje za 500 zł projekt drzewa i mapę normalizacji (~5,5 h).
  Rada oceniła nawet sam etap 1 na 720–1200 zł. Veto wymusiło cenę poniżej kosztu.

### Fałszywe twierdzenia techniczne:
- #2628151: pytanie o HotPay recurring zamieniło się w twierdzenie
  "HotPay obsługuje płatności cykliczne". Research uznał to za niepotwierdzone,
  a weryfikacja oparła się na dokumentacji innego produktu (DCB).

### Checker nie blokuje:
- #2871300: checker zgłosił rozjazd 14 vs 25 dni i oferta i tak wyszła.
  Finalny tekst mówi "14 dni jest realne", choć rada uznała to za ryzykowne.
  Ostrzeżenie o Katalogu Allegro zredukowane do "nie zakładam, że odrzuci".
  Cena 10–15 tys. nadal zakłada pełne mapowanie Katalogu.

### Nieaktualne terminy:
- #2564064 i #2637922: oferty obiecują "ostatni tydzień kwietnia" i "do 15 maja",
  choć dziś jest październik 2026. Research w #2564064 sam zauważył, że termin minął.

============================================================
## REKOMENDACJE — W KOLEJNOŚCI WPŁYWU
============================================================

### 1. Rozpiska zadań zamiast jednej liczby
Każdy model zwraca tabelę zadań z godzinami, a sumę liczy kod.
Dodaj narzut 15–20% na komunikację i poprawki.
Dodaj osobny bufor ryzyka dla niewiadomych.

### 2. Stawka zależna od typu pracy
Osobne stawki dla:
- Standardowy development (WP, Shopify, proste integracje)
- Seniorski development (Java/Spring, PWA offline, systemy B2B)
- Konsulting (AI/OCR, architektura, doradztwo)
Konsulting wyceniaj za wartość, nie za godziny.

### 3. Kalibracja na twoich danych
Podaj 10–15 projektów z realnymi godzinami i licz mnożnik korygujący.

### 4. Estymacja bez budżetu klienta
Budżet widzi dopiero warstwa decyzji o strategii ceny — NIE modele estymujące.

### 5. Różne modele i niezależne rozpiski
Arbiter porównuje różnice zadań, a nie bierze mediany.
Do rekordu dodaj poziom pewności i rozrzut głosów.

### 6. Ceny stałe z założeniami (MVP vs pełny zakres)
Zamiast przedziałów 1,5–4×.
Tam, gdzie zakres jest jasny, dawaj jedną liczbę.

### 7. Walidator po rundzie
Jedna liczba, jedna jednostka dni i netto/brutto we wszystkich polach.
Schemat JSON ze stałymi kluczami.
Checker ma BLOKOWAĆ wysyłkę, nie tylko zgłaszać.

### 8. Ograniczenia pętli veto
Sędzia NIE MOŻE wprowadzać faktów spoza ogłoszenia.
Przepisywanie NIE MOŻE zmieniać cen ani ustaleń z researchu, ani schodzić poniżej kosztu godzin z rady.
