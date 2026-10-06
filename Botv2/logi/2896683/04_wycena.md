=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
## Wycena

**Kwota:** 9 000 – 12 000 zł netto (100–135 h × 90 zł/h)
**Czas:** 20–25 dni roboczych (4–6 tygodni kalendarzowo, praca solo)
**Uzasadnienie:** 12 szablonów w custom Liquid/OS 2.0 z realnie różnymi układami desktop/mobile to ~70% pracy; reszta to konfiguracja PL (płatności, InPost, Fakturownia), analityka z Consent Mode v2 i setup hostingu wideo. Widełki zawężę po NDA — zobaczę prototyp i pliki wideo.

---

## Podział na etapy

| Etap | Zakres | h | Kwota |
|---|---|---|---|
| 1. Motyw | 12 szablonów Liquid/OS 2.0, sekcje warunkowe, slidery, animacje | 70–85 | 6 300–7 650 zł |
| 2. Konfiguracja | płatności, InPost, wysyłki, zwroty, Fakturownia, PL | 10–14 | 900–1 260 zł |
| 3. Analityka | GA4, Google Ads, Consent Mode v2, CMP, testy konwersji | 10–14 | 900–1 260 zł |
| 4. Wideo + PageSpeed | hosting zewn., lazy load, poster, optymalizacja mobile | 8–12 | 720–1 080 zł |
| 5. QA + przekazanie | testy, poprawki, dokumentacja | 8–10 | 720–900 zł |

**Harmonogram:** etap 1 – 3 tyg., etapy 2–4 – 1,5 tyg., QA – 3–4 dni. Płatność etapowa 30/40/30.

---

## Odpowiedzi na pytania

**1. Desktop/mobile o różnym układzie.**
Jeden motyw Liquid/OS 2.0 (nie dwa). Tam, gdzie układy faktycznie się różnią, renderuję dwa bloki DOM i przełączam przez CSS media queries — nie skalowanie, nie user-agent (psuje cache i SEO). Sekcje OS 2.0 z ustawieniami w `settings_schema.json`, żeby klient mógł edytować treści bez kodu.

**2. Duże wideo w tle bez psucia PageSpeed.**
Pliki poza Shopify — Bunny Stream (najtaniej) lub Cloudflare Stream (złoty środek). W Liquid: `<video preload="none" poster playsinline muted loop>` + lazy load przez IntersectionObserver. Na mobile **nie** autoplay wideo w tle — tylko poster + przycisk play (inaczej PageSpeed zabity i transfer użytkownika). Dla desktop krótki webm/mp4 do ~2–3 MB. Weryfikacja PageSpeed Insights przed i po.

**3. Consent Mode v2 + konwersja w Google Ads.**
CMP Google Certified (Pandectes ~$9–25/mies. lub Cookiebot ~€7–30/mies.) → integracja ze Shopify Customer Privacy API → 4 sygnały (`ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`). Weryfikacja: GA4 DebugView + Google Ads → Konwersje → status „Recording conversions" + testowy zakup ze zgodami i bez.

---

## Płatne aplikacje (koszt mies.)

| App | Koszt |
|---|---|
| Pandectes lub Cookiebot (CMP) | ~$9–25 / ~€7–30 |
| InPost Paczkomaty (Progus) | $0 do 5 zam., potem $9.99–49.99 |
| Fakturownia | **do potwierdzenia w App Store** |
| Płatności (Przelewy24/Tpay/PayU) | **do potwierdzenia** — Shopify Payments obsługuje BLIK/P24 natywnie bez opłat app |
| Bunny Stream / Cloudflare Stream | ~$1.50–15 / ~$5.50–55 |

---

## Linki do realizacji

[link 1] [link 2] [link 3] — wkleję po NDA, razem z opisem mojej pracy w każdym (custom theme, OS 2.0, sekcje Liquid).

---

## Do doprecyzowania przed startem

1. **Pliki wideo — są gotowe, czy wchodzi przygotowanie/kompresja/poster?** Realna pozycja w etapie 1, zmienia wycenę.
2. **Kiedy podpisujemy NDA?** Bez prototypu wycena jest widełkowa; po NDA dostroję liczby do realnych różnic desktop/mobile.
3. **Plan Shopify:** zakładam Grow (dla tego zakresu wystarczy). Jeśli Plus — dostroję warstwę checkoutu.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: przy 90 zł/h sama stawka jest sztywna, więc jedyne co mogłem zawyżyć/zaniżyć to godziny — i uważam, że etap 1 (70–85 h na 12 szablonów Liquid z animacjami i warunkowym desktop/mobile) jest raczej optymistyczny niż realny. Translacja gotowego HTML „1:1 wizualnie" na OS 2.0 z sekcjami edytowalnymi przez klienta to zwykle 1,5–2× czas, który się wydaje na papierze — szczególnie animacje i slidery, które w Liquid często trzeba przepisać od zera. Etap 3 (analityka, 10–14 h) też jest na granicy: Consent Mode v2 + CMP + weryfikacja konwersji w Ads z testami „ze zgodą / bez zgody" to realnie 15–20 h, jeśli chce się to zrobić porządnie, a nie tylko „kliknąć appkę". Skorygowałbym górną widełkę w etapie 1 na ~95 h i etap 3 na ~18 h, co daje ~10,5–13,5 k zł netto — niczego nie zgadywałem, ale przy NDA może się okazać, że prototyp ma cięższe animacje niż zakładam i wtedy trzeba to przeliczyć.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna:** **12 000–17 000 zł** (umowa o dzieło, szczegóły rozliczenia na Useme). Po NDA i zobaczeniu prototypu oraz materiałów wideo podam stałą kwotę.

