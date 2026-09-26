# -*- coding: utf-8 -*-
import json

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8') as f:
    przegrane = json.load(f)

with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8') as f:
    wygrane = json.load(f)

wszystkie = przegrane + wygrane

szukane_slowa = [
    ('OCR_AI', 'obiegu dokument'),
    ('KONFIG_3D', 'konfigurator'),
    ('SAAS_B2B', 'paletsystem'),
    ('ERP_SUBIEKT', 'subiekt'),
    ('SCRAPING', 'scrap')
]

for label, keyword in szukane_slowa:
    print(f"\n{'='*70}\nKLUCZ: {label} (szukano: '{keyword}')\n{'='*70}")
    znalezione = [j for j in wszystkie if keyword in (j.get('title', '') + ' ' + j.get('job_description', '')).lower()]
    znalezione.sort(key=lambda x: len(x.get('job_description', '')), reverse=True)
    if znalezione:
        top = znalezione[0]
        print(f"TYTUŁ: {top.get('title')}")
        print(f"KATEGORIA: {top.get('category')} | BUDŻET: {top.get('budget')} | KLIENT: {top.get('client')}")
        print(f"TREŚĆ ORYGINALNA (fragment 1000 znaków):\n{top.get('job_description')[:1200]}")
