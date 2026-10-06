=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
## Wycena

**Kwota wdrożenia:** 14 500 – 21 500 zł netto (160–240 h × 90 zł/h)
**Czas:** 25–35 dni roboczych (5–7 tygodni) przy równoległym dostępie do kont i API
**Utrzymanie:** koszty tokenów LLM ~30–80 zł/mies. przy 400 SKU + opcjonalna opieka 400–600 zł/mies.

**Uzasadnienie:** To nie jest jeden skrypt, a trzy współzależne moduły (pricing, AI editor, inventory sync) na dwóch marketplace'ach z różnymi API, autoryzacją i limitami — dlatego widełki są szerokie i zależą głównie od tego, czy dostępy są gotowe. Rekomenduję hybrydę: n8n/Make do orkiestracji + Python do logiki cenowej i synchronizacji, z BaseLinkerem jako warstwą pośrednią (omija ograniczenia bezpośredniego API Allegro i przyspiesza start). Taniej nie zejdę bez cięcia zakresu — np. rezygnacji z auto-pricingu na start albo ograniczenia do jednego marketplace'u.

## Czego brakuje w zleceniu

1. **Czy macie zatwierdzoną aplikację Amazon SP-API i dostęp do konta sprzedawcy?** Bez tego moduły Amazon startują od etapu rejestracji (doliczam do wyceny).
2. **Czy marka jest w Amazon Brand Registry?** Bez tego **A+ Content nie zadziała** — trzeba go zastąpić zwykłą optymalizacją opisów, co zmienia zakres AI Editora.
3. **Które rynki Amazon (PL, DE, inne) i zakres monitoringu cen** — liczba wywołań API i koszt utrzymania rosną z każdym rynkiem.

Dodatkowo: **reguły marżowe** (na start proponuję tryb sugestii z ręcznym zatwierdzaniem, automatyzacja po ich ustaleniu) oraz **częstotliwość synchronizacji** stanów.

Chcesz, żebym rozpisał propozycję architektury w punktach przed podpisaniem umowy? To 1–2 h roboty — mogę wliczyć w wdrożenie.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: kwota jest zasadna, ale **dolna granica 14 500 zł jest ryzykowna** — przy 160 h zakładasz, że BaseLinker załatwia większość integracji i dostępy są gotowe, a to jeszcze niepotwierdzone. Gdyby SP-API i weryfikacja aplikacji Allegro wymagały rejestracji od zera, realnie robi się 200–240 h, czyli **18 000–21 500 zł** i to jest uczciwsze widełki na start. Nie zawyżyłem — 90 zł/h × 240 h to 21 600 zł, czyli niecałe 5,5 tys. euro za trzy współzależne moduły na dwóch marketplace'ach z LLM i bezpiecznikami; taniej tylko przez cięcie zakresu. Czego **nie** doliczyłem: utrzymania po wdrożeniu (monitoring, poprawki API, rotacja kluczy) i zgodności z AI Act/RODO przy przetwarzaniu danych produktowych — to osobna pozycja, nie część wdrożenia. Koryguję rekomendację: **16 000–22 000 zł netto**, z zastrzeżeniem, że dolna granica obowiązuje wyłącznie przy gotowych dostępach.

=== DeepSeek-B — RUNDA 1 ===
**Wycena: 11 000 – 15 000 zł netto** (120–160 h × 90 zł), **czas: 15–20 dni roboczych** (3–4 tygodnie).

**Uzasadnienie:** Zakres obejmuje 3 moduły z integracjami do dwóch marketplace'ów (Allegro + Amazon SP-API), warstwę LLM do 400 SKU oraz synchronizację stanów — to nie jest projekt na tydzień. Rekomenduję hybrydę: n8n/Make do orkiestracji + Python do logiki cenowej i batchowania LLM, z BaseLinkerem jako warstwą pośrednią dla Allegro (omija weryfikację aplikacji do cen konkurencji). Koszt tokenów przy 400 SKU to rząd kilku–kilkunastu USD/mies. przy batchowaniu i cache; utrzymanie 300–500 zł/mies.

**Czego brakuje w zleceniu:**
1. Czy macie **zatwierdzoną aplikację SP-API** i dostęp do konta sprzedawcy Amazon?
2. Czy marka jest w **Amazon Brand Registry**? Bez tego A+ Content nie zadziała — trzeba zastąpić zwykłą optymalizacją opisów.
3. Które **rynki Amazon** (PL/DE/inne) i czy monitorowanie cen ma być per ASIN/EAN? To wpływa na liczbę wywołań API i koszt utrzymania.
4. **Reguły marżowe** dla auto-pricingu — proponuję start w trybie sugestii z ręcznym zatwierdzaniem, automatyzacja po ich ustaleniu.

