# -*- coding: utf-8 -*-
"""Wysyłacz ofert z poczekalni (Botv2/poczekalnia_ofert).

Pozwala przejrzeć zamrożone oferty i wysłać je:
1. Jako wiadomość prywatną PV (PVDriver - 'Zapytaj o szczegóły')
2. Lub jako oficjalną ofertę Useme (FormDriver)

Użycie:
    python Botv2/wyslij_z_poczekalni.py --list
    python Botv2/wyslij_z_poczekalni.py 145391 --dry-run
    python Botv2/wyslij_z_poczekalni.py 145391 --live
    python Botv2/wyslij_z_poczekalni.py 145391 --tryb oferta --dry-run
    python Botv2/wyslij_z_poczekalni.py --all --dry-run
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
KOD_DIR = CORE_DIR / "kod"
POCZEKALNIA_DIR = BASE_DIR / "poczekalnia_ofert"

sys.path.insert(0, str(KOD_DIR))

import config  # noqa: E402
from ai_pipeline import ProposalResult  # noqa: E402
from browser_driver import BrowserDriver  # noqa: E402
from form_driver import FormDriver  # noqa: E402
from pv_driver import PVDriver  # noqa: E402
from storage import Storage  # noqa: E402


def lista_poczekalni():
    wyniki = []
    if not POCZEKALNIA_DIR.exists():
        return wyniki
    for d in sorted(POCZEKALNIA_DIR.iterdir()):
        if not d.is_dir():
            continue
        meta_file = d / "meta.json"
        txt_file = d / "oferta.txt"
        if meta_file.exists() and txt_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                meta["katalog"] = str(d)
                meta["tresc"] = txt_file.read_text(encoding="utf-8").strip()
                wyniki.append(meta)
            except Exception:
                pass
    return wyniki


def wyslij_pojedyncza(job_id: str, tryb: str, dry_run: bool, headless: bool):
    job_dir = POCZEKALNIA_DIR / str(job_id)
    meta_file = job_dir / "meta.json"
    txt_file = job_dir / "oferta.txt"

    if not meta_file.exists() or not txt_file.exists():
        print(f"[BLAD] Zlecenie #{job_id} nie istnieje w poczekalni ({job_dir}).")
        return False

    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    tresc = txt_file.read_text(encoding="utf-8").strip()

    print("=" * 70)
    print(f"   WYSYŁKA Z POCZEKALNI: #{job_id} ({meta.get('title')})")
    print(f"   Klient: {meta.get('author')}")
    print(f"   Wycena: {meta.get('wycena_dolna')}-{meta.get('wycena_gorna')} zł (domyślna: {meta.get('wycena')} zł)")
    print(f"   Ścieżka: {tryb.upper()} | Tryb: {'DRY_RUN (BEZPIECZNY)' if dry_run else 'LIVE (WYSYŁKA!)'}")
    print("=" * 70)
    print(f"TREŚĆ:\n{tresc}\n" + "-" * 70)

    storage = Storage()
    job_record = storage.load_job(job_id) or {}
    author_id = meta.get("author_id") or job_record.get("author_id") or (job_record.get("full_details") or {}).get("author_id")

    with BrowserDriver(headless=headless) as driver:
        if tryb == "pv":
            pv_driver = PVDriver(driver.context, dry_run=dry_run)
            res = pv_driver.send_private_message(
                job_id=str(job_id),
                message_text=tresc,
                author_id=author_id,
                dry_run=dry_run,
                custom_screenshot_dir=BASE_DIR / "debug"
            )
            print(f"[WYNIK PV] {json.dumps(res, indent=2, ensure_ascii=False)}")
            if not dry_run and res.get("status") in ["WYSLANO", "OK", "WYSLANA", "WYSLANO_PV"]:
                (job_dir / "status_wysylki.json").write_text(
                    json.dumps({"data": datetime.now().isoformat(), "typ": "pv", "wynik": res}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                storage.update_job(job_id, {"status": "WYSLANO_PV", "wyslano_pv_at": datetime.now().isoformat()})
            return res.get("status") in ["WYSLANO", "OK", "WYSLANA", "WYSLANO_PV", "DRY_RUN_OK"]

        elif tryb == "oferta":
            form_driver = FormDriver(driver.context, dry_run=dry_run)
            prop = ProposalResult(
                opis=tresc,
                wycena=int(meta.get("wycena") or 1500),
                dni=int(meta.get("dni_od") or 7),
                powod_wyboru="wysylka_z_poczekalni",
                metadata=meta
            )
            res = form_driver.fill_and_prepare_offer(str(job_id), prop)
            print(f"[WYNIK OFERTA] {json.dumps(res, indent=2, ensure_ascii=False)}")
            if not dry_run and res.get("status") in ["WYSLANO", "OK", "WYSLANA"]:
                (job_dir / "status_wysylki.json").write_text(
                    json.dumps({"data": datetime.now().isoformat(), "typ": "oferta", "wynik": res}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                storage.update_job(job_id, {"status": "WYSLANO", "wyslano_at": datetime.now().isoformat()})
            return res.get("status") in ["WYSLANO", "OK", "WYSLANA", "DRY_RUN_OK"]


def main():
    parser = argparse.ArgumentParser(description="Wysyłka gotowych ofert z poczekalni")
    parser.add_argument("job_id", nargs="?", default=None, help="ID zlecenia z poczekalni")
    parser.add_argument("--list", action="store_true", help="Pokaż listę zleceń w poczekalni")
    parser.add_argument("--tryb", choices=["pv", "oferta"], default="pv", help="Ścieżka wysyłki: pv (domyślna) lub oferta")
    parser.add_argument("--live", "--send", dest="live", action="store_true", help="Wysyłka na żywo (bez tego jest DRY-RUN)")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=None, help="Tylko bezpieczny test")
    parser.add_argument("--headless", action="store_true", default=False, help="Tryb headless")
    parser.add_argument("--all", action="store_true", help="Wyślij wszystkie zlecenia z poczekalni")
    args = parser.parse_args()

    if args.list:
        oferty = lista_poczekalni()
        print(f"\n[POCZEKALNIA] Znaleziono {len(oferty)} zamrożonych ofert:")
        for o in oferty:
            print(f"  #{o['job_id']} | {o.get('author')} | {o.get('wycena_dolna')}-{o.get('wycena_gorna')} zł | {o.get('title')[:60]}")
            print(f"    -> plik: {o['katalog']}\\oferta.txt")
        print()
        return

    dry_run = not args.live

    if args.all:
        oferty = lista_poczekalni()
        for o in oferty:
            wyslij_pojedyncza(o["job_id"], args.tryb, dry_run, args.headless)
    elif args.job_id:
        wyslij_pojedyncza(args.job_id, args.tryb, dry_run, args.headless)
    else:
        print("[INFO] Podaj ID zlecenia lub użyj --list / --all. Np. python Botv2/wyslij_z_poczekalni.py --list")


if __name__ == "__main__":
    main()
