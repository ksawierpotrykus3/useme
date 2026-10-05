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

from curl_cffi import requests as cffi_requests
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


def zbuduj_sesje(konto: dict) -> cffi_requests.Session:
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

    s = cffi_requests.Session(impersonate="chrome120")
    s.headers.update({
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    for c in dane:
        if "name" in c and "value" in c:
            s.cookies.set(c["name"], c["value"], domain=c.get("domain", "useme.com"))
    return s


def _get_json(sesja, url: str):
    """GET z Accept: application/json. Zwraca (json|None, status, final_url).

    Retry na HTTP 429 (rate limit) i 503 — Useme potrafi przydlawic po serii
    requestow. Backoff: 5s, 15s, 30s.
    """
    for proba, opoznienie in enumerate((0, 5, 15, 30)):
        if opoznienie:
            time.sleep(opoznienie)
        r = sesja.get(url, timeout=25, allow_redirects=True,
                      headers={"Accept": "application/json, text/plain, */*"})
        if r.status_code in (429, 503) and proba < 3:
            continue
        ct = r.headers.get("Content-Type", "")
        if "/users/login" in r.url:
            return None, r.status_code, r.url
        if r.status_code == 200 and "json" in ct:
            try:
                return r.json(), r.status_code, r.url
            except Exception:
                return None, r.status_code, r.url
        return None, r.status_code, r.url
    return None, r.status_code, r.url


def _get_html(sesja, url: str):
    """GET HTML z retry na 429/503. Zwraca requests.Response lub None."""
    for proba, opoznienie in enumerate((0, 5, 15, 30)):
        if opoznienie:
            time.sleep(opoznienie)
        r = sesja.get(url, timeout=25, allow_redirects=True)
        if r.status_code in (429, 503) and proba < 3:
            continue
        return r
    return r


def _sprawdz_sesje(sesja, konto: dict) -> None:
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
def _normalizuj(tekst: str) -> str:
    """Lowercase + usuniecie polskich znakow i wszystkiego poza [a-z0-9].

    Dzieki temu slug 'szybka-synchronizacja-stanow-magazynowych' pasuje do
    pelnego tytulu 'Szybka synchronizacja stanów magazynowych...'.
    """
    import unicodedata
    if not tekst:
        return ""
    t = unicodedata.normalize("NFKD", tekst.lower())
    t = t.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", t)


def _znane_tytuly(katalog: Path) -> dict[str, str]:
    """Zwraca {tytul_znormalizowany: job_id} z danego katalogu.

    Obsluguje zarowno pliki <job_id>.json (01_ofertowarka), jak i
    <job_id>/meta.json (04_moje_zlecenia). Tytul jest normalizowany, zeby
    slug z bazy pasowal do pelnego tytulu watku PV.
    """
    mapa: dict[str, str] = {}
    if not katalog.exists():
        return mapa
    for p in katalog.rglob("*.json"):
        if any(part.startswith(".") for part in p.parts):
            continue
        # Nie traktuj pojedynczych plikow ofert ani watkow jako zlecen
        if "oferty" in p.parts or "wiadomosci" in p.parts:
            continue
        # job_id z nazwy pliku (cyfry) albo z folderu rodzica (cyfry w nazwie)
        jid = p.stem if p.stem.isdigit() else None
        if not jid:
            m = re.search(r"(\d{4,})", p.parent.name)
            jid = m.group(1) if m else None
        if not jid:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        for zrodlo_tytulu in (d.get("title"), d.get("job_id")):
            t = _normalizuj(str(zrodlo_tytulu or ""))
            if t:
                mapa[t] = jid
    return mapa


def _scrapuj_liste_watkow(sesja) -> list[dict]:
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


def _scrapuj_tresc_watku(sesja, pk: str) -> list[dict]:
    """Pobiera tresc wiadomosci watku z API. Zwraca liste {sender,date,text}."""
    data, status, _ = _get_json(sesja, f"{BASE_URL}/pl/mesg/mesgs/{pk}/thread")
    if not data:
        return []
    wiadomosci = []
    for m in data.get("results", []):
        tresc = _html_do_tekstu(m.get("content", ""))
        sender = m.get("sender")
        if not sender and isinstance(m.get("user_to_display"), dict):
            sender = m["user_to_display"].get("name")
        wiadomosci.append({
            "pk": m.get("pk"),
            "sender": sender,
            "date": m.get("sent_on") or m.get("created") or m.get("date"),
            "text": tresc,
        })
    return wiadomosci


def _dopasuj_job_id(subject: str, tytuly_zlecen: dict) -> str | None:
    """Zwraca job_id zlecenia, do ktorego pasuje tytul watku (lub None)."""
    s = _normalizuj(subject or "")
    if not s:
        return None
    for t, jid in tytuly_zlecen.items():
        if t and (t in s or s in t):
            return jid
    return None


def _klasyfikuj_watek(subject: str, tytuly_ofert: dict, tytuly_zlecen: dict,
                      is_offer_inquiry) -> tuple[str, str | None]:
    """Zwraca (zrodlo, job_id): 'offer' / 'job' / 'bez_kontekstu'.

    Porownuje znormalizowane tytuly (bez polskich znakow, spacji, myslnikow),
    zeby slug z bazy pasowal do pelnego tytulu watku. Dla 'job' zwraca job_id.
    """
    s = _normalizuj(subject or "")
    if s:
        for t, jid in tytuly_zlecen.items():
            if t and (t in s or s in t):
                return "job", jid
        for t in tytuly_ofert:
            if t and (t in s or s in t):
                return "offer", None
    return "bez_kontekstu", None


def zbierz_wiadomosci(konto: dict, dry_run: bool = False,
                      filtry: list[str] | None = None) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    konto_dir = _katalog_konta(konto)
    tytuly_ofert = _znane_tytuly(konto_dir / "01_ofertowarka")
    tytuly_zlecen = _znane_tytuly(konto_dir / "04_moje_zlecenia")

    kontakty_path = konto_dir / "05_kontakty.json"
    kontakty: dict = {}
    if kontakty_path.exists():
        try:
            kontakty = json.loads(kontakty_path.read_text(encoding="utf-8"))
        except Exception:
            kontakty = {}

    watki = _scrapuj_liste_watkow(sesja)
    print(f"[{konto['id']}][wiadomosci] Watkow w API: {len(watki)}")

    nowe, zaktualizowane, pominiete = 0, 0, 0
    # {job_id: [wpisy wiadomosci zgrupowane per zlecenie]}
    per_job: dict[str, list] = {}
    for w in watki:
        pk = str(w.get("pk"))
        subject = w.get("subject") or ""
        autor = w.get("user_to_display") or {}
        uid = str(autor.get("pk") or f"brak_id_{pk}")
        nazwa = autor.get("visible_name") or autor.get("name")
        zrodlo, job_id = _klasyfikuj_watek(subject, tytuly_ofert, tytuly_zlecen,
                                           w.get("is_offer_inquiry"))

        if filtry is not None and zrodlo not in filtry:
            pominiete += 1
            continue

        wiadomosci = _scrapuj_tresc_watku(sesja, pk)
        teraz = datetime.now().isoformat(timespec="seconds")

        # --- agregat kontaktow (05_kontakty.json) ---
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

        # --- grupowanie per zlecenie (tylko watki 'job' z dopasowanym job_id) ---
        if zrodlo == "job" and job_id:
            per_job.setdefault(job_id, []).append({
                "thread_id": pk,
                "subject": subject,
                "kontakt": nazwa,
                "user_id": uid,
                "last_timestamp": w.get("last_timestamp"),
                "messages": wiadomosci,
            })

    filtr_info = f" | pominieto (filtr): {pominiete}" if filtry is not None else ""
    print(f"[{konto['id']}][wiadomosci] Nowych: {nowe} | zaktualizowanych: {zaktualizowane}"
          f"{filtr_info} | lacznie kontaktow: {len(kontakty)} | "
          f"zlecen z wiadomosciami: {len(per_job)}")

    if dry_run:
        print(f"[{konto['id']}][wiadomosci] DRY-RUN — nie zapisuje.")
        return

    _atomic_write_json(kontakty_path, kontakty)
    print(f"[{konto['id']}][wiadomosci] Zapisano: {kontakty_path}")

    # zapis wiadomosci per zlecenie: 04_moje_zlecenia/<job_id>/wiadomosci/
    for job_id, watki_job in per_job.items():
        folder = _folder_zlecenia(konto_dir / "04_moje_zlecenia", job_id)
        wiad_dir = folder / "wiadomosci"
        wiad_dir.mkdir(parents=True, exist_ok=True)
        for w in watki_job:
            pk = str(w.get("thread_id") or "")
            if pk:
                _atomic_write_json(wiad_dir / f"watek_{pk}.json", w)

        sciezka = folder / "wiadomosci.json"
        _atomic_write_json(sciezka, {
            "job_id": job_id,
            "data_pobrania": datetime.now().isoformat(timespec="seconds"),
            "liczba_watkow": len(watki_job),
            "liczba_wiadomosci": sum(len(w.get("messages", [])) for w in watki_job),
            "watki_ids": [str(w.get("thread_id")) for w in watki_job if w.get("thread_id")],
            "folder_wiadomosci": "wiadomosci/",
        })
        print(f"  + wiadomosci -> {job_id} ({len(watki_job)} watkow w {folder.name}/wiadomosci/)")


# ----------------------------------------------------------------------------
# PORAZKI -> 02_przegrane/
# ----------------------------------------------------------------------------
def _klienci_odpisali(konto: dict) -> set:
    """Zwraca zbior identyfikatorow klientow, ktorzy ODPISALI (sa w 05_kontakty.json).

    Klucze: user_id (str) oraz znormalizowana nazwa autora (lower, spacje). Dzieki temu
    mozna dopasowac zamknieta oferte zarowno po id, jak i po nazwie zleceniodawcy.
    """
    wynik: set = set()
    kontakty_path = _katalog_konta(konto) / "05_kontakty.json"
    if not kontakty_path.exists():
        return wynik
    try:
        dane = json.loads(kontakty_path.read_text(encoding="utf-8"))
    except Exception:
        return wynik
    if not isinstance(dane, dict):
        return wynik
    for uid, v in dane.items():
        if not isinstance(v, dict):
            continue
        if uid:
            wynik.add(str(uid).strip().lower())
        autor = v.get("author_name")
        if autor:
            wynik.add(str(autor).strip().lower())
    return wynik


def _czy_klient_odpisal(odpisani: set, client: str | None, meta: dict) -> bool:
    """Sprawdza, czy zleceniodawca zamknietej oferty znajduje sie na liscie odpisanych."""
    if not odpisani:
        return False
    for kandydat in (client, meta.get("client")):
        if kandydat and str(kandydat).strip().lower() in odpisani:
            return True
    return False


def _wczytaj_liste(path: Path) -> list:
    if not path.exists():
        return []
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _lista_zamknietych(sesja, znane_ids: set) -> list:
    """Nowe zamkniete oferty z dashboardu (offer_id + title). Bez pobierania detali."""
    wynik: list = []
    widziane: set = set()
    for page in range(1, 40):
        url = (f"{BASE_URL}/pl/dashboard/offers/closed/" if page == 1
               else f"{BASE_URL}/pl/dashboard/offers/closed/?page={page}")
        r = sesja.get(url, timeout=25)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        linki = soup.select('a[href*="/jobs/my-offer/"]')
        if not linki:
            break
        nowe_na_stronie = 0
        for a in linki:
            m = re.search(r"/jobs/my-offer/(\d+)/", a.get("href", ""))
            if not m:
                continue
            oid = m.group(1)
            if oid in znane_ids or oid in widziane:
                continue
            wynik.append({"offer_id": oid, "title": a.get_text(" ", strip=True)})
            widziane.add(oid)
            nowe_na_stronie += 1
        # Lista od najnowszych: brak nowych na stronie = dalsze strony sa juz znane.
        if nowe_na_stronie == 0:
            break
        time.sleep(0.4)
    return wynik


def _wczytaj_ofertowarke(konto: dict) -> dict:
    """Mapa 01_ofertowarka: tytul(lower) i #closed_offer_id -> (sciezka, rekord)."""
    mapa: dict = {}
    ofertowarka = _katalog_konta(konto) / "01_ofertowarka"
    if not ofertowarka.exists():
        return mapa
    for jf in ofertowarka.rglob("*.json"):
        if not jf.stem.isdigit() or any(p.startswith(".") for p in jf.parts):
            continue
        try:
            d = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue
        t = (d.get("title") or "").strip().lower()
        if t:
            mapa[t] = (jf, d)
        coid = d.get("closed_offer_id")
        if coid:
            mapa[f"#{coid}"] = (jf, d)
    return mapa


def _dopasuj_01(mapa: dict, z: dict):
    """Dopasowuje zamknieta oferte do rekordu 01 po closed_offer_id lub tytule."""
    hit = mapa.get(f"#{z['offer_id']}")
    if hit:
        return hit
    return mapa.get((z.get("title") or "").strip().lower(), (None, None))


def _rekord_porazki(rec01: dict, offer_id: str) -> dict:
    """Buduje rekord 02/03 z danych 01_ofertowarka (bez scrapowania Useme)."""
    sub = rec01.get("submission_result") or {}
    ai = rec01.get("ai_proposal") or {}
    wycena = sub.get("wycena")
    return {
        "offer_id": str(offer_id),
        "title": rec01.get("title"),
        "our_price": (f"{wycena:.2f}".replace(".", ",") + " PLN") if isinstance(wycena, (int, float)) else None,
        "zrodlo": "feedback",
        "data_pobrania": datetime.now().isoformat(timespec="seconds"),
        "job_url": f"{BASE_URL}/pl/jobs/my-offer/{offer_id}/",
        "client": rec01.get("author"),
        "budget": rec01.get("budget"),
        "job_description": (rec01.get("full_details") or {}).get("full_description", ""),
        "our_proposal": ai.get("opis", ""),
        "our_days": sub.get("dni"),
    }


def _usun_z_01(mapa: dict, z: dict, dry_run: bool) -> bool:
    """Usuwa z 01_ofertowarka rekord przeniesiony do 02/03 (01 trzyma tylko wiszace)."""
    jf, _ = _dopasuj_01(mapa, z)
    if not jf:
        return False
    if dry_run:
        print(f"    [DRY-RUN] usun z 01: {jf.name}")
        return True
    try:
        jf.unlink()
        mapa.pop((z.get("title") or "").strip().lower(), None)
        mapa.pop(f"#{z['offer_id']}", None)
        return True
    except Exception:
        return False


def _zebrane_offer_ids(konto: dict) -> set:
    """Wszystkie identyfikatory (offer_id + job_id) z archiwum 02_przegrane i 03_odpisane.

    Dedup musi widziec WSZYSTKIE pliki archiwum (wygrane_56.json, wygrane.json,
    przegrane_pelne_416.json, przegrane_pelne.json, odpisane_zamkniete.json itd.),
    a nie tylko te, do ktorych pisze feedback. Inaczej przenosi oferte drugi raz.
    """
    ids: set = set()
    for pod in ("02_przegrane", "03_odpisane"):
        d = _katalog_konta(konto) / pod
        if not d.exists():
            continue
        for p in d.glob("*.json"):
            if p.name == "blocklist.json":
                continue
            try:
                dane = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            rekordy = dane if isinstance(dane, list) else [dane]
            for r in rekordy:
                if not isinstance(r, dict):
                    continue
                for k in ("offer_id", "job_id"):
                    if r.get(k):
                        ids.add(str(r[k]))
    return ids


def _rekord_odpisany(rec01: dict) -> dict:
    """Buduje rekord 03_odpisane z danych 01_ofertowarka (przeniesienie z powodu odpowiedzi)."""
    sub = rec01.get("submission_result") or {}
    ai = rec01.get("ai_proposal") or {}
    wycena = sub.get("wycena") or ai.get("wycena")
    return {
        "offer_id": rec01.get("closed_offer_id"),
        "job_id": str(rec01.get("id")),
        "title": rec01.get("title"),
        "our_price": (f"{wycena:.2f}".replace(".", ",") + " PLN") if isinstance(wycena, (int, float)) else None,
        "our_days": str(sub.get("dni") or ai.get("dni") or ""),
        "zrodlo": "feedback_odpisane",
        "data_pobrania": datetime.now().isoformat(timespec="seconds"),
        "job_url": rec01.get("url"),
        "client": rec01.get("author"),
        "budget": rec01.get("budget"),
        "job_description": (rec01.get("full_details") or {}).get("full_description", ""),
        "our_proposal": ai.get("opis", ""),
        "status_koncowy": "ODPISANE_ZAMKNIETE",
        "odpisal": True,
    }


def _przenies_odpisane_z_01(konto: dict, dry_run: bool = False) -> int:
    """Przenosi z 01_ofertowarka oferty, na ktore klient ODPISAL (sa w 05_kontakty).

    Regula: rekord w 01, ktorego tytul pasuje do watku PV (klient odpisal) ->
    03_odpisane. ZAWSZE przenoszenie (unlink z 01), nie kopiowanie.
    Dopasowanie po znormalizowanym tytule (substring), tak jak klasyfikacja watkow.
    """
    ow_dir = _katalog_konta(konto) / "01_ofertowarka"
    if not ow_dir.exists():
        return 0

    kontakty_path = _katalog_konta(konto) / "05_kontakty.json"
    if not kontakty_path.exists():
        return 0
    try:
        kontakty = json.loads(kontakty_path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(kontakty, dict):
        return 0

    # Tylko dopasowanie po TYTULE watku do tytulu zlecenia.
    # NIE dopasowujemy po samym autorze - klient moze miec wiele zlecen i odpisac
    # tylko na jedno, wiec autor bez zgodnosci tytulu daje falszywe trafienia.
    subjecty: list[str] = []
    for v in kontakty.values():
        if not isinstance(v, dict):
            continue
        for w in (v.get("watki") or []):
            s = _normalizuj(w.get("subject") or "")
            if s:
                subjecty.append(s)

    if not subjecty:
        return 0

    odp_path = _katalog_konta(konto) / "03_odpisane" / "odpisane_zamkniete.json"
    istniejace_odp = _wczytaj_liste(odp_path)
    znane = _zebrane_offer_ids(konto)

    do_przeniesienia: list[tuple[Path, dict]] = []
    for p in ow_dir.rglob("*.json"):
        if not p.stem.isdigit():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        tytul = _normalizuj(d.get("title") or "")
        if not tytul:
            continue
        if any(subj and (subj in tytul or tytul in subj) for subj in subjecty):
            do_przeniesienia.append((p, d))

    if not do_przeniesienia:
        return 0

    print(f"[{konto['id']}][odpisane] Ofert w 01 z odpowiedzia klienta: {len(do_przeniesienia)}")
    if dry_run:
        for p, d in do_przeniesienia:
            print(f"  [DRY-RUN] {d.get('id')} -> 03_odpisane | {d.get('title')}")
        return len(do_przeniesienia)

    nowe_rekordy = []
    for p, d in do_przeniesienia:
        jid = str(d.get("id"))
        if jid not in znane:
            nowe_rekordy.append(_rekord_odpisany(d))
        try:
            p.unlink()
        except Exception:
            pass

    if nowe_rekordy:
        _atomic_write_json(odp_path, nowe_rekordy + istniejace_odp)
    print(f"[{konto['id']}][odpisane] Przeniesiono do 03_odpisane: +{len(nowe_rekordy)} "
          f"(usunieto z 01: {len(do_przeniesienia)})")
    return len(do_przeniesienia)


def zbierz_porazki(konto: dict, dry_run: bool = False) -> None:
    """Przenosi zamkniete oferty z 01_ofertowarka do 02_przegrane / 03_odpisane.

    Model konto1 (wykonawca): oferty ktore zlozylismy. Gdy zlecenie zostaje
    zamkniete:
      - klient ODPISAL (jest w 05_kontakty.json) -> 03_odpisane (wygrane/odpisane),
      - klient NIE odpisal                       -> 02_przegrane.
    ZAWSZE przenoszenie (unlink z 01), nie kopiowanie. 01 trzyma tylko wiszace.
    """
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    przegrane_path = _katalog_konta(konto) / "02_przegrane" / "przegrane_pelne.json"
    odp_path = _katalog_konta(konto) / "03_odpisane" / "odpisane_zamkniete.json"
    istniejace = _wczytaj_liste(przegrane_path)
    istniejace_odp = _wczytaj_liste(odp_path)
    # Dedup po CALYM archiwum (wszystkie pliki w 02/03), nie tylko po 2 docelowych.
    znane_ids = _zebrane_offer_ids(konto)

    zamkniete = _lista_zamknietych(sesja, znane_ids)
    print(f"[{konto['id']}][porazki] Zamknietych nowych na Useme: {len(zamkniete)} (znane: {len(znane_ids)})")

    if not zamkniete:
        return

    mapa01 = _wczytaj_ofertowarke(konto)
    odpisani = _klienci_odpisali(konto)
    do_przegranych: list = []
    do_odpisanych: list = []
    pominiete = 0
    for z in zamkniete:
        _, rec01 = _dopasuj_01(mapa01, z)
        if not rec01:
            pominiete += 1
            continue
        rec = _rekord_porazki(rec01, z["offer_id"])
        if _czy_klient_odpisal(odpisani, rec.get("client"), rec):
            rec["status_koncowy"] = "ODPISANE_ZAMKNIETE"
            rec["odpisal"] = True
            rec["zrodlo"] = "feedback_odpisane"
            do_odpisanych.append((z, rec))
        else:
            do_przegranych.append((z, rec))

    if dry_run:
        for z, rec in do_przegranych + do_odpisanych:
            cel = "02_przegrane" if (z, rec) in do_przegranych else "03_odpisane"
            print(f"  [DRY-RUN] #{z['offer_id']} -> {cel} | {rec.get('title')}")
        print(f"[{konto['id']}][porazki] DRY-RUN — nic nie zapisuje.")
        return

    if do_przegranych:
        _atomic_write_json(przegrane_path, [r for _, r in do_przegranych] + istniejace)
        print(f"[{konto['id']}][porazki] -> 02_przegrane: +{len(do_przegranych)}")
    if do_odpisanych:
        znane_odp = {str(x.get("offer_id")) for x in istniejace_odp if x.get("offer_id")}
        nowe_odp = [r for _, r in do_odpisanych if str(r.get("offer_id")) not in znane_odp]
        if nowe_odp:
            _atomic_write_json(odp_path, nowe_odp + istniejace_odp)
        print(f"[{konto['id']}][porazki] -> 03_odpisane: +{len(nowe_odp)}")

    # 01_ofertowarka trzyma tylko oferty ktore jeszcze wisza - usun przeniesione.
    usuniete = 0
    for z, _ in do_przegranych + do_odpisanych:
        if _usun_z_01(mapa01, z, dry_run=False):
            usuniete += 1
    print(f"[{konto['id']}][porazki] Usunieto z 01_ofertowarka: {usuniete} "
          f"(pominiete bez rekordu 01: {pominiete})")


# ----------------------------------------------------------------------------
# WRZUCONE -> 04_moje_zlecenia/  (lista z dashboardu: /pl/dashboard/my-jobs/?status=all)
# ----------------------------------------------------------------------------
def _moje_zlecenia_z_listy(sesja) -> list[dict]:
    """Zwraca liste moich zlecen (zleceniodawca) z dashboardu.

    Kanoniczne zrodlo: /pl/dashboard/my-jobs/?status=all  (WSZYSTKIE statusy:
    otwarte, zamkniete, wersje robocze). Zwraca [{job_id,title,url,status}].
    """
    url = f"{BASE_URL}/pl/dashboard/my-jobs/?status=all"
    r = _get_html(sesja, url)
    if not r or r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")

    wyniki: dict[str, dict] = {}
    # linki publiczne: /pl/jobs/{slug},{id}/  -> tytul ze sluga
    for a in soup.select('a[href*="/pl/jobs/"]'):
        href = a.get("href", "")
        m = re.search(r"/pl/jobs/(?:[^/,]+),(\d+)/?$", href)
        if not m:
            continue
        jid = m.group(1)
        # tytul z tekstu linku jesli sensowny (nie "Zobacz na Useme Jobs")
        tekst = a.get_text(" ", strip=True)
        if jid not in wyniki:
            wyniki[jid] = {"job_id": jid, "title": None,
                           "url": f"{BASE_URL}/pl/jobs/{jid}/offers/",
                           "public_url": urljoin(BASE_URL, href),
                           "status": None}

    # linki do ofert: /pl/jobs/{id}/offers/ -> gwarantuje obecnosc zlecenia
    for a in soup.select('a[href*="/offers/"]'):
        m = re.search(r"/pl/jobs/(\d+)/offers/", a.get("href", ""))
        if not m:
            continue
        jid = m.group(1)
        wyniki.setdefault(jid, {
            "job_id": jid, "title": None,
            "url": f"{BASE_URL}/pl/jobs/{jid}/offers/",
            "public_url": None, "status": None,
        })

    # tytuly z kart dashboardu (naglowki zlecen w .dashboard-list__item)
    for karta in soup.select(".dashboard-list__item"):
        html = str(karta)
        m = re.search(r"/pl/jobs/(\d+)/offers/", html)
        if not m:
            continue
        jid = m.group(1)
        if jid not in wyniki:
            continue
        # naglowek: pierwszy <a> z publicznym linkiem do zlecenia
        pub = karta.select_one('a[href*="/pl/jobs/"]')
        tytul = None
        for a in karta.select("a[href]"):
            h = a.get("href", "")
            if re.search(r"/pl/jobs/(?:[^/,]+),(\d+)/?$", h):
                t = a.get_text(" ", strip=True)
                if t and "Zobacz na Useme" not in t:
                    tytul = t
                    break
        if tytul:
            wyniki[jid]["title"] = tytul
        # status
        for span in karta.select("span, div"):
            s = span.get_text(" ", strip=True)
            if s in ("Otwarte", "Zamknięte", "Wersja robocza", "Weryfikacja"):
                wyniki[jid]["status"] = s
                break

    # slug jako fallback tytulu
    for jid, d in wyniki.items():
        if not d["title"] and d.get("public_url"):
            m = re.search(r"/pl/jobs/([^/]+),\d+/?$", d["public_url"])
            if m:
                d["title"] = m.group(1).replace("-", " ")
    return list(wyniki.values())


def _parsuj_karty_ofert(soup) -> list[dict]:
    """Wyciaga oferty z kart .dashboard-list__item-offer z danego drzewa HTML."""
    oferty: list[dict] = []
    for karta in soup.select(".dashboard-list__item-offer"):
        oid = None
        inp = karta.select_one("input[data-select-offer-id]")
        if inp:
            oid = inp.get("data-select-offer-id")
        if not oid:
            fav = karta.select_one("offer-toggle-favorite[data-offer-pk]")
            if fav:
                oid = fav.get("data-offer-pk")
        if not oid:
            d = karta.select_one('div[id^="offer_"][id$="_description"]')
            if d:
                m = re.search(r"offer_(\d+)_description", d.get("id", ""))
                if m:
                    oid = m.group(1)
        if not oid:
            continue

        autor_el = karta.select_one(".dashboard-list__item-user-name")
        profil = karta.select_one('a[href*="/pl/roles/contractor/"]')
        desc_el = karta.select_one(f"#offer_{oid}_description")

        price = days = umowy = None
        for prop in karta.select(".dashboard-list__item-stats-prop"):
            t = prop.get_text(" ", strip=True)
            if "PLN" in t or re.search(r"\d[\d\s.,]*\s*zł", t):
                price = t
            elif "dni pracy" in t or "dzień pracy" in t:
                days = t
        exp = karta.select_one(".experience")
        if exp:
            umowy = exp.get_text(" ", strip=True)

        oferty.append({
            "offer_id": str(oid),
            "author_name": autor_el.get_text(strip=True) if autor_el else None,
            "author_url": urljoin(BASE_URL, profil.get("href")) if profil and profil.get("href") else None,
            "umowy": umowy,
            "price": price,
            "days": days,
            "proposal_text": desc_el.get_text("\n", strip=True) if desc_el else "",
        })
    return oferty


def _scrapuj_oferty_zlecenia(sesja, job_id: str, max_stron: int = 25) -> list[dict]:
    """Pobiera WSZYSTKIE oferty konkurencji z /pl/jobs/{id}/offers/ (paginacja).

    Struktura kart: .dashboard-list__item-offer
      - offer_id: input[data-select-offer-id] / offer-toggle-favorite[data-offer-pk]
      - autor:    .dashboard-list__item-user-name
      - profil:   a[href*='/pl/roles/contractor/']
      - opis:     div#offer_{id}_description
      - cena:     .dashboard-list__item-stats-prop (zawiera 'PLN')
      - dni:      .dashboard-list__item-stats-prop (zawiera 'dni pracy')

    Kolejne strony: /pl/jobs/{id}/offers/?page=N (10 ofert na strone).
    """
    oferty: list[dict] = []
    widziane: set = set()
    for page in range(1, max_stron + 1):
        url = (f"{BASE_URL}/pl/jobs/{job_id}/offers/" if page == 1
               else f"{BASE_URL}/pl/jobs/{job_id}/offers/?page={page}")
        r = _get_html(sesja, url)
        if not r or r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        nowe = 0
        for o in _parsuj_karty_ofert(soup):
            if o["offer_id"] in widziane:
                continue
            widziane.add(o["offer_id"])
            oferty.append(o)
            nowe += 1
        # brak nowych ofert na stronie = koniec paginacji
        if nowe == 0:
            break
        time.sleep(0.6)
    return oferty


def _scrapuj_moje_zlecenie(sesja, jid: str, meta: dict) -> dict:
    """Buduje rekord mojego zlecenia: dane z listy + opis zlecenia."""
    url = meta.get("url") or f"{BASE_URL}/pl/jobs/{jid}/offers/"
    rekord = {
        "job_id": str(jid),
        "title": meta.get("title"),
        "url": url,
        "public_url": meta.get("public_url"),
        "status": meta.get("status"),
        "zrodlo": "feedback_wrzucone",
        "opis": "",
        "data_pobrania": datetime.now().isoformat(timespec="seconds"),
    }
    if meta.get("public_url"):
        r = _get_html(sesja, meta["public_url"])
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            if not rekord["title"]:
                h = soup.select_one("h1")
                if h:
                    rekord["title"] = h.get_text(" ", strip=True)
            desc = (soup.select_one(".jobs-summary__item-text")
                    or soup.select_one(".job-details__main-desc-body")
                    or soup.select_one(".job-description")
                    or soup.select_one(".job-details__desc"))
            if desc:
                rekord["opis"] = desc.get_text("\n", strip=True)
    return rekord


def _folder_zlecenia(katalog: Path, jid: str) -> Path:
    """Zwraca istniejacy folder zlecenia (sam ID lub z prefiksem), albo nowy <jid>."""
    if (katalog / jid).exists():
        return katalog / jid
    for p in katalog.iterdir():
        if p.is_dir() and re.search(rf"(?<!\d){re.escape(jid)}(?!\d)", p.name):
            return p
    return katalog / jid


def zbierz_wrzucone(konto: dict, dry_run: bool = False) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    katalog = _katalog_konta(konto) / "04_moje_zlecenia"
    katalog.mkdir(parents=True, exist_ok=True)

    wszystkie = _moje_zlecenia_z_listy(sesja)
    # zlecenia do zaktualizowania: nowe (brak folderu) LUB istniejace bez ofert
    do_pobrania: list[dict] = []
    for z in wszystkie:
        folder = _folder_zlecenia(katalog, z["job_id"])
        ma_oferty = (folder / "oferty").is_dir() and any((folder / "oferty").glob("*.json"))
        if not ma_oferty and not (folder / "oferty.json").exists():
            do_pobrania.append(z)
    print(f"[{konto['id']}][wrzucone] Zlecen na liscie: {len(wszystkie)} | "
          f"do pobrania/uzupelnienia: {len(do_pobrania)}")

    if dry_run:
        for z in do_pobrania:
            print(f"  [DRY-RUN] {z['job_id']} | {z.get('title')} | status={z.get('status')}")
        print(f"[{konto['id']}][wrzucone] DRY-RUN — nie zapisuje.")
        return

    for z in do_pobrania:
        jid = z["job_id"]
        folder = _folder_zlecenia(katalog, jid)
        folder.mkdir(parents=True, exist_ok=True)
        # 1) zlecenie.json (dane + opis)
        zlecenie = _scrapuj_moje_zlecenie(sesja, jid, z)
        _atomic_write_json(folder / "zlecenie.json", zlecenie)
        # 2) oferty per plik w podfolderze oferty/ (kazda oferta to lekki plik 1-3 KB)
        oferty = _scrapuj_oferty_zlecenia(sesja, jid)
        oferty_dir = folder / "oferty"
        oferty_dir.mkdir(parents=True, exist_ok=True)
        for o in oferty:
            oid = str(o.get("offer_id") or "")
            if not oid:
                continue
            o_copy = dict(o)
            o_copy["job_id"] = jid
            _atomic_write_json(oferty_dir / f"{oid}.json", o_copy)

        # Meta indeks ofert (kompatybilnosc i szybki podglad bez otwierania 100 plikow)
        _atomic_write_json(folder / "oferty.json", {
            "job_id": jid,
            "title": zlecenie.get("title"),
            "data_pobrania": datetime.now().isoformat(timespec="seconds"),
            "liczba_ofert": len(oferty),
            "oferty_ids": [str(o.get("offer_id")) for o in oferty if o.get("offer_id")],
            "folder_ofert": "oferty/",
        })
        print(f"  + {jid} | {zlecenie.get('title')} | ofert: {len(oferty)} | folder: {folder.name}/oferty/")
        time.sleep(1.0)
    if do_pobrania:
        print(f"[{konto['id']}][wrzucone] Zapisano {len(do_pobrania)} zlecen do {katalog}")


def wczytaj_oferty_zlecenia(folder: Path) -> list[dict]:
    """Wczytuje oferty danego zlecenia: z folderu oferty/ (kazda oferta to plik) lub legacy oferty.json."""
    oferty_dir = folder / "oferty"
    if oferty_dir.is_dir():
        wynik = []
        for p in sorted(oferty_dir.glob("*.json")):
            try:
                wynik.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        if wynik:
            return wynik
    of_path = folder / "oferty.json"
    if of_path.exists():
        try:
            d = json.loads(of_path.read_text(encoding="utf-8"))
            if isinstance(d, dict) and "oferty" in d:
                return d["oferty"]
            if isinstance(d, list):
                return d
        except Exception:
            pass
    return []


def wczytaj_wiadomosci_zlecenia(folder: Path) -> list[dict]:
    """Wczytuje watki wiadomosci danego zlecenia: z folderu wiadomosci/ lub legacy wiadomosci.json."""
    wiad_dir = folder / "wiadomosci"
    if wiad_dir.is_dir():
        wynik = []
        for p in sorted(wiad_dir.glob("*.json")):
            try:
                wynik.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        if wynik:
            return wynik
    w_path = folder / "wiadomosci.json"
    if w_path.exists():
        try:
            d = json.loads(w_path.read_text(encoding="utf-8"))
            if isinstance(d, dict) and "watki" in d:
                return d["watki"]
            if isinstance(d, list):
                return d
        except Exception:
            pass
    return []


# ----------------------------------------------------------------------------
# POWIADOMIENIA -> 06_powiadomienia.json
# ----------------------------------------------------------------------------
def _scrapuj_powiadomienia(sesja, max_stron: int = 30) -> list[dict]:
    """Pobiera powiadomienia z /pl/notifications/nots/all/ (paginacja)."""
    wynik: list[dict] = []
    widziane: set = set()
    for page in range(1, max_stron + 1):
        url = (f"{BASE_URL}/pl/notifications/nots/all/" if page == 1
               else f"{BASE_URL}/pl/notifications/nots/all/?page={page}")
        r = _get_html(sesja, url)
        if not r or r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".notifys__item")
        if not items:
            break
        nowe_na_stronie = 0
        for it in items:
            txt_el = it.select_one(".notifys__notify-text")
            dat_el = it.select_one(".notifys__notify-date")
            a = it.select_one("a[href]")
            tekst = txt_el.get_text(" ", strip=True) if txt_el else ""
            link = a.get("href") if a else None
            data_txt = dat_el.get_text(" ", strip=True) if dat_el else ""
            klucz = f"{tekst}|{data_txt}|{link}"
            if klucz in widziane:
                continue
            widziane.add(klucz)
            nowe_na_stronie += 1
            wynik.append({
                "text": tekst,
                "date": dat_el.get_text(" ", strip=True) if dat_el else None,
                "link": urljoin(BASE_URL, link) if link else None,
            })
        if nowe_na_stronie == 0:
            break
        time.sleep(0.5)
    return wynik


def zbierz_powiadomienia(konto: dict, dry_run: bool = False) -> None:
    sesja = zbuduj_sesje(konto)
    _sprawdz_sesje(sesja, konto)

    powiadomienia = _scrapuj_powiadomienia(sesja)
    print(f"[{konto['id']}][powiadomienia] Zebrano: {len(powiadomienia)}")

    sciezka = _katalog_konta(konto) / "06_powiadomienia.json"
    if dry_run:
        print(f"[{konto['id']}][powiadomienia] DRY-RUN — nie zapisuje.")
        return
    _atomic_write_json(sciezka, {
        "konto": konto["id"],
        "data_pobrania": datetime.now().isoformat(timespec="seconds"),
        "liczba": len(powiadomienia),
        "powiadomienia": powiadomienia,
    })
    print(f"[{konto['id']}][powiadomienia] Zapisano: {sciezka}")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Zbieranie feedbacku z Useme (per konto).")
    ap.add_argument("--konto", default="all", help="konto1 | konto2 | all")
    ap.add_argument("--wiadomosci", action="store_true", help="Zbierz wiadomosci prywatne")
    ap.add_argument("--z-ofert", action="store_true", help="(pod-flaga) tylko wiadomosci od ofert")
    ap.add_argument("--ze-zlecen", action="store_true", help="(pod-flaga) tylko wiadomosci dot. moich zlecen")
    ap.add_argument("--porazki", action="store_true", help="Zbierz porazki")
    ap.add_argument("--odpisane", action="store_true",
                    help="Przenies z 01 do 03_odpisane oferty, na ktore klient odpisal")
    ap.add_argument("--wrzucone", action="store_true", help="Zapisz moje wystawione zlecenia")
    ap.add_argument("--powiadomienia", action="store_true", help="Zbierz powiadomienia (panel powiadomien)")
    ap.add_argument("--wszystko", action="store_true", help="Wszystkie powyzsze")
    ap.add_argument("--dry-run", action="store_true", help="Nic nie zapisuj")
    args = ap.parse_args()

    # --z-ofert / --ze-zlecen sa pod-flagami wiadomosci
    if args.z_ofert or args.ze_zlecen:
        args.wiadomosci = True

    if not (args.wiadomosci or args.porazki or args.odpisane or args.wrzucone
            or args.powiadomienia or args.wszystko):
        ap.error("Podaj akcje: --wiadomosci / --porazki / --odpisane / --wrzucone / "
                 "--powiadomienia / --wszystko")

    filtry = None
    if args.z_ofert or args.ze_zlecen:
        filtry = []
        if args.z_ofert:
            filtry.append("offer")
        if args.ze_zlecen:
            filtry.append("job")

    for konto in _konta_wybrane(args.konto):
        print(f"\n=== KONTO: {konto['id']} ({konto.get('baza_id')}) ===")
        # Kolejnosc ma znaczenie:
        # 1) wiadomosci -> aktualizuje 05_kontakty (kto odpisal)
        # 2) odpisane  -> przenosi z 01 oferty z odpowiedzia klienta do 03_odpisane
        # 3) porazki   -> przenosi zamkniete oferty z 01 do 02_przegrane / 03_odpisane
        if args.wszystko or args.wrzucone:
            zbierz_wrzucone(konto, dry_run=args.dry_run)
        if args.wszystko or args.powiadomienia:
            zbierz_powiadomienia(konto, dry_run=args.dry_run)
        if args.wszystko or args.wiadomosci:
            zbierz_wiadomosci(konto, dry_run=args.dry_run, filtry=filtry)
        if args.wszystko or args.odpisane:
            _przenies_odpisane_z_01(konto, dry_run=args.dry_run)
        if args.wszystko or args.porazki:
            zbierz_porazki(konto, dry_run=args.dry_run)


if __name__ == "__main__":
    main()