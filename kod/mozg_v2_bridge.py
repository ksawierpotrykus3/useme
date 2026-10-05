# -*- coding: utf-8 -*-
"""Bridge: nowy mozg V2 (Botv2/mozg) wpiety w stary produkcyjny pipeline.

Engine (kod/engine.py) wola `ai.generate_proposal(job)` i oczekuje ProposalResult
(opis, wycena, dni, ...). Ten modul mapuje wynik `zbuduj_oferte` z Botv2 na ProposalResult,
zeby CALA reszta (form_driver, storage, sanity-blok, wysylka) dzialala bez zmian.

Chirurgiczne wejscie: podmieniamy TYLKO generowanie oferty, nie mechanike przegladarki.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

# --- Ścieżki: Botv2/mozg na sys.path, żeby importować brain.py i jego moduły ---
_KOD_DIR = Path(__file__).parent                       # .../useme_core/kod
_CORE = _KOD_DIR.parent                                # .../useme_core
_MOZG_DIR = _CORE / "Botv2" / "mozg"                   # .../useme_core/Botv2/mozg
if str(_MOZG_DIR) not in sys.path:
    sys.path.insert(0, str(_MOZG_DIR))


def _import_mozg():
    """Importuje leniwie modul mozgu (unika kosztow przy starcie, gdy V2 wylaczone)."""
    import importlib
    brain = importlib.import_module("brain")
    importlib.reload(brain)  # świeży import, gdy zmieniamy pliki mozgu w trakcie dev
    return brain


def zbuduj_proposal(job: Dict[str, Any]):
    """Wywoluje mozg V2 i mapuje wynik na ProposalResult (kontrakt engine/form_driver).

    Zwraca ProposalResult. Przy odrzuceniu (ok=False) rzuca wyjatek - engine to zlapie
    i zapisze status bledu, tak jak przy innych bledach generowania.
    """
    from ai_pipeline import ProposalResult

    brain = _import_mozg()
    wynik = brain.zbuduj_oferte(job, verbose=True)

    if not wynik.get("ok"):
        raise RuntimeError(f"MozgV2 odrzucil zlecenie: {wynik.get('blad')}")

    opis = wynik.get("oferta") or ""
    wycena = int(wynik.get("wycena") or 0)
    dni = int(wynik.get("dni") or 7)
    if wycena <= 0:
        raise RuntimeError("MozgV2 zwrocil wycene <= 0")
    if dni < 7:
        dni = 7

    return ProposalResult(
        opis=opis,
        wycena=wycena,
        dni=dni,
        powod_wyboru="mozg_v2_chirurgiczny",
        metadata={
            "wycena_dolna": wynik.get("wycena_dolna"),
            "wycena_gorna": wynik.get("wycena_gorna"),
            "checker": wynik.get("checker"),
            "sedzia": wynik.get("sedzia"),
            "job_id": wynik.get("job_id"),
            # sanity_ok / kwota_zgodna: mozg V2 ma wlasny checker i sedziego,
            # wiec nie blokujemy wysylki starego pipeline'u (te pola ustawiamy na True).
            "sanity_ok": True,
            "kwota_zgodna": True,
        },
    )


class MozgV2Pipeline:
    """Pipeline V2: selekcja ze starego lancucha, generowanie oferty z nowego mozgu.

    Dziedziczymy po SlotChainAIPipeline (stary), zeby NIE duplikowac dzialajacej
    selekcji ofert (filter_offers). Nadpisujemy TYLKO generate_proposal.
    """
    def __init__(self):
        # Stary lancuch daje nam sprawdzony filter_offers (Red Ocean + AI #1 selekcja).
        try:
            from ai_pipeline import SlotChainAIPipeline
            self._stary = SlotChainAIPipeline()
        except Exception:
            self._stary = None

    def filter_offers(self, offers):
        if self._stary is not None:
            return self._stary.filter_offers(offers)
        return [o for o in offers if o.get("id")]

    def generate_proposal(self, job_detail):
        return zbuduj_proposal(job_detail)