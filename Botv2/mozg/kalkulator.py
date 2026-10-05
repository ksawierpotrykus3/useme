# -*- coding: utf-8 -*-
"""Deterministyczny kalkulator wyceny (skopiowany z V1, obciety z protezy losowania).

Model zwraca STRUKTURE (moduly, godziny, flagi), a ten modul liczy kwote i dni.
Ta sama struktura = zawsze ta sama cena. LLM nigdy nie liczy ceny.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional

# --- Parametry mechaniki (twarde) ---
STAWKA_EFEKTYWNA = 90          # zl/h (jedyna stawka godzinowa wszedzie)
NARZUT_TESTY = 0.15            # +15% testy/dokumentacja
BUFOR_STANDARD = 0.20          # +20%
BUFOR_NOWA_TECH = 0.30         # +30% tylko dla niszowej nowej technologii
MAX_RISK_MULTIPLIER = 1.15     # twardy sufit mnoznika ryzyka (zero kaskady 1.3*1.25)
CAP_MNOZNIKOW = MAX_RISK_MULTIPLIER
MIN_KWOTA = 500
MIN_DNI = 7
MIN_STAWKA_GODZINOWA = 85      # sanity-check efektywnej stawki
DNI_STOPA = 7
DNI_WEEKEND = 1.30

# Reguly korekty konkurencyjnej (bez dumpingu - mala konkurencja PODNOSI marze)
KOREKTY = [
    (0, 1, 20, None, 1.0),
    (0, 1, 0, 10, 1.05),
    (0, 1, 10, 20, 1.0),
    (1, 3, 20, None, 1.0),
    (1, 3, 0, 10, 1.05),
    (1, 3, 10, 20, 1.0),
    (3, None, 0, 10, 1.15),
    (3, None, 10, 30, 1.0),
    (3, None, 30, None, 1.0),
]

RETAINER_WIDEŁKI = {"opieka_techniczna": (1500, 2500),
                    "customer_success": (2500, 5000)}

CAP_ONE_PAGE_H = 25


def _safe_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else default


def _safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Toleruje '12 000 zl', '2000 USD' (kurs 4.0), '1500 EUR' (kurs 4.3)."""
    if value is None:
        return default
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    raw = str(value)
    txt = raw.replace("\xa0", "").replace(" ", "").lower()
    m = re.search(r"\d+(?:[.,]\d+)?", txt)
    if not m:
        return default
    try:
        val = float(m.group(0).replace(",", "."))
        if "usd" in txt or "$" in txt:
            val = val * 4.0
        elif "eur" in txt or "€" in txt:
            val = val * 4.3
        return val
    except ValueError:
        return default


def _korekta_konkurencyjna(wiek: int, ofert: int) -> float:
    for w_min, w_max, o_min, o_max, mnoz in KOREKTY:
        w_ok = (wiek >= w_min) and (w_max is None or wiek < w_max)
        o_ok = (ofert >= o_min) and (o_max is None or ofert <= o_max)
        if w_ok and o_ok:
            return mnoz
    return 1.0


def _zaokraglij(kwota: float) -> int:
    if kwota <= 2000:
        return int(round(kwota / 50.0) * 50)
    if kwota <= 10000:
        return int(round(kwota / 500.0) * 500)
    return int(round(kwota / 1000.0) * 1000)


