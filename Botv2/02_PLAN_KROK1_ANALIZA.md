# BOT V2 — KROK 1: ANALIZA (plan szczegółowy, nietechniczny)

> Status: plan roboczy. Data: 2026-10-05.
> To jest opis JAK MA MYŚLEĆ bot w pierwszym kroku. Bez kodu, bez techniki. Czysty zamysł.
> Krok 1 to NIE pisanie oferty. To zrozumienie zlecenia i wyznaczenie granic.

---

## 0. Po co w ogóle ten krok

Bot nie może pisać, zanim nie zrozumie. Ale „zrozumieć" to nie znaczy „przeczytać". Zrozumieć to znaczy umieć odpowiedzieć na pytania:

- Kto tu decyduje i czego naprawdę chce?
- Co to za rodzaj zlecenia?
- Co klient powiedział, a czego NIE powiedział?
- Gdzie jest granica tego, co wolno napisać i o co wolno zapytać?
- Czy w ogóle jest sens wchodzić w merytorykę, czy trzeba milczeć?

Ten krok produkuje **dziennik myślenia** — zapis tego rozumienia. Nie ofertę. Jeszcze nic nie piszemy dla klienta.

Cały sens: **żeby pismo w kroku 3 wynikało z myślenia, a nie z szablonu.** Dziś V1 pisze od razu, dlatego wciska merytorykę na siłę i nie wie, kiedy milczeć.

---

## 1. Zasada nadrzędna kroku 1: ZLECENIE JEST GRANICĄ

Zlecenie wyznacza wszystko. Nie my, nie nasza wiedza, nie nasze chęci.

**Metafora włosa (z teorii):**
- Włos to zakres informacji, jaki dał klient.
- Trzeba go uciąć dokładnie tam, gdzie kończy się zlecenie.
- **Przed granicą** = za mało, nie wiemy, czego klient chce.
- **Na granicy** = dokładnie tyle, ile klient dał.
- **Za granicą** = zgadujemy, brzmimy jak AI, wyglądamy na desperatów.

**Kluczowe:** każde słowo ponad granicę to zgadywanie. A zgadywanie to śmierć. Dlatego krok 1 musi **precyzyjnie wyznaczyć granicę** — co zlecenie mówi, a czego nie.

---

## 2. Kolejność myślenia (osiem pytań)

Bot przechodzi przez osiem pytań, w tej kolejności. Każde ma pełne uzasadnienie niżej.

### PYTANIE 0 — Czy w ogóle jest sens składać ofertę?

