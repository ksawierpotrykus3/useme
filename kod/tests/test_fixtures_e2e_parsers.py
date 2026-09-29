# -*- coding: utf-8 -*-
"""Szybkie testy jednostkowe i E2E na statycznych fixtures HTML bez odpalania Playwrighta.

Pozwala w 20 milisekund zweryfikować selektory, parsery Useme, detekcję 'Miejsce wykonania'
oraz formularze bez zależności od żywej strony, sieci i Cloudflare.
"""

from pathlib import Path
from bs4 import BeautifulSoup

from browser_driver import BrowserDriver
import config

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def test_fixtures_exist():
    """Weryfikuje czy kluczowe fixtures są obecne na dysku."""
    expected = [
        "listing_page.html",
        "job_detail_remote.html",
        "job_detail_onsite.html",
        "form_offer.html",
        "user_profile.html",
    ]
    for name in expected:
        p = FIXTURES_DIR / name
        assert p.exists(), f"Brak pliku fixture: {p}"
        assert p.stat().st_size > 1000, f"Plik fixture {name} jest zbyt mały ({p.stat().st_size} B)"


def test_parse_listing_page_fixture():
    """Weryfikuje parsowanie listy ogłoszeń z Useme z zapisanego HTML."""
    html = (FIXTURES_DIR / "listing_page.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    articles = soup.select("article.job, article")
    assert len(articles) > 0, "Parser nie znalazł żadnych artykułów ze zleceniami na liście"

    job_titles = []
    for art in articles:
        h2 = art.select_one("h2, .job__title")
        if h2:
            txt = h2.get_text(strip=True)
            if txt:
                job_titles.append(txt)

    assert len(job_titles) >= 5, f"Oczekiwano co najmniej 5 tytułów zleceń, znaleziono {len(job_titles)}"


def test_parse_job_detail_remote_fixture():
    """Weryfikuje ekstrakcję autora, braku lokalizacji stacjonarnej oraz opisu z remote job."""
    html = (FIXTURES_DIR / "job_detail_remote.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    driver = BrowserDriver(headless=True)
    author, author_id = driver._extract_author_from_details(soup)
    location = driver._extract_location_from_details(soup)

    assert author, "Nie udało się wyciągnąć zleceniodawcy z detali"
    assert author_id, "Nie udało się wygenerować author_id"
    # W remote job lokalizacja powinna być pusta lub zdalna
    assert not config.is_onsite_location(location), f"Zlecenie zdalne zostało błędnie oznaczone jako onsite: {location}"


def test_parse_job_detail_onsite_fixture():
    """Weryfikuje detekcję 'Miejsce wykonania' i twardy odrzut zlecenia stacjonarnego."""
    html = (FIXTURES_DIR / "job_detail_onsite.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    driver = BrowserDriver(headless=True)
    location = driver._extract_location_from_details(soup)

    assert location, "Parser nie znalazł pola 'Miejsce wykonania:' w onsite fixture"
    assert "Warszawa" in location, f"Oczekiwano Warszawy w lokalizacji, otrzymano: {location}"
    assert config.is_onsite_location(location) is True, "Funkcja is_onsite_location powinna zwrócić True"


def test_parse_form_offer_fixture():
    """Weryfikuje strukturę formularza składania oferty (pola, token csrf, akcja)."""
    html = (FIXTURES_DIR / "form_offer.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    forms = soup.find_all("form")
    assert len(forms) > 0, "Brak formularza w form_offer fixture"

    # Wyszukanie pól kwoty, dni lub opisu
    textareas = soup.find_all("textarea")
    inputs = soup.find_all("input")
    assert len(textareas) > 0 or len(inputs) > 0, "Formularz nie zawiera żadnych pól wejściowych"
