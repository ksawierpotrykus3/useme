# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json
import re

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_strony_ofert.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

offers = soup.select('.dashboard-list__item-offer')
print(f"Liczba kart ofert (dashboard-list__item-offer): {len(offers)}")

for i, off in enumerate(offers):
    print(f"\n==================== OFERTA #{i+1} ====================")
    
    # Wykonawca
    # link z nazwą wykonawcy lub avatarem
    author_a = off.select_one('a[href*=\"/roles/contractor/\"]')
    author_url = author_a.get('href') if author_a else None
    
    # Nazwa wykonawcy - szukajmy w nagłówku
    name_el = off.select_one('.dashboard-list__item-title, h3, h4, strong')
    # lub sprawdźmy tekst linku lub sąsiada
    author_name = None
    contract_count = None
    
    # Przejrzyjmy wszystkie linki
    for a in off.find_all('a'):
        href = a.get('href', '')
        if '/roles/contractor/' in href:
            author_url = href
            txt = a.get_text(strip=True)
            if txt and txt != 'Zobacz profil':
                author_name = txt
    
    # Jeśli author_name to dalej None, wyciągnijmy z nagłówka
    header_div = off.select_one('.dashboard-list__item-header, .media-body, .dashboard-list__item-content')
    
    # Szukamy liczby umów
    contracts_m = re.search(r'(\d+)\s+um[óo]w', off.get_text())
    contracts = contracts_m.group(0) if contracts_m else "0 umów"
    
    # Szukamy ceny
    price_el = off.select_one('.dashboard-list__item-stats-prop--green, [class*=\"stats-prop--green\"]')
    price = price_el.get_text(strip=True) if price_el else None
    
    # Szukamy dni
    stats_props = off.select('.dashboard-list__item-stats-prop')
    days = None
    for sp in stats_props:
        txt = sp.get_text(strip=True)
        if 'dni' in txt.lower():
            days = txt
        elif not price and 'pln' in txt.lower():
            price = txt
            
    # Treść oferty
    # Wyciągnijmy tekst z bloku treści
    # Sprawdźmy czy jest dedykowany kontener treści
    desc_el = off.select_one('.dashboard-list__item-description, .offer-description, .dashboard-list__item-body')
    if desc_el:
        content = desc_el.get_text('\n', strip=True)
    else:
        # wyciągamy paragrafy
        paras = [p.get_text(strip=True) for p in off.find_all('p') if p.get_text(strip=True)]
        content = '\n\n'.join(paras)
        
    print(f"Wykonawca: {author_name} | Profil: {author_url} | Umowy: {contracts}")
    print(f"Cena: {price} | Czas: {days}")
    print(f"Treść (pierwsze 300 znaków):\n{content[:300]}...")
