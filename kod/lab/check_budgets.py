# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')
from loader import orders

for o in orders:
    b = o['budget']
    m = re.search(r'(\d+[\d\s]*)\s*(?:zł|pln)', b.lower().replace('\xa0', ' '))
    if m:
        val = float(m.group(1).replace(' ', ''))
        if val <= 500:
            print(f"{o['src']} | #{o['id']} | raw budget: '{b}' | val={val} | {o['title']}")
