import json
import re
from collections import Counter, defaultdict

def classify_client(job_desc, title, client_name, budget_str):
    text = (job_desc + " " + title).lower()
    
    # Signatures of different client personas:
    # 1. BIZNESMEN / WŁAŚCICIEL NIETECHNICZNY (Non-tech Business Owner)
    # Keywords: "firma", "klienci", "sprzedaż", "magazyn", "faktury", "ręcznie", "czas", "usprawnić", "pracownicy", "zlecenie dla firmy", "obsługa zamówień"
    # Tone: Focuses on business pain, manual work, mistakes, revenue, saving hours.
    
    # 2. PM / CTO / TECH LEAD (Agencja / Software House / Doświadczony Zleceniodawca)
    # Keywords: "stack", "repozytorium", "git", "api", "senior", "architektura", "framework", "endpointy", "dokumentacja", "docker", "postman", "figma z autolayoutem", "kod źródłowy"
    # Tone: Precise tech requirements, specific libraries, code quality, testing.
    
    # 3. E-COMMERCE / GROWTH MANAGER (Sklep internetowy / E-com brand)
    # Keywords: "sklep", "shopify", "prestashop", "woocommerce", "konwersja", "koszyk", "bramka płatności", "produkty", "feed produktowy", "cpc", "roas", "klarna", "baselinker", "idosell"
    # Tone: Fast execution, speed, sales, integrations with marketplaces.
    
    # 4. STARTUPOWIEC / POMYSŁODAWCA (Visionary / Early MVP Founder)
    # Keywords: "aplikacja", "platforma", "innowacyjny", "mvp", "portal", "użytkownicy", "start", "pomysł", "długofalowa współpraca", "rozwój projektu"
    # Tone: Long descriptions, ambitious vision, phased rollout, often undefined tech specs.
    
    # 5. ZADANIOWIEC / QUICK-FIX (Szybka naprawa / Małe zlecenie)
    # Keywords: "od zaraz", "na wczoraj", "szybka akcja", "błąd", "poprawka", "skrypt", "drobne zlecenie", "pilne", "naprawić"
    # Tone: Short, urgent, specific problem to fix right away.

    score_biz = sum(1 for w in ['magazyn', 'faktur', 'ręczn', 'reczn', 'pracownik', 'czasu', 'błęd', 'usprawni', 'proces', 'obsług', 'hurtown'] if w in text)
    score_tech = sum(1 for w in ['repozytorium', 'senior', 'architekt', 'framework', 'endpoint', 'postman', 'docker', 'cto', 'lead', 'clean code', 'pull request', 'swagger', 'laravel', 'vue', 'react', 'node'] if w in text)
    score_ecom = sum(1 for w in ['shopify', 'prestashop', 'woocommerce', 'idosell', 'baselinker', 'sklep', 'koszyk', 'klarna', 'feed', 'cenow'] if w in text)
    score_startup = sum(1 for w in ['mvp', 'startup', 'innowacyjn', 'platforma', 'portal', 'użytkownik', 'aplikacja mobilna', 'długofalow', 'faza'] if w in text)
    score_quickfix = sum(1 for w in ['szybka akcja', 'na wczoraj', 'od zaraz', 'piln', 'błąd', 'naprawa', 'poprawka', 'prosty skrypt'] if w in text)
    
    # Word count heuristic
    words = len(job_desc.split())
    if words < 40 and score_quickfix > 0:
        return 'TYP_E_QUICK_FIX'
        
    scores = {
        'TYP_A_BIZNESMEN_NIETECHNICZNY': score_biz,
        'TYP_B_TECH_LEAD_CTO_PM': score_tech,
        'TYP_C_ECOMMERCE_MANAGER': score_ecom,
        'TYP_D_STARTUPOWIEC_MVP': score_startup,
        'TYP_E_QUICK_FIX': score_quickfix
    }
    
    best_type = max(scores.items(), key=lambda x: x[1])
    if best_type[1] == 0:
        # Fallback by category or length
        if 'sklep' in text or 'shopify' in text or 'e-commerce' in text:
            return 'TYP_C_ECOMMERCE_MANAGER'
        elif 'aplikacj' in text or 'portal' in text:
            return 'TYP_D_STARTUPOWIEC_MVP'
        elif words < 50:
            return 'TYP_E_QUICK_FIX'
        else:
            return 'TYP_A_BIZNESMEN_NIETECHNICZNY'
            
    return best_type[0]

