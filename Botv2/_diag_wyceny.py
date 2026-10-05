# -*- coding: utf-8 -*-
"""Diagnoza wycen: 3 zlecenia, po 3 wyceny każde. Porownanie z realnymi ofertami konkurencji."""
import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia")

# 1. Sprawdz strukture jednej oferty
print("=== STRUKTURA OFERTY KONKURENCJI ===")
przyklad = None
for d in BASE.iterdir():
    ofd = d / "oferty"
    if ofd.exists():
        files = sorted(ofd.glob("*.json"))
        if files:
            przyklad = files[0]
            break
if przyklad:
    dane = json.loads(przyklad.read_text(encoding="utf-8"))
    print("Plik:", przyklad.name)
    print("Klucze:", list(dane.keys()))
    for k in ("kwota", "cena", "price", "amount", "stawka", "dni", "days", "wykonawca", "author", "tresc", "opis"):
        if k in dane:
            v = dane[k]
            print(f"  {k}: {str(v)[:120]}")
    print()

# 2. Zbierz realne ceny konkurencji per zlecenie
print("=== REALNE CENY KONKURENCJI (do porownania) ===")
for d in sorted(BASE.iterdir()):
    ofd = d / "oferty"
    if not ofd.exists():
        continue
    ceny = []
    for f in ofd.glob("*.json"):
        try:
            o = json.loads(f.read_text(encoding="utf-8"))
            for k in ("kwota", "cena", "price", "amount"):
                if k in o and o[k]:
                    v = o[k]
                    if isinstance(v, (int, float)):
                        ceny.append(int(v))
                    elif isinstance(v, str):
                        import re
                        m = re.search(r"\d[\d\s]*", v)
                        if m:
                            ceny.append(int(m.group(0).replace(" ", "")))
                    break
        except Exception:
            continue
    if ceny:
        ceny.sort()
        n = len(ceny)
        med = ceny[n // 2]
        print(f"{d.name}: n={n} | min={ceny[0]} | mediana={med} | max={ceny[-1]}")
