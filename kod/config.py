# -*- coding: utf-8 -*-
"""Konfiguracja główna silnika useme_core."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
BADANIA_DIR = BASE_DIR.parent / "badania"
STRATEGIA_DIR = BADANIA_DIR / "strategia"

# --- BAZA ZLECEN (jedno zrodlo prawdy) ---
# Struktura: badania/baza/<konto>/<podzial>/
BAZA_DIR = BADANIA_DIR / "baza"
KONTO1_ID = "ksawierpotrykus3"
KONTO2_ID = "weronikabuchholc13"
KONTO1_DIR = BAZA_DIR / KONTO1_ID
KONTO2_DIR = BAZA_DIR / KONTO2_ID

# Podzialy w bazie
MAGAZYN_DIR = KONTO1_DIR / "01_ofertowarka"      # zlecenia pobrane przez bota (konto wykonawcy)
PRZEGRANE_DIR = KONTO1_DIR / "02_przegrane"      # z nots/ (klient nie odpisal)
ODPISANE_DIR = KONTO1_DIR / "03_odpisane"        # z mesg/ (klient odpisal)
# Moje zlecenia testowe naleza do KONTA ZLECENIODAWCY (weronikabuchholc13),
# bo to z tego konta wystawiamy zlecenia badawcze i zbieramy oferty/wiadomosci.
MOJE_ZLECENIA_DIR = KONTO2_DIR / "04_moje_zlecenia"
PACZKI_DIR = KONTO1_DIR / "_paczki_i_probki"     # analizy zbiorcze, probki

MARKER_FILE = MAGAZYN_DIR / "marker.json"
COOKIES_PATH = BASE_DIR / "tech" / "cookies.json"
DEBUG_DIR = BASE_DIR / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)
for _d in (MAGAZYN_DIR, PRZEGRANE_DIR, ODPISANE_DIR, MOJE_ZLECENIA_DIR, PACZKI_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --- Konta (multi-account) ---
# Miejsce na 2 konta. Konto 1 = dotychczasowe (tech/cookies.json).
# Konto 2 = tech/cookies2.json (wystarczy wrzucić plik, wtedy się aktywuje).
# Jeśli plik cookies nie istnieje -> konto jest pomijane i wszystko działa
# dokładnie tak, jak działało do tej pory (1 konto).
ACCOUNTS = [
    {
        "id": "konto1",
        "nazwa": "Ksawier",
        "podpis": "Ksawier",
        "cookies_path": BASE_DIR / "tech" / "cookies.json",
    },
    {
        "id": "konto2",
        "nazwa": "Konto 2",
        "podpis": "Maksymilian",
        "cookies_path": BASE_DIR / "tech" / "cookies2.json",
    },
]


def aktywne_konta() -> list:
    """Zwraca konta, które mają realnie plik cookies.

    Puste miejsce (brak cookies2.json) -> zwracana jest tylko lista z kontem 1,
    czyli zachowanie identyczne jak przed dodaniem multi-konta.
    """
    return [k for k in ACCOUNTS if Path(k["cookies_path"]).exists()]

# Kategorie monitorowane
CATEGORY_URLS = {
    "programowanie-i-it": "https://useme.com/pl/jobs/category/programowanie-i-it,35/",
    "serwisy-internetowe": "https://useme.com/pl/jobs/category/serwisy-internetowe,34/",
}

# Twarde flagi bezpieczeństwa
TIMEOUT_DNI = 3
DRY_RUN = False         # False: tryb wysyłki na żywo po autoryzacji użytkownika
USE_MOCK_AI = False     # False: uruchamia pełny uodporniony łańcuch AI ze slotami i DeepSeek
HEADLESS = False        # False: tryb z oknem (omija Cloudflare na formularzu ofert)

# Limity i timeouty
NAV_TIMEOUT_MS = 45000
WAIT_AFTER_PAGE_LOAD_S = 3
MAX_OFFERS_PER_CATEGORY = 40
MIN_WORK_DAYS = 7       # Wymóg biznesowy Useme: minimum 7 dni pracy

# Limit konkurencji Anty-Tłum (powyżej 60 ofert odrzucamy, chyba że to Tier A / VIP)
MAX_COMPETITOR_LIMIT = 60

# Słowa kluczowe Fast-Track VIP (Tier A / wysoka marża / natychmiastowy priorytet w kolejce)
VIP_FAST_TRACK_KEYWORDS = [
    "ai", "llm", "n8n", "make", "baselinker", "konfigurator", "three.js", 
    "webgl", "idosell", "ksef", "erp", "scraping", "ocr", "topsolid", "cnc", "cad",
    "enova", "subiekt", "optima", "kotlin", "flutter",
    "klinika", "gabinet", "kancelaria", "komornik", "medyczn", "księgi wieczyste"
]

# Słowa kluczowe pułapek ogłoszeniowych (ukryta rekrutacja na etat / bezbudżetowe equity)
TRAP_KEYWORDS = [
    "umowa o pracę", "pełny etat", "na stałe do zespołu", "szukam wspólnika za udziały",
    "praca stacjonarna w biurze", "rekrutacja do działu"
]

# --- TWARDY FILTR CZERWONEGO OCEANU (HARD_REJECT_PATTERNS) ---
# Zlecenia odrzucane deterministycznie przed AI (oraz w fallbacku przy timeoucie AI #1),
# chyba że zawierają słowa kluczowe VIP (ERP, KSeF, AI/LLM, n8n, BaseLinker, Three.js, CNC).
HARD_REJECT_PATTERNS = [
    r"\b(?:wizyt[óo]wk[aęi]|prost[aąe]\s+stron[aę]|stron[aę]\s+na\s+wordpress(?:ie)?|motyw\s+wordpress|elementor|divi|wpbakery)\b",
    r"\b(?:prowadzenie\s+(?:profilu|fanpage|social\s+media|instagrama|tiktoka)|copywriting|pisanie\s+artyku[łl][óo]w)\b",
    r"\b(?:kampani[aei]\s+(?:google\s+ads|facebook\s+ads|meta\s+ads)|pozycjonowanie\s+seo\s+wizyt[óo]wki)\b",
    r"\b(?:projekt\s+ulotki|projekt\s+logo|grafika\s+w\s+canvie|monta[żz]\s+rolek\s+na\s+instagram)\b",
]

# Wzorce ostrzegawcze Phantom Leads (rozmyte wizje "systemu od wszystkiego" / klony gigantów)
PHANTOM_PATTERNS = [
    r"\b(?:klon\s+(?:ubera|allegro|books[y]|airbnb|olx)|system\s+operacyjny\s+ai\s+dla\s+ca[łl]ej\s+firmy)\b",
    r"\b(?:d[łl]ugofalowa\s+wsp[óo][łl]praca\s+przy\s+niskiej\s+cenie\s+na\s+start|udzia[łl]\s+w\s+zyskach\s+zamiast)\b",
]

# Bramka produkcyjna Niezależnego Audytora 1-100 pkt (audytor_lancuch.py)
USE_AUDYTOR_100 = True
AUDYTOR_100_TARGET_SCORE = 92


def is_hard_reject(title: str = "", description: str = "") -> str | None:
    """Zwraca powód odrzucenia, jeśli zlecenie wpada w Czerwony Ocean i nie ma słów VIP."""
    import re as _re
    full_text = f"{title or ''} {description or ''}".lower()
    for tk in TRAP_KEYWORDS:
        if tk in full_text:
            return f"TRAP_KEYWORD: {tk}"
    # Jeśli zlecenie zawiera twardy sygnał VIP (np. ERP, KSeF, AI, BaseLinker, Three.js, CNC), nie odrzucamy go regexem
    if any(vip in full_text for vip in VIP_FAST_TRACK_KEYWORDS):
        return None
    for pat in HARD_REJECT_PATTERNS:
        m = _re.search(pat, full_text, flags=_re.IGNORECASE)
        if m:
            return f"HARD_REJECT_RED_OCEAN: {m.group(0)}"
    return None

# --- CZARNA LISTA AUTORÓW (Własne profile / zleceniodawcy wykluczeni) ---
# Zakaz składania ofert na zlecenia pochodzące od tych autorów (np. własny profil zleceniodawcy 'wer13').
BLOCKED_AUTHORS = [
    "wer13",
]


def is_blocked_author(author_id: str | None, author_name: str | None = "") -> bool:
    """Sprawdza czy zleceniodawca znajduje się na liście wykluczonych (np. własne profile)."""
    import re as _re
    blocked = {a.strip().lower() for a in BLOCKED_AUTHORS if a}
    if author_id and str(author_id).strip().lower() in blocked:
        return True
    if author_name:
        name_clean = str(author_name).strip().lower()
        if name_clean in blocked:
            return True
        slug = _re.sub(r"[^\w\s-]", "", name_clean).strip()
        slug = _re.sub(r"[\s_]+", "-", slug)
        if slug in blocked:
            return True
    return False

# --- BEZPIECZEŃSTWO OPERACYJNE ---
# Brak limitu dziennego (MAX_OFFERS_PER_DAY usunięte).
# Zasada deduplikacji i segmentacji domenowej: dane zlecenie otrzymuje maksymalnie jedną
# ofertę, a wybór konta następuje wg profilu (Konto 1: Tier A / AI / architektura, Konto 2: Tier B/C).

# Maksymalny czas jednego uruchomienia (minuty). Po przekroczeniu run sie konczy.
MAX_RUN_MINUTES = 180

# Kill switch: jesli ten plik istnieje, pipeline NIE startuje (ani nie wysyla).
# Tworzysz go recznie, zeby natychmiast zatrzymac bota.
STOP_FILE = BASE_DIR / "STOP"

# Naturalny odstęp między ofertami (3s) chroniący przed burst detection.
MIN_DELAY_BETWEEN_OFFERS_S = 3

# Bezpieczne zakresy opóźnień anty-banowych (sekundy z jitterem) - Golden Ratio (18-26s)
INTER_JOB_DELAY_RANGE = (25.0, 40.0)    # Odstęp między kolejnymi zleceniami (regeneracja puli)
INTER_SLOT_DELAY_RANGE = (18.0, 25.0)   # Odstęp między slotami AI w łańcuchu (1.5 req/min)
RESEARCH_COOLDOWN_RANGE = (20.0, 28.0)  # Odstęp po zakończeniu slotu badawczego z searchem

# Maksymalna dlugosc opisu oferty (znaki). Zabezpieczenie przed wypluciem
# gigantycznego tekstu przez model (i przed kosztownym promptem).
MAX_OPIS_DLUGOSC = 6000

# --- ZBIERACZ DANYCH (weryfikacja odpowiedzi klienta) ---
# UWAGA: selektory DOM w BrowserDriver.sprawdz_skrzynke / sprawdz_powiadomienia
# sa NIEPOTWIERDZONE na realnym DOM Useme (patrz komentarze w browser_driver.py).
# Na czas nieobecnosci (wakacje) trzymamy zbieracz WYLACZONY, zeby nie ryzykowac
# awarii i falszywych statusow. Wlacz na True dopiero po recznej weryfikacji
# selektorow na zywym Useme. Wysylanie ofert dziala niezaleznie od tej flagi.
ZBIERACZ_AKTYWNY = False

# Tryb oferty: tryb meta całkowicie wyłączony, zawsze konserwatywny
DOMYSLNY_TRYB = "konserwatywny"

