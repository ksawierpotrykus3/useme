# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

with open('debug_my_offer.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

def extract_offer_data(soup, offer_id, offer_url):
    data = {
        "offer_id": offer_id,
        "offer_url": offer_url,
        "title": "",
        "category": "",
        "client": "",
        "budget": "",
        "copyright": "",
        "job_description": "",
        "our_price": "",
        "our_days": "",
        "our_proposal": ""
    }
    
    # Title
    title_el = soup.find('h2', class_='jobs-summary__title')
    if title_el:
        # Check all h2 with jobs-summary__title
        h2s = soup.find_all('h2', class_='jobs-summary__title')
        for h in h2s:
            t = h.get_text(strip=True)
            if t != "Zlecenie publiczne":
                data["title"] = t
                break
                
    # Breadcrumbs / Category
    bc = soup.select_one('.breadcrumbs, .breadcrumb, [class*="category"]')
    # Let's find category from text
    # In my_offer: "Programowanie i IT – Projekty IT"
    for el in soup.find_all(['span', 'p', 'div']):
        t = el.get_text(strip=True)
        if "Programowanie i IT" in t or "Serwisy internetowe" in t:
            data["category"] = t
            break

    # Client (Zleceniodawca)
    for dt in soup.find_all(lambda tag: tag.name in ['div', 'span', 'dt', 'strong', 'p'] and tag.get_text(strip=True) == 'Zleceniodawca'):
        nxt = dt.find_next_sibling()
        if nxt:
            data["client"] = nxt.get_text(strip=True)
            break
            
    # Budget
    for dt in soup.find_all(lambda tag: tag.name in ['div', 'span', 'dt', 'strong', 'p'] and tag.get_text(strip=True) == 'Budżet'):
        nxt = dt.find_next_sibling()
        if nxt:
            data["budget"] = nxt.get_text(strip=True)
            break
            
    # Copyright
    for dt in soup.find_all(lambda tag: tag.name in ['div', 'span', 'dt', 'strong', 'p'] and tag.get_text(strip=True) == 'Prawa autorskie'):
        nxt = dt.find_next_sibling()
        if nxt:
            data["copyright"] = nxt.get_text(strip=True)
            break

    # Opis zlecenia (Job description)
    # Usually between Opis heading and Twoja oferta heading
    for dt in soup.find_all(lambda tag: tag.name in ['div', 'span', 'dt', 'strong', 'p', 'h3'] and tag.get_text(strip=True) == 'Opis'):
        nxt = dt.find_next_sibling()
        if nxt:
            data["job_description"] = nxt.get_text('\n', strip=True)
            break

    # Twoja oferta section
    offer_h3 = soup.find(lambda tag: tag.name in ['h2', 'h3', 'h4'] and 'Twoja oferta' in tag.get_text(strip=True))
    if offer_h3:
        # container following offer_h3
        container = offer_h3.find_next_sibling('div') or offer_h3.parent
        # find Wycena
        for tag in container.find_all(True):
            if tag.get_text(strip=True) == 'Wycena':
                nxt = tag.find_next_sibling()
                if nxt:
                    data["our_price"] = nxt.get_text(strip=True)
            elif tag.get_text(strip=True) == 'Dni pracy':
                nxt = tag.find_next_sibling()
                if nxt:
                    data["our_days"] = nxt.get_text(strip=True)
            elif tag.get_text(strip=True) == 'Opis' and tag != dt:
                nxt = tag.find_next_sibling()
                if nxt and not data["our_proposal"]:
                    data["our_proposal"] = nxt.get_text('\n', strip=True)

    return data

result = extract_offer_data(soup, "2878817", "https://useme.com/pl/jobs/my-offer/2878817/")
import json
print(json.dumps(result, ensure_ascii=False, indent=2))
