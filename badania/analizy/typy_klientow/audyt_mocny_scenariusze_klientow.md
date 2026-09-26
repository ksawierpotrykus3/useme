# RAPORT AUDYTOWY: 9 SCENARIUSZY PSYCHOLOGICZNO-OPERACYJNYCH
## Główny Arbiter Strategiczny B2B · Red Team · Weryfikacja operacyjna pod bota Useme

**Autor:** Główny Arbiter Strategiczny B2B / Psycholog Biznesu / Szef Red Team
**Przedmiot audytu:** `klient_01` – `klient_06` + 3 modyfikatory (`delegowany`, `phantom_startup`, `rescue`)
**Baza porównawcza:** 470 zleceń (56 wygranych z priv, 414 zamkniętych), 16 kart TECH_01–TECH_16, twarde reguły systemowe 1–4
**Rygor:** twarda prawda rynkowa, zero taryfy ulgowej

---

## 1. WERYFIKACJA RZECZYWISTOŚCI RYNKOWEJ — CZY PORTRETY SĄ PRAWDZIWE?

### 1.1. Diagnoza ogólna

Portrety są **literacko znakomite, operacyjnie w większości prawdziwe, ale miejscami niebezpiecznie przegadane**. To klasyczny problem „scenariusza pisanego przez kogoś, kto rozumie człowieka, ale nie do końca rozumie, po co ten dokument będzie czytany". Ryzyko: model AI potraktuje „gęstość emocjonalną" jako **sygnał do naśladowania w ofercie**, a nie jako **soczewkę do rozumienia intencji**.

Kluczowe pytanie audytowe: **czy scenariusz tłumaczy zachowanie klienta, czy zachęca AI do psychologizowania na zewnątrz?** W 6 z 9 plików granica ta jest rozmyta.

### 1.2. Weryfikacja profil-po-profilu

