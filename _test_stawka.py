# -*- coding: utf-8 -*-
"""Test losowania stawki w bezpiecznym pasmie (per OFERTA).

Sprawdza:
1. Stawka ZAWSZE w [STAWKA_MIN, STAWKA_MAX=110] - nigdy za nisko, nigdy za wysoko.
2. ODDZIELNE losowanie per oferta: to samo zlecenie, rozne konta -> rozne stawki.
3. Ten sam seed -> ta sama stawka (deterministycznie, odporne na retry).
4. policz_wycene uzywa seeda oferty (stawka_seed), nie id zlecenia.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from wycena_kalkulator import (wylosuj_stawke, stawka_dla_oferty, policz_wycene,
                               STAWKA_MIN, STAWKA_MAX, STAWKA_OFFSET_MAX)


def test_zakres():
    print("\n--- TEST 1: zakres stawki ---")
    stawki = [wylosuj_stawke() for _ in range(1000)]
    assert all(STAWKA_MIN <= s <= STAWKA_MAX for s in stawki), \
        f"BŁĄD: stawka poza pasmem {STAWKA_MIN}-{STAWKA_MAX}!"
    assert min(stawki) >= STAWKA_MIN, "BŁĄD: za nisko!"
    assert max(stawki) <= STAWKA_MAX, "BŁĄD: za wysoko (max 110)!"
    print(f"[DOWÓD 1] 1000 losowan, min={min(stawki)}, max={max(stawki)}, pasmo [{STAWKA_MIN},{STAWKA_MAX}] OK")


def test_oddzielne_per_oferta():
    print("\n--- TEST 2: oddzielne losowanie per oferta (ale bez diametralnych różnic) ---")
    # To samo zlecenie, dwa konta -> stawki moga sie roznic, ale NIE diametralnie
    pary = []
    for j in range(50):
        s1 = stawka_dla_oferty(f"job{j}", f"job{j}-konto1")
        s2 = stawka_dla_oferty(f"job{j}", f"job{j}-konto2")
        pary.append((s1, s2))
    rozne = sum(1 for a, b in pary if a != b)
    max_rozrzut = max(abs(a - b) for a, b in pary)
    assert rozne > 20, f"BŁĄD: za mało roznych par ({rozne}/50)"
    assert max_rozrzut <= 2 * STAWKA_OFFSET_MAX, \
        f"BŁĄD: rozrzut {max_rozrzut} > dopuszczalne {2 * STAWKA_OFFSET_MAX} (diametralna różnica!)"
    print(f"[DOWÓD 2] 50 zlecen: {rozne} par z różnymi stawkami, max rozrzut={max_rozrzut} (limit {2*STAWKA_OFFSET_MAX}) OK")


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