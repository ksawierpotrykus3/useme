=== PROBA 1 ===
SEDZIA: {"status": "VETO", "kara_pkt": -20, "cytat_lub_brak": "Oferta zmienia zakres względem wymagań klienta: proponuje \"MVP, czyli Fakturownia w drugiej fazie i raport PDF bez miniatur w pierwszej wersji\" za 20 000 zł netto. Klient wymagał w zamówieniu m.in. integracji z Fakturownia.pl oraz PDF z miniaturami zdjęć od startu. Dodatkowo oferta podaje cenę 24 000–28 000 zł netto przy pełnym zakresie, podczas gdy budżet klienta to 20 000 PLN brutto, a sama oferta zaczyna się od 20 000 zł netto, co jest niespójne z oczekiwaniem klienta.", "uzasadnienie": "Klient wprost określił zakres i budżet: 20 000 PLN brutto, fixed-price, umowa o dzieło. Oferta proponuje inne warunki: 20 000 zł netto za okrojone MVP, a pełny zakres za 24 000–28 000 zł netto. To nie jest drobiazg, bo klient prosił o konkretny zakres, a oferta wycenia go inaczej i proponuje usunięcie części wymaganych funkcji. Klient może to odebrać jako brak uważnego czytania briefu i próbę renegocjacji stawek. Dodatkowo oferta nie odpowiada na kluczowe pytanie o obsługę zdjęć w trybie offline w kontekście wymaganej kompresji poniżej 500 KB przed wysłaniem, chociaż opisuje OffscreenCanvas — to akurat jest zgodne, ale całościowo oferta nie trzyma się warunków zamówienia.", "instrukcja_naprawy": "Utrzymaj zakres zgodny z briefem: Fakturownia i PDF z miniaturami od startu, bez dzielenia na fazy. Zaproponuj cenę mieszczącą się w budżecie klienta (20 000 PLN brutto / fixed-price, umowa o dzieło) albo jednoznacznie zaznacz, że przy tym budżecie zakres musi zostać ograniczony, ale wtedy zapytaj klienta o zgodę, zamiast samodzielnie zmieniać warunki. Nie podawaj ceny netto, jeśli klient podał budżet brutto — ujednolić stawkę. Odpowiedz wprost na pytanie o obsługę offline zdjęć (IndexedDB, kolejka, deduplikacja, Background Sync) i nie pomijaj integracji z Fakturownia ani miniatur w PDF."}

WERYFIKACJA FAKTOW:
**Twierdzenie 1:** Klient wprost określił zakres i budżet: 20 000 PLN brutto, fixed-price, umowa o dzieło.

**Werdykt:** PRAWDA

**Dowód:** W treści zlecenia znajduje się bezpośredni zapis: *„Wynagrodzenie: 20 000 PLN brutto (stała cena / fixed-price). Umowa o dzieło."* Jest to jednoznaczne określenie warunków finansowych i formy współpracy przez klienta.

---

**Twierdzenie 2:** Oferta proponuje inne warunki: 20 000 zł netto za okrojone MVP, a pełny zakres za 24 000–28 000 zł netto.

**Werdykt:** PRAWDA

**Dowód:** W ofercie Ksawiera znajduje się następujący fragment: *„Cena. Przy zakresie ograniczonym do MVP, czyli Fakturownia w drugiej fazie i raport PDF bez miniatur w pierwszej wersji, 20 000 zł netto. Przy pełnym zakresie z briefu, z Fakturownią i PDF-em z miniaturami od startu, 24 000 do 28 000 zł netto."* Oferta wprost kontrastuje dwa warianty cenowe, oba w kwotach netto, co jest niezgodne z budżetem brutto klienta.

---

**Twierdzenie 3:** Klient wymagał w zamówieniu m.in. integracji z Fakturownia.pl oraz PDF z miniaturami zdjęć od startu.

**Werdykt:** PRAWDA

