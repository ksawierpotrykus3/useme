# -*- coding: utf-8 -*-
import json

with open('badania/baza/ksawierpotrykus3/_paczki_i_probki/wybrane_perelki.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_tekstow.txt', 'w', encoding='utf-8') as f:
    for i, it in enumerate(items):
        f.write(f"=== INDEKS {i}: {it.get('title')} ===\n")
        f.write(f"ID: {it.get('id')} | KATEGORIA: {it.get('category')} | BUDŻET: {it.get('budget')} | KLIENT: {it.get('client')}\n")
        f.write("TREŚĆ:\n")
        f.write(it.get('desc') or "")
        f.write("\n\n" + "="*80 + "\n\n")

print("Zapisano badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_tekstow.txt pomyślnie!")
