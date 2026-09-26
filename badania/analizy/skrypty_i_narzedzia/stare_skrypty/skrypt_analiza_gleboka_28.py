# -*- coding: utf-8 -*-
import json
import re

with open('badania/oferty_konkurencji_144890.json', 'r', encoding='utf-8') as f:
    offers = json.load(f)

print(f"Liczba ofert do analizy: {len(offers)}")

# Badamy technologie, hooki, linki, wzorce
tech_mentions = {
    'KSeF': 0,
    'n8n': 0,
    'Make / Integromat': 0,
    'Docker / VPS': 0,
    'Sfera (Optima)': 0,
    'XML / EDI (Import)': 0,
    'MSSQL / Baza danych': 0,
    'OpenAI / GPT': 0,
    'Claude / Anthropic': 0,
    'Textract / AWS': 0,
    'Python / FastAPI': 0,
    'Retainer / Miesięczny abonament': 0
}

offers_analysis = []

for o in offers:
    text = o.get('proposal_text', '')
    text_lower = text.lower()
    
    # Detekcja technologii
    if 'ksef' in text_lower: tech_mentions['KSeF'] += 1
    if 'n8n' in text_lower: tech_mentions['n8n'] += 1
    if 'make' in text_lower or 'integromat' in text_lower: tech_mentions['Make / Integromat'] += 1
    if 'docker' in text_lower or 'vps' in text_lower or 'serwer' in text_lower: tech_mentions['Docker / VPS'] += 1
    if 'sfera' in text_lower: tech_mentions['Sfera (Optima)'] += 1
    if 'xml' in text_lower or 'edi' in text_lower or 'import' in text_lower: tech_mentions['XML / EDI (Import)'] += 1
    if 'sql' in text_lower or 'baza' in text_lower or 'mssql' in text_lower: tech_mentions['MSSQL / Baza danych'] += 1
    if 'openai' in text_lower or 'gpt' in text_lower or 'chatgpt' in text_lower: tech_mentions['OpenAI / GPT'] += 1
    if 'claude' in text_lower or 'anthropic' in text_lower: tech_mentions['Claude / Anthropic'] += 1
    if 'textract' in text_lower or 'aws' in text_lower: tech_mentions['Textract / AWS'] += 1
    if 'python' in text_lower or 'fastapi' in text_lower: tech_mentions['Python / FastAPI'] += 1
    if 'miesięczn' in text_lower or 'abonament' in text_lower or 'retainer' in text_lower or '/mc' in text_lower: tech_mentions['Retainer / Miesięczny abonament'] += 1
    
    # Cena i czas
    p_raw = o.get('price') or ''
    m_p = re.search(r'([\d\s]+(?:,\d+)?)\s*PLN', p_raw)
    price = float(m_p.group(1).replace(' ', '').replace(',', '.')) if m_p else 0
    
    m_d = re.search(r'(\d+)', o.get('days') or '')
    days = int(m_d.group(1)) if m_d else 0
    
    # Pierwsze 2 linijki (Hook)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    hook = ' '.join(lines[:2]) if lines else ''
    
    offers_analysis.append({
        'id': o.get('offer_id'),
        'author': o.get('author_name'),
        'contracts': o.get('author_contracts'),
        'price': price,
        'days': days,
        'length': len(text),
        'links': o.get('links', []),
        'hook': hook,
        'full_text': text
    })

print("\n=== CZĘSTOŚĆ WYSTĘPOWANIA TECHNOLOGII W 28 OFERTACH ===")
for tech, count in sorted(tech_mentions.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(offers)) * 100
    print(f"  {tech:<30}: {count:2d} ofert ({pct:4.1f}%)")

with open('badania/analiza_gleboka_ofert.json', 'w', encoding='utf-8') as out:
    json.dump({'tech_mentions': tech_mentions, 'offers': offers_analysis}, out, ensure_ascii=False, indent=2)

print("\nZapisano badania/analiza_gleboka_ofert.json")
