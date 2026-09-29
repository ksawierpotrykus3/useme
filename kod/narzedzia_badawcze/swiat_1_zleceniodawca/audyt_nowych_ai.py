# -*- coding: utf-8 -*-
"""
ŚWIAT 1 (ZLECENIODAWCA / MYSTERY SHOPPING - #144890):
Przyrostowy Audyt AI nowych ofert publicznych (+16 ofert: #2893397..#2896662)
oraz nowych wątków wiadomości prywatnych (+5 wątków PV) przez lokalny serwer
DeepSeek Proxy (`http://127.0.0.1:4571`).

Wykonuje 2 badania na nowych danych i konfrontuje je z dotychczasowym Top 10:
1. ŚLEPY SĘDZIA KLIENTA (Właściciel firmy handlowo-produkcyjnej):
   - Ocenia wszystkie 16 nowych ofert i 5 nowych wątków PV w skali 1-100,
   - Sprawdza, czy którakolwiek z nowych propozycji przebija dotychczasowych liderów
     (nasz wariant v6, Adam K, Antoni, Dominik Groński, ailone, krzysztof-wasiucionek),
   - Weryfikuje aktualność wniosków z `RAPORT_SLEPY_TEST_144890_Z_PV.md`.
2. ŁOWCA ZAGRYWEK, JĘZYKA I PSYCHOLOGII (`SYSTEM_PSYCHOLOGY_HUNTER`):
   - Wyławia nowe zagrywki sprzedażowe, konstrukcje językowe i anty-wzorce z 21 nowych tekstów,
   - Weryfikuje i wzbogaca `RAPORT_ZAGRYWKI_JEZYK_PSYCHOLOGIA_100.md`.
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

ZLECENIE_DIR = (
    BASE_DIR
    / "badania"
    / "baza"
    / "weronikabuchholc13"
    / "04_moje_zlecenia"
    / "zlecenie_testowe_144890"
)
AUDYT_DIR = BASE_DIR / "badania" / "audyt_100"

PREV_MAX_OFFER_ID = 2892469
PREV_THREAD_IDS = {
    "1963946", "1963840", "1963653", "1963512", "1963409",
    "1963315", "1963291", "1963259", "1963208", "1963195",
    "1963190", "1963167", "1963156", "1963153"
}


def call_llm(sys_p: str, usr_p: str, model: str = DEEPSEEK_MODEL) -> str:
    for attempt in range(3):
        try:
            resp = call_deepseek(sys_p, usr_p, model=model, timeout=300)
            if resp:
                return resp
        except Exception as e:
            print(f"[WARN] Próba {attempt+1} nieudana: {e}")
        time.sleep(4)
    raise RuntimeError("Błąd wywołania modelu DeepSeek na porcie 4571.")


def main() -> None:
    offers = json.loads((ZLECENIE_DIR / "oferty_publiczne_30.json").read_text(encoding="utf-8"))
    pv_threads = json.loads((ZLECENIE_DIR / "wiadomosci_zleceniodawcy_pelne.json").read_text(encoding="utf-8"))

    new_offers = [o for o in offers if int(o["offer_id"]) > PREV_MAX_OFFER_ID]
    new_pvs = [t for t in pv_threads if int(t.get("thread_id") or t.get("thread_pk") or 0) > 1963946]

    print(f"=== AUDYT AI NOWYCH DANYCH #144890: {len(new_offers)} nowych ofert + {len(new_pvs)} nowych wątków PV ===")

    blocks = []
    for idx, o in enumerate(new_offers, 1):
        blocks.append(
            f"### NOWA OFERTA #{idx} (ID: #{o.get('offer_id')} | Autor: {o.get('author_name')} | Umowy: {o.get('author_contracts')} "
            f"| Cena: {o.get('price')} | Czas: {o.get('days')} | Data: {o.get('published_at') or o.get('published')})\n"
            f"{o.get('proposal_text')}\n"
        )

    for idx, t in enumerate(new_pvs, 1):
        tid = str(t.get("thread_id") or t.get("thread_pk"))
        msgs = "\n\n".join(f"[{m.get('sender') or m.get('sender_name') or t.get('author_name')} ({m.get('date')})]:\n{m.get('text')}" for m in t.get("messages", []))
        status = (
            f"Złożył też ofertę #{t['matched_offer_id']} ({t['matched_offer_price']})"
            if t.get("has_submitted_offer")
            else "TYLKO PRIV (brak oferty w formularzu)"
        )
        blocks.append(
            f"### NOWY WĄTEK PRIV #{idx} (Wątek: {tid} | Autor: {t['author_name']} | Status: {status})\n"
            f"{msgs}\n"
        )

    combined_new_text = "\n" + ("=" * 70 + "\n").join(blocks)

    # 1. Ocena oczami Klienta + Konfrontacja z dotychczasowym Top 10
    sys_client = """Jesteś właścicielem firmy handlowo-produkcyjnej w Polsce (nietechnicznym przedsiębiorcą z budżetem 5 000 - 15 000 zł netto) oraz głównym audytorem projektu #144890 („Automatyzacja obiegu faktur i dokumentów kosztowych” do Comarch Optima z n8n i OCR/AI).
