# -*- coding: utf-8 -*-
"""
Skrypt: generuj_scenariusze_klientow.py
Cel: Generowanie głębokich, opisowych DOKUMENTÓW ZROZUMIENIA CZŁOWIEKA (Scenariuszy Psychologicznych)
dla zweryfikowanych typów klientów i modyfikatorów na platformie Useme.
Zasada kluczowa: ZERO sztywnych reguł 'jeśli to to rób to'.
Głęboki kontekst, psychologia, świat klienta, dynamika emocjonalna i elastyczność dla AI.
Uruchamiany blokami (po kolei):
Blok 1: Tradycyjne MŚP/ERP & E-commerce Merchant
Blok 2: Agencja/Software House & Ekspert Dziedzinowy
Blok 3: Tech-Agnostic Biznes & Quick IT Fix
Blok 4: Modyfikatory Psychologiczne (Rescue, Delegowany, Phantom Startup)
"""

import json
import os
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"
TARGET_DIR = "Projekty_autorskie/useme_core/badania/analizy/typy_klientow/scenariusze"

BLOKI = {
    "1": {
        "nazwa": "Blok 1: Komercyjne Filary (Tradycyjne MŚP/ERP & E-commerce)",
        "pliki": [
            {
                "id": "klient_01_tradycyjne_msp_erp_przemysl.md",
                "typ": "Tradycyjne MŚP & ERP / Przemysł",
                "opis": "Właściciel fabryki, hurtowni, firmy produkcyjnej. Magazyn, WZ, KSeF, Enova, Subiekt, Comarch, TopSolid.",
                "case_studies": "OXYGEN (Subiekt nexo WZ komplety), ENERZON (Anteeo/Base/Idosell), Wiktoria Iwanow (TopSolid meble 8.5k), Centrum Budowlane Kołcz (Enova365 5.5k)."
            },
            {
                "id": "klient_02_ecommerce_merchant.md",
                "typ": "E-commerce Merchant (Sklepy Internetowe)",
                "opis": "Właściciel lub manager sklepu online (Shoper, Shopify, Presta, IdoSell). Konwersja, koszyk, kurierzy DPD, integracje stanów.",
                "case_studies": "Paweł (IdoSell B2B 173 wiadomości), Klaudia (Shoper konfigurator 7 wiadomości), Gardd (Shopify dotacja 3929 zł), Arkadiusz (PrestaShop 5.5k)."
            }
        ]
    },
    "2": {
        "nazwa": "Blok 2: B2B i Usługi Regulowane (Agencja & Ekspert Dziedzinowy)",
        "pliki": [
            {
                "id": "klient_03_agencja_software_house.md",
                "typ": "Agencja / Software House (B2B Podwykonawstwo)",
                "opis": "PM w pożarze deadline'u, CTO lub właściciel agencji szukający rąk do pracy. Podwykonawstwo B2B, code-review, staging, terminy.",
                "case_studies": "TG Coders (Kotlin mobile pożar), Wojtek (Senior Node.js 7k), zlecenia B2B ze stawką godzinową."
            },
            {
                "id": "klient_04_ekspert_dziedzinowy_uslugi.md",
                "typ": "Ekspert Dziedzinowy / Biznes Regulowany",
                "opis": "Lekarz, psycholog, komornik, prawnik, szkoleniowiec. RODO, odpowiedzialność prawna, eliminacja realnego bólu finansowego, zaufanie.",
                "case_studies": "Doktor Monika (gabinet medyczny, 12 100 zł netto opłacone escrow), Komornik Tomasz Wójcik (forensic Windows/sabotaż), k8investpro (księgi wieczyste)."
            }
        ]
    },
    "3": {
        "nazwa": "Blok 3: Proces i Szybkie Reagowanie (Tech-Agnostic & Quick Fix)",
        "pliki": [
            {
                "id": "klient_05_tech_agnostic_biznes.md",
                "typ": "Tech-Agnostic Business Owner (33% Rynku)",
                "opis": "Przedsiębiorca nietechniczny. Myśli procesem i rezultatem biznesowym. Zero tolerancji na żargon IT. Chce gotowego pudełka.",
                "case_studies": "skaner (Airtable consultancy), Klaudia (girlandy balonowe), zlecenia na automatyzację Excel/dokumentów bez nazw frameworków."
            },
            {
                "id": "klient_06_quick_fix_awaria_hobbysta.md",
                "typ": "Quick IT Fix & Zlecający Prywatny",
                "opis": "Awaria na wczoraj, błąd 500, zawieszający się skrypt, drobne zlecenie prywatne lub hobbystyczne.",
                "case_studies": "Martin Smith (poprawka strony 400 zł), nagłe błędy serwera, pomoc w instalacji."
            }
        ]
    },
    "4": {
        "nazwa": "Blok 4: Modyfikatory Psychologiczne (Stany Emocjonalno-Operacyjne)",
        "pliki": [
            {
                "id": "modyfikator_rescue_klient_sparzony.md",
                "typ": "Modyfikator: RESCUE / KLIENT SPARZONY (12.1% Rynku)",
                "opis": "Klient po ucieczce dewelopera, porzuconym projekcie lub partaczu. Skrajna nieufność, potrzeba audytu i bezpieczeństwa.",
                "case_studies": "Rafał W. (podejrzenie składaka), Centrum Budowlane Kołcz (audyt wdrożenia Enova), TG Coders (dokończenie Kotlina po kimś)."
            },
            {
                "id": "modyfikator_delegowany_pracownik.md",
                "typ": "Modyfikator: ODDELEGOWANY PRACOWNIK (4.3% Rynku)",
                "opis": "Asystentka, księgowa, pracownik biura piszący w imieniu szefa/zarządu. Brak władzy budżetowej, strach przed wzięciem winy na siebie.",
                "case_studies": "Zlecenia ze zwrotami 'w imieniu szefa', 'zarząd prosił', 'poszukujemy dla naszej firmy'."
            },
            {
                "id": "modyfikator_phantom_startup_wizjoner.md",
                "typ": "Modyfikator: PHANTOM STARTUP / WIZJONER ZA EQUITY",
                "opis": "Founder bez kasy, obietnice equity, wizje jednorożców, budżety 100 zł lub obietnice 30k bez pokrycia w escrow.",
                "case_studies": "Adrian Cwiertnia (Mental Health 100 zł / 34k), Luxwiev (TikTok z ogłoszeniami), joaxx (OpenCV)."
            }
        ]
    }
}

