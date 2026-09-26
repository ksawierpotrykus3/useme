# KROK 2: Selekcja i Triage Zleceń (Filtry Twarde + AI Selector)

Moduł odpowiadający za odrzucenie spamu, zleceń niemożliwych do realizacji oraz segregację na priorytety marżowe.

---

## 1. Twarde Filtry Deterministyczne (Przed AI)

Przed wysłaniem zapytań do modelu AI działają bezwzględne reguły bezpieczeństwa w [`kod/engine.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/engine.py#L227-L254):

1. **Blokada Własnych Kont i Profili**:
   - Sprawdzenie `author_id` oraz `author` względem listy wykluczeń (`config.BLOCKED_AUTHORS`, np. profil `wer13`).
   - Zapobiega składaniu ofert na własne zlecenia testowe. Status: `ODRZUCONA_WLASNY_PROFIL`.
2. **Filtr Anty-Tłum (Limit Konkurencji)**:
   - Jeśli liczba złożonych ofert przekracza `MAX_COMPETITOR_LIMIT` (domyślnie **60 ofert**), zlecenie jest automatycznie odrzucane.
   - Status: `ODRZUCONA_TLUM`.
   - *Wyjątek (Fast-Track VIP)*: Jeśli zlecenie zawiera słowa kluczowe z nisz wysokomarżowych (np. CAD, CAM, TopSolid, ERP, Enova, bot, scraping, reverse engineering), limit tłumu zostaje zignorowany.

---

## 2. Selekcjoner AI (`filter_offers` w `ai_pipeline.py`)

Zlecenia, które przeszły filtry deterministyczne, trafiają w paczce do wyspecjalizowanego agenta AI:
- **Model**: `deepseek-v4-pro-nothink` (model zoptymalizowany pod szybką klasyfikację JSON bez narzutu tokenów myślenia CoT).
- **Wejście**: Tytuły, budżety i pełne opisy nowych zleceń + reguły z [`selekcja_zlecen.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/selekcja_zlecen.md) oraz [`stack_i_filozofia.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/kontekst/stack_i_filozofia.md).
- **Format Odpowiedzi**:
  ```json
  [
    {
      "id": "144890",
      "werdykt": "BIERZEMY",
      "tier": "TIER_A",
      "powod": "Dedykowany scraper z ominięciem Cloudflare, wysoka marża, idealny stack Python"
    }
  ]
  ```

---

## 3. Priorytetyzacja Kolejki (Tiering)

- **Tier A (Wysoka Marża / Nisze Techniczne)**:
  - Automatyzacje, scraping, reverse engineering, integracje API, systemy ERP, aplikacje mobilne (Kotlin/Flutter).
  - Umieszczane na samym początku kolejki generowania i wysyłki.
- **Tier B (Zlecenia Standardowe)**:
  - Dedykowane skrypty PHP/Python, rozbudowa sklepów Shopify/PrestaShop, poprawki bazodanowe.
- **Odrzucone (ODRZUCONA_AI)**:
  - Zlecenia wymagające fizycznej obecności, rekrutacje na etat (B2B/UoP ukryte pod zleceniem), pisanie artykułów SEO, budżety absurdalne (< 100 PLN za miesiąc pracy).