**Dowód:** W treści zlecenia klient wymienia w sekcji „ZAUTOMATYZOWANA ŚCIEŻKA SPRZEDAŻY B2B": *„Integracja z Fakturownia.pl (API) w celu zautomatyzowanego wystawiania i wysyłki faktur."* Natomiast w sekcji „PANEL DYSPOZYTORA (Web Dashboard)" klient pisze: *„Wbudowany generator raportów PDF. Dokument musi czytelnie zestawiać transakcje i posiadać estetycznie osadzone miniatury zdjęć kwitów jako twarde dowody windykacyjne dla magazynów."* Oba wymagania są częścią podstawowego zakresu, bez wskazania na fazowanie.

---

**Twierdzenie 4:** Oferta nie odpowiada na kluczowe pytanie o obsługę zdjęć w trybie offline w kontekście wymaganej kompresji poniżej 500 KB przed wysłaniem.

**Werdykt:** FAŁSZ

**Dowód:** Oferta Ksawiera zawiera szczegółowy opis obsługi offline dla zdjęć: *„Zdjęcie leci przez OffscreenCanvas z iteracyjnym toBlob po jakości aż do zejścia poniżej 500 KB przy maxWidth 1600 px, co trzyma czytelność kwitu. Blob zapisuję bezpośrednio w IndexedDB razem z rekordem formularza w jednej transakcji. Kolejka z deduplikacją po uuid rekordu, odporna na wielokrotne wywołania sync."* Opis ten bezpośrednio adresuje wymagania klienta dotyczące kompresji poniżej 500 KB, zapisu w IndexedDB oraz kolejki z deduplikacją. Jednocześnie oferta rzetelnie informuje o ograniczeniach Background Sync API na iOS, co jest istotnym uzupełnieniem, a nie pominięciem tematu.

---

**Twierdzenie 5:** Oferta podaje cenę 24 000–28 000 zł netto przy pełnym zakresie, podczas gdy budżet klienta to 20 000 PLN brutto, a sama oferta zaczyna się od 20 000 zł netto, co jest niespójne z oczekiwaniem klienta.

**Werdykt:** PRAWDA

**Dowód:** Jak wykazano w Twierdzeniu 2, oferta zawiera dokładnie takie sformułowania. Klient określił budżet brutto, a oferta operuje wyłącznie kwotami netto, co przy stawce 20 000 zł netto daje kwotę brutto znacząco przekraczającą założony budżet (przy 23% VAT byłoby to ok. 24 600 zł brutto). Jest to niespójność formalna i merytoryczna.

---

**Twierdzenie 6:** Background Sync API działa wyłącznie w Chromium; Safari na iOS tego API nie ma.

**Werdykt:** PRAWDA

**Dowód:** Zgodnie z danymi z caniuse.com, Background Sync API nie jest obsługiwane przez Safari ani na iOS, ani na macOS. Potwierdza to również dokumentacja WebKit, gdzie przedstawiciele Apple wskazują, że użytkownicy Safari na iOS muszą mieć otwarte okno przeglądarki, aby synchronizacja mogła się odbyć.

---

**Twierdzenie 7:** Safari czyści IndexedDB po siedmiu dniach bez interakcji, jeśli PWA nie jest zainstalowana na ekranie głównym.

**Werdykt:** PRAWDA

**Dowód:** Zgodnie z dokumentacją WebKit oraz dyskusjami na Stack Overflow, Safari stosuje siedmiodniowy limit na całą pamięć zapisywalną przez skrypty, w tym IndexedDB, jeśli użytkownik nie wchodzi w interakcję z witryną. Wyjątkiem są aplikacje PWA dodane do ekranu głównego, które nie podlegają tej polityce.

---

**Twierdzenie 8:** Supabase obsługuje RLS z użyciem JWT custom claims zawierających org_id i rolę.

**Werdykt:** PRAWDA

**Dowód:** Dokumentacja Supabase oraz liczne źródła społecznościowe potwierdzają, że można wstrzykiwać niestandardowe oświadczenia (custom claims) do tokenów JWT, w tym org_id, i wykorzystywać je w politykach Row Level Security. Przykładowo, w dyskusji na GitHubie opisano dodawanie organization_id do app_metadata jako custom claim, a w innym źródle pokazano funkcję get_org_id() odczytującą org_id z JWT w politykach RLS.

---

