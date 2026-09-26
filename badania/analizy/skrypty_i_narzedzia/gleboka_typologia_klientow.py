import json
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
    przegrane = json.load(f)
with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
    wygrane = json.load(f)

all_jobs = [(x, True) for x in wygrane] + [(x, False) for x in przegrane]

def classify_refined_persona(title, desc, client, budget):
    text = (title + " " + desc).lower()
    
    # 1. HOBBY / GAMING / PRIVATE PERSONAL
    # Explicit gaming bots or private personal micro-tasks
    if any(re.search(p, text) for p in [r'\bgangsters\.pl\b', r'\bpokewars\b', r'\bgrze\b', r'\bbot do gry\b', r'\bskrypt do gry\b', r'\bprywatn(?:ie|e)\b']):
        return "1_HOBBY_GAMER_PRIVATE"
        
    # 2. AGENCJA / SOFTWARE HOUSE / PODWYKONAWCY (Subcontractor / Outsourcing)
    # They mention "nasz klient", "do zespołu", "software house", "agencja", "stała współpraca B2B", "stawka godzinowa"
    if any(re.search(p, text) for p in [
        r'\bdla naszego klienta\b', r'\bdla klienta\b', r'\bnaszego klienta\b', r'\bsoftware house\b',
        r'\bagencj[aię]\b', r'\bpodwykonawc', r'\bdołączenie do zespołu\b', r'\bdla zespołu\b',
        r'\bwsparcie zespołu\b', r'\bstała współpraca b2b\b', r'\brozliczenie godzinowe\b', r'\bstawka godzinowa\b'
    ]):
        return "2_AGENCJA_SOFTWARE_HOUSE"
        
    # 3. E-COMMERCE BRAND / SKLEP INTERNETOWY
    if any(re.search(p, text) for p in [
        r'\bsklep(?:ie|u|y)?\b', r'\bshopify\b', r'\bprestashop\b', r'\bwoocommerce\b', r'\bshoper\b',
        r'\bidosell\b', r'\bmage?nto\b', r'\bbaselinker\b', r'\bkoszyk\b', r'\bhurtowni[aę]\b', r'\bfeed\b'
    ]):
        return "3_ECOMMERCE_MERCHANT"
        
    # 4. STARTUP / FOUNDER NOWEGO PRODUKTU / MVP
    if any(re.search(p, text) for p in [
        r'\bmvp\b', r'\bstartup\b', r'\bnowy portal\b', r'\bnowa aplikacja\b', r'\bplatforma\b',
        r'\baplikacj[aię] mobiln', r'\bflutter\b', r'\bkotli?n\b', r'\bswift\b', r'\bsaas\b', r'\binnowacyjn'
    ]):
        return "4_STARTUP_FOUNDER_MVP"
        
    # 5. EKSPERT DZIEDZINOWY / USŁUGODAWCA / EDUKACJA (Domain Specialist)
    # E.g. psychologists, teachers, real estate, construction estimators, coaches
    if any(re.search(p, text) for p in [
        r'\bpsycholog\b', r'\bterapi\b', r'\bedukacyjn', r'\bkurs(?:u|y)?\b', r'\bszkolen', r'\bquiz\b',
        r'\bkosztorys', r'\bbudow[ay]\b', r'\bnajm\b', r'\bnieruchomośc', r'\blead[yów]*\b', r'\bpartnerów\b'
    ]):
        return "5_EKSPERT_DZIEDZINOWY_USLUGI"
        
    # 6. TRADYCYJNY BIZNES / PRODUKCJA / ERP / HURT (Traditional SME / Operations)
    if any(re.search(p, text) for p in [
        r'\bmagazyn', r'\bfaktur', r'\berp\b', r'\boptima\b', r'\bsubiekt\b', r'\benova\b', r'\bsfera\b',
        r'\bcomarch\b', r'\bprodukcyjn', r'\bcnc\b', r'\btopsolid\b', r'\bksięgow', r'\bzamówień\b'
    ]):
        return "6_TRADYCYJNE_MSP_OPERACJE"
        
    # 7. SZYBKA NAPRAWA / ZADANIOWE IT (Quick IT Fix)
    words = len(text.split())
    if words < 50 or any(re.search(p, text) for p in [r'\bbłąd\b', r'\bnapraw', r'\bpoprawk', r'\bpiln', r'\bna wczoraj\b']):
        return "7_QUICK_FIX_MAŁE_ZLECENIE"
        
    # Default fallback
    return "8_INNE_OGOLNE_PROJEKTY"

persona_stats = defaultdict(lambda: {'total': 0, 'wins': 0, 'prices_won': [], 'threads_won': []})

classified_all = []
for job, won in all_jobs:
    t = job.get('title') or ''
    d = job.get('job_description') or ''
    c = job.get('client') or ''
    b = job.get('budget') or ''
    p = job.get('our_price') or ''
    th = job.get('thread_size') or 0
    
    persona = classify_refined_persona(t, d, c, b)
    persona_stats[persona]['total'] += 1
    if won:
        persona_stats[persona]['wins'] += 1
        persona_stats[persona]['prices_won'].append(p)
        persona_stats[persona]['threads_won'].append(th)
    classified_all.append((persona, job, won))

print("="*85)
print(f"{'NOWA, POGŁĘBIONA TYPOLOGIA ZLECENIODAWCÓW (470 ZLECEŃ)':<45} | TOTAL | WINS | WIN RATE")
print("="*85)
for p, s in sorted(persona_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    wr = (s['wins'] / s['total'] * 100) if s['total'] > 0 else 0
    print(f"{p:<45} | {s['total']:^5} | {s['wins']:^4} | {wr:6.1f}%")

print("\n" + "="*85)
print("SZCZEGÓŁOWY PROFIL KAŻDEGO TYPU KLIENTA (CENY, WĄTKI I PRZYKŁADY WYGRANYCH):")
print("="*85)

for p, s in sorted(persona_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    wr = (s['wins'] / s['total'] * 100) if s['total'] > 0 else 0
    print(f"\n>>> [{p}] (Razem: {s['total']}, Wygrane: {s['wins']}, Win Rate: {wr:.1f}%)")
    if s['threads_won']:
        print(f"    Średnia/Maks liczba wiadomości priv: {sum(s['threads_won'])/len(s['threads_won']):.1f} (Maks: {max(s['threads_won'])})")
        print(f"    Wygrane kwoty w tym segmencie: {s['prices_won'][:6]}")
    # Sample jobs
    sample_won = [j for per, j, won in classified_all if per == p and won][:2]
    for sj in sample_won:
        print(f"    * WYGRANA: [{sj.get('our_price')}] {sj.get('title')[:65]}")
