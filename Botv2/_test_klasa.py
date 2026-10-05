# -*- coding: utf-8 -*-
"""Test stabilnosci klasyfikatora zlozonosci. 3x na tym samym zleceniu, temp 0.0."""
import sys, json, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai

BASE = Path("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
dane = json.loads(BASE.read_text(encoding="utf-8"))
rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []
z = next((r for r in rek if "KSeF" in json.dumps(r, ensure_ascii=False) and "moduł faktur" in json.dumps(r, ensure_ascii=False)), None)
opis = z.get("job_description", "")

PROMPT = """Jesteś rygorystycznym audytorem technicznym oprogramowania.
Twoim zadaniem jest sklasyfikowanie poniższego zlecenia do DOKŁADNIE JEDNEJ klasy złożoności (1-5) na podstawie twardych reguł:

REGUŁY:
- Klasa 1: Poprawki, pojedynczy skrypt, prosty widok UI (1-3 dni).
- Klasa 2: CRUD, standardowe REST API z oficjalnym SDK (4-7 dni).
- Klasa 3: Własna logika biznesowa, przetwarzanie w tle, 2-3 standardowe API (8-14 dni).
- Klasa 4: Systemy krytyczne/transakcyjne, brak oficjalnego stabilnego SDK, wymóg idempotencji/kolejek, grzebanie w cudzym kodzie autorskim (15-25 dni).
- Klasa 5: Pełny system SaaS od zera, architektura rozproszona multi-tenant (26+ dni).

Zwróć WYŁĄCZNIE format JSON:
{"complexity_class": int, "trigger_keywords": [max 3 frazy], "is_vague": bool}"""

print("=== TEST STABILNOSCI KLASYFIKATORA (3x, temp 0.0) ===\n")
for i in range(3):
    odp = call_ai(PROMPT, f"ZLECENIE:\n{opis}", temperature=0.0, max_tokens=500)
    m = re.search(r"\{.*\}", odp or "", re.DOTALL)
    if m:
        try:
            r = json.loads(m.group(0))
            print(f"Run {i+1}: klasa={r.get('complexity_class')} | vague={r.get('is_vague')} | triggery={r.get('trigger_keywords')}")
        except Exception as e:
            print(f"Run {i+1}: blad parsowania: {odp[:200]}")
    else:
        print(f"Run {i+1}: brak JSON: {odp[:200]}")
</parameter>