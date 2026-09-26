# -*- coding: utf-8 -*-
"""Pobieracz ofert konkurencji pod zleceniem zleceniodawcy na Useme.

Pobiera wszystkie nadesłane oferty dla danego zlecenia (np. #144890),
obsługuje paginację, wyciąga pełne teksty ofert, stawki, terminy, profile i linki,
pamięta już pobrane oferty w checkpointcie i aktualizuje bazę przy kolejnych uruchomieniach.
"""

from __future__ import annotations

import datetime
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ScraperOfertZleceniodawcy")

BASE_DIR = Path(__file__).resolve().parent
# Zlecenia testowe: badania/baza/weronikabuchholc13/04_moje_zlecenia/
DATA_DIR = config.MOJE_ZLECENIA_DIR
TECH_DIR = BASE_DIR / "tech"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_JOB_ID = "144890"
COOKIES_FILE = TECH_DIR / "cookies_zleceniodawca.json"


def get_output_paths(job_id: str):
    job_dir = DATA_DIR / f"zlecenie_testowe_{job_id}"
    job_dir.mkdir(parents=True, exist_ok=True)
    output_file = job_dir / f"oferty_publiczne_30.json"
    checkpoint_file = job_dir / f"oferty_checkpoint.json"
    return output_file, checkpoint_file


def load_checkpoint(checkpoint_file: Path) -> Dict[str, Any]:
    if checkpoint_file.exists():
        try:
            return json.loads(checkpoint_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"Błąd odczytu checkpointu: {e}")
    return {
        "last_run": None,
        "total_offers": 0,
        "known_offer_ids": []
    }


def save_checkpoint(checkpoint_file: Path, known_ids: List[str]):
    data = {
        "last_run": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_offers": len(known_ids),
        "known_offer_ids": known_ids
    }
    checkpoint_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_existing_offers(output_file: Path) -> Dict[str, Dict[str, Any]]:
    if output_file.exists():
        try:
            items = json.loads(output_file.read_text(encoding="utf-8"))
            return {str(it.get("offer_id")): it for it in items if it.get("offer_id")}
        except Exception as e:
            logger.warning(f"Błąd odczytu bazy ofert: {e}")
    return {}


def create_session() -> requests.Session:
    if not COOKIES_FILE.exists():
        raise FileNotFoundError(f"Brak pliku ciasteczek: {COOKIES_FILE}")

    session = requests.Session()
    cookies_data = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
    for c in cookies_data:
        session.cookies.set(c["name"], c["value"], domain=c.get("domain", "useme.com"))

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://useme.com/pl/"
    })
    return session


