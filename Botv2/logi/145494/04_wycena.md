=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena**
- **Praca:** 7 000–10 000 zł netto (60–87 h × 115 zł/h).
- **Podzespoły:** 800–1 500 zł netto, jeśli mam je dobrać i kupić (z elektromagnesami; bez elektromagnesów ok. 600–1 100 zł).
- **Razem:** ok. **7 800–11 500 zł netto**.
- **Czas:** 12–18 dni roboczych od ustalenia API/QR i dostępności części.

**Uzasadnienie:** Zakres obejmuje dobór elektroniki, firmware, integrację, testy, schemat, BOM, instrukcję i przekazanie praw autorskich. Rekomenduję ESP32 + gotowy moduł przekaźnikowy z RS485 oraz dedykowany czytnik QR UART zamiast kamery ESP32-CAM — prościej, taniej i pewniej. Backend, web i mobile są poza zakresem.

**Brakuje do startu:** kontrakt API logów (endpoint, format, auth, offline/retry), co koduje QR i mapowanie QR → sekcja, kto kupuje podzespoły, warunki środowiskowe/zasilanie oraz termin startu.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena jest obroniona, ale **górna granica 10 000 zł jest naciągnięta** — przy gotowych modułach (Waveshare S3-Relay-6CH z RS485, czytnik QR UART) schodzi dużo lutowania i projektowania PCB, więc realny zakres to raczej **45–65 h, czyli ok. 5 200–7 500 zł netto**. Nie zgadywałem na siłę niczego poważnego — dodałem tylko flyback, IP65 i rezerwę RS485, co klient sam sugerował („zabezpieczenie do ustalenia”, „rezerwa RS485/UART/USB”), więc to nie jest dopisywanie funkcji. Ryzyko siedzi w API i buforze offline — jeśli klient zażyczy sobie rozbudowany retry/backoff i mapowanie QR→sekcja po stronie firmware, wtedy wracamy do 8–10k. **Koryguję widełki prac na 5 500–8 000 zł netto (48–70 h)**, a podzespoły bez zmian (600–1 500 zł w zależności od tego, czy z elektromagnesami i kto kupuje).

=== DeepSeek-B — RUNDA 1 ===
**Wycena (praca):** 5 200 – 6 400 zł netto (45–55 h × 115 zł/h)
**Podzespoły:** ok. 700 – 1 200 zł (BOM z linkami, klient kupuje lub ja z fakturą – do ustalenia)
**Czas:** 10–15 dni roboczych od zamknięcia specyfikacji (API + QR) i potwierdzenia BOM.

**Uzasadnienie:** Zakres to typowy prototyp embedded — dobre okablowanie sprzętowe, ale głównie firmware z logiką sesji, obsługą QR po UART i buforowanymi logami HTTP; przy 2–3 elektromagnesach i modularności pod RS485 (etap 2) uczciwie wychodzi ~50 h. Idę w ESP32 (Waveshare ESP32-S3-Relay-6CH — ma wbudowany izolowany RS485, więc rezerwa pod wagę z etapu 2 jest za darmo) i dedykowany czytnik QR po UART (GM65/Waveshare) zamiast kamery na ESP32-CAM, bo ta nie uciąga dekodowania QR. Raspberry Pi odpada — droższy, wolniejszy start, prądożerny i wymaga OS tam, gdzie wystarczy bare-metal.

