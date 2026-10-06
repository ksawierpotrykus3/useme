=== PROBA 1 ===
SEDZIA: {"status": "VETO", "kara_pkt": -20, "cytat_lub_brak": "Partia 20 szkiców przed umową to realna praca, proponuję ją jako płatny test odliczany od głównego zlecenia.", "uzasadnienie": "Klient wprost napisał, że 'przed ostatecznym zatwierdzeniem umowy i uruchomieniem głównego importu wymagana jest bezpłatna partia próbna 20 sztuk'. Oferta pomija to życzenie i zamienia bezpłatny test na płatny, mimo że klient postawił ten warunek jednoznacznie. To realny zgrzyt, który może zniechęcić klienta do odpowiedzi, bo pokazuje, że oferent nie uszanował kluczowego wymagania.", "instrukcja_naprawy": "Uszanuj warunek klienta i zaproponuj bezpłatną partię próbną 20 szkiców przed umową, tak jak w ogłoszeniu. Jeśli chcesz zabezpieczyć się przed stratą czasu, możesz zaproponować ograniczenie zakresu testu lub jasne kryteria jego zakończenia, ale nie zmieniaj go na płatny."}

WERYFIKACJA FAKTOW:
Poniżej weryfikacja każdego z zakwestionowanych twierdzeń zawartych w ofercie. Każde twierdzenie zostało ocenione niezależnie, na podstawie dostępnych źródeł.

---

### 1. Twierdzenie: „Od lipca 2024 Allegro wymaga powiązania ofert z Katalogiem, a części samochodowe nie są wśród wyjątków.”

**Werdykt: CZĘŚCIOWO POTWIERDZONE**

- **Wymóg powiązania z Katalogiem od lipca 2024 – POTWIERDZONE.**  
  Oficjalna pomoc Allegro potwierdza, że od 6 czerwca 2024 nie można edytować ofert bez powiązania ich z Katalogiem Produktów. Inny artykuł branżowy podaje, że od 1 lipca 2024 obowiązek ten rozciągnięto na „zdecydowaną większość kategorii”.

- **Części samochodowe jako wyjątek – NIEPOTWIERDZONE (a nawet wskazujące na brak wyjątku).**  
  Lista kategorii zwolnionych z obowiązku, przytoczona w jednym ze źródeł, obejmuje m.in. „Automotive – Cars”, „Automotive – Motorcycles and quads”, „Automotive – Machinery”, ale **nie wymienia kategorii „Części samochodowe”**.  
  Co więcej, oficjalny komunikat deweloperski Allegro z 2019 r. dotyczy **kategorii z częściami motoryzacyjnymi** (np. „Układ hamulcowy”) i opisuje wymagania związane z powiązaniem ofert z produktem, co sugeruje, że kategoria ta **podlega produktyzacji**, a nie jest z niej zwolniona.

**Wniosek:** Twierdzenie oferenta, że „części samochodowe nie są wśród wyjątków”, jest **zgodne z dostępnymi informacjami** – kategoria ta nie pojawia się na liście wyjątków, a wręcz istnieją dowody na objęcie jej wymogiem powiązania z Katalogiem. Oferent słusznie więc ostrzega, że plan klienta (całkowite wyłączenie parowania) może być nierealny.

---

### 2. Twierdzenie: „Regulamin OTOMOTO zakazuje agregowania danych i pobierania materiałów w celu udostępniania ich na innych serwisach; pobranie zdjęć wymaga zgody Grupy OLX.”

**Werdykt: POTWIERDZONE**

Cytat z regulaminu OTOMOTO, przytoczony na forum 4programmers.net, jednoznacznie stwierdza:  
> „Zabronione jest jakiekolwiek agregowanie i przetwarzanie danych oraz innych informacji dostępnych w Serwisie OTOMOTO w celu ich dalszego udostępniania osobom trzecim w ramach innych serwisów internetowych jak i poza Internetem.”  
> „Pobieranie lub wykorzystywanie w jakimkolwiek zakresie dostępnych w ramach Serwisu OTOMOTO materiałów wymaga każdorazowo zgody Grupy OLX…”

**Wniosek:** Oferent prawidłowo zidentyfikował ryzyko prawne związane z migracją danych i zdjęć z OTOMOTO. Twierdzenie jest w pełni potwierdzone.

---

### 3. Twierdzenie: „Nie istnieje gotowy, uniwersalny skrypt OTOMOTO do Allegro dla 5952 ofert.”

**Werdykt: POTWIERDZONE (brak dowodów na istnienie gotowego rozwiązania)**

