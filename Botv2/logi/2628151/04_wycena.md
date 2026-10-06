=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**1. Stos i obsługa offline**

PWA kierowcy: **React + Workbox** (uzasadnienie: dojrzały ekosystem service workerów, `workbox-background-sync` z gotową kolejką IndexedDB, najlepsze wsparcie dla Web Push i Background Sync). Dashboard dyspozytora: **Next.js + Supabase** — ten sam backend, spójny typ, mniej pracy. Backend: Supabase zgodnie z wymogiem — PostgreSQL + Auth + Storage + Edge Functions, RLS per `org_id`, JWT custom claims (`org_id`, `role`), role: Super-Admin / Właściciel / Dyspozytor / Kierowca.

Przepływ offline (4 kroki):
1. Zdjęcie z aparatu → `OffscreenCanvas`/Web Canvas, iteracyjne `toBlob(..., quality)` aż do <500 KB przy `maxWidth` 1600 px (czytelność kwitu zachowana).
2. Blob → IndexedDB (bezpośrednio, bez base64). Rekord formularza + blob w tej samej transakcji.
3. Kolejka `workbox-background-sync` z deduplikacją po `uuid` rekordu (odporna na wielokrotne wywołania sync).
4. Sync: **Android/Chromium** — Background Sync + Periodic Background Sync (po instalacji PWA). **iOS/Safari** — Safari nie ma Background Sync API i czyści IndexedDB po 7 dniach braku interakcji dla nie-zainstalowanych PWA, więc na iOS sync odpala się automatycznie przy starcie PWA (`visibilitychange` + `online`) plus Web Push jako wybudzacz. **Instalacja PWA na ekranie głównym = twardy warunek onboardingu kierowcy** (bez tego nie gwarantuję trwałości danych offline na iOS). Web Push i Periodic Sync wymagają instalacji PWA także na Chromium — dlatego to jeden warunek dla wszystkich.

**2. Portfolio Offline/Supabase**

[TU WPISZ 1-2 LINKI DO WŁASNYCH PROJEKTÓW — najlepiej z widocznym offline-first, IndexedDB/Service Worker i/lub Supabase + RLS]

**3. Termin startu**

