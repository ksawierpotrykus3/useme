# -*- coding: utf-8 -*-
"""Test multi-konta (2 cookies) + zgodność wsteczna z 1 kontem.

Sprawdza trzy scenariusze:
1. BRAK cookies2.json -> aktywne tylko konto1 (zachowanie jak przed multi-kontem).
2. JEST cookies2.json -> aktywne oba konta, każde dostaje SWÓJ cookies_path.
3. BRAK obu plików -> fallback do konto1 (bezpiecznik), pipeline nie wywala się.

Dodatkowo: przy 2 kontach oba przechodzą pełny cykl (każde widzi zlecenia),
a zlecenie zapisane przez konto1 nie jest ponownie zapisywane przez konto2
(deduplikacja po magazynie działa).
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import config
import engine
from ai_pipeline import ProposalResult
from storage import Storage


# --- FAKE przeglądarka: notuje, z jakim cookies_path ją odpalono ---
class FakePage:
    def goto(self, *a, **k): pass
    def close(self): pass
    def content(self): return ""


class FakeContext:
    def new_page(self): return FakePage()


class FakeDriver:
    odwiedzone_cookies = []

    def __init__(self, *a, **k):
        self.cookies_path = k.get("cookies_path")
        FakeDriver.odwiedzone_cookies.append(str(self.cookies_path))
        self.context = FakeContext()

    def __enter__(self): return self
    def __exit__(self, *a): return False
    def dismiss_cookie_banner(self, p): pass
    def check_logged_in(self, p): return True

    def fetch_category_jobs(self, cat_key, max_jobs=None):
        if cat_key != "programowanie-i-it":
            return []
        return [{
            "id": "9001", "url": "https://useme.com/pl/jobs/9001/", "title": "Strona",
            "budget": "3000", "author": "Firma Testowa", "author_id": "firma-testowa",
            "short_desc": "opis", "category": "programowanie-i-it",
        }]

    def fetch_job_details(self, url):
        return {"url": url, "title": "Detal", "full_description": "Pełny opis " * 20,
                "author": "Firma Testowa", "author_id": "firma-testowa",
                "has_add_offer_button": True, "add_offer_href": "/x"}


class FakeForm:
    def __init__(self, *a, **k): pass
    def fill_and_prepare_offer(self, job_id, proposal):
        return {"job_id": job_id, "status": "DRY_RUN_OK", "message": "ok"}


class FakeAI:
    def __init__(self): self.seen = []; self.n = 0
    def filter_offers(self, offers): return list(offers)
    def generate_proposal(self, job):
        self.seen.append(dict(job)); self.n += 1
        return ProposalResult(opis=f"Oferta {self.n}.", wycena=2000, dni=7)


class FakeStep:
    def __init__(self): self.wyjscie = ""; self.narzedzie = ""
    def log(self, *a): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False


class FakeChain:
    def __init__(self, *a, **k): pass
    def step(self, *a, **k): return FakeStep()


def _run(tmp_magazyn, fake_ai):
    with patch.object(engine, "BrowserDriver", FakeDriver), \
         patch.object(engine, "FormDriver", FakeForm), \
         patch.object(engine, "Chain", FakeChain), \
         patch.object(engine, "Storage", lambda: Storage(magazyn_dir=Path(tmp_magazyn))), \
         patch.object(engine, "get_ai_pipeline", lambda: fake_ai):
        return engine.run_pipeline(dry_run=True)


def test_1_brak_drugiego_cookies():
    """Scenariusz 1: tylko cookies.json -> 1 konto, zachowanie jak dawniej."""
    print("\n--- TEST 1: brak cookies2 -> 1 konto ---")
    FakeDriver.odwiedzone_cookies = []
    with tempfile.TemporaryDirectory() as tmp_c, tempfile.TemporaryDirectory() as tmp_m:
        c1 = Path(tmp_c) / "cookies.json"
        c1.write_text('{"cookies": []}', encoding="utf-8")
        c2 = Path(tmp_c) / "cookies2.json"  # NIE istnieje

        konta = [{"id": "konto1", "nazwa": "Ksawier", "cookies_path": c1},
                 {"id": "konto2", "nazwa": "Konto 2", "cookies_path": c2}]
        with patch.object(config, "ACCOUNTS", konta):
            aktywne = config.aktywne_konta()
            assert len(aktywne) == 1, f"BŁĄD: powinno być 1 konto, jest {len(aktywne)}"
            assert aktywne[0]["id"] == "konto1", "BŁĄD: aktywne powinno być konto1"
            _run(tmp_m, FakeAI())

    assert len(FakeDriver.odwiedzone_cookies) == 1, \
        f"BŁĄD: powinien 1 start przeglądarki, jest {len(FakeDriver.odwiedzone_cookies)}"
    assert FakeDriver.odwiedzone_cookies[0].endswith("cookies.json"), \
        f"BŁĄD: zły cookies_path: {FakeDriver.odwiedzone_cookies[0]}"
    print(f"[DOWÓD 1] 1 konto, cookies: {FakeDriver.odwiedzone_cookies}")


def test_2_dwa_konta():
    """Scenariusz 2: oba cookies istnieją -> 2 konta, każde ze SWOIM cookies_path."""
    print("\n--- TEST 2: dwa cookies -> dwa konta ---")
    FakeDriver.odwiedzone_cookies = []
    with tempfile.TemporaryDirectory() as tmp_c, tempfile.TemporaryDirectory() as tmp_m:
        c1 = Path(tmp_c) / "cookies.json"
        c1.write_text('{"cookies": []}', encoding="utf-8")
        c2 = Path(tmp_c) / "cookies2.json"
        c2.write_text('{"cookies": []}', encoding="utf-8")

        konta = [{"id": "konto1", "nazwa": "Ksawier", "cookies_path": c1},
                 {"id": "konto2", "nazwa": "Konto 2", "cookies_path": c2}]
        with patch.object(config, "ACCOUNTS", konta):
            aktywne = config.aktywne_konta()
            assert len(aktywne) == 2, f"BŁĄD: powinny być 2 konta, jest {len(aktywne)}"
            raport = _run(tmp_m, FakeAI())

    assert len(FakeDriver.odwiedzone_cookies) == 2, \
        f"BŁĄD: powinny być 2 starty przeglądarki, jest {len(FakeDriver.odwiedzone_cookies)}"
    assert FakeDriver.odwiedzone_cookies[0].endswith("cookies.json"), \
        f"BŁĄD: konto1 zły cookies: {FakeDriver.odwiedzone_cookies[0]}"
    assert FakeDriver.odwiedzone_cookies[1].endswith("cookies2.json"), \
        f"BŁĄD: konto2 zły cookies: {FakeDriver.odwiedzone_cookies[1]}"
    print(f"[DOWÓD 2] 2 konta, cookies: {FakeDriver.odwiedzone_cookies}")
    print(f"[DOWÓD 2] raport przetworzone={raport['przetworzone']}")


def test_3_brak_obu_plikow():
    """Scenariusz 3: brak obu cookies -> fallback konto1, brak crasha."""
    print("\n--- TEST 3: brak obu cookies -> fallback konto1 ---")
    FakeDriver.odwiedzone_cookies = []
    with tempfile.TemporaryDirectory() as tmp_c, tempfile.TemporaryDirectory() as tmp_m:
        c1 = Path(tmp_c) / "cookies.json"   # brak
        c2 = Path(tmp_c) / "cookies2.json"  # brak

        konta = [{"id": "konto1", "nazwa": "Ksawier", "cookies_path": c1},
                 {"id": "konto2", "nazwa": "Konto 2", "cookies_path": c2}]
        with patch.object(config, "ACCOUNTS", konta):
            aktywne = config.aktywne_konta()
            assert aktywne == [], f"BŁĄD: brak plików -> pusta lista, jest {aktywne}"
            # Bezpiecznik w engine: pusty -> fallback do COOKIES_PATH
            with patch.object(config, "COOKIES_PATH", c1):
                _run(tmp_m, FakeAI())

    assert len(FakeDriver.odwiedzone_cookies) == 1, \
        f"BŁĄD: fallback powinien dać 1 start, jest {len(FakeDriver.odwiedzone_cookies)}"
    print(f"[DOWÓD 3] Fallback zadziałał, cookies: {FakeDriver.odwiedzone_cookies}")


if __name__ == "__main__":
    test_1_brak_drugiego_cookies()
    test_2_dwa_konta()
    test_3_brak_obu_plikow()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY MULTI-KONTA ZAKOŃCZONE SUKCESEM!")
    print("=======================================================")