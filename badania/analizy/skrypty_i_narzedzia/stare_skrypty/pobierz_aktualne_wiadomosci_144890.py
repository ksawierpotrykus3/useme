# -*- coding: utf-8 -*-
"""Pobieranie aktualnych wątków wiadomości prywatnych ze skrzynki zleceniodawcy Useme."""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pobierz_oferty_zleceniodawcy import create_session

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TARGET_DIR = BASE_DIR / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

offers_file = TARGET_DIR / "oferty_publiczne_30.json"
offers = []
if offers_file.exists():
    try:
        offers = json.loads(offers_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Błąd odczytu ofert: {e}")

session = create_session()
session.headers.update({
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://useme.com/pl/mesg/"
})

r_list = session.get("https://useme.com/pl/mesg/mesgs/")
threads_data = r_list.json()
thread_list = threads_data.get("results", [])

print(f"Pobrano listę {len(thread_list)} wątków.")

detailed_threads = []

for item in thread_list:
    pk = item.get("pk")
    u_info = item.get("user_to_display", {})
    author_name = u_info.get("name", "Nieznany")
    author_pk = str(u_info.get("pk", ""))
    subject = item.get("subject", "")

    thread_api_url = f"https://useme.com/pl/mesg/mesgs/{pk}/thread"
    r_thread = session.get(thread_api_url)

    messages = []
    if r_thread.status_code == 200:
        t_data = r_thread.json()
        for msg in t_data.get("results", []):
            raw_html = msg.get("content", "")
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

    matched_offer = None
    norm_name = author_name.lower().strip()
    for off in offers:
        off_author = (off.get("author_name") or "").lower().strip()
        if norm_name in off_author or off_author in norm_name:
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
    print(f" -> Wątek {pk} ({author_name}): {len(messages)} wiadomości")

# Zapis do JSON
out_json = TARGET_DIR / "wiadomosci_prywatne_pelne.json"
out_json.write_text(json.dumps(detailed_threads, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Zapisano: {out_json}")

# Zapis do Markdown
out_md = TARGET_DIR / "wiadomosci_prywatne.md"
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# RAPORT PRYWATNYCH WIADOMOŚCI OD WYKONAWCÓW (USEME #144890)\n\n")
    f.write(f"> Pobrane wątki ze skrzynki zleceniodawcy: {len(detailed_threads)}\n")
    f.write(f"> Stan na: 2026-09-23\n\n")
    f.write("=" * 80 + "\n\n")

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
        f.write("\n" + "=" * 80 + "\n\n")

print(f"Zapisano raport Markdown do: {out_md}")