**Twierdzenie 9:** HotPay obsługuje płatności cykliczne.

**Werdykt:** NIEPOTWIERDZONE

**Dowód:** W wynikach wyszukiwania znaleziono informacje, że HotPay obsługuje BLIK, szybkie przelewy, karty płatnicze i inne metody, ale nie ma wzmianki o płatnościach cyklicznych (subskrypcjach). Dokumentacja API HotPay wspomina o „Single payment" (pojedynczej płatności) i nie wymienia płatności cyklicznych. Brak jest dowodów na potwierdzenie tego twierdzenia, dlatego oznaczam je jako niepotwierdzone.


=== PROBA 2 ===
SEDZIA: {"status": "VETO", "kara_pkt": -20, "cytat_lub_brak": "Nie mamy gotowego portfolio w tej niszy, więc nie będę wpisywał tu cudzych linków.", "uzasadnienie": "Klient wprost wymagał w punkcie 2 aplikacji: 'Portfolio z naciskiem na Offline/Supabase: Podeślij linki do 1-2 autorskich systemów'. Oferta nie tylko nie podaje żadnego linku, ale też nie wskazuje żadnego konkretnego doświadczenia z offline ani z Supabase. Zapowiedź pokazania fragmentu na logice kolejki i schemacie RLS to nie portfolio, tylko propozycja pracy przed startem. Klient czytający trzydziestą ofertę nie ma podstaw, by zaufać wykonawcy, który nie pokazuje niczego, mimo że o to wprost poprosił. Poza tym pojawia się pytanie o płatności cykliczne HotPay, na które klient nie czeka w tym momencie — sam wymaga podpięcia bramki i webhooków, a pytanie na tym etapie może brzmieć jak przerzucanie ustaleń na klienta.", "instrukcja_naprawy": "Zastąp akapit o portfolio konkretnymi, prawdziwymi dowodami doświadczenia: podaj linki do 1-2 własnych wdrożeń lub projektów, które realnie istnieją i które można pokazać (np. repozytorium, demo, case study) — jeśli brak projektów komercyjnych w tej niszy, wskaż własne projekty hobbystyczne lub open-source związane z offline/IndexedDB/Service Worker/Supabase i opisz je jednym zdaniem. Nie zmyślaj klientów ani branż. Pytanie o HotPay przenieś na etap po akceptacji oferty albo sformułuj jako założenie do potwierdzenia w trakcie discovery, a nie jako warunek wyceny."}

WERYFIKACJA FAKTOW:
Poniżej weryfikacja każdego zakwestionowanego twierdzenia z osobna, z dowodami.

---

**Twierdzenie 1: Background Sync API działa wyłącznie w Chromium; Safari na iOS tego API nie ma.**

**Werdykt: PRAWDA.**

Dokumentacja caniuse.com wprost wskazuje, że Background Sync API jest wspierane w Chrome (od wersji 49), Edge (od 79) i Opera (od 42), natomiast Safari — zarówno desktopowe, jak i na iOS — ma oznaczenie „Not supported” we wszystkich wersjach (Safari 3.1–26.6, Safari on iOS 3.2–27.2) . Dodatkowe źródło (Transloadit, 2025) potwierdza: „The Background Sync API is currently supported only in Chromium-based browsers (Chrome, Edge, Opera). Firefox, Safari, and many mobile browsers do not support background sync as of 2024” .

Twierdzenie z oferty jest zatem w pełni zgodne ze stanem faktycznym.

---

**Twierdzenie 2: Safari czyści IndexedDB po siedmiu dniach bez interakcji, jeśli PWA nie jest zainstalowana na ekranie głównym.**

**Werdykt: PRAWDA (z zastrzeżeniem).**

WebKit Bug 237350 zawiera oficjalne stanowisko inżyniera Apple (John Wilander): „The only things that should be capped to 7 days for the main domain of Home Screen web apps are: – Cookies created in JavaScript. – Cookies created in 3rd-party CNAME-cloaked HTTP responses. Non CNAME-cloaked server-set cookies and HTML storage should not be deleted for the main domain of Home Screen web apps” . Oznacza to, że PWA dodane do ekranu głównego **są zwolnione** z 7-dniowego limitu dla IndexedDB i innych form storage. Natomiast dla zwykłych stron otwieranych w Safari (bez instalacji na ekranie głównym) limit 7 dni obowiązuje — potwierdza to m.in. WebKit Bug 232302: „Service worker and storage deleted after 7 days on Web application added to Home Screen” oraz liczne źródła społecznościowe .

