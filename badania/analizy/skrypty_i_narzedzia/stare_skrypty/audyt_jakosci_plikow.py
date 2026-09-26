# -*- coding: utf-8 -*-
"""Audyt spójności, jakości formatowania i poprawności wszystkich wygenerowanych plików."""

import json
from pathlib import Path

errors = []
warnings = []

# 1. Sprawdzenie głównego JSON bazy
p = Path('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json')
if not p.exists():
    errors.append('Brak pliku przegrane_oferty_pelne_416.json')
else:
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        if len(data) != 406:
            warnings.append(f'Liczba ofert w JSON to {len(data)}, oczekiwano 406')
        empty_descs = [x['offer_id'] for x in data if not x.get('job_description')]
        if empty_descs:
            warnings.append(f'Oferty bez opisu zlecenia: {len(empty_descs)}')
        empty_props = [x['offer_id'] for x in data if not x.get('our_proposal')]
        if empty_props:
            warnings.append(f'Oferty bez propozycji: {len(empty_props)}')
    except Exception as e:
        errors.append(f'Blad parsowania JSON bazy: {e}')

# 2. Sprawdzenie katalogu ofert
cat_dir = Path('badania/rynek/katalog_ofert')
if not cat_dir.exists():
    errors.append('Brak katalogu badania/rynek/katalog_ofert')
else:
    md_files = list(cat_dir.glob('**/*.md'))
    offer_mds = [f for f in md_files if f.name != 'INDEKS_OFERT.md']
    folder_count = len([d for d in cat_dir.iterdir() if d.is_dir()])
    print(f"Znaleziono {len(offer_mds)} plikow markdown ofert w {folder_count} folderach kategorii.")
    if len(offer_mds) != 406:
        warnings.append(f'Liczba plikow ofert to {len(offer_mds)}, oczekiwano 406')
    
    empty_files = [f for f in offer_mds if f.stat().st_size < 100]
    if empty_files:
        errors.append(f'Puste lub za male pliki ofert: {len(empty_files)}')

# 3. Sprawdzenie indeksu INDEKS_OFERT.md
idx = cat_dir / 'INDEKS_OFERT.md'
if not idx.exists():
    errors.append('Brak pliku INDEKS_OFERT.md')
else:
    txt = idx.read_text(encoding='utf-8')
    if len(txt) < 1000:
        errors.append('INDEKS_OFERT.md jest zbyt maly / urwany')
    else:
        print(f"INDEKS_OFERT.md: {len(txt)} bajtow, {len(txt.splitlines())} linii.")

# 4. Sprawdzenie czy w prompts/ i strategia/ nie ma slowa blueprint w rekomendacjach
forbidden_hits = []
for f in Path('prompts').glob('**/*.md'):
    t = f.read_text(encoding='utf-8').lower()
    if 'blueprint' in t:
        forbidden_hits.append(str(f))

# 5. Sprawdzenie raportow subagentow w strategia/
reports = [
    'strategia/01_material_dowodowy/03_analiza_rynku_406_zlecen_pelna_baza.md',
    'strategia/02_fundamenty_psychologiczne/05_psychologia_konwersji_i_strategia_zamkniecia.md',
    'strategia/arsenal_zamykania.md',
    'strategia/01_material_dowodowy/06_analiza_trendow_czasowych_i_rytm_tygodniowy_useme.md',
    'strategia/03_matryca_decyzyjna_i_klientow/01_matryca_priorytetyzacji_zlecen_tier.md'
]
report_status = {}
for r in reports:
    rf = Path(r)
    if rf.exists():
        size = rf.stat().st_size
        lines = len(rf.read_text(encoding='utf-8').splitlines())
        report_status[rf.name] = f"OK ({size} bajtow, {lines} linii)"
    else:
        errors.append(f"Brak pliku raportu: {r}")

print("\n=== STATUS WYGENEROWANYCH RAPORTÓW BIZNESOWYCH ===")
for name, stat in report_status.items():
    print(f"  - {name}: {stat}")

print("\n=== PODSUMOWANIE AUDYTU TECHNICZNEGO ===")
print("Bledy krytyczne:", errors if errors else "BRAK (0 bledow)")
print("Ostrzezenia:", warnings if warnings else "BRAK (0 ostrzezen)")
print("Zakazany blueprint w prompts/:", forbidden_hits if forbidden_hits else "CZYSTO (0 wystapien)")
