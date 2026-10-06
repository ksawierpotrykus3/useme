=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena: 42 000 – 55 000 zł netto** (przy stawce 90 zł/h → ~470–610 h)

**Czas: 10–14 tygodni** (solo, part-time, z uwzględnieniem dopracowania UX i testów płatności)

**Uzasadnienie:**
Zakres MVP jest realnie duży: panel organizatora, zakup z płatnością online, generowanie PDF+QR, webapp do check-inu, panel admina i model prowizyjny z ręcznymi wypłatami. Najwięcej zmiennej wnosi warstwa płatności — Model C z rozdzielaniem środków i ręcznymi wypłatami to nie „podpięcie Stripe”, tylko decyzja architektoniczna (PSP marketplace: PayU / Przelewy24 / Tpay / Stripe Connect) plus potencjalnie temat MIP/KNF, jeśli platforma samodzielnie przyjmuje i przekazuje środki. Doradztwo produktowe i technologiczne (o które wprost prosisz) też wkalkulowuję w stawkę.

**Rekomendacja płatności (bo o nią pytasz):**
Przy Modelu C szedłbym w **PSP marketplace z automatycznym splitem** (PayU Marketplace albo Przelewy24 Marketplace) — platforma nie dotyka funduszy submerchantów, co zdejmuje z Ciebie temat MIP/KNF i upraszcza ręczne wypłaty w MVP. Stripe Connect ma sens przy ekspansji zagranicznej, ale w PL przy split payments i PSD3 jest bardziej wymagający operacyjnie. Ostateczny wybór zależy od tego, czy masz własne konto merchant.

**Czego brakuje do doprecyzowania wyceny:**
1. **Wolumeny MVP** — ilu organizatorów, ile wydarzeń/mies., ile biletów na wydarzenie, jaki szczyt równoczesnych zakupów? Od tego zależy architektura, hosting i czy trzeba iść w kolejkę/async.
2. **Kto jest merchantem** — platforma czy organizator? To determinuje PSP i zakres KYC submerchantów.
3. **Budżet i termin** — „do negocjacji” nie pozwala ustawić priorytetów zakresu (np. czy zwroty i offline check-in wchodzą do MVP).

Jeśli wolisz, mogę rozbić wycenę na etapy (organizator → zakup → QR check-in → admin), żebyś mógł ciąć zakres bez przeprojektowywania całości.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 42–55k jest sensowna dla tego zakresu, ale rozjazd 470–610 h przy „part-time” i 10–14 tygodniach się nie spina — 470 h w 10 tygodni to ~47 h/tydzień, czyli pełny etat, nie part-time; przy realnym part-time (20 h/tyg.) to 23–30 tygodni, więc albo wydłużam termin, albo zawężam zakres MVP. Zgadywałem wolumeny, status merchanta i budżet — dlatego widełki są szerokie i bez odpowiedzi na te pytania mogą równie dobrze pójść w górę (płatności + KYC submerchantów potrafią zjeść 80–120 h). Nie dopisałem nic „na siłę”: rekomendacja PSP marketplace i wątek MIP/KNF to wprost odpowiedź na Twoją prośbę o doradztwo i są warunkowe, nie blokujące. Koryguję więc nie kwotę, a framing: 42–55k netto przy założeniu ~25–30 h/tyg. i 16–22 tygodniach, z zastrzeżeniem, że finalna liczba zależy od wolumenów i tego, kto jest merchantem.

=== DeepSeek-B — RUNDA 1 ===
**Wycena MVP: 27 000 – 36 000 zł netto** (300–400 h × 90 zł/h)
**Czas: 40–55 dni roboczych** (przy ~20 h/tyg. realnie 3–4 mies.)

**Uzasadnienie:** Zakres MVP obejmuje 6 modułów (panel organizatora, zakup, płatności, bilety PDF+QR, check-in webapp, panel admina) plus integracje płatnicze, maile transakcyjne i logikę prowizji — to realnie 300+ h dla jednej osoby. Doradztwo produktowe i wybór PSP wchodzą w stawkę, ale nie w zakres implementacji. Rozwój po MVP (mobile, SaaS, subskrypcje organizatorów) wyceniam osobno po zamknięciu etapu pierwszego.

