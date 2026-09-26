# -*- coding: utf-8 -*-
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
KOD_DIR = BASE / "kod"
if str(KOD_DIR) not in sys.path:
    sys.path.insert(0, str(KOD_DIR))

from ai_pipeline import SlotChainAIPipeline
from chain_executor import save_checkpoint, clear_checkpoint


def is_port_open(port=4571):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        return s.connect_ex(("127.0.0.1", port)) == 0


def main():
    proc = None
    if not is_port_open(4571):
        print("Starting deepseek-proxy on port 4571...")
        proxy_dir = BASE.parent / "deepseek-proxy"
        proc = subprocess.Popen(
            [sys.executable, "-u", "server.py"],
            cwd=str(proxy_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(30):
            if is_port_open(4571):
                print("deepseek-proxy is ready!")
                break
            time.sleep(1)

    try:
        real_path = BASE / "badania" / "baza" / "ksawierpotrykus3" / "01_ofertowarka" / "programowanie-i-it" / "144890.json"
        raw = json.loads(real_path.read_text(encoding="utf-8"))
        job = {
            "id": "144890-real",
            "title": raw["title"],
            "budget": raw["budget"],
            "category": raw.get("category", "programowanie-i-it"),
            "full_description": raw["full_details"]["full_description"],
            "author": "Real_144890_Client",
            "nadawca_podpis": "Ksawier Potrykus",
        }

        pipeline = SlotChainAIPipeline()
        t0 = time.time()
        print("1. Running filter_offers on REAL 144890.json (NO ProfiPiek)...")
        wybrane = pipeline.filter_offers([job])
        if not wybrane:
            print("Rejected by filter_offers!")
            return
        sel = wybrane[0]
        print(
            f"   -> TIER: {sel.get('tier')} | ŚCIEŻKA: {sel.get('sciezka')} | "
            f"PROFIL: {sel.get('typ_klienta')} | MODYFIKATORY: {sel.get('modyfikatory')}"
        )

        clear_checkpoint("144890-real")
        save_checkpoint(
            "144890-real",
            "01",
            {
                "research": (
                    "# Raport Research — Automatyzacja obiegu dokumentów (Google Drive -> OCR/AI -> Comarch Optima)\n"
                    "- 3 strumienie dokumentów: (1) Faktury ustrukturyzowane z KSeF w formacie XML (Comarch Optima od wersji 2026.4.1 posiada natywną synchronizację KSeF w tle wraz z pozycjami — w n8n warto więc nie dublować ślepo KSeF, lecz skupić się na automatycznym przypisaniu MPK/kategorii, parowaniu z dokumentami WZ/zamówieniami oraz dokumentach spoza KSeF), (2) Cyfrowe PDF-y z maila posiadające natywną warstwę tekstową (bezpośrednie parsowanie bez kosztów Vision i bez ryzyka halucynacji), (3) Skany papierowe oraz zdjęcia z telefonów od pracowników w terenie (wymagają preprocessingu obrazu: prostowania skosu, poprawy kontrastu oraz ekstrakcji Vision LLM z progiem pewności confidence score).\n"
                    "- Walidacja matematyczna: netto + VAT = brutto z tolerancją 1-2 gr (zgodnie z ustawą o VAT dopuszczającą liczenie podatku od sumy stawek lub od sumy poszczególnych pozycji). Weryfikacja kontrahenta w GUS / Białej Liście VAT (szczególnie przy fakturach powyżej 15 000 zł brutto) oraz deduplikacja po kluczu NIP + numer dokumentu + hash pliku.\n"
                    "- Integracja z Comarch Optima: bezpośredni zapis INSERT do tabel SQL w bazie produkcyjnej niesie ryzyko uszkodzenia indeksów, numeracji rejestrów i utraty gwarancji producenta. Bezpiecznym standardem dla Optimy jest import przez strukturę Pracy Rozproszonej XML (obsługującą zarówno rejestry zakupu VAT, jak i dokumenty handlowo-magazynowe WZ, PZ, RW, PW, RO) lub dedykowane API.\n"
                    "- n8n (self-hosted na VPS Docker) vs Make: n8n rozlicza całe wykonanie procesu niezależnie od liczby pętli po pozycjach faktury/WZ i operacji na plikach binarnych, podczas gdy Make nalicza kredyty za każdy moduł i każdą pozycję dokumentu."
                )
            },
        )

        print("2. Running generate_proposal (02b -> 02a -> 08)...")
        prop = pipeline.generate_proposal(sel)
        elapsed = round(time.time() - t0, 1)

        out = {
            "id": "144890",
            "zrodlo_opisu": "REALNE_OGLOSZENIE_USEME_144890.json (bez sztucznego ProfiPiek)",
            "tier": sel.get("tier"),
            "sciezka": sel.get("sciezka"),
            "typ_klienta": sel.get("typ_klienta"),
            "modyfikatory": sel.get("modyfikatory"),
            "wycena": prop.wycena,
            "dni": prop.dni,
            "time_to_offer_s": elapsed,
            "opis": prop.opis,
        }
        out_path = (
            BASE
            / "badania"
            / "baza"
            / "weronikabuchholc13"
            / "04_moje_zlecenia"
            / "zlecenie_testowe_144890"
            / "nasza_oferta_bot_v3_realne_ogloszenie.json"
        )
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n=== GENERATED OFFER ON REAL 144890 (in {elapsed}s) ===")
        print(f"Cena: {prop.wycena} PLN | Dni: {prop.dni}")
        print("-" * 80)
        print(prop.opis)
        print("-" * 80)
    finally:
        if proc:
            proc.terminate()


if __name__ == "__main__":
    main()
