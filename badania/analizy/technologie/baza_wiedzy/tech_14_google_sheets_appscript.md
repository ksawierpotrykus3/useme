# KARTA WIEDZY INŻYNIERSKIEJ — BOT OFERTOWY USEME / B2B

## TEMAT: Google Sheets + Google Apps Script + Automatyzacje Google Workspace (Gmail / Drive) — Omijanie Limitów Quotas i Architektura Arkusza jako Lekki Backend

---

## 1. METADANE RYNKOWE I PROFIL ZLECENIODAWCÓW NA USEME

**Budżety:** 1 500 – 6 000 zł netto za projekt. Dolna granica (1 500–2 500 zł) dotyczy prostych automatyzacji: mail → Sheets, parser CSV, raport dzienny. Górna (4 000–6 000 zł) — złożonych systemów z kolejką, API zewnętrznym i panelem kontrolnym w arkuszu.

**Profil zleceniodawcy:**
- **Typ A (nietechniczny, ~70% zleceń):** Właściciel małej firmy, e-commerce, dział operacyjny. Nie zna pojęcia „quota”, „trigger”, „batch”. Opisuje ból: „ręcznie kopiuję 200 wierszy codziennie”, „arkusz się zacina”, „skrypt przestaje działać po godzinie”. Szuka kogoś, kto „ogarnie temat”.
- **Typ B (półtechniczny, ~25%):** Manager projektów, analityk. Zna Sheets i formuły, próbował sam napisać skrypt, ale „wyskakuje błąd po 6 minutach”. Rozumie, że potrzebuje inżyniera, ale nie potrafi nazwać architektury.
- **Typ C (techniczny, ~5%):** CTO małego startupu lub deweloper szukający kogoś do „dokończenia” automatyzacji. Oczekuje rozmowy o architekturze, batchingu, idempotencji.

**Win Rate:** 13.3% — oznacza, że oferta musi być **diagnozą, nie portfolio**. Zleceniodawca odrzuca oferty zaczynające się od „Mam 5 lat doświadczenia…”. Wygrywa ten, kto w pierwszych 2 zdaniach nazwie jego problem lepiej, niż on sam go opisał.

**Kontekst rynkowy 2026:** Na Useme rośnie popyt na automatyzacje łączące Gmail + Sheets + Drive, szczególnie w obszarze: parsowanie faktur z maili, synchronizacja zamówień z e-commerce, raportowanie sprzedaży, automatyczne faktury PDF → Drive.

---

## 2. KRYTYCZNE REALIA TECHNOLOGICZNE I STAN NA 2026 ROK

### 2.1 Twardy limit 6 minut — bez wyjątków

Od 2026 roku **zarówno konta consumer (gmail.com), jak i Google Workspace mają identyczny twardy limit 6 minut na pojedyncze wykonanie skryptu**. Stary limit 30 minut dla Workspace został zniesiony.

| Parametr | Consumer (gmail.com) | Google Workspace |
|---|---|---|
| **Max czas wykonania** | **6 minut** | **6 minut** |
| Dzienny czas triggerów | 90 minut | 6 godzin |
| URL Fetch calls / dzień | 20 000 | 100 000 |
| Properties read/write / dzień | 50 000 | 500 000 |

**Konsekwencja architektoniczna:** Nie istnieje legalny sposób na wydłużenie 6 minut. Każda architektura, która zakłada „skrypt będzie działał 20 minut”, jest błędna u samych podstaw. Jedyne rozwiązanie to **dekompozycja na porcje (batch) i continuation triggers**.

### 2.2 Operacje wsadowe getValues() / setValues() — różnica 10–50x

Google oficjalnie rekomenduje: **czytaj raz, przetwarzaj w pamięci, zapisuj raz**. Zamiast 10 000 wywołań `setValue()`, wykonaj **jedno** `setValues()` z dwuwymiarową tablicą.

**Benchmark 2026 (10 000 komórek, 2000 wierszy × 5 kolumn):**

| Metoda | Liczba wywołań API | Czas (mediana) |
|---|---|---|
| `getValue()` / `setValue()` w pętli | 20 000 | **8+ sekund** |
| `getValues()` + `setValues()` | 2 | **< 0,2 sekundy** |

Każde wywołanie `getValue()` lub `setValue()` to **osobna komunikacja z serwerem Google Sheets** — nie operacja lokalna. Pętla po komórkach to zabójca wydajności.

