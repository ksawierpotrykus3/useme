# -*- coding: utf-8 -*-
import sys
sys.path.append(r'C:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/lab')
sys.stdout.reconfigure(encoding='utf-8')
from engine_audit import classified_data

crm_saas = [x for x in classified_data if x['label'] == "Enterprise CRM, SaaS & Dedykowane Web Apps (React/Next/Node/Laravel)"]
print(f"Liczba zleceń w CRM/SaaS: {len(crm_saas)}")

wp_leaks = []
for x in crm_saas:
    o = x['order']
    t = o['title'].lower()
    d = o['desc'].lower()
    full = t + ' ' + d
    if any(k in full for k in ['wordpress', 'elementor', 'divi', 'strona www', 'wizytówk', 'wizytowk']):
        wp_leaks.append((o, t, o['cat']))

print(f"Potencjalne wycieki stron/WP w CRM/SaaS: {len(wp_leaks)}")
for o, t, c in wp_leaks:
    print(f"  #{o['id']} | {c} | {t}")
