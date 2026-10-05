# -*- coding: utf-8 -*-
import json
from pathlib import Path

for p in ["badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json",
          "badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json",
          "badania/baza/ksawierpotrykus3/03_odpisane/wygrane.json"]:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    rek = d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []
    print("=== {} ===".format(p))
    for r in rek:
        if "Monika" in str(r.get("client", "")) or "Monika" in str(r.get("title", "")):
            print("  Znaleziony rekord:")
            for k, v in r.items():
                sv = str(v)
                print("    {}: {}".format(k, sv[:150]))
            print()
            break
