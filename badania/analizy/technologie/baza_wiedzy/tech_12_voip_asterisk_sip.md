# KARTA WIEDZY INŻYNIERSKIEJ — VoIP / ASTERISK / PJSIP / CALL CENTER AI

**Wersja:** 2026.04 | **Klasyfikacja:** Wewnętrzna baza wiedzy bota ofertowego | **Status:** Produkcyjna


## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

**Segmentacja zleceń:**

| Typ zlecenia | Budżet (zł) | Częstotliwość | Win Rate | Kluczowy decydent |
|---|---|---|---|---|
| Konfiguracja trunkingu SIP (1-3 trunków) | 2 500 – 4 000 | Wysoka | 45% | Właściciel małej firmy, 5-20 numerów |
| Migracja chan_sip → PJSIP (Asterisk 18/20 → 22+) | 3 000 – 6 000 | Rosnąca | 35% | Administrator IT lub integrator |
| IVR + kolejka + CRM (webhook) | 4 000 – 7 000 | Średnia | 40% | Manager call center, 5-15 agentów |
| Transkrypcja AI + dashboard QA | 6 000 – 10 000 | Niska | 30% | Head of Customer Success, 15-50 agentów |

**Profil zleceniodawcy — kluczowe cechy:**
- W 70% przypadków klient jest nietechniczny — nie odróżnia SIP od RTP, nie zna pojęcia „trunk”. Używa sformułowań: „chcę dzwonić z komputera”, „telefon nie łączy”, „potrzebuję żeby się nagrywało i wysyłało do CRM”.
- W 30% przypadków klient jest techniczny (administrator IT, integrator) i oczekuje konkretnych parametrów: wersja Asterisku, typ trunkingu (PJSIP vs DAHDI), model transkodowania, architektura ARI.
- Budżety poniżej 2 500 zł dotyczą wyłącznie prostych konfiguracji (single trunk, 2-3 extensiony) — nie warto angażować zasobów.
- Zlecenia powyżej 10 000 zł wymagają zazwyczaj obecności na miejscu (serwerownia, rack) — poza zakresem zdalnym bota.


## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1. Chan_sip vs PJSIP — sytuacja bez odwrotu

`chan_sip` został **oficjalnie usunięty w Asterisk 21** i wszystkich późniejszych wersjach (22, 23+). Asterisk 21 znajduje się w statusie Security Fix Only do października 2026 — po tej dacie nie otrzyma żadnych aktualizacji, w tym bezpieczeństwa. Asterisk 18 jest End of Life i nie otrzymuje nawet łatek bezpieczeństwa.

**Konsekwencja ofertowa:** Każde zlecenie na Asterisku 18 lub 20 wymaga weryfikacji, czy dialplan nie zawiera składni `Dial(SIP/...)` — jeśli tak, migracja na `Dial(PJSIP/...)` jest obowiązkowa przed upgrade'em. Oferta bez tego rozpoznania jest ofertą niekompletną.

### 2.2. NAT i zakres portów RTP

Asterisk domyślnie używa zakresu **UDP 10000–20000** dla strumieni RTP. Nowa funkcjonalność PJSIP (pull request z kwietnia 2026) pozwala na konfigurację `rtp_port_start` i `rtp_port_end` **per endpoint**, co nadpisuje globalne ustawienie w `rtp.conf`. To istotne przy wielu trunkach i wielu instancjach Asterisku za jednym NAT-em — pozwala uniknąć konfliktów portów.

**Krytyczne parametry konfiguracyjne:**
- `externip` / `externhost` — musi być aktualny; nieaktualny IP w SDP powoduje kierowanie RTP na nieosiągalny adres.
- `localnet` — definiuje sieć wewnętrzną; brak tej dyrektywy powoduje, że Asterisk nie rozpoznaje ruchu wewnętrznego i traktuje go jako zewnętrzny.
- **SIP ALG** na routerze — musi być **wyłączony**; włączony SIP ALG psuje negocjację NAT i powoduje one-way audio.

