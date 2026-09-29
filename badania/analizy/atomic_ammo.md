# ATOMIC AMMO — 16 killshotów technologicznych
**STATUS: AKTUALNE (materiał)** | Esencja z 16 kart wiedzy. Jedno zdanie na niszę, gotowe do wplecenia w ofertę. Źródło: badania/analizy/technologie/baza_wiedzy/.

| Karta | Nisza | Killshot |
|:---|:---|:---|
| tech_01 | Scraping & WAF | Zamiast ciezkiego headless Chrome stosujemy patchowany handshake TLS/JA4 z rotacja sesyjnych IP i filtrem Blooma w Redis, co utrzymuje czas detekcji ponizej 3 minut 40 sekund bez ryzyka blokady 403. |
| tech_02 | Optima ERP | Wymiane danych realizujemy przez bezlicencyjny import XML Pracy Rozproszonej z walidacja sumy kontrolnej podatku z dokladnoscia do 1 grosza, z pominieciem bezposrednich insertow SQL do bazy Comarch. |
| tech_03 | Subiekt Sfera | Operacje na kartotekach i dokumentach prowadzimy wylacznie przez obiekty biznesowe Sfery dla Subiekta GT/nexo, gwarantujac integralnosc stanow magazynowych. |
| tech_04 | Python & API | Obsluge webhookow zabezpieczamy asynchroniczna kolejka z algorytmem Leaky Bucket, co eliminuje bledy 429 i gubienie powiadomien przy spietrzeniach ruchu. |
| tech_05 | Kotlin Android | Architektura oparta o Jetpack Compose z offline-first w Room DB i szyfrowaniem kluczy w Android Keystore, gwarantujaca natychmiastowy start bez czekania na siec. |
| tech_06 | Flutter | Pojedyncza baza kodu Dart z odseparowana warstwa logiki w BLoC i natywnymi kanalami platformowymi (MethodChannel), co zapobiega gubieniu klatek na animacjach. |
| tech_07 | Swift iOS | Natywny SwiftUI z twardym zarzadzaniem cyklem zycia pamieci VRAM i asynchronicznym parsowaniem danych w tle, bez drenowania baterii. |
| tech_08 | DevOps / Docker | Konteneryzacja w minimalnych obrazach Alpine/Distroless, staging odseparowany od produkcji i automatyczny rollback przy bledzie healthchecka. |
| tech_09 | Bazy SQL | Eliminacja waskich gardel przez pesymistyczne blokowanie slotow (SELECT FOR UPDATE) i pokrywajace indeksy kompozytowe, eliminujace race condition przy platnosciach. |
| tech_10 | Node.js / Nest | Modularny backend w NestJS z walidacja DTO przez class-validator i pelna typizacja TypeScript, odporny na niekompletne payloady z zewnetrznych bramek. |
| tech_11 | C# / .NET | Wysokowydajne serwisy na .NET 8 z przetwarzaniem strumieniowym (System.IO.Pipelines) i bezposrednia komunikacja z szyna danych bez narzutu refleksji. |
| tech_12 | VoIP Asterisk | Konfiguracja trunkow SIP z optymalizacja jitter buffer i bezpiecznym trasowaniem polaczen w AMI/ARI bez opoznien audio. |
| tech_13 | Enova365 / Odoo | Integracja z Enova365 poprzez dedykowane harmonogramy zadan Soneta i serwis integracyjny XML, zabezpieczajacy transakcje magazynowe. |
| tech_14 | Google Apps Script | Skrypty optymalizowane pod 6-minutowy limit wykonania Google Workspace z przetwarzaniem wsadowym i buforowaniem w CacheService. |
| tech_15 | AI / LLM / RAG | Rozdzielenie ekstrakcji semantycznej od matematyki biznesowej — model Vision wyciaga dane, a sztywny skrypt weryfikuje sumy i NIP w rejestrach panstwowych. |
| tech_16 | Tech-Agnostic | Wdrozenie realizujemy wylacznie na bezpiecznym serwerze testowym — obecna strona, maile i systemy dzialaja bez minuty przestoju az do finalnego odbioru. |

## Uwaga metodologiczna
Karty źródłowe mają po 15-25 KB. Wstrzykiwanie całej karty do slotu generowania przeładowuje kontekst. Ten plik to skondensowana amunicja — używaj jego, nie całych kart.