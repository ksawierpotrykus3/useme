# -*- coding: utf-8 -*-
"""Weryfikator końcowej liczby konkurentów po 48h (Audytor Dynamiki Rynku).

Program przeszukuje zlecenia z magazynu (useme_core/magazyn/):
1. Wybiera zlecenia starsze niż 48h (od momentu wysłania / wykrycia).
2. Sprawdza, czy nie pobrano jeszcze końcowej liczby konkurentów (lub tryb --force).
3. Odpytuje Useme przez curl_cffi i wyciąga końcową liczbę złożonych ofert (nagłówek 'Wysłane oferty (N)').
4. Zapisuje wynik bezpośrednio do pliku JSON w magazynie:
   - 'koncowa_liczba_konkurentow': int
   - 'sprawdzono_konkurencje_at': ISO date
   - 'wiek_przy_sprawdzeniu_h': float
5. Jeśli zlecenie istnieje w katalogu Markdown (badania/rynek/katalog_ofert/),
   dopisuje/aktualizuje linijkę w tabeli:
   '| **Końcowa liczba konkurentów** | N ofert (sprawdzono po Xh) |'
6. Wyświetla czytelne podsumowanie i wnioski o dynamice konkurencji.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from curl_cffi import requests

import config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
MAGAZYN_DIR = config.MAGAZYN_DIR
KATALOG_DIR = BASE_DIR.parent / "badania" / "rynek" / "katalog_ofert"

def atomic_save_json(path: Path, data: dict):
    temp_path = path.with_suffix(f".tmp_{os.getpid()}_{time.time_ns()}")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp_path.replace(path)

def parse_iso_datetime(dt_str: Optional[str]) -> Optional[datetime.datetime]:
    if not dt_str:
        return None
    try:
        # Usuń ułamki sekund jeśli są niestandardowe
        cleaned = re.sub(r'(\.\d+)?(\+.*)?$', '', dt_str.replace("Z", ""))
        return datetime.datetime.fromisoformat(cleaned)
    except Exception:
        return None

def extract_competitors_count(html: str) -> Optional[int]:
    """Wyciąga liczbę złożonych ofert ze strony zlecenia Useme."""
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Główny nagłówek listy ofert: <h2 class="jobs__page-title ...">Wysłane oferty (60)</h2>
    for h in soup.find_all(["h1", "h2", "h3", "h4", "div", "span"]):
        txt = h.get_text(" ", strip=True)
        m = re.search(r'Wys[łl]ane oferty\s*\((\d+)\)', txt, re.I)
        if m:
            return int(m.group(1))
            
    # 2. Alternatywny wzorzec z podsumowania lub tagów
    for s in soup.find_all(string=re.compile(r'\b\d+\s+ofert\b', re.I)):
        m = re.search(r'(\d+)\s+ofert', s, re.I)
        if m:
            return int(m.group(1))
            
    return None

def update_markdown_catalog_file(job_id: str, count: int, hours: float):
    """Aktualizuje lub wstawia wiersz w tabeli pliku Markdown w katalogu ofert."""
    if not KATALOG_DIR.exists():
        return
        
    for md_file in KATALOG_DIR.glob("**/*.md"):
        if md_file.name == "INDEKS_OFERT.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            # Sprawdź czy ten plik odpowiada danemu job_id
            if f"`{job_id}`" in content or f"/{job_id}/" in content or md_file.name.startswith(f"{job_id}_"):
                new_line = f"| **Końcowa liczba konkurentów** | **{count} ofert** (sprawdzono po {hours:.1f}h) |\n"
                
                if "| **Końcowa liczba konkurentów** |" in content:
                    # Zastąp istniejący wiersz
                    content = re.sub(r'\| \*\*Końcowa liczba konkurentów\*\* \|.*?\n', new_line, content)
                elif "| **Nasza Wycena** |" in content:
                    # Wstaw tuż pod naszą wyceną
                    content = content.replace("| **Nasza Wycena** |", f"{new_line}| **Nasza Wycena** |")
                elif "| :--- |" in content:
                    content = re.sub(r'(\| :--- \|\n)', r'\1' + new_line, content, count=1)
                else:
                    continue
                    
                md_file.write_text(content, encoding="utf-8")
                return
        except Exception:
            pass

def fetch_job_html(url: str) -> Optional[str]:
    try:
        r = requests.get(url, impersonate="chrome120", timeout=15)
        if r.status_code == 200:
            return r.text
        if r.status_code == 404:
            return None
    except Exception as e:
        pass
    return None

def run_auditor(min_hours: float = 48.0, force: bool = False, limit: int = 50, dry_run: bool = False):
    now = datetime.datetime.now()
    print("=" * 80)
    print(f" AUDYTOR KONKURENCJI PO 48H — USEME CORE")
    print(f" Czas bieżący: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Próg wieku: >= {min_hours:.1f} godzin | Tryb force: {force} | Limit: {limit}")
    print("=" * 80)

    if not MAGAZYN_DIR.exists():
        print(f"[ERR] Brak folderu {MAGAZYN_DIR}")
        return

    # 1. Przeszukaj magazyn
    json_files = list(MAGAZYN_DIR.glob("*/*.json"))
    candidates = []

    for jf in json_files:
        if ".checkpoints" in str(jf):
            continue
        try:
            with open(jf, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue

        jid = str(d.get("id", "")).strip()
        if not jid:
            continue

        url = d.get("url") or (d.get("list_details") or {}).get("url")
        if not url:
            continue

        # Data bazowa (wysłania lub wykrycia)
        raw_date = d.get("data_wyslania") or d.get("detected_at") or (d.get("full_details") or {}).get("scraped_at")
        job_dt = parse_iso_datetime(raw_date)
        if not job_dt:
            continue

        hours_passed = (now - job_dt).total_seconds() / 3600.0

        if hours_passed < min_hours:
            continue

        # Czy już sprawdzono?
        already_checked = "koncowa_liczba_konkurentow" in d
        if already_checked and not force:
            continue

        status = d.get("status", "")
        # Interesują nas głównie wysłane oferty lub zbadane w magazynie
        candidates.append({
            "file": jf,
            "data": d,
            "id": jid,
            "url": url,
            "title": d.get("title", "Bez tytułu"),
            "status": status,
            "job_dt": job_dt,
            "hours_passed": hours_passed,
            "initial_offers": d.get("list_details", {}).get("offers_count") or 0
        })

    # Sortuj od najstarszych do najświeższych
    candidates.sort(key=lambda x: x["hours_passed"], reverse=True)
    print(f"\nZnaleziono {len(candidates)} zleceń kwalifikujących się do audytu (> {min_hours}h).")

    if not candidates:
        print("[INFO] Brak zleceń wymagających sprawdzenia. Wszystko jest aktualne!")
        return

    results = []
    to_process = candidates[:limit]

    print(f"Przetwarzam pierwsze {len(to_process)} zleceń:\n")

    for i, c in enumerate(to_process, 1):
        print(f"[{i}/{len(to_process)}] #{c['id']} ({c['hours_passed']:.1f}h temu) — {c['title'][:45]}...", end=" ", flush=True)

        if dry_run:
            print("[DRY-RUN - pomijam pobieranie]")
            continue

        html = fetch_job_html(c["url"])
        if not html:
            print("[BŁĄD POBIERANIA / 404]")
            time.sleep(0.3)
            continue

        count = extract_competitors_count(html)
        if count is None:
            print("[BRAK DANYCH O OFERTACH]")
            time.sleep(0.3)
            continue

        print(f"-> KOŃCOWO OFERT: {count} (Początkowo: {c['initial_offers']})")

        # Zaktualizuj JSON
        d = c["data"]
        d["koncowa_liczba_konkurentow"] = count
        d["sprawdzono_konkurencje_at"] = now.isoformat()
        d["wiek_przy_sprawdzeniu_h"] = round(c["hours_passed"], 1)

        atomic_save_json(c["file"], d)

        # Zaktualizuj plik Markdown jeśli istnieje
        update_markdown_catalog_file(c["id"], count, c["hours_passed"])

        results.append({
            "id": c["id"],
            "title": c["title"],
            "status": c["status"],
            "hours": c["hours_passed"],
            "initial": c["initial_offers"],
            "final": count
        })

        time.sleep(0.4)

    # 4. Podsumowanie analityczne
    print("\n" + "=" * 80)
    print(" PODSUMOWANIE AUDYTU KONKURENCJI PO 48H")
    print("=" * 80)
    if results:
        print(f"{'ID':<8} | {'Godz':<6} | {'Start':<6} | {'Koniec':<7} | {'Przyrost':<9} | {'Tytuł'}")
        print("-" * 80)
        for r in results:
            diff = r['final'] - (int(r['initial']) if str(r['initial']).isdigit() else 0)
            diff_str = f"+{diff}" if diff >= 0 else str(diff)
            print(f"{r['id']:<8} | {r['hours']:<5.1f}h | {str(r['initial']):<6} | {r['final']:<7} | {diff_str:<9} | {r['title'][:35]}")

        avg_final = sum(r['final'] for r in results) / len(results)
        print("-" * 80)
        print(f"Średnia końcowa liczba ofert na zlecenie: {avg_final:.1f}")
        print(f"Zaktualizowano pliki w: {MAGAZYN_DIR}")
        print(f"Zaktualizowano powiązane pliki Markdown w: {KATALOG_DIR}")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Weryfikator końcowej liczby ofert po 48h na Useme")
    parser.add_argument("--min-hours", type=float, default=48.0, help="Minimalny wiek zlecenia w godzinach (domyślnie 48)")
    parser.add_argument("--force", action="store_true", help="Wymuś ponowne sprawdzenie nawet jeśli już sprawdzono")
    parser.add_argument("--limit", type=int, default=50, help="Maksymalna liczba zleceń do przetworzenia w jednym uruchomieniu")
    parser.add_argument("--dry-run", action="store_true", help="Tylko wyświetl kwalifikujące się zlecenia bez pobierania")
    args = parser.parse_args()

    run_auditor(min_hours=args.min_hours, force=args.force, limit=args.limit, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
