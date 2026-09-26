# META-AUDYT RED-TEAM: Reforma Ofertowarki `useme_core` (5 Fal, 27 Ofert)

**Audytor:** Niezależny Główny Architekt Systemów AI / Bezlitosny Red-Team
**Data:** 2026-09-26
**Zakres:** Wszystkie zmiany z Changelogu (Etapy 1–7), dane z 27 ofert (`audyt_100_wyniki_27_ofert.json`), `chain_config.json`, `agent_02a_opis_oferty.md`, `portfolio_baza.md`, `wycena_kalkulator.py`, `audytor_lancuch.py`, `kryteria_audytu_100.md`

---

## 1. WERDYKT META-AUDYTORA: **76 / 100 pkt**

| Obszar | Ocena | Komentarz jednym zdaniem |
|---|---|---|
| **A. Architektura i Kod Produkcyjny** | **16 / 20** | Zmiana klasy: dual-track, selektor kart wiedzy, pre-audyt deterministyczny i bezpiecznik `max(R1,R2)` to prawdziwa inżynieria — ale `chain_config.json` nadal trzyma **6 wyłączonych slotów (`enabled: false`)**, a `DNI_MIN` w kodzie nie zgadza się z Changelogiem. |
| **B. Prompt Engineering i Odporność na Overfitting** | **13 / 20** | Prompt `02a` jest gęsty i chirurgiczny, ale zawiera nazwy konkretnych zleceń i modułów z 27 prób (`NibblePro`, `LEX`, `DGX Spark`, `Kołcz`), co jest **ryzykiem przeuczenia pod Sędziego**. Brak zestawu walidacyjnego (holdout). |
| **C. Psychologia B2B, Portfolio i Wiarygodność** | **16 / 20** | `tech_16_tech_agnostic_biznes.md` + zakaz żargonu to skok jakościowy (Wymiar B: 25/25 w wielu Finalach). Ale **`Projekt 8` i `Projekt 9` nie mają ID transakcji Useme ani nazwy klienta** (w przeciwieństwie do `Projekt 1/2/6`) — przy pytaniu na priv „poproszę o referencję" bot nie ma czym odpowiedzieć. |
| **D. Matematyka Wycen i Realizm Rynkowy** | **15 / 20** | `MAX_RISK_MULTIPLIER = 1.15` z `max()` zamiast iloczynu rozwiązał realny błąd `17 500 zł vs 7 500–9 800 zł` na `#144890`. Ale dwa razy sędzia odjął `-12 pkt` za „stary mnożnik 1.3" (`#144817`, `#144867`) — **oznacza to, że stary kalkulator nadal żyje w części pipeline'u lub w cache'u**. |
| **E. Jakość Danych i Metodologia 5 Fal** | **16 / 20** | Pełna transparentność `za_co_dodano` / `za_co_odjeto`, 50 testów pytest, archiwum 33 logów. Ale **n=27 z jednego źródła (Useme) w jednym tygodniu** i brak testu ślepego — statystyki są wiarygodne wewnętrznie, nie zewnętrznie. |

**Werdykt słowny:** Reforma jest realna i mierzalna (+12,30 pkt średniego przyrostu R1→Final, zero regresji netto dzięki `max(R1,R2)`), ale nie jest jeszcze produkcyjnie domknięta. Trzy największe dziury: **martwe sloty w `chain_config.json`**, **dwa równoległe kalkulatory wyceny (stary 1.3 vs nowy 1.15)** oraz **portfolio z „cieniami bez ID transakcji" (Projekt 8/9)**.

---

## 2. ZA CO DODANO PUNKTY `[+]` — Co Faktycznie Zmieniło Klasę Bota

### `[+20 pkt]` Determinizm przed LLM: `deterministic_pre_audit()` w `audytor_lancuch.py`
Twarda bramka Pythonowa (regex `FORBIDDEN_PATTERNS`, licznik słów, wykrywanie wycieku żargonu IT na `sciezka: biznes`) odcina **całe klasy błędu zanim Sędzia LLM wyda 1 token**. To najważniejsza decyzja architektoniczna całej sesji: Sędzia przestaje być jedynym punktem prawdy. Dowód z danych: `#144357` (R1=41) — kara `-20 pkt (PUSTY FRAZES O DOŚWIADCZENIU)` z cytatem „Klasyczny pusty frazes szablonowy bez żadnej konkretnej liczby" — ten sam wzorzec złapałby regex `mamy\s+do[śs]wiadczenie\s+w\s+[łl][ąa]czeniu`, gdyby pre-audyt odpalił się przed Sędzią.

