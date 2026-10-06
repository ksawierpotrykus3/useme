=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena wstępna:** 5 400–9 000 zł (60–100 h × 90 zł/h). Przy większym wolumenie lub ciągłej synchronizacji do ok. 12 000 zł.  
**Czas:** 8–18 dni roboczych dla MVP; przy dużych bazach i stałej aktualizacji 3–5 tygodni.

**Uzasadnienie:** Zakres to ETL z rejestrów (KRS/CEIDG/GUS), dedup po NIP, standaryzacja i target. Rejestry są darmowe, ale mają wąskie gardła: CEIDG daje max 25 wyników/żądanie, GUS BIR1 wymaga rejestracji, a KRS nie szuka po NIP – dlatego wycena mocno zależy od skali i danych wejściowych.

**Brakuje mi:**  
1. Skali – ile firm docelowo i jak często aktualizacja.  
2. Źródeł wejściowych – lista NIP/KRS/nazw, czy zbieramy od zera.  
3. Targetu – plik/eksport, CRM, panel www.

Domyślnie zakładam: PKD 2025 + słownik 2007↔2025, dedup po NIP, staging → target.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Wycena się broni — 60–100 h na ETL z trzema rejestrami, dedupem po NIP i standaryzacją to realistyczny przedział dla MVP, a widełki 5 400–9 000 zł uczciwie oddają niepewność skali. Nie zgadywałem w ofercie: hipotezy o „poprzednich próbach” i celu sprzedażowym zostawiłem w dzienniku, PKD 2025 to nie mina tylko obowiązujący stan prawny, a wąskie gardła GUS/CEIDG wchodzą jako uzasadnienie wyceny, nie jako straszenie klienta. Jedyne, co bym dopisał wprost w ofercie, to zdanie, że jeśli input to nazwy firm (nie NIP/KRS), dochodzi 20–40 h na fuzzy matching — bez tego zakres może puchnąć w trakcie. Kwoty nie zmieniam na tym etapie, ale przy odpowiedzi klienta o źródłach wejściowych zawęziłbym widełki, a nie rozszerzał. Research był lekki i zgodny z dziennikiem — nie rozdmuchałem go ponad potrzebę.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna: 6 000 – 10 000 zł** (66–111 h × 90 zł), **10–20 dni roboczych**.

**Uzasadnienie:** Zakres rozumiem jako pipeline ETL: pobranie z rejestrów (KRS/CEIDG/GUS BIR1) → dedup po NIP → standaryzacja pól → target. Widełki są szerokie, bo skala decyduje o architekturze — sync ciągły vs. batch nocny, a przy dużych wolumenach limity CEIDG (25 wyników/żądanie) i rejestracja GUS BIR1 (nie-self-serve, kilka dni oczekiwania) stają się realnym wąskim gardłem. Do tego dochodzi projekt struktury bazy pod filtrowanie po PKD.

**Czego brakuje w zleceniu (potrzebuję do doprecyzowania wyceny):**
1. **Skala** — ile firm docelowo w bazie i jak często aktualizacja?
2. **Źródła wejściowe** — lista NIP/KRS/nazw, czy zbieramy od zera? (KRS API nie szuka po NIP — przy liście NIP-ów konieczny REGON jako pośrednik.)
3. **Target** — gdzie trafia gotowa baza: plik, CRM, panel www?

**Propozycje domyślne (jeśli brak info):** PKD 2025 z dorobionym słownikiem 2007↔2025 (przejściowy do 31.12.2026), dedup po NIP, staging przed target, stack dobrany do wolumenu po punkcie 1.

Po odpowiedziach na te 3 punkty zawężę widełki do konkretnej kwoty.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Wycena 6–10k przy nieznanej skali to uczciwy strzał w ciemno, ale **dolna granica jest prawdopodobnie zaniżona** — przy 100k+ firm i aktualizacji ciągłej sama obsługa limitów CEIDG (25 rekordów/żądanie = tysiące wywołań) to kilka dni samego inżynierstwa, nie licząc dedupu i standaryzacji. Rejestracja GUS BIR1 (kilka dni oczekiwania, podanie IP) **nie zjada moich godzin, ale zjada termin** — 10–20 dni roboczych może być nierealne, jeśli klient zwleka z wnioskiem; powinienem to zaznaczyć jako zależność, nie ryzyko wykonawcze. PKD 2025 + słownik 2007↔2025 to sensowna propozycja domyślna, ale **nie mina** — jeśli klient ma dane w 2025, słownik jest zbędny i nie powinien być wliczany w zakres bez potwierdzenia. Nie zgadłem jednej rzeczy: **retainer na aktualizację** — to naturalny ciąg dalszy i powinienem był wspomnieć, że wycena go nie obejmuje. Kwoty nie koryguję w górę na zapas, bo bez odpowiedzi na 3 pytania każda zmiana to wróżenie — ale jeśli skala okaże się duża, **widełki zawężą się w stronę 12–15k**, nie 6k.

