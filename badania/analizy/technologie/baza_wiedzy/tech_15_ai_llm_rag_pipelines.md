# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME

## TEMAT: Architektury RAG (Retrieval-Augmented Generation), Wyszukiwanie Hybrydowe, Bazy Wektorowe (Qdrant / pgvector), Integracje LLM (OpenAI, Claude, DeepSeek) i Optymalizacja Kosztów Tokenów

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

**Budżety:** 4 500 – 16 000 zł

**Typowe zlecenia na Useme w tej kategorii:**
- „Chatbot odpowiadający na pytania na podstawie dokumentów firmowych" (budżet 4 500–7 000 zł)
- „System wyszukiwania semantycznego w bazie produktów / regulaminów / umów" (budżet 7 000–11 000 zł)
- „Asystent AI zintegrowany z CRM/ERP z cytowaniem źródeł" (budżet 11 000–16 000 zł)
- „Optymalizacja istniejącego rozwiązania RAG — redukcja kosztów API i poprawa trafności" (budżet 5 500–9 000 zł)

**Profil zleceniodawcy:**
- **Firmy e-commerce / SaaS** — potrzebują wyszukiwarki produktowej, obsługi klienta opartej na bazie wiedzy
- **Kancelarie prawne / firmy doradcze** — wymagają cytowania źródeł i zerowej tolerancji dla halucynacji
- **Działy wewnętrzne (HR, IT, compliance)** — chat wewnętrzny na bazie polityk i procedur
- **Startupy AI** — budowa MVP produktu RAG, często z presją na koszty tokenów

**Realistyczne oczekiwania klientów:** odpowiedzi z cytowaniem dokumentów źródłowych, praca na dokumentach w języku polskim, integracja z istniejącymi systemami (API), kontrola kosztów operacyjnych.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1. Naiwny RAG vs Hybrydowy RAG + Reranker

**Naiwny RAG** (proste osadzenie dokumentów w bazie wektorowej, top-k podobieństwa kosinusowego, wstrzyknięcie do promptu) w 2026 roku jest architekturą **nieprodukcyjną**. Czyste wyszukiwanie gęste (dense-only) zostało wycofane w większości poważnych wdrożeń, ponieważ tryby awarii modeli embeddingowych na encjach (SKU, ID zgłoszeń, nazwy klauzul, sygnatury metod) są zbyt kosztowne w skali.

**Standardem produkcyjnym jest hybrydowy RAG**, łączący:
- **Wyszukiwanie rzadkie (sparse) — BM25**: precyzyjne dopasowanie identyfikatorów, kodów, nazw własnych
- **Wyszukiwanie gęste (dense) — wektory**: dopasowanie semantyczne, parafrazy, synonimy
- **Fuzja wyników — Reciprocal Rank Fusion (RRF)**: łączenie rankingów z obu gałęzi
- **Re-ranking — Cross-Encoder (Cohere Rerank / Jina Reranker / BGE)**: precyzyjne przetasowanie kandydatów

Benchmarki publiczne (BEIR, MTEB) konsekwentnie pokazują, że hybryda (BM25 + dense + reranker) przewyższa dense-only o **5–15 punktów nDCG@10** na korpusach z encjami i kodem. RAGTruth (18 tys. oznaczonych fragmentów) wiąże 5–8% awarii ugruntowania na modelach frontier bezpośrednio z chybieniami wyszukiwania.

**Przykłady typów zapytań i właściwej gałęzi wyszukiwania** (z praktyki produkcyjnej):

| Typ zapytania | Właściwa gałąź | Dlaczego |
|---|---|---|
| „Zamówienie AP-8127 data wysyłki" | BM25 (dokładny ID) | Embeddingi gubią niskoczęstotliwościowe identyfikatory |
| „Jak zresetować hasło?" | Dense (parafraza) | Niedopasowanie słownictwa z dokumentacją |
| „Polityka zwrotów dla UE enterprise" | Hybrid + filtr | Encja + semantyka + metadane |
| „Funkcja SDK parseFlow()" | BM25 | Identyfikatory kodu słabo tokenizują się w dense |
| „Dlaczego aplikacja wolno działa przy zimnym starcie" | Dense + rerank | Styl objawowy; rerank czyści szum |



### 2.2. Qdrant vs pgvector — Stan na 2026

Benchmark 14 przypadków (10 000 produktów Amazon, embeddingi all-MiniLM-L6-v2 384-dim, 54 rdzenie, 96 GB DDR5, 2× RTX 3090) z kwietnia 2026 ujawnia:

