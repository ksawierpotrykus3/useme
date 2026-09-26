# -*- coding: utf-8 -*-
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
import re
sys.stdout.reconfigure(encoding='utf-8')
from audit_strict_red import acc_strict
from test_regex_boundaries import has_word, has_phrase

mobile = []
for o in acc_strict:
    t = o['title']
    cat = o['cat']
    is_m = ('aplikacje mobilne' in cat.lower()) or \
           has_word(t, ['ios', 'android', 'swift', 'swiftui', 'kotlin', 'flutter', 'react native', 'flutterflow']) or \
           has_phrase(t, ['aplikacja mobilna', 'aplikacji mobilnej', 'aplikację mobilną', 'programisty aplikacji mobilnej', 'gra mobilna'])
    if is_m:
        mobile.append(o)

print(f"Mobile count: {len(mobile)}")
for o in mobile:
    print(f"#{o['id']} [{o['budget']}]: {o['title']}")