**Czego brakuje, żeby ruszyć:**
1. Kontrakt API logów: endpoint, format (JSON?), autoryzacja, zachowanie przy braku sieci (bufor lokalny + retry, czy tylko retry w locie).
2. Zawartość QR i mapowanie QR → sekcja: co koduje kod (ID usera / token / URL) i skąd firmware wie, którą sekcję otworzyć — z API czy z lokalnej tablicy.
3. Warunki środowiskowe (IP obudowy, zakres temp., zasilanie na miejscu) i kto kupuje podzespoły.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Wycena była oparta na realnym zakresie prototypu: ESP32 + przekaźniki, czytnik QR po UART, logika sesji, logi HTTP i rezerwa RS485 — bez zgadywania API i zawartości QR, bo klient sam zostawił to do ustalenia. Nie dopisałem na siłę funkcji spoza zakresu (OTA, provisioning, backend), więc zakres merytoryczny był czysty. Uważam jednak, że dolne 45 h jest ryzykowne przy outdoorze, dokumentacji, testach i nieustalonym API — skorygowałbym pracę na 50–60 h, czyli **5 750–6 900 zł netto**. Podzespoły **700–1 200 zł** mogą być za niskie, jeśli dojdzie zasilacz IP65 i porządne elektromagnesy 12 V — realniej **900–1 500 zł**. Reszta bez zmian: ESP32, nie Raspberry Pi; dedykowany czytnik QR UART, nie kamera ESP32-CAM.

=== DeepSeek-C — RUNDA 1 ===
**Wycena**
- **Praca:** 6 000–8 000 zł (52–70 h × 115 zł/h).
- **Podzespoły:** 900–1 600 zł, osobno, wg BOM po ustaleniu czytnika QR i obudowy.
- **Razem:** ok. 6 900–9 600 zł.

**Czas:** 10–15 dni roboczych od ustalenia API/QR i zamówienia części; kalendarzowo 2–3 tygodnie.

**Uzasadnienie:** Zakres obejmuje dobór elektroniki, firmware, integrację, testy i dokumentację, nie tylko samo pisanie kodu. Rekomenduję ESP32 + gotowy moduł przekaźnikowy z RS485 pod etap 2 oraz dedykowany czytnik QR UART zamiast ESP32-CAM — to upraszcza firmware i zmniejsza ryzyko. W cenie: kod, schemat, BOM, instrukcja i przeniesienie praw autorskich.

**Brakuje:** kontrakt API logów (endpoint, format, auth, offline/retry), zawartość QR i mapowanie QR→sekcja, kto kupuje podzespoły, warunki środowiskowe/zasilanie, termin startu. Bez API i QR nie zaczynam firmware.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Wycena 6 000–8 000 zł jest realna dla prototypu z integracją (nie tylko pisanie kodu), ale dolna granica jest bezpieczna — przy trzech otwartych punktach (API, QR, mapowanie) ryzyko rozjazdu jest po stronie wykonawcy, więc trzymam przedział. BOM 900–1 600 zł to szacunek orientacyjny — nie znam jeszcze obudowy, zasilania ani konkretnego czytnika QR, więc to zgadywanie z widełkami, nie twarda kwota. Rekomendacja czytnika QR UART zamiast ESP32-CAM to moja propozycja projektowa, nie fakt — klient może chcieć kamerę i wtedy zakres rośnie. Nie widzę nic dopisanego na siłę; brakuje raczej potwierdzenia, kto kupuje podzespoły, bo od tego zależy, czy BOM wchodzi do mojej wyceny. Korekty kwoty nie robię bez odpowiedzi na pytania 1–2 — one mogą zmienić zakres o kilka godzin w obie strony.

=== DeepSeek-D — RUNDA 1 ===
Wycena wstępna (MVP, bez web/mobile/backend):

- **Praca:** 5 800–7 500 zł (50–65 h × 115 zł/h)
- **Podzespoły:** 600–1 200 zł (BOM; jeśli elektromagnesy i zasilacz 12 V są po Waszej stronie, ok. 400–700 zł)
- **Czas:** 10–15 dni roboczych od ustalenia API/QR i dostępności części

Uzasadnienie: rekomenduję **ESP32, nie Raspberry Pi** – wystarczy do logiki, HTTP i UART, jest tańszy i prostszy. Zamiast kamery ESP32-CAM proponuję dedykowany czytnik QR UART (np. GM65/Waveshare), a moduł typu Waveshare ESP32-S3-Relay-6CH daje przekaźniki i wbudowany RS485 pod etap 2. W cenie: firmware, schemat, BOM, instrukcja i przeniesienie praw autorskich.