def classify_tech(job_desc, title):
    text = (job_desc + " " + title).lower()
    if any(k in text for k in ['subiekt', 'enova', 'optima', 'erp', 'sfera', 'topsolid', 'cad', 'cam', 'wf-mag', 'symfonia', 'comarch']):
        return 'TECH_1_ERP_CAD_SYSTEMY'
    elif any(k in text for k in ['bot', 'skrypt', 'scraping', 'crawler', 'scraper', 'make', 'n8n', 'zapier', 'selenium', 'playwright', 'automatyzacj', 'iptv', 'voip']):
        return 'TECH_2_AUTOMATYZACJE_BOTY_SCRAPING'
    elif any(k in text for k in ['shopify', 'prestashop', 'woocommerce', 'wordpress', 'idosell', 'magento', 'framer', 'webflow', 'sklep']):
        return 'TECH_3_ECOMMERCE_CMS'
    elif any(k in text for k in ['flutter', 'react native', 'kotlin', 'swift', 'ios', 'android', 'mobilna']):
        return 'TECH_4_MOBILE_APPS'
    elif any(k in text for k in ['laravel', 'django', 'fastapi', 'node', 'react', 'vue', 'angular', 'next.js', 'mvp', 'saas', 'webowa']):
        return 'TECH_5_WEB_APPS_SAAS'
    else:
        return 'TECH_6_LEGACY_INNE'

def main():
    base = 'badania/baza/ksawierpotrykus3'
    with open(f'{base}/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
        przegrane = json.load(f)
    with open(f'{base}/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
        wygrane = json.load(f)
        
    records = []
    for x in wygrane:
        c_type = classify_client(x.get('job_description', ''), x.get('title', ''), x.get('client', ''), x.get('budget', ''))
        t_type = classify_tech(x.get('job_description', ''), x.get('title', ''))
        records.append({
            'status': 'wygrana',
            'id': x.get('job_id') or x.get('offer_id'),
            'title': x.get('title', ''),
            'client_type': c_type,
            'tech_type': t_type,
            'price': x.get('our_price'),
            'thread_size': x.get('thread_size', 0)
        })
        
    for x in przegrane:
        c_type = classify_client(x.get('job_description', ''), x.get('title', ''), x.get('client', ''), x.get('budget', ''))
        t_type = classify_tech(x.get('job_description', ''), x.get('title', ''))
        records.append({
            'status': 'przegrana',
            'id': x.get('offer_id'),
            'title': x.get('title', ''),
            'client_type': c_type,
            'tech_type': t_type,
            'price': x.get('our_price'),
            'thread_size': 0
        })

    # 2D Matrix: Client Type x Tech Type
    matrix = defaultdict(lambda: {'wygrana': 0, 'przegrana': 0, 'total': 0})
    client_totals = defaultdict(lambda: {'wygrana': 0, 'przegrana': 0, 'total': 0})
    tech_totals = defaultdict(lambda: {'wygrana': 0, 'przegrana': 0, 'total': 0})
    
    for r in records:
        ct = r['client_type']
        tt = r['tech_type']
        st = r['status']
        matrix[(ct, tt)][st] += 1
        matrix[(ct, tt)]['total'] += 1
        client_totals[ct][st] += 1
        client_totals[ct]['total'] += 1
        tech_totals[tt][st] += 1
        tech_totals[tt]['total'] += 1
        
    print("="*80)
    print("TYPOLOGIA ZLECENIODAWCÓW (Podsumowanie 470 zleceń):")
    print("="*80)
    for ct, vals in sorted(client_totals.items(), key=lambda x: x[1]['total'], reverse=True):
        win_rate = (vals['wygrana'] / vals['total'] * 100) if vals['total'] > 0 else 0
        print(f"{ct:<30} | Razem: {vals['total']:<4} | Wygrane: {vals['wygrana']:<3} | Przegrane: {vals['przegrana']:<3} | Win Rate: {win_rate:.1f}%")

    print("\n" + "="*80)
    print("ARCHETYPY TECHNOLOGICZNE (Podsumowanie 470 zleceń):")
    print("="*80)
    for tt, vals in sorted(tech_totals.items(), key=lambda x: x[1]['total'], reverse=True):
        win_rate = (vals['wygrana'] / vals['total'] * 100) if vals['total'] > 0 else 0
        print(f"{tt:<32} | Razem: {vals['total']:<4} | Wygrane: {vals['wygrana']:<3} | Przegrane: {vals['przegrana']:<3} | Win Rate: {win_rate:.1f}%")

    # Serialize results
    out = {
        'client_totals': dict(client_totals),
        'tech_totals': dict(tech_totals),
        'matrix_2d': {f"{k[0]}__x__{k[1]}": v for k, v in matrix.items()},
        'records_sample': records[:30]
    }
    with open('badania/analizy/02_matryca_2d_klient_x_tech.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nZapisano macierz 2D do: badania/analizy/02_matryca_2d_klient_x_tech.json")

if __name__ == '__main__':
    main()
