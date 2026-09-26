# PLAN: Benchmark ofert — ślepy test na wielu AI

## Cel
Sprawdzić jak nasza oferta (generowana przez bota) wypada na tle konkurencji
z perspektywy KLIENTA symulowanego przez AI. Powtórzyć na wielu modelach AI
żeby zobaczyć co działa uniwersalnie, a co jest specyficzne dla modelu.

## Proces krok po kroku

### Krok 1: Wystawienie zlecenia testowego
- Konto zleceniodawcy na Useme
- Treść z `strategia/mystery_shopping.md` lub `strategia/lista_zlecen_badawczych.md`
- Czekamy 5-7 dni na oferty

### Krok 2: Pobranie ofert
- Skrypt: `pobierz_oferty_zleceniodawcy.py <job_id>`
- Wynik: `badania/baza/<konto>/04_moje_zlecenia/zlecenie_testowe_<job_id>/oferty_publiczne_*.json`

### Krok 3: Wygenerowanie naszej oferty (DRY RUN)
- Uruchomić ofertowarkę na tym zleceniu w trybie DRY_RUN
- Albo: ręcznie wrzucić zlecenie do magazynu i odpalić `engine.py --dry-run`
- Wynik: treść oferty + wycena w magazynie
- WAŻNE: oferta NIE jest wysyłana — zostaje tylko w plikach

### Krok 4: Zanonimizowanie i wrzucenie do puli
- Nasza oferta dostaje pseudonim (np. "team-alpha") zamiast "Ksawier"
- Wrzucona do tego samego JSON co reszta ofert
- AI nie wie która jest nasza

### Krok 5: Ocena przez AI (WIELE MODELI)
Każdy model dostaje TEN SAM prompt (`badania/PROMPT_OCENA_KLIENTA.md`) + te same dane.

Modele do przetestowania:
- DeepSeek V4 Pro (nasz model produkcyjny)
- Claude 3.5/4 Sonnet/Opus
- GPT-4o / GPT-4.1
- Gemini 2.5 Pro
- Llama 3.1 405B (jeśli dostępny)

### Krok 6: Zebranie wyników
Dla każdego modelu zapisujemy:
- Ranking ofert (top 5)
- Zwycięzca
- Powody odrzuceń
- Co irytowało "klienta"
- Czego brakowało
- Czy nasza oferta wygrała/przegrała i dlaczego

### Krok 7: Analiza cross-model
- Które oferty wygrywają NIEZALEŻNIE od modelu? (te techniki działają uniwersalnie)
- Które oferty wygrywają TYLKO na jednym modelu? (specyficzne dla AI)
- Co ZAWSZE odpada? (uniwersalne antywzorce)
- Jak radzi sobie nasza oferta vs średnia?

### Krok 8: Wnioski → aktualizacja promptów bota
- Wyciągnięte wzorce wchodzą do `prompts/kontekst/jak_pisac_oferty.md`
- Wyciągnięte antywzorce wchodzą do `prompts/walidatory/agent_08_weryfikacja_zasad.md`
- Zamknięcie pętli: bot się uczy z benchmarku

---

## Struktura plików

```
badania/
├── PROMPT_OCENA_KLIENTA.md          ← uniwersalny prompt (ten sam dla każdego zlecenia)
│
├── baza/<konto>/04_moje_zlecenia/
│   ├── zlecenie_testowe_144890/
│   │   ├── oferty_publiczne_30.json     ← 36 ofert konkurencji
│   │   ├── nasza_oferta_bot.json        ← oferta wygenerowana przez bota (DRY RUN)
│   │   ├── pula_do_oceny.json           ← 37 ofert (36 + nasza zanonimizowana)
│   │   └── ocena_klienta/
│   │       ├── deepseek_v4.md           ← wynik oceny przez DeepSeek
│   │       ├── claude_sonnet.md         ← wynik oceny przez Claude
│   │       ├── gpt4o.md                 ← wynik oceny przez GPT-4o
│   │       ├── gemini_pro.md            ← wynik oceny przez Gemini
│   │       └── PODSUMOWANIE.md          ← analiza cross-model
│   │
│   └── zlecenie_testowe_XXXXX/          ← kolejne zlecenie testowe (ten sam schemat)
│       ├── oferty_publiczne_*.json
│       ├── nasza_oferta_bot.json
│       ├── pula_do_oceny.json
│       └── ocena_klienta/
│           ├── deepseek_v4.md
│           ├── ...
│           └── PODSUMOWANIE.md
│
└── RAPORT_ZBIORCZY.md               ← wnioski ze WSZYSTKICH zleceń testowych
```

