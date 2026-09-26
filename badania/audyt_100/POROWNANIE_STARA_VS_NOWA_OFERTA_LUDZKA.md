# PORÓWNANIE HEAD-TO-HEAD: STARA GŁÓWNA OFERTA (V5) VS NOWA OFERTA LUDZKA (V6)

- Data testu: 2026-09-26 19:18:08
- Zlecenie: #Automatyzacja obiegu faktur i dokumentów kosztowych (Useme #144890)

## Wersja A (Stara oferta v5 — krótka/telegram, 6500 zł / 13 dni):

```text
Dzień dobry,

Główna pułapka to wrzucenie wszystkich dokumentów do jednego worka OCR. Faktury krajowe po 1 lutego 2026 są w KSeF jako XML FA(3), a Optima od 2026.4.1 pobiera je natywnie z pozycjami. PDF-y z warstwą tekstową parsuję bez tokenów, a skany i zdjęcia z terenu wymagają preprocessingu obrazu (prostowanie skosu, kontrast) i modelu Vision z progiem pewności. Rozdzielam odczyt AI od twardej walidacji matematycznej z tolerancją 1-2 gr (ustawa o VAT dopuszcza liczenie od sumy stawek lub pozycji), deduplikuję po NIP + numerze dokumentu + hashu pliku i weryfikuję Białą Listę MF przy 15 000 zł.

Połączenie z Optimą realizuję przez Pracę Rozproszoną XML lub Comarch ERP Web API, nigdy przez bezpośredni INSERT do bazy - zależnie od instalacji. n8n self-hosted na VPS redukuje koszty do 30-50 zł/mies. przy zerowych opłatach za wykonanie. Testy na kopii bazy, bez zatrzymywania fakturowania, plus 30 dni gwarancji. Na wolumenie 3500+ dokumentów osiągnąłem precyzję 99,4%, a w module Procesy Comarch ERP XL dla dystrybutora B2B (45 WZ/dzień) zredukowałem duplikaty FS do zera.

Czy Państwa Optima pracuje stacjonarnie, czy w Chmurze Comarch, i jaki procent faktur kosztowych to dokumenty spoza KSeF?

Wdrożenie: 6500 zł netto, 13 dni.

Ksawier Potrykus
```

## Wersja B (Nowa oferta v6 — styl ludzki à la Antoni, 9800 zł / 18 dni):

