# -*- coding: utf-8 -*-
"""
Generator kompletnego pakietu analitycznego dla Claude Sonnet 3.5.
Buduje zunifikowany, maksymalnie gęsty zestaw danych w `paczka_analiza_strategii`.
Zawiera 30 ofert publicznych oraz 4 pełne wątki prywatnych wiadomości od seniorów.
"""
import os
import shutil
import json
from pathlib import Path

base_dir = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
target_dir = base_dir / "paczka_analiza_strategii"
zrodla_dir = target_dir / "zrodla_szczegolowe_md"

target_dir.mkdir(parents=True, exist_ok=True)
zrodla_dir.mkdir(parents=True, exist_ok=True)

# 1. Definicja modułów wiedzy
md_modules = [
    ("01_profil_ksawiera_realia_useme.md", base_dir / "badania" / "rynek" / "profil" / "profil_ksawier_potrykus_1do1.md", "MODUŁ 1: PROFIL KSAWIERA, TECHNOLOGIA, FORMALNOŚCI I SPECYFIKA USEME"),
    ("02_audyt_rynku_551_zlecen.md", base_dir / "badania" / "strategia" / "01_material_dowodowy" / "08_bezwzgledny_audyt_statystyczny_551_zlecen.md", "MODUŁ 2: BEZWZGLĘDNY AUDYT STATYSTYCZNY 551 ZLECEŃ NA USEME"),
    ("03_dekonstrukcja_wygranych_ofert.md", base_dir / "badania" / "strategia" / "01_material_dowodowy" / "04_dekonstrukcja_12_wygranych_ofert.md", "MODUŁ 3: DEKONSTRUKCJA WYGRANYCH OFERT I MECHANIZMY SUKCESU"),
    ("04_raport_wywiadu_30_ofert_konkurencji.md", base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "podsumowanie_wywiadu.md", "MODUŁ 4: RAPORT WYWIADU RYNKOWEGO - 30 OFERT KONKURENCJI NA ZLECENIU #144890"),
    # TODO: brak odpowiednika raport_wiadomosci_prywatnych_zleceniodawcy.md; najblizej: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/wiadomosci_prywatne.md
    ("04b_raport_prywatnych_wiadomosci_seniorow.md", base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "wiadomosci_prywatne.md", "MODUŁ 4B: RAPORT PRYWATNYCH WIADOMOŚCI OD SENIORÓW (4 EXPERT THREADS)"),
    ("05_dotychczasowy_arsenal_zamykania.md", base_dir / "badania" / "strategia" / "arsenal_zamykania.md", "MODUŁ 5: ARSENAŁ ZAMYKANIA OFERT DLA GŁÓWNYCH GRUP POPYTU"),
    ("06_zasady_pisania_ofert_i_styl.md", base_dir / "kod" / "prompts" / "kontekst" / "jak_pisac_oferty.md", "MODUŁ 6: REGUŁY PISANIA OFERT, STYL I PSYCHOLOGIA B2B"),
    ("07_lore_i_doswiadczenie_zespolu.md", base_dir / "kod" / "prompts" / "kontekst" / "lore.md", "MODUŁ 7: LORE ZESPOŁU, PODZIAŁ RÓL I ZAPLECZE INŻYNIERSKIE"),
    ("08_strategia_mystery_shopping_i_teoria_gier.md", base_dir / "badania" / "strategia" / "mystery_shopping.md", "MODUŁ 8: STRATEGIA MYSTERY SHOPPING, ZLECENIA DECOY I TEORIA GIER"),
    ("09_portfolio_i_case_studies_b2b.md", base_dir / "badania" / "strategia" / "05_portfolio_i_case_studies" / "01_kompletny_pakiet_portfolio_i_case_studies_b2b.md", "MODUŁ 9: KOMPLETNY PAKIET PORTFOLIO B2B & 9 CASE STUDIES TECHNICZNYCH"),
    ("10_audyt_red_team_ryzyka_i_wady.md", base_dir / "badania" / "strategia" / "04_rejestr_hipotez_i_falsyfikacji" / "05_audyt_red_team_ryzyka_i_wady.md", "MODUŁ 10: AUDYT RED TEAM - RYZYKA, BŁĘDY I MARTWE PUNKTY OFERT"),
    ("11_psychologia_konwersji_i_strategia_zamkniecia.md", base_dir / "badania" / "strategia" / "02_fundamenty_psychologiczne" / "05_psychologia_konwersji_i_strategia_zamkniecia.md", "MODUŁ 11: PSYCHOLOGIA KONWERSJI, ANATOMIA LĘKÓW KLIENTA I CTA"),
    ("12_mapowanie_9_typow_klientow.md", base_dir / "badania" / "strategia" / "03_matryca_decyzyjna_i_klientow" / "02_mapowanie_9_typow_klientow.md", "MODUŁ 12: MATRYCA 9 TYPÓW KLIENTÓW NA USEME I DOPASOWANIE STRATEGII")
]

