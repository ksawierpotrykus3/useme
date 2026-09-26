# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', encoding='utf-8') as f:
    offers = json.load(f)

total = len(offers)
team_phrase = 0
call_15min = 0
call_any = 0
no_signature = 0
signed_ksawier = 0
belfer_phrases = 0
prices = []
budgets_declared = 0
budgets_negotiable = 0
contracts_dist = Counter()
categories_dist = Counter()

# Tech stack keywords
tech_counts = Counter()
tech_keywords = [
    'wordpress', 'woocommerce', 'shopify', 'shoper', 'prestashop', 'magento',
    'react', 'next.js', 'vue', 'angular', 'node', 'python', 'django', 'fastapi',
    'n8n', 'make', 'zapier', 'ai', 'llm', 'chatgpt', 'openai', 'claude',
    'scraping', 'scraper', 'selenium', 'playwright', 'api', 'ksef', 'erp',
    'baselinker', 'allegro', 'otomoto', 'olx', 'three.js', '3d'
]

for o in offers:
    prop = o.get('our_proposal', '')
    prop_lower = prop.lower()
    job_desc = (o.get('job_description', '') or '').lower()
    
    # Analyze proposal patterns
    if any(p in prop_lower for p in ['dwuosobowego zespołu', 'dwuosobowy zespół', 'dwuosobowym zespole', 'piszę w imieniu dwuosobowego']):
        team_phrase += 1
    if any(p in prop_lower for p in ['15 minut', '15 min', 'zdzwońmy się na 15']):
        call_15min += 1
    if any(p in prop_lower for p in ['zdzwońmy się', 'call', 'google meet', 'spotkanie', 'porozmawiajmy']):
        call_any += 1
    if 'ksawier' in prop_lower:
        signed_ksawier += 1
    else:
        no_signature += 1
    if any(p in prop_lower for p in ['mina', 'minę', 'gdzie jest mina', 'gdzie są miny', 'wywali cały', 'błąd']):
        belfer_phrases += 1
        
    p_str = o.get('our_price', '').replace(' ', '').replace('PLN', '').replace(',', '.').replace('zł', '')
    try:
        val = float(re.findall(r'[\d\.]+', p_str)[0])
        prices.append(val)
    except Exception:
        pass
        
    b = o.get('budget', '')
    if 'negocjacji' in b.lower() or not b:
        budgets_negotiable += 1
    else:
        budgets_declared += 1
        
    c = o.get('client_contracts', '0 umów')
    contracts_dist[c] += 1
    categories_dist[o.get('category', 'Inne')] += 1
    
    # Tech in job
    for kw in tech_keywords:
        if kw in job_desc:
            tech_counts[kw] += 1

print("=" * 60)
print(f"ANALIZA STATYSTYCZNA 406 PRZEGRANYCH OFERT (PELNA BAZA)")
print("=" * 60)
print(f"Laczna liczba ofert: {total}")
print(f"Fraza 'dwuosobowy zespol': {team_phrase} ({team_phrase/total*100:.1f}%)")
print(f"Kalka '15 minut': {call_15min} ({call_15min/total*100:.1f}%)")
print(f"Jakikolwiek call / zdzwonmy sie: {call_any} ({call_any/total*100:.1f}%)")
print(f"Calkowity brak podpisu Ksawier: {no_signature} ({no_signature/total*100:.1f}%)")
print(f"Podpis Ksawier: {signed_ksawier} ({signed_ksawier/total*100:.1f}%)")
print(f"Belferski ton (mina / blad / wywali): {belfer_phrases} ({belfer_phrases/total*100:.1f}%)")
print("-" * 60)
print(f"Budzety klientow: Do negocjacji = {budgets_negotiable} ({budgets_negotiable/total*100:.1f}%), Deklarowany budzet = {budgets_declared} ({budgets_declared/total*100:.1f}%)")
if prices:
    print(f"Wyceny: Srednia = {sum(prices)/len(prices):.2f} zl | Mediana = {sorted(prices)[len(prices)//2]:.2f} zl | Min = {min(prices):.2f} zl | Max = {max(prices):.2f} zl")
print("-" * 60)
print("Top doswiadczenie klientow (liczba umow):")
for c, cnt in contracts_dist.most_common(8):
    print(f"  {c}: {cnt} ({cnt/total*100:.1f}%)")
print("-" * 60)
print("Top technologie poszukiwane przez klientow:")
for t, cnt in tech_counts.most_common(12):
    print(f"  {t.upper()}: {cnt} zlecen ({cnt/total*100:.1f}%)")
