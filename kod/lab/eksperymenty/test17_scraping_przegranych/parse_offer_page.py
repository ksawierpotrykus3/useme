# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

with open('debug_my_offer.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("--- TEXT SECTIONS ---")
# find all elements with 'Twoja oferta'
for h in soup.find_all(True):
    if h.string and 'Twoja oferta' in h.string:
        print("Found:", h.name, h.get('class'))
        parent = h.find_parent('div')
        if parent:
            print("Parent text:")
            print(parent.get_text('\n', strip=True)[:1500])
            break

# Also find job title and job description / details
print("\n--- JOB DETAILS ---")
links_to_job = soup.select('a[href*="/jobs/"]')
for a in links_to_job:
    print("Job link:", a.get('href'), a.get_text(strip=True))

# Let's search for price / days
print("\n--- PRICE / TIME / FIELDS ---")
for dt in soup.find_all(['dt', 'th', 'span', 'p']):
    t = dt.get_text(strip=True)
    if any(k in t.lower() for k in ['wartość', 'stawka', 'kwota', 'netto', 'termin', 'czas realizacji', 'status']):
        # print parent or next sibling
        nxt = dt.find_next_sibling()
        nxt_text = nxt.get_text(strip=True) if nxt else ''
        print(f"{t} => {nxt_text}")
