# -*- coding: utf-8 -*-
"""Skrypt uruchamiający pełny benchmark ofert dla zlecenia #144890.

1. Wczytuje naszą ofertę bota (nasza_oferta_bot.json) i ją anonimizuje (jako 'team-alpha').
2. Łączy ją z ofertami konkurencji do pliku 'pula_do_oceny.json'.
3. Formatuje uniwersalny prompt klienta (PROMPT_OCENA_KLIENTA.md).
4. Wysyła prompt do DeepSeek Proxy (port 4571/4570) i Gemini Proxy (port 8045).
5. Zapisuje komplet surowych danych (raw logs) oraz raporty markdown (deepseek_v4.md, gemini_pro.md).
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JOB_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"
RAW_LOGS_DIR = JOB_DIR / "ocena_klienta" / "raw_logs"
RAW_LOGS_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_TEMPLATE_FILE = BASE_DIR / "badania" / "PROMPT_OCENA_KLIENTA.md"
PUBLIC_OFFERS_FILE = JOB_DIR / "oferty_publiczne_30.json"
BOT_OFFER_FILE = JOB_DIR / "nasza_oferta_bot.json"
POOL_FILE = JOB_DIR / "pula_do_oceny.json"

DEEPSEEK_URL = "http://127.0.0.1:4571/v1/chat/completions"
GEMINI_URL = "http://127.0.0.1:8045/v1/chat/completions"


def anonymize_text(text: str) -> str:
    """Usuwa wzmianki o Ksawierze i zamienia na neutralny podpis."""
    t = text
    t = re.sub(r'(?i)\bksawier\s+potrykus\b', 'Zespół Alpha', t)
    t = re.sub(r'(?i)\bksawier\b', 'Alpha', t)
    t = re.sub(r'(?i)\bmaksymilian\b', 'Beta', t)
    return t


def build_evaluation_pool():
    """Tworzy zunifikowaną pulę ofert z zanonimizowaną ofertą bota."""
    if not BOT_OFFER_FILE.exists():
        raise FileNotFoundError(f"Brak pliku oferty bota: {BOT_OFFER_FILE}")
    if not PUBLIC_OFFERS_FILE.exists():
        raise FileNotFoundError(f"Brak pliku ofert konkurencji: {PUBLIC_OFFERS_FILE}")

    bot_raw = json.loads(BOT_OFFER_FILE.read_text(encoding="utf-8"))
    public_offers = json.loads(PUBLIC_OFFERS_FILE.read_text(encoding="utf-8"))

    bot_opis_anon = anonymize_text(bot_raw.get("opis", ""))
    bot_wycena = bot_raw.get("wycena", 9500)
    bot_dni = bot_raw.get("dni", 14)

    our_entry = {
        "offer_id": "bot-team-alpha-144890",
        "job_id": "144890",
        "author_name": "team-alpha",
        "author_profile_url": "https://useme.com/pl/roles/contractor/team-alpha,608362/",
        "author_contracts": "8 umów",
        "price": f"{bot_wycena},00 PLN",
        "days": f"{bot_dni} dni pracy",
        "proposal_text": bot_opis_anon,
        "proposal_length": len(bot_opis_anon),
        "is_our_bot": True,
        "links": []
    }

    # Wstawiamy naszą ofertę w realistyczne miejsce (np. pozycja 12)
    pool = []
    inserted = False
    for idx, off in enumerate(public_offers):
        if idx == 12 and not inserted:
            pool.append(our_entry)
            inserted = True
        off_copy = dict(off)
        off_copy["is_our_bot"] = False
        pool.append(off_copy)

    if not inserted:
        pool.append(our_entry)

    POOL_FILE.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[PULA] Utworzono pulę {len(pool)} ofert (w tym 'team-alpha' na pozycji {pool.index(our_entry) + 1}).")
    return pool, our_entry


def format_prompt(pool: list) -> str:
    template = PROMPT_TEMPLATE_FILE.read_text(encoding="utf-8")

    tresc_zlecenia = """Zlecenie: Automatyzacja obiegu dokumentów (OCR + LLM): n8n / Make
Branża: Piekarnia (firma produkcyjno-handlowa)

Opis zlecenia:
Dzień dobry,
Zlecę stworzenie, pełne wdrożenie oraz opiekę serwisową nad automatyzacją obiegu dokumentów (faktury, zamówienia, dokumenty kosztowe) w firmie z branży piekarniczej.
Logika procesu:
1. Dokumenty ze skanera, maili oraz aplikacji mobilnej trafiają do folderu wejściowego na Google Drive.
2. Automatyzacja pobiera plik, przetwarza go przez silnik OCR wsparty modelem LLM (rozpoznanie typu dokumentu, wyciągnięcie kluczowych danych, kwot, kontrahenta itp.).
3. Plik jest odpowiednio nazywany i przenoszony do docelowego folderu na Google Drive.
4. Dane z dokumentu są przekazywane do naszych systemów: ProfiPiek (program piekarniczy) oraz Comarch Optima.