| Baza | Warstwa | Ingest (wiersze/s) | Semantyczny p50 | Szczyt QPS (10 użytkowników) |
|---|---|---|---|---|
| **pgvector** | Lokalna | 1 943,7 | 5,71 ms | 1 212,3 |
| **Qdrant** | Chmurowa | 1 825,2 | 14,30 ms | 80,4 |
| Elasticsearch | Lokalna | 1 307,7 | 9,12 ms | 983,7 |
| Weaviate | Chmurowa | 1 574,6 | 44,38 ms | 85,8 |
| Pinecone | Chmurowa | 256,6 | 300,23 ms | 40,3 |

**pgvector wygrywa 7/7 kategorii lokalnych. Qdrant wygrywa 6/7 kategorii chmurowych**.

Na zbiorze GloVe-100-angular (1 183 514 wektorów, HNSW m=16, ef_construction=64, Docker, Apple M4 Pro, PostgreSQL 17, pgvector 0.8.5, Qdrant 1.18.2):

| ef_search | pgvector recall@10 | pgvector p50 | Qdrant recall@10 | Qdrant p50 |
|---|---|---|---|---|
| 64 | 0,750 | 2,56 ms | 0,839 | 1,30 ms |
| 128 | 0,820 | 4,14 ms | 0,893 | 1,48 ms |
| 256 | 0,870 | 7,09 ms | 0,934 | 1,91 ms |
| 512 | 0,910 | 12,97 ms | **0,963** | **2,38 ms** |

**Kluczowy insight inżynierski:** Qdrant dzieli kolekcję na 7 niezależnych segmentów, z których każdy ma własny graf HNSW. Jedno zapytanie Qdrant przy ef=64 eksploruje ~7× więcej kandydatów niż jedno zapytanie pgvector przy ef=64. Qdrant osiąga wyższy recall dzięki **równoległości przeszukiwania segmentów**, nie dzięki lepszej jakości grafu.

**Rekomendacja architektoniczna:**
- **pgvector** — gdy projekt już korzysta z PostgreSQL, skala do ~1 mln wektorów, budżet ograniczony, potrzebna transakcyjność ACID
- **Qdrant** — gdy kluczowy jest wysoki recall przy niskim opóźnieniu, skala >1 mln wektorów, potrzebne zaawansowane filtrowanie i wielodostępność (multi-tenancy)

### 2.3. Structured Outputs i Ścisła Walidacja JSON Schema

W 2026 roku **Structured Outputs** (`response_format: { type: "json_schema", strict: true }`) to domyślny standard dla pipeline'ów ekstrakcji danych, systemów tool-use i agentów.

**OpenAI Strict Mode:**
- Gwarantuje, że wyjście modelu **zawsze** pasuje do dostarczonego JSON Schema — 100% zgodności na obsługiwanych modelach (GPT-5.5, GPT-5.4, GPT-5.4-mini, GPT-5.4-nano, GPT-5.2-Codex)
- Wymusza obecność wszystkich pól z `required`, blokuje dodatkowe właściwości (`additionalProperties: false`), wymusza zgodność typów i wartości enum
- Obsługuje `refusal` jako pole pierwszej klasy — gdy model odmawia ze względów bezpieczeństwa, otrzymujesz `message.refusal` zamiast uszkodzonej treści
- Pydantic (Python) i Zod (TypeScript) integrują się bezpośrednio — SDK auto-generuje JSON Schema i parsuje odpowiedź do typowanego obiektu

**Krytyczne zastrzeżenie:** Structured Outputs gwarantuje **schemat**, nie **jakość semantyczną**. Pipeline ekstrakcji na OpenAI strict osiągnął 99,4% ważności schematu, ale po trzech tygodniach zespół wsparcia odkrył, że `priority: 'urgent'` było wybierane w ~11% zgłoszeń, gdy prawidłowa odpowiedź brzmiała `'normal'` lub `'high'` — model zapadł się do bezpiecznej wartości domyślnej, by zadowolić gramatykę. **Jedyna miara, która ma znaczenie, to `schema_validity_rate × semantic_quality_on_passes`**, mierzona na własnych danych, per tryb.

**Anthropic Claude** oferuje structured outputs przez tool use z JSON oraz przez `response_format` w API. Claude Opus 5.5 (wrzesień 2026) wspiera structured outputs, 1M tokenów kontekstu, do 128K tokenów wyjściowych.