Widełki nie zawierają kosztu rejestracji/weryfikacji aplikacji Allegro i Amazon — jeśli ich nie macie, doliczam osobno.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: kwota jest realna, ale na dolnej granicy ryzyka — 120 h przy trzech integracjach (Allegro + SP-API + BaseLinker) i pipeline LLM to scenariusz optymistyczny, gdzie klient ma gotowe dostępy, zatwierdzoną aplikację i nie zmienia zakresu w trakcie. Górną widełkę zawyżyłbym do **17 000 zł** (do ~190 h), bo samo wdrożenie SP-API (OAuth, SigV4, sandbox, testy na żywym koncie) realnie zjada 30–50 h, a do tego dochodzi walidacja promptów i bezpieczniki auto-pricingu. Nie dopisałem na siłę nic — brakuje mi natomiast **osobnej pozycji kosztów stałych** (VPS/hosting n8n, plan BaseLinker, monitoring/logi) poza samymi tokenami, oraz **okresu gwarancji i zakresu poprawek po odbiorze** — to typowe miejsca, gdzie przy 400 SKU robi się niespodzianka. Koszt tokenów „kilka–kilkanaście USD/mies” jest OK dla batchowej optymalizacji, ale przy ciągłym re-generowaniu opisów i monitoringu mógłby dojść do 30–60 USD/mies. Rekomendacja: zostawić 11–15 k jako widełki startowe, ale w ofercie jasno napisać, że **11 k to wariant minimum** (BaseLinker, brak weryfikacji własnej aplikacji Allegro, ręczne zatwierdzanie zmian cen), a **17 k to wariant z bezpośrednimi API i pełną automatyzacją** — i osobno wycenić utrzymanie 300–500 zł/mies + tokeny.

=== DeepSeek-C — RUNDA 1 ===
**Wycena wstępna (MVP):**
- **Wdrożenie:** **12 000–18 000 zł** (135–200 h × 90 zł/h, umowa o dzieło).
- **Utrzymanie:** **800–1 500 zł/mies.** + tokeny LLM **50–300 zł/mies.**  
  Jednorazowa optymalizacja 400 SKU to zwykle **30–100 zł** w tokenach.
- **Czas:** **20–30 dni roboczych**; kalendarzowo **6–10 tygodni** — głównie przez weryfikacje API.

**Uzasadnienie:** To nie jest prosty skrypt: 3 moduły, integracje Allegro/Amazon SP-API/BaseLinker, 400 SKU, bezpieczniki auto-pricing, testy i dokumentacja. Rekomenduję hybrydę **n8n/Make + Python**, a BaseLinker jako warstwę pośrednią, bo bezpośrednie API Allegro do cen konkurencji wymaga zatwierdzonej aplikacji. A+ Content zadziała tylko przy **Amazon Brand Registry**.

**Czego brakuje:** dostępu do zatwierdzonej aplikacji SP-API i konta Amazon, informacji o Brand Registry, rynków Amazon, reguł marżowych, częstotliwości synchronizacji oraz tego, czy ceny mają być zmieniane automatycznie, czy tylko sugerowane.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: sama wycena wdrożenia (12–18k) jest obronna, ale dolna granica 135 h jest napięta — przy dwóch marketplace'ach, LLM i testach realnie celowałbym w **150–220 h, czyli 13,5–20k**, zwłaszcza że weryfikacja aplikacji Allegro i SP-API potrafi ciągnąć się tygodniami i generować dodatkowe iteracje.

Koszt tokenów 30–100 zł za 400 SKU jest OK (GPT-4o: ~3k input + 1k output × 400 ≈ 28 zł, kilka iteracji promptów i wychodzi górna widełka) — tu nie zgadywałem.

Utrzymanie 800–1500 zł/mies. to **tylko moje godziny** i nie doliczyłem tam subskrypcji po stronie klienta: BaseLinker, n8n/Make, hosting/VPS, budżet na LLM API — realnie **+300–800 zł/mies.** kosztów narzędziowych, które klient płaci osobno.

Czego nie dopisałem na siłę: BaseLinker i hybryda n8n+Python to moja rekomendacja, nie jedyna droga — jeśli klient ma już stack, może być inaczej. Mina z API Allegro i A+ to twardy research, nie zgadywanie.

Korekta: **wdrożenie 13,5–20k**, utrzymanie **800–1500 zł/mies. (moje godziny) + ~300–800 zł/mies. koszty narzędzi po stronie klienta**.

=== DeepSeek-D — RUNDA 1 ===
Wycena wstępna (przy dostępie do API i kont):

- **Wdrożenie:** 18 000–24 000 zł (200–260 h × 90 zł/h).
- **MVP:** 12 000–16 000 zł — monitoring + sugestie cen + podstawowy AI Editor + sync.
- **Czas:** 8–12 tygodni od przekazania dostępów. Bez weryfikacji API Allegro/SP-API może wydłużyć się o 2–4 tygodnie.
- **Utrzymanie:** 700–1200 zł/mies. + tokeny LLM ok. 50–200 zł/mies.

