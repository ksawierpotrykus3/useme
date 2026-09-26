# -*- coding: utf-8 -*-
"""Generator kart wiedzy dla Bloku 3 (Nisze: VoIP, Enova365/Odoo, AppScript, AI/RAG)
oraz Bloku 4 (Segment Tech-Agnostic - 33% rynku bez technologii).
Wykorzystuje model deepseek-chat-search na lokalnym proxy laboratorium_modeli (port 4571)
oraz rygorystyczny schemat inżynierski wymuszający odpowiedź na priv.
"""

import json
from pathlib import Path
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-chat-search"

OUTPUT_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\badania\analizy\technologie\baza_wiedzy")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """Jesteś Głównym Architektem i Starszym Inżynierem Systemowym tworzącym elitarną bazę wiedzy dla bota ofertowego na platformie Useme / B2B.

KONTEKST I REALIA ZLECENIODAWCÓW (WYNIKI AUDYTU USEME):
- Zlecenia niszowe (VoIP, Enova365, Odoo) charakteryzują się bardzo małą liczbą ofert konkurencyjnych i gigantyczną marżą (Win Rate dochodzący do 40%).
- Z kolei segment Tech-Agnostic to aż 33% całego rynku (155 zleceń w badaniu), gdzie klienci nie podają żadnego języka ani technologii, tylko problem biznesowy (bot, kalkulator, pobranie bazy, integracja).
- Elita wygrywa zlecenia, ponieważ:
  1. OTWIERA PROBLEMEM ARCHITEKTONICZNYM LUB BIZNESOWYM W PIERWSZYCH 2 ZDANIACH (zamiast pisać o swoim stażu, uderza w sedno procesu: kodeki SIP i NAT, model obiektowy Enova365, limity Google Quotas, koszty tokenów LLM, albo gotowy prosty model wdrożenia dla klienta nietechnicznego).
  2. ZNA AKTUALNE REALIA SYSTEMOWE NA 2026 ROK (PJSIP vs chan_sip, Enova365 pod kątem KSeF, Odoo v17/v18, Quotas Google 2026, RAG hybrydowy BM25+wektory).
  3. ZADAJE 2-3 CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODKU ANALIZY (zmusza klienta do natychmiastowego odpisania na priv).
  4. WSKAZUJE ANTYWZORCE I CZERWONE FLAGI (np. brak obsługi NAT w VoIP, synchroniczne parsowanie w AppScript, naiwny RAG bez re-rankingu, narzucanie ciężkiego frameworka klientowi, który chciał prosty program).
  5. ROZBIJA WYCENĘ NA LOGICZNE MODUŁY ARCHITEKTONICZNE (nie ryczałt).

