# -*- coding: utf-8 -*-
"""
Łańcuch Ekstrakcji Zagrywek, Taktyk, Języka, Stylu i Psychologii z 100 tekstów (#144890:
85 ofert publicznych + 13 wątków PV + 2 nasze poprzednie oferty jako KANDYDAT #25 i KANDYDAT #58).

ZASADA: Całkowicie ignorujemy samą wycenę (kwoty) oraz surową wiedzę merytoryczną (kto wymienił więcej skrótów IT).
Oceniamy i wyciągamy WYŁĄCZNIE:
1. JĘZYK I STYL PISANIA (naturalność, rytm, obrazowość, brak sztywnego tonu AI/telegramu, sposób tłumaczenia).
2. ZAGRYWKI I TAKTYKI PSYCHOLOGICZNE (linki do prototypów/artefaktów, gwarancje 30 dni / 12 mies., mikro-przykłady z życia firmy,
   taktyczna pokora / mówienie o granicach, zdjęcie ryzyka, etapowanie, sposób zaczepienia klienta).
3. ŚLEPY RANKING NAJLEPSZYCH OFERT (w tym naszych dwóch poprzednich: KANDYDAT #25 i KANDYDAT #58)
   ocenianych WYŁĄCZNIE pod kątem JĘZYKA, STYLU, LUDZKOŚCI I PSYCHOLOGII ZAUFANIA (0 pkt za cenę, 0 pkt za suche hasła techniczne!).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

from chain_executor import DEEPSEEK_MODEL, call_deepseek
from run_slepy_test_144890 import build_blind_pool, OUT_DIR, ZLECENIE_DIR


SYSTEM_PSYCHOLOGY_HUNTER = """Jesteś wybitnym analitykiem psychologii sprzedaży B2B, copywritingu konwersyjnego i lingwistyki perswazyjnej.
Przeszukujesz prawdziwe oferty i wiadomości prywatne (PV) wysłane do właściciela firmy na Useme.

TWOJA ŻELAZNA ZASADA OCENY:
1. CAŁKOWICIE IGNORUJESZ WYCENĘ (niska czy wysoka cena daje 0 punktów).
2. CAŁKOWICIE IGNORUJESZ SUROWĄ MERYTORYKĘ TECHNICZNĄ (samo rzucanie mądrych skrótów typu XML FA(3), ODBC, REST API, Docker, n8n, KSeF NIE daje punktów, jeśli jest napisane sucho jak instrukcja lub telegram!).
3. Oceniasz i wyławiasz WYŁĄCZNIE:
   - **JĘZYK I STYL PISANIA**: Kto pisze jak żywy, mądry człowiek przy kawie, a kto jak korpo-szablon albo skompresowany telegram z AI? Jakie konstrukcje zdaniowe sprawiają, że nietechniczny właściciel firmy od razu rozumie i czuje ulgę?
   - **KONKRETNE ZAGRYWKI I TAKTYKI (Tricki sprzedażowe i budujące zaufanie)**:
     * Obrazowe mikro-scenariusze z życia klienta (np. konkretny przykład nazwy towaru albo konkretny przykład błędu na fakturze),
     * Linki-przynęty (np. link do klikalnego prototypu/artefaktu przygotowanego pod to zlecenie, link do konkretnego case study lub repo),
     * Taktyczna szczerość / pokora (przyznanie wprost, czego się nie robiło albo czego AI nie potrafi odczytać, co paradoksalnie buduje 100% wiarygodności),
     * Gwarancje i odwrócenie ryzyka (np. 30 dni dostrajania na żywych dokumentach, 12 miesięcy naprawy błędów za darmo, płatność dopiero po odebraniu etapu, darmowy test na 3 skanach),
     * Sposób otwarcia (pierwsze 2 zdania) i sposób zamknięcia wiadomości (jak zachęcają do odpowiedzi bez nachalnego naganiania).
