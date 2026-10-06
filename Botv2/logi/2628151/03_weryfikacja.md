KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: Projekt jednorazowy — budowa mikro-SaaS od zera, fixed-price, 4 transze, umowa o dzieło, prawa autorskie po każdej transzy. Bez retainera po Go-Live.
INTENCJA: Mieszane — dominująco wykonawcze ("dostarcz moduły"), ale klient WPROST wymaga doradztwa w punkcie 1 zgłoszenia ("Twój pomysł na stos", "Oczekuję mocnego uzasadnienia wyboru").
DECYDENT_I_BOL: Założyciel/właściciel firmy transportowej (pierwsza osoba "Tworzę", własne konta firmowe GitHub/Supabase/Vercel/HotPay). Ból: gubione kwity paletowe = realne straty windykacyjne; brak cyfrowego, odpornego na brak zasięgu obiegu kwitów między trasą a biurem. Ból pod spodem: brak dowodu przy sporach o palety z magazynami.
WYKONALNE: TAK. Zastrzeżenie tylko przy literalnym "całkowicie w tle, bez klikania" na iOS (patrz miny).
POLE_DO_POPISU: JEST — strategia offline (blob w IndexedDB, kolejka z dedup, kompresja <500 KB, sync foreground/background zależnie od platformy) + świadomość limitów Background Sync i ITP.
SCIEZKA_MERYTORYKI: A (klient wprost pyta o stos i offline zdjęć) + B (miny: Background Sync + trwałość IndexedDB na iOS).
MINY_I_CIEKAWOSTKI:
- Mina 1 (iOS — sync w tle). Obiekt w słowach klienta: "całkowicie w tle, bez klikania przez kierowcę" oraz "profesjonalnej obsługi Service Worker Background Sync". Mechanizm: SyncManager/Background Sync API istnieje wyłącznie w Chromium (Chrome/Edge/Samsung; desktop + Android). Safari iOS/macOS oraz Firefox nie mają tego API. Konsekwencja: jeśli we flocie są iPhone'y, dosłowne "zero klikania w tle przy zamkniętej aplikacji" nie jest wykonalne. Remedium: dwie ścieżki — Android: Background Sync (+ Periodic Background Sync po instalacji); iOS: auto-sync przy starcie PWA + opcjonalnie Web Push (działa na iOS tylko przy zainstalowanej PWA). Bez straszenia — fakt + rozwiązanie.
- Mina 2 (iOS — trwałość IndexedDB). Obiekt w słowach klienta: "zdjęcia muszą zapisywać się lokalnie... bezpośrednio w bazie IndexedDB" + "Po odzyskaniu zasięgu siecią aplikacja musi... wysłać". Mechanizm: Safari dla nie-zainstalowanej PWA czyści IndexedDB/LocalStorage/SW cache po 7 dniach bez interakcji (ITP, potwierdzone aktualnie; iOS Home Screen Web App jest wyłączony z ITP). Konsekwencja: bez instalacji PWA na ekranie głównym system nie gwarantuje trwałości lokalnych danych kwitów. Remedium: instalacja PWA jako twardy warunek onboardingu kierowcy — jedna linia w punkcie 1, bo klient wprost pyta "jak dokładnie obsłużysz offline".
ODMOWA: Typ 2 (twardy limit zewnętrzny — brak SyncManager w Safari). Obiekt: "całkowicie w tle, bez klikania". Mechanizm: brak API w Safari. Konsekwencja: na iOS sync musi być foreground. Alternatywa: dwie ścieżki sync + wymóg instalacji PWA. Miejsce: jedna klauzula w punkcie 1 zgłoszenia, nie osobny akapit, bez wzmacniania. Uwaga: NIE robimy osobnego punktu "odmowa Fakturownia webhooks" — klient nie wspomina o webhookach Fakturowni, tylko o HotPay (webhook subskrypcji). To była nadinterpretacja w iteracji 1.
PYTANIA:
1. Czy HotPay, którego Państwo używają, obsługuje płatności cykliczne (recurring/subskrypcje), czy tylko jednorazowe (BLIK, szybki przelew)? Pytam, bo od tego zależy mechanizm przedłużania subskrypcji: jeśli HotPay nie ma recurring, buduję harmonogram (cron + przypomnienia) po naszej stronie i aktywację przez webhook po każdej opłacie. Odpowiedź zmienia architekturę modułu sprzedaży B2B.
(Świadomie NIE pytam o iOS vs Android we flocie — proponujemy rozwiązanie dual-path w punkcie 1, które działa niezależnie od odpowiedzi. To TYP 2. Świadomie NIE pytam o skalę — cena jest fixed 20 000 PLN, więc skala nie zmienia wyceny, a nie kwalifikuje do wykrywacza, bo klient już udowodnił powagę briefu. Świadomie NIE pytam o Web Push — proponujemy domyślnie jako element architektury iOS.)
CO_ZLECENIE_MOWI:
- Backend nienegocjowalny: Supabase (PostgreSQL + Auth + Storage + Edge Functions).
- PWA kierowcy: dowolny framework z uzasadnieniem (React+Workbox / SvelteKit / Next PWA / Vue+Nuxt / Ionic+Capacitor).
- Dashboard: dowolny nowoczesny front-end.
- Offline-first: IndexedDB, kompresja Web Canvas <500 KB, Service Worker Background Sync, kolejka z dedup, auto-sync po powrocie sieci, "całkowicie w tle, bez klikania".
- Multi-tenant: RLS w PostgreSQL, JWT custom claims (org_id + rola), role: Super-Admin / Właściciel / Dyspozytor / Kierowca.
- Dashboard: tabela salda paletowego, generator PDF z miniaturami kwitów.
- Sprzedaż B2B: HotPay (BLIK + szybkie przelewy), webhooki subskrypcji → aktywacja/przedłużenie konta Organizacji, Fakturownia.pl API (wystawianie + wysyłka faktur), archiwum PDF w panelu właściciela.
- Warunki: 20 000 PLN brutto, umowa o dzieło, 4 transze (Architektura+RLS / PWA+tryb samolotowy / Dashboard+webhooki / QA+Go-Live), 8–10 tygodni, prawa autorskie po każdej transzy.
- Format zgłoszenia: dokładnie 3 punkty (stos+offline / portfolio offline/Supabase 1-2 linki / termin startu).
CZEGO_NIE_MOWI:
- Jakich urządzeń używają kierowcy (iOS/Android/mix) — rozstrzyga literalność "tła bez klikania".
- Czy HotPay obsługuje płatności cykliczne — rozstrzyga architekturę subskrypcji.
- Skali wolumenu (organizacje/kierowcy/kwity na dzień).
- Czy są makiety UI dashboardu, czy projektujemy od zera.
- Czy konta HotPay i Fakturownia mają aktywny dostęp API/sandbox w dniu startu.
- Preferencji frameworka dashboardu (klient zostawił dowolność).
GRANICA_CIECIA:
- Długość: dokładnie 3 punkty wymagane przez klienta + jedna krótka klauzula o iOS (dual-path + wymóg instalacji PWA) w punkcie 1 + 1 pytanie na końcu. Nic więcej.
- Głębokość: punkt 1 najmocniejszy (framework + architektura offline krok po kroku: blob w IndexedDB → kolejka z dedup → kompresja <500 KB → sync Android/iOS), punkty 2 i 3 jednym akapitem każdy.
- Nie ruszać: budżetu (fixed, akceptujemy albo odrzucamy — bez negocjacji w zgłoszeniu), zakresu funkcji, kolejności transz.
RESEARCH_POTRZEBNY: TAK, przed wysłaniem:
- caniuse: potwierdzić Background Sync / Periodic Background Sync (potwierdzone: Chromium-only; Periodic tylko dla zainstalowanych PWA).
- iOS Safari: potwierdzić 7-dniowe ITP dla nie-zainstalowanych PWA (potwierdzone, brak zmian w iOS 17/18).
- HotPay: rozstrzygnąć pytanie o recurring — albo z dokumentacji (niepotwierdzone w iteracji 1), albo zostawiamy jako pytanie do klienta.
- Kompresja Canvas: potwierdzić realność <500 KB przy zachowaniu czytelności kwitu (potwierdzone, iteracyjny quality + maxWidth 1280–1600).
- Fakturownia API: do weryfikacji przed implementacją (nie przed ofertą), klient nie zgłaszał tu nietypowych wymagań.