print("1. Kopiowanie modułów źródłowych do 'zrodla_szczegolowe_md'...")
for fname, src, _ in md_modules:
    if src.exists():
        dst = zrodla_dir / fname
        shutil.copy2(src, dst)
        print(f"  -> Skopiowano: {fname} ({dst.stat().st_size} bajtów)")

# 2. Budowa monolitu markdown 01_KOMPLETNA_WIEDZA_STRATEGICZNA_I_LORE.md
print("\n2. Budowa zunifikowanego pliku Master Markdown...")
master_md_path = target_dir / "01_KOMPLETNA_WIEDZA_STRATEGICZNA_I_LORE.md"

with open(master_md_path, "w", encoding="utf-8") as out:
    out.write("""# KOMPLETNE KOMPENDIUM STRATEGICZNO-RYNKOWE DLA AI: USEME B2B ACCELERATOR

> **CEL DOKUMENTU:** 
> Dostarczenie zaawansowanemu modelowi AI (Claude Sonnet 3.5) pełnego, bezkompromisowego kontekstu operacyjnego, rynkowego i psychologicznego Ksawiera Potrykusa na platformie Useme.
> 
> **GŁÓWNY PROBLEM DO ROZWIĄZANIA:**
> Rynek zleceń IT na Useme jest zalany generycznymi ofertami freelancerów i software house'ów (92% proponuje n8n, korpomowę, darmowe calle i powtarzalne slogany). Ksawier chce drastycznie zwiększyć współczynnik wygranych ofert (win rate) w zleceniach o budżetach 3 000 zł - 25 000 zł.
> 
> **KLUCZOWE ODKRYCIE ZLECONEGO BADANIA #144890:**
> - Złożono 30 ofert publicznych (stawki od 500 zł do 36 000 zł, mediana ~4500 zł).
> - Niezależnie od tego, 4 doświadczonych wykonawców / konsultantów NIE ZŁOŻYŁO oferty publicznej, lecz napisało prywatne wiadomości bezpośrednio do zleceniodawcy, punktując krytyczne luki architektoniczne (zaokrąglenia VAT o 1 grosz, deduplikacja NIP+nr dokumentu, integracja KSeF vs niepotrzebny OCR).
> 
> **KLUCZOWE PYTANIE STRATEGICZNE:**
> W jaki sposób wykazać się czymś FUNDAMENTALNIE INNYM niż cała konkurencja (contrarian strategy), łącząc strategiczną głębię z natychmiastowym dowodem kompetencji bezpośrednio w publicznej ofercie, zamiast kopiować ich szablony i ścigać się na dno cenowe?

================================================================================
# SPIS TREŚCI ZUNIFIKOWANEJ BAZY WIEDZY:
- MODUŁ 1: Profil Ksawiera, Technologia, Formalności i Specyfika Useme
- MODUŁ 2: Bezwzględny Audyt Statystyczny 551 Zleceń na Useme
- MODUŁ 3: Dekonstrukcja Wygranych Ofert i Mechanizmy Sukcesu
- MODUŁ 4: Raport Wywiadu Rynkowego - 30 Ofert Konkurencji na Zleceniu #144890
- MODUŁ 4B: Raport Prywatnych Wiadomości od Seniorów (4 Expert Threads)
- MODUŁ 5: Arsenał Zamykania Ofert dla Głównych Grup Popytu
- MODUŁ 6: Reguły Pisania Ofert, Styl i Psychologia B2B
- MODUŁ 7: Lore Zespołu, Podział Ról i Zaplecze Inżynierskie
- MODUŁ 8: Strategia Mystery Shopping, Zlecenia Decoy i Teoria Gier
- MODUŁ 9: Kompletny Pakiet Portfolio B2B & 9 Case Studies Technicznych
- MODUŁ 10: Audyt Red Team - Ryzyka, Błędy i Martwe Punkty Ofert
- MODUŁ 11: Psychologia Konwersji, Anatomia Lęków Klienta i CTA
- MODUŁ 12: Matryca 9 Typów Klientów na Useme i Dopasowanie Strategii
================================================================================

""")
    for fname, src, header in md_modules:
        if src.exists():
            content = src.read_text(encoding="utf-8")
            out.write(f"\n\n{'='*80}\n# {header}\n# Plik źródłowy: {fname}\n{'='*80}\n\n")
            out.write(content)
            out.write("\n")