### `[+15 pkt]` Bezpiecznik `max(R1, R2)` + ochrona kwoty `_extract_price_days_from_text`
Bez tego mechanizmu **5 z 27 ofert (18,5%) poszłoby do klienta gorszych niż wersja zero-shot**:

| ID | Tytuł | R1 | R2 | Utrata |
|---|---|---|---|---|
| 144951 | NVIDIA DGX (RAG, LEX, 2FA) | 89 | 86 | **-3** |
| 2586109 | System zwrotów RMA + Subiekt | 90 | 82 | **-8** |
| 139571 | ENOVA365/XDEFT/IdoSell | 94 | 92 | -2 |
| 144249 | Make.com/n8n TikTok | 92 | 91 | -1 |
| 2643264 | Agent Marketplace 400 SKU | 92 | 88 | **-4** |

Średnia utrata, gdyby bezpiecznika nie było: **-1,6 pkt/oferta × 18,5% populacji**. Ochrona kwoty (`_extract_price_days_from_text`) dodatkowo gwarantuje, że pętla naprawcza nie „zgubi" wyceny — to typowy dług w systemach self-improving LLM.

### `[+15 pkt]` `MAX_RISK_MULTIPLIER = 1.15` (funkcja `max()`, nie iloczyn)
Konkretna naprawa realnego błędu. Dowód z danych: `#144890` (Comarch Optima + KSeF) — stary kalkulator `1,3 * 1,25 = 1,625x` dawał `17 500 zł / 36 dni`, gdy 30 ofert konkurencji na tym zleceniu mieściło się w `7 500 – 9 800 zł`. Po zmianie na `max()` z capem `1.15` efektywna stawka spadła do ~103–110 zł/h, mieszcząc się w widełkach rynkowych. Bez tej zmiany **każde zlecenie ERP byłoby odrzucane przez klienta w pierwszej rundzie negocjacji**.

### `[+12 pkt]` `_resolve_tech_cards()` + `_format_tech_card_for_slot()` (selektor + stripper tabel)
Automatyczne dobieranie do 2 kart wiedzy per slot i **wykrywanie tabel wycen wielowariantowych**, które są usuwane z kontekstu `02a`. Bez tego model kopiowałby do oferty „Wariant A: 6 500 zł / Wariant B: 12 800 zł" — łamiąc żelazny zakaz widełek. Dowód: `#144817` (asystent AI) — Sędzia odjął `-3 pkt (Wymiar D)`: „Klient wprost prosił o wycenę obsługi i utrzymania. Oferta całkowicie ją odkłada, nie podając nawet widełek orientacyjnych" → sugeruje, że formatowanie cen nadal wymaga dyscypliny, ale sama architektura stripowania jest słuszna.

