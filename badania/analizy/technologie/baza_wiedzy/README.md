# Baza Wiedzy Inżynieryjnej i Taktycznej Strefy 2 (Useme B2B)

Baza wiedzy inżynieryjnej stanowi elitarny korpus merytoryczny i taktyczny dla automatycznego bota ofertującego (`kod/`). Pokrywa **100% zleceń inżynieryjnych poza stronami WWW** ($n=343$ z $N=470$ w bazie empirycznej Useme), w tym $188$ zleceń czysto technicznych oraz $155$ zleceń Tech-Agnostic (33% rynku).

---

## 1. Architektura Zasobów

```
badania/analizy/technologie/baza_wiedzy/
├── README.md                                    # Niniejszy katalog i protokół routingu
├── dzwignie_psychologia_merytoryka_wyceny.md    # Dźwignie psychologiczne, autorytet, wyceny
├── audyt_krytyczny_red_team.md                  # Bezwzględny audyt Red Team (co działa, co odrzucono)
│
├── synteza_bojowa_01_erp.md                     # Synteza Grupy 1: ERP & Integracje (tech_02, 03, 13)
├── synteza_bojowa_02_automatyzacje_i_backend.md # Synteza Grupy 2: Scraping & Backend (tech_01, 04, 09, 10, 11)
├── synteza_bojowa_03_mobile_hardware.md         # Synteza Grupy 3: Mobile & Hardware (tech_05, 06, 07, 12)
├── synteza_bojowa_04_infra_ai_biznes.md         # Synteza Grupy 4: DevOps, Arkusze, AI & Tech-Agnostic (tech_08, 14, 15, 16)
│
├── tech_01_scraping_i_boty.md                   # Web Scraping, Boty, Anti-Bot Bypass
├── tech_02_comarch_optima_ksef.md               # Comarch ERP Optima, KSeF 2.0 FA(3), COM/XML
├── tech_03_subiekt_sfera_ecommerce.md           # InsERT Subiekt GT / nexo PRO, Sfera, E-commerce
├── tech_04_python_fastapi_automatyzacje.md      # Python, FastAPI, Celery, Automatyzacje procesowe
├── tech_05_kotlin_android_native.md             # Native Android, Kotlin, Zebra DataWedge, 16 KB pages
├── tech_06_flutter_dart.md                      # Flutter, Dart, Impeller, Riverpod/BLoC
├── tech_07_swift_ios_native.md                  # Native iOS, Swift, StoreKit 2, Privacy Manifests
├── tech_08_devops_docker_linux.md               # Linux Hardening, Docker Rootless, CI/CD, Restic
├── tech_09_sql_optymalizacja_migracje.md        # PostgreSQL, MySQL, MS SQL, DDL Zero-Downtime, Indeksy
├── tech_10_nodejs_nestjs_backend.md             # Node.js, NestJS, WebSockets, Fastify, Microservices
├── tech_11_csharp_dotnet_b2b.md                 # .NET 8/9, C#, MassTransit, Native AOT, EF Core
├── tech_12_voip_asterisk_sip.md                 # Asterisk, PJSIP, VoIP, WebRTC, Whisper STT
├── tech_13_enova365_odoo_erp.md                 # Enova365 (Soneta.Business), Odoo ERP (Python/ORM)
├── tech_14_google_sheets_appscript.md           # Google Sheets, Apps Script, API Quotas, Webhooks
├── tech_15_ai_llm_rag_pipelines.md              # RAG, Wektoryzacja, Local LLM, Function Calling, JSON
├── tech_16_tech_agnostic_biznes.md              # 33% Rynku: Język biznesu, zero żargonu IT, pudełko
└── _drafty/                                     # Archiwum wariantów wstępnych (wariant 1 i 2)
```

---

## 2. Matryca 16 Granularnych Kart Technologicznych