print(f"  -> Zapisano master markdown: {master_md_path.name} ({master_md_path.stat().st_size} bajtów)")

# 3. Zintegrowany plik z ofertami publicznymi (30 sztuk) ORAZ prywatnymi wiadomościami (4 wątki)
print("\n3. Przygotowywanie 02_SUROWE_OFERTY_I_WIADOMOSCI_ZLECENIE_144890.json...")
# TODO: brak pliku oferty_konkurencji_144890.json; najblizej: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/oferty_publiczne_30.json
raw_offers_src = base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "oferty_publiczne_30.json"
# TODO: brak pliku wiadomosci_zleceniodawcy_pelne.json; najblizej: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/wiadomosci_prywatne_pelne.json
raw_messages_src = base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "wiadomosci_prywatne_pelne.json"

offers_data = json.loads(raw_offers_src.read_text(encoding="utf-8")) if raw_offers_src.exists() else []
messages_data = json.loads(raw_messages_src.read_text(encoding="utf-8")) if raw_messages_src.exists() else []

combined_market_survey = {
    "opis": "Kompletny materiał wywiadowczy ze zlecenia #144890: 30 publicznych ofert konkurencji + 4 prywatne wątki od seniorów",
    "zlecenie_badawcze": {
        "id": "144890",
        "tytul": "Automatyzacja obiegu faktur i dokumentów kosztowych",
        "liczba_ofert_publicznych": len(offers_data),
        "liczba_watkow_prywatnych": len(messages_data)
    },
    "prywatne_wiadomosci_od_seniorow_bez_ofert_publicznych": messages_data,
    "publiczne_oferty_konkurencji_30_sztuk": offers_data
}

raw_dst = target_dir / "02_SUROWE_OFERTY_I_WIADOMOSCI_ZLECENIE_144890.json"
with open(raw_dst, "w", encoding="utf-8") as f:
    json.dump(combined_market_survey, f, ensure_ascii=False, indent=2)
print(f"  -> Zapisano surowe oferty i wiadomości: {raw_dst.name} ({raw_dst.stat().st_size} bajtów)")

