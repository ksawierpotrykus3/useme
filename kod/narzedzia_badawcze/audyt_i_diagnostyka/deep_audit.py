# -*- coding: utf-8 -*-
"""
Głęboki audyt i analiza taksonomiczna 551 zleceń Useme.
"""
import sys
import re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from loader import orders

def parse_budget(b):
    if not b:
        return None
    b = b.replace('\xa0', ' ').strip()
    m = re.search(r'([\d\s]+)(?:,(\d{2}))?\s*(?:zł|pln)', b, re.IGNORECASE)
    if m:
        whole = m.group(1).replace(' ', '')
        dec = m.group(2) or '0'
        try:
            return float(f'{whole}.{dec}')
        except:
            return None
    return None

print("=== BADANIE RED OCEAN VS ACCEPTED ===")

# Sprawdźmy wszystkie zlecenia pod kątem Czerwonego Oceanu
# Kryteria:
# A. Kategoria:
#    - marketing · seo (jeśli czyste pozycjonowanie/linkbuilding)
#    - marketing · kampanie reklamowe (FB/Google ads)
#    - marketing · sprzedaż i obsługa sprzedaży (jeśli telemarketing/ogłoszenia)
# B. Tytuł / Opis:
#    - Copywriting / pisanie artykułów / opisy produktów / tłumaczenia / transkrypcje
#    - Grafika / Logo / banery / ulotki / identyfikacja / obróbka zdjęć
#    - WordPress / Elementor / Divi / Wix / Webflow (proste strony, szablony, blogi, wizytówki)
#      UWAGA: Jeśli zlecenie dotyczy zaawansowanej integracji API, dedykowanej wtyczki od zera, synchronizacji ERP/BaseLinker, czy aplikacji mobilnej łączącej się z WP -> czy to WP czy API?
#    - Proste poprawki CSS/HTML / drobne naprawy layoutu / przesunięcia elementów
#    - Tanie wizytówki / landing page dla lokalnych usług (budżet <= 1000 zł lub proste szablonowe)
#    - Budżet jawny <= 500 zł dla prac nieskryptowych (proste poprawki)
#    - Ręczne dodawanie produktów / wprowadzanie danych (data entry)

# Przeanalizujmy najpierw wszystkie 551 zleceń i wyświetlmy ich wstępną kategoryzację,
# aby sprawdzić każdy przypadek graniczny!

