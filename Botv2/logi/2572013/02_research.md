Poniższa diagnoza opiera się na analizie zlecenia i dostępnych źródłach. Skupiam się na zidentyfikowanych ryzykach i niewiadomych, które mogą zagrozić projektowi, a nie na sposobach ich rozwiązania.

### Mapa ryzyk i niewiadomych

**1. Ryzyko architektoniczne: WordPress ≠ backend voicebota**
Zlecenie sugeruje, że klient może oczekiwać pluginu WordPress, który samodzielnie obsłuży voicebota. Tymczasem nowoczesne pipeline'y głosowe (LiveKit, Vapi, Retell, ElevenLabs) działają jako zewnętrzne usługi, a WordPress pełni rolę wyłącznie hosta dla widgetu JavaScript/HTML. Klient może nie być tego świadomy, co grozi nieporozumieniem co do zakresu prac i kosztów. **Mina: klient może oczekiwać "wtyczki", a otrzyma integrację z zewnętrznym backendem.**

**2. Ryzyko latencji i barge-in: standardowy pipeline nie wystarczy**
Klient wymaga natychmiastowego przerwania wypowiedzi (barge-in) i krótkich przerw między wypowiedziami. Osiągnięcie tego wymaga **streamingowego** pipeline'u STT → LLM → TTS z obsługą VAD (voice activity detection). Standardowe, nie-streamingowe rozwiązania generują opóźnienia rzędu 500–1500 ms. Badania pokazują, że użytkownicy zaczynają odczuwać lag przy ~800 ms całkowitego czasu odpowiedzi, a średnie opóźnienie w badaniu z 2025 r. wyniosło 1366 ms. **Mina: bez streamingu na każdym etapie wymagania klienta są nieosiągalne.**

**3. Ryzyko RODO: zbieranie danych i nagrywanie rozmów bez podstawy prawnej**
Zlecenie mówi o "zbieraniu podstawowych danych od klienta" i "rozmowie głosowej", ale nie wspomina o zgodach, klauzuli informacyjnej ani retencji danych. Voicebot prawdopodobnie będzie przetwarzał dane osobowe i nagrywał rozmowę – bez odpowiednich zgód i informacji jest to naruszenie RODO. **Mina compliance: brak wzmianki o zgodach w zleceniu to luka, którą należy zaadresować przed wdrożeniem.**

**4. Niewiadoma: ekosystem voicebota na rynku polskim**
Polski rynek voicebotów dzieli się na proste, szybkie wdrożenia dla małych firm oraz rozbudowane rozwiązania dla bankowości, telekomunikacji i e-commerce. Brak jednak w źródłach potwierdzenia, jakie konkretnie rozwiązania dla polskiego głosu w HVAC są dostępne na rynku. **Niepotwierdzone: nie udało się znaleźć case studies voicebota HVAC w Polsce.**

---

### Tabela porównawcza platform voice AI

| Platforma | Integracja z WordPress | Model wdrożenia | Kluczowa cecha |
|---|---|---|---|
| **LiveKit** | Script tag, gotowy widget na każdą stronę HTML | Open-source, wymaga backendu (Python/Node.js) | Embed widget – jeden tag, bez SDK |
| **Vapi** | Plugin WordPress społecznościowy; integracja przez JS SDK | Developer-first, API-centered | Głęboka customizacja, webhooks, multi-step logic |
| **Retell AI** | Brak natywnego pluginu; integracja przez Make/viaSocket | Managed platform, szybsze wdrożenie | Łatwiejszy start, mniej infrastruktury |
| **ElevenLabs** | Oficjalny plugin WordPress (White Label Voice Chat Widget) | Gotowy widget + API Conversational AI | Naturalny głos, integracja przez Custom HTML Block |

**Wniosek z tabeli:** ElevenLabs oferuje najbardziej bezpośrednią ścieżkę integracji z WordPressem (oficjalny plugin), podczas gdy LiveKit, Vapi i Retell wymagają więcej pracy po stronie backendu.

---

### Kluczowe liczby: budżet latencji

| Etap | Docelowy czas | Źródło |
|---|---|---|
| STT (partial transcripts) | 150–300 ms |  |
| LLM (time to first token) | Zmienna – wąskie gardło |  |
| TTS (pierwszy chunk audio) | 100–200 ms |  |
| **Całkowity end-to-end** | **< 500–700 ms** (inaczej rozmowa "brzmi jak zepsuta") |  |
| Barge-in (przerwanie) | < 1 ms (abort latency) |  |

**Diagnoza:** Osiągnięcie wymagań klienta (naturalna rozmowa, natychmiastowe przerwanie) jest technicznie możliwe, ale wymaga **streamingowego pipeline'u** z każdego etapu. Komponenty muszą być zsynchronizowane, a LLM jest najczęstszym wąskim gardłem.

---

### Pytania do klienta (wynikające z researchu)

1. **Gdzie fizycznie znajduje się baza wiedzy firmy?** (dokumenty, FAQ, strona, CRM) – od tego zależy implementacja RAG.
2. **Czy strona WordPress jest self-hosted, czy na WordPress.com?** – self-hosted pozwala na dowolny JS/backend; WordPress.com Business/Commerce wymaga odpowiedniego planu dla custom JS.
3. **Czy voicebot ma zapisywać dane do istniejącego CRM/kalendarza, czy wystarczy e-mail/zapis w WP?** – od tego zależy zakres integracji.
4. **Czy klient ma politykę prywatności i zgodę na nagrywanie rozmów?** – warunek zgodności RODO.

---

### Podsumowanie: gdzie jest groźnie

| Obszar | Poziom ryzyka | Dlaczego |
|---|---|---|
| **RODO** | 🔴 Wysokie | Brak wzmianki o zgodach, a voicebot zbiera dane osobowe i prawdopodobnie nagrywa rozmowy |
| **Latencja/barge-in** | 🟠 Średnie | Wymagania klienta są ambitne; standardowy pipeline nie wystarczy |
| **WordPress ≠ backend** | 🟠 Średnie | Klient może oczekiwać pluginu, a potrzebna jest integracja z zewnętrznym API |
| **Baza wiedzy** | 🟡 Nieznane | Nie wiadomo, w jakim formacie są dane – to determinuje zakres prac RAG |
| **CRM/kalendarz** | 🟡 Nieznane | Brak informacji o tym, gdzie mają trafiać zebrane dane |

**Największa mina:** RODO. Zlecenie nie wspomina o zgodach, informacji o przetwarzaniu ani retencji danych – to luka, która może zablokować wdrożenie, jeśli nie zostanie zaadresowana na etapie projektowania.