Twierdzenie z oferty jest więc prawdziwe: jeśli PWA **nie jest** zainstalowana na ekranie głównym, Safari usunie IndexedDB po 7 dniach bez interakcji. Autorka oferty słusznie wskazuje, że instalacja PWA na ekranie głównym jest twardym warunkiem onboardingu kierowcy.

---

**Twierdzenie 3: HotPay obsługuje płatności cykliczne.**

**Werdykt: PRAWDA.**

Polski HotPay (ePłatności Sp. z o.o.) w swojej dokumentacji technicznej dla Direct Carrier Billing (DCB) wprost wymienia: „ONE TIME AND SUBSCRIPTION PAYMENT” . W polskiej wersji dokumentacji pojawia się zapis: „Opłata cykliczna – rodzaj usługi (w DCB istnieje możliwość ustanowienia subskrypcji, gdzie klient będzie obciążany równych okresach automatycznie)” . HotPay obsługuje też BLIK i szybkie przelewy online Pay-by-Link (PBL), co jest zgodne z wymogiem klienta .

Twierdzenie z oferty, że HotPay obsługuje płatności cykliczne, jest zatem prawdziwe.

---

**Twierdzenie 4: Supabase RLS per org_id, JWT custom claims z org_id i rolą.**

**Werdykt: PRAWDA.**

Supabase oficjalnie wspiera ten wzorzec. Dokumentacja „Token Security and Row Level Security” opisuje, jak używać `auth.jwt()` do odczytu custom claims w politykach RLS, w tym `client_id` i innych claims . Artykuł „Supabase RLS Advanced Patterns — Team Sharing, Multi-Tenancy, and Admin Access” (DEV Community, kwiecień 2026) wprost pokazuje: „Multi-tenancy → JWT custom claim (org_id) for org isolation” oraz funkcję `get_org_id()` odczytującą `org_id` z JWT . Inny przewodnik Supabase („Custom Claims & Role-based Access Control”) opisuje użycie Custom Access Token Hook do wstrzykiwania `user_role` i innych claims do JWT na potrzeby polityk RLS .

Twierdzenie z oferty jest zgodne z oficjalnymi wzorcami Supabase.

---

**Twierdzenie 5: Fakturownia.pl API do wystawiania faktur.**

**Werdykt: PRAWDA.**

Fakturownia.pl posiada publiczne API REST z dokumentacją dla deweloperów. Endpoint `POST /external/v1/documents` służy do wystawiania faktur, proform, korekt i innych dokumentów . Dokumentacja zawiera pełny opis pól żądania, obsługę KSeF (Krajowy System e-Faktur) oraz idempotencji przez nagłówek `Idempotency-Key` . Istnieją również gotowe SDK (Python, Laravel, n8n) potwierdzające praktyczne użycie API .

Twierdzenie z oferty jest w pełni potwierdzone.

---

**Twierdzenie 6: OffscreenCanvas z iteracyjnym toBlob po jakości aż do zejścia poniżej 500 KB.**

**Werdykt: PRAWDA (technika możliwa do zrealizowania).**

`OffscreenCanvas.convertToBlob()` przyjmuje parametr `quality` (0–1) dla formatów stratnych (image/jpeg, image/webp) i jest dostępny we wszystkich nowoczesnych przeglądarkach od marca 2023 . Można go wywoływać iteracyjnie z coraz niższą jakością, aż rozmiar blobu spadnie poniżej zadanego progu. Potwierdzają to istniejące implementacje: pakiet `browser-image-optimizer-sdk` stosuje „Adaptive Quality Control: Iteratively adjusts compression factors to meet target size constraints” , a `ImageCompressorWeb` używa „binary-search quality down to minQuality until the output fits under maxBytes” .

