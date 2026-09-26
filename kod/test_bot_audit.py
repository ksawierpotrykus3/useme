# -*- coding: utf-8 -*-
"""Kompleksowe testy jednostkowe audytu bota Useme (wiedza tech_01..16, higiena promptów, kalkulator 90 zł/h)."""

from pathlib import Path
import sys

KOD_DIR = Path(__file__).parent
sys.path.insert(0, str(KOD_DIR))

from chain_executor import TECH_CARD_MAP, _resolve_tech_cards, _format_tech_card_for_slot, _build_prompt
from wycena_kalkulator import policz_wycene, STAWKA_EFEKTYWNA, STAWKA_TIER_A


def test_stawka_bazowa_90():
    assert STAWKA_EFEKTYWNA == 90
    assert STAWKA_TIER_A == 90
    res = policz_wycene({
        "typ": "projekt",
        "stawka": 140,  # powinno zostać zignorowane
        "moduly": [{"nazwa": "Integracja API", "godziny_min": 10, "godziny_max": 14}],
        "nowa_technologia": False,
        "mnozniki": [],
        "flagi": {},
    })
    assert res["rozbicie"]["stawka"] == 90


def test_all_16_tech_cards_exist_and_format_cleanly():
    assert len(TECH_CARD_MAP) == 16
    for key in TECH_CARD_MAP:
        txt_02a = _format_tech_card_for_slot(key, "02a")
        assert len(txt_02a) > 500, f"Karta {key} dla 02a jest za krótka!"
        assert "**" not in txt_02a, f"Karta {key} dla 02a zawiera pogrubienia Markdown **!"
        assert "—" not in txt_02a, f"Karta {key} dla 02a zawiera em-dash (—)!"
        # Żadna linia nie powinna być surową tabelą Markdown |...|
        for line in txt_02a.splitlines():
            s = line.strip()
            assert not (s.startswith("|") and s.endswith("|")), f"Karta {key} ma tabelę w 02a: {s}"

        txt_02b = _format_tech_card_for_slot(key, "02b")
        assert len(txt_02b) > 100, f"Karta {key} dla 02b jest pusta!"


def test_resolve_tech_cards_routing():
    # 1. Optima + OCR -> tech_02 + tech_15
    c_optima = _resolve_tech_cards(
        {
            "title": "Wdrożenie automatyzacji obiegu dokumentów (AI OCR + integracja z Comarch Optima)",
            "description": "Pobieranie z KSeF, weryfikacja Białej Listy, Praca Rozproszona XML",
            "sciezka": "inzynieria",
            "typ_klienta": "msp_erp",
        },
        "02a",
    )
    assert "tech_02" in c_optima
    assert "tech_15" in c_optima

    # 2. Tech-Agnostic / sciezka biznes -> wyłącznie tech_16 dla 02a
    c_biz = _resolve_tech_cards(
        {
            "title": "AI w obsłudze klienta - mail / telefon",
            "description": "Chcemy usprawnić odpowiadanie na maile w naszej firmie.",
            "sciezka": "biznes",
            "typ_klienta": "tech_agnostic",
        },
        "02a",
    )
    assert c_biz == ["tech_16"]

    # 3. Mobile Flutter/Android -> tech_06 / tech_05
    c_mob = _resolve_tech_cards(
        {
            "title": "Stworzenie aplikacji mobilnej dla fizjoterapeutów (iOS i Android, Flutter)",
            "description": "Aplikacja mobilna wieloplatformowa",
            "sciezka": "inzynieria",
            "typ_klienta": "ekspert_dziedzinowy",
        },
        "02a",
    )
    assert "tech_06" in c_mob


def test_prompts_free_of_bot_garbage_triggers():
    prompts_dir = KOD_DIR / "prompts"
    mech = (prompts_dir / "kontekst" / "mechanika_wyceniania.md").read_text(encoding="utf-8")
    assert "144788" not in mech
    assert "pokazywane klientowi jako propozycja dodatkowej wyceny" not in mech

    a02a = (prompts_dir / "generatory" / "agent_02a_opis_oferty.md").read_text(encoding="utf-8")
    assert "WERSJI DRUGIEJ" in a02a
    assert "ZAKAZ SZKOLNYCH WYLICZE" in a02a

    a08 = (prompts_dir / "walidatory" / "agent_08_weryfikacja_zasad.md").read_text(encoding="utf-8")
    assert "Zakaz Upsellingu" in a08


def test_audytor_lancuch_pre_audit_and_parser():
    from audytor_lancuch import deterministic_pre_audit, _extract_audyt_json

    # 1. Wykrywanie pustego frazesu 'Mamy doświadczenie w...' oraz żargonu na ścieżce biznes
    pens = deterministic_pre_audit(
        {"sciezka": "biznes", "title": "Pobieranie danych z Allegro", "description": "Formatki meblowe na wymiar"},
        "Dzień dobry,\nPostawimy kontener Docker i FastAPI.\nMamy doświadczenie w łączeniu platform sprzedażowych z systemami produkcyjnymi.",
        3000,
        7,
        "",
    )
    reasons = " ".join(p["uzasadnienie"] for p in pens)
    assert "Pusty frazes szablonowy" in reasons
    assert "docker" in reasons.lower()

    # 2. Wykrywanie fałszywego skoku logicznego Three.js r185 -> PrestaShop
    pens_3d = deterministic_pre_audit(
        {"sciezka": "inzynieria", "title": "Konfigurator 3D", "description": "Three.js"},
        "Zweryfikuję czy kod korzysta z aktualnych wzorców Three.js (r185), co ma bezpośredni wpływ na przyszłą integrację z PrestaShop.",
        3500,
        8,
        "",
    )
    assert any("Three.js" in p["uzasadnienie"] for p in pens_3d)

    # 3. Parser [AUDYT_JSON]
    sample = '[AUDYT_JSON]\n{"wynik_100": 97, "werdykt": "IDEALNA", "za_co_dodano": [], "za_co_odjeto": []}\n[/AUDYT_JSON]'
    parsed = _extract_audyt_json(sample)
    assert parsed is not None
    assert parsed["wynik_100"] == 97