def parse_offer_card(card: BeautifulSoup, job_id: str) -> Optional[Dict[str, Any]]:
    # 1. ID oferty
    chk = card.select_one("input[data-select-offer-id]")
    offer_id = chk.get("data-select-offer-id") if chk else None
    if not offer_id:
        # szukajmy w linkach
        for a in card.find_all("a"):
            m = re.search(r"/offer[s]?/(\d+)", a.get("href", ""))
            if m:
                offer_id = m.group(1)
                break

    if not offer_id:
        return None

    # 2. Wykonawca i profil
    author_a = card.select_one('a[href*="/roles/contractor/"]')
    author_url = None
    author_name = None
    if author_a:
        author_url = "https://useme.com" + author_a.get("href") if author_a.get("href").startswith("/") else author_a.get("href")
        author_name = author_a.get_text(strip=True)
        if author_name == "Zobacz profil":
            # Wyciągnijmy z URL np. ailone,679974 -> ailone
            m_slug = re.search(r'/roles/contractor/([^,/]+)', author_url)
            author_name = m_slug.group(1) if m_slug else "Wykonawca"

    # Liczba umów wykonawcy
    card_text = card.get_text(" ", strip=True)
    contracts_m = re.search(r'(\d+)\s+um[óo]w', card_text, re.IGNORECASE)
    contracts = contracts_m.group(0) if contracts_m else "0 umów"

    # 3. Cena i czas realizacji
    price_el = card.select_one(".dashboard-list__item-stats-prop--green, [class*='stats-prop--green']")
    price = price_el.get_text(strip=True) if price_el else None

    days = None
    stats_props = card.select(".dashboard-list__item-stats-prop")
    for sp in stats_props:
        txt = sp.get_text(strip=True)
        if "dni" in txt.lower():
            days = txt
        elif not price and "pln" in txt.lower():
            price = txt

    # 4. Pełna treść oferty
    desc_el = card.select_one(".dashboard-list__item-description")
    if desc_el:
        proposal_text = desc_el.get_text("\n", strip=True)
    else:
        paras = [p.get_text(strip=True) for p in card.find_all("p") if p.get_text(strip=True)]
        proposal_text = "\n\n".join(paras)

    # Oczyszczenie z przycisków "Zobacz pełny opis" / "Zwiń"
    proposal_text = re.sub(r'\b(Zobacz pełny opis|Zwiń)\b', '', proposal_text).strip()

    # 5. Linki i załączniki w ofercie
    links = []
    if desc_el:
        for a in desc_el.find_all("a"):
            href = a.get("href")
            if href and not href.startswith("#") and href not in links:
                links.append(href)

    # Link do wysłania wiadomości
    msg_a = card.select_one('a[href*="/mesg/compose/"]')
    msg_url = ("https://useme.com" + msg_a.get("href")) if msg_a and msg_a.get("href").startswith("/") else (msg_a.get("href") if msg_a else None)

    return {
        "offer_id": str(offer_id),
        "job_id": str(job_id),
        "author_name": author_name,
        "author_profile_url": author_url,
        "author_contracts": contracts,
        "price": price,
        "days": days,
        "proposal_text": proposal_text,
        "proposal_length": len(proposal_text),
        "links": links,
        "msg_url": msg_url,
        "scraped_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def fetch_all_offers_for_job(job_id: str = DEFAULT_JOB_ID):
    output_file, checkpoint_file = get_output_paths(job_id)
    checkpoint = load_checkpoint(checkpoint_file)
    existing_offers = load_existing_offers(output_file)

    logger.info(f"=== ROZPOCZYNAM POBIERANIE OFERT DLA ZLECENIA #{job_id} ===")
    logger.info(f"Wcześniej pobranych ofert: {len(existing_offers)}")

    session = create_session()

    page_num = 1
    new_count = 0
    updated_count = 0
    total_found = 0

    while True:
        url = f"https://useme.com/pl/jobs/{job_id}/offers/?page={page_num}" if page_num > 1 else f"https://useme.com/pl/jobs/{job_id}/offers/"
        logger.info(f"Pobieram stronę {page_num}: {url}")

        r = session.get(url, timeout=30)
        if "/users/login" in r.url:
            logger.error("Sesja w tech/cookies_zleceniodawca.json wygasła (przekierowanie do logowania)! Odśwież sesję: python login_useme.py zleceniodawca")
            return
        if r.status_code != 200:
            logger.warning(f"Strona {page_num} zwróciła kod {r.status_code}. Kończę paginację.")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select(".dashboard-list__item-offer")
        if not cards:
            logger.info(f"Brak ofert na stronie {page_num}. Koniec.")
            break

        logger.info(f"Znaleziono {len(cards)} ofert na stronie {page_num}.")
        total_found += len(cards)

        for card in cards:
            parsed = parse_offer_card(card, job_id)
            if not parsed:
                continue

            oid = parsed["offer_id"]
            if oid not in existing_offers:
                existing_offers[oid] = parsed
                new_count += 1
                logger.info(f" -> NOWA OFERTA #{oid} od {parsed['author_name']} | Cena: {parsed['price']} | Dni: {parsed['days']}")
            else:
                # Aktualizacja (np. zmiana ceny/opisu)
                existing_offers[oid].update(parsed)
                updated_count += 1

        # Sprawdzenie czy jest następna strona
        # Szukamy linku do page=page_num + 1
        next_page = page_num + 1
        has_next = bool(soup.select_one(f'a[href*="page={next_page}"]'))
        if not has_next:
            logger.info("Osiągnięto ostatnią stronę ofert.")
            break

        page_num += 1
        time.sleep(1.0)  # Pacing

    # Zapis danych
    offers_list = sorted(list(existing_offers.values()), key=lambda x: int(x.get("offer_id", 0)), reverse=True)
    output_file.write_text(json.dumps(offers_list, ensure_ascii=False, indent=2), encoding="utf-8")
    save_checkpoint(checkpoint_file, [o["offer_id"] for o in offers_list])

    logger.info("=" * 60)
    logger.info(f"ZAKOŃCZONO POBIERANIE OFERT DLA ZLECENIA #{job_id}")
    logger.info(f"Nowych dodanych: {new_count}")
    logger.info(f"Zaktualizowanych: {updated_count}")
    logger.info(f"Łącznie w bazie: {len(offers_list)}")
    logger.info(f"Plik wynikowy: {output_file}")
    logger.info("=" * 60)

    return offers_list


if __name__ == "__main__":
    jid = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB_ID
    fetch_all_offers_for_job(jid)
