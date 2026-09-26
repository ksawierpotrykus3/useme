import json
import pathlib
import sys
import statistics

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = pathlib.Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
sys.path.insert(0, str(REPO / "kod"))

from chain_executor import call_deepseek, DEEPSEEK_MODEL  # noqa: E402


def build_statistical_digest(data: dict) -> str:
    r1_scores = []
    final_scores = []
    deltas = []
    by_sciezka = {"inzynieria": [], "biznes": []}
    by_typ = {}
    r1_deductions = []
    final_deductions = []
    degradations = []

    for jid, rec in data.items():
        r1 = rec.get("runda_1", {})
        r1_aud = r1.get("audyt", {})
        s1 = int(r1_aud.get("wynik_100", 0))
        sf = int(rec.get("final_score", s1))
        r1_scores.append(s1)
        final_scores.append(sf)
        deltas.append(sf - s1)

        sc = rec.get("sciezka", "inzynieria")
        by_sciezka.setdefault(sc, []).append((s1, sf))
        tk = rec.get("typ_klienta", "unknown")
        by_typ.setdefault(tk, []).append((jid, s1, sf, rec.get("final_wycena"), r1.get("words")))

        r2 = rec.get("runda_2")
        if r2:
            s2 = int((r2.get("audyt") or {}).get("wynik_100", 0))
            if s2 < s1:
                degradations.append((jid, rec.get("title"), s1, s2))

        for m in r1_aud.get("za_co_odjeto", []):
            r1_deductions.append(f"#{jid} (R1={s1}): {m.get('punkty')} | {m.get('uzasadnienie')[:160]}")

        # Find final round audit
        f_aud = r1_aud
        if rec.get("runda_3") and int((rec["runda_3"].get("audyt") or {}).get("wynik_100", 0)) == sf:
            f_aud = rec["runda_3"]["audyt"]
        elif r2 and int((r2.get("audyt") or {}).get("wynik_100", 0)) == sf:
            f_aud = r2["audyt"]
        for m in f_aud.get("za_co_odjeto", []):
            final_deductions.append(f"#{jid} (Final={sf}): {m.get('punkty')} | {m.get('uzasadnienie')[:160]}")

    lines = [
        f"Liczba przetestowanych zleceń z magazynu: {len(data)}",
        f"Runda 1 (Zero-Shot) — Średnia: {statistics.mean(r1_scores):.2f}/100 | Mediana: {statistics.median(r1_scores):.1f} | Min: {min(r1_scores)} | Max: {max(r1_scores)}",
        f"Wynik Finalny — Średnia: {statistics.mean(final_scores):.2f}/100 | Mediana: {statistics.median(final_scores):.1f} | Min: {min(final_scores)} | Max: {max(final_scores)}",
        f"Średni przyrost po pętli naprawczej: +{statistics.mean(deltas):.2f} pkt",
        f"Przypadki, gdzie Runda 2 pogorszyła wynik Rundy 1 (uratowane przez bezpiecznik max(R1,R2)): {degradations}",
        "\nWyniki wg typu klienta (jid, R1, Final, wycena, słowa R1):",
    ]
    for tk, items in sorted(by_typ.items()):
        avg_r1 = sum(x[1] for x in items) / len(items)
        avg_f = sum(x[2] for x in items) / len(items)
        lines.append(f"  - {tk} (n={len(items)}): śr. R1={avg_r1:.1f}, śr. Final={avg_f:.1f} -> {items}")

    lines.append("\nPróbka najczęstszych odjęć punktów w Rundzie 1 (Zero-Shot):")
    lines.extend("  * " + d for d in r1_deductions[:35])

    lines.append("\nPozostałe odjęcia punktów w wersjach Finalnych (dlaczego nie 100/100 w każdym przypadku):")
    lines.extend("  * " + d for d in final_deductions[:35])
    return "\n".join(lines)


