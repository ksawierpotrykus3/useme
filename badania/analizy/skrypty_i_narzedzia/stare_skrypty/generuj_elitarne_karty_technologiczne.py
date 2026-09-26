# -*- coding: utf-8 -*-
"""Generator elitarnych kart wiedzy technologicznej dla Bota Ofertowego Useme.
Wykorzystuje model z przeszukiwaniem sieci (deepseek-chat-search / deepseek-reasoner)
oraz twardy kontekst zlecenia testowego #144890 i analizy taktyk konkurencji.
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

# Wspólny rygorystyczny kontekst inżynierski
SYSTEM_PROMPT = """Jesteś Głównym Architektem i Starszym Inżynierem Systemowym tworzącym elitarną bazę wiedzy inżynierskiej dla bota ofertowego na platformie Useme / B2B.

KONTEKST I REALIA ZLECENIODAWCÓW (WYNIKI AUDYTU #144890):
- 90% oferentów na Useme to amatorzy piszący generyczne banały: "Dzień dobry, chętnie pomogę, mam 5 lat doświadczenia, zapraszam do kontaktu". Ich oferty lądują w koszu.
- Elita rynkowa (10% najlepszych) dominuje i wygrywa zlecenia za 4 500 - 15 000 zł, ponieważ:
  1. OTWIERAJĄ PROBLEMEM I MINĄ TECHNICZNĄ, A NIE SOBĄ: W pierwszych 2 zdaniach trafiają w newralgiczny problem architektoniczny, o którym sam klient często nie pomyślał.
  2. MÓWIĄ COŚ, CZEGO KLIENT NIE WIE: Wyciągają twarde fakty (np. specyfikacje protokołów, luki w regulacjach, pułapki zaokrągleń, wersje schematów, licencje).
  3. ZADAJĄ 2-3 CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODKU ANALIZY: Zmuszają zleceniodawcę do odpisania w wiadomości prywatnej (jedyny cel to wywołać natychmiastową odpowiedź na priv).
  4. WSKAZUJĄ CZERWONE FLAGI / ANTYWZORCE: Bezwzględnie wytykają amatorskie błędy (np. bezpośredni SQL do ERP, brak idempotencji, naiwne parsowanie HTML zamiast API).
  5. ROZBIJAJĄ WYCENĘ NA MODUŁY ARCHITEKTONICZNE: Uzasadniają wysoką stawkę inżynierską (nie ryczałt "3000 zł w 3 dni").

ZASADY TREŚCI:
- Żadnego udawania mowy ludzkiej ("w sumie", "no hej", "słuchajcie").
- Żadnego proponowania rozmów telefonicznych, Google Meet czy darmowych konsultacji na wideo (komunikacja jest w 100% asynchroniczna i pisemna).
- Twarde, zweryfikowane fakty inżynierskie, aktualne na 2026 rok.
- Język: Polski, ultra-konkretny, techniczny.
"""

TASKS = [
    {
        "id": "tech_01_scraping_i_boty",
        "nazwa": "Web Scraping, Boty Danych i Omijanie Anty-Botów (WAF / Cloudflare Turnstile / TLS JA4)",
        "plik": OUTPUT_DIR / "tech_01_scraping_i_boty.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Web Scraping, Boty Ekstrakcyjne i Zaawansowane Omijanie Systemów Anty-Botowych (Cloudflare Turnstile, DataDome, Akamai, sygnatury TLS JA4)**.

Wykorzystaj wyszukiwarkę sieciową, aby uwzględnić najnowszy stan technologii na 2026 rok.

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Typy zleceń (monitoring cen konkurencji, boty na portale ogłoszeniowe OLX/OtoMoto, agregatory e-commerce, ekstrakcja baz leadów B2B).
   - Realne widełki budżetowe (1 500 - 8 500 zł) i profil klienta (właściciel e-commerce, startup, analityk rynku).
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Zabezpieczenia: Cloudflare Turnstile, DataDome, Kasada, Akamai BMP.
   - Detekcja na poziomie sieci: Fingerprinting TLS (JA3, JA4), cykle negocjacji HTTP/2 (akamaismart / frames), detekcja nagłówków TCP/IP (MTU, p0f).
   - Detekcja przeglądarek: Wykrywanie CDP (Chrome DevTools Protocol) przez flagi Runtime.enable, `navigator.webdriver`, wycieki zmiennych CDC, Canvas/WebGL i AudioContext fingerprinting.
   - Narzędzia nowoczesne: curl_cffi, tls-client, Camoufox (Firefox-based stealth), nodriver / undetected-chromedriver, mitmproxy.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Co pisze klient: "Potrzebuję prostego skryptu w Pythonie do pobierania 50k produktów dziennie".
   - Co jest miną: Rotacja selektorów frontendowych; dynamiczne Shadow DOM; memory leaki w wielowątkowych instancjach Chromium (wzrost zużycia RAM z 500MB do 16GB); koszty i jakość proxy (datacenter natychmiast blokowane, koszty proxy rezydencjalnych liczone w GB).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW Z SELENIUM):
   - Gotowe otwarcia inżynierskie deklasujące oferty ze standardowym BeautifulSoup/Selenium.
   - Technika reverse-engineeringu prywatnych endpointów REST/GraphQL z aplikacji mobilnej lub wersji PWA zamiast renderowania ciężkiego HTML.
   - Optymalizacja kosztów proxy: filtrowanie zapytań o assety (obrazki, CSS, fonty), kompresja Brotli/Gzip, utrzymywanie sesji HTTP/2.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Twardy zakaz deklarowania "darmowych publicznych proxy" (są zaspamowane i służą jako honeypoty).
   - Zakaz pisania o BeautifulSoup / prostym requests do stron z WAF/Cloudflare.
   - Zakaz obiecywania "100% niewykrywalności na zawsze" bez uwzględnienia budżetu na rotację IP i utrzymanie selektorów.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 000 - 8 000 ZŁ):
   - Architektura produkcyjna: Kolejka zadań (Celery/Redis), warstwa pobierania (curl_cffi / stealth browser pool), walidator danych (Pydantic), magazyn danych (PostgreSQL / ClickHouse / S3 / BigQuery).
   - Moduły: 1. Analiza anty-bot i reverse-engineering API; 2. Moduł rotacji sesji i proxy; 3. Silnik parsowania i normalizacji; 4. Baza danych i pipeline eksportu; 5. Monitoring, alerty i retry policy.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 precyzyjne pytania inżynierskie zmuszające zleceniodawcę do odpisania na priv (np. o częstotliwość odświeżania, format docelowy, czy akceptuje koszty proxy rezydencjalnych).
"""
    },
    {
        "id": "tech_02_comarch_optima_ksef",
        "nazwa": "Comarch ERP Optima & KSeF 2.0 (FA(3), XML, Praca Rozproszona, Comarch API)",
        "plik": OUTPUT_DIR / "tech_02_comarch_optima_ksef.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Integracje Comarch ERP Optima, Krajowy System e-Faktur (KSeF 2.0 / struktura FA(3)), Automatyzacja Obiegu Faktur i Praca Rozproszona**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić najnowszy stan prawny KSeF w Polsce (luty/kwiecień 2026 r.) oraz strukturę logiczną FA(3).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia z #144890 i rynku: integracja OCR/AI z Optimą, automatyczny import faktur kosztowych, mostki e-commerce -> Optima, wdrożenia pod KSeF.
   - Budżety: 4 500 - 16 000 zł. Klient: biuro rachunkowe, dyrektor finansowy (CFO), właściciel firmy handlowej/produkcyjnej.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Dokładny harmonogram KSeF 2.0: 1 lutego 2026 r. (obowiązek wystawiania dla dużych firm >200 mln zł oraz obowiązek ODBIORU dla wszystkich podatników; wyłączenie KSeF 1.0; wejście struktury logicznej FA(3) zastępującej FA(2)), 1 kwietnia 2026 r. (obowiązek wystawiania dla MŚP i JDG), 1 stycznia 2027 (najmniejsze podmioty).
   - Nowości w strukturze FA(3) (m.in. rozbicie stawki 0%, nowe reguły GTIN/EAN).
   - Metody integracji z Optimą:
     * Format Pracy Rozproszonej (pliki XML / format COM-ECO) – bezlicencyjny import dokumentów do rejestrów VAT i księgi.
     * Obiektowe API Comarch Optima (COM / CDNBase / Optima.Dokumenty) – pełna walidacja biznesowa, wymaga licencji integratora / klucza.
     * Web API Comarch (dla Optimy w chmurze).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Chcemy prosty OCR AI z czytaniem faktur PDF i zapisem do Optimy".
   - Mina 1 (KSeF vs OCR): Od 1 lutego 2026 faktury krajowe są w KSeF jako czysty XML FA(3). Budowanie OCR dla polskich faktur to palenie budżetu; OCR jest potrzebny TYLKO do faktur zagranicznych, paragonów, WZ i zleceń.
   - Mina 2 (Zaokrąglenia VAT): Dopuszczalne prawnie metody liczenia VAT (od sumy vs od pozycji). Rozbieżność 1-2 groszy przy fakturach wielopozycyjnych (np. 3 x 0.10 zł netto x 23% = 0.06 zł z pozycji vs 0.07 zł z sumy). Sztywna walidacja "na równość groszową" wyłoży automat na 15% faktur.
   - Mina 3 (Deduplikacja): Ten sam dokument trafia mailem, skanem i z KSeF. Klucz unikalności: NIP sprzedawcy + NumerFakturyOryginalny + DataWystawienia.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Gotowe, twarde otwarcia deklasujące amatorów w pierwszych 2 zdaniach (np. kwestia KSeF FA(3) eliminującego potrzebę OCR dla 80% dokumentów oraz pułapka tolerancji groszowej).
   - Wskazanie na konieczność bufora akceptacji / kolejki weryfikacji dla księgowej zamiast bezmyślnego wrzucania prosto do bazy.
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Twardy zakaz bezpośrednich INSERT-ów do bazy MS SQL Optimy (`CDN.TraNag`, `CDN.TraElem` itp.) – łamie licencję Comarch, unieważnia gwarancję i asystę, psuje triggery i sekwencje ID.
   - Zakaz obietnic 100% bezobsługowego księgowania bez udziału człowieka (brak akceptacji wyjątków to katastrofa podatkowa).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 6 000 - 15 000 ZŁ):
   - Rozbicie modułów: 1. Konektor źródeł (KSeF API + Skrzynka IMAP/Drive); 2. Silnik parsowania FA(3) + OCR AI dla zagranicy; 3. Moduł walidacji biznesowej i tolerancji VAT; 4. Mostek importowy do Comarch Optima (XML Praca Rozproszona lub COM); 5. Panel korekt i zatwierdzeń dla księgowości; 6. Wdrożenie i 30 dni asysty.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. czy Optima jest stacjonarna czy w Chmurze Comarch; jaki procent to faktury z NIP PL vs zagraniczne; czy posiadają moduł Handel/Kasa czy tylko Księga Handlowa).
