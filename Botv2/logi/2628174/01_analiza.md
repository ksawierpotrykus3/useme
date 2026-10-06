KWALIFIKOWALNOSC: TAK

TYP_ZLECENIA: mieszane — doradcze (zaprojektowanie drzewa kategorii wspólnie z klientem) + wykonawcze (przypisanie produktów, normalizacja atrybutu rozmiar). Jednorazowe, z realnym ciężarem strategicznym na początku.

INTENCJA: mieszane — klient sam nazywa obie części: „skonsultuje ze mną i zaproponuje nowe drzewo" (doradcze), „przypisze produkty do kategorii" (wykonawcze).

DECYDENT_I_BOL: Właściciel sklepu, techniczny — ma własną wtyczkę do masowego przypisywania, więc nie jest laikiem i zweryfikuje każdą tezę. Ból pod spodem: przy 75 000 produktów drzewo kategorii przestaje być kwestią estetyki, a staje się warstwą wyszukiwania, filtrów i feedów. Niespójny atrybut rozmiar (jako wariant!) psuje konwersję i porównywarkę. Klientowi brakuje nie rąk, a planu — sam to mówi: „porządnie to zaplanuje i ustawi".

WYKONALNE: TAK — ale nie w wersji „ręcznie 75k produktów". Realny plan: (1) wspólny projekt drzewa, (2) reguły przypisania, (3) automatyzacja przez jego wtyczkę + skrypt, (4) normalizacja rozmiaru jako konsolidacja terminów, nie tylko etykiet. „Przypiszę 75k produktów" musi znaczyć „ustawię reguły i przeprowadzę migrację", nie „kliknę 75k razy".

POLE_DO_POPISU: JEST

SCIEZKA_MERYTORYKI: B (mina) + C (lepsza droga niż obrał klient)

MINY_I_CIEKAWOSTKI:
- **Mina (dowód: lista formatów od klienta):** „39,5 EUR" w termach sugeruje dane z feedu dostawcy. Poprawa samego wyświetlania nie wystarczy — WooCommerce dopasowuje warianty po terminach atrybutu, nie po etykiecie. Trzeba skonsolidować terminy, nie przemalować labelki. Inaczej nadal będą „dwa rozmiary 39,5".
- **Mina (dowód: „rozmiar jest kluczowy i wyświetla się jako wariant"):** jedna uniwersalna mapa rozjedzie się, jeśli w sklepie są jednocześnie obuwie (39,5), odzież (S/M/L) i np. rozmiary dziecięce. „39,5" znaczy co innego w każdej z tych rodzin.
- **Mina (dowód: 75 000 produktów + autorska wtyczka):** przy takiej skali taksonomia i tabela term relationships to decyzja architektoniczna, nie kosmetyczna. Bez reguł (rule-based / mapowanie / AI-assisted) nie da się tego zrobić w budżecie — i żadna wtyczka tego nie „domyśli".
- **Ciekawostka (dowód: „moją autorską wtyczką, jednak nie są to doskonałe narzędzia"):** klient ma narzędzie, ale nie ma procesu. Wartość nie leży w kodzie wtyczki, a w regułach, którymi ją zasilimy.

ODMOWA: puste. Nie ma tu miny „nie da się" — jest konflikt zakresu wobec budżetu (500 PLN na zaprojektowanie drzewa + migrację 75k + normalizację wariantów to trzy prace, nie jedna). To nie odmowa, to zakres do ustalenia w ofercie.

PYTANIA:
1. Czy rozmiar jest u Was jednym globalnym atrybutem (np. pa_rozmiar) na wszystkich produktach, czy osobnym per typ produktu? — pytam, bo od tego zależy, czy wystarczy jedna mapa normalizacji, czy trzeba kilku niezależnych.
2. Czy rozmiar występuje tylko na obuwiu, czy też na odzieży / produktach dziecięcych / w systemach US-UK? — pytam, bo od tego zależy skala i ryzyko kolizji (39,5 vs 39,5 EUR vs 6.5 US).
3. Skąd pochodzą dane produktów — feed dostawcy, import, ręcznie? — pytam, bo od tego zależy, czy czyścimy rozmiar u źródła (i problem nie wróci), czy post factum po bazie (i wróci przy następnym imporcie).

(Świadomie nie pytam o: technologię — to nasza propozycja; budżet — nie nasza sprawa; SEO URL-i kategorii — zakładam, że stare adresy mają wartość i zaproponuję przekierowania, dostroję jeśli powie inaczej.)

CO_ZLECENIE_MOWI:
- Platforma: WooCommerce, szablon własny (jest).
- Skala: ~75 000 produktów.
- Narzędzia: autorska wtyczka klienta do masowego przypisywania (auto + ręcznie), oceniana przez klienta jako niedoskonała.
- Rozmiar: atrybut globalny, wyświetlany jako wariant produktu; formaty niespójne: „39,5", „39 1/2", „39-1-2", „39,5 EUR".
- Cel rozmiaru: wszędzie jednolicie „39,5".
- Zakres: konsultacja drzewa kategorii → przypisanie produktów → uporządkowanie rozmiaru.
- Budżet: 500 PLN.

CZEGO_NIE_MOWI:
- Czy rozmiar jest globalny, czy per produkt.
- Jakie typy produktów mają rozmiar (obuwie vs odzież vs dzieci).
- Skąd pochodzą dane (feed, import, ręcznie).
- Ile jest aktualnie kategorii i jak głębokie.
- Jak działa jego wtyczka (API, mechanizm przypisania).
- Czy istnieją historyczne warianty/zamówienia do zachowania.
- Czy stare URL-e kategorii mają wartość SEO.

GRANICA_CIECIA:
Ogłoszenie jest treściwe (klient techniczny, opisał system, narzędzie, konkretne formaty) — stać nas na merytorykę, ale budżet 500 PLN wymusza wąską ofertę. Struktura: 2–3 miny z dowodem, 3 pytania, jasno określone, co 500 PLN pokrywa (projekt drzewa + reguły normalizacji + przeprowadzenie na próbce), i widełki na etap masowy po zobaczeniu danych. Nie rozwlekać, nie straszyć, nie pchać merytoryki ponad dowody.

RESEARCH_POTRZEBNY: TAK — wąsko: (1) potwierdzić mechanizm, po którym WooCommerce dopasowuje warianty do termów (żeby mina o konsolidacji terminów nie była tezą bez dowodu), (2) sprawdzić praktyczne zachowanie taksonomii przy 75k produktów (limity, sens indeksów, wpływ na strony kategorii). Po to, żeby dawać tezę, nie domysł.