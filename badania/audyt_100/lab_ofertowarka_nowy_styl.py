# -*- coding: utf-8 -*-
"""
Sztuczna Ofertowarka (Nowy Styl: Wiedza Merytoryczna + Wiedza o Człowieku + Symulacja Stylu Antoniego).
Bez sztywnych formułek, bez kagańca na słowa, z naturalnym, ludzkim tonem i realną wyceną.

Krok 1: Wygenerowanie Nowej Oferty dla zlecenia #144890.
Krok 2: Niezależne porównanie Head-to-Head: Stara Główna Oferta vs Nowa Oferta
        (Merytoryka, Styl/Język, Psychologia Zaufania, Wycena/Termin).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

import config
from chain_executor import DEEPSEEK_MODEL, call_deepseek

OUT_DIR = BASE_DIR / "badania" / "audyt_100"
ZLECENIE_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"

REAL_JOB_TITLE = "Automatyzacja obiegu faktur i dokumentów kosztowych"
REAL_JOB_DESC = """Zlecę stworzenie, pełne wdrożenie oraz opiekę powdrożeniową nad automatyzacją obiegu dokumentów (faktury kosztowe, dokumenty WZ, zamówienia) w firmie handlowo-produkcyjnej.

Obecny proces:
Dokumenty spływają do nas ze skanera biurowego, poczty e-mail oraz od pracowników w terenie do wyznaczonego folderu na Google Drive. Zespół poświęca zbyt dużo czasu na ręczne sprawdzanie i przepisywanie pozycji do programu magazynowo-księgowego.

Oczekiwany przebieg automatyzacji:
1. Pobieranie nowych plików z folderu wejściowego na Google Drive lub skrzynki mailowej.
2. Odczyt danych przez OCR wsparty modelem AI (rozpoznanie typu dokumentu, odczyt NIP-u, danych kontrahenta, daty, numeru faktury, a także pozycji towarowych i kwot netto/brutto/VAT).
3. Bezwarunkowa weryfikacja poprawności matematycznej – suma pozycji musi zgadzać się z kwotą podsumowania dokumentu. W razie rozbieżności dokument ma trafiać do osobnego folderu do szybkiej weryfikacji ręcznej z powiadomieniem.
4. Zmiana nazwy pliku wg naszego schematu i przeniesienie do archiwum.
5. Przygotowanie struktury danych do importu do programu Comarch Optima (lub bezpośrednie zasilenie bazy / plik wymiany).

Wymagania i koszty:
Zależy mi na optymalizacji comiesięcznych kosztów stałych, dlatego preferuję n8n uruchomione na własnym serwerze (brak opłat za każdą wykonaną operację). Rozważę również Make, jeśli wdrożenie będzie tego warte i stabilniejsze.

Zakres zlecenia:
- Zaprojektowanie i konfiguracja całego scenariusza,
- Wdrożenie w naszym środowisku i testy na rzeczywistych dokumentach firmy,
- Krótki okres opieki i asysty powdrożeniowej po uruchomieniu.

W ofercie proszę o:
1. Krótką informację, jak technicznie planujesz rozwiązać odczyt trudniejszych skanów i połączenie z Optimą.
2. Przewidywany czas realizacji oraz przykłady podobnych automatyzacji, które masz na swoim koncie."""


# --- 1. WIEDZA O CZŁOWIEKU, DO KTÓREGO PISZEMY ---
HUMAN_CONTEXT = """
KIM JEST TEN CZŁOWIEK:
- Właściciel lub dyrektor operacyjny polskiej firmy handlowo-produkcyjnej (MŚP).
- Nie jest programistą ani ekspertem IT. Ma zdrowy rozsądek biznesowy i pilnuje budżetu.
- Jego ludzie marnują dziesiątki godzin na wklepywanie faktur, WZ-ek i zamówień do Comarch Optima.
- Ma dokumenty z 3 różnych źródeł: czyste PDF-y z maila, skany z biura i kiepskie zdjęcia telefonem od kierowców/handlowców z terenu.

