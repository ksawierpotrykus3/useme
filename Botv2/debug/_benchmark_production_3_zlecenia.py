# -*- coding: utf-8 -*-
"""Pełny benchmark 3 zleceń z bazy Useme przez produkcyjny moduł wycena_debata.py."""
import sys
import json
import time
from pathlib import Path
import requests

sys.path.insert(0, str(Path("Botv2/mozg").resolve()))
from brain import call_ai, call_gemini, GEMINI_API_URL
from wycena_debata import wycen_przez_debate

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def reset_gemini():
    try:
        url = GEMINI_API_URL.replace("/chat/completions", "/chat/reset")
        requests.post(url, timeout=5)
    except Exception:
        pass


root = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia")
zlecenia = [
    {
        "id": "145285",
        "nazwa": "145285 Subiekt <-> BaseLinker (40k produktów)",
        "plik": root / "145285" / "zlecenie.json",
    },
    {
        "id": "145287",
        "nazwa": "145287 Aplikacja mobilna offline (kierowcy/serwis)",
        "plik": root / "145287" / "zlecenie.json",
    },
    {
        "id": "144890",
        "nazwa": "144890 Automatyzacja faktur OCR + Optima",
        "plik": root / "zlecenie_testowe_144890" / "zlecenie.json",
    },
]

wyniki = []

for z in zlecenia:
    print("\n" + "=" * 80)
    print(f"BENCHMARK ZLECENIA: {z['nazwa']}")
    print("=" * 80)
    reset_gemini()
    time.sleep(1.0)

    dane = json.loads(z["plik"].read_text(encoding="utf-8"))
    tresc = dane.get("description") or dane.get("opis", "")

    res = wycen_przez_debate(
        tresc_zlecenia=tresc,
        dziennik=f"Dziennik analizy dla {z['nazwa']}: kluczowe ryzyka architektoniczne, integracje i testy.",
        call_wyceniacz_fn=call_ai,
        call_reviewer_fn=call_gemini,
        say=print,
        max_rundy=2,
    )
    wyniki.append({
        "id": z["id"],
        "nazwa": z["nazwa"],
        "wynik": res,
    })
    time.sleep(2.0)

out_file = Path("Botv2/debug/benchmark_produkcyjny_3_zlecenia.json")
out_file.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")

print("\n" + "=" * 80)
print("PODSUMOWANIE BENCHMARKU PRODUKCYJNEGO:")
print("=" * 80)
for w in wyniki:
    r = w["wynik"]
    print(f"* {w['nazwa']}: {r['kwota']} zł ({r['dni_od']}-{r['dni_do']} dni) | Reviewer: {r['reviewer_werdykt']} ({r['widełki_rynkowe']}) | Rundy: {r['rundy']}")
