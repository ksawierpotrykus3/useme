# -*- coding: utf-8 -*-
"""Test PRODUKCYJNEJ debaty single-model (DeepSeek x DeepSeek, prompt z widełkami).

Cel: uczciwe porównanie z eksperymentem cross-model (eksperyment_debata_dwumodelowa.json).
Uruchamia DOKŁADNIE tę samą ścieżkę co brain.py: wycen_przez_debate(call_ai_fn=call_ai).
Zapisuje pełny log (kwoty, uzasadnienia, krytyka reviewera, rundy) do Botv2/debug/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent          # .../useme_core/Botv2
sys.path.insert(0, str(ROOT / "mozg"))

from wycena_debata import wycen_przez_debate      # noqa: E402
from brain import call_ai, MODEL                   # noqa: E402

print(f"MODEL produkcyjny = {MODEL} (oba głosy przez ten sam call_ai)")

BAZA = ROOT.parent / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia"

ZLECENIA = [
    ("145285", "145285 Subiekt <-> BaseLinker (40k produktów)", BAZA / "145285" / "zlecenie.json"),
    ("145287", "145287 Aplikacja mobilna offline (kierowcy/serwis)", BAZA / "145287" / "zlecenie.json"),
    ("144890", "144890 Automatyzacja faktur OCR + Optima", BAZA / "zlecenie_testowe_144890" / "zlecenie.json"),
]


def main():
    wyniki = []
    for job_id, nazwa, plik in ZLECENIA:
        dane = json.loads(plik.read_text(encoding="utf-8"))
        tresc = dane.get("description") or dane.get("opis", "")

        print("\n" + "=" * 80)
        print(f"SINGLE-MODEL DEBATA: {nazwa}")
        print("=" * 80)

        logi = []
        wynik = wycen_przez_debate(
            tresc_zlecenia=tresc,
            dziennik="",
            research="",
            call_ai_fn=call_ai,
            say=lambda m: (logi.append(m), print(m)),
            max_rundy=2,
        )

        wyniki.append({
            "job_id": job_id,
            "nazwa": nazwa,
            "model_wyceniacza": MODEL,
            "model_reviewera": MODEL,
            "kwota_finalna": wynik.get("kwota"),
            "dni_od": wynik.get("dni_od"),
            "dni_do": wynik.get("dni_do"),
            "typ": wynik.get("typ"),
            "werdykt_reviewera": wynik.get("reviewer_werdykt"),
            "uwagi_reviewera": wynik.get("reviewer_uwagi"),
            "widelki_rynkowe": wynik.get("widełki_rynkowe"),
            "rundy": wynik.get("rundy"),
            "rozbicie": wynik.get("rozbicie"),
            "log_say": logi,
        })

    out_dir = ROOT / "debug"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "test_single_model_3_zlecenia.json"
    out_file.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 80)
    print("PODSUMOWANIE SINGLE-MODEL")
    print("=" * 80)
    for w in wyniki:
        print(f"  {w['job_id']}: {w['kwota_finalna']} zł | {w['dni_od']}-{w['dni_do']} dni "
              f"| reviewer: {w['werdykt_reviewera']} | rundy: {w['rundy']}")
    print(f"\nPEŁNY LOG: {out_file}")


if __name__ == "__main__":
    main()