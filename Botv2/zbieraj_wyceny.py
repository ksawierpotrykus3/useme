# -*- coding: utf-8 -*-
"""Zbiera WYCENY na wielu losowych zleceniach (do pozniejszej analizy).

Dla kazdego zlecenia: pelny lancuch V2 -> zapisuje TYLKO wycene do
01_ofertowarka/<id>/4_wycena.md oraz wycena.json (kwoty, dni, uzasadnienie rozjemcy).
Dodatkowo zbiorczy plik: debug/zbior_wycen.json (lista wszystkich).

Uzycie:
    python zbieraj_wyceny.py 10          # 10 losowych zlecen
    python zbieraj_wyceny.py 20 999999   # 20 losowych z seedem
"""
from __future__ import annotations

import html
import json
import random
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).parent                      # .../useme_core/Botv2
CORE = BASE.parent                                 # .../useme_core
KOD_DIR = CORE / "kod"
sys.path.insert(0, str(KOD_DIR))
sys.path.insert(0, str(BASE / "mozg"))

from brain import zbuduj_oferte  # noqa: E402

BAZA = CORE / "badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json"
ZBIOR = BASE / "debug" / "zbior_wycen.json"


def _clean(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _dopasuj(z: dict) -> dict:
    return {
        "id": str(z.get("offer_id") or "?"),
        "title": z.get("title") or "",
        "full_description": _clean(z.get("job_description")),
        "budget": z.get("budget") or "",
    }


def main():
    if not sys.argv[1:2] or not sys.argv[1].isdigit():
        print("Uzycie: python zbieraj_wyceny.py <ile> [seed]")
        return
    ile = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None

    dane = json.loads(BAZA.read_text(encoding="utf-8"))
    rek = [r for r in dane if len(_clean(r.get("job_description"))) > 300]
    print(f"[BAZA] zlecen z trescia >300: {len(rek)}", flush=True)

    # Kumulacja: wczytaj poprzednie wyniki i NIE powtarzaj tych samych zlecen.
    istniejace: list = []
    zrobione: set = set()
    if ZBIOR.exists():
        try:
            istniejace = json.loads(ZBIOR.read_text(encoding="utf-8"))
            zrobione = {str(z.get("job_id")) for z in istniejace}
            print(f"[ZBIOR] wczytano {len(istniejace)} poprzednich wynikow.", flush=True)
        except Exception:
            istniejace = []

    pula = [r for r in rek if str(r.get("offer_id")) not in zrobione]
    print(f"[PULA] do przetworzenia (nowe): {len(pula)}", flush=True)

    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    wybrane = random.sample(pula, min(ile, len(pula)))

    zbior = istniejace
    for i, z in enumerate(wybrane, 1):
        zl = _dopasuj(z)
        jid = zl["id"]
        print("\n" + "=" * 70, flush=True)
        print(f"[{i}/{len(wybrane)}] #{jid} | {zl['title'][:55]} | budzet: {zl['budget']}", flush=True)
        print("=" * 70, flush=True)

        t0 = time.time()
        try:
            # tryb_zapisu="wycena": zapisuje TYLKO wycene do ofertowarki
            w = zbuduj_oferte(zl, verbose=True, zapisz_dziennik=False, tryb_zapisu="wycena")
        except Exception as e:
            print(f"[BLAD] #{jid}: {e}", flush=True)
            zbior.append({"job_id": jid, "title": zl["title"], "budget": zl["budget"], "blad": str(e)})
            continue

        if not w.get("ok"):
            print(f"[STOP] #{jid}: {w.get('blad')}", flush=True)
            zbior.append({"job_id": jid, "title": zl["title"], "budget": zl["budget"],
                          "odrzucone": w.get("blad")})
            continue

        rekord = {
            "job_id": jid,
            "title": zl["title"],
            "budget": zl["budget"],
            "wycena_dolna": w["wycena_dolna"],
            "wycena_gorna": w["wycena_gorna"],
            "definitywna": bool(w.get("definitywna")) if "definitywna" in w else None,
            "dni_od": w["dni_od"],
            "dni_do": w["dni_do"],
            "checker_ok": w["checker"]["ok"],
            "sedzia": w["sedzia"].get("status"),
            "czas_s": round(time.time() - t0, 1),
        }
        zbior.append(rekord)
        print(f"  -> {rekord['wycena_dolna']}-{rekord['wycena_gorna']} zl | "
              f"dni {rekord['dni_od']}-{rekord['dni_do']} | sedzia {rekord['sedzia']} | {rekord['czas_s']}s", flush=True)

        # zapis na biezaco (zeby nie stracic przy crashu)
        ZBIOR.write_text(json.dumps(zbior, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 70, flush=True)
    print(f"ZEBRANO: {len(zbior)} wycen -> {ZBIOR}", flush=True)
    ok = [z for z in zbior if z.get("wycena_dolna")]
    print(f"  z wycena: {len(ok)} | odrzucone: {len([z for z in zbior if z.get('odrzucone')])} | bledy: {len([z for z in zbior if z.get('blad')])}", flush=True)
    for z in ok:
        print(f"  #{z['job_id']:>9} | {z['wycena_dolna']:>6}-{z['wycena_gorna']:<6} zl | {z['title'][:40]}", flush=True)


if __name__ == "__main__":
    main()