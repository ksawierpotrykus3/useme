# -*- coding: utf-8 -*-
"""
Klastrowanie 369 zaakceptowanych zleceń.
"""
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
import re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from audit_strict_red import acc_strict, orders

print(f"Liczba zaakceptowanych zleceń: {len(acc_strict)}")

def assign_cluster_369(o):
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + " " + d
    cat = o['cat'].lower()

    # 1. MOBILE (React Native, Flutter, Swift, Kotlin, iOS, Android)
    if ('aplikacje mobilne' in cat) or any(k in t for k in [
        'aplikacja mobilna', 'aplikacji mobilnej', 'aplikację mobilną',
        'react native', 'flutter', 'ios', 'android', 'swift', 'swiftui', 'kotlin', 'gra mobilna'
    ]) or (any(k in full for k in ['react native', 'flutter', 'swiftui', 'kotlin multiplatform']) and 'mobiln' in full):
        return "K1_MOBILE", "Aplikacje Mobilne (React Native / Flutter / iOS / Android)"

    # 2. CLOUD, DEVOPS & ADMINISTRACJA SERWERAMI (Linux, Docker, VPS, Serwery, CI/CD, KVM, Cloudflare)
    if ('administracja serwerami' in cat) or any(k in t for k in [
        'administracja serwerem', 'konfiguracja serwera', 'wdrożeniowca do serwera',
        'devops', 'docker', 'kubernetes', 'vps', 'linux', 'ci/cd', 'serwer', 'hosting',
        'migracja serwera', 'migracja poczty', 'chmurowej', 'chmura', 'aws', 'atlassian cloud',
        'sharepoint', 'forensic dysku systemowego windows (serwer)'
    ]) or any(k in full for k in ['docker-compose', 'kubernetes', 'vps kvm', 'proxmox']) and any(k in t for k in ['serwer', 'wdrożenie', 'instalacja', 'konfiguracja']):
        return "K2_CLOUD_DEVOPS", "Cloud, DevOps & Administracja Serwerami (Linux / Docker / VPS)"

    # 3. KONFIGURATORY 3D, WEBGL & CAD/CAM/CNC
    if any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid', 'babylon', 'dxf', 'g-code']) and any(k in t for k in ['konfigurator', '3d', 'mebli', 'ar', 'kadrowanie', 'fototapet']):
        return "K3_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"
    if any(k in t for k in ['konfigurator 3d', 'konfiguratora 3d', 'konfigurator']):
        return "K3_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"

    # 4. SCRAPING, WEB CRAWLING & WAF BYPASS (Boty Danych, monitoring)
    if any(k in t for k in ['scraping', 'scraper', 'bot do wyszukiwania', 'crawling', 'crawler', 'pobieranie danych', 'monitoring cen', 'otomoto na allegro', 'badanie rynku']):
        return "K4_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"
    if any(k in full for k in ['playwright', 'puppeteer', 'selenium', 'anti-captcha', 'cloudflare bypass', 'scraping']) and any(k in t for k in ['bot', 'skrypt', 'pobieranie', 'danych']):
        return "K4_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"

    # 5. BAZY DANYCH, BIGQUERY, SQL & DATA ENGINEERING
    if any(k in t for k in ['bigquery', 'baza danych', 'bazy danych', 'sql server', 'postgresql', 'mysql', 'mariadb', 'hurtownia danych', 'optymalizacja zapytań', 'etl']) or ('bigquery' in full and 'api' in t):
        return "K5_DATABASES", "Bazy Danych, SQL, BigQuery & Data Engineering"

    # 6. AI, AGENCI LLM, OCR DOKUMENTÓW & RAG
    if any(k in t for k in ['ai', 'llm', 'ocr', 'rag', 'gpt', 'openai', 'gemini', 'bielik', 'voicebot', 'chatbot', 'mistral', 'asystent ai', 'agent ai']):
        return "K6_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"
    if any(k in full for k in ['ocr', 'langchain', 'llamaindex', 'qlora', 'fine-tuning', 'ksef']) and any(k in t for k in ['faktur', 'dokument', 'automatyzacj', 'ksef']):
        return "K6_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"

    # 7. AUTOMATYZACJE PROCESÓW (n8n / Make / Zapier / Workflow)
    if any(k in t for k in ['n8n', 'make', 'make.com', 'zapier', 'automatyzacja procesów', 'automatyzacja testu', 'automatyzacja']) or ('moodle — konfiguracja i automatyzacja' in t):
        return "K7_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"
    if any(k in full for k in ['n8n', 'make.com', 'zapier']) and any(k in t for k in ['integracja', 'automatyzacja', 'obieg']):
        return "K7_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"

    # 8. SYSTEMY REZERWACJI, BOOKING & CONCURRENCY
    if any(k in t for k in ['rezerwacj', 'booking', 'najmem', 'terminarz', 'wizyt', 'kalendarz']) or ('system rezerwacji' in full):
        return "K8_RESERVATION", "Systemy Rezerwacji, Booking & Concurrency"

    # 9. INTEGRACJE API, MARKETPLACE & ERP SYNC (BaseLinker / Subiekt / Enova / SAP)
    if any(k in t for k in [
        'baselinker', 'subiekt', 'enova', 'comarch', 'symfonia', 'sap', 'erp', 'wapro',
        'allegro', 'apilo', 'sellasist', 'marketplace', 'integracja api', 'połączenie salesforce',
        'synchronizacja sklepu', 'synchronizacj', 'wymiany danych', 'api b2b', 'feed'
    ]) or (any(k in full for k in ['baselinker', 'subiekt gt', 'subiekt nexo', 'enova365', 'comarch opty']) and any(k in t for k in ['integracja', 'synchronizacja', 'wdrożenie'])):
        return "K9_API_SYNC", "Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova)"

    # 10. E-COMMERCE ZAAWANSOWANY, B2B & DEDYKOWANE SKLEPY (IdoSell B2B, Shopify Plus, PrestaShop B2B, Magento)
    if any(k in t for k in [
        'idosell', 'b2b', 'shopify', 'prestashop', 'magento', 'shoper', 'woocommerce', 'sklep', 'e-commerce developer'
    ]) or any(k in cat for k in ['sklepy internetowe']):
        return "K10_ECOMMERCE_ADVANCED", "E-commerce Zaawansowany, B2B & Dedykowane Sklepy (IdoSell/Shopify/Presta)"

    # 11. ENTERPRISE CRM, SAAS & DEDYKOWANE WEB APPS (React, Next.js, Node, Laravel, Python, FastAPI)
    return "K11_CRM_SAAS_WEB", "Enterprise CRM, SaaS & Dedykowane Web Apps (React/Next/Node/Laravel)"

results_369 = []
for o in acc_strict:
    code, label = assign_cluster_369(o)
    results_369.append({
        'order': o,
        'code': code,
        'label': label
    })

counts_369 = Counter(x['label'] for x in results_369)
print("="*70)
print("WYNIK KLASTROWANIA 369 ZAAKCEPTOWANYCH ZLECEŃ:")
print("="*70)
for label, cnt in counts_369.most_common():
    print(f"{label:65} : {cnt:3d} ({cnt/len(acc_strict)*100:5.1f}% puli Tier A/B | {cnt/len(orders)*100:4.1f}% całej bazy)")
