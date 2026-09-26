# -*- coding: utf-8 -*-
"""Mocny łańcuch rozumujący (deepseek-reasoner / R1) dla grup technologicznych.
Przetwarza grupy wiedzy, zderza je z audytem #144890 i generuje KARTY BOJOWE BOTA.
Uruchamiany sekwencyjnie dla grup: 1, 2, 3, 4.
"""

from pathlib import Path
import sys
import time
import requests

PROXY_URL = "http://127.0.0.1:4571/v1/chat/completions"
MODEL = "deepseek-reasoner"

BAZA_DIR = Path(r"c:\Users\Ksawier\Pictures\Screenshots\Projekty_autorskie\useme_core\badania\analizy\technologie\baza_wiedzy")

GRUPY = {
    "1": {
        "nazwa": "Grupa 1: ERP & Integracje Finansowo-Magazynowe",
        "pliki": [
            "tech_02_comarch_optima_ksef.md",
            "tech_03_subiekt_sfera_ecommerce.md",
            "tech_13_enova365_odoo_erp.md"
        ],
        "plik_wyjsciowy": BAZA_DIR / "synteza_bojowa_01_erp.md",
        "opis_grupy": "Comarch Optima, KSeF 2.0 / FA(3), Subiekt GT / nexo PRO Sfera, Enova365, Odoo ERP"
    },
    "2": {
        "nazwa": "Grupa 2: Web Scraping, Automatyzacje B2B & Backend",
        "pliki": [
            "tech_01_scraping_i_boty.md",
            "tech_04_python_fastapi_automatyzacje.md",
            "tech_10_nodejs_nestjs_backend.md",
            "tech_11_csharp_dotnet_b2b.md",
            "tech_14_google_sheets_appscript.md"
        ],
        "plik_wyjsciowy": BAZA_DIR / "synteza_bojowa_02_automatyzacje_i_backend.md",
        "opis_grupy": "Web Scraping anty-WAF/TLS JA4, FastAPI, Celery/Redis, NestJS, .NET 8/9, Apps Script"
    },
    "3": {
        "nazwa": "Grupa 3: Mobile Native, Hardware & VoIP",
        "pliki": [
            "tech_05_kotlin_android_native.md",
            "tech_06_flutter_dart.md",
            "tech_07_swift_ios_native.md",
            "tech_12_voip_asterisk_sip.md"
        ],
        "plik_wyjsciowy": BAZA_DIR / "synteza_bojowa_03_mobile_hardware.md",
        "opis_grupy": "Kotlin/Android (Zebra/BLE), Flutter (Impeller), Swift (StoreKit 2), VoIP Asterisk (PJSIP)"
    },
    "4": {
        "nazwa": "Grupa 4: Infrastruktura, AI & Segment Biznesowy (Tech-Agnostic)",
        "pliki": [
            "tech_08_devops_docker_linux.md",
            "tech_09_sql_optymalizacja_migracje.md",
            "tech_15_ai_llm_rag_pipelines.md",
            "tech_16_tech_agnostic_biznes.md"
        ],
        "plik_wyjsciowy": BAZA_DIR / "synteza_bojowa_04_infra_ai_biznes.md",
        "opis_grupy": "DevOps Linux/Docker, Optymalizacja SQL/Migracje, RAG/AI, Segment Tech-Agnostic (33%)"
    }
}

SYSTEM_PROMPT = """Jesteś Elitarnym Arbitrem Architektonicznym i Głównym Strategiem Systemów Ofertowych B2B / Useme.
Pracujesz w rygorze modelu rozumującego (deep reasoning). Twoim celem jest wykuć bezlitosną, praktyczną KARTĘ BOJOWĄ BOTA OFERTOWEGO.

KONTEKST PROJEKTU I DOWODY Z AUDYTU #144890:
- Budujemy w 100% zautomatyzowanego bota ofertowego na platformę Useme.
- Zbadaliśmy 30 ofert publicznych i 4 oferty prywatne pod zleceniem #144890.
- 90% oferentów to amatorzy piszący generyczne śmieci: "Dzień dobry, chętnie pomogę, mam 5 lat doświadczenia, zapraszam na call / priv". Ich oferty są ignorowane.
- Elita rynkowa (np. ailone, krmob, Adam K na priv) wygrywa kontrakty za 4 500 – 16 000 zł, ponieważ:
  1. Pierwsze 2 zdania oferty mówią o ukrytym problemie klienta, a nie o wykonawcy. W 5 sekund deklasują konkurencję.
  2. Mówią klientowi twardy fakt techniczny, którego klient NIE WIE (np. specyfika protokołu, reguły zaokrągleń, licencje, restrykcje systemowe).
  3. W środek analizy wplatają 2-3 chirurgiczne pytania techniczne/kwalifikujące.
  4. JEDYNY CEL OFERTY: Sprawić, by klient w ciągu 5 minut ODPISAŁ W WIADOMOŚCI PRYWATNEJ.
  5. Zakaz spotkań wideo, calli, telefonów (100% komunikacja pisemna asynchroniczna).
  6. Zakaz udawania mowy potocznej (AI pretend-speech) i tanich trików typu "P.S. pewnie dostałeś 30 ofert z ChatGPT".
"""

