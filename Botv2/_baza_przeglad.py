# -*- coding: utf-8 -*-
"""Przeglad bazy: ile zlecen, jakie typy, jakie tytuly. Dla kontekstu."""
import json, random
from pathlib import Path

PLIKI = [
    ("przegrane", "badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json"),
    ("odpisane", "badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json"),
]

wszystkie = []
for nazwa, p in PLIKI:
    try:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        rek = d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []
        for r in rek:
            if (r.get("job_description") or "").strip():
                wszystkie.append({
                    "zrodlo": nazwa,
                    "title": r.get("title", ""),
                    "budget": r.get("budget", ""),
                    "our_price": r.get("our_price", ""),
                    "opis_len": len(r.get("job_description", "")),
                })
    except Exception as e:
        print(f"{nazwa}: ERR {e}")

# ofertowarka
import glob
for f in glob.glob("badania/baza/ksawierpotrykus3/01_ofertowarka/*/*.json"):
    try:
        r = json.loads(Path(f).read_text(encoding="utf-8"))
        fd = r.get("full_details") or {}
        ld = r.get("list_details") or {}
        opis = r.get("full_description") or fd.get("full_description") or r.get("short_desc") or ld.get("short_desc") or ""
        if opis.strip():
            wszystkie.append({
                "zrodlo": "ofertowarka",
                "title": r.get("title", ""),
                "budget": r.get("budget", ""),
                "our_price": (r.get("ai_proposal") or {}).get("wycena", ""),
                "opis_len": len(opis),
            })
    except Exception:
        pass

print(f"=== LACZNIE ZLECEN Z OPISEM: {len(wszystkie)} ===\n")

print("=== ROZKLAD DLUGOSCI OPISU ===")
krotkie = sum(1 for z in wszystkie if z["opis_len"] < 300)
srednie = sum(1 for z in wszystkie if 300 <= z["opis_len"] < 1000)
dlugie = sum(1 for z in wszystkie if z["opis_len"] >= 1000)
print(f"krotkie (<300 znakow): {krotkie}")
print(f"srednie (300-1000): {srednie}")
print(f"dlugie (1000+): {dlugie}")

print("\n=== PRZYKLADOWE TYTULY (20 losowych) ===")
random.seed(42)
for z in random.sample(wszystkie, min(20, len(wszystkie))):
    print(f"  [{z['zrodlo']}] {z['title'][:70]} | budzet: {z['budget']}")

print("\n=== NASZE CENY (z bazy, gdzie sa) ===")
ceny = [z["our_price"] for z in wszystkie if z["our_price"]]
print(f"zlecen z nasza cena: {len(ceny)}")
