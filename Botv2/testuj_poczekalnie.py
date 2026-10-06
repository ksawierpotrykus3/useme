# -*- coding: utf-8 -*-
"""Testowanie nowego mózgu V2 na świeżych zleceniach z Useme i zapis do poczekalni (bez wysyłki)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CORE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CORE / "kod"))
sys.path.insert(0, str(CORE / "Botv2" / "mozg"))

from browser_driver import BrowserDriver
from storage import Storage
from brain import zbuduj_oferte

POCZEKALNIA = CORE / "Botv2" / "poczekalnia_ofert"
POCZEKALNIA.mkdir(parents=True, exist_ok=True)


def pobierz_lub_wczytaj(job_id: str, driver: BrowserDriver) -> dict:
    storage = Storage()
    job = storage.load_job(job_id)
    url = f"https://useme.com/pl/jobs/{job_id}/"
    if not job or not job.get("full_description"):
        print(f"[POBIERANIE] Pobieram szczegóły zlecenia #{job_id}...", flush=True)
        det = driver.fetch_job_details(url)
        record = {
            "id": str(job_id),
            "url": url,
            "title": det.get("title") or f"Zlecenie #{job_id}",
            "full_description": det.get("full_description") or "",
            "budget": det.get("budget") or "Do negocjacji",
            "author": det.get("author") or "",
            "author_id": det.get("author_id") or "",
            "full_details": det,
        }
        storage.save_new_job(record, "programowanie-i-it")
        return record
    return job


def main():
    job_ids = sys.argv[1:] if len(sys.argv) > 1 else ["145466", "145391"]
    print("=" * 78)
    print(f"   TESTOWANIE MÓZGU V2 NA ZLECENIACH: {job_ids}")
    print(f"   Katalog poczekalni: {POCZEKALNIA}")
    print("=" * 78)

    with BrowserDriver(headless=True) as driver:
        for jid in job_ids:
            print("\n" + "#" * 78)
            print(f"   START ZLECENIA #{jid}")
            print("#" * 78, flush=True)

            job = pobierz_lub_wczytaj(jid, driver)
            print(f"[ZLECENIE] #{jid} | {job.get('title')}")
            print(f"[KLIENT]   {job.get('author')} (budżet: {job.get('budget')})")
            print(f"[OPIS]     {len(job.get('full_description', ''))} znaków\n")

            print("--- PRZEBIEG AI (V2) ---", flush=True)
            wynik = zbuduj_oferte(job, verbose=True)

            if not wynik.get("ok"):
                print(f"[STOP] Błąd lub odrzucenie: {wynik.get('blad')}")
                continue

            # Zapis do poczekalni
            folder_job = POCZEKALNIA / str(jid)
            folder_job.mkdir(parents=True, exist_ok=True)

            (folder_job / "00_zlecenie.txt").write_text(
                f"TYTUŁ: {job.get('title')}\n"
                f"KLIENT: {job.get('author')}\n"
                f"BUDŻET: {job.get('budget')}\n"
                f"URL: {job.get('url')}\n\n"
                f"OPIS:\n{job.get('full_description')}\n",
                encoding="utf-8"
            )

            (folder_job / "oferta.txt").write_text(wynik.get("oferta", "").strip(), encoding="utf-8")

            podsumowanie = {
                "job_id": jid,
                "title": job.get("title"),
                "author": job.get("author"),
                "budget": job.get("budget"),
                "url": job.get("url"),
                "wycena": wynik.get("wycena"),
                "wycena_dolna": wynik.get("wycena_dolna"),
                "wycena_gorna": wynik.get("wycena_gorna"),
                "dni_od": wynik.get("dni_od"),
                "dni_do": wynik.get("dni_do"),
                "definitywna": wynik.get("definitywna"),
                "checker_ok": (wynik.get("checker") or {}).get("ok"),
                "checker_problemy": (wynik.get("checker") or {}).get("problemy", []),
                "sedzia_status": (wynik.get("sedzia") or {}).get("status"),
                "sedzia_kara": (wynik.get("sedzia") or {}).get("kara_pkt"),
            }
            (folder_job / "meta.json").write_text(
                json.dumps(podsumowanie, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            print("\n" + "=" * 50)
            print(f"OFERTA DLA #{jid} (ZAPISANA W POCZEKALNI):")
            print("=" * 50)
            print(wynik.get("oferta"))
            print("=" * 50)
            print(f"Wycena: {wynik.get('wycena_dolna')}-{wynik.get('wycena_gorna')} zł | Czas: {wynik.get('dni_od')}-{wynik.get('dni_do')} dni")
            print(f"Checker: {wynik.get('checker', {}).get('ok')} | Sędzia: {wynik.get('sedzia', {}).get('status')}")
            print(f"Zapisano w: {folder_job}\n")


if __name__ == "__main__":
    main()
