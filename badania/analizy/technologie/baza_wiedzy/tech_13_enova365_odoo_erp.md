# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B

## TEMAT: Zaawansowane Integracje ERP — Enova365 (Soneta.Business, Harmonogram Zadań, WebAPI) oraz Odoo (moduły Python, OWL, KSeF, polska lokalizacja podatkowa)

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW

### 1.1. Typologia zleceń na Useme (obserwacja 2025–2026)

| Typ zlecenia | Charakterystyka klienta | Budżet typowy | Czas realizacji |
|---|---|---|---|
| **Integracja Enova365 ↔ system zewnętrzny** | Dział IT / księgowość średniego przedsiębiorstwa (50–300 pracowników), często po wdrożeniu enova365 przez partnera Soneta | 6 000 – 16 000 zł | 3–6 tygodni |
| **Automatyzacja obiegu faktur KSeF w enova365** | Główna księgowa lub CFO, presja terminu obowiązkowego KSeF od lutego/kwietnia 2026 | 5 000 – 12 000 zł | 2–4 tygodnie |
| **Moduł Odoo (custom) pod polską lokalizację** | Właściciel firmy lub COO, wdrożenie Odoo 17/18 przez partnera OCA, potrzeba modyfikacji l10n_pl | 4 500 – 14 000 zł | 3–8 tygodni |
| **Integracja Odoo ↔ Enova365 (dwukierunkowa)** | Rzadkie, ale najbardziej dochodowe — klient ma dwa systemy po migracji lub przejęciu | 10 000 – 16 000 zł | 6–10 tygodni |
| **Migracja danych / upgrade Odoo 17 → 18** | Klient z niestandardowymi modyfikacjami, boi się utraty customizacji | 5 000 – 12 000 zł | 2–5 tygodni |

### 1.2. Sygnały ostrzegawcze w ogłoszeniu (czerwone flagi po stronie klienta)

- „Mamy stary dodatek do enova365, który przestał działać po aktualizacji” → **prawdopodobnie modyfikacja przez bezpośredni SQL do tabel Sonety lub nieobsługiwany hook**.
- „Potrzebujemy tylko prostej integracji, to zajmie dzień” → klient nie rozumie, że **WebAPI Soneta to płatny moduł**, a nie wbudowana funkcja enova365.
- „Chcemy zmienić zachowanie modułu sprzedaży w Odoo” bez wzmianki o module custom → **ryzyko edycji plików rdzenia `odoo/addons/`**, co blokuje aktualizacje.
- „Mamy budżet 2000 zł na integrację KSeF” → **realny koszt samego modułu WebAPI i certyfikatu KSeF przekracza tę kwotę**; klient nie jest gotowy na projekt.

### 1.3. Poziom konkurencji

Na Useme w kategorii ERP/ integracje dominują freelancerzy oferujący „integracje przez API” bez wiedzy o specyfice Soneta.Business lub Odoo ORM. **Elita wygrywa, gdy w pierwszych zdaniach pokaże, że rozumie różnicę między API REST a bezpośrednim dostępem do bazy oraz konsekwencje edycji rdzenia Odoo.**

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1. Enova365 — architektura Soneta.Business

**Model sesyjno-transakcyjny.** Enova365 opiera się na sesjach `Soneta.Business.Session`, które grupują operacje w transakcje. Każda sesja ma izolowany kontekst, a zatwierdzenie (`Commit`) lub wycofanie (`Rollback`) określa trwałość zmian. **Bezpośrednia manipulacja obiektami biznesowymi poza sesją powoduje `InvalidOperationException` lub ciche pominięcie walidacji.**

**WebAPI jako osobny, płatny moduł.** Soneta WebAPI **nie jest wliczony w licencję enova365** — klient musi dokupić moduł. WebAPI udostępnia REST API z autoryzacją JWT, kontrolery dynamiczne (dokumenty, kontrahenci, produkty) oraz kontrolery statyczne dla obiektów zamodelowanych wprost przez Sonetę. To **wspierana droga integracji** — w przeciwieństwie do bezpośredniego SQL.

