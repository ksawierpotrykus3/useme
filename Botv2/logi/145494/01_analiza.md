``` 
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy – prototyp MVP embedded/IoT, z opcją etapu 2 (waga) i dalszej współpracy
INTENCJA: mieszane (wykonawcze + doradcze w doborze ESP32/Pi i architekturze)
DECYDENT_I_BOL: Decydent nieujawniony; prawdopodobnie firma/osoba wdrażająca kontrolę dostępu do urządzeń zewnętrznych, z backendem/API po swojej stronie. Ból: potrzebny działający prototyp do weryfikacji logiki dostępu, QR, sterowania elektromagnesami i logowania zdarzeń bez budowy serwera; prostota, dokumentacja, prawa autorskie; etap 2 wymusza modularność już teraz.
WYKONALNE: TAK. Najbliższa opcja: ESP32 jako centralka do prostego sterowania i logów HTTP; jeśli QR ma być kamerą i cięższym przetwarzaniem – Raspberry Pi albo ESP32-CAM/zewnętrzny czytnik. Wstępnie: ESP32 + dedykowany czytnik QR UART/USB + driver 12 V (przekaźnik/MOSFET) + kontaktron + PIR + bufor logów + rezerwa UART/RS485/USB pod etap 2.
POLE_DO_POPISU: JEST. Wybór ESP32 vs Pi, stopień wykonawczy 12 V, separacja/zasilanie, obudowa outdoor, modularność pod RS485/USB, kontrakt API i retry.
SCIEZKA_MERYTORYKI: A (klient wprost pyta o podejście/ESP32 vs Pi; elementy B tylko dla standardowych min sprzętowych, bez straszenia)
MINY_I_CIEKAWOSTKI:
- Dowód: „sterowanie 2–3 elektromagnesami 12 V” – nie podłącza się ich wprost do GPIO; potrzebny driver, osobne zasilanie 12 V, diody gaszące, separacja. To zakres doboru elektroniki, nie odmowa.
- Dowód: „centralka ESP32 lub Raspberry Pi — do ustalenia” – wybór wpływa na koszt, pobór, złożoność i możliwość kamery QR. Proponuję ESP32 dla prostoty; Pi tylko jeśli kamera/wideo lub cięższe przetwarzanie.
- Dowód: „odczyt QR: kamera, czytnik lub inne uzgodnione rozwiązanie” – kamera na ESP32 bywa ograniczona pamięciowo; dedykowany czytnik UART/USB zwykle prostszy i pewniejszy w prototypie.
- Dowód: „praca w warunkach zewnętrznych; zabezpieczenie elektroniki do ustalenia” – prototyp outdoor wymaga obudowy, złączy, ochrony przepięciowej i zasilania; zakres do ustalenia.
- Dowód: „wysyłanie logów przez HTTP do uzgodnionego API” – trzeba zdefiniować endpoint, format, auth, retry i bufor offline; inaczej firmware nie będzie gotowy na start.
ODMOWA: BRAK twardej odmowy. Wszystko wykonalne; ograniczenia to decyzje projektowe, nie blokady.
PYTANIA:
1. Jaki jest kontrakt API dla logów: endpoint, format, autoryzacja, oczekiwany sposób obsługi braku sieci (bufor/retry)? – bez tego nie ruszę implementacji; wycena ogólna możliwa, ale start wymaga specyfikacji.
2. Czy QR ma być czytany kamerą, czy dedykowanym czytnikiem (UART/USB)? – proponuję czytnik dla prostoty; jeśli kamera, zmieni się platforma i koszt.
CO_ZLECENIE_MOWI: prototyp MVP IoT do kontroli dostępu do urządzeń zewnętrznych; zakres: elektronika + firmware, bez web/mobile/backend; centralka ESP32 lub Raspberry Pi do ustalenia; sterowanie 2–3 elektromagnesami 12 V; czujnik drzwi indukcyjny/kontaktron; PIR; odczyt QR (kamera/czytnik/inne); logika: aktywacja po otwarciu drzwi, podtrzymanie ruchem, timeout, identyfikacja QR, otwarcie sekcji, logi HTTP bez serwera; QR i API do ustalenia przed startem; etap 2: waga platformowa, rezerwa RS485/UART/USB, nieimplementowana teraz; prototyp, prostota, praca outdoor, zabezpieczenie do ustalenia; oczekiwania: doświadczenie, propozycja podejścia ESP32 vs Pi, wycena prac i podzespołów osobno, dostępność/czas, kod, schemat, BOM, instrukcja, przeniesienie praw autorskich; możliwa dalsza współpraca.
CZEGO_NIE_MOWI: kto jest decydentem; jaki dokładnie jest kontrakt API; jaki dokładnie sposób weryfikacji QR; budżet poza „do negocjacji”; termin startu/deadline; czy podzespoły, zasilanie i obudowa są po stronie klienta czy wykonawcy; warunki środowiskowe (IP, temperatura, zasilanie na miejscu); czy QR/logi to dane osobowe/RODO; wymagania etapu 2 co do protokołu wagi.
GRANICA_CIECIA: długość średnia – zlecenie ma konkretny zakres, ale kilka otwartych decyzji; głębokość do poziomu rekomendacji ESP32 vs Pi, doboru driverów 12 V, QR i API jako warunków startu oraz modularności pod etap 2. Nie wchodzić w backend, nie zgadywać API, nie dopisywać funkcji.
RESEARCH_POTRZEBNY: TAK – do doboru konkretnych modułów ESP32, czytników QR UART/USB, driverów 12 V, transceiverów RS485 i obudów outdoor oraz do wyceny BOM; research zostaje dla mnie, nie wchodzi do oferty jako wykład.
```