# AI Łańcuch – system slotów (plug-and-play)

> Architektura pozwalająca dodawać/usuwać agentów AI w łańcuchu bez grzebania w kodzie.
> Jeden łańcuch = jedno zlecenie. 5 zleceń = 5 łańcuchów (każdy może mieć do 20 agentów).

---

## Koncepcja

Każdy agent AI to osobny "slot" – numerowane od `01` do `20`. Sloty są niezależne. Łańcuch odpala je sekwencyjnie, output jednego wchodzi do następnego + oryginalne dane zlecenia.

**Każdy agent zawsze widzi:**
- Oryginalne dane zlecenia (zawsze dostępne)
- Outputy wszystkich poprzednich slotów (po kluczach)
- Swój własny prompt (opcjonalnie – z pliku `.md`)
- Dodatkowe pliki kontekstowe (opcjonalnie – lista plików `.md`/`.txt`)

**Agent może działać bez własnych plików** – wystarczy mu to co dostał od poprzedników + dane zlecenia. Nie każdy musi mieć `prompt_file`.

**Włączanie/wyłączanie:** każdy slot ma w konfiguracji flagę `enabled: true/false`. Wyłączone sloty są pomijane.

**Dodawanie nowego agenta:** dodajesz wpis w `chain_config.json`. Jeśli potrzebuje prompta – tworzysz plik `.md` i podajesz ścieżkę. Jeśli nie – pomijasz `prompt_file`. Gotowe. Zero grzebania w Pythonie.

---

## Struktura plików

```
prompts/
├── generatory/
│   ├── prompt_ai1.md            # AI #1 – selekcja ofert (Krok 3)
│   ├── agent_00_orchestrator.md # Slot 00 – plan strategii oferty
│   ├── agent_01_research.md     # Slot 01 – research sieciowy
│   ├── agent_02a_opis_oferty.md # Slot 02a – treść oferty
│   └── agent_02b_wycena_dni.md  # Slot 02b – wycena + dni pracy
├── walidatory/
│   ├── agent_08_weryfikacja_zasad.md  # Slot 08 – weryfikator zasad (aktywny)
│   ├── kryteria_audytu_100.md         # kryteria sędziego 1-100 (audytor_lancuch.py)
│   └── sedzia_zdrowego_rozsadku.md    # drugi sędzia (audytor_lancuch.py)
└── kontekst/
    └── ...                      # lore, mechanika, scenariusze klientów, karty wiedzy

chain_config.json              # Konfiguracja slotów
```

---

## chain_config.json – format

```json
{
  "retry_max": 3,
  "slots": [
    {
      "id": "02b",
      "name": "Wycena i dni",
      "prompt_file": "agent_02b_wycena_dni.md",
      "context_files": ["lore.md", "mechanika_wyceniania.md"],
      "enabled": true,
      "role": "generator",
      "output_key": "wycena_dni"
    },
    {
      "id": "02a",
      "name": "Opis oferty",
      "prompt_file": "agent_02a_opis_oferty.md",
      "context_files": ["lore.md", "jak_pisac_oferty.md"],
      "enabled": true,
      "role": "generator",
      "output_key": "opis",
      "requires": ["wycena_dni"]
    },
    {
      "id": "03",
      "name": "Walidator opisu",
      "prompt_file": "agent_03_walidator_opisu.md",
      "context_files": ["lore.md", "zasady_wyceny.md"],
      "enabled": false,
      "role": "validator",
      "requires": ["opis"],
      "on_fail": "retry_from_02a"
    },
    {
      "id": "04",
      "name": "Spójność oferty",
      "enabled": false,
      "role": "validator",
      "requires": ["opis", "wycena_dni"],
      "on_fail": "abort"
    }
  ]
}
```

**Pola:**
- `id` – identyfikator slotu (string, np. "02a", "03")
- `name` – ludzka nazwa (do logów)
- `prompt_file` – (opcjonalny) ścieżka do pliku `.md` z promptem. Jeśli brak – agent działa tylko na danych z kontekstu
- `context_files` – (opcjonalny) lista dodatkowych plików `.md`/`.txt` dołączanych jako wiedza
- `enabled` – `true` = aktywny, `false` = pomijany
- `role` – `generator` (tworzy treść) lub `validator` (sprawdza i daje PASS/FAIL)
- `output_key` – klucz pod którym output trafia do kontekstu (dla generatorów)
- `requires` – lista kluczy outputów potrzebnych do działania (dla walidatorów)
- `on_fail` – co robić gdy validator da FAIL:
  - `retry_from_02a` – wróć do AI #2a i popraw
  - `retry_from_02b` – wróć do AI #2b i popraw
  - `abort` – zatrzymaj łańcuch, zgłoś człowiekowi