**Harmonogram Zadań (Scheduler).** Wbudowany mechanizm enova365 może wywoływać zewnętrzne endpointy (push). Dla integracji wymagających reakcji tego samego dnia (odrzucona faktura KSeF, dokument zmieniony po wygenerowaniu podsumowania) push jest różnicą między kontrolą a alertem.

**KSeF API 2.0.** Enova365 obsługuje nowe API KSeF 2.0 od wersji 2510.1.1 (listopad 2025), zastępując wersję 1.0. Wsparcie obejmuje środowiska testowe i przedprodukcyjne. **Faktury KSeF przychodzą jako ustrukturyzowany XML FA(3) przez API 2.0 — NIP sprzedawcy, kwoty, stawki VAT per linia, daty — wszystko są już polami, nic nie trzeba odczytywać z obrazu**. Klienci enova365 nie ponoszą dodatkowych opłat za wysyłanie i odbieranie faktur z/do KSeF.

### 2.2. Odoo — ORM, OWL, dziedziczenie

**ORM i `_inherit`.** W Odoo 17 i 18 modele dziedziczą przez `_inherit`, rozszerzając istniejące klasy bez modyfikacji rdzenia. **Krytyczna pułapka:** od Odoo 17 atrybut `_inherit` na klasach rejestru (`self.env.registry['model']._inherit`) **nie powinien być używany poza frameworkiem** — jest przeznaczony wyłącznie dla klas definicji modeli. Użycie go w kodzie zewnętrznym prowadzi do błędnego zachowania frameworku.

**OWL Framework (Odoo Web Library).** Odoo 17/18 używa OWL jako frameworka deklaratywnych komponentów frontendowych (luźno inspirowany Vue/React). Komponenty OWL składają się z logiki JS, szablonów XML i opcjonalnego SCSS. **Osadzanie komponentów OWL w szablonach QWeb wymaga zrozumienia cyklu życia komponentu i poprawnego montowania** — najczęstszy błąd to brak `DialogContainer` w głównej aplikacji OWL.

**Polska lokalizacja podatkowa (`l10n_pl`).** Odoo 17/18 oferuje dojrzałą lokalizację polską: `l10n_pl` (plan kont, VAT), `l10n_pl_edi` (integracja KSeF FA(3)), `l10n_pl_reports` (raporty księgowe), `l10n_pl_taxable_supply_date` (data dostawy), `l10n_pl_bank_verification` (weryfikacja rachunku VAT dla płatności PL-to-PL > 15 000 PLN).

**KSeF w Odoo.** Od Odoo 17 w module `l10n_pl_edi` dostępna jest integracja z KSeF: generowanie i wysyłka FA(3) XML, śledzenie statusu KSeF na `account.move`, cron aktualizujący statusy. Konfiguracja wymaga certyfikatu `.pem` i klucza prywatnego z KSeF. **Obowiązek KSeF: najwięksi podatnicy (>200 mln PLN) od 1 lutego 2026; wszyscy podatnicy VAT od 1 kwietnia 2026**.

### 2.3. Tabela porównawcza krytycznych różnic

| Aspekt | Enova365 | Odoo 17/18 |
|---|---|---|
| Język backendu | C# / .NET (Soneta.Business) | Python (ORM) |
| Model transakcyjny | Sesje `Soneta.Business.Session` + jawne transakcje | Automatyczne transakcje per request; `@api.model_create_multi` |
| API zewnętrzne | Soneta WebAPI (płatny moduł, REST + JWT) | XML-RPC / JSON-RPC natywnie; REST przez custom controllers |
| Frontend | WinForms / Web (zależnie od wdrożenia) | OWL (JS) + QWeb (XML) |
| KSeF | API 2.0 od wersji 2510.1.1 | `l10n_pl_edi` (FA(3)) od Odoo 17 |
| Dziedziczenie | Brak odpowiednika `_inherit`; rozszerzenia przez pluginy C# | `_inherit`, `_inherits` (delegation) |
| Aktualizacje | Nowe wersje co kwartał; kompatybilność wsteczna pluginów | Roczny cykl major (17→18→19); aktualizacje łamiące custom |

