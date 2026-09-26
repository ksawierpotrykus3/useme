# -*- coding: utf-8 -*-
"""Deterministyczny kalkulator wyceny.

Model (agent 02b) zwraca STRUKTURE (moduly, godziny, flagi), a ten modul liczy
kwote i dni wg mechanika_wyceniania.md. Ta sama struktura = zawsze ta sama cena.

Funkcja publiczna:
    policz_wycene(dane: dict) -> dict
Zwraca dict z: kwota, dni, typ, rozbicie, ostrzezenia.
"""
from __future__ import annotations

import math
import random
import re
from typing import Any, Dict, List, Optional


# --- Parametry mechaniki (twarde) ---
STAWKA_EFEKTYWNA = 90          # zl/h (stala jedyna stawka godzinowa wszedzie: 90 zl/h)
STAWKA_TIER_A = 90             # zl/h (stala jedyna stawka godzinowa wszedzie: 90 zl/h)
STAWKA_MIN = 90                # dolna granica stawki (zawsze 90 zl/h)
STAWKA_MAX = 90                # gorna granica stawki (zawsze 90 zl/h)
NARZUT_TESTY = 0.15            # +15% testy/dokumentacja
BUFOR_STANDARD = 0.20          # +20%
BUFOR_NOWA_TECH = 0.30         # +30% tylko dla niszowej nowej technologii
MAX_RISK_MULTIPLIER = 1.15     # twardy sufit pojedynczego i lacznego mnoznika ryzyka (max(), zero kaskady 1.3*1.25)
CAP_MNOZNIKOW = MAX_RISK_MULTIPLIER
MIN_KWOTA = 500
MIN_DNI = 7                    # twarde minimum formularza Useme (7 dni)
MIN_STAWKA_GODZINOWA = 85      # sanity-check: efektywna stawka nie moze spasc ponizej (zl/h)
DNI_STOPA = 7                  # h/dzien
DNI_WEEKEND = 1.30             # +30% na weekendy i komunikacje

# Reguly korekty konkurencyjnej (KROK 7) - domkniete przedzialy
# (wiek_min, wiek_max, ofert_min, ofert_max, mnoznik)
# USUNIĘTO DUMPING: nie obniżamy stawek przy dużej konkurencji (stop wyścigowi na dno).
KOREKTY = [
    (0, 1, 20, None, 1.0),      # swieze do 24h, >=20 ofert
    (0, 1, 0, 10, 1.05),        # swieze do 24h, mala konkurencja (<=10 ofert) -> +5% marzy
    (0, 1, 10, 20, 1.0),        # swieze do 24h, 10-20 ofert
    (1, 3, 20, None, 1.0),      # 1-3 dni, >=20
    (1, 3, 0, 10, 1.05),        # 1-3 dni, mala konkurencja (<=10 ofert) -> +5% marzy
    (1, 3, 10, 20, 1.0),        # 1-3 dni, 10-20 ofert
    (3, None, 0, 10, 1.15),     # >3 dni, <10 (brak konkurencji = wyższa marża)
    (3, None, 10, 30, 1.0),     # >3 dni, 10-30
    (3, None, 30, None, 1.0),   # >3 dni, >30 (koniec z obniżką 0.85)
]

# Widełki retainerowe
RETAINER_WIDEŁKI = {"opieka_techniczna": (1500, 2500),
                    "customer_success": (2500, 5000)}

# Twardy cap godzin dla One-Page (kontrakt z uzytkownikiem)
CAP_ONE_PAGE_H = 25

# Stala stawka godzinowa wszedzie (brak rozrzutu: offset = 0, zawsze 90 zl/h).
STAWKA_OFFSET_MAX = 0


def wylosuj_stawke(seed: Optional[str] = None) -> int:
    """Zwraca stawke efektywna (zl/h) = 90 zl/h (STAWKA_MIN == STAWKA_MAX == 90)."""
    if seed is not None:
        rnd = random.Random(str(seed))
        return rnd.randint(STAWKA_MIN, STAWKA_MAX)
    return random.randint(STAWKA_MIN, STAWKA_MAX)


