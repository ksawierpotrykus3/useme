# -*- coding: utf-8 -*-
"""Moduł AI Pipeline – w pełni odizolowany od mechaniki przeglądarki i magazynu.

Każdy model AI lub programista może łatwo modyfikować ten plik:
- zmieniać prompty,
- dodawać/usuwać kroki analizy i walidacji,
- zmieniać kryteria selekcji.
Przeglądarka i magazyn wywołują wyłącznie metody: `filter_offers` oraz `generate_proposal`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import config
from config import USE_MOCK_AI

# Ścieżka do promptów (można swobodnie przestawiać pliki)
PROMPTS_DIR = Path(__file__).parent / "prompts"

# --- ANTY-POWTÓRKA: próg podobieństwa i liczba prób przepisania ---
PROG_PODOBNOSCI = 0.70      # > 70% podobieństwa = oferta do przepisania
MAX_ANTY_POWTORKA_RETRY = 2  # maksymalna liczba prób przepisania

# --- GLOBALNY wykrywacz duplikatów (między zleceniami, nie tylko per klient) ---
PROG_PODOBNOSCI_GLOBALNY = 0.75   # > 75% podobieństwa do DOWOLNEJ ostatniej oferty = flaga
GLOBALNY_OKNO_DNI = 7             # porównuj z ofertami z ostatnich N dni


def _podobienstwo_jaccard(a: str, b: str) -> float:
    """Liczy podobieństwo dwóch tekstów metodą Jaccarda na zbiorze słów.

    Zwraca wartość 0.0–1.0. 1.0 = identyczny zestaw słów.
    Prosty, deterministyczny wskaźnik wykrywania skopiowanych ofert.
    """
    import re as _re
    slowa_a = set(_re.findall(r"\w+", (a or "").lower()))
    slowa_b = set(_re.findall(r"\w+", (b or "").lower()))
    if not slowa_a or not slowa_b:
        return 0.0
    czesc_wspolna = slowa_a & slowa_b
    suma = slowa_a | slowa_b
    return len(czesc_wspolna) / len(suma) if suma else 0.0


def sprawdz_globalne_duplikaty(opis: str, storage, wlasne_job_id: str = "") -> list:
    """Sprawdza, czy nowa oferta jest zbyt podobna do DOWOLNEJ oferty z ostatnich N dni.

    W odroznieniu od anty-powtorki per klient (ktora porownuje tylko oferty dla
    tego samego zleceniodawcy), ta funkcja patrzy na WSZYSTKIE ostatnie oferty.
    Chroni przed tym, ze model z czasem zaczyna pisac wszystkie oferty tak samo.

    Zwraca liste {job_id, podobienstwo} ofert przekraczajacych prog (pusta = OK).
    """
    if not opis or not storage:
        return []
    progi = []
    try:
        ostatnie = storage.wszystkie_oferty(limit_dni=GLOBALNY_OKNO_DNI)
    except Exception:
        return []
    for o in ostatnie:
        if str(o.get("job_id", "")) == str(wlasne_job_id):
            continue
        stary = o.get("opis") or ""
        if not stary.strip():
            continue
        pod = _podobienstwo_jaccard(opis, stary)
        if pod > PROG_PODOBNOSCI_GLOBALNY:
            progi.append({"job_id": o.get("job_id"), "podobienstwo": round(pod, 3)})
    progi.sort(key=lambda x: x["podobienstwo"], reverse=True)
    return progi


@dataclass
class ProposalResult:
    """Zunifikowany wynik pracy modułu AI dla jednej oferty."""
    opis: str
    wycena: int
    dni: int
    powod_wyboru: str = ""
    metadata: Optional[Dict[str, Any]] = None


class BaseAIPipeline:
    """Interfejs bazowy dla łańcucha AI."""
    def filter_offers(self, offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def generate_proposal(self, job_detail: Dict[str, Any]) -> ProposalResult:
        raise NotImplementedError


class MockAIPipeline(BaseAIPipeline):
    """Deterministyczny moduł testowy – do sprawdzania czy szkielet programu działa

    bez czekania na sieć, tokeny czy lokalne proxy DeepSeek.
    """
    def filter_offers(self, offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Wybiera 1 zlecenie do precyzyjnego testu
        return offers[:1] if offers else []

    def generate_proposal(self, job_detail: Dict[str, Any]) -> ProposalResult:
        title = job_detail.get("title", "Zlecenie testowe")
        budget_str = str(job_detail.get("budget", "1500"))
        # Wyciągamy liczbę lub domyślne 1500 zł
        kwota = 1500
        for part in budget_str.replace(" ", "").split(","):
            digits = "".join(filter(str.isdigit, part))
            if digits:
                parsed = int(digits)
                if parsed >= 100:
                    kwota = parsed
                    break

        return ProposalResult(
            opis=f"Dzień dobry,\n\nZgłaszam swoją gotowość do realizacji zlecenia '{title}'.\nPosiadam doświadczenie w wymaganym zakresie i gwarantuję terminowe dowiezienie projektu.\n\nPozdrawiam,\nZespół",
            wycena=kwota,
            dni=7, # Zgodnie z regułą Useme: minimum 7 dni
            powod_wyboru="Deterministyczny mock dla testu szkieletu"
        )


class SlotChainAIPipeline(BaseAIPipeline):
    """Prawdziwy łańcuch AI wykorzystujący system slotów z chain_executor.py oraz Sędziego 1-100 z audytor_lancuch.py."""
    def __init__(self):
        try:
            from chain_executor import run_chain, call_deepseek, parse_ai_json_response
            self._run_chain = run_chain
            self._call_deepseek = call_deepseek
            self._parse_json = parse_ai_json_response
        except ImportError:
            self._run_chain = None
            self._call_deepseek = None
            self._parse_json = None

        try:
            from audytor_lancuch import audit_and_refine_100, _sanitize_opis
            self._audit_100 = audit_and_refine_100
            self._sanitize_opis = _sanitize_opis
        except ImportError:
            self._audit_100 = None
            self._sanitize_opis = None

    def filter_offers(self, offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Selekcja zleceń przez deterministyczny filtr Red Ocean + AI #1 (deepseek-v4-pro-nothink).

        Przyjmuje wszystkie nowe zlecenia (z pełnymi opisami), odrzuca twarde wykluczenia
        z config.is_hard_reject, a następnie przepuszcza przez kryteria selekcji AI #1.
        Zwraca wyłącznie te oferty, które otrzymały werdykt BIERZEMY.
        """
        if not offers:
            return []

        # 1. Deterministyczny twardy filtr Red Ocean / Pułapek / Miejsca wykonania (z centralnego config.py)
        candidate_offers: List[Dict[str, Any]] = []
        for o in offers:
            desc = (
                o.get("full_description")
                or o.get("description")
                or o.get("short_desc")
                or o.get("description_short")
                or ""
            )
            miejsce_wyk = (
                o.get("miejsce_wykonania")
                or (o.get("full_details") or {}).get("miejsce_wykonania")
                or ""
            )
            hr = config.is_hard_reject(str(o.get("title", "")), str(desc), str(miejsce_wyk))
            if hr:
                print(f"[HARD-REJECT] Zlecenie #{o.get('id')} ({o.get('title')}) odrzucone deterministycznie przed AI #1 (wzorzec: {hr}).", flush=True)
                o["rejection_reason"] = f"Deterministyczny filtr: {hr}"
                continue
            candidate_offers.append(o)

        if not candidate_offers:
            return []

        if not self._call_deepseek or not self._parse_json:
            print("[WARN] Brak chain_executor.py - zwracam zlecenia po filtrze deterministycznym")
            return [o for o in candidate_offers if o.get("id")]

        prompt_file = PROMPTS_DIR / "generatory" / "prompt_ai1.md"
        selekcja_file = PROMPTS_DIR / "kontekst" / "selekcja_zlecen.md"
        stack_file = PROMPTS_DIR / "kontekst" / "stack_i_filozofia.md"

        system_parts = []
        if prompt_file.exists():
            system_parts.append(prompt_file.read_text(encoding="utf-8-sig"))

        user_parts = []
        if selekcja_file.exists():
            user_parts.append("--- KRYTERIA SELEKCJI ---\n" + selekcja_file.read_text(encoding="utf-8-sig"))
        if stack_file.exists():
            user_parts.append("--- STACK I FILOZOFIA ---\n" + stack_file.read_text(encoding="utf-8-sig"))

        # Zestawienie zleceń do oceny (z pełnym opisem i miejscem wykonania)
        zlecenia_do_analizy = []
        for o in candidate_offers:
            desc = (
                o.get("full_description")
                or o.get("description")
                or o.get("short_desc")
                or o.get("description_short")
                or ""
            )
            miejsce_wyk = (
                o.get("miejsce_wykonania")
                or (o.get("full_details") or {}).get("miejsce_wykonania")
                or ""
            )
            item_payload = {
                "id": str(o.get("id", "")),
                "title": o.get("title", ""),
                "budget": o.get("budget", ""),
                "category": o.get("category", ""),
                "description": desc[:4000]
            }
            if miejsce_wyk:
                item_payload["miejsce_wykonania"] = miejsce_wyk
            zlecenia_do_analizy.append(item_payload)

        user_parts.append("--- NOWE ZLECENIA DO OCENY ---\n" + json.dumps(zlecenia_do_analizy, ensure_ascii=False, indent=2))

        system_prompt = "\n\n".join(system_parts)
        user_prompt = "\n\n".join(user_parts)

        # Szybki model bez myślenia CoT (nothink) dla błyskawicznej selekcji
        odpowiedz = self._call_deepseek(
            system_prompt,
            user_prompt,
            model="deepseek-v4-pro-nothink",
            timeout=90,
            max_tokens=2000
        )

        if not odpowiedz:
            print("[WARN] Selekcjoner AI timeout lub brak odpowiedzi – fallback: przepuszczam zlecenia po twardym filtrze config.is_hard_reject")
            return [o for o in candidate_offers if o.get("id")]

        parsed = self._parse_json(odpowiedz)

        if isinstance(parsed, dict) and not isinstance(parsed, list):
            for k in ("zlecenia", "oferty", "results", "items"):
                if isinstance(parsed.get(k), list):
                    parsed = parsed[k]
                    break

        wybrane_id = set()
        powody: Dict[str, str] = {}
        tiery: Dict[str, str] = {}
        sciezki: Dict[str, str] = {}
        typy_klientow: Dict[str, str] = {}
        karty_tech: Dict[str, str] = {}
        modyfikatory_map: Dict[str, List[str]] = {}
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    jid = str(item.get("id", "")).strip()
                    werdykt = str(item.get("werdykt") or item.get("decyzja") or "").upper().strip()
                    powod = str(item.get("powod", "")).strip()
                    tier_raw = str(item.get("tier", "TIER_B")).upper().strip()
                    sciezka_raw = str(item.get("sciezka", "inzynieria")).lower().strip()
                    sciezka = "biznes" if "biznes" in sciezka_raw else "inzynieria"
                    typ_klienta = str(item.get("typ_klienta", "")).lower().strip()
                    karta_tech = str(item.get("karta_tech", "")).lower().strip()
                    if typ_klienta == "tech_agnostic" or sciezka == "biznes":
                        sciezka = "biznes"
                        karta_tech = "tech_16"
                    mods_raw = item.get("modyfikatory") or []
                    if isinstance(mods_raw, str):
                        mods_raw = [mods_raw]
                    valid_mods = {"RESCUE", "DELEGOWANY", "PHANTOM"}
                    mods = [str(m).upper().strip() for m in mods_raw if m and str(m).upper().strip() in valid_mods]
                    # Profil flagowy (ekspert_dziedzinowy) zawsze otrzymuje priorytet Tier A
                    tier = "A" if ("TIER_A" in tier_raw or tier_raw == "A" or typ_klienta == "ekspert_dziedzinowy") else "B"
                    powody[jid] = powod
                    if werdykt in ("BIERZEMY", "TAK", "YES", "EDGE CASE", "EDGE_CASE") or "BIERZEMY" in werdykt or "EDGE" in werdykt:
                        wybrane_id.add(jid)
                        tiery[jid] = tier
                        sciezki[jid] = sciezka
                        typy_klientow[jid] = typ_klienta
                        karty_tech[jid] = karta_tech
                        modyfikatory_map[jid] = mods
        else:
            for match in re.finditer(r'"id"\s*:\s*"(\d+)".*?"werdykt"\s*:\s*"(BIERZEMY|EDGE CASE|EDGE_CASE)"', odpowiedz, re.DOTALL | re.IGNORECASE):
                wybrane_id.add(match.group(1))

        zakwalifikowane = []
        for o in candidate_offers:
            oid = str(o.get("id", "")).strip()
            if oid in wybrane_id:
                o["selection_reason"] = powody.get(oid, "Wybrane przez Selekcjonera AI")
                o["tier"] = tiery.get(oid, "B")
                o["sciezka"] = sciezki.get(oid, "inzynieria")
                o["typ_klienta"] = typy_klientow.get(oid, "")
                if karty_tech.get(oid):
                    o["karta_tech"] = karty_tech[oid]
                o["modyfikatory"] = modyfikatory_map.get(oid, [])
                zakwalifikowane.append(o)
            else:
                o["rejection_reason"] = powody.get(oid, "Odrzucona przez Selekcjonera AI #1")

        # Sortowanie: Tier A (nisze wysokomarżowe i ekspert dziedzinowy) ma bezwzględny priorytet przed Tier B
        zakwalifikowane.sort(key=lambda x: 0 if x.get("tier") == "A" else 1)

        summary_items = [
            (o.get("id"), f"Tier {o.get('tier')}", o.get("sciezka"), o.get("typ_klienta"), o.get("karta_tech"), o.get("modyfikatory"))
            for o in zakwalifikowane
        ]
        print(f"[SELEKCJA AI] Z {len(offers)} ofert zakwalifikowano {len(zakwalifikowane)}: {summary_items}")
        return zakwalifikowane

    def generate_proposal(self, job_detail: Dict[str, Any]) -> ProposalResult:
        if not self._run_chain:
            raise RuntimeError("Nie znaleziono chain_executor.py!")

        job_id = str(job_detail.get("id", "brak_id"))
        previous_offers = job_detail.get("previous_offers") or []

        wynik = self._run_chain(
            f"useme-job-{job_id}",
            job_detail,
            parent_id="useme-bot",
            parent_step=f"Generowanie wyceny i oferty #{job_id}",
        )
        if not wynik:
            raise RuntimeError(f"Łańcuch AI zwrócił błąd/abort dla zlecenia {job_id}")

        opis = str(wynik.get("opis", "")).strip()

        # TWARDY BEZPIECZNIK ANTY-POWTÓRKI: jeśli klient dostał już oferty, a nowa
        # jest zbyt podobna do którejkolwiek z nich, wymuszamy przepisanie innym tonem.
        if previous_offers and opis:
            proby = 0
            while proby < MAX_ANTY_POWTORKA_RETRY:
                poprzednie = [(p.get("opis") or "") for p in previous_offers if p.get("opis")]
                if not poprzednie:
                    break
                max_pod = max(_podobienstwo_jaccard(opis, stary) for stary in poprzednie)
                if max_pod <= PROG_PODOBNOSCI:
                    print(f"[ANTY-POWTÓRKA] Oferta #{job_id} OK (maks. podobieństwo {max_pod:.0%}).")
                    break
                proby += 1
                print(f"[ANTY-POWTÓRKA] Oferta #{job_id} zbyt podobna ({max_pod:.0%}) – przepisuję (próba {proby}).")
                # Wymuszamy inny ton i ponawiamy cały łańcuch z nowym ziarnem wariacji.
                retry_ctx = dict(job_detail)
                retry_ctx["variation_seed"] = (int(job_detail.get("variation_seed", 0)) + proby) % 5
                retry_ctx["wymus_inny_styl"] = (
                    "Poprzednia wersja była zbyt podobna do wcześniejszej oferty dla tego klienta. "
                    "Napisz od zera, innym tonem, inną strukturą i innymi argumentami."
                )
                wynik_retry = self._run_chain(
                    f"useme-job-{job_id}-retry{proby}",
                    retry_ctx,
                    parent_id="useme-bot",
                    parent_step=f"Przepisanie oferty #{job_id} (anty-powtórka {proby})",
                )
                if wynik_retry:
                    nowy_opis = str(wynik_retry.get("opis", "")).strip()
                    if nowy_opis:
                        opis = nowy_opis
                        wynik = wynik_retry
            else:
                print(f"[ANTY-POWTÓRKA] Oferta #{job_id}: wyczerpano próby, zostawiam ostatnią wersję.")
        wycena_raw = wynik.get("wycena_dni", {})

        # Parsowanie wyceny i dni. Model zwraca tekst/markdown (nie dict), więc
        # szukamy twardego bloku [WYNIK_KONCOWY] KWOTA: X DNI: Y (zapas: dict).
        kwota, dni = _parse_wycena_dni(wycena_raw)

        # Deterministyczna sanitacja dni, pauz i widełek
        sanitize_fn = getattr(self, "_sanitize_opis", None)
        if sanitize_fn and opis:
            opis = sanitize_fn(opis, wycena=kwota, dni=dni)
            wynik["opis"] = opis

        # PRODUKCYJNY AUDYTOR RED-TEAM 1-100 (jeśli aktywny w config.py i działamy na pełnym łańcuchu)
        audit_fn = getattr(self, "_audit_100", None)
        is_real_chain = getattr(self._run_chain, "__name__", "") == "run_chain"
        if (
            audit_fn
            and getattr(config, "USE_AUDYTOR_100", True)
            and (is_real_chain or job_detail.get("force_audyt_100"))
        ):
            target_score = int(getattr(config, "AUDYTOR_100_TARGET_SCORE", 92))
            max_rounds = int(getattr(config, "AUDYTOR_100_MAX_ROUNDS", 2))
            audyt_res = audit_fn(
                job_detail,
                opis,
                kwota,
                dni,
                wycena_raw=str(wycena_raw or ""),
                research_text=str(wynik.get("research", "")),
                target_score=target_score,
                max_rounds=max_rounds,
            )
            opis = audyt_res["opis"]
            kwota = audyt_res["wycena"]
            dni = audyt_res["dni"]
            wynik["opis"] = opis
            wynik["wycena_dni"] = audyt_res["wycena_raw"]
            wynik["audyt_100"] = audyt_res["audyt_final"]
            print(
                f"[AUDYTOR-100] Oferta #{job_id}: wynik {audyt_res['wynik_100']}/100 pkt "
                f"(rundy: {audyt_res['rounds']})",
                flush=True,
            )

        # TWARDY WALIDATOR KWOTY: sprawdza, czy kwota wpisana w tresci oferty
        # zgadza sie z kwota z bloku [WYNIK_KONCOWY] (kalkulator). Model czasem
        # "poprawia" cene po swojemu - to ma to wychwycic.
        kwota_zgodna, kwoty_w_tresci = _waliduj_kwote_w_tresci(opis, kwota)
        if not kwota_zgodna:
            print(f"[KWOTA-WALIDATOR] Oferta #{job_id}: kwota w tresci NIE zgadza sie z wycena "
                  f"({kwota} zl). Znalezione w tresci: {kwoty_w_tresci}", flush=True)

        # Flagi z kalkulatora (sanity-check wyceny).
        sanity_ok = wynik.get("sanity_ok", True)
        if not sanity_ok:
            print(f"[SANITY] Oferta #{job_id}: kalkulator oznaczył wycenę jako podejrzanie niską!", flush=True)

        if not isinstance(wynik.get("metadata"), dict):
            wynik["metadata"] = {}
        wynik["metadata"].update({
            "kwota_zgodna": kwota_zgodna,
            "kwoty_w_tresci": kwoty_w_tresci,
            "sanity_ok": sanity_ok,
        })

        return ProposalResult(
            opis=opis,
            wycena=kwota,
            dni=dni,
            powod_wyboru="Zaakceptowano przez walidatory slotowe",
            metadata=wynik
        )


