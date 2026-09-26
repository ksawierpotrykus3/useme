# -*- coding: utf-8 -*-
"""
Skrypt: weryfikuj_taksonomie_klientow.py
Cel: Rygorystyczny test falsyfikacyjny i statystyczny taksonomii klientów.
Sprawdza zgodność z danymi empirycznymi 470 zleceń (56 wygranych + 414 zamkniętych),
weryfikuje tezy behawioralne, wykrywa ewentualne przekłamania lub nadinterpretacje.
"""

import json
import os
import re
import requests
import time

WYGRANE_PATH = "Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json"
PRZEGRANE_PATH = "Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json"
OUT_REPORT = "Projekty_autorskie/useme_core/badania/analizy/typy_klientow/raport_falsyfikacji_i_weryfikacji_typow.md"

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
            "our_price": w.get("our_price", "")
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
            "our_price": p.get("our_price", "")
        })
    return all_jobs

def run_empirical_metrics(jobs):
    metrics = {}
    
    # 1. Zlecenia "Klient Sparzony / Rescue" (poprzedni programista, dokończenie, audyt fuszerki)
    rescue_keywords = ["poprzedni", "dokończ", "poprawk", "po innym", "rozgrzeban", "zniknął", "audyt", "sabotaż", "naprawi"]
    rescue_jobs = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in rescue_keywords)]
    metrics["rescue_count"] = len(rescue_jobs)
    metrics["rescue_sample_titles"] = [j["title"] for j in rescue_jobs[:5]]
    
    # 2. Zlecenia "Startup Founder / Wizjoner bez kasy" (wspólnik, equity, 100 zł)
    equity_keywords = ["wspólnik", "udział", "equity", "procent", "co-founder"]
    equity_jobs = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in equity_keywords)]
    metrics["equity_jobs_count"] = len(equity_jobs)
    metrics["equity_sample"] = [{"client": j["client"], "title": j["title"], "budget": j["budget"]} for j in equity_jobs[:5]]
    
    # 3. Zlecenia "Agencja / Software House" (do zespołu, b2b, podwykonawca, stawka godzinowa)
    agency_keywords = ["do zespołu", "software house", "agencj", "podwykonaw", "b2b", "stawka godzinowa", "senior", "mid"]
    agency_jobs = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in agency_keywords)]
    metrics["agency_jobs_count"] = len(agency_jobs)
    
    # 4. Zlecenia "Oddelegowany pracownik / Księgowa / Asystentka"
    delegated_keywords = ["w imieniu", "dla naszego szefa", "właściciel prosił", "nasza firma szuka", "asystent", "księgow"]
    delegated_jobs = [j for j in jobs if any(k in f"{j['title']} {j['desc']}".lower() for k in delegated_keywords)]
    metrics["delegated_jobs_count"] = len(delegated_jobs)
    
    # 5. Długości wątków na priv w zależności od domeny (dla 56 wygranych)
    wygrane = [j for j in jobs if j["source"] == "wygrana_priv"]
    threads_by_tech = {
        "Scraping & Boty": [w["thread_size"] for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["bot", "scraping", "crawler", "olx"])],
        "E-commerce": [w["thread_size"] for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["shoper", "shopify", "prestashop", "idosell", "sklep"])],
        "ERP & Przemysł": [w["thread_size"] for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["enova", "subiekt", "optima", "topsolid"])],
        "Agencja / Mobile": [w["thread_size"] for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["kotlin", "agencja", "software house"])],
        "Startup / MVP": [w["thread_size"] for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["startup", "mental health", "mvp"])],
    }
    
    threads_stats = {}
    for tech, th_list in threads_by_tech.items():
        if th_list:
            threads_stats[tech] = {
                "count": len(th_list),
                "avg_threads": round(sum(th_list) / len(th_list), 1),
                "max_thread": max(th_list),
                "min_thread": min(th_list)
            }
        else:
            threads_stats[tech] = {"count": 0, "avg_threads": 0, "max_thread": 0, "min_thread": 0}
    metrics["threads_stats"] = threads_stats
    
    # 6. Weryfikacja escrow dla rzekomych "Wysokich Stawek" w Startupach
    high_ticket_startups = [w for w in wygrane if any(k in f"{w['title']} {w['desc']}".lower() for k in ["startup", "mental health", "mvp"])]
    metrics["startup_wygrane_details"] = [{
        "client": w["client"], "title": w["title"], "thread": w["thread_size"], "our_price": w["our_price"]
    } for w in high_ticket_startups]

    return metrics