| Profil | Autentyczność rynkowa | Zgodność z danymi (470 zleceń) | Ocena Red Team |
|---|---|---|---|
| **01 Tradycyjne MŚP / ERP** | ✅ Bardzo wysoka. „Syn założyciela", „żona w księgowości", „kubek z logiem dostawcy opakowań" — to nie fikcja, to codzienność polskiego MŚP. | ⚠️ **Konflikt z danymi**: skala 8–80 osób i integracje ERP (Optima/Subiekt/Enova) to segment, w którym Useme historycznie **nie konwertuje** dużymi kwotami. Jedyny duży kontrakt (12,1k) to Doktor Monika — czyli profil **04**, nie **01**. | Ryzyko: AI zacznie pisać ciepłe oferty do właścicieli fabryk, którzy w 90% nie klikną „escrow". |
| **02 E-commerce Merchant** | ✅ Trafny. „Zaczynał na Allegro z garażu", „żona o 2 w nocy", „konwersja spadła" — to jest prawda. | ✅ Segment realnie konwertuje drobnymi zleceniami. ❗Ale scenariusz sugeruje „wrócę z większym" — dane mówią, że **nie wraca** z większym. To pobożne życzenie, nie wzorzec. | Ryzyko: AI zacznie budować relację „na przyszłość", zamiast zamykać transakcję tu i teraz. |
| **03 Agencja / Software House** | ✅ Portret „technicznego rozjemcy" jest celny. ❗Ale to segment **bardzo rzadko** korzystający z Useme (wewnętrzne zespoły, własne sieci podwykonawców). | ❌ **Słabo potwierdzony danymi**. 56 wygranych z priv — trudno uwierzyć, że duży udział to software house'y. Bardziej prawdopodobne: mikro-zlecenia od merchantów i MŚP. | Ryzyko: AI będzie nadinterpretować „agencja szuka podwykonawcy" tam, gdzie jest zwykły klient szukający taniej rączki. |
| **04 Ekspert dziedzinowy / regulowany** | ✅ Portret lekarza/komornika/prawnika jest **bezbłędny psychologicznie**. | ✅✅ **Potwierdzony twardo** — Doktor Monika 12,1k PLN to jedyny duży win i to jest ten profil. | To profil o **najwyższej wartości LTV** w bazie. Należy go promować do rangi „profilu flagowego". |
| **05 Tech-Agnostic Business Owner (33%)** | ✅ Najlepiej skalibrowany ze wszystkich. „Nie pije kawy z programistami" — genialne, operacyjnie prawdziwe. | ✅✅ Segment 33% rynku — zgodne z deklarowaną bazą. | Ryzyko: scenariusz jest tak dobry, że AI może przegapić **kiedy ten klient jest jednocześnie Rescue/Phantom** — hybrydyzacja jest tu krytyczna. |
| **06 Quick Fix / Awaria** | ✅ Dwa bieguny (mikro- i prywatny) prawidłowo rozróżnione. „Kolega programisty za 1500 zł" — kwintesencja polskiego IT. | ✅ Segment najczęściej konwertuje drobnymi kwotami. To jest **chleb powszedni Useme**. | Ryzyko: brak ostrzeżenia, że „szybka naprawa" często jest **wstępem do projektu**, który przekracza budżet i wymaga renegocjacji. |
| **M1 Delegowany Pracownik** | ✅ Portret asystentki/sekretarki jest **bezbłędny** — to najbardziej niedoceniany kanał sprzedaży B2B. | ⚠️ 4,3% rynku brzmi realistycznie, ale dane Useme tego nie potwierdzają wprost. | **Ukryte ryzyko**: to jest kanał **przez który wchodzą największe budżety** (bo asystentka szefa = szef z budżetem). Ale scenariusz tego nie eksponuje! |
| **M2 Phantom Startup** | ✅✅ Portret „nie pyta o cenę, pyta czy wierzysz" — zgodny z danymi (90% Phantom Leads). | ✅✅✅ **Najważniejszy modyfikator w całym zestawie** — bezpośrednio uzasadniony danymi. | ✅ Prawidłowo oznaczony jako „ignoruj gdy pyta o cenę". |
| **M3 Rescue / Sparzony** | ✅✅ Portret traumy po poprzednim wykonawcy — autentyczny, gęsty psychologicznie. | ✅ 12,1% rynku brzmi realnie. To segment, który **realnie płaci** (bo już raz stracił). | Ryzyko: scenariusz może skłonić AI do **zbyt emocjonalnego tonu** w ofercie. Sparzony klient chce **konkretu i gwarancji**, nie empatii. |

### 1.3. Wnioski z sekcji 1

1. **Modyfikatory są mocniejsze niż profile podstawowe.** Phantom Startup i Rescue powinny być **pierwszym filtrem**, a nie doklejką.
2. **Profil 04 (Ekspert dziedzinowy) powinien być podniesiony do rangi „profilu flagowego"** — to jedyny potwierdzony duży win.
3. **Profil 03 (Agencja/Software House) wymaga rewizji** — jest literacko dobry, ale słabo potwierdzony empirycznie. Albo wzmocnić danymi, albo oznaczyć jako „niska konwersja".
4. **Brakuje profilu „Student / niski budżet <500 zł"** — a to, jak sam scenariusz 01 zauważa, jest realny segment do wykluczenia. Powinien być osobnym anty-profilem.

---

## 2. CZY NAPRAWDĘ ZLIKWIDOWANO MECHANIZM „IF-THEN"?

### 2.1. Ocena formalna

