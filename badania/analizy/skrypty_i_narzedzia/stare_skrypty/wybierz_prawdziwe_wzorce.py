# -*- coding: utf-8 -*-
import json

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8') as f:
    przegrane = json.load(f)

with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8') as f:
    wygrane = json.load(f)

all_jobs = []
for p in przegrane:
    all_jobs.append({
        'source': 'przegrane',
        'id': p.get('offer_id'),
        'title': p.get('title', ''),
        'desc': p.get('job_description', ''),
        'cat': p.get('category', ''),
        'budget': p.get('budget', ''),
        'client': p.get('client', '')
    })

for w in wygrane:
    all_jobs.append({
        'source': 'wygrane',
        'id': w.get('job_id') or w.get('offer_id'),
        'title': w.get('title', ''),
        'desc': w.get('job_description', ''),
        'cat': w.get('category', ''),
        'budget': w.get('budget', ''),
        'client': w.get('client', '')
    })

tematy = {
    '1. AI / OCR / Obieg dokumentow': ['ocr', 'dokument', 'n8n', 'faktur', 'automatyzacj'],
    '2. BaseLinker / ERP / Subiekt / Sklepy': ['baselinker', 'subiekt', 'magazyn', 'stanow', 'cen'],
    '3. 3D / Konfiguratory produktow': ['3d', 'konfigurator', 'mebli', 'three.js', 'wymiar'],
    '4. Scraping / Boty danych': ['scrap', 'bot', 'pobierani', 'danych z'],
    '5. B2B / Panele / CRM / Rezerwacje': ['panel', 'b2b', 'crm', 'hurtown', 'zamowien']
}

for nazwa, words in tematy.items():
    print(f"\n=================== {nazwa} ===================")
    matched = [j for j in all_jobs if any(w in (j['title'] + ' ' + j['desc']).lower() for w in words) and len(j['desc']) > 250]
    matched.sort(key=lambda x: len(x['desc']), reverse=True)
    for i, m in enumerate(matched[:3]):
        print(f"\n[{i+1}] TYTUL: {m['title']}")
        print(f"    KATEGORIA: {m['cat']} | BUDZET: {m['budget']} | KLIENT: {m['client']}")
        print(f"    DLUGOSC OPISU: {len(m['desc'])} znakow")
        lines = [line.strip() for line in m['desc'].split('\n') if line.strip()]
        sample = "\n    ".join(lines[:6])
        print(f"    POCZATEK OPISU:\n    {sample}\n")
