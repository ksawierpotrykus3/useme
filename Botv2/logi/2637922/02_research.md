## Wyniki researchu (pokewars.pl)

### 1. Regulamin gry: skrypty i boty są zabronione

**Fakt potwierdzony.** Regulamin PokeWars w §7 pkt 7.6 stanowi:

> „Zabronione jest korzystanie z botów, skryptów, bindów oraz wszelkich innych nieprzewidzainych przez twórców serwisu rzeczy wpływających na polepszenie sytuacji gracza (np. poprzez automatyczne wędrowanie do lokacji).”  
> — https://pokewars.pl/regulamin, linie 150–153 

**Konsekwencja:** proponowany skrypt do automatycznego klikania „walcz z bossem” **narusza regulamin**. Grozi to permanentną blokadą konta. To kluczowa mina — klient może stracić konto, na którym grał.

---

### 2. Struktura strony: przycisk prawdopodobnie niedostępny dla NVDA

**Niepotwierdzone w 100%, ale wysoce prawdopodobne.** Klient pisze: „używając czytnika ekranu z poziomu klawiatury nigdzie tego nie widzę” — to silny sygnał, że przycisk **nie jest zwykłym elementem DOM** (np. `<button>`), który NVDA mógłby odczytać i aktywować z klawiatury.

**Możliwe scenariusze (wymagają weryfikacji po zalogowaniu):**
- Mapa/lokacje renderowane w **`<canvas>`** — wtedy NVDA nie widzi żadnych elementów, a skrypt może klikać wyłącznie po współrzędnych, których nie znamy i które mogą się zmieniać.
- Przycisk jako **obraz/`<div>` z handlerem JS** bez `tabindex` i ARIA — również niedostępny z klawiatury, ale możliwy do kliknięcia selektywnie przez `querySelector`, jeśli ma identyfikator/klasę.

W kodzie strony głównej **nie znaleziono** znacznika `<canvas>` , ale właściwy interfejs gry ładuje się dopiero po zalogowaniu — tam struktura może być inna.

**Wniosek:** bez wejścia na konto i sprawdzenia DOM nie da się ustalić, czy przycisk jest w ogóle klikalny selektywnie. To fundamentalna niepewność, która może przekreślić całe zlecenie.

---

### 3. Rejestracja: otwarta (na podstawie regulaminu)

Regulamin mówi o „założeniu konta poprzez prawidłowe wypełnienie formularza rejestracyjnego” . Brak informacji o zamknięciu rejestracji — **można założyć konto testowe** (o ile formularz działa, czego nie zweryfikowano bez interakcji).

---

### 4. Walka z bossem: przebieg nieznany

**Niepotwierdzone.** Nie wiadomo, czy po kliknięciu „walcz z bossem” walka toczy się automatycznie, czy wymaga dalszych akcji (wybór ataku, przedmiotów). Brak danych publicznych.

---

### 5. Przeglądarka i system klienta

**Niepotwierdzone.** Ogłoszenie nie podaje, z jakiej przeglądarki i systemu korzysta klient. To trzeba dopytać — od tego zależy forma skryptu (Tampermonkey, rozszerzenie, zewnętrzna automatyzacja).

---

### Podsumowanie ryzyk („gdzie i dlaczego groźne”)

| Ryzyko | Status | Dlaczego groźne |
|---|---|---|
| **Naruszenie regulaminu** | Potwierdzone | Skrypt = ban konta. Klient może stracić dostęp do gry, w którą zainwestował czas. |
| **Mapa w canvas / niedostępna** | Prawdopodobne | Jeśli tak, skrypt nie kliknie selektywnie — tylko po współrzędnych, których nie znamy. |
| **Brak danych o walce** | Niepotwierdzone | Może się okazać, że kliknięcie to dopiero początek — skrypt musiałby obsłużyć całą walkę, co zwiększa złożoność i ryzyko błędu. |

**Rekomendacja dla działu:** przed wyceną i podjęciem zlecenia **koniecznie** zweryfikować strukturę DOM po zalogowaniu (czy jest `<canvas>`, czy jest selektywny selektor przycisku) oraz poinformować klienta o ryzyku bana wynikającym z §7.6 regulaminu.