**Czego brakuje do wyceny wiążącej:**
1. **Wolumeny MVP** — ilu organizatorów, ile wydarzeń/mies., ile biletów na wydarzenie, szczyt równoczesnych zakupów? Od tego zależy architektura i koszty infra.
2. **Kto jest merchantem** — masz własne konto merchant, czy platforma ma być pośrednikiem? Od tego zależy PSP.

**Rekomendacja płatności (odpowiadam wprost, bo prosisz):** przy Modelu C i ręcznych wypłatach rekomenduję **PSP marketplace (PayU Marketplace albo Przelewy24 Marketplace)** zamiast Stripe — przyjmują split i nie wymagają od Ciebie własnego merchant account ani obsługi funduszy submerchantów. **Uwaga regulacyjna:** jeśli platforma miałaby sama przyjmować środki i przekazywać je organizatorom, wchodzi temat MIP/KNF (przyjmowanie i przekazywanie środków = usługa płatnicza). PSP marketplace zdejmuje to z Ciebie. Jeśli macie własne konto merchant i świadomie nim rozliczacie — dostroję rekomendację.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 27–36k przy 300–400 h jest realna dla MVP w tym zakresie, ale raczej dolna granica — klient wprost chce „bardzo dobre UX/UI” i doradztwo, a to zwykle zjada więcej niż czysta implementacja; przy porządnym wykonaniu jednej osoby bliżej 400–500 h, czyli **36–45k zł**. Nie zgadywałem roli klienta ani jego intencji — pytania o wolumeny i merchant account są TYP 1, bo tylko on to wie. Mina MIP/KNF jest warunkowa i podana jako doradztwo, nie straszenie — to OK. Jedyne, co mogłem dopisać na siłę, to PWA/offline w check-inie i wątek PSD3 — to propozycje z zastrzeżeniem, nie założenia, więc zostawiłbym. Koryguję widełki na **30–42k zł** (330–460 h), reszta bez zmian.

=== DeepSeek-C — RUNDA 1 ===
## Wycena MVP

**Kwota:** 27 000 – 36 000 zł netto (300–400 h × 90 zł/h)
**Czas:** 7–9 tygodni przy pracy ~40 h/tyg.
**Etapy:** płatny milestone'ami (organizator + zakup + QR → admin → emaile/zwroty).

**Uzasadnienie:** Zakres MVP to realnie 3 produkty w jednym: panel organizatora, checkout z płatnościami online i webapp do check-inu QR plus panel admina — sama integracja PSP w modelu marketplace (split, KYC submerchantów, wypłaty) to 40–60 h. Doradztwo produktowe i technologiczne (rekomendacja PSP, architektura pod SaaS/mobile) wliczam w stawkę, ale wychodzi poza czystą implementację. Kwota nie zawiera etapu 2 (mobile, SaaS).

## Czego brakuje w zleceniu

1. **Wolumeny MVP:** ilu organizatorów, ile wydarzeń/mies., ile biletów na wydarzenie, szczyt równoczesnych zakupów? Od tego zależy architektura i koszty infrastruktury.
2. **Merchant account:** czy platforma ma własne konto merchant, czy działa jako pośrednik? To determinuje wybór PSP.
3. **Rekomendacja PSP (klient pyta wprost):** przy Modelu C i ręcznych wypłatach w MVP rekomenduję **PSP marketplace (PayU Marketplace / Przelewy24 Marketplace / Tpay)** zamiast Stripe Connect — środki submerchantów nie przechodzą wtedy przez moje konto, co zdejmuje temat wpisu MIP/KNF. Jeśli macie własne konto merchant i świadomie chcecie nim rozliczać — dostroję architekturę, ale wtedy wchodzi indywidualna ocena prawna modelu.
4. **Check-in QR:** proponuję PWA z cache offline jako domyślne (hale, słaby zasięg), chyba że wystarczy online.
5. **Zwroty:** proponuję objąć MVP zwrotami przez PSP, nie tylko mailem — inaczej generujecie ręczną robotę przy pierwszej anulacji.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Wycena jest uczciwa co do rzędu wielkości — 300–400 h na ten zakres przy 90 zł/h daje 27–36k i to się broni, bo sama integracja marketplace PSP z KYC submerchantów to realnie 40–60 h, a nie 15. Ale górna granica 400 h jest lekko naciągnięta: dodałem bufor na RODO, deploy i testy, których klient wprost nie zamawiał — przy MVP bez mobile realniej jest 280–360 h, czyli **25 000 – 32 500 zł**. Nie zgadywałem przy stacku ani UI, bo tego w zleceniu nie ma; zgaduję tylko wolumeny, a od nich zależy architektura — dlatego pytam, zamiast dopisywać. „Na siłę" dorzuciłem zwroty przez PSP i PWA offline — to sensowne propozycje, ale jeśli klient je odrzuci, kwota spada o ~10–15 h. Reasumując: koryguję widełki do **25–32,5k zł**, reszta wyceny i uzasadnienie bez zmian.