---

## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### 3.1. Enova365 — LockException i sesje

**LockException** w enova365 pojawia się, gdy dwa procesy próbują jednocześnie modyfikować ten sam obiekt w ramach różnych sesji. W praktyce integracyjnej najczęstsze scenariusze:

1. **Scheduler (Harmonogram Zadań) uruchamia import, podczas gdy użytkownik ręcznie edytuje ten sam dokument** → `LockException` przy próbie `Commit`. Klient widzi komunikat „dokument zablokowany” i traci dane z importu.
2. **Dwa równoległe wątki WebAPI przetwarzają tę samą fakturę KSeF** → drugi wątek otrzymuje `LockException` po timeout. **Rozwiązanie inżynierskie:** kolejka FIFO z jednym workerem per typ dokumentu, nie współbieżne przetwarzanie.
3. **Brak obsługi `LockException` w kodzie integracji** → wyjątek propaguje się do użytkownika końcowego jako „błąd systemu”, bez retry.

**Prawdziwy ból klienta:** „Nasz dodatek do enova365 działał, dopóki nie uruchomiliśmy go na serwerze produkcyjnym z wieloma użytkownikami. Teraz wywala się przy każdym imporcie faktur.” To klasyczny objaw **braku izolacji sesji w kodzie integracyjnym** — dodatek napisany w środowisku single-user, uruchomiony w multi-user.

### 3.2. Enova365 — cicha utrata danych przez bezpośredni SQL

Bezpośredni SQL do tabel Sonety (zamiast WebAPI) to najczęstsza „oszczędność” amatorów. Problem: **schemat bazy nie jest kontraktem.** Soneta nie ma obowiązku utrzymania kolumny tam, gdzie zapytanie jej oczekuje. W dniu, gdy kolumna się przesunie, integracja **nie ulega degradacji — staje się cicho błędna**. Klient dowiaduje się o problemie po miesiącach, gdy dane księgowe nie zgadzają się z rzeczywistością.

**Dodatkowy ból:** bezpośredni SQL omija walidację biznesową Soneta.Business, co prowadzi do dokumentów w stanie niespójnym (np. faktura bez wymaganego kontrahenta, dokument w buforze bez numeracji). Enova365 **nie pozwoli na zapisanie dokumentu z terminem płatności wcześniejszym niż data dokumentu** przez API — ale SQL tego nie sprawdzi.

### 3.3. Odoo — modyfikacja rdzenia blokująca aktualizacje

**Największa mina Odoo:** edycja plików w `odoo/addons/` (np. `sale`, `account`, `stock`). Każda aktualizacja Odoo **nadpisuje pliki rdzenia**. Modyfikacje znikają lub — gorzej — powodują konflikt z nowym kodem.

**Konkretny scenariusz awarii:** dodanie pola do `res.partner` przez edycję rdzenia `res_partner.py` zamiast modułu dziedziczącego. Przy aktualizacji modułu przez UI/RPC, kod wykonuje się **przed** aktualizacją modułu, a `SELECT` na bazie zawiera nową nazwę pola → **Odoo crashuje przy logowaniu**. Jedynym wyjściem jest aktualizacja z linii poleceń.

**Konsekwencja biznesowa:** klient płaci za „dostosowanie Odoo do naszych potrzeb”, a po roku nie może wykonać aktualizacji bezpieczeństwa, bo customizacja jest w rdzeniu. Koszt naprawy: 5 000–12 000 zł na refaktoryzację do modułów dziedziczących.

### 3.4. Odoo — N+1 queries i wydajność

Modyfikacje ORM bez zrozumienia leniwego ładowania (`recordset`, `prefetch`) prowadzą do **N+1 queries** — każdy rekord w pętli generuje osobne zapytanie SQL. Przy 10 000 kontrahentów prosty raport może trwać minuty zamiast sekund. Klient zgłasza „Odoo jest wolne”, a problem leży w customowym module, nie w Odoo.

