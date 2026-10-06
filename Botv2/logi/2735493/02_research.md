Zgodnie z dziennikiem, research ograniczam do trzech obszarów: **statusu PKD 2025** oraz **aktualnych limitów i kosztów API** dla KRS, CEIDG, GUS BIR1 i REGON. Poniżej fakty ze źródłami.

---

## 1. PKD 2025 — status i okres przejściowy

**Potwierdzone.** Nowa Polska Klasyfikacja Działalności (PKD 2025) została opublikowana w Dzienniku Ustaw 27 grudnia 2024 r. Rozporządzenie Rady Ministrów w sprawie PKD weszło w życie **1 stycznia 2025 r.**

- **Podstawa prawna:** Rozporządzenie Rady Ministrów z 18 grudnia 2024 r. w sprawie Polskiej Klasyfikacji Działalności (PKD). Pełny tekst: `https://dziennikustaw.gov.pl/DU/2024/1936`
- **Okres przejściowy:** do **31 grudnia 2026 r.** — w tym czasie rejestry mogą zwracać dane w obu schematach (PKD 2007 i PKD 2025)
- **Konsekwencja dla klienta:** jeśli jego dane źródłowe są w PKD 2007, a filtr działa na nowych wpisach (PKD 2025), wyniki będą niepełne lub błędne. Konieczny słownik przejścia między wersjami.

---

## 2. API rejestrów — koszty i limity (stan na 2025/2026)

### KRS API (Ministerstwo Sprawiedliwości)
- **Koszt:** całkowicie **darmowe**, bez klucza API i rejestracji
- **Zakres:** wyszukiwanie **wyłącznie po numerze KRS** (10 cyfr). Brak wyszukiwania po NIP, REGON lub nazwie firmy
- **Limity:** API publiczne, mogą występować ograniczenia przy dużym ruchu — brak sztywnych, publikowanych progów
- **Wzbogacenie przez REGON:** opcjonalne, wymaga własnego klucza GUS (patrz niżej)

### CEIDG (biznes.gov.pl)
- **Koszt:** darmowe (open data)
- **Limity:** dwa równoczesne ograniczenia:
  - **50 żądań / 3 minuty**
  - **1 000 żądań / 60 minut**
- **Ograniczenie hurtowni:** maksymalnie **25 wyników na jedno żądanie** — ustawienie wyższego limitu powoduje błąd

### GUS BIR1 (REGON API)
- **Koszt:** **bezpłatne** — usługa i dane udostępniane są bez opłat
- **Rejestracja:** wymagany klucz użytkownika. Wniosek wysyła się na `regon_bir@stat.gov.pl` z podaniem nazwy podmiotu, numeru REGON, danych kontaktowych oraz **adresów IP**, z których będą wysyłane zapytania. Brak self-serve — czas oczekiwania „koordynowany indywidualnie” (kilka dni roboczych)
- **Limity:**
  - **6 000 wywołań / godzinę** (w godzinach 8:00–16:59)
  - **120 wywołań / minutę**
  - **3 wywołania / sekundę**
- **Kryteria wyszukiwania:** REGON, NIP, KRS
- **Uwaga:** przekroczenie limitów nie skutkuje natychmiastową blokadą — użytkownik jest informowany

### REGON API (tożsame z GUS BIR1)
Limity identyczne jak powyżej — usługa BIR1 jest jedynym interfejsem API do rejestru REGON

---

## 3. Podsumowanie — co to oznacza dla wyceny

| Rejestr | Koszt | Limit dzienny (przybliżony) | Kluczowa mina |
|---|---|---|---|
| **KRS** | Darmowy | Brak sztywnego limitu (rate limiting) | Tylko po numerze KRS — **brak wyszukiwania po NIP** |
| **CEIDG** | Darmowy | ~24 000 (przy 1 000/h) | **Max 25 wyników na żądanie** — paginacja obowiązkowa |
| **GUS BIR1 / REGON** | Darmowy | ~48 000 (przy 6 000/h w oknie 8h) | **Rejestracja nie-self-serve**, wymaga podania IP, czas oczekiwania kilka dni |

**Kluczowy wniosek dla pytania do klienta o źródła:** GUS BIR1 jest darmowy, ale **proces rejestracji jest barierą** — nie da się go uruchomić „od razu”. CEIDG ma restrykcyjny limit 25 rekordów na żądanie, co przy budowie dużej bazy oznacza tysiące wywołań. KRS API nie pozwala na lookup po NIP — jeśli klient ma listę NIP-ów, a nie KRS-ów, konieczny jest REGON jako pośrednik.

---

**Niepotwierdzone / do weryfikacji u klienta:**
- Skala bazy (liczba firm) — od tego zależy, czy limity CEIDG/GUS stanowią wąskie gardło.
- Czy klient ma już dane w PKD 2007 czy 2025.
- Czy dane wejściowe to NIP-y, KRS-y czy nazwy firm — determinuje architekturę przepływu.