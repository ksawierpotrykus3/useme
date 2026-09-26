import json
import re
import sys
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
    przegrane = json.load(f)
with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
    wygrane = json.load(f)

print("="*80)
print("1. WERYFIKACJA LICZBY REKORDÓW")
print("="*80)
print(f"Liczba zleceń w 'przegrane_pelne_416.json': {len(przegrane)}")
print(f"Liczba zleceń w 'wygrane_56.json':          {len(wygrane)}")
print(f"SUMA CAŁKOWITA:                             {len(przegrane) + len(wygrane)}")

# Catalog of granular technologies
tech_dict = {
    'WordPress / WooCommerce': [r'\bwordpress\b', r'\bwoocommerce\b', r'\bwoo\b'],
    'Shopify / Liquid': [r'\bshopify\b', r'\bliquid\b'],
    'PrestaShop': [r'\bprestashop\b', r'\bpresta\b'],
    'IdoSell (IAI)': [r'\bidosell\b', r'\biai\b'],
    'Shoper': [r'\bshoper\b'],
    'Framer / Webflow': [r'\bframer\b', r'\bwebflow\b'],
    'Laravel / PHP': [r'\blaravel\b', r'\bphp\b', r'\bsymfony\b', r'\bcodeigniter\b', r'\bzend\b'],
    'Python / Django / FastAPI': [r'\bpython\b', r'\bdjango\b', r'\bfastapi\b', r'\bflask\b'],
    'Node.js / Express / Nest': [r'\bnode(?:\.js)?\b', r'\bexpress(?:\.js)?\b', r'\bnest(?:\.js)?\b'],
    'React / Next.js': [r'\breact(?:\.js)?\b', r'\bnext(?:\.js)?\b'],
    'Vue / Nuxt': [r'\bvue(?:\.js)?\b', r'\bnuxt(?:\.js)?\b'],
    'Flutter / Dart': [r'\bflutter\b', r'\bdart\b'],
    'Kotlin / Android native': [r'\bkotlin\b', r'\bandroid\b'],
    'Swift / iOS native': [r'\bswift\b', r'\bios\b'],
    'React Native': [r'\breact\s+native\b'],
    '.NET / C#': [r'\bc#\b', r'\b\.net\b', r'\basp\.net\b'],
    'Make / n8n / Zapier': [r'\bmake(?:\.com)?\b', r'\bn8n\b', r'\bzapier\b', r'\bintegromat\b'],
    'Scraping (Selenium/Playwright/Bs4)': [r'\bscraping\b', r'\bscraper\b', r'\bplaywright\b', r'\bselenium\b', r'\bpuppeteer\b', r'\bcrawler\b'],
    'Subiekt (GT / nexo / Sfera)': [r'\bsubiekt\b', r'\bsfera\b', r'\bnexo\b', r'\binsert\b'],
    'Comarch (Optima / XL)': [r'\boptima\b', r'\bcomarch\b', r'\berp\s*xl\b'],
    'Enova365': [r'\benova(?:365)?\b'],
    'BaseLinker': [r'\bbaselinker\b', r'\bbase\.com\b'],
    'Computer Vision / OCR / AI': [r'\bopencv\b', r'\bocr\b', r'\btesseract\b', r'\byolo\b', r'\bchatgpt\b', r'\bgpt\b', r'\bopenai\b'],
    'Bazy danych / SQL': [r'\bmysql\b', r'\bpostgresql\b', r'\bpostgres\b', r'\bsql\b', r'\bsupabase\b', r'\bmongodb\b', r'\bmssql\b'],
    'DevOps / Docker / VPS': [r'\bdocker\b', r'\bvps\b', r'\blinux\b', r'\bnginx\b', r'\bhosting\b'],
    'Figma / UI design': [r'\bfigma\b', r'\bmakiety\b'],
    'VoIP / Asterisk / SIP': [r'\bvoip\b', r'\basterisk\b', r'\bsip\b'],
    'TopSolid / CAD / CAM': [r'\btopsolid\b', r'\bcad\b', r'\bcam\b', r'\bcnc\b']
}

all_jobs = [(x, True) for x in wygrane] + [(x, False) for x in przegrane]

tech_stats = defaultdict(lambda: {'total': 0, 'wins': 0})
unmatched_won = []
unmatched_lost = []

for job, won in all_jobs:
    text = ((job.get('title') or '') + ' ' + (job.get('job_description') or '')).lower()
    matched = False
    for tech_name, patterns in tech_dict.items():
        if any(re.search(p, text) for p in patterns):
            tech_stats[tech_name]['total'] += 1
            if won:
                tech_stats[tech_name]['wins'] += 1
            matched = True
    if not matched:
        if won:
            unmatched_won.append(job)
        else:
            unmatched_lost.append(job)

print("\n" + "="*80)
print("2. DOKŁADNE STATYSTYKI ZIDENTYFIKOWANYCH TECHNOLOGII")
print("="*80)
print(f"{'TECHNOLOGIA':<35} | {'TOTAL':<6} | {'WYGRANE':<7} | {'WIN RATE'}")
print("-" * 65)
for t, s in sorted(tech_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    wr = (s['wins'] / s['total'] * 100) if s['total'] > 0 else 0
    print(f"{t:<35} | {s['total']:^6} | {s['wins']:^7} | {wr:6.1f}%")

print("\n" + "="*80)
print(f"3. ANALIZA ZLECEŃ BEZ WYMIENIONEJ TECHNOLOGII (UNMATCHED: {len(unmatched_won) + len(unmatched_lost)})")
print("="*80)
print(f"Liczba zleceń bez podanej technologii: {len(unmatched_won) + len(unmatched_lost)} / {len(all_jobs)} ({len(unmatched_won)+len(unmatched_lost)}/470 = {(len(unmatched_won)+len(unmatched_lost))/470*100:.1f}%)")
print(f"Z tego wygrane: {len(unmatched_won)} ({len(unmatched_won)/(len(unmatched_won)+len(unmatched_lost))*100:.1f}% Win Rate)")
print(f"Z tego przegrane: {len(unmatched_lost)}")

print("\nWYGRANE ZLECENIA BEZ TECHNOLOGII W OPISIE (100% ukierunkowane na rezultat):")
for idx, j in enumerate(unmatched_won):
    title = j.get('title', '')
    price = j.get('our_price', '')
    desc = j.get('job_description', '').replace('\n', ' ')[:100]
    print(f"[{idx+1}] {price:<12} | {title[:60]}")
    print(f"    Opis: {desc}...")

# Check categories of unmatched
unmatched_all = unmatched_won + unmatched_lost
cat_counts = Counter(j.get('category', 'Brak') for j in unmatched_all)
print("\nKategorie zleceń bez podanej technologii:")
for cat, count in cat_counts.most_common(8):
    print(f"  - {cat}: {count}")