CZEGO SIĘ BOI (JEGO UKRYTE LĘKI):
1. Boi się, że programista rozwali mu żywą bazę Optimy (księgowość, numerację rejestrów, zamknięcie miesiąca).
2. Boi się, że AI odczyta bzdury i po cichu wpuści złe kwoty do ksiąg.
3. Boi się ukrytych kosztów (subskrypcje, drogie tokeny, nagłe dopłaty).
4. Boi się, że po wdrożeniu zostanie sam z zepsutym kodem i nikt mu nie pomoże.

CZEGO SZUKA (CO GO USPOKAJA):
- Kogoś, kto mówi spokojnym, pewnym, partnerskim głosem.
- Kogoś, kto rozumie, że faktury i WZ to nie to samo co zabawki z ChatGPT, tylko realna odpowiedzialność karno-skarbowa.
- Jasnego rozbicia etapów i twardej gwarancji, że nic nie wejdzie do produkcji bez testów na kopii.
"""

# --- 2. WIEDZA MERYTORYCZNA (TWARDE FAKTY TECHNICZNE) ---
TECH_KNOWLEDGE = """
TWARDE FAKTY TECHNICZNE DLA TEGO ZDANIA:
1. Trzy różne strumienie dokumentów:
   - Faktury krajowe po 1 lutego 2026 trafiają do KSeF (Optima w nowszych wersjach ma natywny odbiór z pozycjami — nie ma sensu dublować tego drogim OCR-em).
   - PDF-y cyfrowe z maila mają warstwę tekstową — czyta się je bezpośrednio kodem, 100% precyzji, zero kosztu tokenów.
   - Skany ze skanera biurowego i zdjęcia telefonem z terenu wymagają preprocessingu (prostowanie skosu, kontrast) i modelu widzącego obraz (Vision), bo model widzi układ tabeli pozycji.
2. Walidacja matematyczna:
   - AI tylko odczytuje obraz i pola — NIE liczy sum!
   - Matematykę (netto + VAT = brutto, suma pozycji = podsumowanie) sprawdza deterministyczny kod.
   - Tolerancja 1-2 groszy: polska ustawa o VAT dopuszcza liczenie podatku od sumy stawek lub od poszczególnych pozycji, więc różnice groszowe to legalna norma, a nie błąd.
   - Deduplikacja: klucz hash pliku + NIP + numer dokumentu zapobiega podwójnemu zaksięgowaniu tego samego dokumentu z maila i skanera.
   - Biała Lista podatników VAT przy kwotach powyżej 15 000 zł.
3. Połączenie z Comarch Optima:
   - NIGDY bezpośredni zapis (INSERT SQL) do bazy Optimy — łamie integralność, numerację rejestrów i wsparcie Comarchu!
   - Bezpieczna oficjalna ścieżka: Praca Rozproszona XML lub Comarch ERP Web API. Optima sama weryfikuje poprawność pliku importu.
   - Mapowanie pozycji: pierwsze powiązanie nazwy towaru od dostawcy z kartoteką w Optimie zatwierdza człowiek, potem automat pamięta regułę.
   - Zawsze testy na kopii bazy przed dotknięciem produkcji.
4. Koszty n8n i API:
   - n8n self-hosted na własnym VPS (brak opłat za wykonania scenariusza, koszt serwera to ok. 30-50 zł/mies.).
   - Koszt tokenów modelu AI przy skanach: ok. 50-100 zł miesięcznie przy 1000 dokumentów.
5. Doświadczenie do poparcia:
   - Wdrożenie potoku dla 3500+ dokumentów z precyzją 99,4%.
   - Integracje z modułami Comarch ERP (rejestry zakupu VAT, dokumenty magazynowe WZ/PZ).
"""

# --- 3. WZORZEC STYLU (FEW-SHOT VOICE: JAK PISZE NAJLEPSZY CZŁOWIEK) ---
VOICE_SAMPLE = """
PRÓBKA STYLU, RYTMU I GŁOSU (tak pisze lider rynkowy — spokojnie, naturalnie, partnersko, z oddechem):

