# -*- coding: utf-8 -*-
"""Skrypt demonstracyjny kalkulatora wycen (Warsztat/Lab).

Wydzielony z kod/wycena_kalkulator.py zgodnie z orzeczeniem Sądu Segregacji Kuratora.
Uruchamia przykładową kalkulację projektu i weryfikuje poprawność obliczeń.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

KOD_DIR = Path(__file__).resolve().parent.parent
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from wycena_kalkulator import policz_wycene


def main():
    przyklad = {
        "typ_zlecenia": "projekt",
        "moduly": [{"nazwa": "Landing page / One-Page", "godziny_real": 20}],
        "flagi": {
            "brak_specyfikacji": True,
            "wiek_ofert_dni": 1,
            "liczba_ofert": 71,
            "nowa_technologia": False,
        },
    }
    w = policz_wycene(przyklad)
    print("[DEMO WYCENY] Wynik kalkulacji:")
    print(json.dumps(w, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