**Czas:** **20–30 dni roboczych** (4–6 tygodni) od NDA i kompletu materiałów.

**Uzasadnienie:** 12 szablonów z realnie różnym mobile/desktop, Liquid/OS 2.0, wideo, slidery, animacje + konfiguracja PL + GA4/Google Ads/Consent Mode v2 to ok. **130–190 h × 90 zł/h**. To nie kopiowanie HTML 1:1, tylko wierne odwzorowanie wizualno-funkcjonalne w Liquid.

**Czego brakuje do stałej wyceny:**
- czy pliki wideo są gotowe pod web, czy wchodzi przygotowanie/kompresja,
- kiedy podpisujemy NDA i dostaję prototyp,
- plan Shopify (domyślnie zakładam Grow),
- nowy sklep czy migracja z istniejącego.

**Koszty zewnętrzne po stronie klienta (mies.):** Shopify Grow ok. 350–430 zł, CMP Google Certified ok. 40–120 zł, InPost ok. 40–90 zł, hosting wideo Bunny/Cloudflare Stream ok. 10–100 zł, Fakturownia – do potwierdzenia w App Store.

**Technicznie w skrócie:** jeden motyw + sekcje warunkowe dla różnic mobile/desktop; wideo na zewnętrznym hostingu z lazy load i posterem; Consent Mode v2 przez CMP + Shopify Customer Privacy API i weryfikacja konwersji w GA4 DebugView oraz Google Ads.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Wycena jest obroniona, ale dolna granica 130 h jest optymistyczna — 12 szablonów z realnie różnym mobile/desktop to nie 10 h na szablon, tylko bliżej 11–13 h, a sama konfiguracja wideo (hosting zewnętrzny + lazy load w Liquid) i Consent Mode v2 z weryfikacją konwersji to kolejne 15–25 h, których nie da się zmieścić w 130 h bez cięcia jakości. Uczciwie: zawężam widełki do **14 000–18 000 zł** (155–200 h × 90 zł/h) i zostawiam 20–30 dni roboczych, bo przy 200 h to nadal realne. Nie dodałem nic na siłę — lista appek z kosztem miesięcznym to wymóg klienta, a Bunny/Cloudflare/CMP wynikają wprost z jego pytania o PageSpeed i Consent Mode v2. Jedno, czego nie zgadłem i nie ukrywam: nie znam planu Shopify ani liczby SKU, więc po NDA kwota może jeszcze drgnąć — dlatego etapowość i „do potwierdzenia" przy Fakturowni/przelewach zostają.

=== DeepSeek-C — RUNDA 1 ===
**Wycena wstępna:** 11 000 – 16 000 zł netto (przy 90 zł/h).

**Czas:** 20–30 dni roboczych.

**Uzasadnienie:** Zakres obejmuje przekład 12 szablonów HTML na Liquid/OS 2.0 z osobnymi układami desktop/mobile, pełną konfigurację PL (płatności, InPost, faktury, zwroty), analitykę z Consent Mode v2 oraz optymalizację wideo pod PageSpeed. Wycena jest widełkowa, bo bez dostępu do prototypu (NDA) nie znam realnej złożoności animacji i różnic mobile vs desktop. Po NDA i potwierdzeniu gotowości plików wideo dostroję kwotę.

**Brakuje mi:**
1. Czy pliki wideo są gotowe, czy wchodzi przygotowanie/kompresja pod web?
2. Kiedy można podpisać NDA i zobaczyć prototyp? (bez tego wycena jest tylko orientacyjna)
3. Plan Shopify – zakładam Grow, ale przy custom checkoutcie może być wymagany Plus.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: wycenę zbudowałem z zakresu wprost z ogłoszenia, nie z domysłów — 12 szablonów Liquid z osobnymi układami mobile/desktop to realnie 90–120h, konfiguracja PL ~15–25h, analityka z Consent Mode v2 ~10–15h, wideo/PageSpeed ~10–20h, co daje 125–180h i kwotę 11–16k przy 90 zł/h. Research potwierdził, że Shopify Files (1 GB, 10 min, brak ABR) nie nadaje się na wideo tła, więc hosting zewnętrzny (Bunny/Cloudflare) to nie opcja, a konieczność — to nie zmienia stawki, ale utwierdza, że wycena nie jest zawyżona. Jedyne, co bym skorygował, to **dolna granica: 11k jest ryzykowna** — przy 122h na styk i realnym ryzyku, że animacje z Claude są cięższe niż się wydaje, bezpieczniej dać **13–18k netto**, a po NDA i zobaczeniu prototypu domknąć liczbę. Nie dopisałem nic na siłę — plan Plus, migracja, liczba SKU i budżet to świadome pominięcia (TYP 2 lub poza zakresem), a trzy pytania klienta potraktowałem jako test kompetencji, nie jako miny do sprzedania.

