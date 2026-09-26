import json

# Compile data from gleboka_typologia_klientow
import sys
sys.path.append('badania/analizy')
from gleboka_typologia_klientow import persona_stats, classified_all

out = {
    'total_jobs': len(classified_all),
    'typology': {}
}

for p, s in sorted(persona_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    wr = round(s['wins'] / s['total'] * 100, 2) if s['total'] > 0 else 0.0
    avg_th = round(sum(s['threads_won'])/len(s['threads_won']), 1) if s['threads_won'] else 0.0
    max_th = max(s['threads_won']) if s['threads_won'] else 0
    sample_won = [{
        'title': j.get('title'),
        'price': j.get('our_price'),
        'thread_size': j.get('thread_size', 0)
    } for per, j, won in classified_all if per == p and won][:5]
    
    out['typology'][p] = {
        'total': s['total'],
        'wins': s['wins'],
        'win_rate_pct': wr,
        'avg_thread_size': avg_th,
        'max_thread_size': max_th,
        'sample_won': sample_won
    }

with open('badania/analizy/03_nowa_gleboka_typologia_klientow.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Zapisano JSON nowej typologii do: badania/analizy/03_nowa_gleboka_typologia_klientow.json")