"""


def call_llm(sys_p: str, usr_p: str) -> str:
    for attempt in range(3):
        try:
            odp = call_deepseek(sys_p, usr_p, model=DEEPSEEK_MODEL, timeout=240)
            if odp:
                return odp
        except Exception as e:
            print(f"[WARN] Attempt {attempt+1} failed: {e}")
        time.sleep(5)
    raise RuntimeError("LLM call failed")


def format_text_only_candidates(candidates: list[dict]) -> str:
    blocks = []
    for c in candidates:
        blocks.append(
            f"==================================================\n"
            f"### {c['anon_id']} ({'Wiadomość PV' if 'PV' in c['channel'] else 'Oferta'})\n"
            f"{c['text']}\n"
        )
    return "\n".join(blocks)


def main():
    our_offer_file = ZLECENIE_DIR / "nasza_oferta_bot_v5_po_audycie.json"
    our_offer = json.loads(our_offer_file.read_text(encoding="utf-8"))
    pool, our_nums = build_blind_pool(our_offer)

    print(f"=== START ANALIZY JĘZYKA, STYLU I ZAGRYWEK NA {len(pool)} KANDYDATACH ===")
    print(f"Nasze zanonimizowane oferty w puli to: KANDYDAT #{our_nums[0]} (wariant prosty) i KANDYDAT #{our_nums[1]} (wariant główny)")

    batches = [
        ("CZĘŚĆ 1 (Kandydaci #1 – #33)", pool[0:33]),
        ("CZĘŚĆ 2 (Kandydaci #34 – #66)", pool[33:66]),
        ("CZĘŚĆ 3 (Kandydaci #67 – #100, w tym wiadomości PV)", pool[66:]),
    ]

    batch_findings = []
    top_style_ids = []

    for b_name, b_items in batches:
        print(f"\n>>> Przeszukuję {b_name} pod kątem zagrywek, języka i psychologii...")
        prompt = f"""Przeanalizuj poniższe {len(b_items)} wiadomości z {b_name}.
PAMIĘTAJ: Ignoruj cenę i ignoruj suche wymienianie technologii. Szukasz WYŁĄCZNIE mistrzostwa w JĘZYKU, STYLU, PSYCHOLOGII ZAUFANIA i SPRYTNYCH ZAGRYWKACH.

Zadanie:
1. **Wyłów wszystkie genialne ZAGRYWKI, TAKTYKI i ZWROTY JĘZYKOWE** z tej grupy (podaj `KANDYDAT #X` + dokładny cytat z tekstu + wyjaśnienie, dlaczego ten zabieg działa psychologicznie na klienta). Szukaj m.in.:
   - Zdań, które tłumaczą trudną rzecz niezwykle prostym, ludzkim językiem,
   - Mikro-przykładów z życia (gdzie klient widzi obraz w głowie),
   - Zagrywek z linkami / prototypami / próbkami / gwarancjami / etapowaniem,
   - Zagrywek z „taktyczną szczerością” (mówienie o ograniczeniach, co buduje zaufanie),
   - Świetnych otwarć i zakończeń.
2. **Wskaż anty-wzorce stylu i języka** (w tym gdzie tekst brzmi jak zimny telegram, ściana skrótów albo pusty marketing).
3. **Wybierz 6 kandydatów z tej grupy, którzy mają NAJLEPSZY JĘZYK, STYL I PSYCHOLOGIĘ** (niezależnie od ceny i liczby terminów technicznych) i podaj ich na końcu w JSON:
```json
{{"top6_style": ["KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #..."]}}
```

OTO TEKSTY:
{format_text_only_candidates(b_items)}
"""
        resp = call_llm(SYSTEM_PSYCHOLOGY_HUNTER, prompt)
        batch_findings.append((b_name, resp))
        m_json = re.search(r'\{\s*"top6_style"\s*:\s*\[(.*?)\]\s*\}', resp, re.DOTALL)
        extracted = []
        if m_json:
            extracted = re.findall(r"KANDYDAT\s*#\d+", m_json.group(1))
        if not extracted:
            extracted = list(dict.fromkeys(re.findall(r"KANDYDAT\s*#\d+", resp)))[:6]
        print(f"    Najlepsi stylowo/psychologicznie z {b_name}: {extracted}")
        for cid in extracted:
            norm = re.sub(r"\s+", " ", cid.strip().upper())
            if norm not in top_style_ids:
                top_style_ids.append(norm)

    # Upewnijmy się, że w wielkim porównaniu stylu i psychologii są wszyscy wyłonieni + nasze 2 oferty (#25 i #58),
    # żeby oceniający porównał je bezpośrednio pod kątem samego języka i psychologii (nadal bez wiedzy, że są nasze!)
    for onum in our_nums:
        kc = f"KANDYDAT #{onum}"
        if kc not in top_style_ids:
            top_style_ids.append(kc)

    pool_by_id = {c["anon_id"]: c for c in pool}
    finalists = [pool_by_id[cid] for cid in top_style_ids if cid in pool_by_id]

    print(f"\n>>> Finałowa synteza wszystkich zagrywek i ocena {len(finalists)} kandydatów wyłącznie po JĘZYKU, STYLU i PSYCHOLOGII...")

    all_findings_text = "\n\n".join(f"### ZNALEZISKA Z {bn}:\n{bf}" for bn, bf in batch_findings)

    master_prompt = f"""Masz przed sobą:
1. Zbiór wszystkich wyłowionych zagrywek, taktyk i zwrotów językowych z całej setki ofert i wiadomości PV,
2. Pełne teksty {len(finalists)} finalistów (wśród nich są zarówno oferty publiczne, jak i wiadomości z PV).