def generuj_synteze_dla_grupy(nr_grupy: str):
    if nr_grupy not in GRUPY:
        print(f"[!] Błąd: nieznana grupa {nr_grupy}. Dostępne: {list(GRUPY.keys())}")
        return False
        
    grupa = GRUPY[nr_grupy]
    print(f"\n==========================================================================")
    print(f"[*] URUCHAMIAM MOCNY ŁAŃCUCH REASONING DLA: {grupa['nazwa']}")
    print(f"[*] MODEL: {MODEL}")
    print(f"[*] PLIK DOCELOWY: {grupa['plik_wyjsciowy'].name}")
    print(f"==========================================================================")
    
    # Wczytujemy zawartość kart składowych
    material_kart = ""
    for plik_nazwa in grupa["pliki"]:
        sciezka = BAZA_DIR / plik_nazwa
        if sciezka.exists():
            tresc = sciezka.read_text(encoding="utf-8")
            material_kart += f"\n\n==================== KARTA: {plik_nazwa} ====================\n{tresc}"
        else:
            print(f"[!] Ostrzeżenie: brak pliku {plik_nazwa}")

    prompt_user = f"""ZADANIE DLA MOCNEGO ŁAŃCUCHA ROZUMUJĄCEGO:
Dokonaj głębokiej syntezy architektoniczno-taktycznej poniższych kart wiedzy inżynierskiej dla grupy:
**{grupa['nazwa']}** ({grupa['opis_grupy']}).

MATERIAŁ ŹRÓDŁOWY Z BAZY WIEDZY:
{material_kart}

WYMAGANA STRUKTURA SYNTEZY BOJOWEJ DLA BOTA (ZAPISZ W MARKDOWN):

# SYNTEZA BOJOWA BOTA — {grupa['nazwa'].upper()}
## DOKUMENT OPERACYJNY DLA GENERATORA OFERT USEME

### 1. STRATEGIA DEKLASACJI W PIERWSZYCH 2 ZDANIACH (KATALOG CIOSÓW OTWIERAJĄCYCH)
- Podaj dla każdej technologii z tej grupy gotowe, bezbłędne otwarcie (dokładnie 2 zdania), które:
  * Uderza w newralgiczny punkt techniczny zlecenia.
  * Sprawia, że klient myśli: "ten człowiek wie o moim systemie więcej niż ja".
  * Nie zawiera ani jednego słowa o "doświadczeniu", "chęci pomocy" ani "zaproszeniu do kontaktu".

### 2. TABELA MIN TECHNICZNYCH (CO KLIENT PISZE VS CO GO UTOPI VS RIPOSTA BOTA)
Zestawienie tabelaryczne:
| Technologia | Pozorne życzenie klienta | Prawdziwa mina pod maską | Twardy fakt inżynierski używany przez bota |

### 3. ZESTAW PYTAŃ ZMUSZAJĄCYCH DO ODPOWIEDZI NA PRIV (W ŚRODEK TEKSTU)
- Po 2-3 chirurgiczne pytania dla każdej domeny, sformułowane tak, że klient NIE MOŻE ich zignorować, bo od nich zależy powodzenie projektu.

### 4. CZERWONA LISTA ANTYWZORCÓW (AUTOMATYCZNA DYSKWALIFIKACJA)
- Konkretne zakazy architektoniczne i pojęciowe, których bot pod żadnym pozorem nie może popełnić (np. zakaz direct SQL do ERP, zakaz synchronicznych webhooków, zakaz obietnic tła na iOS bez APNs).

### 5. MODUŁOWE SZABLONY KOSZTORYSÓW DLA ELITY (4 500 - 16 000 ZŁ)
- Jak rozbić etapy prac w tej grupie na 4-6 logicznych modułów architektonicznych, aby wysoka cena wyglądała na w pełni uzasadnioną i profesjonalną.

### 6. WZORCOWA OFERTA BOJOWA 1:1 (BENCHMARK MISTRZOWSKI)
- Przygotuj jedną kompletną, perfekcyjną ofertę dla reprezentatywnego zlecenia z tej grupy. Pokaż jak te wszystkie zasady łączą się w bezwzględnie skuteczną całość gotową wymusić odpowiedź na priv w 5 minut.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_user}
        ],
        "temperature": 0.2,
        "stream": False
    }

    t0 = time.time()
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=300)
        if r.status_code != 200:
            print(f"[!] BŁĄD HTTP {r.status_code}: {r.text[:500]}")
            return False
            
        dane = r.json()
        wynik = dane["choices"][0]["message"]["content"]
        
        grupa["plik_wyjsciowy"].write_text(wynik, encoding="utf-8")
        dt = round(time.time() - t0, 1)
        print(f"[+] SUKCES! Zapisano syntezę do: {grupa['plik_wyjsciowy'].name} ({len(wynik)} znaków) w {dt}s")
        return True
    except Exception as e:
        print(f"[!] WYJĄTEK: {e}")
        return False

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        print("Użycie: python uruchom_mocny_lancuch_grupowy.py <nr_grupy: 1|2|3|4>")
        sys.exit(1)
        
    grupa_arg = sys.argv[1]
    ok = generuj_synteze_dla_grupy(grupa_arg)
    sys.exit(0 if ok else 1)
