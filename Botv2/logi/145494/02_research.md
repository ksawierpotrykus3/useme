## 1. Moduły ESP32 do sterowania przekaźnikami / elektromagnesami 12 V

**Gotowe moduły przekaźnikowe z ESP32 na pokładzie:**

| Moduł | Kanały | Obciążalność styków | Zasilanie | Uwagi |
|---|---|---|---|---|
| SEEIT ESP32-RELAY01/02/04/08 | 1/2/4/8 | 10 A / 250 VAC lub 10 A / 30 VDC | 5 VDC (MicroUSB) lub 7–60 VDC (terminal) | ESP32-WROOM-32E, 4 MB flash; wyprowadzone wszystkie piny ESP32 na złączu HE10 |
| Waveshare ESP32-S3-Relay-6CH | 6 | ≤10 A / 250 VAC / 30 VDC | 7–36 VDC (terminal) lub USB-C | ESP32-S3 dual-core 240 MHz; wbudowany izolowany RS485, izolacja optoeparatorowa i zasilania; obudowa ABS na szynę DIN; złącze 40-pin kompatybilne z Pico HAT |

**Ważne dla elektromagnesów 12 V:** Przekaźniki w tych modułach mają styki przystosowane do 30 VDC / 10 A, co pozwala na bezpośrednie przełączanie elektromagnesów 12 V (typowy elektromagnes 12 V pobiera 0,5–1 A). **Jednak elektromagnes jest obciążeniem indukcyjnym** — wymaga diody gaszącej (flyback) równolegle do cewki, inaczej napięcie indukowane przy wyłączaniu zniszczy styk przekaźnika lub tranzystor sterujący. Przy przekaźniku dioda powinna być na cewce elektromagnesu, nie na cewce przekaźnika.

**Alternatywa MOSFET:** Jeśli zamiast przekaźnika stosowany jest klucz MOSFET do sterowania elektromagnesem, ESP32 (logika 3,3 V) wymaga **logic-level MOSFET** z gwarantowanym Rds(on) przy Vgs ≤ 3,0 V. Standardowe MOSFET-y jak IRF540N czy część wersji IRFZ44N wymagają Vgs = 10 V do pełnego włączenia — przy 3,3 V z GPIO pracują w obszarze liniowym, grzeją się i ulegają uszkodzeniu. Wymagane są: rezystor bramkowy 20–100 Ω, rezystor pull-down 10–100 kΩ na bramce oraz dioda flyback na cewce elektromagnesu (katoda do +12 V, anoda do drenu MOSFET).

## 2. Czytniki QR z interfejsem UART — alternatywa dla kamery na ESP32

**Ograniczenia ESP32-CAM przy odczycie QR:**
- ESP32 ma ~520 KB SRAM; przy rozdzielczości VGA (640×480) pojawiają się błędy pamięci przy dekodowaniu QR.
- Testy praktyczne wykazały, że nawet z zewnętrznym PSRAM 4 MB płytka ESP32-CAM „nie jest wystarczająco wydajna, by zbudować cokolwiek użytecznego" do przetwarzania obrazu na pokładzie.
- Wniosek: **dedykowany czytnik QR z UART jest prostszy, pewniejszy i nie angażuje zasobów ESP32.**

**Konkretne moduły czytników QR z UART:**

| Moduł | Interfejs | Specyfikacja | Cena / dostępność |
|---|---|---|---|
| **GM65** QR & Barcode Scanner Module | UART | Powszechnie stosowany z ESP32; wymaga konfiguracji przez skanowanie kodów z instrukcji producenta, aby przełączyć na tryb UART/TTL | Dostępny (DFRobot i in.) |
| **Waveshare Round 2D Codes Scanner Module** | UART (9600 8N1 domyślnie) | Rozdzielczość 640×480; QR, DataMatrix, PDF417, EAN-13 i in.; IP54 (front); zasilanie 3,3 V / 120 mA; temp. pracy −30 do +70 °C; ochrona ESD 6 kV | ~35,70 USD (RobotShop) |

**Uwaga integracyjna:** Czytnik Waveshare komunikuje się po UART z ESP32 i zwraca gotowy string — nie wymaga przetwarzania obrazu na MCU. To eliminuje potrzebę kamery i całkowicie rozwiązuje problem pamięci ESP32-CAM.

## 3. Transceivery RS485 do etapu 2 (modularność pod wagę platformową)

Wymaganie etapu 2 mówi o „rezerwie RS485 / UART / USB". Poniżej konkretne opcje dla ESP32:

