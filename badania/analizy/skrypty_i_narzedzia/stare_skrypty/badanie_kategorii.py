# -*- coding: utf-8 -*-
import json
import re
from curl_cffi import requests
from bs4 import BeautifulSoup

def main():
    print("Pobieram https://useme.com/pl/jobs/...")
    r = requests.get('https://useme.com/pl/jobs/', impersonate='chrome120', timeout=20)
    print(f"Status: {r.status_code}, wielkosc: {len(r.text)} bajtow")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 1. Sprawdz kategorie w menu / filtrach / blokach
    cats = {}
    for a in soup.select('a[href*="/jobs/category/"], a[href*="/jobs/subcategories/"]'):
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if href and text:
            full_url = "https://useme.com" + href if href.startswith('/') else href
            cats[full_url] = text
            
    print(f"\nZnaleziono {len(cats)} linkow do kategorii/podkategorii:")
    for url, name in sorted(cats.items(), key=lambda x: x[1]):
        print(f" - {name}: {url}")

    # Zapiszmy do JSON
    with open("badania/rynek/kategorie_useme.json", "w", encoding="utf-8") as f:
        json.dump([{"name": v, "url": k} for k, v in cats.items()], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
