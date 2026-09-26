# -*- coding: utf-8 -*-
import shutil
from pathlib import Path
import json

base_dir = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
target_dir = base_dir / "paczka_analiza_strategii"
target_dir.mkdir(parents=True, exist_ok=True)

files_to_copy = [
    (base_dir / "badania" / "rynek" / "profil" / "profil_ksawier_potrykus_1do1.md", "01_profil_ksawiera_realia_useme.md"),
    (base_dir / "badania" / "strategia" / "01_material_dowodowy" / "08_bezwzgledny_audyt_statystyczny_551_zlecen.md", "02_audyt_rynku_551_zlecen.md"),
    (base_dir / "badania" / "strategia" / "01_material_dowodowy" / "04_dekonstrukcja_12_wygranych_ofert.md", "03_dekonstrukcja_wygranych_ofert.md"),
    (base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "podsumowanie_wywiadu.md", "04_raport_wywiadu_28_ofert_konkurencji.md"),
    (base_dir / "badania" / "strategia" / "arsenal_zamykania.md", "05_dotychczasowy_arsenal_zamykania.md"),
    (base_dir / "kod" / "prompts" / "kontekst" / "jak_pisac_oferty.md", "06_zasady_pisania_ofert_i_styl.md"),
    (base_dir / "kod" / "prompts" / "kontekst" / "lore.md", "07_lore_i_doswiadczenie_zespolu.md"),
    (base_dir / "badania" / "strategia" / "mystery_shopping.md", "08_strategia_mystery_shopping_i_teoria_gier.md")
]

copied_files = []
for src, dst_name in files_to_copy:
    if src.exists():
        dst = target_dir / dst_name
        shutil.copy2(src, dst)
        copied_files.append((dst_name, dst.stat().st_size))
        print(f"Skopiowano: {dst_name} ({dst.stat().st_size} bajtów)")
    else:
        print(f"UWAGA: Plik nie istnieje: {src}")

# Stwórzmy też jeden plik zbiorczy (MONOLIT), żeby użytkownik mógł wkleić WSZYSTKO na raz w 1 plik do Claude / ChatGPT!
monolit_path = target_dir / "KOMPLETNY_KONTEKST_DLA_AI_WSZYSTKO_W_JEDNYM.md"
with open(monolit_path, "w", encoding="utf-8") as out:
    out.write("# KOMPLETNY MATERIAŁ DOWODOWY I STRATEGICZNY DO ANALIZY DLA MODELU AI\n\n")
    out.write("> Ten dokument zawiera kompletny audyt konta, bazy 551 zleceń, profilu wykonawcy, historii wygranych oraz zbadanego rynku konkurencji (28 ofert pod zleceniem badawczym #144890).\n\n")
    out.write("="*80 + "\n\n")
    
    for dst_name, _ in copied_files:
        fpath = target_dir / dst_name
        out.write(f"\n\n{'#'*80}\n# PLIK ŹRÓDŁOWY: {dst_name}\n{'#'*80}\n\n")
        out.write(fpath.read_text(encoding="utf-8"))
        out.write("\n\n")

print(f"\nWygenerowano plik monolit: {monolit_path.name} ({monolit_path.stat().st_size} bajtów)")