# 4. Budowa zunifikowanej bazy wygranych i przegranych Ksawiera
print("\n4. Budowa zunifikowanej bazy ofert Ksawiera (56 wygranych + 16 przegranych)...")
won_src = base_dir / "badania" / "baza" / "ksawierpotrykus3" / "03_odpisane" / "wygrane_56.json"
lost_src = base_dir / "badania" / "baza" / "ksawierpotrykus3" / "02_przegrane" / "przegrane_16.json"

won_data = json.loads(won_src.read_text(encoding="utf-8"))
lost_data = json.loads(lost_src.read_text(encoding="utf-8"))

combined_history = {
    "opis": "Historia rzeczywistych ofert składanych przez Ksawiera na Useme (56 wygranych vs 16 przegranych)",
    "statystyki": {
        "liczba_wygranych": len(won_data),
        "liczba_przegranych": len(lost_data),
        "laczna_liczba_przebadanych_ofert": len(won_data) + len(lost_data)
    },
    "oferty_wygrane_56_sztuk": won_data,
    "oferty_przegrane_16_sztuk": lost_data
}

history_dst = target_dir / "03_HISTORIA_56_WYGRANYCH_I_16_PRZEGRANYCH_OFERT_KSAWIERA.json"
with open(history_dst, "w", encoding="utf-8") as f:
    json.dump(combined_history, f, ensure_ascii=False, indent=2)
print(f"  -> Zapisano historię wygranych/przegranych: {history_dst.name} ({history_dst.stat().st_size} bajtów)")

# 5. Strukturalna analiza cech konkurencji
print("\n5. Kopiowanie analizy cech konkurencji...")
# TODO: brak pliku analiza_gleboka_ofert.json; najblizej: badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/analiza_cech_konkurencji.json
features_src = base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "analiza_cech_konkurencji.json"
features_dst = target_dir / "04_STRUKTURALNA_ANALIZA_CECH_KONKURENCJI.json"
shutil.copy2(features_src, features_dst)
print(f"  -> Zapisano analizę cech: {features_dst.name} ({features_dst.stat().st_size} bajtów)")

# 6. Przygotowanie instrukcji i gotowego promptu dla Claude
print("\n6. Generowanie instrukcji i promptu dla AI...")
prompt_md = target_dir / "00_INSTRUKCJA_I_PROMPT_DLA_AI.md"
prompt_txt = target_dir / "PROMPT_DLA_CLAUDE.txt"

