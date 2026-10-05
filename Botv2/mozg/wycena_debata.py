# -*- coding: utf-8 -*-
"""Wycena debaty wieloagentowej (Adversarial Multi-Model Pricing Debate) dla Useme.

Architektura:
- Dwa niezależne modele:
    * Wyceniacz (domyślnie DeepSeek-v4-Pro): inżynier-architekt, rzetelna ocena ryzyka technicznego.
    * Reviewer (domyślnie Gemini-3.8-Flash): twardy recenzent z Useme, pilnujący realiów budżetowych MŚP.
- Czyste prompty: ZERO wpisanych z góry widełek kwotowych ani sztucznych barier.
- Automatyczny retry z backoffem na błędy sieci i parsowania.
- Deterministyczny guardrail na końcu: zaokrąglenie psychologiczne (500/1000 zł), minimum 500 zł, min. 7 dni.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Callable, Dict, Optional, Tuple

# --- CZYSTE PROMPTY DOMENOWE BEZ HARDKODOWANYCH LICZB/WIDEŁEK ---

PROMPT_WYCENIACZ = """Jesteś Ksawierem – polskim inżynierem-freelancerem na platformie Useme.
Rozliczasz się przez umowę o dzieło na Useme (bez pośredników, bez firmy, bez kosztów biura agencji).
Pracujesz solo, wspomagany zaawansowanymi narzędziami programistycznymi AI (piszesz architekturę, kod i testy znacznie szybciej niż tradycyjne zespoły, zachowując najwyższą jakość).

ZASADY WYCENY DLA FREELANCERA NA USEME:
1. BRAK 'STAWKI DZIENNEJ' (MAN-DAY):
   - Termin w dniach to czas kalendarzowy projektu (etapowanie, testy klienta na rzeczywistych danych, poprawki). Nie przeliczasz tego jak etatu korporacyjnego (dni * 8h).
2. PSYCHOLOGIA I REALIA POLSKICH KLIENTÓW MŚP NA USEME:
   - Klienci na Useme to zazwyczaj małe i średnie polskie firmy, które szukają zwinnego specjalisty, bo agencja software house wyceniła ich na kosmiczne kwoty enterprise.
   - Pamiętaj o dwóch skrajnościach:
     * Unikaj amatorskiego dumpingu za grosze (klient ucieka przed kimś, kto rzuca kwotami niepoważnymi za trudny system).
     * Unikaj stawek korporacyjnego software house'u z Warszawy (przetargi korporacyjne to nie ten rynek; klient na Useme natychmiast odrzuci taką ofertę).
   - Wyceniaj za wartość biznesową, trudność inżynierską, ryzyko i odpowiedzialność za dane/proces klienta.
3. KOTWICA BUDŻETU:
   - Jeśli klient w ogłoszeniu podał bardzo małą kwotę (stawkę rzędu kilkudziesięciu lub stu kilkudziesięciu złotych), to zazwyczaj oznacza deklarowaną preferowaną stawkę za godzinę konsultacji/rozwoju, a NIE budżet na całość projektu!
   - Jeśli klient podał jawny budżet całkowity projektu, weź go pod uwagę przy ocenie realnych możliwości finansowych klienta.

Na podstawie zlecenia oszacuj rzetelną kwotę w PLN netto oraz termin w dniach kalendarzowych (min. 7 dni).

