# -*- coding: utf-8 -*-
"""Segregator bazy zamkniętych ofert Useme na czytelną strukturę folderów i plików.

Dla każdej oferty tworzy dedykowany, sformatowany plik Markdown w odpowiednim folderze
kategorii (np. 01_aplikacje_webowe, 05_strony_internetowe, 06_sklepy_ecommerce),
zawierający:
- Pełną treść ogłoszenia zleceniodawcy (job_description)
- Pełną treść naszej oferty (our_proposal)
- Metadane (budżet, nasza wycena, dni, prawa autorskie, umowy klienta, link)

ZASADA NADRZĘDNOŚCI DANYCH LOKALNYCH:
Jeśli zlecenie istnieje w naszym lokalnym magazynie (magazyn/**/*.json), jego treść
z momentu składania oferty jest traktowana jako jedyna prawdziwa i ma pierwszeństwo
przed późniejszymi modyfikacjami klienta na Useme.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SegregatorOfert")

BASE_DIR = Path(__file__).resolve().parent
BADANIA_DIR = BASE_DIR.parent / "badania"
INPUT_FILE = config.PRZEGRANE_DIR / "przegrane_pelne_416.json"
CATALOG_DIR = BADANIA_DIR / "rynek" / "katalog_ofert"
MAGAZYN_DIR = config.MAGAZYN_DIR

CATEGORY_MAPPING = {
    "Programowanie i IT · Aplikacje webowe": "01_aplikacje_webowe",
    "Programowanie i IT · Oprogramowanie": "02_oprogramowanie_i_skrypty",
    "Programowanie i IT · Projekty IT": "03_projekty_it_systemy",
    "Programowanie i IT · Aplikacje mobilne": "04_aplikacje_mobilne",
    "Serwisy internetowe · Strony internetowe": "05_strony_internetowe",
    "Serwisy internetowe · Sklepy internetowe": "06_sklepy_ecommerce",
    "Serwisy internetowe · Obsługa sklepów internetowych": "07_obsluga_ecommerce",
    "Marketing · Sprzedaż i obsługa sprzedaży": "08_marketing_i_sprzedaz",
}


def slugify(text: str, max_length: int = 45) -> str:
    """Tworzy bezpieczną nazwę pliku z tytułu."""
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'a', 'Ć': 'c', 'Ę': 'e', 'Ł': 'l', 'Ń': 'n',
        'Ó': 'o', 'Ś': 's', 'Ź': 'z', 'Ż': 'z'
    }
    for pol, lat in replacements.items():
        text = text.replace(pol, lat)
    text = re.sub(r'[^a-zA-Z0-9\s_-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-').lower()
    return text[:max_length].rstrip('-')


def normalize_title(title: str) -> str:
    """Normalizuje tytuł do porównań."""
    t = re.sub(r'\s+', ' ', title or '').strip().lower()
    return t


def load_local_warehouse() -> Dict[str, Dict[str, Any]]:
    """Wczytuje lokalny magazyn (magazyn/**/*.json).
    Jeśli zlecenie było w magazynie, jego treść z momentu oferty jest nadrzędna.
    """
    warehouse_by_title: Dict[str, Dict[str, Any]] = {}
    if not MAGAZYN_DIR.exists():
        return warehouse_by_title

    files = list(MAGAZYN_DIR.glob("**/*.json"))
    for f in files:
        if f.name.startswith("."):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            t_norm = normalize_title(d.get("title", ""))
            desc = d.get("full_details", {}).get("full_description", "").strip()
            if not desc:
                desc = d.get("list_details", {}).get("short_desc", "").strip()

            if t_norm and desc and len(desc) > 20:
                warehouse_by_title[t_norm] = {
                    "job_id": str(d.get("id", "")),
                    "file_path": str(f.relative_to(BASE_DIR)),
                    "original_description": desc,
                    "budget": d.get("budget"),
                    "category": d.get("category"),
                    "detected_at": d.get("detected_at") or d.get("data_wyslania")
                }
        except Exception:
            continue

    logger.info(f"Zindeksowano {len(warehouse_by_title)} oryginalnych zleceń z lokalnego magazynu.")
    return warehouse_by_title


def format_offer_markdown(offer: Dict[str, Any]) -> str:
    """Generuje czytelny plik Markdown dla pojedynczej oferty."""
    oid = offer.get("offer_id", "brak_id")
    title = offer.get("title", "Bez tytułu")
    client = offer.get("client", "Nieznany")
    contracts = offer.get("client_contracts", "0 umów")
    category = offer.get("category", "Nieprzypisane")
    budget = offer.get("budget", "Brak danych / Do negocjacji")
    price = offer.get("our_price", "Brak wyceny")
    days = offer.get("our_days", "Brak danych")
    copyright_info = offer.get("copyright", "Brak danych")
    url = offer.get("offer_url", f"https://useme.com/pl/jobs/my-offer/{oid}/")
    job_desc = offer.get("job_description", "").strip() or "*[Brak pobranego opisu klienta]*"
    proposal = offer.get("our_proposal", "").strip() or "*[Brak treści propozycji]*"

    source_alert = ""
    if offer.get("is_original_from_magazyn"):
        source_alert = (
            f"> [!IMPORTANT]\n"
            f"> **Pierwotna treść zlecenia:** Opis został przywrócony z lokalnego pliku `{offer.get('magazyn_source_file')}` "
            f"(stan z momentu złożenia oferty, z pominięciem późniejszych edycji klienta na Useme).\n\n"
        )

    md = f"""# [{oid}] {title}

