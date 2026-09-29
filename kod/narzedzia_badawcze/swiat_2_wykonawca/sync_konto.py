# -*- coding: utf-8 -*-
"""
ŚWIAT 2 (WYKONAWCA / OFERTOWARKA - ksawierpotrykus3):
Przyrostowa synchronizacja konta wykonawcy:
1. Sprawdza `/pl/notifications/nots/` oraz `/pl/dashboard/offers/closed/` pod kątem nowo
   zamkniętych (odrzuconych/nieodpisanych) ofert.
2. Pobiera pełne szczegóły nowych zamkniętych ofert (opis zlecenia, naszą propozycję,
   cenę, dni, budżet, klienta, kategorię) i dopisuje je na początek bazy `02_przegrane/`
   (`przegrane_pelne.json` oraz kompatybilne wstecznie `przegrane_pelne_416.json`)
   z 100% zachowaniem wszystkich dotychczasowych rekordów (atomowy zapis `.tmp` -> `os.replace`).
3. Sprawdza `/pl/mesg/mesgs/` pod kątem ewentualnych nowych odpowiedzi od klientów (`03_odpisane/`).
4. Aktualizuje statusy zleceń w `01_ofertowarka/` — przenosi zlecenia ze stanu `WYSLANO` ("niewiadome")
   do `ZAMKNIETE_NIEODPISANE` ("nieodpisane / pewna porażka") lub `ODPOWIEDZ_KLIENTA`.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
COOKIES_PATH = KOD_DIR / "tech" / "cookies.json"
KSAWIER_DIR = BASE_DIR / "badania" / "baza" / "ksawierpotrykus3"
OFERTOWARKA_DIR = KSAWIER_DIR / "01_ofertowarka"
PRZEGRANE_LEGACY = KSAWIER_DIR / "02_przegrane" / "przegrane_pelne_416.json"
PRZEGRANE_CANON = KSAWIER_DIR / "02_przegrane" / "przegrane_pelne.json"
WYGRANE_LEGACY = KSAWIER_DIR / "03_odpisane" / "wygrane_56.json"
WYGRANE_CANON = KSAWIER_DIR / "03_odpisane" / "wygrane.json"
BASE_URL = "https://useme.com"


def atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def create_contractor_session() -> requests.Session:
    if not COOKIES_PATH.exists():
        raise FileNotFoundError(f"Brak pliku cookies wykonawcy: {COOKIES_PATH}")
    cookies_data = json.loads(COOKIES_PATH.read_text(encoding="utf-8"))
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    )
    for c in cookies_data:
        if "name" in c and "value" in c:
            s.cookies.set(c["name"], c["value"], domain=c.get("domain", "useme.com"))
    return s


def extract_job_id_from_url(url: str) -> str | None:
    if not url:
        return None
    m = re.search(r",(\d+)/?(?:\?|$)", url)
    if m:
        return m.group(1)
    m2 = re.search(r"/jobs/(\d+)/", url)
    return m2.group(1) if m2 else None


def scrape_offer_detail(session: requests.Session, offer_id: str, list_meta: dict) -> dict:
    detail_url = f"{BASE_URL}/pl/dashboard/offers/{offer_id}/"
    r = session.get(detail_url, timeout=20)
    if r.status_code != 200:
        return {**list_meta, "offer_id": str(offer_id), "detail_url": detail_url, "error": f"HTTP {r.status_code}"}

    soup = BeautifulSoup(r.text, "html.parser")
    title = list_meta.get("title")
    job_url = list_meta.get("job_url")
    for a in soup.select('a[href*="/pl/jobs/"]'):
        txt = a.get_text(" ", strip=True)
        href = a.get("href", "")
        if txt and len(txt) > 3 and not re.match(r"^\d+\s+ofert", txt):
            if not title:
                title = txt
            if not job_url:
                job_url = urljoin(BASE_URL, href)
            break

    category = list_meta.get("category")
    cat_a = soup.select_one('a[href*="/pl/jobs/categories/"]')
    if cat_a:
        category = cat_a.get_text(" ", strip=True)

    client = list_meta.get("client")
    budget = list_meta.get("budget")
    published = list_meta.get("published")
    validity = list_meta.get("validity")

    for box in soup.select(".jobs-table__box-item"):
        b_txt = box.get_text(" ", strip=True)
        if "Zleceniodawca" in b_txt and not client:
            c_el = box.select_one("strong, a, span:last-child")
            client = c_el.get_text(" ", strip=True) if c_el else b_txt.replace("Zleceniodawca", "").strip()
        elif "Budżet" in b_txt and not budget:
            val_el = box.select_one(".jobs-item__FromTo, strong, p:last-child")
            budget = val_el.get_text(" ", strip=True) if val_el else b_txt.replace("Budżet:", "").strip()
        elif "Opublikowano" in b_txt and not published:
            published = b_txt.replace("Opublikowano", "").strip()
        elif "Ważność" in b_txt and not validity:
            validity = b_txt.replace("Ważność", "").strip()

    job_desc_div = soup.select_one(".job-details__main-desc-body")
    job_description = job_desc_div.get_text("\n", strip=True) if job_desc_div else ""

    if not job_description and job_url:
        try:
            rj = session.get(job_url, timeout=15)
            if rj.status_code == 200:
                sj = BeautifulSoup(rj.text, "html.parser")
                jd = sj.select_one(".job-details__main-desc-body") or sj.select_one(".job-description")
                if jd:
                    job_description = jd.get_text("\n", strip=True)
                if not category:
                    ca = sj.select_one('a[href*="/pl/jobs/categories/"]')
                    if ca:
                        category = ca.get_text(" ", strip=True)
        except Exception:
            pass

    our_proposal = ""
    prop_div = soup.select_one("#offer_desc .text") or soup.select_one("#offer_desc") or soup.select_one(".offer-details__description")
    if prop_div:
        our_proposal = prop_div.get_text("\n", strip=True)
        if our_proposal.startswith("Opis\n"):
            our_proposal = our_proposal[5:].strip()

    our_price = list_meta.get("our_price")
    our_days = list_meta.get("our_days")
    our_Transfer = None

    for col in soup.select(".panel-frame .col-md-4, .job-Offer_table .col"):
        lbl = col.select_one(".label, .text-muted")
        val = col.select_one(".p, .value, strong")
        if lbl and val:
            l_txt = lbl.get_text(" ", strip=True).lower()
            v_txt = val.get_text(" ", strip=True)
            if "kwota" in l_txt or "stawka" in l_txt or "cena" in l_txt:
                our_price = v_txt
            elif "czas" in l_txt or "dni" in l_txt or "termin" in l_txt:
                our_days = v_txt
            elif "praw" in l_txt:
                our_Transfer = v_txt

    return {
        "offer_id": str(offer_id),
        "title": title,
        "job_url": job_url,
        "detail_url": detail_url,
        "client": client,
        "budget": budget,
        "category": category,
        "published": published,
        "validity": validity,
        "job_description": job_description,
        "our_proposal": our_proposal,
        "our_price": our_price,
        "our_days": our_days,
        "our_Transfer": our_Transfer,
    }


def main() -> None:
    session = create_contractor_session()

    existing_przegrane = json.loads(PRZEGRANE_LEGACY.read_text(encoding="utf-8"))
    existing_wygrane = json.loads(WYGRANE_LEGACY.read_text(encoding="utf-8"))
    existing_closed_ids = {str(x["offer_id"]) for x in existing_przegrane if x.get("offer_id")}
    existing_won_offer_ids = {str(x.get("offer_id")) for x in existing_wygrane if x.get("offer_id")}
    existing_won_job_ids = {str(x.get("job_id")) for x in existing_wygrane if x.get("job_id")}

    print(
        f"[ŚWIAT 2 - START] Baza przegrane: {len(existing_przegrane)} | "
        f"Baza odpisane (wygrane): {len(existing_wygrane)}"
    )

    # 1. Sprawdź powiadomienia
    notif_closed_ids = {}
    for p in range(1, 5):
        url = f"{BASE_URL}/pl/notifications/nots/" if p == 1 else f"{BASE_URL}/pl/notifications/nots/?page={p}"
        r = session.get(url, timeout=20)
        if r.status_code != 200 or "/users/login" in r.url:
            raise RuntimeError(f"Sesja wykonawcy wygasła lub niedostępna (HTTP {r.status_code})")
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".notifications-list__item, .notification-item, li, tr, .panel")
        found_on_p = 0
        for it in items:
            txt = it.get_text(" ", strip=True)
            if "nie została wybrana" in txt or "została odrzucona" in txt:
                for a in it.select("a[href]"):
                    m = re.search(r"/dashboard/offers/(\d+)/", a.get("href", ""))
                    if m:
                        oid = m.group(1)
                        if oid not in notif_closed_ids:
                            notif_closed_ids[oid] = {"offer_id": oid, "title": a.get_text(" ", strip=True)}
                            found_on_p += 1
        if found_on_p == 0 and p > 1:
            break

    # 2. Sprawdź listę zamkniętych ofert (/pl/dashboard/offers/closed/)
    closed_meta_by_id = {}
    for p in range(1, 15):
        url = f"{BASE_URL}/pl/dashboard/offers/closed/" if p == 1 else f"{BASE_URL}/pl/dashboard/offers/closed/?page={p}"
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.select('a[href*="/dashboard/offers/"]')
        new_on_page = 0
        for a in links:
            m = re.search(r"/dashboard/offers/(\d+)/", a.get("href", ""))
            if not m:
                continue
            oid = m.group(1)
            if oid in existing_closed_ids or oid in existing_won_offer_ids:
                continue
            if oid not in closed_meta_by_id:
                new_on_page += 1
                card = a.find_parent(class_=re.compile(r"job|offer|row|item|card|panel|box")) or a.parent.parent
                card_txt = card.get_text(" | ", strip=True) if card else ""
                m_price = re.search(r"Kwota brutto:\s*([\d\s,.]+\s*[A-Z]{3})", card_txt)
                m_client = re.search(r"Zleceniodawca\s*\|\s*([^|]+)", card_txt)
                m_pub = re.search(r"Opublikowano\s*\|\s*(\d{2}\.\d{2}\.\d{4})", card_txt)
                m_val = re.search(r"Ważność\s*\|\s*([^|]+)", card_txt)
                closed_meta_by_id[oid] = {
                    "offer_id": oid,
                    "title": a.get_text(" ", strip=True),
                    "our_price": m_price.group(1).strip() if m_price else None,
                    "client": m_client.group(1).strip() if m_client else None,
                    "published": m_pub.group(1).strip() if m_pub else None,
                    "validity": m_val.group(1).strip() if m_val else None,
                }
        if new_on_page == 0 and p >= 3:
            break
        time.sleep(0.4)

    for oid, meta in notif_closed_ids.items():
        if oid not in existing_closed_ids and oid not in existing_won_offer_ids and oid not in closed_meta_by_id:
            closed_meta_by_id[oid] = meta

    new_closed_records = []
    for oid in sorted(closed_meta_by_id.keys(), key=lambda x: int(x), reverse=True):
        print(f"  -> Pobieranie szczegółów nowej zamkniętej oferty #{oid}...")
        rec = scrape_offer_detail(session, oid, closed_meta_by_id[oid])
        new_closed_records.append(rec)
        time.sleep(0.5)

    updated_przegrane = new_closed_records + existing_przegrane
    atomic_write_json(PRZEGRANE_LEGACY, updated_przegrane)
    atomic_write_json(PRZEGRANE_CANON, updated_przegrane)
    atomic_write_json(WYGRANE_CANON, existing_wygrane)

    # 3. Mapuj wszystkie zamknięte i wygrane oferty na 01_ofertowarka
    closed_by_job_id = {}
    closed_by_title = {}
    for rec in updated_przegrane:
        jid = extract_job_id_from_url(rec.get("job_url") or "")
        if jid:
            closed_by_job_id[jid] = rec
        t_norm = (rec.get("title") or "").strip().lower()
        if t_norm:
            closed_by_title[t_norm] = rec

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    moved_count = 0
    stats_status = {}

    for json_file in sorted(OFERTOWARKA_DIR.rglob("*.json")):
        if not json_file.stem.isdigit() or any(p.startswith(".") for p in json_file.parts):
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        jid = str(data.get("id", ""))
        title_norm = (data.get("title") or "").strip().lower()
        cur_status = data.get("status", "")
        cur_koncowy = data.get("status_koncowy", "")

        matched_closed = closed_by_job_id.get(jid) or closed_by_title.get(title_norm)
        if jid in existing_won_job_ids and cur_koncowy != "ODPOWIEDZ_KLIENTA":
            data["status"] = "ODPISANE"
            data["status_koncowy"] = "ODPOWIEDZ_KLIENTA"
            data["data_weryfikacji"] = now_str
            atomic_write_json(json_file, data)
            moved_count += 1
        elif matched_closed and cur_status == "WYSLANO" and cur_koncowy != "ZAMKNIETE_NIEODPISANE":
            data["status"] = "ZAMKNIETE"
            data["status_koncowy"] = "ZAMKNIETE_NIEODPISANE"
            data["data_weryfikacji"] = now_str
            data["closed_offer_id"] = str(matched_closed.get("offer_id"))
            atomic_write_json(json_file, data)
            moved_count += 1

        st_key = data.get("status_koncowy") or data.get("status") or "NIEZNANY"
        stats_status[st_key] = stats_status.get(st_key, 0) + 1

    print(
        f"[ŚWIAT 2 - KONIEC] Baza przegrane: {len(updated_przegrane)} (+{len(new_closed_records)} nowych) | "
        f"Przeniesiono w 01_ofertowarka: {moved_count}"
    )
    print("  Rozkład statusów w 01_ofertowarka:", json.dumps(stats_status, ensure_ascii=False))


if __name__ == "__main__":
    main()
