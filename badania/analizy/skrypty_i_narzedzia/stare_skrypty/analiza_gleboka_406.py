# -*- coding: utf-8 -*-
import json
import re
from collections import Counter, defaultdict

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', encoding='utf-8') as f:
    offers = json.load(f)

def clean_price(p_str):
    if not p_str: return None
    s = p_str.replace(' ', '').replace('PLN', '').replace('zł', '').replace(',', '.')
    m = re.findall(r'[\d\.]+', s)
    return float(m[0]) if m else None

def get_folder_cat(raw_cat):
    if 'Strony internetowe' in raw_cat: return '05_strony_internetowe'
    if 'Oprogramowanie' in raw_cat: return '02_oprogramowanie_i_skrypty'
    if 'Aplikacje webowe' in raw_cat: return '01_aplikacje_webowe'
    if 'Projekty IT' in raw_cat: return '03_projekty_it_systemy'
    if 'Sklepy internetowe' in raw_cat and 'Obs' not in raw_cat: return '06_sklepy_ecommerce'
    if 'Obs' in raw_cat and 'sklep' in raw_cat.lower(): return '07_obsluga_ecommerce'
    if 'Aplikacje mobilne' in raw_cat: return '04_aplikacje_mobilne'
    if 'Sprzeda' in raw_cat: return '08_marketing_i_sprzedaz'
    return '99_inne_zlecenia'

total_offers = len(offers)
total_our_value = sum(clean_price(o.get('our_price')) or 0 for o in offers)

cat_stats = defaultdict(lambda: {
    'count': 0, 'our_prices': [], 'client_budgets': [], 
    'negotiable': 0, 'declared': 0, 'zero_contracts': 0,
    'days': [], 'titles': []
})

for o in offers:
    raw_cat = o.get('category', 'Inne')
    folder_cat = get_folder_cat(raw_cat)
    our_p = clean_price(o.get('our_price'))
    b_str = o.get('budget', '')
    is_neg = 'negocjacji' in b_str.lower() or not b_str
    client_p = clean_price(b_str) if not is_neg else None
    contracts = o.get('client_contracts', '0 umów')
    is_zero = '0 um' in contracts
    days_str = o.get('our_days', '')
    m_days = re.findall(r'\d+', days_str)
    days = int(m_days[0]) if m_days else None
    
    st = cat_stats[folder_cat]
    st['count'] += 1
    st['titles'].append(o.get('title', ''))
    if our_p is not None:
        st['our_prices'].append(our_p)
    if days is not None:
        st['days'].append(days)
    if is_neg:
        st['negotiable'] += 1
    else:
        st['declared'] += 1
        if client_p is not None:
            st['client_budgets'].append(client_p)
    if is_zero:
        st['zero_contracts'] += 1

print("=" * 90)
print(f"1. SYNTEZA RYNKOWA 406 ZLECEŃ WG 7 GŁÓWNYCH KATEGORII (ŁĄCZNA PULA: {total_our_value:,.2f} PLN)")
print("=" * 90)

order = [
    '05_strony_internetowe', '02_oprogramowanie_i_skrypty', '01_aplikacje_webowe',
    '03_projekty_it_systemy', '06_sklepy_ecommerce', '07_obsluga_ecommerce',
    '04_aplikacje_mobilne', '99_inne_zlecenia', '08_marketing_i_sprzedaz'
]

