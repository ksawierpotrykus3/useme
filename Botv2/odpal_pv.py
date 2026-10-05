# -*- coding: utf-8 -*-
"""Uruchomienie Botv2 w trybie wiadomości prywatnej (PV / 'Zapytaj o szczegóły').

Generuje ofertę za pomocą umysłu V2 (analiza, weryfikacja, debata wycenowa DeepSeek vs Gemini Rozszerzony,
napisanie bezpośredniej wiadomości partnerskiej do klienta) oraz obsługuje ścieżkę Playwright:
karta zlecenia -> kliknięcie 'Zapytaj o szczegóły' -> wpisanie treści do textarea -> wysyłka / DRY_RUN.

Użycie:
    python odpal_pv.py 145494               # konkretne zlecenie, tryb DRY_RUN (domyślny)
    python odpal_pv.py --send 145494        # wysyłka na żywo
    python odpal_pv.py --headless 145494    # tryb bezokienkowy
    python odpal_pv.py                      # 1 losowe zlecenie z magazynu w trybie DRY_RUN
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent
CORE_DIR = BASE_DIR.parent
KOD_DIR = CORE_DIR / "kod"
MOZG_DIR = BASE_DIR / "mozg"

sys.path.insert(0, str(KOD_DIR))
sys.path.insert(0, str(MOZG_DIR))

import config  # noqa: E402
from brain import zbuduj_oferte  # noqa: E402
from browser_driver import BrowserDriver  # noqa: E402
from pv_driver import PVDriver  # noqa: E402
from storage import Storage  # noqa: E402


def _ma_tresc(z: dict) -> bool:
    fd = z.get("full_details") or {}
    desc = (
        z.get("full_description")
        or fd.get("full_description")
        or z.get("description")
        or z.get("short_desc")
        or ""
    )
    return len((desc or "").strip()) > 50


def wczytaj_zlecenie_lub_pobierz(job_id: str, driver: BrowserDriver) -> dict:
    storage = Storage()
    job = storage.load_job(job_id)
    if not job or not _ma_tresc(job):
        print(f"[PV] Pobieram szczegóły zlecenia #{job_id} przez przeglądarkę...", flush=True)
        job_url = f"https://useme.com/pl/jobs/{job_id}/"
        details = driver.fetch_job_details(job_url)
        record = {
            "id": str(job_id),
            "url": job_url,
            "title": details.get("title") or f"Zlecenie #{job_id}",
            "full_description": details.get("full_description") or "",
            "budget": details.get("budget") or "",
            "author": details.get("author") or "",
            "author_id": details.get("author_id") or "",
            "full_details": details,
        }
        storage.save_new_job(record, "programowanie-i-it")
        return record
    return job


def main():
    parser = argparse.ArgumentParser(description="Botv2 - wysyłka wiadomości na PV (Zapytaj o szczegóły)")
    parser.add_argument("job_id", nargs="?", default=None, help="ID zlecenia na Useme (np. 145494)")
    parser.add_argument("--send", "--live", dest="send", action="store_true", help="Wyślij wiadomość naprawdę (brak DRY_RUN)")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=True, help="Tylko wypełnij i zrób screenshot (domyślne)")
    parser.add_argument("--headless", action="store_true", default=False, help="Uruchom przeglądarkę w trybie headless")
    args = parser.parse_args()

    live_mode = args.send
    dry_run = not live_mode

    print("=" * 70, flush=True)
    print(f"   BOT V2 — ŚCIEŻKA PV ('ZAPYTAJ O SZCZEGÓŁY')", flush=True)
    print(f"   Tryb: {'LIVE (WYSYŁKA)' if live_mode else 'DRY_RUN (BEZPIECZNY PODGLĄD)'}", flush=True)
    print("=" * 70, flush=True)

    with BrowserDriver(headless=args.headless) as driver:
        # 1. Wybór lub pobranie zlecenia
        if args.job_id:
            job = wczytaj_zlecenie_lub_pobierz(args.job_id, driver)
        else:
            magazyn = config.MAGAZYN_DIR
            wszystkie = []
            for p in magazyn.rglob("*.json"):
                if ".checkpoints" in str(p) or p.name == "marker.json":
                    continue
                try:
                    d = json.loads(p.read_text(encoding="utf-8"))
                    if _ma_tresc(d):
                        wszystkie.append(d)
                except Exception:
                    continue
            if not wszystkie:
                print("[STOP] Brak zleceń w magazynie. Podaj job_id w argumencie.", flush=True)
                return
            job = random.choice(wszystkie)

        job_id = str(job.get("id"))
        author_id = str(job.get("author_id") or (job.get("full_details") or {}).get("author_id") or "")
        print(f"\n[ZLECENIE] #{job_id} — {job.get('title', '')[:70]}", flush=True)
        print(f"[AUTOR] {job.get('author', 'nieznany')} (id: {author_id or 'auto-detekcja'})", flush=True)

        # 2. Generowanie oferty / wiadomości przez mózg V2
        print("\n--- GENEROWANIE WIADOMOŚCI V2 (DeepSeek + Gemini Thinking) ---", flush=True)
        wynik = zbuduj_oferte(job, verbose=True)

        if not wynik.get("ok"):
            print(f"[STOP] Błąd generowania: {wynik.get('blad')}", flush=True)
            return

        wiadomosc = wynik.get("oferta", "").strip()
        print("\n" + "-" * 50, flush=True)
        print("TREŚĆ WIADOMOŚCI DO KLIENTA (PV):", flush=True)
        print("-" * 50, flush=True)
        print(wiadomosc, flush=True)
        print("-" * 50, flush=True)

        # 3. Uruchomienie ścieżki Playwright PV
        print(f"\n[PLAYWRIGHT] Rozpoczynam wypełnianie formularza PV dla #{job_id}...", flush=True)
        pv_driver = PVDriver(driver.context, dry_run=dry_run)
        res = pv_driver.send_private_message(
            job_id=job_id,
            message_text=wiadomosc,
            author_id=author_id or None,
            dry_run=dry_run,
            custom_screenshot_dir=BASE_DIR / "debug"
        )

        print("\n" + "=" * 70, flush=True)
        print("WYNIK OPERACJI PV:", flush=True)
        print(json.dumps(res, indent=2, ensure_ascii=False), flush=True)
        print("=" * 70, flush=True)


if __name__ == "__main__":
    main()
