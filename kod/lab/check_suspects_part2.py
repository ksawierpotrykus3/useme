# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from check_suspects import suspects

print("\n--- SUSPECTS 71 TO 140 ---")
for i, o in enumerate(suspects[70:140], start=71):
    print(f"[{i}] {o['src']} | #{o['id']} | {o['budget']} | {o['title']}")