=== DeepSeek-D — RUNDA 1 ===
**Wycena:** 12 000 – 17 000 zł (netto, umowa o dzieło)
**Czas:** 20–28 dni roboczych

**Uzasadnienie:** Zakres to głównie custom motyw Liquid/OS 2.0 z ~12 szablonami, warunkowymi układami desktop/mobile i wideo w tle, plus konfiguracja PL (InPost, płatności, faktury) i analityka z Consent Mode v2. Przy 90 zł/h i szacunku 130–190 h wychodzi powyższy przedział. Po NDA i zobaczeniu prototypu podam dokładną wycenę etapową.

**Czego brakuje:**
1. Czy pliki wideo są gotowe, czy wchodzi przygotowanie/kompresja pod web?
2. Kiedy podpisujemy NDA, żeby zobaczyć prototyp i dostroić wycenę?
3. Plan Shopify (Basic/Grow/Plus) i czy budowa od zera, czy migracja?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena jest uczciwa — 130–190 h przy 90 zł/h na 12 szablonów Liquid/OS 2.0, wideo w tle, konfigurację PL i analitykę to realny przedział, a widełki (a nie sztywna kwota) są właściwe, bo bez NDA nie widzę prototypu ani nie wiem, czy to budowa od zera czy migracja. Nie dodałem nic „na siłę": Bunny/Cloudflare i Google Certified CMP to rekomendacje wynikające wprost z pytań klienta o wideo i Consent Mode v2, a nie moje widzimisię — mogę je podać jako opcje, nie jako przymus. Jedyne, co bym dopisał, to że po NDA zawężam widełki, a jeśli okaże się, że to migracja z przekierowaniami — górna granica rośnie (import + SEO). Kwoty nie zmieniam, ale w ofercie wyraźnie zaznaczę, że to widełki wstępne, a wycena etapowa wiążąca będzie po NDA i po odpowiedzi o wideo.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 13000,
  "kwota_gorna": 18000,
  "definitywna": false,
  "od_czego_zaleza": [
    "Podpisanie NDA i dostęp do prototypu HTML",
    "Gotowość plików wideo lub konieczność przygotowania/kompresji pod web",
    "Plan Shopify (Grow vs Plus) i zakres customizacji checkoutu",
    "Nowy sklep vs migracja z istniejącego",
    "Realna złożoność animacji, sliderów i różnic mobile/desktop w 12 szablonach"
  ],
  "dni_od": 20,
  "dni_do": 30,
  "uzasadnienie": "Modele zgodnie wskazują, że dominuje przekład 12 szablonów na Liquid/OS 2.0 z warunkowymi układami mobile/desktop, konfiguracja PL, analityka Consent Mode v2 i zewnętrzny hosting wideo. Rozbieżność dotyczyła głównie liczby godzin: A był najniższy i po autokorekcie dawał ok. 10,5–13,5 tys. zł, natomiast B, C i D oscylowały wokół 12–18 tys. zł, a po autokorektach B i C domykały się na 13–18 tys. zł. Wybieram 13 000–18 000 zł netto jako medianę skorygowanych głosów, z terminem 20–30 dni roboczych. To nadal widełki, bo bez NDA i prototypu nie da się ustalić stałej kwoty; po NDA i potwierdzeniu wideo oraz planu Shopify zakres się domknie."
}

=== FINALNA WYCENA ===
13000-18000 zl netto | 20-30 dni | WIDELKI
Od czego zalezy: Podpisanie NDA i dostęp do prototypu HTML, Gotowość plików wideo lub konieczność przygotowania/kompresji pod web, Plan Shopify (Grow vs Plus) i zakres customizacji checkoutu, Nowy sklep vs migracja z istniejącego, Realna złożoność animacji, sliderów i różnic mobile/desktop w 12 szablonach
Uzasadnienie rozjemcy: Modele zgodnie wskazują, że dominuje przekład 12 szablonów na Liquid/OS 2.0 z warunkowymi układami mobile/desktop, konfiguracja PL, analityka Consent Mode v2 i zewnętrzny hosting wideo. Rozbieżność dotyczyła głównie liczby godzin: A był najniższy i po autokorekcie dawał ok. 10,5–13,5 tys. zł, natomiast B, C i D oscylowały wokół 12–18 tys. zł, a po autokorektach B i C domykały się na 13–18 tys. zł. Wybieram 13 000–18 000 zł netto jako medianę skorygowanych głosów, z terminem 20–30 dni roboczych. To nadal widełki, bo bez NDA i prototypu nie da się ustalić stałej kwoty; po NDA i potwierdzeniu wideo oraz planu Shopify zakres się domknie.
