# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
sys.path.insert(0, str(CORE_DIR / "kod"))

from browser_driver import BrowserDriver
from storage import Storage

jobs_to_check = ['145391', '145466', '145494', '145490', '145468']
results = {}

with BrowserDriver(headless=True) as driver:
    page = driver.context.new_page()
    for jid in jobs_to_check:
        url = f"https://useme.com/pl/jobs/{jid}/"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        driver.dismiss_cookie_banner(page)
        page.wait_for_timeout(1000)

        # Sprawdzenie czy nie przekierowało (np. my-offer)
        curr_url = page.url
        is_redirected = curr_url != url and "my-offer" in curr_url

        # Szukanie autora
        author = "Nieznany"
        author_loc = page.locator("a[href*='/user/'], a[href*='/client/']").first
        if author_loc.count() > 0:
            author = author_loc.inner_text().strip()

        # Szukanie przycisku PV
        pv_btn = page.locator("a:has-text('Zapytaj o szczegóły'), a[href*='/mesg/compose/']").first
        pv_count = pv_btn.count()
        pv_vis = pv_btn.is_visible() if pv_count > 0 else False
        pv_href = pv_btn.get_attribute("href") if pv_count > 0 else None

        # Szukanie przycisku oferty
        offer_btn = page.locator("a:has-text('Złóż ofertę'), a[href*='/offer/start/']").first
        offer_count = offer_btn.count()
        offer_vis = offer_btn.is_visible() if offer_count > 0 else False
        offer_href = offer_btn.get_attribute("href") if offer_count > 0 else None

        results[jid] = {
            "author": author,
            "current_url": curr_url,
            "is_redirected": is_redirected,
            "pv_available": pv_vis,
            "pv_href": pv_href,
            "offer_available": offer_vis,
            "offer_href": offer_href,
        }

print(json.dumps(results, indent=2, ensure_ascii=False))