**DeepSeek** wspiera JSON Output i Tool Calls na modelach V4.1-Flash i V4-Pro. Nie oferuje jednak token-level constrained decoding w stylu OpenAI strict — walidacja po stronie klienta jest obowiązkowa.

---

## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1. Halucynacje bez ugruntowania w źródłach

Klient nie mówi „mam problem z halucynacjami". Mówi: „chatbot wymyśla odpowiedzi", „podaje nieistniejące przepisy", „klient dostał błędną informację o zwrocie i straciliśmy pieniądze". Rzeczywisty problem: **brak ugruntowania odpowiedzi w cytowanych źródłach** — model generuje plausible brzmiącą odpowiedź z słabego kontekstu, gdy retriever zwrócił chybione fragmenty.

RAGTruth wiąże 5–8% awarii ugruntowania na modelach frontier bezpośrednio z chybieniami wyszukiwania. **Bez hybrydowego wyszukiwania i rerankingu nie da się tego naprawić na poziomie promptu.**

### 3.2. Brak cytowań i identyfikowalności źródeł

W zastosowaniach prawnych, compliance i medycznych klient **musi** wiedzieć, z którego dokumentu pochodzi odpowiedź. Naiwny RAG wstrzykuje fragmenty do promptu bez metadanych o źródle. Rozwiązanie: każdy chunk musi nieść `source_document_id`, `page_number`, `section_title`, a prompt musi wymuszać format odpowiedzi z cytowaniem przez Structured Outputs.

### 3.3. Koszty tokenów bez routingu na małe modele

Publiczne stawki API w 2026 roku: od ~$0,10 za milion tokenów dla małych, szybkich modeli do $60+ za frontier reasoning models. **RouteLLM** (LMSYS) wykazał redukcję kosztów o ~85% dzięki routingowi zapytań do tańszych modeli.

**TRIM** (ICLR 2026) idzie dalej: zamiast routować całe zapytanie do jednego modelu, używa Process Reward Model do identyfikacji „krytycznych kroków, które powodują niepowodzenie rozwiązania", przypisując tylko te kroki do drogiego dużego modelu, podczas gdy tani mały model kontynuuje rutynowe kroki. Osiąga to dokładność dużych modeli przy użyciu **zaledwie 20% drogich tokenów**.

**Nvidia NeMo Switchyard** (sierpień 2026) — open-source router modeli — deklaruje redukcję kosztów nawet o **74%** w porównaniu do polegania wyłącznie na modelach frontier, przy minimalnym spadku dokładności ~6 punktów procentowych.

### 3.4. Brak obsługi języka polskiego

Większość gotowych pipeline'ów RAG jest zoptymalizowana pod angielski. Polskie dokumenty wymagają:
- Modelu embeddingowego z dobrym wsparciem dla języka polskiego (np. `intfloat/multilingual-e5-large`, `sdadas/polish-roberta`)
- Tokenizera BM25 z polskim stemmingiem (np. Stempel dla Elasticsearch)
- Testów ewaluacyjnych na polskich zapytaniach — większość benchmarków BEIR/MTEB to angielski

---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

Poniższe otwarcia są zaprojektowane tak, aby w pierwszych dwóch zdaniach oferty zdiagnozować problem klienta i pokazać głębokie zrozumienie inżynierskie:

**Wariant A (dla klienta nietechnicznego):**
> „Pana/Pani obecne rozwiązanie prawdopodobnie gubi połowę trafnych dokumentów, bo wyszukiwanie opiera się wyłącznie na podobieństwie semantycznym — a to nie działa na kodach produktów, numerach umów i nazwach własnych. Standardem produkcyjnym w 2026 roku jest wyszukiwanie hybrydowe: BM25 dla dokładnych identyfikatorów + wektory dla parafraz, scalone przez Reciprocal Rank Fusion i doprecyzowane przez Cross-Encoder Reranker."

**Wariant B (dla klienta technicznego):**
> „Dense-only retrieval na encjach takich jak SKU, ID zgłoszeń czy sygnatury metod generuje 5–8% awarii ugruntowania (RAGTruth 2026) — sam prompt tego nie naprawi. Architektura musi przejść na hybrydę BM25 + wektory z fuzją RRF i rerankingiem Cross-Encoder, a wyjście LLM musi być związane przez JSON Schema w trybie strict, inaczej nie ma gwarancji parsowalności."

