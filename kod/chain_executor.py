# -*- coding: utf-8 -*-
"""Executor łańcucha AI (system slotów) – plug-and-play.

Odczytuje chain_config.json i odtwarza konfigurację slotów. Dla jednego
zlecenia odpala sloty sekwencyjnie: output generatora trafia do kontekstu
pod `output_key`, walidatory sprawdzają PASS/FAIL i mogą cofnąć łańcuch.

Strukturę kroków (Chain/Krok) dostarcza runner.

Użycie:

    from chain_executor import run_chain

    wynik = run_chain("useme-oferty-1", zlecenie_dane)
    # wynik == {"opis": "...", "wycena_dni": "..."} lub None przy aborcie
"""

from __future__ import annotations

import json
import random
import re
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

import requests

from runner import Chain
from storage import clear_checkpoint, load_checkpoint, save_checkpoint

try:
    from wycena_kalkulator import policz_wycene, formatuj_wynik
except Exception:  # kalkulator opcjonalny – nie wywalaj lancucha
    policz_wycene = None
    formatuj_wynik = None

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
CONFIG_PATH = PROMPTS_DIR / "chain_config.json"

# Czyste proxy passthrough (zero wstrzykiwania promptu kodowania)
DEEPSEEK_API_URL = "http://127.0.0.1:4571/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-v4-pro"
RESEARCH_MODEL = "deepseek-v4-pro-search"
PROXY_RETRY_MAX = 3
PROXY_BACKOFF_BASE = 2.0

# Twardy limit czasu jednego wywolania slotu. Bez tego proxy trzymajace
# otwarte polaczenie bez danych zawieszalo slot na domyslne 300s+.
SLOT_TIMEOUT = 120
# Globalny zegar śmierci na przetwarzanie pojedynczej oferty (15 minut max)
MAX_CHAIN_WALL_CLOCK_S = 900

_RESEARCH_QUERY_RE = re.compile(
    r"\[RESEARCH_QUERY\](.*?)(?:\[/RESEARCH_QUERY\]|$)", re.DOTALL | re.IGNORECASE
)


def _extract_research_query(text: str) -> Optional[str]:
    """Wyciąga pytanie badawcze z bloku [RESEARCH_QUERY]...[/RESEARCH_QUERY].

    Toleruje też niedomknięty blok (model często ucina zamykający tag przy
    streamingu) — wtedy bierzemy treść do końca tekstu.
    """
    m = _RESEARCH_QUERY_RE.search(text or "")
    if not m:
        return None
    q = m.group(1).strip()
    return q or None


