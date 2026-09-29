# -*- coding: utf-8 -*-
import re
from pathlib import Path
from bs4 import BeautifulSoup

html = Path('debug/thread_1963306.html').read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

print("Form action:", [f.get('action') for f in soup.find_all('form')])
print("Div data-* attrs:")
for tag in soup.find_all(True):
    for k, v in tag.attrs.items():
        if k.startswith('data-'):
            print(f"  {tag.name} {k} = {v}")

print("Script contents with /mesg/ or API:")
for s in soup.find_all('script'):
    txt = s.get_text()
    if '1963306' in txt or 'mesg' in txt:
        print("Script snippet:", txt[:200])