=== DeepSeek-D — RUNDA 1 ===
**Wycena MVP: 32 000 – 45 000 zł** (ok. 355–500 h × 90 zł/h)

**Czas: 11–13 tygodni** pracy solo (przy założeniu, że dostarczacie treści/grafiki i decyzje na bieżąco).

**Uzasadnienie:** Zakres MVP obejmuje realnie 6 modułów (panel organizatora, sklep+checkout, system biletów PDF/QR, panel admina, check-in webapp, e-maile transakcyjne) plus integrację płatności w modelu marketplace — to nie jest „landing z biletem”, a platforma transakcyjna, gdzie każdy moduł ma własną logikę uprawnień i stanów. Płatności w modelu prowizyjnym (Model C) to najbardziej ryzykowny i czasochłonny element, bo wymaga wyboru PSP i rozstrzygnięcia kto jest merchantem — poniżej moje pytania. Przy budżecie „do negocjacji” traktuję tę kwotę jako punkt startowy; przy rozłożeniu prac etapami (najpierw organizator + zakup + QR, potem admin) można wejść taniej w pierwszym kroku.

**Czego brakuje w zleceniu (potrzebuję odpowiedzi przed startem):**
1. **Wolumeny MVP** — ilu organizatorów, ile wydarzeń/mies., ile biletów na wydarzenie, jaki szczyt równoczesnych zakupów? Od tego zależy architektura, koszty infrastruktury i realna pracochłonność.
2. **Merchant account** — czy macie własne konto merchant i to Wy rozliczacie, czy platforma ma działać jako pośrednik? To przesądza wybór PSP (Stripe Connect vs PayU Marketplace / Przelewy24 Marketplace / Tpay Marketplace) i ewentualny temat wpisu MIP/KNF przy ręcznych wypłatach.

**Moja rekomendacja płatności (bo o to pytacie wprost):** przy Modelu C z ręcznymi wypłatami w MVP rekomenduję **PSP marketplace (PayU Marketplace albo Przelewy24 Marketplace)** — automatyczny split i weryfikacja submerchantów zdejmują z Was obowiązek ręcznego obracania cudzymi środkami, co przy „ręcznych wypłatach” i Modelu C jest realnym ryzykiem regulacyjnym (potencjalnie MIP/KNF). Jeśli macie własne konto merchant i chcecie nim rozliczać — dostroję rekomendację. Stripe Connect zostawiłbym na etap po PSD3 ze względu na zmiany w fund segregation.

**Poza tym proponuję domyślnie (mogę dostroić):** stack Next.js + PostgreSQL + PSP marketplace; check-in jako PWA z cache offline (nie pytam, czy internet w hali będzie działał); zwroty w MVP przez PSP, nie tylko mailem; kolejność prac: panel organizatora → zakup → QR check-in → panel admina.