### 2.3. Kodeki — Opus vs G.711

| Kodek | Przepustowość (z narzutem RTP) | Zastosowanie | Transkodowanie |
|---|---|---|---|
| G.711 (PCMU/PCMA) | ~80–90 kbps | Trunki operatorskie, PSTN | Nie — natywny dla większości trunków |
| Opus | ~16–64 kbps (adaptacyjny) | WebRTC, softphony, wewnętrzne | Tak — wymaga transkodowania na G.711 dla PSTN |
| G.729 | ~24–32 kbps | Rzadko — licencja komercyjna | Tak |

**Strategia produkcyjna:** Dla trunków operatorskich — wyłącznie G.711. Dla WebRTC — Opus z fallbackiem na G.711. Transkodowanie Opus↔G.711 obciąża CPU i wprowadza opóźnienie — przy >20 jednoczesnych kanałach wymaga dedykowanego planowania wydajności.

### 2.4. Interfejsy ARI i AMI

- **AMI (Asterisk Manager Interface)** — TCP, model klient-serwer, do zarządzania PBX, monitorowania kanałów i kolejek. Odpowiedni dla call center, logowania, event-driven call control.
- **ARI (Asterisk REST Interface)** — asynchroniczny REST + WebSocket, do budowy aplikacji komunikacyjnych z surowymi obiektami (kanały, bridge, endpointy). **Preferowany dla integracji z CRM i AI** — pozwala na kontrolę pojedynczych kanałów w czasie rzeczywistym.
- **AEAP (Asterisk External Application Protocol)** — dedykowany protokół do implementacji silników speech-to-text podłączonych jako zewnętrzna aplikacja. Kluczowy dla transkrypcji na żywo.

**Uwaga inżynierska:** Kolejność zdarzeń w AMI i ARI nie jest gwarantowana — aplikacja monitorująca musi być odporna na out-of-order events.


## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1. One-Way Audio — problem numer jeden

Klient zgłasza: „rozmowa się łączy, ale ja nie słyszę dzwoniącego” lub „klient mnie nie słyszy”. To **najczęściej zgłaszany problem** w produkcyjnych wdrożeniach SIP.

**Przyczyna:** SIP signaling (port 5060) i RTP media (dynamiczny port UDP) biegną dwiema osobnymi ścieżkami sieciowymi. Gdy Asterisk za NAT-em reklamuje w SDP swój prywatny adres IP, zdalny endpoint wysyła RTP na adres nieosiągalny.

**Rozwiązanie:** `externip`/`externhost` + `localnet` + `direct_media=no` + wyłączony SIP ALG. Sam `nat=` w konfiguracji bez poprawnego `externip` nie rozwiąże problemu — trzeba naprawić obie warstwy (signaling i media).

### 3.2. Włamania na port 5060 i toll fraud

**Każdy serwer z otwartym portem 5060 otrzymuje próby rejestracji SIP w ciągu kilku godzin od wystawienia na publiczny internet** — automatyczne skanery działają 24/7. Brak fail2ban + słabe hasła = rachunek na tysiące euro w ciągu jednej nocy.

**Warstwy ochrony (2026):**
- **TLS na porcie 5061** zamiast plain SIP na 5060.
- **SRTP** dla szyfrowania strumienia głosowego.
- **Fail2Ban lub CrowdSec** — automatyczne banowanie IP po nieudanych próbach autoryzacji.
- **VPN dla zdalnych extensionów** (Tailscale / WireGuard / ZeroTier) zamiast wystawiania portów SIP.
- **Silne hasła, brak domyślnych extensionów** — ataki wciąż kończą się sukcesem z powodu słabych poświadczeń.

### 3.3. Transkodowanie jako ukryty koszt