def main():
    print("[*] Wczytywanie bazy zleceń...")
    jobs = load_data()
    print(f"[+] Załadowano {len(jobs)} zleceń.")
    
    metrics = run_empirical_metrics(jobs)
    print("\n=== TWARDE METRYKI EMPIRYCZNE ===")
    print(f"1. Zlecenia 'Sparzony / Rescue': {metrics['rescue_count']} zleceń")
    print(f"2. Zlecenia 'Wspólnik / Equity za 0 zł': {metrics['equity_jobs_count']} zleceń")
    print(f"3. Zlecenia 'Agencja / Software House': {metrics['agency_jobs_count']} zleceń")
    print(f"4. Zlecenia 'Oddelegowany pracownik / Księgowa': {metrics['delegated_jobs_count']} zleceń")
    print("\n5. Statystyka długości wątków na priv (komunikacja z człowiekiem):")
    for t, s in metrics["threads_stats"].items():
        print(f"   - {t}: n={s['count']}, Śr: {s['avg_threads']} wiadomości, Maks: {s['max_thread']}")

    system_prompt = """Jesteś Bezwzględnym Audytorem Falsyfikacyjnym i Analitykiem Jakości Danych (Red Team Lead).
Twoim jedynym zadaniem jest brutalne, krytyczne zbadanie nowo stworzonej taksonomii zleceniodawców Useme.
Musisz odpowiedzieć na pytanie:
CZY TA TAKSONOMIA TO TWARDA PRAWDA ZGODNA Z DANYMI, CZY ZAWIERA BŁĘDY, MITOMANIĘ LUB NADINTERPRETACJE?

Zasady:
1. Skonfrontuj każdy typ (A do I) z twardymi liczbami z bazy Useme.
2. Zidentyfikuj ewentualne pułapki (np. czy "Klient Sparzony" to osobny gatunek, czy tylko stan emocjonalny przejściowy? Czy "Startup Founder" rzeczywiście płaci cokolwiek na Useme, czy to w 95% szum informacyjny?).
3. Zweryfikuj cross-tech: czy różnice technologiczne rzeczywiście wynikają z technologii, czy z profilu branżowego firmy?
4. Wskaż co jest w 100% twardym faktem, co jest trafną hipotezą roboczą, a co wymaga natychmiastowej korekty lub precyzacji."""

    user_prompt = f"""DANE STATYSTYCZNE Z EMPIRYCZNEJ BAZY 470 ZLECEŃ:
{json.dumps(metrics, indent=2, ensure_ascii=False)}

OPRACOWANA WCZEŚNIEJ TAKSONOMIA DO SPRAWDZENIA:
- Typ A: Tradycyjne MŚP / ERP (A1 Właściciel Senior, A2 Księgowa/Delegowany, A3 Magazynier, A4 Sparzony ERP)
- Typ B: E-commerce (B1 Dojrzały z ERP, B2 Nerwowy dropshipper, B3 Platformowy bez IT)
- Typ C: Startup Founder (C1 Finansowany Seed, C2 Wizjoner za udziały, C3 Non-tech z długiem tech, C4 MVP/Prototyp)
- Typ D: Agencja / Software House (D1 PM pożar, D2 Rekruter, D3 White-label)
- Typ E: Ekspert Dziedzinowy (E1 Komornik, E2 Medycyna/Doktor Monika, E3 Inwestor KW)
- Typ F: Quick IT Fix (F1 Paraliż, F2 Łatka)
- Typ G: Klient Sparzony / Rescue (nowy typ)
- Typ H: Tech-Agnostic Business Owner (33% rynku)
- Typ I: Zlecający Prywatny / Hobbysta (nowy typ)

WYGENERUJ BEZKOMPROMISOWY RAPORT FALSYFIKACYJNY W FORMACIE MARKDOWN:

# AUDYT FALSYFIKACYJNY I WERYFIKACJA PRAWDZIWOŚCI TAKSONOMII KLIENTÓW
## TEST ZGODNOŚCI Z BAZĄ 470 ZLECEŃ, WYKRYCIE BŁĘDÓW I TWARDA KOREKTA

### 1. WERDYKT OGÓLNY: CO JEST TWARDĄ PRAWDĄ, A CO BYŁO NADINTERPRETACJĄ?
- Czy struktura 9 typów i podgrup odzwierciedla realny rynek Useme?
- Które tezy są podparte faktami transakcyjnymi (escrow, wypłaty, wątki priv), a które to tylko deklaracje z ogłoszeń?

### 2. PUNKT PO PUNKCIE: WERYFIKACJA TYPÓW I PODGRUP (CO ZOSTAJE, CO KORYGUJEMY)
- Przejdź przez każdy typ (A - I):
  * Czy podgrupy są realne i rozróżnialne w treściach zleceń?
  * Czy podział na A1 (Senior) vs A2 (Księgowa) vs A3 (Magazynier) trzyma się danych?
  * Zdemaskowanie Startupów (Typ C): Prawda o "Phantom Leads" (ile z 9 'wygranych' founderów naprawdę wpłaciło depozyt?).
  * Klient Sparzony (Typ G): Czy to osobny typ, czy "modifikator psychologiczny" nakładany na MŚP, E-commerce i Agencję?
  * Prywatny/Hobbysta (Typ I): Czy warto w ogóle z nim gadać na Useme?

### 3. WERYFIKACJA ANALIZY CROSS-TECH (CZY RÓŻNICE SĄ PRAWDZIWE?)
- Zbadaj statystyki wątków:
  * Scraping & Boty: Średnio aż 63+ wiadomości (rekord 373)! Dlaczego?
  * E-commerce: Średnio 16.2 wiadomości (rekord 173)! Dlaczego?
  * ERP: 12.8 wiadomości, wysoka transakcyjność.
  * Agencje i Founderzy: zaledwie 1-2 wiadomości! Co to oznacza w praktyce?
- Czy twarda reguła "W ERP zakaz żargonu programistycznego, a w Scrapingu obowiązek żargonu" jest w 100% prawdziwa?

### 4. OSTATECZNY, OCZYSZCZONY Z BŁĘDÓW KODEKS TYPÓW (GOLD STANDARD)
- Zestawienie tabelaryczne ostatecznych, w 100% zweryfikowanych typów i podgrup, ich wskaźnika opłacalności (ROI) i twardych wytycznych dla bota.

Pisz bezpośrednio, bezlitośnie, inżyniersko i z oparciem o liczby.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
        "stream": False
    }

    print(f"[*] Uruchamiam DeepSeek-Reasoner w trybie rygorystycznego audytu falsyfikacyjnego...")
    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=300)
        if r.status_code == 200:
            result = r.json()["choices"][0]["message"]["content"]
            with open(OUT_REPORT, "w", encoding="utf-8") as f:
                f.write(result)
            dt = round(time.time() - t0, 1)
            print(f"[+] SUKCES! Zapisano raport weryfikacji do: {OUT_REPORT} ({len(result)} znaków) w {dt}s.")
        else:
            print(f"[!] Błąd API {r.status_code}: {r.text[:500]}")
    except Exception as e:
        print(f"[!] Błąd połączenia: {e}")

if __name__ == "__main__":
    main()
