# -*- coding: utf-8 -*-
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
KOD = ROOT / "kod"
sys.path.insert(0, str(KOD))

from audytor_lancuch import (
    evaluate_offer_100,
    regenerate_from_judge_feedback,
)
from run_audyt_wave2 import build_warehouse_index
from run_audyt_wave3 import WAVE3_SPECS

SCRATCH = Path(__file__).parent
OUT_PATH = SCRATCH / "audyt_100_wyniki.json"


def main():
    index = build_warehouse_index()
    out_data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    spec_map = {s[0]: s for s in WAVE3_SPECS}

    for jid in ("144411", "144579"):
        rec = out_data[jid]
        _, tier, sciezka, typ_klienta, karta_tech, modyfikatory = spec_map[jid]
        job = index[jid]
        job["tier"] = tier
        job["sciezka"] = sciezka
        job["typ_klienta"] = typ_klienta
        job["karta_tech"] = karta_tech
        job["modyfikatory"] = modyfikatory

        prev_r = rec.get("runda_2") or rec["runda_1"]
        prev_wycena_raw = prev_r.get("wycena_raw", "")
        if jid == "144411":
            # Przywracamy wycenę 8000 zł / 17 dni z Rundy 1 (którą fałszywy alarm efektywna_stawka kazał obniżyć do 7000 zł)
            prev_wycena_raw = "[WYNIK_KONCOWY]\nKWOTA: 8000\nDNI: 17\n[/WYNIK_KONCOWY]\n"
            prev_r["audyt"]["popraw_wycena"] = ""

        print(f"\n============================================================", flush=True)
        print(f"[DOGRYWKA RUNDA 3] #{jid}: {rec['title']} (poprzedni wynik: {rec['final_score']}/100)", flush=True)
        print(f"============================================================", flush=True)

        nowy_opis, nowa_wycena, nowe_dni, nowy_wycena_raw = regenerate_from_judge_feedback(
            job,
            prev_r["opis"],
            prev_wycena_raw,
            "BRAK_ISTOTNYCH_FAKTOW",
            prev_r["audyt"],
        )
        print(f"\n[NOWA OFERTA #{jid} (RUNDA 3)] Wycena: {nowa_wycena} zł / {nowe_dni} dni ({len(nowy_opis.split())} słów):", flush=True)
        print("-" * 50, flush=True)
        print(nowy_opis, flush=True)
        print("-" * 50, flush=True)

        time.sleep(8)
        audyt3 = evaluate_offer_100(job, nowy_opis, nowa_wycena, nowe_dni, nowy_wycena_raw)
        s3 = int(audyt3.get("wynik_100", 0))
        print(f"-> OCENA RUNDA 3 #{jid}: {s3}/100 pkt (zmiana: {rec['final_score']} -> {s3}) | Kategorie: {audyt3.get('kategorie')}", flush=True)
        for p in audyt3.get("za_co_dodano", []):
            print(f"   [+] {p.get('punkty')}: {p.get('uzasadnienie')}", flush=True)
        for m in audyt3.get("za_co_odjeto", []):
            print(f"   [-] {m.get('punkty')}: [{m.get('cytat')}] -> {m.get('uzasadnienie')}", flush=True)

        rec["runda_3"] = {
            "wycena": nowa_wycena,
            "dni": nowe_dni,
            "words": len(nowy_opis.split()),
            "opis": nowy_opis,
            "wycena_raw": nowy_wycena_raw,
            "audyt": audyt3,
        }
        if s3 >= rec["final_score"]:
            rec["final_score"] = s3
            rec["final_opis"] = nowy_opis
            rec["final_wycena"] = nowa_wycena
            rec["final_dni"] = nowe_dni
            OUT_PATH.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(8)

    print("\n=== PODSUMOWANIE WSZYSTKICH 19 OFERT (16/16 KART TECH) ===", flush=True)
    for idx, (k, r) in enumerate(out_data.items(), 1):
        r1 = r["runda_1"]["audyt"]["wynik_100"]
        fin = r["final_score"]
        opis_f = r.get("final_opis") or r.get("opis_final") or ""
        wyc_f = r.get("final_wycena") or r.get("wycena_final") or 0
        dni_f = r.get("final_dni") or r.get("dni_final") or 0
        karta = r.get("karta_tech") or r.get("karta") or ""
        words = len(opis_f.split())
        print(
            f"{idx:2d}. #{str(k):7s} | {karta:7s} | {r['sciezka']:10s} | "
            f"R1: {r1:2d} -> Final: {fin:2d}/100 | {int(wyc_f):5d} zł / {int(dni_f):2d} dni | "
            f"{words:3d} słów | {r['title'][:52]}",
            flush=True,
        )


if __name__ == "__main__":
    main()
