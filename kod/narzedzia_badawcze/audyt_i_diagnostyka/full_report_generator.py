# -*- coding: utf-8 -*-
"""
Generator twardych danych statystycznych dla raportu Useme.
"""
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
import re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from cluster_369 import results_369, orders
from audit_strict_red import red_strict, parse_budget

# Zliczanie budżetów
def get_budget_stats(order_list):
    vals = []
    for x in order_list:
        o = x['order'] if isinstance(x, dict) and 'order' in x else (x[0] if isinstance(x, tuple) else x)
        v = parse_budget(o['budget'])
        if v is not None and v > 0:
            vals.append(v)
    return {
        'count_with_budget': len(vals),
        'total_declared': sum(vals),
        'mean_declared': (sum(vals) / len(vals)) if vals else 0,
        'median_declared': sorted(vals)[len(vals)//2] if vals else 0,
        'min_val': min(vals) if vals else 0,
        'max_val': max(vals) if vals else 0
    }

print("="*80)
print("SZCZEGÓŁOWE STATYSTYKI KLASTRÓW ZAAKCEPTOWANYCH (N = 369):")
print("="*80)

cluster_groups = defaultdict(list)
for item in results_369:
    cluster_groups[item['label']].append(item['order'])

# Sortowanie wg wielkości
sorted_clusters = sorted(cluster_groups.items(), key=lambda x: len(x[1]), reverse=True)

for name, o_list in sorted_clusters:
    stats = get_budget_stats(o_list)
    ids = [o['id'] for o in o_list]
    print(f"\n### {name}")
    print(f"- Liczba zleceń: {len(o_list)} ({len(o_list)/369*100:.2f}% zaakceptowanych, {len(o_list)/551*100:.2f}% całej bazy 551)")
    print(f"- Zlecenia z jawnym budżetem: {stats['count_with_budget']} / {len(o_list)} ({stats['count_with_budget']/len(o_list)*100:.1f}%)")
    if stats['count_with_budget'] > 0:
        print(f"- Suma jawnych budżetów: {stats['total_declared']:,.2f} PLN | Średnia: {stats['mean_declared']:,.2f} PLN | Max: {stats['max_val']:,.2f} PLN")
    print(f"- Przykładowe ID ({min(6, len(ids))} szt.): {', '.join(ids[:6])}")
    for o in o_list[:3]:
        print(f"    * #{o['id']} [{o['budget']}]: {o['title']}")

print("\n" + "="*80)
print("PODZIAŁ NA 6 PROJEKTÓW VS 5 KLASTRÓW W PRÓŻNI:")
print("="*80)

p_map = {
    "P1: Enterprise AI Document & OCR Engine": "AI, Agenci LLM, OCR Dokumentów & RAG",
    "P2: 3D WebGL Configurator + CAD/CNC": "Konfiguratory 3D, WebGL & CAD/CAM/CNC",
    "P3: Scraping Engine & WAF Bypass": "Scraping, Web Crawling & WAF Bypass (Boty Danych)",
    "P4: BaseLinker & ERP Marketplace Sync": "Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova)",
    "P5: B2B Wholesale Portal & Dynamic Pricing": "E-commerce Zaawansowany, B2B & Dedykowane Sklepy (IdoSell/Shopify/Presta)",
    "P6: Reservation & Concurrency System": "Systemy Rezerwacji, Booking & Concurrency"
}

total_covered = 0
for p_code, c_label in p_map.items():
    o_list = cluster_groups[c_label]
    total_covered += len(o_list)
    print(f"- {p_code:45} : {len(o_list):3d} zleceń ({len(o_list)/369*100:5.2f}% akceptowanych | {len(o_list)/551*100:4.2f}% całej bazy)")

print(f"\n=> ŁĄCZNIE POKRYTE PRZEZ 6 PROJEKTÓW: {total_covered} / 369 ({total_covered/369*100:.2f}% akceptowanych | {total_covered/551*100:.2f}% bazy 551)")

gap_map = [
    "Enterprise CRM, SaaS & Dedykowane Web Apps (React/Next/Node/Laravel)",
    "Aplikacje Mobilne (React Native / Flutter / iOS / Android)",
    "Cloud, DevOps & Administracja Serwerami (Linux / Docker / VPS)",
    "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)",
    "Bazy Danych, SQL, BigQuery & Data Engineering"
]

total_gaps = 0
print("\nKLASTRY WISZĄCE W PRÓŻNI (LUKI BEZ IDEALNEGO DEMO):")
for g_label in gap_map:
    o_list = cluster_groups[g_label]
    total_gaps += len(o_list)
    print(f"- {g_label:65} : {len(o_list):3d} zleceń ({len(o_list)/369*100:5.2f}% akceptowanych | {len(o_list)/551*100:4.2f}% całej bazy)")

print(f"\n=> ŁĄCZNIE W PRÓŻNI (BEZ IDEALNEGO DEMO): {total_gaps} / 369 ({total_gaps/369*100:.2f}% akceptowanych | {total_gaps/551*100:.2f}% bazy 551)")
