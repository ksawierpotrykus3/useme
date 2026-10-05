# -*- coding: utf-8 -*-
"""
audytor_lancuch.py
==================
Niezależny Łańcuch Krytyka (Red Team Judge 1-100) + Pętla Samodoskonalenia Ofert.

Architektura:
1. Łańcuch Generatora (`SlotChainAIPipeline` / `02b` + `02a`) tworzy wycenę i ofertę
   dla zlecenia z magazynu (`badania/baza/`).
2. Niezależny Łańcuch Krytyka (`evaluate_offer_100`):
   - Wykonuje twardy audyt deterministyczny w Pythonie (liczba słów, zakazane frazesy,
     spójność kwoty z `[WYNIK_KONCOWY]`, realna stawka efektywna zł/h, formatowanie).
   - Uruchamia niezależnego sędziego AI (`kryteria_audytu_100.md`), który ma dostęp do
     pełnej treści ogłoszenia, Karty Wiedzy Technologicznej (`tech_01`..`tech_16`) oraz
     profilu psychologicznego klienta (`sciezka`, `typ_klienta`).
   - Zwraca transparentną ocenę `1-100 pkt` z rozbiciem na 5 wymiarów (A-E), dokładną listą
     `za_co_dodano` (+pkt + cytat + reasoning) oraz `za_co_odjeto` (-pkt + cytat/brak + reasoning).
3. Pętla Samodoskonalenia (`run_adversarial_loop`):
   - Jeśli oferta otrzyma `< target_score` (domyślnie `92/100`, patrz `config.AUDYTOR_100_TARGET_SCORE`), przekazuje listę potrąceń
     i instrukcje naprawcze Krytyka z powrotem do generatora (`02b` przy błędnej wycenie,
     `02a` przy błędach treści/psychologii/merytoryki) i generuje udoskonaloną wersję,
     po czym ponownie poddaje ją ocenie Krytyka 1-100.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

KOD_DIR = Path(__file__).resolve().parent
ROOT_DIR = KOD_DIR.parent
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

from chain_executor import (
    DEEPSEEK_MODEL,
    PROMPTS_DIR,
    TECH_CARD_MAP,
    TECH_CARDS_DIR,
    _build_prompt,
    _do_research,
    _extract_research_query,
    _extract_wycena_json,
    _format_tech_card_for_slot,
    _load_config,
    _read_text,
    _resolve_tech_cards,
    _slim_zlecenie,
    call_deepseek,
)
from wycena_kalkulator import formatuj_wynik, policz_wycene

KRYTERIA_PATH = PROMPTS_DIR / "walidatory" / "kryteria_audytu_100.md"
COMMON_SENSE_PATH = PROMPTS_DIR / "walidatory" / "sedzia_zdrowego_rozsadku.md"


def _call_slot_with_optional_research(
    sys_prompt: str, usr_prompt: str, model: str, timeout: int = 200
) -> str:
    """Wywołuje slot 02b/02a i obsługuje ewentualny blok [RESEARCH_QUERY] dokładnie jak chain_executor."""
    odp = call_deepseek(sys_prompt, usr_prompt, model=model, timeout=timeout) or ""
    query = _extract_research_query(odp)
    if query:
        research_wynik = _do_research(query)
        kontynuacja = (
            "\n\n--- WYNIK DODATKOWEGO RESEARCHU ---\n" + research_wynik +
            "\n\nNa podstawie powyższego i wcześniejszych danych dokończ swoje zadanie. "
            "Nie zwracaj już bloku [RESEARCH_QUERY]. Podaj finalny wynik."
        )
        time.sleep(8)
        odp = call_deepseek(
            sys_prompt,
            usr_prompt + "\n\n" + odp + kontynuacja,
            model=model,
            timeout=timeout,
        ) or odp
    return odp

# Twarde wzorce pustych frazesów i artefaktów bota wyłapywane deterministycznie przed sędzią AI
FORBIDDEN_PATTERNS: List[Tuple[str, str, int]] = [
    (
        r"mamy\s+do[śs]wiadczenie\s+w\s+[łl][ąa]czeniu|zrealizowali[śs]my\s+wiele\s+podobnych",
        "Pusty frazes szablonowy bez konkretnego faktu i liczby",
        -20,
    ),
    (
        r"w\s+wersji\s+drugiej|rozszerze[ńn]\s+w\s+wersji\s+drugiej|wyceniam\s+osobno\s+w\s+kolejnym",
        "Upselling standardów domeny do wersji drugiej wycenianej osobno",
        -20,
    ),
    (
        r"to\s+czysta\s+pr[óo]bka\s+techniczna\s+na\s+danych\s+testowych,\s+bez\s+przekazywania\s+kodu",
        "Recytowanie wewnętrznego regulaminu promptu",
        -20,
    ),
    (
        r"\bpo\s+pierwsze\b.*\bpo\s+drugie\b|\bpierwszy\s+strumie[ńn]\b.*\bdrugi\s+strumie[ńn]\b",
        "Szkolna wyliczanka Po pierwsze / Po drugie",
        -10,
    ),
    (
        r"three\.js\s*\(?r\d+\)?[^.]*prestashop",
        "Fałszywy skok logiczny łączący wersję silnika Three.js bezpośrednio z integracją koszyka PrestaShop",
        -15,
    ),
    (
        r"\bnie\s+mamy\s+wprost\s+wdro[żz]enia\b|\bnie\s+robili[śs]my\s+dok[łl]adnie\b",
        "Negatywny disclaimer otwierający akapit zamiast bezpośredniego opisu rozwiązania",
        -10,
    ),
    (
        r"\b(?:inżynier|inzynier)[a-ząćęłńóśźż]*\b",
        "Nazywanie siebie inżynierem lub tandemem/zespołem inżynierskim (brak formalnego wykształcenia inżynierskiego)",
        -20,
    ),
]


def _client_text_blob(zlecenie: Dict[str, Any]) -> str:
    fields = zlecenie.get("fields") or {}
    return (
        str(zlecenie.get("title") or fields.get("title") or "")
        + " "
        + str(zlecenie.get("full_description") or zlecenie.get("description") or fields.get("description") or "")
        + " "
        + str(zlecenie.get("short_desc") or "")
    ).lower()


def deterministic_pre_audit(
    zlecenie: Dict[str, Any],
    opis: str,
    wycena: int,
    dni: int,
    wycena_raw: str,
) -> List[Dict[str, Any]]:
    """Twardy audyt w Pythonie wykrywający obiektywne naruszenia przed oceną AI.

    Uwaga: brak jakichkolwiek sztucznych limitów liczby słów oraz brak wymuszania
    formułek o środowisku testowym tam, gdzie nie pasują.
    """
    penalties: List[Dict[str, Any]] = []
    sciezka = str(zlecenie.get("sciezka") or "").strip().lower()
    client_text = _client_text_blob(zlecenie)
    text = opis or ""

    # 1. Całkowity zakaz EM DASH (— / –) oraz myślników ze spacjami ( - ) -> -20 pkt
    m_dash = re.search(r"[—–\u2014\u2013]|\s+-\s+|^\s*-\s+", text, flags=re.MULTILINE)
    if m_dash:
        start_i = max(0, m_dash.start() - 25)
        end_i = min(len(text), m_dash.end() + 25)
        penalties.append({
            "rule_id": "PEN_DASH_USED",
            "punkty": "-20 pkt (Kara bezwzględna: użycie pauzy lub myślnika)",
            "cytat": text[start_i:end_i].strip(),
            "uzasadnienie": "W treści oferty obowiązuje całkowity zakaz używania pauz (—, –) oraz myślników ( - ). Ma być dokładnie 0 takich znaków.",
        })

    # 2. Całkowity zakaz nawiasów okrągłych ( ) -> -20 pkt
    m_paren = re.search(r"[()]", text)
    if m_paren:
        start_i = max(0, m_paren.start() - 25)
        end_i = min(len(text), m_paren.end() + 25)
        penalties.append({
            "rule_id": "PEN_PARENTHESES_USED",
            "punkty": "-20 pkt (Kara bezwzględna: użycie nawiasów)",
            "cytat": text[start_i:end_i].strip(),
            "uzasadnienie": "W treści oferty obowiązuje całkowity zakaz używania nawiasów ( ). Nawiasy brzmią sztucznie.",
        })

    # 3. Zakaz proponowania instrukcji wideo, chyba że klient sam o to poprosił -> -20 pkt
    client_asked_for_video = bool(re.search(r"\b(?:wideo|video|loom|nagrani[ea]|filmik|screencast)\b", client_text))
    if not client_asked_for_video:
        m_video = re.search(
            r"\b(?:wideo[-\s]*instrukcj\w*|instrukcj\w*\s+wideo|kr[óo]tk\w+\s+wideo|nagrani\w+\s+wideo|wideo\s+z\s+obs[łl]ug\w*|filmik\w*\s+instrukta[żz]\w*|loom)\b",
            text,
            flags=re.IGNORECASE,
        )
        if m_video:
            penalties.append({
                "rule_id": "PEN_UNSOLICITED_VIDEO",
                "punkty": "-20 pkt (Kara bezwzględna: instrukcja wideo bez prośby klienta)",
                "cytat": m_video.group(0),
                "uzasadnienie": "Nigdy nie proponujemy instrukcji wideo po wdrożeniu, chyba że klient sam wyraźnie o to poprosił w ogłoszeniu.",
            })

    # 4. Gwarancja wyłącznie 30 dni (zakaz 12/24 miesięcy gwarancji) -> -20 pkt
    m_warr = re.search(
        r"\b(?:12|24|dwunast\w+|dwadzie[śs]cia\s+czter\w+)\s*miesi[ęe]c\w*[^.]{0,35}gwarancj\w*|\broczn\w+\s+gwarancj\w*",
        text,
        flags=re.IGNORECASE,
    )
    if m_warr:
        penalties.append({
            "rule_id": "PEN_12M_WARRANTY",
            "punkty": "-20 pkt (Kara bezwzględna: gwarancja inna niż 30 dni)",
            "cytat": m_warr.group(0),
            "uzasadnienie": "Obowiązuje wyłącznie 30-dniowa gwarancja rozruchowa. Zakaz obiecywania 12 lub 24 miesięcy gwarancji.",
        })

    # 5. Zakazane frazy / szablony
    for idx_pat, (pattern, reason, pts) in enumerate(FORBIDDEN_PATTERNS):
        m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            penalties.append({
                "rule_id": f"PEN_FORBIDDEN_{idx_pat}",
                "punkty": f"{pts} pkt (Kara bezwzględna)",
                "cytat": m.group(0)[:140],
                "uzasadnienie": reason,
            })

    # 6. Zakaz widełek cenowych w treści oferty (np. '1500-2500 zł' lub 'od 3000 do 5000 zł')
    m_range = re.search(
        r"\b\d{3,5}\s*[-–]\s*\d{3,5}\s*(?:z[łl]|pln)\b|\bod\s+\d[\d\s]*do\s+\d[\d\s]*(?:z[łl]|pln)\b",
        text,
        flags=re.IGNORECASE,
    )
    if m_range:
        penalties.append({
            "rule_id": "PEN_PRICE_RANGE",
            "punkty": "-8 pkt (Wymiar D / Zakaz widełek cenowych)",
            "cytat": m_range.group(0),
            "uzasadnienie": "Użyto widełek cenowych zamiast jednej konkretnej kwoty netto.",
        })

    # 7. Spójność liczby dni między tekstem oferty a kalkulatorem (DNI: dni)
    if dni and dni > 0 and text:
        tail = text[-260:]
        for m_d in re.finditer(r"(\d{1,3})\s*dni(?:\s+robocz[eych]+|\s+kalendarzow[eych]+)?", tail, flags=re.IGNORECASE):
            val_d = int(m_d.group(1))
            ctx_window = tail[max(0, m_d.start() - 20): min(len(tail), m_d.end() + 25)].lower()
            if "gwarancj" in ctx_window or "asyst" in ctx_window or "start" in ctx_window or "ciągu" in ctx_window:
                continue
            if val_d != dni:
                penalties.append({
                    "rule_id": "PEN_DAYS_MISMATCH",
                    "punkty": "-5 pkt (Wymiar D / Rozjazd liczby dni)",
                    "cytat": m_d.group(0),
                    "uzasadnienie": f"Liczba dni w tekście oferty ({val_d} dni) nie zgadza się z kalkulatorem i formularzem Useme ({dni} dni).",
                })
                break

    # 8. Ochrona przed Keyword/Acronym Stuffing (Lexical Mirroring > 10 technicznych skrótów w jednym akapicie)
    ignored_acronyms = {"PL", "UK", "IT", "AI", "B2B", "B2C", "OK", "UE", "RODO", "NIP", "VAT", "KSEF", "WZ", "FS", "ZK", "PLN", "USD", "EUR", "ull"}
    for para in text.split("\n\n"):
        acronyms = [a for a in re.findall(r"\b[A-Z]{2,}[0-9]*\b", para) if a.upper() not in ignored_acronyms]
        if len(acronyms) >= 11:
            penalties.append({
                "rule_id": "PEN_ACRONYM_STUFFING",
                "punkty": "-5 pkt (Wymiar E / Przeładowanie skrótami w jednym akapicie)",
                "cytat": ", ".join(acronyms[:10]),
                "uzasadnienie": f"Zbyt duże zagęszczenie skrótów technicznych w jednym akapicie ({len(acronyms)} skrótów).",
            })
            break

    # 9. Sprawdzenie żargonu IT na ścieżce biznes
    if sciezka == "biznes":
        jargon_terms = [
            "fastapi", "docker", "kubernetes", "playwright", "postgresql", "redis",
            "redlock", "leaky bucket", "webhook", "endpoint", "oauth2", "cron", "sqlcipher",
        ]
        leaked = [t for t in jargon_terms if t in text.lower() and t not in client_text]
        if leaked:
            penalties.append({
                "rule_id": "PEN_JARGON_BIZNES",
                "punkty": "-15 pkt (Wymiar B / Kara Dual-Track)",
                "cytat": ", ".join(leaked),
                "uzasadnienie": f"Na ścieżce 'biznes' użyto żargonu IT niewymienionego przez klienta: {', '.join(leaked)}.",
            })

    # 10. Sprawdzenie mnożnika wyceny (tylko jeśli pochodzi ze starego niekalibrowanego kalkulatora >= 1.3)
    if '"mnoznik_ryzyka": 1.3' in (wycena_raw or "") or '"mnoznik_ryzyka": 1.6' in (wycena_raw or ""):
        penalties.append({
            "rule_id": "PEN_OLD_MULTIPLIER",
            "punkty": "-12 pkt (Wymiar D / Kara Wyceny)",
            "cytat": f"Wycena {wycena} zł (stary mnożnik ryzyka >= 1.3)",
            "uzasadnienie": "Wycena pochodzi ze starego iloczynu mnożników (zawyżona względem zaktualizowanego kalkulatora 90 zł/h).",
        })

    return penalties


def _extract_common_sense_json(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    m = re.search(r"\[COMMON_SENSE_JSON\]\s*(\{.*?\})\s*\[/COMMON_SENSE_JSON\]", text, flags=re.DOTALL)
    raw = m.group(1) if m else None
    if not raw:
        m2 = re.search(r"(\{\s*\"status\".*\})", text, flags=re.DOTALL)
        raw = m2.group(1) if m2 else None
    if not raw:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    try:
        return json.loads(raw)
    except Exception:
        return None


def _extract_audyt_json(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    m = re.search(r"\[AUDYT_JSON\]\s*(\{.*?\})\s*\[/AUDYT_JSON\]", text, flags=re.DOTALL)
    raw = m.group(1) if m else None
    if not raw:
        m2 = re.search(r"(\{\s*\"wynik_100\".*\})", text, flags=re.DOTALL)
        raw = m2.group(1) if m2 else None
    if not raw:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    try:
        return json.loads(raw)
    except Exception:
        return None


def evaluate_common_sense_judge(
    zlecenie: Dict[str, Any],
    opis: str,
    wycena: int,
    dni: int,
) -> Dict[str, Any]:
    """Drugi Sędzia ('Ludzkie Oko / Zdrowy Rozsądek') z prostym, otwartym promptem bez listy kontrolnej.

    Wykrywa elementy niepasujące do zlecenia (szablonowe wklejki z innych branż) oraz pominięcia
    ważnych wymagań z ogłoszenia klienta, które mogłyby umknąć sędziemu 100-punktowemu.
    """
    if not COMMON_SENSE_PATH.exists() or not opis:
        return {"status": "OK", "kara_pkt": 0}
    sys_prompt = _read_text(COMMON_SENSE_PATH)
    fields = zlecenie.get("fields") or {}
    job_payload = {
        "id": zlecenie.get("id"),
        "title": zlecenie.get("title") or fields.get("title") or "",
        "budget": zlecenie.get("budget") or fields.get("budget") or "",
        "miejsce_wykonania": zlecenie.get("miejsce_wykonania") or (zlecenie.get("full_details") or {}).get("miejsce_wykonania") or "",
        "description": (
            zlecenie.get("full_description")
            or zlecenie.get("description")
            or fields.get("description")
            or zlecenie.get("short_desc")
            or ""
        ),
    }
    usr_prompt = (
        "--- OGŁOSZENIE KLIENTA ---\n"
        + json.dumps(job_payload, ensure_ascii=False, indent=2)
        + f"\n\n--- PROPONOWANA WYCENA: {wycena} zł netto / {dni} dni ---\n"
        + "\n--- TREŚĆ OFERTY DO OCENY ---\n"
        + (opis or "")
    )
    resp = call_deepseek(sys_prompt, usr_prompt, model="deepseek-v4-pro-nothink", timeout=120)
    parsed = _extract_common_sense_json(resp or "")
    if not isinstance(parsed, dict):
        return {"status": "OK", "kara_pkt": 0}
    return parsed


def evaluate_offer_100(
    zlecenie: Dict[str, Any],
    opis: str,
    wycena: int,
    dni: int,
    wycena_raw: str = "",
) -> Dict[str, Any]:
    """Uruchamia Niezależnego Krytyka 1-100 oraz 2. Sędziego Zdrowego Rozsądku na wygenerowanej ofercie."""
    pre_penalties = deterministic_pre_audit(zlecenie, opis, wycena, dni, wycena_raw)
    system_prompt = _read_text(KRYTERIA_PATH)

    tech_cards = _resolve_tech_cards(zlecenie, "02a")
    all_cards = list(tech_cards)
    for c in _resolve_tech_cards(zlecenie, "02b"):
        if c not in all_cards:
            all_cards.append(c)

    cards_text_parts = []
    for ck in all_cards:
        fname = TECH_CARD_MAP.get(ck)
        if fname and (TECH_CARDS_DIR / fname).exists():
            cards_text_parts.append(f"=== KARTA WIEDZY ({ck}: {fname}) ===\n" + _read_text(TECH_CARDS_DIR / fname)[:5000])

    words = len((opis or "").split())
    chars = len(opis or "")
    slim_job = _slim_zlecenie(zlecenie)

    user_prompt = (
        "--- OGŁOSZENIE KLIENTA I KLASYFIKACJA ---\n"
        + json.dumps(slim_job, ensure_ascii=False, indent=2)
        + "\n\n--- POMOCNICZE KARTY WIEDZY TECHNOLOGICZNEJ ---\n"
        + "\n\n".join(cards_text_parts)
        + "\n\n--- WYNIK WYCENY (SLOT 02b + KALKULATOR) ---\n"
        + f"KWOTA NETTO: {wycena} zł | CZAS: {dni} dni\n"
        + (wycena_raw or "")
        + "\n\n--- TWARDY PRE-AUDYT DETERMINISTYCZNY (PYTHON) ---\n"
        + f"Liczba słów oferty: {words} | Liczba znaków: {chars} (brak sztucznego limitu słów)\n"
        + (
            "Wykryte twarde naruszenia (OBOWIĄZKOWO uwzględnij je w `za_co_odjeto` i odejmij punkty!):\n"
            + json.dumps(pre_penalties, ensure_ascii=False, indent=2)
            if pre_penalties
            else "Brak twardych naruszeń formalnych w pre-audycie Python."
        )
        + "\n\n--- OCENIANA TREŚĆ OFERTY (SLOT 02a) ---\n"
        + (opis or "")
        + "\n\nOceń powyższą ofertę surowo i sprawiedliwie w skali 1-100 pkt. "
        "Odejmij dużo punktów (-20 do -30 pkt) za wszystko, co nie pasuje do tego ogłoszenia lub pomija wymagania klienta. "
        "Zwróć wyłącznie blok [AUDYT_JSON]...[/AUDYT_JSON]."
    )

    resp = call_deepseek(system_prompt, user_prompt, model=DEEPSEEK_MODEL, timeout=180)
    parsed = _extract_audyt_json(resp or "")
    if not parsed:
        # Fallback retry
        time.sleep(8)
        resp = call_deepseek(system_prompt, user_prompt, model=DEEPSEEK_MODEL, timeout=180)
        parsed = _extract_audyt_json(resp or "")

    if not parsed:
        parsed = {
            "wynik_100": 75,
            "kategorie": {
                "A_merytoryka_25": 18,
                "B_psychologia_25": 18,
                "C_pytanie_cta_20": 15,
                "D_wycena_15": 12,
                "E_styl_zwiezlosc_15": 12,
            },
            "za_co_dodano": [],
            "za_co_odjeto": list(pre_penalties),
            "werdykt": "POPRAW",
            "popraw_oferta": "Dopracuj konkret domenowy i usuń elementy niepasujące do zlecenia.",
            "popraw_wycena": "",
        }
    else:
        existing_blob = " ".join(
            f"{item.get('punkty', '')} {item.get('cytat', '')} {item.get('uzasadnienie', '')}".lower()
            for item in parsed.get("za_co_odjeto", [])
        )
        unaccounted_pts = 0
        total_pre_pts = 0
        for pen in pre_penalties:
            try:
                pts_val = int(re.search(r"-?\d+", pen["punkty"]).group(0))
            except Exception:
                pts_val = 0
            total_pre_pts += pts_val
            rule_id = str(pen.get("rule_id", "")).lower()
            already_listed = (
                (rule_id and rule_id in existing_blob)
                or (pen["cytat"][:20].lower() in existing_blob)
                or ("mnożnik" in pen["uzasadnienie"].lower() and "mnożnik" in existing_blob)
                or ("pauz" in pen["uzasadnienie"].lower() and ("pauz" in existing_blob or "myślnik" in existing_blob))
                or ("nawias" in pen["uzasadnienie"].lower() and "nawias" in existing_blob)
                or ("wideo" in pen["uzasadnienie"].lower() and "wideo" in existing_blob)
                or ("12" in pen["uzasadnienie"].lower() and "gwarancj" in existing_blob)
                or ("żargon" in pen["uzasadnienie"].lower() and "żargon" in existing_blob)
                or ("widełk" in pen["uzasadnienie"].lower() and "widełk" in existing_blob)
                or ("dni" in pen["uzasadnienie"].lower() and "dni" in existing_blob)
            )
            if not already_listed:
                parsed.setdefault("za_co_odjeto", []).append(pen)
                unaccounted_pts += pts_val

        # Uruchomienie 2. Sędziego ("Sędzia Zdrowego Rozsądku / Ludzkie Oko")
        cs_res = evaluate_common_sense_judge(zlecenie, opis, wycena, dni)
        parsed["sedzia_zdrowego_rozsadku"] = cs_res
        if str(cs_res.get("status", "")).upper() == "VETO":
            try:
                cs_pts = int(cs_res.get("kara_pkt", -20))
                if cs_pts > 0:
                    cs_pts = -cs_pts
                if cs_pts == 0:
                    cs_pts = -20
            except Exception:
                cs_pts = -20
            cs_cytat = str(cs_res.get("cytat_lub_brak") or "(wskazanie Sędziego Zdrowego Rozsądku)")
            cs_uzas = str(cs_res.get("uzasadnienie") or "Element niepasujący do ogłoszenia lub pominięcie wymogu klienta.")
            cs_naprawa = str(cs_res.get("instrukcja_naprawy") or "")
            parsed.setdefault("za_co_odjeto", []).append({
                "rule_id": "PEN_COMMON_SENSE_VETO",
                "punkty": f"{cs_pts} pkt (Sędzia #2 Zdrowego Rozsądku - VETO)",
                "cytat": cs_cytat,
                "uzasadnienie": cs_uzas,
            })
            unaccounted_pts += cs_pts
            total_pre_pts += cs_pts
            parsed["werdykt"] = "POPRAW"
            if cs_naprawa:
                cur_popraw = str(parsed.get("popraw_oferta") or "").strip()
                parsed["popraw_oferta"] = (cur_popraw + " " + f"[SĘDZIA #2 VETO]: {cs_naprawa}").strip()

        # Spójność matematyczna wynik_100 z sumą kategorii (A+B+C+D+E) oraz sufitem kar pre-audytu
        kategorie = parsed.get("kategorie") or {}
        cat_sum = sum(int(v) for v in kategorie.values() if isinstance(v, (int, float)))
        raw_score = int(parsed.get("wynik_100", cat_sum or 85))
        if cat_sum > 0:
            raw_score = min(raw_score, cat_sum)
        if unaccounted_pts < 0:
            raw_score = min(raw_score + unaccounted_pts, 100 + total_pre_pts)
        else:
            raw_score = min(raw_score, 100 + total_pre_pts)
        parsed["wynik_100"] = max(1, min(100, raw_score))

    parsed["words"] = words
    parsed["chars"] = chars
    return parsed


def _sanitize_opis(opis: str, wycena: Optional[int] = None, dni: Optional[int] = None) -> str:
    """Deterministyczna sanitacja pauz (— / –), myślników ( - ), nawiasów ( ), widełek i rozjazdu dni."""
    if not opis:
        return ""
    out = opis.replace("**", "")
    # Zamiana ewentualnych widełek w zdaniu o utrzymaniu/retainerze (np. '1500-2500 zł/mies.' -> '1500 zł/mies.')
    out = re.sub(r"\b(\d{3,5})\s*[-–—]\s*\d{3,5}\s*(z[łl](?:\s*netto)?\s*/\s*mies)", r"\1 \2", out, flags=re.IGNORECASE)
    # Usunięcie pauz długich/półpauz oraz myślników otoczonych spacjami (nigdy nie zamieniamy '—' na '-'!)
    out = re.sub(r"\s*[—–\u2014\u2013]\s*", ", ", out)
    out = re.sub(r"\s+-\s+", ", ", out)
    out = re.sub(r"(?m)^\s*-\s+", "", out)
    # Usunięcie nawiasów okrągłych: wplecenie zawartości po przecinku
    while "(" in out and ")" in out:
        out = re.sub(r"\s*\(([^()]*)\)", r", \1", out)
    out = out.replace("(", "").replace(")", "")
    # Usunięcie pozostałości 12-miesięcznej gwarancji -> wyłącznie 30 dni
    out = re.sub(
        r"\s*(?:oraz|\+|i)\s*12\s*miesi[ęe]cy\s*(?:bezp[łl]atnej\s*)?gwarancji(?:\s+na\s+w[łl]asny\s+kod)?",
        "",
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(
        r"\b12\s*miesi[ęe]cy\s*(?:bezp[łl]atnej\s*)?gwarancji",
        "30 dni gwarancji rozruchowej",
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(r"(?i)\bpytanie\s+kwalifikuj[ąa]ce\s*:\s*", "", out)
    out = re.sub(r"(?i)\bkluczowa\s+mina\s*:\s*", "Główna pułapka architektoniczna: ", out)
    out = re.sub(r"(?i)\bnajdro[żz]sza\s+mina\s*:\s*", "Główne ryzyko produkcyjne: ", out)
    out = re.sub(r"(?i)\bdrugi\s+obszar\s+to\s+", "Równie istotny jest ", out)
    out = re.sub(r"(?i)\bkompleksow(?:ego|e|ych|a|ą)\s+", "", out)
    out = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s+z\s+", "w ", out)
    out = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s*,?\s*", "", out)
    # Czyszczenie interpunkcji po usunięciu pauz i nawiasów
    out = re.sub(r",\s*,+", ",", out)
    out = re.sub(r"\.\s*,", ".", out)
    out = re.sub(r",\s*\.", ".", out)
    out = re.sub(r"[ \t]{2,}", " ", out)
    # Jeśli podano dni z kalkulatora, wyrównaj liczbę dni w końcowym zdaniu wyceny (np. '4 dni robocze' -> '7 dni')
    if dni and dni > 0:
        paragraphs = out.split("\n\n")
        if paragraphs:
            last_idx = -1
            for idx_p in range(len(paragraphs) - 1, -1, -1):
                if re.search(r"wycena|koszt|realizacja|netto", paragraphs[idx_p], flags=re.IGNORECASE):
                    last_idx = idx_p
                    break
            def _fix_days(m: re.Match) -> str:
                prefix_window = paragraphs[last_idx][max(0, m.start() - 18): m.start()].lower()
                suffix_window = paragraphs[last_idx][m.end(): min(len(paragraphs[last_idx]), m.end() + 20)].lower()
                if "gwarancj" in suffix_window or "asyst" in suffix_window or "start" in prefix_window or "ciągu" in prefix_window:
                    return m.group(0)
                return f"{dni} dni"
            paragraphs[last_idx] = re.sub(
                r"\b\d{1,3}\s*dni(?:\s+robocz[eych]+|\s+kalendarzow[eych]+)?",
                _fix_days,
                paragraphs[last_idx],
                flags=re.IGNORECASE,
            )
            out = "\n\n".join(paragraphs)
    return out.strip()


def _extract_price_days_from_text(opis: str) -> Tuple[Optional[int], Optional[int]]:
    """Wyciąga kwotę i dni z treści poprzedniej oferty, gdy wycena_raw nie zawiera bloku [WYNIK_KONCOWY]."""
    if not opis:
        return None, None
    m_price = re.search(r"(\d{1,3}(?:[\s\xa0]?\d{3})+|\d{3,6})\s*(?:z[łl]|pln)", opis, flags=re.IGNORECASE)
    price = int(re.sub(r"\D", "", m_price.group(1))) if m_price else None
    m_days = re.search(r"(\d{1,3})\s*dni", opis, flags=re.IGNORECASE)
    days = int(m_days.group(1)) if m_days else None
    return price, days


def regenerate_from_judge_feedback(
    zlecenie: Dict[str, Any],
    prev_opis: str,
    prev_wycena_raw: str,
    research_text: str,
    audyt: Dict[str, Any],
) -> Tuple[str, int, int, str]:
    """Poprawia wycenę (02b) i/lub ofertę (02a) na podstawie punktacji i uwag Krytyka 1-100 oraz Sędziego #2."""
    config = _load_config()
    slots_by_id = {str(s["id"]): s for s in config["slots"]}
    slim_job = _slim_zlecenie(zlecenie)
    job_id = str(slim_job.get("id", "tmp"))

    popraw_wycena = str(audyt.get("popraw_wycena") or "").strip()
    if not prev_wycena_raw and not popraw_wycena:
        p_kw, p_dn = _extract_price_days_from_text(prev_opis)
        if p_kw and p_dn:
            prev_wycena_raw = f"[WYNIK_KONCOWY]\nKWOTA: {p_kw}\nDNI: {p_dn}\n[/WYNIK_KONCOWY]\n"

    context: Dict[str, Any] = {
        "_zlecenie": slim_job,
        "research": research_text or "BRAK_ISTOTNYCH_FAKTOW",
        "wycena_dni": prev_wycena_raw,
        "opis": prev_opis,
        "_feedback": {},
    }

    has_old_multiplier = '"mnoznik_ryzyka": 1.3' in (prev_wycena_raw or "") or '"mnoznik_ryzyka": 1.6' in (prev_wycena_raw or "")

    # 1. Jeśli Krytyk nakazał korektę wyceny LUB wycena miała stary mnożnik -> przelicz 02b
    if popraw_wycena or has_old_multiplier or not prev_wycena_raw:
        slot_02b = slots_by_id["02b"]
        if popraw_wycena:
            context["_feedback"]["02b"] = popraw_wycena
        sys_02b, usr_02b = _build_prompt(slot_02b, context)
        time.sleep(10)
        odp_02b = _call_slot_with_optional_research(sys_02b, usr_02b, model=slot_02b.get("model", DEEPSEEK_MODEL), timeout=200)
        struktura = _extract_wycena_json(odp_02b or "")
        if not struktura:
            time.sleep(8)
            odp_02b = call_deepseek(
                sys_02b,
                usr_02b + "\n\nZwróć teraz wyłącznie poprawny blok [WYCENA_JSON]...[/WYCENA_JSON].",
                model=slot_02b.get("model", DEEPSEEK_MODEL),
                timeout=180,
            ) or ""
            struktura = _extract_wycena_json(odp_02b)
        if struktura:
            struktura.pop("stawka", None)
            struktura.setdefault("id", job_id)
            if str(slim_job.get("tier") or "").upper() == "A" or slim_job.get("typ_klienta") == "ekspert_dziedzinowy":
                struktura["tier"] = "A"
            elif slim_job.get("tier"):
                struktura.setdefault("tier", slim_job.get("tier"))
            flagi = struktura.setdefault("flagi", {})
            if not flagi.get("budzet_jawny") and slim_job.get("budget"):
                flagi["budzet_jawny"] = slim_job.get("budget")
            wynik = policz_wycene(struktura)
            blok = formatuj_wynik(wynik)
            ostrz = struktura.get("uzasadnienie", "")
            prev_wycena_raw = (
                blok + "\n\n--- UZASADNIENIE DOBORU (model) ---\n" + str(ostrz) +
                "\n\n--- ROZBICIE (kalkulator deterministyczny) ---\n" +
                json.dumps(wynik["rozbicie"], ensure_ascii=False, indent=2)
            )
            context["wycena_dni"] = prev_wycena_raw

    # Wyciągnij aktualną kwotę i dni z wycena_dni (z fallbackiem do prev_opis)
    m_kw = re.search(r"KWOTA:\s*(\d+)", context["wycena_dni"])
    m_dn = re.search(r"DNI:\s*(\d+)", context["wycena_dni"])
    p_kw, p_dn = _extract_price_days_from_text(prev_opis)
    wycena_val = int(m_kw.group(1)) if m_kw else (p_kw or 3000)
    dni_val = int(m_dn.group(1)) if m_dn else (p_dn or 7)

    # 2. Zbuduj precyzyjny feedback dla 00 i 02a z listy potrąceń Krytyka 1-100 oraz Sędziego #2
    deductions_lines = []
    for d in audyt.get("za_co_odjeto", []):
        deductions_lines.append(f"- {d.get('punkty')}: [{d.get('cytat')}] -> {d.get('uzasadnienie')}")
    if audyt.get("popraw_oferta"):
        deductions_lines.append(f"- INSTRUKCJA NAPRAWCZA AUDYTORA: {audyt['popraw_oferta']}")
    deductions_lines.append(
        f"- Aktualna wycena z kalkulatora to DOKŁADNIE {wycena_val} zł netto i {dni_val} dni. "
        "Zachowaj wszystkie elementy za które Audytor przyznał punkty dodatnie (`za_co_dodano`), "
        "wyeliminuj w 100% elementy za które odjęto punkty i pamiętaj o całkowitym zakazie używania myślników, pauz, nawiasów oraz proponowania instrukcji wideo bez prośby klienta!"
    )

    feedback_blob = (
        "POPRZEDNIA WERSJA OFERTY:\n" + (prev_opis or "") +
        "\n\nOCENA NIEZALEŻNEGO KRYTYKA RED TEAM (" + str(audyt.get("wynik_100")) + "/100 pkt) - ZA CO ODJĘTO PUNKTY:\n" +
        "\n".join(deductions_lines)
    )
    context["_feedback"]["00"] = feedback_blob
    context["_feedback"]["02a"] = feedback_blob

    # 1b. Jeśli mamy slot 00 (Orchestrator), uruchom go z feedbackiem Sędziów, by wyznaczył blokady kontekstowe
    if "00" in slots_by_id:
        slot_00 = slots_by_id["00"]
        sys_00, usr_00 = _build_prompt(slot_00, context)
        odp_00 = call_deepseek(sys_00, usr_00, model=slot_00.get("model", "deepseek-v4-pro-nothink"), timeout=120)
        if odp_00:
            context["orchestrator_plan"] = odp_00

    slot_02a = slots_by_id["02a"]
    sys_02a, usr_02a = _build_prompt(slot_02a, context)
    time.sleep(12)
    nowy_opis = _call_slot_with_optional_research(sys_02a, usr_02a, model=slot_02a.get("model", DEEPSEEK_MODEL), timeout=180)
    if nowy_opis:
        nowy_opis = _sanitize_opis(nowy_opis, wycena=wycena_val, dni=dni_val)
    else:
        nowy_opis = prev_opis

    return nowy_opis, wycena_val, dni_val, context["wycena_dni"]


