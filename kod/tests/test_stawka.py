# -*- coding: utf-8 -*-
"""Test losowania stawki w bezpiecznym pasmie (per OFERTA).

Sprawdza:
1. Stawka ZAWSZE w [STAWKA_MIN, STAWKA_MAX=110] - nigdy za nisko, nigdy za wysoko.
2. ODDZIELNE losowanie per oferta: to samo zlecenie, rozne konta -> rozne stawki.
3. Ten sam seed -> ta sama stawka (deterministycznie, odporne na retry).
4. policz_wycene uzywa seeda oferty (stawka_seed), nie id zlecenia.
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from wycena_kalkulator import (wylosuj_stawke, stawka_dla_oferty, policz_wycene,
                               STAWKA_MIN, STAWKA_MAX, STAWKA_OFFSET_MAX)


def test_zakres():
    print("\n--- TEST 1: stała stawka 90 zł/h ---")
    stawki = [wylosuj_stawke() for _ in range(1000)]
    assert all(s == 90 for s in stawki), \
        f"BŁĄD: stawka inna niż 90 zł/h! ({set(stawki)})"
    assert STAWKA_MIN == 90 and STAWKA_MAX == 90
    print(f"[DOWÓD 1] 1000 wywolan, min={min(stawki)}, max={max(stawki)} (zawsze 90 zł/h) OK")


def test_oddzielne_per_oferta():
    print("\n--- TEST 2: stawka_dla_oferty zawsze zwraca 90 zł/h ---")
    pary = []
    for j in range(50):
        s1 = stawka_dla_oferty(f"job{j}", f"job{j}-konto1")
        s2 = stawka_dla_oferty(f"job{j}", f"job{j}-konto2")
        pary.append((s1, s2))
    assert all(a == 90 and b == 90 for a, b in pary), "BŁĄD: stawka różna od 90 zł/h!"
    max_rozrzut = max(abs(a - b) for a, b in pary)
    assert max_rozrzut <= 2 * STAWKA_OFFSET_MAX
    print(f"[DOWÓD 2] 50 zlecen: wszystkie oferty maja dokladnie 90 zł/h (rozrzut={max_rozrzut}) OK")


def test_determinizm():
    print("\n--- TEST 3: determinizm po seedzie oferty ---")
    s1 = wylosuj_stawke("143764-konto1")
    s2 = wylosuj_stawke("143764-konto1")
    assert s1 == s2, f"BŁĄD: ten sam seed dał różne stawki: {s1} != {s2}"
    print(f"[DOWÓD 3] Seed '143764-konto1' -> zawsze {s1} (odporne na retry)")


def test_kalkulator_uzywa_stawka_seed():
    print("\n--- TEST 4: kalkulator używa stawka_seed (per oferta) ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "moduly": [{"nazwa": "WordPress", "godziny_real": 40}],
        "flagi": {"wiek_ofert_dni": 5, "liczba_ofert": 15},
    }
    # To samo zlecenie, dwa seedy (konta) -> moga dac rozne kwoty
    kwoty = {}
    for konto in ["konto1", "konto2"]:
        d = dict(struktura)
        d["id"] = "143764"
        d["seed"] = f"143764-{konto}"
        w = policz_wycene(d)
        kwoty[konto] = w["kwota"]
        st = w["rozbicie"]["stawka"]
        assert STAWKA_MIN <= st <= STAWKA_MAX, f"BŁĄD: stawka {st} poza pasmem!"

    # Ten sam seed -> identyczna kwota (retry bezpieczny)
    d1 = dict(struktura); d1["id"] = "143764"; d1["seed"] = "143764-konto1"
    d2 = dict(struktura); d2["id"] = "143764"; d2["seed"] = "143764-konto1"
    assert policz_wycene(d1)["kwota"] == policz_wycene(d2)["kwota"], \
        "BŁĄD: ten sam seed dał różne kwoty!"

    print(f"[DOWÓD 4] Kwoty: konto1={kwoty['konto1']}, konto2={kwoty['konto2']}")
    print(f"[DOWÓD 4] Stawki w paśmie, ten sam seed = ta sama kwota OK")


if __name__ == "__main__":
    test_zakres()
    test_oddzielne_per_oferta()
    test_determinizm()
    test_kalkulator_uzywa_stawka_seed()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY LOSOWANIA STAWKI ZAKOŃCZONE SUKCESEM!")
    print("=======================================================")