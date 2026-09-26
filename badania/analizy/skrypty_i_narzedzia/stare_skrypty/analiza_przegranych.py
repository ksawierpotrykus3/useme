# -*- coding: utf-8 -*-
"""Analiza 16 pobranych przegranych ofert pod kątem psychologii, tonu, wyceny i przyczyn porażki."""

import json
from pathlib import Path


def main():
    data_file = Path(__file__).resolve().parent / "przegrane_oferty_historia.json"
    if not data_file.exists():
        print(f"Brak pliku danych: {data_file}")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        offers = json.load(f)

    print(f"Liczba wczytanych ofert: {len(offers)}\n")

    patterns = {
        "zdzwonmy_sie": 0,
        "15_minut": 0,
        "dwuosobowy_zespol": 0,
        "mina": 0,
        "belfer_ton": 0,
        "demo_oferowane": 0,
        "wymienione_portfolio": 0,
        "podpis_ksawier": 0,
        "brak_podpisu": 0,
    }

    prices = []

    for idx, o in enumerate(offers, 1):
        oid = o.get("offer_id", "")
        title = o.get("title", "")
        client = o.get("client", "")
        budget = o.get("budget", "")
        price = o.get("our_price", "")
        days = o.get("our_days", "")
        prop = o.get("our_proposal", "")

        # Analiza tekstu
        prop_lower = prop.lower()

        has_call = any(w in prop_lower for w in ["zdzwońmy", "zdzwonmy", "porozmawiajmy", "spotkajmy"])
        has_15m = any(w in prop_lower for w in ["15 minut", "15 min", "kwadrans"])
        has_team = any(w in prop_lower for w in ["dwuosobow", "zespoł", "zespol"])
        has_mina = any(w in prop_lower for w in ["mina", "minę", "pułapk"])
        has_belfer = any(w in prop_lower for w in ["zanim zaczniemy", "prawdziwy problem leży", "to błąd", "gdzie w tym planie jest mina", "nie wiesz"])
        has_demo = any(w in prop_lower for w in ["demo", "próbk", "prototyp"])
        has_ksawier = "ksawier" in prop_lower

        if has_call: patterns["zdzwonmy_sie"] += 1
        if has_15m: patterns["15_minut"] += 1
        if has_team: patterns["dwuosobowy_zespol"] += 1
        if has_mina: patterns["mina"] += 1
        if has_belfer: patterns["belfer_ton"] += 1
        if has_demo: patterns["demo_oferowane"] += 1
        if has_ksawier: patterns["podpis_ksawier"] += 1
        else: patterns["brak_podpisu"] += 1

        p_clean = price.replace("PLN", "").replace(" ", "").replace(",", ".").strip()
        try:
            prices.append(float(p_clean))
        except Exception:
            pass

        first_line = prop.split("\n")[0] if prop else ""
        last_line = prop.split("\n")[-1] if prop else ""
        if not last_line and len(prop.split("\n")) > 1:
            last_line = prop.split("\n")[-2]

        print(f"[{idx}] {oid} | Klient: {client:15} | Wycena: {price:12} ({days} dni) | Budżet klienta: {budget}")
        print(f"    Tytuł: {title[:70]}")
        print(f"    Wstęp: {first_line[:80]}")
        print(f"    Koniec: {last_line[:80]}")
        print(f"    Tagi: [Call: {has_call}, 15m: {has_15m}, Zespół: {has_team}, Belfer: {has_belfer}, Demo: {has_demo}, Ksawier: {has_ksawier}]")
        print("-" * 90)

    print("\n=== PODSUMOWANIE STATYSTYCZNE BŁĘDÓW W 16 PRZEGRANYCH OFERTACH ===")
    for k, v in patterns.items():
        pct = (v / len(offers)) * 100 if offers else 0
        print(f"  {k:22}: {v:2}/{len(offers)} ({pct:5.1f}%)")

    if prices:
        print(f"\nŚrednia cena w przegranych ofertach: {sum(prices)/len(prices):.2f} PLN")
        print(f"Mediana cen: {sorted(prices)[len(prices)//2]:.2f} PLN")
        print(f"Min: {min(prices):.2f} PLN | Max: {max(prices):.2f} PLN")


if __name__ == "__main__":
    main()
