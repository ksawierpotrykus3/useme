=== PROBA 1 ===
SEDZIA: {"status": "VETO", "kara_pkt": -20, "cytat_lub_brak": "Nie mam w portfolio strony dla firmy marketingowej, którą mógłbym Wam pokazać online. Zamiast linków proponuję krótkie demo... To da Wam lepszy obraz niż cudze realizacje.", "uzasadnienie": "Klient wprost i z naciskiem poprosił: 'portfolio podobnych realizacji' oraz 'Prosimy przede wszystkim o konkretne przykłady zrealizowanych stron, które można zobaczyć online'. Oferta nie tylko nie podaje żadnego linku, ale wprost odrzuca tę prośbę, sugerując, że demo zastąpi portfolio i będzie 'lepsze niż cudze realizacje'. To brzmi jak wymówka i unik, a nie odpowiedź na twarde życzenie klienta. Klient przeglądający ofertę nie ma żadnego dowodu, że wykonawca w ogóle zrobił kiedykolwiek stronę WWW — to realnie zniechęca do odpowiedzi. Dodatkowo widełki 6500–12000 zł netto przy budżecie 'do negocjacji' i przy przyznanym braku portfolio wyglądają na zaniżoną kotwicę cenową bez pokrycia w jakości, co osłabia wiarygodność.", "instrukcja_naprawy": "Zamień akapit o braku portfolio na uczciwą, ale konkretną odpowiedź: podaj 2–3 realne linki do dowolnych zrealizowanych stron (nawet innych branż), które można obejrzeć online, i krótko opisz, co w każdej z nich było wyzwaniem UX/wdrożeniowym. Jeśli naprawdę nie masz żadnych publicznych realizacji, napisz to wprost jednym zdaniem i zaproponuj konkretny, zawężony zakres płatnej próbki lub audytu UX istniejącej koncepcji klienta (np. 'prześlę 1-stronicowy audyt UX Waszych makiet w ciągu 3 dni'), ale NIE zastępuj tym portfolio i nie pisz, że demo 'da lepszy obraz niż cudze realizacje'. Zachowaj trafną merytorykę o WordPress + ACF vs Next.js/Sanity oraz pytania doprecyzowujące zakres — są dobre i pasują do ogłoszenia."}

WERYFIKACJA FAKTOW:
**VERDICT: CZĘŚCIOWO POTWIERDZONE / CZĘŚCIOWO NIEPOTWIERDZONE**

---

## TWARDDZENIE 1: „WordPress z blokami i ACF spełnia dokładnie to, o co pytacie, czyli edycję treści, zdjęć i poszczególnych sekcji bez dotykania kodu.”

**WERDYKT: POTWIERDZONE**

**DOWÓD:**
Oficjalna dokumentacja ACF (Advanced Custom Fields) potwierdza, że ACF Blocks pozwalają na edycję treści bez znajomości kodu: *„Inline Editing is a new feature of ACF Blocks that allows authors to edit block data directly within the block preview area, offering a more native Gutenberg-like experience without extra code”*. Dokumentacja wskazuje również, że edycja inline działa automatycznie dla elementów HTML zawierających wartości pól ACF – *„if you have a paragraph tag with only an ACF field value in it, it will be editable automatically”* – oraz dla atrybutów obrazów: *„if an img tag's src attribute has a value that comes directly from an ACF field, it will automatically be editable”*. Potwierdza to możliwość edycji treści, zdjęć i poszczególnych sekcji bez dotykania kodu.

**DODATKOWY KONTEKST:** ACF Blocks umożliwia tworzenie niestandardowych typów bloków bez potrzeby pisania rozbudowanego kodu JavaScript czy React: *„ACF Blocks is a game-changer for WordPress developers, allowing you to create custom block types without needing extensive JavaScript or React knowledge”*.

---

## TWIERDZENIE 2: „Jest tani w utrzymaniu i łatwo znaleźć wykonawców.”

**WERDYKT: POTWIERDZONE**

**DOWÓD:**
WordPress jest powszechnie uznawany za opłacalne rozwiązanie CMS. Analiza rynku wskazuje, że *„Using open-source CMS like WordPress reduces software cost but requires paying for hosting and customization”*, a typowy koszt zlecenia freelance budowy strony WordPress to 2000–8000 USD. Dodatkowo, *„WordPress remains the most cost-effective solution for 42.8% of the web in 2026”*.

