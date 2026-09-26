# -*- coding: utf-8 -*-
"""
Ślepy Turniej 99 Kandydatów (85 ofert publicznych + 13 wiadomości PV + 1 nasza zanonimizowana oferta)
dla realnego zlecenia Useme #144890 (Automatyzacja obiegu faktur i dokumentów kosztowych).

Krok 1: Nasza zaktualizowana Ofertowarka (ChainExecutor + Audytor 100) generuje ofertę do realnego ogłoszenia #144890.
Krok 2: Oferta zostaje w 100% zanonimizowana (usunięty podpis Ksawier Potrykus, nadany losowy numer KANDYDAT #48,
        mediana umów: 5 umów) i wrzucona w środek puli 85 ofert publicznych oraz 14 wiadomości prywatnych (PV).
Krok 3: Niezależny 3-etapowy Łańcuch Oceniający (Klient / Przedsiębiorca, który NIE WIE, że którakolwiek oferta jest nasza):
        - Etap 1: 3 koszyki eliminacyjne (po 33 kandydatów) -> wyłania Top 6 z każdego koszyka (18 półfinalistów).
        - Etap 2: Półfinał 18 najlepszych (oferty publiczne + PV) -> zawężenie do Top 7 i głęboka analiza każdego z 18.
        - Etap 3: Wielki Finał -> Ostateczny ranking, wybór zwycięzcy i bezlitosne porównanie wszystkich finalistów.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
KOD_DIR = BASE_DIR / "kod"
sys.path.insert(0, str(KOD_DIR))

import config
from ai_pipeline import SlotChainAIPipeline
from chain_executor import DEEPSEEK_MODEL, call_deepseek
from audytor_lancuch import (
    audit_and_refine_100,
    evaluate_offer_100,
    generate_initial_offer,
    _sanitize_opis,
)

ZLECENIE_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"
OUT_DIR = BASE_DIR / "badania" / "audyt_100"

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


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    for attempt in range(3):
        try:
            odp = call_deepseek(system_prompt, user_prompt, model=DEEPSEEK_MODEL, timeout=240)
            if odp:
                return odp
        except Exception as e:
            print(f"[WARN] LLM call attempt {attempt+1} failed: {e}")
        time.sleep(5)
    raise RuntimeError("Failed to call LLM after 3 attempts")


def strip_identifying_signature(text: str) -> str:
    """Usuwa podpis 'Ksawier Potrykus' / 'Ksawier' z końca naszej oferty, żeby test był w 100% ślepy."""
    cleaned = re.sub(r"\n*(Pozdrawiam,?\s*)?Ksawier(\s+Potrykus)?\s*$", "", text.strip(), flags=re.IGNORECASE)
    return cleaned.strip()


def step1_generate_our_offer() -> dict:
    out_offer_path = ZLECENIE_DIR / "nasza_oferta_bot_v5_po_audycie.json"
    # Wczytaj wcześniej wygenerowaną ścieżkę BIZNES (z task-1152), jeśli istnieje
    biznes_offer = None
    if out_offer_path.exists():
        try:
            prev = json.loads(out_offer_path.read_text(encoding="utf-8"))
            if prev.get("r1_opis"):
                biznes_offer = prev
        except Exception:
            pass

    print("=" * 80)
    print("KROK 1: GENEROWANIE OFERTY (ŚCIEŻKA INŻYNIERIA / MSP_ERP) PRZEZ NASZĄ OFERTOWARKĘ DLA #144890")
    print("=" * 80)
    pipeline = SlotChainAIPipeline()
    job_ctx = {
        "id": "144890",
        "title": REAL_JOB_TITLE,
        "description": REAL_JOB_DESC,
        "description_short": REAL_JOB_DESC,
        "budget": "Do negocjacji",
        "offers_count": 85,
        "category": "Oprogramowanie",
    }
    wybrane = pipeline.filter_offers([job_ctx])
    if wybrane:
        job_ctx = wybrane[0]
        job_ctx["description"] = REAL_JOB_DESC
    else:
        job_ctx.update({
            "tier": "A",
            "sciezka": "inzynieria",
            "typ_klienta": "msp_erp",
            "karta_tech": "tech_02",
            "modyfikatory": [],
        })

    r1_opis, wycena, dni, wyc_raw_r1, res_text = generate_initial_offer(job_ctx)
    r1_opis = _sanitize_opis(r1_opis, wycena=wycena, dni=dni)
    wycena = int(wycena or 0)
    dni = int(dni or 14)

    print(f"[OFERTOWARKA R1 - {job_ctx.get('sciezka')}/{job_ctx.get('typ_klienta')}] Wycena: {wycena} zł | Dni: {dni} | Długość: {len(r1_opis.split())} słów")
    print("-" * 60)
    print(r1_opis)
    print("-" * 60)

    audyt_r1 = evaluate_offer_100(job_ctx, r1_opis, wycena, dni, wyc_raw_r1)
    r1_score = int(audyt_r1.get("wynik_100", 0))
    final_opis = r1_opis
    final_score = r1_score
    rounds = 1
    audyt_r2 = None

    if r1_score < config.AUDYTOR_100_TARGET_SCORE:
        ref = audit_and_refine_100(
            job_ctx,
            r1_opis,
            wycena,
            dni,
            wycena_raw=wyc_raw_r1,
            research_text=res_text,
            target_score=config.AUDYTOR_100_TARGET_SCORE,
            max_rounds=1,
        )
        final_opis = ref["opis"]
        wycena = int(ref["wycena"])
        dni = int(ref["dni"])
        audyt_r2 = ref["audyt_final"]
        final_score = int(audyt_r2.get("wynik_100", r1_score))
        rounds = ref["rounds"]

    print(f"[AUDYTOR 100] R1 Score: {r1_score}/100 -> Final Score (R{rounds}): {final_score}/100")
    if rounds > 1:
        print("FINALNY OPIS PO R2:")
        print(final_opis)

    saved = {
        "id": "144890",
        "title": REAL_JOB_TITLE,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "klasyfikacja": {
            "tier": job_ctx.get("tier"),
            "sciezka": job_ctx.get("sciezka"),
            "typ_klienta": job_ctx.get("typ_klienta"),
            "karta_tech": job_ctx.get("karta_tech"),
        },
        "wycena": wycena,
        "dni": dni,
        "r1_score": r1_score,
        "final_score": final_score,
        "rounds_run": rounds,
        "r1_opis": r1_opis,
        "final_opis": final_opis,
        "wycena_raw": wyc_raw_r1,
        "audit_runda_1": audyt_r1,
        "audit_runda_2": audyt_r2,
        "biznes_variant": biznes_offer,
    }
    out_offer_path.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")
    return saved


def build_blind_pool(our_offer: dict) -> tuple[list[dict], list[int]]:
    offers_file = ZLECENIE_DIR / "oferty_publiczne_30.json"
    pv_file = ZLECENIE_DIR / "wiadomosci_zleceniodawcy_pelne.json"

    public_offers = json.loads(offers_file.read_text(encoding="utf-8"))
    pv_threads = json.loads(pv_file.read_text(encoding="utf-8"))

    # Map PV threads that match a public offer vs PV-only
    pv_by_offer_id = {}
    pv_only_list = []
    for t in pv_threads:
        msgs_text = "\n\n".join(
            f"[Wiadomość PV od wykonawcy]:\n{m.get('text', '').strip()}"
            for m in t.get("messages", [])
            if m.get("text")
        )
        if not msgs_text.strip():
            continue
        if t.get("has_submitted_offer") and t.get("matched_offer_id"):
            pv_by_offer_id[str(t["matched_offer_id"])] = msgs_text
        else:
            pv_only_list.append({
                "real_author": f"{t.get('author_name', 'Nieznany')} [PV]",
                "channel": "TYLKO WIADOMOŚĆ PRYWATNA (PV) — wykonawca napisał na priv bez składania oferty w formularzu",
                "price": "Brak wyceny w formularzu (ew. kwota w treści wiadomości PV)",
                "days": "Brak w formularzu",
                "contracts": "brak danych (wiadomość PV)",
                "text": msgs_text,
            })

    pool = []
    for off in public_offers:
        oid = str(off.get("offer_id", ""))
        txt = (off.get("proposal_text") or "").strip()
        channel = "OFERTA PUBLICZNA"
        if oid in pv_by_offer_id:
            channel = "OFERTA PUBLICZNA + DODATKOWA WIADOMOŚĆ PRYWATNA (PV)"
            txt = f"{txt}\n\n---\n{pv_by_offer_id[oid]}"
        pool.append({
            "real_author": off.get("author_name", "Wykonawca"),
            "real_offer_id": oid,
            "channel": channel,
            "price": off.get("price") or "Brak",
            "days": off.get("days") or "Brak",
            "contracts": off.get("author_contracts") or "0 umów",
            "text": txt,
            "is_ours": False,
        })

    # Dodajemy wykonawców PV-only
    for pv_item in pv_only_list:
        pool.append({
            "real_author": pv_item["real_author"],
            "real_offer_id": "PV_ONLY",
            "channel": pv_item["channel"],
            "price": pv_item["price"],
            "days": pv_item["days"],
            "contracts": pv_item["contracts"],
            "text": pv_item["text"],
            "is_ours": False,
        })

    # 1. Jeśli mamy wariant BIZNES (6000 zł z krótkiego opisu), wstawiamy na pozycję #25 (indeks 24, Koszyk 1)
    our_nums = []
    biz = our_offer.get("biznes_variant")
    if biz and biz.get("r1_opis"):
        biz_entry = {
            "real_author": "NASZA_OFERTOWARKA_WARIANT_BIZNES (6000 zł, prosty język)",
            "real_offer_id": "OUR_BOT_BIZNES",
            "channel": "OFERTA PUBLICZNA",
            "price": f"{biz.get('wycena', 6000)},00 PLN",
            "days": f"{biz.get('dni', 13)} dni pracy",
            "contracts": "5 umów",
            "text": strip_identifying_signature(biz["r1_opis"]),
            "is_ours": True,
        }
        pool.insert(24, biz_entry)
        our_nums.append(25)

    # 2. Nasza główna oferta (pełny opis ogłoszenia) wstawiana na pozycję #58 (indeks 57, Koszyk 2)
    our_anon_text = strip_identifying_signature(our_offer["final_opis"])
    our_entry = {
        "real_author": f"NASZA_OFERTOWARKA_GLOWNA ({our_offer['wycena']} zł, pełny opis)",
        "real_offer_id": "OUR_BOT_MAIN",
        "channel": "OFERTA PUBLICZNA",
        "price": f"{our_offer['wycena']},00 PLN",
        "days": f"{our_offer['dni']} dni pracy",
        "contracts": "5 umów",
        "text": our_anon_text,
        "is_ours": True,
    }
    pool.insert(57, our_entry)
    our_nums.append(58)

    # Nadajemy anonimowe identyfikatory KANDYDAT #1 .. KANDYDAT #N
    for i, item in enumerate(pool, start=1):
        item["anon_id"] = f"KANDYDAT #{i}"

    return pool, our_nums


def format_candidates_block(candidates: list[dict]) -> str:
    blocks = []
    for c in candidates:
        blocks.append(
            f"==================================================\n"
            f"### {c['anon_id']}\n"
            f"**Kanał kontaktu:** {c['channel']}\n"
            f"**Cena w formularzu:** {c['price']} | **Termin:** {c['days']} | **Umowy na Useme:** {c['contracts']}\n\n"
            f"**Treść wiadomości / oferty:**\n{c['text']}\n"
        )
    return "\n".join(blocks)


CLIENT_SYSTEM_PROMPT = """Jesteś właścicielem firmy handlowo-produkcyjnej w Polsce (nie jesteś programistą ani osobą techniczną).
Wystawiłeś na Useme zlecenie „Automatyzacja obiegu faktur i dokumentów kosztowych”.
W głowie masz realny budżet rzędu 5 000 – 15 000 zł netto za całość wdrożenia.
Nie znasz się na kodowaniu, ale masz zdrowy rozsądek biznesowy, znasz realia swojej firmy (faktury kosztowe, WZ, zamówienia, skany z biura, zdjęcia z telefonów od ludzi w terenie, PDF-y z maila, program Comarch Optima) i bardzo uważnie czytasz, co piszą do Ciebie wykonawcy — zarówno ci, którzy złożyli ofertę w formularzu, jak i ci, którzy napisali do Ciebie wiadomość prywatną (PV).