# Mapowanie linii POPRAW_* z walidatora na id slotu-generatora, który ma je poprawić.
_FEEDBACK_TARGETS = {
    "POPRAW_WYCENA": "02b",
    "POPRAW_OFERTA": "02a",
}
_FEEDBACK_RE = re.compile(r"^\s*(POPRAW_[A-Z_]+)\s*:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)


def _extract_feedback(text: str) -> Dict[str, str]:
    """Wyciąga z odpowiedzi walidatora linie POPRAW_<KEY>: <wskazówka>.

    Zwraca dict {POPRAW_KEY: "wskazowka1\\nwskazowka2\\n..."}. Zbiera WSZYSTKIE
    wystąpienia danego klucza (walidator często zwraca kilka poprawek tego samego
    typu) i łączy je w jedną instrukcję. Pusty, gdy brak poprawek.
    """
    out: Dict[str, list[str]] = {}
    for m in _FEEDBACK_RE.finditer(text or ""):
        key = m.group(1).upper()
        val = m.group(2).strip()
        if val:
            out.setdefault(key, []).append(val)
    return {k: "\n".join(v) for k, v in out.items()}


# --- Anty-wyciek: wykrywanie i wycinanie chain-of-thought z outputu slotu 02a ---
# Model pisarza oferty czasem zwraca cały swój tok rozumowania (planowanie,
# iteracyjne przepisywanie, sprawdzanie zakazów) i dopiero na końcu dokleja
# właściwą ofertę. Poniżej: (1) detektor markerów rozumowania, (2) wycinarka,
# która obcina wszystko przed pierwszym powitaniem oferty.
_REASONING_MARKERS_RE = re.compile(
    r"(?mi)(?:"
    r"^\s*(?:hmm|może|sprawd[źz]my|my[śs]l[ęe]|ok[,.]?|okej|zr[óo]bmy|poprawmy|"
    r"wersja robocza|ostateczna wersja|finalna wersja|final|zaczynamy|zacznijmy pisać|"
    r"piszemy proz[ąa]|struktura:|d[łl]ugo[śs][ćc]:|otwarcie:|zako[ńn]czenie:)\b"
    r"|to jest (?:dobre|lepsze|ok)\b"
    r"|^\s*(?:ale|no|wi[ęe]c)\s"
    r"|\bB[1-9]\b\s*(?:m[óo]wi|zakazuje|zabrania)"
    r"|sprawd[źz]my zakazy"
    r"|nie u[żz]ywamy my[śs]lnik[óo]w"
    r"|hmm\b"
    r")"
)
_GREETING_RE = re.compile(
    r"(?m)^[ \t]*(?:dzie[ńn] dobry|dzie[ńn] dobry,|cze[śs][ćc]|witam|"
    r"dobry wiecz[óo]r|dobry dzie[ńn]|hej|hello)\b",
    re.IGNORECASE,
)


def _policz_markery_reasoningu(text: str) -> int:
    """Liczy wystąpienia markerów rozumowania w surowym outputcie modelu."""
    return len(_REASONING_MARKERS_RE.findall(text or ""))


_SIGNATURE_RE = re.compile(r"(?m)^[ \t]*Ksawier[ \t]*$")


def _wytnij_czysta_oferte(text: str) -> str:
    """Obcina reasoning wokół właściwej oferty.

    Model z wyciekiem często iteruje: reasoning, szkic oferty, znowu reasoning,
    finalna oferta. Czystą wersję wyznaczają dwa punkty: OSTATNIE powitanie
    (start oferty) i podpis „Ksawier” (koniec oferty). Wycinamy wszystko przed
    powitaniem oraz wszystko po podpisie. Gdy brak powitania lub podpisu —
    zwracamy tekst bez zmian, a guard zdecyduje o ponowieniu generacji.
    """
    if not text:
        return text
    if _policz_markery_reasoningu(text) == 0:
        return text

    start = 0
    powitania = list(_GREETING_RE.finditer(text))
    if powitania:
        start = powitania[-1].start()

    # Koniec: podpis „Ksawier” występujący po wyznaczonym starcie.
    koniec = len(text)
    podpisy = [m for m in _SIGNATURE_RE.finditer(text) if m.start() > start]
    if podpisy:
        koniec = podpisy[-1].end()

    if start > 0 or koniec < len(text):
        return text[start:koniec].strip()
    return text


_WYCENA_JSON_RE = re.compile(
    r"\[WYCENA_JSON\](.*?)(?:\[/WYCENA_JSON\]|$)", re.DOTALL | re.IGNORECASE
)


def _extract_wycena_json(text: str) -> Optional[Dict[str, Any]]:
    """Wyciąga strukturę JSON z bloku [WYCENA_JSON]...."""
    m = _WYCENA_JSON_RE.search(text or "")
    if not m:
        return None
    raw = m.group(1).strip()
    # usuń ewentualne ogrodzenia markdown
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        mm = re.search(r"\{.*\}", raw, re.DOTALL)
        if mm:
            try:
                return json.loads(mm.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _do_research(query: str) -> str:
    """Odpala jeden krok researchu sieciowego przez proxy i zwraca fakty lub fallback."""
    system_prompt = (
        "Jesteś agentem researchu z dostępem do internetu. Odpowiedz na pytanie "
        "zwięźle po polsku. Podawaj wyłącznie fakty poparte źródłami (URL/cytat). "
        "Czego nie potwierdzisz, oznacz jako niepotwierdzone. Nigdy nie zmyślaj."
    )
    out = call_deepseek(
        system_prompt,
        "Sprawdź w sieci i odpowiedz: " + query,
        model=RESEARCH_MODEL,
        timeout=120,
        max_tokens=2000,
    )
    if not out or len(out.strip()) < 20:
        return "BRAK_ISTOTNYCH_FAKTOW"
    return out


def parse_ai_json_response(content: str) -> Any:
    """Czyści odpowiedź AI i wyodrębnia JSON (zapas dla surowych odpowiedzi)."""
    content = re.sub(r'<!-- PROXY_SID:.*?-->', '', content, flags=re.DOTALL).strip()
    if content.startswith("```"):
        lines = content.split("\n")
        start = 1 if lines[0].startswith("```") else 0
        end = -1 if lines[-1].startswith("```") else len(lines)
        content = "\n".join(lines[start:end]).strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return {"raw_response": content}


def call_deepseek(system_prompt: str, user_prompt: str, max_tokens: int = 3000,
                  temperature: float = 0.7, timeout: int = 300,
                  model: str = DEEPSEEK_MODEL,
                  on_chunk: Optional[Callable[[str], None]] = None,
                  max_continues: int = 3) -> Optional[str]:
    """Wywołuje DeepSeek (localhost:4571 - czysty passthrough) z twardym watchdoggem.

    Prompt rozdzielony na rolę system (instrukcja) i user (dane/kontekst).
    Odpowiedź odczytywana strumieniowo (SSE). Każdy fragment trafia do
    on_chunk (jeśli podany). Zwraca pełny tekst lub None przy timeout.

    Auto-continue: gdy stream urwie się w połowie (proxy wstawia w treść
    „Stream został przerwany..." lub odpowiedź kończy się bez [DONE]), wysyłamy
    „kontynuuj" z dotychczasowym tekstem jako kontekstem i doklejamy wynik.
    """
    _CUT_MARKERS = ("Stream został przerwany", "Stream zostal przerwany")

    def _one_round(messages: list) -> Optional[str]:
        def _post() -> Optional[str]:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }
            last_err: Optional[Exception] = None
            session = requests.Session()
            try:
                # Retry z backoffem: szybkie bledy proxy (502/503/504) ORAZ pusty
                # strumien (proxy potrafi zwrocic 200 bez zadnego tokenu). Timeoutow
                # nie ponawiamy dlugo - one i tak zajmuja caly budzet czasu.
                for attempt in range(PROXY_RETRY_MAX):
                    try:
                        resp = session.post(DEEPSEEK_API_URL, json=payload, headers=headers,
                                             timeout=(10, timeout), stream=True)
                        if resp.status_code == 429:
                            retry_after = 15.0
                            try:
                                retry_after = float(resp.headers.get("Retry-After", 15.0))
                            except Exception:
                                pass
                            last_err = RuntimeError(f"proxy 429 rate limit (wait {retry_after}s)")
                            print(f"[RETRY] Proxy zwrocilo 429 (Rate Limit). Czekam {retry_after}s przed proba {attempt+2}/{PROXY_RETRY_MAX}...", flush=True)
                            if attempt < PROXY_RETRY_MAX - 1:
                                time.sleep(retry_after)
                                continue
                            return None
                        if resp.status_code in (502, 503, 504):
                            last_err = RuntimeError(f"proxy {resp.status_code}")
                            wait_s = 4.0 * (attempt + 1)
                            if attempt < PROXY_RETRY_MAX - 1:
                                time.sleep(wait_s)
                                continue
                            return None
                        if resp.status_code != 200:
                            last_err = RuntimeError(f"http {resp.status_code}")
                            return None
                        full = ""
                        for line in resp.iter_lines(decode_unicode=True):
                            if not line:
                                continue
                            line = line.strip()
                            if not line.startswith("data:"):
                                continue
                            data_str = line[5:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data_str)
                                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if delta:
                                    full += delta
                                    if on_chunk:
                                        on_chunk(delta)
                            except json.JSONDecodeError:
                                pass
                        # Pusty strumien (200 ale zero tokenow) -> traktuj jak blad proxy
                        # i ponow z backoffem. To nas bolalo w testach.
                        if not full.strip():
                            last_err = RuntimeError("pusty strumien")
                            wait_s = 4.0 * (attempt + 1)
                            if attempt < PROXY_RETRY_MAX - 1:
                                time.sleep(wait_s)
                                continue
                            return None
                        return full
                    except requests.exceptions.RequestException as e:
                        # Blad sieci/timeout – nie ponawiamy dlugo, oddajemy fallback.
                        last_err = e
                        return None
            finally:
                session.close()

            if last_err:
                return None
            return ""

        box: Dict[str, Optional[str]] = {}
        def _run() -> None:
            try:
                box["result"] = _post()
            except Exception as e:  # nic nie moze uciec z watku
                box["result"] = None
                box["error"] = str(e)
                print(f"[ERROR] call_deepseek _post exception: {e}", flush=True)
        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout + 15)
        if t.is_alive():
            print(f"[WATCHDOG] call_deepseek: watek przekroczyl limit {timeout + 15}s – przerywam oczekiwanie", flush=True)
            return None
        return box.get("result")

    messages: list = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    full = _one_round(messages)
    if full is None:
        return None

    # Auto-continue, jeśli stream urwany albo odpowiedź nie domknęła się.
    for _ in range(max_continues):
        cut = any(m in full for m in _CUT_MARKERS)
        if not cut:
            break
        # usuń marker przerwania z treści, zachowując resztę jako kontekst
        for m in _CUT_MARKERS:
            idx = full.find(m)
            if idx != -1:
                full = full[:idx]
        messages.append({"role": "assistant", "content": full})
        messages.append({"role": "user", "content": "kontynuuj"})
        cont = _one_round(messages)
        if not cont or not cont.strip():
            break
        # kontynuacja też może nieść marker – zostanie złapany w kolejnej iteracji
        for m in _CUT_MARKERS:
            idx = cont.find(m)
            if idx != -1:
                cont = cont[:idx]
        full += cont

    return full