def stawka_dla_oferty(job_id: Optional[str], offer_seed: Optional[str]) -> int:
    """Zwraca stawke dla oferty (zawsze 90 zl/h)."""
    if job_id:
        baza = wylosuj_stawke(job_id)
    else:
        baza = STAWKA_EFEKTYWNA
    if offer_seed:
        rnd = random.Random(str(offer_seed))
        offset = rnd.randint(-STAWKA_OFFSET_MAX, STAWKA_OFFSET_MAX)
    else:
        offset = 0
    return max(STAWKA_MIN, min(STAWKA_MAX, baza + offset))


def _safe_int(value: Any, default: int = 0) -> int:
    """Bezpieczne parsowanie liczby calkowitej. Toleruje '6 dni temu', '37 ofert'."""
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else default


def _safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Bezpieczne parsowanie liczby zmiennoprzecinkowej z dowolnego tekstu.

    Toleruje '12 000 zl', '2000 USD', '1500 EUR', 'do negocjacji' (-> default).
    Wykrywa waluty obce (USD, EUR, $, €) i przelicza na PLN."""
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
        # Detekcja walut obcych
        if "usd" in txt or "$" in txt:
            val = val * 4.0  # szacunkowy kurs USD -> PLN
        elif "eur" in txt or "€" in txt:
            val = val * 4.3  # szacunkowy kurs EUR -> PLN
        return val
    except ValueError:
        return default


def _korekta_konkurencyjna(wiek: int, ofert: int) -> float:
    """Zwraca mnoznik korekty konkurencyjnej wg KROK 7."""
    for w_min, w_max, o_min, o_max, mnoz in KOREKTY:
        w_ok = (wiek >= w_min) and (w_max is None or wiek < w_max)
        o_ok = (ofert >= o_min) and (o_max is None or ofert <= o_max)
        if w_ok and o_ok:
            return mnoz
    return 1.0


def _zaokraglij(kwota: float) -> int:
    """KROK 9: zaokraglenie wg przedzialu."""
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

    # Stawka efektywna:
    # - Stala i jedyna obowiazujaca stawka godzinowa wszedzie: 90 zl/h (Tier A i Tier B).
    # - Jawny budzet godzinowy klienta (50-250 zl) jest rozpoznawany jako rozliczenie godzinowe
    #   (aby nie potraktowac np. 100 zl jako calkowitego budzetu projektu), ale stawka to zawsze 90 zl/h.
    is_tier_a = bool(flagi.get("specjalizacja_tier_a") or dane.get("tier") == "A")
    budzet_raw = flagi.get("budzet_jawny")
    budzet_val = _safe_float(budzet_raw, None) if budzet_raw is not None else None

    stawka_godzinowa_klienta: Optional[float] = None
    if budzet_val and 50 <= budzet_val <= 250 and flagi.get("budzet_jako_stawka_h") is not False:
        if typ not in ("male", "małe"):
            stawka_godzinowa_klienta = budzet_val

    stawka = STAWKA_EFEKTYWNA
    if is_tier_a:
        ostrzezenia.append(f"Zastosowano stawke: {stawka} zl/h")
    elif stawka_godzinowa_klienta is not None:
        ostrzezenia.append(f"Rozpoznano budzet godzinowy klienta ({int(stawka_godzinowa_klienta)} zl/h) - zastosowano stala stawke {stawka} zl/h")

    # --- Male zlecenia: tabela rynkowa ---
    if typ in ("male", "małe"):
        kwota = _safe_float(dane.get("kwota_rynek"), MIN_KWOTA) or MIN_KWOTA
        kwota = max(kwota, MIN_KWOTA)
        dni = MIN_DNI
        return {
            "typ": "male",
            "kwota": int(kwota),
            "dni": dni,
            "rozbicie": {"tryb": "tabela rynkowa", "kwota_rynek": kwota},
            "ostrzezenia": ostrzezenia,
        }

    # --- Retainer ---
    if typ == "retainer":
        stawka = _safe_float(dane.get("retainer_stawka_mies"), 0.0) or 0.0
        if stawka <= 0:
            ostrzezenia.append("retainer bez stawki - uzyto dolnej granicy opieki")
            stawka = RETAINER_WIDEŁKI["opieka_techniczna"][0]
        # mnozniki ryzyka dla retainera (funkcja max() z sufitem MAX_RISK_MULTIPLIER = 1.15)
        risk_candidates = [1.0]
        if flagi.get("brak_specyfikacji"):
            risk_candidates.append(1.05)
        if flagi.get("ograniczenia_api"):
            risk_candidates.append(1.12)
        if flagi.get("real_time"):
            risk_candidates.append(1.10)
        m = min(max(risk_candidates), MAX_RISK_MULTIPLIER)
        stawka_po = stawka * m
        korekta = _korekta_konkurencyjna(wiek, ofert)
        stawka_po *= korekta
        stawka_konc = int(round(stawka_po / 100.0) * 100)
        return {
            "typ": "retainer",
            "kwota": stawka_konc,
            "dni": MIN_DNI,
            "okres": "miesiecznie",
            "rozbicie": {"tryb": "retainer", "okres": "miesiecznie",
                         "stawka_bazowa": stawka,
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

    # Kontrakt: One-Page ma twardy cap 25h, ale TYLKO gdy zlecenie JEST landingiem.
    # Gdy landing jest jednym z wielu modułów (np. aplikacja mobilna + panel + landing),
    # NIE przycinamy calego zlecenia - inaczej duzy projekt zostanie wyceniony jak landing.
    def _is_landing(n: str) -> bool:
        return ("one-page" in n) or ("landing" in n)
    moduly_landing = [m for m in moduly if _is_landing((m.get("nazwa") or "").lower())]
    moduly_inne = [m for m in moduly if not _is_landing((m.get("nazwa") or "").lower())]
    # "Czysty landing" = sa moduly landingowe i NIC poza nimi (sam landing, max 1-2 moduly).
    czysty_landing = bool(moduly_landing) and not moduly_inne
    if czysty_landing:
        if godziny_real > CAP_ONE_PAGE_H:
            ostrzezenia.append(
                f"One-Page: cap {CAP_ONE_PAGE_H}h (bylo {godziny_real}h) - przycieto")
            godziny_real = CAP_ONE_PAGE_H
    elif moduly_landing:
        # Landing jest czescia wiekszego projektu - przycinamy TYLKO modul landing,
        # jesli sam przekracza cap. Reszta modulow bez zmian.
        do_cap = 0.0
        for m in moduly_landing:
            h = _safe_float(m.get("godziny_real"), 0.0) or 0.0
            if h > CAP_ONE_PAGE_H:
                ostrzezenia.append(
                    f"Modul landing: cap {CAP_ONE_PAGE_H}h (bylo {h}h) - przycieto sam modul")
                do_cap += h - CAP_ONE_PAGE_H
        if do_cap:
            godziny_real -= do_cap

    # KROK 2.5 testy/dokumentacja
    po_testach = godziny_real * (1 + NARZUT_TESTY)

    # KROK 4 buffer
    if flagi.get("nowa_technologia"):
        bufor = BUFOR_NOWA_TECH
    else:
        bufor = BUFOR_STANDARD
    po_buforze = po_testach * (1 + bufor)

    # KROK 5 mnozniki ryzyka: funkcja max() z sufitem MAX_RISK_MULTIPLIER = 1.15
    # (koniec z kaskadowym mnożeniem ryzyk ponad bufor +20% z KROKU 4)
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

    # KROK 6 cena bazowa
    cena_bazowa = po_mnoznikach * stawka

    # KROK 7 korekta konkurencyjna
    korekta = _korekta_konkurencyjna(wiek, ofert)
    cena_po_korekcie = cena_bazowa * korekta

    # KROK 9.5 budzet jawny jako kotwica całkowita (tylko dla budżetów całkowitych > 250 zł)
    if budzet_val and not stawka_godzinowa_klienta:
        if budzet_val > cena_po_korekcie:
            # Ochrona przed szokiem cenowym (klient podaje budzet 50k, kalkulacja 3k):
            # Nie pozwalamy na skok wyzszy niz 1.4x wyliczonej ceny bazowej
            target = budzet_val * 0.85
            cena_po_korekcie = min(target, cena_po_korekcie * 1.4)
            ostrzezenia.append(f"korekta budzetowa (85% budzetu z capem 1.4x): {cena_po_korekcie:.0f} zl")

    # KROK 9 zaokraglenie
    kwota = max(_zaokraglij(cena_po_korekcie), MIN_KWOTA)

    # --- SANITY-CHECK: efektywna stawka za godzine nie moze byc podejrzanie niska ---
    # Lapie sytuacje, gdy korekta/cap zanizyly kwote o rzad wielkosci
    # (np. duzy projekt przyciety do capu landingu).
    sanity_ok = True
    efektywna_stawka = (kwota / godziny_real) if godziny_real > 0 else kwota
    if efektywna_stawka < MIN_STAWKA_GODZINOWA:
        sanity_ok = False
        ostrzezenia.append(
            f"SANITY: efektywna stawka {efektywna_stawka:.1f} zl/h < progu {MIN_STAWKA_GODZINOWA} zl/h "
            f"({godziny_real:.0f}h, kwota {kwota}) - wycena podejrzanie niska!"
        )

    # KROK 10 dni
    dni = math.ceil(po_mnoznikach / DNI_STOPA)
    dni = math.ceil(dni * DNI_WEEKEND)
    dni = max(dni, MIN_DNI)

    rozbicie = {
        "tryb": "projekt",
        "moduly": moduly,
        "godziny_real": round(godziny_real, 1),
        "po_testach_15": round(po_testach, 1),
        "bufor": bufor,
        "po_buforze": round(po_buforze, 1),
        "mnoznik_ryzyka": round(mnoznik, 3),
        "cap_zadzialal": mnoznik >= CAP_MNOZNIKOW,
        "po_mnoznikach": round(po_mnoznikach, 1),
        "stawka": stawka,
        "is_tier_a": is_tier_a,
        "stawka_godzinowa_klienta": stawka_godzinowa_klienta,
        "cena_bazowa": round(cena_bazowa, 1),
        "korekta_konkurencyjna": korekta,
        "cena_po_korekcie": round(cena_po_korekcie, 1),
        "kwota_koncowa": kwota,
        "efektywna_stawka": round(efektywna_stawka, 1),
        "sanity_ok": sanity_ok,
    }
    return {"typ": "projekt", "kwota": kwota, "dni": dni,
            "rozbicie": rozbicie, "ostrzezenia": ostrzezenia,
            "sanity_ok": sanity_ok}


def formatuj_wynik(wynik: Dict[str, Any]) -> str:
    """Zwraca blok [WYNIK_KONCOWY] + krotkie rozbicie do wklejenia."""
    linie = []
    linie.append("[WYNIK_KONCOWY]")
    linie.append(f"KWOTA: {wynik['kwota']}")
    linie.append(f"DNI: {wynik['dni']}")
    if wynik.get("typ") == "retainer" or wynik.get("okres"):
        linie.append("OKRES: miesiecznie (stala wspolpraca, nie kwota jednorazowa)")
    linie.append("[/WYNIK_KONCOWY]")
    return "\n".join(linie)


if __name__ == "__main__":
    import sys, json
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    przyklad = {
        "typ_zlecenia": "projekt",
        "moduly": [{"nazwa": "Landing page / One-Page", "godziny_real": 20}],
        "flagi": {"brak_specyfikacji": True, "wiek_ofert_dni": 1,
                  "liczba_ofert": 71, "nowa_technologia": False},
    }
    w = policz_wycene(przyklad)
    print(json.dumps(w, ensure_ascii=False, indent=2))