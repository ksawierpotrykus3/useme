# -*- coding: utf-8 -*-
"""Generator pojedynczej karty wiedzy dla Bota Useme.
Uruchamiany sekwencyjnie: python generuj_pojedyncza_karte.py <task_id>
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
- Zlecenia niszowe i nietechniczne wygrywa się precyzyjną diagnozą problemu i zerem żargonu, gdy klient jest nietechniczny, LUB głęboką wiedzą inżynierską, gdy klient szuka eksperta.
- Elita wygrywa zlecenia, ponieważ:
  1. OTWIERA PROBLEMEM W PIERWSZYCH 2 ZDANIACH (zamiast pisać o swoim stażu, uderza w sedno problemu).
  2. ZNA AKTUALNE REALIA NA 2026 ROK (aktualne protokoły, wersje API, limity, technologie).
  3. ZADAJE 2-3 CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODKU ANALIZY (zmusza klienta do natychmiastowego odpisania na priv).
  4. WSKAZUJE ANTYWZORCE I CZERWONE FLAGI.
  5. ROZBIJA WYCENĘ NA LOGICZNE MODUŁY ARCHITEKTONICZNE (nie ryczałt).

ZASADY TREŚCI:
- Zero udawania mowy ludzkiej ("no hej", "w sumie", sztuczne idiomy).
- Zero proponowania spotkań wideo, Google Meet czy rozmów telefonicznych (komunikacja wyłącznie pisemna na priv).
- Twarde, zweryfikowane fakty inżynierskie, zaktualizowane pod kątem 2026 roku.
- Język: Polski, wysoce precyzyjny.
"""