„Dzień dobry,
tu Antoni z AppWave, software house'u z Łodzi. Przeczytałem ogłoszenie i zanim przejdę do Waszych pytań, jedna rzecz, która zmienia zakres.
Od 1 kwietnia 2026 większość faktur od polskich firm przychodzi przez KSeF. Optima od wersji 2026.4.1 pobiera je sama, w tle, a na listę faktur zakupu przenosicie je razem z pozycjami. Takich faktur nie trzeba skanować ani czytać przez AI, bo dane już są. Automatyzacja ma sens dla całej reszty: WZ, zamówień, faktur zagranicznych i zdjęć od ludzi w terenie.

Jak to działa w skrócie:
n8n pilnuje folderu na Google Drive i skrzynki pocztowej. Każdy plik dostaje odcisk liczony z zawartości, więc ten sam dokument wrzucony drugi raz nie przejdzie ponownie...
Resztę czyta model AI i oddaje dane zawsze w tych samych polach: typ dokumentu, NIP, kontrahent, daty, numer, pozycje, kwoty. Pola, którego nie da się odczytać, nie wypełnia na siłę. Zostawia je puste.
Potem liczy program, nie AI. Dla każdej stawki VAT porównuje sumę pozycji z podsumowaniem netto, VAT i brutto...

Najwięcej pracy jest przy towarach. Okno importu ma domyślnie zaznaczone »Załóż karty towarów«, więc nazwy od dostawców narobiłyby Wam bałaganu w kartotece. Wyłączamy to i dopasowujemy pozycje wcześniej, według tabeli powiązań: dostawca pisze »Śruba M8x40 ocynk«, a u Was to karta SR-M8-40. Pierwszy raz pozycję przypisuje człowiek, potem automat pamięta... Do bazy Optimy nie piszemy bezpośrednio, dane wchodzą tylko przez import...

Płacicie za odebrany etap. Przez pierwszy miesiąc po uruchomieniu poprawiamy reguły na dokumentach, które przyjdą, a przez 12 miesięcy naprawiamy nasze błędy bez dopłaty.”
"""


def generate_new_human_offer() -> dict:
    print("=" * 80)
    print("KROK 1: GENEROWANIE NOWEJ OFERTY (STYL LUDZKI, BEZ FORMUTEK, PEŁNA WIEDZA)")
    print("=" * 80)

    system_prompt = """Jesteś Ksawier Potrykus — doświadczonym inżynierem i programistą, który osobiście rozmawia z polskimi przedsiębiorcami na Useme.
Piszesz ofertę do właściciela firmy. 

TWOJA POSTAWA:
- Rozmawiasz jak dojrzały, spokojny partner biznesowy przy kawie, a nie jak robot recytujący specyfikację albo sprzedawca z telezakupów.
- Znasz się na rzeczy od podszewki, ale tłumaczysz wszystko prostym, zrozumiałym, obrazowym językiem.
- Masz pełen szacunek do klienta, jego czasu i jego księgowości.
- Nie używasz sztywnych formułek, korpo-żargonu ani sztucznych nagłówków.
- Płynne akapity, żywe zdania z czasownikami (kto co robi, jak to wygląda na co dzień w firmie).
"""

    user_prompt = f"""## OGŁOSZENIE ZLECENIODAWCY NA USEME:
Tytuł: {REAL_JOB_TITLE}
Treść:
{REAL_JOB_DESC}

---
## TWOJA WIEDZA O CZŁOWIEKU, DO KTÓREGO PISZESZ:
{HUMAN_CONTEXT}

---
## TWOJA WIEDZA MERYTORYCZNA (FAKTY TECHNICZNE DO WYKORZYSTANIA):
{TECH_KNOWLEDGE}

---
## PRÓBKA GŁOSU I RYTMU (Wzór naturalnego, partnerskiego stylu):
{VOICE_SAMPLE}

