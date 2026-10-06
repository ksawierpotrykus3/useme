KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: Projekt jednorazowy — budowa mikro-SaaS od zera, fixed-price, 4 transze, przekazanie praw autorskich po każdej transzy. Brak deklaracji utrzymania/retainera po Go-Live.
INTENCJA: Mieszane — dominująco wykonawcze ("dostarcz moduły"), ale z wyraźnym elementem doradczym, bo klient WPROST wymaga uzasadnienia wyboru stosu PWA i strategii offline ("Oczekuję mocnego uzasadnienia wyboru", "Twój pomysł na stos").
DECYDENT_I_BOL: Założyciel "PaletSystem" — pisze w pierwszej osobie ("Tworzę"), ma własne konta firmowe (GitHub, Supabase, Vercel, HotPay), czyli jest decydentem i operatorem biznesu (najpewniej firma transportowa lub spedycja rozwijająca produkt). Ból: gubione kwity paletowe = realne straty windykacyjne; brak cyfrowego, odpornego na brak zasięgu obiegu dokumentów między trasą a biurem. Ból pod spodem: brak kontroli dowodowej przy sporach o palety z magazynami.
WYKONALNE: TAK — całość jest wykonalna technicznie. Jedyne zastrzeżenie dotyczy twardego, literalnego brzmienia wymogu „całkowicie w tle, bez klikania przez kierowcę" na iOS (patrz MINY).
POLE_DO_POPISU: JEST — dwie warstwy: (1) realna strategia offline z kompresją po stronie klienta, blob storage w IndexedDB, kolejką z deduplikacją i foreground/background sync zależnym od platformy; (2) świadomość limitu Background Sync API.
SCIEZKA_MERYTORYKI: A (klient wprost pyta o stos i obsługę offline zdjęć) + B (mina: wsparcie Background Sync API — Chromium-only).
MINY_I_CIEKAWOSTKI:
- Mina 1: „całkowicie w tle, bez klikania przez kierowcę" oparte o Service Worker Background Sync. DOWÓD ZE ZLECENIA: klient wymaga „profesjonalnej obsługi Service Worker Background Sync" oraz „całkowicie w tle, bez klikania". Mechanizm awarii: SyncManager/Background Sync API jest zaimplementowany w Chromium (Chrome/Edge — desktop i Android); Safari (iOS/macOS) i Firefox go NIE mają. Jeśli kierowcy jeżdżą na iPhone'ach, dosłowny wymóg „bez klikania" jest technicznie niewykonalny w tle przy zamkniętej aplikacji. Konsekwencja: nierozstrzygnięte ryzyko „myśleliśmy, że działa na wszystkich telefonach" w 8–10 tygodniu projektu. Alternatywa: jawny podział — na Chromium/Android Background Sync + Periodic Background Sync; na iOS foreground sync przy najbliższym otwarciu PWA (auto, ale przy starcie aplikacji) + ewentualnie Web Push jako wybudzacz. Akceptuję resztę zakresu bez zmian.
- Ciekawostka wspierająca (nie mina, bo klient o to nie pytał): iOS Safari potrafi wyczyścić IndexedDB po dłuższym okresie nieużywania PWA, jeśli aplikacja nie została dodana do ekranu głównego. To argument do rekomendacji „instalacja PWA jako warunek" w onboardingu kierowcy. Wchodzi tylko jako jedna linia w punkcie 1 odpowiedzi, bo klient wprost pyta „jak dokładnie obsłużysz tryb offline".
ODMOWA: Typ 2 — twardy limit zewnętrzny (wsparcie przeglądarki/OS). Obiekt odmowy w słowach klienta: „całkowicie w tle, bez klikania przez kierowcę". Mechanizm: brak SyncManager w Safari. Konsekwencja: na urządzeniach Apple synchronizacja nie zadziała bez otwarcia PWA. Alternatywa: sync foreground przy starcie + Background Sync na Androidzie + rekomendacja instalacji PWA + Web Push. Ton: rzeczowy, jedna akapit, na końcu — spokojnie akceptujemy resztę zakresu (RLS, JWT claims, PDF-y, HotPay, Fakturownia).
PYTANIA:
1. Na jakich urządzeniach jeżdżą kierowcy — iOS, Android, czy mix i w jakich proporcjach? Pytam, bo od tego zależy, czy wymóg „tła bez klikania" da się zrealizować dosłownie (Android + Chromium), czy trzeba zaprojektować dwie ścieżki sync (iOS: foreground przy starcie).
2. Jaka jest skala na start — ile organizacji, ilu kierowców, ile kwitów/dzień na jedną organizację? Pytam, bo od tego zależy tier Supabase, strategia partycjonowania Storage i kolejki Edge Functions.
CO_ZLECENIE_MOWI:
- Backend nienegocjowalny: Supabase (PostgreSQL + Auth + Storage + Edge Functions).
- PWA kierowcy: dowolny framework (React+Workbox / SvelteKit / Next PWA / Vue+Nuxt / Ionic+Capacitor) — z uzasadnieniem.
- Dashboard dyspozytora: dowolny nowoczesny front-end.
- Offline-first: IndexedDB, kompresja zdjęć Web Canvas API do <500 KB, Service Worker Background Sync, kolejka z deduplikacją, auto-sync po powrocie sieci.
- Multi-tenant: RLS w PostgreSQL, JWT custom claims (org_id + rola), role: Super-Admin / Właściciel / Dyspozytor / Kierowca.
- Dashboard: tabela salda paletowego (wydania/pobrania), generator PDF z miniaturami kwitów.
- Sprzedaż B2B: HotPay (BLIK + szybkie przelewy), webhooki subskrypcji, Fakturownia.pl API + archiwum PDF w panelu właściciela.
- Warunki: 20 000 PLN brutto, umowa o dzieło, 4 transze (Architektura+RLS / PWA+tryb samolotowy / Dashboard+webhooki / QA+Go-Live), 8–10 tygodni, prawa autorskie po każdej transzy.
- Zgłoszenie: dokładnie 3 punkty (stos+offline zdjęć, portfolio offline/Supabase 1–2 linki, termin startu).
CZEGO_NIE_MOWI:
- Jakich urządzeń używają kierowcy (iOS vs Android) — a to rozstrzyga o Background Sync.
- Skali wolumenu (organizacje, kierowcy, kwity/dzień) — a to wpływa na tier Supabase i architekturę Storage/kolejek.
- Czy są przygotowane makiety UI/UX dashboardu, czy projektujemy od zera.
- Czy konta HotPay i Fakturownia mają aktywny dostęp API/sandbox w momencie startu prac.
- Czy jest preferencja co do frameworka dashboardu, czy zostawiają to nam.
- Czy planują powiadomienia push/web push do kierowcy.
GRANICA_CIECIA:
- Długość: dokładnie 3 punkty wymagane przez klienta (stos+offline / portfolio / termin startu) + jedna krótka adnotacja o ograniczeniu Background Sync na iOS + 2 pytania na końcu. Nic więcej.
- Głębokość: punkt 1 rozwinięty najmocniej (bo klient tam patrzy — kompresja, IndexedDB, kolejka, dedup, sync), punkty 2 i 3 — jednym akapitem każdy.
- Nie ruszać: budżetu (nie kwestionować, nie negocjować w zgłoszeniu — klient go postawił twardo), zakresu funkcji (jest klarowny), kolejności transz.
RESEARCH_POTRZEBNY: TAK, przed wysłaniem oferty:
- caniuse: aktualne wsparcie Background Sync API i Periodic Background Sync (Chrome Android/desktop, Edge; brak Safari/Firefox — potwierdzić stan na dziś).
- iOS Safari: aktualna polityka eviction IndexedDB/Storage dla PWA nie-zainstalowanej (7 dni? czy coś się zmieniło w iOS 17/18).
- HotPay: publiczna dokumentacja API, model webhooków subskrypcji, tryb sandbox.
- Fakturownia.pl API: zakres endpointów faktur, webhooks, limity.
- OffscreenCanvas / Web Canvas API: potwierdzić, że kompresja <500 KB jest realna bez utraty czytelności kwitu — dobrać parametry jakości/redukcji do dokumentu (tekst, podpis, pieczątka).