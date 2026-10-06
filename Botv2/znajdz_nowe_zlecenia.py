# -*- coding: utf-8 -*-
"""Wyszukiwarka wszystkich dostępnych zleceń z bazy i live z Useme.

Szuka zleceń, na które NIE wysłaliśmy jeszcze ani oferty, ani wiadomości prywatnej (PV).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
KOD_DIR = CORE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

from browser_driver import BrowserDriver
from storage import Storage
import config

storage = Storage()
konta = ["konto1", "ksawierpotrykus3"]

# 1. Sprawdzamy zlecenia w lokalnym magazynie
lokalne_kandydaci = []
magazyn = config.MAGAZYN_DIR

# Pobierz listę już wysłanych (z poczekalni i storage)
juz_wyslane_ids = set()
poczekalnia_dir = BASE_DIR / "poczekalnia_ofert"
if poczekalnia_dir.exists():
    for d in poczekalnia_dir.iterdir():
        if d.is_dir() and (d / "status_wysylki.json").exists():
            juz_wyslane_ids.add(d.name)

print(f"[STATUS] Już wysłane z poczekalni (PV/oferta): {juz_wyslane_ids}")

for f in magazyn.rglob("*.json"):
    if ".checkpoints" in str(f) or f.name in ["marker.json", "meta.json", "status_wysylki.json"]:
        continue
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        jid = str(data.get("id") or "").strip()
        if not jid:
            continue
        if jid in juz_wyslane_ids:
            continue
        if storage.czy_konto_juz_oferowalo(jid, "konto1"):
            continue

        fd = data.get("full_details") or {}
        if fd.get("is_already_submitted"):
            continue

        title = data.get("title") or fd.get("title") or ""
        author = data.get("author") or fd.get("author") or "Nieznany"
        desc = data.get("full_description") or fd.get("full_description") or data.get("description") or ""

        # Wyklucz własny profil i ewidentne śmieci
        if config.is_blocked_author(data.get("author_id"), author):
            continue

        # Data wykrycia
        detected = data.get("detected_at") or fd.get("scraped_at") or ""

        lokalne_kandydaci.append({
            "id": jid,
            "title": title,
            "author": author,
            "author_id": data.get("author_id") or fd.get("author_id"),
            "url": data.get("url") or f"https://useme.com/pl/jobs/{jid}/",
            "detected": detected,
            "opis_len": len(desc),
            "status": data.get("status"),
            "category": data.get("category", "it")
        })
    except Exception:
        continue

print(f"[MAGAZYN] Znaleziono {len(lokalne_kandydaci)} potencjalnych zleceń w magazynie bez wysłanej oferty.")

# 2. Pobieramy live z Useme z kilku stron bez early-stop
live_kandydaci = []
print("[LIVE] Skanuję strony 1-3 na Useme (IT i Serwisy)...")
with BrowserDriver(headless=True) as driver:
    for cat_slug, cat_id in [("programowanie-i-it", 35), ("serwisy-internetowe", 34)]:
        for strona in range(1, 4):
            url = f"https://useme.com/pl/jobs/category/{cat_slug},{cat_id}/?page={strona}"
            try:
                page = driver.context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                driver.dismiss_cookie_banner(page)
                
                # Używamy BeautifulSoup tak jak fetch_category_jobs
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(page.content(), "html.parser")
                page.close()
                
                for art in soup.select("article.job, .jobs-list__item, .job"):
                    link = art.select_one("a.job__title, h2 a, a[href*='/pl/jobs/']")
                    if not link:
                        continue
                    href = link.get("href", "")
                    m = re.search(r",(\d+)/?$", href)
                    if not m:
                        m = re.search(r"/jobs/(\d+)/", href)
                    if not m:
                        continue
                    jid = m.group(1)
                    if jid in juz_wyslane_ids or storage.czy_konto_juz_oferowalo(jid, "konto1"):
                        continue
                        
                    title = link.get_text(strip=True)
                    # autor
                    author_el = art.select_one(".job__user, .job__details-meta a, a[href*='/user/'], a[href*='/client/']")
                    author = author_el.get_text(strip=True) if author_el else "Anonim"
                    
                    # budżet
                    budget_el = art.select_one(".job__budget, .job__details-meta span")
                    budget = budget_el.get_text(strip=True) if budget_el else ""

                    live_kandydaci.append({
                        "id": jid,
                        "title": title,
                        "author": author,
                        "url": f"https://useme.com{href}" if href.startswith("/") else href,
                        "category": cat_slug,
                        "budget": budget,
                        "strona": strona
                    })
            except Exception as e:
                print(f"[BLAD] Strona {url}: {e}")

# Scalanie i unikalność
wszystkie_map = {}
for k in live_kandydaci:
    wszystkie_map[k["id"]] = k

for k in lokalne_kandydaci:
    if k["id"] not in wszystkie_map:
        wszystkie_map[k["id"]] = k

print(f"\n=======================================================")
print(f"ŁĄCZNIE ZNALEZIONO {len(wszystkie_map)} NIEZROBIONYCH ZLECEŃ:")
print(f"=======================================================")

posortowane = sorted(wszystkie_map.values(), key=lambda x: int(x["id"]) if x["id"].isdigit() else 0, reverse=True)

for i, k in enumerate(posortowane[:25], 1):
    print(f"{i:2d}. #{k['id']} | {k.get('author', 'Anonim')} | {k.get('title')[:65]}")
    print(f"    URL: {k.get('url')}")

# Zapisujemy do pliku roboczego
(BASE_DIR / "dostepne_zlecenia.json").write_text(
    json.dumps(posortowane, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"\nZapisano pełną listę {len(posortowane)} zleceń do Botv2/dostepne_zlecenia.json")