### 2.3 PropertiesService — jedyne miejsce na stan międzybatchowy

| Parametr | Wartość |
|---|---|
| Max rozmiar jednej wartości | 9 KB |
| Max całkowity rozmiar store | **500 KB** |
| Dzienny limit read/write | 50 000 (consumer) / 500 000 (Workspace) |

PropertiesService **nie jest bazą danych** — to rejestr klucz-wartość. Do przechowywania stanu batcha (np. ostatni przetworzony wiersz) użyj małych wartości liczbowych. Do większych struktur — CacheService (max 100 KB na klucz, TTL 10 minut).

### 2.4 UrlFetchApp.fetchAll() — równoległość, ale z pułapką

`fetchAll()` wykonuje żądania **równolegle**, co dramatycznie skraca czas w porównaniu do pętli `fetch()`. Jednak w 2026 roku pojawił się problem: **partie 5+ równoległych żądań mogą wyzwalać błąd „Bandwidth quota exceeded”** nawet przy niskim dziennym transferze. Bezpieczna strategia: **fetchAll z porcjami po 3–5 żądań i odstępem 200–500 ms między partiami**.

---

## 3. UKRYTE MINY I PRAWDZIWY BÓL KLIENTA

### Mina #1: Timeout przy 5000 requestów

Klient mówi: „Potrzebuję, żeby skrypt pobrał dane z API dla 5000 produktów”. Nie rozumie, że 5000 synchronicznych `fetch()` w pętli to ~5000 × 0,2 s = **1000 sekund = 16 minut**. Skrypt umrze po 6 minutach, przetworzywszy ~1800 rekordów. Reszta — **cicho zniknie**. Klient nie wie, że dane są niekompletne, dopóki nie sprawdzi ręcznie.

### Mina #2: Pętla komórka-po-komórce

Najczęstszy antywzorzec w kodzie klientów i „tanich” freelancerów:

```javascript
// ANTYWZORZEC — ZABIJA WYDAJNOŚĆ
for (let i = 1; i <= 5000; i++) {
  const value = sheet.getRange(i, 1).getValue(); // 5000 × API call
  sheet.getRange(i, 2).setValue(transform(value)); // kolejne 5000 × API call
}
```

**10 000 wywołań API → timeout gwarantowany.** Klient widzi, że „skrypt nie działa”, ale nie potrafi zdiagnozować przyczyny. To moment, w którym szuka pomocy.

### Mina #3: Trigger uruchamia się, ale nie kończy pracy

Klient ustawia trigger „co 5 minut”. Skrypt startuje, przetwarza 300 rekordów, kończy się po 4 minutach. Przy następnym uruchomieniu — **zaczyna od nowa**, nadpisując to, co już zrobił. Efekt: te same 300 rekordów przetwarzane w nieskończoność, pozostałe 4700 — nigdy.

### Mina #4: „Działa u mnie” — nie działa u klienta

Konto consumer (gmail.com) ma **90 minut dziennie** na triggery. Klient z Workspace ma 6 godzin. Freelancer testował na koncie Workspace, wdrożył u klienta na gmail.com. Skrypt przestaje działać po 1,5 godziny — bez ostrzeżenia, bez błędu w UI.

---

## 4. ZABÓJCZE INSIGHTY DO PIERWSZYCH 2 ZDAŃ

### Wzorzec A — diagnoza timeoutu (dla klienta Typ A)

> „Pani/Pana skrypt przestaje działać po 6 minutach, ponieważ Google wymusza twardy limit wykonania na każdym pojedynczym uruchomieniu — i nie da się go obejść. Rozwiązaniem nie jest szybszy kod, ale architektura porcjowa z continuation triggers, która przetwarza dane w partiach i automatycznie wznawia pracę.”

**Dlaczego działa:** Klient słyszy, że problem nie jest w jego kompetencjach, ale w **niedocumented feature** Google. Dostaje natychmiastową ulgę i konkretny kierunek.

### Wzorzec B — diagnoza wydajności (dla klienta Typ B)

> „Pętla `setValue()` po komórkach to najczęstsza przyczyna timeoutu w Apps Script — każde wywołanie to osobne żądanie HTTP do serwera Google. Zamiast 10 000 wywołań robimy 2: jedno `getValues()`, przetwarzanie w pamięci, jedno `setValues()`. To różnica między 8 sekundami a 0,2 sekundy.”

