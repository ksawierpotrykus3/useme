# KROK 4: Pipeline Generacji AI (System Slotów i Architektura Treści)

Moduł generujący precyzyjną, profesjonalną treść oferty przy użyciu łańcucha modeli AI skoordynowanego przez [`kod/chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py).

---

## 1. Architektura Sekwencyjna Slotów ([`chain_config.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/chain_config.json))

Dla każdego zakwalifikowanego zlecenia uruchamiany jest ciąg dedykowanych agentów:

```
[Nowe Zlecenie]
       │
       ▼
┌──────────────────────────────────────────────┐
│ Slot 01: Agent 01 - Research Sieciowy        │  Model: deepseek-v4-pro-search
│ Zbiera fakty: API, dokumentacje, ryzyka      │
└──────────────────────────────────────────────┘
       │
       ▼  (przekazuje: research)
┌──────────────────────────────────────────────┐
│ Slot 02b: Agent 02b - Wycena i Liczba Dni     │  Model: deepseek-v4-pro
│ Oblicza kwotę i dni zgodnie z kalkulatorem   │
└──────────────────────────────────────────────┘
       │
       ▼  (przekazuje: wycena_dni, research)
┌──────────────────────────────────────────────┐
│ Slot 02a: Agent 02a - Treść Oferty           │  Model: deepseek-v4-pro
│ Generuje finalny tekst (maks. 190 słów)      │
└──────────────────────────────────────────────┘
       │
       ▼  (przekazuje: opis, wycena_dni, research)
┌──────────────────────────────────────────────┐
│ Slot 08: Agent 08 - Bramka Walidatora Zasad  │  Model: deepseek-v4-pro
│ Sprawdza zgodność z twardymi regułami        │
└──────────────────────────────────────────────┘
```

---

## 2. Odpowiedzialności Agentów

### Slot 01: Agent Researchu Sieciowego (`agent_01_research.md`)
- Korzysta z wyszukiwarki internetowej i modelu `deepseek-v4-pro-search`.
- Wyciąga dokładne parametry techniczne: limity darmowych tierów API, dokumentację webhooków, biblioteki dedykowane, znane problemy wersji CMS klienta.
- Efekt: W ofercie Ksawier nie pisze ogólników (*"znam API"*), lecz konkret (*"zgodnie z limitem 100 req/min w API InPostu zastosujemy mechanizm buforowania w Redis/SQLite"*).

### Slot 02b: Agent Wyceny i Dni (`agent_02b_wycena_dni.md`)
- Generuje strukturę `[WYCENA_JSON]` z rozbiciem na liczbę godzin, stawkę za godzinę, liczbę dni oraz uzasadnienie techniczne.

### Slot 02a: Agent Treści Oferty (`agent_02a_opis_oferty.md`)
- Buduje treść oferty w oparciu o wytyczne z [`jak_pisac_oferty.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/jak_pisac_oferty.md), [`lore.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/lore.md) oraz [`portfolio_baza.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/portfolio_baza.md).

---

## 3. Żelazne Zasady Treści Oferty

1. **Długość**: Maksymalnie **190 słów** (zwięzłość inżynierska; długa ściana tekstu jest pomijana przez zabieganego klienta).
2. **Format**: Czysty tekst bez formatowania Markdown (`**`, `#`, `- `).
3. **Struktura 4 Akapitów**:
   - Akapit 1: Diagnoza sedna problemu zlecenia (bez lania wody i wstępów typu *"Chętnie podejmę się..."*).
   - Akapit 2: Konkretna ścieżka realizacji (techniczna lub narzędziowa w zależności od klasyfikacji Dual-Track).
   - Akapit 3: Zabezpieczenie przed ryzykiem (brak przestoju, idempotencja, kopia zapasowa, sanity-check).
   - Akapit 4: **Question CTA** (pytanie z opcjami A/B) + Podpis *"Pozdrawiam, Ksawier"*.
4. **Anty-Powtórka (Dla powracających klientów)**:
   - Jeśli klient (`author_id`) otrzymał już wcześniej ofertę od Ksawiera, system wstrzykuje `previous_offers` i wymusza inny kąt natarcia (variation seed).