=== DeepSeek-C — RUNDA 1 ===
## Wycena

**Widełki: 6 500 – 10 000 zł** (72–110 h × 90 zł/h)
**Czas: 10–15 dni roboczych** od zebrania wymagań i dostępów.

### Uzasadnienie
Zakres to klasyczny pipeline ETL: pobranie z rejestrów (KRS/CEIDG/GUS BIR1), dedup po NIP, standaryzacja pól, wzbogacanie i eksport do targetu — plus słownik PKD 2007↔2025, bo stary i nowy schemat będą współistnieć do końca 2026 r. Górna granica widełek wynika z wąskich gardeł: CEIDG zwraca max 25 wyników na żądanie, KRS API nie szuka po NIP (potrzebny REGON jako pośrednik), a rejestracja GUS BIR1 nie jest self-serve (kilka dni na klucz + IP). Dolna granica to MVP na małej skali i prostym eksporcie.

### Czego brakuje w zleceniu (3 pytania)
1. **Skala** — ile firm docelowo i jak często aktualizacja? Determines czy limity CEIDG (~24k/dzień) i GUS są wąskim gardłem.
2. **Punkt startu** — masz już listę NIP-ów, KRS-ów, nazw, czy zbieramy od zera? To zmienia całą architekturę (KRS API wymaga KRS, nie NIP).
3. **Target** — gdzie ma trafiać gotowa baza: CSV/Excel, CRM, panel www? Determinuje warstwę wyjściową i czy w zakresie jest UI.

### Domyślnie zakładam
PKD 2025 jako podstawę + słownik z 2007; dedup po NIP; warstwa staging przed targetem; batch nocny (nie sync ciągły).

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: górna granica 10 000 zł / 110 h jest naciągnięta — nie mam dowodu na tyle komplikacji, więc to paddowanie na wypadek złych odpowiedzi, nie realna stawka. Realistycznie dla kogoś, kto robił już ETL na tych API, MVP (3 rejestry → dedup → standaryzacja → eksport) to 45–65 h, czyli **4 000–6 000 zł** przy 90 zł/h. Research potwierdził, że wszystkie rejestry są darmowe i limity są hojne — to obniża ryzyko, nie podnosi. Zgadłem też dwie rzeczy bez dowodu: PKD 2025 jako domyślne (może klient ma 2007) i batch nocny (może chce sync). **Korekta: widełki 4 500 – 7 000 zł, 50–78 h, z zastrzeżeniem, że powyżej 5 000 firm lub sync ciągły → osobna wycena.** Górna granica z poprzedniej wyceny była obroną przed nieznanym, nie wyceną pracy.

=== DeepSeek-D — RUNDA 1 ===
## Wycena wstępna

**Kwota:** 4 500 – 8 500 zł (umowa o dzieło)
**Czas:** 10–18 dni roboczych (zależnie od zakresu i tempa odpowiedzi po stronie klienta)

**Uzasadnienie:** Zakres to pipeline ETL z trzech rejestrów (KRS, CEIDG, GUS BIR1) + dedup po NIP + standaryzacja + słownik PKD 2007↔2025 — sama integracja z GUS BIR1 to kilka dni oczekiwania na klucz i adresy IP, a CEIDG wymusza paginację po 25 rekordów. Widełki wynikają z niewiadomej skali: przy kilku tysiącach firm limity API nie bolą, przy dziesiątkach tysięcy trzeba dorobić kolejkę i batch nocny. Do tego dochodzi warstwa docelowa (plik vs CRM vs panel), której nie znam.

**Czego brakuje w zleceniu:**
1. **Skala** — ile firm docelowo i jak często aktualizacja? Od tego zależy, czy limity CEIDG (1 000/h) i GUS (6 000/h) są wąskim gardłem.
2. **Źródła wejściowe** — startujemy z listy NIP, KRS, nazw firm, czy zbieramy od zera? KRS API nie szuka po NIP — jeśli masz NIP-y, REGON jest koniecznym pośrednikiem.
3. **Target** — gdzie ma trafiać gotowa baza: plik/eksport, CRM, panel www? Determinuje format wyjściowy i czy w zakresie jest warstwa wizualna.

**Założenia domyślne (do potwierdzenia):** PKD 2025 z dorobionym słownikiem 2007↔2025, dedup po NIP, staging przed targetem, stack dobrany do wolumenu po odpowiedzi na pytanie 1.

