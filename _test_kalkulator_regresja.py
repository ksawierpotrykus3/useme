# -*- coding: utf-8 -*-
"""Test regresyjny kalkulatora: duze zlecenie z landingiem NIE moze byc przyciete do 25h.

Bug: gdy w nazwach modulow byla fraza 'landing'/'one-page', kalkulator przycinal
CALE zlecenie do CAP_ONE_PAGE_H (25h), przez co duzy projekt (aplikacja mobilna +
panel + landing) byl wyceniany jak sam landing (np. 4500 zl zamiast kilkudziesieciu tys.).
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from wycena_kalkulator import policz_wycene, CAP_ONE_PAGE_H


def test_duzy_projekt_z_landingiem_nie_jest_przyciety():
    print("\n--- TEST: duzy projekt z landingiem (regresja) ---")
    # Odtwarzamy realny przypadek z syntetycznego zlecenia (aplikacja mobilna + landing).
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "TEST-0001",
        "moduly": [
            {"nazwa": "Aplikacja mobilna klienta (Flutter: ekrany, nawigacja)", "godziny_real": 120},
            {"nazwa": "Panel admina rozbudowany (restauracja: menu, zamowienia)", "godziny_real": 20},
            {"nazwa": "Integracja platnosci (Stripe/Przelewy24)", "godziny_real": 16},
            {"nazwa": "Landing page / One-Page (prosta strona www)", "godziny_real": 22},
        ],
        "flagi": {"wiek_ofert_dni": 0, "liczba_ofert": 5, "brak_specyfikacji": True},
    }
    w = policz_wycene(struktura)
    godziny = w["rozbicie"]["godziny_real"]
    print(f"Godziny po korekcie: {godziny}h, kwota: {w['kwota']} zl")

    # Suma modulow = 178h. Landing sam (22h) jest ponizej capu, wiec nic nie przycinamy.
    assert godziny >= 150, f"BŁĄD KRYTYCZNY: duzy projekt przycięty do {godziny}h (bug powrócił!)"
    assert w["kwota"] > 20000, f"BŁĄD: kwota {w['kwota']} zl jest za niska dla duzego projektu"
    print(f"[DOWÓD] Duzy projekt z landingiem nie jest przyciety do {CAP_ONE_PAGE_H}h. OK")


def test_czysty_landing_nadal_przyciety():
    print("\n--- TEST: czysty landing nadal ma cap 25h ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "LAND-1",
        "moduly": [
            {"nazwa": "Landing page / One-Page", "godziny_real": 60},
        ],
        "flagi": {"wiek_ofert_dni": 0, "liczba_ofert": 5},
    }
    w = policz_wycene(struktura)
    godziny = w["rozbicie"]["godziny_real"]
    assert godziny == CAP_ONE_PAGE_H, f"BŁĄD: czysty landing powinien byc capniety do {CAP_ONE_PAGE_H}h, jest {godziny}h"
    print(f"[DOWÓD] Czysty landing przyciety do {godziny}h. OK")


def test_modul_landing_przyciety_reszta_nie():
    print("\n--- TEST: modul landing > cap, reszta bez zmian ---")
    struktura = {
        "typ_zlecenia": "projekt",
        "id": "MIX-1",
        "moduly": [
            {"nazwa": "Backend API", "godziny_real": 40},
            {"nazwa": "Landing page / One-Page", "godziny_real": 50},  # przekracza cap 25
        ],
        "flagi": {"wiek_ofert_dni": 0, "liczba_ofert": 5},
    }
    w = policz_wycene(struktura)
    godziny = w["rozbicie"]["godziny_real"]
    # Backend 40 + landing przycięty do 25 = 65
    assert godziny == 65, f"BŁĄD: oczekiwano 65h (40 + 25), jest {godziny}h"
    print(f"[DOWÓD] Modul landing przyciety do capu, backend bez zmian (65h). OK")


if __name__ == "__main__":
    test_duzy_projekt_z_landingiem_nie_jest_przyciety()
    test_czysty_landing_nadal_przyciety()
    test_modul_landing_przyciety_reszta_nie()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY REGRESJI KALKULATORA ZAKOŃCZONE SUKCESEM!")
    print("=======================================================")