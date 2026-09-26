# -*- coding: utf-8 -*-
import json

with open('badania/analiza_gleboka_ofert.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== WSZYSTKIE LINKI ZAŁĄCZONE W OFERTACH ===")
for o in data['offers']:
    if o['links']:
        print(f"\n{o['author']} (Cena: {o['price']} PLN):")
        for l in o['links']:
            print(f"  -> {l}")

print("\n\n" + "="*80)
print("=== PIERWSZE 2 ZDANIA (HOOKI) TOP WYKONAWCÓW ===")
for o in data['offers'][:12]:
    print(f"\n[{o['author']} - {o['price']} PLN / {o['contracts']}]")
    print(f"HOOK: {o['hook'][:200]}...")
