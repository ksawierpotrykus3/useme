# -*- coding: utf-8 -*-
"""
Skrypt: eksploruj_typy_klientow_i_technologie.py
Cel: Dogłębna analiza zleceniodawców z 470 zleceń Useme (56 wygranych + 414 zamkniętych).
Identyfikuje profile ludzi, ich język, motywacje i lęki.
Kategoryzuje: Baza / Podgrupa / Nowy Typ.
Bada różnice w profilach klientów w zależności od technologii.
"""

import json
import os
import re
import requests
import time

WYGRANE_PATH = "Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json"
PRZEGRANE_PATH = "Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json"
OUT_FILE = "Projekty_autorskie/useme_core/badania/analizy/typy_klientow/analiza_gleboka_typow_i_technologii.md"

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"

def load_data():
    with open(WYGRANE_PATH, "r", encoding="utf-8") as f:
        wygrane = json.load(f)
    with open(PRZEGRANE_PATH, "r", encoding="utf-8") as f:
        przegrane = json.load(f)
    
    all_jobs = []
    for w in wygrane:
        all_jobs.append({
            "source": "wygrana_priv",
            "id": w.get("job_id") or w.get("offer_id"),
            "title": w.get("title", ""),
            "client": w.get("client", ""),
            "budget": w.get("budget", ""),
            "desc": w.get("job_description", "") or "",
            "thread_size": w.get("thread_size", 0),
            "our_proposal": w.get("our_proposal", "") or ""
        })
    for p in przegrane:
        all_jobs.append({
            "source": "przegrana_rynek",
            "id": p.get("offer_id"),
            "title": p.get("title", ""),
            "client": p.get("client", ""),
            "budget": p.get("budget", ""),
            "desc": p.get("job_description", "") or "",
            "thread_size": 0,
            "our_proposal": p.get("our_proposal", "") or ""
        })
    return all_jobs

def extract_client_archetype_signals(job):
    full_text = f"{job['title']} {job['desc']}".lower()
    signals = []
    
    if any(k in full_text for k in ["szukamy do zespołu", "dla naszego klienta", "podwykonawc", "b2b", "senior", "mid", "junior", "godzinowk", "stawka godzinowa", "software house", "agencja"]):
        signals.append("SIGNAL_AGENCY_OR_TEAM")
    if any(k in full_text for k in ["sklep", "shoper", "prestashop", "shopify", "woocommerce", "baselinker", "idosell", "koszyk", "magazyn", "hurtowni", "allegro"]):
        signals.append("SIGNAL_ECOMMERCE")
    if any(k in full_text for k in ["subiekt", "optima", "enova", "ksef", "faktur", "comarch", "insert", "cnc", "produkcyjn", "hale", "maszyn", "wz"]):
        signals.append("SIGNAL_TRADITIONAL_MSP_ERP")
    if any(k in full_text for k in ["startup", "mvp", "innowacyjn", "pomysł na aplikację", "wspólnik", "platforma", "portal", "saas", "od zera"]):
        signals.append("SIGNAL_STARTUP_MVP")
    if any(k in full_text for k in ["poprzedni programista", "niedokończon", "poprawki po", "kod jest gotowy ale", "zniknął", "nie odbiera", "naprawa błędów", "rozgrzeban"]):
        signals.append("SIGNAL_RESCUE_BURNED")
    if any(k in full_text for k in ["szef kazał", "w imieniu zarządu", "w imieniu firmy", "szukamy dla firmy", "właściciel prosił", "nasz dział", "asystent"]):
        signals.append("SIGNAL_DELEGATED_EMPLOYEE")
    if any(k in full_text for k in ["scraper", "scraping", "bot", "pobieranie danych", "crawler", "olx", "otomoto", "vinted", "monitorowani", "antybot"]):
        signals.append("SIGNAL_BOTS_SCRAPING")
    if any(k in full_text for k in ["gabinet", "klinik", "lekarz", "psycholog", "kurs", "szkoleni", "dietetyk", "trener", "pacjent", "konsultacj"]):
        signals.append("SIGNAL_EXPERT_SERVICES")
    if any(k in full_text for k in ["na wczoraj", "pilne", "szybka poprawka", "błąd 500", "nie działa", "awaria", "drobne zlecenie"]):
        signals.append("SIGNAL_QUICK_FIX")
    
    tech_keywords = ["python", "php", "js", "react", "vue", "flutter", "kotlin", "swift", "docker", "c#", ".net", "sql", "api", "node"]
    if not any(k in full_text for k in tech_keywords):
        signals.append("SIGNAL_PURE_BUSINESS_AGNOSTIC")
        
    return signals