[TU WPISZ KONKRETNĄ DATĘ, np. „mogę wystartować 15.11.2025"]

---

**Pytanie do zleceniodawcy:** Czy używany przez Państwa HotPay obsługuje płatności cykliczne (recurring/subskrypcje), czy wyłącznie jednorazowe (BLIK, szybki przelew)? Od tego zależy architektura modułu B2B — przy braku recurring buduję harmonogram (cron + przypomnienia) po naszej stronie i aktywację konta przez webhook po każdej opłacie; przy recurring webhook subskrypcji wystarcza. Fakturownię podpinam przez External REST API (sandbox dostępny) — potwierdzam integrację wystawiania, wysyłki i archiwum PDF w panelu właściciela.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: te 20 000 PLN fixed to kwota poniżej realnej pracochłonności tego zakresu — przy 90 zł/h daje to ok. 222 h, a sam multi-tenant z RLS + offline PWA + PDF z miniaturami + HotPay + Fakturownia to realnie 280–400 h, więc wychodzi ~63–71 zł/h i nie zgadzam się pracować poniżej stawki, chyba że klient zgodzi się na rozbicie zakresu (np. MVP bez modułu faktur i PDF-a w transzy 1) albo na podniesienie budżetu do 28–32 tys. przy tym samym zakresie.

Nie zgadłem na siłę dwóch rzeczy: klauzula o iOS (brak Background Sync + 7-dniowe ITP) jest bezpośrednią odpowiedzią na „całkowicie w tle, bez klikania" i „zdjęcia w IndexedDB", a pytanie o HotPay recurring rozstrzyga architekturę modułu B2B, więc obie są merytoryczne, nie wypełniaczem.

Placeholdery [linki portfolio] i [data startu] zostawiłem świadomie — to Twoje dane, nie moje zgadywanie; bez nich zgłoszenie nie spełnia wymogu „3 punkty" klienta.

Korekta: jeśli trzymamy się sztywno 20k, to punkt 1 zgłoszenia powinien jasno zaznaczyć, co wchodzi w MVP, a co jest poza zakresem (np. Fakturownia webhooki tylko przy update faktury, brak własnego KSeF) — inaczej po podpisaniu umowy będzie spór o zakres przy tej samej cenie.

=== DeepSeek-B — RUNDA 1 ===
**Kwota:** 20 000 PLN brutto — akceptowalne, ale to dolna granica. Uczciwie: **22 000–24 000 PLN** byłoby bezpieczniejsze. Przy 90 zł/h i 8–10 tyg. daje to ~222 h (22–28 h/tyg.).

**Czas:** 8–10 tygodni — realne, zgodnie z briefem.

**Uzasadnienie:** Zakres jest duży jak na 20k (multi-tenant + RLS + offline PWA z kompresją zdjęć + HotPay + Fakturownia + generator PDF z miniaturami), ale 222 h jest wykonalne przy zamkniętym zakresie i braku przeróbek. Dwa twarde ryzyka techniczne: Safari/iOS **nie ma Background Sync API** (trzeba dual-path: Android = Background Sync, iOS = auto-sync przy starcie PWA), a Safari **czyści IndexedDB po 7 dniach** dla niezainstalowanych PWA — instalacja PWA na ekranie głównym kierowcy to warunek konieczny, nie opcja.

**Czego brakuje w zleceniu:**
1. **HotPay — obsługuje płatności cykliczne (recurring/subskrypcje), czy tylko jednorazowe (BLIK, szybki przelew)?** Od tego zależy architektura modułu B2B: recurring = webhook przedłuża subskrypcję, one-off = cron + przypomnienia po naszej stronie. To zmienia zakres, więc pytam przed wyceną.
2. Jakich urządzeń używają kierowcy — iOS, Android, mix? Wpływa na to, czy „tło bez klikania" da się zrealizować dosłownie.
3. Czy są makiety UI dashboardu, czy projektujemy od zera?

Jak potwierdzisz punkt 1 i urządzenia — mogę dać wiążącą wycenę i termin startu.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: 20k przy 90 zł/h to ~222 h i to jest realne tylko przy zamkniętym zakresie i zero przeróbek — gdyby klient chciał negocjować, broniłbym 22–24k, ale skoro budżet jest fixed, przyjmuję 20k jako świadomą decyzję, nie „dobrą cenę". Wycena nie jest zaniżona z ostrożności — jest na dolnej granicy przez dwa niewiadome: czy HotPay ma recurring (jeśli nie, dochodzi cron + przypomnienia po naszej stronie) i czy Fakturownia ma gotowe sandbox/API w dniu startu. W researchu wróciły dwie rzeczy, które dziennik świadomie wyciął: webhooki Fakturowni (klient ich nie wymagał, tylko HotPay) i pytania o iOS/Android oraz Web Push (dziennik kazał nie pytać, research pyta) — to niespójność, do wyrzucenia ze zgłoszenia, zostaje jedno pytanie o HotPay recurring. Nie zgadywałem frameworka — SvelteKit po obu stronach to moja realna rekomendacja, nie wymuszona pod tezę. Kwoty nie koryguję w górę, bo fixed-price = albo akceptuję 20k z tymi ryzykami, albo odrzucam — a przy tym bólu klienta (gubione kwity = realne straty) 20k jest do przyjęcia.

=== DeepSeek-C — RUNDA 1 ===
**Wycena: 20 000 zł brutto jest realne, ale tylko przy twardym zamknięciu zakresu — inaczej 24 000–26 000 zł.**

**Czas: 10–12 tygodni (50–60 dni roboczych).** Nie 8–10 — brief jest gęsty, a Ty jesteś solo dev, nie agencja.

**Dlaczego:**
- 20 000 zł / 90 zł/h = ~222 h. To wystarczy na MVP, ale nie na „bezawaryjnie w trudnych warunkach terenowych" + pełną obsługę iOS/Android bez buforu na poprawki.
- Offline-first PWA z kolejką, dedup, kompresją <500 KB i dual-path sync (Android Background Sync vs. iOS auto-sync + Web Push) to sam w sobie 60–80 h.
- Multi-tenant RLS + JWT custom claims + 4 role + dashboard z PDF + HotPay + Fakturownia = drugie tyle.

**Czego brakuje w zleceniu — muszę wiedzieć przed startem:**
1. **HotPay — czy obsługuje płatności cykliczne (recurring)?** Od tego zależy, czy buduję webhook aktywacyjny, czy harmonogram cron + przypomnienia. To zmienia architekturę modułu B2B.
2. **Jakich telefonów używają kierowcy — iOS, Android, mix?** Jeśli iOS, wymóg „całkowicie w tle, bez klikania" jest niewykonalny (Safari nie ma Background Sync API) i wymuszam instalację PWA na ekranie głównym jako warunek onboardingu — inaczej iOS usunie IndexedDB po 7 dniach bez interakcji i kwity znikną.
3. **Czy są makiety dashboardu, czy projektuję UI od zera?** To 15–20 h różnicy.

Jeśli 20 000 zł jest sztywne, wchodzę — ale z zakresem ograniczonym do MVP i jasnym „co nie wchodzi" (np. bez Fakturowni w v1, bez makiety custom dashboardu). Bez tego buforu nie podpisuję fixed-price.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: 20 000 zł przy 90 zł/h to ~222 h, a sam offline-first z dual-path sync, RLS z JWT claims i PDF z miniaturami to realnie 260–300 h — więc cena jest na dolnej granicy i albo zamrażam zakres do MVP (bez Fakturowni w v1, bez custom dashboardu), albo odpuszczam, bo przy tej szerokości zlecenia robię to poniżej stawki. Nie zgadłem nic na siłę — mina o Fakturownia webhooks wyleciała jako nadinterpretacja, a iOS dual-path to nie domysł, tylko fakt (Safari bez SyncManager + 7-dniowe ITP), który wprost koliduje z wymogiem „całkowicie w tle, bez klikania". Pytanie o iOS/Android świadomie pominąłem, bo dual-path działa niezależnie od odpowiedzi; zostaje jedno realne pytanie — czy HotPay obsługuje recurring, bo to zmienia architekturę subskrypcji. Korekta: nie zmieniam kwoty w zgłoszeniu (budżet fixed, albo akceptuję, albo odrzucam), ale wchodzę tylko z pisemnym „co nie wchodzi w v1".

=== DeepSeek-D — RUNDA 1 ===
**Kwota:** 27 000–31 500 zł netto (300–350 h × 90 zł/h). Budżet 20 000 zł brutto pokrywa ~222 h — realnie o 80–130 h za mało.

**Czas:** 8–10 tygodni jest realne, ale tylko przy pełnym zakresie i założeniu, że nie ma po drodze zmian zakresu — co przy 4 transzach fixed-price jest ryzykowne.

**Uzasadnienie:** Sam offline-first PWA z IndexedDB, kompresją Web Canvas, kolejką z deduplikacją i dual-path sync (Android/iOS) to ok. 120–140 h. Do tego multi-tenant RLS + JWT custom claims, dashboard z PDF, integracja HotPay + Fakturownia — każdy z tych modułów to 30–80 h. 20 000 zł przy tej stawce to praca po ok. 60–65 zł/h, czyli de facto poniżej twojej stawki.

**Czego brakuje:**
1. **HotPay** — czy obsługuje płatności cykliczne (recurring), czy tylko jednorazowe (BLIK, szybki przelew)? Od tego zależy cała architektura modułu subskrypcji B2B.
2. **Urządzenia kierowców** — iOS, Android czy mix? Wymóg „sync całkowicie w tle, bez klikania" jest wykonalny dosłownie tylko na Chromium (Background Sync API nie istnieje w Safari). Na iOS trzeba dual-path: auto-sync przy starcie PWA + Web Push — i **twardy wymóg instalacji PWA na ekranie głównym**, bo Safari czyści IndexedDB po 7 dniach bez interakcji dla nie-zainstalowanych PWA. Bez tego dane kwitów znikają — czyli dokładnie ten problem, który masz rozwiązać.

**Rekomendacja:** negocjować budżet do ~28 000 zł brutto albo ciąć zakres (np. Fakturownia w Fazie 2 po Go-Live, PDF bez miniatur w v1). Inaczej nie wchodzić — fixed-price + 4 transze + prawa autorskie po każdej transzy przy niedoszacowaniu = praca poniżej stawki i ryzyko konfliktu przy odbiorach.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena 27–31,5k netto jest uczciwa dla pełnego zakresu, ale przy sztywnym budżecie 20k brutto (~16,3k netto po VAT) realna stawka spada do ~55–65 zł/h — czyli grubo poniżej mojej — więc korekta kwoty w dół byłaby kłamstwem, a nie negocjacją. Nie zgadłem na siłę żadnego modułu: PWA z dual-path sync, multi-tenant RLS, dashboard z PDF i subskrypcje B2B to realnie 300–350 h. Jedyne, co wcisnąłem na siłę, to mina nr 3 o Fakturowni — klient nie pytał, research to wykrył, ale w zgłoszeniu to zbędny szum i można to wyciąć. HotPay recurring słusznie został pytaniem, bo research tego nie rozstrzygnął. Uczciwa rekomendacja bez zmian: albo klient podnosi budżet do ~28k brutto, albo tniemy zakres (Fakturownia do Fazy 2, PDF bez miniatur w v1) — inaczej nie wchodzić.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 20000,
  "kwota_gorna": 28000,
  "definitywna": false,
  "od_czego_zaleza": [
    "Czy zakres zostaje zamrożony do MVP (np. Fakturownia w Fazie 2, PDF bez miniatur w v1), czy realizowany jest pełny zakres z briefu",
    "Czy HotPay obsługuje płatności cykliczne (recurring), czy wymagany jest cron i własna logika przypomnień po stronie wykonawcy",
    "Jakich urządzeń używają kierowcy (iOS/Android/mix) — wpływa na dual-path sync i konieczność twardego wymogu instalacji PWA",
    "Czy są makiety UI dashboardu, czy projektowanie interfejsu odbywa się od zera",
    "Gotowość środowisk HotPay i Fakturownia (API/sandbox) w dniu startu"
  ],
  "dni_od": 56,
  "dni_do": 84,
  "uzasadnienie": "Modele są zgodne, że pełny zakres briefu jest wart więcej niż 20 000 PLN; przy 90 zł/h daje to ok. 222 h, a realna pracochłonność pełnego multi-tenant SaaS z offline-first PWA, RLS, PDF, HotPay i Fakturownią to ok. 260–400 h. Zbieżność dotyczy też dwóch min: braku Background Sync w Safari oraz 7-dniowego czyszczenia IndexedDB na iOS bez instalacji PWA, co wymusza dual-path sync i warunek instalacji PWA. Rozbieżność jest w strategii: DeepSeek-B i C akceptują 20 000 PLN tylko przy twardym zamrożeniu zakresu/MVP, a DeepSeek-A i D odrzucają pełny zakres i wskazują 27 000–31 500 PLN. Dlatego finalnie wycena jest widełkowa: 20 000 PLN za ograniczony, jednoznacznie zamknięty MVP albo 24 000–28 000 PLN za pełniejszy zakres; bez doprecyzowania zakresu i HotPay recurring wycena nie może być definitywna." 
}

