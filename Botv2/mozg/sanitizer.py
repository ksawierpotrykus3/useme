# -*- coding: utf-8 -*-
"""Deterministyczna sanitacja oferty PRZED checkerem (z V1 _sanitize_opis).

Zamiast karac - naprawia. Pauzy -> przecinki, nawiasy -> wplecione, wyrownanie dni,
wyciecie etykiet promptu. Obniza obciazenie checkera i sedziego.
"""

from __future__ import annotations

import re
from typing import Optional


def _fix_days(m: re.Match, dni: int) -> str:
    return f"{dni} dni"


def sanitize_opis(opis: str, wycena: Optional[int] = None, dni: Optional[int] = None) -> str:
    """Deterministyczna sanitacja pauz, myslnikow, nawiasow, widelek i rozjazdu dni."""
    if not opis:
        return ""
    out = opis.replace("**", "")

    # Widełki w zdaniu o utrzymaniu (np. '1500-2500 zl/mies.' -> '1500 zl/mies.')
    out = re.sub(r"\b(\d{3,5})\s*[-–—]\s*\d{3,5}\s*(z[łl](?:\s*netto)?\s*/\s*mies)",
                 r"\1 \2", out, flags=re.IGNORECASE)

    # Pauzy dlugie/polpauzy oraz myslniki otoczone spacjami -> przecinek
    out = re.sub(r"\s*[—–\u2014\u2013]\s*", ", ", out)
    out = re.sub(r"\s+-\s+", ", ", out)
    out = re.sub(r"(?m)^\s*-\s+", "", out)

    # Nawiasy okragle -> wplecenie zawartosci po przecinku
    while "(" in out and ")" in out:
        out = re.sub(r"\s*\(([^()]*)\)", r", \1", out)
    out = out.replace("(", "").replace(")", "")

    # Gwarancja 12 mies -> 30 dni
    out = re.sub(
        r"\s*(?:oraz|\+|i)\s*12\s*miesi[ęe]cy\s*(?:bezp[łl]atnej\s*)?gwarancji(?:\s+na\s+w[łl]asny\s+kod)?",
        "", out, flags=re.IGNORECASE)
    out = re.sub(r"\b12\s*miesi[ęe]cy\s*(?:bezp[łl]atnej\s*)?gwarancji",
                 "30 dni gwarancji rozruchowej", out, flags=re.IGNORECASE)

    # Wyciecie etykiet promptu
    out = re.sub(r"(?i)\bpytanie\s+kwalifikuj[ąa]ce\s*:\s*", "", out)
    out = re.sub(r"(?i)\bkluczowa\s+mina\s*:\s*", "Główna pułapka architektoniczna: ", out)
    out = re.sub(r"(?i)\bnajdro[żz]sza\s+mina\s*:\s*", "Główne ryzyko produkcyjne: ", out)
    out = re.sub(r"(?i)\bdrugi\s+obszar\s+to\s+", "Równie istotny jest ", out)
    out = re.sub(r"(?i)\bkompleksow(?:ego|e|ych|a|ą)\s+", "", out)
    out = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s+z\s+", "w ", out)
    out = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s*,?\s*", "", out)

    # Czyszczenie interpunkcji
    out = re.sub(r",\s*,+", ",", out)
    out = re.sub(r"\.\s*,", ".", out)
    out = re.sub(r",\s*\.", ".", out)
    out = re.sub(r"[ \t]{2,}", " ", out)

    # Wyrownanie liczby dni w ostatnim akapicie o wycenie
    if dni and dni > 0:
        paragraphs = out.split("\n\n")
        if paragraphs:
            last_idx = -1
            for idx_p in range(len(paragraphs) - 1, -1, -1):
                if re.search(r"wycena|koszt|realizacja|netto", paragraphs[idx_p], flags=re.IGNORECASE):
                    last_idx = idx_p
                    break
            if last_idx >= 0:
                def _fix(m: re.Match) -> str:
                    prefix = paragraphs[last_idx][max(0, m.start() - 18): m.start()].lower()
                    suffix = paragraphs[last_idx][m.end(): min(len(paragraphs[last_idx]), m.end() + 20)].lower()
                    if "gwarancj" in suffix or "asyst" in suffix or "start" in prefix or "ciągu" in prefix:
                        return m.group(0)
                    return f"{dni} dni"
                paragraphs[last_idx] = re.sub(
                    r"\b\d{1,3}\s*dni(?:\s+robocz[eych]+|\s+kalendarzow[eych]+)?",
                    _fix, paragraphs[last_idx], flags=re.IGNORECASE)
                out = "\n\n".join(paragraphs)
    return out.strip()