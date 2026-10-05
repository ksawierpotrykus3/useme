# BOT V2 — PLAN OGÓLNY

> Status: plan roboczy. Data: 2026-10-05.
> Cel: nowy bot ofertowy, który MYŚLI jak człowiek, a nie leci sztywnym łańcuchem slotów.
> Stary bot (`kod/`) zostaje nietknięty. Z niego tylko KOPIUJEMY klocki (storage, browser_driver, form_driver, config).
> Kod to rzecz prosta i drugorzędna. Najważniejsze: JAK MA DZIAŁAĆ AI.

---

## 0. Założenie bazowe (fizyka)

- **Zlecenie jest jedynym pełnym artefaktem intencji** dostępnym przed napisaniem oferty. To jedyne źródło prawdy.
- Z treści zlecenia wynika WSZYSTKO: czy odpalać research, jak głęboka merytoryka, co dopisać, na co odpowiedzieć, o co dopytać.
- **Zero zgadywania.** Piszemy dokładnie tyle, ile jest informacji.
- Jeden decydent = jeden człowiek = jedna decyzja. Wygrana = dopasowanie do TEGO człowieka, nie „lepsza oferta w próżni".
- Sztywne formułki to shit. Mózg budujemy **materiałem edukacyjnym** (teoria warstw, lore, lekcje z ofert), nie twardymi regułkami. AI jest darmowe → ilość materiału nie gra roli.

---

## 1. Dlaczego stary bot nie myśli

Sloty są **głuchе na siebie**. Slot 02a pisze ofertę, nie wiedząc, DLACZEGO wcześniej uznano, że warto wejść w merytorykę. Każdy slot to osobny model z osobnym promptem. To nie mózg, to taśma produkcyjna: research → wycena → tekst → walidacja, zawsze w tej samej kolejności, zawsze dla każdego zlecenia.

Mózg działa inaczej: **najpierw myśli, potem pisze.** I myślenie zostaje jako ślad, do którego pisanie może wrócić.

---

## 2. Rdzeń V2 — jedno myślenie, nie pipeline

Zamiast 4 slotów, które się nie znają → **JEDEN umysł, który w wielu iteracjach dochodzi do oferty.**

Kluczowe różnice względem V1:

1. **Jedno wejście** = całe zlecenie + CAŁA teoria (teoria_warstw, lore, lekcje, typy klientów). Model czyta wszystko naraz.
2. **Najpierw myślenie, nie pisanie.** Model produkuje „dziennik myślenia" wg top-down (Krok 0-5 z `03_teoria_warstw.md`), nie od razu ofertę.
3. **Iteracje zamiast jednego przebiegu.** Minimum 3 iteracje. Każda coś dokłada albo poprawia (patrz sekcja 3).
4. **Ślad myślenia zostaje.** Dziennik myślenia to osobny artefakt na dysku — widać, JAK bot myślał i DLACZEGO napisał to, co napisał.
5. **Krytyk patrzy na myślenie, nie na ofertę.** Błąd rodzi się w myśleniu, nie w pisaniu.

---

## 3. Iteracje (minimum 3)

Iteracja = pełny obieg „myśl → sprawdź → popraw". Nie chodzi o 3 wywołania modelu, tylko o 3 REALNE przejścia przez rozumienie zlecenia, gdzie każde może zmienić poprzednie.

### ITERACJA 1 — ANALIZA (zrozumienie, bez pisania oferty)
Wejście: surowe zlecenie.
Wyjście: dziennik myślenia. Model odpowiada SOBIE (nie klientowi):
- Kto tu decyduje i czego NAPRAWDĘ chce? (bol biznesowy pod problemem technicznym)
- Czy zlecenie jest wykonawcze (zrób X) czy doradcze (powiedz mi, co lepsze)?
- Czy jest w ogóle pole do popisu? (co klient wie, a czego nie wie)
- Jakie miny / okazje (haczyki) widzę? Bez ograniczeń — tyle, ile znajdę.
- Czego nie wiem, bez czego NIE da się wycenić? (kandydaci na pytania)
- Jaki styl i jaka długość (granica cięcia — na styk, nigdy za)?
- Czy potrzebny research? Jaki dokładnie i PO CO?

To jest akceptowany Krok 1. Nic nie piszemy dla klienta.

