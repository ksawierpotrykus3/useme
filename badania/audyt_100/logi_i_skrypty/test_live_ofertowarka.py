# -*- coding: utf-8 -*-
"""Test na żywo (DeepSeek Proxy port 4571) nowego łańcucha ofertowarki:
1. Selekcja AI (Dual-Track + Typ Klienta + Modyfikatory + Tier A)
2. Generowanie pełnej oferty na zlecenie #144890 (Mystery Shopping - Piekarnia ProfiPiek + Optima)
3. Generowanie pełnej oferty na zlecenie #144817 (Bot do maili firmowych - ścieżka BIZNES / tech_agnostic)
"""

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KOD_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\kod")
BAZA_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\badania\baza")
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

from ai_pipeline import SlotChainAIPipeline
from chain_executor import save_checkpoint, clear_checkpoint


def main():
    pipeline = SlotChainAIPipeline()

    # 1. Wczytanie danych zlecenia #144890 (Mystery Shopping)
    stara_144890_path = BAZA_DIR / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "nasza_oferta_bot.json"
    stara_144890 = json.loads(stara_144890_path.read_text(encoding="utf-8"))

    opis_144890 = (
        "Dzień dobry,\n"
        "Zlecę stworzenie, pełne wdrożenie oraz opiekę serwisową nad automatyzacją obiegu dokumentów "
        "(faktury, zamówienia, dokumenty kosztowe) w firmie z branży piekarniczej.\n"
        "Logika procesu:\n"
        "1. Dokumenty ze skanera, maili oraz aplikacji mobilnej trafiają do folderu wejściowego na Google Drive.\n"
        "2. Automatyzacja pobiera plik, przetwarza go przez silnik OCR wsparty modelem LLM (rozpoznanie typu dokumentu, "
        "wyciągnięcie kluczowych danych, kwot, kontrahenta itp.).\n"
        "3. Plik jest odpowiednio nazywany i przenoszony do docelowego folderu na Google Drive.\n"
        "4. Dane z dokumentu są przekazywane do naszych systemów: ProfiPiek (program piekarniczy) oraz Comarch Optima.\n\n"
        "Wymagania dotyczące technologii i wyceny:\n"
        "Zależy mi na optymalizacji kosztów bieżących, dlatego skłaniam się ku n8n postawionym na własnym serwerze "
        "(brak opłat za każdą operację). Dopuszczam jednak Make, jeśli wdrożenie będzie tego warte.\n"
        "Zależy mi na otrzymaniu:\n"
        "- Wyceny na n8n (z uwzględnieniem postawienia/konfiguracji środowiska),\n"
        "- Opcjonalnie wyceny na Make (lub krótkiego uzasadnienia w ofercie, dlaczego rekomendujesz jedno z tych rozwiązań pod ten konkretny przypadek).\n\n"
        "Zakres zlecenia:\n"
        "Cena musi być kompleksowa i obejmować:\n"
        "- Zaprojektowanie i zbudowanie całej automatyzacji,\n"
        "- Wdrożenie całości w naszym środowisku i przetestowanie na rzeczywistych dokumentach,\n"
        "- Serwis i wsparcie techniczne w razie komplikacji powdrożeniowych (okres gwarancyjny/asysta po uruchomieniu).\n\n"
        "W ofercie proszę o:\n"
        "- Konkretną kwotę (lub widełki dla n8n oraz Make).\n"
        "- Krótki opis, jak technicznie planujesz rozwiązać połączenie z Optimą i ProfiPiekiem (np. API, bezpośrednie zapytania do bazy SQL, pliki wymiany).\n"
        "- Szacowany czas realizacji oraz warunki wsparcia po wdrożeniu."
    )

    # 2. Wczytanie zlecenia #144817 (Bot do maili firmowych - klient nietechniczny)
    j144817_path = BAZA_DIR / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it" / "144817.json"
    j144817_raw = json.loads(j144817_path.read_text(encoding="utf-8"))

    # 3. Wczytanie zlecenia #144867 (Aplikacja mobilna dla fizjoterapeutów)
    j144867_path = BAZA_DIR / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it" / "144867.json"
    j144867_raw = json.loads(j144867_path.read_text(encoding="utf-8"))

    batch_do_selekcji = [
        {
            "id": "144890-test",
            "title": "Automatyzacja obiegu dokumentów (OCR + LLM): n8n / Make",
            "budget": "Do negocjacji",
            "category": "programowanie-i-it",
            "full_description": opis_144890,
            "author": "Piekarnia",
            "nadawca_podpis": "Ksawier Potrykus",
        },
        {
            "id": "144817-test",
            "title": j144817_raw["title"],
            "budget": j144817_raw["budget"],
            "category": "programowanie-i-it",
            "full_description": j144817_raw["full_details"]["full_description"],
            "author": j144817_raw["author"],
            "nadawca_podpis": "Ksawier Potrykus",
        },
        {
            "id": "144867-test",
            "title": j144867_raw["title"],
            "budget": j144867_raw["budget"],
            "category": "programowanie-i-it",
            "full_description": j144867_raw["full_details"]["full_description"],
            "author": j144867_raw["author"],
            "nadawca_podpis": "Ksawier Potrykus",
        },
        {
            "id": "999999-pulapka",
            "title": "Szukamy programisty Python na stałe 160h w biurze za udziały w startupie",
            "budget": "Do negocjacji",
            "category": "programowanie-i-it",
            "full_description": "Szukamy wspólnika technicznego na pełny etat 160h miesięcznie w biurze, rozliczenie wyłącznie za udziały (equity) po zdobyciu inwestora.",
            "author": "StartupWizjoner",
        },
    ]

    print("=" * 80)
    print("ETAP 1: TEST SELEKCJONERA AI (Dual-Track + Taksonomia Klientów + Modyfikatory)")
    print("=" * 80)
    t0 = time.time()
    wybrane = pipeline.filter_offers(batch_do_selekcji)
    print(f"\nCzas selekcji: {time.time() - t0:.1f}s")
    for w in wybrane:
        print(
            f"  -> ID: {w['id']} | TIER: {w.get('tier')} | ŚCIEŻKA: {w.get('sciezka')} "
            f"| PROFIL: {w.get('typ_klienta')} | MODYFIKATORY: {w.get('modyfikatory')}\n"
            f"     POWÓD: {w.get('selection_reason')}"
        )

    by_id = {w["id"]: w for w in wybrane}

    # -------------------------------------------------------------------------
    # ETAP 2: GENEROWANIE OFERTY #144890 (MYSTERY SHOPPING - PORÓWNANIE Z ELITĄ)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("ETAP 2: GENEROWANIE OFERTY #144890 (Mystery Shopping - ProfiPiek + Optima)")
    print("=" * 80)
    job_144890 = by_id.get("144890-test") or batch_do_selekcji[0]
    clear_checkpoint("144890-test")
    # Wstrzykujemy ten sam raport researchu (slot 01) co w benchmarku z 23.09, aby porównać 1:1
    # nową wycenę (90 zł/h) i nową treść (ze scenariuszem msp_erp i bez Google Meet)
    research_144890 = (stara_144890.get("metadata") or {}).get("research", "")
    if research_144890:
        save_checkpoint("144890-test", "01", {"research": research_144890})

    t1 = time.time()
    prop_144890 = pipeline.generate_proposal(job_144890)
    print(f"\n[SUKCES #144890] Czas: {time.time() - t1:.1f}s | Wycena: {prop_144890.wycena} PLN | Dni: {prop_144890.dni}")
    print("-" * 80)
    print(prop_144890.opis)
    print("-" * 80)

    # -------------------------------------------------------------------------
    # ETAP 3: GENEROWANIE OFERTY #144817 (ŚCIEŻKA BIZNES / TECH_AGNOSTIC)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("ETAP 3: GENEROWANIE OFERTY #144817 (Bot do maili firmowych - ścieżka BIZNES)")
    print("=" * 80)
    job_144817 = by_id.get("144817-test") or batch_do_selekcji[1]
    clear_checkpoint("144817-test")
    # Zapiszmy zwięzły research dla 144817, aby przyspieszyć test slotów 02b -> 02a -> 08
    save_checkpoint(
        "144817-test",
        "01",
        {
            "research": (
                "# Raport Research — Asystent odpowiedzi na maile firmowe (#144817)\n"
                "- Klient oczekuje zamkniętego narzędzia uczącego się wyłącznie z firmowego FAQ i historii korespondencji (bez dostępu do otwartego internetu).\n"
                "- Etap 1: tryb szkiców (człowiek zatwierdza lub edytuje odpowiedź przed wysyłką, system zapamiętuje poprawki pracownika).\n"
                "- Etap 2: wysyłka automatyczna dla powtarzalnych zapytań + przekazywanie nietypowych spraw do pracownika.\n"
                "- Koszt utrzymania serwera i modelu językowego przy skali małej/średniej firmy to ok. 50–120 zł miesięcznie."
            ),
        },
    )

    t2 = time.time()
    prop_144817 = pipeline.generate_proposal(job_144817)
    print(f"\n[SUKCES #144817] Czas: {time.time() - t2:.1f}s | Wycena: {prop_144817.wycena} PLN | Dni: {prop_144817.dni}")
    print("-" * 80)
    print(prop_144817.opis)
    print("-" * 80)

    # Zapisz wyniki do pliku JSON do dalszej analizy
    out_path = Path(__file__).parent / "wyniki_testu_live.json"
    out_path.write_text(
        json.dumps(
            {
                "selekcja": [
                    {
                        "id": w["id"],
                        "tier": w.get("tier"),
                        "sciezka": w.get("sciezka"),
                        "typ_klienta": w.get("typ_klienta"),
                        "modyfikatory": w.get("modyfikatory"),
                        "powod": w.get("selection_reason"),
                    }
                    for w in wybrane
                ],
                "oferta_144890_nowa": {
                    "wycena": prop_144890.wycena,
                    "dni": prop_144890.dni,
                    "opis": prop_144890.opis,
                    "powod": prop_144890.powod_wyboru,
                },
                "oferta_144817_nowa": {
                    "wycena": prop_144817.wycena,
                    "dni": prop_144817.dni,
                    "opis": prop_144817.opis,
                    "powod": prop_144817.powod_wyboru,
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nZapisano pełne wyniki do: {out_path}")


if __name__ == "__main__":
    main()
