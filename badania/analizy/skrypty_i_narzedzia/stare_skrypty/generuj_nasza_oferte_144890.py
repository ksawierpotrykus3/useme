# -*- coding: utf-8 -*-
"""Generowanie oferty bota dla zlecenia badawczego #144890 (DRY RUN)."""

import json
import sys
import time
from pathlib import Path

# Ustawienie kodowania konsoli
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ai_pipeline import SlotChainAIPipeline
from storage import clear_checkpoint

TARGET_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

JOB_ID = "144890"

job_detail = {
    "id": JOB_ID,
    "title": "Automatyzacja obiegu faktur i dokumentów kosztowych (OCR + n8n / Make)",
    "author": "Tomasz Zych",
    "author_id": "tomasz-zych",
    "budget": "Do negocjacji",
    "category": "programowanie-i-it",
    "full_description": """<p>Dzień dobry,</p>
<p>Zlecę stworzenie, pełne wdrożenie oraz opiekę serwisową nad automatyzacją obiegu dokumentów (faktury, zamówienia, dokumenty kosztowe) w firmie z branży piekarniczej.</p>
<p>Logika procesu:</p>
<p>Dokumenty ze skanera, maili oraz aplikacji mobilnej trafiają do folderu wejściowego na Google Drive.<br>
Automatyzacja pobiera plik, przetwarza go przez silnik OCR wsparty modelem LLM (rozpoznanie typu dokumentu, wyciągnięcie kluczowych danych, kwot, kontrahenta itp.).<br>
Plik jest odpowiednio nazywany i przenoszony do docelowego folderu na Google Drive.<br>
Dane z dokumentu są przekazywane do naszych systemów: ProfiPiek (program piekarniczy) oraz Comarch Optima.</p>
<p>Wymagania dotyczące technologii i wyceny:</p>
<p>Zależy mi na optymalizacji kosztów bieżących, dlatego skłaniam się ku n8n postawionym na własnym serwerze (brak opłat za każdą operację). Dopuszczam jednak Make, jeśli wdrożenie będzie tego warte.<br>
Zależy mi na otrzymaniu:<br>
Wyceny na n8n (z uwzględnieniem postawienia/konfiguracji środowiska),<br>
Opcjonalnie wyceny na Make (lub krótkiego uzasadnienia w ofercie, dlaczego rekomendujesz jedno z tych rozwiązań pod ten konkretny przypadek).</p>
<p>Zakres zlecenia:</p>
<p>Cena musi być kompleksowa i obejmować:<br>
Zaprojektowanie i zbudowanie całej automatyzacji,<br>
Wdrożenie całości w naszym środowisku i przetestowanie na rzeczywistych dokumentach,<br>
Serwis i wsparcie techniczne w razie komplikacji powdrożeniowych (okres gwarancyjny/asysta po uruchomieniu).</p>
<p>W ofercie proszę o:<br>
Konkretną kwotę (lub widełki dla n8n oraz Make).<br>
Krótki opis, jak technicznie planujesz rozwiązać połączenie z Optimą i ProfiPiekiem (np. API, bezpośrednie zapytania do bazy SQL, pliki wymiany).<br>
Szacowany czas realizacji oraz warunki wsparcia po wdrożeniu.</p>""",
    "tier": "A",
    "stawka_seed": f"{JOB_ID}-konto1",
    "variation_seed": 0,
    "tryb": "konserwatywny",
}

print(f"=== ROZPOCZYNAM GENEROWANIE OFERTY BOTA DLA ZLECENIA #{JOB_ID} ===")
print("Czyszczenie ewentualnych starych checkpointów...")
clear_checkpoint(f"useme-job-{JOB_ID}")

start_time = time.time()
pipeline = SlotChainAIPipeline()

try:
    wynik = pipeline.generate_proposal(job_detail)
    elapsed = time.time() - start_time
    print(f"\n[SUKCES] Generowanie oferty powiodło się w {elapsed:.1f}s!")
    print(f"Wycena: {wynik.wycena} PLN | Dni pracy: {wynik.dni}")
    print("=" * 60)
    print("[TREŚĆ OFERTY]:")
    print(wynik.opis)
    print("=" * 60)

    # Zapis surowej oferty bota
    bot_offer_file = TARGET_DIR / "nasza_oferta_bot.json"
    offer_data = {
        "job_id": JOB_ID,
        "wycena": wynik.wycena,
        "dni": wynik.dni,
        "opis": wynik.opis,
        "powod_wyboru": wynik.powod_wyboru,
        "metadata": wynik.metadata,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generation_time_s": round(elapsed, 2)
    }
    bot_offer_file.write_text(json.dumps(offer_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Zapisano naszą ofertę do: {bot_offer_file}")

except Exception as e:
    print(f"[BŁĄD GENEROWANIA]: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
