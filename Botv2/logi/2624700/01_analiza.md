KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy / etapowy (wdrożenie aplikacji webowej)
INTENCJA: wykonawcze (z elementem doradczym: etapowanie i wycena)
DECYDENT_I_BOL: Firma z dystrybucji wody; decydent nieznany – prawdopodobnie właściciel / manager operacyjny / IT. Ból: rozproszone zarządzanie zamówieniami, trasami, magazynem i kierowcami; potrzeba jednego systemu od zamówienia do raportu.
WYKONALNE: TAK. Stack Java/Spring Boot, React, PostgreSQL, własny serwer. Najbliższa opcja: wdrożenie etapowe zamiast „pełnej funkcjonalności od pierwszego wdrożenia” – to zmniejsza ryzyko i pozwala wycenić zakres.
POLE_DO_POPISU: JEST. Etapowanie, architektura ról, planowanie tras, powiadomienia, raporty. Wchodzi przez A, bo klient wprost pyta o wycenę, czas, etapy i portfolio.
SCIEZKA_MERYTORYKI: A (klient pyta o wycenę, czas, etapy, portfolio). B/C brak.
MINY_I_CIEKAWOSTKI: Ciekawostka: klient pisze „pełna funkcjonalność od pierwszego wdrożenia”, ale równocześnie „podział na etapy mile widziany”. To nie mina, tylko zaproszenie do zaproponowania etapów.
ODMOWA: brak
PYTANIA:
1. Czy możemy dostać dostęp do Figmy i specyfikacji wymagań? – pytam, bo bez nich nie da się rzetelnie wycenić ani zaproponować etapów; to jedyne źródło pełnego zakresu.
2. Planowanie tras ma być ręczne z panelem dyspozytora, czy automatyczna optymalizacja? Jeśli automatyczna – z jakim API map? – pytam, bo to największy mnożnik pracochłonności i architektury.
3. Powiadomienia o zmianach statusu: tylko in-app, e-mail, SMS, push? – pytam, bo SMS/push wymagają zewnętrznych dostawców, kosztów i konfiguracji.
4. Czy aplikacja ma integrować się z istniejącym systemem zamówień, magazynu, księgowości lub map? Jeśli tak – jakie API? – pytam, bo każda integracja to osobny moduł i ryzyko.
Poza tym TYP 2: etapowanie, domyślny deploy Docker/Linux, architektura ról – proponujemy, nie pytamy.
CO_ZLECENIE_MOWI: wewnętrzna aplikacja webowa do zarządzania dostawami wody; stack Java/Spring Boot, React, PostgreSQL; wdrożenie na własnym serwerze; responsywność; moduły: zamówienia, trasy, klienci, magazyn, panel dyspozytora, lista kierowcy, role admin/dyspozytor/kierowca, powiadomienia, raporty; klient dostarcza Figmę i specyfikację; oczekuje wyceny, czasu, portfolio i propozycji etapów.
CZEGO_NIE_MOWI: kto jest decydentem; konkretnego budżetu; czy planowanie tras jest automatyczne czy ręczne; kanałów powiadomień; integracji zewnętrznych; wolumenu użytkowników/zamówień/dostaw; szczegółów serwera; czy Figma i specyfikacja są kompletne i dostępne; terminu; czy są etapy akceptacyjne.
GRANICA_CIECIA: Zlecenie obszerne, ale bez kluczowych parametrów. Odpowiedź średnia: 4 pytania + propozycja etapów. Nie wchodzić w szczegóły implementacji, dopóki nie zobaczymy Figmy i specyfikacji.
RESEARCH_POTRZEBNY: TAK (lekki) – po odpowiedziach: API map, dostawcy SMS/push, integracje. Na tym etapie brak nazw systemów, więc twardy research nie jest możliwy.