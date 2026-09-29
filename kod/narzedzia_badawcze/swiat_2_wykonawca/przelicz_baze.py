# -*- coding: utf-8 -*-
"""
ŚWIAT 2 (WYKONAWCA / OFERTOWARKA - ksawierpotrykus3):
Zunifikowany kalkulator statystyk empirycznych dla całej bazy ofert Ksawiera
(zarówno archiwalnych z `02_przegrane` i `03_odpisane`, jak i nowych z `01_ofertowarka`).

Zastępuje dawne jednorazowe skrypty:
- `skrypt_audyt_470.py`
- `weryfikacja_danych.py`
- `skrypt_klient_x_tech.py`
- `gleboka_typologia_klientow.py`

Aktualizuje pliki analityczne (z zachowaniem kompatybilności nazw):
1. `badania/analizy/01_dane_empiryczne.json` (oraz alias `01_dane_empiryczne_470.json`)
2. `badania/analizy/technologie/02_matryca_granularna_technologie_i_unmatched.json`
3. `badania/analizy/typy_klientow/02_matryca_2d_klient_x_tech.json`
4. `badania/analizy/03_analiza_zlecen_niewyslanych_selekcja.json`
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KSAWIER_DIR = BASE_DIR / "badania" / "baza" / "ksawierpotrykus3"
ANALIZY_DIR = BASE_DIR / "badania" / "analizy"


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


def analyze_proposal(prop: str | None) -> dict:
    if not prop:
        return {
            "chars": 0,
            "words": 0,
            "has_question_cta": False,
            "has_call_cta": False,
            "has_artifact_cta": False,
            "has_direct_priv": False,
            "coaching_score": 0,
            "tech_density": 0,
        }
    chars = len(prop)
    words = len(prop.split())
    lines = [l.strip() for l in prop.splitlines() if l.strip()]
    last_3 = " ".join(lines[-3:]) if len(lines) >= 3 else " ".join(lines)
    last_3_low = last_3.lower()

    has_question_cta = "?" in last_3
    has_call_cta = any(
        k in last_3_low
        for k in ["zdzwoń", "zdzwon", "call", "rozmow", "telefon", "spotkan", "meet", "google meet"]
    )
    has_artifact_cta = any(
        k in last_3_low
        for k in ["podeślij", "podeslij", "zrzut", "screen", "plik", "link", "figm", "próbk", "probk", "dostęp", "dostep", "repo"]
    )
    has_direct_priv = any(
        k in last_3_low
        for k in ["priv", "wiadomość prywatn", "wiadomosc prywatn", "na czacie", "w wiadomości"]
    )

    coaching_phrases = [
        "doskonale rozumiem", "chętnie pomogę", "chetnie pomoge", "z przyjemnością", "z przyjemnoscia",
        "kompleksow", "indywidualne podejście", "indywidualne podejscie", "profesjonalne podejście",
        "jako doświadczony", "jako doswiadczony", "szerokie doświadczenie", "bogate doświadczenie",
        "gwarantuję pełne", "gwarantuje pelne", "zadbam o każdy", "zadbam o kazdy",
    ]
    prop_lower = prop.lower()
    coaching_score = sum(1 for phrase in coaching_phrases if phrase in prop_lower)

    tech_keywords = [
        "api", "sql", "database", "baza", "json", "xml", "python", "node", "react", "vue",
        "laravel", "docker", "endpoint", "webhook", "rest", "soap", "cron", "middleware",
        "c#", ".net", "php", "wordpress", "woocommerce", "shopify", "prestashop", "postman",
        "git", "token", "auth", "jwt", "redis", "n8n", "make", "zapier", "selenium", "playwright",
        "flutter", "kotlin", "swift", "ios", "android", "css", "html", "liquid", "headless",
    ]
    tech_density = sum(1 for kw in tech_keywords if re.search(r"\b" + re.escape(kw) + r"\b", prop_lower))

    return {
        "chars": chars,
        "words": words,
        "has_question_cta": has_question_cta,
        "has_call_cta": has_call_cta,
        "has_artifact_cta": has_artifact_cta,
        "has_direct_priv": has_direct_priv,
        "coaching_score": coaching_score,
        "tech_density": tech_density,
    }


TECH_DICT_28 = {
    "WordPress / WooCommerce": [r"\bwordpress\b", r"\bwoocommerce\b", r"\bwoo\b"],
    "Shopify / Liquid": [r"\bshopify\b", r"\bliquid\b"],
    "PrestaShop": [r"\bprestashop\b", r"\bpresta\b"],
    "IdoSell (IAI)": [r"\bidosell\b", r"\biai\b"],
    "Shoper": [r"\bshoper\b"],
    "Framer / Webflow": [r"\bframer\b", r"\bwebflow\b"],
    "Laravel / PHP": [r"\blaravel\b", r"\bphp\b", r"\bsymfony\b", r"\bcodeigniter\b", r"\bzend\b"],
    "Python / Django / FastAPI": [r"\bpython\b", r"\bdjango\b", r"\bfastapi\b", r"\bflask\b"],
    "Node.js / Express / Nest": [r"\bnode(?:\.js)?\b", r"\bexpress(?:\.js)?\b", r"\bnest(?:\.js)?\b"],
    "React / Next.js": [r"\breact(?:\.js)?\b", r"\bnext(?:\.js)?\b"],
    "Vue / Nuxt": [r"\bvue(?:\.js)?\b", r"\bnuxt(?:\.js)?\b"],
    "Flutter / Dart": [r"\bflutter\b", r"\bdart\b"],
    "Kotlin / Android native": [r"\bkotlin\b", r"\bandroid\b"],
    "Swift / iOS native": [r"\bswift\b", r"\bios\b"],
    "React Native": [r"\breact\s+native\b"],
    ".NET / C#": [r"\bc#\b", r"\b\.net\b", r"\basp\.net\b"],
    "Make / n8n / Zapier": [r"\bmake(?:\.com)?\b", r"\bn8n\b", r"\bzapier\b", r"\bintegromat\b"],
    "Scraping (Selenium/Playwright/Bs4)": [r"\bscraping\b", r"\bscraper\b", r"\bplaywright\b", r"\bselenium\b", r"\bpuppeteer\b", r"\bcrawler\b"],
    "Subiekt (GT / nexo / Sfera)": [r"\bsubiekt\b", r"\bsfera\b", r"\bnexo\b", r"\binsert\b"],
    "Comarch (Optima / XL)": [r"\boptima\b", r"\bcomarch\b", r"\berp\s*xl\b"],
    "Enova365": [r"\benova(?:365)?\b"],
    "BaseLinker": [r"\bbaselinker\b", r"\bbase\.com\b"],
    "Computer Vision / OCR / AI": [r"\bopencv\b", r"\bocr\b", r"\btesseract\b", r"\byolo\b", r"\bchatgpt\b", r"\bgpt\b", r"\bopenai\b"],
    "Bazy danych / SQL": [r"\bmysql\b", r"\bpostgresql\b", r"\bpostgres\b", r"\bsql\b", r"\bsupabase\b", r"\bmongodb\b", r"\bmssql\b"],
    "DevOps / Docker / VPS": [r"\bdocker\b", r"\bvps\b", r"\blinux\b", r"\bnginx\b", r"\bhosting\b"],
    "Figma / UI design": [r"\bfigma\b", r"\bmakiety\b"],
    "VoIP / Asterisk / SIP": [r"\bvoip\b", r"\basterisk\b", r"\bsip\b"],
    "TopSolid / CAD / CAM": [r"\btopsolid\b", r"\bcad\b", r"\bcam\b", r"\bcnc\b"],
}


def classify_client(job_desc: str, title: str) -> str:
    text = ((job_desc or "") + " " + (title or "")).lower()
    score_biz = sum(1 for w in ["magazyn", "faktur", "ręczn", "reczn", "pracownik", "czasu", "błęd", "usprawni", "proces", "obsług", "hurtown"] if w in text)
    score_tech = sum(1 for w in ["repozytorium", "senior", "architekt", "framework", "endpoint", "postman", "docker", "cto", "lead", "clean code", "pull request", "swagger", "laravel", "vue", "react", "node"] if w in text)
    score_ecom = sum(1 for w in ["shopify", "prestashop", "woocommerce", "idosell", "baselinker", "sklep", "koszyk", "klarna", "feed", "cenow"] if w in text)
    score_startup = sum(1 for w in ["mvp", "startup", "innowacyjn", "platforma", "portal", "użytkownik", "aplikacja mobilna", "długofalow", "faza"] if w in text)
    score_quickfix = sum(1 for w in ["szybka akcja", "na wczoraj", "od zaraz", "piln", "błąd", "naprawa", "poprawka", "prosty skrypt"] if w in text)

    words = len((job_desc or "").split())
    if words < 40 and score_quickfix > 0:
        return "TYP_E_QUICK_FIX"

    scores = {
        "TYP_A_BIZNESMEN_NIETECHNICZNY": score_biz,
        "TYP_B_TECH_LEAD_CTO_PM": score_tech,
        "TYP_C_ECOMMERCE_MANAGER": score_ecom,
        "TYP_D_STARTUPOWIEC_MVP": score_startup,
        "TYP_E_QUICK_FIX": score_quickfix,
    }
    best_type = max(scores.items(), key=lambda x: x[1])
    if best_type[1] == 0:
        if "sklep" in text or "shopify" in text or "e-commerce" in text:
            return "TYP_C_ECOMMERCE_MANAGER"
        elif "aplikacj" in text or "portal" in text:
            return "TYP_D_STARTUPOWIEC_MVP"
        elif words < 50:
            return "TYP_E_QUICK_FIX"
        else:
            return "TYP_A_BIZNESMEN_NIETECHNICZNY"
    return best_type[0]


def classify_tech(job_desc: str, title: str) -> str:
    text = ((job_desc or "") + " " + (title or "")).lower()
    if any(k in text for k in ["subiekt", "enova", "optima", "erp", "sfera", "topsolid", "cad", "cam", "wf-mag", "symfonia", "comarch"]):
        return "TECH_1_ERP_CAD_SYSTEMY"
    elif any(k in text for k in ["bot", "skrypt", "scraping", "crawler", "scraper", "make", "n8n", "zapier", "selenium", "playwright", "automatyzacj", "iptv", "voip"]):
        return "TECH_2_AUTOMATYZACJE_BOTY_SCRAPING"
    elif any(k in text for k in ["shopify", "prestashop", "woocommerce", "wordpress", "idosell", "magento", "framer", "webflow", "sklep"]):
        return "TECH_3_ECOMMERCE_CMS"
    elif any(k in text for k in ["flutter", "react native", "kotlin", "swift", "ios", "android", "mobilna"]):
        return "TECH_4_MOBILE_APPS"
    elif any(k in text for k in ["laravel", "django", "fastapi", "node", "react", "vue", "angular", "next.js", "mvp", "saas", "webowa"]):
        return "TECH_5_WEB_APPS_SAAS"
    else:
        return "TECH_6_LEGACY_INNE"


def main() -> None:
    przegrane = json.loads((KSAWIER_DIR / "02_przegrane" / "przegrane_pelne_416.json").read_text(encoding="utf-8"))
    wygrane = json.loads((KSAWIER_DIR / "03_odpisane" / "wygrane_56.json").read_text(encoding="utf-8"))
    total_n = len(przegrane) + len(wygrane)

    print("=" * 80)
    print(f"PRZELICZANIE BAZY EMPIRYCZNEJ WYKONAWCY (N = {total_n}: {len(wygrane)} wygranych + {len(przegrane)} przegranych)")
    print("=" * 80)

    # 1. Statystyki porównawcze ofert (01_dane_empiryczne)
    dataset = []
    for item in wygrane:
        analysis = analyze_proposal(item.get("our_proposal", ""))
        dataset.append(
            {
                "status": "wygrana",
                "id": item.get("job_id") or item.get("offer_id"),
                "title": item.get("title", ""),
                "category": item.get("category", ""),
                "client": item.get("client", ""),
                "price": parse_price(item.get("our_price")),
                "days": parse_days(item.get("our_days")),
                "job_desc_len": len(item.get("job_description") or ""),
                "thread_size": item.get("thread_size", 0),
                **analysis,
            }
        )
    for item in przegrane:
        analysis = analyze_proposal(item.get("our_proposal", ""))
        dataset.append(
            {
                "status": "przegrana",
                "id": item.get("offer_id"),
                "title": item.get("title", ""),
                "category": item.get("category", ""),
                "client": item.get("client", ""),
                "price": parse_price(item.get("our_price")),
                "days": parse_days(item.get("our_days")),
                "job_desc_len": len(item.get("job_description") or ""),
                "thread_size": 0,
                **analysis,
            }
        )

    def get_stats(subset: list[dict]) -> dict:
        n = len(subset)
        if n == 0:
            return {}
        prices = [x["price"] for x in subset if x["price"] is not None and x["price"] < 100000]
        days = [x["days"] for x in subset if x["days"] is not None]
        return {
            "count": n,
            "avg_words": round(sum(x["words"] for x in subset) / n, 1),
            "avg_chars": round(sum(x["chars"] for x in subset) / n, 1),
            "pct_question_cta": round(sum(1 for x in subset if x["has_question_cta"]) / n * 100, 1),
            "pct_call_cta": round(sum(1 for x in subset if x["has_call_cta"]) / n * 100, 1),
            "pct_artifact_cta": round(sum(1 for x in subset if x["has_artifact_cta"]) / n * 100, 1),
            "pct_direct_priv": round(sum(1 for x in subset if x["has_direct_priv"]) / n * 100, 1),
            "avg_coaching_score": round(sum(x["coaching_score"] for x in subset) / n, 2),
            "avg_tech_density": round(sum(x["tech_density"] for x in subset) / n, 2),
            "avg_price": round(sum(prices) / len(prices), 1) if prices else 0,
            "median_price": sorted(prices)[len(prices) // 2] if prices else 0,
            "avg_days": round(sum(days) / len(days), 1) if days else 0,
        }

    stats_w = get_stats([x for x in dataset if x["status"] == "wygrana"])
    stats_p = get_stats([x for x in dataset if x["status"] == "przegrana"])

    emp_payload = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs": total_n,
        "overall_win_rate_pct": round(len(wygrane) / total_n * 100, 2) if total_n else 0,
        "stats_wygrane": stats_w,
        "stats_przegrane": stats_p,
        "dataset": dataset,
    }
    (ANALIZY_DIR / "01_dane_empiryczne_470.json").write_text(json.dumps(emp_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (ANALIZY_DIR / "01_dane_empiryczne.json").write_text(json.dumps(emp_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[1] STATYSTYKI PORÓWNAWCZE (WYGRANE {len(wygrane)} vs PRZEGRANE {len(przegrane)}):")
    for k in stats_w:
        print(f"  {k:<24}: WYGRANE = {str(stats_w[k]):<10} | PRZEGRANE = {str(stats_p[k]):<10}")

    # 2. Granularna matryca 28 technologii + Unmatched
    all_jobs = [(x, True) for x in wygrane] + [(x, False) for x in przegrane]
    tech_stats = defaultdict(lambda: {"total": 0, "wins": 0, "losses": 0, "win_rate_pct": 0.0})
    unmatched_won = []
    unmatched_lost = []

    for job, won in all_jobs:
        text = ((job.get("title") or "") + " " + (job.get("job_description") or "")).lower()
        matched = False
        for tech_name, patterns in TECH_DICT_28.items():
            if any(re.search(p, text) for p in patterns):
                tech_stats[tech_name]["total"] += 1
                if won:
                    tech_stats[tech_name]["wins"] += 1
                else:
                    tech_stats[tech_name]["losses"] += 1
                matched = True
        if not matched:
            if won:
                unmatched_won.append(job)
            else:
                unmatched_lost.append(job)

    for t_name, st in tech_stats.items():
        st["win_rate_pct"] = round(st["wins"] / st["total"] * 100, 1) if st["total"] > 0 else 0.0

    unmatched_total = len(unmatched_won) + len(unmatched_lost)
    tech_matrix_payload = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs_analyzed": total_n,
        "technologies_28": dict(sorted(tech_stats.items(), key=lambda x: x[1]["total"], reverse=True)),
        "unmatched_summary": {
            "total_unmatched": unmatched_total,
            "pct_of_all_jobs": round(unmatched_total / total_n * 100, 1) if total_n else 0,
            "wins": len(unmatched_won),
            "losses": len(unmatched_lost),
            "win_rate_pct": round(len(unmatched_won) / unmatched_total * 100, 1) if unmatched_total else 0,
            "categories_breakdown": dict(Counter(j.get("category") or "Brak" for j in (unmatched_won + unmatched_lost)).most_common()),
        },
    }
    tech_out_path = ANALIZY_DIR / "technologie" / "02_matryca_granularna_technologie_i_unmatched.json"
    tech_out_path.parent.mkdir(parents=True, exist_ok=True)
    tech_out_path.write_text(json.dumps(tech_matrix_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[2] TOP 12 TECHNOLOGII (z 28 badanych na N={total_n}):")
    for t_name, st in list(tech_matrix_payload["technologies_28"].items())[:12]:
        print(f"  - {t_name:<35}: Total={st['total']:<3} | Wygrane={st['wins']:<2} | WinRate={st['win_rate_pct']}%")
    print(
        f"  - ZLECENIA BEZ TECHNOLOGII (Unmatched): {unmatched_total}/{total_n} "
        f"({tech_matrix_payload['unmatched_summary']['pct_of_all_jobs']}%) | "
        f"Wygrane={len(unmatched_won)} ({tech_matrix_payload['unmatched_summary']['win_rate_pct']}% Win Rate)"
    )

    # 3. Macierz 2D: Typ Klienta x Archetyp Technologiczny
    matrix_2d = defaultdict(lambda: {"wygrana": 0, "przegrana": 0, "total": 0, "win_rate_pct": 0.0})
    client_totals = defaultdict(lambda: {"wygrana": 0, "przegrana": 0, "total": 0, "win_rate_pct": 0.0})
    tech_arch_totals = defaultdict(lambda: {"wygrana": 0, "przegrana": 0, "total": 0, "win_rate_pct": 0.0})

    for job, won in all_jobs:
        ct = classify_client(job.get("job_description") or "", job.get("title") or "")
        tt = classify_tech(job.get("job_description") or "", job.get("title") or "")
        st_key = "wygrana" if won else "przegrana"
        for bucket in (matrix_2d[f"{ct}__x__{tt}"], client_totals[ct], tech_arch_totals[tt]):
            bucket[st_key] += 1
            bucket["total"] += 1
            bucket["win_rate_pct"] = round(bucket["wygrana"] / bucket["total"] * 100, 1)

    matrix_2d_payload = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_jobs": total_n,
        "client_totals": dict(sorted(client_totals.items(), key=lambda x: x[1]["total"], reverse=True)),
        "tech_totals": dict(sorted(tech_arch_totals.items(), key=lambda x: x[1]["total"], reverse=True)),
        "matrix_2d": dict(sorted(matrix_2d.items(), key=lambda x: x[1]["total"], reverse=True)),
    }
    mat2d_path = ANALIZY_DIR / "typy_klientow" / "02_matryca_2d_klient_x_tech.json"
    mat2d_path.parent.mkdir(parents=True, exist_ok=True)
    mat2d_path.write_text(json.dumps(matrix_2d_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[3] MACIERZ TYPÓW KLIENTÓW (N={total_n}):")
    for ct, vals in matrix_2d_payload["client_totals"].items():
        print(f"  - {ct:<32}: Total={vals['total']:<3} | Wygrane={vals['wygrana']:<2} | WinRate={vals['win_rate_pct']}%")

    print(f"\n[4] MACIERZ ARCHETYPÓW TECHNOLOGICZNYCH (N={total_n}):")
    for tt, vals in matrix_2d_payload["tech_totals"].items():
        print(f"  - {tt:<35}: Total={vals['total']:<3} | Wygrane={vals['wygrana']:<2} | WinRate={vals['win_rate_pct']}%")

    # 4. Aktualizacja statusów w 01_ofertowarka (03_analiza_zlecen_niewyslanych_selekcja.json)
    ofertowarka_dir = KSAWIER_DIR / "01_ofertowarka"
    sel_path = ANALIZY_DIR / "03_analiza_zlecen_niewyslanych_selekcja.json"
    existing_sel = json.loads(sel_path.read_text(encoding="utf-8")) if sel_path.exists() else {}

    all_ofertowarka_files = [
        jf for jf in ofertowarka_dir.rglob("*.json")
        if jf.stem.isdigit() and not any(p.startswith(".") for p in jf.parts)
    ]
    status_counts = Counter()
    closed_bot_offers = []
    active_bot_offers = []

    for jf in sorted(all_ofertowarka_files):
        try:
            jd = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue
        st = jd.get("status_koncowy") or jd.get("status") or "NIEZNANY"
        status_counts[st] += 1
        if st == "ZAMKNIETE_NIEODPISANE":
            closed_bot_offers.append(
                {
                    "id": str(jd.get("id")),
                    "title": jd.get("title"),
                    "budget": jd.get("budget"),
                    "offers_count": jd.get("offers_count"),
                    "closed_offer_id": jd.get("closed_offer_id"),
                    "data_wyslania": jd.get("data_wyslania"),
                    "data_weryfikacji": jd.get("data_weryfikacji"),
                    "wycena": (jd.get("oferta") or {}).get("wycena"),
                    "dni": (jd.get("oferta") or {}).get("dni"),
                }
            )
        elif st == "WYSLANO":
            active_bot_offers.append(
                {
                    "id": str(jd.get("id")),
                    "title": jd.get("title"),
                    "budget": jd.get("budget"),
                    "offers_count": jd.get("offers_count"),
                    "data_wyslania": jd.get("data_wyslania"),
                }
            )

    existing_sel["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if "summary" not in existing_sel:
        existing_sel["summary"] = {}
    existing_sel["summary"]["total_ofertowarka"] = len(all_ofertowarka_files)
    existing_sel["summary"]["status_breakdown_live"] = dict(status_counts)
    existing_sel["summary"]["sent_active_waiting_count"] = len(active_bot_offers)
    existing_sel["summary"]["sent_closed_unanswered_count"] = len(closed_bot_offers)
    existing_sel["closed_unanswered_bot_offers"] = closed_bot_offers
    existing_sel["active_waiting_bot_offers"] = active_bot_offers

    sel_path.write_text(json.dumps(existing_sel, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[5] ZAKTUALIZOWANO LEJEK 01_ofertowarka ({len(all_ofertowarka_files)} zleceń):", dict(status_counts))


if __name__ == "__main__":
    main()
