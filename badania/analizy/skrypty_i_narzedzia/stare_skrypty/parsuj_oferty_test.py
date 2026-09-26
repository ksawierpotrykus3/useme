# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_strony_ofert.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Tytuł strony:", soup.title.string.strip() if soup.title else "Brak")

# Szukamy głównych kontenerów ofert
# Sprawdźmy wszystkie linki do ofert lub wykonawców
contractor_links = soup.find_all('a', href=re.compile(r'/roles/contractor/|/user/|/contractor/'))
print(f"Znaleziono linków do wykonawców: {len(contractor_links)}")

# Zobaczmy unikalnych wykonawców
contractors = set()
for a in contractor_links:
    href = a.get('href')
    text = a.get_text(strip=True)
    if text and href:
        contractors.add((text, href))

print(f"Unikalnych wykonawców: {len(contractors)}")
for name, href in sorted(contractors)[:10]:
    print(f" - {name} ({href})")

# Sprawdźmy paginację
pagination = soup.find_all(['ul', 'nav', 'div'], class_=re.compile(r'paginat', re.I))
print(f"Kontenery paginacji: {len(pagination)}")
if pagination:
    for p in pagination:
        print("Paginacja tekst:", p.get_text(strip=True))
        for a in p.find_all('a'):
            print("  Link paginacji:", a.get('href'), a.get_text(strip=True))

# Wypiszmy struktury kart ofert
# Poszukajmy bloków z cenami (PLN / zł)
price_nodes = soup.find_all(text=re.compile(r'\d+\s*(?:PLN|zł)', re.I))
print(f"Znaleziono wystąpień cen: {len(price_nodes)}")
for p in price_nodes[:10]:
    parent = p.parent
    print(f"Cena: '{p.strip()}' w tagu <{parent.name}> class='{parent.get('class')}'")