---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

### 4.1. Dla zleceń Enova365

> **Insight 1:** „Zanim dotkniemy integracji — czy Państwa enova365 ma aktywną licencję na moduł Soneta WebAPI? Bez niego każda integracja z KSeF przez REST jest niemożliwa bezpośrednio z systemu, a obejście przez SQL do tabel Sonety kończy się cichą utratą spójności danych przy najbliższej aktualizacji schematu.”

Dlaczego działa: **natychmiast pokazuje, że znasz realny koszt projektu (WebAPI to płatny moduł)** i ostrzegasz przed antywzorcem (SQL). Amator napisze „zrobię integrację przez API” — nie wiedząc, że API trzeba dokupić.

> **Insight 2:** „Jeśli Państwa obecny dodatek do enova365 przestał działać po aktualizacji — w 9 na 10 przypadków to nie błąd Sonety, tylko bezpośredni SQL do tabel, który przestał trafiać w kolumny po zmianie schematu. Naprawa wymaga przepisania integracji na WebAPI, a nie kolejnej łatki SQL.”

Dlaczego działa: **diagnozujesz problem klienta zanim on go opisze.** Klient szukający pomocy po awarii natychmiast rozpoznaje swój przypadek.

### 4.2. Dla zleceń Odoo

> **Insight 3:** „Jeśli Państwa modyfikacje Odoo były robione przez edycję plików w `odoo/addons/`, to przy najbliższej aktualizacji (17→18) stracą Państwo wszystkie zmiany — a jeśli pole zostało dodane do rdzenia, Odoo może crashować przy logowaniu. Standardowa naprawa to refaktoryzacja do modułu dziedziczącego `_inherit`, co zajmuje 2–4 dni, ale ratuje możliwość aktualizacji na lata.”

Dlaczego działa: **nazywasz konkretny plik (`odoo/addons/`) i konkretny objaw (crash przy logowaniu).** To buduje wiarygodność inżynierską w 2 zdaniach.

> **Insight 4:** „Czy Państwa Odoo ma już włączoną integrację KSeF w `l10n_pl_edi`? Od 1 kwietnia 2026 wszyscy podatnicy VAT w Polsce są objęci obowiązkiem — brak konfiguracji certyfikatu `.pem` i cronu statusów oznacza, że faktury nie będą wysyłane, a system nie zgłosi błędu.”

Dlaczego działa: **precyzyjna data obowiązku i konkretny moduł.** Klient, który „odkłada KSeF na później”, nagle widzi, że czas minął.

### 4.3. Dla zleceń hybrydowych (Enova365 + Odoo)

> **Insight 5:** „Integracja Enova365 ↔ Odoo przez tabelę pośredniczącą (np. SQL) to najdroższa droga — oba systemy mają własne modele transakcyjne, a brak wspólnego klucza biznesowego (poza NIP) powoduje duplikaty kontrahentów i dokumentów. Poprawna architektura to kolejka komunikatów z idempotentnym przetwarzaniem po obu stronach.”

Dlaczego działa: **wskazujesz architekturę, nie narzędzie.** Amator powie „zrobię synchronizację przez API”.

---

## 5. CZERWONA LISTA / ANTYWZORCE

### 5.1. Enova365 — czego NIGDY nie robić

| Antywzorzec | Konsekwencja | Poprawna alternatywa |
|---|---|---|
| **Bezpośredni SQL do tabel Sonety** | Cicha utrata spójności przy zmianie schematu; brak walidacji biznesowej | Soneta WebAPI (kontrolery dynamiczne/statyczne) |
| **Brak obsługi `LockException` w kodzie integracyjnym** | Użytkownik widzi „błąd systemu”; import przerywany przy współbieżności | Retry z backoffem; kolejka FIFO per typ dokumentu |
| **Współbieżne przetwarzanie tych samych dokumentów z WebAPI** | `LockException` po timeout; duplikaty | Jeden worker per typ dokumentu; idempotencja po kluczu KSeF |
| **Zapis dokumentów jako finalnych przez WebAPI** | Soneta WebAPI **zapisuje dokumenty jako szkice do przejrzenia, nigdy jako finalne księgowania** | Akceptacja przez człowieka; status `Do zatwierdzenia` |
| **Ignorowanie faktu, że WebAPI to płatny moduł** | Projekt wstrzymany na etapie licencji | Weryfikacja licencji przed wyceną |
| **Brak rozróżnienia między odrzuconą fakturą KSeF a fakturą, która nie została wysłana** | Księgi mówią „faktura istnieje”, rejestr państwowy milczy; wykrywane po miesiącach | Rekoncyliacja list: dokumenty w enova vs. KSeF |

