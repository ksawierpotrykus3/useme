# -*- coding: utf-8 -*-
"""
ŚWIAT 1 (ZLECENIODAWCA / MYSTERY SHOPPING - #144890):
Przelicza statystyki wszystkich ofert publicznych i wiadomości prywatnych (PV)
dla zlecenia #144890 (obecnie 101 ofert + 19 wątków PV = 110 unikalnych wykonawców),
aktualizuje `analiza_cech_konkurencji.json` oraz synchronizuje pliki referencyjne
w `laboratorium_modeli/03_DANE_REFERENCYJNE/zlecenie_144890/`.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ZLECENIE_DIR = (
    BASE_DIR
    / "badania"
    / "baza"
    / "weronikabuchholc13"
    / "04_moje_zlecenia"
    / "zlecenie_testowe_144890"
)
LAB_REF_DIR = (
    BASE_DIR.parent
    / "laboratorium_modeli"
    / "03_DANE_REFERENCYJNE"
    / "zlecenie_144890"
)


def parse_price(p_str: str | None) -> float | None:
    if not p_str:
        return None
    m = re.search(r"([\d\s]+(?:[.,]\d+)?)", str(p_str))
    if not m:
        return None
    try:
        return float(m.group(1).replace(" ", "").replace(",", "."))
    except ValueError:
        return None


def parse_days(d_str: str | None) -> int | None:
    if not d_str:
        return None
    m = re.search(r"(\d+)", str(d_str))
    return int(m.group(1)) if m else None


def parse_contracts(c_str: str | None) -> int:
    if not c_str:
        return 0
    m = re.search(r"(\d+)", str(c_str))
    return int(m.group(1)) if m else 0


def compute_competitor_stats() -> dict:
    offers_path = ZLECENIE_DIR / "oferty_publiczne_30.json"
    pv_path = ZLECENIE_DIR / "wiadomosci_zleceniodawcy_pelne.json"

    offers = json.loads(offers_path.read_text(encoding="utf-8"))
    pv_threads = json.loads(pv_path.read_text(encoding="utf-8")) if pv_path.exists() else []

    tech_patterns = {
        "KSeF": r"\bksef\b",
        "n8n": r"\bn8n\b",
        "Make / Integromat": r"\bmake\b|\bintegromat\b",
        "Docker / VPS": r"\bdocker\b|\bvps\b|\bself-hosted\b|\bwłasnym serwerze\b|\bwlasnym serwerze\b",
        "Sfera / API (Optima)": r"\bsfera\b|\boptima\s*api\b|\bweb\s*api\b|\brest\s*api\b",
        "XML / EDI / Praca Rozproszona (Import)": r"\bxml\b|\bedi\b|\bpraca rozproszona\b|\bplik wymiany\b|\bplik importu\b",
        "MSSQL / Baza danych": r"\bmssql\b|\bms sql\b|\bsql\b|\bpostgres\b",
        "OpenAI / GPT": r"\bopenai\b|\bgpt\b|\bchatgpt\b",
        "Claude / Anthropic": r"\bclaude\b|\banthropic\b",
        "Gemini / Google AI": r"\bgemini\b|\bdocument ai\b|\bvertex\b",
        "Textract / Azure / Mistral OCR": r"\btextract\b|\bazure\b|\bmistral\b|\bpaddleocr\b|\btesseract\b",
        "Python / FastAPI": r"\bpython\b|\bfastapi\b",
        "Retainer / Miesięczny abonament": r"\babonament\b|\bmiesięcznie\b|\bmiesiecznie\b|\bretainer\b|\bsla\b",
        "Gwarancja / Opieka powdrożeniowa": r"\bgwarancj\w*\b|\basyst\w*\b|\bopiek\w*\b",
        "Etapowanie / PoC / Próbka przed umową": r"\betap\w*\b|\bpróbk\w*\b|\bprobk\w*\b|\bpoc\b|\bpilot\w*\b|\bprototyp\w*\b",
    }

    tech_counts = {k: 0 for k in tech_patterns}
    processed_offers = []
    prices = []
    days_list = []
    lengths = []
    contracts_list = []

    for off in offers:
        txt = off.get("proposal_text") or ""
        txt_lower = txt.lower()
        p_val = parse_price(off.get("price"))
        d_val = parse_days(off.get("days"))
        c_val = parse_contracts(off.get("author_contracts"))

        if p_val is not None:
            prices.append(p_val)
        if d_val is not None:
            days_list.append(d_val)
        lengths.append(len(txt))
        contracts_list.append(c_val)

        for t_name, pat in tech_patterns.items():
            if re.search(pat, txt_lower):
                tech_counts[t_name] += 1

        first_para = next((line.strip() for line in txt.splitlines() if len(line.strip()) > 20), txt[:250])
        processed_offers.append(
            {
                "id": str(off.get("offer_id")),
                "author": off.get("author_name"),
                "contracts": off.get("author_contracts"),
                "contracts_num": c_val,
                "published_at": off.get("published_at"),
                "price": p_val,
                "days": d_val,
                "length": len(txt),
                "links": off.get("proposal_links", []),
                "hook": first_para[:350],
                "full_text": txt,
            }
        )

    pv_with_offer = [t for t in pv_threads if t.get("has_submitted_offer")]
    pv_without_offer = [t for t in pv_threads if not t.get("has_submitted_offer")]

    # Filtrujemy ceny bez ekstremalnego dumpingu (<= 100 PLN) do realnej średniej rynkowej, ale raportujemy obie
    real_prices = [p for p in prices if p >= 500]

    summary = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_public_offers": len(offers),
        "total_pv_threads": len(pv_threads),
        "pv_with_public_offer": len(pv_with_offer),
        "pv_only_without_public_offer": len(pv_without_offer),
        "total_unique_contractors": len(offers) + len(pv_without_offer),
        "price_stats_all_pln": {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "mean": round(statistics.mean(prices), 2) if prices else 0,
            "median": round(statistics.median(prices), 2) if prices else 0,
            "p25": round(statistics.quantiles(prices, n=4)[0], 2) if len(prices) >= 4 else 0,
            "p75": round(statistics.quantiles(prices, n=4)[2], 2) if len(prices) >= 4 else 0,
        },
        "price_stats_real_b2b_pln": {
            "count": len(real_prices),
            "min": min(real_prices) if real_prices else 0,
            "max": max(real_prices) if real_prices else 0,
            "mean": round(statistics.mean(real_prices), 2) if real_prices else 0,
            "median": round(statistics.median(real_prices), 2) if real_prices else 0,
        },
        "price_brackets": {
            "dumping_below_3000": sum(1 for p in prices if p < 3000),
            "budget_3000_to_5999": sum(1 for p in prices if 3000 <= p < 6000),
            "sweet_spot_6000_to_10000": sum(1 for p in prices if 6000 <= p <= 10000),
            "agency_10001_to_16000": sum(1 for p in prices if 10000 < p <= 16000),
            "enterprise_above_16000": sum(1 for p in prices if p > 16000),
        },
        "days_stats": {
            "min": min(days_list) if days_list else 0,
            "max": max(days_list) if days_list else 0,
            "mean": round(statistics.mean(days_list), 1) if days_list else 0,
            "median": round(statistics.median(days_list), 1) if days_list else 0,
        },
        "length_chars_stats": {
            "min": min(lengths) if lengths else 0,
            "max": max(lengths) if lengths else 0,
            "mean": round(statistics.mean(lengths), 1) if lengths else 0,
            "median": round(statistics.median(lengths), 1) if lengths else 0,
        },
        "contracts_stats": {
            "zero_contracts_count": sum(1 for c in contracts_list if c == 0),
            "zero_contracts_pct": round(sum(1 for c in contracts_list if c == 0) / len(contracts_list) * 100, 1) if contracts_list else 0,
            "max_contracts": max(contracts_list) if contracts_list else 0,
            "mean_contracts": round(statistics.mean(contracts_list), 1) if contracts_list else 0,
        },
    }

    result = {
        "summary": summary,
        "tech_mentions": tech_counts,
        "offers": processed_offers,
    }

    out_path = ZLECENIE_DIR / "analiza_cech_konkurencji.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ŚWIAT 1 - STATYSTYKI] Zaktualizowano {out_path}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\n[Wzmianki technologiczne i taktyczne w 101 ofertach]:")
    for k, v in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True):
        pct = round(v / len(offers) * 100, 1) if offers else 0
        print(f"  - {k:<40}: {v:>3} / {len(offers)} ({pct}%)")

    sync_laboratorium_modeli_refs(offers, pv_threads)
    return result


def sync_laboratorium_modeli_refs(offers: list[dict], pv_threads: list[dict]) -> None:
    if not LAB_REF_DIR.exists():
        return

    # Podziel 101 ofert na 3 równe części do plików referencyjnych laboratorium_modeli
    chunk1 = offers[0:34]
    chunk2 = offers[34:68]
    chunk3 = offers[68:]

    def format_offers_md(title: str, subset: list[dict]) -> str:
        lines = [f"# {title}\n"]
        for o in subset:
            txt = (o.get("proposal_text") or "").strip()
            lines.append(
                f"=== OFERTA #{o.get('offer_id')} | Autor: {o.get('author_name')} ({o.get('author_contracts')}) "
                f"| Cena: {o.get('price')} | Czas: {o.get('days')} | Data: {o.get('published_at')} | Długość: {len(txt)} zn. ==="
            )
            lines.append(txt)
            lines.append("")
        return "\n".join(lines)

    (LAB_REF_DIR / "01_oferty_144890_czesc1_najnowsze.md").write_text(
        format_offers_md(f"NAJNOWSZE OFERTY Z #144890 (CZĘŚĆ 1: {len(chunk1)} OFERT, W TYM 16 NAJNOWSZYCH)", chunk1),
        encoding="utf-8",
    )
    (LAB_REF_DIR / "02_oferty_144890_czesc2.md").write_text(
        format_offers_md(f"OFERTY Z #144890 (CZĘŚĆ 2: {len(chunk2)} OFERT)", chunk2),
        encoding="utf-8",
    )
    (LAB_REF_DIR / "03_oferty_144890_czesc3.md").write_text(
        format_offers_md(f"OFERTY Z #144890 (CZĘŚĆ 3: {len(chunk3)} OFERT)", chunk3),
        encoding="utf-8",
    )

    # Aktualizuj 04_priv_oraz_nasze_oferty.md (zachowując sekcję naszych ofert jeśli była na końcu)
    priv_md_path = ZLECENIE_DIR / "raport_wiadomosci_prywatnych_zleceniodawcy.md"
    if priv_md_path.exists():
        priv_content = priv_md_path.read_text(encoding="utf-8")
        old_04_path = LAB_REF_DIR / "04_priv_oraz_nasze_oferty.md"
        tail_ours = ""
        if old_04_path.exists():
            old_txt = old_04_path.read_text(encoding="utf-8")
            marker = "# NASZE OFERTY"
            if marker in old_txt:
                tail_ours = "\n\n" + old_txt[old_txt.index(marker) :]
        new_04 = "# WIADOMOŚCI PRYWATNE Z #144890 (19 WĄTKÓW) ORAZ NASZE OFERTY\n\n" + priv_content + tail_ours
        old_04_path.write_text(new_04, encoding="utf-8")

    print(f"[ŚWIAT 1 -> LABORATORIUM MODELI] Zsynchronizowano 101 ofert i 19 wątków PV w {LAB_REF_DIR}")


if __name__ == "__main__":
    compute_competitor_stats()
