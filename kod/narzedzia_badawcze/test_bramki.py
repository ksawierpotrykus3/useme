# -*- coding: utf-8 -*-
"""Test samej BRAMKI researchu (ON/OFF) na wielu zleceniach.

Odpala TYLKO prompt bramki (agent_01_research.md) na zleceniach z bazy
i zapisuje decyzję ON/OFF dla każdego. Bez całego łańcucha, więc szybko.

Użycie:
    python narzedzia_badawcze/test_bramki.py
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

KOD_DIR = Path(__file__).resolve().parent.parent
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

from chain_executor import call_deepseek, DEEPSEEK_MODEL, PROMPTS_DIR

BAZA_DIR = KOD_DIR.parent / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka"
OUT_DIR = KOD_DIR.parent / "badania" / "profilowanie_zleceniodawcy" / "testy_ofert" / "bramka"

# Zlecenia testowe: różne typy (proste, techniczne, doradcze, bez sensu)
TEST_IDS = ["145098", "144890", "145383", "144069", "144001", "143916", "143891", "144010"]


def _tresc_zlecenia(z: dict) -> str:
    fields = z.get("fields") or {}
    desc = (
        z.get("full_description")
        or z.get("description")
        or fields.get("description")
        or (z.get("list_details") or {}).get("short_desc")
        or ""
    )
    return (
        f"TITLE: {z.get('title') or fields.get('title') or ''}\n"
        f"BUDGET: {z.get('budget') or fields.get('budget') or ''}\n"
        f"OPIS:\n{desc}"
    )


def _znajdz(job_id: str) -> Path | None:
    for p in BAZA_DIR.rglob(f"{job_id}.json"):
        return p
    return None


def _decyzja(z: dict) -> str:
    """Odpala samą bramkę i zwraca ON/OFF + odpowiedź."""
    bramka_prompt = (PROMPTS_DIR / "generatory" / "agent_01_research.md").read_text(encoding="utf-8-sig")
    # bierzemy tylko część A (bramka), bez części B (research) - żeby było szybko
    czesc_a = bramka_prompt.split("## CZĘŚĆ B")[0]
    usr = "--- ZLECENIE DO OCENY ---\n" + _tresc_zlecenia(z)
    odp = call_deepseek(czesc_a, usr, model=DEEPSEEK_MODEL, timeout=90) or ""
    if "BRAK_ISTOTNYCH_FAKTOW" in odp.upper() and len(odp.strip()) < 60:
        return "OFF"
    if re.search(r"BRAK_ISTOTNYCH_FAKTOW", odp, re.IGNORECASE) and "MINY" not in odp.upper():
        return "OFF"
    return "ON"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wyniki = []
    for jid in TEST_IDS:
        plik = _znajdz(jid)
        if not plik:
            print(f"[{jid}] brak pliku")
            continue
        z = json.loads(plik.read_text(encoding="utf-8-sig"))
        try:
            dec = _decyzja(z)
        except Exception as e:
            dec = f"BLAD: {e}"
        dl = len((z.get("full_description") or (z.get("list_details") or {}).get("short_desc") or ""))
        print(f"[{jid}] {dec}  (dlugosc opisu: {dl} znakow)", flush=True)
        wyniki.append({"id": jid, "decyzja": dec, "dlugosc_opisu": dl, "tytul": z.get("title", "")})
        time.sleep(6)

    out = OUT_DIR / "wyniki_bramki.json"
    out.write_text(json.dumps(wyniki, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nZapisano: {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    main()