Klient chce WebRTC (przeglądarka, Opus) i jednocześnie dzwonić na PSTN przez trunek operatorski (G.711). Każda taka rozmowa wymaga transkodowania na CPU. Przy 30 jednoczesnych kanałach to różnica między serwerem 2 vCPU a 8 vCPU — klient tego nie uwzględnił w budżecie infrastruktury.


## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

**Dla klienta nietechnicznego (70% przypadków):**

> „Problem, który opisujesz — dzwonienie z przeglądarki i odbieranie na telefonie stacjonarnym — to w 80% przypadków kwestia tego, że Asterisk za NAT-em wysyła do operatora swój wewnętrzny adres IP zamiast publicznego, przez co audio idzie tylko w jedną stronę. Naprawa wymaga poprawnego `externip` w PJSIP i wyłączenia SIP ALG na routerze — to dwie osobne warstwy, których amatorzy nie rozdzielają.”

**Dla klienta technicznego (30% przypadków):**

> „Zakładam, że mówimy o migracji z Asterisk 18/20, gdzie `chan_sip` już nie istnieje w wersji 21+ — dialplan z `Dial(SIP/...)` wymaga konwersji na `Dial(PJSIP/...)` przed upgrade'em. Jeśli dodatkowo planujesz WebRTC z Opus, przy >20 kanałach transkodowanie na G.711 dla trunkingu operatorskiego wymaga osobnego planu CPU i ewentualnie dedykowanego serwera mediów.”


## 5. CZERWONA LISTA / ANTYWZORCE

**Czego kategorycznie nie pisać w ofercie:**

1. **„Znam się na Asterisku”** — zero wartości merytorycznej. Zamiast tego: „Wdrożyłem X instancji PJSIP z trunkingiem operatorskim i konfiguracją NAT w scenariuszach za CGNAT”.
2. **„Skonfiguruję SIP”** — zbyt ogólne. Zamiast tego: „Konfiguracja PJSIP endpointów z `allow=ulaw,alaw`, `direct_media=no`, `rtp_symmetric=yes` i weryfikacją `externip` w `pjsip.conf`”.
3. **„Zrobię IVR”** — klient nie wie, co to IVR. Zamiast tego: „Zaprojektuję menu głosowe (naciśnij 1, aby…), które przekieruje rozmowy do właściwych działów i zapisze każdy wybór w CRM”.
4. **Proponowanie spotkania wideo / rozmowy telefonicznej** — komunikacja wyłącznie pisemna na priv. Zero wyjątków.
5. **Wycena ryczałtowa bez rozbicia** — „3 500 zł za całość” bez modułów jest nieczytelna i rodzi pytania. Klient chce widzieć, za co płaci.
6. **Ignorowanie bezpieczeństwa** — brak wzmianki o fail2ban, TLS, SRTP w ofercie dla klienta z publicznym IP to czerwona flaga dla świadomego odbiorcy.
7. **„Użyję chan_sip”** — chan_sip nie istnieje w Asterisk 21+. Każda wzmianka o nim w 2026 roku to dowód nieaktualnej wiedzy.


## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 3 500 – 9 000 zł)

### Moduł 1: Audyt i plan sieciowy (500 – 800 zł)
- Inwentaryzacja istniejącej infrastruktury (wersja Asterisku, `modules.conf`, `sip.conf`/`pjsip.conf`).
- Weryfikacja `externip`, `localnet`, zakresu RTP w `rtp.conf`.
- Sprawdzenie obecności i konfiguracji fail2ban, TLS, SRTP.
- **Deliverable:** raport z mapą portów, rekomendacją zakresu RTP i planem migracji PJSIP (jeśli dotyczy).

### Moduł 2: Trunking operatorski + PJSIP (1 200 – 2 000 zł)
- Konfiguracja `pjsip.conf`: transport (UDP/TCP/TLS), endpoint trunka, AOR, auth.
- Konfiguracja `Dial(PJSIP/...)`, prefiksy, obsługa DDI/DID.
- Kodeki: `allow=ulaw,alaw`, `disallow=all`, `direct_media=no`.
- Testy rejestracji, obsługa NAT z `externip` i `localnet`.
- **Deliverable:** działający trunk z poprawnym routingiem przychodzącym i wychodzącym.

