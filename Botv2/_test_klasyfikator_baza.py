# -*- coding: utf-8 -*-
"""Test klasyfikatora zlozonosci na PROBCE z calej bazy (nie 1 zlecenie).
Mierzy: stabilnosc klasy + korelacje z nasza realna cena."""
import json, random, re, time
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent / "mozg"))
from brain import call_ai

PROMPT = """Jesteś rygorystycznym audytorem technicznym oprogramowania.
Sklasyfikuj zlecenie do DOKŁADNIE JEDNEJ klasy złożoności (1-5) wg twardych reguł:

- Klasa 1: Poprawki, pojedynczy skrypt, prosty widok UI (1-3 dni).
- Klasa 2: CRUD, standardowe REST API z oficjalnym SDK (4-7 dni).
- Klasa 3: Własna logika biznesowa, przetwarzanie w tle, 2-3 standardowe API (8-14 dni).
- Klasa 4: Systemy krytyczne/transakcyjne, brak stabilnego SDK, idempotencja/kolejki, cudzy autorski kod (15-25 dni).
- Klasa 5: Pełny SaaS od zera, architektura rozproszona multi-tenant (26+ dni).

Zwróć WYŁĄCZNIE JSON:
{"klasa": int, "triggery": ["max 3 frazy"]}"""

# Zbierz zlecenia z opisem i cena
zlecenia = []
for p in ['badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne.json',
          'badania/baza/ksawierpotrykus3/03_odpisane/odpisane_zamkniete.json']:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    rek = d if isinstance(d, list) else d.get("oferty") or d.get("rekordy") or []
    for r in rek:
        opis = (r.get("job_description") or "").strip()
        c = r.get("our_price")
        if not opis or not c:
            continue
        m = re.search(r"(\d[\d\s]*)", str(c))
        if not m:
            continue
        v = int(m.group(1).replace(" ", ""))
        if 100 <= v <= 200000:
            zlecenia.append({"id": r.get("job_id") or r.get("offer_id"), "title": r.get("title", "")[:50],
                             "opis": opis, "cena": v})

print(f"=== BAZA: {len(zlecenia)} zlecen z opisem i cena ===\n")
random.seed(7)
probka = random.sample(zlecenia, min(20, len(zlecenia)))

print("=== PROBKA 20 ZLECEN (klasyfikacja 1x) ===\n")
wyniki = []
for z in probka:
    odp = call_ai(PROMPT, f"ZLECENIE:\n{z['opis'][:3000]}", temperature=0.0, max_tokens=300)
    m = re.search(r"\{.*\}", odp or "", re.DOTALL)
    klasa = "?"
    if m:
        try:
            klasa = json.loads(m.group(0)).get("klasa", "?")
        except Exception:
            pass
    wyniki.append((klasa, z["cena"], z["title"]))
    print(f"  klasa={klasa} | cena={z['cena']:>6} zl | {z['title']}")

# Korelacja klasa vs cena
print("\n=== SREDNIA CENA PER KLASA ===")
for k in range(1, 6):
    ceny = [c for kl, c, _ in wyniki if kl == k]
    if ceny:
        print(f"  klasa {k}: n={len(ceny)} | srednia cena {sum(ceny)//len(ceny)} zl")

# Stabilnosc: 3 zlecenia x 3 razy
print("\n=== STABILNOSC (3 zlecenia x 3 razy) ===")
for z in probka[:3]:
    klasy = []
    for _ in range(3):
        odp = call_ai(PROMPT, f"ZLECENIE:\n{z['opis'][:3000]}", temperature=0.0, max_tokens=300)
        m = re.search(r"\{.*\}", odp or "", re.DOTALL)
        if m:
            try:
                klasy.append(json.loads(m.group(0)).get("klasa"))
            except Exception:
                pass
    stab = "STABILNA" if len(set(klasy)) == 1 else f"PLYWA: {klasy}"
    print(f"  {z['title'][:45]} -> {stab}")
