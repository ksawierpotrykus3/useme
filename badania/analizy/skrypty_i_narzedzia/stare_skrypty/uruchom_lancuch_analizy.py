import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def call_deepseek(prompt, system_prompt="Jesteś czołowym analitykiem systemów sprzedaży B2B i inżynierii odwrotnej rynku Useme."):
    url = "http://127.0.0.1:4571/v1/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000,
        "stream": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return res['choices'][0]['message']['content']

def main():
    print("Inicjalizacja łańcucha analitycznego z DeepSeek...")
    
    with open('badania/analizy/01_dane_empiryczne_470.json', 'r', encoding='utf-8') as f:
        d_emp = json.load(f)
    with open('badania/analizy/02_matryca_2d_klient_x_tech.json', 'r', encoding='utf-8') as f:
        d_mat = json.load(f)
        
    stats_w = d_emp['stats_wygrane']
    stats_p = d_emp['stats_przegrane']
    client_totals = d_mat['client_totals']
    tech_totals = d_mat['tech_totals']
    matrix = d_mat['matrix_2d']
    
    prompt = f"""
Przeanalizuj twarde dane statystyczne z audytu 470 zleceń na Useme (56 wygranych z odpowiedziami i wątkami na priv vs 414 przegranych) oraz macierz 2D [Typ Klienta x Archetyp Technologiczny].

DANE STATYSTYCZNE:
Wygrane:
{json.dumps(stats_w, indent=2, ensure_ascii=False)}

Przegrane:
{json.dumps(stats_p, indent=2, ensure_ascii=False)}

KLASYFIKACJA KLIENTÓW:
{json.dumps(client_totals, indent=2, ensure_ascii=False)}

KLASYFIKACJA TECHNOLOGII:
{json.dumps(tech_totals, indent=2, ensure_ascii=False)}

MACIERZ 2D (TOP KOMBINACJE):
{json.dumps(matrix, indent=2, ensure_ascii=False)}

TWOJE ZADANIE:
Napisz wyczerpujący, inżynieryjny raport badawczy:
1. TWARDE POTWIERDZENIE EMPIRYCZNE (Dlaczego oferty wygrywały i dlaczego nikt nie kupuje bez priv):
   - Co statystyka mówi o długości tekstu, CTA, pytaniach diagnostycznych, gęstości technologicznej.
   - Analiza wątków (dlaczego niektóre zlecenia miały po 373, 173 czy 53 wiadomości na priv).
2. TYPOLOGIA ZLECENIODAWCÓW (5 typów ludzi, którzy piszą na Useme):
   - Dla każdego typu: profil psychologiczny, styl pisania, czego się boi, co go irytuje, jaki haczyk wymusza u niego kliknięcie na priv.
3. MACIERZ 2D: [TYP KLIENTA] x [ARCHETYP TECHNOLOGICZNY]:
   - Opracuj zasady gry dla kluczowych przecięć (np. Biznesmen x ERP, Tech Lead x Web/SaaS, E-com Manager x Shopify, Startupowiec x Mobile Apps, Quick-Fix x Boty).
   - Wskaż, które kombinacje mają najwyższy Win Rate i dlaczego, a które mają 0% i są pułapkami.
4. PROTOKÓŁ PRZEJŚCIA I ROZMOWY NA PRIV:
   - Dokładny schemat 3 kroków na priv dla każdego typu klienta (jak wyciągnąć pliki/dostęp i jak zamknąć bezpieczne escrow na Useme).

Napisz raport w formacie Markdown, czysto, analitycznie, bez marketingowego bełkotu.
"""
    print("Wysyłanie zapytania do DeepSeek (Łańcuch 1 i 2)...")
    raport_md = call_deepseek(prompt)
    
    out_md = 'badania/analizy/01_pelny_raport_empiryczny_i_matryca_2d.md'
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write(raport_md)
        
    print(f"Raport zapisany pomyślnie w: {out_md}")

if __name__ == '__main__':
    main()
