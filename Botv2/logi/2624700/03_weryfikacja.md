```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (z etapowaniem) — budowa aplikacji webowej
INTENCJA: wykonawcze z elementem doradczym (klient sam prosi o propozycję etapów i wycenę)
DECYDENT_I_BOL: Firma dystrybucyjna (woda); decydent nieznany — prawdopodobnie właściciel / manager operacyjny. Ból: rozproszone zarządzanie zamówieniami, trasami, magazynem i kierowcami; potrzeba jednego systemu od zamówienia do raportu. Ból nazwany wprost przez klienta („pełen proces zarządzania dostawami”), nie domysł.
WYKONALNE: TAK. Stack Java/Spring Boot, React, PostgreSQL, własny serwer — spójny i wykonalny. Najbliższa opcja: wdrożenie etapowe zamiast „pełnej funkcjonalności od pierwszego wdrożenia”.
POLE_DO_POPISU: JEST, ale wąskie. Klient wprost prosi o: wycenę, czas, etapy, portfolio. To ścieżka A. Nie ma pola na miny (brak nazw systemów, brak liczb). Etapowanie to nasza propozycja (TYP 2), nie rewelacja.
SCIEZKA_MERYTORYKI: A (klient pyta wprost o wycenę, czas, etapy, portfolio).
MINY_I_CIEKAWOSTKI: BRAK MIN. Jest jedno napięcie: „pełna funkcjonalność od pierwszego wdrożenia” vs „podział na etapy mile widziany”. To nie mina — to sprzeczność życzeń, którą rozstrzygamy propozycją (TYP 2): proponujemy etapowanie jako realizację „pełnej funkcjonalności” w bezpiecznej kolejności. Nie straszymy, nie negujemy.
ODMOWA: BRAK. Żadna z 6 okazji nie zachodzi z dowodem ze zlecenia:
- brak kanału dostępu — nie znamy systemów, nie ma nazw,
- twardy limit — nie ma liczb ani API,
- konflikt zakresu — stack spójny z celem, brak narzuconej technologii sprzecznej z celem,
- zgodność — RODO/WCAG mogą się pojawić, ale to nie jest blokada, tylko zakres do zaproponowania,
- nieistniejący termin — brak nazw funkcji,
- bariera autorska — brak.
Uwaga: gdyby klient odpowiedział, że chce integracji z Symfonią/Comarch/KSeF — wtedy wchodzi okazja #1 (kanał dostępu: WebAPI za paywallem/licencją). Na razie — cisza.
PYTANIA:
1. Czy Figma i specyfikacja są już kompletne i obejmują wszystkie moduły z ogłoszenia (panel dyspozytora, listę kierowcy, raporty)? — pytam, bo od kompletności makiet zależy, czy wycena etapu 1 jest wiążąca, czy wymaga dopłaty za projektowanie brakujących widoków.
2. Planowanie tras: dyspozytor układa trasy ręcznie, czy system ma optymalizować automatycznie? — pytam, bo automatyczna optymalizacja to osobny moduł z zewnętrznym API map (koszt abonamentowy + koszt per request), a ręczne planowanie to zwykły CRUD. To największy pojedynczy mnożnik wyceny w tym zleceniu.
3. Powiadomienia o zmianach statusu: wystarczą in-app (w aplikacji), czy potrzebne e-mail / SMS / push? — pytam, bo SMS to koszt zmienny od wolumenu (przy braku danych o liczbie dostaw/dzień nie da się go oszacować), a push wymaga konfiguracji Firebase po stronie klienta.
4. Czy aplikacja ma się integrować z jakimkolwiek istniejącym systemem (ERP, księgowość, system zamówień, mapy) czy startuje jako samodzielna? — pytam, bo każda integracja to osobny moduł i osobne ryzyko; jeśli startuje samodzielnie, wycena etapu 1 jest dużo prostsza.

Poza tym TYP 2 (proponujemy, nie pytamy): etapowanie prac, konteneryzacja (Docker), architektura ról (admin/dyspozytor/kierowca), domyślny kanał powiadomień in-app z możliwością rozszerzenia.
CO_ZLECENIE_MOWI: wewnętrzna aplikacja webowa do zarządzania dostawami wody; stack Java/Spring Boot, React, PostgreSQL; wdrożenie na własnym serwerze; responsywność; moduły: zamówienia, trasy, klienci, magazyn, panel dyspozytora, lista kierowcy, role admin/dyspozytor/kierowca, powiadomienia, raporty; klient dostarcza Figmę i specyfikację; oczekuje wyceny, czasu, portfolio i propozycji etapów. Budżet „do negocjacji”.
CZEGO_NIE_MOWI: kto jest decydentem; budżetu liczbowego; czy planowanie tras jest ręczne czy automatyczne; kanałów powiadomień; integracji zewnętrznych; wolumenu użytkowników/zamówień/dostaw; szczegółów serwera (OS, konteneryzacja); czy Figma i specyfikacja są kompletne; terminu; etapów akceptacyjnych; czy istnieje obecny system, z którego migrujemy.
GRANICA_CIECIA: Zlecenie wielowarstwowe (moduły: zamówienia / trasy / magazyn / role / powiadomienia / raporty). Odpowiedź średnia: 4 pytania + propozycja etapów + wycena widełkowa lub „od”. Bez wchodzenia w implementację, dopóki nie zobaczymy Figmy i specyfikacji. Research (mapy, SMS, ERP) zostaje u nas — do oferty wchodzi tylko wtedy, gdy klient odpowie, że chce automatycznej optymalizacji lub integracji.
RESEARCH_POTRZEBNY: TAK, ale tylko jako przygotowanie do rozmowy po odpowiedziach. Na tym etapie research nie zmienia oferty, bo klient nie potwierdził ani optymalizacji tras, ani SMS, ani integracji ERP. Fakty zebrane (Google Maps Platform, Mapbox Optimization, Twilio SMS PL, FCM, Symfonia WebAPI) trzymamy w pogotowiu — wejdą do oferty tylko warunkowo: „jeśli planowanie ma być automatyczne, to…”, „jeśli powiadomienia SMS, to…”. Bez potwierdzenia — nie piszemy.

---

DECYZJE:
- DOPISAĆ do oferty: propozycję podziału na etapy (klient wprost o to prosi), widełkową wycenę z zaznaczeniem, że po zobaczeniu Figmy i specyfikacji zaokrąglimy do konkretu, portfolio link.
- ODPOWIEDZIEĆ: 4 pytania powyżej (Figma, trasy, powiadomienia, integracje) — wplecione po propozycji etapów, nie zamiast niej.
- DOPYTAĆ: tylko to, co realnie zmienia wycenę. Nie pytać o budżet, termin, wolumen (nie blokują wyceny etapowej), nie pytać o stack (klient podał), nie pytać o role (klient podał).
```