### Moduł 3: IVR + kolejka call center (1 500 – 2 500 zł)
- Menu głosowe (IVR) z `Background()` i `Goto()` w `extensions.conf`.
- Kolejka z `Queue()` — strategia ringall, timeout, muzyka na czekanie.
- Automatyczny zapis nagrań do dedykowanego katalogu z timestampem.
- **Deliverable:** działające IVR z routingiem do działów i nagrywaniem rozmów.

### Moduł 4: Integracja CRM + transkrypcja AI (2 000 – 3 500 zł)
- **Webhook do CRM:** przy każdym odebranym połączeniu Asterisk wysyła POST z numerem dzwoniącego, czasem trwania i linkiem do nagrania.
- **Transkrypcja wsadowa (batch):** nagrania po zakończeniu rozmowy trafiają do Whisper (OpenAI API lub lokalny `whisper.cpp`) lub Deepgram Nova-2. Format wyjściowy: JSON z timestampami i speaker diarization.
- **Transkrypcja w czasie rzeczywistym (opcjonalnie):** AudioSocket + Deepgram WebSocket streaming — surowe audio (resampling do 16 kHz) strumieniowane do usługi STT z opóźnieniem 1–5 sekund.
- **Dashboard QA:** prosty widok (FastAPI + WebSocket) z transkrypcją na żywo, wskaźnikiem sentymentu i alertami na słowa kluczowe.
- **Deliverable:** integracja CRM + pipeline transkrypcji z dashboardem (jeśli wybrany wariant real-time).

### Moduł 5: Hardening bezpieczeństwa (500 – 1 000 zł)
- Konfiguracja fail2ban dla PJSIP (`/etc/fail2ban/jail.d/asterisk-iptables.local` z portem 5060/5061).
- Włączenie TLS (port 5061) i SRTP.
- ACL dla endpointów (ograniczenie do `localnet`).
- **Deliverable:** raport z konfiguracją fail2ban, TLS i reguł firewall.

**Łączna wycena modułowa:** 5 700 – 9 800 zł. Dla klientów z ograniczonym budżetem — Moduły 1+2+5 (audyt + trunking + security) od 2 200 zł.


## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU

**Pytanie 1 — weryfikacja wersji i migracji (dla klientów technicznych):**
> „Czy Twój Asterisk działa na wersji 18/20 (z chan_sip), czy już na 21+? Jeśli starsza — czy masz świadomość, że `Dial(SIP/...)` w dialplanie przestanie działać po upgrade i wymaga konwersji na `Dial(PJSIP/...)`? To determinuje zakres prac migracyjnych.”

**Pytanie 2 — weryfikacja NAT (dla wszystkich):**
> „Czy Asterisk stoi za routerem NAT (większość przypadków), czy ma publiczny adres IP bezpośrednio na interfejsie? Jeśli za NAT — czy router ma wyłączony SIP ALG i czy `externip` jest aktualny? Bez tego każda konfiguracja trunkingu może zakończyć się one-way audio.”

**Pytanie 3 — weryfikacja transkrypcji (dla zleceń z AI):**
> „Czy transkrypcja ma być wsadowa (po zakończeniu rozmowy, tańsza, dokładniejsza) czy w czasie rzeczywistym (podgląd na żywo, wyższy koszt GPU/API)? To determinuje architekturę — batch korzysta z Whisper large-v3, real-time wymaga AudioSocket + Deepgram WebSocket.”


**Uwagi końcowe dla operatora bota:**
Karta jest zgodna ze stanem wiedzy na kwiecień 2026. W przypadku zleceń, w których klient nie potrafi odpowiedzieć na żadne z pytań kwalifikujących — oznacza to, że wymaga pełnego audytu (Moduł 1) przed jakąkolwiek wyceną. Nie składaj oferty bez tego kroku.