SYSTEM_PROMPT = """Jesteś Elitarnym Psychologiem Biznesu B2B, Głównym Architektem Behawioralnym i Mistrzem Sprzedaży Asynchronicznej na platformach freelancerskich (Useme).
Tworzysz POGŁĘBIONY DOKUMENT ZROZUMIENIA CZŁOWIEKA (SCENARIUSZ PSYCHOLOGICZNY).

ZASADA NACZELNA UŻYTKOWNIKA:
"ZERO sztywnych formułek typu: 'jeśli klient mówi A, napisz B'. To jest głupie i rodzi robotyczne oferty.
Zamiast tego tworzymy bogate, głębokie opisy, które COŚ TŁUMACZĄ:
- Wyjaśniają rzeczywistość, w jakiej ten człowiek żyje i pracuje,
- Pokazują jego ukryte lęki, mechanizmy obronne i presję otoczenia,
- Wyjaśniają, jak postrzega ryzyko i dlaczego standardowe oferty go odrzucają,
- Dają AI głębokie zrozumienie kontekstu, aby model sam, elastycznie wyczuwał podobieństwo i dobierał właściwy ton."
"""

def generuj_scenariusz(plik_info):
    target_path = os.path.join(TARGET_DIR, plik_info["id"])
    print(f"\n[*] Generuję scenariusz dla: {plik_info['typ']}")
    print(f"[*] Cel: {target_path}")

    user_prompt = f"""ZADANIE:
Napisz wyczerpujący, głęboki, psychologiczno-operacyjny DOKUMENT ZROZUMIENIA CZŁOWIEKA dla profilu:
TYP: {plik_info['typ']}
OPIS BAZOWY: {plik_info['opis']}
EMPIRYCZNE CASE STUDIES Z BAZY USEME: {plik_info['case_studies']}

STRUKTURA DOKUMENTU (W MARKDOWN):

# SCENARIUSZ PSYCHOLOGICZNO-OPERACYJNY: {plik_info['typ'].upper()}
## GŁĘBOKI PRZEWODNIK ZROZUMIENIA CZŁOWIEKA DLA MODELU AI

### 1. ŚWIAT CZŁOWIEKA: W JAKIEJ RZECZYWISTOŚCI ŻYJE I PRACUJE?
- Kim jest w świecie fizycznym? (wiek, pozycja, otoczenie, z kim pije kawę, kto na niego krzyczy, przed kim odpowiada).
- Jaki jest jego rytm dnia i poziom stresu operacyjnego?
- Co ten człowiek widzi, gdy loguje się na Useme? (czy to dla niego codzienność, czy ostateczność i zło konieczne?).

### 2. ANATOMIA UKRYTEGO BÓLU I PARANOI
- Co jest jego prawdziwym, niewypowiedzianym lękiem? (to nigdy nie jest "chcę skrypt", to jest: "boi się, że magazynierzy nie wydadzą towaru", "boi się kary z US", "boi się że szef go zwolni").
- Jaki błąd popełniają amatorzy, którzy czytają jego ogłoszenie powierzchownie?
- Dlaczego ten człowiek ma alergię na korpo-gadki i generyczne oferty?

### 3. MECHANIKA MYŚLENIA I FILTRY ZAUFANIA (JAK PODEJMUJE DECYZJĘ?)
- Co sprawia, że w ułamku sekundy myśli: "O, ten człowiek naprawdę wie, o co u mnie chodzi"?
- Jaki jest jego naturalny słownik pojęciowy? (jakie pojęcia budują natychmiastowy autorytet, a jakie go natychmiast odstraszają?).
- Dlaczego woli krótką, oszczędną diagnozę inżynierską od 3-stronicowego elaboratu?

### 4. DYNAMIKA ROZMOWY NA PRIV I ZACHOWANIE NEGOCJACYJNE
- Jak ten człowiek zachowuje się w wiadomości prywatnej? (czy odpisuje w 3 minuty z telefonu, czy potrzebuje 2 dni na konsultację z księgową?).
- Ile wiadomości zazwyczaj trwa domknięcie transakcji i od czego to zależy?
- Jak reaguje na wycenę i jak uzasadnić stawkę bez tłumaczenia się?

### 5. DOWODY Z ŻYCIA: DEKONSTRUKCJA PRAWDZIWYCH ZLECEŃ Z BAZY
- Weź pod lupę konkretne przypadki z bazy Useme ({plik_info['case_studies']}).
- Pokaż krok po kroku: co napisał w ogłoszeniu -> co działo się pod maską -> jak należało z nim rozmawiać.

### 6. WSKAZÓWKI ELASTYCZNEJ ADAPTACJI DLA AI (BEZ SZTYWNYCH IF-ELSE)
- Jak AI ma oceniać stopień dopasowania do tego scenariusza?
- Jakie niuanse hybrydowe mogą się pojawić (np. ten typ + modyfikator Rescue)?
- KIEDY ZIGNOROWAĆ TEN SCENARIUSZ? (granice, kiedy ten profil przestaje pasować).

Pisz bez korporacyjnego bełkotu, bez lania wody, z głębokim wglądem w realia polskiego biznesu i psychologię platform freelancerskich.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }

    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=300)
        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"]
            os.makedirs(TARGET_DIR, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            dt = round(time.time() - t0, 1)
            print(f"[+] Zapisano: {plik_info['id']} ({len(content)} znaków) w {dt}s")
            return True
        else:
            print(f"[!] Błąd HTTP {r.status_code}: {r.text[:400]}")
            return False
    except Exception as e:
        print(f"[!] Wyjątek: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Użycie: python generuj_scenariusze_klientow.py <nr_bloku: 1|2|3|4>")
        sys.exit(1)
        
    nr_bloku = sys.argv[1]
    if nr_bloku not in BLOKI:
        print(f"Nieznany blok {nr_bloku}. Dostępne: {list(BLOKI.keys())}")
        sys.exit(1)
        
    blok = BLOKI[nr_bloku]
    print(f"============================================================")
    print(f"[*] URUCHAMIAM ŁAŃCUCH REASONING DLA: {blok['nazwa']}")
    print(f"============================================================")
    
    for plik_info in blok["pliki"]:
        generuj_scenariusz(plik_info)
        time.sleep(2)
        
    print(f"\n[+] Blok {nr_bloku} zakończony pomyślnie!")

if __name__ == "__main__":
    main()
