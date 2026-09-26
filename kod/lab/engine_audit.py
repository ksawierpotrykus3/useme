# -*- coding: utf-8 -*-
"""
Precyzyjny silnik analityczny: Red Ocean vs Akceptowane + Klastrowanie 551 zleceń.
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

def is_hard_tech(full_text):
    """Czy w treści zlecenia występuje twarda technologia programistyczna/inżynierska?"""
    return any(k in full_text for k in [
        'three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid',
        'scraper', 'scraping', 'waf', 'cloudflare', 'playwright', 'selenium', 'crawler',
        'ksef', 'erp', 'enova', 'comarch', 'subiekt', 'sap', 'symfonia', 'wapro',
        'baselinker', 'allegro api', 'rest api', 'webhook', 'synchronizacj', 'mikro-saas',
        'n8n', 'make.com', 'rag', 'llm', 'langchain', 'openai api', 'fine-tuning',
        'react native', 'flutter', 'swift', 'kotlin', 'ios', 'android', 'pwa',
        'docker', 'kubernetes', 'devops', 'ci/cd', 'vps', 'linux', 'kvm',
        'bigquery', 'postgresql', 'mysql', 'mariadb', 'sql server', 'hurtownia danych',
        'laravel', 'django', 'fastapi', 'spring boot', 'nestjs', 'next.js', 'vue', 'react'
    ])

def classify_order(o):
    title = o['title'].lower()
    desc = o['desc'].lower()
    full = title + " " + desc
    cat = o['cat'].lower()
    b_val = parse_budget(o['budget'])
    hard_tech = is_hard_tech(full)

    # ==========================================
    # KROK 1: FILTROWANIE CZERWONEGO OCEANŮ
    # ==========================================

    # 1. Marketing, SEO, Social Media, Reklamy
    if any(k in cat for k in ['marketing · seo', 'marketing · kampanie reklamowe', 'marketing · sprzedaż']):
        return "RED_OCEAN", "Marketing / SEO / Social Media", "Kategoria marketingowa / SEO"
    if any(k in title for k in [
        'kampania google ads', 'facebook ads', 'prowadzenie fanpage', 'link building',
        'pozycjonowanie', 'google ads', 'meta ads', 'seo - (white label)', 'audyt lejka',
        'cro, ux', 'head of growth', 'konfiguracja i weryfikacja gtm', 'naprawa meta piel'
    ]):
        return "RED_OCEAN", "Marketing / SEO / Social Media", "Czysty marketing / kampanie / SEO"

    # 2. Copywriting, pisanie artykułów, teksty, korekta, tłumaczenia
    if any(k in title for k in [
        'copywriting', 'pisanie tekst', 'napisanie tekst', 'artykuł', 'artykul',
        'tekstów seo', 'tekstow seo', 'korekta tekst', 'redagowanie', 'tłumaczenie',
        'tlumaczenie', 'transkrypcja', 'posty na bloga', 'wpisy na bloga', 'tworzenie treści',
        'seo, ux, copy'
    ]):
        return "RED_OCEAN", "Copywriting / Pisanie tekstów", "Copywriting / tłumaczenia"

    # 3. Grafika, Logo, Wizytówki, Banery, Mockupy, Ulotki
    if any(k in title for k in [
        'logo', 'logotyp', 'baner', 'banner', 'ulotk', 'plakat', 'projekt graficzny',
        'obróbka zdjęć', 'grafik do', 'szata graficzna', 'wizytówka', 'wizytowka',
        'materiały reklamowe', 'przygotowanie materiałów graficznych', 'mockup', 'dodanie zakładki z logami'
    ]) and not any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc']):
        return "RED_OCEAN", "Grafika / Logo / Wizytówki", "Projektowanie graficzne / materiały reklamowe"

    # 4. Manualne wprowadzanie danych, wklejanie produktów (Content/Data Entry), Manualne testy
    if any(k in title for k in [
        'dodanie produktów', 'dodawanie produktów', 'wprowadzanie produktów',
        'wklejanie produktów', 'wprowadzanie danych', 'przepisywanie',
        'wystawianie ofert na allegro', 'wystawienie ok 50 produktów', 'content entry',
        'wystawianie ofert', 'tester manualny do testowania'
    ]) and not ('skrypt' in full or 'bot' in full or 'scraper' in full or 'api' in full or 'automatyz' in full):
        return "RED_OCEAN", "Manualne wprowadzanie danych / produktów", "Ręczne wklejanie / manualne testy"

    # 5. Proste poprawki CSS/HTML, naprawy layoutu, mikro-fixy
    if any(k in title for k in [
        'poprawka css', 'poprawki css', 'modyfikacja css', 'poprawka html', 'poprawki html',
        'prosta poprawka', 'drobne poprawki', 'drobna poprawka', 'poprawki na stronie',
        'poprawka na stronie', 'poprawki strony www', 'naprawa strony', 'odzyskanie dostępu',
        'drobne zmiany', 'poprawa szybkości', 'optymalizacja pagespeed', 'naprawienie pętli',
        'naprawa formularza', 'poprawienie strony', 'edycji strony', 'zmiany w lp',
        'drobne poprawki strony', 'optymalizacja core web vitals', 'korekta cen w menu',
        'animacje na stronach internetowych', 'chatting na stronie'
    ]) and not hard_tech:
        return "RED_OCEAN", "Proste poprawki CSS/HTML / drobne naprawy", "Drobne poprawki wizualne / mikro-fixy"

    # 6. Elementor, Divi, Wix, Webflow, Squarespace, Framer (No-code / Page Buildery)
    if any(k in title for k in ['elementor', 'divi', 'wix', 'webflow', 'greenshift', 'squarespace', 'framer']) and not hard_tech:
        return "RED_OCEAN", "No-code / Page Buildery (Elementor/Divi/Wix)", "Kreatory stron / page buildery"

    # 7. WordPress - strony wizytówkowe, proste motywy, szablony, administracja
    if ('wordpress' in title or ' na wp' in title or 'word press' in title or 'król / królowa wordpress' in title or 'wordpress specialist' in title):
        # Sprawdzamy czy to zaawansowana integracja API/ERP/AI
        if any(k in title for k in ['api', 'gemini', 'openai', 'salesforce', 'integracja z', 'wtyczka integrująca']):
            pass # Przepuszczamy jako zaawansowane API / AI
        elif not hard_tech:
            return "RED_OCEAN", "WordPress (proste strony, motywy, szablony)", "Standardowy WordPress bez zaawansowanego backendu"

    # 8. Tanie strony wizytówkowe, landing pages dla lokalnych firm
    if any(k in title for k in [
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
        'poszukiwana osoba do wykonania strony', 'stworzenie/poprawa strony internetowej'
    ]) and not hard_tech:
        if not any(k in full for k in ['react', 'vue', 'next.js', 'laravel', 'saas', 'crm', 'three.js', 'rezerwacj', 'django', 'fastapi']):
            return "RED_OCEAN", "Proste strony WWW / wizytówki / landingi", "Tania strona wizytówkowa / landing page"

    # 9. Proste sklepy internetowe na szablonach / jedno-produktowe / proste konfiguracje
    if any(k in title for k in [
        'prosty sklep', 'sklep – 2 produktów', 'sklep internetowy na shopify (ok. 15 produktów)',
        'stworzenie prostego jednoproduktowego sklepu', 'sklep internetowy z małym sklepem',
        'strona (a\'la sklep)', 'stworzenie od zera sklepu internetowego',
        'zlecę dodanie prostego sklepu', 'sklep internetowy na wp', 'sklep internetowy – branża dziecięca',
        'wdrożenie strony wordpress + woocommerce', 'stworzenie prostej strony na worpress +prosty sklep',
        'skonfigurowanie sklepu na prestashop', 'konfiguracja prostego sklepu autorskiego na shoper storefront',
        'szukam osoby do shopify'
    ]) and not hard_tech and not any(k in full for k in ['b2b', 'erp', 'baselinker', 'hurtown', 'subskrypcj', 'api', 'custom']):
        return "RED_OCEAN", "Proste sklepy szablonowe", "Prosty szablonowy sklep e-commerce"

    # 10. Mikrobudżety (<= 500 zł)
    if b_val is not None and b_val <= 500 and not hard_tech:
        if not any(k in title for k in ['skrypt', 'bot', 'python', 'scraping', 'narzędzie']):
            return "RED_OCEAN", f"Mikrobudżet <= 500 PLN ({b_val} zł)", "Budżet poniżej progu opłacalności"

    # 11. Obsługa stron / sklepów / niemerytoryczne zlecenia
    if any(k in cat for k in ['serwisy internetowe · obsługa stron', 'serwisy internetowe · obsługa sklepów']) and not hard_tech:
        return "RED_OCEAN", "Podstawowa obsługa stron / sklepów", "Niemerytoryczna obsługa bieżąca"
    if any(k in title for k in ['project manager', 'client-facing interviewer']):
        return "RED_OCEAN", "Zlecenia niemerytoryczne / rekrutacja", "Zlecenie nie-programistyczne"

    # ==========================================
    # KROK 2 & 3: KLASTROWANIE ZAAKCEPTOWANYCH (TIER A & B)
    # ==========================================

    # KLASTER 1: Aplikacje Mobilne (React Native / Flutter / iOS / Android)
    if ('aplikacje mobilne' in cat) or any(k in title for k in [
        'aplikacja mobilna', 'aplikacji mobilnej', 'aplikację mobilną',
        'react native', 'flutter', 'ios', 'android', 'swift', 'swiftui', 'kotlin', 'gra mobilna'
    ]) or (any(k in full for k in ['react native', 'flutter', 'swiftui', 'kotlin multiplatform']) and 'mobiln' in full):
        return "ACCEPTED", "K1_MOBILE", "Aplikacje Mobilne (React Native / Flutter / iOS / Android)"

    # KLASTER 2: Cloud, DevOps & Administracja Serwerami
    if ('administracja serwerami' in cat) or any(k in title for k in [
        'administracja serwerem', 'konfiguracja serwera', 'wdrożeniowca do serwera',
        'devops', 'docker', 'kubernetes', 'vps', 'linux', 'ci/cd', 'serwer', 'hosting',
        'migracja serwera', 'migracja poczty', 'chmurowej', 'chmura', 'aws', 'atlassian cloud',
        'sharepoint'
    ]):
        return "ACCEPTED", "K2_CLOUD_DEVOPS", "Cloud, DevOps & Administracja Serwerami (Linux / Docker / VPS)"

    # KLASTER 3: Konfiguratory 3D, WebGL & CAD/CAM/CNC
    if any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid', 'babylon', 'dxf', 'g-code']) and any(k in title for k in ['konfigurator', '3d', 'mebli', 'ar', 'kadrowanie', 'fototapet']):
        return "ACCEPTED", "K3_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"
    if any(k in title for k in ['konfigurator 3d', 'konfiguratora 3d', 'konfigurator']):
        return "ACCEPTED", "K3_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"

    # KLASTER 4: Scraping, Web Crawling & WAF Bypass (Boty Danych)
    if any(k in title for k in ['scraping', 'scraper', 'bot do wyszukiwania', 'crawling', 'crawler', 'pobieranie danych', 'monitoring cen', 'otomoto na allegro', 'badanie rynku']):
        return "ACCEPTED", "K4_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"
    if any(k in full for k in ['playwright', 'puppeteer', 'selenium', 'anti-captcha', 'cloudflare bypass', 'scraping']) and any(k in title for k in ['bot', 'skrypt', 'pobieranie', 'danych']):
        return "ACCEPTED", "K4_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"

    # KLASTER 5: Bazy Danych, SQL, BigQuery & Data Engineering
    if any(k in title for k in ['bigquery', 'baza danych', 'bazy danych', 'sql server', 'postgresql', 'mysql', 'mariadb', 'hurtownia danych', 'optymalizacja zapytań', 'etl']) or ('bigquery' in full and 'api' in title):
        return "ACCEPTED", "K5_DATABASES", "Bazy Danych, SQL, BigQuery & Data Engineering"

    # KLASTER 6: AI, Agenci LLM, OCR Dokumentów & RAG
    if any(k in title for k in ['ai', 'llm', 'ocr', 'rag', 'gpt', 'openai', 'gemini', 'bielik', 'voicebot', 'chatbot', 'mistral', 'asystent ai', 'agent ai']):
        return "ACCEPTED", "K6_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"
    if any(k in full for k in ['ocr', 'langchain', 'llamaindex', 'qlora', 'fine-tuning', 'ksef']) and any(k in title for k in ['faktur', 'dokument', 'automatyzacj', 'ksef']):
        return "ACCEPTED", "K6_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"

    # KLASTER 7: Automatyzacje Procesów (n8n / Make / Zapier / Workflow)
    if any(k in title for k in ['n8n', 'make', 'make.com', 'zapier', 'automatyzacja procesów', 'automatyzacja testu', 'automatyzacja']):
        return "ACCEPTED", "K7_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"
    if any(k in full for k in ['n8n', 'make.com', 'zapier']) and any(k in title for k in ['integracja', 'automatyzacja', 'obieg']):
        return "ACCEPTED", "K7_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"

    # KLASTER 8: Systemy Rezerwacji, Booking & Concurrency
    if any(k in title for k in ['rezerwacj', 'booking', 'najmem', 'terminarz', 'wizyt', 'kalendarz']) or ('system rezerwacji' in full):
        return "ACCEPTED", "K8_RESERVATION", "Systemy Rezerwacji, Booking & Concurrency"

    # KLASTER 9: Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova / SAP)
    if any(k in title for k in [
        'baselinker', 'subiekt', 'enova', 'comarch', 'symfonia', 'sap', 'erp',
        'allegro', 'apilo', 'sellasist', 'marketplace', 'integracja api', 'połączenie salesforce',
        'synchronizacja sklepu', 'synchronizacj', 'wymiany danych', 'api b2b', 'feed'
    ]) or (any(k in full for k in ['baselinker', 'subiekt gt', 'subiekt nexo', 'enova365', 'comarch opty']) and any(k in title for k in ['integracja', 'synchronizacja', 'wdrożenie'])):
        return "ACCEPTED", "K9_API_SYNC", "Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova)"

    # KLASTER 10: E-commerce Zaawansowany, B2B & Platformy Hurtowe (IdoSell B2B, Shopify Plus, PrestaShop B2B, Magento)
    if any(k in title for k in [
        'idosell', 'b2b', 'shopify', 'prestashop', 'magento', 'shoper', 'woocommerce', 'sklep'
    ]) or any(k in cat for k in ['sklepy internetowe']):
        return "ACCEPTED", "K10_ECOMMERCE_ADVANCED", "E-commerce Zaawansowany, B2B & Dedykowane Sklepy (IdoSell/Shopify/Presta)"

    # KLASTER 11: Enterprise CRM, SaaS & Dedykowane Web Apps (React, Next.js, Node, Laravel, Python, FastAPI)
    # Zlecenia na aplikacje webowe, systemy portalowe, backendy, architekturę
    return "ACCEPTED", "K11_CRM_SAAS_WEB", "Enterprise CRM, SaaS & Dedykowane Web Apps (React/Next/Node/Laravel)"

classified_data = []
for o in orders:
    status, tag, label = classify_order(o)
    classified_data.append({
        'order': o,
        'status': status,
        'tag': tag,
        'label': label
    })

red_orders = [x for x in classified_data if x['status'] == "RED_OCEAN"]
accepted_orders = [x for x in classified_data if x['status'] == "ACCEPTED"]

print("="*70)
print("RAPORT KLASYFIKACJI BAZY 551 ZLECEŃ USEME")
print("="*70)
print(f"1. ŁĄCZNA PRÓBA BADAWCZA: {len(orders)} zleceń")
print(f"   - 406 zleceń historycznych (archiwum)")
print(f"   -  61 zleceń w toku (kategoria programowanie-i-it)")
print(f"   -  84 zlecenia w toku (kategoria serwisy-internetowe)")
print(f"\n2. CZERWONY OCEAN (BEZWZGLĘDNY AUTO-REJECT): {len(red_orders)} ({len(red_orders)/len(orders)*100:.2f}%)")
print(f"3. ZAAKCEPTOWANE DO OFERTOWANIA (TIER A & TIER B): {len(accepted_orders)} ({len(accepted_orders)/len(orders)*100:.2f}%)")
print("="*70)

print("\nSZCZEGÓŁOWY ROZKŁAD PRZYCZYN ODRZUCENIA (CZERWONY OCEAN):")
red_counts = Counter(x['tag'] for x in red_orders)
for tag, cnt in red_counts.most_common():
    print(f"  - {tag:50} : {cnt:3d} ({cnt/len(red_orders)*100:5.1f}% odrzuconych | {cnt/len(orders)*100:4.1f}% całej bazy)")

print("\nSZCZEGÓŁOWY ROZKŁAD KLASTRÓW ZAAKCEPTOWANYCH (TIER A & TIER B):")
acc_counts = Counter(x['label'] for x in accepted_orders)
for label, cnt in acc_counts.most_common():
    print(f"  - {label:65} : {cnt:3d} ({cnt/len(accepted_orders)*100:5.1f}% puli Tier A/B | {cnt/len(orders)*100:4.1f}% całej bazy)")