def analyze_tech_correlation(jobs):
    categories = {
        "ERP_B2B": ["subiekt", "optima", "enova", "ksef", "insert", "comarch", "odoo", "erp"],
        "SCRAPING_BOTS": ["scraping", "scraper", "bot", "selenium", "playwright", "crawler", "antybot"],
        "MOBILE": ["android", "ios", "kotlin", "swift", "flutter", "react native", "aplikacja mobilna"],
        "PYTHON_AUTOMATION": ["python", "fastapi", "django", "n8n", "make", "celery", "skrypt"],
        "ECOMMERCE": ["prestashop", "shopify", "shoper", "idosell", "baselinker", "woocommerce"],
        "TECH_AGNOSTIC": ["automatyzacja", "integracja", "baza", "system", "program"]
    }
    
    tech_stats = {k: {"total": 0, "signals": {}} for k in categories}
    
    for j in jobs:
        txt = f"{j['title']} {j['desc']}".lower()
        sigs = extract_client_archetype_signals(j)
        
        for cat, kw_list in categories.items():
            if cat == "TECH_AGNOSTIC":
                if not any(k in txt for sub in categories.values() if sub != kw_list for k in sub):
                    tech_stats[cat]["total"] += 1
                    for s in sigs:
                        tech_stats[cat]["signals"][s] = tech_stats[cat]["signals"].get(s, 0) + 1
            else:
                if any(k in txt for k in kw_list):
                    tech_stats[cat]["total"] += 1
                    for s in sigs:
                        tech_stats[cat]["signals"][s] = tech_stats[cat]["signals"].get(s, 0) + 1
                        
    return tech_stats

def get_representative_quotes(jobs):
    # Wybieramy konkretne cytaty i fragmenty opisujące ludzi w różnych domenach
    quotes = {}
    
    # 1. ERP & B2B
    erp_samples = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in ["subiekt", "optima", "enova", "ksef", "topsolid"])][:4]
    quotes["ERP_B2B"] = [{
        "client": j["client"], "title": j["title"], "budget": j["budget"],
        "snippet": j["desc"][:300].replace("\n", " ")
    } for j in erp_samples]
    
    # 2. Scraping & Boty
    scraping_samples = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in ["bot", "scraping", "crawler", "olx", "vinted"])][:4]
    quotes["SCRAPING_BOTS"] = [{
        "client": j["client"], "title": j["title"], "budget": j["budget"],
        "snippet": j["desc"][:300].replace("\n", " ")
    } for j in scraping_samples]
    
    # 3. Mobile
    mobile_samples = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in ["kotlin", "swift", "flutter", "aplikacja mobilna"])][:4]
    quotes["MOBILE"] = [{
        "client": j["client"], "title": j["title"], "budget": j["budget"],
        "snippet": j["desc"][:300].replace("\n", " ")
    } for j in mobile_samples]
    
    # 4. Tech-Agnostic
    agnostic_samples = [j for j in jobs if "SIGNAL_PURE_BUSINESS_AGNOSTIC" in extract_client_archetype_signals(j)][:4]
    quotes["TECH_AGNOSTIC"] = [{
        "client": j["client"], "title": j["title"], "budget": j["budget"],
        "snippet": j["desc"][:300].replace("\n", " ")
    } for j in agnostic_samples]

    # 5. Zlecenia z długimi wątkami (gdzie doszło do intensywnej wymiany myśli)
    deep_threads = sorted([j for j in jobs if j['thread_size'] > 5], key=lambda x: x['thread_size'], reverse=True)[:5]
    quotes["DEEP_THREADS_HUMAN_INSIGHT"] = [{
        "client": j["client"], "title": j["title"], "thread_size": j["thread_size"],
        "snippet": j["desc"][:350].replace("\n", " ")
    } for j in deep_threads]
    
    return quotes