PAMIĘTAJ O ZASADZIE:
Oceniasz **ZERO za cenę** i **ZERO za samo napakowanie trudnymi hasłami merytorycznymi/technicznymi**!
Oceniasz **100% za JĘZYK, STYL PISANIA, LUDZKOŚĆ, PSYCHOLOGIĘ ZAUFANIA i SPRYTNE ZAGRYWKI SPRZEDAŻOWE**!

Wykonaj 3 zadania:

### ZADANIE 1: WIELKA KSIĘGA ZAGRYWEK I JĘZYKA (Co musimy ukraść do naszej ofertowarki?)
Wyodrębnij i pogrupuj **wszystkie najlepsze zagrywki, taktyki i konstrukcje językowe** ze wszystkich części. Dla każdej zagrywki podaj:
- **Nazwę zagrywki / taktyki**,
- **Dokładny cytat z oferty (i od którego KANDYDATA pochodzi)**,
- **Dlaczego to działa na mózg klienta (psychologia)**,
- **Jak możemy użyć tej samej zagrywki w uniwersalnym szablonie naszej ofertowarki**.
Uwzględnij osobno:
1. *Język i tłumaczenie („jak Antoni / Dominik / Adam K”)* — jak zamieniają żargon na ludzki obraz,
2. *Mikro-przykłady z życia firmy* — jak jedno zdanie z przykładem robi większą robotę niż 10 skrótów IT,
3. *Artefakty, linki, prototypy i próbki przed umową*,
4. *Gwarancje, 30 dni, 12 miesięcy, etapowanie, odwracanie ryzyka*,
5. *Taktyczna szczerość / mówienie o ograniczeniach (dlaczego przyznanie się do słabości buduje zaufanie)*,
6. *Otwarcia (pierwsze 2 zdania) i zakończenia (CTA)*.

### ZADANIE 2: RANKING TOP 12 WYŁĄCZNIE POD WZGLĘDEM JĘZYKA, STYLU I PSYCHOLOGII (0% za cenę, 0% za suchą merytorykę!)
Ułóż ranking najlepszych ofert spośród poniższych finalistów, oceniając **tylko to, jak są napisane, jak budują relację, jak dobrze się je czyta i jak sprytnie rozgrywają klienta psychologicznie**.

### ZADANIE 3: SZCZEGÓŁOWA OCENA STYLU I PSYCHOLOGII KAŻDEGO Z FINALISTÓW (w tym dokładnie oceń każdy z {len(finalists)} tekstów po kolei!)
Dla każdego kandydata z listy finalistów napisz:
- **Ocena stylu i psychologii (1-100 pkt)**,
- **Co w jego JĘZYKU i ZAGRYWKACH jest genialne**,
- **Co w jego JĘZYKU i STYLU kuleje** (np. czy brzmi jak zimny telegram, czy ma za dużo skrótów w jednym zdaniu, czy brzmi jak AI, czy brakuje mu ludzkiego ciepła i obrazowości).

---
ZNALEZISKA Z PRZESZUKANIA CAŁEJ SETKI:
{all_findings_text}

---
PEŁNE TEKSTY FINALISTÓW DO OCENY STYLU I PSYCHOLOGII:
{format_text_only_candidates(finalists)}
"""
    master_report = call_llm(SYSTEM_PSYCHOLOGY_HUNTER, master_prompt)

    out_md = OUT_DIR / "RAPORT_ZAGRYWKI_JEZYK_PSYCHOLOGIA_100.md"
    legend_lines = [
        "# WIELKI AUDYT JĘZYKA, STYLU, PSYCHOLOGII I ZAGRYWEK (100 OFERT I WIADOMOŚCI PV — #144890)\n",
        "## Mapa rozszyfrowująca kandydatów w finale stylu i psychologii:\n",
        "| ID w ślepym teście | Kto to naprawdę? | Kanał |",
        "|---|---|---|",
    ]
    for f in finalists:
        bold = "**" if f["is_ours"] else ""
        legend_lines.append(f"| {bold}{f['anon_id']}{bold} | {bold}{f['real_author']}{bold} | {f['channel']} |")

    legend_lines.append("\n---\n")
    legend_lines.append(master_report)
    legend_lines.append("\n\n---\n## Surowe notatki z 3 koszyków (100 ofert i PV)\n")
    for bn, bf in batch_findings:
        legend_lines.append(f"### {bn}\n\n{bf}\n\n---\n")

    out_md.write_text("\n".join(legend_lines), encoding="utf-8")
    print(f"\n[GOTOWE] Zapisano pełny raport do: {out_md}")


if __name__ == "__main__":
    main()
