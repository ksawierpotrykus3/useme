# -*- coding: utf-8 -*-
"""
Weryfikacja pokrycia 6 projektów vs luki w próżni.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from engine_audit import classified_data, accepted_orders, red_orders

p1_ai = [x for x in accepted_orders if x['label'] == "AI, Agenci LLM, OCR Dokumentów & RAG"]
p2_3d = [x for x in accepted_orders if x['label'] == "Konfiguratory 3D, WebGL & CAD/CAM/CNC"]
p3_scraping = [x for x in accepted_orders if x['label'] == "Scraping, Web Crawling & WAF Bypass (Boty Danych)"]
p4_api_sync = [x for x in accepted_orders if x['label'] == "Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova)"]
p5_ecom_b2b = [x for x in accepted_orders if x['label'] == "E-commerce Zaawansowany, B2B & Dedykowane Sklepy (IdoSell/Shopify/Presta)"]
p6_reservation = [x for x in accepted_orders if x['label'] == "Systemy Rezerwacji, Booking & Concurrency"]

covered_orders = p1_ai + p2_3d + p3_scraping + p4_api_sync + p5_ecom_b2b + p6_reservation
covered_count = len(covered_orders)
acc_count = len(accepted_orders)

print("="*70)
print("POKRYCIE PRZEZ 6 PROJEKTÓW DEMO:")
print("="*70)
print(f"Projekt 1 (AI Document & OCR Engine)       : {len(p1_ai):3d} zleceń ({len(p1_ai)/acc_count*100:5.1f}%)")
print(f"Projekt 2 (3D WebGL Configurator + CAD/CNC): {len(p2_3d):3d} zleceń ({len(p2_3d)/acc_count*100:5.1f}%)")
print(f"Projekt 3 (Scraping & WAF Bypass)          : {len(p3_scraping):3d} zleceń ({len(p3_scraping)/acc_count*100:5.1f}%)")
print(f"Projekt 4 (BaseLinker / ERP API Sync)      : {len(p4_api_sync):3d} zleceń ({len(p4_api_sync)/acc_count*100:5.1f}%)")
print(f"Projekt 5 (B2B Wholesale & Pricing Engine) : {len(p5_ecom_b2b):3d} zleceń ({len(p5_ecom_b2b)/acc_count*100:5.1f}%)")
print(f"Projekt 6 (Reservation & Concurrency Lock) : {len(p6_reservation):3d} zleceń ({len(p6_reservation)/acc_count*100:5.1f}%)")
print("-"*70)
print(f"ŁĄCZNIE POKRYTE PRZEZ 6 PROJEKTÓW: {covered_count} / {acc_count} ({covered_count/acc_count*100:5.2f}% akceptowanych)")
print(f"POKRYCIE W CAŁEJ BAZIE (551): {covered_count} / 551 ({covered_count/551*100:5.2f}%)")
print("="*70)

void_orders = [x for x in accepted_orders if x not in covered_orders]
void_count = len(void_orders)
print(f"\nZLECENIA WISZĄCE W PRÓŻNI (BEZ IDEALNEGO DEMO): {void_count} / {acc_count} ({void_count/acc_count*100:5.2f}% akceptowanych)")
print(f"UDZIAŁ W CAŁEJ BAZIE (551): {void_count} / 551 ({void_count/551*100:5.2f}%)")

from collections import Counter
void_by_label = Counter(x['label'] for x in void_orders)
for label, cnt in void_by_label.most_common():
    print(f"  * {label:65} : {cnt:3d} ({cnt/acc_count*100:5.1f}% puli akceptowanej)")

print("\n--- PRZYKŁADOWE REALNE ID DLA KLASTRÓW W PRÓŻNI ---")
for label in void_by_label.keys():
    samples = [x['order']['id'] for x in void_orders if x['label'] == label][:6]
    print(f"\n{label}:")
    print(f"  Przykładowe ID: {', '.join(samples)}")
    for s_id in samples[:3]:
        o = next(x['order'] for x in void_orders if x['order']['id'] == s_id)
        print(f"    - #{o['id']} [{o['budget']}]: {o['title']}")