Przeszukanie publicznych repozytoriów (GitHub), forów i wyników wyszukiwania nie ujawniło istnienia gotowego, uniwersalnego skryptu, który realizowałby kompleksową migrację ofert z OTOMOTO do Allegro. Znalezione projekty to albo scrapery danych (np. `scrapy-otomoto`), albo narzędzia do integracji pośredniej (BaseLinker, EasyUploader), które nie stanowią „gotowego skryptu” dedykowanego temu konkretnemu zadaniu.

**Wniosek:** Oferent ma rację, twierdząc, że nie istnieje gotowy, uniwersalny skrypt – tego typu migracja zawsze wymaga pracy dostosowawczej. Twierdzenie jest potwierdzone brakiem dowodów przeciwnych.

---

### 4. Twierdzenie: „Partia 20 szkiców przed umową to realna praca, proponuję ją jako płatny test.”

**Werdykt: SPRZECZNE Z WYMAGANIEM KLIENTA**

Ogłoszenie klienta zawiera jednoznaczne stwierdzenie:  
> „Przed ostatecznym zatwierdzeniem umowy i uruchomieniem głównego importu wymagana jest bezpłatna partia próbna 20 sztuk w formie szkiców na koncie.”

Oferta proponuje jednak:  
> „Partia 20 szkiców przed umową to realna praca, proponuję ją jako płatny test odliczany od głównego zlecenia.”

**Wniosek:** Oferent **zmienia warunek klienta** (bezpłatny test) na płatny. Jest to **realny zgrzyt**, który może zniechęcić klienta. Zgodnie z instrukcją naprawy, oferta powinna uszanować warunek klienta i zaproponować **bezpłatną partię próbną 20 szkiców**, ewentualnie z jasno określonymi kryteriami zakończenia testu, ale bez zmiany go na płatny.

---

### 5. Pozostałe elementy oferty (dla kompletności)

- **Twierdzenie o „całkowitym wyłączeniu parowania” i wpisywaniu początku tytułu w pole numeru części:**  
  Oferent słusznie ostrzega, że szkice bez powiązania z Katalogiem mogą zostać odrzucone przez API lub zablokowane po utworzeniu. Dokumentacja Allegro wskazuje, że zasób `POST /sale/product-offers` służy do tworzenia ofert **powiązanych z produktem**, a nie do tworzenia szkiców bez takiego powiązania. Zatem plan klienta może być technicznie niewykonalny w obecnych ramach API.

- **Twierdzenie o braku gotowego skryptu i konieczności prac dostosowawczych:**  
  Potwierdzone – patrz punkt 3.

- **Twierdzenie o potrzebie weryfikacji po stronie Allegro, czy kategoria kwalifikuje się do wyjątku:**  
  Zasadne – brak jednoznacznej informacji, że „Części samochodowe” są zwolnione z obowiązku powiązania z Katalogiem.

---

### Podsumowanie

| Twierdzenie | Werdykt |
|---|---|
| Wymóg Katalogu od lipca 2024, części samochodowe bez wyjątku | Częściowo potwierdzone (wymóg potwierdzony, brak wyjątku dla części – potwierdzony) |
| Zakaz agregacji danych i zdjęć z OTOMOTO | Potwierdzone |
| Brak gotowego, uniwersalnego skryptu | Potwierdzone |
| Płatny test zamiast bezpłatnej partii próbnej | Sprzeczne z wymaganiem klienta |

Oferta w przeważającej części trafnie identyfikuje ryzyka techniczne i prawne. Jedynym istotnym mankamentem – z punktu widzenia relacji z klientem – jest **zmiana bezpłatnego testu na płatny**, co może zostać odebrane jako ignorowanie kluczowego warunku zlecenia.


