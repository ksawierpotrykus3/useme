# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

with open('badania/baza/weronikabuchholc13/04_moje_zlecenia/zlecenie_testowe_144890/podglad_strony_ofert.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

offers = soup.select('.dashboard-list__item-offer')
for i, off in enumerate(offers[:3]):
    print(f"\n--- OFERTA {i+1} PRZYCISKI I FORMULARZE ---")
    for btn in off.find_all(['a', 'button', 'input']):
        print(f"Tag: <{btn.name}> class='{btn.get('class')}' href='{btn.get('href')}' value='{btn.get('value')}' action='{btn.get('action')}'")
        for k, v in btn.attrs.items():
            if 'id' in k.lower() or 'offer' in k.lower() or 'data' in k.lower():
                print(f"   attr: {k} = {v}")
