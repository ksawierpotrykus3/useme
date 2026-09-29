# -*- coding: utf-8 -*-
"""feedback.py — jeden plik do zbierania feedbacku z Useme (per konto).

Zbiera TYLKO 3 rzeczy (ofertowarka/engine.py robi reszte sama):
  1. Wiadomosci prywatne  -> badania/baza/<konto>/05_kontakty.json
  2. Porazki              -> badania/baza/<konto>/02_przegrane/
  3. Wrzucone zlecenia    -> badania/baza/<konto>/04_moje_zlecenia/

Useme ma API JSON (naglowek Accept: application/json) - nie parsujemy HTML dla wiadomosci.
  - Lista watkow:  GET /pl/mesg/mesgs/           -> {results:[{pk,subject,is_offer_inquiry,
                                                       thread_size,user_to_display,last_timestamp,...}]}
  - Tresc watku:   GET /pl/mesg/mesgs/{pk}/thread -> {results:[{pk,content,...}]}

Uzycie:
    python kod/feedback.py --konto konto1 --wiadomosci
    python kod/feedback.py --konto konto1 --porazki
    python kod/feedback.py --konto konto1 --wrzucone
    python kod/feedback.py --konto all --wszystko
    python kod/feedback.py --konto konto1 --wiadomosci --dry-run

Konta i foldery pochodza z config.ACCOUNTS (pole baza_id). Brak cookies -> czytelny blad i stop.
"""
from __future__ import annotations

import argparse
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "https://useme.com"
BAZA_DIR = Path(config.BAZA_DIR)


# ----------------------------------------------------------------------------
# Cookies / sesja
# ----------------------------------------------------------------------------
def _konta_wybrane(sel: str) -> list[dict]:
    if sel == "all":
        return list(config.ACCOUNTS)
    dopasowane = [k for k in config.ACCOUNTS if k["id"] == sel]
    if not dopasowane:
        dostepne = ", ".join(k["id"] for k in config.ACCOUNTS)
        raise SystemExit(f"[BLAD] Nieznane konto '{sel}'. Dostepne: {dostepne}, all")
    return dopasowane


