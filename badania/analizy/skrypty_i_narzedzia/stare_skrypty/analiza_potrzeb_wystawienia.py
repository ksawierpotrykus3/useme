# -*- coding: utf-8 -*-
import json
import re

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8') as f:
    przegrane = json.load(f)

with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8') as f:
    wygrane = json.load(f)

wszystkie = []
for p in przegrane:
    wszystkie.append({'zrodlo': 'przegrane', 'id': p.get('offer_id'), 'title': p.get('title', ''), 'desc': p.get('job_description', ''), 'cat': p.get('category', ''), 'budget': p.get('budget', ''), 'price': p.get('our_price', '')})

for w in wygrane:
    wszystkie.append({'zrodlo': 'wygrane', 'id': w.get('offer_id'), 'title': w.get('title', ''), 'desc': w.get('job_description', ''), 'cat': w.get('category', ''), 'budget': w.get('budget', ''), 'price': w.get('our_price', '')})

klastry = {
    'AI / LLM / OCR / RAG / Agenci': ['ai', 'llm', 'chatgpt', 'openai', 'claude', 'rag', 'ocr', 'agent', 'langchain'],
    'Integracje ERP / BaseLinker / API': ['baselinker', 'erp', 'subiekt', 'enova', 'comarch', 'wf-mag', 'optima', 'api', 'webhook'],
    'Scraping / Crawling / Boty': ['scrap', 'crawl', 'bot', 'selenium', 'playwright', 'pars', 'dane z portalu'],
    'Konfiguratory 3D / WebGL / Three.js / CAD': ['3d', 'three.js', 'webgl', 'konfigurator', 'cad', 'cam', 'cnc', 'topsolid', 'blender'],
    'Dedykowane SaaS / CRM / Portale B2B': ['saas', 'crm', 'portal', 'panel klienta', 'system b2b', 'rezerwacj', 'platforma'],
    'Sklepy E-commerce zaawansowane': ['shopify', 'prestashop', 'woocommerce', 'magento', 'idosell', 'hurtownia'],
    'Mobile (React Native / Flutter / iOS / Android)': ['flutter', 'react native', 'ios', 'android', 'mobilna', 'kotlin', 'swift']
}

wyniki = {k: {'total': 0, 'wygrane': 0, 'przegrane': 0, 'przykłady': []} for k in klastry}

for z in wszystkie:
    text = (z['title'] + " " + z['desc']).lower()
    for nazwa_klastra, slowa in klastry.items():
        if any(s in text for s in slowa):
            wyniki[nazwa_klastra]['total'] += 1
            if z['zrodlo'] == 'wygrane':
                wyniki[nazwa_klastra]['wygrane'] += 1
            else:
                wyniki[nazwa_klastra]['przegrane'] += 1
            if len(wyniki[nazwa_klastra]['przykłady']) < 4:
                wyniki[nazwa_klastra]['przykłady'].append((z['title'], z['price'], z['zrodlo']))

print('=== PODSUMOWANIE KLASTRÓW W CAŁEJ BAZIE (462 ZLECENIA) ===')
for k, v in sorted(wyniki.items(), key=lambda x: x[1]['total'], reverse=True):
    wr = (v['wygrane'] / v['total'] * 100) if v['total'] > 0 else 0
    print(f"\n[{k}] - Total: {v['total']} | Wygrane: {v['wygrane']} | Przegrane: {v['przegrane']} | Win Rate: {wr:.1f}%")
    for ex in v['przykłady']:
        print(f"   * [{ex[2]}] {ex[0][:75]} | Cena: {ex[1]}")
