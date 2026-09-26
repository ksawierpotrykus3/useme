# -*- coding: utf-8 -*-
"""Analiza trendów rynkowych w czasie na bazie 406 ofert oraz magazynu zleceń."""

import json
import re
from collections import Counter
from pathlib import Path

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', encoding='utf-8') as f:
    offers = json.load(f)

valid_offers = []
for o in offers:
    try:
        oid = int(o.get('offer_id'))
        valid_offers.append((oid, o))
    except Exception:
        pass

valid_offers.sort(key=lambda x: x[0])
total = len(valid_offers)
third = total // 3

epoka1 = [o for oid, o in valid_offers[:third]]
epoka2 = [o for oid, o in valid_offers[third:2*third]]
epoka3 = [o for oid, o in valid_offers[2*third:]]

def analyze_epoch(name, ep):
    prices = []
    ai_count = 0
    api_count = 0
    wp_count = 0
    zero_contracts = 0
    for o in ep:
        jdesc = (o.get('job_description') or '').lower()
        if any(w in jdesc for w in ['ai', 'llm', 'chatgpt', 'openai', 'agent', 'rag']):
            ai_count += 1
        if any(w in jdesc for w in ['api', 'webhook', 'integracj', 'scraping', 'crawler']):
            api_count += 1
        if any(w in jdesc for w in ['wordpress', 'elementor', 'woocommerce']):
            wp_count += 1
        if o.get('client_contracts') == '0 umów':
            zero_contracts += 1
            
        p_str = o.get('our_price', '').replace(' ', '').replace('PLN', '').replace(',', '.').replace('zł', '')
        try:
            val = float(re.findall(r'[\d\.]+', p_str)[0])
            prices.append(val)
        except Exception:
            pass
            
    avg_price = sum(prices)/len(prices) if prices else 0
    med_price = sorted(prices)[len(prices)//2] if prices else 0
    
    first_id = ep[0].get('offer_id')
    last_id = ep[-1].get('offer_id')
    print(f"=== {name} (N={len(ep)}, ID: {first_id} -> {last_id}) ===")
    print(f"  Średnia wycena złożona: {avg_price:.0f} zł | Mediana: {med_price:.0f} zł")
    print(f"  Popyt na AI / LLM / Agentów: {ai_count} zleceń ({ai_count/len(ep)*100:.1f}%)")
    print(f"  Popyt na API / Integracje:   {api_count} zleceń ({api_count/len(ep)*100:.1f}%)")
    print(f"  Popyt na WordPress / Woo:    {wp_count} zleceń ({wp_count/len(ep)*100:.1f}%)")
    print(f"  Udział nowych klientów (0 umów): {zero_contracts} ({zero_contracts/len(ep)*100:.1f}%)\n")

print("=" * 65)
print("DYNAMIKA ZMIAN W CZASIE (OŚ CZASU WG KOLEJNOŚCI OFERT USEME)")
print("=" * 65)
analyze_epoch("EPOKA 1 (Starsza faza bazy - ID 2.51M do 2.58M)", epoka1)
analyze_epoch("EPOKA 2 (Środkowa faza bazy - ID 2.58M do 2.68M)", epoka2)
analyze_epoch("EPOKA 3 (Najnowsza faza bazy - ID 2.68M do 2.87M, wrzesień 2026)", epoka3)

# Analiza tempa dziennego z magazynu
print("=" * 65)
print("TEMPO WPŁYWU ZLECEŃ DZIENNIE (DANE Z MAGAZYNU 08.09 - 22.09.2026)")
print("=" * 65)
daily_counts = Counter()
for f in Path('magazyn').glob('**/*.json'):
    if f.name.startswith('.'): continue
    try:
        d = json.loads(f.read_text(encoding='utf-8'))
        dt = d.get('detected_at') or d.get('data_wyslania') or d.get('updated_at')
        if dt:
            daily_counts[dt[:10]] += 1
    except: pass

sorted_days = sorted(daily_counts.items())
for day, count in sorted_days:
    print(f"  {day}: {count} nowych zleceń IT / Serwisy")

if sorted_days:
    avg_daily = sum(c for _, c in sorted_days) / len(sorted_days)
    print(f"\nŚrednio nowych zleceń IT dziennie: {avg_daily:.1f}")

# Konkurencja z archiwum
print("=" * 65)
print("LICZBA KONKURENTÓW NA ZLECENIE (ARCHIWUM)")
print("=" * 65)
comp_list = []
comp_by_cat = Counter()
cat_counts = Counter()
for f in Path('badania/rynek/archiwum').glob('**/*.json'):
    try:
        d = json.loads(f.read_text(encoding='utf-8'))
        cc = d.get('competitors_count')
        cat = d.get('fields', {}).get('Kategoria', 'Inne')
        if cc is not None:
            comp_list.append(cc)
            comp_by_cat[cat] += cc
            cat_counts[cat] += 1
    except: pass

if comp_list:
    print(f"Średnia liczba konkurentów ogółem: {sum(comp_list)/len(comp_list):.1f} wykonawców na zlecenie")
    print(f"Mediana konkurentów: {sorted(comp_list)[len(comp_list)//2]}")
    print(f"Najmniej konkurentów: {min(comp_list)} (nisze techniczne)")
    print(f"Najwięcej konkurentów: {max(comp_list)} (proste zlecenia WordPress/grafika)")
    print("\nŚrednia konkurencja wg kategorii:")
    for cat, total_c in comp_by_cat.items():
        n = cat_counts[cat]
        print(f"  - {cat}: {total_c/n:.1f} konkurentów / zlecenie (próba N={n})")