Brakuje do startu: kontrakt API logów (endpoint, format, autoryzacja, offline/retry), zawartość QR i mapowanie QR → sekcja oraz informacja, kto kupuje podzespoły i jakie są warunki outdoor/zasilanie.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wybrałem ESP32, a nie Raspberry Pi, bo do tej logiki, HTTP i UART nie potrzeba systemu operacyjnego, a ESP32 jest tańszy, prostszy i lepiej pasuje do pracy ciągłej; Pi miałby sens tylko przy lokalnym przetwarzaniu obrazu z kamery, czego nie rekomenduję. Czytnik QR po UART zamiast ESP32-CAM to nie zgadywanie, tylko świadoma decyzja: ESP32-CAM ma za mało SRAM do stabilnego dekodowania QR, a dedykowany moduł zwraca gotowy string i upraszcza firmware. Nie dopisałem na siłę funkcji spoza zakresu – API, zawartość QR i mapowanie QR→sekcja nadal są po stronie ustaleń, dlatego start jest warunkowy. Kwota pracy 5 800–7 500 zł (50–65 h × 115 zł/h) jest nadal realna dla prototypu z dokumentacją i przekazaniem praw. Koryguję tylko BOM: jeśli elektromagnesy i zasilacz 12 V są po mojej stronie, realniej 800–1 500 zł; jeśli po Waszej – zostaje 400–700 zł.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 6600,
  "kwota_gorna": 9500,
  "definitywna": false,
  "od_czego_zaleza": [
    "Kontrakt API logów: endpoint, format JSON, autoryzacja oraz zachowanie offline (bufor lokalny + retry/backoff).",
    "Zawartość QR i mapowanie QR na sekcję: co koduje QR i czy firmware ma lokalną tablicę, czy pyta API.",
    "Kto kupuje podzespoły i czy w zakresie są elektromagnesy 12 V, zasilacz outdoor IP65 oraz obudowa.",
    "Warunki środowiskowe: IP, temperatura, zasilanie na miejscu i wymagany poziom zabezpieczeń.",
    "Dostępność części i termin startu po zamknięciu specyfikacji API/QR."
  ],
  "dni_od": 10,
  "dni_do": 18,
  "uzasadnienie": "Modele zgodnie rekomendują ESP32, dedykowany czytnik QR po UART zamiast ESP32-CAM oraz modularność pod RS485 na etap 2. Zbieżność prac to ok. 5,8-8,0 tys. zł netto, a podzespołów ok. 0,8-1,5 tys. zł netto, co daje łącznie 6,6-9,5 tys. zł netto. Rozbieżność dotyczy głównie górnej granicy prac (A początkowo do 10 tys. zł) i BOM w zależności od tego, kto kupuje części. Wycena jest widełkowa, bo API, zawartość QR, mapowanie na sekcję i warunki outdoor pozostają nieustalone."
}

=== FINALNA WYCENA ===
6600-9500 zl netto | 10-18 dni | WIDELKI
Od czego zalezy: Kontrakt API logów: endpoint, format JSON, autoryzacja oraz zachowanie offline (bufor lokalny + retry/backoff)., Zawartość QR i mapowanie QR na sekcję: co koduje QR i czy firmware ma lokalną tablicę, czy pyta API., Kto kupuje podzespoły i czy w zakresie są elektromagnesy 12 V, zasilacz outdoor IP65 oraz obudowa., Warunki środowiskowe: IP, temperatura, zasilanie na miejscu i wymagany poziom zabezpieczeń., Dostępność części i termin startu po zamknięciu specyfikacji API/QR.
Uzasadnienie rozjemcy: Modele zgodnie rekomendują ESP32, dedykowany czytnik QR po UART zamiast ESP32-CAM oraz modularność pod RS485 na etap 2. Zbieżność prac to ok. 5,8-8,0 tys. zł netto, a podzespołów ok. 0,8-1,5 tys. zł netto, co daje łącznie 6,6-9,5 tys. zł netto. Rozbieżność dotyczy głównie górnej granicy prac (A początkowo do 10 tys. zł) i BOM w zależności od tego, kto kupuje części. Wycena jest widełkowa, bo API, zawartość QR, mapowanie na sekcję i warunki outdoor pozostają nieustalone.