| Moduł | Układ | Zasilanie | Prędkość | Uwagi |
|---|---|---|---|---|
| **Boardoza RS485 3V3 Transceiver Breakout** | HTC Korea MAX485 | 3,3 V (natywna zgodność z ESP32) | do 10 Mbps | Automatyczna kontrola przepływu (bez pinów RE/DE); półdupleks; wbudowana odporność na zakłócenia; złącza śrubowe / 4-pin header; temp. pracy −10 do +70 °C |
| **Waveshare ESP32-S3-Relay-6CH** (wbudowany RS485) | Izolowany RS485 | 7–36 VDC | — | Moduł przekaźnikowy z **już zintegrowanym izolowanym RS485** — jeśli wybrany zostanie ten moduł, rezerwa RS485 jest wbudowana bez dodatkowego komponentu |
| **LILYGO T-CAN485** | ESP32 + transceivery CAN i RS485 | — | — | Płytka deweloperska z ESP32 i oboma interfejsami przemysłowymi |

**Wybór zależy od architektury:** jeśli w etapie 1 stosowany jest zwykły ESP32 (np. WROOM-32E) na płytce stykowej lub dedykowanym PCB, transceiver Boardoza MAX485 jest najprostszym rozwiązaniem — 3,3 V, automatyczny przepływ, bez dodatkowych pinów sterujących. Jeśli wybrany zostanie moduł Waveshare z wbudowanym RS485, rezerwa jest gotowa od razu.

## 4. Obudowy outdoor IP65 i zasilanie 12 V

**Obudowy IP65:**

| Produkt | Wymiary | Materiał | Cechy | Cena orientacyjna |
|---|---|---|---|---|
| R-TECH 524325 | 115 × 65 × 40 mm | Poliwęglan | IP65, uszczelka neoprenowa, UV-stabilny, temp. −40 do +120 °C, UL94-HB; wewnętrzne prowadnice PCB | ~£7,09 (1 szt.) |
| R-TECH 524326 | 160 × 80 × 55 mm | Poliwęglan | Jak wyżej, większa | — |
| LeMotech F4-2 | 240 × 120 × 75 mm | ABS | IP65, odporny na kurz i zachlapania, do PCB | — |
| Bud Industries PN-1346 | ~354 × 244 × 104 mm | — | IP65 / NEMA 4X, przemysłowa | — |

**Zasilanie 12 V outdoor:**
- **Dycon IP65 Power Solutions** — obudowa IP65 z zasilaczem 12 VDC / 0,5–10 A, opcjonalnie z baterią i ładowaniem; ABS odporny na uderzenia (IK07/8); automatyczny zawór odpowietrzający dla gazów bateryjnych; uchwyty montażowe bez wiercenia obudowy; opcja czujnika antysabotażowego.
- **ALPHIoT POWER** — gotowy outdoorowy box zasilający z wyjściami 3,3 V / 5 V / 12 V, bateria litowo-tionylowa (żywotność do 10 lat), IP65, temp. −20 do +60 °C; dedykowany dla IoT w trudnych warunkach.

**Uwaga:** Cena ALPHIoT nie jest publicznie podana — „szczegóły na zapytanie". Dycon to produkt brytyjski, dostępny przez dystrybutorów.

## Podsumowanie dla wykonawcy

- **ESP32 (WROOM-32E lub S3) + gotowy moduł przekaźnikowy** — najprostsza droga do sterowania elektromagnesami 12 V. Jeśli wybrany zostanie Waveshare ESP32-S3-Relay-6CH, otrzymuje się jednocześnie przekaźniki, RS485 (etap 2) i obudowę ABS na szynę DIN.
- **Dedykowany czytnik QR UART (GM65 lub Waveshare)** zamiast kamery ESP32-CAM — eliminuje problem pamięci i upraszcza firmware.
- **Dioda flyback na każdej cewce elektromagnesu** — obowiązkowa, niezależnie od tego, czy sterowanie odbywa się przez przekaźnik, czy MOSFET.
- **Transceiver RS485 (np. Boardoza MAX485 3V3)** — jeśli moduł ESP32 nie ma wbudowanego RS485, zapewnia rezerwę pod wagę platformową w etapie 2.
- **Obudowa IP65 z poliwęglanu** (np. R-TECH) + **zasilanie 12 V w obudowie IP65** (Dycon lub podobne) — kompletny zestaw outdoorowy do prototypu.

**Niepotwierdzone:** Dokładne ceny BOM dla wszystkich komponentów (część cen pochodzi z pojedynczych źródeł i może się różnić w zależności od dostawcy i ilości); kompatybilność konkretnych modułów czytnika QR z ESP32 (GM65 — potwierdzona w forach, ale nie w oficjalnej dokumentacji producenta); dostępność ALPHIoT w Polsce.