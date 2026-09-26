# -*- coding: utf-8 -*-
"""
Pobieracz i analityk prywatnych wiadomości zleceniodawcy z Useme.
Pobiera pełne treści wszystkich wiadomości z wątków i koreluje je z ofertami na zleceniu #144890.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from pobierz_oferty_zleceniodawcy import create_session

base_dir = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
data_dir = base_dir / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"
offers_file = data_dir / "oferty_publiczne_30.json"

session = create_session()
session.headers.update({
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://useme.com/pl/mesg/"
})

# 1. Pobierz listę wątków
r_list = session.get("https://useme.com/pl/mesg/mesgs/", allow_redirects=False)
if r_list.status_code in (301, 302) or "/users/login" in r_list.headers.get("Location", ""):
    print("[AUTH BŁĄD] Sesja w tech/cookies_zleceniodawca.json wygasła! Uruchom: python login_useme.py zleceniodawca")
    raise SystemExit(1)
try:
    threads_resp = r_list.json()
except Exception:
    print("[AUTH BŁĄD] Nieprawidłowa odpowiedź JSON (prawdopodobnie wygasła sesja). Przerywam bez nadpisywania plików.")
    raise SystemExit(1)
thread_list = threads_resp.get("results", [])

print(f"Znaleziono {len(thread_list)} wątków wiadomości.")
if not thread_list:
    print("[STOP] Brak wątków do zapisania – nie nadpisuję istniejących plików.")
    raise SystemExit(0)

# 2. Wczytaj istniejące 30 ofert ze zlecenia #144890
offers = []
if offers_file.exists():
    offers = json.loads(offers_file.read_text(encoding="utf-8"))

print(f"Wczytano {len(offers)} ofert ze zlecenia #144890.")

# Indeksy ofert po nazwisku i author_url
offers_by_author = {}
for off in offers:
    aname = off.get("author_name", "").strip().lower()
    aurl = off.get("author_profile_url", "")
    offers_by_author[aname] = off
    # wyciągnij slug z url np. /pl/roles/contractor/ailone/
    slug = aurl.strip("/").split("/")[-1].lower() if aurl else ""
    if slug:
        offers_by_author[slug] = off

# 3. Pobierz pełne wiadomości z każdego wątku
detailed_threads = []

for item in thread_list:
    pk = item.get("pk")
    u_info = item.get("user_to_display", {})
    author_name = u_info.get("name", "Nieznany")
    author_pk = str(u_info.get("pk", ""))
    subject = item.get("subject", "")
    
    # Endpoint do pobrania pełnej treści wiadomości w wątku
    thread_api_url = f"https://useme.com/pl/mesg/mesgs/{pk}/thread"
    r_thread = session.get(thread_api_url)
    
    messages = []
    if r_thread.status_code == 200:
        t_data = r_thread.json()
        for msg in t_data.get("results", []):
            raw_html = msg.get("content", "")
            # Czyścimy HTML do czystego tekstu
            soup = BeautifulSoup(raw_html, "html.parser")
            clean_text = soup.get_text("\n", strip=True)
            
            created_at = msg.get("created_at") or msg.get("date_created") or msg.get("sent_date")
            sender = msg.get("user_sender", {})
            sender_name = sender.get("name") if isinstance(sender, dict) else str(sender)
            
            messages.append({
                "message_pk": msg.get("pk"),
                "sender_id": sender.get("pk") if isinstance(sender, dict) else None,
                "sender_name": sender_name,
                "text": clean_text,
                "raw_html": raw_html,
                "date": created_at
            })
            
    # Sprawdźmy korelację z ofertami: czy ten użytkownik złożył oficjalną ofertę pod zleceniem #144890?
    matched_offer = None
    # 1. Po nazwisku
    norm_name = author_name.lower().strip()
    for off in offers:
        off_author = off.get("author_name", "").lower().strip()
        if norm_name in off_author or off_author in norm_name:
            matched_offer = off
            break
        # Sprawdź też częściowe dopasowanie (np. Adam K vs Adam Kowalski)
        parts_a = norm_name.split()
        parts_b = off_author.split()
        if len(parts_a) > 0 and len(parts_b) > 0:
            if parts_a[0] == parts_b[0]:
                if len(parts_a) > 1 and len(parts_b) > 1 and (parts_a[1][0] == parts_b[1][0]):
                    matched_offer = off
                    break

    detailed_threads.append({
        "thread_pk": pk,
        "author_name": author_name,
        "author_user_id": author_pk,
        "subject": subject,
        "thread_size": item.get("thread_size"),
        "has_submitted_offer": matched_offer is not None,
        "matched_offer_id": matched_offer.get("offer_id") if matched_offer else None,
        "matched_offer_price": matched_offer.get("price") if matched_offer else None,
        "matched_offer_days": matched_offer.get("days") if matched_offer else None,
        "messages": messages
    })

# Zapis do JSON
output_json = data_dir / "wiadomosci_zleceniodawcy_pelne.json"
output_json.write_text(json.dumps(detailed_threads, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Zapisano pełne wiadomości do: {output_json}")

# Generowanie raportu w Markdown
report_md = data_dir / "raport_wiadomosci_prywatnych_zleceniodawcy.md"
with open(report_md, "w", encoding="utf-8") as f:
    f.write("# RAPORT PRYWATNYCH WIADOMOŚCI OD WYKONAWCÓW (USEME #144890)\n\n")
    f.write(f"> Pobrane wątki ze skrzynki zleceniodawcy: {len(detailed_threads)}\n")
    f.write("> Stan na: 2026-09-23\n\n")
    f.write("="*80 + "\n\n")
    
    for t in detailed_threads:
        f.write(f"## Rozmówca: **{t['author_name']}** (User ID: `{t['author_user_id']}`)\n")
        f.write(f"- **Temat:** {t['subject']}\n")
        f.write(f"- **Wątek ID:** `{t['thread_pk']}`\n")
        if t['has_submitted_offer']:
            f.write(f"- **STATUS OFERTY:** ✅ **ZŁOŻYŁ OFERTĘ PUBLICZNĄ** (#{t['matched_offer_id']}, Cena: **{t['matched_offer_price']}**, Czas: {t['matched_offer_days']})\n")
        else:
            f.write(f"- **STATUS OFERTY:** ❌ **BRAK OFERTY PUBLICZNEJ** (pisze TYLKO na priv bez składania oferty!)\n")
        
        f.write("\n### Treść wiadomości w wątku:\n\n")
        for m in t["messages"]:
            f.write(f"> **Nadawca:** {m.get('sender_name') or t['author_name']} | **Data:** {m.get('date')}\n\n")
            f.write(m["text"])
            f.write("\n\n---\n\n")
        f.write("\n" + "="*80 + "\n\n")

print(f"Zapisano raport Markdown do: {report_md}")
