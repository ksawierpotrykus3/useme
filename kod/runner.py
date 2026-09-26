# -*- coding: utf-8 -*-
"""Struktura kroków łańcucha (bez telemetrii Cortexa).

Klasa `Chain` opakowuje kolejne kroki bota w czytelne bloki:

    chain = Chain("useme-bot", "Automatyczna Ofertowarka")

    with chain.step("Weryfikacja sesji", typ="kod") as krok:
        krok.log("Sprawdzam...")
        krok.wyjscie = "OK"

Krok niesie nazwę, status (`w_toku` / `zrobione` / `blad` / `czeka_na_ciebie`),
logi, wejście/wyjście, prompty i reasoning. Wszystko żyje w pamięci procesu —
żaden plik stanu nie jest zapisywany, żaden zewnętrzny supervisor tego nie czyta.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional


class Krok:
    def __init__(self, nazwa: str, typ: str, opis: str = ""):
        self.nazwa = nazwa
        self.typ = typ
        self.opis = opis
        self.status = "w_toku"
        self._start = time.time()
        self.narzedzie: Optional[str] = None
        self.wejscie: Optional[str] = None
        self.promptSystem: Optional[str] = None
        self.promptUser: Optional[str] = None
        self.wyjscie: Optional[str] = None
        self._wyjscie_chunks: List[str] = []
        self.reasoning: Optional[str] = None
        self.logi: List[str] = []

    def czekaj_na_ciebie(self) -> None:
        self.status = "czeka_na_ciebie"

    def log(self, wiadomosc: str) -> None:
        self.logi.append(wiadomosc)

    def stream(self, fragment: str) -> None:
        """Dokleja fragment wyniku AI do pola `wyjscie` (podglad na zywo w pamięci)."""
        self._wyjscie_chunks.append(fragment)
        self.wyjscie = "".join(self._wyjscie_chunks)

    def finalizuj_wynik(self, tresc: str) -> None:
        """Ustawia pełny, końcowy wynik (nadpisuje stream)."""
        self.wyjscie = tresc

    def to_dict(self, index: int) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": index,
            "nazwa": self.nazwa,
            "typ": self.typ,
            "status": self.status,
        }
        if self.opis:
            d["opis"] = self.opis
        if self.narzedzie:
            d["narzedzie"] = self.narzedzie
        if self.wejscie:
            d["wejscie"] = self.wejscie
        if self.promptSystem:
            d["promptSystem"] = self.promptSystem
        if self.promptUser:
            d["promptUser"] = self.promptUser
        if self.wyjscie:
            d["wyjscie"] = self.wyjscie
        if self.reasoning:
            d["reasoning"] = self.reasoning
        if self.logi:
            d["logi"] = self.logi
        d["czas_trwania_s"] = round(time.time() - self._start, 1)
        return d


class Chain:
    def __init__(self, id: str, nazwa: str,
                 opis: str = "", silnik: str = "", wyzwalacz: str = "manual",
                 parent_id: Optional[str] = None, parent_step: Optional[str] = None):
        self.id = id
        self.nazwa = nazwa
        self.opis = opis
        self.silnik = silnik
        self.wyzwalacz = wyzwalacz
        self.parent_id = parent_id
        self.parent_step = parent_step
        self.kroki: List[Krok] = []

    @contextmanager
    def step(self, nazwa: str, typ: str = "ai", opis: str = "") -> Iterator[Krok]:
        krok = Krok(nazwa, typ, opis)
        self.kroki.append(krok)
        try:
            yield krok
        except Exception as e:
            krok.status = "blad"
            krok.log(f"[BŁĄD KROKU] {type(e).__name__}: {e}")
            if not krok.wyjscie:
                krok.wyjscie = f"BŁĄD: {type(e).__name__}: {e}"
            raise
        else:
            # Nadpisz na zrobione tylko jeśli nikt nie ustawił bramki.
            if krok.status == "w_toku":
                krok.status = "zrobione"

    def _zapisz(self) -> None:
        """No-op — struktura kroków żyje w pamięci, nie ma stanu na dysku."""
        return None

    def _status_ogolny(self) -> str:
        if not self.kroki:
            return "oczekuje"
        statusy = [k.status for k in self.kroki]
        if "blad" in statusy:
            return "blad"
        if "w_toku" in statusy:
            return "w_toku"
        if "czeka_na_ciebie" in statusy:
            return "czeka_na_ciebie"
        if all(s == "zrobione" for s in statusy):
            return "zakonczono"
        return "oczekuje"

    def _to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": self.id,
            "nazwa": self.nazwa,
            "kroki": [k.to_dict(i + 1) for i, k in enumerate(self.kroki)],
            "status_ogolny": self._status_ogolny(),
        }
        if self.opis:
            d["opis"] = self.opis
        if self.silnik:
            d["silnik"] = self.silnik
        if self.parent_id:
            d["parent_id"] = self.parent_id
        if self.parent_step:
            d["parent_step"] = self.parent_step
        if self.wyzwalacz:
            d["wyzwalacz"] = self.wyzwalacz
        return d