# -*- coding: utf-8 -*-
"""Test stabilnosci wycen: 3 zlecenia x 3 uruchomienia. Porownanie z mediana konkurencji."""
import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))

from brain import call_ai, PROMPT_WYCENA, _wyciagnij_json_blok, _czytaj, _parsuj_dziennik
from kalkulator import policz_wycene

BASE = Path("badania/baza/weronikabuchholc13/04_moje_zlecenia")

# mediany konkurencji (z diag)
MEDIANY = {"145285": 4800, "145287": 11999, "zlecenie_testowe_144890": 5900}

system_myslenie = _czytaj("myslenie.md")


def tresc_zlecenia(z):
    return f"TYTUL: {z.get('title','')}\n\nTRESC OGLOSZENIA:\n{z.get('opis','')}"


def policz_raz(tresc):
    """Analiza + wycena. Zwraca (kwota, dni, struktura) albo None."""
    dziennik = call_ai(system_myslenie, f"OTO ZLECENIE:\n\n{tresc}\n\nZrob dziennik myslenia wg formatu.", temperature=0.4)
    if not dziennik:
        return None
    odp = call_ai(PROMPT_WYCENA, f"OTO ZLECENIE:\n{tresc}\n\nDZIENNIK:\n{dziennik}\n\nRESEARCH:\nBRAK", temperature=0.3)
    struktura = _wyciagnij_json_blok(odp or "", "WYCENA_JSON")
    if not struktura:
        return None
    try:
        w = policz_wycene(struktura)
        moduly = struktura.get("moduly") or []
        godziny = sum((m.get("godziny_real") or 0) for m in moduly)
        return (w["kwota"], w["dni"], len(moduly), godziny)
    except Exception as e:
        return ("BLAD", str(e), 0, 0)


for d in sorted(BASE.iterdir()):
    zf = d / "zlecenie.json"
    if not zf.exists():
        continue
    z = json.loads(zf.read_text(encoding="utf-8"))
    tresc = tresc_zlecenia(z)
    med = MEDIANY.get(d.name, "?")
    print("=" * 70)
    print(f"ZLECENIE {d.name} | mediana konkurencji: {med} zl")
    print("=" * 70)
    wyniki = []
    for i in range(3):
        r = policz_raz(tresc)
        if r:
            wyniki.append(r[0])
            print(f"  Run {i+1}: {r[0]} zl / {r[1]} dni | modulow={r[2]} | godzin={r[3]}")
        else:
            print(f"  Run {i+1}: BRAK")
    if wyniki and all(isinstance(x, int) for x in wyniki):
        rozrzut = max(wyniki) - min(wyniki)
        print(f"  --> ROZRZUT: {rozrzut} zl ({(rozrzut/min(wyniki)*100):.0f}%)")
    print()
