# -*- coding: utf-8 -*-
"""Test integracyjny CAŁEGO pipeline'u na mockach (bez sieci, bez przeglądarki, bez AI).

To nie jest test pojedynczej funkcji. Odpalamy engine.run_pipeline od początku
do końca, podmieniając tylko zewnętrzne zależności (przeglądarka, formularz, AI).
Sprawdzamy, czy przy dwóch zleceniach TEGO SAMEGO klienta, drugie dostaje
wstrzyknięte previous_offers — czyli że cała ścieżka anty-powtórki faktycznie działa.
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import engine
from ai_pipeline import ProposalResult
from storage import Storage


def test_7_pelny_pipeline_wykrywa_powtorke():
    """Test 7: End-to-end run_pipeline — dwa zlecenia tego samego klienta."""
    print("\n--- TEST 7: Pełny pipeline (end-to-end) ---")

    # --- FAKE przeglądarka ---
    class FakePage:
        def goto(self, *a, **k): pass
        def close(self): pass
        def content(self): return ""

    class FakeContext:
        def new_page(self): return FakePage()

    class FakeDriver:
        def __init__(self, *a, **k): self.context = FakeContext()
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def dismiss_cookie_banner(self, p): pass
        def check_logged_in(self, p): return True
        def fetch_category_jobs(self, cat_key, max_jobs=None):
            if cat_key != "programowanie-i-it":
                return []
            return [
                {"id": "7001", "url": "https://useme.com/pl/jobs/7001/", "title": "Strona www",
                 "budget": "3000", "author": "Firma Testowa", "author_id": "firma-testowa",
                 "short_desc": "opis", "category": "programowanie-i-it"},
                {"id": "7002", "url": "https://useme.com/pl/jobs/7002/", "title": "Sklep online",
                 "budget": "4000", "author": "Firma Testowa", "author_id": "firma-testowa",
                 "short_desc": "opis", "category": "programowanie-i-it"},
            ]
        def fetch_job_details(self, url):
            return {"url": url, "title": "Detal", "full_description": "Pełny opis zlecenia " * 20,
                    "author": "Firma Testowa", "author_id": "firma-testowa",
                    "has_add_offer_button": True, "add_offer_href": "/x"}

    # --- FAKE formularz ---
    class FakeForm:
        def __init__(self, *a, **k): pass
        def fill_and_prepare_offer(self, job_id, proposal):
            return {"job_id": job_id, "status": "DRY_RUN_OK", "message": "ok"}

    # --- FAKE AI: notuje, co dostał ---
    class FakeAI:
        def __init__(self):
            self.seen = []
            self.n = 0
        def filter_offers(self, offers): return list(offers)
        def generate_proposal(self, job):
            self.seen.append(dict(job))
            self.n += 1
            return ProposalResult(opis=f"Unikalna oferta numer {self.n} dla klienta.", wycena=2000, dni=7)

    # --- FAKE Chain (Cortex) ---
    class FakeStep:
        def __init__(self): self.wyjscie = ""; self.narzedzie = ""
        def log(self, *a): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
    class FakeChain:
        def __init__(self, *a, **k): pass
        def step(self, *a, **k): return FakeStep()

    fake_ai = FakeAI()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_storage = Storage(magazyn_dir=Path(tmp))
        with patch.object(engine, "BrowserDriver", FakeDriver), \
             patch.object(engine, "FormDriver", FakeForm), \
             patch.object(engine, "Chain", FakeChain), \
             patch.object(engine, "Storage", lambda: tmp_storage), \
             patch.object(engine, "get_ai_pipeline", lambda: fake_ai):
            raport = engine.run_pipeline(dry_run=True)

    assert len(fake_ai.seen) == 2, f"BŁĄD: AI powinno dostać 2 zlecenia, dostało {len(fake_ai.seen)}"

    pierwsze, drugie = fake_ai.seen[0], fake_ai.seen[1]

    # Pierwsze zlecenie: klient nowy -> brak poprzednich ofert
    assert pierwsze.get("previous_offers") == [], \
        f"BŁĄD: Pierwsze zlecenie nie powinno mieć previous_offers, ma {pierwsze.get('previous_offers')}"

    # Drugie zlecenie: ten sam klient -> MUSI mieć previous_offers z ofertą #7001
    prev = drugie.get("previous_offers") or []
    assert len(prev) >= 1, f"BŁĄD KRYTYCZNY: Drugie zlecenie nie dostało previous_offers! Ma: {prev}"
    assert any(str(p.get("job_id")) == "7001" for p in prev), \
        f"BŁĄD: W previous_offers brakuje oferty #7001! Jest: {[p.get('job_id') for p in prev]}"
    assert any((p.get("opis") or "").strip() for p in prev), "BŁĄD: Poprzednia oferta nie ma treści do porównania!"
    assert 0 <= drugie.get("variation_seed", -1) <= 4, "BŁĄD: Zły variation_seed!"

    print(f"Zlecenie #7001 previous_offers: {len(pierwsze.get('previous_offers'))}")
    print(f"Zlecenie #7002 previous_offers: {[p.get('job_id') for p in prev]}, seed={drugie.get('variation_seed')}")
    print(f"Raport pipeline'u: nowe={raport['nowe_zlecenia']}, przetworzone={raport['przetworzone']}")
    print("[DOWÓD 7] Cały pipeline zadziałał: drugie zlecenie tego samego klienta dostało kontekst anty-powtórki.")


if __name__ == "__main__":
    test_7_pelny_pipeline_wykrywa_powtorke()
    print("\n=======================================================")
    print("TEST INTEGRACYJNY END-TO-END ZAKOŃCZONY SUKCESEM!")
    print("=======================================================")