Wcześniej przebadałeś 85 ofert publicznych i 14 wątków prywatnych (PV). Dotychczasową czołówkę stanowili:
- Nasza oferta v6 (7200 zł, ludzki język, 3 etapy, darmowy test na 3 skanach, XML do bufora Optimy, KSeF),
- Adam K [PV] (~8000 zł, świetny prosty język i rozbicie kosztów, choć pomylił Sferę z Insertem),
- Antoni (#2891755, 8610 zł, genialny język ludzki i prototyp, ale ryzykowny bezpośredni zapis do SQL Optimy),
- Dominik Groński GroDev [PV] (9500 zł, perfekcyjna wiedza o Pracy Rozproszonej XML i licencjach Comarch),
- ailone (#2889525, 10500 zł, świetna uwaga o KSeF, duplikatach NIP+nr i groszowych zaokrągleniach VAT),
- krzysztof-wasiucionek (#2892469, 9000 zł, KSeF + certyfikat NVIDIA + lokalny/chmurowy model AI).

Teraz spłynęło 16 NOWYCH ofert publicznych (#2893397..#2896662) oraz 5 NOWYCH wątków prywatnych (PV)."""

    prompt_client = f"""Przeanalizuj dokładnie wszystkie **16 nowych ofert publicznych** oraz **5 nowych wątków prywatnych (PV)**, które spłynęły do zlecenia #144890 przed jego zamknięciem.

Wykonaj 4 konkretne zadania:

1. **TABELA OCEN WSZYSTKICH 16 NOWYCH OFERT I 5 NOWYCH WĄTKÓW PV (Skala 1–100 pkt oczami klienta)**:
   - Dla każdej z 16 ofert i 5 wiadomości PV podaj: ID/Autora, Cenę, Ocenę (1-100 pkt), Werdykt (Odrzut / Średniak / Półfinał / Finał) oraz krótkie uzasadnienie (co zrobił świetnie, a na czym poległ).

2. **CZY KTÓRAKOLWIEK Z NOWYCH OFERT WCHODZI DO TOP 10 CAŁEGO ZLECENIA (101 OFERT + 19 PV)?**
   - Przeanalizuj szczególnie najmocniejszych nowych graczy (m.in. `natalia-szczepanik` #2895200, `tomaszmyszak` / cerbIT #2896654, `michal-trzaskoma` #2894558, `arkadiusz-koszewski` #2894760 + PV, `bartlomiej-drezek` #2895043, `repulse-tomasz-kadziela` #2893397, oraz nowe wątki PV: `HubertS`, `Rafał Bagrowski`, follow-up `Kamil Duś`, `AG Software`).
   - Wskaż dokładnie, które miejsce w zaktualizowanym rankingu całej puli (112 wykonawców) zajmują najlepsi z nowej szesnastki i czy nasza oferta v6 nadal utrzymuje pozycję #1 / Top 2.

3. **NOWE ZAGRYWKI, TRICKI PSYCHOLOGICZNE I KONSTRUKCJE JĘZYKOWE (Co nowego rzucają te oferty?)**:
   - Wyłów wszystkie nowe, wcześniej niespotykane zagrywki sprzedażowe i techniczne z tych 21 zgłoszeń (np. sekcja „Czego NIE będę automatyzować” u Natalii Szczepanik, hybryda gotowego systemu CerbOffice + OptimaAgent u Tomasza Myszaka, pułapka rozbieżności ceny w tabeli 6200 zł vs 13 600 zł w treści, follow-up Kamila Dusia na PV przed zamknięciem zlecenia, propozycja Comarch BPM za 100 zł u lukasheek88 itd.).
   - Oceń, które z tych zagrywek warto zaadaptować do naszej bazy wiedzy, a które są błędem lub anty-wzorcem.

4. **WERYFIKACJA DOTYCHCZASOWYCH PRAW RYNKOWYCH**:
   - Czy po wzroście puli z 85 do 101 ofert i z 14 do 19 wątków PV nasze dotychczasowe wnioski (o cenach, o KSeF, o XML vs SQL w Optimie, o przewadze ludzkiego stylu nad szablonem AI, o sile kanału PV) są nadal w 100% aktualne i prawdziwe, czy coś uległo zmianie?

OTO PEŁNE TREŚCI 16 NOWYCH OFERT I 5 NOWYCH WĄTKÓW PV:
{combined_new_text}
"""

    print(">>> Wysyłam zapytanie do DeepSeek (ocena 16 nowych ofert + 5 nowych PV)...")
    report_md = call_llm(sys_client, prompt_client)

    out_json = AUDYT_DIR / "wyniki_audytu_nowych_16_ofert_5_pv_144890.json"
    out_md = AUDYT_DIR / "RAPORT_NOWE_OFERTY_I_PV_144890_AKTUALIZACJA.md"

    payload = {
        "audited_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "new_offers_count": len(new_offers),
        "new_pv_count": len(new_pvs),
        "new_offer_ids": [o["offer_id"] for o in new_offers],
        "new_pv_thread_ids": [str(t.get("thread_id") or t.get("thread_pk")) for t in new_pvs],
        "report_markdown": report_md,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(
        f"# AUDYT AI NOWYCH OFERT (+16) I WIADOMOŚCI PRIV (+5) — ZLECENIE #144890 (STAN KOŃCOWY: 101 OFERT + 19 PV)\n\n"
        f"- **Data audytu:** `{payload['audited_at']}`\n"
        f"- **Przebadane nowe oferty publiczne (16):** `{', '.join('#' + x for x in payload['new_offer_ids'])}`\n"
        f"- **Przebadane nowe wątki PV (5):** `{', '.join(payload['new_pv_thread_ids'])}`\n\n---\n\n"
        + report_md,
        encoding="utf-8",
    )
    print(f"[GOTOWE] Zapisano raport z audytu nowych ofert i PV do: {out_md}")


if __name__ == "__main__":
    main()
