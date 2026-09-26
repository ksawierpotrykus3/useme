# -*- coding: utf-8 -*-
"""Test nowego generatora Human Voice v6 na 4 skrajnie różnych domenach.

Testowane zlecenia:
1. #144092: 3D WebGL Konfigurator mebli (Three.js / parametryczne 3D)
2. #144038: BaseLinker Administrator (E-commerce / marketplace / stany magazynowe)
3. #143981: Integracja CloudTalk -> Notion CRM (No-code / AI notatki / nietechniczny klient)
4. #144165: CNC Punch Software & Postprocessor (Przemysł / G-code / język ANGIELSKI)
"""

import json
import re
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

from chain_executor import call_deepseek

PROMPTS_DIR = KOD_DIR / "prompts"
AGENT_02A_PATH = PROMPTS_DIR / "generatory" / "agent_02a_opis_oferty.md"
PORTFOLIO_PATH = PROMPTS_DIR / "kontekst" / "portfolio_baza.md"
JAK_PISAC_PATH = PROMPTS_DIR / "kontekst" / "jak_pisac_oferty.md"

ZLECENIA_IDS = ["144092", "144038", "143981", "144165"]

def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return " ".join(text.split())

def load_jobs():
    jobs = []
    for jid in ZLECENIA_IDS:
        p = BASE_DIR / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it" / f"{jid}.json"
        d = json.load(open(p, encoding="utf-8"))
        fd = d.get("full_details", {})
        jobs.append({
            "id": jid,
            "title": fd.get("title", ""),
            "description": strip_html(fd.get("full_description", "")),
            "raw": d
        })
    return jobs

def generate_offer(job: dict) -> dict:
    prompt_template = AGENT_02A_PATH.read_text(encoding="utf-8")
    portfolio_text = PORTFOLIO_PATH.read_text(encoding="utf-8")
    jak_pisac_text = JAK_PISAC_PATH.read_text(encoding="utf-8")
    
    system_prompt = f"""{prompt_template}

--- ZASADY JAK PISAĆ OFERTY ---
{jak_pisac_text}

--- BAZA PORTFOLIO I DOWODÓW ---
{portfolio_text}
"""
    user_prompt = f"""--- DANE ZLECENIA ---
ID: {job['id']}
Tytuł: {job['title']}
Treść zlecenia:
{job['description']}

--- DANE WYCENY I DNI (SYNTETYCZNE BAZOWE DO OFERTY) ---
[WYNIK_KONCOWY]
KWOTA: {4500 if job['id'] == '143981' else 8500 if job['id'] == '144038' else 9200 if job['id'] == '144092' else 12000}
DNI: {10 if job['id'] == '143981' else 14 if job['id'] == '144038' else 18 if job['id'] == '144092' else 21}
[/WYNIK_KONCOWY]

Napisz bezpośrednią, partnerską ofertę według struktury Human Voice v6.
Dostosuj język i styl w 100% do klienta:
- Jeśli zlecenie jest po angielsku, napisz 100% po angielsku.
- Jeśli klient jest nietechniczny (jak Notion), zero żargonu, proste korzyści.
- Jeśli zlecenie jest inżynieryjne (Three.js 3D lub CNC), pełny konkret inżynierski.
- Zastosuj: uporządkowanie zakresu, micro-przykłady, twardą zasadę bezpieczeństwa, 2 etapy płatne po odbiorze, darmową próbkę testową (1-3 pliki/przypadki na sucho) oraz jedno pytanie operacyjne na końcu.
"""
    offer_text = call_deepseek(system_prompt, user_prompt, model="deepseek-chat", timeout=120)
    return {
        "job_id": job["id"],
        "title": job["title"],
        "offer_text": offer_text or ""
    }

def evaluate_offer_with_ai(job: dict, offer_text: str) -> str:
    judge_prompt = f"""Jesteś niezależnym, wymagającym klientem biznesowym, który wystawił ogłoszenie na portalu zleceniowym:

OGŁOSZENIE:
Tytuł: {job['title']}
Treść: {job['description']}

DOSTAŁEŚ PONIŻSZĄ OFERTĘ OD WYKONAWCY:
\"\"\"
{offer_text}
\"\"\"

Oceń tę ofertę szczerze i bez owijania w bawełnę pod kątem:
1. Dopasowanie domenowe: Czy wykonawca naprawdę rozumie tę konkretną dziedzinę ({job['title']}), czy pisze ogólnikami albo wkleił szablon z innej branży (np. z faktur/ERP)?
2. Język i styl: Czy ton jest naturalny, partnerski i ludzki? Jeśli zlecenie było po angielsku, czy oferta jest bezbłędna językowo?
3. Bezpieczeństwo i etapy: Jak oceniasz podział na etapy i propozycję darmowej próbki testowej na sucho?
4. Decyzja: Czy jako klient odpisałbyś na tę ofertę na priv? Oceń w skali 1-100 i podaj 1 najważniejszy plus i 1 ewentualny minus.
"""
    verdict = call_deepseek("", judge_prompt, model="deepseek-chat", timeout=120)
    return verdict or ""

def run():
    print("="*70)
    print("TEST GENERATORA HUMAN VOICE V6 NA 4 SKRAJNIE RÓŻNYCH DOMENACH")
    print("="*70)
    
    jobs = load_jobs()
    results = []
    
    for i, job in enumerate(jobs, 1):
        print(f"\n[{i}/4] Generuję ofertę dla zlecenia #{job['id']}: {job['title']}...", flush=True)
        res = generate_offer(job)
        print(f"      Wygenerowano ({len(res['offer_text'])} znaków, {len(res['offer_text'].split())} słów).")
        print(f"      Odpytuję niezależnego sędziego AI...", flush=True)
        eval_text = evaluate_offer_with_ai(job, res["offer_text"])
        res["evaluation"] = eval_text
        results.append(res)
        time.sleep(2)
        
    out_file = BASE_DIR / "badania" / "audyt_100" / "RAPORT_4_ROZNE_DOMENY_V6.md"
    
    md = "# RAPORT: TEST NOWEGO GENERATORA HUMAN VOICE V6 NA 4 SKRAJNIE RÓŻNYCH DOMENACH\n\n"
    md += "**Data testu:** 2026-09-26\n"
    md += "**Cel:** Sprawdzenie, czy bot potrafi pisać w nowym stylu ludzkim (v6) w zupełnie obcych dziedzinach: 3D WebGL, BaseLinker, integracje no-code/Notion oraz przemysłowe CNC po angielsku.\n\n"
    
    for r in results:
        md += f"## Zlecenie #{r['job_id']}: {r['title']}\n\n"
        md += "### Wygenerowana Oferta (Human Voice v6):\n"
        md += "```\n" + r["offer_text"] + "\n```\n\n"
        md += "### Niezależna Ocena Klienta AI:\n"
        md += r["evaluation"] + "\n\n---\n\n"
        
    out_file.write_text(md, encoding="utf-8")
    json_file = BASE_DIR / "badania" / "audyt_100" / "wyniki_4_rozne_domeny_v6.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUKCES] Test zakończony! Pełny raport zapisano w: {out_file}")

if __name__ == "__main__":
    run()
