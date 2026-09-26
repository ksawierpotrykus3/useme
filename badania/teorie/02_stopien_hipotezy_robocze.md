# STOPIEŃ 2: Hipotezy Robocze (Pewność 60% – 80%)

> Kryterium kwalifikacji: Silna spójność w danych empirycznych ($15 \le n < 100$), powtarzalne wzorce behawioralne zleceniodawców, wysokie prawdopodobieństwo logiczne poparte praktyką rynkową.

---

## HIPOTEZA 2.1: Model Rynku Dual-Track (67% Inżynieria vs 33% Rezultat Biznesowy)

- **Podstawa empiryczna**:
  - $n = 315$ (67%) zleceń wymienia konkretną technologię (Python, React, PHP, Docker, Swift).
  - $n = 155$ (33%) zleceń to zlecenia tech-agnostic (klient nie wymienia żadnej technologii, opisuje ból operacyjny: *"potrzebuję bazy firm"*, *"skrypt do wystawiania"*, *"system rezerwacji"*).
- **Założenie operacyjne**:
  - Ścieżka 1 (Inżynieria): Precyzja stacku, biblioteki, specyfikacja protokołów API, Question CTA o bazę danych lub architekturę.
  - Ścieżka 2 (Biznes): Zero żargonu technicznego. Propozycja najprostszego, bezobsługowego narzędzia (arkusz Google, prosty skrypt w tle, webhook), Question CTA o format wejściowy danych klienta.
- **Poziom pewności**: **80%**. Działa powtarzalnie w klasyfikacji zleceń.

---

## HIPOTEZA 2.2: Mobile Native Jako Filtr Odsiewający Konkurencję Amatorską

- **Podstawa empiryczna**:
  - Kotlin / Android Native: $n = 22$, wygrane = 6, **Win Rate = 27.27%**.
  - Flutter / Dart: $n = 20$, wygrane = 4, **Win Rate = 20.00%**.
  - Łącznie rynek mobilny: $n = 42$, Win Rate $\approx 23.8\%$.
- **Mechanizm**:
  Większość masowych agencji i amatorów z Useme specjalizuje się wyłącznie w prostych stronach WWW i CMS. Bariera kompilacji kodu natywnego, konfiguracji Gradle/Xcode oraz obsługi Google Play / App Store drastycznie zmniejsza liczbę ofert konkurencji.
- **Poziom pewności**: **75%**.

---

## HIPOTEZA 2.3: Klient AI-Pragmatyk (Dominik Łyżwa) vs AI-Sceptyk

- **Mechanizm behawioralny**:
  - Klienci zaawansowani biznesowo (jak Dominik Łyżwa z Doktor Monika) sami używają LLM (np. Claude) do budowy modułów. Nie potrzebują "kodera od zera", lecz inżyniera do trudnych kwestii infrastrukturalnych (concurrency, race conditions, transakcyjność SQL, webhooki).
  - Klienci tradycyjni są zalewani 50-100 ofertami ze sztucznego ChatGPT i natychmiast odrzucają szablony.
- **Wniosek operacyjny**:
  Oferta musi celować w twardą architekturę i bezbłędność produkcyjną, bez sztucznej empatii ani bez pretensjonalnego hejtowania AI konkurencji.
- **Poziom pewności**: **75%**.

---

## HIPOTEZA 2.4: Trojan Horse na Priv (Żądanie Konkretnego Artefaktu)

- **Mechanizm**:
  W pierwszej wiadomości prywatnej (lub w pytaniu końcowym oferty) prosimy o konkretny, istniejący artefakt:
  - *"Czy mogę zobaczyć przykładowy plik CSV/JSON ze strukturą obecnych produktów?"*
  - *"Jaka jest dokładna wersja silnika sklepu i czy API REST jest odblokowane?"*
- **Psychologia**:
  Dostarczenie artefaktu kosztuje klienta 1 minutę, ale tworzy zaangażowanie (efekt utopionych kosztów). Klient, który przesłał plik, niemal nigdy nie porzuca wątku.
- **Poziom pewności**: **70%**.

---

## HIPOTEZA 2.5: Wpływ Czasu Złożenia Oferty (< 30 Minut od Publikacji)

- **Obserwacja**:
  Zleceniodawcy logują się na Useme najczęściej w momencie publikacji ogłoszenia i przeglądają pierwsze 3-5 ofert w ciągu pierwszej godziny.
- **Założenie**:
  Oferty złożone w ciągu 15-30 minut od pojawienia się zlecenia w feedzie mają o 50% większą szansę na przeczytanie niż oferty składane po 24 godzinach.
- **Poziom pewności**: **65%** (Wymaga dalszej telemetrii w module zbieracza danych).