def classify_red_ocean(o):
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + " " + d
    cat = o['cat'].lower()
    b_val = parse_budget(o['budget'])
    
    # 1. Grafika i Design (bez 3D/CAD/WebGL)
    if any(k in t for k in ['logo', 'logotyp', 'baner', 'banner', 'ulotk', 'plakat', 'projekt graficzny', 'obróbka zdjęć', 'grafik do', 'szata graficzna', 'wizytówka', 'wizytowka']) and not any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'kod', 'programist', 'react', 'vue']):
        return "RED_GRAPHICS", "Grafika / Logo / Wizytówki"
        
    # 2. Copywriting i pisanie tekstów
    if any(k in t for k in ['copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul', 'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie', 'tlumaczenie', 'transkrypcja', 'posty na bloga', 'wpisy na bloga']):
        return "RED_COPYWRITING", "Copywriting / Pisanie tekstów"
        
    # 3. Marketing / SEO / Kampanie reklamowe
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']) or any(k in t for k in ['kampania google ads', 'facebook ads', 'prowadzenie fanpage', 'link building', 'pozycjonowanie']):
        return "RED_MARKETING", "Marketing / SEO / Social Media"
        
    # 4. Manualne wprowadzanie danych / wklejanie produktów
    if any(k in t for k in ['dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów', 'wklejanie produktów', 'wprowadzanie danych', 'przepisywanie']) and not any(k in full for k in ['skrypt', 'scraper', 'scraping', 'api', 'automatyz', 'bot', 'python']):
        return "RED_DATA_ENTRY", "Manualne wprowadzanie danych / produktów"
        
    # 5. Drobne poprawki CSS/HTML / drobne bugfixy layoutu (200-500 zł lub proste css)
    if any(k in t for k in ['poprawka css', 'poprawki css', 'poprawka html', 'poprawki html', 'modyfikacja css', 'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawka formularza', 'odzyskanie dostępu do', 'drobne zmiany na stronie']):
        return "RED_CSS_HTML_FIXES", "Proste poprawki CSS/HTML / drobne fixy"
        
    # 6. Elementor / Divi / Wix / Webflow w tytule lub jako główne zadanie
    if any(k in t for k in ['elementor', 'divi', 'wix', 'webflow']):
        return "RED_NO_CODE_BUILDERS", "Elementor / Divi / Wix / Webflow"

    # 7. WordPress - proste strony, wizytówki, szablony, blogi
    # Jeśli zlecenie w tytule lub opisie jest o WordPressie:
    if 'wordpress' in t:
        # Sprawdźmy czy to zaawansowana integracja lub custom development backendu:
        is_advanced = any(k in full for k in [
            'api', 'baselinker', 'erp', 'salesforce', 'synchronizacja', 'scraper', 
            'n8n', 'dedykowana wtyczka', 'dedykowany plugin', 'architektura', 
            'ksef', 'mikro-saas', 'aplikacja mobilna'
        ])
        # Jeśli to typowe zlecenie WP:
        if not is_advanced or any(k in t for k in ['strona wordpress', 'poprawki wordpress', 'szablon wordpress', 'motyw wordpress', 'strona na wordpress', 'programista wordpress', 'postawienie wordpress']):
            # Sprawdźmy czy to nie jest np. MVP z Gemini / integracja API
            if 'api' in t or 'integracja' in t or 'gemini' in t or 'openai' in t or 'ksef' in t:
                pass # Może być zaakceptowane jako integracja API/AI!
            else:
                return "RED_WORDPRESS", "WordPress / Proste strony i szablony"

    # 8. Tanie strony wizytówkowe / proste landingi (szczególnie z kategorii serwisy internetowe)
    if any(k in t for k in ['strona wizytówkowa', 'strona wizytowkowa', 'prosta strona', 'landing page dla', 'strona www dla', 'strona internetowa dla biura', 'strona dla gabinetu', 'strona dla salonu', 'wykonanie prostej strony', 'tworzenie stron']):
        if not any(k in full for k in ['three.js', 'webgl', '3d', 'aplikacja', 'saas', 'crm', 'react', 'vue', 'next.js', 'api', 'ksef']):
            return "RED_LANDING_WIZYTOWKA", "Prosta strona wizytówkowa / Landing"

    # 9. Bardzo niski budżet (<= 500 zł) na nieskomplikowane prace www
    if b_val is not None and b_val <= 500:
        if not any(k in full for k in ['skrypt', 'python', 'api', 'scraping', 'bot', 'automatyz']):
            return "RED_MICRO_BUDGET", f"Mikrobudżet (<= 500 zł: {b_val} zł)"

    return None, None

results = []
for o in orders:
    tag, desc = classify_red_ocean(o)
    results.append((o, tag, desc))

red_orders = [x for x in results if x[1] is not None]
accepted_orders = [x for x in results if x[1] is None]

print(f"Łącznie zleceń: {len(orders)}")
print(f"Czerwony Ocean: {len(red_orders)} ({len(red_orders)/len(orders)*100:.2f}%)")
print(f"Zaakceptowane (Tier A + B): {len(accepted_orders)} ({len(accepted_orders)/len(orders)*100:.2f}%)")

c_red = Counter(x[2] for x in red_orders)
print("\nRozbicie Czerwonego Oceanu:")
for k, v in c_red.most_common():
    print(f"  {k}: {v} ({v/len(red_orders)*100:.1f}%)")
