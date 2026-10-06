=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena: 8 000 – 12 000 zł netto** (umowa o dzieło)
**Czas: 15–25 dni roboczych** (3–5 tygodni, zależnie od wolumenu i liczby modułów)

**Uzasadnienie:** To nie upgrade 1-Click, tylko czysta instalacja PS 8.x + migracja danych — przy 1.6→8.x wymienia się szablon, moduły i framework (Symfony), więc 90% pracy to przenosiny i konfiguracja od zera, a nie kliknięcie „aktualizuj". Widełki wynikają głównie z nieznanej liczby modułów do zastąpienia i wolumenu danych — im więcej customowych integracji i kombinacji produktów, tym bliżej górnej granicy.

**Czego brakuje w zleceniu (wpływa na cenę/termin):**
1. **Lista aktywnych modułów i integracji** — które są krytyczne (płatności, wysyłki, faktury, marketing)? Część modułów 1.6 nie ma odpowiedników PS8 i trzeba je zastąpić lub dopisać.
2. **Wolumen danych** — liczba produktów, kombinacji, zdjęć, klientów, zamówień i rozmiar bazy. To bezpośrednio przekłada się na czas migracji i ryzyko limitów na stagingu.
3. **Czy szablon Warehouse był modyfikowany indywidualnie** (layout, checkout, funkcje)? Customizacje 1.6 nie przeniosą się 1:1 — trzeba je odtworzyć, co może dodać sporo godzin.
4. **Multistore / multijęzyk / multuwalutowość?** Zakładam standard jednojęzyczny, jedna waluta — jeśli inaczej, wycena w górę.
5. **Oczekiwane okno przełączenia na domenę główną** (np. noc/weekend) — wpływa na harmonogram.

Chętnie zrobię krótki audyt (2–3h) po dostępie do stagingu i wtedy podam kwotę wiążącą zamiast widełek.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 8–12 tys. są obronne, ale dolna granica jest ryzykowna — przy 90 zł/h to ~89 h, a sama migracja danych + BaseLinker + 301 przy customowych modułach może to zjeść. Realnie bezpieczniej zakotwiczyć się na 10–14 tys. netto, z 8 tys. tylko jako absolutne minimum przy małym, czystym sklepie. Nie zaniżyłem świadomie — brakuje mi trzech danych (moduły, wolumen, customizacje Warehouse), więc każda kwota poniżej 10 tys. to zgadywanie. Kwotę wiążącą i tak podam po 2–3h audytu, więc na razie trzymam górę widełek jako kotwicę.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna:** **6 000–11 000 zł** (na rękę, przy 90 zł/h; ok. 67–122 h).  
Dla standardowego zakresu bez multistore i dużych customów realnie: **7 000–10 000 zł**.

**Czas:** **70–120 h**, czyli **9–15 dni roboczych**; kalendarzowo **3–5 tygodni** zależnie od feedbacku i testów.

**Uzasadnienie:** 1.6 → 8.x to nie upgrade 1-Click, tylko czysta instalacja PS 8 + migracja danych, nowy szablon Warehouse, odpowiedniki modułów, BaseLinker i przekierowania 301. Najwięcej pracy i ryzyka siedzi w modułach, migracji bazy, testach oraz SEO.  

**Brakuje mi:** listy aktywnych modułów/integracji, wolumenu produktów/kombinacji/klientów/zamówień, informacji czy Warehouse był customizowany, oraz czy jest multistore/waluty/języki. Od tego może się zmienić wycena.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Wycena 7–10 tys. zł przy 90 zł/h jest uczciwa jako widełki, ale opiera się na założeniu „standardowego” zakresu, którego nie potwierdziłem — bez listy modułów i wolumenu danych to wciąż zgadywanie, nie kalkulacja. Realnie sama migracja danych + odtworzenie modułów + testy BaseLinkera + mapowanie 301 przy większym sklepie może zjeść 120–150 h, czyli 11–13,5 tys. zł, a przy customowym Warehouse i multistore jeszcze więcej. Nie zaniżyłem świadomie — po prostu brak danych o module i wolumenie jest na tyle istotny, że każda kwota poniżej 12 tys. zł jest obarczona ryzykiem straty. Korekta: trzymam 7–10 tys. jako dolną, warunkową wycenę, ale w ofercie wyraźnie piszę, że ostateczna cena zależy od odpowiedzi na 3 pytania i przy dużym wolumenie/customach wzrośnie do 12–15 tys. zł.

