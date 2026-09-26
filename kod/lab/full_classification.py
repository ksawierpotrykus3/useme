# -*- coding: utf-8 -*-
"""
Pełna klasyfikacja i klastrowanie 551 zleceń Useme.
Zasada: Żelazna dyscyplina analityczna, zero naciągania danych, pełna identyfikowalność per ID.
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

def is_red_ocean_order(o):
    """
    Zwraca (is_red: bool, subcategory: str, reason: str)
    Kryteria:
    - WordPress / Elementor / Divi / Wix / Webflow (poza zaawansowanymi integracjami backendowymi / API)
    - Tanie wizytówki / landing page dla lokalnych usług
    - Logo, grafika, banery, ulotki, identyfikacja wizualna
    - Copywriting, pisanie tekstów, tłumaczenia, transkrypcje
    - Proste poprawki CSS/HTML, drobne naprawy stron za 200-500 zł
    - Manualne wprowadzanie danych / dodawanie produktów
    - Marketing / SEO / Social Media
    - Mikrobudżety (<= 500 zł) bez zaawansowanego skryptu/inżynierii
    """
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + " " + d
    cat = o['cat'].lower()
    b_val = parse_budget(o['budget'])

    # Czy w zleceniu występuje twarda technologia inżynierska?
    # Sprawdzamy czy to nie jest zaawansowany projekt IT, który tylko powierzchownie wspomina stronę
    has_hard_tech = any(k in full for k in [
        'three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid',
        'scraper', 'scraping', 'waf', 'cloudflare', 'playwright', 'selenium', 'crawler',
        'ksef', 'erp', 'enova', 'comarch', 'subiekt', 'sap', 'symfonia', 'sap',
        'baselinker', 'allegro api', 'rest api', 'webhook', 'synchronizacj', 'mikro-saas',
        'n8n', 'make.com', 'rag', 'llm', 'langchain', 'openai api', 'fine-tuning',
        'react native', 'flutter', 'swift', 'kotlin', 'ios', 'android', 'pwa',
        'docker', 'kubernetes', 'devops', 'ci/cd', 'vps', 'linux', 'kvm',
        'bigquery', 'postgresql', 'mysql', 'sql server', 'hurtownia danych'
    ])

    # 1. Marketing / SEO / Kampanie reklamowe
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']):
        return True, "RED_MARKETING", "Marketing / SEO / Social Media"
    if any(k in t for k in ['kampania google ads', 'facebook ads', 'prowadzenie fanpage', 'link building', 'pozycjonowanie', 'google ads', 'meta ads', 'seo']):
        if not has_hard_tech and not any(k in t for k in ['programist', 'developer', 'skrypt', 'api']):
            return True, "RED_MARKETING", "Marketing / SEO / Social Media"

    # 2. Copywriting / Pisanie artykułów / Tłumaczenia
    if any(k in t for k in [
        'copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul',
        'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie',
        'tlumaczenie', 'transkrypcja', 'posty na bloga', 'wpisy na bloga', 'tworzenie treści', 'copy'
    ]) and not has_hard_tech:
        return True, "RED_COPYWRITING", "Copywriting / Pisanie artykułów / Treści"

    # 3. Grafika / Logo / Wizytówki / Banery / Mockupy
    if any(k in t for k in [
        'logo', 'logotyp', 'baner', 'banner', 'ulotk', 'plakat', 'projekt graficzny',
        'obróbka zdjęć', 'grafik do', 'szata graficzna', 'wizytówka', 'wizytowka',
        'materiały reklamowe', 'przygotowanie materiałów graficznych', 'mockup', 'ux/ui', 'figma'
    ]) and not has_hard_tech:
        # Jeśli tytuł to czysty design bez programowania
        if not any(k in t for k in ['programist', 'developer', 'wdrożenie', 'frontend', 'react', 'full stack']):
            return True, "RED_GRAPHICS", "Grafika / Logo / Identyfikacja wizualna"

    # 4. Manualne wprowadzanie danych / dodawanie produktów (Data entry)
    if any(k in t for k in [
        'dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów',
        'wklejanie produktów', 'wprowadzanie danych', 'przepisywanie',
        'wystawianie ofert na allegro', 'wystawienie ok 50 produktów', 'content entry', 'wystawianie ofert'
    ]) and not ('skrypt' in full or 'bot' in full or 'scraper' in full or 'api' in full or 'automatyz' in full or 'kod' in full):
        return True, "RED_DATA_ENTRY", "Manualne wprowadzanie produktów / danych"

    # 5. Drobne poprawki CSS/HTML / drobne naprawy stron / layout
    if any(k in t for k in [
        'poprawka css', 'poprawki css', 'modyfikacja css', 'poprawka html', 'poprawki html',
        'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawki na stronie',
        'poprawka na stronie', 'poprawki strony www', 'naprawa strony', 'odzyskanie dostępu',
        'drobne zmiany', 'poprawa szybkości', 'optymalizacja pagespeed', 'naprawienie pętli',
        'naprawa formularza', 'poprawienie strony', 'edycji strony', 'zmiany w lp', 'drobne poprawki strony'
    ]) and not has_hard_tech:
        return True, "RED_CSS_HTML_FIXES", "Drobne poprawki CSS/HTML / naprawy wizualne"

    # 6. Elementor / Divi / Wix / Webflow / Squarespace / Framer
    if any(k in t for k in ['elementor', 'divi', 'wix', 'webflow', 'greenshift', 'squarespace', 'framer']) and not has_hard_tech:
        return True, "RED_NO_CODE", "No-code / Page buildery (Elementor/Divi/Wix/Webflow)"

    # 7. WordPress (strony wizytówkowe, proste blogi, szablony)
    # Zlecenia typu "Programista WordPress", "Nowa strona WordPress", "Strona na WordPress", "Król WordPress"
    if 'wordpress' in t or ' na wp' in t or 'word press' in t:
        # Czy to jest zaawansowana integracja API/AI/ERP z WP?
        if any(k in t for k in ['api', 'gemini', 'openai', 'salesforce', 'integracja z', 'wtyczka integrująca']):
            pass # Zaawansowana integracja API!
        elif not has_hard_tech:
            return True, "RED_WORDPRESS", "WordPress (strony, szablony, administracja)"

    # Proste strony wizytówkowe / landing page / małe strony firmowe
    simple_web_kw = [
        'strona wizytówkowa', 'strona wizytowkowa', 'prosta strona', 'landing page dla',
        'strona www dla', 'strona internetowa dla', 'projekt i wykonanie strony internetowej',
        'stworzenie strony www', 'nowa strona www', 'nowa strona', 'postawienie strony',
        'tworzenie stron', 'strona dla agencji', 'strona dla gabinetu', 'strona dla biura',
        'strona dla firmy', 'wykonanie strony www', 'zlecę wykonanie strony', 'modernizacja istniejącej strony',
        'strona internetowa', 'wykonanie strony internetowej', 'strona dla dietetyczki',
        'strona dla suplementów', 'strona www', 'prosty landing page', 'budowa strony internetowej',
        'nowy landing'
    ]
    if any(k in t for k in simple_web_kw) and not has_hard_tech:
        # Sprawdźmy czy to nie jest dedykowany web app w Next.js/React/Laravel/SaaS
        if not any(k in full for k in ['react', 'vue', 'next.js', 'laravel', 'saas', 'crm', 'three.js', 'rezerwacj', 'django']):
            return True, "RED_WEBSITE_SIMPLE", "Prosta strona WWW / wizytówka / landing"

    # Proste sklepy internetowe na gotowych szablonach (np. "prosty sklep na shopify", "sklep internetowy 2 produktów")
    if any(k in t for k in [
        'prosty sklep', 'sklep – 2 produktów', 'sklep internetowy na shopify (ok. 15 produktów)',
        'stworzenie prostego jednoproduktowego sklepu', 'sklep internetowy z małym sklepem',
        'strona (a\'la sklep)', 'stworzenie od zera sklepu internetowego'
    ]) and not has_hard_tech and not any(k in full for k in ['b2b', 'erp', 'baselinker', 'hurtown', 'subskrypcj', 'api']):
        return True, "RED_WEBSITE_SIMPLE", "Prosty szablonowy sklep internetowy"

    # 8. Mikrobudżety (<= 500 zł) bez zaawansowanego skryptu/inżynierii
    if b_val is not None and b_val <= 500 and not has_hard_tech:
        if not any(k in t for k in ['skrypt', 'bot', 'python', 'scraping', 'narzędzie']):
            return True, "RED_MICRO_BUDGET", f"Mikrobudżet <= 500 PLN ({b_val} zł)"

    # 9. Obsługa stron / sklepów bez twardego IT
    if any(k in cat for k in ['serwisy internetowe · obsługa stron', 'serwisy internetowe · obsługa sklepów']) and not has_hard_tech:
        return True, "RED_MAINTENANCE", "Podstawowa obsługa stron / sklepów"

    return False, "ACCEPTED", "Zaakceptowane (Tier A/B)"

# Test klasyfikatora
red_list = []
acc_list = []
for o in orders:
    is_red, code, desc = is_red_ocean_order(o)
    if is_red:
        red_list.append((o, code, desc))
    else:
        acc_list.append(o)

print("="*60)
print(f"WYNIK SELEKCJI CZERWONEGO OCEANŮ (KROK 1 & 2):")
print(f"Łączna baza zleceń: {len(orders)}")
print(f"Odrzucone (Czerwony Ocean): {len(red_list)} ({len(red_list)/len(orders)*100:.2f}%)")
print(f"Zaakceptowane (Tier A i B): {len(acc_list)} ({len(acc_list)/len(orders)*100:.2f}%)")
print("="*60)

reasons_c = Counter(x[2] for x in red_list)
print("\nRozbicie odrzuconych wg kategorii:")
for r, c in reasons_c.most_common():
    print(f"  - {r}: {c} ({c/len(red_list)*100:.1f}%)")
