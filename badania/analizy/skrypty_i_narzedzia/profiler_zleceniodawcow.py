import json
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
    przegrane = json.load(f)
with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
    wygrane = json.load(f)

all_jobs = []
for x in wygrane: all_jobs.append((x, True))
for x in przegrane: all_jobs.append((x, False))

print(f"Łącznie zleceń do zbadania: {len(all_jobs)}")

# Let's inspect features of the job descriptions:
features = []
for job, won in all_jobs:
    title = job.get('title') or ''
    desc = job.get('job_description') or ''
    client = job.get('client') or ''
    budget = job.get('budget') or ''
    contracts = job.get('client_contracts') or 'Nieznane'
    category = job.get('category') or ''
    
    text = (title + "\n" + desc).strip()
    words = len(text.split())
    lines = [l.strip() for l in desc.splitlines() if l.strip()]
    
    # 1. Format/Style:
    has_bullets = any(l.startswith(('-', '*', '•', '1.', '2.', '3.')) for l in lines)
    has_headers = any(l.startswith(('#', '==', '--')) or l.endswith(':') for l in lines)
    is_english = any(w in text.lower() for w in ['the ', 'we are', 'looking for', 'project', 'description', 'requirements'])
    
    # 2. Level of detail:
    if words < 35:
        detail_level = 'MINIMAL_TELEGRAPHIC' # 1-2 zdania
    elif words < 120:
        detail_level = 'SHORT_CONCRETE'
    elif words < 300:
        detail_level = 'STANDARD_SPEC'
    else:
        detail_level = 'EXHAUSTIVE_RFP' # długi elaborat / RFP
        
    # 3. Agency / Outsourcing signals:
    is_agency_subcontract = any(k in text.lower() for k in [
        'dla naszego klienta', 'dla klienta', 'nasz klient', 'software house', 'agencja',
        'podwykonawc', 'dołączenie do zespołu', 'dla zespołu', 'poszukujemy programisty do zespołu',
        'wsparcie zespołu', 'b2b', 'zlecenie stałe', 'rozliczenie godzinowe'
    ])
    
    # 4. E-commerce / Shop owner signals:
    is_ecommerce = any(k in text.lower() for k in [
        'sklep', 'shopify', 'prestashop', 'woocommerce', 'shoper', 'idosell', 'magento',
        'baselinker', 'koszyk', 'produkty', 'zamówień', 'zamowien', 'hurtown'
    ])
    
    # 5. Non-tech Traditional SME / B2B firm signals:
    is_traditional_sme = any(k in text.lower() for k in [
        'firma', 'magazyn', 'faktur', 'biuro', 'produkcja', 'obsługa klienta', 'pracownik',
        'nieruchomości', 'księgow', 'transport', 'hotel', 'gastronom', 'gabinet', 'dział handlowy'
    ])
    
    # 6. Startup / MVP Founder signals:
    is_startup_mvp = any(k in text.lower() for k in [
        'mvp', 'portal', 'platforma', 'aplikacja', 'użytkownik', 'startup', 'innowacyjny',
        'monetyzacja', 'pomysł', 'rozwój aplikacji', 'społecznościow'
    ])
    
    # 7. Hobby / Solo user / Gaming / Personal task:
    is_hobby_personal = any(k in text.lower() for k in [
        'gra', 'grze', 'bot do gry', 'pokewars', 'gangsters', 'prywatn', 'hobbystyczn', 'dla siebie'
    ])

    features.append({
        'won': won,
        'title': title,
        'words': words,
        'detail_level': detail_level,
        'has_bullets': has_bullets,
        'is_english': is_english,
        'is_agency_subcontract': is_agency_subcontract,
        'is_ecommerce': is_ecommerce,
        'is_traditional_sme': is_traditional_sme,
        'is_startup_mvp': is_startup_mvp,
        'is_hobby_personal': is_hobby_personal,
        'budget': budget,
        'category': category,
        'client': client
    })

print("="*80)
print("ROZKŁAD CECH STYLISTYCZNYCH I PROFILOWYCH (470 ZLECEŃ):")
print("="*80)

def stat_check(name, cond):
    total = sum(1 for f in features if cond(f))
    wins = sum(1 for f in features if cond(f) and f['won'])
    wr = (wins / total * 100) if total > 0 else 0
    print(f"{name:<40} | Total: {total:<4} | Wins: {wins:<3} | Win Rate: {wr:.1f}%")

stat_check("Długość: MINIMAL (1-2 zdania, <35 słów)", lambda f: f['detail_level'] == 'MINIMAL_TELEGRAPHIC')
stat_check("Długość: KRÓTKA (35-120 słów)", lambda f: f['detail_level'] == 'SHORT_CONCRETE')
stat_check("Długość: STANDARD (120-300 słów)", lambda f: f['detail_level'] == 'STANDARD_SPEC')
stat_check("Długość: BARDZO DŁUGA / RFP (>300 słów)", lambda f: f['detail_level'] == 'EXHAUSTIVE_RFP')
print("-" * 75)
stat_check("Struktura: Wypunktowania (bullet points)", lambda f: f['has_bullets'])
stat_check("Język: Angielski", lambda f: f['is_english'])
print("-" * 75)
stat_check("Persona: Podwykonawstwo / Agencja / Software House", lambda f: f['is_agency_subcontract'])
stat_check("Persona: E-commerce / Sklep online", lambda f: f['is_ecommerce'])
stat_check("Persona: Tradycyjne MŚP / Firma usługowo-produkcyjna", lambda f: f['is_traditional_sme'])
stat_check("Persona: Startupowiec / MVP Nowego Portalu", lambda f: f['is_startup_mvp'])
stat_check("Persona: Hobbysta / Gracz / Zlecenie Osobiste", lambda f: f['is_hobby_personal'])
