# -*- coding: utf-8 -*-
import json
from pathlib import Path
from collections import Counter

for p in ["badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json",
          "badania/baza/ksawierpotrykus3/03_odpisane/wygrane.json",
          "badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json"]:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    rek = d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []
    print("=== {} ===".format(p))
    print("  rekordow:", len(rek))
    print("  status_koncowy:", dict(Counter(r.get("status_koncowy") for r in rek)))
    print("  status:", dict(Counter(r.get("status") for r in rek)))
    # unikalne job_id
    ids = [r.get("job_id") for r in rek if r.get("job_id")]
    print("  unikalnych job_id:", len(set(ids)))
    print()
