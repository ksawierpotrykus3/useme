# -*- coding: utf-8 -*-
"""Deterministyczny test dowodowy: DOWOD 1 (Konto 2 nie jest martwe).

Test NIE uzywa mockow AI ani przegladarki. Sprawdza wylacznie logike magazynu,
ktora wczesniej blokowala Konto 2:

  BUG (przed naprawa):
    Konto 1 zapisuje zlecenie -> storage.exists() == True.
    Konto 2 pyta storage.exists() -> True -> "juz istnieje, pomijam".
    Efekt: Konto 2 nie zapisze zadnej oferty na to samo zlecenie.

  POPRAWKA (po naprawie):
    Pomin tylko, gdy TO KONKRETNE konto juz oferowalo (czy_konto_juz_oferowalo).
    Konto 2 ma zlozyc wlasna oferte na to samo zlecenie co Konto 1.

Uruchom: python _test_multi_konto_przeplyw.py
"""

import tempfile
from pathlib import Path

from storage import Storage


def test_konto2_nie_jest_martwe():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        storage = Storage(magazyn_dir=tmp)
        job_id = "12345"

        # --- Konto 1: pobiera zlecenie, zapisuje i wysyla oferte ---
        job = {"id": job_id, "url": "https://useme.com/pl/jobs/12345/",
               "title": "Zlecenie testowe", "category": "programowanie-i-it",
               "author_id": "klient_x"}
        assert not storage.exists(job_id), "Na starcie magazyn musi byc pusty."
        storage.save_new_job(job, job["category"])

        # Konto 1 zapisuje swoja oferte.
        storage.zapisz_oferte(job_id, {"job_id": job_id, "konto": "konto1",
                                       "opis": "Oferta konta 1", "wycena": 3000})

        # --- Symulacja logiki z engine.py dla Konta 2 ---
        # Konto 2 widzi, ze zlecenie jest w magazynie (exists == True)...
        assert storage.exists(job_id), "Zlecenie zapisane przez Konto 1 musi byc w magazynie."

        # ...ale NIE pomija go, bo sprawdza per konto, nie globalnie.
        konto2_juz_oferowalo = storage.czy_konto_juz_oferowalo(job_id, "konto2")
        assert konto2_juz_oferowalo is False, \
            "BUG: Konto 2 pomija zlecenie tylko dlatego, ze Konto 1 je zapisalo!"

        # Konto 2 zapisuje wlasna oferte na TO SAMO zlecenie.
        storage.zapisz_oferte(job_id, {"job_id": job_id, "konto": "konto2",
                                       "opis": "Oferta konta 2", "wycena": 2500})

        # --- Weryfikacja: obie oferty istnieja na tym samym zleceniu ---
        rekord = storage.load_job(job_id)
        konta = sorted(o.get("konto") for o in rekord.get("oferty", []))
        assert konta == ["konto1", "konto2"], f"Oczekiwano obu kont, jest: {konta}"

        # --- Zabezpieczenie: to samo konto NIE moze oferowac dwa razy ---
        assert storage.czy_konto_juz_oferowalo(job_id, "konto2") is True
        assert storage.czy_konto_juz_oferowalo(job_id, "konto1") is True

        print("[SUKCES] DOWOD 1: Konto 2 zlozylo wlasna oferte na to samo zlecenie co Konto 1.")
        print(f"          Oferty na zleceniu {job_id}: {konta}")


if __name__ == "__main__":
    test_konto2_nie_jest_martwe()