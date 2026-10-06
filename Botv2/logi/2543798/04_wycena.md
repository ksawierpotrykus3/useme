=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
## Wycena

**Etap 0 — makiety UX + architektura + backlog**
- Czas: 5–7 dni roboczych
- Kwota: **3 600 – 5 400 zł**

**MVP na 1 lokal** (stoliki, menu, koszyk, WYŚLIJ, płatności: całość + split równo, panel admin podstawowy)
- Czas: 8–11 tygodni
- Kwota: **31 500 – 45 000 zł**

**Wersja produkcyjna na 8 lokali** (rollout + multi-tenant + split po pozycjach + QR gościa z zamówieniem)
- Czas: dodatkowe 6–9 tygodni
- Kwota: **22 500 – 36 000 zł**

**Razem z etapem 0: 57 600 – 86 400 zł**, rozłożone na etapy, płatne po każdym.

## Uzasadnienie

Split po pozycjach z zachowaniem opłaconych pozycji jako wyszarzone to nie funkcja bramki — żadna polska bramka (P24/PayU/Stripe) nie daje tego „z pudełka”. To osobny silnik rozliczeniowy w architekturze, nie konfiguracja, i to główny czynnik ceny. Rollout na 8 lokali to nie kopiuj-wklej — trzeba rozstrzygnąć, czy dzielą menu i bazę, czy każde ma własne.

## Rekomendacja techniczna

**React Native** (backend Node + PostgreSQL) — mniejszy bundle, ekosystem JS, szybszy prototyp na małych ekranach. Jeśli POS ma integrować się z fizycznymi terminalami płatniczymi, może wymusić podejście natywne/hybrydowe — to zmienia wycenę.

## Czego brakuje, żeby wycena była dokładna

1. **Płatności w POS** — kelner rozlicza przez terminal fizyczny (jakiego producenta?) czy przez płatność online z aplikacji? Od tego zależy zakres integracji i czy split da się domknąć w jednym silniku z QR gościa.
2. **Kuchnia/bar** — macie już drukarki kuchenne lub KDS, z którymi mamy się zintegrować, czy definiujemy własny ticket? To dwa różne zakresy.
3. **8 lokali** — jedna wspólna baza z jednym menu, czy każde miasto/lokal ma własne menu, ceny i rozliczenia? Decyduje o architekturze (multi-tenant vs single-tenant) i o tym, czy rollout to konfiguracja, czy osobne wdrożenia.

Po tych trzech odpowiedziach zwężę widełki dla wersji 8-lokalowej. Etap 0 ma sens przed nią — inaczej wyceniam na ślepo.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena jest metodologicznie poprawna i nic nie dopisałem na siłę — etapowanie, teza o własnym silniku split i React Native jako rekomendacja wynikają wprost z briefu i researchu, a nie z chęci podbicia stawki. Ale jedno bym skorygował: **dolna granica MVP (31 500 zł / 8 tygodni) jest zbyt optymistyczna**, jeśli split po pozycjach ma być w MVP — to osobny moduł rozliczeniowy, nie konfiguracja, i przy 90 zł/h realnie potrzebuję na to 380–420 h, nie 350. Proponuję **MVP: 36 000 – 45 000 zł, 9–11 tygodni**, a wersja 8-lokalowa bez zmian (22 500 – 36 000 zł), bo tam widełki już zawierają niepewność multi-tenant. Górne widełki zostawiłbym, bo jeśli dojdą terminale fizyczne albo integracja z Pyszne/Uber/Glovo, kwota pójdzie w górę i to nie jest widzimisię, tylko zakres. Etap 0 (3 600 – 5 400 zł) bez zmian — to najtańszy sposób, żeby przestać zgadywać.

=== DeepSeek-B — RUNDA 1 ===
Wycena wstępna (90 zł/h, solo, umowa o dzieło):

**Etap 0 — makiety UX + architektura + backlog**  
40–60 h → **3 600–5 400 zł**, ok. **5–8 dni**

**MVP — 1 lokal**  
Stoliki, menu, koszyk, WYŚLIJ, podstawowe płatności split  
350–550 h → **31 500–49 500 zł**, ok. **45–70 dni roboczych**

