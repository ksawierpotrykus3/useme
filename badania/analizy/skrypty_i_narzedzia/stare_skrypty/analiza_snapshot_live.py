# -*- coding: utf-8 -*-
"""Skrypt analityczny dla bieżącego badania rynku Live (Top 40 + kategorie 3D/Design)."""

import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "badania" / "badanie_kategorii_live_snapshot.json"
REPORT_FILE = BASE_DIR / "strategia" / "01_material_dowodowy" / "07_badanie_rentownosci_kategorii_i_3d_live.md"

def analyze():
    if not INPUT_FILE.exists():
        print(f"Brak pliku {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    top40 = data.get("top40_jobs", [])
    detailed = data.get("detailed_jobs", [])
    cat_counts = data.get("category_counts", {})
    
    print(f"Pobrano {len(top40)} zleceń z Top 40 oraz {len(detailed)} łącznie szczegółowych.")

    # 1. Rozkład kategorii w Top 40
    top40_cats = Counter([j.get("category", "Nieznana") for j in top40])
    
    # 2. Konkurencja w Top 40
    zero_offers = [j for j in top40 if j.get("offers_count", 0) == 0]
    low_offers = [j for j in top40 if 1 <= j.get("offers_count", 0) <= 5]
    crowded_offers = [j for j in top40 if j.get("offers_count", 0) > 10]
    
    # 3. Zbadanie zleceń związanych z 3D, Architekturą, Animacją
    niche_3d = [j for j in detailed if any(k in (j.get("source_category", "") + " " + j.get("category", "") + " " + j.get("title", "")).lower() for k in ["3d", "animacj", "architekt", "render", "modelow"])]
    
    # 4. Zbadanie zleceń IT / Web / Sklepy
    it_jobs = [j for j in detailed if any(k in (j.get("category", "") + " " + j.get("title", "")).lower() for k in ["program", "aplikacj", "sklep", "crm", "api", "web", "serwis", "automatyz"])]
    
    print("\n--- ROZKŁAD KATEGORII W NAJNOWSZYCH 40 ZLECENIACH ---")
    for cat, cnt in top40_cats.most_common():
        print(f"  {cat}: {cnt} ({cnt/len(top40)*100:.1f}%)")
        
    print(f"\nStan konkurencji w Top 40:")
    print(f"  0 ofert (świeżo wystawione dzisiaj): {len(zero_offers)} ({len(zero_offers)/len(top40)*100:.1f}%)")
    print(f"  1-5 ofert: {len(low_offers)} ({len(low_offers)/len(top40)*100:.1f}%)")
    print(f"  >10 ofert: {len(crowded_offers)} ({len(crowded_offers)/len(top40)*100:.1f}%)")

    print(f"\nZnalezione zlecenia 3D / Architektura / Animacja ({len(niche_3d)} szt.):")
    for j in niche_3d:
        print(f"  [{j['id']}] {j['title']} | Kat: {j['category']} | Budżet: {j['budget']} | Ofert: {j['offers_count']}")

if __name__ == "__main__":
    analyze()
