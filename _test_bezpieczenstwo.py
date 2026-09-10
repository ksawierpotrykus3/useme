# -*- coding: utf-8 -*-
"""Testy bezpieczeństwa operacyjnego: kill switch, limit dzienny, limiter czasu."""

import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import config
import bezpieczenstwo


def test_kill_switch():
    print("\n--- TEST: kill switch (plik STOP) ---")
    with tempfile.TemporaryDirectory() as tmp:
        stop = Path(tmp) / "STOP"
        import types
        orig = config.STOP_FILE
        try:
            config.STOP_FILE = stop
            assert bezpieczenstwo.czy_stop() is False, "BŁĄD: brak pliku -> False"
            stop.write_text("stop", encoding="utf-8")
            assert bezpieczenstwo.czy_stop() is True, "BŁĄD: plik istnieje -> True"
            stop.unlink()
            assert bezpieczenstwo.czy_stop() is False, "BŁĄD: usunięty -> False"
        finally:
            config.STOP_FILE = orig
    print("[DOWÓD] Kill switch działa: brak pliku=False, jest plik=True, usunięty=False")


def test_licznik_dzienny():
    print("\n--- TEST: licznik dzienny ---")
    with tempfile.TemporaryDirectory() as tmp:
        orig_dir = config.MAGAZYN_DIR
        try:
            config.MAGAZYN_DIR = Path(tmp)
            bezpieczenstwo.STAN_FILE = Path(tmp) / ".bezpieczenstwo.json"

            assert bezpieczenstwo.pobierz_licznik_dzienny() == 0

            for i in range(3):
                bezpieczenstwo.zapisz_wyslana_oferte()
            assert bezpieczenstwo.pobierz_licznik_dzienny() == 3, "BŁĄD: licznik statystyczny powinien wynosic 3"
        finally:
            config.MAGAZYN_DIR = orig_dir
    print("[DOWÓD] Licznik statystyczny: 0 -> 3")


def test_reset_licznika_nowy_dzien():
    print("\n--- TEST: reset licznika nowego dnia ---")
    with tempfile.TemporaryDirectory() as tmp:
        bezpieczenstwo.STAN_FILE = Path(tmp) / ".bezpieczenstwo.json"
        # Recznie zapisz stan z wczoraj
        import json
        bezpieczenstwo.STAN_FILE.write_text(
            json.dumps({"data": "2000-01-01", "wyslane_dzis": 99}), encoding="utf-8")
        assert bezpieczenstwo.pobierz_licznik_dzienny() == 0, "BŁĄD: wczorajszy licznik powinien byc 0"
    print("[DOWÓD] Wczorajszy licznik zignorowany -> 0 (nowy dzien)")


def test_run_limiter():
    print("\n--- TEST: limiter czasu runu ---")
    lim = bezpieczenstwo.RunLimiter(max_minutes=1)
    assert lim.przekroczono() is False, "BŁĄD: swiezy limiter nie przekroczony"
    # Symuluj uplyw czasu
    lim.start = time.time() - 120  # 2 min temu
    assert lim.przekroczono() is True, "BŁĄD: po 2 min powinien byc przekroczony"
    print("[DOWÓD] Limiter: swiezy=False, po 2 min (limit 1 min)=True")


if __name__ == "__main__":
    test_kill_switch()
    test_licznik_dzienny()
    test_reset_licznika_nowy_dzien()
    test_run_limiter()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY BEZPIECZEŃSTWA ZAKOŃCZONE SUKCESEM!")
    print("=======================================================")