Czego szukasz jako nietechniczny przedsiębiorca:
1. Kogoś, kto przeczytał Twoje ogłoszenie ze zrozumieniem i mówi o TWOIM procesie i TWOJEJ Optimie, a nie wkleja ogólnikowy bełkot z ChatGPT albo reklamę swojej agencji.
2. Kogoś, kto pisze normalnym, zrozumiałym językiem (jeśli ktoś zarzuca Cię niezrozumiałym żargonem bez wyjaśnienia po co to jest, albo odwrotnie — pisze ogólnikowe lanie wody bez konkretu jak połączy się z Optimą, to traci punkty).
3. Uczciwego podejścia do kosztów, bezpieczeństwa bazy Comarch Optima (żeby nikt nie rozwalił Ci księgowości na żywej bazie!) i realnej weryfikacji matematycznej faktur.
4. Konkretu zamiast naganiania na „szybki telefon / Google Meet zanim cokolwiek powiem”.

WAŻNE: Wszystkie oferty są zanonimizowane jako KANDYDAT #1 .. KANDYDAT #N. Oceniasz wyłącznie to, co widzisz w treści, cenie, kanale kontaktu (Oferta vs PV) i podejściu do Twojego problemu."""


def run_blind_tournament(pool: list[dict], our_num: int) -> dict:
    print("=" * 80)
    print(f"KROK 2: START ŚLEPEGO TURNIEJU ({len(pool)} KANDYDATÓW: 85 OFERT + 13 PV + 1 NASZA JAKO KANDYDAT #{our_num})")
    print("=" * 80)

    # Podział na 3 koszyki po 33 kandydatów
    batch1 = pool[0:33]
    batch2 = pool[33:66]  # Zawiera KANDYDAT #48 (nasza oferta)
    batch3 = pool[66:]    # Zawiera resztę ofert publicznych oraz wiadomości PV!

    batches = [
        ("KOSZYK 1 (Kandydaci #1 – #33)", batch1),
        ("KOSZYK 2 (Kandydaci #34 – #66)", batch2),
        ("KOSZYK 3 (Kandydaci #67 – #99, w tym wiadomości z PV)", batch3),
    ]

    stage1_reports = []
    shortlist_ids = []

    for b_name, b_items in batches:
        print(f"\n>>> Etap 1: Oceniam {b_name} ({len(b_items)} kandydatów)...")
        prompt = f"""## TWOJE OGŁOSZENIE NA USEME:
Tytuł: {REAL_JOB_TITLE}
{REAL_JOB_DESC}

---
Poniżej znajduje się {len(b_items)} propozycji od wykonawców z puli ({b_name}). Część złożyła ofertę publiczną, a część napisała bezpośrednio na czacie prywatnym (PV).

Twoje zadanie jako zleceniodawcy (właściciela firmy):
1. Przejrzyj wszystkie propozycje z tego koszyka.
2. Wskaż, które oferty od razu odrzucasz i dlaczego (wypisz krótko główne grupy odrzuconych).
3. Wybierz **DOKŁADNIE 6 NAJLEPSZYCH KANDYDATÓW** z tego koszyka, którzy przechodzą do półfinału.
4. Dla każdego z 6 wybranych podaj:
   - Numer (`KANDYDAT #X`),
   - Dlaczego przykuł Twoją uwagę jako nietechnicznego właściciela firmy,
   - Jakie widzisz u niego plusy, a jakie minusy / wątpliwości.
5. Na samym końcu wypisz wybraną szóstkę w formacie JSON:
```json
{{"top6": ["KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #...", "KANDYDAT #..."]}}
```

OTO KANDYDACI:
{format_candidates_block(b_items)}
"""
        resp = call_llm(CLIENT_SYSTEM_PROMPT, prompt, temperature=0.2)
        stage1_reports.append((b_name, resp))
        # Wyciągnij numery KANDYDAT #X z bloku JSON lub tekstu
        m_json = re.search(r'\{\s*"top6"\s*:\s*\[(.*?)\]\s*\}', resp, re.DOTALL)
        extracted = []
        if m_json:
            extracted = re.findall(r"KANDYDAT\s*#\d+", m_json.group(1))
        if not extracted:
            extracted = list(dict.fromkeys(re.findall(r"KANDYDAT\s*#\d+", resp)))[:6]
        print(f"    Wyłonieni z {b_name}: {extracted}")
        for cid in extracted:
            norm_cid = re.sub(r"\s+", " ", cid.strip().upper())
            if norm_cid not in shortlist_ids:
                shortlist_ids.append(norm_cid)

    # Pobierz obiekty kandydatów z półfinału
    pool_by_id = {c["anon_id"]: c for c in pool}
    semifinalists = [pool_by_id[cid] for cid in shortlist_ids if cid in pool_by_id]

    print(f"\n>>> Etap 2 i 3 (PÓŁFINAŁ I WIELKI FINAŁ): {len(semifinalists)} najlepszych kandydatów (oferty + PV)")
    print("    Lista półfinalistów:")
    for sf in semifinalists:
        print(f"      - {sf['anon_id']} -> {sf['real_author']} ({sf['channel']} | {sf['price']})")

    final_prompt = f"""## TWOJE OGŁOSZENIE NA USEME:
Tytuł: {REAL_JOB_TITLE}
{REAL_JOB_DESC}

---
W pierwszym etapie przesiewu z 99 zgłoszeń (ofert publicznych i wiadomości prywatnych PV) wybrałeś do półfinału **{len(semifinalists)} najlepszych wykonawców**.
Poniżej masz ich pełne, dokładne wiadomości i oferty.

Twoje zadanie jako właściciela firmy (nietechnicznego przedsiębiorcy, budżet w głowie 5 000 – 15 000 zł netto, który sam będzie z nimi rozmawiał na czacie prywatnym):

1. **Szczegółowa, uczciwa ocena KAŻDEGO z {len(semifinalists)} półfinalistów po kolei** (w skali 1–100 pkt oczami prawdziwego klienta):
   - Co Ci się w tej wiadomości/ofercie podoba?
   - Co brzmi sztucznie, zbyt technicznie, podejrzanie albo czego w niej brakuje?
   - Czy po przeczytaniu tej wiadomości masz ochotę odpisać temu człowiekowi na czacie?

2. **Porównanie: Oferty Publiczne vs Wiadomości Prywatne (PV)**:
   - Kto zrobił na Tobie lepsze wrażenie: wykonawcy ze sztywnymi ofertami publicznymi, czy ci, którzy napisali bezpośrednio na priv (PV)? Dlaczego?

3. **ŚCISŁY RANKING TOP 10 (Od 1. miejsca — Zwycięzcy — do 10. miejsca)**:
   - Ułóż bezwzględne podium i Top 10.
   - Dla każdego z Top 10 napisz dokładnie, dlaczego wygrał z tymi, którzy są niżej, i co zadecydowało o kolejności.
   - Napisz wprost: **Komu odpisujesz jako pierwszemu i kogo zatrudniasz?**

OTO {len(semifinalists)} PÓŁFINALISTÓW (PEŁNE TREŚCI):
{format_candidates_block(semifinalists)}
"""
    final_verdict = call_llm(CLIENT_SYSTEM_PROMPT, final_prompt, temperature=0.2)

    return {
        "our_candidate_id": f"KANDYDAT #{our_num}",
        "total_candidates": len(pool),
        "shortlist_ids": shortlist_ids,
        "semifinalists_map": [
            {
                "anon_id": sf["anon_id"],
                "real_author": sf["real_author"],
                "channel": sf["channel"],
                "price": sf["price"],
                "days": sf["days"],
                "is_ours": sf["is_ours"],
            }
            for sf in semifinalists
        ],
        "stage1_reports": stage1_reports,
        "final_verdict": final_verdict,
    }


