# RAPORT: TEST GENERATORA NA 4 SKRAJNIE RÓŻNYCH DOMENACH

**STATUS: HISTORYCZNE (oceny konkurencji)** | Data testu: 2026-09-26.

> Ten raport zachowuje **wyłącznie niezależne oceny klientów AI** dla czterech domen (3D WebGL, BaseLinker, CloudTalk→Notion, CNC EN).
> Usunięto pełne teksty wygenerowanych ofert V6 (zawierały myślniki, nawiasy i stopkę — łamią obecne zasady i nie mogą służyć za wzór).
> Średnia ocen: 92 / 82 / 83 / 88 = ~86,3/100.
> Wnioski o kodzie/silniku: nieaktualne (kod ewoluował, patrz `docs/STANDARD_DOKUMENTACJI.md`).

---

## Zlecenie #144092: Konfigurator mebli 3D (Three.js / PrestaShop)

### Ocena Klienta AI: 92/100

**1. Dopasowanie domenowe: 9/10**
Wykonawca wprost odnosi się do kluczowych problemów konfiguratorów 3D opartych na Three.js:
- **VRAM i dispose()** – wie, że Three.js nie zwalnia automatycznie geometrii i materiałów, co przy zmianach parametrów prowadzi do wycieków pamięci i crashy na mobile.
- **Draco/KTX2** – wymienia realne narzędzia do kompresji modeli 3D.
- **Jednostki i walidacja** – wspomina o mieszaniu cm/mm, usłojeniu, obrzeżach, niekompletnych modułach.
- **Oddzielenie stanu konfiguracji od sceny 3D** – kluczowe dla integracji z koszykiem i PrestaShop (czysty JSON, SKU, cena).
- **Pytanie o PrestaShop API vs JSON** – trafne, operacyjne.

**2. Język i styl: 10/10**
Ton naturalny, partnerski, ludzki. Widać człowieka, nie generator. Brak błędów, kalk, sztucznej nowomowy.

**3. Bezpieczeństwo i etapy: 8/10**
Plusy: staging na kopii (zero ryzyka dla demo), dwa etapy płatne po odbiorze, darmowy audyt kodu przed wyceną, pytanie operacyjne o integrację.
Minusy: brak widełek cenowych (zrozumiałe — najpierw chce kod), brak mowy o testach na różnych przeglądarkach.

**4. Decyzja: 92/100.** Odpisałbym na priv bez wahania. Konkretna wiedza techniczna + przełożenie na język biznesowy. Ewentualny minus: optymistyczny harmonogram (2 × 9 dni) — do weryfikacji po audycie.

---

## Zlecenie #144038: Administrator BaseLinker (stała opieka)

### Ocena Klienta AI: 82/100

**1. Dopasowanie domenowe: 8,5/10**
Konkretne pojęcia: BaseLinker ↔ Comarch XL, FS z WZ, moduł Procesy, WZ, SKU, magazyny, statusy zamówień, marketplace, integracje kurierskie, API vs mostek pośredni, idempotentność, deduplikacja po kluczu biznesowym. Rozumie istotę problemu: przepływ danych i kontrola procesów, nie samo klikanie zamówień.
Zastrzeżenie: część doświadczenia z Enova365, nie z Comarch XL — do weryfikacji referencjami.

**2. Język i styl: 9/10**
Naturalny, partnerski, konkretny. Miejscami sprzedażowo, ale w granicach dobrego ogłoszenia.

**3. Bezpieczeństwo i etapy: 7/10**
Plusy: zero surowego SQL na produkcji, środowisko testowe, płatność po odbiorze etapu, darmowa diagnoza 1–3 przypadków, pytanie o API vs mostek.
Minusy (poważne względem ogłoszenia): brak modelu stałej opieki (retainer, SLA, czas reakcji, eskalacja), etapy projektowe zamiast utrzymaniowych, „12 miesięcy gwarancji" nie chroni przed zmianami API, nie wiadomo kto administruje VPS po wdrożeniu.

**4. Decyzja: 82/100.** Odpisałbym na priv, ale jako wstęp do negocjacji stałej opieki. Najważniejszy minus: nie zaadresował sedna ogłoszenia (utrzymanie i reagowanie na awarie w trybie ciągłym).

---

## Zlecenie #143981: Integracja API CloudTalk.io → Notion

### Ocena Klienta AI: 83/100