ZASADY TREŚCI:
- Zero udawania mowy ludzkiej ("no hej", "w sumie", sztuczne idiomy).
- Zero proponowania spotkań wideo, Google Meet czy rozmów telefonicznych (komunikacja wyłącznie pisemna na priv).
- Twarde, zweryfikowane fakty inżynierskie, zaktualizowane pod kątem 2026 roku.
- Język: Polski, wysoce precyzyjny, techniczny.
"""

TASKS = [
    {
        "id": "tech_12_voip_asterisk_sip",
        "nazwa": "VoIP, Centrale Telefoniczne Asterisk, SIP Trunking i FreePBX",
        "plik": OUTPUT_DIR / "tech_12_voip_asterisk_sip.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **VoIP, Centrale Asterisk / FreePBX, Protokół SIP (PJSIP), Trunking Operatorski, IVR i Integracje Call Center z CRM (Transkrypcja AI)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić nowoczesne wdrożenia VoIP w 2026 roku (całkowite wycofanie chan_sip na rzecz res_pjsip w nowym Asterisku, WebRTC w przeglądarce, integracja nagrań z modelami STT Whisper/Deepgram w czasie rzeczywistym).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: wdrożenie wirtualnej centrali telefonicznej dla biura obsługi / działu sprzedaży, konfiguracja kolejkowania połączeń (ACD) i IVR, integracja telefonu z CRM (HubSpot, Pipedrive, Bitrix24), automatyczne wybieranie numerów (predictive dialer), transkrypcja rozmów z AI.
   - Budżety: 2 500 – 10 000 zł (Win Rate w badaniu: 40%). Profil klienta: właściciel firmy handlowej, kierownik call center, agencja marketingu telefonicznego.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Asterisk & SIP: Wycofanie starego `chan_sip` – standardem produkcyjnym jest wyłącznie `res_pjsip` (obsługa wielu endpoints na jednym AOR, transport TLS/SRTP); konfiguracja NAT (STUN/TURN/ICE, nagłówki `external_media_address` i `external_signaling_address` zapobiegające problemowi braku dźwięku w jedną stronę / One-Way Audio).
   - Kodeki i pasmo: G.711 (alaw/ulaw) dla standardowej telefonii PSTN, Opus / G.722 dla jakości HD Voice i WebRTC; kalkulacja pasma (ok. 80-100 kbps na kanał z nagłówkami IP/UDP/RTP).
   - Integracje zewnętrzne: Asterisk Manager Interface (AMI) i Asterisk Gateway Interface (AGI) vs nowoczesny Asterisk REST Interface (ARI) dla aplikacji czasu rzeczywistego.
   - AI i Transkrypcja: Przesyłanie strumienia RTP bezpośrednio do transkrypcji w czasie rzeczywistym (np. Whisper / Deepgram) w celu analizy sentymentu i podsumowań w CRM.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję prostej centrali telefonicznej z IVR i przekierowaniem na 5 konsultantów".
   - Co go utopi (Mina 1 - One-Way Audio): Brak prawidłowej konfiguracji NAT/RTP portów na routerze klienta (zakres UDP 10000-20000) powoduje, że klient słyszy konsultanta, ale konsultant nie słyszy klienta (lub połączenie rozłącza się po 30 sekundach z powodu braku ACK).
   - Co go utopi (Mina 2 - Włamania na centralę i rachunki na tysiące euro): Brak Fail2ban na portach SIP (5060) i brak restrykcji IP dla trunków operatora — botnety skanujące internet przejmują konto SIP i w ciągu nocy wydzwaniają numery premium na Kubę czy Somalię.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Otwarcie uderzające w konfigurację PJSIP za NAT-em (zapobieganie One-Way Audio) oraz zabezpieczenie portów SIP przed atakami brute-force (SIP scanner).
   - Wskazanie na ARI / AMI jako standard mostka z CRM klienta.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz proponowania przestarzałego `chan_sip`.
   - Zakaz ignorowania zabezpieczeń firewall/fail2ban na porcie SIP UDP 5060.
   - Zakaz obietnic "krystalicznej jakości bez jittera" bez weryfikacji łącza i polityki QoS u klienta.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 3 500 – 9 000 ZŁ):
   - Moduły: 1. Konfiguracja serwera Asterisk/FreePBX z PJSIP i zabezpieczeniami (Firewall, Fail2ban, SRTP); 2. Konfiguracja operatora SIP Trunk i reguł trasowania przychodzącego/wychodzącego; 3. Projekt drzewa zapowiedzi IVR, kolejek i poczty głosowej; 4. Moduł integracji z CRM (web pop-up przy połączeniu przez webhook/AMI); 5. Testy obciążeniowe i wdrożenie softphone (WebRTC / Linphone / MicroSIP).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. u jakiego operatora mają wykupiony SIP Trunk i czy operator wymaga rejestracji czy uwierzytelniania po IP; ilu konsultantów ma dzwonić jednocześnie; czy telefony to fizyczne aparaty IP czy softphone na komputerach).
"""
    },
    {
        "id": "tech_13_enova365_odoo_erp",
        "nazwa": "Systemy ERP: Enova365 (Soneta.Business) oraz Odoo ERP (Python/OWL)",
        "plik": OUTPUT_DIR / "tech_13_enova365_odoo_erp.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Zaawansowane Integracje ERP: Enova365 (Architektura .NET Soneta.Business, Harmonogram Zadań, API) oraz Odoo ERP (Moduły Python, OWL Framework, Integracja z Polskim Prawem i KSeF)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić stan ekosystemu Enova365 (wersje 2404+, obsługa KSeF, web api Soneta) oraz Odoo (wersje 17 i 18, polska lokalizacja podatkowa, integracje headless).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: integracja sklepu internetowego lub systemu zamówień z Enova365 / Odoo, automatyczny import dokumentów, pisanie dedykowanych modułów biznesowych, wdrożenia pod KSeF w Enova/Odoo.
   - Budżety: 4 500 – 16 000 zł. Profil klienta: średnia firma produkcyjna lub handlowa, dystrybutor, biuro rachunkowe obsługujące korporacje.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Enova365 Architektura: Framework `Soneta.Business` w C# (.NET). Bezpieczne programowanie obiektowe: sesja transakcyjna `using (var session = login.CreateSession(false, false))`, obiekty biznesowe (Handel, Kasa, Rozrachunki), harmonogram zadań serwera biznesowego (Soneta.Server). Wymóg korzystania z API Soneta zamiast bezpośrednich modyfikacji bazy SQL (zachowanie reguł walidacji i przeliczania podatków).
   - Odoo ERP Architektura: Python 3.x, PostgreSQL, ORM Odoo z polami computed (`@api.depends`), model dziedziczenia (`_inherit`), interfejs OWL (Odoo Web Library). Polska lokalizacja (moduły `l10n_pl`, split payment, biała lista podatników VAT, KSeF connector).
   - Wymiana danych: Web Services (Enova365 WebAPI REST / OData) vs szyna danych XML/JSON; Odoo XML-RPC / JSON-RPC oraz zewnętrzne endpointy webhooków `@http.route`.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebujemy zintegrować zamówienia z naszego sklepu internetowego do Enova365".
   - Co go utopi w Enova365: Próba zapisu dokumentów handlowych bez prawidłowego zarządzania sesją i blokadami (`LockException`) lub brak obsługi przeliczania marż i stanów magazynowych na poziomie sesji Sonety; brak licencji na moduł WebAPI / Integrator (dodatkowy koszt licencyjny Soneta dla klienta).
   - Co go utopi w Odoo: Nadpisanie standardowych metod Odoo zamiast ich eleganckiego rozszerzenia przez `super()`, co kompletnie blokuje możliwość migracji do kolejnej wersji Odoo (np. z 17 na 18) i psuje kalkulacje księgowe.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia inżynierskie uderzające w oficjalne API Soneta.Business (z zachowaniem integralności bazy i licencji Sonety) lub czystą architekturę modułową Odoo bez hackowania kodu bazowego.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz bezpośrednich INSERT-ów do tabel MS SQL w Enova365 (psuje wewnętrzne mechanizmy GUID-ów, log audytowy i integralność transakcyjną).
   - Zakaz modyfikacji rdzennego kodu Odoo (`odoo/addons/core`) zamiast tworzenia custom addona w `custom_addons`.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 5 000 – 14 000 ZŁ):
   - Moduły: 1. Analiza procesów biznesowych i mapowanie kartotek/kontrahentów; 2. Moduł konektora API (Soneta WebAPI / Odoo controller); 3. Silnik walidacji biznesowej, rezerwacji magazynowych i obsługi VAT; 4. Asynchroniczna kolejka synchronizacji z mechanizmem retry; 5. Testy na bazie testowej klienta i procedura deploymentu.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy Enova365 działa w wersji wielodostępnej z Soneta Server; czy posiadają licencję na moduł Integrator/WebAPI; w przypadku Odoo - czy jest to Odoo Community, Odoo Enterprise on-prem czy Odoo.sh).
