# GRANICE TEORII — dla jakich zleceń zasady NIE przechodzą

> Źródło: analiza 4 rozmów (oferta1-4.md) + bazy ~180 zleceń (01_ofertowarka).
> Data: 2026-10-04. Status: materiał do decyzji, nie reguła.

## Wniosek główny

Teoria zbudowana na 4 zleceniach (145098 Wojciech, 145383 websystems, 145012 Tomasz Kaza,
145337 Makler) jest spójna, ale działa TYLKO na jednym typie rynku:

**zlecenie projektowe z deliverable, z klientem opisującym problem, z budżetem do negocjacji.**

To pokrywa ok. 80% rynku. Pozostałe ~17-20% (~30 zleceń z 180) wymaga dodatków.

## Sześć kategorii, gdzie teoria się wyłamuje

### Kategoria 1: Klient SAM prosi o portfolio/referencje (11 zleceń)
Teoria mówi „nigdy portfolio". Klient wprost tego wymaga jako warunku zgłoszenia.
To nie styl, to twardy filtr formalny.

- 143996 | audyt lejka Shopify + Meta Ads | BO: „prześlij link do portfolio lub opisz podobny problem... Nie interesują mnie generowane automatycznie raporty PDF"
- 143921 | strona + konfigurator domów | BO: „Proszę o przesłanie portfolio, przykładowych realizacji, technologii"
- 144106 | strona www | BO: „osoby z doświadczeniem, najlepiej z portfolio"
- 143994 | Google Ads psychoterapia | BO: „Twoje portfolio lub krótkie opisy projektów z branży medycznej"
- 144210 | migracja sklepu z Shoper | BO: „portfolio i przykładów wykonanych migracji"
- 145198 | WordPress 2.0 + WooCommerce | BO: „Oferta powinna zawierać portfolio... case study"
- 145263 | strona kursów fotograficznych | BO: „Proszę o podanie portfolio"
- 145158 | automatyzacja procesów | BO: „Portfolio i doświadczenie są konieczne"
- 145289 | ArenaDesk | BO: „Apply with... multi-tenant/workflow examples"
- 145333 | automatyzacja medialna | BO: „portfolio lub stronę"
- 145337 | Makler | BO: „Linki do portfolio z podobnymi realizacjami"

Wzorzec dobrej odpowiedzi (z 145333): uczciwe „nie prowadzimy publicznego portfolio,
proponuję test na Twoich danych".

### Kategoria 2: Rekrutacja / stała współpraca / etat / retainer (8 zleceń)
Teoria zakłada jednorazowe zlecenie z deliverable + wycena ryczałtowa. Tu jest stawka i dostępność.

- 145381 | stała opieka IT | BO: „stała opieka techniczna, rozliczenie czasu pracy, przejęcie dostępów"
- 145297 | WordPress Developer | BO: „stała współpraca, min 20h/tyg", budżet 50 zł
- 145166 | Junior-Mid Software Engineer | BO: „CV, short video intro, C1 English", 1200 EUR
- 145270 | wsparcie techniczne stron | BO: „rozliczenie godzinowe, stawka godzinowa, czas reakcji"
- 145182 | Dynamics 365 BC | BO: „stała współpraca, stawka godzinowa, dostępność"
- 144199 | US based Senior Dev | BO: „US-native, long-term collaboration, joins client meetings"
- 144644 | React Native | BO: „Jaka stawka godzinowa? Ile godzin tygodniowo?"
- 145158 | automatyzacja | BO: „współpraca projektowa + serwis, stała współpraca" (VETO -28 pkt za narzucenie modelu miesięcznego)

### Kategoria 3: Ogólne, bez treści do wyceny (4 zlecenia)
Nie ma nawet punktu zaczepienia na pytanie o zakres.

- 145322 | Makoinstal + Subiekt Nexo | BO: całe ogłoszenie to jedno zdanie, zero zakresu
- 144106 | strona www | BO: „Szczegóły zlecenia do ustalenia po kontakcie"
- 145263 | kursy fotograficzne | BO: 3 linijki, zero zakresu
- 145247 | strona korporacyjna PTX | BO: klient ma już POC i kierunek, brak o co pytać

### Kategoria 4: Sprzeczne reguły (4 zlecenia)
- 145182 | stawka godzinowa wymuszona (teoria: tylko 90 zł/h)
- 145234 | test penetracyjny | BO: wymóg niezależności od 16IT, budżet 15853,67 PLN
- 145372 | CI/CD GitHub→VPS | BO: twardy deadline 24h (teoria: dni 7)
- 145337 | Makler | BO: anty-sniping wymagany, bot samowolnie zmienił wymóg

### Kategoria 5: Budżet jawny/skrajny (6 zleceń)
Widełki nie mają sensu, gdy budżet jest już ustalony albo to budżet-etat.

- 145297 | 50 PLN (placeholder przy rekrutacji)
- 143891 | .NET | 2000 USD
- 145234 | test pentest | 15853,67 PLN (z groszami)
- 145289 | ArenaDesk | 6000 USD (stawka, nie kwota projektu)
- 145166 | 1200 EUR (etat)
- 145337 | Makler | 50000 PLN vs wycena bota 28000 (niedoszacowanie)

### Kategoria 6: Scam / patologia (1 zlecenie)
- 144010 | „chatting na stronie" | BO: „znajomość relacji damsko-męskich", info na priv. Romance scam.

## Cztery twarde granice teorii

1. **Granica portfolio.** ~11/180 (6%) klientów wymaga portfolio jako warunku. Teoria potrzebuje
   wyjątku: „jeśli klient wprost prosi o portfolio, to element obowiązkowy" + szablon uczciwej odpowiedzi.

2. **Granica modelu współpracy.** ~8/180 (4,5%) to retainer/etat/stała współpraca. Teoria potrzebuje
   osobnego trybu „umowa o współpracę" zamiast „oferta + kwota + dni".

3. **Granica pola do popisu.** Przy zleceniach 1-2 zdaniowych (145322, 145263, 145247) detektor
   zwraca „brak" i teoria nie ma co dalej zrobić. Brakuje reguły „tryb czystego dopytania o zakres".

4. **Granica stawek i formatów.** Przy budżetach jawnych (50k PLN, 6000 USD, 15853,67 PLN) i wymogach
   formalnych (niezależność, deadline 24h, US-native, video intro) teoria nie wykrywa „to nie jest zwykłe
   zlecenie". Potrzebny detektor typu zlecenia uruchamiany PRZED detektorem pola do popisu.

5. **Granica bezpieczeństwa.** Teoria nie ma detektora scamów. 144010 odrzucone dopiero przez
   zewnętrzny selekcja_powod. Luka: teoria opisuje jak pisać, ale nie kiedy w ogóle nie pisać.

## Wniosek dla łańcucha

Przed całym łańcuchem potrzebny **detektor typu zlecenia** (projekt / retainer / rekrutacja /
audyt / ogólne / scam). Od typu zależy tryb odpowiedzi. Bez tego teoria obsłuży tylko ~80% rynku.