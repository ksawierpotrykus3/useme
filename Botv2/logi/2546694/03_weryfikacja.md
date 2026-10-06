```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (możliwy tryb cykliczny — nowe wersje APK w czasie; do rozstrzygnięcia pytaniem)
INTENCJA: wykonawcze
DECYDENT_I_BOL: nieznany — ogłoszenie bezosobowe, brak nazwy firmy. Ból pod spodem: audyt licencyjny fontów / IP-compliance. NIE nazwany wprost → NIE wpisujemy jako pewnika do oferty. Research nie zmienia tego ustalenia.
WYKONALNE: TAK — pod warunkiem że serwer nie narzuca kanału niedostępnego bez konta. Najbliższa opcja: scraper/pobieracz + rekurencyjny unpacker (APK→ZIP→JAR/AAR/XAPK/APKM/split APK) + parser fontów (name table TTF/OTF) + panel web z kolejką zadań. Research potwierdza, że rekurencja jest konieczna na każdym z trzech głównych serwerów.
POLE_DO_POPISU: JEST — ale WĘŻSZE niż w iteracji 1. Tylko to, co potwierdzone:
  (a) APK to ZIP; XAPK (APKPure) i APKM (APKMirror) to ZIP-y zawierające base APK + split APK + OBB — bez rekurencji część fontów wypada. Research: tak, wprost.
  (b) split APK / AAB oznacza brak jednego pliku do analizy — trzeba scalać paczki per konfiguracja. Research: tak.
  WYCINAM z iteracji 1: „subsetowane/obfuskowane fonty" i „fonty w native libs z losową nazwą" — brak dowodu w briefie i w researchu. To było zgadywanie.
SCIEZKA_MERYTORYKI: C (udowodniona alternatywa — rekurencyjny unpack + fallback ścieżek fontów, oparta na faktach o formacie APK, nie o serwerze klienta). B (mina o serwerze) wchodzi DOPIERO po odpowiedzi na Q1 — bez nazwy serwera nie mam dowodu, na którym mógłbym postawić minę.
MINY_I_CIEKAWOSTKI:
  - C1 (ciekawostka, dowód: research): „wszystkie wewnętrzne archiwa" — na APKPure/APKMirror to nie APK, a XAPK/APKM (ZIP w ZIP-ie). Nazywam to wprost, żeby klient wiedział, że rozumiem głębokość zadania. Wchodzi jako propozycja techniczna, nie jako zarzut.
  - M1 (mina, WARUNKOWA — dopiero po Q1): jeśli serwer = Google Play → brak publicznego API, wszystkie narzędzia nieoficjalne i wymagają konta Google (OAuth → token AAS), endpointy prywatne i mogą się zmienić bez ostrzeżenia, format to split APK. Research: potwierdzone. UWAGA: NIE mówię „ToS zabrania scrapingu" — research tego nie potwierdza cytatem. Mówię tylko o braku publicznego kanału i zależności od konta.
ODMOWA: w iteracji 1 była za mocna. Korekta:
  - Jeśli serwer = Google Play → to NIE jest automatyczna odmowa, to mina. Realnie da się pobrać przez konto Google klienta. Odmowa zachodzi tylko jeśli klient DODATKOWO zażąda stabilnego, legalnego, produkcyjnego kanału bez własnego konta i bez ryzyka zmian — wtedy: typ 1 (brak kanału dostępu). Alternatywa: APKPure / APKMirror (publiczne, ale niestabilne — Cloudflare, rate limit) ALBO klient dostarcza APK sam ALBO akceptuje szarą strefę.
  - Typ 4 (ToS) — WYCINAM, brak dowodu.
  - Bez nazwy serwera odmowy NIE piszemy.
PYTANIA (3 pytania TYP 1 + 1 propozycja z domyślnym wariantem):
  1. Który to serwer? (Google Play / APKPure / APKMirror / własny klienta / inny). Uzasadnienie: trzy główne serwery mają różne kanały dostępu i różne formaty paczek (APK / XAPK / APKM / split APK / AAB) — od tego zależy i architektura, i cena, i ryzyko. Research: potwierdzone, że różnice są realne i nie da się ich zgadnąć.
  2. Skala — ile kont deweloperów i rząd wielkości (dziesiątki / setki / tysiące aplikacji)? Uzasadnienie: od skali zależy storage, kolejka, retry, czas realizacji. Bez tego widełki byłyby strzelaniem.
  3. Jednorazowo czy cyklicznie (nowe wersje w czasie)? Uzasadnienie: jednorazowo = skrypt + raport; cyklicznie = harmonogram + diff + powiadomienia — inna architektura i inna cena.
  PROPOZYCJA (TYP 2, nie pytanie): metadane fontu — domyślnie proponuję nazwa + rodzina + wersja + copyright + ścieżka w APK. „Jeśli pasuje, nie trzeba odpowiadać; jeśli chcecie inny zakres — dostroję." To nie pytanie, to propozycja z zastrzeżeniem.
  WYCINAM pytanie z iteracji 1: „preferuje webowo" — to TYP 2, proponuję panel web + upload listy + download XLSX jako domyślne, nie pytam.
CO_ZLECENIE_MOWI: lista kont deweloperów; scraper pobiera APK; rozpakowanie APK + wszystkich wewnętrznych archiwów; ekstrakcja fontów; raport XLSX (nazwa app, nazwa fontu, metadane, lokalizacja w APK); preferencja web.
CZEGO_NIE_MOWI: nazwy serwera; liczby deweloperów; definicji „metadanych"; formatu docelowego webu (panel? API? upload?); czy zadanie ma być powtarzalne; statusu prawnego ekstrahowanych fontów (poza granicą briefu — nie dopisuję).
GRANICA_CIECIA: 3 pytania TYP 1 + 1 propozycja domyślna + 2 zdania popisu technicznego (rekurencyjny unpack + parser + panel web). Bez wycieczek o RODO/AI Act. Bez pytań o budżet. Bez „zadzwońmy".
RESEARCH_POTRZEBNY: TAK — po Q1 sprawdzić konkretny kanał dostępu dla wskazanego serwera (publiczne API / scraping HTML / wymóg konta) oraz dominujący format paczek. Research z iteracji 1 pokrył już mapę ogólną i wystarcza do sformułowania pytań.
DECYZJE:
  DOPISAĆ: nic nowego poza tym, co już jest w polu POLE_DO_POPISU (wersja węższa). Wyciąć z popisu obfuskację/subsetowanie fontów i native libs — brak dowodu.
  ODPOWIEDZIEĆ: 2 zdania propozycji technicznej (APK=ZIP, XAPK/APKM/split APK → rekurencyjny unpack z fallbackiem ścieżek `res/font` i `assets`) + propozycja domyślnych kolumn metadanych + deklaracja: panel web z uploadem listy deweloperów i eksportem XLSX. Widełki cenowe po odpowiedziach na Q1-Q3.
  DOPYTAĆ: Q1 (serwer), Q2 (skala), Q3 (tryb jednorazowy/cykliczny).
```