Wymagania dotyczące technologii i wyceny:
Zależy mi na optymalizacji kosztów bieżących, dlatego skłaniam się ku n8n postawionym na własnym serwerze (brak opłat za każdą operację). Dopuszczam jednak Make, jeśli wdrożenie będzie tego warte.
Zależy mi na otrzymaniu:
- Wyceny na n8n (z uwzględnieniem postawienia/konfiguracji środowiska),
- Opcjonalnie wyceny na Make (lub krótkiego uzasadnienia w ofercie, dlaczego rekomendujesz jedno z tych rozwiązań pod ten konkretny przypadek).

Zakres zlecenia:
Cena musi być kompleksowa i obejmować:
- Zaprojektowanie i zbudowanie całej automatyzacji,
- Wdrożenie całości w naszym środowisku i przetestowanie na rzeczywistych dokumentach,
- Serwis i wsparcie techniczne w razie komplikacji powdrożeniowych (okres gwarancyjny/asysta po uruchomieniu).

W ofercie proszę o:
- Konkretną kwotę (lub widełki dla n8n oraz Make).
- Krótki opis, jak technicznie planujesz rozwiązać połączenie z Optimą i ProfiPiekiem (np. API, bezpośrednie zapytania do bazy SQL, pliki wymiany).
- Szacowany czas realizacji oraz warunki wsparcia po wdrożeniu."""

    budzet = """Budżet w zleceniu: "Do negocjacji".
