# -*- coding: utf-8 -*-
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
KOD = ROOT / "kod"
sys.path.insert(0, str(KOD))

from ai_pipeline import SlotChainAIPipeline
from audytor_lancuch import (
    evaluate_offer_100,
    generate_initial_offer,
    regenerate_from_judge_feedback,
)

SCRATCH = Path(__file__).parent
OUT_PATH = SCRATCH / "audyt_100_wyniki.json"


def build_warehouse_index() -> dict:
    all_jobs = {}
    baza_dir = ROOT / "badania" / "baza"
    for p in baza_dir.rglob("*.json"):
        if "zlecenie_testowe_144890" in str(p) or p.stat().st_size > 200000:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8-sig"))
            if not isinstance(d, dict):
                continue
            fd = d.get("full_details") or {}
            ld = d.get("list_details") or {}
            f_inner = d.get("fields") or {}
            title = d.get("title") or fd.get("title") or ld.get("title") or f_inner.get("title") or ""
            desc = (
                d.get("full_description")
                or fd.get("full_description")
                or d.get("description")
                or f_inner.get("description")
                or ""
            )
            jid = str(d.get("id") or "")
            if not jid:
                m = re.search(r"(\d{6})", str(p))
                jid = m.group(1) if m else p.stem
            if len(desc) >= 150:
                budget = d.get("budget") or ld.get("budget") or "Do negocjacji"
                all_jobs[jid] = {
                    "id": jid,
                    "title": title,
                    "budget": budget,
                    "category": ld.get("category", "Programowanie i IT"),
                    "full_description": desc,
                    "competitors_count": len(fd.get("competitors") or []) or 12,
                    "fields": {
                        "title": title,
                        "description": desc,
                        "budget": budget,
                        "author": "Klient B2B",
                        "competitors_count": len(fd.get("competitors") or []) or 12,
                    },
                }
        except Exception:
            pass

    for fname in [
        "badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json",
        "badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json",
    ]:
        items = json.loads((ROOT / fname).read_text(encoding="utf-8-sig"))
        for it in items:
            jid = str(it.get("job_id") or it.get("offer_id") or "")
            title = it.get("title") or ""
            desc = (
                it.get("job_description")
                or (it.get("job_details") or {}).get("description")
                or it.get("description")
                or ""
            )
            if jid and len(desc) >= 150 and jid not in all_jobs:
                budget = it.get("budget") or "Do negocjacji"
                all_jobs[jid] = {
                    "id": jid,
                    "title": title,
                    "budget": budget,
                    "category": it.get("category") or "Programowanie i IT",
                    "full_description": desc,
                    "competitors_count": 12,
                    "fields": {
                        "title": title,
                        "description": desc,
                        "budget": budget,
                        "author": "Klient B2B",
                        "competitors_count": 12,
                    },
                }
    return all_jobs


WAVE2_SPECS = [
    ("144951", "A", "inzynieria", "ekspert_dziedzinowy", "tech_15", []),
    ("144645", "A", "inzynieria", "agencja", "tech_08", ["RESCUE"]),
    ("144737", "A", "inzynieria", "msp_erp", "tech_09", ["RESCUE"]),
    ("2586109", "A", "inzynieria", "ecommerce", "tech_03", []),
    ("139571", "A", "inzynieria", "msp_erp", "tech_13", []),
    ("132598", "A", "inzynieria", "msp_erp", "tech_12", []),
]


def main():
    index = build_warehouse_index()
    out_data = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}

    for jid, tier, sciezka, typ_klienta, karta_tech, modyfikatory in WAVE2_SPECS:
        if jid in out_data and out_data[jid].get("final_score", 0) >= 94:
            print(f"[SKIP] #{jid} już w bazie z wynikiem {out_data[jid]['final_score']}/100", flush=True)
            continue

        job = index.get(jid)
        if not job:
            print(f"[WARN] Nie znaleziono #{jid} w magazynie!", flush=True)
            continue

        job["tier"] = tier
        job["sciezka"] = sciezka
        job["typ_klienta"] = typ_klienta
        job["karta_tech"] = karta_tech
        job["modyfikatory"] = modyfikatory

        print(f"\n============================================================", flush=True)
        print(f"[GENEROWANIE + AUDYT RUNDA 1] #{jid}: {job['title']} (karta={karta_tech}, sciezka={sciezka})", flush=True)
        print(f"============================================================", flush=True)

        opis_r1, wycena_r1, dni_r1, wycena_raw_r1, research_txt = generate_initial_offer(job)
        print(f"\n[OFERTA RUNDA 1 #{jid}] Wycena: {wycena_r1} zł / {dni_r1} dni ({len(opis_r1.split())} słów):", flush=True)
        print("-" * 50, flush=True)
        print(opis_r1, flush=True)
        print("-" * 50, flush=True)

        time.sleep(8)
        audyt_r1 = evaluate_offer_100(job, opis_r1, wycena_r1, dni_r1, wycena_raw_r1)
        score_r1 = int(audyt_r1.get("wynik_100", 0))
        print(f"-> OCENA RUNDA 1: {score_r1}/100 pkt | Kategorie: {audyt_r1.get('kategorie')}", flush=True)
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

        if score_r1 < 95 and audyt_r1.get("za_co_odjeto"):
            print(f"\n[REFINEMENT #{jid}] Wynik {score_r1}/100 -> Uruchamiam pętlę naprawczą na bazie uwag Krytyka...", flush=True)
            opis_r2, wycena_r2, dni_r2, wycena_raw_r2 = regenerate_from_judge_feedback(
                job, opis_r1, wycena_raw_r1, research_txt, audyt_r1
            )
            print(f"\n[NOWA OFERTA #{jid} (RUNDA 2)] Wycena: {wycena_r2} zł / {dni_r2} dni ({len(opis_r2.split())} słów):", flush=True)
            print("-" * 50, flush=True)
            print(opis_r2, flush=True)
            print("-" * 50, flush=True)

            time.sleep(8)
            audyt_r2 = evaluate_offer_100(job, opis_r2, wycena_r2, dni_r2, wycena_raw_r2)
            score_r2 = int(audyt_r2.get("wynik_100", 0))
            print(f"-> OCENA RUNDA 2: {score_r2}/100 pkt (zmiana: {score_r1} -> {score_r2}) | Kategorie: {audyt_r2.get('kategorie')}", flush=True)
            for p in audyt_r2.get("za_co_dodano", []):
                print(f"   [+] {p.get('punkty')}: {p.get('uzasadnienie')}", flush=True)
            for m in audyt_r2.get("za_co_odjeto", []):
                print(f"   [-] {m.get('punkty')}: [{m.get('cytat')}] -> {m.get('uzasadnienie')}", flush=True)

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

    print(f"\nZakończono Fale 2 (łącznie {len(out_data)} przetestowanych i ocenionych ofert w {OUT_PATH})!", flush=True)


if __name__ == "__main__":
    main()
