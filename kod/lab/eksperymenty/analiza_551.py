# -*- coding: utf-8 -*-
"""
Eksploracja i analiza 551 zleceń Useme pod kątem Czerwonego Oceanu, Tierów i Klastrów.
"""
import json
import glob
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# 1. Wczytanie danych
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

print(f"Załadowano {len(orders)} zleceń.")

# Sprawdźmy występowanie słów kluczowych Czerwonego Oceanu
# Kryteria z promptu:
# 1. Odsiej bezwzględnie zlecenia Czerwonego Oceanu, które ZAWSZE odrzucamy:
# (WordPress, Elementor, tanie wizytówki, logo, pisanie tekstów, proste poprawki CSS/HTML za 200-500 zł, copywriting, grafika).

red_ocean_keywords = [
    'elementor', 'divi', 'wizytówk', 'wizytowk', 'logo', 'logotyp', 
    'pisanie tekst', 'copywriting', 'artykuł', 'artykul', 'tekstów seo', 
    'tekstow seo', 'grafik', 'baner', 'banner', 'ulotk', 'plakat',
    'poprawka css', 'poprawki css', 'poprawka html', 'poprawki html',
    'proste poprawki', 'drobne poprawki', 'wklejanie produkt', 'dodanie produkt',
    'wprowadzanie produkt', 'wprowadzanie danych', 'przepisywanie',
    'wix', 'webflow'
]

# Przeanalizujmy także wordpress i woocommerce
# Ile zleceń to czysty WordPress/Elementor?
# Zobaczmy treść zleceń zawierających "wordpress"
print("\n--- ANALIZA ZLECEŃ ZE SŁOWEM WORDPRESS ---")
wp_count = 0
woo_count = 0
for o in orders:
    t = (o['title'] + " " + o['desc']).lower()
    if 'wordpress' in t:
        wp_count += 1
    if 'woocommerce' in t:
        woo_count += 1
print(f"Zlecenia z 'wordpress': {wp_count}")
print(f"Zlecenia z 'woocommerce': {woo_count}")