=== DeepSeek-C — RUNDA 1 ===
## Wycena

**Kwota:** 6 000 – 10 000 zł netto (przy 90 zł/h = ok. 65–110 h)
**Czas:** 12–20 dni roboczych od zebrania danych i dostępu do stagingu

**Uzasadnienie:**
To nie upgrade 1-Click, tylko czysta instalacja PS 8.x + migracja danych — inaczej się nie da przy 1.6→8.x. Najwięcej czasu zjada baza (produkty, kombinacje, zdjęcia, klienci, zamówienia), odtworzenie szablonu Warehouse na wersji PS8 (customizacje z 1.6 nie przenoszą się 1:1) oraz moduły i BaseLinker (oficjalny moduł + klucz WebService z pełnymi uprawnieniami). Widełki zależą głównie od wolumenu i liczby modułów do zastąpienia.

**Czego brakuje w zleceniu (do wyceny wiążącej):**
1. **Lista aktywnych modułów i integracji** — płatności, wysyłki, faktury, marketing; które są krytyczne po migracji? Bez tego nie ocenię, czy są odpowiedniki pod PS8.
2. **Czy szablon Warehouse był modyfikowany** (layout, checkout, funkcje) i czy są pliki/dokumentacja? Nowa wersja nie przeniesie customizacji 1:1.
3. **Wolumen danych** — liczba produktów, kombinacji, klientów, zamówień, rozmiar bazy i zdjęć.

Zakładam standard: jednojęzyczny, jedną walutę, bez multistore. Jeśli inaczej — dostroję wycenę.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: dolna granica 6 000 zł była optymistyczna. Przy pełnej migracji 1.6→8.x (staging, migracja bazy z kombinacjami i zdjęciami, odtworzenie customizacji Warehouse, wymiana modułów, BaseLinker z pełnym kluczem, mapowanie 301 z GSC, testy i bugfixy po go-live) realny zakres to raczej 100–150 h, nie 65. Przy 90 zł/h daje to **9 000–13 500 zł netto** jako uczciwe widełki, a nie 6 000–10 000. Nie zaniżyłem świadomie — po prostu wolumen i stan modułów są nieznane, więc dolna granica miała charakter „minimum przy bardzo lekkim sklepie”. Korekta: **8 000–14 000 zł netto**, z zastrzeżeniem, że do 8 000 zejdę tylko po potwierdzeniu małego wolumenu i braku customizacji szablonu.

=== DeepSeek-D — RUNDA 1 ===
**Wycena: 7 200 – 10 800 zł** (80–120 h × 90 zł/h)
**Czas: 15–25 dni roboczych**

**Uzasadnienie:**
To nie upgrade 1-Click, tylko czysta instalacja PS 8.x + migracja danych na stagingu, więc zakres obejmuje osobno: staging, migrację bazy (produkty/kombinacje/zdjęcia/klienci/zamówienia), nowy Warehouse pod PS 8, odpowiedniki modułów, BaseLinker (oficjalny moduł + klucz WebService z pełnymi uprawnieniami) oraz mapowanie 301 z GSC. Kluczowe ryzyko: 90% modułów 1.6 nie przenosi się 1:1, a customizacje szablonu trzeba odtworzyć — stąd szerokie widelki.