def _read_text(path: Path) -> str:
    # utf-8-sig toleruje (i usuwa) ewentualny BOM na początku pliku.
    return path.read_text(encoding="utf-8-sig")


def _slim_zlecenie(zlecenie: Dict[str, Any]) -> Dict[str, Any]:
    """Usuwa z danych zlecenia ciezkie smieci, ktorych pipeline nie potrzebuje.

    Lista konkurentow (po 60+ tagow + avatary) potrafi miec 30k znakow i rozdyma
    prompt do 85k+, przez co kazdy call AI jest wolny. Agentom wystarcza sama
    LICZBA ofert (competitors_count), nie lista kto zlozyl oferte.
    """
    if not isinstance(zlecenie, dict):
        return zlecenie
    slim = {k: v for k, v in zlecenie.items() if k not in ("competitors", "job_tags", "ai_proposal", "submission_result", "oferty")}
    # zachowaj liczbe ofert, jesli nie ma jej wprost
    if "competitors_count" not in slim and "competitors" in zlecenie:
        try:
            slim["competitors_count"] = len(zlecenie["competitors"] or [])
        except Exception:
            pass
    return slim


def _load_config() -> Dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))


TECH_CARDS_DIR = BASE_DIR.parent / "badania" / "analizy" / "technologie" / "baza_wiedzy"

SCENARIO_MAP: Dict[str, str] = {
    "msp_erp": "klient_01_tradycyjne_msp_erp_przemysl.md",
    "ecommerce": "klient_02_ecommerce_merchant.md",
    "agencja": "klient_03_agencja_software_house.md",
    "ekspert_dziedzinowy": "klient_04_ekspert_dziedzinowy_uslugi.md",
    "tech_agnostic": "klient_05_tech_agnostic_biznes.md",
    "quick_fix": "klient_06_quick_fix_awaria_hobbysta.md",
}

MODIFIER_MAP: Dict[str, str] = {
    "RESCUE": "modyfikator_rescue_klient_sparzony.md",
    "DELEGOWANY": "modyfikator_delegowany_pracownik.md",
    "PHANTOM": "modyfikator_phantom_startup_wizjoner.md",
}

TECH_CARD_MAP: Dict[str, str] = {
    "tech_01": "tech_01_scraping_i_boty.md",
    "tech_02": "tech_02_comarch_optima_ksef.md",
    "tech_03": "tech_03_subiekt_sfera_ecommerce.md",
    "tech_04": "tech_04_python_fastapi_automatyzacje.md",
    "tech_05": "tech_05_kotlin_android_native.md",
    "tech_06": "tech_06_flutter_dart.md",
    "tech_07": "tech_07_swift_ios_native.md",
    "tech_08": "tech_08_devops_docker_linux.md",
    "tech_09": "tech_09_sql_optymalizacja_migracje.md",
    "tech_10": "tech_10_nodejs_nestjs_backend.md",
    "tech_11": "tech_11_csharp_dotnet_b2b.md",
    "tech_12": "tech_12_voip_asterisk_sip.md",
    "tech_13": "tech_13_enova365_odoo_erp.md",
    "tech_14": "tech_14_google_sheets_appscript.md",
    "tech_15": "tech_15_ai_llm_rag_pipelines.md",
    "tech_16": "tech_16_tech_agnostic_biznes.md",
}

_TECH_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "tech_01": ("scraping", "scraper", "crawler", "cloudflare", "datadome", "akamai", "playwright", "selenium", "puppeteer", "scrapy", "pobieranie danych ze stron", "monitoring cen"),
    "tech_02": ("optima", "comarch", "ksef", "cdn xl", "cdn optima", "fa(2)", "fa(3)", "praca rozproszona", "biuro rachunkowe", "biała lista", "biala lista"),
    "tech_03": ("subiekt", "sfera", "nexo", "insert", "baselinker", "allegro", "idosell", "prestashop", "shoper", "woocommerce", "shopify", "sklep internetowy", "e-commerce"),
    "tech_04": ("fastapi", "celery", "n8n", "make.com", "zapier", "webhook", "mikroserwis", "rest api", "python"),
    "tech_05": ("kotlin", "android", "zebra", "datawedge", "honeywell", "kolektor danych", "skaner kodów", "bluetooth ble", "google play"),
    "tech_06": ("flutter", "dart", "wieloplatformow", "cross-platform", "ios i android", "android i ios", "aplikacja mobilna", "aplikacji mobilnej"),
    "tech_07": ("swift", "swiftui", "storekit", "app store", "xcode", "natywna ios"),
    "tech_08": ("docker", "linux", "ubuntu", "debian", "nginx", "traefik", "vps", "devops", "ci/cd", "wireguard"),
    "tech_09": ("postgresql", "postgres", "mysql", "mariadb", "mssql", "sql server", "optymalizacja bazy", "migracja bazy", "zapytania sql"),
    "tech_10": ("node.js", "nodejs", "nestjs", "typescript", "fastify", "websocket", "socket.io", "next.js"),
    "tech_11": ("c#", ".net", "dotnet", "asp.net", "entity framework", "ef core", "masstransit", "wpf", "blazor"),
    "tech_12": ("voip", "asterisk", "freepbx", "pjsip", "sip trunk", "webrtc", "centrala telefoniczna", "call center"),
    "tech_13": ("enova", "enova365", "soneta", "odoo"),
    "tech_14": ("google sheets", "apps script", "arkusze google", "google workspace", "vba", "makro excel"),
    "tech_15": ("llm", "rag", "openai", "claude", "deepseek", "ocr", "qdrant", "pgvector", "embedding", "wektor", "agent ai", "sztuczn"),
}