prompt_content = """# INSTRUKCJA I ZAAWANSOWANY PROMPT STRATEGICZNY DLA CLAUDE 3.5 SONNET

Ten folder zawiera **WSZYSTKIE** dane empiryczne, analizy psychologiczne, case studies, 30 ofert publicznych oraz 4 wątki prywatnych wiadomości od seniorów z polskiego Useme.

---

## JAK SKORZYSTAĆ W CLAUDE (CLAUDE.AI):
1. Otwórz nową rozmowę w [Claude.ai](https://claude.ai/new) (zalecany model: **Claude 3.5 Sonnet**).
2. Przeciągnij i upuść do okna czatu dokładnie poniższe **4 pliki danych** (wszystkie 4 mieszczą się w limicie 5 plików Claude):
   - `01_KOMPLETNA_WIEDZA_STRATEGICZNA_I_LORE.md` (zintegrowane kompendium wiedzy, psychologii, portfolio i raportu z wiadomości)
   - `02_SUROWE_OFERTY_I_WIADOMOSCI_ZLECENIE_144890.json` (30 pełnych ofert konkurencji + 4 pełne wątki prywatnych wiadomości od seniorów)
   - `03_HISTORIA_56_WYGRANYCH_I_16_PRZEGRANYCH_OFERT_KSAWIERA.json` (twarde dane: 56 wygranych i 16 przegranych ofert Ksawiera ze stawkami do 34k PLN)
   - `04_STRUKTURALNA_ANALIZA_CECH_KONKURENCJI.json` (matryca technologiczna, cenowa i SLA konkurencji)
3. Skopiuj poniższy **PROMPT DLA CLAUDE** i wklej go jako treść wiadomości.

---

### TREŚĆ PROMPTU DO SKOPIOWANIA DO CLAUDE:

```text
Jesteś elitarnym doradcą strategicznym B2B, architektem sprzedaży usług technologicznych oraz bezwzględnym analitykiem teorii gier na platformach freelancerskich.

Otrzymujesz 4 kompletne pliki z danymi empirycznymi z polskiej platformy Useme:
1. `01_KOMPLETNA_WIEDZA_STRATEGICZNA_I_LORE.md` – pełny profil Ksawiera Potrykusa, audyt 551 zleceń, psychologia konwersji, 9 archetypów klientów, zasady zamykania, 9 technicznych case studies B2B, audyty Red Team oraz raport z prywatnych wiadomości od seniorów.
2. `02_SUROWE_OFERTY_I_WIADOMOSCI_ZLECENIE_144890.json` – pełne, surowe teksty 30 ofert konkurencji ORAZ 4 pełne wątki prywatnych wiadomości zebranych w ramach zlecenia badawczego #144890 („Automatyzacja obiegu faktur i dokumentów kosztowych”).
3. `03_HISTORIA_56_WYGRANYCH_I_16_PRZEGRANYCH_OFERT_KSAWIERA.json` – baza 56 zleceń wygranych przez Ksawiera (z realnymi stawkami od 300 zł do 34 000 zł i pełnymi treściami ofert) oraz 16 zleceń przegranych.
4. `04_STRUKTURALNA_ANALIZA_CECH_KONKURENCJI.json` – algorytmiczna ekstrakcja cech 30 konkurentów (stack technologiczny, widełki cenowe 500 zł - 36k zł, gwarancje, retainery, błędy architektoniczne).

### KLUCZOWE ODKRYCIE ZLECONEGO BADANIA:
Gdy wystawiliśmy zlecenie #144890, zalała nas fala 30 publicznych ofert, ale jednocześnie 4 doświadczonych wykonawców (Adam K, Kamil Wojtulewicz, Konrad Szydłowski, Adam Wolski) w ogóle NIE ZŁOŻYŁO oferty publicznej, tylko napisało prywatne wiadomości, wskazując kluczowe problemy:
1. Różnice zaokrągleń VAT o 1 grosz między pozycjami a sumą faktury (Adam K).
2. Deduplikację faktur wpadających różnymi drogami (skan + mail) po NIP i nr dokumentu (Adam K).
3. Bezsensowność OCR-owania polskich faktur VAT w dobie KSeF (Konrad Szydłowski, Adam K) – pobieranie czystego XML prosto z KSeF, a OCR tylko na WZ i zamówienia.
4. Odmowę strzelania ceną w ciemno bez próbki dokumentów i testu formatu wymiany Optimy (Adam Wolski, Kamil Wojtulewicz).

Natomiast 30 ofert publicznych to w 90% generyczny spam: rzucanie n8n, korposlogany („chętnie pomogę”, „bezpłatna konsultacja”) i ściganie się na dno (500-1500 zł) lub bezpodstawne 15 000 - 18 000 zł.

### NASZ DYLEMAT I GŁÓWNY CEL:
Moja intuicja mówi mi: **NIE WOLNO ICH KOPIOWAĆ. Kopiowanie konkurencji to ściganie się na dno i bycie 31. generycznym botem.**
Chcę wykazać się czymś **FUNDAMENTALNIE INNYM (Contrarian Strategy)**. Chcę połączyć strategiczną merytorykę seniorów (którzy pisali na priv) z magnetyczną, bezkonkurencyjną ofertą publiczną na Useme.

Moim celem jest wygrywanie intratnych zleceń o budżetach 3 000 zł – 25 000 zł (zwłaszcza integracje ERP, automatyzacje procesów, backendy, API, systemy dedykowane) przy zachowaniu wysokich stawek i natychmiastowego budowania zaufania decydenta.

### TWOJE ZADANIE – PRZEPROWADŹ GŁĘBOKĄ ANALIZĘ I ODPOWIEDZ W 5 SEKWENCJACH:

#### 1. SEKCJA 1: ANATOMIA RYNKOWEGO STADA VS STRATEGIA PRYWATNYCH WIADOMOŚCI
- Porównaj zachowanie 30 oferentów publicznych z 4 wykonawcami piszącymi na priv. Dlaczego seniorzy unikają składania ofert publicznych i jakie są tego wady i zalety na Useme?
- Dlaczego 26 z 30 ofert publicznych to śmieci i gdzie leży „Błękitny Ocean” (Blue Ocean) na Useme?

#### 2. SEKCJA 2: DEKONSTRUKCJA 56 WYGRANYCH OFERT KSAWIERA
- Przeanalizuj zbiór 56 wygranych ofert Ksawiera (z pliku `03_HISTORIA_...`).
- Jakie schematy, zwroty i struktury w dotychczasowych ofertach Ksawiera przynosiły najwyższą konwersję i największe kwoty (np. zlecenia po 8,5k, 10k, 34k PLN)?
- Zestaw to z 16 przegranymi ofertami: w jakie pułapki Ksawier wpadał, gdy oferta była odrzucana?

#### 3. SEKCJA 3: STRATEGIA WYRÓŻNIENIA (CONTRARIAN PLAYBOOK – CZYM SIĘ WYKAZAĆ?)
- W jaki sposób Ksawier może wybić się z tłumu 30 ofert, bazując na swoim realnym zapleczu (patrz Moduł 9: Portfolio 9 projektów, inżynieria odwrotna, integracje ERP Comarch/Subiekt/Symfonia, boty, systemy kolejkowania)?
- Jak zaadresować obawy techniczne (KSeF, błędy groszowe VAT, spójność bazy Optimy) bezpośrednio w publicznej ofercie, sprawiając, że konkurencja wygląda przy nas jak amatorzy?
- Jak zaprojektować natychmiastowy „Dowód Kompetencji” (Proof of Concept w ofercie), który zdejmuje z klienta konieczność wielogodzinnych calli?
- Jak ustalić cenę: sztywna kwota, widełki, czy model dwufazowy (faza 1: MVP/rdzeń, faza 2: SLA)?

#### 4. SEKCJA 4: NOWY WZORZEC PRZEŁOMOWEJ OFERTY (SZABLON OPERACYJNY)
- Zaprojektuj modularny szkielet nowej oferty B2B na Useme (od pierwszego hooka, przez diagnozę ryzyka klienta, twardy dowód wdrożenia, po beztarciowe CTA).
- Sformułuj konkretne zasady: czego NIGDY nie pisać, a co MUSI znaleźć się w pierwszych 3 linijkach oferty.

#### 5. SEKCJA 5: WZORCOWA OFERTA DLA ZLECENIA #144890 (BENCHMARK)
- Napisz gotową, bezbłędną ofertę 1:1, którą Ksawier mógłby złożyć na zleceniu #144890, deklasującą wszystkie 30 ofert konkurentów i deklasującą wiadomości na priv, łączącą wiedzę o KSeF, zaokrągleniach VAT i integracji Optimy w jeden bezapelacyjny kontrakt.

Pisz konkretnie, dosadnie, bez lania wody i bez akademickiego żargonu. Skup się wyłącznie na maksymalizacji konwersji i psychologii decydenta B2B.
```
"""

prompt_md.write_text(prompt_content, encoding="utf-8")
prompt_txt.write_text(prompt_content, encoding="utf-8")
print(f"  -> Zapisano pliki promptu: {prompt_md.name} i {prompt_txt.name}")

print("\nWSZYSTKIE PLIKI ZOSTAŁY POMYŚLNIE ZAKTUALIZOWANE W:")
print(f"  {target_dir}")
