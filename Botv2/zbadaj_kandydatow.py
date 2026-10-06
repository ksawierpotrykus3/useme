# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
sys.path.insert(0, str(CORE_DIR / "kod"))

from browser_driver import BrowserDriver
from storage import Storage

jobs = ["145278", "145304", "145415", "145455", "145243", "145198", "145394"]
storage = Storage()
wyniki = []

with BrowserDriver(headless=True) as driver:
    page = driver.context.new_page()
    for jid in jobs:
        url = f"https://useme.com/pl/jobs/{jid}/"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            driver.dismiss_cookie_banner(page)
            page.wait_for_timeout(800)
            
            # Czy przekierowano do my-offer?
            curr_url = page.url
            if "my-offer" in curr_url:
                continue
                
            # Autor
            author_loc = page.locator("a[href*='/user/'], a[href*='/client/']").first
            author = author_loc.inner_text().strip() if author_loc.count() > 0 else "Nieznany"
            
            # PV button
            pv_btn = page.locator("a:has-text('Zapytaj o szczegóły'), a[href*='/mesg/compose/']").first
            pv_ok = pv_btn.count() > 0 and pv_btn.is_visible()
            pv_href = pv_btn.get_attribute("href") if pv_btn.count() > 0 else None
            
            # Tytuł
            h1 = page.locator("h1").first
            title = h1.inner_text().strip() if h1.count() > 0 else ""
            
            if pv_ok:
                wyniki.append({
                    "id": jid,
                    "title": title,
                    "author": author,
                    "pv_href": pv_href,
                    "url": curr_url
                })
        except Exception as e:
            print(f"Błąd dla #{jid}: {e}")

print(json.dumps(wyniki, indent=2, ensure_ascii=False))
