# -*- coding: utf-8 -*-
import json
from pathlib import Path
from collections import Counter

p = "badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json"
d = json.loads(Path(p).read_text(encoding="utf-8"))
print("typ:", type(d).__name__)
if isinstance(d, dict):
    print("klucze dict:", list(d.keys()))
rek = d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []
print("rekordow:", len(rek))
ids = [r.get("job_id") or r.get("offer_id") for r in rek]
print("unikalnych ID:", len(set(ids)))
print("statusy:", dict(Counter(r.get("status_koncowy") for r in rek)))
print("odpisal:", dict(Counter(str(r.get("odpisal")) for r in rek)))
print()
print("=== 10 rekordow ===")
for r in rek[:10]:
    print("  job_id={} | {} | status={} | odpisal={}".format(
        r.get("job_id"), str(r.get("title", ""))[:55], r.get("status_koncowy"), r.get("odpisal")))