**Dlaczego działa:** Klient półtechniczny od razu widzi, że rozmawia z inżynierem, który **rozumie mechanikę**, a nie tylko „klepie kod”.

### Wzorzec C — diagnoza architektury (dla klienta Typ C)

> „Problem nie leży w API ani w limitach — leży w braku idempotentnego batch processora. Przy 5000 rekordach i 6-minutowym oknie potrzebna jest kolejka z zapisem stanu w PropertiesService i triggerem continuation, który przejmuje pracę tam, gdzie poprzednie wykonanie zostało przerwane.”

**Dlaczego działa:** Klient techniczny otrzymuje **nazwę wzorca architektonicznego**, którego szukał. To sygnał, że oferent myśli kategoriami systemowymi.

---

## 5. CZERWONA LISTA / ANTYWZORCE

### ZAKAZ #1: Pętla `for` z `setValue()` wewnątrz

```javascript
// ABSOLUTNY ZAKAZ
for (let i = 1; i <= lastRow; i++) {
  sheet.getRange(i, 1).setValue(data[i]);
}
```

**Dlaczego:** Każde `setValue()` to osobne wywołanie API. Przy 1000 wierszach — 1000 żądań HTTP. Czas: sekundy/minuty. Ryzyko timeoutu: **krytyczne**。

### ZAKAZ #2: Obietnica „skryptu na 30 minut”

Google **nie oferuje** możliwości wydłużenia 6-minutowego limitu — ani na Workspace, ani na Enterprise. Każda oferta zawierająca „skrypt będzie działał 30 minut” to **kłamstwo techniczne**. Prawidłowa odpowiedź: „Dekomponujemy zadanie na porcje po 3–5 minut i łańcuchujemy triggery.”

### ZAKAZ #3: Brak zapisu stanu między wykonaniami

Trigger uruchamia skrypt co 5 minut, ale skrypt nie wie, **gdzie skończył**. Efekt: duplikaty, nadpisania, nieskończone pętle. Każdy batch processor **musi** zapisywać ostatni przetworzony indeks w PropertiesService.

### ZAKAZ #4: `fetchAll()` z 10+ żądaniami w jednej partii

Od 2026 roku obserwowane są błędy „Bandwidth quota exceeded” przy partiach ≥ 5 żądań, nawet przy niskim dziennym transferze. Bezpieczna liczba: **3–5 żądań na partię** z odstępem 200–500 ms.

### ZAKAZ #5: Ignorowanie różnicy consumer vs Workspace

Skrypt testowany na Workspace (6h dziennie) wdrożony na gmail.com (90 min dziennie) przestanie działać po 1,5 godziny. **Zawsze pytaj o typ konta zleceniodawcy** przed wyceną.

---

## 6. PRODUKCYJNA ARCHITEKTURA I ROZBICIE MODUŁOWE

### Wycena: 2 000 – 5 500 zł netto

| Moduł | Zakres | Czas | Cena (zł) |
|---|---|---|---|
| **M1: Audyt i projekt kontraktu danych** | Analiza obecnego arkusza, identyfikacja wąskich gardeł, projekt struktury docelowej, mapowanie API | 1–2 dni | 400 – 800 |
| **M2: Batch Processor Core** | Silnik porcjowania: `getValues()` → przetwarzanie w pamięci → `setValues()`. Zapis stanu w PropertiesService. | 2–3 dni | 800 – 1 500 |
| **M3: Continuation Trigger Engine** | Tworzenie triggera czasowego, wznawianie pracy od ostatniego indeksu, cleanup po zakończeniu. Logika idempotencji. | 1–2 dni | 500 – 1 000 |
| **M4: Warstwa integracji Gmail/Drive/API** | Parsowanie maili (`GmailApp`), zapis plików na Drive (`DriveApp`), `fetchAll()` z kontrolą partii dla zewnętrznych API. | 2–3 dni | 800 – 1 500 |
| **M5: Panel kontrolny i monitoring** | Arkusz „Status” z postępem batcha, licznikiem błędów, ostatnim uruchomieniem. Powiadomienia mailowe o zakończeniu. | 1 dzień | 400 – 700 |
| **RAZEM** | | **7–11 dni** | **2 000 – 5 500** |

### Architektura przepływu

