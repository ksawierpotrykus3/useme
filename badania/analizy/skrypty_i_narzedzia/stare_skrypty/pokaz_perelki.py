# -*- coding: utf-8 -*-
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("badania/badanie_kategorii_live_snapshot.json", encoding="utf-8") as f:
    d = json.load(f)

print("=== LIVE SNAPSHOT: TOP NOWE ZLECENIA IT / AUTOMATYZACJE / 3D ===\n")
for j in d["top40_jobs"]:
    cat = j.get("category", "")
    title = j.get("title", "")
    if any(k in (cat + " " + title).lower() for k in ["program", "oprogramowanie", "aplikacj", "sklep", "crm", "bot", "automatyz", "3d", "konfigurator", "shopify", "wordpress", "lovable", "landing"]):
        print(f"[{j['id']}] {title}")
        print(f"   Kategoria: {cat} | Budżet: {j.get('budget')} | Ofert: {j.get('offers_count')}")
        print(f"   Opis: {j.get('short_desc', '')[:160]}...")
        print(f"   URL: {j.get('url')}\n")
