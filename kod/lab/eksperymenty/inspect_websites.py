# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from loader import orders

web_orders = [o for o in orders if 'strony internetowe' in o['cat'].lower() or o['cat'] == 'serwisy-internetowe']
print(f"Liczba zleceń w kategoriach stron www: {len(web_orders)}")

for i, o in enumerate(web_orders):
    print(f"[{i+1}] {o['src']} | #{o['id']} | {o['budget']} | {o['title']}")