---

## Jak działa łańcuch (przetwarzanie)

Dla jednego zlecenia:

```
START ŁAŃCUCHA
  │
  ▼
[DANE ZLECENIA]
  │
  ▼
[Slot 01] Research sieciowy → output: "research"
  │
  ▼
[Slot 02b] Wycena + dni → output: "wycena_dni"
  │
  ▼
[Slot 00] Orchestrator strategii → output: "orchestrator_plan"
  │
  ▼
[Slot 02a] Treść oferty (dostaje research + wycenę + plan) → output: "opis"
  │
  ▼
[Slot 08] Weryfikator zasad → sprawdza treść i wycenę
  │
  ├── PASS → ✅ ŁAŃCUCH OK
  └── FAIL → retry od 02a lub 02b (max 2 rundy) → jeśli nadal FAIL, akceptacja najlepszej wersji
  │
  ▼
[AUDYTOR 1-100] (audytor_lancuch.py) → sędzia 1-100 + Sędzia Zdrowego Rozsądku, próg 92
  │
  ▼
[Krok 6] WERYFIKACJA CZŁOWIEKA
```

> **Kolejność 02b → 02a (wycena przed treścią):** wycena liczy się z samych danych zlecenia, nie potrzebuje treści. Treść natomiast musi znać kwotę i dni, żeby wpisać je naturalnie w sekcji wyceny oferty. Dlatego najpierw 02b produkuje `wycena_dni`, potem 02a je konsumuje jako input (`requires: ["wycena_dni"]`) i nie zmienia kwoty.

**Każde AI widzi:**
- Oryginalne dane zlecenia (zawsze dostępne)
- Outputy wszystkich poprzednich slotów (po kluczach)
- Swój własny prompt (jeśli ma `prompt_file`)
- Dodatkowe pliki (jeśli ma `context_files`)

**Retry:** jeśli validator da FAIL i `on_fail: "retry_from_*"`, łańcuch wraca do wskazanego generatora. Max 3 próby (`retry_max`). Po 3 failach – abort.

---

## Jak Playwright odpala łańcuch

```python
# Pseudokod – nie implementacja
def run_chain(zlecenie_dane, chain_config):
    context = {"zlecenie": zlecenie_dane}
    
    for slot in chain_config["slots"]:
        if not slot["enabled"]:
            continue
        
        prompt = read_file(f"prompts/{slot['prompt_file']}")
        lore = read_file("prompts/lore.md")
        
        response = deepseek_api.call(
            prompt=prompt,
            lore=lore,
            context=context
        )
        
        if slot["role"] == "generator":
            context[slot["output_key"]] = response
        
        elif slot["role"] == "validator":
            if response == "PASS":
                continue
            else:
                return handle_fail(slot, context, chain_config)
    
    return context  # zawiera "opis" i "wycena_dni" do formularza
```

---

## Aktywne sloty

| Slot | Nazwa | Rola | Co robi |
|---|---|---|---|
| 01 | Research sieciowy | generator | Zbiera fakty z sieci (API, stawki, progi) z dowodami |
| 02b | Wycena i dni | generator | Proponuje stawkę i liczbę dni |
| 00 | Orchestrator strategii | generator | Plan odpowiedzi, blokady anty-szablonowe |
| 02a | Treść oferty | generator | Pisze treść propozycji |
| 08 | Weryfikator zasad | validator | Sprawdza treść, wycenę i fakty z researchu (PASS/FAIL) |

Po łańcuchu działa jeszcze **Audytor 1-100** (`audytor_lancuch.py`): niezależny sędzia punktowy (`kryteria_audytu_100.md`) plus **Sędzia Zdrowego Rozsądku** (`sedzia_zdrowego_rozsadku.md`), próg zaliczenia 92/100.

> Historyczne sloty walidatorów 03-07 i 20 zostały usunięte jako nieużywane. Jedynym walidatorem łańcucha jest slot 08.

---

## Zasady

1. **Jeden łańcuch = jedno zlecenie.** Nie mieszamy kontekstów między zleceniami.
2. **Aktywne sloty to 01, 02b, 00, 02a i 08.** Reszta numeracji jest wolna dla przyszłych agentów.
3. **Kolejność ma znaczenie.** Sloty są przetwarzane w kolejności z `chain_config.json`.
4. **Validator FAIL nie kasuje outputu.** Output generatora zostaje w kontekście, validator tylko blokuje przejście dalej.
5. **Pliki promptów to zwykłe `.md`.** Możesz je edytować w dowolnym edytorze tekstowym.