# -*- coding: utf-8 -*-
"""Test naturalności ofert na zleceniach z bazy.

Przepuszcza wybrane zlecenia przez SUROWY łańcuch 01 -> 02b -> 02a -> 08
(sędzia 1-100 wyłączony w config.py) i zapisuje wynik do pliku, żeby
spokojnie ocenić, czy oferty brzmią jak pisane przez człowieka.

Użycie:
    python narzedzia_badawcze/test_naturalnosci.py 145098 144890 145383
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

KOD_DIR = Path(__file__).resolve().parent.parent
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

from chain_executor import run_chain

BAZA_DIR = KOD_DIR.parent / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka"
OUT_DIR = KOD_DIR.parent / "badania" / "profilowanie_zleceniodawcy" / "testy_ofert"


def _ma_dane_zlecenia(dane: dict) -> bool:
    """Czy dict wygląda jak surowe zlecenie (ma opis/fields), a nie checkpoint."""
    if not isinstance(dane, dict):
        return False
    if dane.get("fields"):
        return True
    if (dane.get("full_details") or {}).get("full_description"):
        return True
    return bool(dane.get("full_description") or dane.get("description"))


def znajdz_plik(job_id: str) -> Path | None:
    """Szuka pliku zlecenia po id w drzewie bazy, pomijając checkpointy."""
    kandydaci = []
    for p in BAZA_DIR.rglob(f"{job_id}.json"):
        if ".checkpoints" in p.parts:
            continue
        kandydaci.append(p)

    # Preferuj plik, który faktycznie zawiera dane zlecenia.
    for p in kandydaci:
        try:
            dane = json.loads(p.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if _ma_dane_zlecenia(dane):
            return p

    return kandydaci[0] if kandydaci else None


def uruchom(job_id: str) -> dict:
    plik = znajdz_plik(job_id)
    if not plik:
        return {"id": job_id, "blad": "nie znaleziono pliku w bazie"}

    zlecenie = json.loads(plik.read_text(encoding="utf-8-sig"))
    t0 = time.time()
    wynik = run_chain(f"test-naturalnosci-{job_id}", zlecenie)
    dt = round(time.time() - t0, 1)

    if not wynik:
        return {"id": job_id, "blad": "łańcuch zwrócił None (abort)", "czas_s": dt}

    return {
        "id": job_id,
        "tytul": zlecenie.get("title", ""),
        "autor": zlecenie.get("author", ""),
        "budzet": zlecenie.get("budget", ""),
        "czas_s": dt,
        "opis": wynik.get("opis", ""),
        "wycena_dni": wynik.get("wycena_dni", ""),
        "research": wynik.get("research", ""),
    }


def main() -> None:
    ids = sys.argv[1:] or ["145098", "144890", "145383"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for job_id in ids:
        print(f"\n{'=' * 60}\n[{job_id}] start...", flush=True)
        try:
            res = uruchom(job_id)
        except Exception as e:
            res = {"id": job_id, "blad": f"{type(e).__name__}: {e}"}
        out_path = OUT_DIR / f"{job_id}.json"
        out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        slow = len(res.get("opis", "").split())
        print(f"[{job_id}] zapisano -> {out_path.name} ({slow} słów, {res.get('czas_s')}s)", flush=True)

    print(f"\nGotowe. Wyniki w: {OUT_DIR}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    main()