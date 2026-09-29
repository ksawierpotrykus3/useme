# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from eval_red_ocean import accepted_orders

print("Checking accepted orders for WP / simple web...")
suspects = []
for o in accepted_orders:
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + ' ' + d
    if any(k in full for k in ['wordpress', 'woocommerce', 'prestashop', 'strona', 'landing', 'sklep', 'shoper']):
        suspects.append(o)

print(f"Suspects count: {len(suspects)}")
print("\n--- FIRST 70 SUSPECTS ---")
for i, o in enumerate(suspects[:70]):
    print(f"[{i+1}] {o['src']} | #{o['id']} | {o['budget']} | {o['title']}")