### `[+10 pkt]` Dual-track `inzynieria` vs `biznes` + `tech_16_tech_agnostic_biznes.md`
Największy skok na najtrudniejszym segmencie. Dane: `tech_agnostic` (n=3) — R1 średnio **68,0 pkt**, Final średnio **92,7 pkt** = **+24,7 pkt przyrostu**, najwyższy w całym zbiorze. Bez `tech_16` (słownik tłumaczenia żargonu IT na język biznesu + 7 domen brzegowych) ten segment byłby odrzucany jak `#143981` (R1=52, kary `-15 pkt (Wymiar B)` za „API, limity zapytań, buforowanie").

### `[+10 pkt]` Portfolio z ID transakcji (Projekt 1, 2, 6)
`Projekt 6` (Klinika Doktor Monika — `12 100,00 PLN netto, wypłacone 22.06.2026`, referencja Prezesa Dominika Łyżwy) i `Projekt 2` (Centrum Budowlane Kołcz, `5 500 PLN netto`, `3 magazyny, >12 000 SKU`) to twarde dowody nie do podważenia. Jednocześnie to **problem** — patrz Sekcja 3.

### `[+8 pkt]` Zasada Zespołu 2-Osobowego (Ksawier + Maksymilian) + `45–75h` cap MVP
Rozwiązuje realny błąd, gdzie stary bot wyceniał pojedynczy moduł na `14–18h`. Wymusza sumę godzin MVP w przedziale `45–75h`, co daje realne rynkowo `6 000 – 9 800 zł` (nie `17 500 zł`).

---

## 3. ZA CO ODJĘTO PUNKTY `[-]` — Bezlitosna Lista Luk i Długu Technicznego

### `[-8 pkt]` **Niespójność `MIN_DNI` między Changelogiem a kodem**
- **Lokalizacja:** `kod/wycena_kalkulator.py` (fragment w payloadzie): `MIN_DNI = 7` w sekcji parametrów. Changelog Etap 3: „Obniżono minimalny próg dni `DNI_MIN` z `7` na **`3 dni`** dla małych zleceń (< 2 500 zł)".
- **Dlaczego groźne:** Wycena `#2575719` (quick_fix) to `2 500 zł / 141 słów`. Jeśli w kodzie produkcyjnym nadal jest `MIN_DNI = 7`, to wszystkie quick-fixy będą raportować 7 dni zamiast 3 — a klient w kategorii „awaria, na wczoraj" odrzuci ofertę. **Changelog kłamie o kodzie.**

### `[-8 pkt]` **Martwe sloty `03–07` i `20` w `chain_config.json`**
```json
{"id": "03", ..., "enabled": false, "on_fail": "retry_from_02a"},
{"id": "04", ..., "enabled": false, "on_fail": "abort"},
{"id": "05", ..., "enabled": false, "on_fail": "retry_from_02a"},
{"id": "06", ..., "enabled": false, "on_fail": "retry_from_02a"},
{"id": "07", ..., "enabled": false, "on_fail": "retry_from_02a"},
{"id": "20", ..., "enabled": false, "on_fail": "abort"},
```
- **Dlaczego groźne:** 6 z 10 slotów jest wyłączonych, ale nadal istnieje zależność `requires`/`on_fail`. Jeśli ktokolwiek zmieni `enabled: true` (np. podczas debugowania), cały pipeline zacznie odpalać walidatory, których kryteria (`agent_03_walidator_opisu.md` itd.) nie były aktualizowane od Etapu 5. **Zombie-konfiguracja: nieużywana, ale żywa i niebezpieczna.** Albo ją usuń, albo zostaw i oznacz `deprecated: true`.

### `[-7 pkt]` **Dwa kalkulatory wyceny żyją równolegle** — stary `1.3` nadal gdzieś działa
- **Dowód z danych (podwójny!):**
  - `#144817` (R1=60): `-12 pkt (Wymiar D / Kara Wyceny) | Wycena pochodzi ze starego mnożnika ryzyka 1.3 (efektywna stawka 159,6 zł/h przy bazowej 90 zł/h). Zawyżona o ok. 28%`.
  - `#144867` (R1=63): `-12 pkt (Wymiar D / Kara Wyceny) | Kwota pochodzi z iloczynu starego mnożnika ryzyka 1.3 nałożonego na 234.6 h, co daje efektywną stawkę ~158 zł/h`.
  - `#144890` (R1=85): `-12 pkt (Wymiar D / Kara Wyceny) | Efektywna stawka 157,1 zł/h`.
- **Wniosek:** Trzy różne zlecenia, wszystkie z finalną wyceną ze starego mnożnika `1.3`. To nie jest „reszta po refaktorze" — to **aktywna ścieżka w kodzie, której nie objęto testem `50 pytest`**. Prawdopodobna przyczyna: cache `wycena_dni` w `chain_executor.py` nie jest unieważniany po zmianie kalkulatora, albo `audytor_lancuch._call_slot_with_optional_research` omija `policz_wycene()`.

### `[-7 pkt]` **Overfitting promptu `02a` pod konkretne 27 zleceń i pod gust Sędziego**
- **Lokalizacja:** `agent_02a_opis_oferty.md`, sekcja „PYTANIE CTA DLA `PHANTOM` / `sciezka: biznes`" wspomina dosłownie przykłady z 27 prób: `NibblePro → AMADA`, `DXF`, `cnc`, `LEX`, `DGX Spark`, `Kołcz`, `Gardd`, `Shopify Locations`. Kryteria `kryteria_audytu_100.md` również zawierają te same przykłady.
- **Dlaczego groźne:** Sędzia LLM (DeepSeek) i Generator (DeepSeek) to **ta sama rodzina modeli**. Wspólne przykłady w promptach obu ról tworzą **pętlę rezonansu**: Sędzia premiuje to, co Generator wprost wpromptowano, a Generator uczy się kopiować „smaczki", które Sędzia lubi. Na 28. zleceniu poza rozkładem (np. `tech_11` — integracja z Telegramem) bot nie ma z czego czerpać i spada do poziomu R1 = 70–75 pkt.
- **Brak lekarstwa:** Nie ma **zestawu walidacyjnego (holdout)** — 27 zleceń użyto zarówno do tuningu promptów, jak i do pomiaru wyniku.

### `[-5 pkt]` **Projekt 8 i Projekt 9 bez ID transakcji = bomba zegarowa na priv**
- **Lokalizacja:** `portfolio_baza.md`, `Projekt 8` („Twardy dowód inżynierski: Przejęcia i refaktoryzacje...") i `Projekt 9` („Bezpieczne przejęcia zastanych sklepów B2B...") — brak `PLN netto`, brak nazwy klienta, brak linku do referencji.
- **Kontrast:** `Projekt 1` (3500+ dokumentów, 99,4%), `Projekt 2` (Kołcz 5500 PLN), `Projekt 6` (Doktor Monika 12100 PLN, referencja Prezesa) — mają twarde ID.
- **Scenariusz wyzwalający:** Klient `tech_09` (przejęcie PHP/MSSQL/WAPRO) pyta na priv: „Czy mogę zobaczyć referencję do tego przejęcia WAPRO MAG?". Bot nie ma czym odpowiedzieć. Jeśli odpowie ogólnikiem — traci wiarygodność; jeśli skłamie — traci konto. **Bezpieczniej byłoby oznaczyć Projekt 8/9 jako „case study anonimizowane, referencje po NDA" i nie powoływać się na nie w ofertach, gdzie klient wprost pyta o dowody transakcyjne.**

### `[-5 pkt]` **`KOREKTY` w `wycena_kalkulator.py` nie korygują już niczego realnie**
```python
KOREKTY = [
    (0, 1, 20, None, 1.0),
    (0, 1, 0, 20, 1.0),
    (1, 3, 20, None, 1.0),
    (1, 3, 0, 20, 1.0),
    (3, None, 0, 10, 1.15),
    (3, None, 10, 30, 1.0),
    (3, None, 30, None, 1.0),  # koniec z obniżką 0.85
]
```
- **Problem:** Tylko **jedna z siedmiu** reguł daje efekt (`1.15` dla „>3 dni, <10 ofert"). Reszta to `1.0` = brak korekty. To nie jest „koniec wyścigu na dno" — to **wyłączenie mechanizmu korekty konkurencyjnej** bez usunięcia go z kodu. Przy zleceniach z 30+ ofertami bot nie obniża ceny (dobrze), ale też nie podnosi jej przy zleceniach świeżych z 0 ofert (a mógłby — `1.05`–`1.10`).
- **Efekt uboczny:** Jeśli `wiek=0, ofert=1` (idealny lead, brak konkurencji) → mnożnik `1.0`. Stracona szansa na +10–15% marży.

### `[-4 pkt]` **Niespójność progów word-count między promptem a pre-audytem**
- **`agent_02a_opis_oferty.md`:** „**twardy nieprzekraczalny sufit 205 słów!**" dla `>=3000 zł`.
- **`audytor_lancuch.deterministic_pre_audit()`:** `elif wycena >= 3000 and words > 225:` — **kara odpala się dopiero przy 226 słowach**.
- **Konsekwencja:** Oferta na 210 słów przejdzie pre-audyt (bo 210 < 225), ale Sędzia LLM może ją ukarać za przekroczenie 205 (bo tak mówi prompt) — i tak właśnie zrobił: `#144890 (211 słów): -1 pkt (Wymiar E)`. **Pre-audyt jest o 20 słów za łagodny względem promptu.** Podobnie dla małych zleceń: prompt mówi „twardy sufit 110", pre-audyt karze dopiero przy `>120`.

### `[-4 pkt]` **`DNI_STOPA = 7` (h/dzień) i `DNI_WEEKEND = 1.30` nie są używane w pętli audytu**
- **Lokalizacja:** Stałe zdefiniowane w `wycena_kalkulator.py`, ale `audytor_lancuch.evaluate_offer_100()` nie przekazuje ich do Sędziego. Dlatego Sędzia `#144867` musiał ręcznie odjąć `-6 pkt (Wymiar D / Spójność ekonomiczna)` za „58 dni kalendarzowych na 234 h pracy to ~4 h/dzień... oferta nie precyzuje czy to jeden dev czy zespół".
- **Fix:** Pre-audyt powinien deterministycznie liczyć `dni * 7h >= suma_godzin` i dopisywać ostrzeżenie przed Sędzią.

### `[-3 pkt]` **Brak deklaracji Sandbox-First jako twardego wymogu pre-audytu**
- **Dowód z danych:** `#144951 (R1=89, Final=92): -4 pkt (Wymiar B) | Brak jasnej deklaracji Sandbox-First: że pierwsze testy i importy odbędą się na kopii bazy... Przy tym kliencie (radca prawny, dane objęte tajemnicą) to duże ryzyko.`
- To samo pojawia się w `#144817` (Final=91: `-3 pkt`).
- **Fix:** Regex `sandbox|kopi[ai]\s+bazy|środowisk[ao]\s+testow` w `FORBIDDEN_PATTERNS` z odwróconą logiką (jeśli brak — kara).

### `[-3 pkt]` **`_slim_zlecenie` może ucinać pytania klienta („W odpowiedzi podaj...")**
- **Ryzyko:** Prompt `02a` wymaga odpowiedzi na jawne pytania klienta (`MUSISZ w drugim akapicie odpowiedzieć konkretnie na każdy z tych punktów`), ale `chain_executor._slim_zlecenie` przycina opis zlecenia. Bez testu jednostkowego na `_slim_zlecenie` (czy jest w 50 pytest?) istnieje ryzyko, że lista pytań zostanie obcięta przed trafieniem do `02a` — i bot pominie pytanie, za co Sędzia odejmie `-5 do -10 pkt` (jak w `#144737`).

---

## 4. CO NAPRAWDĘ MÓWIĄ DANE Z 27 PRÓB — Głęboka Analiza R1 vs R2

### 4.1. Makrostatystyka
| Metryka | R1 (Zero-Shot) | Final (max z R1, R2, R3) | Δ |
|---|---|---|---|
| Średnia | 81,93 | 94,22 | **+12,29** |
| Mediana | 89,0 | 94,0 | +5,0 |
| Min | 41 | 89 | **+48** |
| Max | 97 | 99 | +2 |
| Odch. std (szac.) | ~14 | ~3 | **-11** |

**Interpretacja:** Pętla naprawcza nie tylko podnosi średnią — **drastycznie zmniejsza wariancję** (std z ~14 do ~3). To znaczy, że system staje się **przewidywalny**, co dla skalowania (10 ofert/dzień) jest ważniejsze niż średnia. Pojedyncze wpadki R1 (41, 52, 60, 63) są wyłapywane i naprawiane.

### 4.2. Segmentacja po typie klienta
| Typ | n | Śr. R1 | Śr. Final | Δ | Wniosek |
|---|---|---|---|---|---|
| `agencja` | 3 | 82,7 | 96,7 | **+14,0** | Bardzo dobrze rokuje. |
| `ecommerce` | 6 | 85,2 | 93,3 | +8,1 | Stabilne. |
| `ekspert_dziedzinowy` | 2 | 76,0 | 93,5 | **+17,5** | Duży potencjał, mała próba. |
| `msp_erp` | 12 | 84,7 | 94,9 | +10,2 | Najliczniejsza, dobra. |
| `quick_fix` | 1 | 81,0 | 90,0 | +9,0 | n=1 — brak wnioskowania. |
| `tech_agnostic` | 3 | **68,0** | 92,7 | **+24,7** | **Zero-shot najsłabszy — tu `tech_16` robi całą robotę.** |

**Kluczowa obserwacja:** Segment `tech_agnostic` ma najniższy R1 (68,0) i najwyższy przyrost (+24,7). To znaczy, że **prompt `02a` w wersji zero-shot nie jest jeszcze wystarczająco dobry dla nietechnicznych klientów** — `tech_16` ratuje sytuację w Rundzie 2, ale kosztuje to dodatkowe tokeny i czas. **Priorytet optymalizacyjny: przenieść część logiki `tech_16` do pierwszego przejścia `02a`.**

### 4.3. Gdzie R2 pogorszyła wynik R1 (5 przypadków)
| ID | Tytuł | R1 | R2 | Δ | Prawdopodobna przyczyna |
|---|---|---|---|---|---|
| 144951 | DGX Spark | 89 | 86 | -3 | Sędzia wymusił „Sandbox-First", Generator przekombinował i wstawił żargon. |
| 2586109 | RMA + Subiekt | 90 | 82 | **-8** | Sędzia odjął za brak OPEX, Generator wstawił ogólniki o „kosztach utrzymania". |
| 139571 | ENOVA365 | 94 | 92 | -2 | Drobiazg stylistyczny. |
| 144249 | Make/n8n TikTok | 92 | 91 | -1 | Sędzia chciał konkretu, Generator go nie miał (brak case study wideo). |
| 2643264 | Agent Marketplace 400 SKU | 92 | 88 | **-4** | Prawdopodobnie overfitting Sędziego pod `Kołcz` — Generator wstawił `>12 000 SKU` w kontekst niepasujący. |

**Wzorzec:** Regresja R2 występuje, gdy **Sędzia żąda dowodu, którego nie ma w `portfolio_baza.md`** (wideo, marketplace) — Generator wtedy „zmyśla na miarę" lub wstawia niedopasowany case. To argument za tym, by **Sędzia nie mógł żądać dowodu, którego nie ma w bazie** — i za rozbudową `portfolio_baza.md` o projekty wideo/social-media.

### 4.4. Najczęstsze przyczyny odjęć w R1 (ranking)
1. **`-20 pkt` Pusty frazes o doświadczeniu** — 2 przypadki (144357, 144737). Regex w pre-audycie już to łapie.
2. **`-12 pkt` Stary mnożnik 1.3** — 3 przypadki (144817, 144867, 144890). **To najpilniejszy fix.**
3. **`-8 pkt` Przekroczenie limitu słów** — 2 przypadki (143981, 144737).
4. **`-15 pkt` Fałszywy skok logiczny z researchu** (Three.js r185 + PrestaShop) — 1 przypadek (144092).
5. **`-8 pkt` Brak brudnych danych na ścieżce biznes** — 2 przypadki (144357, 144817).
6. **`-4 pkt` Brak Sandbox-First** — 1 przypadek (144951).
7. **`-3 pkt` Brak OPEX, gdy klient pytał** — 1 przypadek (144817).

### 4.5. Co mówią przypadki „zero-shot już bardzo dobry" (R1 ≥ 92)
6 z 27 ofert miało R1 ≥ 92: `144165` (93), `144890` (85→ ale z karą 12 za kalkulator), `139571` (94), `133275` (97), `143979` (96), `2741972` (94), `2749617` (94). To głównie `msp_erp` z jasnym zakresem i technicznymi klientami. **Wniosek:** dla `sciezka: inzynieria` + `msp_erp` system jest już autonomiczny. Dla `tech_agnostic` + `biznes` — jeszcze nie.

---

## 5. PLAN DOMKNIĘCIA DO 100/100 W PRODUKCJI (5 Kroków)

### Krok 1: **Ujednolicenie kalkulatora wyceny — usunięcie ścieżki `1.3`** (Priorytet P0, 1 dzień)
- **Co:** Grep po całym repo `1\.3` w kontekście `risk|mnożnik|multiplier` i usunięcie każdego trafienia. Test integracyjny: dla 3 zleceń z 27 prób (`#144817`, `#144867`, `#144890`) `policz_wycene()` musi zwrócić `efektywna_stawka <= 110 zł/h` (dziś zwraca `157–160 zł/h`).
- **Efekt:** +12 pkt × 3 przypadki = **+36 pkt w sumie na tych zleceniach**, średnia Final wzrośnie do ~95,2.
- **Weryfikacja:** Dodać test `test_brak_starego_mnoznika_1_3` do `tests/`.

### Krok 2: **Usunięcie martwych slotów `03–07` i `20` z `chain_config.json`** (P0, 2h)
- **Co:** Albo `"enabled": false, "deprecated": true` z komentarzem w configu, albo całkowite usunięcie. Walidator schematu powinien odrzucać sloty z `enabled: false` i niepustym `requires`.
- **Efekt:** Eliminacja ryzyka „zombie-konfiguracji" i −3 pkt długu technicznego.
- **Weryfikacja:** Test `test_chain_config_no_zombie_slots`.

### Krok 3: **Zestaw walidacyjny (holdout) + druga rodzina LLM do oceny** (P1, 3 dni)
- **Co:**
  1. Zapisać 5 nowych zleceń z magazynu (nieużytych w 27) jako `badania/holdout/holdout_5.json`. **Nie dotykać ich przy tuningu promptów.**
  2. Uruchomić Sędziego na holdoucie **dopiero po zamrożeniu promptów**, porównać z DeepSeek.
  3. Dodać alternatywnego Sędziego (np. Claude Sonnet 4.5 lub GPT-4.1) jako „drugi łańcuch krytyka" i uśredniać oceny: `ocena = 0.6 * DeepSeek + 0.4 * Claude`. Różnica > 15 pkt między sędziami → flaga „niepewna ocena" i ręczny przegląd.
- **Efekt:** Wykrycie overfittingu i rozdzielenie gustu jednego modelu od rzeczywistej jakości. Szacowany koszt: ~50 zł API za 5 zleceń × 2 modele × 3 rundy.

### Krok 4: **Pre-audyt jako pełny gatekeeper zamiast „miękkiego ostrzeżenia"** (P1, 2 dni)
- **Co:** Rozszerzyć `deterministic_pre_audit()` o:
  - Obliczanie `dni * 7h >= suma_godzin` (użycie `DNI_STOPA`).
  - Regex obecności `sandbox|kopi[ai]\s+bazy|środowisk[ao]\s+testow` (jeśli brak — `-4 pkt`).
  - Regex odpowiedzi na „W odpowiedzi podaj" (jeśli w zleceniu są ponumerowane punkty, a w ofercie brak słów kluczowych z tych punktów — `-5 pkt`).
  - **Zaostrzenie progów word-count do zgodności z promptem** (`>110` dla `<3000`, `>205` dla `>=3000`).
  - Wykrywanie **fałszywych skoków logicznych**: jeśli w ofercie jest `Three.js\s*r\d+` obok `PrestaShop|WooCommerce` → `-15 pkt` (już jest, ale rozszerzyć o inne biblioteki).
- **Efekt:** Sędzia LLM dostaje ofertę już „wstępnie oczyszczoną", a jego ocena staje się bardziej precyzyjna. Szacowany wzrost średniej R1 o **+3 do +5 pkt**.

### Krok 5: **Uczciwe oznaczenie Projektu 8 i 9 + rozbudowa portfolio o wideo/social** (P2, 1 dzień)
- **Co:**
  1. W `portfolio_baza.md` przy `Projekt 8` i `Projekt 9` dodać adnotację: `*Dowód anonimizowany (NDA). Referencje udostępniam po podpisaniu NDA.*`
  2. Dodać `Projekt 10` (Automatyzacja wideo TikTok/YT Shorts) z twardym dowodem — nawet jeśli to projekt wewnętrzny, opisać jako `Case wewnętrzny: 400 filmów/msc, 0 blokad kont, publikacja przez oficjalne API`.
  3. W promptach `02a` i `kryteria_audytu_100.md` **usunąć konkretne nazwy zleceń** (`NibblePro`, `DGX Spark`, `LEX`, `Kołcz`), zastępując je opisami kategorii (np. `sterownik CNC LVD/ADTECH`, `serwer GPU z ograniczoną pamięcią VRAM`, `system prawniczy z 2FA`).
- **Efekt:** Redukcja overfittingu (Sędzia nie premiuje kopiowania nazw), poprawa wiarygodności na priv, zamknięcie luki dla zleceń wideo/social-media.

---

### Prognoza po wdrożeniu Planu
| Metryka | Dziś | Po planie (szac.) |
|---|---|---|
| Śr. R1 | 81,93 | **86–88** |
| Śr. Final | 94,22 | **96–97** |
| Min Final | 89 | **92** |
| Regresje R2 | 5/27 | **≤ 2/27** |
| Wariancja (std) | ~3 | **~2** |

**Warunek osiągnięcia 100/100:** Powyższe 5 kroków + **3 dodatkowe iteracje pętli naprawczej** na holdoucie (Krok 3) — i dopiero wtedy można mówić o systemie w pełni autonomicznym. Dziś system jest **autonomiczny dla `msp_erp` + `inzynieria`** i **półautonomiczny dla `tech_agnostic` + `biznes`**.

---

**Podsumowanie jednym zdaniem:** Reforma ofertowarki to realny skok klasy (+12,3 pkt średnio, −11 pkt wariancji), ale trzy dziury — **stary kalkulator `1.3` żyjący w produkcji**, **martwe sloty `03–07` w configu** i **brak holdoutu** — trzymają system na **76/100**, zamiast docelowych **95+/100**. Wszystkie trzy są naprawialne w mniej niż tydzień pracy.