| Parametr | Wartość |
| :--- | :--- |
| **ID Oferty** | `{oid}` |
| **Kategoria** | {category} |
| **Zleceniodawca** | **{client}** ({contracts}) |
| **Budżet Klienta** | `{budget}` |
| **Nasza Wycena** | `{price}` |
| **Czas Realizacji** | `{days} dni roboczych` |
| **Prawa Autorskie** | {copyright_info} |
| **Link do zlecenia** | [{url}]({url}) |

---

## 1. Pełna Treść Ogłoszenia Klienta

{source_alert}{job_desc}

---

## 2. Nasza Złożona Oferta

{proposal}

---

## 3. Metadane Techniczne (JSON)

```json
{json.dumps(offer, ensure_ascii=False, indent=2)}
```
"""
    return md


def segregate_offers():
    """Wczytuje bazę, priorytetyzuje wersje lokalne z magazynu, zapisuje pliki i tworzy indeks."""
    if not INPUT_FILE.exists():
        logger.error(f"Plik źródłowy nie istnieje: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        offers = list(data.values())
    else:
        offers = data

    logger.info(f"Wczytano {len(offers)} ofert do segregacji...")
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Wczytanie lokalnego magazynu
    warehouse = load_local_warehouse()
    replaced_from_local = 0

    index_rows = []
    category_counts: Dict[str, int] = {}

    for off in offers:
        oid = str(off.get("offer_id", ""))
        title = off.get("title", "zlecenie")
        t_norm = normalize_title(title)

        # SPRAWDZENIE CZY MAMY ORYGINAŁ W LOKALNYM MAGAZYNIE
        if t_norm in warehouse:
            local_entry = warehouse[t_norm]
            off["job_description"] = local_entry["original_description"]
            off["is_original_from_magazyn"] = True
            off["magazyn_source_file"] = local_entry["file_path"]
            if not off.get("budget") or off.get("budget") == "Do negocjacji":
                if local_entry.get("budget"):
                    off["budget"] = local_entry["budget"]
            replaced_from_local += 1

        raw_cat = off.get("category", "")
        cat_folder_name = CATEGORY_MAPPING.get(raw_cat, "99_inne_zlecenia")

        target_folder = CATALOG_DIR / cat_folder_name
        target_folder.mkdir(parents=True, exist_ok=True)

        safe_slug = slugify(title)
        filename = f"{oid}_{safe_slug}.md" if safe_slug else f"{oid}.md"
        file_path = target_folder / filename

        content = format_offer_markdown(off)
        with open(file_path, "w", encoding="utf-8") as f_out:
            f_out.write(content)

        category_counts[cat_folder_name] = category_counts.get(cat_folder_name, 0) + 1

        rel_link = f"{cat_folder_name}/{filename}"
        client_info = f"{off.get('client', 'Anonim')} ({off.get('client_contracts', '')})"
        budget_info = off.get("budget", "-")
        price_info = off.get("our_price", "-")
        days_info = off.get("our_days", "-")

        safe_title = title.replace("|", "/")
        index_rows.append(
            f"| `{oid}` | [{safe_title}]({rel_link}) | `{cat_folder_name}` | {client_info} | {budget_info} | **{price_info}** | {days_info} |"
        )

    # Generowanie INDEKS_OFERT.md
    index_md_path = CATALOG_DIR / "INDEKS_OFERT.md"
    with open(index_md_path, "w", encoding="utf-8") as f_idx:
        f_idx.write(f"# Katalog Zamkniętych Ofert Useme ({len(offers)} zleceń)\n\n")
        f_idx.write("Kompletna, posegregowana baza zleceń z podziałem na kategorie tematyczne. ")
        f_idx.write("Każdy rekord zawiera pełną treść ogłoszenia klienta oraz naszą kompletną ofertę.\n\n")

        if replaced_from_local > 0:
            f_idx.write(f"> [!NOTE]\n")
            f_idx.write(f"> Dla **{replaced_from_local} zleceń** przywrócono pierwotną treść ogłoszenia z lokalnego `magazynu/` (stan z momentu składania oferty).\n\n")

        f_idx.write("### Rozkład wg Kategorii:\n\n")
        for cat_name, cnt in sorted(category_counts.items(), key=lambda x: -x[1]):
            f_idx.write(f"- **`{cat_name}/`**: {cnt} zleceń\n")
        f_idx.write("\n---\n\n")

        f_idx.write("### Pełny Spis Zleceń:\n\n")
        f_idx.write("| ID | Tytuł (Link do pliku) | Folder Kategorii | Klient (Umowy) | Budżet Klienta | Nasza Wycena | Dni |\n")
        f_idx.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for row in index_rows:
            f_idx.write(row + "\n")

    logger.info(f"Pomyślnie posegregowano {len(offers)} ofert do {CATALOG_DIR}!")
    logger.info(f"Przywrócono pierwotną treść z lokalnego magazynu dla {replaced_from_local} ofert.")
    logger.info(f"Utworzono główny indeks: {index_md_path}")


if __name__ == "__main__":
    segregate_offers()
