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
    generate_initial_offer,
    regenerate_from_judge_feedback,
)
from run_audyt_wave2 import build_warehouse_index

SCRATCH = Path(__file__).parent
OUT_PATH = SCRATCH / "audyt_100_wyniki.json"

# 1. Część A: Dogrywka 6 ofert, które w poprzednich falach miały 89-91/100
REFINE_SPECS = [
    ("144867", "A", "inzynieria", "ekspert_dziedzinowy", "tech_06", []),
    ("144951", "A", "inzynieria", "ekspert_dziedzinowy", "tech_15", []),
    ("144411", "A", "inzynieria", "ecommerce", "tech_03", []),
    ("144737", "A", "inzynieria", "ecommerce", "tech_09", ["RESCUE"]),
    ("2586109", "A", "inzynieria", "ecommerce", "tech_03", []),
    ("144817", "B", "biznes", "msp_erp", "tech_16", []),
]

# 2. Część B: 4 zupełnie nowe zlecenia z magazynu (test Zero-Shot Runda 1 "same z siebie")
NEW_WAVE4_SPECS = [
    ("143979", "A", "inzynieria", "msp_erp", "tech_02", []),
    ("144188", "A", "inzynieria", "msp_erp", "tech_02", []),
    ("144077", "A", "inzynieria", "agencja", "tech_04", []),
    ("144249", "B", "biznes", "tech_agnostic", "tech_16", []),
]