def generate_initial_offer(zlecenie: Dict[str, Any]) -> Tuple[str, int, int, str, str]:
    """Generuje pierwszą wersję oferty (01 Research -> 02b Wycena -> 00 Orchestrator -> 02a Opis) dla nowego zlecenia z magazynu."""
    config = _load_config()
    slots_by_id = {str(s["id"]): s for s in config["slots"]}
    slim_job = _slim_zlecenie(zlecenie)
    job_id = str(slim_job.get("id", "tmp"))

    context: Dict[str, Any] = {
        "_zlecenie": slim_job,
        "_feedback": {},
    }

    # 1. Slot 01 (Research)
    slot_01 = slots_by_id["01"]
    sys_01, usr_01 = _build_prompt(slot_01, context)
    odp_01 = call_deepseek(sys_01, usr_01, model=slot_01.get("model", DEEPSEEK_MODEL), timeout=220)
    if not odp_01 or len(odp_01.strip()) < 20:
        odp_01 = "BRAK_ISTOTNYCH_FAKTOW"
    context["research"] = odp_01
    time.sleep(10)

    # 2. Slot 02b (Wycena + Kalkulator)
    slot_02b = slots_by_id["02b"]
    sys_02b, usr_02b = _build_prompt(slot_02b, context)
    odp_02b = _call_slot_with_optional_research(sys_02b, usr_02b, model=slot_02b.get("model", DEEPSEEK_MODEL), timeout=200)
    wycena_raw = odp_02b or ""
    struktura = _extract_wycena_json(wycena_raw)
    if not struktura:
        time.sleep(8)
        odp_02b = call_deepseek(
            sys_02b,
            usr_02b + "\n\nZwróć teraz wyłącznie poprawny blok [WYCENA_JSON]...[/WYCENA_JSON].",
            model=slot_02b.get("model", DEEPSEEK_MODEL),
            timeout=180,
        ) or ""
        struktura = _extract_wycena_json(odp_02b)
    if struktura:
        struktura.pop("stawka", None)
        struktura.setdefault("id", job_id)
        if str(slim_job.get("tier") or "").upper() == "A" or slim_job.get("typ_klienta") == "ekspert_dziedzinowy":
            struktura["tier"] = "A"
        elif slim_job.get("tier"):
            struktura.setdefault("tier", slim_job.get("tier"))
        flagi = struktura.setdefault("flagi", {})
        if not flagi.get("budzet_jawny") and slim_job.get("budget"):
            flagi["budzet_jawny"] = slim_job.get("budget")
        wynik = policz_wycene(struktura)
        blok = formatuj_wynik(wynik)
        ostrz = struktura.get("uzasadnienie", "")
        wycena_raw = (
            blok + "\n\n--- UZASADNIENIE DOBORU (model) ---\n" + str(ostrz) +
            "\n\n--- ROZBICIE (kalkulator deterministyczny) ---\n" +
            json.dumps(wynik["rozbicie"], ensure_ascii=False, indent=2)
        )
    context["wycena_dni"] = wycena_raw
    m_kw = re.search(r"KWOTA:\s*(\d+)", wycena_raw)
    m_dn = re.search(r"DNI:\s*(\d+)", wycena_raw)
    wycena_val = int(m_kw.group(1)) if m_kw else 3000
    dni_val = int(m_dn.group(1)) if m_dn else 7
    time.sleep(8)

    # 2b. Slot 00 (Orchestrator strategii oferty)
    if "00" in slots_by_id:
        slot_00 = slots_by_id["00"]
        sys_00, usr_00 = _build_prompt(slot_00, context)
        odp_00 = call_deepseek(sys_00, usr_00, model=slot_00.get("model", "deepseek-v4-pro-nothink"), timeout=120)
        if odp_00:
            context["orchestrator_plan"] = odp_00
        time.sleep(8)

    # 3. Slot 02a (Opis oferty)
    slot_02a = slots_by_id["02a"]
    sys_02a, usr_02a = _build_prompt(slot_02a, context)
    opis = _call_slot_with_optional_research(sys_02a, usr_02a, model=slot_02a.get("model", DEEPSEEK_MODEL), timeout=180)
    if opis:
        opis = _sanitize_opis(opis, wycena=wycena_val, dni=dni_val)
    else:
        opis = ""

    return opis, wycena_val, dni_val, wycena_raw, odp_01


