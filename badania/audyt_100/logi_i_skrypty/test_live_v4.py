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

from storage import clear_checkpoint
from ai_pipeline import SlotChainAIPipeline
from chain_executor import _resolve_tech_cards

JOBS_DIR = ROOT / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it"
JOB_IDS = ["143981", "144165", "144092", "144357"]


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
    out_all = Path(__file__).parent / "wyniki_live_v4.json"
    results = {}
    if out_all.exists():
        try:
            results = json.loads(out_all.read_text(encoding="utf-8"))
        except Exception:
            results = {}

    for jid in JOB_IDS:
        clear_checkpoint(jid)

    jobs = [load_real_job(jid) for jid in JOB_IDS]
    pipeline = SlotChainAIPipeline()

    print("=== KROK 1: SELEKCJA AI #1 (filter_offers) ===", flush=True)
    selected = pipeline.filter_offers(jobs)
    selected_map = {str(o["id"]): o for o in selected}

    for jid in JOB_IDS:
        job = selected_map.get(jid)
        if not job:
            job = next(j for j in jobs if j["id"] == jid)
        cards_02a = _resolve_tech_cards(job, "02a")
        print(
            f"\n============================================================\n"
            f"START GENEROWANIA #{jid}: {job['title']}\n"
            f"Tier={job.get('tier')} | sciezka={job.get('sciezka')} | typ_klienta={job.get('typ_klienta')} | "
            f"karta_tech={job.get('karta_tech')} | modyfikatory={job.get('modyfikatory')} | resolved_02a={cards_02a}\n"
            f"============================================================",
            flush=True,
        )
        t0 = time.time()
        prop = pipeline.generate_proposal(job)
        dt = time.time() - t0
        words = len(prop.opis.split())
        chars = len(prop.opis)
        print(f"\n[WYNIK #{jid}] ({dt:.1f}s) Wycena: {prop.wycena} zł | Dni: {prop.dni} | Słów: {words} | Znaków: {chars}", flush=True)
        print("-" * 60, flush=True)
        print(prop.opis, flush=True)
        print("-" * 60, flush=True)

        results[jid] = {
            "id": jid,
            "title": job["title"],
            "tier": job.get("tier"),
            "sciezka": job.get("sciezka"),
            "typ_klienta": job.get("typ_klienta"),
            "karta_tech": job.get("karta_tech"),
            "modyfikatory": job.get("modyfikatory"),
            "resolved_cards_02a": cards_02a,
            "wycena": prop.wycena,
            "dni": prop.dni,
            "words": words,
            "chars": chars,
            "opis": prop.opis,
            "wycena_raw": (prop.metadata or {}).get("wycena_dni", ""),
        }
        out_all.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nZapisano pełne wyniki (łącznie {len(results)} ofert) do: {out_all}", flush=True)


if __name__ == "__main__":
    main()
