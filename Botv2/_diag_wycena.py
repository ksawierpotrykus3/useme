# -*- coding: utf-8 -*-
"""Diagnoza: co model zwraca do kalkulatora przy TYM SAMYM zleceniu, 3x pod rzad."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
sys.path.insert(0, str(Path(__file__).parent.parent / "kod"))

import config
from brain import call_ai, _tresc_zlecenia, PROMPT_WYCENA, _wyciagnij_json_blok
from kalkulator import policz_wycene

# zlecenie 144249
p = list(config.MAGAZYN_DIR.rglob("144249.json"))[0]
z = json.loads(p.read_text(encoding="utf-8"))
tresc = _tresc_zlecenia(z)

print("=== ZLECENIE ===")
print(tresc[:300])
print()

for i in range(3):
    print(f"=== RUN {i+1} ===")
    odp = call_ai(PROMPT_WYCENA, f"OTO ZLECENIE:\n{tresc}\n\nDZIENNIK:\n(brak)\n\nRESEARCH:\n(brak)", temperature=0.3)
    struktura = _wyciagnij_json_blok(odp or "", "WYCENA_JSON")
    if not struktura:
        print("  BRAK STRUKTURY")
        continue
    print("  STRUKTURA:")
    print("   ", json.dumps(struktura, ensure_ascii=False))
    try:
        w = policz_wycene(struktura)
        print(f"  -> KALKULATOR: {w['kwota']} zl / {w['dni']} dni")
    except Exception as e:
        print(f"  -> BLAD: {e}")
    print()