**Częściowo tak, ale nie w 100%.** Scenariusze w większości używają języka soczewki („AI ma przez nią patrzeć"), ale w każdej sekcji „Kiedy zignorować" i „Kiedy odrzucić" **faktycznie wprowadzają ukryte IF-THEN**. Przykłady:

- *„Gdy kwota jest absurdalnie niska (poniżej 500 zł) — to nie ten typ"* → to jest **IF kwota < 500 THEN odrzuć**.
- *„Jeśli pyta o cenę – to nie Phantom Startup"* → **IF pyta_o_cenę THEN nie_phantom**.
- *„Gdy klient nie wspomina o poprzednim wykonawcy i nie ma oznak traumy"* → **IF brak_wzmianki_o_wykonawcy THEN nie_rescue**.

**Verdict:** deklaracja „zero IF-THEN" jest **nieprawdziwa**. Prawda jest taka: **IF-THEN zostały przeniesione z formy „instrukcja" do formy „demarkacja kontekstu"**. To jest różnica istotna — ale nie jest to likwidacja. To jest **transformacja**.

### 2.2. Czy transformacja jest wartościowa?

✅ **Tak, jest wartościowa**, z trzech powodów:

1. **Dają modelowi prawo do wątpliwości.** Klasyczne IF-THEN wymusza decyzję binarną. Nowa forma daje modelowi „aparat pojęciowy" i pozwala mu **ważyć podobieństwo**, a nie tylko klasyfikować.
2. **Umożliwiają hybrydyzację.** Scenariusz 05 (Tech-Agnostic) jawnie mówi o hybrydach z Rescue/Phantom. Klasyczny IF-THEN by to uniemożliwił.
3. **Zmuszają do myślenia o człowieku, nie o ogłoszeniu.** To jest realna wartość operacyjna.

### 2.3. Gdzie transformacja zawodzi?

❌ **Sekcja 6 („waga podobieństwa", „kiedy zignorować") jest napisana nierówno.** W niektórych plikach jest genialna (Phantom Startup: „granica jest jedna — nie pyta o cenę"), w innych mglista (Merchant: „nie naciskaj, wróć za miesiąc" — co to znaczy operacyjnie?).

❌ **Brakuje sekcji „jak rozpoznać hybrydę"** w 7 z 9 plików. Jedynie Tech-Agnostic i Rescue mają cokolwiek na ten temat.

### 2.4. Rekomendacja

**Nie likwidujcie IF-THEN całkowicie — one są potrzebne jako bezpieczniki.** Ale przenieście je do jednego, wspólnego pliku `demarkacje.md`, żeby nie zaśmiecały scenariuszy. Scenariusze mają być soczewką. Demarkacje mają być twarde.

---

## 3. SPÓJNOŚĆ Z BAZĄ INŻYNIERYJNĄ (TECH_01 – TECH_16)

### 3.1. Punkty styku profil ↔ karta techniczna

| Profil | Karty TECH | Spójność | Uwagi Red Team |
|---|---|---|---|
| 01 MŚP/ERP | Optima, Subiekt, Enova, WZ, magazyn | ✅ Wysoka | Scenariusz mówi językiem magazynu — zgodne z TECH. Ale **brak wzmianki o KSeF**, który jest realnym triggerem 2025/2026. |
| 02 E-commerce | Integracje, stany magazynowe, płatności | ✅ Wysoka | „Stany magazynowe się nie zgadzają" → wprost do TECH_04 (integracje). Spójne. |
| 03 Agencja/SW House | API, deployment, CI/CD | ⚠️ Częściowa | Scenariusz używa słowa „deployment" (05 go unika) — to OK dla tego profilu. Ale **brakuje TECH_xx dla code review / rescue code** — a to jest główny use case agencji. |
| 04 Ekspert dziedzinowy | RODO, dokumentacja medyczna, KSeF | ⚠️ Wymaga wzmocnienia | Scenariusz świetnie mówi o odpowiedzialności prawnej, ale **nie mapuje jej na konkretne karty TECH** (np. szyfrowanie, backup, audyt). Luka do uzupełnienia. |
| 05 Tech-Agnostic | Wszystkie, ale unika żargonu | ✅✅ Wysoka | „Deployment" jest zakazane — spójne z TECH. Ale **brakuje mapy: kiedy użyć jakiej karty TECH bez mówienia o niej wprost**. |
| 06 Quick Fix | Hosting, WordPress, WooCommerce | ✅ Wysoka | Spójne z TECH_07/08 (prawdopodobnie). |
| M1 Delegowany | Raportowanie, statusy | ⚠️ Luka | Scenariusz mówi „będzie kontrola i raportowanie" — ale **nie mapuje tego na TECH_y (dashboard, checklisty)**. |
| M2 Phantom | Brak — i słusznie | ✅ | Phantom nie dostaje karty TECH, bo nie jest klientem. Dobrze. |
| M3 Rescue | Audyt, backup, ratunek | ⚠️ Częściowa | Scenariusz mówi o ratunku, ale **zakaz darmowych audytów** (reguła #2) jest w konflikcie z tym, co Rescue oczekuje. Trzeba to jasno zaznaczyć: „Rescue chce audytu — ale my dajemy audyt **w ramach zlecenia**, nie przed". |

### 3.2. Kluczowa luka systemowa

**Brak tabeli mapowania PROFIL → KARTY TECH → SEKCJA SCENARIUSZA.** Bez tego model AI sam musi zgadywać, którą kartę TECH „podczepić" pod dany profil. To jest zaproszenie do halucynacji technicznej.

**Rekomendacja:** stwórzcie plik `mapa_profil_tech.md` z prostą tabelą: profil → karty TECH → sugerowany poziom żargonu → sugerowany poziom empatii → docelowa długość oferty.

---

## 4. ANALIZA LUK I RYZYK (BLINDSPOTS)

### 4.1. Ryzyko #1 — „PRZEGADANIE" OFERTY (KRYTYCZNE)

**Scenariusze są pisane gęstym, emocjonalnym językiem. Model AI ma tendencję do naśladowania stylu wejściowego.** Efekt: bot będzie generował oferty 1500-znakowe, gdy walidator wymaga 300-450 znaków dla mikro-zleceń.

**Dowód z materiału:** scenariusz 02 mówi „wróć za miesiąc" — sugeruje **relację**, nie transakcję. To jest zaproszenie do rozwlekłości.

**Mitygacja:**
- Dodać do każdego scenariusza sekcję „**MINIMUM OPERACYJNE**" — jedno zdanie, które MUSI się znaleźć w ofercie, niezależnie od długości.
- W walidatorze `agent_06`: twardy limit znaków + test „czy oferta zawiera konkret techniczny w pierwszych 100 znakach?".

### 4.2. Ryzyko #2 — PSYCHOLOGIZACJA KOSZTEM KONKRETU

Scenariusze 04 i M3 (Rescue, Ekspert) są napisane tak, że AI może uznać, że „wystarczy zrozumieć ból". **Nie wystarczy.** Doktor Monika zapłaciła 12,1k, bo dostała **konkretny produkt** (prawdopodobnie dokumentacja medyczna + RODO + integracja), a nie dlatego, że ktoś „zrozumiał jej świat".

**Mitygacja:**
- W każdym scenariuszu dodać **sekcję „KONKRET, KTÓRY MUSI PAŚĆ"** — co konkretnie oferta musi zawierać (np. „karta TECH_04", „30 dni gwarancji", „przykład podobnego wdrożenia").
- W walidatorze `agent_07`: test „czy w ofercie jest minimum 1 element inżynierski?".

### 4.3. Ryzyko #3 — PHANTOM LEAK

90% founderów z budżetem 10k-35k to Phantom Leads. Modyfikator M2 jest przydatny do zrozumienia ich psychologii, ale bot nie może traktować ich obietnic jako pewnego zysku.

**Mitygacja:**
- **ZAKAZ samowolnego wyceniania „małego MVP” czy cięcia zakresu zlecenia**. Bot wycenia pełny zakres zlecenia zgodnie z rynkiem.
- **Ścisły, dokładny warunek na wycenę MVP/etapową:** Dopuszczalna WYŁĄCZNIE wtedy, gdy: (a) analiza konkurencji pod danym zleceniem wykazuje, że inni wykonawcy składają oferty na etap wstępny/PoC, LUB (b) zleceniodawca wprost zażądał w ogłoszeniu fazy MVP / prototypu. W przeciwnym razie wyceniamy całość.
- Brak jałowego czatowania w nieskończoność o wirtualnej wizji bez domknięcia zlecenia.

### 4.4. Ryzyko #4 — NADUŻYCIE „RESCUE"

Scenariusz M3 sugeruje, że każdy klient wspominający poprzedniego wykonawcę to Rescue. Nie — część wzmianek o poprzednim wykonawcy to neutralny kontekst, nie trauma.

**Mitygacja:**
- W M3 rozróżniać: Rescue ma realny ból i nieufność po porzuceniu projektu, neutralny podaje po prostu stan faktyczny kodu.

### 4.5. Ryzyko #5 — BRAK STRATEGII NA PRZEGRANĄ

Scenariusze mówią, kiedy wygrać, ale nie mówią, co zrobić, gdy klient nie odpowiada w 48h. W realiach 56 wygranych z 470 zleceń, większość zleceń to brak odpowiedzi. Bot musi mieć strategię na brak odpowiedzi.

**Mitygacja:**
- Follow-up nie istnieje. Jeśli klient nie odpowiada na priv — nie ponawiamy i nie spamujemy. 100% asynchronicznie i z klasą.

### 4.6. Ryzyko #6 — HALUCYNACJA SYSTEMÓW

Scenariusze mówią ogólnie „integracja z ERP”, ale model musi wiedzieć, o jaki konkretny system chodzi, by nie rzucać nazwami z sufitu.

**Mitygacja:**
- Zakaz sztywnych whitelist (na Useme jest masa nisz: TopSolid CNC, Anteeo WMS, Odoo, Strapi, własne API). Model opiera się ściśle na nazwach systemów wymienionych przez klienta w ogłoszeniu lub w powiązanej karcie technologicznej. Zero zgadywania.

---

## 5. WERDYKT I REKOMENDACJE WDROŻENIOWE

### 5.1. Werdykt końcowy

**Zielone światło warunkowe.** Scenariusze są **znacznie lepsze niż standardowa baza promptów**, ale w obecnej formie **nie nadają się do bezpośredniego wpięcia** pod produkcyjnego bota w `kod/`. Wymagają trzech zmian przed wdrożeniem:

1. **Skrócenia i ustrukturyzowania** — każdy scenariusz musi mieć jednolitą strukturę z sekcjami: `MINIMUM OPERACYJNE`, `KONKRET KTÓRY MUSI PAŚĆ`, `DEMARKACJE`, `HYBRYDY`.
2. **Oddzielenia soczewki od instrukcji** — IF-THEN przenieść do osobnego pliku `demarkacje.md`.
3. **Dodania mapy PROFIL → TECH** — inaczej model będzie halucynował karty techniczne.

**Ocena w skali 1–10: 7,5/10.** Materiał jest ponadprzeciętny, ale ma zbyt wiele „literackiego tłuszczu" i za mało „operacyjnego mięsa".

### 5.2. Prawdziwe, Minimalne Bezpieczniki (Korekta Falsyfikacyjna: AI Ogarnie)

> **Kluczowa zasada:** Odrzucamy wszelkie sztuczne wyliczenia procentowe w tekście, sztywne whitelisty systemów i roszczeniowe żądania depozytu w pierwszej wiadomości. Sztuczne procenty i sztywne zakazy zabijają naturalność i konwersję. Pozostawiamy wyłącznie **minimalne, fundamentalne ramy**, a całą resztę niuansów i inteligencji kontekstowej powierzamy modelowi AI:

1. **Ramy Długości (Zwięzłość zamiast Lania Wody)**:
   - Mikro-naprawy i proste poprawki: naturalnie zwięzłe (~300–450 znaków – cena, czas, gwarancja + pytanie).
   - Średnie i duże projekty: naturalnie szersze (~600–900 znaków – podział na logiczne etapy).
   - *Brak jakichkolwiek sztucznych limitów procentowych na sekcje!*

2. **Zero Korpo-Bełkotu i Pustego Marketingu**:
   - Wycięcie generycznych formułek: *„Dzień dobry, chętnie podejmę się zlecenia...”*, *„Posiadam bogate doświadczenie...”*.
   - Start od razu od sedna problemu klienta.

3. **100% Asynchroniczność**:
   - Zakaz propozycji calli, spotkań wideo i telefonów. Rozmowa toczy się pisemnie na czacie/priv.

4. **Trzeźwa Gwarancja**:
   - Standardowo 30 dni asysty na własny kod (ochrona przed pułapką darmowego rocznego supportu na zewnętrzne API czy antyboty).

*Odrzucono jako szkodliwe:*
- ❌ **Żądanie depozytu w 1. wiadomości** – zabija relację; profesjonalista wycenia etapy, a platforma sama zabezpiecza escrow.
- ❌ **Sztywna playlista/whitelist systemów** – zabiłaby zlecenia niszowe (TopSolid, Anteeo, Odoo, Strapi, własne API).
- ❌ **Sztuczne limity procentowe słów/zdań** – prowadzą do zubożenia językowego i robotycznego tonu.

### 5.3. Rekomendacje dodatkowe (poza bezpiecznikami)

1. **Przenieś profil 04 (Ekspert dziedzinowy) na pozycję flagową.** To jedyny potwierdzony duży win (Doktor Monika). Zbuduj wokół niego osobny playbook.
2. **Zdemontuj profil 03 (Agencja/SW House) albo wzmocnij go danymi.** W obecnej formie to potencjalna pułapka: AI może marnować zasoby na segment, który nie konwertuje.
3. **Dodaj anty-profil `student_low_budget.md`** — dla zleceń < 500 zł. Jasny komunikat: „nie odpowiadaj, nie edukuj, nie trać czasu".
4. **Dodaj profil `hybryda_05+rescue.md`** — Tech-Agnostic + trauma. To najczęstszy realny przypadek: właściciel MŚP, który nie zna się na tech i został oszukany. Wymaga osobnego, krótkiego playbooka.
5. **Ujednolić styl wejściowy.** Scenariusze 04 i M3 są pisane zbyt literacko. Skróć o 30% i zamień metafory na fakty operacyjne.

### 5.4. Ostateczna rekomendacja wdrożeniowa

**Wdróż z zachowaniem minimalnych reguł:**
- Bezpośrednie podłączenie scenariuszy pod bota jako soczewki kontekstowej.
- Utrzymanie sprawdzonych minimalnych zasad w walidatorach: ramy długości (300–450 vs 600–900 znaków), zero korpomowy, 100% asynchroniczność na priv, 30 dni gwarancji na własny kod.
- AI samodzielnie i organicznie zarządza proporcjami i słownikiem na podstawie ogłoszenia.

**Kluczowy KPI do monitorowania:** konwersja na priv (bo to jedyny kanał z realnym potencjałem) oraz **naturalność i inżynierski konkret oferty**.

---

## KONKLUZJA

Zestaw 9 scenariuszy to **najlepszy materiał psychologiczny, jaki widziałem w kontekście bota B2B na polskim rynku**. Ale ma jedną fundamentalną wadę: **jest pisany dla człowieka, który ma czytać i rozumieć, a nie dla modelu, który ma ważyć i decydować**. AI nie potrzebuje metafor o „kubku z logiem dostawcy opakowań" — potrzebuje jasnych demarkacji, mapy TECH i twardych limitów.

**Zamień poezję na precyzję. Zachowaj głębię, wyrzuć tłuszcz. Wtedy — zielone światło bezwarunkowe.**

*Koniec raportu.*