cat_summary_table = []
for folder_cat in order:
    st = cat_stats[folder_cat]
    cnt = st['count']
    if cnt == 0: continue
    prs = st['our_prices']
    avg_p = sum(prs) / len(prs) if prs else 0
    med_p = sorted(prs)[len(prs) // 2] if prs else 0
    min_p = min(prs) if prs else 0
    max_p = max(prs) if prs else 0
    tot_p = sum(prs)
    cb = st['client_budgets']
    avg_cb = sum(cb) / len(cb) if cb else 0
    med_cb = sorted(cb)[len(cb) // 2] if cb else 0
    days_avg = sum(st['days']) / len(st['days']) if st['days'] else 0
    neg_pct = st['negotiable'] / cnt * 100
    zero_pct = st['zero_contracts'] / cnt * 100
    
    cat_summary_table.append({
        'kategoria': folder_cat, 'wolumen': cnt, 'udzial_wolumen': cnt/total_offers*100,
        'wartosc': tot_p, 'udzial_wartosc': tot_p/total_our_value*100,
        'srednia': avg_p, 'mediana': med_p, 'min': min_p, 'max': max_p,
        'srednie_dni': days_avg, 'negocjacji_pct': neg_pct, 'zero_umow_pct': zero_pct,
        'deklarowane_cnt': len(cb), 'deklarowane_srednia': avg_cb, 'deklarowane_mediana': med_cb
    })
    
    print(f"KATEGORIA: {folder_cat}")
    print(f"  • Wolumen: {cnt:2d} zleceń ({cnt/total_offers*100:.1f}%) | Wartość portfela: {tot_p:10,.2f} PLN ({tot_p/total_our_value*100:.1f}%)")
    print(f"  • Wycena nasza: Średnia = {avg_p:6,.0f} PLN | Mediana = {med_p:6,.0f} PLN | Zakres = {min_p:,.0f} - {max_p:,.0f} PLN")
    print(f"  • Średni szacowany czas: {days_avg:.1f} dni")
    print(f"  • Budżet klienta: Do negocjacji = {st['negotiable']} ({neg_pct:.1f}%) | Jawny = {st['declared']} ({100-neg_pct:.1f}%)")
    if cb:
        print(f"  • Jawny budżet klienta (N={len(cb)}): Średnia = {avg_cb:6,.0f} PLN | Mediana = {med_cb:6,.0f} PLN | Zakres = {min(cb):,.0f} - {max(cb):,.0f} PLN")
    print(f"  • Współczynnik nowicjuszy (0 umów): {st['zero_contracts']} ({zero_pct:.1f}%)")
    print("-" * 90)

# Deep check of Tech Keywords in Descriptions
print("\n" + "=" * 90)
print("2. GDZIE LEŻĄ NAJWIĘKSZE PIENIĄDZE? ANALIZA NISZ I TECHNOLOGII")
print("=" * 90)

# Exact checks for user prompts:
# AI: 159 (39.2%)
# API / Integracje: 149 (36.7%)
# WordPress: 91 (22.4%)
def matches_pattern(text, pat):
    return bool(re.search(pat, text, re.IGNORECASE))

# Let's inspect which regex exactly produces ~159, ~149, ~91
all_texts = [(o.get('title', '') + ' ' + (o.get('job_description', '') or '')).lower() for o in offers]

ai_kw = r'(ai\b|llm|gpt|openai|claude|sztuczn|inteligencj|machine learning|rag\b|agent|deep learning|neural|chatbot|bot\b|automatyzacj|n8n|make\b)'
api_kw = r'(api\b|integracj|webhook|rest\b|ksef|erp|baselinker|crm|subiekt|enova|comarch|zapier|allegro|otomoto|synchr)'
wp_kw = r'(wordpress|elementor|woocommerce|\bwp\b|divi)'

cnt_ai = sum(1 for t in all_texts if matches_pattern(t, ai_kw))
cnt_api = sum(1 for t in all_texts if matches_pattern(t, api_kw))
cnt_wp = sum(1 for t in all_texts if matches_pattern(t, wp_kw))

print(f"Kluczowe agregaty rynkowe:")
print(f"  • AI / Automatyzacja / Agenci / Boty: {cnt_ai} ({cnt_ai/total_offers*100:.1f}%)")
print(f"  • API / Integracje / Ekosystemy B2B:   {cnt_api} ({cnt_api/total_offers*100:.1f}%)")
print(f"  • Czerwony Ocean WordPress / Web:      {cnt_wp} ({cnt_wp/total_offers*100:.1f}%)")

# Detailed Niche Breakdown
niches = {
    'AI & Agenci LLM (ChatGPT, OpenAI, RAG, Claude)': r'\b(ai|llm|gpt|chatgpt|openai|claude|sztuczn[a-z]+ inteligencj[a-z]+|rag|agenci|agent)\b',
    'n8n / Make / Zapier (Workflow Automation)': r'\b(n8n|make|zapier)\b',
    'API & Integracje B2B (REST, Webhooki, Sync)': r'\b(api|integracj[a-z]+|webhook|rest)\b',
    'KSeF / FinTech / ERP (Comarch, Enova, Subiekt)': r'\b(ksef|erp|comarch|enova|subiekt|symfonia|faktur[a-z]*)\b',
    'Baselinker & E-commerce Hubs (Allegro, OTOMOTO)': r'\b(baselinker|allegro|otomoto|olx|amazon)\b',
    'Scraping & Data Mining (Selenium, Playwright)': r'\b(scraping|scraper|selenium|playwright|puppeteer|crawler)\b',
    'Konfiguratory 3D / WebGL / Three.js': r'\b(konfigurator|three\.?js|webgl|3d|blender)\b',
    'Czerwony Ocean: WordPress & Elementor': r'\b(wordpress|elementor|divi|\bwp\b)\b',
    'Dedykowany E-commerce (Shopify, Presta, Shoper)': r'\b(shopify|prestashop|shoper|magento|idosell)\b',
    'Custom Web & SaaS (React, Vue, Node, Python)': r'\b(react|next\.?js|vue|angular|node|python|fastapi|django)\b',
    'Mobile Development (Flutter, Kotlin, Swift)': r'\b(flutter|react native|ios|android|kotlin|swift|mobiln[a-z]+)\b'
}

print("\nSzczegółowe zestawienie nisz technologicznych:")
print(f"{'Nisza / Segment':48s} | {'N':3s} | {'%':5s} | {'Średnia PLN':12s} | {'Mediana PLN':11s} | {'Pula PLN':14s}")
print("-" * 105)

niche_data = []
for n_name, pat in niches.items():
    matched = [o for o in offers if matches_pattern((o.get('title','')+' '+(o.get('job_description','') or '')).lower(), pat)]
    cnt = len(matched)
    prs = [clean_price(o.get('our_price')) for o in matched if clean_price(o.get('our_price')) is not None]
    avg_p = sum(prs)/len(prs) if prs else 0
    med_p = sorted(prs)[len(prs)//2] if prs else 0
    tot_p = sum(prs)
    niche_data.append((n_name, cnt, cnt/total_offers*100, avg_p, med_p, tot_p))
    print(f"{n_name:48s} | {cnt:3d} | {cnt/total_offers*100:4.1f}% | {avg_p:10,.0f} zł | {med_p:9,.0f} zł | {tot_p:12,.0f} zł")

# 3. Zachowanie klientów przy budżetach (86.2% 'Do negocjacji')
print("\n" + "=" * 90)
print("3. DEKODOWANIE ZACHOWAŃ I PSYCHOLOGII KLIENTÓW (86.2% 'DO NEGOCJACJI')")
print("=" * 90)

neg_offers = [o for o in offers if 'negocjacji' in o.get('budget', '').lower() or not o.get('budget', '')]
dec_offers = [o for o in offers if o not in neg_offers]

print(f"Rozkład budżetów:")
print(f"  • 'Do negocjacji': {len(neg_offers)} ({len(neg_offers)/total_offers*100:.1f}%)")
print(f"  • Deklarowany budżet: {len(dec_offers)} ({len(dec_offers)/total_offers*100:.1f}%)")

# Segmentation of declared budgets
budget_brackets = {
    'Mikro / Placeholdery (< 1 000 zł)': (0, 999),
    'Niski / Budżet studencki (1 000 - 2 500 zł)': (1000, 2500),
    'Średni / Standard MŚP (2 501 - 7 000 zł)': (2501, 7000),
    'Wysoki / Korporacyjny / Enterprise (> 7 000 zł)': (7001, 9999999)
}

print("\nStruktura jawnych budżetów klienta (N=56):")
for b_name, (b_min, b_max) in budget_brackets.items():
    in_b = [clean_price(o.get('budget')) for o in dec_offers if clean_price(o.get('budget')) is not None and b_min <= clean_price(o.get('budget')) <= b_max]
    print(f"  • {b_name:50s}: {len(in_b):2d} ({len(in_b)/len(dec_offers)*100:4.1f}%) | Średnia: {sum(in_b)/len(in_b) if in_b else 0:6,.0f} zł")

# Experience distribution (contracts on Useme)
print("\nDoświadczenie klientów wg liczby zawartych umów Useme (Proxy dojrzałości):")
exp_buckets = defaultdict(list)
for o in offers:
    raw = o.get('client_contracts', '0 umów').strip()
    m = re.search(r'(\d+)', raw)
    num = int(m.group(1)) if m else 0
    our_p = clean_price(o.get('our_price')) or 0
    if num == 0:
        exp_buckets['0 umów (Zleceniodawca jednorazowy / Nowicjusz)'].append(our_p)
    elif num <= 3:
        exp_buckets['1-3 umowy (Wczesny etap zaufania / MŚP)'].append(our_p)
    elif num <= 10:
        exp_buckets['4-10 umów (Regularny nabywca na Useme)'].append(our_p)
    elif num <= 30:
        exp_buckets['11-30 umów (Dojrzały klient / Agencja / Software House)'].append(our_p)
    else:
        exp_buckets['31+ umów (Power Buyer / Korporacja / Ciągły zleceniodawca)'].append(our_p)

for b_name, prs in exp_buckets.items():
    print(f"  • {b_name:65s}: {len(prs):3d} ({len(prs)/total_offers*100:4.1f}%) | Średnia wycena: {sum(prs)/len(prs):6,.0f} zł | Mediana: {sorted(prs)[len(prs)//2]:6,.0f} zł")
