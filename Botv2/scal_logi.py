# -*- coding: utf-8 -*-
"""Skrypt scalający logi z Botv2/logi do pojedynczych plików JSON.

Dla każdego zlecenia w `Botv2/logi/<job_id>/` tworzy jeden spójny plik JSON,
w którym wszystkie etapy pracy bota (zlecenie, analiza, research, weryfikacja,
wycena, draft, oferta końcowa, checker, sędzia, veto, logi, wynik) są
uporządkowane po kolei w czytelnej strukturze gotowej do wysłania do AI w przeglądarce.

Generuje:
1. `logi_scalone_json/<job_id>.json` - pojedynczy scalony JSON dla każdego zlecenia.
2. `logi_scalone_json/_wszystkie_scalone.json` - zbiorczy plik ze wszystkimi zleceniami na raz.
3. `logi_scalone_json/_indeks.json` - lekki indeks wszystkich zleceń (ID, tytuł, budżet, wycena, werdykt).
4. `logi_scalone_json/_indeks.md` - czytelny spis treści w Markdown.
5. `logi_scalone_json/z_tytulami/<job_id> - <tytul>.json` - kopie z tytułem w nazwie pliku.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
LOGI_DIR = BASE_DIR / "logi"
OUT_DIR = BASE_DIR / "logi_scalone_json"
OUT_WITH_TITLES_DIR = OUT_DIR / "z_tytulami"


def sanitize_filename(name: str, max_length: int = 60) -> str:
    """Oczyszcza tytuł pod kątem bezpiecznej nazwy pliku w Windows."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip()
    return cleaned


def read_text_file(path: Path) -> Optional[str]:
    """Wczytuje zawartość pliku tekstowego UTF-8."""
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def read_json_file(path: Path) -> Optional[Any]:
    """Wczytuje i parsuje plik JSON."""
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        return {"error": f"Blad parsowania JSON: {e}"}


def scal_zlecenie(folder_path: Path) -> Dict[str, Any]:
    """Scala wszystkie pliki z folderu zlecenia w jeden obiekt słownikowy."""
    job_id = folder_path.name

    zlecenie_raw = read_text_file(folder_path / "00_zlecenie.txt") or ""
    tytul_m = re.search(r"TYTUL:\s*(.*?)(?=\nBUDZET:|\nOPIS:|$)", zlecenie_raw, re.DOTALL)
    budzet_m = re.search(r"BUDZET:\s*(.*?)(?=\nOPIS:|$)", zlecenie_raw, re.DOTALL)
    opis_m = re.search(r"OPIS:\s*(.*)", zlecenie_raw, re.DOTALL)

    tytul_parsed = tytul_m.group(1).strip() if tytul_m else ""
    budzet_parsed = budzet_m.group(1).strip() if budzet_m else ""
    opis_parsed = opis_m.group(1).strip() if opis_m else ""

    analiza = read_text_file(folder_path / "01_analiza.md")
    research = read_text_file(folder_path / "02_research.md")
    weryfikacja = read_text_file(folder_path / "03_weryfikacja.md")
    wycena = read_text_file(folder_path / "04_wycena.md")
    pismo_raw = read_text_file(folder_path / "05_pismo_raw.md")
    oferta_final = read_text_file(folder_path / "06_oferta_final.md")
    checker = read_json_file(folder_path / "07_checker.json")
    sedzia = read_json_file(folder_path / "08_sedzia.json")
    veto = read_text_file(folder_path / "09_veto_przebieg.md")
    log_txt = read_text_file(folder_path / "10_log.txt")
    wynik = read_json_file(folder_path / "wynik.json") or {}

    tytul = tytul_parsed or wynik.get("title") or ""
    budzet = budzet_parsed or wynik.get("budget") or ""

    podsumowanie = {
        "wycena_dolna": wynik.get("wycena_dolna"),
        "wycena_gorna": wynik.get("wycena_gorna"),
        "definitywna": wynik.get("definitywna"),
        "dni_od": wynik.get("dni_od"),
        "dni_do": wynik.get("dni_do"),
        "uzasadnienie_rozjemcy": wynik.get("uzasadnienie_rozjemcy"),
        "od_czego_zaleza": wynik.get("od_czego_zaleza") or [],
        "checker_ok": wynik.get("checker_ok", checker.get("ok") if isinstance(checker, dict) else None),
        "sedzia": wynik.get("sedzia", sedzia.get("status") if isinstance(sedzia, dict) else None),
        "veto_napraw": wynik.get("veto_napraw", 1 if veto else 0),
    }

    # Uporządkowane etapy procesu krok po kroku
    etapy = {
        "00_zlecenie": {
            "tytul": tytul,
            "budzet": budzet,
            "opis": opis_parsed,
            "raw": zlecenie_raw,
        },
        "01_analiza": analiza,
        "02_research": research,
        "03_weryfikacja": weryfikacja,
        "04_wycena": wycena,
        "05_pismo_raw": pismo_raw,
        "06_oferta_final": oferta_final,
        "07_checker": checker,
        "08_sedzia": sedzia,
        "09_veto_przebieg": veto,
        "10_log": log_txt,
    }

    return {
        "job_id": job_id,
        "tytul": tytul,
        "budzet": budzet,
        "podsumowanie": podsumowanie,
        "oferta_finalna": oferta_final,
        "opis_zlecenia": opis_parsed,
        "etapy": etapy,
        "wynik_pelny": wynik,
    }