def zbuduj_sesje(konto: dict) -> requests.Session:
    cookies_path = Path(konto["cookies_path"])
    if not cookies_path.exists():
        raise SystemExit(
            f"[BLAD] Brak cookies dla {konto['id']} ({cookies_path.name}).\n"
            f"       Sesja wygasla lub konto nie jest zalogowane.\n"
            f"       Wrzuc swiezy plik cookies do: {cookies_path}\n"
            f"       i uruchom ponownie."
        )
    try:
        dane = json.loads(cookies_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"[BLAD] Nie moge odczytac cookies {cookies_path.name}: {e}")

    s = requests.Session()
    s.headers.update({
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"),
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    for c in dane:
        if "name" in c and "value" in c:
            s.cookies.set(c["name"], c["value"], domain=c.get("domain", "useme.com"))
    return s


def _get_json(sesja: requests.Session, url: str):
    """GET z Accept: application/json. Zwraca (json|None, status, final_url)."""
    r = sesja.get(url, timeout=25, allow_redirects=True,
                  headers={"Accept": "application/json, text/plain, */*"})
    ct = r.headers.get("Content-Type", "")
    if "/users/login" in r.url:
        return None, r.status_code, r.url
    if r.status_code == 200 and "json" in ct:
        try:
            return r.json(), r.status_code, r.url
        except Exception:
            return None, r.status_code, r.url
    return None, r.status_code, r.url


def _sprawdz_sesje(sesja: requests.Session, konto: dict) -> None:
    data, status, url = _get_json(sesja, f"{BASE_URL}/pl/mesg/mesgs/")
    if data is None:
        raise SystemExit(
            f"[BLAD] Sesja dla {konto['id']} wygasla lub brak dostepu (status {status}).\n"
            f"       Wrzuc swiezy plik cookies ({Path(konto['cookies_path']).name}) i uruchom ponownie."
        )


def _katalog_konta(konto: dict) -> Path:
    return BAZA_DIR / konto["baza_id"]


def _atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _html_do_tekstu(html: str) -> str:
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text("\n", strip=True)


# ----------------------------------------------------------------------------
# WIADOMOSCI -> 05_kontakty.json
# ----------------------------------------------------------------------------
def _znane_tytuly(katalog: Path) -> dict[str, str]:
    """Zwraca {tytul_lower: job_id} z danego katalogu (01_ofertowarka / 04_moje_zlecenia)."""
    mapa: dict[str, str] = {}
    if not katalog.exists():
        return mapa
    for p in katalog.rglob("*.json"):
        if p.name.startswith(".") or not p.stem.isdigit():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        t = (d.get("title") or "").strip().lower()
        if t:
            mapa[t] = p.stem
    return mapa


def _scrapuj_liste_watkow(sesja: requests.Session) -> list[dict]:
    """Pobiera wszystkie watki PV z API (JSON)."""
    watki: list[dict] = []
    seen: set = set()
    page = 1
    while page <= 60:
        url = f"{BASE_URL}/pl/mesg/mesgs/" if page == 1 else f"{BASE_URL}/pl/mesg/mesgs/?page={page}"
        data, status, _ = _get_json(sesja, url)
        if not data:
            break
        results = data.get("results", [])
        if not results:
            break
        for t in results:
            pk = str(t.get("pk"))
            if pk in seen:
                continue
            seen.add(pk)
            watki.append(t)
        if not data.get("links", {}).get("next"):
            break
        page += 1
        time.sleep(0.3)
    return watki


def _scrapuj_tresc_watku(sesja: requests.Session, pk: str) -> list[dict]:
    """Pobiera tresc wiadomosci watku z API. Zwraca liste {sender,date,text}."""
    data, status, _ = _get_json(sesja, f"{BASE_URL}/pl/mesg/mesgs/{pk}/thread")
    if not data:
        return []
    wiadomosci = []
    for m in data.get("results", []):
        tresc = _html_do_tekstu(m.get("content", ""))
        wiadomosci.append({
            "pk": m.get("pk"),
            "sender": m.get("sender") or m.get("user_to_display", {}).get("name") if isinstance(m.get("user_to_display"), dict) else m.get("sender"),
            "date": m.get("sent_on") or m.get("created") or m.get("date"),
            "text": tresc,
        })
    return wiadomosci


def _klasyfikuj_watek(subject: str, tytuly_ofert: dict, tytuly_zlecen: dict, is_offer_inquiry) -> str:
    """'offer' / 'job' / 'bez_kontekstu'."""
    s = (subject or "").strip().lower()
    if s:
        for t, jid in tytuly_ofert.items():
            if t and (t in s or s in t):
                return "offer"
        for t, jid in tytuly_zlecen.items():
            if t and (t in s or s in t):
                return "job"
    return "bez_kontekstu"


def zbierz_wiadomosci(konto: dict, dry_run: bool = False) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    tytuly_ofert = _znane_tytuly(_katalog_konta(konto) / "01_ofertowarka")
    tytuly_zlecen = _znane_tytuly(_katalog_konta(konto) / "04_moje_zlecenia")

    kontakty_path = _katalog_konta(konto) / "05_kontakty.json"
    kontakty: dict = {}
    if kontakty_path.exists():
        try:
            kontakty = json.loads(kontakty_path.read_text(encoding="utf-8"))
        except Exception:
            kontakty = {}

    watki = _scrapuj_liste_watkow(sesja)
    print(f"[{konto['id']}][wiadomosci] Watkow w API: {len(watki)}")

    nowe, zaktualizowane = 0, 0
    for w in watki:
        pk = str(w.get("pk"))
        subject = w.get("subject") or ""
        autor = w.get("user_to_display") or {}
        uid = str(autor.get("pk") or f"brak_id_{pk}")
        nazwa = autor.get("visible_name") or autor.get("name")
        zrodlo = _klasyfikuj_watek(subject, tytuly_ofert, tytuly_zlecen, w.get("is_offer_inquiry"))

        wiadomosci = _scrapuj_tresc_watku(sesja, pk)
        teraz = datetime.now().isoformat(timespec="seconds")

        if uid not in kontakty:
            kontakty[uid] = {
                "user_id": uid, "author_name": nazwa, "zrodlo": zrodlo,
                "watki": [], "liczba_wiadomosci": 0,
                "pierwszy_kontakt": teraz, "ostatni_kontakt": teraz,
            }
            nowe += 1
        else:
            zaktualizowane += 1
            if kontakty[uid].get("zrodlo") == "bez_kontekstu" and zrodlo != "bez_kontekstu":
                kontakty[uid]["zrodlo"] = zrodlo

        istniejace = {str(t.get("thread_id")) for t in kontakty[uid]["watki"]}
        if pk not in istniejace:
            kontakty[uid]["watki"].append({
                "thread_id": pk, "subject": subject,
                "is_offer_inquiry": w.get("is_offer_inquiry"),
                "last_timestamp": w.get("last_timestamp"),
                "messages": wiadomosci,
            })
        kontakty[uid]["liczba_wiadomosci"] = sum(len(t["messages"]) for t in kontakty[uid]["watki"])
        kontakty[uid]["ostatni_kontakt"] = teraz
        time.sleep(0.3)

    print(f"[{konto['id']}][wiadomosci] Nowych: {nowe} | zaktualizowanych: {zaktualizowane} "
          f"| lacznie kontaktow: {len(kontakty)}")
    if dry_run:
        print(f"[{konto['id']}][wiadomosci] DRY-RUN — nie zapisuje.")
        return
    _atomic_write_json(kontakty_path, kontakty)
    print(f"[{konto['id']}][wiadomosci] Zapisano: {kontakty_path}")


# ----------------------------------------------------------------------------
# PORAZKI -> 02_przegrane/
# ----------------------------------------------------------------------------
def zbierz_porazki(konto: dict, dry_run: bool = False) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    przegrane_path = _katalog_konta(konto) / "02_przegrane" / "przegrane_pelne.json"
    istniejace: list = []
    if przegrane_path.exists():
        try:
            istniejace = json.loads(przegrane_path.read_text(encoding="utf-8"))
        except Exception:
            istniejace = []
    znane_ids = {str(x.get("offer_id")) for x in istniejace if x.get("offer_id")}

    nowe: list = []
    stop = False
    for page in range(1, 40):
        url = (f"{BASE_URL}/pl/dashboard/offers/closed/" if page == 1
               else f"{BASE_URL}/pl/dashboard/offers/closed/?page={page}")
        r = sesja.get(url, timeout=25)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        linki = soup.select('a[href*="/dashboard/offers/"]')
        if not linki:
            break
        for a in linki:
            m = re.search(r"/dashboard/offers/(\d+)/", a.get("href", ""))
            if not m:
                continue
            oid = m.group(1)
            if oid in znane_ids:
                stop = True
                break
            if oid in {x["offer_id"] for x in nowe}:
                continue
            card = a.find_parent(class_=re.compile(r"job|offer|row|item|card|panel|box")) or a.parent
            card_txt = card.get_text(" | ", strip=True) if card else ""
            m_price = re.search(r"Kwota brutto:\s*([\d\s,.]+\s*[A-Z]{3})", card_txt)
            nowe.append({
                "offer_id": oid, "title": a.get_text(" ", strip=True),
                "our_price": m_price.group(1).strip() if m_price else None,
                "zrodlo": "feedback",
                "data_pobrania": datetime.now().isoformat(timespec="seconds"),
            })
        if stop:
            break
        time.sleep(0.4)

    print(f"[{konto['id']}][porazki] Nowych: {len(nowe)} (znane: {len(znane_ids)})")
    if dry_run:
        print(f"[{konto['id']}][porazki] DRY-RUN — nie zapisuje.")
        return
    if nowe:
        _atomic_write_json(przegrane_path, nowe + istniejace)
        print(f"[{konto['id']}][porazki] Zapisano: {przegrane_path}")


# ----------------------------------------------------------------------------
# WRZUCONE -> 04_moje_zlecenia/
# ----------------------------------------------------------------------------
def zbierz_wrzucone(konto: dict, dry_run: bool = False) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    katalog = _katalog_konta(konto) / "04_moje_zlecenia"
    znane: set = set()
    if katalog.exists():
        for p in katalog.glob("*/meta.json"):
            znane.add(p.parent.name)

    zebrane: list = []
    for page in range(1, 20):
        url = f"{BASE_URL}/pl/my-jobs/" if page == 1 else f"{BASE_URL}/pl/my-jobs/?page={page}"
        r = sesja.get(url, timeout=25)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        linki = soup.select('a[href*="/pl/jobs/"]')
        if not linki:
            break
        nowe_na_stronie = 0
        for a in linki:
            href = a.get("href", "")
            m = re.search(r"/pl/jobs/(?:[^/]*,)?(\d+)/", href)
            if not m:
                continue
            jid = m.group(1)
            if jid in znane:
                continue
            nowe_na_stronie += 1
            zebrane.append({
                "job_id": jid, "title": a.get_text(" ", strip=True),
                "url": urljoin(BASE_URL, href), "zrodlo": "feedback_wrzucone",
            })
        if nowe_na_stronie == 0 and page > 1:
            break
        time.sleep(0.4)

    print(f"[{konto['id']}][wrzucone] Nowych moich zlecen: {len(zebrane)}")
    if dry_run:
        print(f"[{konto['id']}][wrzucone] DRY-RUN — nie zapisuje.")
        return
    for z in zebrane:
        _atomic_write_json(katalog / z["job_id"] / "meta.json", z)
    if zebrane:
        print(f"[{konto['id']}][wrzucone] Zapisano {len(zebrane)} do {katalog}")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Zbieranie feedbacku z Useme (per konto).")
    ap.add_argument("--konto", default="all", help="konto1 | konto2 | all")
    ap.add_argument("--wiadomosci", action="store_true", help="Zbierz wiadomosci prywatne")
    ap.add_argument("--porazki", action="store_true", help="Zbierz porazki")
    ap.add_argument("--wrzucone", action="store_true", help="Zapisz moje wystawione zlecenia")
    ap.add_argument("--wszystko", action="store_true", help="Wszystkie powyzsze")
    ap.add_argument("--dry-run", action="store_true", help="Nic nie zapisuj")
    args = ap.parse_args()

    if not (args.wiadomosci or args.porazki or args.wrzucone or args.wszystko):
        ap.error("Podaj akcje: --wiadomosci / --porazki / --wrzucone / --wszystko")

    for konto in _konta_wybrane(args.konto):
        print(f"\n=== KONTO: {konto['id']} ({konto.get('baza_id')}) ===")
        if args.wszystko or args.wiadomosci:
            zbierz_wiadomosci(konto, dry_run=args.dry_run)
        if args.wszystko or args.porazki:
            zbierz_porazki(konto, dry_run=args.dry_run)
        if args.wszystko or args.wrzucone:
            zbierz_wrzucone(konto, dry_run=args.dry_run)


if __name__ == "__main__":
    main()