**Wersja produkcyjna na 8 lokali**  
Multi-tenant, rollout, panel admina, QR gościa, płatności, integracje, testy  
700–1 200 h → **63 000–108 000 zł**, ok. **90–150 dni roboczych**  
Łącznie z MVP: **94 500–157 500 zł**

**Uzasadnienie:**  
Split po pozycjach z zachowaniem opłaconych pozycji to własny silnik rozliczeniowy, nie funkcja bramki — dlatego traktuję go jako osobny moduł. Rollout na 8 lokali to nie kopiuj-wklej: potrzebna jest architektura multi-tenant i decyzja o wspólnym menu/cenach. Rekomenduję React Native + Node/PostgreSQL.

**Czego brakuje do zawężenia wyceny:**  
1. Płatności w POS: terminal fizyczny czy online?  
2. Kuchnia/bar: istniejący KDS/drukarki czy definiujemy własny ticket?  
3. 8 lokali: jedna wspólna baza/menu czy osobne menu i rozliczenia per lokal?  

Po tych 3 odpowiedziach podam dokładniejsze widełki.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: wycena jest poprawna co do rzędu wielkości, ale górne widełki MVP (550 h) są ostrożnościowe — przy realnie wąskim MVP (stoliki, menu, koszyk, WYŚLIJ, split całość/na równo) bliżej 280–420 h. Nie zgadłem dwóch rzeczy: (1) czy „menu jak delivery” znaczy tylko UX, czy realną integrację z Pyszne/Uber/Glovo — to zmienia zakres o kilkadziesiąt godzin; (2) czy 8 lokali to jedna firma z jedną bazą, czy franczyza z osobnymi rozliczeniami — przy franczyzie rollout to nie konfiguracja, tylko osobne wdrożenia. Nie dopisałem na siłę — świadomie pominąłem offline, bo klient go nie wymienił, ale powinienem był zaznaczyć, że online-first z kolejką to moje założenie, nie jego wymóg. Kwoty zostawiam, ale dolną granicę MVP obniżyłbym do ~28 000 zł, żeby nie odstraszyć, a górną zostawił jako widełki „z buforem na integracje”.

=== DeepSeek-C — RUNDA 1 ===
## Wycena

**Etap 0 — makiety UX + architektura + backlog**
**3 600 – 5 400 zł** | 5–7 dni roboczych

**MVP na 1 lokal** (stoliki, menu, koszyk, WYŚLIJ, płatność całość + split równo)
**22 000 – 32 000 zł** | 6–9 tygodni

**Wersja produkcyjna na 8 lokali** (multi-tenant, QR gościa, split po pozycjach z mapowaniem, panel admin, rollout, testy, wdrożenie)
**45 000 – 75 000 zł** | 8–14 tygodni

---

## Uzasadnienie (2–3 zdania)

Split po pozycjach z zachowaniem opłaconych jako wyszarzone to **własny silnik rozliczeniowy**, nie funkcja bramki — żadna polska bramka (P24/PayU/Stripe) nie daje tego „z pudełka”, więc traktuję to jako osobny moduł w architekturze i to głównie on podnosi wycenę produkcji. MVP wyceniam wąsko (jeden lokal, split tylko równo), żeby dało się je domknąć i przetestować na sali, zanim wejdziemy w 8 lokalizacji. Rollout na 8 lokali to nie konfiguracja, a wdrożenia — dlatego widełki są szerokie i domknę je po odpowiedziach poniżej.

---

## Czego brakuje w zleceniu (3 pytania)

1. **Płatności w POS** — kelner rozlicza przez terminal fizyczny (jaki producent?), czy przez płatność online (BLIK/przelew/karta) wywoływaną z aplikacji? Od tego zależy zakres integracji i to, czy split częściowy domknie się w jednym silniku z QR gościa. Terminal z certyfikowanym SDK może wymusić podejście natywne.

2. **Kuchnia/bar** — macie już drukarki kuchenne lub KDS, z którymi mamy się zintegrować, czy system ma dostarczyć ticket w formie, jaką sami zdefiniujemy? „Ticket” bez adresata to albo integracja z konkretnym sprzętem, albo własny moduł druku/KDS — dwa różne zakresy i dwie różne wyceny.

3. **8 lokali** — jedna wspólna baza z jednym menu i raportem, czy każde miasto/lokal ma własne menu, ceny i rozliczenia? To decyduje o architekturze (multi-tenant vs single-tenant) i o tym, czy rollout to konfiguracja, czy osobne wdrożenia.

