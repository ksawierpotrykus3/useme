# -*- coding: utf-8 -*-
"""Łańcuch głębokiego rozumowania (deepseek-reasoner) dla odkrycia
nieoczywistych dźwigni: PSYCHOLOGICZNYCH, MERYTORYCZNYCH i WYCENY.
Zderza persony decyzyjne z laboratorium_modeli, audyt zlecenia #144890
oraz 16 domen technologicznych Useme.
"""

from pathlib import Path
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"

BASE_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core")
LAB_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\laboratorium_modeli\01_WIEDZA_I_SYNTEZY\useme_i_b2b")
OUTPUT_FILE = BASE_DIR / r"badania\analizy\technologie\baza_wiedzy\dzwignie_psychologia_merytoryka_wyceny.md"

# Wczytujemy fundamenty
konkurencja_txt = (BASE_DIR / r"badania\analizy\analiza_taktyk_konkurencji.md").read_text(encoding="utf-8")
persony_txt = (LAB_DIR / r"01_persony_zleceniodawcow.md").read_text(encoding="utf-8") if (LAB_DIR / r"01_persony_zleceniodawcow.md").exists() else ""
plan_mod_txt = (LAB_DIR / r"04_plan_modernizacji_ofertowarki.md").read_text(encoding="utf-8") if (LAB_DIR / r"04_plan_modernizacji_ofertowarki.md").exists() else ""

SYSTEM_PROMPT = """Jesteś Elitarnym Strategiem Negocjacji B2B, Psychologiem Decyzyjnym i Architektem Systemów Wycen dla Zaawansowanych Usług Programistycznych.
Działasz w trybie Deep Reasoning (Głębokie Myślenie R1). 
Twoim celem jest odkrycie i wypracowanie NAJWYŻSZEJ KLASY DŹWIGNI (levers), które zwielokrotnią szanse bota ofertowego na Useme na natychmiastową odpowiedź klienta na priv oraz wygranie zlecenia po wysokiej cenie (4 500 - 18 000 zł).

BEZWZGLĘDNE REGUŁY:
- Zero banałów, zero powtarzania ogólników typu "zbuduj zaufanie" czy "bądź miły".
- Każda dźwignia musi być twardym, gotowym mechanizmem psychologicznym lub inżynierskim do wdrożenia 1:1 w tekście oferty.
- Zero propozycji rozmów wideo, calli telefonicznych czy darmowych konsultacji na Zoomie (100% komunikacji pisemnej na Useme priv).
- Zero sztucznej mowy ("w sumie", "no hej", pseudoludzkie wtrącenia).
"""

