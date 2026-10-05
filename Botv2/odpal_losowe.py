# -*- coding: utf-8 -*-
"""Odpala mozg V2 na losowych zleceniach z magazynu. Podglad bez wysylki.

Uzycie:
    python odpal_losowe.py            # 3 losowe zlecenia z magazynu
    python odpal_losowe.py 5          # 5 losowych
    python odpal_losowe.py 3 144890   # konkretne ID (ignoruje losowanie)
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

KOD_DIR = Path(__file__).parent.parent / "kod"
sys.path.insert(0, str(KOD_DIR))
sys.path.insert(0, str(Path(__file__).parent / "mozg"))

import config  # noqa: E402
from brain import zbuduj_oferte  # noqa: E402


def _ma_tresc(z: dict) -> bool:
    fd = z.get("full_details") or {}
    desc = (
        z.get("full_description")
        or fd.get("full_description")
        or z.get("description")
        or z.get("short_desc")
        or ""
    )
    return len((desc or "").strip()) > 100


def wczytaj_zlecenia() -> list[dict]:
    """Czyta wszystkie rekordy zlecen z magazynu (konto wykonawcy)."""
    magazyn = config.MAGAZYN_DIR
    wyniki = []
    for path in magazyn.rglob("*.json"):
        if ".checkpoints" in str(path) or path.name == "marker.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if "id" in data and "status" in data:
                wyniki.append(data)
        except Exception:
            continue
    return wyniki


def main():
    args = [a for a in sys.argv[1:] if not a.isdigit() or len(a) < 4]
    ids = [a for a in sys.argv[1:] if len(a) >= 5]

    n = 3
    if sys.argv[1:2] and sys.argv[1].isdigit() and len(sys.argv[1]) < 4:
        n = int(sys.argv[1])

    wszystkie = [z for z in wczytaj_zlecenia() if _ma_tresc(z)]
    print(f"[MAGAZYN] Zlecen z trescia: {len(wszystkie)}", flush=True)

    if ids:
        wybrane = [z for z in wszystkie if str(z.get("id")) in ids]
    else:
        random.seed()
        wybrane = random.sample(wszystkie, min(n, len(wszystkie)))

    for z in wybrane:
        jid = z.get("id")
        print("\n" + "=" * 70, flush=True)
        print(f"ZLECENIE #{jid} - {z.get('title', '')[:60]}", flush=True)
        print("=" * 70, flush=True)
        try:
            wynik = zbuduj_oferte(z)
        except Exception as e:
            print(f"[BLAD] #{jid}: {e}", flush=True)
            continue

        if not wynik.get("ok"):
            print(f"[STOP] {wynik.get('blad')}", flush=True)
            continue

        print("\n--- DZIENNIK MYSLENIA ---", flush=True)
        print(wynik["dziennik"][:1500], flush=True)
        print("\n--- OFERTA ---", flush=True)
        print(wynik["oferta"], flush=True)
        print(f"\n[WYCENA] {wynik['wycena']} zl / {wynik['dni']} dni", flush=True)
        chk = wynik["checker"]
        print(f"[CHECKER] {'OK' if chk['ok'] else 'PROBLEMY: ' + str([p['regula'] for p in chk['problemy']])}", flush=True)


if __name__ == "__main__":
    main()