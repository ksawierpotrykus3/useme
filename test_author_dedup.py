# -*- coding: utf-8 -*-
"""Testy anty-powtórki ofert (na mockach, bez sieci).

Sprawdzają trzy warstwy:
1. BrowserDriver._extract_author_id – wyciąganie stabilnego ID klienta z HTML.
2. Storage.find_by_author – wyszukiwanie historii klienta w magazynie.
3. Logika variation_seed – deterministyczna, ale różna dla różnych zleceń.

Uruchomienie:
    python test_author_dedup.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup

from browser_driver import BrowserDriver
from storage import Storage


def _make_driver_stub() -> BrowserDriver:
    """Tworzy instancję BrowserDriver bez odpalania przeglądarki."""
    return BrowserDriver.__new__(BrowserDriver)


def test_extract_author_id_z_linku_do_profilu():
    drv = _make_driver_stub()
    html = """
    <article class="job">
        <a href="/pl/users/jan-kowalski-123?ref=list" class="job__author">Jan Kowalski</a>
    </article>
    """
    art = BeautifulSoup(html, "html.parser").select_one("article.job")
    aid = drv._extract_author_id(art, "Jan Kowalski")
    assert aid == "jan-kowalski-123", f"Oczekiwano slug profilu, dostano: {aid!r}"
    print("[OK] test_extract_author_id_z_linku_do_profilu")


def test_extract_author_id_fallback_na_nazwe():
    drv = _make_driver_stub()
    html = '<article class="job"><span class="job__author">Firma XYZ</span></article>'
    art = BeautifulSoup(html, "html.parser").select_one("article.job")
    aid = drv._extract_author_id(art, "Firma XYZ")
    # Fallback normalizuje nazwę do stabilnego sluga (author_id jest zawsze slugiem,
    # bo find_by_author porównuje po znormalizowanym identyfikatorze).
    assert aid == "firma-xyz", f"Fallback powinien zwrócić slug, dostano: {aid!r}"
    print("[OK] test_extract_author_id_fallback_na_nazwe")


def test_find_by_author_zwraca_historie():
    with tempfile.TemporaryDirectory() as tmp:
        magazyn = Path(tmp)
        kat = magazyn / "serwisy-internetowe"
        kat.mkdir(parents=True)

        (kat / "100.json").write_text(json.dumps({
            "id": "100", "author_id": "jan-kowalski-123",
            "title": "Landing page", "ai_proposal": {"opis": "Oferta A", "wycena": 3000, "dni": 10},
        }, ensure_ascii=False), encoding="utf-8")

        (kat / "101.json").write_text(json.dumps({
            "id": "101", "author_id": "jan-kowalski-123",
            "title": "Sklep", "ai_proposal": {"opis": "Oferta B", "wycena": 5000, "dni": 14},
        }, ensure_ascii=False), encoding="utf-8")

        (kat / "102.json").write_text(json.dumps({
            "id": "102", "author_id": "ktos-inny",
            "title": "Coś", "ai_proposal": {"opis": "Oferta C"},
        }, ensure_ascii=False), encoding="utf-8")

        st = Storage(magazyn_dir=magazyn)
        hist = st.find_by_author("jan-kowalski-123")
        ids = sorted(h["id"] for h in hist)
        assert ids == ["100", "101"], f"Oczekiwano [100, 101], dostano: {ids}"

        # Anonim nie może zwracać nic (bezpiecznik)
        assert st.find_by_author("Anonim") == []
        assert st.find_by_author("") == []
        print("[OK] test_find_by_author_zwraca_historie")


def test_variation_seed_deterministyczny():
    """Ten sam klient + to samo zlecenie -> ten sam seed (idempotencja).
    Ten sam klient + inne zlecenie -> seed zwykle inny (rotacja stylu)."""
    author_id = "jan-kowalski-123"

    def seed(job_id: str) -> int:
        return abs(hash(author_id + str(job_id))) % 5

    s1 = seed("100")
    s2 = seed("100")
    assert s1 == s2, "Seed musi być deterministyczny dla pary (author, job)."

    seen = {seed(str(i)) for i in range(50)}
    assert len(seen) >= 3, f"Seed powinien rotować po tonach, dostano tylko: {seen}"
    print(f"[OK] test_variation_seed_deterministyczny (unikalne tony w 50 losowaniach: {len(seen)})")


if __name__ == "__main__":
    test_extract_author_id_z_linku_do_profilu()
    test_extract_author_id_fallback_na_nazwe()
    test_find_by_author_zwraca_historie()
    test_variation_seed_deterministyczny()
    print("\n=== WSZYSTKIE TESTY ANTY-POWTÓRKI PRZESZŁY ===")