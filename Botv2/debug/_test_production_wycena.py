# -*- coding: utf-8 -*-
"""Weryfikacja produkcyjnego modułu wycena_debata.py i routingu brain.py."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path("Botv2/mozg").resolve()))
from brain import call_ai, call_gemini
from wycena_debata import wycen_przez_debate

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

z = json.loads(open("badania/baza/weronikabuchholc13/04_moje_zlecenia/145285/zlecenie.json", encoding="utf-8").read())
tresc = z.get("description") or z.get("opis")

print("--- START PRODUKCYJNEJ WYCENY DEBATOWEJ (DeepSeek vs Gemini) ---")
res = wycen_przez_debate(
    tresc_zlecenia=tresc,
    dziennik="Testowy dziennik: integracja 40k SKU, Subiekt, BaseLinker, silent-guard.",
    call_wyceniacz_fn=call_ai,
    call_reviewer_fn=call_gemini,
    say=print,
    max_rundy=2,
)

print("\n--- WYNIK KOŃCOWY ---")
print(json.dumps(res, ensure_ascii=False, indent=2))
