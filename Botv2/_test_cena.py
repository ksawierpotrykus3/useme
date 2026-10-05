# -*- coding: utf-8 -*-
"""Test: czy model oceni sama cene bez promptu? Zlecenie KSeF + cena 6500."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai

BASE = Path("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
dane = json.loads(BASE.read_text(encoding="utf-8"))
rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
z = next((r for r in rek if "KSeF" in json.dumps(r, ensure_ascii=False) and "moduł faktur" in json.dumps(r, ensure_ascii=False)), None)

opis = z.get("job_description", "")
print("=== ZLECENIE (skrot) ===")
print(opis[:400])
print()

# Wysylamy jak czlowiek - samo zlecenie + cena, bez instrukcji
msg = f"Zlecenie:\n{opis}\n\nMoja wycena: 6500 zl"

for model in ["deepseek-v4-pro", "deepseek-v4-pro-nothink"]:
    print(f"=== MODEL: {model} ===")
    odp = call_ai("", msg, model=model, temperature=0.3, max_tokens=1500)
    print(odp)
    print()