def _wyciagnij_kwoty_z_tekstu(tekst: str) -> list:
    """Wyciaga wszystkie kwoty (>= 3 cyfry) z dowolnego tekstu.

    Toleruje: '17000', '17 000', '17 000 zl', '17,000 PLN', '56000 zł'.
    Ignoruje grosze i pojedyncze/dwucyfrowe liczby (np. dni, procenty).
    """
    wyniki = []
    for m in re.finditer(r"\d[\d\s.,]{2,}\d", tekst or ""):
        raw = m.group(0).replace(" ", "").replace("\xa0", "")
        raw = re.sub(r"[,.]\d{2}$", "", raw)  # usun grosze na koncu
        cyfry = re.sub(r"[^\d]", "", raw)
        if cyfry and len(cyfry) >= 3:
            val = int(cyfry)
            # Ignoruj lata kalendarzowe (np. 2024, 2025, 2026), to nie są kwoty
            if val in (2024, 2025, 2026, 2027, 2028, 2029):
                continue
            wyniki.append(val)
    return wyniki


def _waliduj_kwote_w_tresci(opis: str, kwota: int) -> tuple:
    """Sprawdza, czy kwota z kalkulatora pojawia sie w tresci oferty.

    Zwraca (zgodna: bool, znalezione_kwoty: list).
    Zgodna = kwota z kalkulatora jest w tresci (lub tresc nie ma zadnej kwoty).
    """
    if not opis or kwota <= 0:
        return True, []
    znalezione = _wyciagnij_kwoty_z_tekstu(opis)
    if not znalezione:
        # Tresc bez kwot - nie ma czego walidowac (np. oferta-retainer opisowa).
        return True, []
    return (kwota in znalezione), znalezione


