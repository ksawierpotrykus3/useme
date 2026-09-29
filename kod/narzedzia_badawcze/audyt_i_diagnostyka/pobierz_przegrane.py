# -*- coding: utf-8 -*-
"""Pobieracz historii przegranych/zamkniętych ofert z Useme z obsługą checkpointów.

Zbiera oferty z 3 zakładek powiadomień Useme (https://useme.com/pl/notifications/nots/),
odczytuje treść zlecenia oraz złożoną przez nas ofertę (wycena, dni, treść propozycji),
zapisuje wyniki na bieżąco do pliku JSON. Odporny na przerwania – wznawia pracę
od miejsca, w którym skończył.
"""

from __future__ import annotations

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

# Lokalne moduły
import config
from browser_driver import BrowserDriver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("PobieraczPrzegranych")

BASE_DIR = Path(__file__).resolve().parent
TECH_DIR = BASE_DIR / "tech"

# Baza: badania/baza/<konto>/02_przegrane/
OUTPUT_FILE = config.PRZEGRANE_DIR / "przegrane_oferty_historia.json"
CHECKPOINT_FILE = BASE_DIR.parent / "badania" / "skrypty" / "checkpointy" / "przegrane_checkpoint.json"

PAGES = [
    "https://useme.com/pl/notifications/nots/",
    "https://useme.com/pl/notifications/nots/?page=2",
    "https://useme.com/pl/notifications/nots/?page=3",
]


def load_scraped_data() -> Dict[str, Dict[str, Any]]:
    """Ładuje już pobrane dane z pliku wynikowego."""
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {item.get("offer_id", str(i)): item for i, item in enumerate(data)}
                elif isinstance(data, dict):
                    return data
        except Exception as e:
            logger.warning(f"Błąd ładowania {OUTPUT_FILE}: {e}")
    return {}


