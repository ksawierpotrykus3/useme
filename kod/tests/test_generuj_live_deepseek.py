# -*- coding: utf-8 -*-
"""Test generowania oferty na żywo przez lokalne DeepSeek Proxy (port 4571)
z nowym łańcuchem i zaktualizowanym manualem (jak_pisac_oferty, lore, wycena).

Porównuje nową ofertę z archiwalną starą ofertą zapisaną w magazynie (#144590).
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ai_pipeline import SlotChainAIPipeline
from storage import Storage

def main():
    job_file = ROOT_DIR / "magazyn" / "programowanie-i-it" / "144590.json"
    if not job_file.exists():
        print(f"BŁĄD: Nie znaleziono pliku {job_file}")
        return

    job_data = json.loads(job_file.read_text(encoding="utf-8"))
    job_id = job_data.get("id", "144590")
    print(f"--- TEST GENEROWANIA OFERTY DLA ZLECENIA #{job_id} ---")
    print(f"Tytuł: {job_data.get('title')}")
    print(f"Autor: {job_data.get('author')}")
    print(f"Budżet: {job_data.get('budget')}")
    
    stara_oferta = job_data.get("ai_proposal", {}).get("opis", "")
    print(f"\n[STARA OFERTA (PRZED REFORMĄ)]:\n{stara_oferta}\n")
    print("=" * 60)
    print("URUCHAMIAM ŁAŃCUCH AI Z NOWYMI PROMPTAMI I PROXY DEEPSEEK (PORT 4571)...")
    print("=" * 60)

    # Przygotowanie danych wejściowych
    job_detail = {
        "id": f"{job_id}-nowy-test",
        "title": job_data.get("title"),
        "author": job_data.get("author"),
        "author_id": job_data.get("author_id"),
        "budget": job_data.get("budget"),
        "category": job_data.get("category"),
        "full_description": job_data.get("full_details", {}).get("full_description", ""),
        "tier": "B",  # E-commerce developer / bieżące wdrożenia
    }

    # Wymuszenie czyszczenia ewentualnego starego checkpointu testowego
    from storage import clear_checkpoint
    clear_checkpoint(f"{job_id}-nowy-test")

    start_t = time.time()
    pipeline = SlotChainAIPipeline()
    
    try:
        wynik = pipeline.generate_proposal(job_detail)
        elapsed = time.time() - start_t
        print(f"\n[SUKCES] Generowanie zakończone w {elapsed:.1f}s!\n")
        print("=" * 60)
        print("[NOWA OFERTA (PO REFORMIE Z 22 WRZEŚNIA)]:")
        print(f"Wycena: {wynik.wycena} zł | Dni: {wynik.dni}")
        print("-" * 60)
        print(wynik.opis)
        print("-" * 60)
        
        # Zapisujemy porównanie do pliku testowego
        out_file = Path(__file__).parent.parent.parent / "badania" / f"porownanie_przed_po_{job_id}.md"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        porownanie_md = f"""# Porównanie Ofert: Przed vs Po Reformie (Zlecenie #{job_id})

**Tytuł:** {job_data.get('title')}  
**Zleceniodawca:** {job_data.get('author')}  
**Budżet:** {job_data.get('budget')}  

---

## 1. Stara Oferta (Przed Reformą – 18 września)
- **Wycena:** {job_data.get('ai_proposal', {}).get('wycena')} zł / {job_data.get('ai_proposal', {}).get('dni')} dni
- **Podpis:** Brak podpisu (tylko „Pozdrawiam”)
- **Stemple:** „Piszę w imieniu dwuosobowego zespołu”, „Zdzwońmy się na 15 minut”, belferskie pouczanie o lukach bezpieczeństwa.

```text
{stara_oferta}
```

---

## 2. Nowa Oferta (Po Reformie – DeepSeek Proxy)
- **Wycena:** {wynik.wycena} zł / {wynik.dni} dni
- **Podpis:** Osobisty podpis Ksawier
- **Charakterystyka:** Złota Zasada Ksawiera, brak formułek, sytuacyjne CTA.

```text
{wynik.opis}
```
"""
        out_file.write_text(porownanie_md, encoding="utf-8")
        print(f"\nZapisano pełne porównanie do: {out_file}")

    except Exception as e:
        print(f"\n[BŁĄD GENEROWANIA]: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