def _parse_wycena_dni(wycena_raw: Any) -> tuple[int, int]:
    """Wyciąga kwotę i dni z outputu generatora wyceny.

    Kolejność bezpieczników:
    1. Jeśli model zwrócił dict (stary format) — czytamy klucze kwota/cena i dni.
    2. W przeciwnym razie szukamy twardego bloku: KWOTA: <n> oraz DNI: <n>.
    3. Brak rozpoznanej kwoty lub dni -> rzucamy błąd zamiast cichego fallbacku.
    """
    if isinstance(wycena_raw, dict):
        kwota = int(wycena_raw.get("kwota", wycena_raw.get("cena", 0)))
        dni = int(wycena_raw.get("dni", 0))
        return _waliduj(kwota, dni)

    tekst = str(wycena_raw or "")

    m_kwota = re.search(r"KWOTA\s*[:=]\s*([^\r\n]+)", tekst, re.IGNORECASE)
    m_dni = re.search(r"DNI\s*[:=]\s*(\d+)", tekst, re.IGNORECASE)

    kwota = _wyciagnij_kwote(m_kwota.group(1)) if m_kwota else 0
    dni = int(m_dni.group(1)) if m_dni else 0

    return _waliduj(kwota, dni)


def _wyciagnij_kwote(raw: str) -> int:
    """Pancernie czyści wartość kwoty: toleruje spacje, kropki, przecinki,
    grosze oraz dopiski zł/PLN. Np. '10 000 zł', '5.500 PLN', '6000,00 zł'."""
    # zostaw tylko cyfry, przecinki i kropki (wyrzuć 'zł', 'PLN', spacje)
    raw = re.sub(r"[^\d,.]", "", raw)
    # usuń grosze na końcu: '6000,00' -> '6000' (nie rusza '5.500' bo to 3 cyfry)
    raw = re.sub(r"[,.]\d{2}$", "", raw)
    cyfry = re.sub(r"[^\d]", "", raw)
    return int(cyfry) if cyfry else 0


def _waliduj(kwota: int, dni: int) -> tuple[int, int]:
    """Twarde minimum biznesowe: 500 zł i 7 dni. Brak wartości -> błąd."""
    if not kwota or not dni:
        raise ValueError(
            "Nie udało się wyciągnąć kwoty lub dni z outputu generatora wyceny. "
            "Sprawdź, czy prompt agent_02b zwraca blok [WYNIK_KONCOWY] z KWOTA i DNI."
        )
    kwota = max(500, kwota)
    dni = max(7, dni)
    return kwota, dni


def get_ai_pipeline() -> BaseAIPipeline:
    """Fabryka zwracająca aktywny pipeline AI na podstawie flagi w config.py."""
    if USE_MOCK_AI:
        return MockAIPipeline()
    return SlotChainAIPipeline()