**Czego brakuje do doprecyzowania ceny:**
1. **Lista aktywnych modułów/integracji** i które są krytyczne po migracji (płatności, wysyłki, faktury, marketing, BaseLinker).
2. **Wolumen danych**: liczba produktów, kombinacji, klientów, zamówień, rozmiar bazy i zdjęć.
3. **Czy szablon Warehouse był modyfikowany indywidualnie** i czy są pliki/dokumentacja — nowa wersja nie przeniesie customizacji 1:1.

Po odpowiedziach na te 3 punkty zawężę wycenę do konkretnej kwoty.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena jest uczciwa i raczej po dolnej granicy rynku — 80–120 h na 1.6→8.x z migracją danych, odtworzeniem szablonu, mapowaniem modułów, BaseLinkerem i 301 to realistyczny zakres, nie zaniżony na siłę.

Nie zgadłem na siłę niczego — widełki są szerokie właśnie dlatego, że brakuje trzech danych: listy modułów, wolumenu i zakresu customizacji Warehouse. Jeśli okaże się, że są płatności/wysyłki/faktury do przepisania, multistore, wiele języków/walut albo głębokie modyfikacje szablonu, kwota idzie w górę (nawet 12–15 tys. zł), a nie w dół.

Jeśli nic takiego nie wyjdzie — 7,2–9 tys. zł jest realne. Kwoty nie koryguję teraz, bo korekta bez odpowiedzi klienta byłaby wróżeniem; zawężam po jego trzech odpowiedziach.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 8000,
  "kwota_gorna": 14000,
  "definitywna": false,
  "od_czego_zaleza": [
    "lista aktywnych modułów i integracji oraz ich krytyczność po migracji",
    "wolumen danych: liczba produktów, kombinacji, zdjęć, klientów, zamówień i rozmiar bazy",
    "zakres customizacji szablonu Warehouse i dostępność plików lub dokumentacji",
    "multistore, liczba języków i walut",
    "oczekiwane okno wdrożenia oraz zakres testów po go-live"
  ],
  "dni_od": 15,
  "dni_do": 25,
  "uzasadnienie": "Wszystkie modele zgodnie uznały, że to nie upgrade 1-Click, lecz czysta instalacja PS 8.x z migracją danych, stagingiem, wymianą modułów, BaseLinkerem i mapowaniem 301. Po autokrytyce rozbieżność dotyczyła głównie dolnej granicy: 6-8 tys. zł uznano za ryzykowne, a bezpieczniejsze widełki przesunęły się w stronę 8-14 tys. zł netto. Rozbieżność wynika z braku danych o modułach, wolumenie i customizacjach szablonu, więc wycena musi pozostać warunkowa. 8 tys. zł jest realne tylko przy małym, czystym sklepie i prostych integracjach, a 14 tys. zł przy większym wolumenie, customach lub multistore."
}

=== FINALNA WYCENA ===
8000-14000 zl netto | 15-25 dni | WIDELKI
Od czego zalezy: lista aktywnych modułów i integracji oraz ich krytyczność po migracji, wolumen danych: liczba produktów, kombinacji, zdjęć, klientów, zamówień i rozmiar bazy, zakres customizacji szablonu Warehouse i dostępność plików lub dokumentacji, multistore, liczba języków i walut, oczekiwane okno wdrożenia oraz zakres testów po go-live
Uzasadnienie rozjemcy: Wszystkie modele zgodnie uznały, że to nie upgrade 1-Click, lecz czysta instalacja PS 8.x z migracją danych, stagingiem, wymianą modułów, BaseLinkerem i mapowaniem 301. Po autokrytyce rozbieżność dotyczyła głównie dolnej granicy: 6-8 tys. zł uznano za ryzykowne, a bezpieczniejsze widełki przesunęły się w stronę 8-14 tys. zł netto. Rozbieżność wynika z braku danych o modułach, wolumenie i customizacjach szablonu, więc wycena musi pozostać warunkowa. 8 tys. zł jest realne tylko przy małym, czystym sklepie i prostych integracjach, a 14 tys. zł przy większym wolumenie, customach lub multistore.
