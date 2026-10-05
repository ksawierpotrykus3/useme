# -*- coding: utf-8 -*-
"""Test na zleceniu E-Beige #145290 (KSeF .NET) - to ktore zaniepokoilo usera."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))

from brain import zbuduj_oferte

BASE = Path("badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json")
dane = json.loads(BASE.read_text(encoding="utf-8"))
rek = dane if isinstance(dane, list) else dane.get("oferty") or dane.get("rekordy") or []

z = None
for r in rek:
    if "KSeF" in json.dumps(r, ensure_ascii=False) and "moduł faktur" in json.dumps(r, ensure_ascii=False):
        z = r
        break

if not z:
    print("Nie znaleziono zlecenia")
    sys.exit(1)

# Dopasuj strukture do tego, co zna brain (_tresc_zlecenia czyta full_details/list_details/opis)
zlecenie = {
    "id": str(z.get("job_id", "145290")),
    "title": z.get("title", ""),
    "full_description": z.get("job_description", ""),
    "budget": z.get("budget", ""),
}

wynik = zbuduj_oferte(zlecenie)
print("\n=== OFERTA ===")
print(wynik.get("oferta", "BRAK"))
print("\n[WYCENA]", wynik.get("wycena"), "zl | dni", wynik.get("dni_od"), "-", wynik.get("dni_do"))
print("[CHECKER]", wynik.get("checker"))