"""
    },
    {
        "id": "tech_14_google_sheets_appscript",
        "nazwa": "Google Sheets, Apps Script & Workspace Automation (API Quotas, Lekki Backend)",
        "plik": OUTPUT_DIR / "tech_14_google_sheets_appscript.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Google Sheets, Google Apps Script, Automatyzacje Google Workspace (Gmail / Drive), Omijanie Limitów Quotas i Architektura Arkusza jako Lekki Backend**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić aktualne limity Google Apps Script Quotas w 2026 roku (twardy limit 6 minut na wykonanie skryptu, limity URLFetchApp, trigger ograniczenia per dzień, integracja z zewnętrznym Node/Python przez Google Sheets API v4).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: automatyzacja raportowania z wielu arkuszy, integracja Google Sheets z zewnętrznymi API (pobieranie kursów walut, zamówień z Allegro/Stripe), generowanie faktur PDF i wysyłka mailem z Gmaila, niestandardowe makra i dashboardy biznesowe.
   - Budżety: 1 500 – 6 000 zł (Win Rate w badaniu: 13.3%). Profil klienta: dyrektor sprzedaży, właściciel małej firmy, analityk finansowy, agencja marketingowa.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Twarde limity Google Apps Script (Quotas):
     * Czas wykonania: maksymalnie **6 minut na jedno uruchomienie** (dla kont darmowych i Workspace!). Skrypt trwający dłużej zostaje brutalnie zabity z błędem `Exceeded maximum execution time`.
     * Wywołania sieciowe: limit `UrlFetchApp` (20 000 wywołań dziennie dla darmowych, 100 000 dla Workspace).
     * Ograniczenia zapisu do komórek: Zapisywanie komórka po komórce (`sheet.getRange(i, j).setValue()`) to najgorszy antywzorzec blokujący skrypt po 100 wierszach. Wymóg operacji wsadowych: `getValues()` i `setValues()` na całej macierzy 2D w pamięci RAM.
   - Architektura obejścia limitu 6 minut: Wzorzec "Batch Processor + Continuations Trigger" — skrypt zapisuje stan (ostatni przetworzony wiersz) w `PropertiesService.getScriptProperties()` i rejestruje czasowy Time-driven trigger uruchamiający kolejną partię.
   - Kiedy Apps Script to za mało: Przekroczenie limitów wymaga przeniesienia logiki na zewnętrzny mikroserwis w Pythonie/Node.js, który komunikuje się z arkuszem przez oficjalne Google Sheets API v4 (Google Cloud Service Account) bez limitu 6 minut.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję prostego skryptu w Apps Script, który codziennie pobiera dane z API dla 5000 produktów i aktualizuje ceny w arkuszu".
   - Co go utopi: Skrypt puszczony na 5000 requestów `UrlFetchApp` synchronicznie wywali się z timeoutem po 6 minutach na około 400. produkcie. Klient zostanie z częściowo zaktualizowanym arkuszem i niespójnymi danymi. Wymóg: `UrlFetchApp.fetchAll()` (równoległe zapytania asynchroniczne) lub zewnętrzny skrypt w Pythonie.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe otwarcia uderzające w limit 6 minut na trigger, operacje wsadowe (`setValues`) zamiast pojedynczych komórek oraz asynchroniczne `fetchAll()`.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz pisania pętli `for` wywołujących `getValue()` / `setValue()` wewnątrz każdej iteracji.
   - Zakaz obietnic, że Apps Script może wykonywać zadania trwające ciągiem 30 minut.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 2 000 – 5 500 ZŁ):
   - Moduły: 1. Silnik parsowania i transformacji danych w pamięci (operacje na tablicach JS); 2. Warstwa pobierania danych zewnętrznych (obsługa `UrlFetchApp.fetchAll` z retry); 3. Mechanizm kontynuacji i zapis stanu w PropertiesService; 4. Interfejs użytkownika w arkuszu (custom menu, modalne okna HTML Service, walidacja danych); 5. Dokumentacja obsługi i testy wydajnościowe.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. ile wierszy danych ma docelowo przetwarzać arkusz; czy konto Google to prywatny Gmail czy Google Workspace z wyższymi limitami; czy arkusz ma działać automatycznie o stałej godzinie w nocy).
"""
    },
    {
        "id": "tech_15_ai_llm_rag_pipelines",
        "nazwa": "Sztuczna Inteligencja, RAG, Bazy Wektorowe i Integracje LLM (OpenAI, Anthropic, Qdrant)",
        "plik": OUTPUT_DIR / "tech_15_ai_llm_rag_pipelines.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Architektury RAG (Retrieval-Augmented Generation), Wyszukiwanie Hybrydowe, Bazy Wektorowe (Qdrant / pgvector), Integracje LLM (OpenAI, Claude, DeepSeek) i Optymalizacja Kosztów Tokenów**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić nowoczesny stan inżynierii RAG w 2026 roku (hybrydowe wyszukiwanie gęste wektory + rzadkie BM25 / SPLADE, re-ranking z modelami Cross-Encoder / Cohere Rerank, Structured Outputs ze ścisłą walidacją JSON Schema, frameworki LlamaIndex / LangChain vs lekki natywny kod).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: bot odpowiadający na pytania na podstawie wewnętrznej bazy wiedzy firmy (PDF-y, dokumentacja, regulaminy), inteligentna ekstrakcja danych z nieustrukturyzowanych umów/faktur, klasyfikacja i automatyczne odpowiadanie na maile klientów, audyt kosztów API LLM.
   - Budżety: 4 500 – 16 000 zł. Profil klienta: zarząd firmy usługowej, startup AI, kancelaria prawna, platforma e-commerce.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Naiwny RAG vs RAG Produkcyjny: Naiwny RAG (prosty chunking na 500 znaków + k-NN na wektorach OpenAI) zawodzi w 60% przypadków biznesowych (halucynacje, gubienie kontekstu tabelarycznego). Produkcyjny RAG wymaga:
     * Chunkingu semantycznego lub strukturalnego (rozpoznawanie nagłówków Markdown / układu dokumentu).
     * Wyszukiwania hybrydowego: Wektory semantyczne + wyszukiwanie pełnotekstowe BM25 (kluczowe przy specyficznych kodach produktów, numerach NIP, artykułach prawnych).
     * Re-rankingu: Drugi etap z modelem re-rankera (np. Cohere Rerank, BGE-Reranker), który precyzyjnie sortuje top 20 wyników do top 3-5 najbardziej relewantnych.
   - Bazy wektorowe: `pgvector` w PostgreSQL (dla prostych projektów, gdzie nie chcemy mnożyć infrastruktury) vs dedykowany silnik **Qdrant** / Milvus (dla milionów wektorów, filtrowania metadanych w czasie rzeczywistym i wysokiej wydajności).
   - Structured Outputs & Strict Schemas: Wykorzystanie natywnego `response_format: { type: "json_schema", strict: true }` zamiast błagania modelu promptem "zwróć tylko JSON".
   - Ekonomia tokenów i dobór modeli: Modele reasoningowe / ciężkie (GPT-4o, Claude Opus) tylko do ostatecznej syntezy; małe szybkie modele (Claude Haiku, GPT-4o-mini, DeepSeek V3) do chunkingu, tagowania i routingu zapytań (obniżka kosztów API o 85%).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Chcemy prostego bota, który ma wgrane nasze instrukcje w PDF i odpowiada klientom na stronie".
   - Co go utopi: Halucynacja bota na pytaniach out-of-scope (np. bot wymyśla zniżki lub obiecuje darmowe usługi), brak weryfikacji cytowań źródeł (grounding), astronomiczne rachunki za API przy braku cache'owania i braku filtrów spamu/prompt injection.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Otwarcie uderzające w konieczność wyszukiwania hybrydowego (BM25 + wektory) z re-rankingiem, aby wyeliminować halucynacje, oraz twardą walidację schematów JSON Schema.
   - Wskazanie na mechanizm Guardrails (ochrona przed prompt injection i odpowiedziami poza zakresem).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Zakaz obiecywania "100% braku halucynacji bez architektury weryfikacji faktów".
   - Zakaz proponowania prostego splitu tekstu na stałą liczbę znaków bez uwzględnienia struktury dokumentu (tabel, nagłówków).
   - Zakaz ignorowania kosztów API OpenAI/Anthropic i braku estymacji tokenów.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 5 500 – 15 000 ZŁ):
   - Moduły: 1. Pipeline przetwarzania dokumentów (ekstrakcja z PDF, semantyczny chunking, generowanie embeddingów); 2. Hybrydowa baza wiedzy (Qdrant / pgvector z indeksem BM25); 3. Silnik re-rankingu i orkiestracji zapytań (system prompt z twardymi guardrails); 4. Brama API z walidacją JSON Schema i cache'owaniem semantycznym; 5. Panel ewaluacji odpowiedzi i logowanie kosztów tokenów.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. w jakim formacie są źródła wiedzy i czy zawierają tabele/wykresy; jaki jest szacowany dzienny wolumen zapytań; czy system ma działać wewnętrznie dla pracowników czy publicznie dla klientów).
