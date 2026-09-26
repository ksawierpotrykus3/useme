import json

path = 'badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

updated = False
for item in data:
    if item.get('offer_id') == '2625963' or 'monik' in (item.get('title') or '').lower():
        item['status_umowy'] = 'WYPŁACONO WYKONAWCY'
        item['data_utworzenia_umowy'] = '2026-04-30'
        item['data_wyplaty'] = '2026-06-22'
        item['kwota_faktury_netto'] = 12100.0
        item['kwota_brutto'] = 14883.0
        item['wyplata_na_reke'] = 11083.52
        item['podatek_dochodowy'] = 708.0
        item['oplata_useme'] = 308.48
        item['przeniesienie_praw'] = 'Protokół'
        item['is_verified_paid_contract'] = True
        updated = True
        print(f"Updated item {item.get('offer_id')} in wygrane_56.json")
        break

if updated:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved updated wygrane_56.json")
else:
    print("Item not found!")
