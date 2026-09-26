# -*- coding: utf-8 -*-
"""Niezależny test sędziowski na modelach Gemini (przez gemini_proxy).

Modele:
1. gemini-3.8-flash
2. gemini-3.1-pro-thinking (z rozszerzonym myśleniem)
"""

import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LAB_SEDZIOWIE = Path(__file__).resolve().parent / "lab_niezalezni_sedziowie.py"

# Importuj kandydatów i treść zlecenia z lab_niezalezni_sedziowie.py
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab_niezalezni_sedziowie import ZLECENIE_OPIS, KANDYDACI

PROMPT_GEMINI = f"""Cześć! Wystawiłem na portalu Useme takie ogłoszenie o zleceniu:

\"\"\"
{ZLECENIE_OPIS}
\"\"\"

Dostałem 6 różnych odpowiedzi/ofert od programistów i agencji. Oto one:

============================================================
KANDYDAT A:
Wycena: {KANDYDACI['Kandydat A']['wycena']}
Treść:
{KANDYDACI['Kandydat A']['tekst']}

============================================================
KANDYDAT B:
Wycena: {KANDYDACI['Kandydat B']['wycena']}
Treść:
{KANDYDACI['Kandydat B']['tekst']}

============================================================
KANDYDAT C:
Wycena: {KANDYDACI['Kandydat C']['wycena']}
Treść:
{KANDYDACI['Kandydat C']['tekst']}

============================================================
KANDYDAT D:
Wycena: {KANDYDACI['Kandydat D']['wycena']}
Treść:
{KANDYDACI['Kandydat D']['tekst']}

============================================================
KANDYDAT E:
Wycena: {KANDYDACI['Kandydat E']['wycena']}
Treść:
{KANDYDACI['Kandydat E']['tekst']}

============================================================
KANDYDAT F:
Wycena: {KANDYDACI['Kandydat F']['wycena']}
Treść:
{KANDYDACI['Kandydat F']['tekst']}
============================================================

Jestem właścicielem firmy handlowo-produkcyjnej (nie jestem programistą). Chcę wybrać wykonawcę, który bezpiecznie dowiezie ten projekt i nie rozwali mi księgowości.

Odpowiedz mi po ludzku, bez korpomowy i prosto z mostu na 4 pytania:
1. Które oferty są Twoim zdaniem najlepsze i dlaczego?
2. Co myślisz o kandydatach, którzy zamiast pełnej oferty z ceną zadają mi tylko pytania (jak Kandydat E)? Czy są klienci, którzy tego oczekują i czy to dobra taktyka na Useme?
3. Czy jeśli oferta jest długa i szczegółowa (jak Kandydat A i B), to czy może to odrzucić klienta? W jakich sytuacjach i dla jakich klientów pisanie tak dużo to zaleta, a kiedy wada?
4. Kogo byś wybrał na moim miejscu? Ułóż ranking od 1 do 6 z krótkim podsumowaniem każdego kandydata.
"""

def call_gemini(model: str, prompt: str, timeout: int = 240) -> str:
    url = "http://127.0.0.1:8045/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"].get("content", "")

def run():
    out_dir = Path(__file__).resolve().parent
    report_file = out_dir / "RAPORT_GEMINI_SEDZIOWIE.md"
    json_file = out_dir / "wyniki_gemini_sedziowie.json"
    
    print("=" * 70)
    print("START: TEST SĘDZIOWSKI NA MODELACH GEMINI (3.8 FLASH & 3.1 PRO THINKING)")
    print("=" * 70)
    
    wyniki = {}
    
    # 1. Gemini 3.8 Flash
    print("\n[1/2] Odpytuję Gemini 3.8 Flash...", flush=True)
    try:
        resp_flash = call_gemini("gemini-3.8-flash", PROMPT_GEMINI)
        print("[OK] Gemini 3.8 Flash odpowiedział!", flush=True)
        wyniki["gemini_3_8_flash"] = resp_flash
    except Exception as e:
        print(f"[ERROR] Flash error: {e}", flush=True)
        wyniki["gemini_3_8_flash"] = f"Błąd: {e}"
        
    # 2. Gemini 3.1 Pro Thinking
    print("\n[2/2] Odpytuję Gemini 3.1 Pro Thinking (rozszerzone myślenie)...", flush=True)
    try:
        resp_pro = call_gemini("gemini-3.1-pro-thinking", PROMPT_GEMINI)
        print("[OK] Gemini 3.1 Pro Thinking odpowiedział!", flush=True)
        wyniki["gemini_3_1_pro_thinking"] = resp_pro
    except Exception as e:
        print(f"[ERROR] Pro Thinking error: {e}", flush=True)
        wyniki["gemini_3_1_pro_thinking"] = f"Błąd: {e}"
        
    # Zapis JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(wyniki, f, ensure_ascii=False, indent=2)
        
    # Zapis Markdown
    md_content = f"""# RAPORT SĘDZIOWSKI GEMINI (FLASH 3.8 & PRO 3.1 THINKING)
**Data badania:** 2026-09-26  
**Proxy:** http://127.0.0.1:8045 (gemini_proxy - sesja autoryzowana)  
**Zlecenie:** Automatyzacja obiegu dokumentów (#144890)  

---

## 1. OCENA GEMINI 3.8 FLASH
{wyniki.get('gemini_3_8_flash', 'Brak')}

---

## 2. OCENA GEMINI 3.1 PRO (ROZSZERZONE MYŚLENIE)
{wyniki.get('gemini_3_1_pro_thinking', 'Brak')}

---
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\n[SUKCES] Raport Gemini zapisany w: {report_file}")

if __name__ == "__main__":
    run()
