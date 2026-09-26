# -*- coding: utf-8 -*-
"""
Audyt i dopracowanie reguł Red Ocean na czysto.
"""
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
import re
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

def is_red_ocean_strict(o):
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + " " + d
    cat = o['cat'].lower()
    b_val = parse_budget(o['budget'])

    # Czy to specjalistyczna integracja backendowa / AI / 3D / Mobile / DevOps?
    # Sprawdzamy to w TYTULE lub w konkretnych frazach kluczowych w opisie
    is_real_ai = any(k in t for k in ['ai', 'llm', 'gpt', 'gemini', 'openai', 'ocr', 'rag', 'voicebot', 'chatbot', 'mistral', 'bielik', 'asystent ai']) or ('fine-tuning' in full or 'qlora' in full or 'ksef' in t)
    is_real_3d = any(k in t for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid', 'konfigurator']) and any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid', 'wymiar'])
    is_real_scraping = any(k in t for k in ['scraping', 'scraper', 'bot do wyszukiwania', 'crawling', 'crawler', 'monitoring cen', 'otomoto na allegro']) or (any(k in t for k in ['bot', 'skrypt']) and any(k in full for k in ['scraper', 'scraping', 'playwright', 'selenium', 'anty-captcha']))
    is_real_mobile = ('aplikacje mobilne' in cat) or any(k in t for k in ['aplikacja mobilna', 'aplikacji mobilnej', 'aplikację mobilną', 'react native', 'flutter', 'ios', 'android', 'swift', 'kotlin', 'gra mobilna'])
    is_real_devops = ('administracja serwerami' in cat) or any(k in t for k in ['administracja serwerem', 'devops', 'docker', 'kubernetes', 'vps', 'linux', 'ci/cd', 'wdrożeniowca do serwera'])
    is_real_api_erp = any(k in t for k in ['baselinker', 'subiekt', 'enova', 'comarch', 'sap', 'symfonia', 'wapro', 'api b2b', 'połączenie salesforce', 'sellasist', 'apilo']) or ('subiekt' in full and 'integracja' in t)

    is_high_tech_project = is_real_ai or is_real_3d or is_real_scraping or is_real_mobile or is_real_devops or is_real_api_erp

    # 1. Marketing / SEO / Kampanie reklamowe / Social media
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']):
        return True, "RED_MARKETING", "Marketing / SEO / Social Media"
    if any(k in t for k in [
        'kampania google ads', 'facebook ads', 'prowadzenie fanpage', 'link building',
        'pozycjonowanie', 'google ads', 'meta ads', 'seo - (white label)', 'audyt lejka',
        'cro, ux', 'head of growth', 'konfiguracja i weryfikacja gtm', 'naprawa meta piel',
        'seo, ux, copy', 'seo + seo pod ai', 'potrzebuję osoby, która pomoże mi skonfigurować konwersje',
        'strategia marketingowa'
    ]):
        return True, "RED_MARKETING", "Marketing / SEO / Social Media"

    # 2. Copywriting / Pisanie tekstów / Artykuły / Tłumaczenia
    if any(k in t for k in [
        'copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul',
        'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie',
        'tlumaczenie', 'transkrypcja', 'posty na bloga', 'wpisy na bloga', 'tworzenie treści'
    ]):
        return True, "RED_COPYWRITING", "Copywriting / Pisanie tekstów"

    # 3. Grafika / Logo / Wizytówki / Identyfikacja / Mockupy
    if any(k in t for k in [
        'logo', 'logotyp', 'baner', 'banner', 'ulotk', 'plakat', 'projekt graficzny',
        'obróbka zdjęć', 'grafik do', 'szata graficzna', 'wizytówka', 'wizytowka',
        'materiały reklamowe', 'przygotowanie materiałów graficznych', 'mockup', 'dodanie zakładki z logami'
    ]) and not is_real_3d:
        return True, "RED_GRAPHICS", "Grafika / Logo / Wizytówki"

    # 4. Manualne wprowadzanie danych / dodawanie produktów / ręczne wystawianie
    if any(k in t for k in [
        'dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów',
        'wklejanie produktów', 'wprowadzanie danych', 'przepisywanie',
        'wystawianie ofert na allegro', 'wystawienie ok 50 produktów', 'content entry',
        'wystawianie ofert', 'tester manualny do testowania'
    ]) and not is_real_scraping and not is_real_api_erp:
        return True, "RED_DATA_ENTRY", "Manualne wprowadzanie danych / produktów"

    # 5. Drobne poprawki CSS/HTML / drobne naprawy / optymalizacje wizualne
    if any(k in t for k in [
        'poprawka css', 'poprawki css', 'modyfikacja css', 'poprawka html', 'poprawki html',
        'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawki na stronie',
        'poprawka na stronie', 'poprawki strony www', 'naprawa strony', 'odzyskanie dostępu',
        'drobne zmiany', 'poprawa szybkości', 'optymalizacja pagespeed', 'naprawienie pętli',
        'naprawa formularza', 'poprawienie strony', 'edycji strony', 'zmiany w lp',
        'drobne poprawki strony', 'optymalizacja core web vitals', 'korekta cen w menu',
        'animacje na stronach internetowych', 'chatting na stronie', 'wersje mobilne stron:',
        'optymalizacji wydajności woocommerce', 'optymalizacja wydajności strony internetowej wordpress',
        'naprawa funkcjonalności wtyczki wpml', 'optymalizacja strony i sklepu ux'
    ]) and not is_high_tech_project:
        return True, "RED_CSS_HTML_FIXES", "Proste poprawki CSS/HTML / drobne naprawy"

    # 6. No-code / Page Buildery (Elementor, Divi, Wix, Webflow, Squarespace, Framer)
    if any(k in t for k in ['elementor', 'divi', 'wix', 'webflow', 'greenshift', 'squarespace', 'framer']) and not is_high_tech_project:
        return True, "RED_NO_CODE", "No-code / Page Buildery (Elementor/Divi/Wix)"

    # 7. WordPress (strony wizytówkowe, szablony, administracja WP)
    if ('wordpress' in t or ' na wp' in t or 'word press' in t or 'król / królowa wordpress' in t or 'wordpress specialist' in t or 'poszukujemy osoby do serwisowania i rozwoju strony wordpress' in t):
        if not is_high_tech_project:
            return True, "RED_WORDPRESS", "WordPress (proste strony, motywy, szablony)"

    # 8. Tanie strony WWW / wizytówki / landingi
    if any(k in t for k in [
        'strona wizytówkowa', 'strona wizytowkowa', 'prosta strona', 'landing page dla',
        'strona www dla', 'strona internetowa dla', 'projekt i wykonanie strony internetowej',
        'stworzenie strony www', 'nowa strona www', 'nowa strona', 'postawienie strony',
        'tworzenie stron', 'strona dla agencji', 'strona dla gabinetu', 'strona dla biura',
        'strona dla firmy', 'wykonanie strony www', 'zlecę wykonanie strony', 'modernizacja istniejącej strony',
        'strona internetowa', 'wykonanie strony internetowej', 'strona dla dietetyczki',
        'strona dla suplementów', 'strona www', 'prosty landing page', 'budowa strony internetowej',
        'nowy landing', 'stona intenetowa uk budownictwo', 'strona dla szkoły kulinarnej',
        'strona internetowa gabinetu', 'landing page z ofertą mebli', 'landing page pod kampanie',
        'wykonanie profesjonalnej strony', 'stworzenia 4 stron', 'firma perca zleci wykonanie landing',
        'deasing istniejacej juz strony', 'freelancer / agencja do obsługi strony',
        'aktualizacja strony internetowej z zakresu ochrony', 'stworzenie/przerobienie strony',
        'poszukiwana osoba do wykonania strony', 'stworzenie/poprawa strony internetowej',
        'landing page + 4 języki', 'oferta na rozbudowanie strony', 'strona internetowa firmy',
        'przeniesienie gotowego prototypu html na stronę w cms', 'projekt i wykonanie strony internetowej marki spożywczej'
    ]) and not is_high_tech_project:
        # Sprawdzamy czy to nie jest dedykowana aplikacja webowa w React/Next.js/Laravel
        if not any(k in full for k in ['react.js', 'next.js', 'laravel', 'vue.js', 'saas', 'crm']):
            return True, "RED_WEBSITE_SIMPLE", "Proste strony WWW / wizytówki / landingi"

    # 9. Proste sklepy internetowe na gotowcach (np. sklep 1-2 produkty, szablonik)
    if any(k in t for k in [
        'prosty sklep', 'sklep – 2 produktów', 'sklep internetowy na shopify (ok. 15 produktów)',
        'stworzenie prostego jednoproduktowego sklepu', 'sklep internetowy z małym sklepem',
        'strona (a\'la sklep)', 'stworzenie od zera sklepu internetowego',
        'zlecę dodanie prostego sklepu', 'sklep internetowy na wp', 'sklep internetowy – branża dziecięca',
        'wdrożenie strony wordpress + woocommerce', 'stworzenie prostej strony na worpress +prosty sklep',
        'skonfigurowanie sklepu na prestashop', 'konfiguracja prostego sklepu autorskiego na shoper storefront',
        'szukam osoby do shopify', 'konfiguracja wygladu sklepu', 'zlecę modyfikację szablonu w shoper'
    ]) and not is_high_tech_project and not any(k in full for k in ['b2b', 'erp', 'baselinker', 'hurtown', 'subskrypcj', 'api']):
        return True, "RED_WEBSITE_SIMPLE", "Proste sklepy szablonowe"

    # 10. Mikrobudżety (<= 500 zł) bez zaawansowanego skryptu/inżynierii
    if b_val is not None and b_val <= 500 and not is_high_tech_project:
        if not any(k in t for k in ['skrypt', 'bot', 'python', 'scraping', 'narzędzie']):
            return True, "RED_MICRO_BUDGET", f"Mikrobudżet <= 500 PLN ({b_val} zł)"

    # 11. Obsługa stron / sklepów / niemerytoryczne
    if any(k in cat for k in ['serwisy internetowe · obsługa stron', 'serwisy internetowe · obsługa sklepów']) and not is_high_tech_project:
        return True, "RED_MAINTENANCE", "Podstawowa obsługa stron / sklepów"
    if any(k in t for k in ['project manager', 'client-facing interviewer']):
        return True, "RED_NON_TECHNICAL", "Zlecenia niemerytoryczne / rekrutacja"

    return False, "ACCEPTED", "Zaakceptowane (Tier A/B)"

red_strict = []
acc_strict = []
for o in orders:
    is_red, tag, label = is_red_ocean_strict(o)
    if is_red:
        red_strict.append((o, tag, label))
    else:
        acc_strict.append(o)

print("="*70)
print("WYNIK RYGORYSTYCZNEJ SELEKCJI (CZERWONY OCEAN VS ZAAKCEPTOWANE):")
print("="*70)
print(f"Cała baza Useme: {len(orders)} zleceń")
print(f"1. Odrzucone (Czerwony Ocean): {len(red_strict)} ({len(red_strict)/len(orders)*100:.2f}%)")
print(f"2. Zaakceptowane (Tier A i B): {len(acc_strict)} ({len(acc_strict)/len(orders)*100:.2f}%)")
print("="*70)

from collections import Counter
r_c = Counter(x[2] for x in red_strict)
print("\nRozbicie Czerwonego Oceanu:")
for l, c in r_c.most_common():
    print(f"  - {l:50} : {c:3d} ({c/len(red_strict)*100:5.1f}% odrzuconych | {c/len(orders)*100:4.1f}% całej bazy)")
