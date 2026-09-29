# -*- coding: utf-8 -*-
"""
Precyzyjny filtr Czerwonego Oceanu i weryfikacja każdego zlecenia.
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

def evaluate_order(o):
    title = o['title'].lower()
    desc = o['desc'].lower()
    full = title + " " + desc
    cat = o['cat'].lower()
    b_val = parse_budget(o['budget'])

    # Czy to zaawansowane inżynieryjne zadanie, które przypadkiem zawiera słowo WP/grafika?
    is_high_tech = any(k in full for k in [
        'three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid',
        'scraper', 'scraping', 'waf', 'cloudflare', 'playwright', 'selenium', 'crawler',
        'ksef', 'erp', 'enova', 'comarch', 'subiekt', 'sap', 'symfonia',
        'baselinker', 'allegro api', 'rest api', 'webhook', 'synchronizacj',
        'n8n', 'make.com', 'rag', 'llm', 'langchain', 'openai api', 'fine-tuning', 'vision',
        'react native', 'flutter', 'swift', 'kotlin', 'ios', 'android',
        'docker', 'kubernetes', 'devops', 'ci/cd', 'vps', 'linux', 'kvm',
        'bigquery', 'postgresql', 'mysql', 'optymalizacja bazy', 'hurtownia danych'
    ])

    # 1. Kategoria czysty marketing / SEO / obsługa
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']):
        return True, "RED_MARKETING", "Marketing / SEO / Social Media"

    # 2. Copywriting / Pisanie tekstów / Tłumaczenia
    if any(k in title for k in [
        'copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul',
        'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie',
        'tlumaczenie', 'transkrypcja', 'posty na bloga', 'wpisy na bloga', 'tworzenie treści'
    ]):
        return True, "RED_COPYWRITING", "Copywriting / Pisanie tekstów"

    # 3. Grafika / Logo / Wizytówki / Banery / Mockupy
    if any(k in title for k in [
        'logo', 'logotyp', 'baner', 'banner', 'ulotk', 'plakat', 'projekt graficzny',
        'obróbka zdjęć', 'grafik do', 'szata graficzna', 'wizytówka', 'wizytowka',
        'materiały reklamowe', 'przygotowanie materiałów graficznych', 'mockup'
    ]) and not ('three.js' in full or 'webgl' in full or '3d' in full or 'cad' in full):
        return True, "RED_GRAPHICS", "Grafika / Logo / Identyfikacja wizualna"

    # 4. Manualne wprowadzanie danych / wklejanie produktów (Content entry)
    if any(k in title for k in [
        'dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów',
        'wklejanie produktów', 'wprowadzanie danych', 'przepisywanie',
        'wystawianie ofert na allegro', 'wystawienie ok 50 produktów', 'content entry'
    ]) and not ('skrypt' in full or 'bot' in full or 'scraper' in full or 'api' in full or 'automatyz' in full):
        return True, "RED_DATA_ENTRY", "Manualne wprowadzanie produktów / danych"

    # 5. Proste poprawki CSS/HTML / drobne naprawy stron / layout
    if any(k in title for k in [
        'poprawka css', 'poprawki css', 'modyfikacja css', 'poprawka html', 'poprawki html',
        'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawki na stronie',
        'poprawka na stronie', 'poprawki strony www', 'naprawa strony', 'odzyskanie dostępu',
        'drobne zmiany', 'poprawa szybkości', 'optymalizacja pagespeed'
    ]) and not is_high_tech:
        return True, "RED_CSS_HTML_FIXES", "Drobne poprawki CSS/HTML / naprawy wizualne"

    # 6. Elementor / Divi / Wix / Webflow / Squarespace w tytule lub jako rdzeń
    if any(k in title for k in ['elementor', 'divi', 'wix', 'webflow', 'greenshift']) and not is_high_tech:
        return True, "RED_NO_CODE", "No-code / Page buildery (Elementor/Divi/Wix/Webflow)"

    # 7. WordPress - strony wizytówkowe, blogi, szablony, proste sklepy WP
    # Jeśli w tytule występuje WordPress:
    if 'wordpress' in title:
        # Jeśli to zaawansowana integracja lub API (np. custom plugin, KSeF, Gemini API, Salesforce)
        if any(k in title for k in ['api', 'gemini', 'openai', 'salesforce', 'integracja']):
            pass # Nie odrzucamy od razu!
        elif not is_high_tech:
            return True, "RED_WORDPRESS", "WordPress (strony, motywy, szablony, administracja)"

    # Sprawdźmy opis: jeśli to typowa strona na WP / szablon
    if any(k in title for k in [
        'strona wizytówkowa', 'strona wizytowkowa', 'prosta strona', 'landing page dla',
        'strona www dla', 'strona internetowa dla', 'projekt i wykonanie strony internetowej',
        'stworzenie strony www', 'nowa strona www', 'nowa strona wordpress', 'postawienie strony',
        'tworzenie stron', 'strona dla agencji', 'strona dla gabinetu', 'strona dla biura',
        'strona dla firmy', 'wykonanie strony www', 'zlecę wykonanie strony', 'modernizacja istniejącej strony'
    ]) and not is_high_tech:
        # Sprawdźmy czy to nie jest np. portal SaaS z autorskim kodem
        if not any(k in full for k in ['react', 'vue', 'next', 'django', 'laravel', 'fastapi', 'spring', 'saas', 'three.js']):
            return True, "RED_WEBSITE_SIMPLE", "Prosta strona WWW / wizytówka / landing"

    # 8. Mikrobudżety (<= 500 zł) bez zaawansowanego skryptu/inżynierii
    if b_val is not None and b_val <= 500 and not is_high_tech:
        if not any(k in title for k in ['skrypt', 'bot', 'python', 'scraping']):
            return True, "RED_MICRO_BUDGET", f"Mikrobudżet <= 500 PLN ({b_val} zł)"

    # 9. Sprawdźmy zlecenia z kategorii obsługa stron internetowych / obsługa sklepów bez automatyzacji
    if 'obsługa stron internetowych' in cat and not is_high_tech:
        return True, "RED_WEBSITE_MAINTENANCE", "Podstawowa obsługa stron / serwisu"

    return False, "ACCEPTED", "Zaakceptowane (Tier A/B)"

red_orders = []
accepted_orders = []

for o in orders:
    is_red, code, reason = evaluate_order(o)
    if is_red:
        red_orders.append((o, code, reason))
    else:
        accepted_orders.append(o)

print(f"ŁĄCZNA LICZBA ZLECEŃ: {len(orders)}")
print(f"ODRZUCONE (Czerwony Ocean): {len(red_orders)} ({len(red_orders)/len(orders)*100:.1f}%)")
print(f"ZAAKCEPTOWANE (Tier A i B): {len(accepted_orders)} ({len(accepted_orders)/len(orders)*100:.1f}%)")

print("\nRozbicie odrzuconych wg przyczyny:")
reasons_c = Counter(x[2] for x in red_orders)
for r, c in reasons_c.most_common():
    print(f"  - {r}: {c} ({c/len(red_orders)*100:.1f}%)")