def main():
    print("[*] Wczytywanie danych z bazy 470 zleceń...")
    jobs = load_data()
    print(f"[+] Załadowano {len(jobs)} zleceń.")
    
    tech_stats = analyze_tech_correlation(jobs)
    quotes = get_representative_quotes(jobs)
    
    system_prompt = """Jesteś Elitarnym Zespołem Analitycznym i Psychologiem Biznesu B2B badającym rynek Useme.
Twoim celem jest przeprowadzenie bezlitosnej, chirurgicznej dekonstrukcji LUDZI (zleceniodawców) stojących za zleceniami.
Zgodnie z poleceniem:
1. NAJPIERW OPISUJESZ TO, CO WIDZISZ: kim są ci ludzie, w jakim stanie psychicznym piszą, co ich boli, czego się boją, jak mówią.
2. KLASYFIKACJA HIERARCHICZNA:
   - Jeśli pasuje do znanego typu -> DOPASUJ DO BAZY.
   - Jeśli pasuje, ale wykazuje specyficzny wariant -> STWÓRZ PODGRUPĘ.
   - Jeśli to coś całkowicie nowego, co dotychczas umykało -> ZDEFINIUJ CAŁKOWICIE NOWY TYP.
3. KORELACJA Z TECHNOLOGIĄ:
   - Zbadaj twardo, czy i jak typy klientów różnią się w zależności od technologii (ERP vs Scraping vs Mobile vs Python vs Tech-Agnostic vs E-commerce).
   - Wykaż różnice w: poziomie wiedzy, tolerancji na żargon IT, lęku przed ryzykiem, procesie decyzyjnym (kto płaci i zatwierdza) oraz elastyczności cenowej.
NARAZIE SKUP SIĘ WYŁĄCZNIE NA TYPACH, PODGRUPACH I RÓŻNICACH WOBEC TECHNOLOGII. Nie twórz jeszcze gotowych szablonów ofert."""

    user_prompt = f"""DANE WEJŚCIOWE Z EMPIRYCZNEJ BAZY USEME (470 ZLECEŃ):

1. ROZKŁAD ILOŚCIOWY SYGNAŁÓW W DOMENACH TECHNOLOGICZNYCH:
{json.dumps(tech_stats, indent=2, ensure_ascii=False)}

2. REPREZENTATYWNE CYTATY I FRAGMENTY ZLECEŃ POKAZUJĄCE LUDZI:
{json.dumps(quotes, indent=2, ensure_ascii=False)}

WYGENERUJ DOKŁADNY, SPÓJNY RAPORT W FORMACIE MARKDOWN:

# POGŁĘBIONY AUDYT BEHAWIORALNY ZLECENIODAWCÓW USEME
## DEKONSTRUKCJA PSYCHOLOGICZNA, TAKSONOMIA (BAZA / PODGRUPY / NOWE TYPY) ORAZ MATRYCA ZALEŻNOŚCI OD TECHNOLOGII

### SEKCJA 1: CO WIDZI ZESPÓŁ ANALLITYCZNY W ZLECENIACH? (OBRAZ CZŁOWIEKA)
- Kto naprawdę siedzi po drugiej stronie ekranu?
- Przegląd stanów emocjonalnych: paranoja po poprzednim wykonawcy, presja szefa, gorączka marzyciela, pragmatyzm magazyniera/księgowej.
- Język i maski: jak klienci maskują brak wiedzy technicznej lub brak budżetu.

### SEKCJA 2: PEŁNA TAKSONOMIA TYPÓW (BAZA -> PODGRUPY -> NOWE TYPY)
Ustrukturyzuj każdy typ wedle schematu:
- **Nazwa Typu** (Status: TYP BAZOWY / PODGRUPA / CAŁKOWICIE NOWY TYP)
- **Kim jest człowiek?** (Rola w firmie, decyzyjność, budżet)
- **Główny lęk i motywacja**
- **Symptomy w treści zlecenia** (zwroty, styl opisu, długość)
- **Dynamika na priv** (czy odpisuje szybko, ile wiadomości generuje, czego oczekuje)

*Wymagane do uwzględnienia:*
- Tradycyjne MŚP (i podgrupy: Właściciel Senior vs Oddelegowana Księgowa/Pracownik)
- E-commerce (i podgrupy: Dojrzały Sklep z Subiektem/ERP vs Nerwowy Dropshipper)
- Startup Founder (i podgrupy: Zabezpieczony Rundy Seed vs Wizjoner szukający darmowego CTO za udziały)
- Agencja / Software House (i podgrupy: PM w pożarze deadline'u vs Rekruter pod przykrywką łowiący na godziny)
- Ekspert Dziedzinowy / Edukacja (Lekarz, Psycholog - case Doktor Monika)
- Quick IT Fix (Awaria / Pożar)
- NOWE TYPY (np. Klient Sparzony po ucieczce poprzednika; Zlecający Prywatny / Hobbysta)

### SEKCJA 3: CZY TYPY KLIENTÓW RÓŻNIĄ SIĘ W ZALEŻNOŚCI OD TECHNOLOGII? (ANALIZA CROSS-TECH)
Dokonaj precyzyjnego porównania:
1. **ERP & B2B (Optima, Subiekt, Enova, KSeF)**: Jaki to typ? Czego wymaga? Jaki lęk nim kieruje?
2. **Web Scraping & Boty (Cloudflare, OLX, Vinted, Boty)**: Jaki to typ? Czego wymaga? Jaki lęk nim kieruje?
3. **Mobile & Hardware (Android Kotlin, iOS Swift, Zebra)**: Jaki to typ?
4. **Python & Automatyzacje procesowe (FastAPI, n8n, Make)**: Jaki to typ?
5. **Tech-Agnostic (33% rynku - zero technologii)**: Jaki to typ człowieka? Dlaczego nie podał technologii?
6. **Tabela Podsumowująca Różnice Cross-Tech**:
   | Domena Technologiczna | Dominujący Typ Klienta | Tolerancja na Żargon | Prędkość Decyzji | Główny Lęk | Wrażliwość Cenowa |

Pisz zwięźle, inżyniersko, bezpośrednio i bez komunałów.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }

    print(f"[*] Wysyłam zapytanie do {MODEL} (timeout=300s)...")
    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=300)
        if r.status_code == 200:
            result = r.json()["choices"][0]["message"]["content"]
            with open(OUT_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            dt = round(time.time() - t0, 1)
            print(f"[+] SUKCES! Zapisano analizę do: {OUT_FILE} ({len(result)} znaków) w {dt}s.")
        else:
            print(f"[!] Błąd API {r.status_code}: {r.text[:500]}")
    except Exception as e:
        print(f"[!] Błąd połączenia: {e}")

if __name__ == "__main__":
    main()
