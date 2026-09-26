import json
import re
import os
from collections import Counter

def parse_price(p_str):
    if not p_str:
        return None
    # e.g. "8500,00 PLN", "2200,00 EUR", "300 PLN"
    m = re.search(r'([\d\s]+(?:[.,]\d+)?)', p_str)
    if m:
        num = m.group(1).replace(' ', '').replace(',', '.')
        try:
            return float(num)
        except:
            return None
    return None

def parse_days(d_str):
    if not d_str:
        return None
    m = re.search(r'(\d+)', str(d_str))
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

def analyze_proposal(prop):
    if not prop:
        return {
            'chars': 0, 'words': 0, 'has_question_cta': False,
            'has_call_cta': False, 'has_artifact_cta': False,
            'coaching_score': 0, 'tech_density': 0, 'has_direct_priv': False
        }
    chars = len(prop)
    words = len(prop.split())
    lines = [l.strip() for l in prop.splitlines() if l.strip()]
    last_3 = " ".join(lines[-3:]) if len(lines) >= 3 else " ".join(lines)
    
    # CTA features in last lines
    has_question_cta = '?' in last_3
    has_call_cta = any(k in last_3.lower() for k in ['zdzwoń', 'zdzwon', 'call', 'rozmow', 'telefon', 'spotkan', 'meet', 'google meet'])
    has_artifact_cta = any(k in last_3.lower() for k in ['podeślij', 'podeslij', 'zrzut', 'screen', 'plik', 'link', 'figm', 'próbk', 'probk', 'dostęp', 'dostep', 'repo'])
    has_direct_priv = any(k in last_3.lower() for k in ['priv', 'wiadomość prywatn', 'wiadomosc prywatn', 'na czacie', 'w wiadomości'])
    
    # Coaching words
    coaching_phrases = [
        'doskonale rozumiem', 'chętnie pomogę', 'chetnie pomoge', 'z przyjemnością', 'z przyjemnoscia',
        'kompleksow', 'indywidualne podejście', 'indywidualne podejscie', 'profesjonalne podejście',
        'jako doświadczony', 'jako doswiadczony', 'szerokie doświadczenie', 'bogate doświadczenie',
        'gwarantuję pełne', 'gwarantuje pelne', 'zadbam o każdy', 'zadbam o kazdy'
    ]
    coaching_score = sum(1 for phrase in coaching_phrases if phrase in prop.lower())
    
    # Tech terms
    tech_keywords = [
        'api', 'sql', 'database', 'baza', 'json', 'xml', 'python', 'node', 'react', 'vue',
        'laravel', 'docker', 'endpoint', 'webhook', 'rest', 'soap', 'cron', 'middleware',
        'c#', '.net', 'php', 'wordpress', 'woocommerce', 'shopify', 'prestashop', 'postman',
        'git', 'token', 'auth', 'jwt', 'redis', 'n8n', 'make', 'zapier', 'selenium', 'playwright',
        'flutter', 'kotlin', 'swift', 'ios', 'android', 'css', 'html', 'liquid', 'headless'
    ]
    prop_lower = prop.lower()
    tech_density = sum(1 for kw in tech_keywords if re.search(r'\b' + re.escape(kw) + r'\b', prop_lower))
    
    return {
        'chars': chars,
        'words': words,
        'has_question_cta': has_question_cta,
        'has_call_cta': has_call_cta,
        'has_artifact_cta': has_artifact_cta,
        'has_direct_priv': has_direct_priv,
        'coaching_score': coaching_score,
        'tech_density': tech_density
    }

def main():
    base = 'badania/baza/ksawierpotrykus3'
    with open(f'{base}/02_przegrane/przegrane_pelne_416.json', 'r', encoding='utf-8', errors='ignore') as f:
        przegrane = json.load(f)
        
    with open(f'{base}/03_odpisane/wygrane_56.json', 'r', encoding='utf-8', errors='ignore') as f:
        wygrane = json.load(f)
        
    print(f"Loaded {len(przegrane)} przegranych and {len(wygrane)} wygranych.")
    
    # Process both
    dataset = []
    for item in wygrane:
        analysis = analyze_proposal(item.get('our_proposal', ''))
        dataset.append({
            'status': 'wygrana',
            'id': item.get('job_id') or item.get('offer_id'),
            'title': item.get('title', ''),
            'category': item.get('category', ''),
            'client': item.get('client', ''),
            'price': parse_price(item.get('our_price')),
            'days': parse_days(item.get('our_days')),
            'job_desc_len': len(item.get('job_description', '')),
            'thread_size': item.get('thread_size', 0),
            **analysis
        })
        
    for item in przegrane:
        analysis = analyze_proposal(item.get('our_proposal', ''))
        dataset.append({
            'status': 'przegrana',
            'id': item.get('offer_id'),
            'title': item.get('title', ''),
            'category': item.get('category', ''),
            'client': item.get('client', ''),
            'price': parse_price(item.get('our_price')),
            'days': parse_days(item.get('our_days')),
            'job_desc_len': len(item.get('job_description', '')),
            'thread_size': 0,
            **analysis
        })
        
    # Aggregate statistics
    def get_stats(subset):
        n = len(subset)
        if n == 0:
            return {}
        avg_words = sum(x['words'] for x in subset) / n
        avg_chars = sum(x['chars'] for x in subset) / n
        pct_question = sum(1 for x in subset if x['has_question_cta']) / n * 100
        pct_call = sum(1 for x in subset if x['has_call_cta']) / n * 100
        pct_artifact = sum(1 for x in subset if x['has_artifact_cta']) / n * 100
        pct_priv = sum(1 for x in subset if x['has_direct_priv']) / n * 100
        avg_coaching = sum(x['coaching_score'] for x in subset) / n
        avg_tech = sum(x['tech_density'] for x in subset) / n
        prices = [x['price'] for x in subset if x['price'] is not None and x['price'] < 100000]
        avg_price = sum(prices) / len(prices) if prices else 0
        median_price = sorted(prices)[len(prices)//2] if prices else 0
        days = [x['days'] for x in subset if x['days'] is not None]
        avg_days = sum(days) / len(days) if days else 0
        return {
            'count': n,
            'avg_words': round(avg_words, 1),
            'avg_chars': round(avg_chars, 1),
            'pct_question_cta': round(pct_question, 1),
            'pct_call_cta': round(pct_call, 1),
            'pct_artifact_cta': round(pct_artifact, 1),
            'pct_direct_priv': round(pct_priv, 1),
            'avg_coaching_score': round(avg_coaching, 2),
            'avg_tech_density': round(avg_tech, 2),
            'avg_price': round(avg_price, 1),
            'median_price': median_price,
            'avg_days': round(avg_days, 1)
        }
        
    stats_w = get_stats([x for x in dataset if x['status'] == 'wygrana'])
    stats_p = get_stats([x for x in dataset if x['status'] == 'przegrana'])
    
    print("\n--- STATYSTYKI PORÓWNAWCZE (WYGRANE vs PRZEGRANE) ---")
    print(f"Metryka                     | WYGRANE (56)   | PRZEGRANE (414)")
    print(f"----------------------------|----------------|----------------")
    for k in stats_w:
        print(f"{k:<27} | {str(stats_w[k]):<14} | {str(stats_p[k]):<14}")
        
    # Save processed analysis dataset
    out_file = 'badania/analizy/01_dane_empiryczne_470.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'stats_wygrane': stats_w, 'stats_przegrane': stats_p, 'dataset': dataset}, f, ensure_ascii=False, indent=2)
    print(f"\nZapisano dane do: {out_file}")

if __name__ == '__main__':
    main()
