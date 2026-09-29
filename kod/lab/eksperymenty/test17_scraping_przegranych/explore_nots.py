# -*- coding: utf-8 -*-
from browser_driver import BrowserDriver
from bs4 import BeautifulSoup
import json

with BrowserDriver(headless=False) as driver:
    page = driver.context.new_page()
    page.goto('https://useme.com/pl/notifications/nots/', timeout=30000)
    driver.dismiss_cookie_banner(page)
    page.wait_for_timeout(3000)
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    # check pagination
    all_links = soup.find_all('a')
    page_links = []
    job_links = []
    for a in all_links:
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if 'page=' in href or 'nots/' in href:
            page_links.append((text, href))
        if '/jobs/' in href:
            job_links.append((text, href))
            
    print("PAGE LINKS:")
    for text, href in page_links:
        print(f"  [{text}] -> {href}")
        
    print("\nJOB LINKS IN NOTIFICATIONS:")
    for text, href in job_links:
        print(f"  [{text}] -> {href}")

    # Inspect notifications list container
    print("\nNOTIFICATION CONTAINERS:")
    # look for items that have 'zostało zamknięte'
    for tag in soup.find_all(True):
        if 'zostało zamknięte' in tag.get_text():
            # find smallest containing element
            children_with_text = [c for c in tag.children if hasattr(c, 'get_text') and 'zostało zamknięte' in c.get_text()]
            if not children_with_text:
                print(f"Leaf tag: <{tag.name} class='{tag.get('class')}'> text: {tag.get_text(strip=True)}")
                # also print parent tag
                p = tag.parent
                print(f"  Parent: <{p.name} class='{p.get('class')}'>")