=== PROBA 2 ===
SEDZIA: {"status": "VETO", "kara_pkt": -20, "cytat_lub_brak": "Od połowy 2024 ofert nie da się swobodnie edytować bez powiązania z Katalogiem, a kategoria części samochodowych nie figuruje na liście zwolnień publikowanej przez Allegro. Twój plan opiera się na całkowitym wyłączeniu parowania... Proponuję migrację z powiązaniem z Katalogiem tam, gdzie jest wymagane", "uzasadnienie": "Klient wprost i szczegółowo opisał, że jego model publikacji opiera się na CAŁKOWITYM WYŁĄCZENIU parowania z Katalogiem Allegro, bo bez tego system podmienia opisy i ucina galerie zdjęć. Oferta nie tylko punktowo kwestionuje ten element, ale proponuje zmianę całego podejścia na 'migrację z powiązaniem z Katalogiem', czyli dokładnie to, przed czym klient się zabezpieczał. To negowanie kierunku projektu, nie punktowa odmowa. Dodatkowo oferta składa szereg fałszywych/niepotwierdzonych faktów technicznych podanych jako pewnik (np. 'od połowy 2024 ofert nie da się swobodnie edytować bez powiązania z Katalogiem', 'kategoria części samochodowych nie figuruje na liście zwolnień publikowanej przez Allegro'), których nie ma w materiale źródłowym i które mogą być nieprawdziwe. Klient poczuje, że wykonawca nie przyjął jego wymagań, tylko forsuje własną wizję, i dodatkowo straszy regulacjami, których nie potwierdził.", "instrukcja_naprawy": "Usunąć tezę, że Katalog Allegro uniemożliwia publikację szkiców bez parowania oraz że kategoria części samochodowych nie jest zwolniona — to niepotwierdzone twierdzenia. Nie proponować zmiany modelu na 'powiązanie z Katalogiem'. Zachować punktową uwagę: 'Twój sposób obejścia Katalogu przez numer części z tytułu może zadziałać, ale wymaga weryfikacji na 20 szkicach przed głównym importem; jeśli API odrzuci szkice bez powiązania, wrócimy do rozmowy o alternatywie' — bez negowania całego podejścia klienta. Legalność zdjęć i dostęp do API OTOMOTO można zostawić jako pytania weryfikacyjne, ale nie jako zarzut łamania regulaminu postawiony ex cathedra. Termin: zamiast '14 dni realne tylko przy braku blokad' napisać wprost, czy przy założeniach klienta jesteś w stanie zmieścić się w 14 dniach, czy nie — i dlaczego."}

WERYFIKACJA FAKTOW:
Poniżej weryfikacja każdego zakwestionowanego twierdzenia z oferty. Werdykt oparty wyłącznie na dostępnych dowodach.

---

### 1. „Od połowy 2024 ofert nie da się swobodnie edytować bez powiązania z Katalogiem”

**WERDYKT: PRAWDA**

**Dowód:**
- Oficjalna pomoc Allegro: „From June 6, 2024, you cannot edit offers until you link them to the Allegro Product Catalog. If you want to change, for example, the offer title, its parameters, or images — you need to link it to the product from the Catalog first.”
- Komunikat na developer.allegro.pl: „Od czerwca 2024 nie edytujesz ofert, dopóki nie połączysz ich z Katalogiem produktów Allegro. Od 1 lipca 2024 będziemy wymagali, aby wszystkie Twoje oferty były połączone z Katalogiem produktów.”

Twierdzenie oferty jest zgodne z dokumentacją. Nie mówi ono, że nie da się *utworzyć* szkicu bez powiązania, a jedynie że nie da się *edytować* oferty. To jest poprawne.

---

### 2. „Kategoria części samochodowych nie figuruje na liście zwolnień publikowanej przez Allegro”

**WERDYKT: FAŁSZ (nieprecyzyjne / wprowadzające w błąd)**

**Dowód:**
Oficjalna lista kategorii wykluczonych z obowiązku łączenia z Katalogiem zawiera konkretne podkategorie w ramach „Motoryzacja > Części samochodowe”, m.in.:
- „Motoryzacja > Części samochodowe > Układ wydechowy > Tłumiki > Komplety”
- „Motoryzacja > Części samochodowe > Filtry > Zestawy filtrów”
- „Motoryzacja > Części samochodowe > Układ hamulcowy > … > Zestawy (tarcze, klocki, zaciski)”
- „Motoryzacja > Części samochodowe > Części karoserii > Zestawy części blacharskich”

Niektóre podkategorie części samochodowych **są** zwolnione. Twierdzenie, że kategoria części samochodowych „nie figuruje na liście zwolnień”, jest zatem nieprawdziwe w swoim ogólnym brzmieniu.

---

### 3. „Regulamin OTOMOTO wprost zabrania agregowania danych i pobierania materiałów z serwisu w celu udostępniania ich dalej”

**WERDYKT: PRAWDA**

**Dowód:**
Cytat z regulaminu OTOMOTO (obowiązujący co najmniej od 2024 r.):
> „Pobieranie lub wykorzystywanie w jakimkolwiek zakresie dostępnych w ramach Serwisu OTOMOTO materiałów wymaga każdorazowo zgody Grupy OLX i nie może naruszać postanowień Regulaminu […]. Zabronione jest jakiekolwiek agregowanie i przetwarzanie danych oraz innych informacji dostępnych w Serwisie OTOMOTO w celu ich dalszego udostępniania osobom trzecim w ramach innych serwisów internetowych jak i poza Internetem.”

