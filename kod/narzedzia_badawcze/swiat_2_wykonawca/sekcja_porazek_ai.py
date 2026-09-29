# -*- coding: utf-8 -*-
"""
ŚWIAT 2 (WYKONAWCA / OFERTOWARKA - ksawierpotrykus3):
Sekcja Porażek AI (Failure Alchemy) dla nowo zamkniętych, nieodpisanych ofert
wysłanych z konta `ksawierpotrykus3` (zarówno z `01_ofertowarka`, jak i najnowszych
11 zamkniętych ofert w `02_przegrane`).

Używa lokalnego serwera DeepSeek Proxy (`http://127.0.0.1:4571`) do przeprowadzenia
bezlitosnej sekcji zwłok każdej z nowych przegranych ofert:
- Dlaczego klient nie odpisał? (Cena vs budżet, czas wejścia / liczba konkurentów,
  styl starego bota vs nowy styl, długość, brak haczyka lub błędy w treści),
- Jak wyglądała stara oferta (np. w zleceniach z 18-24 września) w porównaniu z obecnym
  standardem v6,
- Jakie wnioski płyną dla selekcji zleceń (Triage) i generatora ofert.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

from chain_executor import call_deepseek, DEEPSEEK_MODEL

KSAWIER_DIR = BASE_DIR / "badania" / "baza" / "ksawierpotrykus3"
ANALIZY_DIR = BASE_DIR / "badania" / "analizy"


def call_llm(sys_p: str, usr_p: str) -> str:
    for attempt in range(3):
        try:
            resp = call_deepseek(sys_p, usr_p, model=DEEPSEEK_MODEL, timeout=300)
            if resp:
                return resp
        except Exception as e:
            print(f"[WARN] Próba {attempt+1} nieudana: {e}")
        time.sleep(4)
    raise RuntimeError("Nie udało się wywołać DeepSeek na porcie 4571.")


def main() -> None:
    przegrane = json.loads((KSAWIER_DIR / "02_przegrane" / "przegrane_pelne_416.json").read_text(encoding="utf-8"))
    # 11 nowo pobranych zamkniętych ofert znajduje się na początku listy (indeksy 0..10)
    new_11 = przegrane[:11]

    # Dołączmy metadane z 01_ofertowarka (np. offers_count, data_wyslania), jeśli istnieją
    ofertowarka_by_closed_id = {}
    for jf in (KSAWIER_DIR / "01_ofertowarka").rglob("*.json"):
        if not jf.stem.isdigit() or any(p.startswith(".") for p in jf.parts):
            continue
        try:
            jd = json.loads(jf.read_text(encoding="utf-8"))
            cid = str(jd.get("closed_offer_id") or "")
            if cid:
                ofertowarka_by_closed_id[cid] = jd
        except Exception:
            pass

    cases_blocks = []
    for idx, rec in enumerate(new_11, 1):
        oid = str(rec.get("offer_id"))
        of_meta = ofertowarka_by_closed_id.get(oid, {})
        offers_cnt = of_meta.get("offers_count", "brak danych")
        sent_at = of_meta.get("data_wyslania", rec.get("published"))
        cases_blocks.append(
            f"### PRZYPADEK #{idx}: Oferta #{oid} — {rec.get('title')}\n"
            f"- **Klient:** `{rec.get('client')}` | **Kategoria:** `{rec.get('category')}`\n"
            f"- **Budżet klienta w ogłoszeniu:** `{rec.get('budget')}` | **Liczba konkurentów w momencie wysyłki:** `{offers_cnt}`\n"
            f"- **Nasza wycena:** `{rec.get('our_price')}` | **Nasz czas:** `{rec.get('our_days')}` | **Data:** `{sent_at}`\n\n"
            f"**Opis zlecenia klienta:**\n{rec.get('job_description')}\n\n"
            f"**Nasza wysłana oferta (która przegrała / pozostała bez odpowiedzi):**\n{rec.get('our_proposal')}\n"
        )

    all_cases_text = "\n" + ("=" * 70 + "\n").join(cases_blocks)

    sys_prompt = """Jesteś głównym analitykiem konwersji B2B i architektem systemu Ofertowarki Useme (metodologia Failure Alchemy).
Twoim zadaniem jest przeprowadzenie bezlitosnej sekcji zwłok 11 nowo zamkniętych (nieodpisanych / przegranych) ofert z konta `ksawierpotrykus3` (9 ofert wysłanych przez wcześniejsze iteracje bota w dniach 18-24 września 2026 oraz 2 starsze historyczne oferty).