### ITERACJA 2 — WERYFIKACJA / POGŁĘBIENIE
Wejście: dziennik z iteracji 1.
Model patrzy na własne myślenie krytycznie:
- Czy na pewno wiem, czego klient chce? Gdzie zgaduję? (zgadywanie = śmierć)
- Czy każda mina ma dowód z zlecenia, czy to domysł?
- Czy research coś realnie zmienia, czy to szum?
- Czy moje pytania są bez odpowiedzi NAPRAWDĘ nie do ruszenia?
- Gdzie jestem za granicą cięcia (za dużo), a gdzie przed (za mało)?
- Czy to już pełny obraz, czy brakuje mi faktów?
Efekt: uzupełniony / skorygowany dziennik. Tu może wjechać research (jeśli iteracja 1 uznała, że trzeba).

### ITERACJA 3 — DECYZJA I PISMO
Wejście: dojrzały dziennik.
- Model podejmuje decyzje: co DOPISAĆ, na co ODPOWIEDZIEĆ, o co DOPYTAĆ.
- Wycena: konsekwencja zlecenia. Rzeczy otwarte → widełki → warunek wprost („taniej gdy X, drożej gdy Y"). Widełki zawsze.
- Pisze ofertę: na styk, prozą, bez wyliczanek, bez AI-izmów, ludzkim językiem.
- Ślad: dziennik + oferta obok siebie, żeby było widać związek myślenie → tekst.

(Jeśli po iteracji 3 krytyk widzi braki → wracamy do 2 lub 3. Liczba iteracji jest MINIMUM, nie maksimum.)

---

## 4. Trzy osie jako jedna całość

Bot musi wiedzieć jednocześnie i spójnie:
- **DOPISAĆ** — co wiemy sami, czego klient nie napisał, a co jest miną/wartością.
- **ODPOWIEDZIEĆ** — co klient wprost pyta.
- **DOPYTAĆ** — czego brakuje, bez czego nie da się ruszyć.

To nie trzy osobne kroki. To jedna decyzja w jednym myśleniu. Materiał edukacyjny tłumaczy, KIEDY która oś wchodzi — nie twarda reguła, tylko rozumienie.

---

## 5. Materiał edukacyjny (to jest „klasa", nie formułki)

Zamiast sztywnych reguł wstrzykujemy:
- `badania/profilowanie_zleceniodawcy/03_teoria_warstw.md` (top-down, granica cięcia, miny, AI-izmy, spark, zawsze widełki)
- typy klientów (`badania/analizy/typy_klientow_v2/`)
- lore i lekcje z realnych ofert
- przykłady dobrych i złych ofert (z komentarzem DLACZEGO)

AI ma ROZUMIEĆ, nie wykonywać checklistę. Formułki to shit.

---

## 6. Co kopiujemy ze starego bota (nie piszemy od zera)

- `storage.py` — magazyn, deduplikacja, checkpointy (ewentualnie)
- `browser_driver.py` — pobieranie zleceń, detale
- `form_driver.py` — wypełnianie i wysyłka formularza
- `config.py` — ścieżki, konta, filtry twarde (Czerwony Ocean / pułapki)

Te klocki są sprawdzone. V2 zmienia TYLKO mózg (generowanie oferty), nie mechanikę przeglądarki.

---

## 7. Otwarte pytania (do rozstrzygnięcia w toku)

1. Czy dziennik myślenia zapisujemy na dysk per zlecenie? (proponuję TAK — debug i dowód)
2. Ile maksymalnie iteracji, zanim bot uzna, że obraz jest pełny? (3 minimum, ale górny limit?)
3. Jak konkretnie wygląda „krytyk" — osobne AI, czy ten sam model w kolejnej iteracji?
4. Widełki: jak szerokie i jak je liczyć? (materiał edukacyjny vs twarda formuła)
5. Research: kiedy wchodzi — w iteracji 1 (analiza) czy 2 (weryfikacja)?

---

## 8. Kolejność pracy

1. [ ] Ustalić format dziennika myślenia (co dokładnie model ma odpowiedzieć w iteracji 1)
2. [ ] Wybrać i zebrać materiał edukacyjny do wstrzyknięcia
3. [ ] Zaprojektować pętlę iteracji (ile, kiedy stop, kiedy wraca)
4. [ ] Zaprojektować przejście: dziennik dojrzały → oferta (co DOPISAĆ/ODPOWIEDZIEĆ/DOPYTAĆ + wycena)
5. [ ] Dopiero potem: kod (kopiowanie klocków z V1)