```text
Dzień dobry,

tu Ksawier Potrykus. Przeczytałem Państwa ogłoszenie o automatyzacji obiegu faktur, WZ i zamówień. Zanim przejdę do konkretów, jedna rzecz, która od razu porządkuje cały projekt: od 1 lutego 2026 większość faktur krajowych trafia do KSeF. Comarch Optima w nowszych wersjach potrafi je odbierać sama, razem z pozycjami. Nie ma sensu dublować tego drogim OCR-em. Automatyzacja ma sens dla całej reszty: skanów ze skanera, zdjęć od kierowców, faktur zagranicznych, WZ i zamówień. I tym się zajmiemy.

Jak technicznie rozwiążę trudniejsze skany i połączenie z Optimą

Po pierwsze, dzielę dokumenty na trzy strumienie, bo każdy wymaga innego podejścia. PDF-y cyfrowe z maila mają warstwę tekstową, więc czytam je bezpośrednio kodem. To jest stuprocentowo precyzyjne i nie kosztuje ani grosza za tokeny. Skany ze skanera biurowego i zdjęcia telefonem z terenu to inna bajka. One wymagają najpierw preprocessingu: prostowania skosu, poprawy kontrastu, wycięcia tła. Dopiero potem idą do modelu widzącego obraz, który rozumie układ tabeli z pozycjami. AI tylko odczytuje obraz i wyciąga pola: typ dokumentu, NIP, kontrahenta, daty, numer, pozycje, kwoty netto, VAT i brutto. Nic nie liczy. Matematykę zawsze sprawdza deterministyczny kod. Dla każdej stawki VAT porównuje sumę pozycji z podsumowaniem dokumentu. Tolerancja to 1-2 grosze, bo polska ustawa o VAT dopuszcza liczenie podatku od sumy stawek albo od poszczególnych pozycji. Jeśli suma się nie zgadza, dokument trafia do osobnego folderu do szybkiej weryfikacji ręcznej, a Wy dostajecie powiadomienie. Do tego deduplikacja: klucz hash pliku plus NIP i numer dokumentu. Ten sam dokument wrzucony drugi raz z maila i ze skanera nie przejdzie ponownie. Przy kwotach powyżej 15 000 zł sprawdzam kontrahenta na Białej Liście podatników VAT.

Po drugie, połączenie z Comarch Optima. Tu chcę być bardzo wyraźny, bo to jest miejsce, w którym nie wolno iść na skróty. Nigdy nie piszemy bezpośrednio do bazy Optimy przez INSERT SQL. To łamie integralność bazy, numerację rejestrów, a przy zamknięciu miesiąca potrafi narobić prawdziwego bałaganu. Comarch może wtedy odmówić wsparcia, a księgowość ma problem. Zamiast tego korzystam z oficjalnej, bezpiecznej ścieżki: Praca Rozproszona XML albo Comarch ERP Web API. Optima sama weryfikuje poprawność pliku importu, zanim cokolwiek trafi do obiegu. Najwięcej pracy jest przy mapowaniu towarów. Okno importu ma domyślnie zaznaczone „Załóż karty towarów”, więc nazwy od dostawców narobiłyby Wam bałaganu w kartotece. Wyłączamy to i dopasowujemy pozycje według tabeli powiązań. Dostawca pisze „Śruba M8x40 ocynk”, a u Was to karta SR-M8-40. Pierwszy raz pozycję przypisuje człowiek, potem automat pamięta regułę. I najważniejsze: wszystkie testy robimy na kopii bazy. Produkcja nie zostaje dotknięta, dopóki import nie przejdzie czysto na kopii.

Przewidywany czas realizacji i przykłady podobnych automatyzacji

Całość zajmie 18 dni roboczych. Rozbijam to na dwa etapy, żebyście mieli pełną kontrolę i płacili za odebrany kawałek pracy.

Etap pierwszy to przygotowanie n8n na własnym serwerze, pobieranie plików z Google Drive i skrzynki mailowej, preprocessingu skanów i testy odczytu na Waszych rzeczywistych dokumentach. Ten etap wyceniam na 5 400 zł netto. Po jego zakończeniu zobaczycie, jak automat radzi sobie z Waszymi fakturami, WZ-kami i zamówieniami, jeszcze bez dotykania Optimy.

Etap drugi to integracja importu z Optimą, mapowanie kartotek, testy na kopii bazy i asysta powdrożeniowa. Ten etap to 4 400 zł netto. Płatność za każdy etap po jego odebraniu.

Mam za sobą wdrożenie potoku dla ponad 3500 dokumentów z precyzją 99,4 procent. Robiłem też integracje z modułami Comarch ERP: rejestrami zakupu VAT oraz dokumentami magazynowymi WZ i PZ. Wiem, gdzie Optima bywa wrażliwa i jak przeprowadzić import, żeby nie zablokować księgowości.

Koszty utrzymania są przewidywalne. n8n działa na własnym VPS, więc nie ma opłat za każdą operację. Serwer to około 30-50 zł miesięcznie. Tokeny modelu AI przy skanach to zwykle 50-100 zł miesięcznie przy 1000 dokumentów. Razem 80-150 zł miesięcznie. Żadnych ukrytych subskrypcji ani nagłych dopłat.

Po uruchomieniu dostajecie 30 dni asysty powdrożeniowej. Przez pierwszy miesiąc poprawiamy reguły na dokumentach, które faktycznie przyjdą. A przez 12 miesięcy od wdrożenia naprawiam bezpłatnie ewentualne błędy w kodzie, który napisałem. Jeśli będzie trzeba, pomogę też przy drobnych zmianach, ale to już poza gwarancją.

Zanim podejmiemy decyzję, proponuję prostą rzecz: prześlijcie mi kilka przykładowych dokumentów, najlepiej takich, które sprawiają najwięcej kłopotu. Jedną fakturę z maila, jeden skan ze skanera i jedno zdjęcie od kierowcy. Przerobię je na sucho i pokażę, co automat odczyta, a co wymaga dopracowania. Bez zobowiązań. Zobaczycie na własne oczy, jak to działa na Waszym materiale.

Czy taka forma współpracy i rozbicia na etapy Państwu odpowiada?
```

---
## WERDYKT SĘDZIEGO HEAD-TO-HEAD:

## Audyt ofert #144890 — werdykt bezlitosny

Punktacja za 4 kategorie merytoryczne (0–25 każda). Kategoria 5 to werdykt końcowy.

| Kategoria | Wersja A | Wersja B | Zwycięzca |
|---|---:|---:|---|
| 1. Język, styl i ludzkość | 12/25 | 24/25 | **B** |
| 2. Merytoryka i architektura techniczna | 22/25 | 24/25 | **B** |
| 3. Psychologia zaufania i odwrócenie ryzyka | 15/25 | 25/25 | **B** |
| 4. Realność wyceny i terminu | 10/25 | 22/25 | **B** |
| **Razem** | **59/100** | **95/100** | **B** |

