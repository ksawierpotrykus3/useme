# -*- coding: utf-8 -*-
"""Monitor dostępności portalu Useme.

Wydzielony z kod/engine.py zgodnie z werdyktem Sądu Segregacji Kuratora.
Sprawdza dostępność serwisu Useme (status 200) z obsługą kodów 503 ('Oops!')
i wznawia działanie bota po przywróceniu sprawności platformy.
"""

from __future__ import annotations

import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import bezpieczenstwo


def czekaj_na_dostepnosc_useme(interval_s: int = 60, max_prob: int = 180) -> bool:
    """Sprawdza co interval_s sekund, czy portal Useme działa (status 200).
    
    W przypadku awarii serwerowej (HTTP 503 'Oops!'), bot samoczynnie odczekuje
    i sprawdza portal co minutę, ruszając natychmiast po jego przywróceniu.
    """
    from curl_cffi import requests as cffi_requests
    print("[USEME MONITOR] Weryfikuję dostępność portalu Useme...", flush=True)
    for proba in range(1, max_prob + 1):
        if bezpieczenstwo.czy_stop():
            print("[STOP] Wykryto plik STOP podczas oczekiwania na Useme.", flush=True)
            return False
        try:
            r = cffi_requests.get("https://useme.com/pl/", impersonate="chrome120", timeout=15)
            if r.status_code == 200 and "error-page" not in r.text.lower() and "oops" not in r.text.lower():
                print(f"[USEME ONLINE] Portal Useme działa poprawnie (status 200). Uruchamiam proces!", flush=True)
                return True
            else:
                print(f"[USEME OFFLINE] Portal Useme niedostępny (HTTP {r.status_code}, 'Oops!'). Czekam {interval_s}s... (próba {proba}/{max_prob})", flush=True)
        except Exception as e:
            print(f"[USEME OFFLINE] Błąd połączenia ({e}). Czekam {interval_s}s... (próba {proba}/{max_prob})", flush=True)
        time.sleep(interval_s)
    return False
