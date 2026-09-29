# -*- coding: utf-8 -*-
"""
GŁÓWNY PUNKT WEJŚCIA NARZĘDZI BADAWCZYCH (`kod/narzedzia_badawcze/aktualizuj_wszystko.py`):
Pozwala jedną komendą zsynchronizować dane i przeliczyć statystyki dla obu światów:
- Świat 1 (`--swiat 1`): Zleceniodawca / Mystery Shopping (`weronikabuchholc13`, #144890)
- Świat 2 (`--swiat 2`): Wykonawca / Ofertowarka (`ksawierpotrykus3`, 01_ofertowarka + 02_przegrane + 03_odpisane)
- Opcja `--ai`: Uruchamia dodatkowo przyrostowy audyt AI (DeepSeek Proxy `http://127.0.0.1:4571`)
  dla nowych ofert konkurencji i nowo zamkniętych ofert własnych.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

NARZEDZIA_DIR = Path(__file__).resolve().parent


def run_script(rel_path: str) -> None:
    script_path = NARZEDZIA_DIR / rel_path
    print(f"\n>>> Uruchamiam: {rel_path}")
    res = subprocess.run([sys.executable, str(script_path)], check=False)
    if res.returncode != 0:
        print(f"[WARN] Skrypt {rel_path} zakończył się kodem {res.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Centralny synchronizator i analityk obu światów Useme.")
    parser.add_argument(
        "--swiat",
        choices=["1", "2", "oba"],
        default="oba",
        help="Który świat zsynchronizować i przeliczyć: 1 (Zleceniodawca), 2 (Wykonawca), oba (domyślnie)",
    )
    parser.add_argument(
        "--tylko-statystyki",
        action="store_true",
        help="Pomiń pobieranie z sieci (scraping) i przelicz wyłącznie lokalne statystyki i macierze",
    )
    parser.add_argument(
        "--ai",
        action="store_true",
        help="Uruchom również audyt AI nowych ofert i sekcję porażek przez http://127.0.0.1:4571",
    )
    args = parser.parse_args()

    if args.swiat in ("1", "oba"):
        if not args.tylko_statystyki:
            run_script("swiat_1_zleceniodawca/sync_zlecenie.py")
        run_script("swiat_1_zleceniodawca/przelicz_statystyki.py")
        if args.ai:
            run_script("swiat_1_zleceniodawca/audyt_nowych_ai.py")

    if args.swiat in ("2", "oba"):
        if not args.tylko_statystyki:
            run_script("swiat_2_wykonawca/sync_konto.py")
        run_script("swiat_2_wykonawca/przelicz_baze.py")
        if args.ai:
            run_script("swiat_2_wykonawca/sekcja_porazek_ai.py")


if __name__ == "__main__":
    main()
