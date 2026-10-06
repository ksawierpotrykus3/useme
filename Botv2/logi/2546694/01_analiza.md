```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (z możliwym trybem cyklicznym — nowe wersje APK w czasie)
INTENCJA: wykonawcze
DECYDENT_I_BOL: nieznany — ogłoszenie bezosobowe, brak nazwy firmy. Ból pod spodem: audyt licencyjny fontów w aplikacjach / IP-compliance / brand monitoring. Nie nazwany wprost, więc NIE wpisujemy go do oferty jako pewnika.
WYKONALNE: TAK. Najbliższa opcja: scraper + rekurencyjny unpacker + parser fontów + panel web (Django/Flask + kolejka zadań). Warunek — zależny od pytania 1.
POLE_DO_POPISU: JEST. Trzy rzeczy, o których klient nie wie, a które decydują o wyniku: (a) APK to ZIP, ale wewnątrz siedzą JAR/AAR/nested ZIP, split APK i XAPK — bez rekurencji fontów nie wyciągniesz; (b) część fontów jest subsetowana lub ma obfuskowane nazwy — „nazwa fontu" z metadanych bywa pusta, trzeba fallbacku po stronie pliku; (c) fonty bywają wkładane do native libs / assets z losową nazwą.
SCIEZKA_MERYTORYKI: B (mina warunkowa — zależna od serwera) + C (propozycja rekurencyjnego rozpakowania z fallbackiem nazw). NIE wchodzi na siłę jako pewnik — wchodzi po pytaniu 1.
MINY_I_CIEKAWOSTKI:
  - M1 (warunkowa): „wskazany serwer" — jeśli to Google Play → brak publicznego API, download wymaga Play Store, ToS zabrania scrapingu, AAB/split APK zamiast pełnego APK. Dowód: samo słowo „serwer" nie jest nazwane. Bez nazwy NIE twierdzę — zamieniam na pytanie.
  - C1 (ciekawostka): „wszystkie wewnętrzne archiwa" — klient prawdopodobnie nie wie, jak głęboko to idzie. Wchodzi jako propozycja w ofercie, nie jako zarzut.
ODMOWA: warunkowa — tylko jeśli serwer okaże się Google Play. Wtedy: typ 1 (brak kanału dostępu) + typ 4 (ToS/zgodność). Mechanizm: GP nie wystawia APK publicznie, konto dewelopera nie daje downloadu innym. Konsekwencja: projekt nie ruszy jako „scraper". Alternatywa: APKPure/APKMirror (publiczne, ale nieregularne) ALBO własny serwer klienta ALBO lista APK dostarczona przez klienta. Bez tej wiedzy — odmowy NIE piszemy.
PYTANIA (4 — wielowarstwowe):
  1. Który to serwer? (Google Play / APKPure / APKMirror / serwer klienta / inny). Uzasadnienie: od tego zależy kanał dostępu, metoda pobierania i czy w ogóle da się to zrobić legalnie i stabilnie. Odpowiedź zmienia architekturę i cenę.
  2. Ile kont deweloperów i rząd wielkości — dziesiątki, setki, tysiące aplikacji? Uzasadnienie: od skali zależy infrastruktura (kolejka, retry, storage) i czas realizacji. Bez tego nie da się podać widełek sensownie.
  3. „Metadane fontu" — konkretnie co ma być w kolumnach? (nazwa, rodzina, wersja, copyright, licencja, format pliku?). Uzasadnienie: metadane TTF/OTF siedzą w name table, ale zakres pól decyduje o parserze. Proponuję domyślnie: nazwa + rodzina + wersja + copyright + ścieżka — jeśli pasuje, nie trzeba odpowiadać.
  4. Jednorazowo czy cyklicznie (nowe wersje aplikacji co jakiś czas)? Uzasadnienie: tryb jednorazowy = skrypt + raport; cykliczny = harmonogram, diff, powiadomienia — inna architektura i inna cena.
CO_ZLECENIE_MOWI: lista kont deweloperów; scraper pobiera APK; rozpakowanie APK + archiwów wewnętrznych; ekstrakcja fontów; raport XLSX (nazwa app, nazwa fontu, metadane, lokalizacja w APK); preferencja web.
CZEGO_NIE_MOWI: nazwy serwera; liczby deweloperów; definicji „metadanych"; formatu docelowego webu (panel? API? jednorazowy upload?); czy zadanie ma być powtarzalne; RODO/praw autorskich do ekstrahowanych fontów (istotne, ale poza granicą briefu — nie dopisuję).
GRANICA_CIECIA: 4 pytania (multi-layer: serwer + skala + metadane + tryb). W ofercie: 2-3 zdania propozycji technicznej (rekurencyjny unpack + parser name table + panel web) + 4 pytania. Bez wycieczek o RODO/AI Act — poza granicą.
RESEARCH_POTRZEBNY: TAK — po odpowiedzi na pytanie 1 sprawdzić realny kanał dostępu do APK na wskazanym serwerze (publiczne API / scraping HTML / brak dostępu) oraz typowy format zwracanych paczek (APK vs XAPK vs split APK vs AAB).
```