---

## Technologia — rekomendacja

**React Native** (front POS + QR gościa), **Node + PostgreSQL** (backend, multi-tenant). Uzasadnienie jednym zdaniem: mniejszy bundle i ekosystem JS/React = szybszy prototyp na małych ekranach i łatwiejsze utrzymanie przy etapowym rozwoju.

Jeśli któraś z powyższych odpowiedzi zmieni zakres (terminal fizyczny, integracja z istniejącym KDS, osobne bazy per lokal) — dostroję widełki.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: **MVP trzyma się kupy** (22–32k przy 90 zł/h to ~245–355h, realne dla jednego lokalu z wąskim splitem równo). Ale **produkcja na 8 lokali jest moim zdaniem niedoszacowana** — 45k to 500h, a sama warstwa multi-tenant + własny silnik splitu po pozycjach + panel admin + rollout 8 wdrożeń to spokojnie 600–900h, więc uczciwe widełki to raczej **55 000 – 90 000 zł**, nie 45–75k. Nie zgadłem też jednej rzeczy: jeśli okaże się, że POS musi gadać z **fizycznym terminalem** (certyfikowane SDK, PCI PTS), to cross-platform może nie wystarczyć i dochodzi natywny moduł — to podnosi i MVP, i produkcję, dlatego trzymam to jako jawny warunek zmieniający wycenę, a nie ukryty bufor. Etapu 0 (3,6–5,4k) nie ruszam — to dobra cena za makiety, architekturę i backlog, i realnie chroni obie strony przed przepaleniem budżetu na źle oszacowanym MVP.

=== DeepSeek-D — RUNDA 1 ===
## Wycena

**Etap 0 — makiety UX + architektura + backlog**
3 000 – 4 500 zł | 7–10 dni roboczych
Bez tego nie wycenię produkcyjnie uczciwie — a Ty nie podejmiesz decyzji o budżecie na 8 lokali w ciemno.

**MVP (1 lokal, wąski zakres: stoliki + menu + koszyk + WYŚLIJ + płatność całość/po równo)**
45 000 – 65 000 zł | 60–90 dni roboczych
Zakres: POS mobile (React Native — mniejszy bundle, ekosystem JS, szybszy prototyp na małych ekranach), QR menu dla gościa (web), panel admin, backend + PostgreSQL, płatności online (BLIK/przelew/karta).

**Wersja produkcyjna na 8 lokali (MVP + rollout + hartowanie + raporty)**
70 000 – 100 000 zł | 100–140 dni roboczych
Rollout to nie kopia — to multi-tenant, uprawnienia per lokal, menu/ceny per lokal, raporty zbiorcze, szkolenia, wsparcie powdrożeniowe.

---

## Co zmienia wycenę (i dlaczego pytam)

**Split po pozycjach z zachowaniem opłaconych pozycji jako wyszarzone to własny silnik rozliczeniowy, nie funkcja bramki** — żadna polska bramka (P24, PayU, Stripe) nie daje tego „z pudełka”. W architekturze traktuję to jako osobny moduł. To główny koszt w MVP i główne ryzyko.

Trzy pytania, od których zależą widełki:

1. **Płatności w POS** — kelner rozlicza przez terminal fizyczny (jakiego producenta?) czy przez płatność online wywoływaną z aplikacji? Jeśli terminal z certyfikowanym SDK (Ingenico/PAX), może wymusić natywne podejście lub hybrydę — to zmienia stack i wycenę.

2. **Kuchnia/bar** — macie już drukarki kuchenne lub KDS, z którymi mamy się zintegrować, czy system ma dostarczyć ticket w formie, jaką sami zdefiniujemy? „Ticket” bez adresata to albo integracja z konkretnym sprzętem/API, albo własny moduł druku/KDS — dwa różne zakresy.

3. **8 lokali** — jedna wspólna baza z jednym menu i raportem, czy każde miasto/lokal ma własne menu, ceny i rozliczenia? To decyduje o architekturze (multi-tenant vs single-tenant) i o tym, czy rollout to konfiguracja, czy osobne wdrożenia.

---

## Czego brakuje w zleceniu