### 5.2. Odoo — czego NIGDY nie robić

| Antywzorzec | Konsekwencja | Poprawna alternatywa |
|---|---|---|
| **Edycja plików w `odoo/addons/`** | Aktualizacja nadpisuje zmiany; możliwy crash przy logowaniu | Moduł dziedziczący `_inherit` w `custom_addons/` |
| **Użycie `self.env.registry['model']._inherit` poza frameworkiem** | Framework Odoo rezerwuje ten atrybut dla klas definicji; użycie zewnętrzne prowadzi do błędów | Odczyt przez `_fields` lub `_get_fields()` |
| **Brak `DialogContainer` w głównej aplikacji OWL** | Komponenty dialogowe nie renderują się | `import { DialogContainer } from "@web/core/dialog/dialog_container"` w root app |
| **Modyfikacja `res.partner` przez edycję rdzenia zamiast modułu** | Crash przy aktualizacji modułu przez UI/RPC | Moduł `_inherit = 'res.partner'` |
| **Brak wersjonowania Git dla custom modułów** | Brak możliwości rollbacku po nieudanej aktualizacji | Repozytorium Git per moduł; tagi wersji Odoo |
| **Testowanie aktualizacji bezpośrednio na produkcji** | Ryzyko utraty danych i przestoju | Środowisko staging z dumpem produkcyjnym |

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE

### 6.1. Szablon wyceny dla integracji Enova365 (5 000 – 14 000 zł)

| Moduł | Zakres | Czas | Wycena (PLN) |
|---|---|---|---|
| **M1. Analiza i projekt interfejsu** | Inwentaryzacja obiektów Soneta (dokumenty, kontrahenci), mapowanie pól, wybór WebAPI vs. push przez Scheduler, projekt kluczy idempotencji | 2–3 dni | 2 000 – 3 500 |
| **M2. Warstwa transportowa** | Konfiguracja Soneta WebAPI (JWT, kontrolery dynamiczne), implementacja klienta REST po stronie zewnętrznej, obsługa błędów sieciowych | 3–5 dni | 2 500 – 4 500 |
| **M3. Logika biznesowa i mapowanie** | Mapowanie NIP → kontrahent, VAT → stawki, KSeF FA(3) → dokumenty enova, obsługa wyjątków (brak kontrahenta, duplikat) | 4–6 dni | 3 000 – 5 000 |
| **M4. Harmonogram i kolejkowanie** | Konfiguracja Harmonogramu Zadań dla push, kolejka FIFO, retry z backoffem, obsługa `LockException` | 2–3 dni | 1 500 – 2 500 |
| **M5. Rekoncyliacja i monitoring** | Rekoncyliacja enova vs. KSeF, alertowanie o rozbieżnościach, log audytowy | 2–3 dni | 1 500 – 2 500 |
| **M6. Testy i dokumentacja** | Testy integracyjne na środowisku przedprodukcyjnym, dokumentacja API, instrukcja obsługi | 2–3 dni | 1 500 – 2 500 |
| **RAZEM** | | **15–23 dni** | **12 000 – 20 500** |

> **Uwaga:** widełki 5 000 – 14 000 zł dotyczą **wyłącznie modułów M2–M4** (bez pełnej rekoncyliacji i dokumentacji). Dla budżetu 5 000–8 000 zł realny zakres to „integracja jednego typu dokumentu w jedną stronę”.