---

## Co zbieramy z każdej rundy

### Tabela wyników (per model, per zlecenie)
| Pytanie | Odpowiedź |
|---|---|
| Ile ofert odpadło w 3 sekundy? | X / Y |
| Ile weszło na shortlistę? | X |
| Czy nasza oferta weszła na shortlistę? | TAK / NIE |
| Która pozycja nasza oferta? | #X z Y |
| Zwycięzca (wybrana oferta) | nick oferenta |
| Dlaczego zwycięzca wygrał? | 1-2 zdania |
| Dlaczego nasza przegrała (jeśli przegrała)? | 1-2 zdania |

### Wzorce do zebrania
1. **Co działa na KAŻDYM modelu** — te techniki wchodzą do promptów bota
2. **Co odpada na KAŻDYM modelu** — te antywzorce wchodzą do walidatora
3. **Co klient chciał przeczytać a nikt nie napisał** — luki do wypełnienia
4. **Jakie elementy budują zaufanie** — rankingowane po częstości

---

## Wyniki zlecenia testowego #144890 (AI/OCR/Optima)

| Pytanie | DeepSeek V4 Pro | Gemini 3.8 Flash Thinking |
|---|---|---|
| Pula ofert | 42 (41 konkurencji + 1 nasza) | 42 (41 konkurencji + 1 nasza) |
| Ile ofert odpadło w 3 sekundy? | 17 / 42 | 14 / 42 |
| Ile weszło na shortlistę? | 5 (ailone, team-alpha, lukasz-glowacz, krmob, marcin-korolko) | 4 (team-alpha, ailone, konrad-szydlowski, craftko-studio) |
| Czy nasza oferta weszła na shortlistę? | **TAK** | **TAK** |
| Która pozycja nasza oferta? | **#2 z 42 (Runner-up)** | **#1 z 42 (ZWYCIĘZCA 🏆)** |
| Zwycięzca (wybrana oferta) | `#16 ailone` (10 500 zł) | **`#13 team-alpha` (17 000 zł — NASZ BOT)** |
| Dlaczego zwycięzca wygrał? | Cena w budżecie, KSeF, zaokrąglenia VAT (zastrzeżenie: brak ProfiPieka) | Zauważenie specyfiki ProfiPieka (brak API), licencje Optimy, Demo Guard |
| Dlaczego nasza przegrała na DeepSeek? | Jedynie cena (17 000 zł vs mentalny budżet 15 000 zł) — uznana za najlepszą merytorycznie | — (WYGRAŁA) |

---

## Status

| Zlecenie | Oferty | Nasza oferta | Oceny AI | Analiza |
|---|---|---|---|---|
| #144890 (AI/OCR/Optima) | 41 publiczne + 6 priv ✅ | Wygenerowana (17k/30d) ✅ | DeepSeek + Gemini ✅ | **Zakończona (#1 Gemini, #2 DeepSeek)** ✅ |
| #2 BaseLinker/Subiekt | ⬜ do wystawienia | ⬜ | ⬜ | ⬜ |
| #3 Konfigurator 3D | ⬜ do wystawienia | ⬜ | ⬜ | ⬜ |
| #4 Scraping | ⬜ do wystawienia | ⬜ | ⬜ | ⬜ |
| #5 Panel B2B | ⬜ do wystawienia | ⬜ | ⬜ | ⬜ |