"""
    },
    {
        "id": "tech_16_tech_agnostic_biznes",
        "nazwa": "Segment Tech-Agnostic (33% Rynku Useme) — Sprzedaż Czysto Biznesowa bez Żargonu",
        "plik": OUTPUT_DIR / "tech_16_tech_agnostic_biznes.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy strategicznej dla bota ofertowego:
TEMAT: **Obsługa Segmentu Tech-Agnostic (155 zleceń w badaniu, 33% całego rynku Useme) — Zlecenia bez Podanej Technologii, Sprzedaż Językiem Rezultatu Biznesowego, Rozwiązania Pudełkowe i Bezpieczne Wdrożenia**.

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW (DANE EMPIRYCZNE):
   - Statystyka: 155 zleceń z próby N=470 (dokładnie 33% rynku) NIE zawiera żadnej nazwy technologii (brak słów Python, React, PHP itp.).
   - Przykłady zapytań z bazy Useme: "Potrzebuję bota do wystawiania ogłoszeń na portalach", "Program do przeliczania prowizji ze sprzedaży", "Automatyczne pobieranie kontaktów ze stron firm", "Skrypt do generowania raportów dla zarządu", "System rezerwacji wizyt dla gabinetu".
   - Win Rate w segmencie: 10.97% (17 wygranych zleceń).
   - Budżety: 1 500 – 7 000 zł. Profil klienta: właściciel małej/średniej firmy, menedżer, osoba całkowicie nietechniczna. Klient szuka ROZWIĄZANIA PROBLEMU, a nie technologii.
2. ZASADY PSYCHOLOGICZNE I JĘZYKOWE W SEGMENTIE TECH-AGNOSTIC:
   - Kategoryczny zakaz żargonu programistycznego: Klient nie wie i nie chce wiedzieć, co to jest Docker, FastAPI, PostgreSQL czy async/await. Jeśli w ofercie pojawią się te słowa, klient poczuje się zagubiony i wybierze kogoś, kto mówi językiem korzyści.
   - Język rezultatu: "Aplikacja działa w tle jednym kliknięciem", "Dane trafiają automatycznie do pliku Excel", "Program posiada prosty panel w przeglądarce", "Gwarancja bezawaryjności i asysta".
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA NIETECHNICZNEGO:
   - Co pisze klient: "Potrzebuję programu do X".
   - Co go przeraża pod maską: Strach przed tym, że dostanie skrypt w konsoli tekstowej, którego nie potrafi uruchomić; strach przed skomplikowaną instalacją; obawa, że po skończeniu zlecenia program przestanie działać, a programista zniknie.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW Z ŻARGONEM):
   - Otwarcie opisujące dokładny stan docelowy ("Program dostarczam w formie gotowej aplikacji z prostym panelem, która nie wymaga żadnej wiedzy technicznej — instalacja sprowadza się do uruchomienia jednego pliku").
   - Wskazanie na bezobsługowość: "Wyniki lądują bezpośrednio w pliku Excel/Google Sheets, a w razie jakichkolwiek zmian na portalach program posiada automatyczne powiadomienia".
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz narzucania technologii jako zalety samej w sobie ("napiszę to w React i FastAPI z bazą Postgres").
   - Zakaz dostarczania kodu "do odpalenia z terminala" bez prostego interfejsu (chyba że klient wyraźnie o to prosi).
   - Zakaz zadawania skomplikowanych pytań architektonicznych (pytamy wyłącznie o logikę biznesową i format danych).
6. PRODUKCYJNA ARCHITEKTURA WDROŻENIA BIZNESOWEGO (WYCENA 2 500 – 6 500 ZŁ):
   - Jak ubrać ofertę modułowo bez żargonu: 1. Konfiguracja i przygotowanie programu pod specyfikę firmy; 2. Moduł automatycznego pobierania/przetwarzania danych; 3. Prosty panel sterowania dla użytkownika (przeglądarka / ikona na pulpicie); 4. Instrukcja wideo krok po kroku + instalacja na komputerze klienta; 5. Gwarancja działania i opieka powdrożeniowa 30 dni.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE DLA KLIENTA BIZNESOWEGO:
   - 2-3 pytania zadane ludzkim, biznesowym językiem (np. "W jakim formacie chce Pan/Pani otrzymywać gotowe wyniki — plik Excel na maila czy bezpośredni podgląd w tabeli?", "Na ilu komputerach program ma działać?", "Jak często proces ma się powtarzać — na żądanie kliknięciem czy automatycznie o określonej godzinie?").
"""
    }
]

