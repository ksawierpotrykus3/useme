# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
sys.path.insert(0, str(CORE_DIR / "kod"))

from browser_driver import BrowserDriver
from storage import Storage

storage = Storage()
konta = ["ksawierpotrykus3"]

wyniki = []

with BrowserDriver(headless=True) as driver:
    for cat in ["programowanie-i-it", "serwisy-internetowe"]:
        jobs = driver.fetch_category_jobs(cat)
        for j in jobs[:8]:
            jid = str(j.get("id"))
            j_url = j.get("url")
            j_title = j.get("title")
            j_author = j.get("author") or "Nieznany"
            j_offers = j.get("offers_count", 0)
            
            # Sprawdź czy już oferowaliśmy
            juz_bylo = storage.czy_konto_juz_oferowalo(jid, "konto1")
            
            wyniki.append({
                "id": jid,
                "category": cat,
                "title": j_title,
                "author": j_author,
                "offers_count": j_offers,
                "juz_oferowano": juz_bylo,
                "url": j_url
            })

# Deduplikacja po ID
unikalne = {}
for w in wyniki:
    if w["id"] not in unikalne:
        unikalne[w["id"]] = w

print(json.dumps(list(unikalne.values()), indent=2, ensure_ascii=False))
