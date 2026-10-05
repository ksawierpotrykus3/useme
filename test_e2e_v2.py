# -*- coding: utf-8 -*-
"""End-to-end test wpiecia mozgu V2 w stary pipeline - BEZ WYSYLKI.

Sprawdza dokladnie to, co robi engine.py:
  1. Storage().load_job(job_id)   -> dict zlecenia z magazynu
  2. get_ai_pipeline()            -> fabryka (teraz zwraca MozgV2Pipeline)
  3. ai.generate_proposal(job)    -> ProposalResult (opis, wycena, dni)
  4. walidacja kontraktu form_driver: opis<=6000, wycena int>0, dni>=7

Nie odpala przegladarki, nie wysyla nic. Czysty test generowania.

Uzycie:
    python test_e2e_v2.py 2897327
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CORE = Path(__file__).parent
KOD = CORE / "kod"
sys.path.insert(0, str(KOD))

import config  # noqa: E402
from storage import Storage  # noqa: E402
from ai_pipeline import get_ai_pipeline, ProposalResult  # noqa: E402


def main():
    ids = [a for a in sys.argv[1:] if len(a) >= 5]
    if not ids:
        print("Uzycie: python test_e2e_v2.py <job_id>")
        return

    print(f"[CONFIG] USE_MOZG_V2 = {getattr(config, 'USE_MOZG_V2', None)}")
    print(f"[CONFIG] DRY_RUN = {config.DRY_RUN}")

    storage = Storage()
    ai = get_ai_pipeline()
    print(f"[PIPELINE] {type(ai).__name__}\n")

    for jid in ids:
        print("=" * 78, flush=True)
        print(f"E2E #{jid}", flush=True)
        print("=" * 78, flush=True)

        job = storage.load_job(jid)
        if not job:
            print(f"[BRAK] #{jid} nie ma w magazynie (Storage.load_job zwrocil None)")
            continue

        fd = job.get("full_details") or {}
        desc = job.get("full_description") or fd.get("full_description") or job.get("short_desc") or ""
        print(f"[JOB] title={job.get('title', '')[:60]!r} | budzet={job.get('budget')!r}")
        print(f"[JOB] dlugosc opisu={len(desc)} znakow\n")

        # --- KROK 1: fabryka zwraca V2 ---
        assert isinstance(ai, object), "brak pipeline"
        print("[1] Fabryka zwrocila:", type(ai).__name__, flush=True)

        # --- KROK 2: generowanie (dokladnie jak engine.py:392) ---
        print("[2] generate_proposal...", flush=True)
        try:
            prop = ai.generate_proposal(job)
        except Exception as e:
            print(f"[BLAD] generate_proposal: {e}")
            continue

        # --- KROK 3: walidacja kontraktu ProposalResult (to co form_driver czyta) ---
        print("\n[3] Kontrakt form_driver:")
        ok = True
        if not isinstance(prop, ProposalResult):
            print(f"  FAIL: nie ProposalResult, tylko {type(prop)}")
            ok = False
        if not (prop.opis or "").strip():
            print("  FAIL: opis pusty")
            ok = False
        if len(prop.opis) > config.MAX_OPIS_DLUGOSC:
            print(f"  FAIL: opis {len(prop.opis)} > {config.MAX_OPIS_DLUGOSC}")
            ok = False
        if not isinstance(prop.wycena, int) or prop.wycena <= 0:
            print(f"  FAIL: wycena={prop.wycena!r}")
            ok = False
        if not isinstance(prop.dni, int) or prop.dni < 7:
            print(f"  FAIL: dni={prop.dni!r} < 7")
            ok = False

        print(f"  opis:   {len(prop.opis)} znakow")
        print(f"  wycena: {prop.wycena} zl (int={isinstance(prop.wycena, int)})")
        print(f"  dni:    {prop.dni} (>=7: {prop.dni >= 7})")
        print(f"  powod:  {prop.powod_wyboru}")
        print(f"  meta:   {prop.metadata}")

        print("\n[4] OFERTA:\n")
        print(prop.opis)

        print("\n" + "-" * 78)
        print(f"[E2E #{jid}] {'OK - kontrakt spelniony' if ok else 'PROBLEMY - patrz FAIL wyzej'}")
        print("-" * 78, flush=True)


if __name__ == "__main__":
    main()