Każda karta posiada ustandaryzowaną strukturę 7 sekcji:
1. Esencja Technologiczna i Podział Wewnętrzny
2. Prawdziwe Zlecenia Useme i Identyfikatory
3. Wykrywacz Zagrożeń i Pułapek (Gotchas)
4. Słownik Żargonu Inżynierskiego (Shibboleths)
5. Strategia Wyceny i Podziału Etapów
6. Szablony Haczyków i Otwarć (Hook & CTA)
7. Kompletna, Wzorcowa Odpowiedź

| Karta | Domena Technologiczna | Tagi & Słowa Kluczowe | Win Rate w Bazie | Główne Przewagi Merytoryczne |
|---|---|---|---|---|
| [`tech_01`](file:///badania/analizy/technologie/baza_wiedzy/tech_01_scraping_i_boty.md) | Web Scraping & Boty | Cloudflare, Kasada, Akamai, Playwright, Scrapy, JA4, cURL-impersonate | 15.69% | TLS fingerprinting, bypass antybotów bez headless chrome, intercept prywatnych API mobile |
| [`tech_02`](file:///badania/analizy/technologie/baza_wiedzy/tech_02_comarch_optima_ksef.md) | Comarch Optima & KSeF | Optima, CDN, KSeF 2.0, FA(3), COM, Praca Rozproszona | 100.0% (nisza) | Unikanie COM deadlocks, parsowanie XML FA(3), integracja faktur ustrukturyzowanych |
| [`tech_03`](file:///badania/analizy/technologie/baza_wiedzy/tech_03_subiekt_sfera_ecommerce.md) | Subiekt GT / nexo PRO | Subiekt, Sfera GT, nexo PRO, InsERT, E-commerce | 20.00% | 32-bit COM STA wrapper vs .NET 8 x64, transakcje MS SQL, kolejkowanie dokumentów WZ/ZK |
| [`tech_04`](file:///badania/analizy/technologie/baza_wiedzy/tech_04_python_fastapi_automatyzacje.md) | Python, FastAPI & Skrypty | Python, FastAPI, Celery, Redis, Pydantic, n8n, Make | 15.38% | Idempotentne webhooks, self-hosted n8n/FastAPI vs drogie tokeny Make, zadania w tle |
| [`tech_05`](file:///badania/analizy/technologie/baza_wiedzy/tech_05_kotlin_android_native.md) | Android Native & Hardware | Android, Kotlin, Zebra, DataWedge, Bluetooth BLE, Magazyn | 27.27% | Android 14/15 `foregroundServiceType`, 16 KB page size w Android 15, Zebra DataWedge API |
| [`tech_06`](file:///badania/analizy/technologie/baza_wiedzy/tech_06_flutter_dart.md) | Flutter Cross-Platform | Flutter, Dart, Riverpod, BLoC, Impeller, iOS/Android | 18.18% | Impeller rendering, Swift Package Manager migracja, unikanie problemów WorkManager na iOS |
| [`tech_07`](file:///badania/analizy/technologie/baza_wiedzy/tech_07_swift_ios_native.md) | iOS Native | iOS, Swift, SwiftUI, StoreKit 2, Privacy Manifests | 16.67% | StoreKit 2 JWS, App Store Guideline 3.1.1, `PrivacyInfo.xcprivacy` dla SDK zewnętrznych |
| [`tech_08`](file:///badania/analizy/technologie/baza_wiedzy/tech_08_devops_docker_linux.md) | DevOps, Linux & Docker | Linux, Ubuntu, Debian, Docker, Nginx, WireGuard, VPS | 14.29% | Rootless Docker, rotacja logów w `daemon.json`, hardening UFW/SSH, kopie Restic S3 |
| [`tech_09`](file:///badania/analizy/technologie/baza_wiedzy/tech_09_sql_optymalizacja_migracje.md) | Bazy Danych & SQL | PostgreSQL, MySQL, MSSQL, EXPLAIN, Indeksy, Migracje | 16.67% | `EXPLAIN (ANALYZE, BUFFERS)`, indeksy częściowe i BRIN, migracje bez blokowania tabel |
| [`tech_10`](file:///badania/analizy/technologie/baza_wiedzy/tech_10_nodejs_nestjs_backend.md) | Node.js & NestJS Backend | Node.js, NestJS, TypeScript, WebSocket, Express, Fastify | 11.11% | Architektura modularna NestJS, Fastify adapter, skalowanie Socket.io przez Redis pub/sub |
| [`tech_11`](file:///badania/analizy/technologie/baza_wiedzy/tech_11_csharp_dotnet_b2b.md) | .NET & C# Enterprise | .NET, C#, Entity Framework Core, MassTransit, AOT | 20.00% | .NET 8/9 Native AOT, unikanie problemów N+1 z `.AsSplitQuery()`, RabbitMQ z MassTransit |
| [`tech_12`](file:///badania/analizy/technologie/baza_wiedzy/tech_12_voip_asterisk_sip.md) | VoIP, Asterisk & SIP | VoIP, Asterisk, FreePBX, PJSIP, WebRTC, SIP Trunk | 25.00% | `res_pjsip` zamiast martwego `chan_sip`, porty RTP i NAT traversal, Whisper STT pipeline |
| [`tech_13`](file:///badania/analizy/technologie/baza_wiedzy/tech_13_enova365_odoo_erp.md) | Enova365 & Odoo ERP | Enova365, Soneta.Business, Odoo, Python ORM, XML-RPC | 100.0% (zweryf.) | `Soneta.Business.Session` dispose pattern, Odoo `_inherit` zamiast modyfikacji core |
| [`tech_14`](file:///badania/analizy/technologie/baza_wiedzy/tech_14_google_sheets_appscript.md) | Google Sheets & Apps Script | Google Sheets, Apps Script, SpreadsheetApp, Webhooks | 15.00% | Obejście limitu 6 minut przez triggery, wsadowe `getValues`/`setValues`, unikanie Rate Limit |
| [`tech_15`](file:///badania/analizy/technologie/baza_wiedzy/tech_15_ai_llm_rag_pipelines.md) | AI, LLM & RAG Pipelines | OpenAI, Anthropic, Qdrant, RAG, Ollama, LangChain | 12.50% | RAG hybrydowy (BM25 + Dense) z Cohere re-ranking, walidacja Pydantic JSON schema |
| [`tech_16`](file:///badania/analizy/technologie/baza_wiedzy/tech_16_tech_agnostic_biznes.md) | Zlecenia Tech-Agnostic | Automatyzacja firmy, integracja systemów, narzędzie | 14.19% | Język czystego rezultatu biznesowego, gotowe pudełko, zerowy koszt wdrożenia dla klienta |

---

## 3. Cztery Syntezy Bojowe (Wielodomenowe)

Syntezy strategiczne łączą wiedzę z poszczególnych kart w spójne grupy operacyjne:
1. [`synteza_bojowa_01_erp.md`](file:///badania/analizy/technologie/baza_wiedzy/synteza_bojowa_01_erp.md) – **Grupa 1: ERP & Integracje Finansowo-Magazynowe** (Comarch Optima, Subiekt GT/nexo, Enova365, Odoo, KSeF). Standardy transakcyjności, ochrona przed blokadami bazy, obsługa formatów FA(3).
2. [`synteza_bojowa_02_automatyzacje_i_backend.md`](file:///badania/analizy/technologie/baza_wiedzy/synteza_bojowa_02_automatyzacje_i_backend.md) – **Grupa 2: Scraping, Boty & Backend Systemowy** (Scraping, Python/FastAPI, SQL, Node/NestJS, C#/.NET). Omijanie antybotów, odporność na zmiany struktur stron, idempotencja webhooków.
3. [`synteza_bojowa_03_mobile_hardware.md`](file:///badania/analizy/technologie/baza_wiedzy/synteza_bojowa_03_mobile_hardware.md) – **Grupa 3: Mobile & Sprzęt Przemysłowy** (Android Kotlin, Flutter, iOS Swift, VoIP Asterisk). Praca w tle, obsługa skanerów magazynowych (Zebra DataWedge), kodeki SIP/WebRTC.
4. [`synteza_bojowa_04_infra_ai_biznes.md`](file:///badania/analizy/technologie/baza_wiedzy/synteza_bojowa_04_infra_ai_biznes.md) – **Grupa 4: Infrastruktura, AI & Segment Tech-Agnostic** (Linux/Docker, Apps Script, AI/RAG, 33% rynku bez technologii). Bezpieczeństwo serwerów, stabilne potoki RAG bez halucynacji, narracja zorientowana na zysk i oszczędność czasu.

---

## 4. Zasady Bojowe i Taktyczne (Wyciąg z Audytu i Dźwigni)

Wszystkie generowane odpowiedzi muszą bezwzględnie przestrzegać ustaleń z [`audyt_krytyczny_red_team.md`](file:///badania/analizy/technologie/baza_wiedzy/audyt_krytyczny_red_team.md) oraz [`dzwignie_psychologia_merytoryka_wyceny.md`](file:///badania/analizy/technologie/baza_wiedzy/dzwignie_psychologia_merytoryka_wyceny.md):

1. **Skalowanie Długości Oferty (Character Limits)**:
   - **Mikro/Małe zlecenia (<3 000 PLN)**: Maksymalnie **300–450 znaków**. Format 3 liczb: Cena, Czas, Gwarancja (30 dni) + 1 konkretne pytanie diagnostyczne. Zakaz elaboratów!
   - **Średnie/Duże zlecenia (>5 000 PLN)**: **600–900 znaków**. Zwięzła diagnoza ryzyk, 3–4 czyste kamienie milowe, 1 pytanie techniczne.
2. **Kanał Komunikacji: Elastyczność (Priv + Public)**:
   - System nie jest sztywno zablokowany na public/priv. Wiadomości prywatne w Useme są eksponowane w czytelnym i przejrzystym oknie, a konkurencja na priv jest wielokrotnie mniejsza niż na liście publicznej. Oferty priv chronią unikalną diagnozę przed kradzieżą przez konkurencję.
3. **Zakaz "Hopsiup do przodu"**:
   - Zakaz sztucznych sekcji typu "Podkładka dla szefa / Podsumowanie dla zarządu" (brzmi protekcjonalnie i natarczywie).
   - Oferta ma być naturalnie przejrzysta, tak by pracownik (księgowa, PM) mógł ją pokazać przełożonemu, bez pouczania go o tym.
4. **Odrzucenie Pułapek Odpowiedzialności**:
   - Gwarancja: **30 dni na własny kod** (zero darmowych gwarancji 12-miesięcznych na cudze API/antyboty; dłuższe wsparcie wyłącznie w ramach płatnego abonamentu SLA).
   - Brak darmowych "mikro-proofów na 2 plikach klienta" przed zleceniem.
5. **Autorytet i Styl**:
   - Spokojny, oszczędny w słowach ton starszego inżyniera.
   - Zero korpo-gadek ("Chętnie podejmę się...", "Posiadam wieloletnie doświadczenie...").
   - Zero propozycji calli/spotkań – 100% asynchroniczne domknięcie pisemne.

---

## 5. Protokół Integracji z Botem (`kod/`)

1. **Wykrywanie Kategoryzacji**:
   - `kod/prompts/generatory/agent_01_research.md` analizuje treść i przypisuje zleceniu odpowiednią kartę (`tech_01` do `tech_16`).
   - W przypadku braku technologii w opisie, automatycznie mapuje do `tech_16_tech_agnostic_biznes.md`.
2. **Wstrzykiwanie Kontekstu**:
   - Generator `kod/prompts/generatory/agent_02a_opis_oferty.md` ładuje sekcje 3, 4 i 6 z właściwej karty oraz odpowiednią syntezę bojową.
3. **Kalkulacja i Bramka**:
   - `wycena_kalkulator.py` dobiera stawkę zgodnie z sekcją 5 karty oraz rynkiem.
   - Walidatory (`agent_03` do `agent_08`) pilnują limitu znaków (300–450 vs 600–900) i czystości inżynierskiej.
