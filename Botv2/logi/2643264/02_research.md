## Wyniki researchu

### 1. API Allegro – ceny konkurencji i limity

**Dostęp do cen konkurencji:** Publiczny endpoint `GET /offers/listing` wymaga weryfikacji aplikacji (zwraca 403 Forbidden z kodem `VerificationRequired`). Jest to wewnętrzne narzędzie do monitorowania cen konkurencji i automatycznej korekty cen w zdefiniowanych widełkach min/max.

**Limity zapytań:** Główny limit nakładany na Client ID to **9000 zapytań na minutę**. Po przekroczeniu następuje blokada na minutę i odpowiedź `429 Too Many Requests`. Dla niektórych zasobów stosowane są dodatkowe, niższe limity, a dla wybranych zasobów działa mechanizm Leaky Bucket ograniczający liczbę zapytań na użytkownika (user.id) na minutę.

**Ważne:** Monitorowanie cen konkurencji przez oficjalne API Allegro **nie jest dostępne bez weryfikacji aplikacji**. Alternatywnie BaseLinker oferuje moduł cenotworzenia dla Allegro (limit bezpłatnego sprawdzania cen: 1000 ofert dziennie na wszystkie konta w ramach marketplace'u Allegro).

---

### 2. Amazon SP-API – limity i wymagania

**Algorytm limitów:** SP-API używa algorytmu **Token Bucket**. Każde żądanie zużywa jeden token. Tokeny są uzupełniane z określoną szybkością (rate limit) aż do maksymalnego rozmiaru (burst limit). Gdy bucket jest pusty, żądanie zostaje ograniczone (throttled).

**Czynniki wpływające na limity:** Rate i burst limit zależą od: konkretnej operacji API, konta sprzedawcy, aplikacji wywołującej API oraz regionu/Amazon store.

**Praktyczne widełki:** Limity wahają się od **0,1 do 100 żądań na sekundę** w zależności od endpointu. Wymagana jest autoryzacja OAuth 2.0 z rolami IAM i podpisywanie AWS SigV4.

**Wymagania aplikacji:** SP-API to nie jest zwykły klucz API — wymaga zatwierdzonej aplikacji i zgodności z politykami Amazon.

---

### 3. BaseLinker API – integracja

**Możliwości:** BaseLinker łączy się przez API z Allegro, Amazon, eBay i in. (integracja dwukierunkowa). Oferuje metodę `getInventoryProductsData` do pobierania szczegółowych danych produktów, w tym ASIN, EAN, SKU, cen, stanów magazynowych, kategorii marketplace'owych oraz mediów per kanał (np. osobne obrazy dla `amazon_0` i `allegro_123`).

**Limit API:** BaseLinker ma limit **100 żądań na minutę**. Pobieranie danych z magazynu BaseLinker odbywa się w paginacji po **1000 produktów na stronę**.

**AI w BaseLinker:** System oferuje integrację własnego modelu AI wytrenowanego na milionach ofert oraz automatyczne generowanie opisów sekcyjnych dla Allegro i bullet points dla Amazon.

---

### 4. Koszty tokenów LLM

**GPT-4o:**
| Źródło | Input / 1M tokenów | Output / 1M tokenów | Cached input / 1M |
|---|---|---|---|
| ScienceDirect (Aug 2024) | $2,50 | $10,00 | $1,35 |
| HuggingFace | $3,00 | $10,00 | — |
| GitHub (Oct 2025) | $2,50 | $10,00 | — |
| arXiv (Maj 2025) | $5,00 | $15,00 | — |

Różnice w cenniku wynikają z różnych okresów pomiaru i modeli (base vs. fine-tuned vs. wersje datowane).

**Gemini Pro (2.5):**
- Input: **$1,25–$2,50** / 1M tokenów
- Output: **$10,00–$15,00** / 1M tokenów

**Gemini 3 Pro (preview):**
- Input: **$2,00** / 1M tokenów
- Output: **$12,00** / 1M tokenów
- Dla promptów ≤ 200k tokenów

---

### 5. Amazon Brand Registry a A+ Content

**Wymagania twarde:** A+ Content (w tym Premium A+) jest dostępne **wyłącznie dla sprzedawców zarejestrowanych w Amazon Brand Registry**. Wymagany jest zastrzeżony znak towarowy i rola Brand Representative lub Reseller przypisana do marki w Brand Registry. Bez Brand Registry moduł A+ **nie zadziała** — pozostaje zwykła optymalizacja opisów.

**Premium A+ – dodatkowe kryteria:**
1. Opublikowana Brand Story dla wszystkich ASIN-ów marki
2. Co najmniej **5 modułów A+ zatwierdzonych i opublikowanych w ciągu ostatnich 12 miesięcy**
3. Automatyczna comiesięczna weryfikacja przez Amazon

**Dostęp przez API:** Selling Partners i deweloperzy mogą tworzyć, zarządzać i uzyskiwać dostęp do A+ Content programowo przez SP-API.

---

### Niepotwierdzone / do weryfikacji

- **Koszt tokenów dla 400 SKU** — brak konkretnych wyliczeń; zależy od częstotliwości optymalizacji, długości promptów i modelu. Wymaga oszacowania na podstawie rzeczywistych danych.
- **Aktualny cennik GPT-4o** — rozbieżności między źródłami; rekomendowana weryfikacja bezpośrednio na stronie OpenAI.
- **Szczegółowe limity per operacja SP-API** — dokumentacja podaje mechanizm, ale konkretne wartości per endpoint wymagają sprawdzenia w dokumentacji referencyjnej każdej operacji.
- **Czy BaseLinker zastępuje bezpośrednie API Allegro/Amazon dla wszystkich funkcji** — potwierdzona integracja dwukierunkowa, ale zakres funkcjonalny (np. czy obsługuje pełne listowanie z A+ Content) nie został zweryfikowany w źródłach.