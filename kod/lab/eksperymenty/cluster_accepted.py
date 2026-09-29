# -*- coding: utf-8 -*-
"""
Klastrowanie 409 zaakceptowanych zleceń Useme (Tier A i Tier B).
"""
import sys
import re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from full_classification import acc_list, parse_budget

print(f"Liczba zaakceptowanych zleceń do klastrowania: {len(acc_list)}")

def assign_cluster(o):
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + " " + d
    cat = o['cat'].lower()

    # Sprawdzamy poszczególne klastry w logicznej kolejności inżynierskiej:

    # 1. MOBILE (React Native, Flutter, iOS, Android, Swift, Kotlin)
    # Zlecenia natywne lub cross-platform na urządzenia mobilne
    if ('aplikacje mobilne' in cat) or any(k in t for k in [
        'aplikacja mobilna', 'aplikacji mobilnej', 'aplikację mobilną',
        'react native', 'flutter', 'ios', 'android', 'swift', 'swiftui', 'kotlin'
    ]) or (any(k in full for k in ['react native', 'flutter', 'swiftui', 'kotlin multiplatform']) and 'mobiln' in full):
        return "CLUSTER_MOBILE", "Aplikacje Mobilne (React Native / Flutter / iOS / Android)"

    # 2. CLOUD, DEVOPS & INFRASTRUKTURA (Linux, Docker, VPS, Serwery, CI/CD, Kubernetes)
    if ('administracja serwerami' in cat) or any(k in t for k in [
        'administracja serwerem', 'konfiguracja serwera', 'wdrożeniowca do serwera',
        'devops', 'docker', 'kubernetes', 'vps', 'linux', 'ci/cd', 'serwer', 'hosting',
        'migracja serwera', 'migracja poczty', 'chmurowej', 'chmura', 'aws', 'cloudflare setup'
    ]) or (any(k in full for k in ['docker-compose', 'kubernetes', 'nginx', 'traefik', 'proxmox', 'hetzner', 'ovh']) and any(k in t for k in ['serwer', 'wdrożenie', 'instalacja'])):
        return "CLUSTER_CLOUD_DEVOPS", "Cloud, DevOps & Administracja Serwerami (Linux / Docker / VPS)"

    # 3. KONFIGURATORY 3D, WEBGL & CAD/CAM/CNC
    if any(k in full for k in ['three.js', 'webgl', '3d', 'cad', 'cnc', 'topsolid', 'babylon', 'dxf', 'g-code']) and any(k in t for k in ['konfigurator', '3d', 'mebli', 'ar', 'kadrowanie']):
        return "CLUSTER_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"
    if any(k in t for k in ['konfigurator 3d', 'konfiguratora 3d', 'konfigurator']):
        return "CLUSTER_3D_CAD", "Konfiguratory 3D, WebGL & CAD/CAM/CNC"

    # 4. SCRAPING, WEB CRAWLING & WAF BYPASS
    if any(k in t for k in ['scraping', 'scraper', 'bot do wyszukiwania', 'crawling', 'crawler', 'pobieranie danych', 'monitoring cen', 'otomoto na allegro', 'badanie rynku']):
        if any(k in full for k in ['scraper', 'scraping', 'otomoto', 'olx', 'allegro', 'playwright', 'selenium', 'curl_cffi', 'skrypt']):
            return "CLUSTER_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"
    if any(k in full for k in ['playwright', 'puppeteer', 'selenium', 'anti-captcha', 'cloudflare bypass', 'scraping']) and any(k in t for k in ['bot', 'skrypt', 'pobieranie', 'danych']):
        return "CLUSTER_SCRAPING", "Scraping, Web Crawling & WAF Bypass (Boty Danych)"

    # 5. BAZY DANYCH, BIGQUERY, SQL & ANALITYKA DANYCH
    if any(k in t for k in ['bigquery', 'baza danych', 'bazy danych', 'sql server', 'postgresql', 'mysql', 'hurtownia danych', 'optymalizacja zapytań', 'etl']) or ('bigquery' in full and 'api' in t):
        return "CLUSTER_DATABASES", "Bazy Danych, SQL, BigQuery & Data Engineering"

    # 6. AI, AGENCI LLM, OCR DOKUMENTÓW & RAG
    if any(k in t for k in ['ai', 'llm', 'ocr', 'rag', 'gpt', 'openai', 'gemini', 'bielik', 'voicebot', 'chatbot', 'mistral', 'asystent ai', 'agent ai']):
        return "CLUSTER_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"
    if any(k in full for k in ['ocr', 'langchain', 'llamaindex', 'qlora', 'fine-tuning', 'ksef']) and any(k in t for k in ['faktur', 'dokument', 'automatyzacj', 'ksef']):
        return "CLUSTER_AI_LLM", "AI, Agenci LLM, OCR Dokumentów & RAG"

    # 7. AUTOMATYZACJE N8N / MAKE / WORKFLOW (Automatyzacje procesowe bez twardego LLM OCR)
    if any(k in t for k in ['n8n', 'make', 'make.com', 'zapier', 'automatyzacja procesów', 'automatyzacja testu', 'automatyzacje']):
        return "CLUSTER_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"
    if any(k in full for k in ['n8n', 'make.com', 'zapier']) and any(k in t for k in ['integracja', 'automatyzacja', 'obieg']):
        return "CLUSTER_AUTOMATION_N8N", "Automatyzacje Procesów (n8n / Make / Workflow / Zapier)"

    # 8. SYSTEMY REZERWACJI, BOOKING & CONCURRENCY
    if any(k in t for k in ['rezerwacj', 'booking', 'najmem', 'terminarz', 'wizyt', 'kalendarz']) or ('system rezerwacji' in full):
        return "CLUSTER_RESERVATION", "Systemy Rezerwacji, Booking & Concurrency"

    # 9. INTEGRACJE API & MARKETPLACE SYNC (BaseLinker, ERP, Allegro, Subiekt, Comarch, Webhooks)
    if any(k in t for k in [
        'baselinker', 'subiekt', 'enova', 'comarch', 'symfonia', 'sap', 'erp',
        'allegro', 'apilo', 'sellasist', 'marketplace', 'integracja api', 'połączenie salesforce',
        'synchronizacja sklepu', 'synchronizacj', 'wymiany danych', 'api b2b', 'feed'
    ]) or any(k in full for k in ['baselinker', 'subiekt gt', 'subiekt nexo', 'enova365', 'comarch opty']) and any(k in t for k in ['integracja', 'synchronizacja', 'wdrożenie']):
        return "CLUSTER_API_SYNC", "Integracje API, Marketplace & ERP Sync (BaseLinker / Subiekt / Enova)"

    # 10. E-COMMERCE ZAAWANSOWANY, B2B & PLATFORMY HURTOWE (IdoSell B2B, Shopify Plus/B2B, PrestaShop B2B, Magento)
    if any(k in t for k in [
        'idosell', 'b2b', 'shopify', 'prestashop', 'magento', 'shoper', 'woocommerce', 'sklep'
    ]) or any(k in cat for k in ['sklepy internetowe']):
        return "CLUSTER_ECOMMERCE_ADVANCED", "E-commerce Zaawansowany, B2B & Dedykowane Sklepy (IdoSell/Shopify/Presta)"

    # 11. ENTERPRISE CRM, SAAS & DEDYKOWANE PLATFORMY WEBOWE (React, Next.js, Node, Laravel, Python, FastAPI)
    if any(k in t for k in [
        'saas', 'crm', 'platformy webowej', 'platforma webowa', 'aplikacja webowa', 'portal',
        'systemu obsługi', 'system dla', 'aplikacji', 'full-stack', 'full stack', 'backend',
        'laravel', 'react', 'next.js', 'vue', 'django', 'fastapi', 'node'
    ]) or any(k in cat for k in ['aplikacje webowe', 'projekty it', 'oprogramowanie']):
        return "CLUSTER_CRM_SAAS_WEB", "Enterprise CRM, SaaS & Dedykowane Web Apps (React/Next/Node/Laravel)"

    return "CLUSTER_OTHER", "Inne zlecenia specjalistyczne"

# Klastrowanie
cluster_results = []
for o in acc_list:
    c_code, c_name = assign_cluster(o)
    cluster_results.append((o, c_code, c_name))

c_dist = Counter(x[2] for x in cluster_results)
print("="*60)
print("WYNIK KLASTROWANIA ZAAKCEPTOWANYCH ZLECEŃ:")
print("="*60)
for name, cnt in c_dist.most_common():
    print(f"{name:70} : {cnt:3d} ({cnt/len(acc_list)*100:5.1f}%)")

others = [x for x in cluster_results if x[1] == "CLUSTER_OTHER"]
print(f"\nLiczba zleceń w 'Inne specjalistyczne' (CLUSTER_OTHER): {len(others)}")
for o, c, n in others:
    print(f"  - #{o['id']} | {o['title']} ({o['cat']})")