DEFINICJE_ZADAN = {
    "tech_12_voip_asterisk_sip": {
        "nazwa": "VoIP, Centrale Asterisk, SIP Trunking i FreePBX",
        "plik": OUTPUT_DIR / "tech_12_voip_asterisk_sip.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **VoIP, Centrale Asterisk / FreePBX, Protokół SIP (PJSIP), Trunking Operatorski, IVR i Integracje Call Center z CRM (Transkrypcja AI)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić nowoczesne wdrożenia VoIP w 2026 roku (całkowite wycofanie chan_sip na rzecz res_pjsip w nowym Asterisku, WebRTC w przeglądarce, integracja nagrań z modelami STT Whisper/Deepgram w czasie rzeczywistym).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME (budżety 2 500 – 10 000 zł, Win Rate 40%).
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK (PJSIP vs chan_sip, NAT/RTP port range, kodeki Opus/G.711, ARI/AMI interfejsy).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (One-Way Audio za NAT-em, włamania na port 5060 i rachunki na tysiące euro bez fail2ban).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (deklasacja amatorów na start).
5. CZERWONA LISTA / ANTYWZORCE (czego kategorycznie nie pisać).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (wycena 3 500 – 9 000 zł).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU (zmuszające do priv).
"""
    },
    "tech_13_enova365_odoo_erp": {
        "nazwa": "Systemy ERP: Enova365 (Soneta.Business) oraz Odoo ERP (Python/OWL)",
        "plik": OUTPUT_DIR / "tech_13_enova365_odoo_erp.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Zaawansowane Integracje ERP: Enova365 (Architektura .NET Soneta.Business, Harmonogram Zadań, API) oraz Odoo ERP (Moduły Python, OWL Framework, Integracja z Polskim Prawem i KSeF)**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić stan ekosystemu Enova365 (wersje 2404+, obsługa KSeF, web api Soneta) oraz Odoo (wersje 17 i 18, polska lokalizacja podatkowa, integracje headless).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME (budżety 4 500 – 16 000 zł).
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK (Soneta.Business w C#, sesje transakcyjne, Odoo ORM, dziedziczenie _inherit).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (błędy LockException w Enova, modyfikacja rdzenia Odoo blokująca aktualizacje).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (deklasacja amatorów).
5. CZERWONA LISTA / ANTYWZORCE (zakaz bezpośredniego SQL do Enova, zakaz edycji odoo/addons/core).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (wycena 5 000 – 14 000 zł).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU (zmuszające do priv).
"""
    },
    "tech_14_google_sheets_appscript": {
        "nazwa": "Google Sheets, Apps Script & Workspace Automation (API Quotas, Lekki Backend)",
        "plik": OUTPUT_DIR / "tech_14_google_sheets_appscript.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Google Sheets, Google Apps Script, Automatyzacje Google Workspace (Gmail / Drive), Omijanie Limitów Quotas i Architektura Arkusza jako Lekki Backend**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić aktualne limity Google Apps Script Quotas w 2026 roku (twardy limit 6 minut na wykonanie skryptu, limity URLFetchApp, trigger ograniczenia per dzień, operacje wsadowe setValues).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME (budżety 1 500 – 6 000 zł, Win Rate 13.3%).
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK (twardy limit 6 minut, operacje wsadowe getValues/setValues, PropertiesService).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (timeout po 6 minutach przy 5000 requestów, pętle komórka po komórce).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (wzorzec batch processor z continuations trigger, fetchAll).
5. CZERWONA LISTA / ANTYWZORCE (zakaz pętli for z setValue, zakaz obietnic skryptów 30-minutowych bez kolejkowania).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (wycena 2 000 – 5 500 zł).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU (zmuszające do priv).
"""
    },
    "tech_15_ai_llm_rag_pipelines": {
        "nazwa": "Sztuczna Inteligencja, RAG, Bazy Wektorowe i Integracje LLM (OpenAI, Anthropic, Qdrant)",
        "plik": OUTPUT_DIR / "tech_15_ai_llm_rag_pipelines.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy inżynierskiej dla bota ofertowego:
TEMAT: **Architektury RAG (Retrieval-Augmented Generation), Wyszukiwanie Hybrydowe, Bazy Wektorowe (Qdrant / pgvector), Integracje LLM (OpenAI, Claude, DeepSeek) i Optymalizacja Kosztów Tokenów**.

Wykorzystaj wyszukiwarkę sieciową, aby sprawdzić nowoczesny stan inżynierii RAG w 2026 roku (hybrydowe wyszukiwanie gęste wektory + rzadkie BM25 / SPLADE, re-ranking z modelami Cross-Encoder / Cohere Rerank, Structured Outputs ze ścisłą walidacją JSON Schema).

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME (budżety 4 500 – 16 000 zł).
2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK (Naiwny RAG vs Hybrydowy RAG + Reranker, Qdrant vs pgvector, strict JSON schemas).
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA (halucynacje, brak cytowań, koszty tokenów bez routingu na małe modele).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (otwarcie o hybrydowym searchu BM25+wektory i guardrails).
5. CZERWONA LISTA / ANTYWZORCE (zakaz prostego dzielenia po 500 znaków, zakaz braku walidacji schematów).
6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE (wycena 5 500 – 15 000 zł).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU (zmuszające do priv).
"""
    },
    "tech_16_tech_agnostic_biznes": {
        "nazwa": "Segment Tech-Agnostic (33% Rynku Useme) — Sprzedaż Czysto Biznesowa bez Żargonu",
        "plik": OUTPUT_DIR / "tech_16_tech_agnostic_biznes.md",
        "prompt": """Przygotuj kompletną, oficjalną kartę wiedzy strategicznej dla bota ofertowego:
TEMAT: **Obsługa Segmentu Tech-Agnostic (155 zleceń w badaniu, 33% całego rynku Useme) — Zlecenia bez Podanej Technologii, Sprzedaż Językiem Rezultatu Biznesowego, Rozwiązania Pudełkowe i Bezpieczne Wdrożenia**.

Struktura karty musi zawierać dokładnie:
1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW (155 zleceń bez podanej technologii, budżety 1 500 – 7 000 zł, klient nietechniczny).
2. ZASADY PSYCHOLOGICZNE I JĘZYKOWE (kategoryczny zakaz żargonu programistycznego, język rezultatu: "program działa w tle jednym kliknięciem").
3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA NIETECHNICZNEGO (strach przed konsolą tekstową, strach przed zniknięciem programisty).
4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ (otwarcie opisujące gotowy stan docelowy bez żargonu, program pudełkowy z ikoną na pulpicie).
5. CZERWONA LISTA / ANTYWZORCE (zakaz chwalenia się stackiem React/FastAPI/Postgres, zakaz skomplikowanych pytań).
6. PRODUKCYJNA ARCHITEKTURA WDROŻENIA BIZNESOWEGO (wycena 2 500 – 6 500 zł rozbita na etapy zrozumiałe dla laika).
7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE DLA KLIENTA BIZNESOWEGO (język formatu wyników i wygody).
"""
    }
}

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        print(f"Użycie: python {sys.argv[0]} <task_id>")
        print(f"Dostępne zadania: {list(DEFINICJE_ZADAN.keys())}")
        sys.exit(1)
        
    task_id = sys.argv[1]
    if task_id not in DEFINICJE_ZADAN:
        print(f"Nieznane zadanie: {task_id}")
        sys.exit(1)
        
    zadanie = DEFINICJE_ZADAN[task_id]
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
            sys.exit(1)
            
        dane = r.json()
        tresc = dane["choices"][0]["message"]["content"]
        
        # Zapis do pliku UTF-8
        zadanie["plik"].write_text(tresc, encoding="utf-8")
        duration = round(time.time() - start_t, 1)
        print(f"[SUKCES] Wygenerowano i zapisano: {zadanie['plik'].name} ({len(tresc)} znaków) w {duration}s")
    except Exception as e:
        print(f"[WYJĄTEK] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
