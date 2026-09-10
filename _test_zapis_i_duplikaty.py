# -*- coding: utf-8 -*-
"""Test #3 (zapis ofert per konto z metadanymi) i #4 (globalny wykrywacz duplikatow)."""

import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from storage import Storage
from ai_pipeline import sprawdz_globalne_duplikaty, _podobienstwo_jaccard


def test_zapis_oferty_per_konto():
    print("\n--- TEST #3: zapis ofert per konto z metadanymi ---")
    with tempfile.TemporaryDirectory() as tmp:
        st = Storage(magazyn_dir=Path(tmp))
        st.save_new_job({"id": "5001", "title": "Aplikacja", "author": "Klient",
                         "author_id": "klient", "url": "http://x/5001"}, "programowanie-i-it")

        # Dwie oferty na to samo zlecenie, z roznych kont, rozne tryby
        st.zapisz_oferte("5001", {"job_id": "5001", "konto": "konto1", "tryb": "konserwatywny",
                                  "wycena": 5000, "dni": 10, "stawka": 83, "opis": "Oferta A"})
        st.zapisz_oferte("5001", {"job_id": "5001", "konto": "konto2", "tryb": "meta",
                                  "wycena": 5500, "dni": 12, "stawka": 95, "opis": "Oferta B"})

        job = st.load_job("5001")
        oferty = job.get("oferty") or []
        assert len(oferty) == 2, f"BŁĄD: powinny być 2 oferty, jest {len(oferty)}"
        assert oferty[0]["konto"] == "konto1" and oferty[0]["tryb"] == "konserwatywny"
        assert oferty[1]["konto"] == "konto2" and oferty[1]["tryb"] == "meta"
        assert oferty[0]["stawka"] == 83 and oferty[1]["stawka"] == 95
        assert "zapisano_at" in oferty[0], "BŁĄD: brak znacznika czasu!"

        # Deduplikacja per konto
        assert st.czy_konto_juz_oferowalo("5001", "konto1") is True
        assert st.czy_konto_juz_oferowalo("5001", "konto2") is True
        assert st.czy_konto_juz_oferowalo("5001", "konto3") is False
        print(f"[DOWÓD #3] 2 oferty zapisane z kontem i trybem: konto1/konserwatywny, konto2/meta")
        print(f"[DOWÓD #3] czy_konto_juz_oferowalo: konto1={st.czy_konto_juz_oferowalo('5001','konto1')}, konto3={st.czy_konto_juz_oferowalo('5001','konto3')}")


def test_find_by_account():
    print("\n--- TEST #3b: find_by_account ---")
    with tempfile.TemporaryDirectory() as tmp:
        st = Storage(magazyn_dir=Path(tmp))
        st.save_new_job({"id": "6001", "title": "A", "author": "K", "author_id": "k",
                         "url": "http://x/6001"}, "programowanie-i-it")
        st.save_new_job({"id": "6002", "title": "B", "author": "K", "author_id": "k",
                         "url": "http://x/6002"}, "programowanie-i-it")
        st.zapisz_oferte("6001", {"konto": "konto1", "opis": "x"})
        st.zapisz_oferte("6002", {"konto": "konto2", "opis": "y"})

        k1 = st.find_by_account("konto1")
        k2 = st.find_by_account("konto2")
        assert len(k1) == 1 and k1[0]["id"] == "6001", f"BŁĄD: konto1 powinno mieć 6001, ma {[w['id'] for w in k1]}"
        assert len(k2) == 1 and k2[0]["id"] == "6002", f"BŁĄD: konto2 powinno mieć 6002"
        print(f"[DOWÓD #3b] find_by_account: konto1->{ [w['id'] for w in k1] }, konto2->{ [w['id'] for w in k2] }")


def test_globalne_duplikaty():
    print("\n--- TEST #4: globalny wykrywacz duplikatow ---")
    with tempfile.TemporaryDirectory() as tmp:
        st = Storage(magazyn_dir=Path(tmp))
        st.save_new_job({"id": "7001", "title": "A", "author": "A", "author_id": "a",
                         "url": "http://x/7001"}, "programowanie-i-it")
        st.save_new_job({"id": "7002", "title": "B", "author": "B", "author_id": "b",
                         "url": "http://x/7002"}, "programowanie-i-it")

        baza = ("Dzień dobry, zrealizuję sklep WordPress z bezpiecznym streamingiem audio "
                "i integracją płatności Stripe oraz pełną migracją bazy klientów z OpenCart.")
        # Oferta 7001 - bazowa
        st.zapisz_oferte("7001", {"job_id": "7001", "konto": "konto1", "opis": baza})

        # Nowa oferta praktycznie identyczna -> powinna zostac wykryta
        identyczna = baza.replace("Dzień dobry", "Cześć")
        dups = sprawdz_globalne_duplikaty(identyczna, st, wlasne_job_id="7002")
        assert len(dups) >= 1, f"BŁĄD: nie wykryto duplikatu! dups={dups}"
        assert any(d["job_id"] == "7001" for d in dups), "BŁĄD: brak 7001 w duplikatach"
        print(f"[DOWÓD #4] Wykryto duplikat: {dups}")

        # Oferta zupelnie inna -> brak flag
        inna = ("Hej, robimy aplikacje mobilne Flutter. Zbudujemy odtwarzacz audio w tle, "
                "logowanie, koszyk i płatności BLIK. Backend Node.js, deploy na VPS.")
        dups2 = sprawdz_globalne_duplikaty(inna, st, wlasne_job_id="7002")
        assert len(dups2) == 0, f"BŁĄD: fałszywy alarm dla różnej oferty! {dups2}"
        print(f"[DOWÓD #4] Różna oferta -> brak flag (dups={dups2})")


def test_wlasne_job_id_wykluczone():
    print("\n--- TEST #4b: wlasne job_id wykluczone z porownania ---")
    with tempfile.TemporaryDirectory() as tmp:
        st = Storage(magazyn_dir=Path(tmp))
        st.save_new_job({"id": "8001", "title": "A", "author": "a", "author_id": "a",
                         "url": "http://x/8001"}, "programowanie-i-it")
        baza = "Dzień dobry, zrealizuję sklep WordPress z bezpiecznym streamingiem audio i płatnościami."
        st.zapisz_oferte("8001", {"job_id": "8001", "konto": "konto1", "opis": baza})
        # Sprawdzamy te sama oferte, ale z wlasne_job_id=8001 -> nie powinna flagowac samej siebie
        dups = sprawdz_globalne_duplikaty(baza, st, wlasne_job_id="8001")
        assert len(dups) == 0, f"BŁĄD: oferta porownala sie sama ze soba! {dups}"
        print(f"[DOWÓD #4b] Ta sama oferta nie flaguje siebie (dups={dups})")


if __name__ == "__main__":
    test_zapis_oferty_per_konto()
    test_find_by_account()
    test_globalne_duplikaty()
    test_wlasne_job_id_wykluczone()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY (#3 + #4) ZAKOŃCZONE SUKCESEM!")
    print("=======================================================")