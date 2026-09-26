# -*- coding: utf-8 -*-
"""Całkowicie krytyczny audyt Red Team (deepseek-reasoner) dla taktyk i bazy wiedzy.
Bezlitosna weryfikacja: co jest głupie, co odpada, co zostaje, dla kogo i dlaczego.
Zawiera analizę dylematu: OFERTA PUBLICZNA vs PRYWATNA WIADOMOŚĆ (PRIV).
"""

from pathlib import Path
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"

BASE_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
OUTPUT_FILE = BASE_DIR / r"badania\analizy\technologie\baza_wiedzy\audyt_krytyczny_red_team.md"

# Wczytujemy dotychczasowe materiały
dzwignie_txt = (BASE_DIR / r"badania\analizy\technologie\baza_wiedzy\dzwignie_psychologia_merytoryka_wyceny.md").read_text(encoding="utf-8")
konkurencja_txt = (BASE_DIR / r"badania\analizy\analiza_taktyk_konkurencji.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = """Jesteś Szefem Czerwonego Zespołu (Red Team), bezlitosnym audytorem operacyjnym, sceptycznym architektem i doświadczonym przedsiębiorcą, który zjadł zęby na polskich platformach freelancerskich (Useme, B2B).

TWOJA ROLA:
Twoim zadaniem NIE JEST chwalenie nikogo. Twoim jedynym zadaniem jest brutalna, zimna, bezwzględna krytyka dotychczas wypracowanych koncepcji, taktyk i założeń. Masz wytknąć wszystko, co jest:
- Naiwne,
- Przekombinowane (over-engineering),
- Groźne dla biznesu i marży,
- Odpychające dla klienta w rzeczywistym świecie,
- Iluzoryczne lub oparte na myśleniu życzeniowym.

KLUCZOWY KONTEKST I OSTRZEŻENIE OD DOWÓDZTWA:
Nadal NIE ZDECYDOWALIŚMY, czy bot ma składać ofertę publiczną, czy pisać na priv, czy łączyć oba kanały! Musisz poddać to głębokiej, bezwzględnej analizie anatomicznej (zalety, wady, ryzyka obu dróg).
"""

PROMPT_USER = f"""ZADANIE DLA RED TEAMU:
Przeprowadź bezlitosny audyt dotychczas wypracowanego arsenału taktyk, dźwigni i założeń bota Useme.

MATERIAŁ DO OSTRZAŁU (ARSENAŁ DŹWIGNI I ANALIZA KONKURENCJI):
{dzwignie_txt}

DODATKOWY KONTEKST ZLECENIA TESTOWEGO #144890:
{konkurencja_txt[:6000]}

WYMAGANA STRUKTURA RAPORTU AUDYTORSKIEGO RED TEAMU (W FORMACIE MARKDOWN):

# RAPORT AUDYTU RED TEAM: CO JEST GŁUPIE, CO ODPADA, A CO ZOSTAJE
## BEZLITOSNY OSTRZAŁ TAKTYK, PSYCHOLOGII I ARCHITEKTURY OFERTOWANIA USEME 2026

### CZĘŚĆ 1: WIELKI SPÓR — OFERTA PUBLICZNA VS WIADOMOŚĆ PRYWATNA (PRIV)
1. **Anatomia Ścieżki A: Tylko Wiadomość Prywatna (Priv)**:
   - Gdzie jest naiwność w założeniu, że "seniorzy piszą tylko na priv"?
   - Kiedy klient w ogóle NIE ODBIERA priva na Useme (brak powiadomień, lenistwo, strach przed spamem)?
   - W jakich zleceniach priv to czyste marnowanie energii, a w jakich jest jedyną szansą?
2. **Anatomia Ścieżki B: Tylko Oferta Publiczna**:
   - Dlaczego publiczna oferta jest widoczna dla konkurencji (kradzież insightów)?
   - Jakie daje przewagi (widoczność w zestawieniu, formalna obecność w panelu decyzyjnym Useme)?
3. **Anatomia Ścieżki C: Podejście Hybrydowe lub Warunkowe**:
   - Kiedy złożyć publiczną ofertę, a kiedy wejść z uderzeniem na priv?
   - Konkretne kryteria decyzyjne dla bota: Budżet, Typ zlecenia, Czas od publikacji.

### CZĘŚĆ 2: ROZSTRZELANIE ARSENAŁU — CO JEST GŁUPIE I NAIWNE?
Przeanalizuj każdą wypracowaną dotąd dźwignię i bezlitośnie wskaż jej słabe punkty:
1. **Odwrócenie Władzy (Power Inversion)**: Czy "Zanim złożę ofertę..." nie brzmi dla zapracowanego klienta jak arogancka bezczelność freelancera, którego zaraz skasuje, bo ma 29 innych chętnych? Gdzie jest granica między autorytetem a bufonadą?
2. **Darmowy Mikro-Proof 24h (Darmowy test 2 plików)**: Czy to nie jest idealna furtka dla cwaniaków i "wyzyskiwaczy", którzy wrzucą swoje 2 najtrudniejsze pliki, dostaną darmowy kod/dane, po czym znikną i zlecą resztę studentowi za 200 zł?
3. **12 Miesięcy Gwarancji na Kod**: Dlaczego dawanie rocznej gwarancji przy integracjach zewnętrznych (KSeF, Allegro, API sklepów, zmiany bibliotek) to potencjalna pętla na szyję programisty? Na co wolno dać gwarancję, a na co to samobójstwo?
4. **"Podkładka dla Szefa" i Tabele 8 Modułów**: Czy wrzucanie 8-modułowej tabeli do zlecenia za 2 000 zł nie wygląda komicznie i nie odstrasza ludzi szukających szybkiego rozwiązania?
5. **Kradzież Wątpliwości (Radical Honesty)**: Czy mówienie "czego nie potrafię / czego nie robię" nie zostanie przez 80% klientów zinterpretowane po prostu jako brak kompetencji?

### CZĘŚĆ 3: CO BEZWZGLĘDNIE ZOSTAJE (SELEKCJA OSTATECZNA)
Dla każdej ocalałej taktyki podaj:
- **Co dokładnie zostaje?**
- **DLA KOGO zostaje?** (dokładne mapowanie na persony: Kujawska / Zajechany Founder / CTO / Minimalista / Klient Nietechniczny).
- **DLACZEGO przetrwało ostrzał?** (twarde uzasadnienie biznesowe).

### CZĘŚĆ 4: CO BEZWZGLĘDNIE LĄDUJE W KOSZU (LUB POD TWARDYM WARUNKIEM)
- Wypisz czarną listę pomysłów, które brzmią mądrze na papierze, ale w boju na Useme poniosą klęskę.
- Dla pomysłów warunkowych: jaki twardy warunek (IF) musi zajść, aby w ogóle wolno było ich użyć?

### CZĘŚĆ 5: MISTRZOWSKA REKOMENDACJA DLA ARCHITEKTURY BOTA
Zwięzłe podsumowanie: jak bot ma podejmować decyzję o tonie, długości, kanale (public vs priv) i cenie w 2026 roku.
"""

def main():
    print(f"\n==========================================================================")
    print(f"[*] URUCHAMIAM KRYTYCZNY RED TEAM (DEEP REASONING)")
    print(f"[*] MODEL: {MODEL}")
    print(f"[*] PLIK WYNIKOWY: {OUTPUT_FILE.name}")
    print(f"==========================================================================")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": PROMPT_USER}
        ],
        "temperature": 0.3,
        "stream": False
    }

    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=360)
        if r.status_code != 200:
            print(f"[!] BŁĄD HTTP {r.status_code}: {r.text[:500]}")
            sys.exit(1)
            
        dane = r.json()
        wynik = dane["choices"][0]["message"]["content"]
        
        OUTPUT_FILE.write_text(wynik, encoding="utf-8")
        dt = round(time.time() - t0, 1)
        print(f"[+] SUKCES! Zapisano audyt Red Teamu do: {OUTPUT_FILE.name} ({len(wynik)} znaków) w {dt}s")
    except Exception as e:
        print(f"[!] WYJĄTEK: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