Twierdzenie z oferty opisuje zatem realną i udokumentowaną technikę.

---

**Twierdzenie 7: Service Worker Background Sync oraz niestandardowa kolejka z deduplikacją danych.**

**Werdykt: PRAWDA.**

Wzorzec „outbox queue w IndexedDB + Background Sync API + deduplikacja” jest szeroko opisany w literaturze i implementacjach. Przykład: „outbox in IndexedDB … Your service worker can then … removing it from the IndexedDB queue if it was sent successfully” . Inny wzorzec z deduplikacją: „deduplicate by server ID or client UUID … Background sync: When a message is queued while offline, the service worker registers a sync event” . Pakiety takie jak `offline-sync-engine` oferują „Offline-first mutation queue + idempotent server sync” , a `react-offline-kit` zawiera „IndexedDB, service worker, background sync, and conflict resolution” .

Twierdzenie z oferty jest zgodne z ugruntowanymi wzorcami inżynierii offline-first.

---

**Twierdzenie 8 (z komentarza sędziego): Klient wprost wymagał w punkcie 2 aplikacji: „Portfolio z naciskiem na Offline/Supabase: Podeślij linki do 1-2 autorskich systemów”.**

**Werdykt: PRAWDA.**

Treść ogłoszenia zawiera dosłownie ten wymóg w sekcji „JAK APLIKOWAĆ (Wymagam konkretów)”, punkt 2: „Portfolio z naciskiem na Offline/Supabase: Podeślij linki do 1-2 autorskich systemów.”

---

**Twierdzenie 9 (z komentarza sędziego): Oferta nie podaje żadnego linku ani nie wskazuje doświadczenia z offline/Supabase.**

**Werdykt: PRAWDA.**

W punkcie 2 oferty autor pisze: „Nie mamy gotowego portfolio w tej niszy, więc nie będę wpisywał tu cudzych linków. Podejście mogę pokazać na fragmencie Waszego zakresu, na przykład na logice kolejki z deduplikacją i schemacie RLS, jeszcze przed startem prac.” Nie podano żadnego linku do repozytorium, demo ani case study. Zapowiedź pokazania fragmentu kodu „przed startem prac” nie jest portfolio w rozumieniu wymogu klienta.

---

**Twierdzenie 10 (z komentarza sędziego): Pytanie o płatności cykliczne HotPay może być odebrane jako przerzucanie ustaleń na klienta.**

**Werdykt: NIEPOTWIERDZONE (ocena subiektywna, nie techniczna).**

Nie da się zweryfikować obiektywnie, czy pytanie „Czy Wasz HotPay obsługuje płatności cykliczne, czy tylko jednorazowe?” zostanie odebrane jako przerzucanie ustaleń na klienta. Jest to ocena percepcji, zależna od kontekstu i odbiorcy. HotPay **faktycznie obsługuje** płatności cykliczne (patrz Twierdzenie 3), więc pytanie ma merytoryczne uzasadnienie — ale jego umiejscowienie (przed akceptacją oferty, w kontekście wyceny) może budzić wątpliwości komunikacyjne. Sędzia słusznie sugeruje przeniesienie tego pytania na etap discovery po akceptacji oferty.

---

**Podsumowanie:**

| # | Twierdzenie | Werdykt |
|---|---|---|
| 1 | Background Sync tylko w Chromium, brak w Safari iOS | PRAWDA |
| 2 | Safari czyści IndexedDB po 7 dniach bez instalacji PWA | PRAWDA |
| 3 | HotPay obsługuje płatności cykliczne | PRAWDA |
| 4 | Supabase RLS per org_id + JWT custom claims | PRAWDA |
| 5 | Fakturownia.pl API do faktur | PRAWDA |
| 6 | OffscreenCanvas iteracyjne toBlob < 500 KB | PRAWDA |
| 7 | Service Worker Background Sync + kolejka z deduplikacją | PRAWDA |
| 8 | Klient wymagał portfolio z linkami | PRAWDA |
| 9 | Oferta nie podała żadnego linku ani doświadczenia | PRAWDA |
| 10 | Pytanie o HotPay = przerzucanie ustaleń | NIEPOTWIERDZONE |