Jeśli chodzi o łatwość znalezienia wykonawców, istnieją dedykowane platformy i rynki pracy dla deweloperów WordPress: *„platform-matched freelance marketplaces like Codeable, Fiverr, or Upwork are great places to hire vetted WordPress specialists for small monthly retainers or quick hourly tasks”*. Dostępne są również wyspecjalizowane giełdy, takie jak Zinn Hub, gdzie *„you can hire verified WordPress developers for theme and plugin work”*.

---

## TWIERDZENIE 3: „Alternatywa to Next.js z Sanity... mniej intuicyjne dla marketingowca.”

**WERDYKT: POTWIERDZONE (z zastrzeżeniem)**

**DOWÓD:**
Porównanie Sanity z WordPress wskazuje, że Sanity wymaga więcej pracy programistycznej: *„Studio is an open-source React application. It's not a product you simply switch on since your developers scaffold it, define the schemas, customize the inputs, deploy it, and maintain it for as long as you use the platform”*. Oznacza to, że Sanity nie jest gotowym produktem „włącz i działa” – wymaga zaangażowania dewelopera do skonfigurowania i utrzymania.

Dodatkowo, analiza doświadczeń edytorów wskazuje, że *„Sanity trades freeform page-builder layout control for structured, validated fields”* – co oznacza, że edytorzy mają mniej swobody w układzie strony niż w tradycyjnych CMS-ach typu WordPress z Gutenberg. Jednakże Sanity Studio oferuje przyjazny interfejs dla edytorów: *„The editor experience is closer to a form than a canvas”*.

**ZASTRZEŻENIE:** Określenie „mniej intuicyjne” jest subiektywne. Sanity może być intuicyjne dla prostych zadań edycyjnych, ale wymaga wsparcia dewelopera przy dodawaniu nowych typów treści lub pól.

---

## TWIERDZENIE 4: „Next.js z Sanity... zwykle droższe.”

**WERDYKT: POTWIERDZONE**

**DOWÓD:**
Porównania kosztów jednoznacznie wskazują, że headless CMS z Next.js jest droższy w początkowym wdrożeniu. Jeden z serwisów podaje: *„Le headless (Next.js + Sanity/Strapi) coute plus cher a l'entree”* (kosztuje więcej na wejściu) – widełki 18 000–45 000 EUR vs tradycyjne WordPress. Inny ranking porównawczy podaje koszt budowy: *„WordPress: £3-8K | Headless CMS (Sanity / Strapi + Next.js): £8-15K”*.

Koszty utrzymania (TCO) są bardziej złożone – Sanity ma subskrypcję SaaS ($15/mies. za projekt), ale WordPress wymaga hostingu i ewentualnego wsparcia. Jednak koszt **początkowego wdrożenia** jest wyraźnie wyższy dla Next.js + Sanity.

---

## TWIERDZENIE 5: „Widełki 6500 do 12000 zł netto [za wykonanie strony].”

**WERDYKT: POTWIERDZONE (mieszczą się w rynkowych widełkach)**

**DOWÓD:**
Polski kalkulator wyceny stron WWW na WordPress z ACF podaje orientacyjne widełki **6000–9000 zł netto** za projekt. Inne źródło wskazuje: *„Strona na WordPressie kosztuje najczęściej od 1 500 do 6 000 zł netto”* dla prostszych realizacji, ale także: *„Standardowa strona firmowa na kilka–kilkanaście podstron z indywidualnym projektem to zwykle 14 000–20 000 zł netto”*.

Widełki 6500–12000 zł netto mieszczą się pomiędzy tymi kategoriami – są powyżej prostych wizytówek, ale poniżej rozbudowanych serwisów korporacyjnych. Przy założeniu, że oferta dotyczy strony firmowej na WordPress z ACF (6–15 podstron, projekt do dopracowania), widełki są **wiarygodne i zgodne z rynkiem**.

---

## TWIERDZENIE 6: „Orientacyjnie 15 do 28 dni roboczych od przekazania materiałów i akceptacji zakresu.”

**WERDYKT: NIEPOTWIERDZONE**

**DOWÓD:**
Nie znaleziono wiarygodnego źródła, które potwierdzałoby konkretny przedział 15–28 dni roboczych dla projektu WordPress z ACF o zakresie opisanym w ogłoszeniu. Czas realizacji zależy od wielu czynników (liczba podstron, gotowość makiet, liczba integracji, tempo feedbacku klienta), więc bez szczegółowych danych projektowych nie można tego zweryfikować.

