# -*- coding: utf-8 -*-
import json
from pathlib import Path
from bs4 import BeautifulSoup
from pobierz_oferty_zleceniodawcy import create_session

session = create_session()

# Pobierz listę wątków
r_list = session.get('https://useme.com/pl/mesg/mesgs/', headers={'X-Requested-With': 'XMLHttpRequest'})
threads_data = r_list.json()

print(f"Liczba wątków: {len(threads_data.get('results', []))}")

parsed_threads = []

for item in threads_data.get('results', []):
    pk = item.get('pk')
    user_info = item.get('user_to_display', {})
    user_name = user_info.get('name')
    user_pk = user_info.get('pk')
    subject = item.get('subject')
    latest_msg = item.get('latest_message_content')
    
    thread_url = f"https://useme.com/pl/mesg/{pk}/"
    r_thread = session.get(thread_url)
    
    soup = BeautifulSoup(r_thread.text, 'html.parser')
    
    # Szukamy wiadomości w wątku
    # Sprawdźmy wszystkie kontenery wiadomości
    msg_boxes = soup.select('.thread__message, .messages-list__item, .message-bubble, [class*="message"]')
    
    messages = []
    for box in msg_boxes:
        # Pomiń kontenery formularzy lub nagłówków
        if 'form' in ' '.join(box.get('class', [])):
            continue
        text = box.get_text('\n', strip=True)
        if text and len(text) > 10 and text not in messages:
            messages.append(text)
            
    parsed_threads.append({
        "thread_pk": pk,
        "author_name": user_name,
        "author_user_id": user_pk,
        "subject": subject,
        "latest_content": latest_msg,
        "html_messages_found": messages,
        "thread_url": thread_url
    })
    print(f"Pobrano wątek {pk} od {user_name}: znaleziono {len(messages)} bloków tekstu")

out_file = Path(__file__).resolve().parent / ".." / "badania" / "baza" / "weronikabuchholc13" / "04_moje_zlecenia" / "zlecenie_testowe_144890" / "wiadomosci_zleceniodawcy.json"
out_file.write_text(json.dumps(parsed_threads, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Zapisano do: {out_file}")