def wykonaj_zadanie(zadanie):
    print(f"\n=======================================================")
    print(f"[START] Rozpoczynam zadanie: {zadanie['nazwa']}")
    print(f"[PLIK]  {zadanie['plik'].name}")
    print(f"[MODEL] {MODEL}")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": zadanie["prompt"]}
        ],
        "temperature": 0.3,
        "stream": False
    }
    
    start_t = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=240)
        if r.status_code != 200:
            print(f"[BŁĄD HTTP {r.status_code}] {r.text[:500]}")
            return False
            
        dane = r.json()
        tresc = dane["choices"][0]["message"]["content"]
        
        # Zapis do pliku UTF-8
        zadanie["plik"].write_text(tresc, encoding="utf-8")
        duration = round(time.time() - start_t, 1)
        print(f"[SUKCES] Wygenerowano i zapisano: {zadanie['plik'].name} ({len(tresc)} znaków) w {duration}s")
        return True
    except Exception as e:
        print(f"[WYJĄTEK] {e}")
        return False

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== Generator Kart Wiedzy: Blok 3 (Nisze) & Blok 4 (Tech-Agnostic) ===")
    sukcesy = 0
    for zadanie in TASKS:
        ok = wykonaj_zadanie(zadanie)
        if ok:
            sukcesy += 1
        time.sleep(2)
        
    print(f"\n=======================================================")
    print(f"[KONIEC] Pomyślnie ukończono {sukcesy}/{len(TASKS)} kart technologicznych!")

if __name__ == "__main__":
    main()