**UWAGA:** Zgodnie z instrukcją, twierdzenie pozostaje **NIEPOTWIERDZONE** – nie oznacza to, że jest fałszywe, a jedynie, że nie da się go potwierdzić na podstawie dostępnych źródeł.

---

## TWIERDZENIE 7: „Nie mam w portfolio strony dla firmy marketingowej, którą mógłbym Wam pokazać online.”

**WERDYKT: PRZYZNANIE STRONY – NIEWERYFIKOWALNE**

**DOWÓD:**
To jest stwierdzenie o stanie faktycznym, którego nie można zweryfikować za pomocą źródeł zewnętrznych. Można jedynie odnotować, że:
1. Klient **wprost i z naciskiem** poprosił o portfolio i konkretne przykłady online.
2. Oferta **nie zawiera żadnego linku** do realnej realizacji.
3. Autor oferty sam przyznaje, że **nie ma** strony z branży marketingowej do pokazania.

Z perspektywy weryfikacji: jest to **przyznanie braku dowodu**, a nie twierdzenie podlegające weryfikacji faktograficznej.

---

## TWIERDZENIE 8: „Demo da Wam lepszy obraz niż cudze realizacje.”

**WERDYKT: OPINIA SUBIEKTYWNA – NIEWERYFIKOWALNE**

**DOWÓD:**
To jest sąd wartościujący, a nie twierdzenie faktograficzne. Nie istnieje obiektywny miernik, który pozwoliłby potwierdzić lub zaprzeczyć, że „demo da lepszy obraz niż cudze realizacje”. Można jedynie ocenić kontekst: klient **wprost prosił o portfolio**, więc odmowa jego przedstawienia i zastąpienie go demem jest **niezgodna z oczekiwaniem klienta**, ale sama w sobie nie jest „fałszem” – jest wyborem komunikacyjnym.

---

## TWIERDZENIE 9: „Zanim dopnę wycenę, potrzebuję trzech informacji: ile podstron i kluczowych sekcji, czy macie gotowe makiety, czy potrzebne są integracje.”

**WERDYKT: POTWIERDZONE (jako uzasadnione działanie)**

**DOWÓD:**
Potrzeba doprecyzowania zakresu przed podaniem ostatecznej wyceny jest standardową praktyką. Kalkulatory wyceny stron WWW na WordPress z ACF wskazują, że na cenę wpływają: *„Rodzaj: wizytówka/one-page, firmowa czy serwis korporacyjny; Liczba podstron (do 5, 6–15, 15+); Indywidualność projektu graficznego; Wielojęzyczność i strefa klienta z logowaniem; Integracje z CRM / newsletterem”*. Pytania zadane przez autora oferty są **merytorycznie trafne** i bezpośrednio dotyczą czynników wpływających na wycenę.

---

## PODSUMOWANIE

| # | Twierdzenie | Werdykt |
|---|-------------|---------|
| 1 | WordPress + ACF umożliwia edycję bez kodu | **POTWIERDZONE** |
| 2 | WordPress tani w utrzymaniu, łatwo znaleźć wykonawców | **POTWIERDZONE** |
| 3 | Next.js + Sanity mniej intuicyjne dla marketingowca | **POTWIERDZONE** (z zastrzeżeniem) |
| 4 | Next.js + Sanity droższe | **POTWIERDZONE** |
| 5 | Widełki 6500–12000 zł netto | **POTWIERDZONE** (w rynkowych widełkach) |
| 6 | Czas realizacji 15–28 dni roboczych | **NIEPOTWIERDZONE** |
| 7 | Brak portfolio do pokazania online | **PRZYZNANIE – nieweryfikowalne** |
| 8 | „Demo da lepszy obraz niż cudze realizacje” | **OPINIA – nieweryfikowalne** |
| 9 | Potrzeba 3 informacji przed wyceną | **POTWIERDZONE** (uzasadnione) |

**Kluczowy wniosek:** Merytoryczna część oferty (technologia, uzasadnienie wyboru, widełki cenowe) jest **rzetelna i potwierdzona w źródłach**. Głównym problemem jest **brak odpowiedzi na wprost wyrażoną prośbę klienta o portfolio** oraz **zastąpienie go subiektywną opinią o demie** – co nie jest kłamstwem, ale jest **unikiem komunikacyjnym**, który realnie osłabia wiarygodność oferty.