=== FINALNA WYCENA ===
20000-28000 zl netto | 56-84 dni | WIDELKI
Od czego zalezy: Czy zakres zostaje zamrożony do MVP (np. Fakturownia w Fazie 2, PDF bez miniatur w v1), czy realizowany jest pełny zakres z briefu, Czy HotPay obsługuje płatności cykliczne (recurring), czy wymagany jest cron i własna logika przypomnień po stronie wykonawcy, Jakich urządzeń używają kierowcy (iOS/Android/mix) — wpływa na dual-path sync i konieczność twardego wymogu instalacji PWA, Czy są makiety UI dashboardu, czy projektowanie interfejsu odbywa się od zera, Gotowość środowisk HotPay i Fakturownia (API/sandbox) w dniu startu
Uzasadnienie rozjemcy: Modele są zgodne, że pełny zakres briefu jest wart więcej niż 20 000 PLN; przy 90 zł/h daje to ok. 222 h, a realna pracochłonność pełnego multi-tenant SaaS z offline-first PWA, RLS, PDF, HotPay i Fakturownią to ok. 260–400 h. Zbieżność dotyczy też dwóch min: braku Background Sync w Safari oraz 7-dniowego czyszczenia IndexedDB na iOS bez instalacji PWA, co wymusza dual-path sync i warunek instalacji PWA. Rozbieżność jest w strategii: DeepSeek-B i C akceptują 20 000 PLN tylko przy twardym zamrożeniu zakresu/MVP, a DeepSeek-A i D odrzucają pełny zakres i wskazują 27 000–31 500 PLN. Dlatego finalnie wycena jest widełkowa: 20 000 PLN za ograniczony, jednoznacznie zamknięty MVP albo 24 000–28 000 PLN za pełniejszy zakres; bez doprecyzowania zakresu i HotPay recurring wycena nie może być definitywna.