---

## 1. Język, styl i ludzkość — A: 12, B: 24

**Wersja A** jest kompetentna, ale czyta się jak zrzut myśli z głowy inżyniera tuż przed deadline’em. Gęsta, telegramowa, bez prowadzenia klienta za rękę. Dla właściciela firmy, który nie siedzi w n8n, KSeF, FA(3), API i INSERT-ach, to mur. Nie jest to bełkot — to jest dobra techniczna notatka, ale zła oferta sprzedażowa.

**Wersja B** brzmi jak człowiek-ekspert, który tłumaczy przy kawie, ale nie traci kompetencji. Zaczyna od sensownego uporządkowania problemu: KSeF załatwia Optima, OCR ma sens dla reszty. Potem tłumaczy trudne rzeczy prosto: trzy strumienie dokumentów, AI tylko czyta, matematykę sprawdza kod, nigdy INSERT do bazy. To buduje zrozumienie, a nie tylko wrażenie „dużo mądrych słów”.

**Wygrywa B. Bezapelacyjnie.**

---

## 2. Merytoryka i architektura techniczna — A: 22, B: 24

Wersja A nie jest technicznie słaba. Ma bardzo dobre konkrety:
- KSeF jako XML FA(3),
- natywne pobieranie w nowszych Optimach,
- parsowanie PDF z warstwą tekstową bez tokenów,
- preprocessing skanów,
- model Vision z progiem pewności,
- walidacja matematyczna z tolerancją 1–2 gr,
- deduplikacja po NIP + numer + hash,
- Biała Lista MF przy 15 000 zł,
- Praca Rozproszona XML / Comarch ERP Web API,
- zakaz bezpośredniego INSERT do bazy,
- testy na kopii bazy,
- 30 dni gwarancji,
- referencja: 3500+ dokumentów, 99,4% precyzji.

To jest solidny poziom.

Wersja B **nie traci głębi**. Ma wszystkie kluczowe elementy A, a dodatkowo dokłada rzeczy, które w praktyce zabijają takie wdrożenia:
- mapowanie kartotek towarowych,
- problem domyślnego „Załóż karty towarów” w Optimie,
- tabela powiązań typu „Śruba M8x40 ocynk” → SR-M8-40,
- pierwsze przypisanie przez człowieka, potem reguła automatu,
- podział na trzy strumienie: PDF cyfrowy, skan, zdjęcie z terenu,
- jasne rozdzielenie AI vs deterministyczna walidacja,
- testy wyłącznie na kopii bazy,
- transparentne koszty tokenów AI.

A ma przewagę w kilku szczegółach: podaje dokładniejszą wersję Optima 2026.4.1 i próg pewności Vision. Ale B wygrywa architekturą wdrożenia i podejściem do mapowania danych, które jest najczęstszym realnym wąskim gardłem w Comarch Optima.

**Wygrywa B, ale różnica jest mniejsza niż w innych kategoriach.**

---

## 3. Psychologia zaufania i odwrócenie ryzyka — A: 15, B: 25

Tu Wersja A przegrywa strategicznie.

A daje:
- 30 dni gwarancji,
- testy na kopii bazy,
- pytanie o środowisko Optimy,
- referencję.

To OK, ale za mało jak na pełne wdrożenie obejmujące integrację z systemem księgowo-magazynowym.

Wersja B robi coś znacznie ważniejszego: **przenosi ryzyko z klienta na wykonawcę i rozkłada je na etapy**.
- Etap 1: n8n, pobieranie plików, preprocessing, testy odczytu na rzeczywistych dokumentach. Klient widzi efekty, zanim dotknięta zostanie Optima.
- Etap 2: integracja z Optimą, mapowanie kartotek, testy na kopii bazy, asysta.
- Płatność za każdy etap po odbiorze.
- 30 dni asysty powdrożeniowej.
- 12 miesięcy bezpłatnej naprawy błędów w kodzie.
- Propozycja bezpłatnego testu na próbce dokumentów klienta.
- Wyjaśnienie, dlaczego nie wolno iść na skróty z INSERT do bazy.

To jest oferta, która mówi właścicielowi: „Nie musisz mi wierzyć na słowo. Zobaczysz działanie na swoich dokumentach, zanim zapłacisz za całość i zanim dotkniemy produkcji”.

**Wygrywa B. To jest najmocniejsza różnica między ofertami.**

---

## 4. Realność wyceny i terminu — A: 10, B: 22

