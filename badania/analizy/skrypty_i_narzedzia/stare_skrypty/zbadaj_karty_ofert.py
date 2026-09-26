# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_strony_ofert.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Szukamy listy elementów ofert (np. .dashboard-list__item)
items = soup.select('.dashboard-list__item, [class*=\"dashboard-list__item\"]')
print(f"Liczba elementów dashboard-list__item: {len(items)}")

if items:
    sample = items[0]
    print("Klasy sample:", sample.get('class'))
    print("ID sample:", sample.get('id'))
    print("\nTekst sample:\n", sample.get_text(separator=' | ', strip=True)[:500])

# Zbadajmy strukturę jednej pełnej karty
for i, it in enumerate(items[:3]):
    print(f"\n--- ELEMENT {i} ---")
    # szukajmy linku wykonawcy
    a_author = it.select_one('a[href*=\"/roles/contractor/\"]')
    author = a_author.get_text(strip=True) if a_author else "Brak autora"
    author_href = a_author.get('href') if a_author else "Brak href"
    
    # szukajmy kwoty
    price_el = it.select_one('.dashboard-list__item-stats-prop--green, [class*=\"stats-prop--green\"], [class*=\"price\"]')
    price = price_el.get_text(strip=True) if price_el else "Brak ceny"
    
    # szukajmy dni
    days_el = it.select_one('.dashboard-list__item-stats-prop, [class*=\"stats-prop\"]')
    
    # treść oferty
    # zobaczmy jakie divy/p są wewnątrz
    paragraphs = [p.get_text(strip=True) for p in it.find_all(['p', 'div']) if len(p.get_text(strip=True)) > 40]
    
    print(f"Wykonawca: {author} ({author_href})")
    print(f"Cena: {price}")
    print(f"Długość tekstu: {sum(len(p) for p in paragraphs)} znaków")
    print("Początek oferty:", paragraphs[0][:150] if paragraphs else "Brak akapitów")
