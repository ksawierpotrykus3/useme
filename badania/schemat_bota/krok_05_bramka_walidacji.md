# KROK 5: Bramka Walidacji i Jakości (Agent 08 + Anty-Powtórka)

Moduł kontroli jakości gwarantujący, że żadna halucynacja, błąd merytoryczny ani powtarzalny schemat nie trafi do formularza Useme.

---

## 1. Działanie Agenta 08 (Weryfikator Zasad)

Agent 08 ([`agent_08_weryfikacja_zasad.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/prompts/walidatory/agent_08_weryfikacja_zasad.md)) to bezkompromisowy audytor sprawdzający wygenerowaną ofertę względem twardych wytycznych:

1. **Test Objętości**: Czy opis mieści się w limicie 190 słów?
2. **Test Stylizacji**: Czy tekst zawiera zakazane znaczniki markdown (`**`, bulletpointy `- `, nagłówki `#`)?
3. **Test CTA**: Czy oferta kończy się pytaniem decyzyjnym (Question CTA) zamiast prośby o call/telefon?
4. **Test Sygnatury**: Czy na końcu znajduje się poprawny podpis (np. "Pozdrawiam, Ksawier")?
5. **Test Spójności Dual-Track**:
   - Czy w zleceniu biznesowym (tech-agnostic) nie pojawił się zbędny żargon IT?
   - Czy w zleceniu technicznym padły precyzyjne odniesienia do stacku klienta?

---

## 2. Mechanizm Pętli Zwrotnej (Feedback Loop)

Jeśli Agent 08 wykryje uchybienia, zwraca werdykt `FAIL` z precyzyjną instrukcją naprawczą w formacie:
```
POPRAW_OFERTA: Skróć opis o 30 słów, usuń myślniki z drugiego akapitu i zastąp prośbę o kontakt pytaniem o wersję API.
```

- **Egzekutor Łańcucha ([`chain_executor.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/chain_executor.py))**:
  - Odczytuje linię `POPRAW_OFERTA`.
  - Wycofuje łańcuch do Slota 02a (Agent Treści Oferty).
  - Wstrzykuje uwagi walidatora jako instrukcję korekty.
  - Generuje poprawioną wersję (maksymalnie `retry_max = 3` próby).
  - Jeśli po 3 próbach oferta nadal nie spełnia kryteriów, całe zlecenie zostaje odrzucone (status `ABORT`).

---

## 3. Globalny Wykrywacz Duplikatów (Współczynnik Jaccarda)

Przed zatwierdzeniem propozycji silnik uruchamia procedurę `sprawdz_globalne_duplikaty()` ([`kod/ai_pipeline.py`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/ai_pipeline.py#L49-L76)):
- Porównuje zbiór słów nowej oferty ze wszystkimi ofertami wysłanymi w ciągu ostatnich 7 dni (`GLOBALNY_OKNO_DNI = 7`).
- Jeśli współczynnik podobieństwa Jaccarda przekracza **0.75 (75%)**, oferta zostaje oflagowana jako zbyt monotonna i skierowana do przeredagowania.
- Chroni konto przed wrażeniem "maszynowego bota" wysyłającego ten sam szablon do wszystkich klientów.

---

## 4. Ostateczny Cap Długości

Jako bezpiecznik ostateczny przed anomaliami modelu, silnik weryfikuje twardy limit znakowy:
- `len(proposal.opis) <= config.MAX_OPIS_DLUGOSC` (domyślnie 2500 znaków).
- W przypadku przekroczenia tekst jest natychmiast ucinany na granicy ostatniego zdania.
