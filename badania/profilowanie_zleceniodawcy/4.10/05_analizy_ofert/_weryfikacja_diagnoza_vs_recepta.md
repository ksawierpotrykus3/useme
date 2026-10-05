# Weryfikacja: diagnoza vs recepta, alternatywy, długość (na nieodpisanych)

> Źródło: 28 ofert nieodpisanych (02_przegrane) vs 14 odpisanych (03_odpisane).
> Data: 2026-10-04. Weryfikacja tezy użytkownika.

## Najważniejsze liczby

| Cecha | Nieodpisane | Odpisane |
|---|---|---|
| Insight/pułapka | prawie zawsze | prawie zawsze |
| Pełna recepta krok po kroku | **68% (19/28)** | ~30% |
| Długość (średnio) | **300-600 słów** | **100-250 słów** |
| Puste/nic | 3 | 0 |

## Teza 1: "dawać diagnozę, nie receptę" — POTWIERDZONA

Insight sam nie szkodzi. Szkodzi **insight + pełna recepta**. Najwięcej nieodpisanych (19/28) to oferty, gdzie wyłożono całą architekturę i sposób wykonania. Klient dostał plan i mógł go zrealizować sam.

Przykłady nieodpisanych z receptą:
- 2897172 (Shoper) — cała architektura: wyścig skryptu z Sellintegro, limity API, VAT, ZK vs WZ
- 2896427 (Presta B2B) — trzy gotowe recepty + plan etapów
- 2892997 (Meta Pixel) — lista poprawek krok po kroku
- 2887274 (bot mailowy) — RAG, prompt injection, cała architektura

Kontrast (odpisane, sama diagnoza bez przepisu):
- 2514016 (OLX) — "nazwa Olx skaner to czerwona flaga", bez recepty → odpisane
- 2861189 (Uber) — 60 słów, samo pytanie → odpisane

## Teza 2: "wiedza za darmo szkodzi" — BACKFIRE POTWIERDZONY

Tam, gdzie oddano receptę (2897172, 2892997, 2878820, 2896683), klient nie odpisał. Klasyczne "dałem gotowe rozwiązanie za darmo".

## Teza 3: "alternatywa pewnym tonem przy mało info szkodzi" — POTWIERDZONA

- 2897362 (camera) — pewna diagnoza "root cause in three places" przy zerowej wiedzy o kodzie → nieodpisane
- 2896500 (ArenaDesk) — pewna architektura RLS bez dostępu do repo → nieodpisane
- 2891620 (b2b) — "przyjmuję założenia robocze" przy braku danych → nieodpisane

## Teza 4: DŁUGOŚĆ — silny sygnał

Nieodpisane są 2-3x dłuższe. 2861189 (odpisane, 60 słów). 2887274 (nieodpisane, ~500 słów).

## Rekomendowana reguła dla bota

1. **Tease zamiast recepty:** diagnoza kończy się na skutku, nie na kroku. Zamiast "wymaga FORCE ROW LEVEL SECURITY i tenant context fails closed" → "widziałem ten błąd, mam na to sposób, chętnie pokażę".
2. **Ton asekuracyjny przy mało info:** "na podstawie opisu podejrzewam X, zweryfikuję na Waszych danych" zamiast pewnej diagnozy.
3. **Jedna pułapka, nie lista trzech możliwych przyczyn.**
4. **Wzór:** diagnoza (1 zdanie) + "chętnie się tym zajmę i pokażę rozwiązanie" + 1 pytanie. Bez recepty.
5. **Długość:** trzymać krótko.

Wzorzec do naśladowania: 2861189, 2514016.
Wzorzec do unikania: 2897172, 2896427, 2887274.