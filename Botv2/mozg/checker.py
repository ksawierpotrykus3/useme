# -*- coding: utf-8 -*-
"""Deterministyczny checker twardych zakazow (z V1 deterministic_pre_audit + lista B).

Nie prompt - skrypt. Lapie mechaniczne AI-izmy ze 100% pewnoscia.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

_FORBIDDEN = [
    (r"mamy\s+do[śs]wiadczenie\s+w\s+[łl][ąa]czeniu|zrealizowali[śs]my\s+wiele\s+podobnych",
     "Pusty frazes szablonowy bez konkretu"),
    (r"w\s+wersji\s+drugiej|rozszerze[ńn]\s+w\s+wersji\s+drugiej|wyceniam\s+osobno\s+w\s+kolejnym",
     "Upselling do wersji drugiej"),
    (r"to\s+czysta\s+pr[óo]bka\s+techniczna\s+na\s+danych\s+testowych,\s+bez\s+przekazywania\s+kodu",
     "Recytowanie wewnetrznego regulaminu promptu"),
    (r"\bpo\s+pierwsze\b.*\bpo\s+drugie\b|\bpierwszy\s+strumie[ńn]\b.*\bdrugi\s+strumie[ńn]\b",
     "Szkolna wyliczanka Po pierwsze / Po drugie"),
    (r"\bnie\s+mamy\s+wprost\s+wdro[żz]enia\b|\bnie\s+robili[śs]my\s+dok[łl]adnie\b",
     "Negatywny disclaimer zamiast opisu rozwiazania"),
    (r"\b(?:inżynier|inzynier)[a-ząćęłńóśźż]*\b",
     "Nazywanie siebie inzynierem"),
    (r"\b(?:przyznam\s+szczerze|nie\s+ukrywam)\b", "Frazes przyznam szczerze / nie ukrywam"),
    (r"\b(?:w\s+osobnej\s+wiadomo[sś]ci|w\s+kolejnej\s+wiadomo[sś]ci|tuż\s+po\s+tej\s+ofercie|pode[sś]l[eę]\s+(?:linki|realizacje)\s+w\s+wiadomo[sś]ci|wy[sś]l[eę]\s+(?:linki|realizacje)\s+w\s+wiadomo[sś]ci)\b",
     "Obietnica wysłania linków/materiałów w osobnej wiadomości prywatnej (bot wysyła tylko tę ofertę)"),
]

_ETYKIETY = [
    "dlaczego to ważne", "dlaczego to wazne", "kluczowa mina", "najdroższa mina",
    "najdrozsza mina", "podsumowanie", "wniosek", "uwaga",
    "główna pułapka", "glowna pulapka", "główne ryzyko", "glowne ryzyko",
    "kluczowe", "najważniejsze", "najwazniejsze",
]

_FRAZY_B = [
    "dzień dobry", "dzien dobry", "pozdrawiam", "zapraszam do współpracy",
    "zapraszam do wspolpracy", "chętnie omówię szczegóły", "chetnie omowie szczegoly",
    "mam doświadczenie", "mam doswiadczenie", "jako ekspert", "jako inżynier",
    "poprowadzę", "poprowadze", "wszystko wyjaśnię", "wszystko wyjasnie",
    "tandem inżynierski", "tandem inzynierski", "doskonale rozumiem",
    "czytam twoje ogłoszenie", "czytam twoje ogloszenie",
]

_STAWKA_ZL_H = re.compile(r"\b(\d{1,3})\s*(?:zł|zl|pln)?\s*/\s*(?:h|godz|godzin)", re.IGNORECASE)
_GWARANCJA = re.compile(r"\b(?:gwarancj\w*|gwarantuj\w*)\s*(\d{1,3})\s*dni", re.IGNORECASE)

_JARGON_BIZNES = [
    "fastapi", "docker", "kubernetes", "playwright", "postgresql", "redis",
    "redlock", "leaky bucket", "webhook", "endpoint", "oauth2", "cron", "sqlcipher",
]

_IGNORED_ACRONYMS = {"PL", "UK", "IT", "AI", "B2B", "B2C", "OK", "UE", "RODO", "NIP",
                     "VAT", "KSEF", "WZ", "FS", "ZK", "PLN", "USD", "EUR"}


def _linie_z_wypunktowaniem(tekst: str) -> List[str]:
    out = []
    for line in tekst.splitlines():
        if re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line):
            out.append(line.strip())
    return out


def sprawdz(tekst: str, dni: Optional[int] = None, sciezka: str = "",
            client_text: str = "") -> Dict[str, Any]:
    """Sprawdza twarde zakazy. Zwraca ok + liste problemow z dowodami."""
    problemy: List[Dict[str, Any]] = []
    t = tekst or ""
    t_low = t.lower()
    client_low = (client_text or "").lower()

    def dodaj(regula, dowody):
        problemy.append({"regula": regula, "dowody": dowody[:5]})

    # 1. Myslniki, pauzy, polpauzy
    myslniki = []
    for m in re.finditer(r"[\u2014\u2013]", t):
        myslniki.append(t[max(0, m.start() - 15):m.end() + 15])
    for m in re.finditer(r"\s+-\s+", t):
        myslniki.append(t[max(0, m.start() - 15):m.end() + 15])
    for m in re.finditer(r"(?m)^\s*-\s+", t):
        myslniki.append(m.group(0).strip())
    if myslniki:
        dodaj("myslnik/pauza", myslniki)

    # 2. Nawiasy okragle
    nawiasy = re.findall(r"\([^)]{0,40}\)", t)
    if nawiasy:
        dodaj("nawiasy okragle", nawiasy)

    # 3. Markdown
    md = []
    for m in re.finditer(r"(?m)^\s*#{1,6}\s+", t):
        md.append(t[m.start():m.start() + 30].strip())
    for m in re.finditer(r"\*\*[^*]{1,40}\*\*", t):
        md.append(m.group(0))
    if re.search(r"(?m)^\s*\|.*\|", t):
        md.append("tabela markdown")
    if md:
        dodaj("markdown", md)

    # 4. Wypunktowania
    wy = _linie_z_wypunktowaniem(t)
    if wy:
        dodaj("wypunktowanie", wy)

    # 5. Etykiety z dwukropkiem
    etykiety = []
    for e in _ETYKIETY:
        for m in re.finditer(re.escape(e) + r"\s*:", t_low):
            etykiety.append(t[m.start():m.start() + 40])
    if etykiety:
        dodaj("etykieta z dwukropkiem", etykiety)

    # 6. Czarna lista B
    b = [f for f in _FRAZY_B if f in t_low]
    if b:
        dodaj("czarna lista B", b)

    # 7. Forbidden patterns
    forb = []
    for pat, reason in _FORBIDDEN:
        m = re.search(pat, t, flags=re.IGNORECASE | re.DOTALL)
        if m:
            forb.append(f"{reason}: {m.group(0)[:60]}")
    if forb:
        dodaj("forbidden pattern", forb)

    # 8. Stawka godzinowa
    stawki = [m.group(0) for m in _STAWKA_ZL_H.finditer(t)]
    if stawki:
        dodaj("stawka godzinowa", stawki)

    # 9. Gwarancja inna niz 30 dni
    gwar = [m.group(0) for m in _GWARANCJA.finditer(t) if m.group(1) != "30"]
    if gwar:
        dodaj("gwarancja inna niz 30 dni", gwar)

    # 10. Wideo bez prosby klienta
    client_asked_video = bool(re.search(r"\b(?:wideo|video|loom|nagrani[ea]|filmik|screencast)\b", client_low))
    if not client_asked_video:
        m_video = re.search(
            r"\b(?:wideo[-\s]*instrukcj\w*|instrukcj\w*\s+wideo|kr[óo]tk\w+\s+wideo|nagrani\w+\s+wideo|loom)\b",
            t, flags=re.IGNORECASE)
        if m_video:
            dodaj("wideo bez prosby klienta", [m_video.group(0)])

    # 11. Surowe URL
    url = re.findall(r"https?://\S+", t)
    if url:
        dodaj("surowy URL", url)

    # 12. Spojnosc dni z kalkulatorem
    if dni and dni > 0 and t:
        tail = t[-260:]
        for m_d in re.finditer(r"(\d{1,3})\s*dni(?:\s+robocz[eych]+|\s+kalendarzow[eych]+)?", tail, re.IGNORECASE):
            val_d = int(m_d.group(1))
            ctx = tail[max(0, m_d.start() - 20): min(len(tail), m_d.end() + 25)].lower()
            if "gwarancj" in ctx or "asyst" in ctx or "start" in ctx or "ciągu" in ctx:
                continue
            if val_d != dni:
                dodaj("rozjazd dni z kalkulatorem", [f"tekst: {val_d} dni vs kalkulator: {dni} dni"])
                break

    # 13. Zargon IT na sciezce biznes
    if sciezka == "biznes":
        leaked = [term for term in _JARGON_BIZNES if term in t_low and term not in client_low]
        if leaked:
            dodaj("zargon IT na sciezce biznes", leaked)

    # 14. Acronym stuffing
    for para in t.split("\n\n"):
        acr = [a for a in re.findall(r"\b[A-Z]{2,}[0-9]*\b", para) if a.upper() not in _IGNORED_ACRONYMS]
        if len(acr) >= 11:
            dodaj("przeladowanie skrotami", [", ".join(acr[:10])])
            break

    # 15. Mozliwe zmyslone portfolio
    portfolio = []
    for m in re.finditer(
        r"\b(?:m[óo]j\s+(?:najbli[żz]szy\s+)?projekt|robi[łl]em\s+to\s+przy|prowadzi[łl]em\s+integracj|"
        r"realizowa[łl]em|w\s+ramach\s+projektu\s+dla|mam\s+za\s+sob[ąa])\b",
        t, flags=re.IGNORECASE):
        portfolio.append(t[max(0, m.start() - 20):m.end() + 60])
    if portfolio:
        dodaj("mozliwe zmyslone portfolio (do weryfikacji)", portfolio)

    return {"ok": len(problemy) == 0, "problemy": problemy}
