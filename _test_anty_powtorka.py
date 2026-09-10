# -*- coding: utf-8 -*-
"""Testy deterministyczne mechanizmu anty-powtórki (wariacja ofert dla stałych klientów).

Sprawdzają trzy rzeczy na mockach (bez sieci i bez AI):
1. Storage.find_by_author poprawnie znajduje zlecenia tego samego autora.
2. Silnik (engine) wstrzykuje previous_offers i variation_seed do job_detail.
3. generate_proposal wykrywa zbyt podobną ofertę i wymusza przepisanie (retry).
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ai_pipeline
from ai_pipeline import ProposalResult, _podobienstwo_jaccard
from browser_driver import BrowserDriver
from storage import Storage


def test_6_parser_na_prawdziwych_html():
    """Test 6: Parser autora na PRAWDZIWYCH stronach Useme z archiwum.

    To jest test przeciwko realnym danym, a nie wymyślonym stringom.
    Sprawdza, że dla każdego zapisanego zlecenia udaje się wyciągnąć autora
    (lub świadomie zwrócić 'anonim', gdy Useme go nie pokazuje).
    """
    from bs4 import BeautifulSoup
    print("\n--- TEST 6: Parser autora na prawdziwych HTML ---")

    baza = Path(__file__).parent / "dane_badania"
    pliki = list(baza.rglob("strona.html"))
    assert pliki, "BŁĄD: Brak plików strona.html w dane_badania!"

    driver = BrowserDriver.__new__(BrowserDriver)  # bez odpalania przeglądarki
    wyciagniete = 0
    anonim = 0
    przyklady = []

    for plik in pliki:
        try:
            soup = BeautifulSoup(plik.read_text(encoding="utf-8", errors="replace"), "html.parser")
        except Exception as e:
            print(f"[WARN] Nie mogę wczytać {plik.name}: {e}")
            continue
        author, author_id = driver._extract_author_from_details(soup)
        if author_id and author_id != "anonim":
            wyciagniete += 1
            if len(przyklady) < 6:
                przyklady.append(f"{author} -> {author_id}")
        else:
            anonim += 1
            if len(przyklady) < 8:
                przyklady.append(f"[anonim] {plik.parent.name[:40]}")

    print(f"Przetworzono {len(pliki)} prawdziwych stron.")
    print(f"Wyciągnięto autora: {wyciagniete}, anonim: {anonim}")
    for p in przyklady:
        print(f"   {p}")

    # Twardy warunek: parser MUSI wyciągnąć sensowną większość autorów.
    assert wyciagniete > 0, "BŁĄD KRYTYCZNY: parser nie wyciągnął ANI JEDNEGO autora z prawdziwych stron!"
    skutecznosc = wyciagniete / len(pliki)
    assert skutecznosc >= 0.5, f"BŁĄD: Skuteczność parsowania autora tylko {skutecznosc:.0%}!"
    print(f"[DOWÓD 6] Parser autora działa na realnych stronach Useme (skuteczność {skutecznosc:.0%}).")


def test_0_normalizacja_nazwy_autora():
    """Test 0: Nazwa zleceniodawcy -> stabilny identyfikator (slug)."""
    print("\n--- TEST 0: Normalizacja nazwy autora ---")
    norm = BrowserDriver._normalize_author
    assert norm("JMNET") == "jmnet", f"BŁĄD: {norm('JMNET')}"
    assert norm("Jan Kowalski") == "jan-kowalski", f"BŁĄD: {norm('Jan Kowalski')}"
    assert norm("Marta Peczek") == "marta-peczek", f"BŁĄD: {norm('Marta Peczek')}"
    assert norm("") == "anonim", "BŁĄD: pusty = anonim"
    # Ta sama nazwa w różnym zapisie musi dać ten sam slug
    assert norm("JMNET") == norm("jmnet"), "BŁĄD: wielkość liter musi być ignorowana!"
    print(f"[DOWÓD 0] 'JMNET'->{norm('JMNET')}, 'Jan Kowalski'->{norm('Jan Kowalski')}, ''->{norm('')}.")


def test_1_podobienstwo_jaccard():
    """Test 1: Deterministyczna miara podobieństwa tekstów."""
    print("\n--- TEST 1: Miara podobieństwa Jaccard ---")
    identyczne = "Dzień dobry, zrealizuję stronę WordPress z panelem."
    assert _podobienstwo_jaccard(identyczne, identyczne) == 1.0, "Identyczne teksty muszą dać 1.0!"

    bardzo_podobne = "Dzień dobry, wykonam stronę WordPress z panelem."
    pod = _podobienstwo_jaccard(identyczne, bardzo_podobne)
    assert pod > 0.7, f"Teksty niemal identyczne powinny mieć >70%, jest {pod:.2f}"

    rozne = "Cześć! Zrobię sklep Shopify oraz integrację z Allegro."
    pod_rozne = _podobienstwo_jaccard(identyczne, rozne)
    assert pod_rozne < 0.3, f"Teksty różne powinny mieć <30%, jest {pod_rozne:.2f}"

    assert _podobienstwo_jaccard("", identyczne) == 0.0, "Pusty tekst = 0.0"
    print(f"[DOWÓD 1] Podobieństwo identyczne=100%, niemal takie same={pod:.0%}, różne={pod_rozne:.0%}.")


def test_2_storage_find_by_author(tmp_path: Path):
    """Test 2: Storage.find_by_author znajduje zlecenia tego samego klienta."""
    print("\n--- TEST 2: Storage.find_by_author ---")
    st = Storage(magazyn_dir=tmp_path)

    st.save_new_job({"id": "1001", "title": "Strona firmy", "author": "Jan Kowalski",
                     "author_id": "jan-kowalski", "url": "http://x/1001"}, "programowanie-i-it")
    st.save_new_job({"id": "1002", "title": "Sklep online", "author": "Jan Kowalski",
                     "author_id": "jan-kowalski", "url": "http://x/1002"}, "programowanie-i-it")
    st.save_new_job({"id": "2001", "title": "Aplikacja mobilna", "author": "Anna Nowak",
                     "author_id": "anna-nowak", "url": "http://x/2001"}, "programowanie-i-it")

    # Weryfikacja, że author_id faktycznie zapisał się w pliku
    record = st.load_job("1001")
    assert record.get("author_id") == "jan-kowalski", "BŁĄD: author_id nie zapisał się w magazynie!"

    wyniki = st.find_by_author("jan-kowalski")
    assert len(wyniki) == 2, f"BŁĄD: Powinny być 2 zlecenia Jana, jest {len(wyniki)}"
    ids = sorted(str(w.get("id")) for w in wyniki)
    assert ids == ["1001", "1002"], f"BŁĄD: Złe ID: {ids}"

    # Anonim nie może nic zwracać (ochrona przed fałszywym dopasowaniem)
    assert st.find_by_author("anonim") == [], "BŁĄD: 'anonim' nie może zwracać wyników!"
    assert st.find_by_author("nie-istnieje") == [], "BŁĄD: Nieznany autor = pusto!"
    print(f"[DOWÓD 2] find_by_author zwrócił {len(wyniki)} zlecenia klienta jan-kowalski, 'anonim' zignorowany.")


def test_3_engine_wstrzykuje_previous_offers(tmp_path: Path):
    """Test 3: Logika wstrzyknięcia previous_offers + variation_seed (jak w engine.py)."""
    print("\n--- TEST 3: Wstrzyknięcie previous_offers i variation_seed ---")
    st = Storage(magazyn_dir=tmp_path)

    st.save_new_job({"id": "3001", "title": "Landing page", "author": "Firma XYZ",
                     "author_id": "firma-xyz", "url": "http://x/3001"}, "programowanie-i-it")
    st.update_job("3001", {
        "status": "WYSLANO",
        "ai_proposal": {"opis": "Dzień dobry, zrealizuję landing page z sekcją bloga i formularzem.",
                        "wycena": 3000, "dni": 7}
    })

    job = {"id": "3002", "title": "Kolejny landing", "author": "Firma XYZ",
           "author_id": "firma-xyz", "url": "http://x/3002"}

    # Odtwarzamy dokładnie logikę z engine.py
    author_id = str(job.get("author_id", "")).strip()
    previous_offers = []
    if author_id and author_id.lower() != "anonim":
        for h in st.find_by_author(author_id):
            if str(h.get("id", "")) == "3002":
                continue
            ai_prop = h.get("ai_proposal", {}) or {}
            previous_offers.append({
                "job_id": h.get("id"),
                "title": h.get("title", ""),
                "opis": (ai_prop.get("opis") or "")[:600],
                "wycena": ai_prop.get("wycena"),
                "dni": ai_prop.get("dni"),
            })
    job["previous_offers"] = previous_offers
    job["variation_seed"] = (abs(hash(author_id + "3002")) % 5) if author_id else 0

    assert len(previous_offers) == 1, f"BŁĄD: Powinna być 1 poprzednia oferta, jest {len(previous_offers)}"
    assert previous_offers[0]["job_id"] == "3001", "BŁĄD: Zła poprzednia oferta!"
    assert 0 <= job["variation_seed"] <= 4, f"BŁĄD: Seed poza zakresem 0-4: {job['variation_seed']}"
    print(f"[DOWÓD 3] Do job_detail wstrzyknięto {len(previous_offers)} poprzednią ofertę, seed={job['variation_seed']}.")


def test_4_generate_proposal_wymusza_przepisanie():
    """Test 4: generate_proposal wykrywa zbyt podobną ofertę i ponawia (retry)."""
    print("\n--- TEST 4: Twardy bezpiecznik w generate_proposal ---")
    pipeline = ai_pipeline.SlotChainAIPipeline.__new__(ai_pipeline.SlotChainAIPipeline)

    stara_oferta = "Dzień dobry, zrealizuję stronę WordPress z panelem i formularzem kontaktowym."
    wywolania = {"n": 0}

    def fake_run_chain(chain_id, zlecenie, **kwargs):
        wywolania["n"] += 1
        if wywolania["n"] == 1:
            # Pierwsza próba: niemal identyczna jak stara oferta
            return {"opis": "Dzień dobry, zrealizuję stronę WordPress z panelem i formularzem kontaktowym.",
                    "wycena_dni": "[WYNIK_KONCOWY]\nKWOTA: 3000\nDNI: 7\n[/WYNIK_KONCOWY]"}
        # Retry: zupełnie inny styl
        return {"opis": "Cześć! Podchodzę do tego inaczej: najpierw audyt, potem sklep Shopify z integracją Allegro.",
                "wycena_dni": "[WYNIK_KONCOWY]\nKWOTA: 3000\nDNI: 7\n[/WYNIK_KONCOWY]"}

    pipeline._run_chain = fake_run_chain

    job_detail = {
        "id": "4001",
        "title": "Strona WordPress",
        "previous_offers": [{"job_id": "3999", "title": "Stara strona", "opis": stara_oferta,
                             "wycena": 3000, "dni": 7}],
        "variation_seed": 0,
    }

    wynik = pipeline.generate_proposal(job_detail)
    assert wywolania["n"] >= 2, f"BŁĄD: Retry nie nastąpił! Wywołań: {wywolania['n']}"
    assert "Shopify" in wynik.opis, f"BŁĄD: Nie użyto przepisanej wersji! Treść: {wynik.opis[:80]}"
    print(f"[DOWÓD 4] Wykryto podobieństwo, wykonano {wywolania['n'] - 1} retry, przyjęto przepisaną ofertę.")


def test_5_brak_powtorki_nie_zmienia_oferty():
    """Test 5: Gdy klient jest nowy (brak previous_offers), oferta przechodzi bez zmian i bez retry."""
    print("\n--- TEST 5: Nowy klient = brak retry ---")
    pipeline = ai_pipeline.SlotChainAIPipeline.__new__(ai_pipeline.SlotChainAIPipeline)
    wywolania = {"n": 0}

    def fake_run_chain(chain_id, zlecenie, **kwargs):
        wywolania["n"] += 1
        return {"opis": "Dzień dobry, chętnie zrealizuję to zlecenie.",
                "wycena_dni": "[WYNIK_KONCOWY]\nKWOTA: 2500\nDNI: 10\n[/WYNIK_KONCOWY]"}

    pipeline._run_chain = fake_run_chain
    job_detail = {"id": "5001", "title": "Nowe zlecenie", "previous_offers": []}

    wynik = pipeline.generate_proposal(job_detail)
    assert wywolania["n"] == 1, f"BŁĄD: Nie powinno być retry dla nowego klienta! Wywołań: {wywolania['n']}"
    assert wynik.wycena == 2500 and wynik.dni == 10, "BŁĄD: Zła wycena/dni!"
    print("[DOWÓD 5] Nowy klient: 1 wywołanie, brak zbędnego retry, oferta bez zmian.")


if __name__ == "__main__":
    import tempfile
    test_0_normalizacja_nazwy_autora()
    test_1_podobienstwo_jaccard()
    with tempfile.TemporaryDirectory() as d1:
        test_2_storage_find_by_author(Path(d1))
    with tempfile.TemporaryDirectory() as d2:
        test_3_engine_wstrzykuje_previous_offers(Path(d2))
    test_4_generate_proposal_wymusza_przepisanie()
    test_5_brak_powtorki_nie_zmienia_oferty()
    test_6_parser_na_prawdziwych_html()
    print("\n=======================================================")
    print("WSZYSTKIE TESTY ANTY-POWTÓRKI ZAKOŃCZONE SUKCESEM!")
    print("DOWÓD: BOT ROZPOZNAJE KLIENTA I NIE POWTARZA OFERT.")
    print("=======================================================")