def main():
    changelog = (REPO / "badania" / "audyt_100" / "CHANGELOG_OD_POCZATKU_ROZMOWY.md").read_text(encoding="utf-8")
    data = json.loads((REPO / "badania" / "audyt_100" / "audyt_100_wyniki_27_ofert.json").read_text(encoding="utf-8"))
    stats_digest = build_statistical_digest(data)

    agent_02a = (REPO / "kod" / "prompts" / "generatory" / "agent_02a_opis_oferty.md").read_text(encoding="utf-8")
    portfolio = (REPO / "kod" / "prompts" / "kontekst" / "portfolio_baza.md").read_text(encoding="utf-8")
    chain_cfg = (REPO / "kod" / "prompts" / "chain_config.json").read_text(encoding="utf-8")
    kalkulator = (REPO / "kod" / "wycena_kalkulator.py").read_text(encoding="utf-8")[:4500]
    audytor = (REPO / "kod" / "audytor_lancuch.py").read_text(encoding="utf-8")[:5500]

    system_prompt = """Jesteś Niezależnym Głównym Architektem Systemów AI i Bezlitosnym Audytorem Red-Team (Meta-Krytykiem).
Twoim zadaniem jest krytyczna, głęboka, w 100% transparentna ocena WSZYSTKICH ZMIAN wprowadzonych w ofertowarce (`useme_core`) oraz WSZYSTKICH DANYCH zebranych podczas 5 fal testowych (27 zleceń z magazynu).

NIE BĄDŹ POTAKIWACZEM. Szukaj zarówno realnych przełomów inżynierskich/psychologicznych, jak i:
1. Dziur architektonicznych i miejsc, gdzie nowe moduły nie są jeszcze wpięte w produkcyjny potok (`chain_config.json`, `chain_executor.py`, `engine.py`, `priv_engine.py`).
2. Ryzyka przeuczenia (overfittingu) promptów `agent_02a` i `portfolio_baza.md` pod konkretne 27 zleceń lub pod gusta Sędziego LLM.
3. Słabych punktów w wycenie (`wycena_kalkulator.py`, `90 zł/h`, mnożnik `1.15`), szczególnie na skrajnych zleceniach (bardzo małe quick-fixy vs wielomodułowe systemy ERP/RMA).
4. Ryzyka związanego z wiarygodnością dowodów w `portfolio_baza.md` (kiedy klient na priv poprosi o szczegóły lub link/screen do Projektu 8 / Projektu 9).
5. Analizy danych z 27 prób: co dokładnie dały nam te próby, gdzie Runda 1 (Zero-Shot) wciąż traci punkty (średnia R1 vs średnia Final), dlaczego w niektórych przypadkach Runda 2 pogorszyła wynik Rundy 1 (np. #2643264 92->88) i jak temu zapobiec systemowo.

Struktura Twojego raportu (w języku polskim, maksymalnie konkretna, z cytatami z kodu/danych i punktacją):
1. **WERDYKT META-AUDYTORA (Ocena Całości Reformy: X / 100 pkt z rozbiciem na 5 obszarów po 20 pkt)**
   - Architektura i Kod Produkcyjny (0-20 pkt)
   - Prompt Engineering i Odporność na Overfitting (0-20 pkt)
   - Psychologia B2B, Portfolio i Wiarygodność (0-20 pkt)
   - Matematyka Wycen i Realizm Rynkowy (0-20 pkt)
   - Jakość Zebranych Danych i Metodologia 5 Fal Testowych (0-20 pkt)
2. **ZA CO DODANO PUNKTY (`[+]` Twarde dowody z kodu i z 27 prób — co faktycznie zmieniło klasę bota)**
3. **ZA CO ODJĘTO PUNKTY (`[-]` Bezlitosna lista luk, ryzyk produkcyjnych, długu technicznego i słabości danych)** — przy każdym punkcie podaj dokładną liczbę odjętych punktów (`-X pkt`), lokalizację w kodzie/prompcie/danych i wyjaśnienie dlaczego to groźne.
4. **CO NAPRAWDĘ MÓWIĄ DANE Z 27 PRÓB (Głęboka analiza statystyczna Runda 1 vs Runda 2)** — gdzie system jest już autonomiczny (Zero-Shot 92-97/100), a gdzie wciąż wymaga koła ratunkowego Rundy 2.
5. **PLAN DOMKNIĘCIA DO 100/100 W PRODUKCJI (5 konkretnych kroków inżynierskich do wdrożenia od zaraz)**."""

    user_prompt = (
        "=== 1. CHANGELOG WSZYSTKICH ZMIAN OD POCZĄTKU SESJI ===\n"
        + changelog
        + "\n\n=== 2. TWARDA STATYSTYKA I DANE Z 27 PRZETESTOWANYCH OFERT (FALE 1-5) ===\n"
        + stats_digest
        + "\n\n=== 3. AKTUALNY CHAIN_CONFIG.JSON ===\n"
        + chain_cfg
        + "\n\n=== 4. AKTUALNY PROMPT GENERATORA (agent_02a_opis_oferty.md) ===\n"
        + agent_02a
        + "\n\n=== 5. AKTUALNA BAZA PORTFOLIO (portfolio_baza.md) ===\n"
        + portfolio
        + "\n\n=== 6. FRAGMENT KODU KALKULATORA (wycena_kalkulator.py) I AUDYTORA (audytor_lancuch.py) ===\n"
        + kalkulator
        + "\n---\n"
        + audytor
    )

    print("[META-AUDYT] Uruchamiam głęboki łańcuch krytyczny (DeepSeek Reasoner)...", flush=True)
    resp = call_deepseek(system_prompt, user_prompt, model=DEEPSEEK_MODEL, timeout=300)
    out_file = REPO / "badania" / "audyt_100" / "RAPORT_META_AUDYTU_ZMIAN_I_DANYCH.md"
    out_file.write_text(resp or "BRAK ODPOWIEDZI", encoding="utf-8")
    print(f"[META-AUDYT] Zapisano raport do: {out_file} ({len(resp or '')} znaków)", flush=True)
    print("\n" + "=" * 70 + "\n")
    print(resp)


if __name__ == "__main__":
    main()