- Czy QR gościa w MVP tylko zamawia, czy też płaci? (od tego zależy, czy silnik split obsługuje gościa, czy tylko kelnera)
- Czy „podstawowe płatności split” w MVP = całość + po równo, a „po pozycjach” dopiero w etapie 2?
- Czy wchodzą integracje z Pyszne/Uber/Glovo? Opis mówi „menu jak delivery” — to może znaczyć tylko wygląd, albo realne API agregatorów. Różnica: ~10–20k zł.
- RODO wobec danych gości z QR — czy zbieramy dane, czy tylko zamówienie anonimowe?

Odpowiedz na 3 pytania powyżej, a zawężę widełki produkcyjne do konkretu. Etap 0 mogę zacząć w ciągu tygodnia.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: **Etap 0 zaniżyłem** — 3000–4500 zł to 33–50h, a same makiety UX + architektura + backlog dla tego zakresu to realnie 40–60h; koryguję na **4000–6000 zł**.

**MVP (45–65k)** trzyma się dolnej granicy widełek, ale przy własnym silniku split (mapowanie pozycja→płatność, stany częściowe), real-time dla kelner/KDS i osobnej web-appce QR — 500–720h to raczej **560–800h**, więc realniej **50–70k zł** przy założeniu, że płatności są online, a nie przez terminal fizyczny.

**Produkcja na 8 lokali (70–100k)** — widełki OK, ale górna granica może pęknąć, jeśli rollout okaże się per-lokalny, a nie konfiguracją multi-tenant; dlatego pytanie nr 3 jest kluczowe.

Czego nie zgadłem: rekomendacja React Native to wciąż **rekomendacja**, nie ustalenie — jeśli wejdzie terminal z certyfikowanym SDK, wracamy do native/hybrydy i kwota MVP idzie w górę. Nie dopisałem na siłę niczego poza tym — integracje Pyszne/Uber/Glovo świadomie zostawiłem poza wyceną, bo brief ich nie wymaga.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 80000,
  "kwota_gorna": 140000,
  "definitywna": false,
  "od_czego_zalea": [
    "Płatności w POS: terminal fizyczny z certyfikowanym SDK vs płatność online z aplikacji",
    "Kuchnia/bar: integracja z istniejącym KDS/drukarkami vs własny moduł ticketów",
    "8 lokali: wspólna baza multi-tenant vs osobne menu, ceny i rozliczenia per lokal",
    "QR gościa w MVP: tylko zamówienie vs zamówienie i płatność",
    "Integracje z Pyszne/Uber/Glovo oraz wymagania offline"
  ],
  "dni_od": 110,
  "dni_do": 200,
  "uzasadnienie": "Finalna wycena obejmuje całość: Etap 0 + MVP na 1 lokal + wersję produkcyjną na 8 lokali. Modele były zgodne co do etapu 0 (ok. 4–6 tys. zł), tezy o własnym silniku split po pozycjach oraz rekomendacji React Native + Node/PostgreSQL. Rozbieżność dotyczyła głównie MVP (22–70 tys. zł) i produkcji na 8 lokali (22,5–108 tys. zł dodatkowo), bo brakuje trzech kluczowych decyzji: płatności, KDS i modelu multi-tenant. Dlatego podaję widełki 80–140 tys. zł; górna granica może wzrosnąć przy terminalach fizycznych, istniejącym KDS, integracjach z agregatorami lub osobnym wdrożeniu per lokal."
}

=== FINALNA WYCENA ===
80000-140000 zl netto | 110-200 dni | WIDELKI
Od czego zalezy: brak
Uzasadnienie rozjemcy: Finalna wycena obejmuje całość: Etap 0 + MVP na 1 lokal + wersję produkcyjną na 8 lokali. Modele były zgodne co do etapu 0 (ok. 4–6 tys. zł), tezy o własnym silniku split po pozycjach oraz rekomendacji React Native + Node/PostgreSQL. Rozbieżność dotyczyła głównie MVP (22–70 tys. zł) i produkcji na 8 lokali (22,5–108 tys. zł dodatkowo), bo brakuje trzech kluczowych decyzji: płatności, KDS i modelu multi-tenant. Dlatego podaję widełki 80–140 tys. zł; górna granica może wzrosnąć przy terminalach fizycznych, istniejącym KDS, integracjach z agregatorami lub osobnym wdrożeniu per lokal.
