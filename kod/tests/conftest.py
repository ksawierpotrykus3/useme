# -*- coding: utf-8 -*-
"""Konfiguracja testów pytest i dołączanie katalogu głównego do sys.path."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_useme_availability():
    with patch("engine.czekaj_na_dostepnosc_useme", return_value=True):
        yield

