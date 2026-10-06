## 1. WCAG 2.2 AA a dokumenty PDF w archiwum ESPI/EBI

**Potwierdzone:** Standardy EN 301 549 i WCAG 2.2 AA obejmują **nie tylko strony internetowe, ale również dokumenty niebędące stronami** (non-web documents), takie jak PDF, udostępniane przez witrynę. Wprost wskazuje na to dokument czeskiego Ministerstwa Przemysłu i Handlu, powołujący się na wymogi EAA (European Accessibility Act) dla sektorów objętych regulacją, w tym **usług finansowych**: „webové stránky… včetně newebových dokumentů poskytovaných přes web (např. PDF)”. Dokument B tego samego resortu dodaje, że dla dokumentów ke stažení (PDF, MS Office) rekomendowanym trybem jest **PDF/UA**, a primárním formátem je HTML — PDF tylko tam, kde je to nezbytné.

**Wniosek dla miny:** Sama zgodność szablonu strony z WCAG 2.2 AA **nie wystarczy**, jeśli archiwum ESPI/EBI zawiera setki lub tysiące plików PDF bez remediacji. Formalny audyt dostępności obejmie również te pliki.

**Niepotwierdzone:** Czy polskie przepisy (ustawa o dostępności cyfrowej) nakładają na spółki publiczne konkretny obowiązek remediacji **historycznych** PDF-ów w archiwach ESPI/EBI — w dostępnych źródłach nie znalazłem jednoznacznego potwierdzenia w odniesieniu do tego konkretnego typu archiwum.

---

## 2. CMP a RODO w sektorze finansowym

**Potwierdzone:** Instytucje finansowe podlegają **surowszym wymogom** dotyczącym zgód niż większość innych branż, ze względu na wolumen i wrażliwość przetwarzanych danych (historia transakcji, dane kont, identyfikatory osobiste). RODO, ePrivacy Directive i CCPA nakładają obowiązek uzyskania zgody, która jest **informed, freely given, explicit, and easy to withdraw** — a CMP ma umożliwiać śledzenie, audyt i wykazanie ważności zgody w czasie rzeczywistym.

**Realny przykład kary:** Hiszpański organ ochrony danych (AEPD) nałożył na **Caixabank S.A.** karę **6 mln EUR** (później obniżoną do 2 mln EUR) za naruszenie art. 6, 13 i 14 RODO — bank wymagał akceptacji polityki prywatności pozwalającej na udostępnianie danych w ramach grupy **bez możliwości prostego opt-out** (rezygnacja wymagała wysłania osobnych listów do każdej spółki grupy).

**Wniosek dla miny:** Wdrożenie CMP „na szablonie” bez dostosowania do specyfiki sektora finansowego (wielość podstaw prawnych, odrębne zgody na przetwarzanie w celach marketingowych vs. niezbędność umowna) może skutkować karą i zakwestionowaniem ważności zgód.

---

## 3. Core Web Vitals i przekierowania 301 przy migracji

**Potwierdzone:** Każdy indeksowalny stary URL wymaga **pojedynczego przekierowania 301 (lub 308)** na poziomie serwera lub edge — łańcuchy przekierowań (2+ skoki) negatywnie wpływają na Core Web Vitals, w szczególności na **TTFB i FCP**, ponieważ każde przekierowanie dodaje opóźnienie sieciowe. Google potwierdza, że 301 nie powoduje utraty PageRank, ale błędna konfiguracja (np. staging robots.txt na produkcji) może doprowadzić do utraty **nawet 90% ruchu organicznego w ciągu 24 godzin**.

**Skala ryzyka:** Standardowy, tymczasowy spadek ruchu po migracji wynosi **10–30%** (praktyka branżowa), ale przy braku mapy przekierowań — zwłaszcza w archiwum z tysiącami unikalnych URL-i do PDF — może być znacznie większy. Checklisty migracyjne zalecają **pełny crawl starej witryny, eksport top 1000 URL-i z Search Console i mapowanie każdego starego URL na nowy** przed cutoverem.

**Wniosek dla miny:** Archiwum IR/ESPI/EBI to szczególnie ryzykowny obszar — wiele URL-i prowadzi bezpośrednio do PDF-ów, które mogą nie mieć odpowiedników w nowej strukturze. Bez inwentaryzacji i mapy 301 **utrata linków przychodzących i ruchu z wyszukiwarek jest wysoce prawdopodobna**.

**Niepotwierdzone:** Czy istnieją branżowe standardy (np. wytyczne GPW lub KNF) określające **minimalny zakres** mapy przekierowań dla archiwów ESPI/EBI — nie znalazłem takich źródeł.