def _resolve_tech_cards(zlecenie: Dict[str, Any], slot_id: str) -> list[str]:
    """Dobiera 1–2 karty wiedzy technologicznej (`tech_01`..`tech_16`) do zlecenia.

    - Dla `sciezka == 'biznes'` lub `typ_klienta == 'tech_agnostic'` w slocie `02a`
      zwraca wyłącznie `['tech_16']`, aby nie skazić oferty żargonem IT.
    - Dla ścieżki inżynierskiej łączy jawne `karta_tech` z AI #1 oraz dopasowanie
      słów kluczowych w tytule i opisie zlecenia (maksymalnie 2 karty).
    """
    sciezka = str(zlecenie.get("sciezka") or "").strip().lower()
    typ_klienta = str(zlecenie.get("typ_klienta") or "").strip().lower()
    if (sciezka == "biznes" or typ_klienta == "tech_agnostic") and slot_id == "02a":
        return ["tech_16"]

    selected: list[str] = []
    explicit = zlecenie.get("karta_tech")
    if isinstance(explicit, str) and explicit.strip().lower() in TECH_CARD_MAP:
        k = explicit.strip().lower()
        if k != "tech_16" or sciezka == "biznes":
            selected.append(k)
    elif isinstance(explicit, list):
        for item in explicit:
            k = str(item).strip().lower()
            if k in TECH_CARD_MAP and k not in selected:
                selected.append(k)

    fields = zlecenie.get("fields") or {}
    text_blob = " ".join([
        str(zlecenie.get("title") or ""),
        str(fields.get("title") or ""),
        str(zlecenie.get("full_description") or ""),
        str(zlecenie.get("description") or ""),
        str(fields.get("description") or ""),
    ]).lower()

    scores: list[tuple[int, str]] = []
    for card_key, kw_list in _TECH_KEYWORDS.items():
        hits = sum(2 if kw in text_blob else 0 for kw in kw_list)
        if hits > 0:
            scores.append((hits, card_key))
    scores.sort(key=lambda x: (-x[0], x[1]))

    for _, card_key in scores:
        if card_key not in selected:
            selected.append(card_key)
        if len(selected) >= 2:
            break

    if not selected and (sciezka == "biznes" or typ_klienta == "tech_agnostic"):
        selected.append("tech_16")
    return selected[:2]


def _format_tech_card_for_slot(card_key: str, slot_id: str) -> str:
    """Wyciąga i oczyszcza perełki merytoryczne z karty `tech_XX` dla slotu `02a` lub `02b`.

    - Dla `02a`: wycina Sekcję 1 (statystyki rynkowe) oraz Sekcję 6 (tabele wycen wielowariantowych
      i diagramy ASCII, które mogłyby zmylić generator oferty), zamienia wiersze tabel Markdown
      na czysty tekst bez pionowych kresek `|` i usuwa gwiazdki `**`, aby model nie kopiował
      formatowania Markdown do oferty.
    - Dla `02b`: wyciąga Sekcję 3 (ukryte miny) oraz Sekcję 6 (architektura modułowa) z wyciętymi
      kwotami PLN, wspierając realistyczny podział na moduły i godziny.
    """
    filename = TECH_CARD_MAP.get(card_key)
    if not filename:
        return ""
    card_path = TECH_CARDS_DIR / filename
    if not card_path.exists():
        return ""

    raw = _read_text(card_path)
    lines = raw.splitlines()
    kept_lines: list[str] = []
    current_sec = 0
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        m_sec = re.match(r"^#{1,3}\s+(\d+)\.", stripped)
        if m_sec:
            current_sec = int(m_sec.group(1))
        elif re.match(r"^##\s+(PODSUMOWANIE|ZAŁĄCZNIK)", stripped, re.IGNORECASE):
            current_sec = 8

        if slot_id == "02a":
            # Pomijamy sekcję 1 (metadane rynkowe), sekcję 6 (tabele wycen/modułów) i sekcję 8 (podsumowania/załączniki)
            if current_sec in (1, 6, 8):
                continue
        elif slot_id == "02b":
            # Dla kalkulatora godzin (02b) zostawiamy wyłącznie sekcję 3 (miny) i 6 (moduły)
            if current_sec not in (0, 3, 6):
                continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            # Pomijamy diagramy ASCII w blokach kodu
            if any(ch in stripped for ch in ("┌", "│", "└", "▼", "─", "──", "↓")):
                continue

        # Konwersja wierszy tabel Markdown | A | B | -> czysty tekst bez tabel i bez myślników
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^[-:]+$", c or "-") for c in cells):
                continue
            row_txt = ", ".join(c for c in cells if c)
            if slot_id == "02b":
                row_txt = re.sub(r"\b\d[\d\s–-]*zł\b", "", row_txt, flags=re.IGNORECASE)
            row_clean = row_txt.replace("**", "").replace(" — ", ", ").replace(" – ", ", ").replace(" - ", ", ").replace("—", ", ").replace("–", ", ")
            if slot_id == "02a":
                row_clean = re.sub(r"\s*\(([^()]*)\)", r", \1", row_clean)
            kept_lines.append(row_clean)
            continue

        clean_line = line.replace("**", "")
        if slot_id == "02a":
            clean_line = clean_line.replace(" — ", ", ").replace(" – ", ", ").replace(" - ", ", ").replace("—", ", ").replace("–", ", ")
            clean_line = re.sub(r"^\s*[-*•]\s+", "", clean_line)
            while "(" in clean_line and ")" in clean_line:
                clean_line = re.sub(r"\s*\(([^()]*)\)", r", \1", clean_line)
            clean_line = clean_line.replace("(", "").replace(")", "")
            clean_line = re.sub(r",\s*,", ",", clean_line)
        elif slot_id == "02b":
            clean_line = re.sub(r"\(\s*WYCENA[^)]*\)", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"\b\d[\d\s–-]*zł\b", "", clean_line, flags=re.IGNORECASE)
        kept_lines.append(clean_line)

    out_text = "\n".join(kept_lines).strip()
    out_text = re.sub(r"\n{3,}", "\n\n", out_text)
    if slot_id == "02a":
        header = (
            f"--- POMOCNICZA BAZA WIEDZY TECHNOLOGICZNEJ: {card_key} ---\n"
            "INSTRUKCJA: Poniższa baza wiedzy to wyłącznie materiał pomocniczy. "
            "Wybierz z niej tylko to, co realnie pasuje do ogłoszenia klienta i jest zgodne z planem Orchestratora. "
            "Jeśli dany mechanizm z karty nie dotyczy problemu klienta, całkowicie go pomiń. "
            "Pamiętaj o całkowitym zakazie używania myślników, pauz oraz nawiasów w treści oferty.\n\n"
        )
        return header + out_text
    return f"--- KARTA WIEDZY TECHNOLOGICZNEJ DLA WYCENY: {card_key} ---\n" + out_text


