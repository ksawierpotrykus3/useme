# -*- coding: utf-8 -*-
"""
Audyt Jakości Ofert Po Optymalizacji i Odchudzeniu Promptów (De-Overfitting + Anti-Keyword-Stuffing):
1. Re-test Zero-Shot R1 najtrudniejszych zleceń z Fali 1 i 2, które na starym generatorze v4 miały niskie wyniki R1:
   - #144357 (AI do faktur i paragonów -> Comarch Optima; stare R1: 41/100)
   - #143981 (Allegro -> formatki meblowe na wymiar; stare R1: 52/100)
   - #144867 (PHP/MySQL + WAPRO MAG / SQL Server; stare R1: 63/100 — test po usunięciu przykładu WAPRO z promptu 02a!)
2. Pełny test Out-of-Sample (Zero-Shot R1) na zupełnie nowym zleceniu spoza 27 ofert (#143924: Moodle – automatyzacja przydzielania ankiet),
   przepuszczonym przez produkcyjny `SlotChainAIPipeline.filter_offers()` -> `generate_initial_offer()` -> `evaluate_offer_100()`.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KOD_DIR = Path(__file__).resolve().parent.parent.parent / "kod"
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

import config
from ai_pipeline import SlotChainAIPipeline
from audytor_lancuch import (
    audit_and_refine_100,
    evaluate_offer_100,
    generate_initial_offer,
)

OUT_FILE = Path(__file__).resolve().parent / "wyniki_audyt_po_poprawkach.json"
ALL_27_FILE = Path(__file__).resolve().parent / "audyt_100_wyniki_27_ofert.json"


def _load_job_from_magazyn(jid: str) -> dict:
    for p in config.MAGAZYN_DIR.rglob(f"*{jid}*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if str(d.get("id")) == str(jid):
                fd = d.get("full_details") or {}
                ld = d.get("list_details") or {}
                merged = dict(ld)
                merged.update(d)
                merged.update(fd)
                merged["id"] = str(jid)
                return merged
        except Exception:
            pass
    raise FileNotFoundError(f"Nie znaleziono zlecenia #{jid} w magazynie!")


def main() -> None:
    all_27 = json.loads(ALL_27_FILE.read_text(encoding="utf-8"))
    pipeline = SlotChainAIPipeline()

    test_cases = [
        {
            "id": "144357",
            "mode": "retest_wave1_zeroshot",
            "old_r1": 41,
            "sciezka": "inzynieria",
            "typ_klienta": "msp_erp",
            "karta_tech": "tech_02",
            "tier": "A",
            "modyfikatory": [],
        },
        {
            "id": "143981",
            "mode": "retest_wave1_zeroshot",
            "old_r1": 52,
            "sciezka": "biznes",
            "typ_klienta": "tech_agnostic",
            "karta_tech": "tech_16",
            "tier": "B",
            "modyfikatory": [],
        },
        {
            "id": "144867",
            "mode": "retest_deoverfit_wapro",
            "old_r1": 63,
            "sciezka": "inzynieria",
            "typ_klienta": "msp_erp",
            "karta_tech": "tech_06",
            "tier": "A",
            "modyfikatory": ["RESCUE"],
        },
        {
            "id": "143924",
            "mode": "holdout_unseen_e2e",
            "old_r1": None,
        },
    ]

    results = {}
    if OUT_FILE.exists():
        try:
            results = json.loads(OUT_FILE.read_text(encoding="utf-8"))
        except Exception:
            results = {}

    for tc in test_cases:
        jid = tc["id"]
        if jid in results and results[jid].get("final", {}).get("audyt", {}).get("wynik_100", 0) >= 88:
            print(f"[SKIP] #{jid} już przetestowane ({results[jid]['final']['audyt']['wynik_100']}/100 pkt)", flush=True)
            continue

        job = _load_job_from_magazyn(jid)
        if tc["mode"] == "holdout_unseen_e2e":
            print(f"\n=== [HOLDOUT E2E] Selekcja AI #1 dla nowego zlecenia #{jid}: {job.get('title')} ===", flush=True)
            wybrane = pipeline.filter_offers([job])
            if wybrane:
                job = wybrane[0]
            else:
                job.update({"tier": "B", "sciezka": "inzynieria", "typ_klienta": "msp_erp", "karta_tech": "tech_06", "modyfikatory": []})
        else:
            job.update({
                "tier": tc["tier"],
                "sciezka": tc["sciezka"],
                "typ_klienta": tc["typ_klienta"],
                "karta_tech": tc["karta_tech"],
                "modyfikatory": tc["modyfikatory"],
            })

        print(
            f"\n=== [ZERO-SHOT R1 PO OPTYMALIZACJI] #{jid}: {job.get('title')} "
            f"(sciezka={job.get('sciezka')}, typ={job.get('typ_klienta')}, tech={job.get('karta_tech')}) ===",
            flush=True,
        )
        opis_r1, wyc_r1, dni_r1, wyc_raw_r1, res_text = generate_initial_offer(job)
        time.sleep(8)
        audyt_r1 = evaluate_offer_100(job, opis_r1, wyc_r1, dni_r1, wyc_raw_r1)
        score_r1 = int(audyt_r1.get("wynik_100", 0))
        print(
            f" -> [WYNIK ZERO-SHOT R1] #{jid}: {score_r1}/100 pkt "
            f"(stare R1: {tc['old_r1']}, wycena: {wyc_r1} zł / {dni_r1} dni, słów: {audyt_r1.get('words')})",
            flush=True,
        )

        # Jeśli < 92 pkt, odpalamy produkcyjną pętlę naprawczą audit_and_refine_100
        final_opis, final_wyc, final_dni, final_audyt = opis_r1, wyc_r1, dni_r1, audyt_r1
        rounds_used = 1
        if score_r1 < 92:
            print(f" -> [REFINEMENT R2] Wynik R1 ({score_r1}) < 92, uruchamiam pętlę naprawczą...", flush=True)
            ref = audit_and_refine_100(
                job,
                opis_r1,
                wyc_r1,
                dni_r1,
                wycena_raw=wyc_raw_r1,
                research_text=res_text,
                target_score=92,
                max_rounds=1,
            )
            final_opis = ref["opis"]
            final_wyc = ref["wycena"]
            final_dni = ref["dni"]
            final_audyt = ref["audyt_final"]
            rounds_used = ref["rounds"]
            print(f" -> [WYNIK R2] #{jid}: {final_audyt.get('wynik_100')}/100 pkt", flush=True)

        results[jid] = {
            "id": jid,
            "title": job.get("title"),
            "mode": tc["mode"],
            "old_r1_score": tc["old_r1"],
            "klasyfikacja": {
                "tier": job.get("tier"),
                "sciezka": job.get("sciezka"),
                "typ_klienta": job.get("typ_klienta"),
                "karta_tech": job.get("karta_tech"),
                "modyfikatory": job.get("modyfikatory", []),
            },
            "new_zero_shot_r1": {
                "opis": opis_r1,
                "wycena": wyc_r1,
                "dni": dni_r1,
                "audyt": audyt_r1,
            },
            "final": {
                "opis": final_opis,
                "wycena": final_wyc,
                "dni": final_dni,
                "rounds": rounds_used,
                "audyt": final_audyt,
            },
        }
        OUT_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

        # Aktualizacja historycznych wpisów R1 w audyt_100_wyniki_27_ofert.json dla re-testowanych ofert Fali 1/2
        if jid in all_27:
            all_27[jid]["runda_1_zero_shot_post_fix"] = {
                "opis": opis_r1,
                "wycena": wyc_r1,
                "dni": dni_r1,
                "audyt": audyt_r1,
            }
            if int(final_audyt.get("wynik_100", 0)) >= int(all_27[jid]["runda_2"]["audyt"].get("wynik_100", 0)):
                all_27[jid]["runda_2"] = {
                    "opis": final_opis,
                    "wycena": final_wyc,
                    "dni": final_dni,
                    "audyt": final_audyt,
                }
            ALL_27_FILE.write_text(json.dumps(all_27, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== ZAKOŃCZONO AUDYT JAKOŚCI OFERT PO OPTYMALIZACJI ===", flush=True)


if __name__ == "__main__":
    main()
