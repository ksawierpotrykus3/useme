# -*- coding: utf-8 -*-
"""
Audyt dopasowań słów kluczowych i eliminacja fałszywych dopasowań podciągów.
"""
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
import re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
from audit_strict_red import orders, parse_budget

def has_word(text, words):
    pattern = r'\b(' + '|'.join(re.escape(w) for w in words) + r')\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def has_phrase(text, phrases):
    for p in phrases:
        if p.lower() in text.lower():
            return True
    return False

# Przetestujmy 3D i AI z użyciem granic słów
print("Test dopasowania 3D i AI:")
for o in orders:
    t = o['title']
    d = o['desc']
    full = t + ' ' + d
    
    # 3D
    is_3d = has_word(t, ['3d', 'webgl', 'three.js', 'cad', 'cnc', 'topsolid', 'babylon']) or \
            has_phrase(t, ['konfigurator 3d', 'konfigurator mebli', 'konfigurator produktu', 'konfigurator']) or \
            (has_phrase(full, ['three.js', 'webgl']) and has_phrase(t, ['konfigurator', 'mebli', 'brył']))
            
    if is_3d:
        print(f"3D: #{o['id']} | {t}")