**Co bot sprawdza:**
- Czy jest realny decydent (człowiek, który wybierze)?
- Czy jest budżet (choćby „do negocjacji")?
- Czy to nie scam / patologia / rekrutacja pod przykrywką?
- Czy zlecenie da się w ogóle wykonać i czy jest opłacalne?

**Dlaczego to pierwsze:** nie ma sensu analizować i pisać czegoś, czego nie powinniśmy wysyłać. V1 tego nie ma — wysyła ofertę nawet na zlecenia strukturalnie nie do wygrania (np. wymóg pracy w USA).

**Wynik:** TAK (idziemy dalej) / NIE (odrzucamy i NIE piszemy).

---

### PYTANIE 1 — Jaki to TYP ZLECENIA?

**Ważne:** typ ZLECENIA, nie typ klienta. To nie to samo.

**Możliwe typy:**
- projekt jednorazowy z deliverable (zrób mi apkę/stronę/integrację),
- stała współpraca / podwykonawstwo (kupuję twój czas),
- retainer (miesięczna opieka),
- audyt / diagnoza (przejrzyj i powiedz, co jest),
- egzamin wiedzy (klient sprawdza, czy się znamy),
- rekrutacja pod przykrywką (to nie zlecenie, to etat),
- doradcze (powiedz mi, co lepsze),
- scam / spekulacja (zbiera wyceny pod coś innego).

**Dlaczego to przed typem klienta:** od typu zlecenia zależy **tryb odpowiedzi**, a nie od tego, czy klient jest techniczny. Stała współpraca rządzi się innymi prawami niż jednorazowy projekt. Rekrutacja to w ogóle inny tryb. V1 miesza to — dlatego obsługuje ~80% rynku.

**Wynik:** jeden typ (albo kombinacja).

---

### PYTANIE 2 — Wykonawcze czy doradcze?

**Co bot sprawdza:** czy klient chce, żeby COŚ ZROBIĆ („zrób X"), czy żeby POWIEDZIEĆ, CO LEPSZE („czy warto", „co wybrać", „jak to ugryźć").

**Dlaczego:** to zmienia cały tryb.
- Wykonawcze → oferta.
- Doradcze → nie oferta, tylko „mądry kolega": mieszamy styl merytoryczny z laickim, dajemy tyle wiedzy, by pokazać kompetencję, ale nie sprzedajemy wiedzy za darmo. Proponujemy rozmowę.

Z teorii: „AI tego nie czuje, jeśli łańcuch nie ma kroku rozpoznania intencji". Dlatego to osobne pytanie.

**Wynik:** wykonawcze / doradcze / mieszane.

---

### PYTANIE 3 — Kto decyduje i czego NAPRAWDĘ chce?

**Co bot sprawdza:**
- Kto pisze: osoba prywatna, firma, agencja, pośrednik (PM/asystentka)?
- Co klient napisał, a co jest pod spodem? (ból biznesowy pod problemem technicznym)
- Czego NAPRAWDĘ chce, a czego tylko tak się wydaje?

**Dlaczego:** decyduje człowiek, nie „rynek". Trzeba wiedzieć, do kogo się pisze. I trzeba znaleźć **prawdziwy ból** — często nie jest techniczny. Przykład: w #145012 bólem nie jest „wyścig statusów", tylko „Subiekt nie wie, co sprzedaliśmy, nie mamy kontroli nad magazynem".

**Spark:** klient musi poczuć, że rozumiemy nie tylko JAK, ale PO CO mu to. Bez tego oferta jest zimna.

**Wynik:** profil decydenta + prawdziwy ból.

---

### PYTANIE 4 — Czy zlecenie jest wykonalne?

**Co bot sprawdza:** czy to, o co prosi klient, da się zrobić. Sprawdza SAM, zanim cokolwiek napisze.

**Dlaczego:** klient może pytać wprost („czy to da się zrobić"), albo tego nie mówić — a my i tak musimy znać odpowiedź. Jeśli się nie da tak, jak chce, nie mówimy „nie da się", tylko dajemy **najbliższą wykonalną opcję** („nie w ten sposób, ale tak").

**Wynik:** wykonalne / niewykonalne tak jak chce (wtedy najbliższa opcja).

---

### PYTANIE 5 — Czy jest POLE DO POPISU? (najważniejsze)

**Co bot sprawdza:** czy w tym zleceniu jest coś, czego klient NIE wie, a my wiemy?

**Dlaczego to serce kroku 1:** tu rozstrzyga się, czy w ogóle wchodzimy w merytorykę.

- **Jeśli TAK** → wchodzimy. Ale tylko wtedy, gdy wiemy SKĄD (patrz pytanie 6).
- **Jeśli NIE** → **nie piszemy merytoryki na siłę.** Idziemy ścieżką krótką: cena, zakres, pytanie.

Z teorii: „lepiej wykryć brak pola do popisu niż pisać merytorykę na siłę". W erze AI merytoryka przestała być przewagą — każdy ma AI i każdy może napisać mądrą ofertę. Przewagą jest trafność, naturalność i dawkowanie.

**Wynik:** pole do popisu JEST / NIE MA.

---

### PYTANIE 6 — Skąd wchodzi merytoryka? (trzy i tylko trzy ścieżki)

Jeśli pole do popisu JEST, bot ustala, **skąd** ono wynika. Są dokładnie trzy ścieżki:

**Ścieżka A — klient wprost pyta.**
Zadał konkretne pytanie, prosi o opinię, pyta „co lepsze", „czy da się", „czy warto". Wtedy odpowiadamy. Krótko, konkretnie, bez wykładu.

**Ścieżka B — mina albo ciekawostka.**
- **Mina** = coś, co klienta zabije albo narazi na stratę, jeśli się o tym nie dowie. Musi wiedzieć.
- **Ciekawostka** = coś, co realnie pomaga i zachęca, ale nie jest konieczne.
- Każda mina musi być oparta na DOWODZIE z zlecenia, nie na domysle.

**Ścieżka C — udowodniona alternatywa.**
Jest lepsza droga niż ta, którą klient obrał. Możemy ją zaproponować, ale tylko jeśli mamy dowód. Dobieramy ton do ilości informacji, jakich dał klient.

**Jeśli żadna z trzech ścieżek nie zachodzi → merytoryka NIE WCHODZI.** Koniec. Zero nazw bibliotek, zero architektury, zero „trzech kroków". Research zostaje dla nas, nie dla klienta.

**Bramka researchu (złoto z V1) — jak bot rozpoznaje, czy to fakt, czy zgadywanie:**
- „jeśli to jest X, to...", „zwykle bywa, że...", „prawdopodobnie..." → **ZGADUJĘ**. Research OFF, merytoryka OFF.
- „w Państwa procesie X, więc Y", „odpowiadając na pytanie o X..." → **ODPOWIADAM**. Research ON.
- Sama nazwa technologii to NIE zaproszenie do merytoryki. Nazwa bez procesu i bez pytania to za mało.
- W razie wątpliwości: **OFF**, bo brak researchu kosztuje mniej niż research na siłę.

**Wynik:** ścieżka A / B / C / żadna.

---

### PYTANIE 7 — Czego nie wiemy, a bez czego NIE da się wycenić?

**Co bot sprawdza:** jakie informacje są konieczne do wyceny, których klient nie podał.

**Kryterium jedyne:** czy bez odpowiedzi da się wycenić?
- Jeśli NIE da się → pytanie wchodzi.
- Jeśli da się → to jest za granicą, wycinamy.

**Każde pytanie z uzasadnieniem:** „nie pisaliście o tym, więc pytam, bo od tego zależy X". To pokazuje, że przeczytaliśmy ogłoszenie uważnie i pytanie nie jest z szablonu.

**Liczba pytań wynika ze zlecenia, nie z szablonu.** Raz jedno, raz pięć.

**Wynik:** lista pytań (tylko koniecznych).

---

## 3. WYZNACZANIE GRANIC — co mówi zlecenie, o co NIE pytać

To jest osobna, kluczowa część kroku 1. Bot musi **dokładnie** wiedzieć, gdzie leży granica.

### 3.1. Co zlecenie MÓWI (fakty do wykorzystania)
Bot wypisuje wszystko, co klient faktycznie napisał:
- technologie, które wymienił,
- problemy, które opisał,
- pytania, które zadał,
- zakres, który określił,
- termin/budżet, jeśli podał.

To jest materiał, na którym WOLNO pracować. Nic poza tym.

### 3.2. Czego zlecenie NIE mówi (strefa zakazana)
Bot wypisuje wszystko, czego klient NIE napisał. Do tej strefy **nie wolno wchodzić bez pytania**. Przykłady zakazanych ruchów:
- zakładać technologię, której klient nie podał,
- dopisywać funkcje, o których nie było mowy,
- domyślać się modelu rozliczenia,
- zgadywać skalę (ilu użytkowników, ile zamówień),
- tworzyć korzyści na siłę, żeby zabrzmiały.

### 3.3. O co NIE WOLNO pytać (i dlaczego)

To jest sedno. Bot musi odrzucać pytania, które byłyby **zgadywaniem w przebraniu pytania**. Kryterium: **czy bez odpowiedzi da się wycenić?** Jeśli tak — pytanie jest za granicą, wycinamy.

**Zakazane pytania i ich uzasadnienie:**

1. **Pytania o rzeczy oczywiste z kontekstu.**
   - Przykład z teorii: klient napisał „najwyższa wersja PHP" → pytanie „po co migrujesz" jest useless, bo i tak zrobimy najnowszą.
   - Uzasadnienie: odpowiedź nie zmieni niczego w wycenie ani w ofercie. To zgadywanie, że czegoś nie wiemy, choć wiemy.

2. **Pytania, które brzmią jak przepytywanie.**
   - Kryterium z teorii: pytanie musi być ALBO akceptowalne (nie za granicą cięcia, nie brzmi jak egzamin), ALBO ważne dla wyceny.
   - Uzasadnienie: za dużo pytań = brzmimy jak AI i jak ktoś, kto nie ogarnia. Człowiek pewny siebie pyta mało.

3. **Pytania o rzeczy, które klient już powiedział albo dał do zrozumienia.**
   - Uzasadnienie: to echo klienta, brak szacunku dla jego czasu, znak że nie przeczytaliśmy.

4. **Pytania „na wszelki wypadek".**
   - Uzasadnienie: jeśli nie musimy wiedzieć, nie pytamy. Każde zbędne pytanie to zgadywanie, że nam to potrzebne.

5. **Pytania, na które odpowiedź i tak nie zmieni wyceny.**
   - Uzasadnienie: jeśli nie wpływa na cenę ani na zakres, to jest za granicą.

**Reguła:** jeśli po zadaniu sobie pytania „a co, jeśli klient odpowie X, a co jeśli Y?" wycena i oferta wychodzą takie same — pytanie jest zbędne. Wycinamy.

### 3.4. Czym jest zgadywanie (do wykrywania)
Bot musi rozpoznawać własne zgadywanie. Sygnały:
- używam słów „jeśli", „zwykle", „prawdopodobnie", „zazwyczaj",
- dopisuję korzyść, której nie ma w zleceniu,
- zakładam coś, żeby zdanie zabrzmiało,
- muszę coś dodać, bo inaczej oferta jest za krótka.

Każdy z tych sygnałów → STOP. To za granicą.

### 3.5. Zasada „nie ma nic z merytoryki → nie wchodzimy"
Jeśli pole do popisu NIE ISTNIEJE (klient nic nie napisał, o nic nie pyta, nie ma miny) — **merytoryka nie wchodzi.** Chyba że klient wprost pyta — wtedy odpowiadamy, ale krótko i konkretnie.

To jest twarda zasada. Nie „staramy się coś znaleźć". Nie „dorzucimy coś mądrego". Cisza jest lepsza niż wata. Krótka oferta lepsza niż długa.

---

## 4. Co krok 1 produkuje (dziennik myślenia)

Na koniec krok 1 zostawia zapis — dziennik myślenia. Zawiera odpowiedzi na wszystkie osiem pytań:

1. Kwalifikowalność: tak/nie.
2. Typ zlecenia.
3. Intencja: wykonawcze/doradcze.
4. Kto decyduje + prawdziwy ból.
5. Wykonalność (+ najbliższa opcja, jeśli nie).
6. Pole do popisu: jest/nie ma.
7. Skąd merytoryka: ścieżka A/B/C/żadna.
8. Pytania konieczne (+ uzasadnienie każdego).
9. **Granice:**
   - co zlecenie MÓWI,
   - czego NIE mówi,
   - o co NIE pytać i DLACZEGO (bo zgadywanie),
   - gdzie przebiega linia cięcia (długość, głębokość).

Dziennik jest zapisywany. Dzięki temu w kroku 3 pismo widzi własne myślenie — wie, DLACZEGO mówi albo milczy.

---

## 5. Zasady, które rządzą krokiem 1 (ściągawka)

1. Zlecenie jest granicą. Nic ponad to, co dał klient.
2. Nie zgadujemy. Sygnały zgadywania → STOP.
3. Merytoryka domyślnie ZERO. Wchodzi tylko ścieżką A, B lub C.
4. Brak pola do popisu → merytoryka nie wchodzi (chyba że klient pyta).
5. Pytamy tylko o to, bez czego nie da się wycenić.
6. Każde pytanie z uzasadnieniem, po co pytamy.
7. Krok 1 nie pisze oferty. Produkuje rozumienie.
8. Na styk — nigdy przed, nigdy za granicą.

---

## 6. Otwarte do dopracowania w kolejnych krokach

1. Jak konkretnie rozpoznawać typ zlecenia (pytanie 1) — jakie sygnały?
2. Jak działać przy sprzeczności widełki vs jawny budżet vs cena od razu?
3. Jak wygląda detektor kwalifikowalności/scamów (pytanie 0)?
4. Jak dobrać rejestr żargonu bez podziału techniczny/nietechniczny?
5. Czy dziennik myślenia ma stały format, czy swobodny?