def _build_prompt(slot: Dict[str, Any], context: Dict[str, Any]) -> tuple[str, str]:
    """Składa prompt dla slotu na role: system (instrukcja) i user (dane + outputy)."""
    system_parts: list[str] = []
    user_parts: list[str] = []

    # Własny prompt slotu -> rola system
    if slot.get("prompt_file"):
        prompt_path = PROMPTS_DIR / slot["prompt_file"]
        if prompt_path.exists():
            system_parts.append(_read_text(prompt_path))

    # Pliki kontekstowe -> rola user
    for cf in slot.get("context_files", []):
        ctx_path = PROMPTS_DIR / cf
        if ctx_path.exists():
            user_parts.append(f"--- {cf} ---\n" + _read_text(ctx_path))

    # Dynamiczne wstrzyknięcie scenariusza klienta, modyfikatorów i Kart Wiedzy Technologicznej (tech_01..16)
    zlecenie = context.get("_zlecenie")
    slot_id = str(slot.get("id", ""))
    if isinstance(zlecenie, dict) and slot_id in ("00", "02a", "02b", "08", "20"):
        sciezka = str(zlecenie.get("sciezka") or "").strip().lower()
        typ_klienta = str(zlecenie.get("typ_klienta") or "").strip().lower()
        tier = str(zlecenie.get("tier") or "").strip().upper()
        modyfikatory = zlecenie.get("modyfikatory") or []
        if not isinstance(modyfikatory, list):
            modyfikatory = []
        tech_cards = _resolve_tech_cards(zlecenie, slot_id)

        if sciezka or typ_klienta or tier or modyfikatory or tech_cards:
            meta_lines = []
            if tier:
                meta_lines.append(f"TIER: {tier}")
            if sciezka:
                meta_lines.append(
                    f"ŚCIEŻKA KOMUNIKACJI (Dual-Track): {sciezka.upper()} "
                    + (
                        "- język efektu biznesowego, zero żargonu IT niewymienionego przez klienta"
                        if sciezka == "biznes"
                        else "- język konkretu technicznego dopasowany do ogłoszenia klienta"
                    )
                )
            if typ_klienta:
                meta_lines.append(f"TYP KLIENTA: {typ_klienta}")
            if tech_cards:
                meta_lines.append(f"POWIĄZANE KARTY WIEDZY: {', '.join(tech_cards)}")
            if modyfikatory:
                meta_lines.append(f"AKTYWNE MODYFIKATORY: {', '.join(str(m) for m in modyfikatory)}")
            user_parts.append("--- KLASYFIKACJA STRATEGICZNA ZLECENIA ---\n" + "\n".join(meta_lines))

        if slot_id in ("00", "02a", "08"):
            scen_dir = PROMPTS_DIR / "kontekst" / "scenariusze"
            if typ_klienta in SCENARIO_MAP:
                scen_path = scen_dir / SCENARIO_MAP[typ_klienta]
                if scen_path.exists():
                    user_parts.append(
                        f"--- SCENARIUSZ KLIENTA ({typ_klienta}) ---\n" + _read_text(scen_path)
                    )
            for mod in modyfikatory:
                mod_key = str(mod).strip().upper()
                if mod_key in MODIFIER_MAP:
                    mod_path = scen_dir / MODIFIER_MAP[mod_key]
                    if mod_path.exists():
                        user_parts.append(
                            f"--- MODYFIKATOR ({mod_key}) ---\n" + _read_text(mod_path)
                        )

        if slot_id == "02a" and tech_cards:
            for tc_key in tech_cards:
                tc_formatted = _format_tech_card_for_slot(tc_key, slot_id)
                if tc_formatted:
                    user_parts.append(tc_formatted)

    # Dane zlecenia (zawsze dostępne) -> rola user
    if zlecenie is not None:
        user_parts.append("--- DANE ZLECENIA ---\n" + json.dumps(zlecenie, ensure_ascii=False, indent=2))

    # Outputy poprzednich slotów -> rola user
    for key in slot.get("requires", []):
        if key in context:
            user_parts.append(f"--- OUTPUT {key} ---\n{context[key]}")

    # Feedback z walidatora (jeśli ten slot jest właśnie poprawiany) -> rola user
    feedback = context.get("_feedback", {})
    slot_feedback = feedback.get(slot.get("id"))
    if slot_feedback:
        user_parts.append(
            "--- OBOWIĄZKOWE POPRAWKI Z WERYFIKACJI ---\n"
            "Poprzednia wersja została odrzucona. Popraw DOKŁADNIE poniższe rzeczy, "
            "nie zmieniając niczego innego, co było poprawne:\n" + slot_feedback
        )

    return "\n\n".join(system_parts), "\n\n".join(user_parts)


def _is_pass(response: str) -> bool:
    """Walidator zwrócił PASS?"""
    if not response:
        return False
    clean = re.sub(r"^```(?:markdown|text)?\s*", "", response.strip(), flags=re.IGNORECASE).strip()
    head = clean.upper()
    return head.startswith("PASS") and not head.startswith("FAIL")


