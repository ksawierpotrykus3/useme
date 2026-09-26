# -*- coding: utf-8 -*-
"""Pobieracz 416 zamkniętych ofert z Useme z odpornym mechanizmem wznawiania (Checkpointing & State Machine).

Funkcjonalności:
- Przelot przez 42 podstrony listy https://useme.com/pl/dashboard/offers/closed/?page=N
- Ekstrakcja pełnej treści zlecenia (job_description klienta) oraz pełnej naszej oferty (our_proposal)
- Zbieranie budżetu, wyceny, dni roboczych, kategorii, klienta i umów
- Pamięć stanu (checkpointing) – if/else zapobiega ponownemu pobieraniu tego samego
- Atomowy zapis do pliku JSON po każdej stronie oraz po każdej wzbogaconej ofercie
- Obsługa bezpiecznego wyłączenia (Ctrl+C lub plik STOP)
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from playwright.sync_api import Page

# Lokalne moduły projektu
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
from browser_driver import BrowserDriver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Pobieracz416")

BADANIA_DIR = BASE_DIR.parent / "badania"
# Baza: badania/baza/<konto>/02_przegrane/
OUTPUT_FILE = config.PRZEGRANE_DIR / "przegrane_pelne_416.json"
CHECKPOINT_FILE = BADANIA_DIR / "skrypty" / "checkpointy" / "closed_offers_checkpoint.json"
LEGACY_HISTORY_FILE = config.PRZEGRANE_DIR / "przegrane_16.json"
KILL_SWITCH_FILE = BASE_DIR / "STOP"

DASHBOARD_CLOSED_URL = "https://useme.com/pl/dashboard/offers/closed/"
TOTAL_PAGES = 42


def load_legacy_data() -> Dict[str, Dict[str, Any]]:
    """Wczytuje wcześniej pobrane 16 ofert ze starych badań z pełnymi opisami zleceń."""
    if LEGACY_HISTORY_FILE.exists():
        try:
            with open(LEGACY_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {str(item.get("offer_id")): item for item in data if item.get("offer_id")}
        except Exception as e:
            logger.warning(f"Nie udało się wczytać starszej historii: {e}")
    return {}


def load_state() -> tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    """Wczytuje aktualną bazę 416 oraz checkpoint z dysku."""
    database: Dict[str, Dict[str, Any]] = {}
    checkpoint: Dict[str, Any] = {
        "completed_pages": [],
        "scraped_ids": [],
        "enriched_ids": [],
        "last_update": None,
        "total_offers": 0,
        "total_enriched": 0
    }

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    database = {str(item.get("offer_id")): item for item in data if item.get("offer_id")}
                elif isinstance(data, dict):
                    database = data
        except Exception as e:
            logger.warning(f"Błąd odczytu bazy {OUTPUT_FILE}: {e}")

    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
        except Exception as e:
            logger.warning(f"Błąd odczytu checkpointu {CHECKPOINT_FILE}: {e}")

    # Synchronizacja list i liczników
    enriched = [oid for oid, item in database.items() if item.get("job_description")]
    checkpoint["scraped_ids"] = list(database.keys())
    checkpoint["enriched_ids"] = enriched
    checkpoint["total_offers"] = len(database)
    checkpoint["total_enriched"] = len(enriched)
    return database, checkpoint


def save_state(database: Dict[str, Dict[str, Any]], checkpoint: Dict[str, Any]):
    """Atomowo zapisuje bazę i checkpoint na dysk."""
    config.PRZEGRANE_DIR.mkdir(parents=True, exist_ok=True)

    items_list = list(database.values())
    enriched = [oid for oid, item in database.items() if item.get("job_description")]
    checkpoint["last_update"] = datetime.datetime.now().isoformat()
    checkpoint["scraped_ids"] = list(database.keys())
    checkpoint["enriched_ids"] = enriched
    checkpoint["total_offers"] = len(database)
    checkpoint["total_enriched"] = len(enriched)

    # 1. Atomowy zapis bazy danych
    tmp_out = OUTPUT_FILE.with_suffix(".tmp")
    with open(tmp_out, "w", encoding="utf-8") as f:
        json.dump(items_list, f, ensure_ascii=False, indent=2)
    os.replace(tmp_out, OUTPUT_FILE)

    # 2. Atomowy zapis checkpointu
    tmp_chk = CHECKPOINT_FILE.with_suffix(".tmp")
    with open(tmp_chk, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    os.replace(tmp_chk, CHECKPOINT_FILE)


def check_kill_switch() -> bool:
    """Sprawdza czy użytkownik utworzył plik STOP."""
    if KILL_SWITCH_FILE.exists():
        logger.warning(f"Wykryto plik STOP ({KILL_SWITCH_FILE}). Bezpieczne zatrzymanie pracy!")
        return True
    return False


def parse_page_cards(html_content: str, page_num: int) -> List[Dict[str, Any]]:
    """Parsuje karty ofert z HTML podstrony listy closed offers."""
    soup = BeautifulSoup(html_content, "html.parser")
    items = soup.select("ul.my-offers__list > li.my-offers__list-item")
    parsed_cards = []

    for it in items:
        name_el = it.select_one("a.my-offer__name")
        title = name_el.get_text(strip=True) if name_el else ""
        href = name_el.get("href", "") if name_el else ""

        offer_id = ""
        if href:
            parts = [p for p in href.strip("/").split("/") if p]
            if parts:
                offer_id = parts[-1]

        author_el = it.select_one(".active__offers-item-content-headline-author")
        client = author_el.get_text(strip=True) if author_el else ""

        agr_el = it.select_one(".active__offers-item-content-headline-agreements-count")
        client_contracts = agr_el.get_text(strip=True) if agr_el else ""

        desc_el = it.select_one(".my-offer__quote-description")
        our_proposal = desc_el.get_text("\n", strip=True) if desc_el else ""

        if offer_id:
            parsed_cards.append({
                "offer_id": offer_id,
                "offer_url": f"https://useme.com{href}" if href.startswith("/") else href,
                "title": title,
                "client": client,
                "client_contracts": client_contracts,
                "our_proposal": our_proposal,
                "page_scraped": page_num,
                "status": "closed",
                "scraped_at": datetime.datetime.now().isoformat()
            })

    return parsed_cards


def scrape_offer_details(driver: BrowserDriver, page: Page, offer_url: str, offer_id: str) -> Dict[str, Any]:
    """Wzbogaca ofertę o całą treść zlecenia klienta, budżet, naszą wycenę i dni robocze."""
    for attempt in range(1, 3):
        try:
            page.goto(offer_url, wait_until="domcontentloaded", timeout=45000)
            break
        except Exception as e:
            if attempt == 2:
                raise
            logger.warning(f"   [RETRY] Ponawiam próbę dla {offer_id} po błędzie: {e}")
            time.sleep(1.5)

    try:
        page.wait_for_selector(".jobs-summary", timeout=12000)
    except Exception:
        page.wait_for_timeout(1000)

    driver.dismiss_cookie_banner(page)

    soup = BeautifulSoup(page.content(), "html.parser")
    summaries = soup.find_all("div", class_="jobs-summary")

    details: Dict[str, Any] = {
        "category": "",
        "budget": "",
        "copyright": "",
        "job_description": "",
        "our_price": "",
        "our_days": "",
    }

    if len(summaries) >= 1:
        job_sum = summaries[0]
        cat_el = job_sum.select_one(".jobs-summary__heading span.jobs-summary__item-label")
        if cat_el:
            details["category"] = cat_el.get_text(strip=True)

        for item in job_sum.select(".jobs-summary__item"):
            t = item.get_text(strip=True)
            if "Zleceniodawca" in t:
                details["client"] = t.replace("Zleceniodawca", "").strip()
                break

        brief = job_sum.select_one(".jobs-summary__brief")
        if brief:
            bt = brief.get_text("\n", strip=True)
            lines = [l.strip() for l in bt.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                if line == "Budżet" and i + 1 < len(lines):
                    details["budget"] = lines[i + 1]
                elif line == "Prawa autorskie" and i + 1 < len(lines):
                    details["copyright"] = lines[i + 1]

        # Pełny opis zlecenia od klienta
        desc_el = job_sum.select_one(".offer-details")
        if desc_el:
            details["job_description"] = desc_el.get_text("\n", strip=True)

    if len(summaries) >= 2:
        offer_sum = summaries[1]
        brief = offer_sum.select_one(".jobs-summary__brief")
        if brief:
            bt = brief.get_text("\n", strip=True)
            lines = [l.strip() for l in bt.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                if line == "Wycena" and i + 1 < len(lines):
                    details["our_price"] = lines[i + 1]
                elif line == "Dni pracy" and i + 1 < len(lines):
                    details["our_days"] = lines[i + 1]

        prop_el = offer_sum.select_one(".jobs-summary__item-text")
        if prop_el and not details.get("our_proposal"):
            details["our_proposal"] = prop_el.get_text("\n", strip=True)

    return details


def run_pipeline(enrich_details: bool = True, max_pages: int = 42):
    """Główna pętla sterująca pobieraniem 416 pełnych zleceń i ofert."""
    logger.info("=" * 75)
    logger.info("  START POBIERANIA 416 PEŁNYCH ZLECEŃ I OFERT Z USEME")
    logger.info(f"  Baza:       {OUTPUT_FILE}")
    logger.info(f"  Checkpoint: {CHECKPOINT_FILE}")
    logger.info(f"  Tryb:       {'PEŁNY (Treść zlecenia klienta + Treść naszej oferty)' if enrich_details else 'TYLKO LISTA'}")
    logger.info("=" * 75)

    legacy_data = load_legacy_data()
    database, checkpoint = load_state()

    logger.info(f"Aktualny stan: {len(database)} ofert, z czego {checkpoint.get('total_enriched', 0)} ma pełen opis zlecenia.")

    # Wstrzyknięcie 16 ofert ze starszego badania, jeśli jeszcze nie miały opisu
    if legacy_data:
        injected = 0
        for lid, litem in legacy_data.items():
            if lid in database and not database[lid].get("job_description"):
                for k in ["category", "budget", "copyright", "job_description", "our_price", "our_days"]:
                    if litem.get(k):
                        database[lid][k] = litem[k]
                injected += 1
        if injected:
            logger.info(f"Wstępnie uzupełniono {injected} ofert z poprzedniego badania.")
            save_state(database, checkpoint)

    with BrowserDriver(headless=False) as driver:
        page = driver.context.new_page()

        # =====================================================================
        # FAZA 1: Szybki przelot przez podstrony listy (1 do max_pages)
        # =====================================================================
        logger.info("\n>>> FAZA 1: Pobieranie spisu 416 pozycji z podstron 1..%d...", max_pages)

        for page_num in range(1, max_pages + 1):
            if check_kill_switch():
                break

            if page_num in checkpoint.get("completed_pages", []):
                logger.info(f" [SKIP] Strona {page_num}/{max_pages} już w checkpointcie.")
                continue

            url = f"{DASHBOARD_CLOSED_URL}?page={page_num}" if page_num > 1 else DASHBOARD_CLOSED_URL
            logger.info(f" [STRONA {page_num}/{max_pages}] Otwieram: {url}")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                driver.dismiss_cookie_banner(page)
                page.wait_for_timeout(1500)

                html = None
                for _try in range(3):
                    try:
                        page.wait_for_load_state("networkidle", timeout=10000)
                    except Exception:
                        pass
                    try:
                        html = page.content()
                        break
                    except Exception as ce:
                        logger.warning(f"   [RETRY content] strona {page_num}, proba {_try + 1}/3: {ce}")
                        page.wait_for_timeout(1500)
                if html is None:
                    raise RuntimeError(f"Nie udalo sie pobrac HTML strony {page_num} po 3 probach")
                cards = parse_page_cards(html, page_num)
                logger.info(f"   Znaleziono {len(cards)} pozycji na stronie {page_num}.")

                if not cards and "Just a moment" in page.title():
                    logger.error("   Wykryto Cloudflare Turnstile! Czekam 10s...")
                    page.wait_for_timeout(10000)
                    continue

                for card in cards:
                    cid = card["offer_id"]
                    if cid in database:
                        existing_entry = database[cid]
                        for k, v in card.items():
                            if k not in existing_entry or not existing_entry[k]:
                                existing_entry[k] = v
                    else:
                        if cid in legacy_data:
                            litem = legacy_data[cid]
                            for k in ["category", "budget", "copyright", "job_description", "our_price", "our_days"]:
                                if litem.get(k):
                                    card[k] = litem[k]
                        database[cid] = card

                if page_num not in checkpoint.setdefault("completed_pages", []):
                    checkpoint["completed_pages"].append(page_num)
                checkpoint["completed_pages"].sort()

                save_state(database, checkpoint)
                logger.info(f"   -> Zapisano stan po stronie {page_num}. Łącznie w bazie: {len(database)} ofert.")

            except Exception as e:
                logger.error(f"   Błąd na stronie {page_num}: {e}")

            time.sleep(random.uniform(1.8, 2.8))

        logger.info(f"\n[FAZA 1 ZAKOŃCZONA] Zgromadzono listę {len(database)} ofert.")

        # =====================================================================
        # FAZA 2: Pobranie PEŁNYCH opisów zleceń klienta i wycen (job_description)
        # =====================================================================
        if enrich_details:
            logger.info("\n>>> FAZA 2: Pobieranie pełnych treści zleceń od klientów (job_description)...")
            to_enrich = [oid for oid, item in database.items() if not item.get("job_description")]
            total_need = len(to_enrich)
            total_all = len(database)
            already_done = total_all - total_need

            logger.info(f"Stan: {already_done}/{total_all} ma już pełną treść zlecenia. Do pobrania pozostało: {total_need}.")

            for idx, oid in enumerate(to_enrich, 1):
                if check_kill_switch():
                    break

                item = database[oid]
                url = item.get("offer_url")
                title = item.get("title", "")
                progress_pct = ((already_done + idx) / total_all) * 100

                logger.info(f"[{already_done + idx}/{total_all}] ({progress_pct:.1f}%) Pobieram pełne zlecenie {oid}: '{title[:40]}...'")

                try:
                    det = scrape_offer_details(driver, page, url, oid)
                    item.update(det)
                    save_state(database, checkpoint)
                    desc_len = len(item.get("job_description", ""))
                    logger.info(f"   -> OK! Opis klienta: {desc_len} zn., Budżet: {item.get('budget')}, Wycena: {item.get('our_price')}")
                except Exception as e:
                    logger.error(f"   -> Błąd pobierania detali dla {oid}: {e}")

                # Human pacing 1.2 - 2.2s
                time.sleep(random.uniform(1.2, 2.2))

            logger.info("\n[FAZA 2 ZAKOŃCZONA]")

    logger.info("=" * 75)
    logger.info(f"  ZAKOŃCZONO POBIERANIE! W bazie {OUTPUT_FILE}:")
    logger.info(f"  - Wszystkich ofert: {len(database)}")
    logger.info(f"  - Z pełnym opisem zlecenia klienta: {len([o for o in database.values() if o.get('job_description')])}")
    logger.info("=" * 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pobieracz 416 ofert z Useme")
    parser.add_argument("--no-enrich", action="store_true", help="Pomiń Fazę 2 (tylko lista)")
    parser.add_argument("--max-pages", type=int, default=42, help="Maksymalna liczba stron do pobrania (domyślnie 42)")
    args = parser.parse_args()

    run_pipeline(enrich_details=not args.no_enrich, max_pages=args.max_pages)