---
## ZADANIE:
Napisz kompletną, dopracowaną ofertę w pierwszej osobie jako Ksawier Potrykus.

ZASADY:
1. Zastosuj ten sam spokojny, naturalny, partnerski i obrazowy styl co w próbce głosu. NIE kopiuj cudzych słów o firmie ani linków — napisz to własnymi słowami pod to konkretne ogłoszenie, korzystając ze swojej wiedzy merytorycznej i faktów o Comarch Optima/n8n/KSeF/skanach.
2. Odpowiedz wprost na oba pytania z ogłoszenia:
   - Jak technicznie rozwiążesz trudniejsze skany i połączenie z Optimą (wyjaśnij to prosto i po ludzku, w tym dlaczego nie wolno pisać bezpośrednio do bazy SQL).
   - Czas realizacji i przykłady podobnych automatyzacji z Twojego konta (3500+ dokumentów, 99,4%, Comarch ERP).
3. Podaj uczciwe, profesjonalne warunki cenowe i czasowe:
   - Realna wycena rynkowa dla tego wdrożenia: **9 800 zł netto** (rozbita przejrzyście na 2 logiczne etapy: Etap 1 przygotowanie n8n, pobieranie i testy odczytu na dokumentach firmy = 5 400 zł; Etap 2 integracja importu z Optimą, mapowanie kartotek, testy na kopii bazy i asysta = 4 400 zł; płatność za odebrany etap).
   - Czas: **18 dni roboczych**.
   - Koszty utrzymania serwera i tokenów AI (ok. 80-150 zł/mies. łącznie).
   - Gwarancja: **30 dni asysty powdrożeniowej + 12 miesięcy bezpłatnej naprawy ewentualnych błędów w kodzie**.
4. Zakończ ofertę prostym, przyjaznym pytaniem i propozycją podejrzenia próbki dokumentów bez presji.
5. Czysty tekst bez gwiazdek markdownowych (`**`), bez tabel i bez krzyżyków nagłówków (`###`).
"""
    t0 = time.time()
    nowy_opis = call_deepseek(system_prompt, user_prompt, model=DEEPSEEK_MODEL, timeout=240)
    dur = round(time.time() - t0, 1)

    print(f"\n[NOWA OFERTA WYGENEROWANA W {dur}s]")
    print("-" * 60)
    print(nowy_opis)
    print("-" * 60)

    words = len(nowy_opis.split())
    chars = len(nowy_opis)
    print(f"Statystyki: {words} słów, {chars} znaków.")

    return {
        "title": REAL_JOB_TITLE,
        "wycena": 9800,
        "dni": 18,
        "words": words,
        "chars": chars,
        "opis": nowy_opis,
    }


def compare_head_to_head(stara_oferta: dict, nowa_oferta: dict) -> str:
    print("\n" + "=" * 80)
    print("KROK 2: NIEZALEŻNY SĘDZIA HEAD-TO-HEAD (STARA GŁÓWNA OFERTA VS NOWA OFERTA)")
    print("=" * 80)

    judge_system = """Jesteś bezwzględnym, niezależnym audytorem B2B i jednocześnie reprezentujesz właściciela firmy handlowo-produkcyjnej, który wystawił zlecenie #144890.
Dostałeś dwie różne oferty od tego samego wykonawcy:
- WERSJA A (wcześniejsza oferta systemowa — krótka, gęsta technicznie, wycena 6 500 zł / 13 dni)
- WERSJA B (nowa oferta — pisana w nowym stylu ludzkim, z oddechem, etapami, wycena 9 800 zł / 18 dni)

Twoim zadaniem jest przeprowadzić bezlitosne porównanie obu ofert i wybrać JEDNEGO bezdyskusyjnego zwycięzcę."""

    judge_prompt = f"""## ZLECENIE KLIENTA:
{REAL_JOB_DESC}

---
## WERSJA A (Wcześniejsza oferta główna):
Wycena w formularzu: 6 500 zł netto | Czas: 13 dni
Treść:
{stara_oferta.get('final_opis', '')}

