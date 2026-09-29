# -*- coding: utf-8 -*-
"""Narzędzie do podglądu i automatycznego eksportu raportów Audytora 100-punktowego do folderu."""

import json
import sys
from pathlib import Path

# UTF-8 w konsoli Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import config

MAGAZYN_DIR = config.MAGAZYN_DIR
AUDYTY_DIR = Path(__file__).resolve().parent.parent / "audyty"


def formatuj_audyt(job_data: dict, include_offer_text: bool = False) -> str:
    jid = job_data.get("id")
    title = job_data.get("title")
    prop = job_data.get("ai_proposal") or {}
    audyt = prop.get("audyt_100")

    lines = []
    lines.append("=" * 70)
    lines.append(f"RAPORT AUDYTU DLA ZLECENIA #{jid}")
    lines.append(f"Tytuł: {title}")
    lines.append(f"Status: {job_data.get('status')} | Wycena: {prop.get('wycena')} zł | Czas: {prop.get('dni')} dni")
    lines.append("=" * 70)

    if not audyt:
        lines.append("Brak zapisanego pełnego raportu audytu dla tego zlecenia.")
        lines.append("(Audyt był uruchomiony przed włączeniem trwałego zapisu lub zlecenie nie przeszło audytu).")
        return "\n".join(lines)

    score = audyt.get("wynik_100", prop.get("audyt_wynik_100", 0))
    werdykt = audyt.get("werdykt", "BRAK")
    rundy = prop.get("audyt_rundy", 1)

    lines.append(f"WYNIK KOŃCOWY: {score}/100 pkt | WERDYKT: {werdykt} | RUNDY AUDYTU: {rundy}")
    lines.append("-" * 70)

    # Wymiary
    wymiary = audyt.get("wymiary") or {}
    if wymiary:
        lines.append("PUNKTACJA W 5 WYMIARACH:")
        for k, v in wymiary.items():
            lines.append(f"  • {k}: {v}")
        lines.append("")

    # Za co dodano punkty
    dodano = audyt.get("za_co_dodano") or []
    if dodano:
        lines.append("ZA CO DODANO PUNKTY:")
        for item in dodano:
            if isinstance(item, dict):
                pkt = item.get("punkty", "+pkt")
                uzas = item.get("uzasadnienie", "")
                cytat = item.get("cytat", "")
                cytat_str = f' [Cytat: "{cytat}"]' if cytat else ""
                lines.append(f"  [+] {pkt}: {uzas}{cytat_str}")
            else:
                lines.append(f"  [+] {item}")
        lines.append("")

    # Za co odjęto punkty / Kary
    odjeto = audyt.get("za_co_odjeto") or []
    if odjeto:
        lines.append("ZA CO ODJĘTO PUNKTY (FEEDBACK SĘDZIEGO):")
        for item in odjeto:
            if isinstance(item, dict):
                pkt = item.get("punkty", "-pkt")
                uzas = item.get("uzasadnienie", "")
                cytat = item.get("cytat", "")
                cytat_str = f' [Cytat: "{cytat}"]' if cytat else ""
                lines.append(f"  [-] {pkt}: {uzas}{cytat_str}")
            else:
                lines.append(f"  [-] {item}")
        lines.append("")
    else:
        lines.append("ZA CO ODJĘTO PUNKTY: Brak kar! Oferta spełniła wszystkie kryteria.")
        lines.append("")

    # Rekomendacja poprawki
    rekomendacja = audyt.get("rekomendacja_poprawki")
    if rekomendacja:
        lines.append("REKOMENDACJA POPRAWKI (TREŚĆ FEEDBACKU DLA GENERATORA):")
        lines.append(f"  {rekomendacja}")
        lines.append("")

    # Historia pierwszej rundy jeśli była poprawka
    audyt_r1 = prop.get("audyt_r1")
    if audyt_r1:
        score_r1 = audyt_r1.get("wynik_100", 0)
        lines.append(f"HISTORIA 1. RUNDY (PRZED POPRAWKĄ): {score_r1}/100 pkt (finalnie: {score}/100 pkt)")
        r1_odjeto = audyt_r1.get("za_co_odjeto") or []
        if r1_odjeto:
            lines.append("  Feedback z 1. rundy, na podstawie którego poprawiono ofertę:")
            for item in r1_odjeto:
                if isinstance(item, dict):
                    lines.append(f"    [-] {item.get('punkty', '-pkt')}: {item.get('uzasadnienie', '')}")
                else:
                    lines.append(f"    [-] {item}")
        r1_rek = audyt_r1.get("rekomendacja_poprawki")
        if r1_rek:
            lines.append(f"  Instrukcja naprawcza z 1. rundy: {r1_rek}")
        lines.append("")

    if include_offer_text and prop.get("opis"):
        lines.append("-" * 70)
        lines.append("PEŁNA TREŚĆ WYSŁANEJ OFERTY:")
        lines.append("-" * 70)
        lines.append(prop.get("opis", ""))
        lines.append("")

    return "\n".join(lines)


