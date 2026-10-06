# -*- coding: utf-8 -*-
"""Cienki runner: odpala CALY lancuch V2 przez brain.zbuduj_oferte i pokazuje oferte.

Nie duplikuje logiki (analiza/research/wycena/pismo/sedzia+petla VETO sa w brain.py).
Artefakty (1_analiza.md ... 6_koncowa.md) zapisuje sam brain do 01_ofertowarka/<id>/.

Uzycie:
    python odpal_lancuch.py 2897327
    python odpal_lancuch.py 2897327 2538404
"""
from __future__ import annotations

import html
import json
import re
import sys
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
OFERTOWARKA = CORE / "badania/baza/ksawierpotrykus3/01_ofertowarka"


def _clean(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _dopasuj(z: dict) -> dict:
    """Adapter rekordu przegranej -> format zlecenia dla zbuduj_oferte."""
    return {
        "id": str(z.get("offer_id") or "?"),
        "title": z.get("title") or "",
        "full_description": _clean(z.get("job_description")),
        "budget": z.get("budget") or "",
    }


def uruchom(zlecenie: dict) -> dict:
    job_id = str(zlecenie.get("id", "?"))
    # zapisz_dziennik=False: produkcja nie zostawia roboczego pliku w mozg/dzienniki.
    # Artefakty i tak trafiaja do ofertowarki (robi to brain).
    wynik = zbuduj_oferte(zlecenie, verbose=True, zapisz_dziennik=False)
    return wynik


def main():
    ids = [a for a in sys.argv[1:] if len(a) >= 5]
    if not ids:
        print("Uzycie: python odpal_lancuch.py <job_id> [job_id2 ...]")
        return

    dane = json.loads(BAZA.read_text(encoding="utf-8"))
    rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
    mapa = {str(r.get("offer_id")): r for r in rek}

    wyniki = []
    for jid in ids:
        surowy = mapa.get(jid)
        if not surowy:
            print(f"[BRAK] #{jid} nie ma w bazie przegranych")
            continue
        zl = _dopasuj(surowy)
        print("\n" + "=" * 78, flush=True)
        print(f"ZLECENIE #{jid} | {zl['title'][:60]}", flush=True)
        print("=" * 78, flush=True)
        try:
            w = uruchom(zl)
        except Exception as e:
            print(f"[BLAD] #{jid}: {e}", flush=True)
            continue

        if not w.get("ok"):
            print(f"[STOP] {w.get('blad')}", flush=True)
            continue

        print("\n--- OFERTA ---", flush=True)
        print(w["oferta"], flush=True)
        print("\n" + "-" * 78, flush=True)
        print(f"[WYCENA]  {w['wycena_dolna']}-{w['wycena_gorna']} zl / {w['dni_od']}-{w['dni_do']} dni", flush=True)
        chk = w["checker"]
        print(f"[CHECKER] {'OK' if chk['ok'] else [p['regula'] for p in chk['problemy']]}", flush=True)
        sed = w["sedzia"]
        print(f"[SEDZIA]  {sed.get('status')} (kara {sed.get('kara_pkt')} pkt) | napraw: {len(w.get('veto_przebieg') or [])}x", flush=True)
        print(f"[ZAPIS]   {OFERTOWARKA / jid}", flush=True)
        wyniki.append(w)

    print("\n" + "=" * 78, flush=True)
    print(f"GOTOWE. Wyniki w: {OFERTOWARKA}", flush=True)
    for w in wyniki:
        if w.get("ok"):
            print(f"  #{w['job_id']}: {w['wycena_dolna']}-{w['wycena_gorna']} zl "
                  f"| checker {'OK' if w['checker']['ok'] else 'PROBLEMY'} "
                  f"| sedzia {w['sedzia'].get('status')}", flush=True)
        else:
            print(f"  #{w.get('job_id')}: STOP - {w.get('blad')}", flush=True)


if __name__ == "__main__":
    main()