def main():
    index = build_warehouse_index()
    out_data = json.loads(OUT_PATH.read_text(encoding="utf-8"))

    print("======================================================================", flush=True)
    print("CZĘŚĆ A: DOGRYWKA 6 OFERT Z WYNIKIEM 89-91/100 PO AKTUALIZACJI PROMPTÓW", flush=True)
    print("======================================================================", flush=True)

    for jid, tier, sciezka, typ_klienta, karta_tech, modyfikatory in REFINE_SPECS:
        rec = out_data.get(jid)
        if not rec:
            continue
        job = index.get(jid)
        if not job:
            continue
        job["tier"] = tier
        job["sciezka"] = sciezka
        job["typ_klienta"] = typ_klienta
        job["karta_tech"] = karta_tech
        job["modyfikatory"] = modyfikatory

        prev_r = rec.get("runda_3") or rec.get("runda_2") or rec["runda_1"]
        prev_opis = prev_r["opis"]
        prev_audyt = dict(prev_r["audyt"])

        # Specjalna korekta dla 2586109 (przywrócenie właściwej wyceny 32000 zł / 55 dni z Rundy 1)
        if jid == "2586109":
            prev_opis = rec["runda_1"]["opis"]
            prev_audyt = dict(rec["runda_1"]["audyt"])
            prev_audyt["popraw_wycena"] = ""
            prev_wycena_raw = "[WYNIK_KONCOWY]\nKWOTA: 32000\nDNI: 55\n[/WYNIK_KONCOWY]\n"
        elif jid == "144411":
            prev_audyt["popraw_wycena"] = ""
            prev_wycena_raw = "[WYNIK_KONCOWY]\nKWOTA: 11500\nDNI: 24\n[/WYNIK_KONCOWY]\n"
        elif jid == "144951":
            prev_audyt["popraw_wycena"] = ""
            prev_wycena_raw = "[WYNIK_KONCOWY]\nKWOTA: 15000\nDNI: 33\n[/WYNIK_KONCOWY]\n"
        else:
            prev_wycena_raw = prev_r.get("wycena_raw", "")
            prev_audyt["popraw_wycena"] = ""

        print(f"\n[DOGRYWKA #{jid}] {rec['title']} (obecny wynik: {rec['final_score']}/100)", flush=True)
        nowy_opis, nowa_wycena, nowe_dni, nowy_wycena_raw = regenerate_from_judge_feedback(
            job,
            prev_opis,
            prev_wycena_raw,
            "BRAK_ISTOTNYCH_FAKTOW",
            prev_audyt,
        )
        print(f"[NOWA OFERTA #{jid}] Wycena: {nowa_wycena} zł / {nowe_dni} dni ({len(nowy_opis.split())} słów):", flush=True)
        print("-" * 50, flush=True)
        print(nowy_opis, flush=True)
        print("-" * 50, flush=True)

        time.sleep(8)
        audyt_new = evaluate_offer_100(job, nowy_opis, nowa_wycena, nowe_dni, nowy_wycena_raw)
        score_new = int(audyt_new.get("wynik_100", 0))
        print(f"-> OCENA PO POPRAWCE #{jid}: {score_new}/100 pkt (zmiana: {rec['final_score']} -> {score_new}) | Kategorie: {audyt_new.get('kategorie')}", flush=True)
        for p in audyt_new.get("za_co_dodano", []):
            print(f"   [+] {p.get('punkty')}: {p.get('uzasadnienie')}", flush=True)
        for m in audyt_new.get("za_co_odjeto", []):
            print(f"   [-] {m.get('punkty')}: [{m.get('cytat')}] -> {m.get('uzasadnienie')}", flush=True)

        rec["runda_final"] = {
            "wycena": nowa_wycena,
            "dni": nowe_dni,
            "words": len(nowy_opis.split()),
            "opis": nowy_opis,
            "wycena_raw": nowy_wycena_raw,
            "audyt": audyt_new,
        }
        if score_new >= rec["final_score"]:
            rec["final_score"] = score_new
            rec["final_opis"] = nowy_opis
            rec["final_wycena"] = nowa_wycena
            rec["final_dni"] = nowe_dni
            OUT_PATH.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(8)

    print("\n======================================================================", flush=True)
    print("CZĘŚĆ B: TEST ZERO-SHOT (RUNDA 1 'SAME Z SIEBIE') NA 4 NOWYCH ZLECENIACH", flush=True)
    print("======================================================================", flush=True)

    for jid, tier, sciezka, typ_klienta, karta_tech, modyfikatory in NEW_WAVE4_SPECS:
        job = index.get(jid)
        if not job:
            continue
        job["tier"] = tier
        job["sciezka"] = sciezka
        job["typ_klienta"] = typ_klienta
        job["karta_tech"] = karta_tech
        job["modyfikatory"] = modyfikatory

        print(f"\n[FALA 4 ZERO-SHOT RUNDA 1] #{jid}: {job['title']} (karta={karta_tech}, sciezka={sciezka})", flush=True)
        opis_r1, wycena_r1, dni_r1, wycena_raw_r1, research_txt = generate_initial_offer(job)
        print(f"\n[OFERTA RUNDA 1 (BEZ POPRAWEK!) #{jid}] Wycena: {wycena_r1} zł / {dni_r1} dni ({len(opis_r1.split())} słów):", flush=True)
        print("-" * 50, flush=True)
        print(opis_r1, flush=True)
        print("-" * 50, flush=True)

        time.sleep(8)
        audyt_r1 = evaluate_offer_100(job, opis_r1, wycena_r1, dni_r1, wycena_raw_r1)
        score_r1 = int(audyt_r1.get("wynik_100", 0))
        print(f"-> OCENA RUNDA 1 (ZERO-SHOT) #{jid}: {score_r1}/100 pkt | Kategorie: {audyt_r1.get('kategorie')}", flush=True)
        for p in audyt_r1.get("za_co_dodano", []):
            print(f"   [+] {p.get('punkty')}: {p.get('uzasadnienie')}", flush=True)
        for m in audyt_r1.get("za_co_odjeto", []):
            print(f"   [-] {m.get('punkty')}: [{m.get('cytat')}] -> {m.get('uzasadnienie')}", flush=True)

        record = {
            "id": jid,
            "title": job["title"],
            "sciezka": sciezka,
            "typ_klienta": typ_klienta,
            "karta_tech": karta_tech,
            "runda_1": {
                "wycena": wycena_r1,
                "dni": dni_r1,
                "words": len(opis_r1.split()),
                "opis": opis_r1,
                "audyt": audyt_r1,
            },
            "final_score": score_r1,
            "final_opis": opis_r1,
            "final_wycena": wycena_r1,
            "final_dni": dni_r1,
        }

        if score_r1 < 94 and audyt_r1.get("za_co_odjeto"):
            print(f"\n[REFINEMENT #{jid}] Wynik {score_r1}/100 -> Uruchamiam pętlę naprawczą...", flush=True)
            opis_r2, wycena_r2, dni_r2, wycena_raw_r2 = regenerate_from_judge_feedback(
                job, opis_r1, wycena_raw_r1, research_txt, audyt_r1
            )
            time.sleep(8)
            audyt_r2 = evaluate_offer_100(job, opis_r2, wycena_r2, dni_r2, wycena_raw_r2)
            score_r2 = int(audyt_r2.get("wynik_100", 0))
            print(f"-> OCENA RUNDA 2 #{jid}: {score_r2}/100 pkt (zmiana: {score_r1} -> {score_r2})", flush=True)
            record["runda_2"] = {
                "wycena": wycena_r2,
                "dni": dni_r2,
                "words": len(opis_r2.split()),
                "opis": opis_r2,
                "wycena_raw": wycena_raw_r2,
                "audyt": audyt_r2,
            }
            if score_r2 >= score_r1:
                record["final_score"] = score_r2
                record["final_opis"] = opis_r2
                record["final_wycena"] = wycena_r2
                record["final_dni"] = dni_r2

        out_data[jid] = record
        OUT_PATH.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(8)

    print("\n=== TABELA WSZYSTKICH 23 OFERT PO FALI 4 ===", flush=True)
    scores = [int(r["final_score"]) for r in out_data.values()]
    print(f"Średnia końcowa wszystkich {len(scores)} ofert: {sum(scores)/len(scores):.1f} / 100 pkt", flush=True)
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
            f"{words:3d} słów | {r['title'][:50]}",
            flush=True,
        )


if __name__ == "__main__":
    main()
