# -*- coding: utf-8 -*-
"""W pełni autonomiczny bot Useme (Botv2).

Działa samodzielnie od A do Z:
1. Skanuje strony 1-3 kategorii IT i Serwisy na Useme.
2. Wykrywa nowe i nieobsłużone zlecenia, pobiera pełne detale do bazy prawdy.
3. Filtruje pułapki (własne profile, etaty, tłum konkurencji >60).
4. Kwalifikuje i wycenia zlecenia Mózgiem V2 (4x DeepSeek + sędzia + checker).
5. Automatycznie wysyła wiadomość na PV ('Zapytaj o szczegóły') z konta Ksawiera.
6. Może działać w trybie jednorazowym (--raz) lub w ciągłej pętli (--petla).

Użycie:
    python Botv2/autonomiczny_bot.py --raz            # Jeden pełny cykl autonomiczny (LIVE)
    python Botv2/autonomiczny_bot.py --raz --dry-run  # Jeden pełny cykl (bez klikania 'Wyślij')
    python Botv2/autonomiczny_bot.py --petla          # Ciągły monitoring co 15 minut
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import random
import re
import sys
import time
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

POCZEKALNIA_DIR = BASE_DIR / "poczekalnia_ofert"
POCZEKALNIA_DIR.mkdir(parents=True, exist_ok=True)


def juz_wyslano_na_to_zlecenie(jid: str, storage: Storage) -> bool:
    """Sprawdza, czy na dane zlecenie wysłano już ofertę lub PV."""
    # 1. W poczekalni
    p_status = POCZEKALNIA_DIR / str(jid) / "status_wysylki.json"
    if p_status.exists():
        try:
            d = json.loads(p_status.read_text(encoding="utf-8"))
            if d.get("wynik", {}).get("status") in ["WYSLANO", "OK", "WYSLANA", "WYSLANO_PV"]:
                return True
        except Exception:
            pass

    # 2. W Storage
    if storage.czy_konto_juz_oferowalo(str(jid), "konto1"):
        return True

    job = storage.load_job(str(jid))
    if job:
        fd = job.get("full_details") or {}
        if fd.get("is_already_submitted"):
            return True
        if job.get("status") in ["WYSLANO", "WYSLANO_PV"]:
            return True

    return False


def pobierz_liste_zlecen_live(driver: BrowserDriver, max_stron: int = 3) -> list:
    """Pobiera listę najnowszych zleceń ze stron 1..max_stron."""
    from bs4 import BeautifulSoup
    znalezione = []
    seen = set()

    for cat_slug, cat_id in [("programowanie-i-it", 35), ("serwisy-internetowe", 34)]:
        for p in range(1, max_stron + 1):
            url = f"https://useme.com/pl/jobs/category/{cat_slug},{cat_id}/?page={p}"
            try:
                page = driver.context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                driver.dismiss_cookie_banner(page)
                soup = BeautifulSoup(page.content(), "html.parser")
                page.close()

                for art in soup.select("article.job, .jobs-list__item, .job"):
                    link = art.select_one("a.job__title, h2 a, a[href*='/pl/jobs/']")
                    if not link:
                        continue
                    href = link.get("href", "")
                    m = re.search(r",(\d+)/?$", href) or re.search(r"/jobs/(\d+)/", href)
                    if not m:
                        continue
                    jid = m.group(1)
                    if jid in seen:
                        continue
                    seen.add(jid)

                    title = link.get_text(strip=True)
                    author, aid = driver._extract_author_from_details(art)
                    budget_el = art.select_one(".job__budget, .job__details-meta span")
                    budget = budget_el.get_text(strip=True) if budget_el else "Do negocjacji"

                    znalezione.append({
                        "id": jid,
                        "title": title,
                        "author": author or "Nieznany",
                        "author_id": aid,
                        "budget": budget,
                        "url": f"https://useme.com{href}" if href.startswith("/") else href,
                        "category": cat_slug
                    })
            except Exception as e:
                print(f"[WARN] Błąd pobierania listy {url}: {e}")

    return znalezione


def uruchom_cykl_autonomiczny(dry_run: bool = False, max_ofert: int = 10, headless: bool = False):
    """Jeden pełny, autonomiczny cykl bota."""
    storage = Storage()
    print("\n" + "=" * 78)
    print(f"   START CYKLU AUTONOMICZNEGO BOTA | Tryb: {'DRY_RUN' if dry_run else 'LIVE (WYSYŁKA PV)'}")
    print(f"   Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 78, flush=True)

    with BrowserDriver(headless=headless) as driver:
        # Krok 1: Skanowanie Useme
        print("\n[KROK 1] Skanuję świeże zlecenia z Useme (strony 1-3)...")
        live_jobs = pobierz_liste_zlecen_live(driver, max_stron=3)
        print(f"[KROK 1] Znaleziono {len(live_jobs)} zleceń na listach kategorii.")

        # Krok 2: Filtracja i kwalifikacja wstępna
        kandydaci = []
        for j in live_jobs:
            jid = j["id"]
            if juz_wyslano_na_to_zlecenie(jid, storage):
                continue
            if config.is_blocked_author(j.get("author_id"), j.get("author")):
                continue
            kandydaci.append(j)

        # Dołącz nieobsłużone zlecenia z magazynu
        for kat in config.CATEGORY_URLS.keys():
            slug = storage._get_category_slug(kat)
            for jf in (storage.magazyn_dir / slug).glob("*.json"):
                try:
                    data = json.loads(jf.read_text(encoding="utf-8"))
                    jid = str(data.get("id"))
                    if jid and not any(k["id"] == jid for k in kandydaci) and not juz_wyslano_na_to_zlecenie(jid, storage):
                        if not config.is_blocked_author(data.get("author_id"), data.get("author")):
                            if data.get("status") in ["POBRANO_DETALE", "NOWA", None]:
                                kandydaci.append(data)
                except Exception:
                    pass

        print(f"[KROK 2] Wytypowano {len(kandydaci)} kandydatów bez wysłanej oferty.")
        if not kandydaci:
            print("[INFO] Brak nowych zleceń do przetworzenia w tym cyklu.")
            return 0

        # Krok 3: Przetwarzanie i wysyłka
        wyslano_w_cyklu = 0

        for idx, job in enumerate(kandydaci, 1):
            if wyslano_w_cyklu >= max_ofert:
                print(f"[LIMIT] Osiągnięto limit {max_ofert} wysyłek w tym cyklu. Kończę.")
                break

            jid = str(job["id"])
            print(f"\n" + "-" * 70)
            print(f"[{idx}/{len(kandydaci)}] Przetwarzam zlecenie #{jid}: {job.get('title', '')[:50]}")
            print("-" * 70)

            # Pobierz pełne detale jeśli brak
            if not job.get("full_description") or len(job.get("full_description", "")) < 50:
                print(f"[DETALE] Pobieram pełny opis #{jid}...")
                try:
                    url = job.get("url") or f"https://useme.com/pl/jobs/{jid}/"
                    det = driver.fetch_job_details(url)
                    job.update(det)
                    job["full_details"] = det
                    storage.save_new_job(job, job.get("category", "programowanie-i-it"))
                except Exception as e:
                    print(f"[WARN] Błąd pobierania detali #{jid}: {e}")
                    continue

            # Sprawdź czy po pobraniu detali nie okazało się, że już złożono ofertę
            if (job.get("full_details") or {}).get("is_already_submitted"):
                print(f"[POMIJAM] Zlecenie #{jid} ma już złożoną ofertę.")
                continue

            # Mózg V2
            print(f"[MÓZG V2] Uruchamiam analizę i wycenę dla #{jid}...")
            wynik = zbuduj_oferte(job, verbose=False)

            if not wynik.get("ok"):
                print(f"[ODRZUCONE] #{jid}: {wynik.get('blad')}")
                storage.update_job(jid, {"status": "ODRZUCONA_V2", "powod": wynik.get("blad")})
                continue

            tresc = (wynik.get("oferta") or "").strip()
            wycena = wynik.get("wycena")
            wycena_d = wynik.get("wycena_dolna")
            wycena_g = wynik.get("wycena_gorna")
            print(f"[ZATWIERDZONA] Wycena: {wycena_d}-{wycena_g} zł ({wycena} zł) | Sędzia: {wynik.get('sedzia', {}).get('status')}")

            # Zamrożenie w poczekalni
            job_folder = POCZEKALNIA_DIR / jid
            job_folder.mkdir(parents=True, exist_ok=True)
            (job_folder / "oferta.txt").write_text(tresc, encoding="utf-8")
            (job_folder / "meta.json").write_text(
                json.dumps({
                    "job_id": jid,
                    "title": job.get("title"),
                    "author": job.get("author"),
                    "budget": job.get("budget"),
                    "url": job.get("url"),
                    "wycena": wycena,
                    "wycena_dolna": wycena_d,
                    "wycena_gorna": wycena_g,
                    "sedzia": wynik.get("sedzia"),
                    "checker": wynik.get("checker"),
                }, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

            # Wysyłka PV
            author_id = job.get("author_id") or (job.get("full_details") or {}).get("author_id")
            pv_driver = PVDriver(driver.context, dry_run=dry_run)

            if wyslano_w_cyklu > 0 and not dry_run:
                pauza = random.randint(10, 20)
                print(f"[PAUZA] Czekam {pauza}s przed wysłaniem PV...")
                time.sleep(pauza)

            res = pv_driver.send_private_message(
                job_id=jid,
                message_text=tresc,
                author_id=author_id,
                dry_run=dry_run,
                custom_screenshot_dir=BASE_DIR / "debug"
            )

            status_wys = res.get("status")
            print(f"[WYNIK PV] #{jid}: {status_wys}")

            if not dry_run and status_wys in ["WYSLANO", "OK", "WYSLANA", "WYSLANO_PV"]:
                (job_folder / "status_wysylki.json").write_text(
                    json.dumps({"data": datetime.now().isoformat(), "typ": "pv", "wynik": res}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                storage.update_job(jid, {"status": "WYSLANO_PV", "wyslano_pv_at": datetime.now().isoformat()})
                wyslano_w_cyklu += 1
            elif dry_run:
                wyslano_w_cyklu += 1

        print(f"\n[PODSUMOWANIE CYKLU] Wysłano / przetworzono {wyslano_w_cyklu} ofert.")
        return wyslano_w_cyklu


def main():
    parser = argparse.ArgumentParser(description="Autonomiczny Bot Useme (V2)")
    parser.add_argument("--raz", action="store_true", default=True, help="Uruchom jeden pełny cykl (domyślne)")
    parser.add_argument("--petla", action="store_true", help="Uruchom w ciągłej pętli co N minut")
    parser.add_argument("--interval", type=int, default=15, help="Interwał w minutach dla pętli (domyślnie 15)")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Tryb DRY-RUN (nie wysyła na żywo)")
    parser.add_argument("--limit", type=int, default=10, help="Maksymalna liczba ofert na cykl (domyślnie 10)")
    parser.add_argument("--headless", action="store_true", default=False, help="Tryb bezokienkowy")
    args = parser.parse_args()

    if args.petla:
        print(f"[AUTONOMIA] Start bota w pętli co {args.interval} minut...")
        while True:
            try:
                uruchom_cykl_autonomiczny(dry_run=args.dry_run, max_ofert=args.limit, headless=args.headless)
            except Exception as e:
                print(f"[BLAD PĘTLI] {e}")
            print(f"\n[SEN] Kolejne sprawdzenie za {args.interval} minut. Czekam...", flush=True)
            time.sleep(args.interval * 60)
    else:
        uruchom_cykl_autonomiczny(dry_run=args.dry_run, max_ofert=args.limit, headless=args.headless)


if __name__ == "__main__":
    main()
