# -*- coding: utf-8 -*-
"""Analiza realnych stawek konkurencji dla 3 zleceń testowych.

Czyta wszystkie oferty (oferty/*.json) dla 145285, 145287, 144890 i liczy:
min, percentyle (10/25/50/75/90), max, średnią, histogram.
Wynik zapisuje do Botv2/debug/stawki_konkurencji_3_zlecenia.json.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
BAZA = ROOT.parent / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia"

ZLECENIA = [
    ("145285", "Subiekt <-> BaseLinker (40k SKU)", BAZA / "145285"),
    ("145287", "Aplikacja mobilna offline (Flutter/Kotlin)", BAZA / "145287"),
    ("144890", "Automatyzacja faktur OCR + Optima", BAZA / "zlecenie_testowe_144890"),
]


def _cena_pln(s):
    if not s:
        return None
    m = re.search(r"([\d\s]+)", str(s))
    if not m:
        return None
    digits = re.sub(r"[^\d]", "", m.group(1))
    return int(digits) if digits else None


def _percentyl(dane, p):
    if not dane:
        return None
    dane = sorted(dane)
    k = (len(dane) - 1) * p
    f = int(k)
    c = min(f + 1, len(dane) - 1)
    if f == c:
        return dane[f]
    return round(dane[f] + (dane[c] - dane[f]) * (k - f))


def main():
    raport = {}
    for job_id, nazwa, folder in ZLECENIA:
        oferty_dir = folder / "oferty"
        ceny, wpisy = [], []
        if oferty_dir.exists():
            for f in sorted(oferty_dir.glob("*.json")):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                c = _cena_pln(d.get("price"))
                if c is None:
                    continue
                ceny.append(c)
                wpisy.append({
                    "offer_id": d.get("offer_id"),
                    "autor": d.get("author_name"),
                    "umowy": d.get("umowy"),
                    "cena": c,
                    "dni": d.get("days"),
                })

        if not ceny:
            raport[job_id] = {"nazwa": nazwa, "liczba_ofert": 0}
            continue

        stat = {
            "nazwa": nazwa,
            "liczba_ofert": len(ceny),
            "min": min(ceny),
            "p10": _percentyl(ceny, 0.10),
            "p25": _percentyl(ceny, 0.25),
            "mediana": _percentyl(ceny, 0.50),
            "p75": _percentyl(ceny, 0.75),
            "p90": _percentyl(ceny, 0.90),
            "max": max(ceny),
            "srednia": round(statistics.mean(ceny)),
        }

        print("\n" + "=" * 70)
        print(f"#{job_id} {nazwa}  ({len(ceny)} ofert)")
        print("=" * 70)
        print(f"  min={stat['min']}  p10={stat['p10']}  p25={stat['p25']}  "
              f"MEDIANA={stat['mediana']}  p75={stat['p75']}  p90={stat['p90']}  max={stat['max']}")
        print(f"  średnia={stat['srednia']}")

        # Histogram w kubełkach
        kubełki = [0, 2000, 4000, 6000, 8000, 10000, 12500, 15000, 20000, 30000, 10**9]
        print("  Rozkład:")
        for i in range(len(kubełki) - 1):
            lo, hi = kubełki[i], kubełki[i + 1]
            n = sum(1 for c in ceny if lo <= c < hi)
            if n:
                etykieta = f"{lo//1000}k-{hi//1000}k" if hi < 10**9 else f"{lo//1000}k+"
                print(f"    {etykieta:>10}: {'#' * n} ({n})")

        # Top 10 najdroższych i najtańszych
        posort = sorted(wpisy, key=lambda x: x["cena"])
        stat["top5_najdrozsze"] = posort[-5:]
        stat["top5_najtansze"] = posort[:5]
        print("  Najdroższe:")
        for w in posort[-5:]:
            print(f"    {w['cena']:>7} zł | {w['autor']} ({w['umowy']}) | {w['dni']}")
        raport[job_id] = stat

    out = ROOT / "debug" / "stawki_konkurencji_3_zlecenia.json"
    out.write_text(json.dumps(raport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nZapisano: {out}")


if __name__ == "__main__":
    main()