Chętnie pokażę portfolio i rozbiję wycenę na etapy — dajcie znać, czy odpowiadacie na punkty 1–2 powyżej.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: **wycena była zaniżona o jakieś 20–30%.** Realnie ten zakres solo to 400–550 h, a nie 355–500 h — sam marketplace split + onboarding submerchantów + testy płatności potrafią zjeść 100 h, do tego dochodzi panel admina z konfiguracją prowizji i e-maile transakcyjne z załącznikami PDF/QR. Korekta: **40 000 – 55 000 zł** przy 90 zł/h, 13–16 tygodni; niższa granica 32 k była kalkulacją „wszystko idzie gładko”, a tak nie idzie.

Co zgadłem, a czego nie powinienem: **zwroty przez PSP w MVP** — klient wprost wpisał „zwroty” tylko przy e-mailach, nie jako osobny moduł, więc to był lekki scope creep. **PWA offline do check-inu** to sensowny default, ale nadal moja propozycja, nie wymóg klienta — oznaczyłem to jako „mogę dostroić”, więc OK. **MIP/KNF** nie zgadłem — to realna mina przy Modelu C z ręcznymi wypłatami i dobrze, że ją podniosłem warunkowo, a nie jako straszak.

Czego nie zgadłem wcale: **wolumenów i tego, kto jest merchantem** — bez tego każda wycena jest w widełkach, nie w kwocie. Dlatego trzymam 2 pytania TYP 1 i nie schodzę z widełek, dopóki klient nie odpowie.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 35000,
  "kwota_gorna": 50000,
  "definitywna": false,
  "od_czego_zaleza": [
    "wolumeny MVP: liczba organizatorów, wydarzeń/mies., biletów na wydarzenie i szczyt równoczesnych zakupów",
    "kto jest merchantem i wybór PSP marketplace (PayU/Przelewy24/Tpay vs Stripe Connect) oraz zakres KYC submerchantów",
    "zakres zwrotów, check-inu offline/PWA, e-maili transakcyjnych i doradztwa produktowo-technologicznego w MVP",
    "tempo pracy i skład wykonawcy: freelancer part-time vs mały zespół"
  ],
  "dni_od": 75,
  "dni_do": 120,
  "uzasadnienie": "Po dwóch rundach widać rozrzut: B i C oscylują wokół 25–42 tys. zł, a A i D wokół 40–55 tys. zł; mediana i średnia środka wypadają blisko 40 tys. zł, więc finalne widełki 35–50 tys. zł netto najlepiej godzą te głosy. Zakres MVP jest duży i transakcyjny: płatności w Modelu C, wypłaty, QR check-in, panel admina, e-maile i doradztwo PSP realnie zwiększają pracochłonność ponad prostą implementację. Rozbieżność wynika głównie z nieznanych wolumenów i tego, kto jest merchantem — od tego zależy architektura, KYC i ryzyko MIP/KNF. Dlatego to nie wycena definitywna, lecz widełki do doprecyzowania po odpowiedziach na pytania TYP 1."
}

=== FINALNA WYCENA ===
35000-50000 zl netto | 75-120 dni | WIDELKI
Od czego zalezy: wolumeny MVP: liczba organizatorów, wydarzeń/mies., biletów na wydarzenie i szczyt równoczesnych zakupów, kto jest merchantem i wybór PSP marketplace (PayU/Przelewy24/Tpay vs Stripe Connect) oraz zakres KYC submerchantów, zakres zwrotów, check-inu offline/PWA, e-maili transakcyjnych i doradztwa produktowo-technologicznego w MVP, tempo pracy i skład wykonawcy: freelancer part-time vs mały zespół
Uzasadnienie rozjemcy: Po dwóch rundach widać rozrzut: B i C oscylują wokół 25–42 tys. zł, a A i D wokół 40–55 tys. zł; mediana i średnia środka wypadają blisko 40 tys. zł, więc finalne widełki 35–50 tys. zł netto najlepiej godzą te głosy. Zakres MVP jest duży i transakcyjny: płatności w Modelu C, wypłaty, QR check-in, panel admina, e-maile i doradztwo PSP realnie zwiększają pracochłonność ponad prostą implementację. Rozbieżność wynika głównie z nieznanych wolumenów i tego, kto jest merchantem — od tego zależy architektura, KYC i ryzyko MIP/KNF. Dlatego to nie wycena definitywna, lecz widełki do doprecyzowania po odpowiedziach na pytania TYP 1.