"""
    },
    {
        "id": "tech_03_subiekt_sfera_ecommerce",
        "nazwa": "Subiekt GT & Subiekt nexo PRO (Sfera API, E-commerce, Magazyn, Baselinker)",
        "plik": OUTPUT_DIR / "tech_03_subiekt_sfera_ecommerce.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Integracje Subiekt GT i Subiekt nexo PRO, Sfera API, Synchronizacja E-commerce (Baselinker, WooCommerce, PrestaShop, Allegro), Gospodarka Magazynowa (WZ/PZ/ZK)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić różnice techniczne między Sferą dla GT a Sferą dla nexo PRO oraz specyfikę blokad bazodanowych w MS SQL.

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: integracja sklepu internetowego z Subiektem, dwukierunkowa synchronizacja stanów magazynowych i cen, automatyczne wystawianie paragonów i faktur imiennych, integracja z Baselinkerem.
   - Budżety: 3 000 - 12 000 zł. Profil klienta: właściciel e-commerce, hurtownia wielokanałowa, menedżer logistyki.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Różnice architektoniczne:
     * Subiekt GT Sfera: Architektura COM / OLE Automation, 32-bitowa, osobna licencja stanowiskowa Sfery (lub Sfera dla Subiekta GT), obiektowy model `gt = win32com.client.Dispatch("InsERT.Subiekt")`.
     * Subiekt nexo Sfera PRO: Natywna biblioteka .NET (`InsERT.Moria.*`), wbudowana w każdą licencję nexo PRO (nie wymaga dokupywania dodatku jak w GT), praca 64-bitowa, obsługa Dependency Injection.
   - Dokumenty handlowe i magazynowe: ZK (zamówienie od klienta) z rezerwacją stanu, WZ (wydanie zewnętrzne - skutek magazynowy), FS (faktura sprzedaży), PA/PAi (paragony fiskalne).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję prostego skryptu, który co 5 minut aktualizuje stany magazynowe w WooCommerce i pobiera zamówienia do Subiekta".
   - Mina 1 (Deadlocki i blokady w MS SQL): W Subiekcie GT baza `InsERT` intensywnie lockuje tabele `tw__Towar`, `dok__Dokument`, `st__Stan` przy zapisie. Puszczanie wielowątkowych requestów bez kolejkowania powoduje błędy `Lock timeout` lub błędy COM.
   - Mina 2 (Nadmiarowa sprzedaż / Overselling): Brak rezerwacji twardych (status magazynowy ZK) powoduje, że ten sam towar zostaje sprzedany na Allegro i w sklepie internetowym zanim Subiekt zdejmie go ze stanu.
   - Mina 3 (Wariantowość i cechy towarów): Rozbieżność w mapowaniu ID produktów z platform e-commerce (np. warianty rozmiar/kolor w PrestaShop/Woo vs kartoteki w Subiekcie powiązane kodem kreskowym EAN/PLU lub polem własnym).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Natychmiastowe wskazanie na konieczność kolejkowania transakcji (buforowanie asynchroniczne) i rezerwacji stanów (ZK z rezerwacją) w pierwszych 2 zdaniach.
   - Pytanie o wersję: Czy klient posiada Subiekta GT ze Sferą czy nexo PRO, oraz czy baza działa na SQL Server Standard czy Express (ograniczenia 1GB RAM / 10GB bazy w SQL Express).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz bezpośrednich operacji INSERT/UPDATE na tabelach `dok__Dokument`, `tw__Towar`, `dok_Pozycja` bez Sfery! Bezpośredni SQL rozspójnia stan magazynowy, nie przelicza kosztów zakupu FIFO/LIFO i niszczy bazę.
   - Zakaz pisania o "ciągłym pollingu bazy co 10 sekund" bez kolejkowania i mechanizmu timestampów/delta sync.
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 500 - 10 000 ZŁ):
   - Moduły: 1. Usługa Windows / demon integracyjny (wrapper na Sferę COM/.NET); 2. Kolejka asynchroniczna zleceń (RabbitMQ / Redis / SQLite FIFO); 3. Konektor E-commerce (API Baselinker/WooCommerce/Allegro REST); 4. Silnik mapowania kartotek i cen wielopoziomowych; 5. Moduł logowania transakcji, obsługi błędów i automatycznych powiadomień.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie zmuszające klienta do odpisania na priv (np. o wersję GT vs nexo PRO, obecność licencji Sfery, liczbę magazynów i wolumen zamówień na dobę).
"""
    },
    {
        "id": "tech_04_python_fastapi_automatyzacje",
        "nazwa": "Python, FastAPI, Kolejki Zadań i Architektura Automatyzacji B2B (n8n on-prem vs Make)",
        "plik": OUTPUT_DIR / "tech_04_python_fastapi_automatyzacje.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Zaawansowane Automatyzacje B2B, Backend w Pythonie / FastAPI, Asynchroniczne Webhooki, Kolejki Zadań (Celery/Redis) i Self-Hosted n8n vs SaaS**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić aktualne trendy w architekturze mikroserwisów automatyzacyjnych B2B oraz optymalizację kosztów operacyjnych API/Cloud.

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME:
   - Zlecenia: budowa mikroserwisów integracyjnych, webhooki płatności i zamówień, data pipelines (zbieranie, czyszczenie i przesyłanie danych), automatyzacje procesów w firmach (CRM -> ERP -> BI).
   - Budżety: 3 500 - 14 000 zł. Profil klienta: CTO software house'u, founder startupu, operations manager w firmie usługowej.
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK:
   - Nowoczesny stack: FastAPI (asynchroniczny ASGI, Pydantic v2 dla błyskawicznej walidacji typów), SQLAlchemy 2.0 (asyncio).
   - Przetwarzanie asynchroniczne i kolejki: Celery + Redis / RabbitMQ, Redis Streams, RQ, Arq.
   - Porównanie ekonomiczne i architektoniczne: Self-hosted n8n na serwerze Linux VPS (Docker Compose) vs chmurowy Make.com / Zapier. Koszt 100 000 operacji w Make.com to setki euro miesięcznie; w self-hosted n8n / FastAPI to koszt serwera za 30-50 zł/mies.
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (CO KLIENT PISZE VS CO GO UTOPI):
   - Klient pisze: "Potrzebuję prostego skryptu / webhooka, który po opłaceniu zamówienia w Stripe przesyła dane do CRM i wystawia fakturę".
   - Mina 1 (Brak idempotencji): Bramki płatności (Stripe, PayU, Przelewy24) wysyłają webhooki z gwarancją 'at-least-once'. Przy chwilowym lagu sieciowym webhook przyjdzie 2-3 razy. Bez klucza idempotencji klient dostanie 2 faktury, a towar zostanie wydany podwójnie!
   - Mina 2 (Brak kolejkowania i timeouty): Zewnętrzne API (np. CRM klienta lub ERP) ma downtime lub odpowiada 15 sekund. Synchroniczny skrypt blokuje wątek i zwraca błąd 504 do Stripe, co powoduje wyłączenie webhooka przez dostawcę płatności.
   - Mina 3 (Zarządzanie sekretami i bezpieczeństwo): Hardcodowanie API keys w kodzie, brak weryfikacji sygnatur HMAC w przychodzących webhookach.
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (DEKLASACJA AMATORÓW):
   - Otwarcie problemem idempotencji i architektury 'Fast-Ack + Background Worker' w pierwszych 2 zdaniach (odbieramy webhook, zwracamy 200 OK w 50ms, a zadanie ląduje w kolejce Redis z retry policy).
   - Wskazanie na oszczędność kosztów operacyjnych (self-hosted vs Make.com).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ):
   - Kategoryczny zakaz synchronicznego przetwarzania webhooków bezpośrednio w endpointzie HTTP.
   - Zakaz ignorowania nagłówków weryfikacyjnych (np. Stripe-Signature) – otwiera to system na fałszywe żądania i wstrzykiwanie danych.
   - Zakaz proponowania rozwiązań bez bazy do śledzenia statusów transakcji (audyt trail).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (WYCENA 4 500 - 12 000 ZŁ):
   - Moduły: 1. Bezpieczna warstwa odbiorcza API (FastAPI + walidacja HMAC + bufor idempotencji); 2. Silnik kolejkowy (Redis + Celery worker z Dead Letter Queue); 3. Konektory integracyjne z systemami trzecimi (obsługa rate limitów i exponential backoff); 4. Baza danych audytu i logowanie (PostgreSQL + Sentry); 5. Konteneryzacja (Docker Compose) i instrukcja wdrożenia produkcyjnego.
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE (W ŚRODEK TEKSTU):
   - 2-3 pytania inżynierskie kwalifikujące klienta (np. o wolumen transakcji na minutę w szczycie, wymóg SLA na czas przetworzenia, preferencje hostingowe - VPS klienta czy AWS/GCP).
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
    print("=== Generator Elitarnych Kart Wiedzy Technologicznej dla Bota Useme ===")
    sukcesy = 0
    for zadanie in TASKS:
        ok = wykonaj_zadanie(zadanie)
        if ok:
            sukcesy += 1
        time.sleep(2)  # Krótka pauza między requestami
        
    print(f"\n=======================================================")
    print(f"[KONIEC] Pomyślnie ukończono {sukcesy}/{len(TASKS)} kart technologicznych!")

if __name__ == "__main__":
    main()
