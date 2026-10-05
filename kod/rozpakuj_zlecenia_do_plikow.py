# -*- coding: utf-8 -*-
"""
rozpakuj_zlecenia_do_plikow.py - Konwertuje monolityczne pliki JSON z ofertami i wiadomosciami
w 04_moje_zlecenia na osobne, czytelne pliki per oferta i per watek.

Struktura po konwersji w kazdym folderze zlecenia:
  <job_id>/
    zlecenie.json
    oferty.json (lekki indeks z metadanymi i lista ID)
    oferty/
      <offer_id>.json (pelny rekord 1 oferty: 1-3 KB)
      ...
    wiadomosci.json (lekki indeks z metadanymi i lista ID watkow)
    wiadomosci/
      watek_<thread_id>.json (pelny rekord 1 watku z wiadomosciami)
      ...
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOJE_ZLECENIA_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia"


def _atomic_write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def rozpakuj_folder_zlecenia(folder: Path) -> dict:
    stats = {"oferty": 0, "watki": 0, "job_id": folder.name}
    
    # 1. Rozpakuj oferty
    oferty_map: dict[str, dict] = {}
    
    # a) Sprawdz oferty_publiczne.json (bogatsze dane, jesli istnieja)
    pub_path = folder / "oferty_publiczne.json"
    if not pub_path.exists():
        pub_path = folder / "oferty_publiczne_30.json"
    if pub_path.exists():
        try:
            d_pub = json.loads(pub_path.read_text(encoding="utf-8"))
            if isinstance(d_pub, list):
                for item in d_pub:
                    oid = str(item.get("offer_id") or "")
                    if oid:
                        oferty_map[oid] = item
        except Exception as e:
            print(f"[{folder.name}] Blad czytania {pub_path.name}: {e}")

    # b) Sprawdz oferty.json
    of_path = folder / "oferty.json"
    of_meta = {}
    if of_path.exists():
        try:
            d_of = json.loads(of_path.read_text(encoding="utf-8"))
            if isinstance(d_of, dict):
                of_meta = {k: v for k, v in d_of.items() if k != "oferty"}
                raw_oferty = d_of.get("oferty", [])
            elif isinstance(d_of, list):
                raw_oferty = d_of
            else:
                raw_oferty = []
                
            for item in raw_oferty:
                oid = str(item.get("offer_id") or "")
                if oid:
                    if oid in oferty_map:
                        # scal brakujace klucze
                        for k, v in item.items():
                            if k not in oferty_map[oid] or not oferty_map[oid][k]:
                                oferty_map[oid][k] = v
                    else:
                        oferty_map[oid] = item
        except Exception as e:
            print(f"[{folder.name}] Blad czytania oferty.json: {e}")

    # Zapisz oferty do folderu oferty/
    if oferty_map:
        oferty_dir = folder / "oferty"
        oferty_dir.mkdir(parents=True, exist_ok=True)
        for oid, offer in oferty_map.items():
            _atomic_write_json(oferty_dir / f"{oid}.json", offer)
        stats["oferty"] = len(oferty_map)

        # Zaktualizuj of_path do lekkiego indeksu (kompatybilnosc z kodem bez czytania 300KB)
        of_meta["liczba_ofert"] = len(oferty_map)
        of_meta["oferty_ids"] = sorted(list(oferty_map.keys()))
        of_meta["folder_ofert"] = "oferty/"
        _atomic_write_json(of_path, of_meta)

    # 2. Rozpakuj wiadomosci / watki
    watki_map: dict[str, dict] = {}
    
    # a) wiadomosci_prywatne_pelne.json / wiadomosci_zleceniodawcy_pelne.json
    priv_pelne = folder / "wiadomosci_prywatne_pelne.json"
    if not priv_pelne.exists():
        priv_pelne = folder / "wiadomosci_zleceniodawcy_pelne.json"
    if priv_pelne.exists():
        try:
            d_priv = json.loads(priv_pelne.read_text(encoding="utf-8"))
            if isinstance(d_priv, list):
                for item in d_priv:
                    tid = str(item.get("thread_pk") or item.get("thread_id") or "")
                    if tid:
                        watki_map[tid] = item
        except Exception as e:
            print(f"[{folder.name}] Blad czytania {priv_pelne.name}: {e}")

    # b) wiadomosci.json
    w_path = folder / "wiadomosci.json"
    w_meta = {}
    if w_path.exists():
        try:
            d_w = json.loads(w_path.read_text(encoding="utf-8"))
            if isinstance(d_w, dict):
                w_meta = {k: v for k, v in d_w.items() if k != "watki"}
                raw_watki = d_w.get("watki", [])
            elif isinstance(d_w, list):
                raw_watki = d_w
            else:
                raw_watki = []
                
            for item in raw_watki:
                tid = str(item.get("thread_id") or item.get("thread_pk") or item.get("pk") or "")
                if tid:
                    if tid in watki_map:
                        for k, v in item.items():
                            if k not in watki_map[tid] or not watki_map[tid][k]:
                                watki_map[tid][k] = v
                    else:
                        watki_map[tid] = item
        except Exception as e:
            print(f"[{folder.name}] Blad czytania wiadomosci.json: {e}")

    # Zapisz watki do folderu wiadomosci/
    if watki_map:
        wiad_dir = folder / "wiadomosci"
        wiad_dir.mkdir(parents=True, exist_ok=True)
        for tid, thread in watki_map.items():
            _atomic_write_json(wiad_dir / f"watek_{tid}.json", thread)
        stats["watki"] = len(watki_map)

        # Zaktualizuj w_path do lekkiego indeksu
        w_meta["liczba_watkow"] = len(watki_map)
        w_meta["watki_ids"] = sorted(list(watki_map.keys()))
        w_meta["folder_wiadomosci"] = "wiadomosci/"
        _atomic_write_json(w_path, w_meta)

    return stats


def main():
    print(f"Przeszukuje foldery w: {MOJE_ZLECENIA_DIR}")
    if not MOJE_ZLECENIA_DIR.exists():
        print(f"Brak katalogu: {MOJE_ZLECENIA_DIR}")
        return

    foldery = [p for p in MOJE_ZLECENIA_DIR.iterdir() if p.is_dir()]
    print(f"Znaleziono {len(foldery)} folderow zlecen.")
    
    lacznie_ofert = 0
    lacznie_watkow = 0
    for f in foldery:
        res = rozpakuj_folder_zlecenia(f)
        print(f" - {f.name}: {res['oferty']} ofert -> oferty/, {res['watki']} watkow -> wiadomosci/")
        lacznie_ofert += res["oferty"]
        lacznie_watkow += res["watki"]

    print("\n" + "="*50)
    print(f"ZAKONCZONO ROZPAKOWYWANIE:")
    print(f"Lacznie utworzono {lacznie_ofert} plikow ofert oraz {lacznie_watkow} plikow watkow.")
    print("="*50)


if __name__ == "__main__":
    main()