DECYZJE:
DOPISAĆ (do treści odpowiedzi klientowi, nie do dziennika):
- Punkt 1: konkret framework PWA (rekomendacja: SvelteKit albo React+Workbox — jedno uzasadnienie, nie lista opcji), architektura offline w 4 krokach (blob w IndexedDB → kolejka z dedup → kompresja <500 KB przez OffscreenCanvas/Web Canvas z iteracyjnym quality → sync), jedna klauzula: "Dla iOS (Safari nie ma Background Sync API i czyści IndexedDB po 7 dniach dla nie-zainstalowanych PWA) proponuję dual-path: Android = Background Sync + Periodic, iOS = auto-sync przy starcie PWA + Web Push; instalacja PWA na ekranie głównym jako warunek onboardingu kierowcy".
- Punkt 2: 1-2 linki portfolio offline/Supabase (poza zakresem dziennika — dostarcza człowiek wysyłający zgłoszenie).
- Punkt 3: konkretna data startu.
- Pytanie na końcu: HotPay recurring (jak w PYTANIA).
ODPOWIEDZIEĆ (merytorycznie w treści zgłoszenia):
- Backend: Supabase zgodnie z wymogiem.
- RLS + JWT custom claims (org_id, rola) — potwierdzić.
- Dashboard: rekomendacja jednego stosu z PWA (np. SvelteKit po obu stronach) — mniej pracy, spójny typ.
- PDF kwitów: potwierdzić podejście (miniatury jako twarde dowody).
- Fakturownia API + HotPay — potwierdzić integrację, bez wchodzenia w szczegóły webhooków (klient nie pytał).
DOPYTAĆ (tylko 1 pytanie, jak wyżej):
- HotPay recurring vs one-off.

USUNIĘTE Z ITERACJI 1 (świadomie): mina o Fakturownia webhooks (brak dowodu ze zlecenia — klient wymagał webhooków tylko od HotPay); pytanie o skalę (fixed price = nie zmienia wyceny); osobne traktowanie ciekawostki o ITP (wciągnięte jako mina 2, bo wprost uderza w ból klienta: zniknięcie kwitów = gubione kwity).