def audit_and_refine_100(
    zlecenie: Dict[str, Any],
    opis: str,
    wycena: int,
    dni: int,
    wycena_raw: str = "",
    research_text: str = "",
    target_score: int = 92,
    max_rounds: int = 1,
) -> Dict[str, Any]:
    """
    Produkcyjna bramka audytowa 1-100 dla ai_pipeline.py:
    1. Sanitacja deterministyczna (_sanitize_opis z wyrównaniem dni i ucięciem widełek).
    2. Ocena Sędziego Red-Team 1-100 (evaluate_offer_100).
    3. Jeśli wynik < target_score lub werdykt != PASS, wykonuje do max_rounds pętli naprawczych (regenerate_from_judge_feedback).
    """
    cur_opis = _sanitize_opis(opis, wycena=wycena, dni=dni)
    cur_wycena = int(wycena)
    cur_dni = int(dni)
    cur_wycena_raw = wycena_raw

    audyt_r1 = evaluate_offer_100(zlecenie, cur_opis, cur_wycena, cur_dni, cur_wycena_raw)
    best_opis = cur_opis
    best_wycena = cur_wycena
    best_dni = cur_dni
    best_wycena_raw = cur_wycena_raw
    best_audyt = audyt_r1
    rounds_run = 1

    for _ in range(max_rounds):
        score = int(best_audyt.get("wynik_100", 0))
        werdykt = str(best_audyt.get("werdykt", "PASS")).upper()
        # Pętla kończy się TYLKO gdy wynik jest wystarczający AND sędzia nie żąda poprawy.
        # Wcześniej warunek `or score >= 92` powodował, że oferta z werdyktem POPRAW
        # i wynikiem 92/100 wychodziła z pętli bez żadnej poprawki (feedback nie wracał).
        if score >= target_score and werdykt not in ("POPRAW", "RETRY", "FAIL"):
            break
        rounds_run += 1
        new_opis, new_wycena, new_dni, new_wycena_raw = regenerate_from_judge_feedback(
            zlecenie,
            best_opis,
            best_wycena_raw,
            research_text,
            best_audyt,
        )
        audyt_next = evaluate_offer_100(zlecenie, new_opis, new_wycena, new_dni, new_wycena_raw)
        if int(audyt_next.get("wynik_100", 0)) >= score:
            best_opis = new_opis
            best_wycena = new_wycena
            best_dni = new_dni
            best_wycena_raw = new_wycena_raw
            best_audyt = audyt_next

    return {
        "opis": best_opis,
        "wycena": best_wycena,
        "dni": best_dni,
        "wycena_raw": best_wycena_raw,
        "audyt_r1": audyt_r1,
        "audyt_final": best_audyt,
        "wynik_100": int(best_audyt.get("wynik_100", 0)),
        "rounds": rounds_run,
    }


