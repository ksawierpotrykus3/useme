# -*- coding: utf-8 -*-
from browser_driver import BrowserDriver
from bs4 import BeautifulSoup
import time

urls = [
    "https://useme.com/pl/notifications/nots/",
    "https://useme.com/pl/notifications/nots/?page=2",
    "https://useme.com/pl/notifications/nots/?page=3"
]

all_offers = []

with BrowserDriver(headless=False) as driver:
    page = driver.context.new_page()
    for p_idx, url in enumerate(urls, 1):
        print(f"Loading page {p_idx}: {url}...")
        page.goto(url, timeout=30000)
        driver.dismiss_cookie_banner(page)
        page.wait_for_timeout(2500)
        
        soup = BeautifulSoup(page.content(), 'html.parser')
        links = soup.find_all('a')
        
        page_offers = []
        for a in links:
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if '/jobs/my-offer/' in href:
                page_offers.append((text, href))
                
        print(f"  Page {p_idx}: found {len(page_offers)} offer links.")
        for title, href in page_offers:
            print(f"    - {title} -> {href}")
            all_offers.append({"page": p_idx, "title": title, "href": href})
            
print(f"\nTotal offer links across 3 pages: {len(all_offers)}")