```
[Gmail Trigger] → [Parser maili] → [Zapis do Sheets (batch)]
       ↓
[Batch Processor] → getValues() → transform() → setValues()
       ↓
[PropertiesService: lastProcessedIndex]
       ↓
[Continuation Trigger] → sprawdź czy są dane → przetwórz kolejną porcję
       ↓
[Cleanup] → usuń trigger → wyślij mail „Zakończono”
```

**Kluczowa zasada:** Żaden pojedynczy moduł nie przekracza **3 minut** wykonania. Margines 3 minut chroni przed timeoutem, gdy Sheets spowolni z powodu przeciążenia.

**Rekomendowany wzorzec kodowy (szkielet):**

```javascript
const BATCH_SIZE = 500; // bezpieczna liczba wierszy na porcję

function processBatch() {
  const props = PropertiesService.getScriptProperties();
  const startIndex = Number(props.getProperty('lastIndex') || 1);
  const sheet = SpreadsheetApp.getActive().getSheetByName('Dane');
  const lastRow = sheet.getLastRow();

  if (startIndex > lastRow) {
    cleanupTriggers();
    return;
  }

  const endIndex = Math.min(startIndex + BATCH_SIZE - 1, lastRow);
  const data = sheet.getRange(startIndex, 1, endIndex - startIndex + 1, 5).getValues();

  // Przetwarzanie w pamięci
  const transformed = data.map(row => transformRow(row));

  // Jeden zapis wsadowy
  sheet.getRange(startIndex, 1, transformed.length, 5).setValues(transformed);

  props.setProperty('lastIndex', String(endIndex + 1));
}
```

---

## 7. CHIRURGICZNE PYTANIA KWALIFIKUJĄCE

Poniższe pytania należy wpleść **w środek analizy**, nie na końcu. Mają jedno zadanie: **zmusić zleceniodawcę do natychmiastowej odpowiedzi na priv**.

### Pytanie #1 — konta i limity
> „Czy zleceniodawca pracuje na koncie Google Workspace (firmowym), czy consumer (gmail.com)? Ma to bezpośredni wpływ na dzienny limit triggerów — 90 minut vs 6 godzin — i determinuje architekturę kolejkowania.”

**Cel:** Ustalenie typu konta przed wyceną. Uniknięcie wdrożenia niedziałającego u klienta.

### Pytanie #2 — skala danych
> „Ile wierszy/rekordów ma być przetwarzanych w jednym cyklu? Czy 5000 to wartość stała, czy rośnie w czasie? Przy jakim wolumenie obecny skrypt przestaje działać?”

**Cel:** Ustalenie rozmiaru batcha i liczby iteracji continuation triggers. Jeśli dane rosną — potrzebna architektura skalowalna, nie jednorazowa.

### Pytanie #3 — źródło danych i trigger
> „Skąd dokładnie pochodzą dane — z maila (`GmailApp`), z API zewnętrznego (`UrlFetchApp`), czy z innego arkusza? Czy obecny trigger jest czasowy, czy oparty na zdarzeniu (onEdit/onChange)?”

**Cel:** Dobór właściwego mechanizmu pobierania danych. `UrlFetchApp` wymaga kontroli partii; `GmailApp` wymaga paginacji; `onEdit` nie nadaje się do batch processingu.

### Pytanie #4 — tolerancja na opóźnienia
> „Czy przetwarzanie może trwać 15–30 minut w tle, pod warunkiem, że dane są kompletne i nikt nie ingeruje w arkusz w trakcie? Czy jest wymóg, aby całość zakończyła się w jednym oknie czasowym?”

**Cel:** Ustalenie, czy klient zaakceptuje architekturę „wolniej, ale niezawodnie” (batch processing) zamiast „szybko, ale ryzykownie” (próba zmieszczenia się w 6 minutach).

### Pytanie #5 — dostęp do API
> „Czy zleceniodawca posiada własne klucze API / tokeny do zewnętrznych systemów, czy integracja opiera się wyłącznie na tym, co jest dostępne w Workspace (Gmail, Drive, Sheets)?”

**Cel:** Ocena złożoności modułu M4 (integracje). Brak kluczy API = konieczność parsowania maili/PDF, co znacząco podnosi pracochłonność.

---

**Podsumowanie:** Oferta wygrywająca na Useme w 2026 roku nie mówi „znam Apps Script”. Mówi: „Wiem, gdzie pęknie Twój skrypt — na 6-minutowym wallu i pętli `setValue`. Mam architekturę, która to omija.” Reszta to już tylko wycena.