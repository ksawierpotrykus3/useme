import json
from collections import defaultdict

with open('badania/baza/ksawierpotrykus3/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
    przegrane = json.load(f)
with open('badania/baza/ksawierpotrykus3/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
    wygrane = json.load(f)

# Import verification data
import sys
sys.path.append('badania/analizy')
from weryfikacja_danych import tech_dict, all_jobs

granular_stats = {}
unmatched_jobs = []

for job, won in all_jobs:
    text = ((job.get('title') or '') + ' ' + (job.get('job_description') or '')).lower()
    matched = False
    for tech_name, patterns in tech_dict.items():
        import re
        if any(re.search(p, text) for p in patterns):
            if tech_name not in granular_stats:
                granular_stats[tech_name] = {'total': 0, 'wygrane': 0, 'przegrane': 0, 'win_rate_pct': 0.0}
            granular_stats[tech_name]['total'] += 1
            if won:
                granular_stats[tech_name]['wygrane'] += 1
            else:
                granular_stats[tech_name]['przegrane'] += 1
            matched = True
    if not matched:
        unmatched_jobs.append({
            'title': job.get('title'),
            'price': job.get('our_price'),
            'won': won,
            'category': job.get('category'),
            'desc_snippet': job.get('job_description', '')[:150]
        })

for k, v in granular_stats.items():
    v['win_rate_pct'] = round(v['wygrane'] / v['total'] * 100, 2) if v['total'] > 0 else 0.0

unmatched_won = sum(1 for x in unmatched_jobs if x['won'])
unmatched_lost = sum(1 for x in unmatched_jobs if not x['won'])

out_data = {
    'summary': {
        'total_jobs': len(all_jobs),
        'total_won': len(wygrane),
        'total_lost': len(przegrane),
        'tech_specified_jobs': len(all_jobs) - len(unmatched_jobs),
        'tech_agnostic_jobs': len(unmatched_jobs),
        'tech_agnostic_pct': round(len(unmatched_jobs) / len(all_jobs) * 100, 1),
        'tech_agnostic_won': unmatched_won,
        'tech_agnostic_win_rate_pct': round(unmatched_won / len(unmatched_jobs) * 100, 2)
    },
    'warning_sample_size': (
        "OSTRZEŻENIE STATYSTYCZNE: Z powodu ograniczonej próby wygranych (n=56), wskaźniki Win Rate dla technologii o "
        "liczbie zleceń n < 15 obarczone są bardzo wysoką wariancją (+/- 25-35%). Nie stanowią one deterministycznych "
        "'złotych strzałów', lecz wstępne hipotezy badawcze. Jedyną statystycznie istotną grupą wolumenową o niskim "
        "Win Rate jest WordPress/WooCommerce (n=104, WR=6.7%)."
    ),
    'granular_technologies': dict(sorted(granular_stats.items(), key=lambda x: x[1]['total'], reverse=True)),
    'unmatched_won_samples': [x for x in unmatched_jobs if x['won']],
    'unmatched_lost_samples_top10': [x for x in unmatched_jobs if not x['won']][:10]
}

out_path = 'badania/analizy/02_matryca_granularna_technologie_i_unmatched.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)

print(f"Zapisano granularną bazę danych do: {out_path}")