def main() -> None:
    if not LOGI_DIR.is_dir():
        print(f"Blad: Katalog {LOGI_DIR} nie istnieje!")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_WITH_TITLES_DIR.mkdir(parents=True, exist_ok=True)

    folder_list = sorted([d for d in LOGI_DIR.iterdir() if d.is_dir()])
    print(f"Znaleziono {len(folder_list)} zlecen w {LOGI_DIR}")

    wszystkie: List[Dict[str, Any]] = []
    indeks: List[Dict[str, Any]] = []
    indeks_md_lines = [
        "# Indeks scalonych logów zleceń Botv2",
        "",
        f"Liczba zleceń: **{len(folder_list)}**",
        "",
        "| ID | Tytuł | Budżet klienta | Wycena bota (PLN) | Czas (dni) | Sędzia | Veto | Plik JSON |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for fld in folder_list:
        job_id = fld.name
        try:
            scalone = scal_zlecenie(fld)
            wszystkie.append(scalone)

            # 1. Zapis per job_id.json
            out_file = OUT_DIR / f"{job_id}.json"
            out_file.write_text(json.dumps(scalone, ensure_ascii=False, indent=2), encoding="utf-8")

            # 2. Zapis w wersji z tytułem
            title_slug = sanitize_filename(scalone["tytul"])
            title_filename = f"{job_id} - {title_slug}.json" if title_slug else f"{job_id}.json"
            (OUT_WITH_TITLES_DIR / title_filename).write_text(
                json.dumps(scalone, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            # Wpis do indeksu
            pod = scalone["podsumowanie"]
            wycena_str = (
                f"{pod['wycena_dolna']} - {pod['wycena_gorna']}"
                if pod["wycena_dolna"] is not None and pod["wycena_gorna"] is not None
                else "Brak"
            )
            dni_str = f"{pod['dni_od']} - {pod['dni_do']}" if pod["dni_od"] is not None else "-"
            sedzia_status = pod["sedzia"] or "-"
            veto_status = "TAK" if pod["veto_napraw"] and pod["veto_napraw"] > 0 else "NIE"

            indeks.append({
                "job_id": job_id,
                "tytul": scalone["tytul"],
                "budzet": scalone["budzet"],
                "wycena_dolna": pod["wycena_dolna"],
                "wycena_gorna": pod["wycena_gorna"],
                "dni_od": pod["dni_od"],
                "dni_do": pod["dni_do"],
                "sedzia": sedzia_status,
                "veto_napraw": pod["veto_napraw"],
                "plik_json": f"{job_id}.json",
                "plik_z_tytulem": title_filename,
            })

            clean_title_table = scalone["tytul"].replace("|", "\\|")
            indeks_md_lines.append(
                f"| `{job_id}` | {clean_title_table} | {scalone['budzet']} | {wycena_str} | {dni_str} | {sedzia_status} | {veto_status} | [{job_id}.json](./{job_id}.json) |"
            )

            print(f"  OK: {job_id} -> {out_file.name}")
        except Exception as e:
            print(f"  BLAD: {job_id}: {e}")

    # 3. Zapis zbiorczego pliku _wszystkie_scalone.json
    all_file = OUT_DIR / "_wszystkie_scalone.json"
    all_file.write_text(json.dumps(wszystkie, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nZapisano zbiorczy plik: {all_file.name} ({len(wszystkie)} zlecen)")

    # 4. Zapis _indeks.json
    indeks_file = OUT_DIR / "_indeks.json"
    indeks_file.write_text(json.dumps(indeks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Zapisano indeks JSON: {indeks_file.name}")

    # 5. Zapis _indeks.md
    indeks_md_file = OUT_DIR / "_indeks.md"
    indeks_md_file.write_text("\n".join(indeks_md_lines), encoding="utf-8")
    print(f"Zapisano indeks Markdown: {indeks_md_file.name}")

    print("\nGotowe! Wszystko wyeksportowane do:", OUT_DIR)


if __name__ == "__main__":
    main()