Zwróć WYŁĄCZNIE JSON:
{
  "kwota": <int>,
  "dni_od": <int>,
  "dni_do": <int>,
  "typ": "projekt" lub "male" lub "retainer",
  "uzasadnienie": "2-3 konkretne zdania inżynierskie: dlaczego taka kwota i termin dla freelancera z AI na Useme"
}
"""

PROMPT_REVIEWER = "Jesteś niezależnym ekspertem i recenzentem wycen zleceń na portalu Useme."


def _oczysc_int(wartosc: Any, domyslna: int = 0) -> int:
    """Konwertuje dowolną wartość (int, str np. '15 000 zł', float) na czysty int."""
    if wartosc is None:
        return domyslna
    if isinstance(wartosc, (int, float)):
        return int(wartosc)
    s = str(wartosc).strip()
    tylko_cyfry = re.sub(r"[^\d]", "", s)
    if tylko_cyfry:
        return int(tylko_cyfry)
    return domyslna


def _parsuj_json_wyceniacz(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass

    if isinstance(data, dict):
        kwota = _oczysc_int(data.get("kwota"))
        dni_od = _oczysc_int(data.get("dni_od"), 7)
        dni_do = _oczysc_int(data.get("dni_do"), max(dni_od, 14))
        typ = str(data.get("typ") or "projekt").strip()
        if kwota > 0:
            return {
                "kwota": kwota,
                "dni_od": dni_od,
                "dni_do": dni_do,
                "typ": typ,
                "uzasadnienie": str(data.get("uzasadnienie", "")).strip(),
            }

    # Fallback regex (w przypadku obcięcia strumienia pod koniec)
    m_kwota = re.search(r'"kwota"\s*:\s*["\']?(\d[\d\s]*)', raw)
    if m_kwota:
        kwota = _oczysc_int(m_kwota.group(1))
        if kwota > 0:
            m_od = re.search(r'"dni_od"\s*:\s*["\']?(\d[\d\s]*)', raw)
            m_do = re.search(r'"dni_do"\s*:\s*["\']?(\d[\d\s]*)', raw)
            m_uz = re.search(r'"uzasadnienie"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
            dni_od = _oczysc_int(m_od.group(1), 7) if m_od else 7
            dni_do = _oczysc_int(m_do.group(1), max(dni_od, 14)) if m_do else 21
            uz = m_uz.group(1) if m_uz else "Uzasadnienie wyceny."
            return {
                "kwota": kwota,
                "dni_od": dni_od,
                "dni_do": dni_do,
                "typ": "projekt",
                "uzasadnienie": uz.strip(),
            }
    return None


def _parsuj_json_reviewer(tekst: Optional[str]) -> Optional[Dict[str, Any]]:
    if not tekst:
        return None
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", tekst.strip(), flags=re.MULTILINE).strip()
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass

    if isinstance(data, dict):
        werdykt_raw = str(data.get("werdykt", "")).upper().strip()
        if "MALA" in werdykt_raw or "MAŁA" in werdykt_raw:
            werdykt = "ZA_MALA"
        elif "DUZA" in werdykt_raw or "DUŻA" in werdykt_raw:
            werdykt = "ZA_DUZA"
        elif "OK" in werdykt_raw:
            werdykt = "OK"
        else:
            werdykt = "OK"

        kwota_sug = _oczysc_int(data.get("kwota_sugerowana"), 0)
        dni_sug = _oczysc_int(data.get("dni_sugerowane_do"), 0)

        return {
            "werdykt": werdykt,
            "kwota_sugerowana": kwota_sug,
            "dni_sugerowane_do": dni_sug,
            "uzasadnienie": str(data.get("uzasadnienie", "")).strip(),
            "twoje_oszacowanie_rynku": str(data.get("twoje_oszacowanie_rynku", "")).strip(),
        }

    # Fallback regex
    m_w = re.search(r'"werdykt"\s*:\s*["\']?([A-Za-z_]+)', raw)
    if m_w:
        werdykt_raw = m_w.group(1).upper().strip()
        if "MALA" in werdykt_raw or "MAŁA" in werdykt_raw:
            werdykt = "ZA_MALA"
        elif "DUZA" in werdykt_raw or "DUŻA" in werdykt_raw:
            werdykt = "ZA_DUZA"
        else:
            werdykt = "OK"
        m_kw = re.search(r'"kwota_sugerowana"\s*:\s*["\']?(\d[\d\s]*)', raw)
        kwota_sug = _oczysc_int(m_kw.group(1)) if m_kw else 0
        m_dni = re.search(r'"dni_sugerowane_do"\s*:\s*["\']?(\d[\d\s]*)', raw)
        dni_sug = _oczysc_int(m_dni.group(1)) if m_dni else 0
        m_uz = re.search(r'"uzasadnienie"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
        uz = m_uz.group(1) if m_uz else ""
        m_ryn = re.search(r'"twoje_oszacowanie_rynku"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)', raw)
        ryn = m_ryn.group(1) if m_ryn else ""
        return {
            "werdykt": werdykt,
            "kwota_sugerowana": kwota_sug,
            "dni_sugerowane_do": dni_sug,
            "uzasadnienie": uz.strip(),
            "twoje_oszacowanie_rynku": ryn.strip(),
        }
    return None


def _zaokraglij_psychologicznie(kwota: int) -> int:
    """Zaokrąglenie cenowe pod psychologię klienta Useme."""
    if kwota <= 2000:
        return int(round(kwota / 50.0) * 50)
    if kwota <= 10000:
        return int(round(kwota / 500.0) * 500)
    return int(round(kwota / 1000.0) * 1000)


def _call_z_retry(
    fn_call: Callable[[str, str], Optional[str]],
    parser_fn: Callable[[Optional[str]], Optional[Dict[str, Any]]],
    system_prompt: str,
    user_prompt: str,
    rola: str,
    say: Callable[[str], None],
    max_proby: int = 3,
    delay: float = 2.0,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Wywołuje funkcję AI z automatycznym ponawianiem w przypadku pustego tekstu lub błędu parsowania."""
    for proba in range(1, max_proby + 1):
        if proba > 1:
            say(f"    [{rola}] Retry próba {proba}/{max_proby} po {delay}s (reset sesji)...")
            try:
                import requests
                requests.post("http://127.0.0.1:8045/v1/chat/reset", timeout=5)
            except Exception:
                pass
            time.sleep(delay)
        raw = fn_call(system_prompt, user_prompt)
        parsed = parser_fn(raw)
        if parsed is not None:
            return parsed, raw
    return None, None


