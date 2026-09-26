import json
import shutil
import pathlib

repo = pathlib.Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
brain = pathlib.Path(r"C:\Users\Ksawier\.gemini\antigravity\brain\27ae8295-368e-43dc-98d7-6dbdc79d7ca2")
target_dir = repo / "badania" / "audyt_100"
logs_dir = target_dir / "logi_i_skrypty"
target_dir.mkdir(parents=True, exist_ok=True)
logs_dir.mkdir(parents=True, exist_ok=True)

# 1. Copy JSON results
json_src = brain / "scratch" / "audyt_100_wyniki.json"
json_dst = target_dir / "audyt_100_wyniki_27_ofert.json"
shutil.copy2(json_src, json_dst)

# 2. Copy all scratch scripts
for p in (brain / "scratch").glob("*.py"):
    shutil.copy2(p, logs_dir / p.name)

# 3. Copy all task logs
tasks_dir = brain / ".system_generated" / "tasks"
if tasks_dir.exists():
    for p in tasks_dir.glob("*.log"):
        shutil.copy2(p, logs_dir / p.name)

# 4. Copy all 4 artifacts into badania/audyt_100/artefakty_sesji/
art_dir = target_dir / "artefakty_sesji"
art_dir.mkdir(parents=True, exist_ok=True)
for name in ["analiza_bota.md", "strategia_vs_bot.md", "plan_wdrozenia.md", "porownanie_ofert_live_z_elita.md"]:
    src = brain / name
    if src.exists():
        shutil.copy2(src, art_dir / name)

# 5. Generate full human-readable markdown dump of all 27 offers (R1 + R2 + Judge logs)
data = json.loads(json_src.read_text(encoding="utf-8"))
lines = [
    "# Pełne Archiwum Logów i Ocen 27 Ofert (Runda 1 + Runda 2 + Reasoning Sędziego 1-100)",
    "",
    f"Łącznie przetestowanych zleceń z magazynu: **{len(data)}**",
    "",
]
for idx, (jid, rec) in enumerate(data.items(), 1):
    lines.append(f"## {idx}. Zlecenie #{jid}: {rec.get('title', '')}")
    lines.append(
        f"- **Ścieżka:** `{rec.get('sciezka')}` | **Typ klienta:** `{rec.get('typ_klienta')}` "
        f"| **Karta Wiedzy:** `{rec.get('karta_tech')}` | **Modyfikatory:** `{rec.get('modyfikatory')}`"
    )
    lines.append(
        f"- **Wynik Końcowy:** **`{rec.get('final_score')}/100 pkt`** "
        f"| **Wycena Końcowa:** `{rec.get('final_wycena')} zł / {rec.get('final_dni')} dni`"
    )
    lines.append("")
    for r_key, r_label in [
        ("runda_1", "Runda 1 (Zero-Shot)"),
        ("runda_2", "Runda 2 (Po Pętli Naprawczej)"),
        ("runda_3", "Runda 3 (Dogrywka)"),
    ]:
        r = rec.get(r_key)
        if not r:
            continue
        aud = r.get("audyt") or {}
        lines.append(
            f"### {r_label} — Wynik: `{aud.get('wynik_100')}/100 pkt` "
            f"(`{r.get('wycena')} zł / {r.get('dni')} dni`, `{r.get('words')} słów`)"
        )
        lines.append(f"- **Kategorie:** `{json.dumps(aud.get('kategorie', {}), ensure_ascii=False)}`")
        lines.append("```text")
        lines.append(str(r.get("opis", "")).strip())
        lines.append("```")
        lines.append("**Za co dodano punkty (`+pkt`):**")
        for p in aud.get("za_co_dodano", []):
            lines.append(f"- **[+] `{p.get('punkty')}`:** {p.get('uzasadnienie')}")
        lines.append("")
        lines.append("**Za co odjęto punkty (`-pkt`):**")
        for m in aud.get("za_co_odjeto", []):
            lines.append(f"- **[-] `{m.get('punkty')}`:** *„{m.get('cytat')}”* -> {m.get('uzasadnienie')}")
        lines.append("")
    lines.append("---")
    lines.append("")

dump_path = target_dir / "PELNE_LOGI_27_OFERT_RUNDA1_I_RUNDA2.md"
dump_path.write_text("\n".join(lines), encoding="utf-8")
print("Saved:", json_dst, dump_path, "Logs count:", len(list(logs_dir.iterdir())))
