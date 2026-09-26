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

from audytor_lancuch import evaluate_offer_100, regenerate_from_judge_feedback
from ai_pipeline import SlotChainAIPipeline
from chain_executor import _resolve_tech_cards

SCRATCH = Path(__file__).parent
V4_PATH = SCRATCH / "wyniki_live_v4.json"
OUT_PATH = SCRATCH / "audyt_100_wyniki.json"
JOBS_DIR = ROOT / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it"


def load_real_job(jid: str) -> dict:
    raw = json.loads((JOBS_DIR / f"{jid}.json").read_text(encoding="utf-8-sig"))
    full_det = raw.get("full_details") or {}
    list_det = raw.get("list_details") or {}
    title = raw.get("title") or full_det.get("title") or list_det.get("title") or ""
    desc = (
        raw.get("full_description")
        or full_det.get("full_description")
        or raw.get("description")
        or list_det.get("short_desc")
        or ""
    )
    budget = raw.get("budget") or list_det.get("budget") or "Do negocjacji"
    author = full_det.get("author") or list_det.get("author") or ""
    if "wer13" in author.lower():
        author = "Firma Handlowo-Produkcyjna"
    competitors_count = len(full_det.get("competitors") or []) or 15
    return {
        "id": str(jid),
        "title": title,
        "budget": budget,
        "category": list_det.get("category", "Programowanie i IT"),
        "full_description": desc,
        "competitors_count": competitors_count,
        "fields": {
            "title": title,
            "description": desc,
            "budget": budget,
            "author": author,
            "competitors_count": competitors_count,
        },
    }


def main():
    v4_data = json.loads(V4_PATH.read_text(encoding="utf-8")) if V4_PATH.exists() else {}
    out_data = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}

    # Kolejność: najpierw te które miały najwięcej do poprawy (144357, 144092, 144817, 144890, 143981, 144165, 144867),
    # oraz nowe zlecenia z magazynu z innych technologii (144951 - AI DGX/RAG, 144645 - DevOps/Docker, 144579 - Python/BigQuery)
    target_ids = [
        "144357",  # tech_16 (Allegro produkcja mebli na wymiar)
        "144092",  # tech_10 + RESCUE (Konfigurator 3D Three.js)
        "144817",  # tech_16 (Bot do maili firmowych AI)
        "144890",  # tech_02 + tech_04 (Comarch Optima + AI OCR)
        "143981",  # tech_16 / API (CloudTalk -> Notion)
        "144165",  # tech_11 (CNC Punch Software EN)
        "144867",  # tech_06 + tech_05 (Aplikacja mobilna dla fizjoterapeutów)
    ]

    for jid in target_ids:
        if jid in out_data and out_data[jid].get("final_score", 0) >= 95:
            print(f"[SKIP] #{jid} już osiągnęło {out_data[jid]['final_score']}/100", flush=True)
            continue

        job = load_real_job(jid)
        prev = v4_data.get(jid, {})
        job["tier"] = prev.get("tier", "A")
        job["sciezka"] = prev.get("sciezka", "inzynieria")
        job["typ_klienta"] = prev.get("typ_klienta", "msp_erp")
        job["karta_tech"] = prev.get("karta_tech", "tech_04")
        job["modyfikatory"] = prev.get("modyfikatory") or ([] if jid != "144092" else ["RESCUE"])

        opis_r1 = prev.get("opis", "")
        wycena_r1 = int(prev.get("wycena", 3000))
        dni_r1 = int(prev.get("dni", 7))
        wycena_raw_r1 = prev.get("wycena_raw", "")

        print(f"\n============================================================", flush=True)
        print(f"[AUDYT RUNDA 1] #{jid}: {job['title']} (sciezka={job['sciezka']}, karta={job['karta_tech']})", flush=True)
        print(f"============================================================", flush=True)

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
            "sciezka": job["sciezka"],
            "typ_klienta": job["typ_klienta"],
            "karta_tech": job["karta_tech"],
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

        if score_r1 < 95 or audyt_r1.get("za_co_odjeto"):
            print(f"\n[REFINEMENT #{jid}] Wynik {score_r1}/100 -> Uruchamiam pętlę naprawczą na bazie uwag Krytyka...", flush=True)
            opis_r2, wycena_r2, dni_r2, wycena_raw_r2 = regenerate_from_judge_feedback(
                job, opis_r1, wycena_raw_r1, "", audyt_r1
            )
            print(f"\n[NOWA OFERTA #{jid} (RUNDA 2)] Wycena: {wycena_r2} zł / {dni_r2} dni ({len(opis_r2.split())} słów):", flush=True)
            print("-" * 50, flush=True)
            print(opis_r2, flush=True)
            print("-" * 50, flush=True)

            time.sleep(10)
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
            record["final_score"] = score_r2
            record["final_opis"] = opis_r2
            record["final_wycena"] = wycena_r2
            record["final_dni"] = dni_r2

        out_data[jid] = record
        OUT_PATH.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(10)

    print(f"\nZakończono audyt i optymalizację 1-100! Wyniki w: {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