### 6.2. Szablon wyceny dla modułu Odoo (4 500 – 14 000 zł)

| Moduł | Zakres | Czas | Wycena (PLN) |
|---|---|---|---|
| **M1. Audyt istniejących customizacji** | Przegląd `custom_addons/`, identyfikacja edycji rdzenia, ocena ryzyka aktualizacji | 1–2 dni | 1 500 – 2 500 |
| **M2. Moduł dziedziczący (`_inherit`)** | Nowe pola, widoki XML, logika ORM, security (`ir.model.access`) | 3–5 dni | 2 500 – 4 500 |
| **M3. Warstwa OWL (jeśli dotyczy)** | Komponenty frontendowe, integracja z QWeb, `DialogContainer` | 2–4 dni | 2 000 – 3 500 |
| **M4. Integracja KSeF (`l10n_pl_edi`)** | Konfiguracja certyfikatu `.pem`, cron statusów, walidacja FA(3), obsługa błędów KSeF | 2–3 dni | 1 500 – 2 500 |
| **M5. Migracja / upgrade** | Skrypty migracyjne, testy na stagingu, refaktoryzacja customizacji z rdzenia | 3–5 dni | 2 500 – 4 500 |
| **M6. Testy i dokumentacja** | Testy jednostkowe ORM, testy integracyjne KSeF, dokumentacja modułu | 2–3 dni | 1 500 – 2 500 |
| **RAZEM** | | **13–22 dni** | **11 500 – 20 000** |

> **Uwaga:** widełki 4 500 – 14 000 zł dotyczą **M2–M4** (nowy moduł + KSeF bez audytu i migracji). Dla budżetu poniżej 6 000 zł zakres ogranicza się do jednego modułu bez integracji KSeF.

### 6.3. Architektura referencyjna — Enova365 ↔ Odoo

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   enova365      │     │  Warstwa         │     │   Odoo 17/18    │
│   (Soneta)      │     │  pośrednicząca   │     │                 │
│                 │     │                  │     │                 │
│  Soneta WebAPI  │◄───►│  Kolejka         │◄───►│  Custom module  │
│  (REST + JWT)   │     │  komunikatów     │     │  _inherit       │
│                 │     │  (RabbitMQ/Kafka) │     │                 │
│  Harmonogram    │     │                  │     │  l10n_pl_edi    │
│  Zadań (push)   │     │  Idempotencja    │     │  (KSeF FA(3))   │
│                 │     │  po NIP + numer  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

**Zasady:**
1. **Nigdy nie łączyć obu systemów bezpośrednio przez SQL** — każdy ma własny model transakcyjny.
2. **Klucz idempotencji:** NIP kontrahenta + numer dokumentu źródłowego (KSeF number jest unikalny i stanowi fakt, nie heurystykę).
3. **Zapis do enova365 wyłącznie jako szkice** — finalne księgowanie przez człowieka.
4. **Odoo jako źródło prawdy dla KSeF** — `l10n_pl_edi` generuje FA(3) i wysyła do KSeF; enova365 odbiera KSeF XML i tworzy szkice dokumentów.

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE W ŚRODEK TEKSTU

Poniższe pytania należy wpleść **w środku analizy oferty** (nie na końcu), aby zmusić klienta do natychmiastowego odpisania na priv. Każde pytanie jest zaprojektowane tak, aby odpowiedź ujawniła zakres projektu i poziom dojrzałości klienta.

### 7.1. Pytania dla zleceń Enova365

> **P1:** „Czy Państwa licencja enova365 obejmuje aktywny moduł **Soneta WebAPI**, czy integracja ma być realizowana przez Harmonogram Zadań z zapisem do pliku/ bazy pośredniej?”

*Dlaczego działa:* Jeśli klient nie wie, co to WebAPI — projekt wymaga edukacji i większego budżetu. Jeśli WebAPI jest — od razu wiadomo, że można iść wspieraną drogą.

> **P2:** „Czy obecny dodatek/ integracja używa **bezpośredniego SQL do tabel Sonety**, czy operuje przez obiekty `Soneta.Business`?”