def main():
    our_offer = step1_generate_our_offer()
    pool, our_num = build_blind_pool(our_offer)
    tournament = run_blind_tournament(pool, our_num)

    # Zapisz pełny raport Markdown i JSON
    json_path = OUT_DIR / "wyniki_slepego_testu_144890_99_kandydatow.json"
    md_path = OUT_DIR / "RAPORT_SLEPY_TEST_144890_Z_PV.md"

    full_data = {
        "our_offer": our_offer,
        "tournament": tournament,
    }
    json_path.write_text(json.dumps(full_data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# ŚLEPY TEST 99 KANDYDATÓW (85 OFERT + 13 PV + 1 NASZA) — ZLECENIE #144890\n",
        f"- **Data badania:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Nasza oferta ukryta jako:** `KANDYDAT #{our_num}` (Wycena: **{our_offer['wycena']} zł netto**, Czas: **{our_offer['dni']} dni**)",
        f"- **Ocena wewnętrznego Audytora 100 dla naszej oferty:** R1 = `{our_offer['r1_score']}/100` -> Final = `{our_offer['final_score']}/100`\n",
        "## 1. Nasza wygenerowana oferta (ukryta w teście jako `KANDYDAT #" + str(our_num) + "`)\n",
        "```text\n" + our_offer["final_opis"] + "\n```\n",
        "## 2. Kto przeszedł do Półfinału (Top 18 z 99 kandydatów — rozszyfrowana mapa)\n",
        "| ID w teście | Prawdziwy autor | Kanał | Cena | Czas |",
        "|---|---|---|---|---|",
    ]
    for sf in tournament["semifinalists_map"]:
        bold = "**" if sf["is_ours"] else ""
        md_lines.append(
            f"| {bold}{sf['anon_id']}{bold} | {bold}{sf['real_author']}{bold} | {sf['channel']} | {sf['price']} | {sf['days']} |"
        )

    md_lines.append("\n---\n## 3. Werdykt Finałowy Zleceniodawcy (w 100% ślepy test)\n")
    md_lines.append(tournament["final_verdict"])

    md_lines.append("\n---\n## 4. Logi z Etapu 1 (3 Koszyki Eliminacyjne po 33 kandydatów)\n")
    for b_name, b_rep in tournament["stage1_reports"]:
        md_lines.append(f"### {b_name}\n\n{b_rep}\n\n---\n")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\n[GOTOWE] Zapisano raport do: {md_path}")


if __name__ == "__main__":
    main()
