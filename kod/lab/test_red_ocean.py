# -*- coding: utf-8 -*-
"""
Testowanie i kalibracja filtrów Czerwonego Oceanu.
"""
import sys
import re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
from loader import orders

def is_red_ocean(o):
    title = o['title'].lower()
    desc = o['desc'].lower()
    full = title + " " + desc
    cat = o['cat'].lower()
    
    # Wyciągnijmy liczbę z budżetu, jeśli jest podana
    budget_val = None
    m = re.search(r'(\d+[\d\s]*)\s*(?:zł|pln)', o['budget'].lower().replace('\xa0', ' '))
    if m:
        try:
            budget_val = float(m.group(1).replace(' ', ''))
        except:
            pass

    reasons = []

    # 1. Kategoria czysto nie-programistyczna / marketingowa / graficzna / SEO
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']):
        reasons.append(f"Kategoria marketing/seo: {cat}")
    
    # 2. Copywriting, pisanie artykułów, teksty, korekta, tłumaczenia
    copywriting_kw = [
        'copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul',
        'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie',
        'tlumaczenie', 'opisy produkt'
    ]
    if any(k in title for k in copywriting_kw) or (any(k in desc for k in ['pisanie artykułów', 'pisanie tekstów', 'copywritera']) and 'programist' not in full and 'api' not in full):
        reasons.append("Copywriting/teksty")

    # 3. Logo, grafika, banery, ulotki, identyfikacja wizualna
    graphics_kw = [
        'logo', 'logotyp', 'projekt graficzny', 'baner', 'banner', 'ulotk', 
        'plakat', 'wizytówk', 'wizytowk', 'obróbka zdjęć', 'grafik do', 'szata graficzna',
        'grafika do'
    ]
    if any(k in title for k in graphics_kw) and not any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc']):
        reasons.append("Grafika/Logo/Wizytówka")

    # 4. WordPress / Elementor / Divi / Wix / Webflow
    # Zwróćmy uwagę: Czy są zlecenia z WP, które są zaawansowanymi integracjami (np. n8n, BaseLinker, custom plugin backend, API)?
    # Prompt mówi: "(WordPress, Elementor, tanie wizytówki, logo, pisanie tekstów, proste poprawki CSS/HTML za 200-500 zł, copywriting, grafika)"
    # Sprawdźmy czy odrzucamy WSZYSTKIE zlecenia gdzie sednem jest strona WordPress/Elementor,
    # czy są jakieś wyjątki (np. połączenie Salesforce z WooCommerce - to integracja API).
    
    # Proste strony WordPress, Elementor, Divi, szablony, wizytówki
    wp_indicators = ['wordpress', 'elementor', 'divi', 'wix', 'webflow', 'prestashop', 'joomla']
    
    # Jeśli w tytule jest Elementor, Divi, Wix, Webflow -> bezwzględnie Red Ocean
    if any(k in title for k in ['elementor', 'divi', 'wix', 'webflow']):
        reasons.append("Elementor/Divi/Wix/Webflow w tytule")
    
    # Proste strony / wizytówki / landing page
    if any(k in title for k in ['strona wizytówkowa', 'strona wizytowkowa', 'prosta strona', 'landing page', 'one page', 'strona www dla']):
        if not any(k in full for k in ['three.js', 'webgl', '3d', 'aplikacja', 'system', 'react', 'vue', 'next']):
            reasons.append("Prosta strona/wizytówka")
            
    # Proste poprawki CSS / HTML / drobne bugfixy
    fixes_kw = [
        'poprawka css', 'poprawki css', 'poprawka html', 'poprawki html', 
        'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawki na stronie',
        'poprawka na stronie', 'naprawa strony', 'odzyskanie dostępu', 'drobne zmiany',
        'poprawka formularza', 'poprawa szybkości', 'optymalizacja pagespeed'
    ]
    if any(k in title for k in fixes_kw):
        reasons.append("Drobne poprawki CSS/HTML/strony")
        
    # Manualne wprowadzanie danych / dodawanie produktów
    data_entry_kw = ['dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów', 'wklejanie produktów', 'manualne']
    if any(k in title for k in data_entry_kw) and 'skrypt' not in full and 'scraper' not in full and 'automatyz' not in full:
        reasons.append("Manualne wprowadzanie produktów")

    # WordPress w tytule lub jako główne zadanie:
    if 'wordpress' in title:
        # Sprawdźmy czy to jest zaawansowany custom plugin / API czy zwykła robota WP
        is_advanced = any(k in full for k in ['api', 'baselinker', 'erp', 'salesforce', 'synchronizacja', 'scraper', 'n8n', 'dedykowana wtyczka'])
        # Ale jeśli to "programista wordpress", "poprawki wordpress", "strona wordpress", "motyw wordpress":
        if any(k in title for k in ['strona wordpress', 'poprawki wordpress', 'postawienie wordpress', 'szablon wordpress', 'motyw wordpress', 'strona na wordpress']):
            reasons.append("WordPress strona/poprawki")
        elif not is_advanced:
            reasons.append("WordPress ogólny bez zaawansowanego API/ERP")

    # Niska kwota (200-500 zł) na proste prace:
    if budget_val is not None and budget_val <= 500:
        if not any(k in full for k in ['skrypt', 'python', 'api', 'scraping']):
            reasons.append(f"Bardzo niski budżet ({budget_val} zł)")

    return reasons

red_count = 0
reasons_dist = Counter()
red_orders = []
accepted_orders = []

for o in orders:
    res = is_red_ocean(o)
    if res:
        red_count += 1
        for r in res:
            reasons_dist[r] += 1
        red_orders.append((o, res))
    else:
        accepted_orders.append(o)

print(f"Łącznie zleceń: {len(orders)}")
print(f"Czerwony Ocean (odrzucone): {red_count} ({red_count/len(orders)*100:.1f}%)")
print(f"Zaakceptowane (Tier A + B): {len(accepted_orders)} ({len(accepted_orders)/len(orders)*100:.1f}%)")
print("\nRozkład przyczyn odrzucenia:")
for r, c in reasons_dist.most_common():
    print(f"  {r}: {c}")
