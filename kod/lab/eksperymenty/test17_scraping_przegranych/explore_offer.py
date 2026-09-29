# -*- coding: utf-8 -*-
from browser_driver import BrowserDriver
from bs4 import BeautifulSoup
import json

with BrowserDriver(headless=False) as driver:
    page = driver.context.new_page()
    url = "https://useme.com/pl/jobs/my-offer/2878817/"
    page.goto(url, timeout=30000)
    driver.dismiss_cookie_banner(page)
    page.wait_for_timeout(3000)
    print("URL:", page.url)
    print("Title:", page.title())
    
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Save html to debug to inspect
    with open("debug_my_offer.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Page length:", len(html))
    # Let's find main headings, job title, offer details, status
    h1 = soup.find('h1')
    if h1:
        print("H1:", h1.get_text(strip=True))
    
    # Let's print interesting texts
    for h2 in soup.find_all(['h2', 'h3', 'h4', 'strong', 'b']):
        t = h2.get_text(strip=True)
        if any(w in t.lower() for w in ['oferta', 'status', 'cena', 'netto', 'brutto', 'termin', 'dni', 'zamknięt', 'odrzucon', 'wybran']):
            print(f"[{h2.name}]: {t}")
