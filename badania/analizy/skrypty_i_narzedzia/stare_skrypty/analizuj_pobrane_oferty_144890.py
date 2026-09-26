# -*- coding: utf-8 -*-
import json
import re

with open('badania/oferty_konkurencji_144890.json', 'r', encoding='utf-8') as f:
    offers = json.load(f)

print(f"Łącznie pobranych ofert: {len(offers)}")

ceny = []
dni_list = []
raport = []

for o in offers:
    p_raw = o.get('price') or ''
    p_val = None
    m_p = re.search(r'([\d\s]+(?:,\d+)?)\s*PLN', p_raw)
    if m_p:
        try:
            p_val = float(m_p.group(1).replace(' ', '').replace(',', '.'))
            ceny.append(p_val)
        except:
            pass

    d_raw = o.get('days') or ''
    m_d = re.search(r'(\d+)', d_raw)
    d_val = int(m_d.group(1)) if m_d else None
    if d_val:
        dni_list.append(d_val)

    # pierwsze 120 znaków propozycji
    lead = o.get('proposal_text', '').replace('\n', ' ')[:100]
    raport.append({
        'author': o.get('author_name'),
        'contracts': o.get('author_contracts'),
        'price': p_val,
        'days': d_val,
        'lead': lead,
        'links_count': len(o.get('links') or []),
        'text_len': o.get('proposal_length')
    })

ceny.sort()
dni_list.sort()

median_cena = ceny[len(ceny)//2] if ceny else 0
avg_cena = sum(ceny)/len(ceny) if ceny else 0
min_cena = min(ceny) if ceny else 0
max_cena = max(ceny) if ceny else 0

median_dni = dni_list[len(dni_list)//2] if dni_list else 0

print("\n" + "="*80)
print(f"STATYSTYKI RYNKOWE DLA ZLECENIA #144890 (AI / OCR / n8n / Optima):")
print(f"Liczba ofert: {len(offers)}")
print(f"Ceny: Min = {min_cena:,.0f} PLN | Mediana = {median_cena:,.0f} PLN | Średnia = {avg_cena:,.0f} PLN | Max = {max_cena:,.0f} PLN")
print(f"Czas realizacji: Mediana = {median_dni} dni (Min: {min(dni_list) if dni_list else 0}, Max: {max(dni_list) if dni_list else 0})")
print("="*80 + "\n")

print(f"{'WYKONAWCA':<30} | {'UMOWY':<9} | {'CENA (PLN)':<10} | {'DNI':<5} | {'ZNAKÓW':<7} | {'LINKI'}")
print("-" * 80)
for r in sorted(raport, key=lambda x: (x['price'] or 0), reverse=True):
    print(f"{r['author']:<30} | {r['contracts']:<9} | {r['price'] or 0:>10.0f} | {r['days'] or 0:>5} | {r['text_len']:>7} | {r['links_count']} linków")