Po trzech odpowiedziach zawężam do konkretnej kwoty.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: wycena jest obroniona, ale dolna granica 4 500 zł jest zbyt optymistyczna, jeśli klient ma dziesiątki tysięcy rekordów albo target to CRM/panel — wtedy same kolejkowanie, retry i warstwa docelowa zjadają 30–40 h. Górna granica 8 500 zł też może być za niska przy dużym wolumenie i integracji z systemem klienta — realnie widełki powinny być **5 500–12 000 zł**, z zastrzeżeniem, że dokładna kwota zależy od odpowiedzi na trzy pytania. Nie zgadłem na siłę niczego — PKD 2025 słusznie zostało propozycją, nie miną, bo nie mam dowodu na dane w 2007. Czas 10–18 dni roboczych zawiera bufor na rejestrację GUS BIR1 (kilka dni oczekiwania, nie pracy), co jest uczciwe. Jedyne, co bym zmienił, to dopisać wprost w wycenie, że **dolna granica dotyczy kilku tysięcy rekordów i prostego eksportu CSV** — bez tego klient może uznać 4 500 zł za cenę za pełny zakres.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 5500,
  "kwota_gorna": 10000,
  "definitywna": false,
  "od_czego_zaleza": [
    "Skala bazy (liczba firm) i częstotliwość aktualizacji — batch nocny vs sync ciągły; powyżej ~5 000 firm limity CEIDG (25 rekordów/żądanie) i GUS stają się wąskim gardłem",
    "Źródła wejściowe — lista NIP/KRS/nazw czy zbieranie od zera; przy NIP-ach konieczny REGON jako pośrednik (KRS API nie szuka po NIP), przy nazwach dochodzi 20–40 h na fuzzy matching",
    "Target — plik/CSV, CRM czy panel www; integracja z systemem klienta lub warstwa wizualna podnoszą zakres i czas",
    "Zakres wzbogacania i liczby zewnętrznych API/rejestrów do podłączenia"
  ],
  "dni_od": 10,
  "dni_do": 20,
  "uzasadnienie": "Wszystkie cztery modele zgodnie wskazują ten sam zakres (ETL z KRS/CEIDG/GUS BIR1 → dedup po NIP → standaryzacja → target) i te same wąskie gardła: limit 25 rekordów/żądanie w CEIDG, brak lookupu po NIP w KRS API, nie-self-serve rejestracja GUS BIR1. Zbieżność po rundzie 2 jest wyraźna w dolnej granicy (ok. 5 400–6 000 zł, po autokorekcie C zszedł do 4 500, D podniósł do 5 500) i górnej (7 000–12 000 zł, przy medianie ok. 9 500–10 000). Rozbieżność dotyczy głównie tego, jak mocno wyceniać bufor na nieznaną skalę — C ściął wycenę do 4 500–7 000 zł, uznając że limity API są hojne i ryzyko niskie, natomiast D podniósł do 5 500–12 000 zł z uwagi na możliwy duży wolumen i integrację z CRM. Wybrana kwota 5 500–10 000 zł to środek ciężkości obu rund, z zachowaniem zastrzeżenia, że przy >5 000 firm lub sync ciągłym widełki idą w stronę 12–15 tys. Wycena nie jest definitywna, bo brakuje skali, źródeł wejściowych i targetu — bez nich każde zawężenie byłoby zgadywaniem."
}

=== FINALNA WYCENA ===
5500-10000 zl netto | 10-20 dni | WIDELKI
Od czego zalezy: Skala bazy (liczba firm) i częstotliwość aktualizacji — batch nocny vs sync ciągły; powyżej ~5 000 firm limity CEIDG (25 rekordów/żądanie) i GUS stają się wąskim gardłem, Źródła wejściowe — lista NIP/KRS/nazw czy zbieranie od zera; przy NIP-ach konieczny REGON jako pośrednik (KRS API nie szuka po NIP), przy nazwach dochodzi 20–40 h na fuzzy matching, Target — plik/CSV, CRM czy panel www; integracja z systemem klienta lub warstwa wizualna podnoszą zakres i czas, Zakres wzbogacania i liczby zewnętrznych API/rejestrów do podłączenia
Uzasadnienie rozjemcy: Wszystkie cztery modele zgodnie wskazują ten sam zakres (ETL z KRS/CEIDG/GUS BIR1 → dedup po NIP → standaryzacja → target) i te same wąskie gardła: limit 25 rekordów/żądanie w CEIDG, brak lookupu po NIP w KRS API, nie-self-serve rejestracja GUS BIR1. Zbieżność po rundzie 2 jest wyraźna w dolnej granicy (ok. 5 400–6 000 zł, po autokorekcie C zszedł do 4 500, D podniósł do 5 500) i górnej (7 000–12 000 zł, przy medianie ok. 9 500–10 000). Rozbieżność dotyczy głównie tego, jak mocno wyceniać bufor na nieznaną skalę — C ściął wycenę do 4 500–7 000 zł, uznając że limity API są hojne i ryzyko niskie, natomiast D podniósł do 5 500–12 000 zł z uwagi na możliwy duży wolumen i integrację z CRM. Wybrana kwota 5 500–10 000 zł to środek ciężkości obu rund, z zachowaniem zastrzeżenia, że przy >5 000 firm lub sync ciągłym widełki idą w stronę 12–15 tys. Wycena nie jest definitywna, bo brakuje skali, źródeł wejściowych i targetu — bez nich każde zawężenie byłoby zgadywaniem.