def run_chain(chain_id: str, zlecenie_dane: Dict[str, Any],
              parent_id: str = "useme-bot",
              parent_step: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Odpala łańcuch slotów dla jednego zlecenia z obsługą checkpointów i watchdogów.

    Kroki są opakowywane w Chain/Krok (runner) dla czytelnej struktury i logów.
    Wznawia stan z dysku (.checkpoints/) jeśli poprzedni bieg został przerwany.
    Zwraca context z kluczami outputów lub None przy aborcie.
    """
    config = _load_config()
    retry_max = config.get("retry_max", 3)
    slots = [s for s in config["slots"] if s.get("enabled")]

    # Normalizacja danych wejściowych zlecenia (zarówno z bazy/archiwum jak i live scrapingu)
    _fields = (zlecenie_dane or {}).get("fields")
    if not _fields or not isinstance(_fields, dict):
        full_det = (zlecenie_dane or {}).get("full_details") or {}
        list_det = (zlecenie_dane or {}).get("list_details") or {}
        desc = (
            (zlecenie_dane or {}).get("full_description")
            or full_det.get("full_description")
            or (zlecenie_dane or {}).get("description")
            or (zlecenie_dane or {}).get("short_desc")
            or list_det.get("short_desc")
            or ""
        )
        if desc:
            _fields = {
                "title": (zlecenie_dane or {}).get("title") or full_det.get("title") or list_det.get("title") or "",
                "description": desc,
                "budget": (zlecenie_dane or {}).get("budget") or list_det.get("budget") or "",
                "author": (zlecenie_dane or {}).get("author") or full_det.get("author") or list_det.get("author") or ""
            }
            zlecenie_dane["fields"] = _fields
        else:
            _fields = {}

    # Guard: zlecenie bez danych wejsciowych (brak fields i brak opisu) nie ma z czym pracowac.
    if not _fields or len(json.dumps(_fields, ensure_ascii=False)) < 50:
        print(f"[SKIP] Zlecenie {zlecenie_dane.get('id','?')} bez danych wejściowych "
              f"(puste fields i brak opisu) - pomijam.", flush=True)
        return None

    # Odetnij ciezkie smieci (lista konkurentow), zanim trafia do promptow AI.
    zlecenie_dane = _slim_zlecenie(zlecenie_dane)
    job_id = str(zlecenie_dane.get("id", "tmp")).strip()

    context: Dict[str, Any] = {"_zlecenie": zlecenie_dane}

    # --- ODCZYT CHECKPOINTU ---
    cp = load_checkpoint(job_id)
    last_cp_slot = None
    if cp and isinstance(cp.get("context"), dict):
        last_cp_slot = cp.get("last_completed_slot")
        print(f"[CHECKPOINT] Znaleziono checkpoint dla #{job_id} (ostatni ukończony slot: {last_cp_slot})", flush=True)
        context.update(cp["context"])

    chain = Chain(
        chain_id,
        "Generator oferty Useme",
        opis="Generuje wycenę i treść oferty dla zlecenia z useme.com",
        silnik="Python + DeepSeek (łańcuch AI)",
        wyzwalacz="manual",
        parent_id=parent_id,
        parent_step=parent_step,
    )

    i = 0
    # Jeśli mamy checkpoint, przeskocz ukończone sloty i odtwórz je jako kroki
    if last_cp_slot:
        last_idx = next((j for j, s in enumerate(slots) if s.get("id") == last_cp_slot), None)
        if last_idx is not None:
            print(f"[CHECKPOINT] Wznawiam od slotu {last_idx + 1}/{len(slots)} (pomijam {last_idx + 1} slotów)", flush=True)
            for prev_s in slots[:last_idx + 1]:
                with chain.step(prev_s["name"], typ="ai", opis="(Wczytano z checkpointu dyskowego)") as k_cp:
                    k_cp.status = "zrobione"
                    k_cp.wyjscie = str(context.get(prev_s.get("output_key", ""), "OK (z checkpointu)"))[:300]
                    k_cp.log("Pominięto generowanie – stan przywrócony z dysku.")
            i = last_idx + 1

    empty_retries = 0
    feedback_rounds = 0
    # Dwie rundy poprawek: 1 runda okazala sie niewystarczajaca (11/13 retry
    # konczylo sie FAIL). 2. runda daje walidatorowi szanse na realna poprawe.
    max_feedback_rounds = 2
    total_steps = 0
    # Limit krokow MUSI uwzgledniac rundy feedbacku: kazda runda cofa lancuch do
    # 02a i powtarza walidator 08. Bez mnoznika petla poprawek wywalala Circuit Breaker.
    max_total_steps = max(40, len(slots) * (max_feedback_rounds + 2) * 2)
    chain_start_time = time.time()

    while i < len(slots):
        total_steps += 1

        # 1. Twardy bezpiecznik liczby kroków (Koniec z pętlami nieskończonymi)
        if total_steps > max_total_steps:
            print(f"[CIRCUIT BREAKER] Zlecenie #{job_id}: Przekroczono limit kroków ({total_steps}/{max_total_steps}) – abort!", flush=True)
            with chain.step("Limit kroków przekroczony", typ="warunek") as k_err:
                k_err.status = "blad"
                k_err.wyjscie = "ABORT_STEP_LIMIT_EXCEEDED"
                k_err.log("Łańcuch zatrzymany przez Circuit Breaker – zbyt wiele ponowień/poprawek.")
            chain._zapisz()
            return None

        # 2. Twardy zegar śmierci (Wall-Clock Watchdog)
        elapsed = time.time() - chain_start_time
        if elapsed > MAX_CHAIN_WALL_CLOCK_S:
            print(f"[DEADLINE WATCHDOG] Zlecenie #{job_id}: Czas minął ({elapsed:.1f}s > {MAX_CHAIN_WALL_CLOCK_S}s) – abort!", flush=True)
            with chain.step("Zegar śmierci", typ="warunek") as k_err:
                k_err.status = "blad"
                k_err.wyjscie = "ABORT_WALL_CLOCK_TIMEOUT"
                k_err.log(f"Zlecenie przekroczyło dopuszczalny czas {MAX_CHAIN_WALL_CLOCK_S}s.")
            chain._zapisz()
            return None

        slot = slots[i]

        with chain.step(slot["name"],
                        typ="ai",
                        opis=slot.get("opis", "")) as krok:
            krok.narzedzie = "DeepSeek"
            krok.wejscie = json.dumps(zlecenie_dane, ensure_ascii=False, indent=2)
            system_prompt, user_prompt = _build_prompt(slot, context)
            krok.promptSystem = system_prompt
            krok.promptUser = user_prompt
            slot_model = slot.get("model", DEEPSEEK_MODEL)
            # Research sieciowy i wycena potrzebuja wiecej czasu niz zwykla generacja.
            slot_timeout = 240 if slot.get("id") in ("01", "02b") else SLOT_TIMEOUT
            odpowiedz = call_deepseek(system_prompt, user_prompt, model=slot_model,
                                      timeout=slot_timeout, on_chunk=krok.stream)

            if slot["role"] == "generator":
                # Research slot (01): jeśli zwrócił pustkę LUB bramka dała OFF
                # (zwróciła BRAK_ISTOTNYCH_FAKTOW), podstaw fallback.
                is_fallback = False
                if slot.get("id") == "01":
                    if (
                        not odpowiedz
                        or len(odpowiedz.strip()) < 20
                        or "BRAK_ISTOTNYCH_FAKTOW" in odpowiedz.upper()
                    ):
                        odpowiedz = "BRAK_ISTOTNYCH_FAKTOW"
                        is_fallback = True
                        krok.log("Research OFF lub pustka – podstawiam BRAK_ISTOTNYCH_FAKTOW")

                # Generator 02b/02a: jeśli poprosił o dopytywanie researchu,
                # odpal wyszukiwanie i poproś model o dokończenie w tej samej turze.
                if slot.get("id") in ("02b", "02a"):
                    query = _extract_research_query(odpowiedz or "")
                    if query:
                        krok.log(f"Model prosi o research: {query[:80]}...")
                        research_wynik = _do_research(query)
                        kontynuacja = (
                            "\n\n--- WYNIK DODATKOWEGO RESEARCHU ---\n" + research_wynik +
                            "\n\nNa podstawie powyższego i wcześniejszych danych dokończ swoje zadanie. "
                            "Nie zwracaj już bloku [RESEARCH_QUERY]. Podaj finalny wynik."
                        )
                        odpowiedz = call_deepseek(
                            system_prompt,
                            user_prompt + "\n\n" + (odpowiedz or "") + kontynuacja,
                            model=slot_model,
                            on_chunk=krok.stream,
                        )

                # Slot 02b: model zwraca STRUKTURE (JSON), a kalkulator w Pythonie
                # liczy kwote deterministycznie. Podstawiamy wynik jako output.
                if slot.get("id") == "02b" and policz_wycene is not None:
                    struktura = _extract_wycena_json(odpowiedz or "")
                    if struktura:
                        try:
                            # Stawka jest DETERMINISTYCZNA (stałe 90 zl/h wszędzie) - kalkulator
                            # ignoruje pole "stawka", ale dla pewnosci usuwamy je tutaj.
                            struktura.pop("stawka", None)
                            struktura.setdefault("id", job_id)
                            if str(zlecenie_dane.get("tier") or "").upper() == "A" or zlecenie_dane.get("typ_klienta") == "ekspert_dziedzinowy":
                                struktura["tier"] = "A"
                            elif zlecenie_dane.get("tier"):
                                struktura.setdefault("tier", zlecenie_dane.get("tier"))
                            flagi = struktura.setdefault("flagi", {})
                            if not flagi.get("budzet_jawny") and zlecenie_dane.get("budget"):
                                flagi["budzet_jawny"] = zlecenie_dane.get("budget")
                            wynik = policz_wycene(struktura)
                            blok = formatuj_wynik(wynik)
                            ostrz = struktura.get("uzasadnienie", "")
                            odpowiedz = (
                                blok + "\n\n--- UZASADNIENIE DOBORU (model) ---\n" + str(ostrz) +
                                "\n\n--- ROZBICIE (kalkulator deterministyczny) ---\n" +
                                json.dumps(wynik["rozbicie"], ensure_ascii=False, indent=2)
                            )
                            if wynik.get("ostrzezenia"):
                                krok.log("Kalkulator: " + "; ".join(wynik["ostrzezenia"]))
                            krok.log(f"Kalkulator: {wynik['kwota']} zl / {wynik['dni']} dni (typ={wynik['typ']})")
                        except Exception as e:
                            krok.log(f"Kalkulator błąd: {e} – zostawiam odpowiedź modelu")
                    else:
                        krok.log("Brak bloku [WYCENA_JSON] – zostawiam odpowiedź modelu")

                # Anty-wyciek (slot 02a): model czasem zwraca chain-of-thought
                # przed właściwą ofertą. Najpierw obcinamy reasoning, a jeśli
                # po wycięciu output nadal jest nim przesycony (brak powitania,
                # dużo markerów) — traktujemy jak pusty wynik i ponawiamy.
                is_reasoning_leak = False
                if slot.get("id") == "02a" and odpowiedz:
                    markery_przed = _policz_markery_reasoningu(odpowiedz)
                    if markery_przed >= 3:
                        oczyszczona = _wytnij_czysta_oferte(odpowiedz)
                        markery_po = _policz_markery_reasoningu(oczyszczona)
                        odpowiedz = oczyszczona
                        if markery_po >= 3:
                            is_reasoning_leak = True
                        else:
                            krok.log(
                                f"Anty-wyciek 02a: obcięto reasoning "
                                f"(markery {markery_przed} -> {markery_po})"
                            )

                # Sprawdzenie pustego wyniku lub braku KWOTA/DNI w slocie 02b
                is_missing_wycena = (
                    slot.get("id") == "02b"
                    and ("KWOTA:" not in (odpowiedz or "").upper() or "DNI:" not in (odpowiedz or "").upper())
                )
                is_empty = (
                    is_reasoning_leak
                    or (not is_fallback and (odpowiedz is None or len(odpowiedz.strip()) < 30))
                    or is_missing_wycena
                )
                if is_empty:
                    empty_retries += 1
                    err_desc = (
                        "wyciek rozumowania (chain-of-thought) zamiast oferty"
                        if is_reasoning_leak
                        else (
                            "brak bloku [WYCENA_JSON] / KWOTA / DNI"
                            if is_missing_wycena
                            else ("timeout AI" if odpowiedz is None else f"pusty lub za krótki wynik ({len(odpowiedz.strip()) if odpowiedz else 0} znaków)")
                        )
                    )
                    if empty_retries > retry_max:
                        krok.log(f"BŁĄD KRYTYCZNY: {err_desc} po {empty_retries} próbach dla slotu {slot['id']} – abort łańcucha")
                        krok.wyjscie = "ABORT_EMPTY_OUTPUT"
                        return None
                    krok.log(f"Generator zwrócił {err_desc} – ponawiam próbę ({empty_retries}/{retry_max})...")
                    continue

                # Deterministyczne oczyszczenie oferty (02a) z pauz długich (— / –), myślników ( - ), nawiasów ( ) i pogrubień Markdown (**)
                # oraz ewentualnych etykiet z promptu typu "Pytanie kwalifikujące:" i kolokwializmów.
                if slot.get("id") == "02a" and odpowiedz:
                    odpowiedz = odpowiedz.replace("**", "").strip()
                    odpowiedz = re.sub(r"\s*[—–\u2014\u2013]\s*", ", ", odpowiedz)
                    odpowiedz = re.sub(r"\s+-\s+", ", ", odpowiedz)
                    odpowiedz = re.sub(r"(?m)^\s*-\s+", "", odpowiedz)
                    while "(" in odpowiedz and ")" in odpowiedz:
                        odpowiedz = re.sub(r"\s*\(([^()]*)\)", r", \1", odpowiedz)
                    odpowiedz = odpowiedz.replace("(", "").replace(")", "")
                    odpowiedz = re.sub(r"(?i)\bpytanie\s+kwalifikuj[ąa]ce\s*:\s*", "", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bkluczowa\s+mina\s*:\s*", "Główna pułapka architektoniczna: ", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bnajdro[żz]sza\s+mina\s*:\s*", "Główne ryzyko produkcyjne: ", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bdrugi\s+obszar\s+to\s+", "Równie istotny jest ", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bkompleksow(?:ego|e|ych|a|ą)\s+", "", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s+z\s+", "w ", odpowiedz)
                    odpowiedz = re.sub(r"(?i)\bwed[łl]ug\s+mojej\s+wiedzy\s*,?\s*", "", odpowiedz)
                    odpowiedz = re.sub(r",\s*,+", ",", odpowiedz)
                    odpowiedz = re.sub(r"\.\s*,", ".", odpowiedz)
                    odpowiedz = re.sub(r"[ \t]{2,}", " ", odpowiedz)

                output_key = slot.get("output_key")
                if output_key:
                    context[output_key] = odpowiedz
                krok.wyjscie = odpowiedz
                krok.reasoning = odpowiedz

                # ZAPIS CHECKPOINTU PO POMYŚLNYM GENERATORZE
                save_checkpoint(job_id, slot["id"], context)
                krok.log(f"[CHECKPOINT] Zapisano stan po slocie {slot['id']}")

                i += 1
                empty_retries = 0

            elif slot["role"] == "validator":
                ok = _is_pass(odpowiedz) if (odpowiedz and odpowiedz.strip()) else False
                krok.wyjscie = "PASS" if ok else "FAIL"
                krok.reasoning = (odpowiedz or "")[:300]
                if ok:
                    save_checkpoint(job_id, slot["id"], context)
                    krok.log(f"[CHECKPOINT] Zapisano stan po walidatorze {slot['id']} (PASS)")
                    i += 1
                    empty_retries = 0
                else:
                    on_fail = slot.get("on_fail", "abort")
                    feedback = _extract_feedback(odpowiedz or "")
                    if feedback and feedback_rounds < max_feedback_rounds:
                        feedback_rounds += 1
                        context["_feedback"] = {
                            _FEEDBACK_TARGETS[k]: v
                            for k, v in feedback.items()
                            if k in _FEEDBACK_TARGETS
                        }
                        target = None
                        for key in ("POPRAW_WYCENA", "POPRAW_OFERTA"):
                            if key in feedback and key in _FEEDBACK_TARGETS:
                                target = _FEEDBACK_TARGETS[key]
                                break
                        if target is None:
                            krok.log("FAIL – nieznany cel poprawek – akceptuję wynik")
                            save_checkpoint(job_id, slot["id"], context)
                            i += 1
                            continue
                        idx = next((j for j, s in enumerate(slots) if s.get("id") == target), None)
                        if idx is None:
                            krok.log(f"nie znaleziono slotu {target} – akceptuję wynik")
                            save_checkpoint(job_id, slot["id"], context)
                            i += 1
                            continue
                        krok.log(f"FAIL – poprawki {list(feedback.keys())} -> retry od {target} "
                                 f"(runda {feedback_rounds}/{max_feedback_rounds})")
                        i = idx
                        continue

                    # Jeśli feedback wyczerpany lub brak wskazówek
                    if feedback or feedback_rounds >= max_feedback_rounds:
                        krok.log(f"FAIL – limit rund feedbacku ({max_feedback_rounds}) – akceptuję najlepszy wynik")
                        save_checkpoint(job_id, slot["id"], context)
                        i += 1
                        continue

                    # Fallback dla starszych walidatorów (lub gdy walidator zwrócił FAIL bez struktury POPRAW_*)
                    feedback_rounds += 1
                    target = on_fail.replace("retry_from_", "")
                    idx = next((j for j, s in enumerate(slots) if s.get("id") == target), None)
                    if idx is None or on_fail == "abort":
                        krok.log("FAIL – abort walidatora")
                        return None

                    krok.log(f"FAIL – retry od {target} (runda {feedback_rounds}/{max_feedback_rounds})")
                    i = idx

    # Pełny sukces łańcucha – czyścimy checkpoint, bo oferta została sfinalizowana
    clear_checkpoint(job_id)
    print(f"[CHECKPOINT] Usunięto checkpoint #{job_id} po pełnym sukcesie łańcucha.", flush=True)

    chain._zapisz()
    # Usuń klucz wewnętrzny przed zwróceniem
    context.pop("_zlecenie", None)
    return context


if __name__ == "__main__":
    import sys

    # Zmuszamy konsolę Windows do UTF-8, żeby print nie wywalał się na
    # znakach unicode (np. „→”) przy kodowaniu cp1250.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    # Użycie:
    #   python chain_executor.py <pipeline_id> [dane_zlecenia.json]
    pipeline_id = sys.argv[1] if len(sys.argv) > 1 else "useme-oferty"

    if len(sys.argv) > 2:
        zlecenie = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8-sig"))
    else:
        # Smoke test – przykładowe zlecenie
        zlecenie = {
            "title": "Strona internetowa dla firmy",
            "budget": "do uzgodnienia",
            "description": "Potrzebuję nowoczesnej strony wizytówki.",
        }

    wynik = run_chain(pipeline_id, zlecenie)
    print(json.dumps({"opis_dlugosc": len(wynik.get("opis", "")) if wynik else None,
                      "wycena": wynik.get("wycena_dni", None)[:200] if wynik else None},
                     ensure_ascii=False, indent=2))