## 1. Czy istnieje gotowy moduł PrestaShop do centralnego cennika komponentów / kombinacji?

**Nie znaleziono gotowego modułu, który realizowałby dokładnie ten scenariusz (centralna tabela komponentów → automatyczne przeliczenie kombinacji wszystkich produktów).**

Znalezione moduły rozwiązują problem **częściowo** — oferują globalne opcje lub dynamiczne przeliczanie ceny, ale nie centralny cennik komponentów z synchronizacją do istniejących kombinacji:

| Moduł | Co robi | Cena | Zgodność | Luka względem zlecenia |
|---|---|---|---|---|
| **Product Options Configurator** (01generator.com) | Konfigurator z regułami cenowymi (formuły, zakresy, dropdowny), live pricing, mass option generator | €99.99 | PS 1.7–9.x | Brak centralnej tabeli komponentów; konfiguracja per produkt lub kopiowana, nie globalna tabela RAM/SSD |
| **Global Product Attributes** (mypresta.rocks) | Globalne szablony atrybutów dla rodzin produktów, synchronizacja do natywnych kombinacji, price impact per wartość | brak ceny w źródle | PS 1.6–9.0 | Globalne **atrybuty**, nie globalne **ceny komponentów**. Każda wartość ma price impact, ale nie ma jednej tabeli „DDR4 16GB = 400 zł” |
| **Extra Options** (prestahero) | Globalne opcje dla wszystkich produktów z price impact per opcja | brak ceny w źródle | PS 1.7.x i 8.x | Globalne **opcje**, nie komponenty z centralną tabelą cen |
| **Dynamic Pricing Calculator** (FME Modules) | Kalkulator cen z polami zmiennymi per produkt | brak ceny w źródle | brak danych o wersji PS w źródle | Per produkt, nie centralna tabela |
| **More Dynamic Product Fields** (PrestaShop Addons) | Live pricing (formuła lub macierz), per-product fields | brak ceny w źródle | PS 1.7.1–9.2 | Per produkt, nie globalna tabela komponentów |

**Wniosek:** Klient prawdopodobnie potrzebuje modułu custom, który łączy: (a) centralną tabelę komponentów, (b) synchronizację z natywnymi kombinacjami PrestaShop, (c) przeliczenie różnicy względem konfiguracji bazowej. Żaden znaleziony moduł nie robi tego w całości.

---

## 2. PrestaShop 1.7 vs 8.x — różnice w kombinacjach i price impact

**Nie znaleziono dowodów na fundamentalne różnice w mechanizmie price impact między 1.7 a 8.x.** Dokumentacja i poradniki opisują kombinacje w sposób jednolity:

- **Price impact w kombinacjach to stała kwota +/−** dodawana do ceny bazowej — dotyczy to zarówno 1.7, jak i 8.x. Wariant procentowy należy do „Cen specyficznych”, a nie do wiersza kombinacji.
- **Zapowiadana zmiana w PS 8.1:** Na forum PrestaShop pojawiła się informacja, że w wersji 8.1 „pojawi się spora zmiana w zarządzaniu atrybutami i tam będzie prościej zarządzać nimi masowo na podstawie określonego parametru”. **To jedyny konkretny sygnał różnicy** — ale źródło to wypowiedź forumowa, nie oficjalna dokumentacja. **Niepotwierdzone jako oficjalne stanowisko PrestaShop.**
- **Encja importu CSV kombinacji** dotyczy PrestaShop 1.7, 8 i 9 — czyli format danych kombinacji jest wspólny.

**Konsekwencja dla zlecenia:** Jeśli klient ma PS 1.7, custom moduł działający na natywnych kombinacjach powinien być kompatybilny również z 8.x (z zastrzeżeniem ewentualnych zmian w 8.1, których zakresu nie udało się potwierdzić w oficjalnych źródłach).

---

## 3. Mina — natywne ograniczenie PrestaShop

Kluczowa mina potwierdzona w źródłach: **PrestaShop natywnie nie ma centralnego cennika komponentów.** Mechanizm kombinacji działa per produkt:

- „W standardowym sklepie klient, który waha się pomiędzy rozmiarami, kolorami czy wykończeniami, musi wybierać każdą opcję po kolei, aby poznać jej cenę”.
- Przy dużej liczbie kombinacji pojawia się problem wydajnościowy: „Duża ilość atrybutów mocno obciąża sklep przez co strona wczytuje się wolniej”.
- Forumowy wątek o produkcie z 180 kombinacjami pokazuje dokładnie ten ból: „w zakładce kombinacje powinienem wypełnić 180 pól z cenami, one się będą oczywiście powtarzać”.

**To jest sedno problemu klienta** — i potwierdzenie, że custom moduł jest konieczny, chyba że klient zaakceptuje rozwiązanie częściowe (globalne opcje zamiast kombinacji).