Oceniasz każdy przypadek na podstawie twardych praw empirycznych z naszej bazy 481 zleceń oraz wniosków z mystery shoppingu (#144890):
1. Czy przyczyną porażki była **SELEKCJA / CZERWONY OCEAN** (np. WordPress/PrestaShop/strona wizytówka z 20-38 ofertami, gdzie nasz Win Rate wynosi <5%)?
2. Czy przyczyną była **PRZESTRZELONA WYCENA** względem budżetu klienta lub kotwicy cenowej?
3. Czy przyczyną był **STYL I KONSTRUKCJA OFERTY** (np. zimny, skrótowy „telegram inżynierski” ze starszej wersji bota v4/v5, nadmiar żargonu technicznego dla nietechnicznego klienta, brak ludzkiego języka, brak odwrócenia ryzyka / próbki, albo stara mała czcionka bez wielkich liter)?"""

    user_prompt = f"""Przeprowadź pełną sekcję zwłok poniższych **11 nowo zamkniętych ofert**, które właśnie spłynęły z powiadomień Useme jako zakończone bez wyboru naszej oferty (`ZAMKNIETE_NIEODPISANE`).

Wykonaj 3 zadania:

1. **TABELA DIAGNOSTYCZNA WSZYSTKICH 11 ZAMKNIĘTYCH OFERT**:
   - Dla każdej z 11 ofert podaj: ID oferty, Tytuł, Budżet klienta vs Nasza cena, Typ klienta i technologii, Główną przyczynę porażki (Triage / Cena / Styl oferty / Konkurencja) oraz prawdopodobieństwo, że w ogóle dało się to wygrać (0-100%).

2. **SZCZEGÓŁOWA SEKCJA ZWŁOK KAŻDEJ Z 9 OFERT BOTA (#2896427, #2892997, #2887326, #2887274, #2887209, #2868642, #2865617, #2865512, #2865458)**:
   - Wskaż dokładnie, jakiej generacji tekstu użył tam nasz bot (np. które oferty były jeszcze pisane zepsutym „telegramem inżynierskim” pełnym skrótów typu `100% deterministyczny kod`, `REST API`, `cron`, `brak halucynacji`, a które weszły w bagno WordPress/PrestaShop przy 25-38 konkurentach).
   - Pokaż na konkretnym cytacie z naszej oferty, w którym zdaniu klient stracił zainteresowanie lub poczuł, że czyta bota AI.

3. **WERYFIKACJA: CZY OBECNA WERSJA SYSTEMU (PO REFORMIE V6 I NOWYM TRIAGE) JUŻ ROZWIĄZUJE TE BŁĘDY, CZY TRZEBA COŚ DODAĆ?**
   - Oceń, które z tych 9 porażek zostałyby dziś automatycznie odfiltrowane lub napisane zupełnie inaczej przez nasz zaktualizowany styl v6 („mądry człowiek przy kawie”), a jakie **nowe wnioski** rzucają te zamknięte oferty (np. wycena małych skryptów Excel/VBA/Python z budżetem 1000 zł, oferty po angielsku jak Odoo ERP #2892997, czy strony dla medycyny estetycznej #2896427).

OTO PEŁNE DANE 11 NOWO ZAMKNIĘTYCH OFERT:
{all_cases_text}
"""

    print(">>> Wysyłam zapytanie do DeepSeek (Sekcja Porażek 11 nowo zamkniętych ofert)...")
    report_md = call_llm(sys_prompt, user_prompt)

    out_json = ANALIZY_DIR / "sekcja_porazek_ofertowarki.json"
    out_md = ANALIZY_DIR / "RAPORT_SEKCJA_PORAZEK_OFERTOWARKI.md"

    payload = {
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "analyzed_count": len(new_11),
        "offer_ids": [str(x.get("offer_id")) for x in new_11],
        "report_markdown": report_md,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(
        f"# SEKCJA PORAŻEK (FAILURE ALCHEMY) — 11 NOWO ZAMKNIĘTYCH OFERT (`ksawierpotrykus3`)\n\n"
        f"- **Data analizy:** `{payload['analyzed_at']}`\n"
        f"- **Przebadane zamknięte oferty (11):** `{', '.join('#' + x for x in payload['offer_ids'])}`\n\n---\n\n"
        + report_md,
        encoding="utf-8",
    )
    print(f"[GOTOWE] Zapisano raport Sekcji Porażek do: {out_md}")


if __name__ == "__main__":
    main()