def policz_wycene(dane: Dict[str, Any]) -> Dict[str, Any]:
    """Liczy wycene deterministycznie z struktury zwroconej przez model."""
    flagi = dane.get("flagi", {}) or {}
    typ = (dane.get("typ_zlecenia") or "projekt").lower()
    ostrzezenia: List[str] = []
    rozbicie: Dict[str, Any] = {}

    wiek = _safe_int(flagi.get("wiek_ofert_dni"), 0)
    ofert = _safe_int(flagi.get("liczba_ofert"), 0)

    is_tier_a = bool(flagi.get("specjalizacja_tier_a") or dane.get("tier") == "A")
    budzet_raw = flagi.get("budzet_jawny")
    budzet_val = _safe_float(budzet_raw, None) if budzet_raw is not None else None

    stawka_godzinowa_klienta: Optional[float] = None
    if budzet_val and 50 <= budzet_val <= 250 and flagi.get("budzet_jako_stawka_h") is not False:
        if typ not in ("male", "małe"):
            stawka_godzinowa_klienta = budzet_val

    stawka = STAWKA_EFEKTYWNA
    if stawka_godzinowa_klienta is not None:
        ostrzezenia.append(
            f"Rozpoznano budzet godzinowy klienta ({int(stawka_godzinowa_klienta)} zl/h) - "
            f"zastosowano stala stawke {stawka} zl/h")

    # --- Male zlecenia: tabela rynkowa ---
    if typ in ("male", "małe"):
        kwota = _safe_float(dane.get("kwota_rynek"), MIN_KWOTA) or MIN_KWOTA
        kwota = max(kwota, MIN_KWOTA)
        return {
            "typ": "male", "kwota": int(kwota), "dni": MIN_DNI,
            "rozbicie": {"tryb": "tabela rynkowa", "kwota_rynek": kwota},
            "ostrzezenia": ostrzezenia,
        }

    # --- Retainer ---
    if typ == "retainer":
        stawka_r = _safe_float(dane.get("retainer_stawka_mies"), 0.0) or 0.0
        if stawka_r <= 0:
            ostrzezenia.append("retainer bez stawki - uzyto dolnej granicy opieki")
            stawka_r = RETAINER_WIDEŁKI["opieka_techniczna"][0]
        risk_candidates = [1.0]
        if flagi.get("brak_specyfikacji"):
            risk_candidates.append(1.05)
        if flagi.get("ograniczenia_api"):
            risk_candidates.append(1.12)
        if flagi.get("real_time"):
            risk_candidates.append(1.10)
        m = min(max(risk_candidates), MAX_RISK_MULTIPLIER)
        korekta = _korekta_konkurencyjna(wiek, ofert)
        stawka_konc = int(round((stawka_r * m * korekta) / 100.0) * 100)
        return {
            "typ": "retainer", "kwota": stawka_konc, "dni": MIN_DNI, "okres": "miesiecznie",
            "rozbicie": {"tryb": "retainer", "okres": "miesiecznie", "stawka_bazowa": stawka_r,
                         "mnoznik": round(m, 3), "korekta": korekta},
            "ostrzezenia": ostrzezenia,
        }

    # --- Projekt godzinowy ---
    moduly = dane.get("moduly") or []
    if not moduly:
        ostrzezenia.append("brak modulow - uzyto minimum")
        godziny_real = 1.0
    else:
        godziny_real = sum(_safe_float(m.get("godziny_real"), 0.0) or 0.0 for m in moduly)

    # One-Page cap 25h TYLKO dla czystego landingu (nie przycinaj calego duzego projektu)
    def _is_landing(n: str) -> bool:
        return ("one-page" in n) or ("landing" in n)
    moduly_landing = [m for m in moduly if _is_landing((m.get("nazwa") or "").lower())]
    moduly_inne = [m for m in moduly if not _is_landing((m.get("nazwa") or "").lower())]
    czysty_landing = bool(moduly_landing) and not moduly_inne
    if czysty_landing:
        if godziny_real > CAP_ONE_PAGE_H:
            ostrzezenia.append(f"One-Page: cap {CAP_ONE_PAGE_H}h (bylo {godziny_real}h) - przycieto")
            godziny_real = CAP_ONE_PAGE_H
    elif moduly_landing:
        do_cap = 0.0
        for m in moduly_landing:
            h = _safe_float(m.get("godziny_real"), 0.0) or 0.0
            if h > CAP_ONE_PAGE_H:
                ostrzezenia.append(f"Modul landing: cap {CAP_ONE_PAGE_H}h (bylo {h}h) - przycieto sam modul")
                do_cap += h - CAP_ONE_PAGE_H
        if do_cap:
            godziny_real -= do_cap

    po_testach = godziny_real * (1 + NARZUT_TESTY)
    bufor = BUFOR_NOWA_TECH if flagi.get("nowa_technologia") else BUFOR_STANDARD
    po_buforze = po_testach * (1 + bufor)

    ma_figme = bool(flagi.get("figma_w_ogloszeniu"))
    if ma_figme:
        mnoznik = 0.9
    else:
        risk_candidates = [1.0]
        if flagi.get("brak_specyfikacji"):
            risk_candidates.append(1.05)
        if flagi.get("ograniczenia_api"):
            ma_modul_api = any(
                any(k in (m.get("nazwa") or "").lower() for k in ("api", "integracj", "erp", "ksef", "ocr", "webhook"))
                for m in moduly
            )
            risk_candidates.append(1.05 if ma_modul_api else 1.15)
        if flagi.get("real_time"):
            risk_candidates.append(1.10)
        mnoznik = min(max(risk_candidates), MAX_RISK_MULTIPLIER)
    po_mnoznikach = po_buforze * mnoznik

    cena_bazowa = po_mnoznikach * stawka
    korekta = _korekta_konkurencyjna(wiek, ofert)
    cena_po_korekcie = cena_bazowa * korekta

    # Kotwica budzetu jawnego z capem 1.4x (ochrona przed szokiem cenowym)
    if budzet_val and not stawka_godzinowa_klienta:
        if budzet_val > cena_po_korekcie:
            target = budzet_val * 0.85
            cena_po_korekcie = min(target, cena_po_korekcie * 1.4)
            ostrzezenia.append(f"korekta budzetowa (85% budzetu z capem 1.4x): {cena_po_korekcie:.0f} zl")

    kwota = max(_zaokraglij(cena_po_korekcie), MIN_KWOTA)

    sanity_ok = True
    efektywna_stawka = (kwota / godziny_real) if godziny_real > 0 else kwota
    if efektywna_stawka < MIN_STAWKA_GODZINOWA:
        sanity_ok = False
        ostrzezenia.append(
            f"SANITY: efektywna stawka {efektywna_stawka:.1f} zl/h < progu {MIN_STAWKA_GODZINOWA} zl/h "
            f"({godziny_real:.0f}h, kwota {kwota}) - wycena podejrzanie niska!")

    dni = math.ceil(po_mnoznikach / DNI_STOPA)
    dni = math.ceil(dni * DNI_WEEKEND)
    dni = max(dni, MIN_DNI)

    rozbicie = {
        "tryb": "projekt", "godziny_real": round(godziny_real, 1),
        "po_testach_15": round(po_testach, 1), "bufor": bufor,
        "po_buforze": round(po_buforze, 1), "mnoznik_ryzyka": round(mnoznik, 3),
        "cap_zadzialal": mnoznik >= CAP_MNOZNIKOW, "po_mnoznikach": round(po_mnoznikach, 1),
        "stawka": stawka, "cena_bazowa": round(cena_bazowa, 1),
        "korekta_konkurencyjna": korekta, "cena_po_korekcie": round(cena_po_korekcie, 1),
        "kwota_koncowa": kwota, "sanity_ok": sanity_ok,
    }
    return {"typ": "projekt", "kwota": kwota, "dni": dni,
            "rozbicie": rozbicie, "ostrzezenia": ostrzezenia, "sanity_ok": sanity_ok}