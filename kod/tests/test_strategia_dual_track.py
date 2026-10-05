"""Testy wdrożenia strategii Dual-Track, profili klientów, modyfikatorów i filtrów pułapek."""

import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config
import chain_executor
from ai_pipeline import SlotChainAIPipeline
from wycena_kalkulator import policz_wycene


def test_selekcjoner_parsuje_dual_track_i_promuje_eksperta():
    """Sprawdza parsowanie sciezka, typ_klienta, modyfikatory oraz auto-promocję eksperta do Tier A."""
    fake_ai_response = """
    [
      {
        "id": "101",
        "decyzja": "BIERZEMY",
        "tier": "TIER_B",
        "sciezka": "biznes",
        "typ_klienta": "ekspert_dziedzinowy",
        "modyfikatory": ["DELEGOWANY"],
        "powod": "System dla kancelarii prawnej"
      },
      {
        "id": "102",
        "decyzja": "BIERZEMY",
        "tier": "TIER_B",
        "sciezka": "inzynieria",
        "typ_klienta": "tech_agnostic",
        "modyfikatory": ["RESCUE", "NIEZNANY_MOD"],
        "powod": "Prosty program do Excela dla biura"
      },
      {
        "id": "103",
        "decyzja": "ODRZUCAMY",
        "powod": "Ukryty etat"
      }
    ]
    """
    offers = [
        {"id": "101", "title": "System dla kancelarii", "short_desc": "Obsługa akt"},
        {"id": "102", "title": "Program do Excela", "short_desc": "Połączenie tabel"},
        {"id": "103", "title": "Programista na stałe 160h", "short_desc": "Szukamy do zespołu"},
    ]

    pipeline = SlotChainAIPipeline()
    with patch.object(pipeline, "_call_deepseek", return_value=fake_ai_response):
        wybrane = pipeline.filter_offers(offers)

    assert len(wybrane) == 2
    by_id = {o["id"]: o for o in wybrane}

    # 101: ekspert_dziedzinowy -> musi zostać automatycznie podniesiony do Tier A
    assert by_id["101"]["tier"] == "A"
    assert by_id["101"]["sciezka"] == "biznes"
    assert by_id["101"]["typ_klienta"] == "ekspert_dziedzinowy"
    assert by_id["101"]["modyfikatory"] == ["DELEGOWANY"]

    # 102: tech_agnostic -> musi mieć wymuszone sciezka == "biznes" i odfiltrowany nieznany modyfikator
    assert by_id["102"]["tier"] == "B"
    assert by_id["102"]["sciezka"] == "biznes"
    assert by_id["102"]["typ_klienta"] == "tech_agnostic"
    assert by_id["102"]["modyfikatory"] == ["RESCUE"]


def test_build_prompt_wstrzykuje_scenariusz_i_modyfikatory():
    """Sprawdza dynamiczne wstrzykiwanie kart scenariuszy i modyfikatorów w _build_prompt."""
    slot_02a = {
        "id": "02a",
        "name": "Treść oferty",
        "role": "generator",
        "prompt_file": "generatory/agent_02a_opis_oferty.md",
        "context_files": ["kontekst/jak_pisac_oferty.md"],
        "requires": [],
    }
    context = {
        "_zlecenie": {
            "id": "555",
            "title": "Automatyzacja raportów w gabinecie lekarskim",
            "tier": "A",
            "sciezka": "biznes",
            "typ_klienta": "ekspert_dziedzinowy",
            "modyfikatory": ["RESCUE", "DELEGOWANY"],
        }
    }

    sys_prompt, user_prompt = chain_executor._build_prompt(slot_02a, context)

    assert "--- KLASYFIKACJA STRATEGICZNA ZLECENIA ---" in user_prompt
    assert "ŚCIEŻKA KOMUNIKACJI (Dual-Track): BIZNES" in user_prompt
    assert "--- SCENARIUSZ KLIENTA (ekspert_dziedzinowy) ---" in user_prompt
    assert "PROFIL OPERACYJNY KLIENTA: EKSPERT DZIEDZINOWY" in user_prompt
    assert "--- MODYFIKATOR (RESCUE) ---" in user_prompt
    assert "--- MODYFIKATOR (DELEGOWANY) ---" in user_prompt
    assert "ZAKAZ pisania jawnych nagłówków typu „Podkładka dla szefa" in user_prompt


def test_config_zawiera_slowa_vip_i_pulapki():
    """Sprawdza obecność słów kluczowych VIP dla eksperta/ERP oraz słów pułapek."""
    assert "kancelaria" in config.VIP_FAST_TRACK_KEYWORDS
    assert "enova" in config.VIP_FAST_TRACK_KEYWORDS
    assert "subiekt" in config.VIP_FAST_TRACK_KEYWORDS
    assert hasattr(config, "TRAP_KEYWORDS")
    assert len(config.TRAP_KEYWORDS) >= 5


def test_tier_a_stala_stawka_90_zl_w_kalkulatorze():
    """Sprawdza, że zlecenie Tier A ma stałą stawkę 90 zł/h i flagę is_tier_a=True."""
    struktura = {
        "id": "999",
        "typ_zlecenia": "projekt",
        "tier": "A",
        "moduly": [{"nazwa": "System rezerwacji dla kliniki", "godziny_real": 20}],
        "mnozniki": [],
        "flagi": {},
    }
    wynik = policz_wycene(struktura)
    assert wynik["rozbicie"]["stawka"] == 90
    assert wynik["rozbicie"]["is_tier_a"] is True
    assert wynik["kwota"] >= 2000