def save_scraped_data(data: Dict[str, Dict[str, Any]]):
    """Zapisuje zebrane oferty atomowo do pliku JSON."""
    config.PRZEGRANE_DIR.mkdir(parents=True, exist_ok=True)
    TECH_DIR.mkdir(parents=True, exist_ok=True)
    
    # Lista ofert posortowana wg daty/id
    items_list = list(data.values())
    
    temp_file = OUTPUT_FILE.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(items_list, f, ensure_ascii=False, indent=2)
    os.replace(temp_file, OUTPUT_FILE)

    # Zapisz checkpoint
    checkpoint = {
        "last_update": datetime.datetime.now().isoformat(),
        "total_scraped": len(data),
        "scraped_ids": list(data.keys())
    }
    temp_chk = CHECKPOINT_FILE.with_suffix(".tmp")
    with open(temp_chk, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    os.replace(temp_chk, CHECKPOINT_FILE)


def extract_notification_items(page: Page) -> List[Dict[str, str]]:
    """Wyciąga powiadomienia o zamkniętych zleceniach z aktualnie otwartej strony."""
    soup = BeautifulSoup(page.content(), "html.parser")
    items = []
    
    # Szukamy linków do my-offer
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "/jobs/my-offer/" in href:
            title = a.get_text(strip=True)
            # Wyciągnij ID z linku: /pl/jobs/my-offer/2878817/ -> 2878817
            parts = [p for p in href.strip("/").split("/") if p]
            offer_id = parts[-1] if parts else ""
            
            # Spróbuj znaleźć kontekst czasowy (np. 5 godzin temu, wczoraj)
            parent = a.find_parent("li") or a.find_parent("div")
            time_ago = ""
            if parent:
                parent_text = parent.get_text(" ", strip=True)
                # szukamy fraz typu "X temu", "wczoraj", "dni temu"
                for word in ["temu", "wczoraj", "dzisiaj", "godzin", "dni", "minut"]:
                    if word in parent_text:
                        # znajdź kawałek tekstu
                        tokens = parent_text.split()
                        for i, tok in enumerate(tokens):
                            if tok in ["temu", "wczoraj"]:
                                time_ago = " ".join(tokens[max(0, i-2):i+1])
                                break
                        break

            items.append({
                "offer_id": offer_id,
                "title": title,
                "url": f"https://useme.com/pl/jobs/my-offer/{offer_id}/" if not href.startswith("http") else href,
                "time_ago": time_ago
            })
            
    return items


def scrape_offer_details(page: Page, offer_url: str, offer_id: str) -> Dict[str, Any]:
    """Pobiera pełne detale zlecenia i złożonej oferty."""
    page.goto(offer_url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    
    # Auto akceptacja cookies w razie potrzeby
    for sel in ["#cookiescript_accept", "button:has-text('AKCEPTUJ WSZYSTKIE')", "button:has-text('Akceptuj')"]:
        try:
            btn = page.locator(sel).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                page.wait_for_timeout(500)
                break
        except Exception:
            pass

    soup = BeautifulSoup(page.content(), "html.parser")
    summaries = soup.find_all("div", class_="jobs-summary")
    
    result = {
        "offer_id": offer_id,
        "offer_url": offer_url,
        "title": "",
        "category": "",
        "client": "",
        "budget": "",
        "copyright": "",
        "job_description": "",
        "our_price": "",
        "our_days": "",
        "our_proposal": "",
        "scraped_at": datetime.datetime.now().isoformat()
    }
    
    if len(summaries) >= 1:
        job_sum = summaries[0]
        # Kategoria
        cat_el = job_sum.select_one(".jobs-summary__heading span.jobs-summary__item-label")
        if cat_el:
            result["category"] = cat_el.get_text(strip=True)
            
        # Tytuł
        title_el = job_sum.select_one(".jobs-summary__heading h2.jobs-summary__title")
        if title_el:
            result["title"] = title_el.get_text(strip=True)
            
        # Zleceniodawca
        for item in job_sum.select(".jobs-summary__item"):
            t = item.get_text(strip=True)
            if "Zleceniodawca" in t:
                result["client"] = t.replace("Zleceniodawca", "").strip()
                break
                
        # Budżet i prawa autorskie
        brief = job_sum.select_one(".jobs-summary__brief")
        if brief:
            bt = brief.get_text("\n", strip=True)
            lines = [l.strip() for l in bt.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                if line == "Budżet" and i + 1 < len(lines):
                    result["budget"] = lines[i + 1]
                elif line == "Prawa autorskie" and i + 1 < len(lines):
                    result["copyright"] = lines[i + 1]
                    
        # Opis zlecenia
        desc_el = job_sum.select_one(".offer-details")
        if desc_el:
            result["job_description"] = desc_el.get_text("\n", strip=True)
            
    if len(summaries) >= 2:
        offer_sum = summaries[1]
        
        # Wycena i dni pracy
        brief = offer_sum.select_one(".jobs-summary__brief")
        if brief:
            bt = brief.get_text("\n", strip=True)
            lines = [l.strip() for l in bt.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                if line == "Wycena" and i + 1 < len(lines):
                    result["our_price"] = lines[i + 1]
                elif line == "Dni pracy" and i + 1 < len(lines):
                    result["our_days"] = lines[i + 1]
                    
        # Treść naszej oferty
        prop_el = offer_sum.select_one(".jobs-summary__item-text")
        if prop_el:
            result["our_proposal"] = prop_el.get_text("\n", strip=True)

    return result


def run_scraper():
    logger.info("=" * 65)
    logger.info(" ROZPOCZYNAM POBIERANIE PRZEGRANYCH OFERT Z USEME")
    logger.info(f" Plik docelowy: {OUTPUT_FILE}")
    logger.info(f" Checkpoint:    {CHECKPOINT_FILE}")
    logger.info("=" * 65)

    existing_data = load_scraped_data()
    logger.info(f"Pobrano wczeniej ofert: {len(existing_data)}")

    with BrowserDriver(headless=False) as driver:
        page = driver.context.new_page()

        all_target_offers: List[Dict[str, str]] = []

        # KROK 1: Przeglądanie 3 stron powiadomień
        for page_idx, url in enumerate(PAGES, 1):
            logger.info(f"Otwieram zakadk powiadomie {page_idx}/3: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=40000)
                driver.dismiss_cookie_banner(page)
                page.wait_for_timeout(2000)

                items = extract_notification_items(page)
                logger.info(f"  Znaleziono {len(items)} ofert na stronie {page_idx}")
                for it in items:
                    if not any(x["offer_id"] == it["offer_id"] for x in all_target_offers):
                        all_target_offers.append(it)
            except Exception as e:
                logger.error(f"  Bd podczas adowania strony {page_idx}: {e}")

            time.sleep(random.uniform(1.5, 2.5))

        logger.info(f"Razem wykrytych zamknitych ofert na 3 zakadkach: {len(all_target_offers)}")

        # KROK 2: Pobieranie szczegółów brakujących ofert
        to_fetch = [it for it in all_target_offers if it["offer_id"] not in existing_data]
        logger.info(f"Liczba nowych ofert do pobrania: {len(to_fetch)} (pomijam {len(all_target_offers) - len(to_fetch)} ju pobranych)")

        for idx, item in enumerate(to_fetch, 1):
            oid = item["offer_id"]
            url = item["url"]
            title = item["title"]

            logger.info(f"[{idx}/{len(to_fetch)}] Pobieram ofert {oid}: '{title[:45]}...'")
            try:
                details = scrape_offer_details(page, url, oid)
                if item.get("time_ago"):
                    details["closed_time_ago"] = item["time_ago"]

                # Aktualizuj stan
                existing_data[oid] = details
                save_scraped_data(existing_data)

                price = details.get("our_price", "brak")
                days = details.get("our_days", "brak")
                logger.info(f"   -> Zapisano! Cena: {price}, Czas: {days} dni, Zleceniodawca: {details.get('client', 'Anonim')}")

            except Exception as e:
                logger.error(f"   -> Bd przy pobieraniu oferty {oid}: {e}")

            # Odstęp czasowy między zapytaniami (ludzkie tempo 2.5 - 4.5 sekundy)
            delay = random.uniform(2.5, 4.5)
            logger.info(f"   Czekam {delay:.1f}s przed kolejnym zleceniem...")
            time.sleep(delay)

        logger.info("=" * 65)
        logger.info(f" ZAKOCZONO POBIERANIE! Razem w bazie: {len(existing_data)} ofert.")
        logger.info("=" * 65)


if __name__ == "__main__":
    run_scraper()
