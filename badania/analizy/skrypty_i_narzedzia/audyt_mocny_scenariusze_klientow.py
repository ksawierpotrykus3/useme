# -*- coding: utf-8 -*-
"""
Skrypt: audyt_mocny_scenariusze_klientow.py
Cel: Uruchomienie mocnego łańcucha rozumowania (deepseek-reasoner) do przeprowadzenia
bezwzględnego audytu jakościowego, psychologicznego i operacyjnego wszystkich 9 nowo powstałych
scenariuszy klientów w kontekście bota Useme, danych empirycznych 470 zleceń i bazy technologicznej.
"""

import json
import os
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"
SCENARIUSZE_DIR = "Projekty_autorskie/useme_core/badania/analizy/typy_klientow/scenariusze"
OUT_AUDIT = "Projekty_autorskie/useme_core/badania/analizy/typy_klientow/audyt_mocny_scenariusze_klientow.md"

def load_scenarios():
    scenarios = {}
    for fname in sorted(os.listdir(SCENARIUSZE_DIR)):
        if fname.endswith(".md") and fname != "README.md":
            path = os.path.join(SCENARIUSZE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # Ekstrakcja kluczowych fragmentów i nagłówków
                scenarios[fname] = {
                    "size": len(content),
                    "summary_snippet": content[:1200] + "\n...\n" + content[-800:]
                }
    return scenarios

def main():
    print("[*] Wczytywanie scenariuszy do audytu...")
    scenarios = load_scenarios()
    print(f"[+] Załadowano {len(scenarios)} plików scenariuszy.")

    system_prompt = """Jesteś Głównym Arbitrem Strategicznym B2B, Psychologiem Biznesu i Szefem Zespołu Red Team dla autonomicznego bota Useme.
Twoim celem jest przeprowadzenie bezkompromisowego, głębokiego audytu jakościowego 9 scenariuszy psychologiczno-operacyjnych klientów.
Audytujesz w rygorze twardej prawdy rynkowej, psychologii asynchronicznej i mechaniki Useme."""

    user_prompt = f"""ZADANIE DLA MOCNEGO ŁAŃCUCHA AUDYTOWEGO (DEEP REASONING):

Oto 9 nowo wygenerowanych scenariuszy zrozumienia człowieka (łączna objętość ponad 160 tys. znaków), stworzonych w oparciu o zasadę:
"ZERO sztywnych formułek 'jeśli X to rób Y'. Zamiast tego głębokie opisy tłumaczące rzeczywistość klienta, jego ukryty ból, presję otoczenia i mechanikę zaufania, tak aby AI elastycznie ważyło podobieństwo".

PRZEGLĄD PLIKÓW I PROFILI W BAZIE:
{json.dumps(scenarios, indent=2, ensure_ascii=False)}

TWARDE REGUŁY SYSTEMOWE, Z KTÓRYMI MUSISZ ZDERZYĆ TE MATERIAŁY:
1. Dane empiryczne: 470 zleceń z Useme (56 wygranych z historią priv, 414 zamkniętych). Jedyny potwierdzony duży kontrakt gotówkowy to Doktor Monika (12 100 zł netto). Founderzy startupów z budżetami 10k-35k to w 90% Phantom Leads (brak wpłaty escrow).
2. Odrzucenie overengineeringu: 30 dni gwarancji na własny kod (zero darmowych gwarancji 12-miesięcznych na API/antyboty), zakaz darmowych audytów przed umową, zakaz propozycji calli/spotkań (100% asynchronicznie), zakaz natarczywych "podkładek pod szefa".
3. Skalowanie długości oferty: 300–450 znaków dla mikro-zleceń (<3000 zł), 600–900 znaków dla średnich/dużych zleceń (>5000 zł).
4. Pełne wsparcie dla priv jako czystego kanału z małą konkurencją i eksponowanym oknem wiadomości.

ZAKRES AUDYTU KRYTYCZNEGO:
1. CZY WSZYSTKO SIĘ ZGADZA Z RZECZYWISTOŚCIĄ RYNKOWĄ I DANYMI?
   - Czy portrety ludzi (właściciel fabryki, merchant e-commerce, PM agencji, lekarz/komornik, klient tech-agnostic) są autentyczne, czy uciekają w fikcję literacką?
   - Czy zdemaskowanie modyfikatorów (Rescue, Delegowany, Phantom Startup) jest bezbłędne operacyjnie?

2. CZY NAPRAWDĘ ZLIKWIDOWANO NAIWNY MECHANIZM "IF-THEN"?
   - Czy scenariusze rzeczywiście dają modelowi AI soczewkę i aparat pojęciowy, zamiast ukrytych instrukcji warunkowych?
   - Jak oceniasz wskazówki elastycznej adaptacji w sekcji 6 (waga podobieństwa, hybrydy, kiedy zignorować)?

3. SPÓJNOŚĆ Z BAZĄ INŻYNIERYJNĄ (16 KART TECH_01 - TECH_16):
   - Czy język przypisany klientom współgra z architekturą inżynierską (np. Optima/Subiekt/Enova a myślenie o magazynie i WZ-kach; Scraping a lęki przed Cloudflare; Tech-Agnostic a unikanie żargonu IT)?

4. ANALIZA POTENCJALNYCH LUK I RYZYK (BLINDSPOTS):
   - Co może pójść nie tak, gdy bot podłączy te scenariusze pod prompt generatora?
   - Gdzie jest ryzyko, że model AI "przegada" ofertę lub wpadnie w zbytnią psychologizację kosztem inżynierskiego konkretu?

5. OSTATECZNY WERDYKT I REKOMENDACJE WDROŻENIOWE:
   - Czy zestaw scenariuszy otrzymuje zielone światło do wpięcia pod produkcyjnego bota w `kod/`?
   - Jakie 3-4 żelazne bezpieczniki należy założyć w walidatorach (`agent_03` - `agent_08`), aby bot idealnie balansował między empatią biznesową a twardym inżynierskim limitem znaków?

Wygeneruj kompletny, analityczny, bezkompromisowy raport w formacie Markdown.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.15,
        "stream": False
    }

    print(f"[*] Uruchamiam mocny łańcuch audytowy {MODEL} (timeout=300s)...")
    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=300)
        if r.status_code == 200:
            result = r.json()["choices"][0]["message"]["content"]
            with open(OUT_AUDIT, "w", encoding="utf-8") as f:
                f.write(result)
            dt = round(time.time() - t0, 1)
            print(f"[+] SUKCES! Zapisano raport audytu do: {OUT_AUDIT} ({len(result)} znaków) w {dt}s.")
        else:
            print(f"[!] Błąd API {r.status_code}: {r.text[:500]}")
    except Exception as e:
        print(f"[!] Błąd połączenia: {e}")

if __name__ == "__main__":
    main()
