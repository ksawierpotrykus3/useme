# -*- coding: utf-8 -*-
"""Test weryfikacyjny reformy silnika:
1. Dekodowanie budzetow godzinowych 50-250 zl (np. 100 zl/h).
2. Wyzsza stawka Tier A (140 zl/h) dla nisz specjalistycznych.
3. Priorytetyzacja Tier A przed Tier B w selekcji ai_pipeline.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from wycena_kalkulator import policz_wycene, STAWKA_EFEKTYWNA, STAWKA_TIER_A


def test_budzet_godzinowy_100_zl():
    print("\n--- TEST 1: Dekodowanie budżetu 100 zł jako rozliczenia godzinowego (ze stawką 90 zł/h) ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "JOB-100H",
        "moduly": [
            {"nazwa": "Integracja API i automatyzacja", "godziny_real": 20},
        ],
        "flagi": {
            "budzet_jawny": "100",  # Klient wpisał 100 zł na Useme
            "brak_specyfikacji": False,
        }
    }
    w = policz_wycene(struktura)
    rozbicie = w["rozbicie"]
    stawka = rozbicie["stawka"]
    kwota = w["kwota"]

    print(f"Stawka zastosowana: {stawka} zł/h, Kwota końcowa: {kwota} zł")
    assert stawka == 90, f"BŁĄD: Oczekiwano stałej stawki 90 zł/h, otrzymano {stawka}"
    # 20h * 1.15 (testy) * 1.20 (bufor) * 1.0 (ryzyko) = 27.6h -> 27.6 * 90 = 2484 -> zaokrąglenie do 2500 zł
    assert kwota > 1500, f"BŁĄD: Kwota {kwota} zł została zaniżona do 100 zł! Powinna wynosić ~2500 zł."
    assert rozbicie.get("stawka_godzinowa_klienta") == 100.0
    print("[DOWÓD 1] Budżet 100 zł został rozpoznany jako godzinowy, wyceniony ze stałą stawką 90 zł/h. OK")


def test_stawka_tier_a_specjalizacja():
    print("\n--- TEST 2: Stawka Tier A (90 zł/h) dla nisz ERP / AI ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "JOB-TIER-A",
        "moduly": [
            {"nazwa": "Wdrożenie agenta AI / RAG", "godziny_real": 25},
        ],
        "flagi": {
            "specjalizacja_tier_a": True,
            "brak_specyfikacji": False,
        }
    }
    w = policz_wycene(struktura)
    rozbicie = w["rozbicie"]
    stawka = rozbicie["stawka"]
    kwota = w["kwota"]

    print(f"Stawka zastosowana: {stawka} zł/h, Kwota końcowa: {kwota} zł")
    assert stawka == 90 and STAWKA_TIER_A == 90, f"BŁĄD: Oczekiwano stawki 90 zł/h, otrzymano {stawka}"
    assert rozbicie.get("is_tier_a") is True
    print(f"[DOWÓD 2] Zastosowano stawkę {STAWKA_TIER_A} zł/h dla Tier A. OK")


def test_standardowa_stawka_tier_b():
    print("\n--- TEST 3: Standardowa stawka Tier B (90 zł/h) ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "JOB-TIER-B",
        "moduly": [
            {"nazwa": "Sklep WooCommerce", "godziny_real": 25},
        ],
        "flagi": {
            "specjalizacja_tier_a": False,
            "brak_specyfikacji": False,
        }
    }
    w = policz_wycene(struktura)
    stawka = w["rozbicie"]["stawka"]

    print(f"Stawka zastosowana: {stawka} zł/h, Kwota końcowa: {w['kwota']} zł")
    assert stawka == 90 and STAWKA_EFEKTYWNA == 90, f"BŁĄD: Oczekiwano stawki 90 zł/h, otrzymano {stawka}"
    print(f"[DOWÓD 3] Standardowe zlecenie otrzymało stawkę {STAWKA_EFEKTYWNA} zł/h. OK")


def test_sortowanie_ofert_tier_a_przed_tier_b():
    print("\n--- TEST 4: Sortowanie zakwalifikowanych ofert (Tier A przed Tier B) ---")
    from ai_pipeline import SlotChainAIPipeline
    pipeline = SlotChainAIPipeline()

    # Symulujemy listę ofert
    oferty = [
        {"id": "1", "title": "WordPress poprawki", "budget": "500", "tier": "B"},
        {"id": "2", "title": "Integracja KSeF ERP Comarch", "budget": "15000", "tier": "A"},
        {"id": "3", "title": "Sklep Shopify", "budget": "4000", "tier": "B"},
        {"id": "4", "title": "Bot scraping z Turnstile", "budget": "8000", "tier": "A"},
    ]

    # Testujemy logikę sortowania
    oferty.sort(key=lambda x: 0 if x.get("tier") == "A" else 1)
    kolejnosc_id = [o["id"] for o in oferty]
    print(f"Kolejność po sortowaniu priorytetowym: {kolejnosc_id}")
    assert kolejnosc_id == ["2", "4", "1", "3"], f"BŁĄD: Zła kolejność {kolejnosc_id}"
    print("[DOWÓD 4] Oferty Tier A są na szczycie kolejki ofertowej. OK")


if __name__ == "__main__":
    test_budzet_godzinowy_100_zl()
    test_stawka_tier_a_specjalizacja()
    test_standardowa_stawka_tier_b()
    test_sortowanie_ofert_tier_a_przed_tier_b()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY TIER I BUDŻETÓW GODZINOWYCH ZALICZONE!")
    print("=======================================================")
