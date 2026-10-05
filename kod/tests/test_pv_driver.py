# -*- coding: utf-8 -*-
"""Testy jednostkowe i integracyjne dla PVDriver (Playwright - 'Zapytaj o szczegóły')."""

import json
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

import config
from pv_driver import PVDriver, AuthenticationRequiredError


HTML_JOB_PAGE = """<!DOCTYPE html>
<html>
<head><title>Zlecenie testowe Useme</title></head>
<body>
    <div id="cookiescript_injected_wrapper">Cookie Banner</div>
    <h1>Aplikacja mobilna IoT</h1>
    <div class="jobs-summary">
        <a class="button button--yellow-solid" href="/pl/jobs/145494/offer/start/">Dodaj ofertę</a>
        <a class="button button--yellow-outline" href="/pl/mesg/compose/145494/708188/">Zapytaj o szczegóły</a>
    </div>
</body>
</html>
"""

HTML_COMPOSE_PAGE = """<!DOCTYPE html>
<html>
<head><title>Napisz wiadomość | Useme</title></head>
<body>
    <div id="cookiescript_injected_wrapper">Cookie Banner</div>
    <h2>Do mbrvm</h2>
    <form action="/pl/mesg/compose/145494/708188/" method="post">
        <label for="id_content">Treść:</label>
        <textarea name="content" id="id_content" class="form__textarea"></textarea>
        <button class="button button--primary" type="submit">Wyślij wiadomość</button>
    </form>
</body>
</html>
"""


def test_pv_driver_blocked_author_fails(monkeypatch):
    """Próba kontaktu PV z własnym profilem / wykluczonym autorem rzuca RuntimeError."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pv = PVDriver(context, dry_run=True)

        # Mock is_blocked_author to return True
        monkeypatch.setattr(config, "is_blocked_author", lambda aid, name: True)

        with pytest.raises(RuntimeError, match="BLOKADA WŁASNY PROFIL"):
            pv.send_private_message(job_id="145494", message_text="Cześć...")

        context.close()
        browser.close()


def test_pv_driver_dry_run_flow(tmp_path):
    """Weryfikacja pełnego przepływu DRY_RUN: nawigacja, kliknięcie 'Zapytaj o szczegóły', uzupełnienie textarea i zrzut."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Mock routes for local testing
        def handle_route(route):
            url = route.request.url
            if "/mesg/compose/" in url:
                route.fulfill(status=200, content_type="text/html", body=HTML_COMPOSE_PAGE)
            elif "/jobs/" in url:
                route.fulfill(status=200, content_type="text/html", body=HTML_JOB_PAGE)
            else:
                route.continue_()

        page = context.new_page()
        page.route("**/*", handle_route)
        page.close()

        # Override new_page to automatically route
        orig_new_page = context.new_page
        def routed_new_page():
            pg = orig_new_page()
            pg.route("**/*", handle_route)
            return pg
        context.new_page = routed_new_page

        pv = PVDriver(context, dry_run=True)
        tresc_testowa = "Cześć! Zobaczyłem Twoje ogłoszenie o ESP32 i mam jedno pytanie o sensory."

        res = pv.send_private_message(
            job_id="145494",
            message_text=tresc_testowa,
            custom_screenshot_dir=tmp_path
        )

        assert res["ok"] is True
        assert res["status"] == "DRY_RUN_OK"
        assert res["mode"] == "pv"
        assert res["job_id"] == "145494"
        assert res["tresc"] == tresc_testowa
        assert Path(res["proof_screenshot"]).exists()

        context.close()
        browser.close()


def test_pv_driver_empty_content_raises():
    """Pusta treść wiadomości rzuca błąd."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pv = PVDriver(context, dry_run=True)

        with pytest.raises(Exception):
            pv.send_private_message(job_id="145494", message_text="")

        context.close()
        browser.close()