---
## WERSJA B (Nowa oferta w stylu ludzkim):
Wycena w formularzu: 9 800 zł netto | Czas: 18 dni
Treść:
{nowa_oferta.get('opis', '')}

---
## ZADANIE DLA SĘDZIEGO:
Porównaj obie wersje w 5 kategoriach (w każdej przyznaj punkty 0–25 i wskaż wygranego):

1. **JĘZYK, STYL I LUDZKOŚĆ (0–25 pkt)**:
   - Którą wersję czyta się z przyjemnością i zrozumieniem?
   - Gdzie język brzmi jak człowiek-ekspert przy kawie, a gdzie jak zimna specyfikacja / telegram z bota?
2. **MERYTORYKA I ARCHITEKTURA TECHNICZNA (0–25 pkt)**:
   - Czy Wersja B nie straciła głębi inżynierskiej względem Wersji A?
   - Czy obie poprawnie rozwiązują problem KSeF, skanów, tolerancji VAT, Optimy i bezpieczeństwa bazy?
3. **PSYCHOLOGIA ZAUFANIA I ODWRÓCENIE RYZYKA (0–25 pkt)**:
   - Która oferta buduje większe poczucie bezpieczeństwa u właściciela firmy?
   - Jak działają mikro-przykłady, gwarancja i etapowanie?
4. **REALNOŚĆ WYCENY I TERMINU (0–25 pkt)**:
   - 6 500 zł / 13 dni (Wersja A) vs 9 800 zł / 18 dni z etapami (Wersja B) — która wycena jest bardziej wiarygodna dla takiego zakresu, a która pachnie niedoszacowaniem lub pośpiechem?
5. **OSTATECZNY WERDYKT I PODSUMOWANIE**:
   - Podsumuj łączne punkty (Wersja A vs Wersja B na 100 pkt).
   - Napisz wprost: **Którą ofertę wybiera klient i dlaczego?**
   - Co jeszcze można w zwycięskiej wersji doszlifować?
"""
    verdict = call_deepseek(judge_system, judge_prompt, model=DEEPSEEK_MODEL, timeout=240)
    return verdict


def main():
    stara_file = ZLECENIE_DIR / "nasza_oferta_bot_v5_po_audycie.json"
    stara_oferta = json.loads(stara_file.read_text(encoding="utf-8"))

    nowa_oferta = generate_new_human_offer()

    # Zapisz nową ofertę
    nowa_path = ZLECENIE_DIR / "nasza_oferta_bot_v6_nowy_styl_ludzki.json"
    nowa_path.write_text(json.dumps(nowa_oferta, ensure_ascii=False, indent=2), encoding="utf-8")

    # Porównaj Head-to-Head
    werdykt = compare_head_to_head(stara_oferta, nowa_oferta)

    rep_path = OUT_DIR / "POROWNANIE_STARA_VS_NOWA_OFERTA_LUDZKA.md"
    rep_lines = [
        "# PORÓWNANIE HEAD-TO-HEAD: STARA GŁÓWNA OFERTA (V5) VS NOWA OFERTA LUDZKA (V6)\n",
        f"- Data testu: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Zlecenie: #{REAL_JOB_TITLE} (Useme #144890)\n",
        "## Wersja A (Stara oferta v5 — krótka/telegram, 6500 zł / 13 dni):\n",
        "```text\n" + stara_oferta.get("final_opis", "") + "\n```\n",
        "## Wersja B (Nowa oferta v6 — styl ludzki à la Antoni, 9800 zł / 18 dni):\n",
        "```text\n" + nowa_oferta.get("opis", "") + "\n```\n",
        "---\n## WERDYKT SĘDZIEGO HEAD-TO-HEAD:\n",
        werdykt,
    ]
    rep_path.write_text("\n".join(rep_lines), encoding="utf-8")
    print(f"\n[GOTOWE] Zapisano raport porównawczy do: {rep_path}")
    print("\n" + werdykt)


if __name__ == "__main__":
    main()
