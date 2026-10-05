# -*- coding: utf-8 -*-
"""Odpala mozg V2 na LOSOWYCH zleceniach z bazy NIEODPISANYCH (02_przegrane).

Porownuje nowa wycene V2 z nasza stara cena (our_price) i pokazuje pelny przebieg.

Uzycie:
    python odpal_przegrane.py            # 3 losowe
    python odpal_przegrane.py 5          # 5 losowych
    python odpal_przegrane.py 0 2908477 # konkretny offer_id (0 = tryb ID)
"""

from __future__ import annotations

import html
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).parent          # .../useme_core/Botv2
CORE = BASE.parent                     # .../useme_core
KOD_DIR = CORE / "kod"
sys.path.insert(0, str(KOD_DIR))
sys.path.insert(0, str(BASE / "mozg"))

from brain import zbuduj_oferte  # noqa: E402

BAZA = CORE / "badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json"
WYNIKI = BASE / "debug" / "benchmark_v2_przegrane.json"


def _clean(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _cena(s) -> int:
    """'1800,00 PLN' -> 1800 ; obcina grosze po przecinku/kropce dziesietnej."""
    t = str(s or "").strip()
    t = re.sub(r"[,.]\d{1,2}\s*(?:PLN|zl|zł)?\s*$", "", t)  # usun koncowke ',00 PLN'
    cyfry = re.sub(r"[^\d]", "", t)
    return int(cyfry) if cyfry else 0


def _dopasuj(z: dict) -> dict:
    """Adapter rekordu przegranej -> format zlecenia dla zbuduj_oferte."""
    return {
        "id": str(z.get("offer_id") or "?"),
        "title": z.get("title") or "",
        "full_description": _clean(z.get("job_description")),
        "budget": z.get("budget") or "",
        "_stara_cena": _cena(z.get("our_price")),
        "_stare_dni": _cena(z.get("our_days")),
        "_stara_oferta": z.get("our_proposal") or "",
        "_client": z.get("client") or "",
        "_url": z.get("job_url") or "",
    }


def main():
    n = 3
    if sys.argv[1:2] and sys.argv[1].isdigit():
        n = int(sys.argv[1])

    ids = [a for a in sys.argv[2:] if len(a) >= 5]

    dane = json.loads(BAZA.read_text(encoding="utf-8"))
    rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
    rek = [r for r in rek if len(_clean(r.get("job_description"))) > 100]
    print(f"[BAZA] przegrane z trescia: {len(rek)}", flush=True)

    if ids:
        wybrane = [r for r in rek if str(r.get("offer_id")) in ids]
    else:
        random.seed()
        wybrane = random.sample(rek, min(n, len(rek)))

    wyniki = []
    for z in wybrane:
        zl = _dopasuj(z)
        jid = zl["id"]
        print("\n" + "=" * 78, flush=True)
        print(f"ZLECENIE #{jid} | {zl['title'][:66]}", flush=True)
        print(f"KLIENT: {zl['_client']} | BUDZET KLIENTA: {zl['budget']}", flush=True)
        print(f"NASZA STARA CENA: {zl['_stara_cena']} zl / {zl['_stare_dni']} dni", flush=True)
        print("=" * 78, flush=True)

        try:
            wynik = zbuduj_oferte(zl)
        except Exception as e:
            print(f"[BLAD] #{jid}: {e}", flush=True)
            continue

        if not wynik.get("ok"):
            print(f"[STOP] {wynik.get('blad')}", flush=True)
            wyniki.append({"id": jid, "ok": False, "blad": wynik.get("blad"),
                           "stara_cena": zl["_stara_cena"]})
            continue

        nowa = wynik["wycena"]
        stara = zl["_stara_cena"]
        print(f"\n--- OFERTA V2 ---\n{wynik['oferta']}", flush=True)
        print("\n" + "-" * 78, flush=True)
        print(f"[WYCENA]    stara: {stara} zl / {zl['_stare_dni']} dni   ->   V2: {nowa} zl / {wynik['dni_od']}-{wynik['dni_do']} dni", flush=True)
        if stara:
            delta = (nowa - stara) / stara * 100
            print(f"[ROZNICA]   {delta:+.1f}%", flush=True)
        print(f"[CHECKER]   {'OK' if wynik['checker']['ok'] else [p['regula'] for p in wynik['checker']['problemy']]}", flush=True)
        print(f"[SEDZIA]    {wynik['sedzia'].get('status')} (kara {wynik['sedzia'].get('kara_pkt')} pkt)", flush=True)

        wyniki.append({
            "id": jid,
            "ok": True,
            "title": zl["title"],
            "budget_klienta": zl["budget"],
            "stara_cena": stara, "stare_dni": zl["_stare_dni"],
            "nowa_cena": nowa, "nowe_dni": f"{wynik['dni_od']}-{wynik['dni_do']}",
            "delta_pct": round((nowa - stara) / stara * 100, 1) if stara else None,
            "checker_ok": wynik["checker"]["ok"],
            "sedzia": wynik["sedzia"].get("status"),
            "oferta": wynik["oferta"],
            "log": wynik["log"],
        })

    WYNIKI.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[ZAPIS] {WYNIKI}", flush=True)

    print("\n" + "=" * 78, flush=True)
    print("PODSUMOWANIE (stara -> V2)", flush=True)
    print("=" * 78, flush=True)
    for w in wyniki:
        if w.get("ok"):
            print(f"#{w['id']:>9} | {w['stara_cena']:>6} -> {w['nowa_cena']:>6} zl ({w['delta_pct']:+.0f}%) | {w['title'][:40]}", flush=True)
        else:
            print(f"#{w['id']:>9} | STOP: {w.get('blad')}", flush=True)


if __name__ == "__main__":
    main()