**1. Dopasowanie domenowe: 8/10**
Wymienia konkretne elementy: dopasowanie kontaktu po numerze telefonu, obsługa nowego numeru (auto-karta), kumulacja wielu rozmów na jednej karcie, transkrypcja + notatka AI + link + data, edge case'y (brak transkrypcji, rozmowa nieodebrana). To nie szablon z faktur/ERP.
Rysa: nie odnosi się do ograniczeń planu Essential. Z pricing wynika, że **API i standardowe integracje dostępne dopiero od planu Expert** — może być potrzebny upgrade, dodatkowy stały koszt, którego wykonawca nie sygnalizuje. Drugi drobiazg: nie wspomina o add-onie AI Conversation Intelligence ($9/user/mies.).

**2. Język i styl: 9/10**
Naturalny, partnerski, ludzki. „Dzień dobry", „Zanim podejmiemy decyzję". Zero błędów. Minus: momentami za dużo narracji o sobie.

**3. Bezpieczeństwo i etapy: 9/10**
Wzorowy podział: płatność 50/50, etap 1 to konfiguracja + testy na 5–10 rozmowach, etap 2 to pełne wdrożenie + historia + edge case'y + wideo. Bezpieczeństwo: „nie nadpisuję i nie kasuję niczego", testy na kopii, idempotencja, 30 dni asysty, 12 miesięcy gwarancji. Darmowa próbka testowa na 2–3 rozmowach — świetny ruch.
Zastrzeżenie: brak precyzji co do czasu etapów i całkowitego kosztu.

**4. Decyzja: 83/100.** Odpisałbym na priv zdecydowanie. Najważniejszy minus: przemilczenie kwestii planu Essential (możliwy konieczny upgrade). Gdyby nie to — 90+.

---

## Zlecenie #144165: CNC Punch Software / Postprocessor (LVD, ADTECH)

### Ocena Klienta AI: 88/100

**1. Dopasowanie domenowe: 9/10**
Realnie rozumie CNC punch: grupowanie cięć po tool station + kąt dla Auto-Index, podział grupy w bezpiecznym punkcie przy reposition/clamp, stabilny model segmentów dla Micro-Joint, dodanie micro-jointa nie przesuwa istniejących, minimalna długość wykrawania, postprocessor to mapowanie a nie zgadywanie, golden reference + diff check dla tool selection / współrzędnych / kątów / reposition / clamp logic. Brakuje pytania o źródła/SDK NibblePro.

**2. Język i styl: 9/10**
Angielski naturalny, techniczny, partnerski. Drobiazgi: „You see the result on your own material" nieprecyzyjne, „There is no mandatory monthly server cost" trąci szablonem SaaS, sekwencja „punch clear area, reposition, clamp, continue" uproszczona (brak unclamp/reclamp).

**3. Bezpieczeństwo i etapy: 8/10**
Sensowny podział: Stage 1 (analiza, test harness, Auto-Index grouping, micro-joint), Stage 2 (pełny postprocessor ADTECH, reposition/clamp, testy, wsparcie). Płatność po akceptacji każdego etapu, darmowy dry test, praca na kopii, wersjonowanie, rollback, brak edycji live postprocessora.
Haczyki: brak zdefiniowanych kryteriów akceptacji, brak pytania o dostęp do źródeł/SDK NibblePro, cena 12 000 PLN i 21 dni mogą być optymistyczne.

**4. Decyzja: 88/100.** Odpisałbym na priv jako zaproszenie do doprecyzowania. Najważniejszy plus: rozumie, że Auto-Index, Micro-Joint, clamp/reposition i postprocessor to jeden system, i proponuje walidację offline na golden samples przed dotknięciem maszyny. Najważniejszy minus: brak pytania o źródła/SDK i twardych kryteriów odbioru.

---

## Wnioski przekrojowe (4 domeny)

| Domena | Ocena | Co działało najlepiej | Co było ryzykiem |
|---|---|---|---|
| Konfigurator 3D | 92 | Konkret techniczny (VRAM, dispose, Draco) + język biznesowy | Optymistyczny harmonogram |
| BaseLinker | 82 | Konkret domenowy, darmowa diagnostyka na sucho | Nie zaadresował stałej opieki (sedno ogłoszenia) |
| CloudTalk → Notion | 83 | Edge case'y, etapowanie, darmowy test | Przemilczenie limitu planu Essential |
| CNC / ADTECH | 88 | Walidacja offline przed maszyną, systemowe podejście | Brak SDK/kryteriów odbioru |

**Wspólny wzorzec:** najwyżej oceniane oferty łączą **konkret techniczny** z **bezpieczeństwem wdrożenia** (staging/kopia, etapy płatne po odbiorze, darmowy dry-run). Przemilczenie ukrytych kosztów lub ograniczeń planu obniża ocenę o 7–10 punktów.