**Wersja A: 6 500 zł / 13 dni** na:
- zaprojektowanie całego scenariusza,
- n8n self-hosted,
- pobieranie z Google Drive i maila,
- OCR/AI dla skanów i zdjęć,
- walidację matematyczną,
- deduplikację,
- Białą Listę,
- zmianę nazw i archiwizację,
- integrację z Comarch Optima,
- mapowanie danych,
- testy na rzeczywistych dokumentach,
- opiekę powdrożeniową.

To jest **poważnie niedoszacowane**. 13 dni roboczych na całość z integracją Optimy i mapowaniem kartotek to pośpiech. Może skończyć się albo niedokończonym zakresem, albo ciągłymi dopłatami, albo wdrożeniem, które „działa” tylko na demo. Przy 6 500 zł wykonawca musi ciąć gdzieś zakres, testy albo czas na dopracowanie wyjątków.

**Wersja B: 9 800 zł / 18 dni**, rozbite na 5 400 zł + 4 400 zł, z etapem testowym przed Optimą, jest znacznie bardziej wiarygodna. Nadal nie jest to wycena „enterprise”, ale przy doświadczonym wykonawcy i ograniczonym zakresie jest realna. Klient płaci więcej na starcie, ale kupuje mniejsze ryzyko wpadki, przestoju księgowości i bałaganu w kartotekach.

**Wygrywa B. A pachnie niedoszacowaniem i ryzykiem scope creep.**

---

## 5. Ostateczny werdykt i podsumowanie

**Łączna punktacja:**
- **Wersja A: 59/100**
- **Wersja B: 95/100**

**Klient wybiera Wersję B.**

Nie dlatego, że jest ładniej napisana. Dlatego, że jest **bezpieczniejsza wdrożeniowo**. Wersja A jest technicznie dobra, ale zbyt krótka, zbyt tania i zbyt szybka jak na pełne wdrożenie z integracją Comarch Optima. Wygląda jak oferta człowieka, który wie, co robi, ale nie zabezpieczył projektu przed typowymi problemami wdrożeniowymi.

Wersja B:
- lepiej tłumaczy technologię,
- nie traci głębi inżynierskiej,
- rozdziela AI od walidacji,
- pokazuje realne ryzyka Optimy,
- etapuje płatność,
- daje test na próbce dokumentów,
- chroni produkcję,
- jasno liczy koszty utrzymania,
- daje 12 miesięcy gwarancji na kod,
- i buduje zaufanie.

Dla właściciela firmy handlowo-produkcyjnej, który nie chce ryzykować paraliżu obiegu dokumentów, **Wersja B jest jedynym rozsądnym wyborem**.

---

## Co jeszcze doszlifować w zwycięskiej Wersji B

1. **Dodać twarde kryteria odbioru etapów**  
   Np. etap 1 zaliczony, jeśli na próbce 50 dokumentów automat poprawnie sklasyfikuje min. 95% i odczyta min. 90% pól krytycznych.

2. **Doprecyzować SLA i gwarancję**  
   Co dokładnie obejmuje 12 miesięcy gwarancji? Czas reakcji? Co jest błędem, a co zmianą zakresu? Wyłączyć zmiany API Comarch, nowe wersje Optimy, nowe typy dokumentów.

3. **Ustalić limit zakresu**  
   Ile typów dokumentów? Ile formatów? Ile kartotek? Ile wyjątków? Ilu użytkowników? Jaki wolumen miesięczny? Bez tego każda automatyzacja może się rozlać.

4. **Dodać klauzulę KSeF-first**  
   Jasno: faktury krajowe z KSeF są pobierane natywnie, OCR tylko dla dokumentów spoza KSeF. To oszczędza tokeny i upraszcza architekturę.

5. **Opisać odpowiedzialność za dostępy i RODO**  
   VPS, n8n, Google Drive, mail, Optima, kopie bazy, umowa powierzenia przetwarzania danych. Kto zarządza dostępami? Kto odpowiada za wyciek?

6. **Dodać cennik zmian po gwarancji**  
   Stawka godzinowa, minimalny blok, tryb zgłaszania. Klient musi wiedzieć, ile kosztuje rozwój po 12 miesiącach.

7. **Zabezpieczyć przed vendor lock-in**  
   Dokumentacja workflow, eksport n8n, przekazanie credentiali, instrukcja odtworzenia środowiska.

8. **Doprecyzować koszty AI**  
   Kto płaci za tokeny? Czy są limity? Co się dzieje przy przekroczeniu? Czy jest fallback na tańszy model?

**Werdykt końcowy: Wersja B. Nie negocjować ceny w dół — negocjować zakres, SLA i kryteria odbioru.**