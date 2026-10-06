# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
baza_dir = CORE_DIR / "badania" / "baza"

all_baza_jobs = {}

for p in baza_dir.rglob("*.json"):
    if ".checkpoints" in str(p) or p.name in ["marker.json", "meta.json", "status_wysylki.json", "blocklist.json"]:
        continue
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        jid = str(data.get("id") or p.stem).strip()
        if jid.isdigit():
            fd = data.get("full_details") or {}
            all_baza_jobs[jid] = {
                "id": jid,
                "path": str(p),
                "rel_path": str(p.relative_to(baza_dir)),
                "status": data.get("status"),
                "title": data.get("title") or fd.get("title") or "",
                "author": data.get("author") or fd.get("author") or "",
                "has_ai_proposal": bool(data.get("ai_proposal")),
                "is_already_submitted": fd.get("is_already_submitted", False),
                "konto_oferty": data.get("konto"),
                "detected_at": data.get("detected_at") or fd.get("scraped_at") or "",
            }
    except Exception:
        pass

print("=" * 70)
print(f"RAPORT Z PEŁNEGO AUDYTU BAZY: {baza_dir}")
print("=" * 70)
print(f"Łącznie unikalnych zleceń w bazie: {len(all_baza_jobs)}")

by_folder = {}
for jid, info in all_baza_jobs.items():
    parts = Path(info["rel_path"]).parts
    kat = "/".join(parts[:2]) if len(parts) >= 2 else parts[0]
    by_folder[kat] = by_folder.get(kat, 0) + 1

print("\nPodział na foldery w bazie:")
for f, cnt in sorted(by_folder.items()):
    print(f"  - {f}: {cnt} zleceń")

by_status = {}
for jid, info in all_baza_jobs.items():
    st = str(info["status"])
    by_status[st] = by_status.get(st, 0) + 1

print("\nPodział według statusu w bazie:")
for st, cnt in sorted(by_status.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {st}: {cnt}")

# Sprawdzenie z plikiem dostepne_zlecenia.json (te 105 co znaleźliśmy)
dostepne_file = BASE_DIR / "dostepne_zlecenia.json"
if dostepne_file.exists():
    dostepne = json.loads(dostepne_file.read_text(encoding="utf-8"))
    print("\n" + "=" * 70)
    print(f"PORÓWNANIE Z LISTĄ 105 ZLECEŃ:")
    print("=" * 70)
    w_bazie = 0
    nie_w_bazie = 0
    w_bazie_ale_bez_oferty = 0
    w_bazie_z_oferta = 0
    
    statusy_tych_w_bazie = {}
    
    for d in dostepne:
        jid = str(d["id"])
        if jid in all_baza_jobs:
            w_bazie += 1
            info = all_baza_jobs[jid]
            st = str(info["status"])
            statusy_tych_w_bazie[st] = statusy_tych_w_bazie.get(st, 0) + 1
            if info["is_already_submitted"] or info["status"] in ["WYSLANO", "WYSLANO_PV"]:
                w_bazie_z_oferta += 1
            else:
                w_bazie_ale_bez_oferty += 1
        else:
            nie_w_bazie += 1
            
    print(f"Z tych 105 zleceń:")
    print(f"  - W bazie (zapisane wcześniej przez bota): {w_bazie}")
    print(f"    * W bazie, ale BEZ wysłanej oferty (czekały/pobrane detale/odrzucone): {w_bazie_ale_bez_oferty}")
    print(f"    * W bazie z statusem wysłano/złożono: {w_bazie_z_oferta}")
    print(f"  - Całkowicie NOWE (tylko na Useme live, nie ma ich jeszcze w plikach): {nie_w_bazie}")
    print("\nStatusy tych, które już były zapisane w magazynie:")
    for st, cnt in sorted(statusy_tych_w_bazie.items(), key=lambda x: x[1], reverse=True):
        print(f"    * {st}: {cnt}")