PROMPT_USER = f"""ZADANIE DLA MODELU ROZUMUJĄCEGO:
Zbadaj poniższe materiały źródłowe (audyt 30 ofert konkurencji #144890, 4 persony decyzyjne z laboratorium_modeli, realia 16 domen technologii na Useme) i przeprowadź głęboką eksplorację:
CO JESZCZE MOŻEMY WYMYŚLIĆ, ABY MAKSYMALNIE ZWIĘKSZYĆ SZANSE:
1. PSYCHOLOGICZNE (psychika decydenta, odwrócenie dynamiki, usuwanie lęku, reguła wzajemności, uderzenie w ego/obawy),
2. MERYTORYCZNE (twarde dowody, architektura odwracalna, testy 24h na próbce danych, mierzalne SLA, likwidacja ryzyka wykonawczego),
3. WYCENY (architektura cenowa, dekompozycja modułowa, kontrast kotwiczenia, schemat Pilot 48h vs Full, retainery powdrożeniowe 400-600 zł/mies.).

MATERIAŁ 1 — ANALIZA KONKURENCJI #144890:
{konkurencja_txt[:10000]}

MATERIAŁ 2 — PERSONY DECYZYJNE (KTO PŁACI I PRZED KIM ODPOWIADA):
{persony_txt[:6000]}

MATERIAŁ 3 — PLAN MODERNIZACJI OFERTOWARKI:
{plan_mod_txt[:5000]}

STRUKTURA DOKUMENTU, KTÓRY MASZ STWORZYĆ (ZAPISZ W FORMACIE MARKDOWN):

# ARSENAŁ DŹWIGNI STRATEGICZNYCH: PSYCHOLOGIA, MERYTORYKA, WYCENA
## TAJNA BROŃ BOTA OFERTOWEGO USEME (EDYCJA ELITARNA 2026)

### CZĘŚĆ 1: PSYCHOLOGICZNE HAKI DECYZYJNE (JAK PRZEŁAMAĆ BARIERĘ MILCZENIA W 5 MINUT)
1. **Odwrócenie Dynamiki Władzy (Power Inversion)**: Jak pisać z pozycji pożądanego architekta-doradcy, który sam kwalifikuje projekt, a nie żebraka proszącego o zlecenie (przykłady zdań, które odwracają układ sił).
2. **Kradzież Wątpliwości i Radykalna Szczerość (Radical Honesty)**: Mówienie wprost czego NIE robimy, czego nie dotykamy i na co nie damy gwarancji (paradoks budowy zaufania).
3. **Technika "Podkładki dla Szefa" (dla Persony Kujawskiej)**: Gotowy fragment w ofercie, który pracownik może skopiować i wysłać przełożonemu/zarządowi jako uzasadnienie wyboru nas.
4. **Technika "Ulgi w Cierpieniu" (dla Zajechanego Foundera)**: Jak skrócić proces myślowy przedsiębiorcy z 2 godzin do 30 sekund i zdjąć z niego ciężar decyzyjny.
5. **Formatowanie Pytania w Środku Tekstu**: Anatomia idealnego pytania kwalifikującego – dlaczego pytania na końcu są ignorowane jako szablonowe CTA, a pytanie wplecione w 3. akapit wymusza natychmiastową reakcję.

### CZĘŚĆ 2: MERYTORYCZNE DŹWIGNIE DEKLASACJI (LIKWIDACJA RYZYKA WYKONAWCZEGO)
1. **Darmowy Mikro-Proof 24h (Darmowy Test na 3 Zanonimizowanych Plikach)**: Jak zaproponować natychmiastowy bezpłatny dowód bez przepracowywania się (np. "Wyślij mi 2 zanonimizowane skany/rekordy, w 24h odeślę gotowy sparsowany XML/JSON na priv").
2. **Koncepcja Decyzji Odwracalnej (Two-Way Door / Sandbox-First)**: Jak udowodnić klientowi, że nasze wdrożenie jest w 100% bezpieczne dla jego działającej produkcji (np. baza testowa, import do bufora, brak modyfikacji rejestrów).
3. **Kalkulacja TCO (Total Cost of Ownership)**: Uderzenie w ukryte koszty konkurencji (np. wyliczenie ile klient zapłaci za tokeny OpenAI, serwery proxy czy operacje Make.com w ciągu roku, jeśli wybierze tanią ofertę konkurenta).
4. **Klauzula 12 Miesięcy Gwarancji na Kod**: Jak sformułować gwarancję serwisową, której boi się dać 99% freelancerów, a która dla nas (przy poprawnym kodzie) jest zerowym kosztem.

### CZĘŚĆ 3: ARCHITEKTURA WYCENY I STRATEGIE MONETYZACJI
1. **Kotwiczenie 3-Wariantowe (Wariant A: Pilot 48h / Wariant B: Wdrożenie Produkcyjne / Wariant C: Turnkey Enterprise)**: Jak konstruować widełki cenowe, aby opcja docelowa (np. 7 500 zł) wydawała się oczywistym, bezpiecznym kompromisem.
2. **Dekompozycja Modułowa (Koniec z ryczałtem "3000 zł")**: Psychologia rozbicia na 6 modułów — dlaczego klient woli zapłacić 12 000 zł za 6 nazwanych klocków niż 4 000 zł za "kompleksowe wdrożenie".
3. **Model Retainera Powdrożeniowego (Opieka 400 - 800 zł/miesiąc)**: Jak już w pierwszej ofercie zasadzić ziarno pod stały miesięczny abonament serwisowy.
4. **Klauzula Płatności Kamieniami Milowymi (Escrow Useme)**: Jak użyć zabezpieczeń Useme na naszą korzyść, eliminując opór finansowy klienta.

### CZĘŚĆ 4: TABELA SZYBKIEGO WSTRZYKIWANIA (DŹWIGNIE DLA 4 GRUP TECHNOLOGICZNYCH)
Macierz dla:
- Grupa 1: ERP & KSeF
- Grupa 2: Scraping & Automatyzacje
- Grupa 3: Mobile & Hardware
- Grupa 4: DevOps, SQL & Tech-Agnostic
Podaj dla każdej grupy: Najsilniejszą Dźwignię Psychologiczną, Najtwardszy Proof Merytoryczny i Rekomendowany Model Wyceny.
"""

def main():
    print(f"\n==========================================================================")
    print(f"[*] URUCHAMIAM MOCNY ŁAŃCUCH ROZUMUJĄCY DLA DŹWIGNI: PSYCHOLOGIA + MERYTORYKA + WYCENA")
    print(f"[*] MODEL: {MODEL}")
    print(f"[*] PLIK WYJŚCIOWY: {OUTPUT_FILE.name}")
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
        print(f"[+] SUKCES! Zapisano arsenał dźwigni do: {OUTPUT_FILE.name} ({len(wynik)} znaków) w {dt}s")
    except Exception as e:
        print(f"[!] WYJĄTEK: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
