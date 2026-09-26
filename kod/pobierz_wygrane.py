# -*- coding: utf-8 -*-
"""Pobieracz historii wygranych zleceń z Useme ze skrzynki wiadomości (mesg).

Zbiera wątki ze skrzynki https://useme.com/pl/mesg/,
weryfikuje w każdym wątku obecność sekcji 'Dotyczy zlecenia',
pomija wątki bez zlecenia,
sprawdza deduplikację (jeśli zlecenie już jest w systemie - pomija),
pobiera pełne detale zlecenia oraz naszej oferty (cena, dni, propozycja),
zapisuje wyniki na bieżąco do pliku JSON z checkpointem.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

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
logger = logging.getLogger("PobieraczWygranych")

BASE_DIR = Path(__file__).resolve().parent
BADANIA_DIR = BASE_DIR.parent / "badania"
TECH_DIR = BASE_DIR / "tech"

# Baza: badania/baza/<konto>/03_odpisane/
OUTPUT_FILE = config.ODPISANE_DIR / "wygrane_56.json"
CHECKPOINT_FILE = BADANIA_DIR / "skrypty" / "checkpointy" / "wygrane_checkpoint.json"


def load_scraped_data() -> tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    """Ładuje już pobrane dane z pliku wynikowego oraz checkpointu."""
    data: Dict[str, Dict[str, Any]] = {}
    checkpoint: Dict[str, Any] = {
        "last_update": None,
        "total_scraped": 0,
        "scraped_offer_ids": [],
        "scraped_job_ids": [],
        "scraped_thread_ids": []
    }

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, list):
                    for item in raw:
                        key = str(item.get("offer_id") or item.get("job_id") or "")
                        if key:
                            data[key] = item
                elif isinstance(raw, dict):
                    data = raw
        except Exception as e:
            logger.warning(f"Błąd ładowania {OUTPUT_FILE}: {e}")

    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
        except Exception as e:
            logger.warning(f"Błąd ładowania {CHECKPOINT_FILE}: {e}")

    return data, checkpoint


def save_scraped_data(data: Dict[str, Dict[str, Any]], checkpoint_extra: Optional[Dict[str, Any]] = None):
    """Zapisuje zebrane oferty atomowo do pliku JSON oraz aktualizuje checkpoint."""
    config.ODPISANE_DIR.mkdir(parents=True, exist_ok=True)
    TECH_DIR.mkdir(parents=True, exist_ok=True)

    items_list = list(data.values())

    temp_file = OUTPUT_FILE.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(items_list, f, ensure_ascii=False, indent=2)
    os.replace(temp_file, OUTPUT_FILE)

    scraped_offer_ids = [str(item.get("offer_id")) for item in items_list if item.get("offer_id")]
    scraped_job_ids = [str(item.get("job_id")) for item in items_list if item.get("job_id")]
    scraped_thread_ids = [str(item.get("thread_id")) for item in items_list if item.get("thread_id")]

    checkpoint = {
        "last_update": datetime.datetime.now().isoformat(),
        "total_scraped": len(items_list),
        "scraped_offer_ids": list(set(scraped_offer_ids)),
        "scraped_job_ids": list(set(scraped_job_ids)),
        "scraped_thread_ids": list(set(scraped_thread_ids))
    }
    if checkpoint_extra:
        checkpoint.update(checkpoint_extra)

    temp_chk = CHECKPOINT_FILE.with_suffix(".tmp")
    with open(temp_chk, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)
    os.replace(temp_chk, CHECKPOINT_FILE)


def fetch_all_message_threads(page: Page) -> List[Dict[str, Any]]:
    """Pobiera wszystkie wątki ze skrzynki wiadomości Useme."""
    logger.info("Otwieram skrzynkę wiadomości https://useme.com/pl/mesg/...")
    page.goto("https://useme.com/pl/mesg/", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)

    # Zamknięcie ciasteczek jeśli widoczne
    for sel in ["#cookiescript_accept", "button:has-text('AKCEPTUJ WSZYSTKIE')", "button:has-text('Akceptuj')"]:
        try:
            btn = page.locator(sel).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                page.wait_for_timeout(500)
                break
        except Exception:
            pass

    all_threads: List[Dict[str, Any]] = []
    page_num = 1
    total_pages = 1

    # Próba pobrania poprzez wbudowane API stronicowania (najszybsze i najdokładniejsze)
    try:
        while page_num <= total_pages:
            logger.info(f"Pobieram stronę wątków {page_num}...")
            api_data = page.evaluate(f"""async () => {{
                const resp = await fetch('https://useme.com/pl/mesg/mesgs/?page={page_num}', {{
                    headers: {{ 'X-Requested-With': 'XMLHttpRequest' }}
                }});
                if (!resp.ok) return null;
                return await resp.json();
            }}""")

            if not api_data or "results" not in api_data:
                logger.warning(f"Brak danych z API dla strony {page_num}, przerywam API.")
                break

            total_pages = api_data.get("total_pages", 1)
            results = api_data.get("results", [])
            logger.info(f"  Pobrano {len(results)} wątków z podstrony {page_num}/{total_pages}")

            for r in results:
                pk = str(r.get("pk", ""))
                url = f"https://useme.com{r.get('mesg_thread_url')}" if r.get("mesg_thread_url") else f"https://useme.com/pl/mesg/{pk}/"
                all_threads.append({
                    "thread_id": pk,
                    "subject": r.get("subject", ""),
                    "user_name": r.get("user_to_display", {}).get("name", "Nieznany"),
                    "thread_url": url,
                    "sent_on": r.get("sent_on", ""),
                    "last_timestamp": r.get("last_timestamp", ""),
                    "thread_size": r.get("thread_size", 0)
                })

            page_num += 1
    except Exception as e:
        logger.warning(f"Błąd podczas odpytywania API wiadomości: {e}")

    # Fallback DOM jeśli API nie zwróciło wątków
    if not all_threads:
        logger.info("Uruchamiam fallback DOM dla listy wątków...")
        soup = BeautifulSoup(page.content(), "html.parser")
        items = soup.select(".threads-list__item, a[href*='/mesg/']")
        for it in items:
            href = it.get("href", "")
            if href and any(c.isdigit() for c in href):
                pk = [p for p in href.strip("/").split("/") if p and p.isdigit()]
                tid = pk[-1] if pk else ""
                url = f"https://useme.com{href}" if href.startswith("/") else href
                all_threads.append({
                    "thread_id": tid,
                    "subject": it.get_text(" ", strip=True)[:60],
                    "user_name": "",
                    "thread_url": url,
                    "sent_on": "",
                    "last_timestamp": "",
                    "thread_size": 0
                })

    logger.info(f"Łącznie zebrano wątków do analizy: {len(all_threads)}")
    return all_threads


def check_thread_job(page: Page, thread_url: str) -> Optional[Dict[str, str]]:
    """Wchodzi w wątek i sprawdza czy dotyczy zlecenia.
    
    Zwraca dict z job_url, job_id, job_title jeśli zlecenie istnieje,
    lub None jeśli brak zlecenia (jak na zrzucie 3).
    """
    page.goto(thread_url, wait_until="domcontentloaded", timeout=35000)
    page.wait_for_timeout(1000)

    soup = BeautifulSoup(page.content(), "html.parser")

    # Główny selektor nagłówka 'Dotyczy zlecenia'
    job_el = soup.select_one(".threads__job-name")
    if not job_el:
        # Alternatywne wyszukiwanie po tekście
        for div in soup.find_all(["div", "p", "span"]):
            if "dotyczy zlecenia" in div.get_text().lower():
                job_el = div
                break

    if not job_el:
        return None

    link = job_el.select_one("a[href*='/jobs/']")
    if not link:
        # Sprawdź dowolny link w tym elemencie lub rodzicu
        link = job_el.select_one("a")

    if not link:
        return None

    href = link.get("href", "")
    if not href or "/jobs/" not in href:
        return None

    job_title = link.get_text(strip=True)
    job_url = f"https://useme.com{href}" if href.startswith("/") else href

    # Wyciągnij ID zlecenia z URL (np. /pl/jobs/144834/ lub /pl/jobs/nazwa,144834/)
    m = re.search(r',(\d+)/?$', href) or re.search(r'/jobs/(\d+)/?', href)
    job_id = m.group(1) if m else ""

    return {
        "job_url": job_url,
        "job_id": job_id,
        "job_title": job_title
    }


def scrape_job_and_offer_details(page: Page, job_url: str, thread_info: Dict[str, Any], known_job_id: str = "") -> Dict[str, Any]:
    """Przechodzi do zlecenia (i oferty my-offer) i pobiera kompletne dane."""
    page.goto(job_url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)

    # Zamknięcie ciasteczek jeśli widoczne
    for sel in ["#cookiescript_accept", "button:has-text('AKCEPTUJ WSZYSTKIE')", "button:has-text('Akceptuj')"]:
        try:
            btn = page.locator(sel).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                page.wait_for_timeout(500)
                break
        except Exception:
            pass

    current_url = page.url

    # Jeśli strona nie przekierowała do my-offer, a jest przycisk 'Twoja oferta' / 'Edytuj ofertę'
    if "/my-offer/" not in current_url:
        for btn_sel in ["a:has-text('Twoja oferta')", "a:has-text('Edytuj ofertę')", "a[href*='/jobs/my-offer/']", "a[href*='/offer/']"]:
            loc = page.locator(btn_sel).first
            if loc.count() > 0 and loc.is_visible():
                target_href = loc.get_attribute("href")
                if target_href:
                    full_target = f"https://useme.com{target_href}" if target_href.startswith("/") else target_href
                    page.goto(full_target, wait_until="domcontentloaded", timeout=35000)
                    page.wait_for_timeout(1500)
                    current_url = page.url
                    break

    # Wyciągamy offer_id z URL jeśli dostępny
    offer_id = ""
    m_offer = re.search(r'/my-offer/(\d+)/?', current_url) or re.search(r'/offer/(\d+)/?', current_url)
    if m_offer:
        offer_id = m_offer.group(1)

    # Wyciągamy job_id
    job_id = known_job_id
    if not job_id:
        m_job = re.search(r',(\d+)/?$', current_url) or re.search(r'/jobs/(\d+)/?', current_url)
        if m_job:
            job_id = m_job.group(1)

    soup = BeautifulSoup(page.content(), "html.parser")
    summaries = soup.find_all("div", class_="jobs-summary")

    result: Dict[str, Any] = {
        "offer_id": offer_id or job_id,
        "job_id": job_id,
        "offer_url": current_url,
        "job_url": job_url,
        "title": "",
        "category": "",
        "client": thread_info.get("user_name", ""),
        "budget": "",
        "copyright": "",
        "job_description": "",
        "our_price": "",
        "our_days": "",
        "our_proposal": "",
        "thread_id": thread_info.get("thread_id", ""),
        "thread_url": thread_info.get("thread_url", ""),
        "thread_size": thread_info.get("thread_size", 0),
        "last_message_date": thread_info.get("last_timestamp", ""),
        "sent_on": thread_info.get("sent_on", ""),
        "scraped_at": datetime.datetime.now().isoformat()
    }

    # Parsowanie sekcji zlecenia
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
                client_name = t.replace("Zleceniodawca", "").strip()
                if client_name:
                    result["client"] = client_name
                break

        # Budżet i Prawa autorskie
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
        desc_el = job_sum.select_one(".offer-details, .job-details__content, .job-description")
        if desc_el:
            result["job_description"] = desc_el.get_text("\n", strip=True)

    # Parsowanie sekcji naszej oferty
    for s in summaries[1:]:
        brief = s.select_one(".jobs-summary__brief")
        if brief:
            bt = brief.get_text("\n", strip=True)
            lines = [l.strip() for l in bt.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                if line == "Wycena" and i + 1 < len(lines):
                    result["our_price"] = lines[i + 1]
                elif line == "Dni pracy" and i + 1 < len(lines):
                    result["our_days"] = lines[i + 1]

        prop_el = s.select_one(".jobs-summary__item-text")
        if prop_el:
            result["our_proposal"] = prop_el.get_text("\n", strip=True)

    # Fallback jeśli tytuł nie został wyciągnięty z jobs-summary
    if not result["title"]:
        h1 = soup.select_one("h1, h2")
        if h1:
            result["title"] = h1.get_text(strip=True)

    return result


def is_already_in_system(job_id: str, offer_id: str, existing_data: Dict[str, Any], checkpoint: Dict[str, Any]) -> bool:
    """Sprawdza deterministycznie czy zlecenie lub oferta znajduje się już w systemie."""
    scraped_offers: Set[str] = set(checkpoint.get("scraped_offer_ids", []))
    scraped_jobs: Set[str] = set(checkpoint.get("scraped_job_ids", []))

    # Sprawdzenie w pliku wyników
    if offer_id and offer_id in existing_data:
        return True
    if job_id and job_id in existing_data:
        return True

    # Sprawdzenie w checkpointach
    if offer_id and offer_id in scraped_offers:
        return True
    if job_id and job_id in scraped_jobs:
        return True

    # Sprawdzenie w polach itemów existing_data
    for item in existing_data.values():
        if job_id and str(item.get("job_id")) == str(job_id):
            return True
        if offer_id and str(item.get("offer_id")) == str(offer_id):
            return True

    return False


def run_scraper(limit: Optional[int] = None):
    logger.info("=" * 65)
    logger.info(" ROZPOCZYNAM POBIERANIE WYGRANYCH OFERT ZE SKRZYNKI USEME")
    logger.info(f" Plik docelowy: {OUTPUT_FILE}")
    logger.info(f" Checkpoint:    {CHECKPOINT_FILE}")
    logger.info("=" * 65)

    existing_data, checkpoint = load_scraped_data()
    logger.info(f"Wcześniej zapisano w bazie: {len(existing_data)} wygranych zleceń.")

    with BrowserDriver(headless=False) as driver:
        page = driver.context.new_page()

        # 1. Pobierz wszystkie wątki ze skrzynki
        threads = fetch_all_message_threads(page)
        if not threads:
            logger.warning("Nie znaleziono żadnych wątków wiadomości! Kończę pracę.")
            return

        if limit:
            threads = threads[:limit]
            logger.info(f"Ograniczam przetwarzanie do pierwszych {limit} wątków.")

        logger.info(f"Rozpoczynam analizę {len(threads)} wątków...")
        nowe_zapisane = 0
        pominiete_brak_zlecenia = 0
        pominiete_duplikaty = 0

        for idx, t in enumerate(threads, 1):
            tid = t.get("thread_id", "")
            t_url = t.get("thread_url", "")
            subject = t.get("subject", "Brak tematu")
            user = t.get("user_name", "Anonim")

            logger.info(f"[{idx}/{len(threads)}] Sprawdzam wątek #{tid} od '{user}' ('{subject[:40]}')...")

            try:
                # Krok 1: Weryfikacja obecności 'Dotyczy zlecenia'
                job_link_info = check_thread_job(page, t_url)

                if not job_link_info:
                    logger.info("   -> [BRAK ZLECENIA] Wątek nie dotyczy publicznego zlecenia. OLEWAM.")
                    pominiete_brak_zlecenia += 1
                    time.sleep(random.uniform(0.8, 1.5))
                    continue

                job_id = job_link_info.get("job_id", "")
                job_url = job_link_info.get("job_url", "")
                job_title = job_link_info.get("job_title", "")
                logger.info(f"   -> [WYKRYTO ZLECENIE] #{job_id}: '{job_title[:45]}'")

                # Krok 2: Sprawdzenie deduplikacji w systemie
                if job_id and is_already_in_system(job_id=job_id, offer_id="", existing_data=existing_data, checkpoint=checkpoint):
                    logger.info(f"   -> [W SYSTEMIE] Zlecenie #{job_id} jest już w systemie. OLEWAM.")
                    pominiete_duplikaty += 1
                    time.sleep(random.uniform(0.8, 1.5))
                    continue

                # Krok 3: Wejście w zlecenie i pobranie detali
                logger.info(f"   -> Pobieram ofertę i zlecenie: {job_url} ...")
                details = scrape_job_and_offer_details(page, job_url, t, known_job_id=job_id)

                offer_id = details.get("offer_id") or job_id
                # Ponowne sprawdzenie deduplikacji po offer_id
                if offer_id and is_already_in_system(job_id=job_id, offer_id=offer_id, existing_data=existing_data, checkpoint=checkpoint):
                    logger.info(f"   -> [W SYSTEMIE] Oferta #{offer_id} jest już w systemie. OLEWAM.")
                    pominiete_duplikaty += 1
                    continue

                # Zapis rekordu
                record_key = offer_id or job_id or tid
                existing_data[record_key] = details
                save_scraped_data(existing_data)
                nowe_zapisane += 1

                price = details.get("our_price", "brak")
                days = details.get("our_days", "brak")
                client = details.get("client", user)
                logger.info(f"   -> [ZAPISANO SUKCES] Cena: {price} | Dni: {days} | Klient: {client}")

                # Human-like delay anty-ban
                delay = random.uniform(2.0, 3.5)
                logger.info(f"   Czekam {delay:.1f}s przed kolejnym wątkiem...")
                time.sleep(delay)

            except Exception as e:
                logger.error(f"   -> Błąd podczas przetwarzania wątku #{tid}: {e}")
                time.sleep(2.0)

        logger.info("=" * 65)
        logger.info(" PODSUMOWANIE POBIERANIA WYGRANYCH:")
        logger.info(f" Nowo pobranych i zapisanych: {nowe_zapisane}")
        logger.info(f" Pominiętych (brak zlecenia): {pominiete_brak_zlecenia}")
        logger.info(f" Pominiętych (już w systemie): {pominiete_duplikaty}")
        logger.info(f" Łącznie w bazie wygranych:   {len(existing_data)}")
        logger.info("=" * 65)


if __name__ == "__main__":
    run_scraper()
