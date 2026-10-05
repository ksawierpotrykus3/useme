# -*- coding: utf-8 -*-
"""Testy weryfikujące reformę silnika: brak wymuszonych szablonów, odrzut Miejsca wykonania,
2. Sędzia Zdrowego Rozsądku, kary za myślniki/nawiasy/wideo oraz brak limitów słów.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import config
from audytor_lancuch import (
    _sanitize_opis,
    deterministic_pre_audit,
    evaluate_common_sense_judge,
    evaluate_offer_100,
)


def test_miejsce_wykonania_rejection():
    """Weryfikuje, że Miejsce wykonania nie blokuje zleceń (żeby nie tracić perełek jak Tegra 2)."""
    assert config.is_onsite_location("warszawa") is True
    assert config.is_onsite_location("Kraków, biuro") is True
    assert config.is_onsite_location("Poznań") is True
    assert config.is_onsite_location("zdalnie") is False
    assert config.is_onsite_location("online") is False
    assert config.is_onsite_location("cała polska") is False
    assert config.is_onsite_location("") is False
    assert config.is_onsite_location(None) is False

    # Zlecenie z miejscem wykonania (np. Warszawa) NIE jest już odrzucane przez is_hard_reject
    rej = config.is_hard_reject("Power Glitch Attack Tegra", "ukierunkowane zakłucenie", "Warszawa")
    assert rej is None


def test_deterministic_audit_penalties_dashes_parens_video_warranty():
    """Weryfikuje kary -20 pkt za myślniki, nawiasy, nieproszone wideo i 12m gwarancji oraz brak kar za liczbę słów."""
    zlecenie = {
        "id": "101",
        "title": "Aplikacja w Pythonie",
        "sciezka": "inzynieria",
        "full_description": "Potrzebuję prostego skryptu.",
    }

    # 1. Oferta z myślnikiem i nawiasami -> kary -20 pkt za myślnik i -20 pkt za nawias
    bad_opis = "Dzień dobry, przygotuję skrypt - szybko (oraz sprawnie). Wycena wynosi 1500 zł netto."
    pens = deterministic_pre_audit(zlecenie, bad_opis, 1500, 7, "")
    rule_ids = {p["rule_id"] for p in pens}
    assert "PEN_DASH_USED" in rule_ids
    assert "PEN_PARENTHESES_USED" in rule_ids

    # 2. Brak kar za długość słów (np. 15 słów lub 300 słów nie generuje PEN_WORD_LIMIT ani PEN_WORD_TOO_SHORT)
    assert "PEN_WORD_LIMIT_SMALL" not in rule_ids
    assert "PEN_WORD_LIMIT_LARGE" not in rule_ids
    assert "PEN_WORD_TOO_SHORT" not in rule_ids
    assert "PEN_MISSING_SANDBOX" not in rule_ids

    # 3. Nieproszone wideo -> kara -20 pkt
    video_opis = "Dzień dobry, przygotuję skrypt. Po wdrożeniu nagram krótką instrukcję wideo z obsługi."
    pens_video = deterministic_pre_audit(zlecenie, video_opis, 1500, 7, "")
    assert any(p["rule_id"] == "PEN_UNSOLICITED_VIDEO" for p in pens_video)

    # 4. Proszone wideo (klient sam o to prosił w ogłoszeniu) -> brak kary za wideo!
    zlecenie_z_wideo = {
        "id": "102",
        "title": "Aplikacja w Pythonie",
        "sciezka": "inzynieria",
        "full_description": "Wymagane krótkie wideo instruktarzowe dla zespołu po wdrożeniu.",
    }
    pens_solicited = deterministic_pre_audit(zlecenie_z_wideo, video_opis, 1500, 7, "")
    assert not any(p["rule_id"] == "PEN_UNSOLICITED_VIDEO" for p in pens_solicited)

    # 5. Gwarancja 12 miesięcy -> kara -20 pkt
    warr_opis = "Dzień dobry, przygotuję skrypt. Zapewniam 12 miesięcy bezpłatnej gwarancji na kod."
    pens_warr = deterministic_pre_audit(zlecenie, warr_opis, 1500, 7, "")
    assert any(p["rule_id"] == "PEN_12M_WARRANTY" for p in pens_warr)


def test_sanitize_opis_removes_dashes_parens_and_12m():
    """Weryfikuje, że _sanitize_opis nigdy nie zamienia em-dash na myślnik ze spacjami, usuwa nawiasy i poprawia gwarancję."""
    raw = "Dzień dobry — tu Ksawier. Przygotuję integrację — bez przestojów (na kopii roboczej). Oferuję 12 miesięcy bezpłatnej gwarancji."
    clean = _sanitize_opis(raw, wycena=2000, dni=7)

    # Żadnych pauz ani myślników ze spacjami
    assert "—" not in clean
    assert "–" not in clean
    assert " - " not in clean
    # Żadnych nawiasów
    assert "(" not in clean
    assert ")" not in clean
    # 12 miesięcy zamienione lub usunięte
    assert "12 miesięcy" not in clean
    assert "30 dni gwarancji" in clean


def test_common_sense_judge_veto_integration():
    """Weryfikuje integrację 2. Sędziego (Sędzia Zdrowego Rozsądku) i potrącenie punktów przy VETO."""
    zlecenie = {
        "id": "103",
        "title": "Projekt układu optycznego oscyloskopu",
        "full_description": "Potrzebuję analizy i oprogramowania do testów sygnałów oscyloskopu.",
    }
    bad_offer = "Dzień dobry, prześlijcie mi 1 do 3 przykładowych faktur PDF do bezpłatnego przetestowania."

    fake_veto = {
        "status": "VETO",
        "kara_pkt": -25,
        "cytat_lub_brak": "1 do 3 przykładowych faktur PDF",
        "uzasadnienie": "Zlecenie dotyczy oscyloskopu, a oferta proponuje testowanie faktur PDF.",
        "instrukcja_naprawy": "Usuń wzmiankę o fakturach PDF.",
    }

    with patch("audytor_lancuch.evaluate_common_sense_judge", return_value=fake_veto), \
         patch("audytor_lancuch.call_deepseek", return_value=json.dumps({
             "wynik_100": 90,
             "kategorie": {"A_merytoryka_25": 22, "B_psychologia_25": 22, "C_pytanie_cta_20": 18, "D_wycena_15": 14, "E_styl_zwiezlosc_15": 14},
             "za_co_dodano": [],
             "za_co_odjeto": [],
             "werdykt": "PASS"
         })):
        audyt = evaluate_offer_100(zlecenie, bad_offer, 3000, 7)

    assert audyt["werdykt"] == "POPRAW"
    assert any(p.get("rule_id") == "PEN_COMMON_SENSE_VETO" for p in audyt.get("za_co_odjeto", []))
    assert audyt["wynik_100"] <= 70  # 90 - 25 = 65


def test_chain_config_without_orchestrator_slot_00():
    """Weryfikuje nową architekturę: slot 00 Orchestrator usunięty, 02a nie zależy od orchestrator_plan."""
    cfg_path = Path(__file__).resolve().parent.parent / "prompts" / "chain_config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    slot_ids = [s["id"] for s in cfg["slots"]]
    assert "00" not in slot_ids
    assert "02a" in slot_ids
    assert "01" in slot_ids
    assert "02b" in slot_ids
    assert "08" in slot_ids

    slot_02a = next(s for s in cfg["slots"] if s["id"] == "02a")
    assert "orchestrator_plan" not in slot_02a.get("requires", [])
