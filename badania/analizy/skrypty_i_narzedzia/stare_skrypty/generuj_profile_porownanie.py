# -*- coding: utf-8 -*-
"""Porównanie 2 wariantów wiedzy technologicznej dla:
WEB SCRAPING, BOTY I OMIJANIE ANTY-BOTÓW (Playwright / Cloudflare / WAF).
Wariant 1: Rygorystyczny schemat 6 sekcji inżynierskich.
Wariant 2: Wolnościowe, autonomiczne podejście modelu (laboratorium_modeli).
"""

import json
from pathlib import Path
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-chat"

OUTPUT_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\badania\analizy\technologie\baza_wiedzy")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_WARIANT_1 = (
    "Pracujesz w bezwzględnym rygorze inżynierskim. Zero poezji, zero pustego marketingu. "
    "Konkret, twarde fakty techniczne, reverse-engineering, protokoły sieciowe i mechanika omijania bot-detection. Pisz po polsku."
)

PROMPT_WARIANT_1 = """
Przygotuj profil wiedzy technologicznej dla: **Web Scraping, Boty Danych i Omijanie Zabezpieczeń (Playwright / Cloudflare / WAF)** do wykorzystania przez bota ofertowego na Useme.
Celem jest wyposażyć bota w twardą wiedzę inżynierską, która natychmiast prowokuje zleceniodawcę do odpisania na priv.

Struktura profilu MUSI zawierać dokładnie 6 sekcji:
1. METADANE RYNKOWE I BIZNESOWE (zlecenia na scraping, monitoring cen, boty wystawiające np. OLX, migracje baz firm, budżety 1 500 - 8 500 zł).
2. KRYTYCZNE ZMIANY W TECHNOLOGII I OCHRONIE (stan na 2026 r.: Cloudflare Turnstile, DataDome, Akamai, sygnatury TLS JA3/JA4, wykrywanie flag navigator.webdriver w CDP, canvas/WebGL fingerprinting, limity zapytań).
3. PRAWDZIWY BÓL KLIENTA (UKRYTA MINA) - co klient pisze w zleceniu (np. 'potrzebuję prostego skryptu do pobierania cen') vs co jest prawdziwą techniczną miną pod maską (np. blokada IP po 50 requestach, dynamiczny DOM renderowany w Shadow DOM, rotacja selektorów CSS przy aktualizacjach portalu, memory leak przy wielowątkowym Chromium).
4. ZABÓJCZY DOWÓD TECHNOLOGICZNY (INSIGHT DO PIERWSZYCH 2 ZDAŃ) - twardy fakt deklasujący amatorów z Selenium/BeautifulSoup (np. przechwycenie nieudokumentowanego prywatnego JSON API z aplikacji mobilnej/frontendu zamiast parsowania ciężkiego HTML; użycie curl_cffi/impersonate zamiast odpalania 50 instancji przeglądarki).
5. CZERWONA LISTA / ANTYWZORCE (CZEGO KATEGORYCZNIE NIE PISAĆ) - zakazy (zakaz obietnic 'darmowych publicznych proxy', zakaz pisania o BeautifulSoup do stron z WAF, zakaz deklarowania 100% niewykrywalności bez rotacji IP).
6. GOTOWE PYTANIA ROBOCZE (W TOKU ANALIZY) - 2-3 precyzyjne pytania inżynierskie wplecione w analizę problemu, na które klient musi odpisać na priv.
"""

SYSTEM_WARIANT_2 = (
    "Jesteś elitarnym inżynierem reverse-engineeringu, scraping-ninja i architektem wygrywania kontraktów technicznych. "
    "Masz całkowitą autonomię twórczą. Pisz po polsku, bezpośrednio, bez gotowych szablonów, z potężną wiedzą o protokołach, sieci i omijaniu bot-detection."
)

PROMPT_WARIANT_2 = """
Przygotuj profil wiedzy dla bota ofertowego pod dziedzinę: **Web Scraping, Boty Danych i Automatyzacje (Anty-WAF, Cloudflare, Ekstrakcja)**.
Celem bota jest jedno: **sprawić, żeby klient zlecający bota lub scraping natychmiast odpisał na priv**, miażdżąc 30 innych ofert od amatorów, którzy proponują proste Selenium i padną na pierwszej captchy.

Nie narzucamy Ci żadnego schematu ani szablonu. Sam zaprojektuj strukturę tego dokumentu.
Zastanów się:
- Co sprawia, że zleceniodawca myśli: 'ten człowiek naprawdę wie jak wyciągnąć te dane i nie wyłoży się po 2 dniach'?
- Jakie są kluczowe dźwignie w scrapingu (koszty proxy, reverse-engineering API vs renderowanie DOM, stabilność crona, formaty wyjściowe)?
- Jak wyposażyć bota w gotowe, bezbłędne schematy inżynierskie, żeby oferta brzmiała jak konkretna robocza diagnoza fachowca?

Stwórz profil w takiej formie, jaką uważasz za najskuteczniejszą.
"""

def generuj(prompt, system, plik_wyjsciowy):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "stream": False
    }
    print(f"[START] Generuję: {plik_wyjsciowy.name}...")
    r = requests.post(PROXY_URL, json=payload, timeout=180)
    if r.status_code != 200:
        raise RuntimeError(f"Błąd HTTP {r.status_code}: {r.text}")
    
    tresc = r.json()["choices"][0]["message"]["content"]
    plik_wyjsciowy.write_text(tresc, encoding="utf-8")
    print(f"[OK] Zapisano do: {plik_wyjsciowy.name} ({len(tresc)} znaków)")
    return tresc

if __name__ == "__main__":
    p1 = OUTPUT_DIR / "tech_scraping_wariant_1_schemat.md"
    p2 = OUTPUT_DIR / "tech_scraping_wariant_2_wolnosciowy.md"
    
    t1 = generuj(PROMPT_WARIANT_1, SYSTEM_WARIANT_1, p1)
    t2 = generuj(PROMPT_WARIANT_2, SYSTEM_WARIANT_2, p2)
    print("\n[SUKCES] Wygenerowano oba warianty dla Web Scrapingu!")