**Wariant C (dla projektu optymalizacyjnego):**
> „Jeśli koszt tokenów rósł szybciej niż liczba zapytań, to prawdopodobnie każde zapytanie — nawet trywialne — idzie do modelu frontier. Routing krokowy (TRIM, ICLR 2026) pozwala przypisać tylko krytyczne kroki rozumowania do drogiego modelu, redukując koszt tokenów o 60–80% bez utraty dokładności. Druga dźwignia to re-ranking przed wywołaniem LLM — Cohere Rerank tnie 50 kandydatów do 5 za ~$0,30/10k dokumentów, oszczędzając tokeny kontekstu."

---

## 5. CZERWONA LISTA / ANTYWZORCE

### ZAKAZ: Proste dzielenie dokumentów po 500 znaków

Dzielenie po stałej liczbie znaków bez respektu dla granic semantycznych (nagłówki, sekcje, akapity) niszczy kontekst. Chunk musi być **samowystarczalny semantycznie** — musi zawierać pełną myśl, a nie urwany fragment zdania. Standard 2026: **recursive character splitting** z nakładką 10–20% oraz chunkowanie semantyczne oparte na nagłówkach i strukturze dokumentu.

### ZAKAZ: Brak walidacji schematów wyjściowych

Poleganie na tym, że LLM „zwróci JSON" bez `strict: true` i `json_schema` to przepis na awarię produkcyjną. JSON mode (bez schematu) gwarantuje tylko parsowalność, nie zgodność ze schematem. **Każde wywołanie LLM w pipeline produkcyjnym musi mieć zdefiniowany JSON Schema i walidację.**

### ZAKAZ: Brak rerankingu przy top-k > 10

Wstrzykiwanie 20–50 fragmentów do promptu bez rerankingu to marnowanie tokenów kontekstu i degradacja jakości odpowiedzi (szum). Reranking Cross-Encoder to standard drugiego etapu wyszukiwania w produkcyjnym RAG.

### ZAKAZ: Brak routingu na małe modele

Wysyłanie każdego zapytania — w tym klasyfikacji intencji, ekstrakcji encji, generowania metadanych — do modelu frontier to niepotrzebne koszty. Zapytania proste (klasyfikacja, ekstrakcja, formatowanie) powinny trafiać do modeli takich jak DeepSeek V4.1 Flash ($0,15/$0,60 za 1M tokenów w off-peak) lub Claude Haiku.

### ZAKAZ: Brak metadanych o źródle w chunku

Chunk bez `source_document_id`, `page_number` i `section` uniemożliwia cytowanie. W zastosowaniach prawnych i compliance jest to wymóg twardy.

### ZAKAZ: Brak ewaluacji na danych klienta

Wdrażanie RAG bez zestawu testowego ( „Ile dokumentów źródłowych ma być przeszukiwanych (rząd wielkości: setki, tysiące, dziesiątki tysięcy) i w jakich formatach są przechowywane (PDF, DOCX, HTML, baza danych)? To determinuje wybór między pgvector a Qdrant oraz strategię chunkowania."

**Pytanie 2 (architektoniczne — wymagania jakościowe):**
> „Czy odpowiedzi muszą zawierać cytowanie konkretnego dokumentu i strony, czy wystarczy ogólna odpowiedź? W zastosowaniach prawnych i compliance cytowanie jest wymogiem twardym i wymusza Structured Outputs z polem `source_citations` — to zmienia architekturę promptu i walidacji."

**Pytanie 3 (ekonomiczne — budżet tokenów i wolumen):**
> „Jaki jest przewidywany miesięczny wolumen zapytań i czy koszt API jest kluczowym ograniczeniem? Przy wolumenie powyżej 10 000 zapytań/miesiąc routing na małe modele (DeepSeek V4.1 Flash, Claude Haiku) redukuje koszt tokenów o 60–85% — ale wymaga dodatkowego modułu klasyfikacji intencji."

**Pytanie 4 (integracyjne — środowisko docelowe):**
> „Czy system ma być samodzielnym API, czy zintegrowanym z istniejącym CRM/ERP/stroną? Czy klient ma już infrastrukturę PostgreSQL (co czyni pgvector naturalnym wyborem) czy Elasticsearch (co upraszcza wdrożenie BM25)?"

---

*Karta wiedzy wygenerowana na podstawie zweryfikowanych źródeł inżynierskich z 2026 roku. Wszystkie stawki cenowe i benchmarki podane za publicznie dostępnymi dokumentacjami i publikacjami. Zaleca się weryfikację aktualnych cenników API przed składaniem oferty.*