*Dlaczego działa:* Odpowiedź „SQL” oznacza, że przed rozbudową trzeba przepisać istniejący kod — to dodatkowe 2–4 dni i ryzyko.

> **P3:** „Jaki jest **klucz idempotencji** dla dokumentów w Państwa systemie — numer KSeF, NIP + numer obcy, czy inny? Czy przy duplikacie system ma tworzyć nowy dokument, czy aktualizować istniejący?”

*Dlaczego działa:* Ujawnia, czy klient myślał o duplikatach. Brak klucza idempotencji = ryzyko podwójnych księgowań.

### 7.2. Pytania dla zleceń Odoo

> **P4:** „Czy istniejące customizacje Odoo są w **`custom_addons/` jako moduły dziedziczące**, czy były wprowadzane przez edycję plików w `odoo/addons/`?”

*Dlaczego działa:* Jeśli edycja rdzenia — konieczna refaktoryzacja przed jakąkolwiek aktualizacją. To zmienia zakres projektu o 3–5 dni.

> **P5:** „Czy Państwa Odoo ma już włączoną integrację KSeF w **`l10n_pl_edi`** i skonfigurowany certyfikat `.pem`? Jaki jest obecny status wysyłki faktur do KSeF — ręczna, przez cron, czy brak?”

*Dlaczego działa:* Odpowiedź „brak” oznacza, że projekt obejmuje konfigurację KSeF od zera — dodatkowe 2–3 dni.

> **P6:** „Czy modyfikacje są wersjonowane w **Git** i czy istnieje środowisko **staging** z dumpem produkcyjnym do testowania aktualizacji?”

*Dlaczego działa:* Brak Git i staging to czerwona flaga — każda zmiana na produkcji to ryzyko. Klient, który to rozumie, doceni profesjonalizm.

### 7.3. Pytania dla zleceń hybrydowych

> **P7:** „Który system jest **źródłem prawdy** dla danych kontrahentów i dokumentów — enova365 czy Odoo? Czy synchronizacja ma być jednokierunkowa, czy dwukierunkowa z rozwiązywaniem konfliktów?”

*Dlaczego działa:* Ujawnia, czy klient ma architekturę, czy tylko „chce, żeby działało”. Dwukierunkowa synchronizacja bez źródła prawdy to projekt na 8–12 tygodni.

> **P8:** „Czy **KSeF number** jest używany jako unikalny identyfikator dokumentu w obu systemach? Jeśli nie — jak obecnie rozwiązujecie duplikaty faktur od tego samego kontrahenta na tę samą kwotę?”

*Dlaczego działa:* KSeF number jest unikalny i stanowi fakt, a nie heurystykę. Brak wykorzystania tego klucza oznacza, że klient ma problem z duplikatami, którego sobie nie uświadamia.

---

## PODSUMOWANIE — ESENCJA OFERTY ELITARNEJ

1. **Otwieraj problemem, nie stażem.** Pierwsze 2 zdania muszą nazwać ból klienta: „Jeśli Państwa dodatek do enova365 przestał działać po aktualizacji — to SQL do tabel, nie błąd Sonety” / „Jeśli modyfikacje Odoo były w `odoo/addons/`, stracą Państwo zmiany przy aktualizacji”.
2. **Nazywaj konkretne pliki, moduły i API.** `Soneta.Business.Session`, `odoo/addons/`, `_inherit`, `l10n_pl_edi`, `LockException` — to buduje wiarygodność.
3. **Rozbijaj wycenę na moduły.** Nigdy nie podawaj ryczałtu. Klient ma widzieć, za co płaci.
4. **Zadawaj 2–3 pytania w środku tekstu.** Zmuszają do odpowiedzi i filtrują klientów, którzy nie znają swojego systemu.
5. **Wskazuj antywzorce.** „Bezpośredni SQL do Sonety”, „edycja rdzenia Odoo” — nazwane wprost, pokazują, że znasz ryzyko.
6. **Zero spotkań wideo.** Komunikacja wyłącznie pisemna na priv.