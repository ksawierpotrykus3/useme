# -*- coding: utf-8 -*-
"""Narzędzie do pobierania i zarządzania fixtures (zrzutami HTML) dla testów Useme.

Pozwala na:
1. Zapisanie aktualnych stron Useme przez Playwright (listing, detale zlecenia, formularz oferty, profil)
   do folderu tests/fixtures/, aby testy jednostkowe i E2E nie musiały łączyć się z żywą stroną.
2. Odczytanie struktury HTML przez model/developera bez konieczności uruchamiania przeglądarki.
"""

import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Ścieżki
KOD_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOD_DIR))

import config
from browser_driver import BrowserDriver

FIXTURES_DIR = KOD_DIR / "tests" / "fixtures"


def upewnij_sie_ze_folder_istnieje():
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)


def stworz_fixture_onsite_z_remote():
    """Tworzy referencyjny fixture zlecenia stacjonarnego (Miejsce wykonania) na bazie remote."""
    remote_path = FIXTURES_DIR / "job_detail_remote.html"
    onsite_path = FIXTURES_DIR / "job_detail_onsite.html"

    if not remote_path.exists():
        print(f"[WARN] Brak {remote_path} – pomijam generowanie {onsite_path.name}")
        return

    content = remote_path.read_text(encoding="utf-8")
    onsite_badge = (
        '<div class="jobs-summary__item">\n'
        '    <div class="jobs-summary__item-label">Miejsce wykonania:</div>\n'
        '    <div class="jobs-summary__item-text">Warszawa, Mazowieckie (praca na miejscu)</div>\n'
        '</div>\n'
    )
    if "Miejsce wykonania:" not in content:
        if '<div class="jobs-summary__item-label">Zleceniodawca</div>' in content:
            content = content.replace(
                '<div class="jobs-summary__item-label">Zleceniodawca</div>',
                onsite_badge + '<div class="jobs-summary__item-label">Zleceniodawca</div>',
                1
            )
        else:
            content = content.replace("</body>", onsite_badge + "</body>", 1)

    onsite_path.write_text(content, encoding="utf-8")
    print(f"[OK] Utworzono fixture zlecenia stacjonarnego: {onsite_path}")


def pobierz_live_fixtures(headless: bool = True):
    """Łączy się przez Playwright z Useme i pobiera świeże zrzuty HTML."""
    upewnij_sie_ze_folder_istnieje()
    print("[INFO] Uruchamianie Playwright do pobrania świeżych fixtures...")

    with BrowserDriver(headless=headless) as driver:
        page = driver.context.new_page()

        # 1. Listing zleceń
        listing_url = config.CATEGORY_URLS.get("it", "https://useme.com/pl/jobs/category/programowanie-i-it,36/")
        print(f"[INFO] Pobieranie listingu: {listing_url}")
        try:
            page.goto(listing_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3000)
            driver.dismiss_cookie_banner(page)
            listing_html = page.content()
            (FIXTURES_DIR / "listing_page.html").write_text(listing_html, encoding="utf-8")
            print(f"[OK] Zapisano {FIXTURES_DIR / 'listing_page.html'} ({len(listing_html)} znaków)")
        except Exception as e:
            print(f"[BŁĄD] Nie udało się pobrać listingu: {e}")

        # 2. Pierwsze dostępne zlecenie ze strony
        try:
            soup = BeautifulSoup(listing_html, "html.parser")
            job_links = []
            for a in soup.select("article.job h2 a, a.job__title, article a[href*='/pl/jobs/']"):
                href = a.get("href", "")
                if href and "/pl/jobs/" in href and href not in job_links:
                    full_url = href if href.startswith("http") else f"https://useme.com{href}"
                    job_links.append(full_url)

            if job_links:
                first_job_url = job_links[0]
                print(f"[INFO] Pobieranie detali zlecenia: {first_job_url}")
                page.goto(first_job_url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(2000)
                detail_html = page.content()
                (FIXTURES_DIR / "job_detail_remote.html").write_text(detail_html, encoding="utf-8")
                print(f"[OK] Zapisano {FIXTURES_DIR / 'job_detail_remote.html'} ({len(detail_html)} znaków)")

                # Formularz oferty jeśli widoczny
                if "Dodaj ofertę" in detail_html or "Złóż ofertę" in detail_html or page.locator("form").count() > 0:
                    (FIXTURES_DIR / "form_offer.html").write_text(detail_html, encoding="utf-8")
                    print(f"[OK] Zapisano {FIXTURES_DIR / 'form_offer.html'}")
        except Exception as e:
            print(f"[BŁĄD] Nie udało się pobrać detali zlecenia: {e}")

    stworz_fixture_onsite_z_remote()
    print("[SUKCES] Pobieranie fixtures zakończone.")


def main():
    parser = argparse.ArgumentParser(description="Zarządzanie fixtures HTML dla Useme.")
    parser.add_argument("--live", action="store_true", help="Pobierz świeże fixtures z Useme przez Playwright")
    parser.add_argument("--no-headless", action="store_true", help="Uruchom przeglądarkę w trybie z interfejsem graficznym")
    args = parser.parse_args()

    upewnij_sie_ze_folder_istnieje()

    if args.live:
        pobierz_live_fixtures(headless=not args.no_headless)
    else:
        stworz_fixture_onsite_z_remote()
        print(f"[INFO] Fixtures obecne w folderze: {FIXTURES_DIR}")
        for p in FIXTURES_DIR.glob("*.html"):
            print(f"  - {p.name} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
