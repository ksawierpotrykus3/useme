```
KWALIFIKOWALNOSC: TAK, ale z poważnym zastrzeżeniem — projekt może być technicznie niewykonalny w zakresie, w jakim klient go opisał (szkice bez Katalogu Allegro w kategorii części samochodowych), a bezpłatna partia 20 sztuk przed umową to sygnał ryzyka wyłudzenia pracy. Nie skreśla zlecenia, ale wymaga nazwania problemów i zaproponowania alternatyw.

TYP_ZLECENIA: projekt jednorazowy z elementem testu (bezpłatna partia 20 sztuk przed umową) — mieszanka wykonawczego i doradczego (klient ma gotową wizję, ale wizja zawiera błędy).

INTENCJA: wykonawcze z konieczną korektą założeń (doradcze wchodzi jako mina, nie jako sprzedaż wiedzy).

DECYDENT_I_BOL: firma sprzedająca części samochodowe, przenosząca 5952 ofert z OTOMOTO na Allegro. Ból — masowa migracja bez ręcznej pracy, bez utraty jakości, bez blokad katalogowych. Decydent prawdopodobnie właściciel/właścicielka sklepu. Brak przesłanek, że to pośrednik.

WYKONALNE: CZĘŚCIOWO. Najbliższa wykonalna opcja: migracja jako szkice z POWIĄZANIEM z Katalogiem Allegro (tam, gdzie to wymagane) albo w kategoriach, które są wyłączone z obowiązku katalogowego. Bez tego — ryzyko, że szkice zostaną zablokowane lub oferty nie przejdą.

POLE_DO_POPISU: JEST — trzy obszary, z czego jeden (Katalog Allegro) może być blokadą projektu, a nie drobnym zastrzeżeniem. To wymaga spokojnego, rzeczowego przedstawienia z alternatywą.

SCIEZKA_MERYTORYKI: B (miny) — wszystkie z dowodem ze zlecenia lub z researchu.

MINY_I_CIEKAWOSTKI:

1. **Szkice bez Katalogu Allegro — najpoważniejsza.** Dowód: klient WPROST pisze „całkowite WYŁĄCZENIE automatycznego parowania i wyszukiwania produktów z Katalogu Allegro". Research potwierdza: od lipca 2024 Allegro wymaga powiązania wszystkich ofert z Katalogiem, z wyjątkami, które nie obejmują części samochodowych. Mechanizm awarii: szkice bez powiązania mogą zostać odrzucone przez API lub zablokowane po utworzeniu. Konsekwencja: 5952 szkiców do wyrzucenia, praca do powtórzenia, termin 14 dni nie do utrzymania. Alternatywa: migracja z powiązaniem z Katalogiem tam, gdzie to wymagane, albo weryfikacja, czy kategoria części samochodowych kwalifikuje się do wyjątku — to wymaga sprawdzenia po stronie Allegro.

2. **Pobranie danych i zdjęć z OTOMOTO — ryzyko regulaminowe.** Dowód: klient pisze „pobraniu danych z OTOMOTO" i „lokalne repozytorium zdjęć", ale nie precyzuje, skąd zdjęcia pochodzą. Research potwierdza: regulamin OTOMOTO zakazuje agregowania i przetwarzania danych w celu udostępniania na innych serwisach; pobieranie materiałów wymaga zgody Grupy OLX. Mechanizm awarii: jeśli dane i zdjęcia są pobierane z OTOMOTO bez zgody, cała migracja opiera się na naruszeniu regulaminu. Konsekwencja: roszczenia, usunięcie ofert, blokada konta. Alternatywa: użycie oryginalnych zdjęć klienta (jeśli je ma) albo zdjęć z własnego źródła; dane pobrane przez API dealerskie OTOMOTO (jeśli klient ma do niego dostęp) — ale nawet wtedy regulamin może ograniczać eksport na inne serwisy.

3. **„Gotowy, działający skrypt" — korekta oczekiwań, nie mina.** Dowód: klient pisze „Szukam profesjonalisty z gotowym, działającym skryptem". Nie istnieje uniwersalny skrypt OTOMOTO→Allegro dla 5952 ofert — to zawsze praca dostosowawcza (mapowanie kategorii, parametrów, katalogu, obsługa wyjątków). To nie mina, ale warto zaznaczyć, że oferujemy dostosowanie, nie „gotowca".

ODMOWA:

- **Obiekt:** całkowite wyłączenie parowania z Katalogiem Allegro przy 5952 ofertach w kategorii części samochodowych.
- **Typ:** 2 (twardy limit zewnętrzny — wymóg Allegro od lipca 2024).
- **Mechanizm awarii:** API Allegro może odrzucić szkice bez powiązania z Katalogiem albo zablokować je po utworzeniu; kategoria części samochodowych nie jest objęta wyjątkami.
- **Konsekwencja:** 5952 szkiców do wyrzucenia, praca do powtórzenia, termin 14 dni nie do utrzymania, strata czasu i pieniędzy.
- **Alternatywa:** migracja z powiązaniem z Katalogiem tam, gdzie to wymagane; weryfikacja po stronie Allegro, czy kategoria kwalifikuje się do wyjątku; jeśli nie — dostosowanie procesu do wymogów Allegro.

- **Obiekt:** programowe rozmycie znaku wodnego OTOMOTO.
- **Typ:** 4 (zgodność i regulacje).
- **Mechanizm awarii:** znak wodny to oznaczenie chronione; jego celowe usunięcie w celu użycia zdjęć na innej platformie może być traktowane jako obejście zabezpieczenia i naruszenie regulaminu OTOMOTO oraz praw do znaku.
- **Konsekwencja:** roszczenia OTOMOTO, blokada konta, usunięcie ofert na Allegro.
- **Alternatywa:** użycie oryginalnych zdjęć bez znaku wodnego (z zasobu klienta) albo zdjęć z własnego źródła; obróbka kadru bez neutralizacji cudzych oznaczeń.

PYTANIA:

1. Czy masz dostęp do API OTOMOTO (dealerskie/partnerskie) do pobrania własnych ogłoszeń, czy dane trzeba pozyskać inaczej? — pytam, bo od tego zależy metoda pobrania, legalność i czas; bez tego nie da się wycenić.

2. Czy masz konto firmowe Allegro z aktywnym dostępem do REST API i uprawnieniami do tworzenia szkiców ofert? — pytam, bo od tego zależy możliwość realizacji „bezpiecznych szkiców".

3. Czy 5952 ogłoszeń jest w jednej kategorii na OTOMOTO (części samochodowe), czy w kilku? — pytam, bo od tego zależy mapowanie kategorii i parametrów na Allegro, a co za tym idzie zakres prac i ryzyko katalogowe.

4. Czy zdjęcia w lokalnym repozytorium są Twoją własnością (bez znaku wodnego OTOMOTO), czy pochodzą z OTOMOTO? — pytam, bo od tego zależy, czy w ogóle można ich legalnie użyć na Allegro; jeśli są z OTOMOTO, blur znaku wodnego nie rozwiązuje problemu prawnego.

CO_ZLECENIE_MOWI: 5952 ofert części samochodowych; OTOMOTO → Allegro (konto firmowe); szkice robocze; wyłączenie automatycznego parowania z Katalogiem Allegro; numer części z początku tytułu (Marka + Model); mapowanie stanu Nowy/Używany; pełne opisy, parametry, ceny; blur lewego dolnego narożnika na zdjęciach z lokalnego repozytorium; raport końcowy; bezpłatna partia 20 sztuk przed umową; termin 14 dni; wymagane udokumentowane doświadczenie w API Allegro; wzór oferty ID 18907450972.

CZEGO_NIE_MOWI: skąd dokładnie dane z OTOMOTO (API czy scraping); czy klient ma uprawnienia API Allegro; czy wszystkie ogłoszenia są w jednej kategorii; czy zdjęcia są własnością klienta; czy 20 sztuk próbnych jest płatne; jaki jest budżet poza „do negocjacji".

GRANICA_CIECIA: krótko — trzy miny z dowodem (Katalog Allegro, pobranie danych/zdjęć, korekta „gotowego skryptu"), cztery pytania wycenowe/wykrywacze, bez rozwijania merytoryki ponad to, co klient napisał. Żadnych założeń o API OTOMOTO ani o prawach do zdjęć poza tym, co wprost w ogłoszeniu. Research użyty do wzmocnienia min, nie do budowania oferty.

RESEARCH_POTRZEBNY: TAK — ale już zrobiony. Teraz trzeba go użyć w ofercie: (1) potwierdzić w API Allegro, czy szkice bez Katalogu w kategorii części samochodowych są możliwe; (2) potwierdzić, czy OTOMOTO API pozwala na eksport własnych ogłoszeń i na jakich warunkach; (3) potwierdzić regulamin OTOMOTO w zakresie pobierania danych i zdjęć.

DECYZJE:

**DOPISAĆ do oferty:**
- Mina o Katalogu Allegro — najważniejsza, z dowodem i alternatywą. Spokojnie: „Od lipca 2024 Allegro wymaga powiązania ofert z Katalogiem; w kategorii części samochodowych wyjątki nie obejmują. Proponuję migrację z powiązaniem tam, gdzie to wymagane, albo weryfikację po stronie Allegro."
- Mina o pobraniu danych i zdjęć z OTOMOTO — z dowodem i alternatywą. Spokojnie: „Regulamin OTOMOTO zakazuje agregowania danych i pobierania materiałów bez zgody. Jeśli zdjęcia pochodzą z OTOMOTO, blur znaku wodnego nie rozwiązuje problemu prawnego. Proponuję użycie oryginalnych zdjęć klienta albo zdjęć z własnego źródła."
- Korekta „gotowego skryptu" — krótko: „Nie ma uniwersalnego skryptu OTOMOTO→Allegro dla 5952 ofert; to praca dostosowawcza. Oferuję dostosowanie, nie gotowca."

**ODPOWIEDZIEĆ:**
- Na pytania klienta (API Allegro, konto firmowe) — jeśli klient ich nie zadał w ogłoszeniu, nie odpowiadamy. W ofercie tylko potwierdzamy, że mamy doświadczenie w API Allegro i możemy realizować szkice.

**DOPYTAĆ:**
- 4 pytania z sekcji PYTANIA — wysłać w ofercie jako pytania wycenowe/wykrywacze, każde z uzasadnieniem. Bez pytania o bezpłatną partię 20 sztuk — klient już to określił, to nie jest pytanie, to fakt.
```