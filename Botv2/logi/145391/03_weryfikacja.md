```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (naprawa błędu + replikacja na drugą platformę)
INTENCJA: wykonawcze
DECYDENT_I_BOL: Firma/agencja obsługująca klientów na Subiekt+WooCommerce. Ból: koszt przesyłki nie trafia do dokumentu w Subiekcie → niepełne dane w ERP, problemy z dokumentacją/księgowością. Decydent prawdopodobnie techniczny (ma kod, wie co to Sfera).
WYKONALNE: TAK — pod warunkiem dostępu do kodu i środowiska Subiekta. Jeśli platformy mają różne wersje Subiekta (GT vs nexo), "skopiowanie" może wymagać adaptacji, nie kopiowania 1:1 — to jest do rozstrzygnięcia, nie do założenia.
POLE_DO_POPISU: NIE MA na podstawie ogłoszenia. Research nie dał dowodu ze zlecenia — dał ogólną wiedzę o Sferze i o potencjalnym problemie UJ/US, ale bez potwierdzenia, że dotyczy tej integracji. Zgodnie z bramką fakt vs zgadywanie: to jest research dla nas, nie merytoryka dla klienta.
SCIEZKA_MERYTORYKI: ZADNA
MINY_I_CIEKAWOSTKI: puste. Research wspomina o różnicy UJ (usługa jednorazowa) vs US (usługa z kartoteki) w kontekście Sello/EZ, ale (a) nie potwierdzono, że dotyczy Sfery, (b) nie ma dowodu ze zlecenia, że integracja używa US. To domysł → poza granicą → wyrzucone.
ODMOWA: puste. Nie ma okazji z dowodem. Ewentualny konflikt zakresu (skopiowanie przy różnych wersjach) to pytanie TYP 1, nie odmowa.
PYTANIA:
1. Jakie wersje Subiekta i Sfery są na obu platformach — identyczne czy różne? Pytam, bo od tego zależy, czy "skopiowanie istniejącego rozwiązania" faktycznie zadziała, czy trzeba adaptować kod. Odpowiedź zmienia zakres prac.
2. Jaki typ dokumentu tworzy integracja w Subiekcie (ZK / FS / PA)? Pytam, bo od typu dokumentu zależy, gdzie koszt przesyłki ma zostać dopisany (nagłówek vs pozycja) i jak głęboko trzeba wejść w kod.
CO_ZLECENIE_MOWI: Integracja WooCommerce ↔ Subiekt przez Sferę. Bug: koszt przesyłki nie importuje się do Subiekta. Jest kod źródłowy. Do zrobienia na dwóch platformach (dwóch klientów), zasada identyczna, skopiowanie rozwiązania. Budżet: do negocjacji.
CZEGO_NIE_MOWI: Wersje Subiekt/Sfera na obu platformach. Typ dokumentu. Jak wygląda kod (jaki język, jak zorganizowany). Czy platformy mają identyczną konfigurację Subiekta. Czy jest środowisko testowe. Czy koszt przesyłki ma być pozycją asortymentową czy polem nagłówkowym. Czy klient oczekuje również poprawki po stronie WooCommerce.
GRANICA_CIECIA: Zlecenie konkretne, wąskie, dwuwarstwowe (Subiekt/Sfera + WooCommerce). Odpowiedź krótka: potwierdzenie kompetencji, zakres, cena (lub widełki przy niejasności), 2 pytania. Zero merytoryki na siłę.
RESEARCH_POTRZEBNY: NIE — research z iteracji 1 nie dał twardych faktów, które wchodzą do oferty. Wiedza o Sferze GT vs nexo (osobna licencja vs wbudowana w PRO) i o UJ/US zostaje u nas jako tło, ale nie zmienia odpowiedzi. Gdyby klient w pytaniu zwrotnym podał wersję lub typ pozycji — wtedy można wrócić do researchu.

DECYZJE:
- DOPISAĆ: nic ponad zakres, cenę i 2 pytania. Żadnej merytoryki o Sferze/UJ/US — brak dowodu ze zlecenia.
- ODPOWIEDZIEĆ: potwierdzenie, że znamy Sferę i WooCommerce, że naprawa kosztu przesyłki to kwestia analizy kodu i mapowania pola/pozycji — krótko, bez wykładu. Widełki cenowe orientacyjne (bo bez wglądu w kod nie da się wycenić w punkt), z zastrzeżeniem, że po zobaczeniu kodu podamy konkret. Zaznaczyć, że replikacja na drugą platformę jest realna, ale zależy od zgodności wersji (stąd pytanie 1).
- DOPYTAĆ: (1) wersje Subiekt/Sfera na obu platformach — czy identyczne; (2) typ dokumentu tworzonego przez integrację (ZK/FS/PA). Oba pytania z uzasadnieniem: od pierwszego zależy, czy kopiujemy czy adaptujemy; od drugiego — gdzie i jak dopisujemy koszt przesyłki.
```