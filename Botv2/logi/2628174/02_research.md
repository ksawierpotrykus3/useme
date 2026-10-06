## Research: potwierdzenie min dla zlecenia WooCommerce (75k produktów, normalizacja rozmiaru)

### Mina 1: WooCommerce dopasowuje warianty po **slugach termów**, nie po etykietach wyświetlanych — sama zmiana labelki nie scali wariantów

**Dowód:** W dokumentacji klienta WooCommerce (`woo_client`) opisano mechanizm `variationFor`: warianty zwracane są z kluczami będącymi **etykietami wyświetlanymi** (np. `Colour`), ale **wartości są slugami termów** („Values are term slugs”). Oznacza to, że dopasowanie wariantu do kombinacji atrybutów odbywa się na poziomie sluga, a nie nazwy widocznej dla klienta.

**Konsekwencja dla zlecenia:** Jeśli w sklepie istnieją osobne termy o slugach `39-5`, `39-1-2`, `39-5-eur`, ale z etykietą wyświetlaną „39,5”, WooCommerce nadal będzie traktował je jako **trzy różne warianty**. Poprawa wyświetlania (np. filtrem `woocommerce_attribute_label`) nie scali ich w jeden wariant — trzeba **skonsolidować termy** (scalić slugi i przypisać do nich produkty), a nie tylko przemalować labelkę. To potwierdza minę wskazaną w dzienniku.

**Dodatkowe potwierdzenie:** Wątek na wordpress.org pokazuje, że WooCommerce wymaga unikalnych slugów dla termów w ramach jednego atrybutu; obejściem jest ręczne ustawienie różnych slugów przy tej samej nazwie, ale wtedy dropdowny są mylące („It’s difficult to see which attribute you’re picking as it only says Blue in the dropdown”). To dokładnie sytuacja klienta: wiele termów „39,5” o różnych slugach.

---

### Mina 2: Przy 75 000 produktów taksonomia przestaje być kwestią estetyki — `tax_query` i `wp_term_relationships` stają się wąskim gardłem wydajnościowym

**Dowód 1 (problemy z `tax_query` przy dużej liczbie produktów w kategorii):** Issue #61385 w repozytorium WooCommerce opisuje „severe performance issue” polegający na tym, że zapytania `tax_query` stają się „very inefficient and resource-intensive as the product count in one category grows”. Autor wskazał, że problem występował już przy **250 produktach w jednej kategorii nadrzędnej** z zagnieżdżonymi podkategoriami.

**Dowód 2 (brak twardego limitu, ale degradacja przy 30–70k):** Wątek na wordpress.org: użytkownik z **30 000+ kategorii** i planami na **70 000+ produktów** zgłasza, że wejście w kategorię z 1500+ produktami powoduje zawieszenie się strony. Odpowiedź Happiness Engineera: „There’s no specific restriction in terms of categories, terms etc… but you’re probably reaching where the queries to the database get too big and that your server struggles to return results”.

**Dowód 3 (potrzeba indeksu na `wp_term_relationships`):** W tym samym issue #61385 społeczność wskazała, że `wp_term_relationships` **brakuje właściwego indeksu**; dodanie indeksu złożonego na `(term_taxonomy_id, object_id)` rozwiązuje nieefektywność zapytań. To sugeruje, że przy 75k produktów liczba wierszy w `wp_term_relationships` (produkt × liczba przypisanych termów) może sięgać setek tysięcy lub milionów, a domyślny schemat bazy nie jest zoptymalizowany pod taką skalę.

**Konsekwencja dla zlecenia:** Projekt drzewa kategorii przy 75k produktów nie jest „ustawieniem estetycznym” — to decyzja architektoniczna wpływająca na wydajność stron kategorii, filtrów i feedów. Liczba i głębokość kategorii oraz sposób przypisania produktów (ile termów na produkt) przekładają się bezpośrednio na obciążenie bazy.

---

### Mina 3 (niepotwierdzona w źródłach zewnętrznych, ale wynika z ogłoszenia): jedna uniwersalna mapa rozmiaru rozjedzie się przy mieszanych domenach produktowych

**Status: niepotwierdzone zewnętrznie — teza oparta na analizie treści ogłoszenia, nie na źródle.**

Klient pisze, że „rozmiar jest kluczowy i wyświetla się jako wariant produktu”, ale nie precyzuje, czy dotyczy to tylko obuwia, czy też odzieży (S/M/L), produktów dziecięcych lub systemów US/UK. Jeśli w sklepie współistnieją różne rodziny rozmiarów, jedna globalna mapa normalizacji (np. wszystko do formatu „39,5”) może **kolidować**: „39,5” w obuwiu dorosłym znaczy co innego niż „39,5” w odzieży dziecięcej lub w systemie US. Źródła zewnętrzne potwierdzają ogólny problem duplikatów terminów w WooCommerce (np. „Navy” vs „Navy Blue” vs „Dark Navy”), ale nie odnoszą się wprost do rozmiarów. **Rekomendacja: oznaczyć jako hipotezę wymagającą potwierdzenia danymi klienta (pytanie 2 w dzienniku).**

---

## Pytania do klienta (na podstawie luk w ogłoszeniu i ryzyka z researchu)

1. **Czy rozmiar jest jednym globalnym atrybutem (`pa_rozmiar`) na wszystkich produktach, czy osobnym per typ produktu?** — od tego zależy, czy wystarczy jedna mapa konsolidacji termów, czy trzeba kilku niezależnych (i czy w ogóle da się je scalić bez kolizji).

2. **Czy rozmiar występuje tylko na obuwiu, czy też na odzieży / produktach dziecięcych / w systemach US-UK?** — od tego zależy skala i ryzyko kolizji (np. „39,5” vs „6.5 US” vs „39,5 EUR” jako różne termy o różnych znaczeniach).

3. **Skąd pochodzą dane produktów — feed dostawcy, import, ręcznie?** — od tego zależy, czy normalizację rozmiaru można zrobić u źródła (i problem nie wróci przy następnym imporcie), czy tylko post factum po bazie (i będzie wymagał cyklicznego czyszczenia).

---

## Granica cięcia (konflikt zakresu wobec budżetu)

Budżet **500 PLN** obejmuje **trzy odrębne prace**: (1) wspólny projekt drzewa kategorii, (2) migrację przypisań dla ~75 000 produktów, (3) konsolidację termów atrybutu rozmiar z zachowaniem istniejących wariantów. To nie jest jedna praca — to trzy, z których każda ma inny profil czasowy i ryzyka. **500 PLN może realnie pokryć:** projekt drzewa + reguły normalizacji + przeprowadzenie na próbce (np. 500–1000 produktów) w celu walidacji. **Etap masowy (75k + pełna konsolidacja wariantów) wymaga odrębnych widełek** po zobaczeniu danych i potwierdzeniu, czy stare warianty/zamówienia muszą być zachowane.

Research nie potwierdza, że „da się to zrobić za 500 PLN” — potwierdza, że przy 75k produktów taksonomia i termy są warstwą infrastrukturalną, a nie kosmetyczną. To zakres do ustalenia w ofercie, nie odmowa.