# -*- coding: utf-8 -*-
"""
ŚWIAT 1 (ZLECENIODAWCA / MYSTERY SHOPPING - weronikabuchholc13):
Przyrostowa synchronizacja ofert publicznych oraz wątków wiadomości prywatnych (PV)
dla zlecenia testowego (domyślnie #144890).

Zasada działania:
1. Nigdy nie kasuje istniejących rekordów — wczytuje obecną bazę i dokleja/aktualizuje
   wyłącznie nowe oferty oraz nowe wiadomości w wątkach PV (atomowy zapis .tmp -> os.replace).
2. Wspiera zarówno otwarte, jak i zamknięte zlecenia (fallback na offer-toggle-favorite[data-offer-pk]
   oraz div#offer_<id>_description).
3. Zapisuje czyste pliki kanoniczne (oferty_publiczne.json, wiadomosci_prywatne_pelne.json,
   raport_wiadomosci_prywatnych_zleceniodawcy.md) oraz zachowuje kompatybilność wsteczną
   (oferty_publiczne_30.json, wiadomosci_zleceniodawcy_pelne.json).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
COOKIES_PATH = KOD_DIR / "tech" / "cookies_zleceniodawca.json"
DEFAULT_JOB_ID = "144890"
DEFAULT_OUT_DIR = (
    BASE_DIR
    / "badania"
    / "baza"
    / "weronikabuchholc13"
    / "04_moje_zlecenia"
    / "zlecenie_testowe_144890"
)
BASE_URL = "https://useme.com"


def atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def create_employer_session(cookies_path: Path = COOKIES_PATH) -> requests.Session:
    if not cookies_path.exists():
        raise FileNotFoundError(f"Brak pliku cookies zleceniodawcy: {cookies_path}")
    cookies_data = json.loads(cookies_path.read_text(encoding="utf-8"))
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


def parse_offer_card(card) -> dict | None:
    oid = None
    inp = card.select_one("input[data-select-offer-id]")
    if inp:
        oid = inp.get("data-select-offer-id")
    if not oid:
        fav = card.select_one("offer-toggle-favorite[data-offer-pk]")
        if fav:
            oid = fav.get("data-offer-pk")
    if not oid:
        desc_div = card.select_one('div[id^="offer_"][id$="_description"]')
        if desc_div:
            m = re.search(r"offer_(\d+)_description", desc_div.get("id", ""))
            if m:
                oid = m.group(1)
    if not oid:
        return None

    user_el = card.select_one(".job-Offer_userName")
    author_name = user_el.get_text(strip=True) if user_el else None
    author_url = user_el.get("href") if user_el else None

    user_id = None
    avatar_el = card.select_one("[data-user-id]")
    if avatar_el:
        user_id = avatar_el.get("data-user-id")

    contracts_el = card.select_one(".job-Offer_userContracts")
    contracts_text = contracts_el.get_text(" ", strip=True) if contracts_el else "0 umów"

    pub_date = None
    for muted in card.select(".text-muted.small"):
        txt = muted.get_text(" ", strip=True)
        if "Opublikowano:" in txt:
            pub_date = txt.replace("Opublikowano:", "").strip()
            break

    desc_el = card.select_one(f"#offer_{oid}_description") or card.select_one(".job-Offer_description")
    proposal_text = desc_el.get_text("\n", strip=True) if desc_el else ""
    proposal_links = [a.get("href") for a in desc_el.select("a[href]") if a.get("href")] if desc_el else []

    attachments = []
    for att in card.select(".job-Offer_files a[href]"):
        attachments.append({"name": att.get_text(strip=True), "url": urljoin(BASE_URL, att.get("href"))})

    price_gross = None
    work_days = None
    copyright_transfer = None
    for col in card.select(".job-Offer_table .col"):
        val_el = col.select_one(".value")
        lbl_el = col.select_one(".text-muted")
        if val_el and lbl_el:
            val = val_el.get_text(" ", strip=True)
            lbl = lbl_el.get_text(" ", strip=True).lower()
            if "stawka" in lbl or "kwota" in lbl or "cena" in lbl:
                price_gross = val
            elif "czas" in lbl or "dni" in lbl or "termin" in lbl:
                work_days = val
            elif "praw" in lbl or "autorsk" in lbl:
                copyright_transfer = val

    return {
        "offer_id": str(oid),
        "user_id": str(user_id) if user_id else None,
        "author_name": author_name,
        "author_url": urljoin(BASE_URL, author_url) if author_url else None,
        "author_contracts": contracts_text,
        "published_at": pub_date,
        "price": price_gross,
        "days": work_days,
        "copyright": copyright_transfer,
        "proposal_text": proposal_text,
        "proposal_links": proposal_links,
        "attachments": attachments,
    }


def sync_public_offers(session: requests.Session, job_id: str, out_dir: Path) -> list[dict]:
    legacy_file = out_dir / "oferty_publiczne_30.json"
    canon_file = out_dir / "oferty_publiczne.json"

    existing_list = []
    for candidate in (canon_file, legacy_file):
        if candidate.exists():
            try:
                existing_list = json.loads(candidate.read_text(encoding="utf-8"))
                break
            except Exception:
                pass

    existing_by_id = {str(x["offer_id"]): x for x in existing_list if x.get("offer_id")}
    initial_count = len(existing_by_id)

    base_job_url = f"{BASE_URL}/pl/jobs/{job_id}/"
    r0 = session.get(base_job_url, timeout=25, allow_redirects=True)
    if r0.status_code != 200 or "/users/login" in r0.url:
        raise RuntimeError(f"Błąd autoryzacji na koncie zleceniodawcy (HTTP {r0.status_code}, URL: {r0.url})")
    canonical_job_url = r0.url.split("?")[0]

    new_offers = []
    for page in range(1, 25):
        url = canonical_job_url if page == 1 else f"{canonical_job_url}?page={page}"
        r = session.get(url, timeout=25) if page > 1 else r0
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select(".job-Offer")
        if not cards:
            break
        added_on_page = 0
        for c in cards:
            parsed = parse_offer_card(c)
            if not parsed:
                continue
            oid = parsed["offer_id"]
            if oid not in existing_by_id:
                existing_by_id[oid] = parsed
                new_offers.append(parsed)
                added_on_page += 1
            else:
                # Uzupełnij brakujące pola, zachowując istniejące dane
                existing_by_id[oid].update({k: v for k, v in parsed.items() if v is not None})
        print(f"  [Oferty Strona {page}] Kart: {len(cards)} | Nowych: {added_on_page} | Łącznie w bazie: {len(existing_by_id)}")
        next_link = soup.select_one(f'a[href*="page={page+1}"]')
        if not next_link:
            break
        time.sleep(1.0)

    # Sortuj malejąco po offer_id (od najnowszych do najstarszych)
    final_offers = sorted(existing_by_id.values(), key=lambda x: int(x["offer_id"]), reverse=True)
    atomic_write_json(canon_file, final_offers)
    atomic_write_json(legacy_file, final_offers)
    oferty_dir = out_dir / "oferty"
    oferty_dir.mkdir(parents=True, exist_ok=True)
    for o in final_offers:
        oid = str(o.get("offer_id") or "")
        if oid:
            atomic_write_json(oferty_dir / f"{oid}.json", o)
    print(f"[ŚWIAT 1 - OFERTY] Baza przed: {initial_count} -> Po synchronizacji: {len(final_offers)} (+{len(new_offers)} nowych; zapisano do oferty/).")
    return final_offers


def sync_private_messages(session: requests.Session, offers: list[dict], out_dir: Path) -> list[dict]:
    offers_by_uid = {str(o["user_id"]): o for o in offers if o.get("user_id")}
    offers_by_name = {(o["author_name"] or "").strip().lower(): o for o in offers if o.get("author_name")}

    canon_json = out_dir / "wiadomosci_prywatne_pelne.json"
    legacy_json = out_dir / "wiadomosci_zleceniodawcy_pelne.json"
    existing_threads = {}
    for candidate in (canon_json, legacy_json):
        if candidate.exists():
            try:
                loaded = json.loads(candidate.read_text(encoding="utf-8"))
                existing_threads = {str(t["thread_id"]): t for t in loaded if t.get("thread_id")}
                break
            except Exception:
                pass
    initial_threads_count = len(existing_threads)

    threads_meta = []
    seen_tids = set()
    for page in range(1, 15):
        list_url = f"{BASE_URL}/pl/mesg/mesgs/" if page == 1 else f"{BASE_URL}/pl/mesg/mesgs/?page={page}"
        r = session.get(list_url, timeout=20)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("a.messages-list-item[href]")
        if not items:
            break
        new_on_page = 0
        for item in items:
            href = item.get("href", "")
            m = re.search(r"/mesg/mesgs/(\d+)/", href)
            tid = m.group(1) if m else None
            if not tid or tid in seen_tids:
                continue
            seen_tids.add(tid)
            new_on_page += 1
            header = item.select_one(".messages-list-item__header")
            author_el = header.select_one("span") if header else None
            time_el = item.select_one(".messages-list-item__send-time")
            subj_el = item.select_one(".messages-list-item__subject span")
            threads_meta.append(
                {
                    "thread_id": tid,
                    "url": urljoin(BASE_URL, href),
                    "author_name": author_el.get_text(strip=True) if author_el else "",
                    "last_send_time": time_el.get_text(strip=True) if time_el else "",
                    "subject": subj_el.get_text(strip=True) if subj_el else "",
                }
            )
        if new_on_page == 0:
            break
        time.sleep(0.5)

    all_threads = []
    for t in threads_meta:
        r_t = session.get(t["url"], timeout=20)
        s_t = BeautifulSoup(r_t.text, "html.parser")

        uid = None
        for el in s_t.select("[data-user-id]"):
            cand = el.get("data-user-id")
            if cand and str(cand) != "702683":
                uid = str(cand)
                break

        matched_offer = None
        if uid and uid in offers_by_uid:
            matched_offer = offers_by_uid[uid]
        else:
            norm = t["author_name"].strip().lower().replace(" ", "-")
            for k, o in offers_by_name.items():
                if k == t["author_name"].strip().lower() or k == norm or t["author_name"].strip().lower() in k:
                    matched_offer = o
                    break

        messages = []
        for msg in s_t.select(".message"):
            sender_el = msg.select_one(".message__user-data strong") or msg.select_one(".message__sender")
            sender = sender_el.get_text(strip=True) if sender_el else None
            date_el = msg.select_one(".message__user-data span") or msg.select_one(".message__date")
            m_date = date_el.get_text(strip=True) if date_el else None
            body_el = msg.select_one(".message__body") or msg.select_one(".message__content")
            text = body_el.get_text("\n", strip=True) if body_el else msg.get_text("\n", strip=True)
            links = [a.get("href") for a in (body_el or msg).select("a[href]") if a.get("href")]
            messages.append({"sender": sender, "date": m_date, "text": text, "links": links})

        entry = {
            **t,
            "counterpart_user_id": uid,
            "has_submitted_offer": matched_offer is not None,
            "matched_offer_id": matched_offer["offer_id"] if matched_offer else None,
            "matched_offer_price": matched_offer["price"] if matched_offer else None,
            "matched_offer_days": matched_offer["days"] if matched_offer else None,
            "matched_offer_author": matched_offer["author_name"] if matched_offer else None,
            "messages_count": len(messages),
            "messages": messages,
        }
        existing_threads[t["thread_id"]] = entry
        all_threads.append(entry)
        time.sleep(0.5)

    # Zachowaj też ewentualne starsze wątki, gdyby zniknęły z paginacji
    for tid, old_t in existing_threads.items():
        if tid not in {x["thread_id"] for x in all_threads}:
            all_threads.append(old_t)

    all_threads.sort(key=lambda x: int(x["thread_id"]), reverse=True)
    atomic_write_json(canon_json, all_threads)
    atomic_write_json(legacy_json, all_threads)
    wiad_dir = out_dir / "wiadomosci"
    wiad_dir.mkdir(parents=True, exist_ok=True)
    for t in all_threads:
        tid = str(t.get("thread_id") or t.get("thread_pk") or "")
        if tid:
            atomic_write_json(wiad_dir / f"watek_{tid}.json", t)

    # Generuj czytelny raport Markdown
    md_lines = [
        "# RAPORT PRYWATNYCH WIADOMOŚCI OD WYKONAWCÓW (USEME #144890)\n",
        f"> Pobrane wątki ze skrzynki zleceniodawcy: **{len(all_threads)}**",
        f"> Złożyli również ofertę publiczną: **{sum(1 for x in all_threads if x['has_submitted_offer'])}**",
        f"> Napisali TYLKO na priv (bez oferty): **{sum(1 for x in all_threads if not x['has_submitted_offer'])}**",
        f"> Ostatnia aktualizacja: `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n",
        "=" * 80 + "\n",
    ]
    for idx, t in enumerate(all_threads, 1):
        status_str = (
            f"✅ **ZŁOŻYŁ OFERTĘ PUBLICZNĄ** (#{t['matched_offer_id']}, `{t['matched_offer_author']}`, "
            f"Cena: **{t['matched_offer_price']}**, Czas: {t['matched_offer_days']})"
            if t["has_submitted_offer"]
            else "❌ **BRAK OFERTY PUBLICZNEJ** (pisze TYLKO na priv bez składania oferty!)"
        )
        md_lines.append(f"## {idx}. Rozmówca: **{t['author_name']}** (User ID: `{t['counterpart_user_id']}`)")
        md_lines.append(f"- **Temat:** {t['subject']}")
        md_lines.append(f"- **Wątek ID:** `{t['thread_id']}` | **Ostatnia aktywność:** `{t['last_send_time']}`")
        md_lines.append(f"- **STATUS OFERTY:** {status_str}\n")
        md_lines.append("### Treść wiadomości w wątku:\n")
        for m in t["messages"]:
            md_lines.append(f"> **Nadawca:** {m['sender']} | **Data:** {m['date']}\n")
            md_lines.append(f"{m['text']}\n")
            if m["links"]:
                md_lines.append(f"*Linki w wiadomości:* {', '.join(m['links'])}\n")
            md_lines.append("---\n")
        md_lines.append("\n" + "=" * 80 + "\n")

    md_path = out_dir / "raport_wiadomosci_prywatnych_zleceniodawcy.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(
        f"[ŚWIAT 1 - PRIV] Wątki przed: {initial_threads_count} -> Po synchronizacji: {len(all_threads)} "
        f"(+{len(all_threads) - initial_threads_count} nowych)."
    )
    return all_threads


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronizacja ofert i wiadomości PV ze zlecenia Useme (Świat 1).")
    parser.add_argument("--job-id", default=DEFAULT_JOB_ID, help="ID zlecenia na Useme (domyślnie 144890)")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Katalog docelowy zapisu danych")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    session = create_employer_session()
    offers = sync_public_offers(session, args.job_id, out_dir)
    sync_private_messages(session, offers, out_dir)


if __name__ == "__main__":
    main()
