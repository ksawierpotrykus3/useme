# -*- coding: utf-8 -*-
"""
Moduł analizujący i klasyfikujący każde z 551 zleceń Useme.
"""
import json
import glob
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

f406_path = r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json'
with open(f406_path, 'r', encoding='utf-8') as f:
    d406 = json.load(f)

dir_it = r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/magazyn/programowanie-i-it'
d61 = [json.load(open(p, 'r', encoding='utf-8')) for p in sorted(glob.glob(os.path.join(dir_it, '*.json')))]

dir_serw = r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/magazyn/serwisy-internetowe'
d84 = [json.load(open(p, 'r', encoding='utf-8')) for p in sorted(glob.glob(os.path.join(dir_serw, '*.json')))]

def extract_desc(d):
    desc = d.get('job_description') or d.get('full_description') or ''
    if not desc and isinstance(d.get('full_details'), dict):
        desc = d['full_details'].get('full_description') or ''
    if not desc and isinstance(d.get('list_details'), dict):
        desc = d['list_details'].get('short_desc') or ''
    return desc or ''

orders = []
for x in d406:
    orders.append({
        'src': '406_closed',
        'id': str(x.get('offer_id')),
        'title': (x.get('title') or '').strip(),
        'cat': (x.get('category') or '').strip(),
        'budget': str(x.get('budget') or '').strip(),
        'our_price': x.get('our_price') or 0,
        'desc': extract_desc(x)
    })

for x in d61:
    our_price = 0
    if isinstance(x.get('ai_proposal'), dict):
        our_price = x['ai_proposal'].get('wycena') or 0
    orders.append({
        'src': '61_it_active',
        'id': str(x.get('id')),
        'title': (x.get('title') or '').strip(),
        'cat': (x.get('category') or '').strip(),
        'budget': str(x.get('budget') or '').strip(),
        'our_price': our_price,
        'desc': extract_desc(x)
    })

for x in d84:
    our_price = 0
    if isinstance(x.get('ai_proposal'), dict):
        our_price = x['ai_proposal'].get('wycena') or 0
    orders.append({
        'src': '84_serw_active',
        'id': str(x.get('id')),
        'title': (x.get('title') or '').strip(),
        'cat': (x.get('category') or '').strip(),
        'budget': str(x.get('budget') or '').strip(),
        'our_price': our_price,
        'desc': extract_desc(x)
    })

# Zapiszmy pomocniczy plik ze wszystkimi zleceniami w formacie ujednoliconym
print(f"Liczba zleceń: {len(orders)}")
