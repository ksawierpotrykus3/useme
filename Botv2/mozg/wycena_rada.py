# -*- coding: utf-8 -*-
"""Rada wycen: 4x DeepSeek rownolegle, 2 rundy, rozjemca DeepSeek.

Przebieg:
1. RUNDA 1 — 4 wywolania DeepSeeka dostaja TEN SAM prosty prompt i to samo zlecenie.
   Prosty prompt: kim jestes (solo dev, 90 zl/h), wycen to, nie z kosmosu, nie za darmo.
2. RUNDA 2 — kazde wywolanie dostaje z powrotem SWOJA wlasna odpowiedz + pytanie:
   "dlaczego tak a nie inaczej? czy na pewno dobrze wyceniles i nie zgadles niczego?"
3. ROZJEMCA — DeepSeek dostaje WSZYSTKIE surowe odpowiedzi (runda 1 i 2) i decyduje:
   finalna kwota (definitywna albo widelki), od czego zaleza, dlaczego.
4. CALY SUROWY TEKST (wszystkie 8 odpowiedzi + werdykt rozjemcy) idzie dalej do pisma.

Zero kalkulatora, zero godzin liczonych przez AI, zero Gemini.
Tylko: cztery niezalezne glosy DeepSeeka + jeden sedzia DeepSeek.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, List, Optional

PROMPT_SYS = (
    "Jestes polskim freelancerem programista pracujacym solo na Useme. "
    "Rozliczasz sie przez umowe o dzielo, bez firmy i bez kosztow biura. "
    "Masz 90 zl stawki za godzine. Odpowiadasz konkretnie i krotko."
)

PROMPT_R1 = (
    "Wycen to zlecenie.\n\n"
    "Jestem solo dev, freelancer. Nie chce dawac kwot z kosmosu, ani nie chce "
    "robic za darmo. Moja stawka to 90 zl za godzine.\n\n"
    "Podaj: kwota (albo widelki), orientacyjny czas w dniach, i 2-3 zdania uzasadnienia. "
    "Jesli cos jest niejasne w zleceniu, powiedz czego brakuje.\n\n"
    "TRESC ZLECENIA:\n{tresc}"
)

PROMPT_R2 = (
    "Twoja poprzednia wycena tego zlecenia:\n\n{poprzednia}\n\n"
    "Tresc zlecenia:\n{tresc}\n\n"
    "Dlaczego tak a nie inaczej? Czy na pewno dobrze wyceniles? "
    "Czy czegos nie zgadles albo nie dopisales na sile? Jesli trzeba, skoryguj kwote. "
    "Odpowiedz szczerze, 3-5 zdan."
)

PROMPT_ROZJEMCA_SYS = (
    "Jestes rozjemca wycen zlecen na Useme. Dostajesz surowe odpowiedzi od czterech "
    "niezaleznych modeli (dwie rundy kazdy). Twoim zadaniem jest wybrac JEDNA finalna "
    "wycene i ja uzasadnic. Nie zgadujesz. Patrzysz na zbieznosc i rozbieznosc glosow."
)

PROMPT_ROZJEMCA = (
    "Oto zlecenie:\n__TRESC__\n\n"
    "Oto SUROWE odpowiedzi czterech modeli (kazdy w dwoch rundach):\n\n__GLOSY__\n\n"
    "Zdecyduj:\n"
    "1. Jaka jest finalna wycena (kwota dolna i gorna).\n"
    "2. Czy to wycena definitywna, czy widelki. Jesli widelki, od czego zaleza.\n"
    "3. Dlaczego taka, a nie inna. Gdzie modele sie zgadzaly, a gdzie rozjechaly.\n"
    "4. Czego w zleceniu brakuje, ze wycena jest niepewna.\n\n"
    "Zwroc WYLACZNIE poprawny JSON, bez markdown, bez komentarzy:\n"
    "{\n"
    '  "kwota_dolna": <int>,\n'
    '  "kwota_gorna": <int>,\n'
    '  "definitywna": true/false,\n'
    '  "od_czego_zaleza": ["...", "..."],\n'
    '  "dni_od": <int>,\n'
    '  "dni_do": <int>,\n'
    '  "uzasadnienie": "3-5 zdan: dlaczego tak, gdzie zbieznosc, gdzie rozbieznosc"\n'
    "}"
)


def _oczysc_int(v: Any, default: int = 0) -> int:
    if v is None:
        return default
    if isinstance(v, (int, float)):
        return int(v)
    s = re.sub(r"[^\d]", "", str(v))
    return int(s) if s else default


def _parsuj_rozjemce(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    if not isinstance(data, dict):
        return None
    cd = _oczysc_int(data.get("kwota_dolna"))
    cg = _oczysc_int(data.get("kwota_gorna"))
    if cd <= 0:
        return None
    definitywna = bool(data.get("definitywna"))
    # Naturalna logika: definitywna => jedna cena (dolna == gorna).
    if definitywna:
        cg = cd
    elif cg < cd:
        cg = cd
    return {
        "kwota_dolna": cd,
        "kwota_gorna": cg,
        "definitywna": definitywna,
        "od_czego_zaleza": [str(x).strip() for x in (data.get("od_czego_zaleza") or []) if str(x).strip()],
        "dni_od": _oczysc_int(data.get("dni_od"), 14),
        "dni_do": _oczysc_int(data.get("dni_do"), 21),
        "uzasadnienie": str(data.get("uzasadnienie") or "").strip(),
    }


def _zaokraglij(kwota: int) -> int:
    if kwota <= 2000:
        return int(round(kwota / 50.0) * 50)
    if kwota <= 10000:
        return int(round(kwota / 500.0) * 500)
    return int(round(kwota / 1000.0) * 1000)


def _wyciagnij_kwoty(tekst: str) -> List[int]:
    """Wyciaga z surowego tekstu modelu wszystkie sensowne kwoty (2-6 cyfr)."""
    if not tekst:
        return []
    wyniki = []
    for m in re.finditer(r"\b(\d{1,3}(?:[\s\u00a0]\d{3})+|\d{3,6})\b", tekst):
        cyfry = re.sub(r"[^\d]", "", m.group(1))
        if cyfry:
            v = int(cyfry)
            if 300 <= v <= 200000:
                wyniki.append(v)
    return wyniki


def _fallback_z_glosow(r1: Dict[str, str], r2: Dict[str, str]) -> tuple:
    """Awaryjny przedzial, gdy rozjemca padnie: mediana kwot z glosow modeli.

    Bierze wszystkie kwoty z rundy 1 i 2, liczy mediane jako srodek i zwraca
    waski przedzial wokol niej. Odporne na smieci - jak malo danych, daje domyslny.
    """
    kwoty: List[int] = []
    for n in r1:
        tekst = f"{r1.get(n) or ''} {r2.get(n) or ''}"
        kwoty.extend(_wyciagnij_kwoty(tekst))
    if len(kwoty) < 2:
        return 3000, 6000
    kwoty.sort()
    med = kwoty[len(kwoty) // 2]
    dolna = _zaokraglij(int(med * 0.8))
    gorna = _zaokraglij(int(med * 1.3))
    return dolna, max(gorna, dolna)


def _call_par(call_fn: Callable[[str, str], Optional[str]], sys_p: str, usr_p: str) -> Optional[str]:
    try:
        return call_fn(sys_p, usr_p)
    except Exception as e:
        return f"[BLAD: {e}]"


def wycen_rada(
    tresc_zlecenia: str,
    dziennik: str = "",
    research: str = "",
    call_ai_fn: Optional[Callable[[str, str], Optional[str]]] = None,      # DeepSeek
    call_gemini_fn: Optional[Callable[[str, str], Optional[str]]] = None,  # nieuzywane (kompatybilnosc)
    say: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """Rada 4x DeepSeek -> rozjemca DeepSeek -> finalna wycena + surowy tekst."""
    if say is None:
        say = lambda msg: None
    if call_ai_fn is None:
        from brain import call_ai
        call_ai_fn = call_ai

    tresc = tresc_zlecenia
    if dziennik:
        tresc = f"{tresc_zlecenia}\n\nDZIENNIK MYSLENIA:\n{dziennik}"
    if research:
        tresc = f"{tresc}\n\nRESEARCH:\n{research}"

    prompt1 = PROMPT_R1.format(tresc=tresc)
    nazwy = ["DeepSeek-A", "DeepSeek-B", "DeepSeek-C", "DeepSeek-D"]

    # --- RUNDA 1: 4x DeepSeek SEKWENCYJNIE ---
    # UWAGA: proxy DeepSeek (port 4571) NIE obsluguje rownoleglych requestow.
    # Przy ThreadPoolExecutor wracalo tylko 1 z 4 odpowiedzi (reszta pusta).
    # Dlatego lecimy po kolei - wolniej, ale komplet glosow.
    say("    rada wycen: 4x DeepSeek (sekwencyjnie)...")
    r1: Dict[str, str] = {}
    for n in nazwy:
        r1[n] = _call_par(call_ai_fn, PROMPT_SYS, prompt1) or ""

    for nazwa in nazwy:
        say(f"      [{nazwa} R1] {(r1[nazwa] or '')[:90].strip()}...")

    # --- RUNDA 2: kazdy komentuje wlasna odpowiedz (tez sekwencyjnie) ---
    say("    rada wycen: runda 2 (czy na pewno nie zgadles?)...")
    r2: Dict[str, str] = {}
    for n in nazwy:
        r2[n] = _call_par(call_ai_fn, PROMPT_SYS,
                          PROMPT_R2.format(poprzednia=r1[n], tresc=tresc)) or ""

    for nazwa in nazwy:
        say(f"      [{nazwa} R2] {(r2[nazwa] or '')[:90].strip()}...")

    # --- Surowy zbior glosow dla rozjemcy ---
    bloki = []
    for nazwa in nazwy:
        bloki.append(
            f"=== {nazwa} — RUNDA 1 ===\n{r1[nazwa]}\n\n"
            f"=== {nazwa} — RUNDA 2 (autokrytyka) ===\n{r2[nazwa]}"
        )
    surowe_wszystko = "\n\n".join(bloki)

    # --- ROZJEMCA (DeepSeek) ---
    say("    rada wycen: rozjemca DeepSeek wybiera finalna wycene...")
    prompt_rozjemca = (
        PROMPT_ROZJEMCA
        .replace("__TRESC__", tresc)
        .replace("__GLOSY__", surowe_wszystko)
    )
    rozjemca_raw = call_ai_fn(
        PROMPT_ROZJEMCA_SYS,
        prompt_rozjemca,
    )
    rozjemca = _parsuj_rozjemce(rozjemca_raw)

    if not rozjemca:
        say("    [Rozjemca] brak/pusty JSON - fallback z glosow...")
        cd_fb, cg_fb = _fallback_z_glosow(r1, r2)
        rozjemca = {
            "kwota_dolna": cd_fb, "kwota_gorna": cg_fb, "definitywna": False,
            "od_czego_zaleza": ["rozjemca nie odpowiedzial - przedzial z mediany glosow"],
            "dni_od": 14, "dni_do": 21,
            "uzasadnienie": "Fallback: rozjemca nie odpowiedzial, przedzial policzony z glosow modeli.",
        }

    cd = _zaokraglij(max(rozjemca["kwota_dolna"], 500))
    cg = _zaokraglij(max(rozjemca["kwota_gorna"], cd))
    if cg < cd:
        cg = cd
    dni_od = max(7, rozjemca["dni_od"])
    dni_do = max(dni_od, rozjemca["dni_do"])

    say(f"    -> wycena rady: {cd}-{cg} zl / {dni_od}-{dni_do} dni "
        f"({'definitywna' if rozjemca['definitywna'] else 'widelki'})")

    surowy_tekst = (
        f"=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===\n\n"
        f"{surowe_wszystko}\n\n"
        f"=== WERDYKT ROZJEMCY ===\n{rozjemca_raw or 'brak'}\n\n"
        f"=== FINALNA WYCENA ===\n"
        f"{cd}-{cg} zl netto | {dni_od}-{dni_do} dni | "
        f"{'DEFINITYWNA (jedna cena)' if rozjemca['definitywna'] else 'WIDELKI'}\n"
        f"Od czego zalezy: {', '.join(rozjemca['od_czego_zaleza']) or 'brak'}\n"
        f"Uzasadnienie rozjemcy: {rozjemca['uzasadnienie'] or 'brak'}\n"
    )

    return {
        "ok": True,
        "kwota_dolna": cd,
        "kwota_gorna": cg,
        "kwota": (cd + cg) // 2,
        "definitywna": rozjemca["definitywna"],
        "od_czego_zaleza": rozjemca["od_czego_zaleza"],
        "dni_od": dni_od,
        "dni_do": dni_do,
        "uzasadnienie_rozjemcy": rozjemca["uzasadnienie"],
        "glosy_r1": r1,
        "glosy_r2": r2,
        "surowy_tekst": surowy_tekst,
        "rozbicie": {
            "tryb": "rada_4_modeli",
            "glosy_r1": r1,
            "glosy_r2": r2,
            "rozjemca": rozjemca,
            "kwota_dolna": cd,
            "kwota_gorna": cg,
            "definitywna": rozjemca["definitywna"],
        },
    }