---

### 4. „Pobranie zdjęć wymaga zgody Grupy OLX”

**WERDYKT: PRAWDA**

**Dowód:**
Ten sam cytat z regulaminu OTOMOTO: „Pobieranie lub wykorzystywanie w jakimkolwiek zakresie dostępnych w ramach Serwisu OTOMOTO materiałów wymaga każdorazowo zgody Grupy OLX”. „Materiały” obejmują zdjęcia.

---

### 5. „Rozmycie znaku wodnego to obejście zabezpieczenia, nie źródło praw do zdjęcia”

**WERDYKT: NIEPOTWIERDZONE (ocena prawna, brak bezpośredniego dowodu w materiale źródłowym)**

**Uwaga:**
Można potwierdzić, że OTOMOTO stosuje znaki wodne na zdjęciach – użytkownicy zgłaszają, że „zdjęcia na otomoto mają znak wodny”. Jednak stwierdzenie, że rozmycie takiego znaku jest „obejściem zabezpieczenia” w rozumieniu prawnym, wymagałoby analizy prawnej (np. art. 79 prawa autorskiego, ochrona zabezpieczeń technicznych). W dostarczonym materiale brak jest aktu prawnego lub orzeczenia, które wprost tak kwalifikowałoby rozmycie znaku wodnego OTOMOTO. To pozostaje opinią, nie faktem zweryfikowanym.

---

### 6. „Nie znalazłem gotowego, uniwersalnego skryptu OTOMOTO do Allegro”

**WERDYKT: NIEPOTWIERDZONE (twierdzenie o braku – trudne do dowiedzenia)**

**Uwaga:**
W wyszukiwaniu pojawiają się narzędzia integracyjne (BaseLinker, EasyUploader), które obsługują OTOMOTO i Allegro, ale są to platformy SaaS, a nie „gotowe, uniwersalne skrypty”. Nie można jednak wykluczyć istnienia prywatnych skryptów, które nie są publicznie indeksowane. Brak dowodu na istnienie takiego skryptu nie jest dowodem na jego brak. Twierdzenie pozostaje niepotwierdzone.

---

### 7. „Szkice przez product-offers to standard”

**WERDYKT: PRAWDA (z zastrzeżeniem)**

**Dowód:**
Dokumentacja Allegro REST API:
- `POST /sale/product-offers` – „wystaw ofertę z produktem w jednym requeście”
- `POST /sale/offers` – „dodaj szkic oferty lub edytuj ofertę”

Zatem tworzenie szkiców odbywa się przez `POST /sale/offers`, a nie przez `product-offers`. Stwierdzenie, że „szkice przez product-offers to standard”, jest **nieścisłe** – `product-offers` służy do tworzenia ofert powiązanych z produktem, natomiast surowe szkice tworzy się przez `sale/offers`. Werdykt: **częściowo prawda, ale terminologicznie błędne**.

---

### Podsumowanie werdyktów

| Twierdzenie | Werdykt |
|---|---|
| 1. Brak edycji ofert bez powiązania z Katalogiem od poł. 2024 | **PRAWDA** |
| 2. Kategoria części samochodowych nie figuruje na liście zwolnień | **FAŁSZ** (nieprecyzyjne) |
| 3. Regulamin OTOMOTO zabrania agregowania danych i pobierania materiałów | **PRAWDA** |
| 4. Pobranie zdjęć wymaga zgody Grupy OLX | **PRAWDA** |
| 5. Rozmycie znaku wodnego to obejście zabezpieczenia | **NIEPOTWIERDZONE** |
| 6. Brak gotowego, uniwersalnego skryptu OTOMOTO→Allegro | **NIEPOTWIERDZONE** |
| 7. Szkice przez product-offers to standard | **CZĘŚCIOWO PRAWDA** (błędna terminologia) |

**Wniosek dla autora oferty:** Twierdzenia 1, 3 i 4 są udokumentowane i mogą pozostać. Twierdzenie 2 należy usunąć lub przeformułować – lista zwolnień zawiera wybrane podkategorie części samochodowych. Twierdzenie 5 to opinia, nie fakt – warto oznaczyć jako „wymaga weryfikacji prawnej”. Twierdzenie 6 jest niepotwierdzalne – lepiej napisać „nie znam publicznie dostępnego gotowego skryptu” zamiast twierdzić o jego braku. Twierdzenie 7 wymaga korekty terminologicznej: szkice tworzy się przez `POST /sale/offers`, a nie `product-offers`.