def wycen_przez_debate(
    tresc_zlecenia: str,
    dziennik: str = "",
    research: str = "",
    call_wyceniacz_fn: Optional[Callable[[str, str], Optional[str]]] = None,
    call_reviewer_fn: Optional[Callable[[str, str], Optional[str]]] = None,
    call_ai_fn: Optional[Callable[[str, str], Optional[str]]] = None,
    say: Optional[Callable[[str], None]] = None,
    max_rundy: int = 2,
) -> Dict[str, Any]:
    """Przeprowadza prawdziwą debatę dwumodelową (Cross-Model Adversarial Pricing).

    Domyślnie:
    - Wyceniacz: DeepSeek-v4-Pro (precyzyjna analiza techniczna)
    - Reviewer: Gemini-3.8-Flash (twardy recenzent budżetowy MŚP na Useme)
    """
    if say is None:
        say = lambda msg: None

    # Reset sesji przeglądarki Gemini na start debaty
    try:
        import requests
        requests.post("http://127.0.0.1:8045/v1/chat/reset", timeout=5)
    except Exception:
        pass

    # Kompatybilność wsteczna: jeśli podano tylko call_ai_fn, użyj go jako fallback
    if call_wyceniacz_fn is None:
        if call_ai_fn is not None:
            call_wyceniacz_fn = call_ai_fn
        else:
            from brain import call_ai
            call_wyceniacz_fn = call_ai

    if call_reviewer_fn is None:
        try:
            from brain import call_gemini
            call_reviewer_fn = call_gemini
        except ImportError:
            call_reviewer_fn = call_wyceniacz_fn

    say("    debata wycenowa: Wyceniacz [DeepSeek] vs Reviewer [Gemini]...")

    kontekst_wyceniacza = (
        f"ZLECENIE KLIENTA NA USEME:\n{tresc_zlecenia}\n\n"
        f"DZIENNIK MYŚLENIA:\n{dziennik or 'Brak'}\n\n"
        f"RESEARCH DOWODOWY:\n{research or 'Brak'}"
    )

    # --- RUNDA 0: Wyceniacz ---
    prop, raw_w0 = _call_z_retry(
        fn_call=call_wyceniacz_fn,
        parser_fn=_parsuj_json_wyceniacz,
        system_prompt=PROMPT_WYCENIACZ,
        user_prompt=kontekst_wyceniacza,
        rola="Wyceniacz",
        say=say,
    )

    if not prop:
        say("    [Wyceniacz] Brak poprawnej odpowiedzi po retry – zastosowano bezpieczną stawkę bazową 6000 zł.")
        prop = {
            "kwota": 6000,
            "dni_od": 14,
            "dni_do": 21,
            "typ": "projekt",
            "uzasadnienie": "Standardowa realizacja zwinnego systemu z narzędziami AI.",
        }

    say(f"    [Wyceniacz R0] {prop['kwota']} zł | {prop['dni_od']}-{prop['dni_do']} dni ({prop.get('uzasadnienie', '')[:65]}...)")

    przebieg: list = [{
        "runda": 0,
        "aktor": "WYCENIACZ",
        "kwota": prop["kwota"],
        "dni_od": prop["dni_od"],
        "dni_do": prop["dni_do"],
        "uzasadnienie": prop.get("uzasadnienie", ""),
    }]

    rev: Dict[str, Any] = {"werdykt": "OK", "uzasadnienie": "Brak uwag."}
    wynegocjowane_w_rundzie = 0

    for runda in range(1, max_rundy + 1):
        time.sleep(1.0)

        # --- REVIEWER ---
        prompt_rev_usr = (
            f"Oceń poniższą ofertę freelancera na zlecenie Useme.\n\n"
            f"Zakres zlecenia klienta:\n{tresc_zlecenia}\n\n"
            f"Oferta freelancera do oceny:\n"
            f"- Kwota: {prop['kwota']} zł netto\n"
            f"- Czas realizacji: {prop['dni_do']} dni\n"
            f"- Zakres: {prop.get('uzasadnienie', '')}\n\n"
            f"Zwróć WYŁĄCZNIE poprawny JSON w formacie:\n"
            f"{{\n"
            f'  "werdykt": "ZA_MALA" | "OK" | "ZA_DUZA",\n'
            f'  "kwota_sugerowana": <int>,\n'
            f'  "dni_sugerowane_do": <int>,\n'
            f'  "uzasadnienie": "2-3 zdania analizy",\n'
            f'  "twoje_oszacowanie_rynku": "widełki rynkowe"\n'
            f"}}"
        )

        rev_wynik, raw_r = _call_z_retry(
            fn_call=call_reviewer_fn,
            parser_fn=_parsuj_json_reviewer,
            system_prompt=PROMPT_REVIEWER,
            user_prompt=prompt_rev_usr,
            rola="Reviewer",
            say=say,
        )

        if not rev_wynik:
            say("    [Reviewer] Brak odpowiedzi po retry – zatwierdzam aktualną wycenę.")
            rev = {"werdykt": "OK", "uzasadnienie": "Brak zastrzeżeń recenzenta po retry."}
            wynegocjowane_w_rundzie = runda
            break

        rev = rev_wynik
        werdykt = rev["werdykt"]
        say(f"    [Reviewer R{runda}] {werdykt} (sugeruje: {rev.get('kwota_sugerowana')} zł, rynek: {rev.get('twoje_oszacowanie_rynku', '?')})")

        przebieg.append({
            "runda": runda,
            "aktor": "REVIEWER",
            "werdykt": werdykt,
            "kwota_sugerowana": rev.get("kwota_sugerowana"),
            "rynek": rev.get("twoje_oszacowanie_rynku", ""),
            "uzasadnienie": rev.get("uzasadnienie", ""),
        })

        if werdykt == "OK":
            wynegocjowane_w_rundzie = runda
            break

        time.sleep(1.0)

        # --- WYCENIACZ KONTRA ---
        prompt_w_kontra = (
            f"ZLECENIE KLIENTA NA USEME:\n{tresc_zlecenia}\n\n"
            f"TWOJA POPRZEDNIA PROPOZYCJA: {prop['kwota']} zł / {prop['dni_od']}-{prop['dni_do']} dni.\n"
            f"RECENZENT Z USEME OCENIŁ: {werdykt}\n"
            f"KRYTYKA RECENZENTA: {rev.get('uzasadnienie', '')}\n"
            f"SUGESTIA RECENZENTA: {rev.get('kwota_sugerowana')} zł (jego szacunek rynku: {rev.get('twoje_oszacowanie_rynku', '')})\n\n"
            f"Ustosunkuj się merytorycznie. Jeśli recenzent ma rację, skoryguj kwotę. Jeśli Twoja wycena broni się inżyniersko, uzasadnij to. Zwróć JSON."
        )

        nowy_prop, raw_w = _call_z_retry(
            fn_call=call_wyceniacz_fn,
            parser_fn=_parsuj_json_wyceniacz,
            system_prompt=PROMPT_WYCENIACZ,
            user_prompt=prompt_w_kontra,
            rola="Wyceniacz_kontra",
            say=say,
        )

        if nowy_prop:
            prop = nowy_prop
            say(f"    [Wyceniacz R{runda} Kontra] -> {prop['kwota']} zł / {prop['dni_od']}-{prop['dni_do']} dni")
            przebieg.append({
                "runda": runda,
                "aktor": "WYCENIACZ_KONTRA",
                "kwota": prop["kwota"],
                "dni_od": prop["dni_od"],
                "dni_do": prop["dni_do"],
                "uzasadnienie": prop.get("uzasadnienie", ""),
            })
        else:
            say(f"    [Wyceniacz R{runda}] Brak odpowiedzi w kontrze – zachowuję {prop['kwota']} zł.")
            wynegocjowane_w_rundzie = runda
            break

        wynegocjowane_w_rundzie = runda

    # --- DETERMINISTYCZNY GUARDRAIL (twarde wymogi Useme) ---
    surowa_kwota = int(prop.get("kwota") or 3000)
    kwota = _zaokraglij_psychologicznie(max(surowa_kwota, 500))

    dni_do = int(prop.get("dni_do") or prop.get("dni") or 21)
    dni_od = int(prop.get("dni_od") or max(7, dni_do - 7))
    dni_do = max(dni_do, 7)
    dni_od = max(min(dni_od, dni_do), 7)

    typ = prop.get("typ") or "projekt"
    say(f"    -> [Finał Debaty] {kwota} zł / {dni_od}-{dni_do} dni (psychologiczne zaokrąglenie, Useme ready)")

    return {
        "kwota": kwota,
        "dni": dni_do,
        "dni_od": dni_od,
        "dni_do": dni_do,
        "typ": typ,
        "uzasadnienie": prop.get("uzasadnienie", ""),
        "reviewer_werdykt": rev.get("werdykt", "OK"),
        "reviewer_uwagi": rev.get("uzasadnienie", ""),
        "widełki_rynkowe": rev.get("twoje_oszacowanie_rynku", ""),
        "rundy": wynegocjowane_w_rundzie,
        "przebieg": przebieg,
        "rozbicie": {
            "tryb": "debata_dwumodelowa_useme",
            "surowa_kwota_ai": surowa_kwota,
            "kwota_koncowa": kwota,
            "dni_od": dni_od,
            "dni_do": dni_do,
            "rundy_debaty": wynegocjowane_w_rundzie,
            "uzasadnienie_wyceniacza": prop.get("uzasadnienie", ""),
            "krytyka_reviewera": rev.get("uzasadnienie", ""),
            "widełki_rynkowe": rev.get("twoje_oszacowanie_rynku", ""),
            "przebieg": przebieg,
        },
    }
