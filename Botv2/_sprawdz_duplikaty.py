# -*- coding: utf-8 -*-
import json
from pathlib import Path

def wczytaj(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []

a = wczytaj("badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json")
b = wczytaj("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
c = wczytaj("badania/baza/ksawierpotrykus3/03_odpisane/wygrane.json")

ta = set(r.get("title", "").strip() for r in a)
tb = set(r.get("title", "").strip() for r in b)
tc = set(r.get("title", "").strip() for r in c)

print("wygrane_56: {}".format(len(ta)))
print("odpisane_zamkniete: {}".format(len(tb)))
print("wygrane: {}".format(len(tc)))
print()
print("a ∩ b (te same): {}".format(len(ta & tb)))
print("a ∩ c: {}".format(len(ta & tc)))
print("b ∩ c: {}".format(len(tb & tc)))
print()
print("suma unikalna (a|b|c): {}".format(len(ta | tb | tc)))