Uzasadnienie: Trzy moduły, dwie integracje marketplace, LLM, 400 SKU i bezpieczniki auto-pricing to realnie 200+ godzin. Rekomenduję hybrydę: n8n/Make do orkiestracji + Python do logiki cen i sync, z BaseLinkerem jako warstwą pośrednią dla Allegro. Auto-pricing startuje w trybie sugestii z ręcznym zatwierdzaniem.

Braki, które zmieniają wycenę:
- Czy marka jest w **Amazon Brand Registry**? Bez tego A+ Content nie zadziała.
- Czy jest zatwierdzona aplikacja **SP-API** i dostępy do Allegro/Amazon/BaseLinker?
- Które rynki Amazon, jakie reguły marżowe, częstotliwość sync i czy ceny mają być zmieniane automatycznie?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena była oparta na realnym nakładzie: 3 moduły, 2 marketplace’y, LLM, 400 SKU i bezpieczniki auto-pricingu to ok. 200–260 h, więc 18–24 tys. zł przy 90 zł/h jest obronne. Nie dopisałem na siłę A+ Content ani weryfikacji API Allegro – oba wynikają wprost z opisu i researchu, a BaseLinker to sensowna alternatywa, nie wymysł. Jeśli brakuje dostępów SP-API i Brand Registry, dół widełek jest zbyt optymistyczny: podniósłbym wdrożenie do 20–28 tys. zł, utrzymanie do 900–1500 zł/mies., a tokeny do 100–400 zł/mies. przy częstszej optymalizacji. MVP 12–16 tys. zł nadal broni się tylko dla zakresu okrojonego do Allegro/BaseLinkera i AI Editora bez A+.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 16000,
  "kwota_gorna": 24000,
  "definitywna": false,
  "od_czego_zaleza": [
    "Gotowość zatwierdzonej aplikacji Amazon SP-API oraz dostępów do kont Allegro/Amazon/BaseLinker",
    "Czy marka jest w Amazon Brand Registry, bo bez tego A+ Content wypada z zakresu AI Editora",
    "Liczba rynków Amazon i zakres monitoringu cen konkurencji per ASIN/EAN",
    "Tryb auto-pricingu: ręczne zatwierdzanie sugestii czy pełna automatyzacja po regułach marżowych",
    "Zakres utrzymania oraz koszty narzędzi i tokenów LLM po stronie klienta"
  ],
  "dni_od": 25,
  "dni_do": 45,
  "uzasadnienie": "Modele zgodnie rekomendują architekturę hybrydową n8n/Make + Python oraz BaseLinker jako warstwę pośrednią, a także wskazują te same miny: A+ Content wymaga Brand Registry, a bezpośrednie API Allegro do cen konkurencji wymaga weryfikacji aplikacji. Rozbieżność dotyczy głównie nakładu: niższe wyceny 11–15 tys. zł zakładają gotowe dostępy i wariant minimum, a wyższe 20–28 tys. zł pełną automatyzację i brak gotowych integracji. Po korektach autokrytycznych najbardziej obronne są widełki 16–24 tys. zł netto: dół przy gotowych dostępach i BaseLinkerze, góra przy bezpośrednich API, pełnym auto-pricingu i szerszym utrzymaniu. Wycena nie jest definitywna, bo brakuje potwierdzenia SP-API, Brand Registry, rynków Amazon i reguł marżowych."
}

=== FINALNA WYCENA ===
16000-24000 zl netto | 25-45 dni | WIDELKI
Od czego zalezy: Gotowość zatwierdzonej aplikacji Amazon SP-API oraz dostępów do kont Allegro/Amazon/BaseLinker, Czy marka jest w Amazon Brand Registry, bo bez tego A+ Content wypada z zakresu AI Editora, Liczba rynków Amazon i zakres monitoringu cen konkurencji per ASIN/EAN, Tryb auto-pricingu: ręczne zatwierdzanie sugestii czy pełna automatyzacja po regułach marżowych, Zakres utrzymania oraz koszty narzędzi i tokenów LLM po stronie klienta
Uzasadnienie rozjemcy: Modele zgodnie rekomendują architekturę hybrydową n8n/Make + Python oraz BaseLinker jako warstwę pośrednią, a także wskazują te same miny: A+ Content wymaga Brand Registry, a bezpośrednie API Allegro do cen konkurencji wymaga weryfikacji aplikacji. Rozbieżność dotyczy głównie nakładu: niższe wyceny 11–15 tys. zł zakładają gotowe dostępy i wariant minimum, a wyższe 20–28 tys. zł pełną automatyzację i brak gotowych integracji. Po korektach autokrytycznych najbardziej obronne są widełki 16–24 tys. zł netto: dół przy gotowych dostępach i BaseLinkerze, góra przy bezpośrednich API, pełnym auto-pricingu i szerszym utrzymaniu. Wycena nie jest definitywna, bo brakuje potwierdzenia SP-API, Brand Registry, rynków Amazon i reguł marżowych.
