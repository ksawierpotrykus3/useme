# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_strony_ofert.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

off = soup.select_one('.dashboard-list__item-offer')
read_more = off.select_one('[data-module="read-more"]')
if read_more:
    parent = read_more.parent
    print("Parent tag:", parent.name, parent.get('class'))
    # Sprawdźmy rodzeństwo lub dzieci
    for child in parent.children:
        if child.name:
            print(f"Child: <{child.name}> class='{child.get('class')}' len={len(child.get_text())}")
            
    # Zobaczmy czy cały tekst oferty jest w parent
    full_text = parent.get_text(separator="\n", strip=True)
    print("Długość całego tekstu w bloku opisu:", len(full_text))
    with open('badania/baza/ksawierpotrykus3/_paczki_i_probki/probka_oferta_1.txt', 'w', encoding='utf-8') as out:
        out.write(full_text)
    print("Zapisano probka_oferta_1.txt!")