def eksportuj_wszystkie_audyty_do_folderu() -> Path:
    """Tworzy gotowe pliki .md z audytami w folderze useme_core/audyty/."""
    AUDYTY_DIR.mkdir(parents=True, exist_ok=True)
    audited_jobs = []

    for p in MAGAZYN_DIR.rglob("*.json"):
        if ".checkpoints" in str(p) or p.name in ("marker.json", ".bezpieczenstwo.json"):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            prop = data.get("ai_proposal") or {}
            # Fallback: sprawdź w tablicy oferty, jeśli w ai_proposal brakuje audyt_100
            if not prop.get("audyt_100") and data.get("oferty"):
                for o in reversed(data["oferty"]):
                    if o.get("audyt_100"):
                        for k in ("audyt_100", "audyt_r1", "audyt_rundy", "audyt_wynik_100"):
                            if k in o:
                                prop[k] = o[k]
                        break
            if prop.get("audyt_100"):
                audited_jobs.append(data)
        except Exception:
            pass

    audited_jobs.sort(key=lambda j: j.get("data_wyslania") or str(j.get("id") or ""), reverse=True)

    zbiorcze_lines = [
        "# ZBIORCZY RAPORT AUDYTÓW OFERT (100 PKT) – FEEDBACK SĘDZIEGO",
        "",
        f"Liczba zaudytowanych ofert w folderze: **{len(audited_jobs)}**",
        "",
    ]

    for j in audited_jobs:
        jid = j.get("id")
        prop = j.get("ai_proposal") or {}
        aud = prop.get("audyt_100") or {}
        score = aud.get("wynik_100") or prop.get("audyt_wynik_100") or 0
        raport_txt = formatuj_audyt(j, include_offer_text=True)

        # Zapis pojedynczego pliku dla zlecenia
        single_path = AUDYTY_DIR / f"audyt_{jid}_{score}pkt.md"
        single_path.write_text(raport_txt, encoding="utf-8")

        zbiorcze_lines.append(raport_txt)
        zbiorcze_lines.append("\n\n")

    master_path = AUDYTY_DIR / "00_WSZYSTKIE_AUDYTY_ZBIORCZO.md"
    master_path.write_text("\n".join(zbiorcze_lines), encoding="utf-8")
    return AUDYTY_DIR


def main():
    eksportuj_wszystkie_audyty_do_folderu()
    if len(sys.argv) > 1:
        target_id = sys.argv[1].strip()
        found = False
        for p in MAGAZYN_DIR.rglob(f"{target_id}.json"):
            if ".checkpoints" in str(p):
                continue
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(formatuj_audyt(data, include_offer_text=False))
            found = True
            break
        if not found:
            print(f"Nie znaleziono zlecenia #{target_id} w bazie {MAGAZYN_DIR}.")
    else:
        print(f"=== OSTATNIE OFERTY I ICH AUDYTY (Folder: {AUDYTY_DIR}) ===")
        all_jobs = []
        for p in MAGAZYN_DIR.rglob("*.json"):
            if ".checkpoints" in str(p) or p.name in ("marker.json", ".bezpieczenstwo.json"):
                continue
            try:
                data = json.load(open(p, encoding="utf-8"))
                prop = data.get("ai_proposal") or {}
                if prop.get("audyt_100") or data.get("status") in ("WYSLANO", "PRZYGOTOWANA"):
                    all_jobs.append((1 if prop.get("audyt_100") else 0, data.get("data_wyslania") or "", data))
            except Exception:
                pass
        all_jobs.sort(key=lambda x: (x[0], x[1]), reverse=True)

        for _, _, j in all_jobs[:15]:
            jid = j.get("id")
            title = (j.get("title") or "")[:45]
            st = j.get("status")
            prop = j.get("ai_proposal") or {}
            aud = prop.get("audyt_100") or {}
            score = aud.get("wynik_100") or prop.get("audyt_wynik_100")
            score_str = f"{score}/100 pkt" if score else "brak audytu"
            print(f"#{jid:7} | {st:12} | {score_str:12} | {title}...")

        print(f"\nGotowe pliki z audytami zapisano w folderze: {AUDYTY_DIR}")


if __name__ == "__main__":
    main()
