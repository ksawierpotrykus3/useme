```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (budowa systemu ETL) z potencjałem na retainer (ciągłe wzbogacanie/aktualizacja bazy)
INTENCJA: mieszane — projektowanie = doradcze, budowa/wdrożenie = wykonawcze
DECYDENT_I_BOL: osoba fizyczna lub mała firma ("pomóż mi"), buduje bazę B2B prawdopodobnie pod sprzedaż/outreach. Ból pod spodem: dane firm są rozproszone i brudne, ręczne pozyskiwanie zabija czas, poprzednie próby integracji "się sypały" (stąd fraza "systemy rozmawiają ze sobą bez błędu"). Szuka kogoś, kto to ogarnie end-to-end.
WYKONALNE: TAK — ale zależne od źródeł i skali. Najbliższa opcja: ETL z rejestrów publicznych (KRS / CEIDG / GUS BIR1 / REGON) + deduplikacja po NIP + standaryzacja pól, ewentualnie dodatkowe źródła komercyjne, jeśli klient je wskaże.
POLE_DO_POPISU: OGRANICZONE — dwie rzeczy wchodzą: (1) PKD 2025 jako pytanie/kontekst (klient nie podał wersji), (2) krajobraz polskich rejestrów — co darmowe, co płatne, jakie limity. Reszta researchu zostaje dla nas.
SCIEZKA_MERYTORYKI: A (klient wprost prosi o automatyzację i wzbogacanie) + B (PKD 2025 warunkowo jako mina — patrz niżej)
MINY_I_CIEKAWOSTKI:
- PKD 2025 (Rozporządzenie RM z 24.06.2024, Dz.U. 2024 poz. 1102) zastąpiło PKD 2007 od 1 stycznia 2025, okres przejściowy do 31.12.2026. Klient pisze "kody PKD" bez wersji — jeśli jego dane są w PKD 2007, filtr po PKD zwróci błędne wyniki albo w ogóle nie zadziała na nowych wpisach. Dowód: fraza "wyznaczonych kodów PKD" bez wskazania wersji. To warunkowe, więc idzie jako pytanie z kontekstem, nie jako teza.
ODMOWA: puste — brief nie zawiera twardej blokady. Żadna z okazji 1–6 nie zachodzi na tym etapie (brak nazwy systemu, brak liczby, brak API do zakwestionowania).
PYTANIA:
1. Skala — ile firm w bazie docelowej i jak często aktualizacja? Od tego zależy architektura (sync ciągły vs batch nocny) i koszt API (GUS BIR1 jest płatny per zapytanie, przy dużym wolumenie to realna pozycja w budżecie).
2. Źródła — z których rejestrów/API korzystacie lub chcecie korzystać? To determinuje wykonalność i koszt: KRS API darmowe ale ubogie w pola, CEIDG darmowe, GUS BIR1 płatne i limitowane, REGON z tokenem. Bez tej odpowiedzi wycena jest wróżeniem.
3. PKD — której wersji używacie: 2007 czy 2025? Od tego zależy mapowanie i filtrowanie; jeśli macie dane w 2007, trzeba dorobić słownik przejścia.
4. Cel końcowy — gdzie trafia gotowa baza (CRM, eksport CSV/Excel, panel www)? Determinuje format wyjściowy i to, czy w zakresie jest warstwa wizualna.
CO_ZLECENIE_MOWI: budowa bazy B2B firm, filtrowanie po PKD i parametrach biznesowych, automatyczne wzbogacanie z rejestrów/API, czyszczenie (mapowanie pól, dedup, standaryzacja). Budżet: do negocjacji.
CZEGO_NIE_MOWI: skala (ile firm, jak często), konkretne źródła/rejestry, wersja PKD, system docelowy (CRM? plik? panel?), czy dane już istnieją czy trzeba je pozyskać od zera, technologia, konkretny budżet.
GRANICA_CIECIA: krótka odpowiedź — brief jest ogólny (1 akapit, zero konkretów), więc odpowiedź też. Cztery pytania + szkic podejścia (ETL z rejestrów → staging → dedup po NIP → standaryzacja → target). Zero rozpisywania się o stacku bez danych o skali i źródłach.
RESEARCH_POTRZEBNY: TAK, lekki — sprawdzić aktualne limity i koszty API rejestrów (KRS, CEIDG, GUS BIR1, REGON) oraz status PKD 2025. Po to, żeby pytanie o źródła i PKD było oparte na faktach, nie na pamięci.
```