W mojej głowie: Zależy mi na uniknięciu kosztów subskrypcyjnych (dlatego preferuję self-hosted n8n na serwerze zamiast drogiego Make). Szukam rzetelnego, kompleksowego rozwiązania od A do Z z gwarancją. Oczekuję realnego budżetu w granicach 5 000 – 15 000 zł w zależności od tego, czy wykonawca ogarnia integrację z Comarch Optima i trudne skany bez błędów."""

    oferty_str_parts = []
    for idx, off in enumerate(pool, start=1):
        name = off.get("author_name", f"oferent_{idx}")
        cena = off.get("price", "Brak ceny")
        dni = off.get("days", "Brak terminu")
        umowy = off.get("author_contracts", "0 umów")
        tresc = (off.get("proposal_text") or "").strip()
        oferty_str_parts.append(
            f"### OFERTA #{idx}: {name}\n"
            f"**Cena:** {cena} | **Termin:** {dni} | **Doświadczenie Useme:** {umowy}\n\n"
            f"**Treść propozycji:**\n{tresc}\n"
        )

    sep = "\n\n" + ("=" * 50) + "\n\n"
    lista_ofert = sep + sep.join(oferty_str_parts)

    prompt = template.replace("{TRESC_ZLECENIA}", tresc_zlecenia)
    prompt = prompt.replace("{BUDZET}", budzet)
    prompt = prompt.replace("{LISTA_OFERT}", lista_ofert)

    return prompt


def call_ai(url: str, model_name: str, prompt: str, stream: bool = True, timeout: int = 600) -> dict:
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4,
        "max_tokens": 8192,
        "stream": stream
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw_lines = []
            full_content = ""
            full_reasoning = ""
            raw_body = ""

            # Sprawdź czy to strumień SSE
            if "text/event-stream" in content_type or stream:
                first_line = resp.readline()
                if not first_line:
                    return {"success": False, "elapsed_s": round(time.time() - t0, 2), "error": "Pusta odpowiedź serwera"}
                
                first_line_str = first_line.decode("utf-8", errors="replace")
                raw_lines.append(first_line_str)

                if first_line_str.strip().startswith("{"):
                    # Serwer zwrócił jednak pojedynczy JSON (nie SSE)
                    rest = resp.read().decode("utf-8", errors="replace")
                    raw_body = first_line_str + rest
                    try:
                        data = json.loads(raw_body)
                        choices = data.get("choices", [{}])
                        msg = choices[0].get("message", {}) if choices else {}
                        full_content = msg.get("content", "")
                        full_reasoning = msg.get("reasoning_content", "") or msg.get("reasoning", "")
                    except Exception as je:
                        return {"success": False, "elapsed_s": round(time.time() - t0, 2), "error": f"JSON parse error: {je}", "raw_response": raw_body}
                else:
                    # Rzeczywisty strumień SSE
                    def process_sse_line(line_s):
                        nonlocal full_content, full_reasoning
                        line_s = line_s.strip()
                        if not line_s.startswith("data:"):
                            return False
                        data_part = line_s[5:].strip()
                        if data_part == "[DONE]":
                            return True
                        try:
                            chunk = json.loads(data_part)
                            choices = chunk.get("choices", [{}])
                            if choices:
                                delta = choices[0].get("delta", {})
                                text = delta.get("content", "")
                                reasoning = delta.get("reasoning_content", "") or delta.get("reasoning", "")
                                if text:
                                    full_content += text
                                    print(text, end="", flush=True)
                                if reasoning:
                                    full_reasoning += reasoning
                        except Exception:
                            pass
                        return False

                    process_sse_line(first_line_str)
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        l_str = line.decode("utf-8", errors="replace")
                        raw_lines.append(l_str)
                        if process_sse_line(l_str):
                            break
                    raw_body = "".join(raw_lines)
            else:
                raw_body = resp.read().decode("utf-8", errors="replace")
                try:
                    data = json.loads(raw_body)
                    choices = data.get("choices", [{}])
                    msg = choices[0].get("message", {}) if choices else {}
                    full_content = msg.get("content", "")
                    full_reasoning = msg.get("reasoning_content", "") or msg.get("reasoning", "")
                except Exception as je:
                    return {"success": False, "elapsed_s": round(time.time() - t0, 2), "error": f"JSON parse error: {je}", "raw_response": raw_body}

            elapsed = time.time() - t0
            print() # Nowa linia po strumieniu
            return {
                "success": bool(full_content.strip()),
                "elapsed_s": round(elapsed, 2),
                "content": full_content,
                "reasoning": full_reasoning,
                "raw_response": raw_body
            }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "success": False,
            "elapsed_s": round(elapsed, 2),
            "content": "",
            "reasoning": "",
            "error": str(e)
        }


def run_benchmark():
    print("=== ROZPOCZYNAM BENCHMARK OFERT #144890 ===")
    pool, our_entry = build_evaluation_pool()
    full_prompt = format_prompt(pool)

    # Zapisz pełny prompt ewaluacyjny
    prompt_file = RAW_LOGS_DIR / "prompt_klienta_pelen.md"
    prompt_file.write_text(full_prompt, encoding="utf-8")
    print(f"[PROMPT] Zapisano pełny prompt ({len(full_prompt)} znaków) do: {prompt_file}")

    # 1. DEEPSEEK EVALUATION
    print("\n--- [1/2] URUCHAMIAM OCENĘ PRZEZ DEEPSEEK V4 PRO (Port 4571)... ---")
    ds_res = call_ai(DEEPSEEK_URL, "deepseek-v4-pro", full_prompt, stream=True, timeout=600)
    (RAW_LOGS_DIR / "deepseek_raw_response.json").write_text(
        json.dumps(ds_res, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if ds_res["success"]:
        print(f"\n[DEEPSEEK] Zakończono sukcesem w {ds_res['elapsed_s']}s!")
        ds_text = ds_res.get("content", "")
        out_ds = JOB_DIR / "ocena_klienta" / "deepseek_v4.md"
        out_ds.write_text(ds_text, encoding="utf-8")
        print(f"[DEEPSEEK] Zapisano recenzję klienta do: {out_ds}")
        if ds_res.get("reasoning"):
            (RAW_LOGS_DIR / "deepseek_reasoning.md").write_text(ds_res["reasoning"], encoding="utf-8")
            print(f"[DEEPSEEK] Zapisano ślad rozumowania (reasoning trace) do raw_logs/deepseek_reasoning.md")
    else:
        print(f"\n[DEEPSEEK BŁĄD]: {ds_res.get('error')}")

    # 2. GEMINI EVALUATION
    print("\n--- [2/2] URUCHAMIAM OCENĘ PRZEZ GEMINI PROXY (Port 8045)... ---")
    gem_res = call_ai(GEMINI_URL, "gemini-3.8-flash-thinking", full_prompt, stream=False, timeout=600)
    (RAW_LOGS_DIR / "gemini_raw_response.json").write_text(
        json.dumps(gem_res, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if gem_res["success"]:
        print(f"\n[GEMINI] Zakończono sukcesem w {gem_res['elapsed_s']}s!")
        gem_text = gem_res.get("content", "")
        out_gem = JOB_DIR / "ocena_klienta" / "gemini_pro.md"
        out_gem.write_text(gem_text, encoding="utf-8")
        print(f"[GEMINI] Zapisano recenzję klienta do: {out_gem}")
        if gem_res.get("reasoning"):
            (RAW_LOGS_DIR / "gemini_reasoning.md").write_text(gem_res["reasoning"], encoding="utf-8")
            print(f"[GEMINI] Zapisano ślad rozumowania (reasoning trace) do raw_logs/gemini_reasoning.md")
    else:
        print(f"\n[GEMINI BŁĄD]: {gem_res.get('error')}")

    print("\n=== ZAKOŃCZONO ETAP EWALUACJI MODELI ===")


if __name__ == "__main__":
    run_benchmark()
