# -*- coding: utf-8 -*-
"""Niezależny test sędziowski bez sztucznych promptów i wag.

Porównuje 6 autentycznych podejść do zlecenia #144890:
- Kandydat A: Nowa Oferta v6 (Styl ludzki, micro-przykłady, próbka 3 dok, etapy 5400/4400)
- Kandydat B: Antoni (AppWave - lider testów, 8900-11500 zł, prototyp, etapy)
- Kandydat C: Stara Oferta v5 (Techniczna ściana, CDN.TraNag, 6500 zł, bez etapów)
- Kandydat D: Dominik (grodev.pl - konkretny programista, 7500 zł, szczery brak n8n na prod)
- Kandydat E: Konrad Szydłowski (Pytacz z priv - brak ceny, brak terminu, samo pytanie o KSeF)
- Kandydat F: Dawid (dawidweb - 3600 zł, pilot 30 dok, pytanie o magazyn)

Sędziowie:
1. deepseek-reasoner (R1 - model reasoning/wnioskujący)
2. deepseek-chat (standardowy czat AI)
"""

import json
import sys
from pathlib import Path

# Upewnij się że kod jest na ścieżce
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "kod"))
from chain_executor import call_deepseek

ZLECENIE_OPIS = """Zlecę stworzenie, pełne wdrożenie oraz opiekę powdrożeniową nad automatyzacją obiegu dokumentów (faktury kosztowe, dokumenty WZ, zamówienia) w firmie handlowo-produkcyjnej.
Obecny proces:
Dokumenty spływają do nas ze skanera biurowego, poczty e-mail oraz od pracowników w terenie do wyznaczonego folderu na Google Drive. Zespół poświęca zbyt dużo czasu na ręczne sprawdzanie i przepisywanie pozycji do programu magazynowo-księgowego.
Oczekiwany przebieg automatyzacji:
1. Pobieranie nowych plików z folderu wejściowego na Google Drive lub skrzynki mailowej.
2. Odczyt danych przez OCR wsparty modelem AI (rozpoznanie typu dokumentu, odczyt NIP-u, danych kontrahenta, daty, numeru faktury, a także pozycji towarowych i kwot netto/brutto/VAT).
3. Bezwarunkowa weryfikacja poprawności matematycznej – suma pozycji musi zgadzać się z kwotą podsumowania dokumentu. W razie rozbieżności dokument ma trafiać do osobnego folderu do szybkiej weryfikacji ręcznej z powiadomieniem.
4. Zmiana nazwy pliku wg naszego schematu i przeniesienie do archiwum.
5. Przygotowanie struktury danych do importu do programu Comarch Optima (lub bezpośrednie zasilenie bazy / plik wymiany).
Wymagania i koszty:
Zależy mi na optymalizacji comiesięcznych kosztów stałych, dlatego preferuję n8n uruchomione na własnym serwerze (brak opłat za każdą wykonaną operację). Rozważę również Make, jeśli wdrożenie będzie tego warte i stabilniejsze.
Zakres zlecenia:
- Zaprojektowanie i konfiguracja całego scenariusza,
- Wdrożenie w naszym środowisku i testy na rzeczywistych dokumentach firmy,
- Krótki okres opieki i asysty powdrożeniowej po uruchomieniu.
W ofercie proszę o:
1. Krótką informację, jak technicznie planujesz rozwiązać odczyt trudniejszych skanów i połączenie z Optimą.
2. Przewidywany czas realizacji oraz przykłady podobnych automatyzacji, które masz na swoim koncie."""

KANDYDACI = {
    "Kandydat A": {
        "podpis": "Ksawier (Wersja v6 - Nowy Styl Ludzki)",
        "wycena": "9 800 zł netto (Etap 1: 5400 zł, Etap 2: 4400 zł), 18 dni roboczych",
        "tekst": """Dzień dobry,

tu Ksawier Potrykus. Przeczytałem Państwa ogłoszenie o automatyzacji obiegu faktur, WZ i zamówień. Zanim przejdę do konkretów, jedna rzecz, która od razu porządkuje cały projekt: od 1 lutego 2026 większość faktur krajowych trafia do KSeF. Comarch Optima w nowszych wersjach potrafi je odbierać sama, razem z pozycjami. Nie ma sensu dublować tego drogim OCR-em. Automatyzacja ma sens dla całej reszty: skanów ze skanera, zdjęć od kierowców, faktur zagranicznych, WZ i zamówień. I tym się zajmiemy.

Jak technicznie rozwiążę trudniejsze skany i połączenie z Optimą

Po pierwsze, dzielę dokumenty na trzy strumienie, bo każdy wymaga innego podejścia. PDF-y cyfrowe z maila mają warstwę tekstową, więc czytam je bezpośrednio kodem. To jest stuprocentowo precyzyjne i nie kosztuje ani grosza za tokeny. Skany ze skanera biurowego i zdjęcia telefonem z terenu to inna bajka. One wymagają najpierw preprocessingu: prostowania skosu, poprawy kontrastu, wycięcia tła. Dopiero potem idą do modelu widzącego obraz, który rozumie układ tabeli z pozycjami. AI tylko odczytuje obraz i wyciąga pola: typ dokumentu, NIP, kontrahenta, daty, numer, pozycje, kwoty netto, VAT i brutto. Nic nie liczy. Matematykę zawsze sprawdza deterministyczny kod. Dla każdej stawki VAT porównuje sumę pozycji z podsumowaniem dokumentu. Tolerancja to 1-2 grosze, bo polska ustawa o VAT dopuszcza liczenie podatku od sumy stawek albo od poszczególnych pozycji. Jeśli suma się nie zgadza, dokument trafia do osobnego folderu do szybkiej weryfikacji ręcznej, a Wy dostajecie powiadomienie. Do tego deduplikacja: klucz hash pliku plus NIP i numer dokumentu. Ten sam dokument wrzucony drugi raz z maila i ze skanera nie przejdzie ponownie. Przy kwotach powyżej 15 000 zł sprawdzam kontrahenta na Białej Liście podatników VAT.

Po drugie, połączenie z Comarch Optima. Tu chcę być bardzo wyraźny, bo to jest miejsce, w którym nie wolno iść na skróty. Nigdy nie piszemy bezpośrednio do bazy Optimy przez INSERT SQL. To łamie integralność bazy, numerację rejestrów, a przy zamknięciu miesiąca potrafi narobić prawdziwego bałaganu. Comarch może wtedy odmówić wsparcia, a księgowość ma problem. Zamiast tego korzystam z oficjalnej, bezpiecznej ścieżki: Praca Rozproszona XML albo Comarch ERP Web API. Optima sama weryfikuje poprawność pliku importu, zanim cokolwiek trafi do obiegu. Najwięcej pracy jest przy mapowaniu towarów. Okno importu ma domyślnie zaznaczone „Załóż karty towarów”, więc nazwy od dostawców narobiłyby Wam bałaganu w kartotece. Wyłączamy to i dopasowujemy pozycje według tabeli powiązań. Dostawca pisze „Śruba M8x40 ocynk”, a u Was to karta SR-M8-40. Pierwszy raz pozycję przypisuje człowiek, potem automat pamięta regułę. I najważniejsze: wszystkie testy robimy na kopii bazy. Produkcja nie zostaje dotknięta, dopóki import nie przejdzie czysto na kopii.

Przewidywany czas realizacji i przykłady podobnych automatyzacji

Całość zajmie 18 dni roboczych. Rozbijam to na dwa etapy, żebyście mieli pełną kontrolę i płacili za odebrany kawałek pracy.

Etap pierwszy to przygotowanie n8n na własnym serwerze, pobieranie plików z Google Drive i skrzynki mailowej, preprocessingu skanów i testy odczytu na Waszych rzeczywistych dokumentach. Ten etap wyceniam na 5 400 zł netto. Po jego zakończeniu zobaczycie, jak automat radzi sobie z Waszymi fakturami, WZ-kami i zamówieniami, jeszcze bez dotykania Optimy.

Etap drugi to integracja importu z Optimą, mapowanie kartotek, testy na kopii bazy i asysta powdrożeniowa. Ten etap to 4 400 zł netto. Płatność za każdy etap po jego odebraniu.

Mam za sobą wdrożenie potoku dla ponad 3500 dokumentów z precyzją 99,4 procent. Robiłem też integracje z modułami Comarch ERP: rejestrami zakupu VAT oraz dokumentami magazynowymi WZ i PZ. Wiem, gdzie Optima bywa wrażliwa i jak przeprowadzić import, żeby nie zablokować księgowości.

Koszty utrzymania są przewidywalne. n8n działa na własnym VPS, więc nie ma opłat za każdą operację. Serwer to około 30-50 zł miesięcznie. Tokeny modelu AI przy skanach to zwykle 50-100 zł miesięcznie przy 1000 dokumentów. Razem 80-150 zł miesięcznie. Żadnych ukrytych subskrypcji ani nagłych dopłat.

Po uruchomieniu dostajecie 30 dni asysty powdrożeniowej. Przez pierwszy miesiąc poprawiamy reguły na dokumentach, które faktycznie przyjdą. A przez 12 miesięcy od wdrożenia naprawiam bezpłatnie ewentualne błędy w kodzie, który napisałem. Jeśli będzie trzeba, pomogę też przy drobnych zmianach, ale to już poza gwarancją.

Zanim podejmiemy decyzję, proponuję prostą rzecz: prześlijcie mi kilka przykładowych dokumentów, najlepiej takich, które sprawiają najwięcej kłopotu. Jedną fakturę z maila, jeden skan ze skanera i jedno zdjęcie od kierowcy. Przerobię je na sucho i pokażę, co automat odczyta, a co wymaga dopracowania. Bez zobowiązań. Zobaczycie na własne oczy, jak to działa na Waszym materiale.

Czy taka forma współpracy i rozbicia na etapy Państwu odpowiada?"""
    },
    "Kandydat B": {
        "podpis": "Antoni (AppWave - z oferty publicznej)",
        "wycena": "8 900 zł netto (Etap 1 i 2) / 11 500 zł (z Etapem 3), 15-20 dni roboczych",
        "tekst": """Dzień dobry,
tu Antoni z AppWave, software house'u z Łodzi. Przeczytałem ogłoszenie i zanim przejdę do Waszych pytań, jedna rzecz, która zmienia zakres.
Od 1 kwietnia 2026 większość faktur od polskich firm przychodzi przez KSeF. Optima od wersji 2026.4.1 pobiera je sama, w tle, a na listę faktur zakupu przenosicie je razem z pozycjami. Takich faktur nie trzeba skanować ani czytać przez AI, bo dane już są. Automatyzacja ma sens dla całej reszty: WZ, zamówień, faktur zagranicznych, faktur od najmniejszych firm (te do końca 2026 nie muszą wystawiać w KSeF) i zdjęć od ludzi w terenie.
Rozrysowałem to na osobnej stronie. Jest tam schemat i prototyp, w którym możecie przepuścić sześć przykładowych dokumentów i zobaczyć, gdzie automat się zatrzymuje:
https://claude.ai/artifact/C8UMxBUoLpvWvjPyYw5qN4
Jak to działa w skrócie
n8n pilnuje folderu na Google Drive i skrzynki pocztowej. Każdy plik dostaje odcisk liczony z zawartości, więc ten sam dokument wrzucony drugi raz nie przejdzie ponownie. Faktury sprawdzamy w KSeF osobnym kluczem, który pozwala tylko czytać. Jeśli faktura już tam jest, plik idzie wyłącznie do archiwum.
Resztę czyta model AI i oddaje dane zawsze w tych samych polach: typ dokumentu, NIP, kontrahent, daty, numer, pozycje, kwoty. Pola, którego nie da się odczytać, nie wypełnia na siłę. Zostawia je puste.
Potem liczy program, nie AI. Dla każdej stawki VAT porównuje sumę pozycji z podsumowaniem netto, VAT i brutto. Przepisy pozwalają liczyć VAT od netto, od brutto albo sumować go z pozycji, więc na zaokrągleniach wychodzi czasem grosz różnicy. Próg ustalimy razem. NIP i numer konta sprawdzamy w wykazie podatników VAT. Przy transakcjach powyżej 15 000 zł przelew na konto spoza wykazu odbiera koszt i daje solidarną odpowiedzialność za VAT, więc lepiej wiedzieć o tym przed przelewem.
Jeśli coś się nie zgadza albo brakuje pola, dokument trafia do folderu „Do sprawdzenia”, a wskazana osoba dostaje maila z powodem, na przykład „suma pozycji 1 230,00 zł, podsumowanie 1 320,00 zł”. Dokumenty bez uwag dostają nazwę według Waszego schematu i idą do archiwum.
Trudniejsze skany
Model czyta każdą stronę PDF naraz jako tekst i jako obraz. PDF z maila zwykle ma warstwę tekstową, więc tekst jest brany wprost. Skan albo zdjęcie model czyta jako obraz, więc widzi też układ tabeli. Najbardziej szkodzą zdjęcia rozmazane, przekręcone i mocno skompresowane. Ludzie w terenie dostaną krótką instrukcję: cały dokument w kadrze, dobre światło, telefon prosto. Rozmazanej kwoty nikt nie odczyta pewnie, ani AI, ani księgowa. Taki dokument nie przejdzie kontroli sumy i trafi do sprawdzenia.
Połączenie z Optimą
Korzystamy z importu z plików XML, który Optima ma wbudowany. Obejmuje on między innymi faktury zakupu, przyjęcia zewnętrzne (tak w Optimie wchodzi WZ od dostawcy) i zamówienia u dostawcy. Automatyzacja odkłada pliki do katalogu importu ustawionego w Optimie, a import uruchamia księgowa z listy dokumentów. Kontrahenta Optima rozpoznaje po kodzie, NIP albo GLN.
Najwięcej pracy jest przy towarach. Okno importu ma domyślnie zaznaczone „Załóż karty towarów”, więc nazwy od dostawców narobiłyby Wam bałaganu w kartotece. Wyłączamy to i dopasowujemy pozycje wcześniej, według tabeli powiązań: dostawca pisze „Śruba M8x40 ocynk”, a u Was to karta SR-M8-40. Pierwszy raz pozycję przypisuje człowiek, potem automat pamięta. Po czym dokładnie Optima łączy pozycję z kartą, sprawdzimy na kopii Waszej bazy, zanim cokolwiek wejdzie do prawdziwej. Do bazy Optimy nie piszemy bezpośrednio, dane wchodzą tylko przez import.
n8n czy Make? n8n. W Make każdy moduł liczy operację przy każdym elemencie, więc faktura z trzydziestoma pozycjami mnoży operacje. n8n w wersji Community jest bezpłatny. Postawimy go u Was z bazą PostgreSQL, bo tak dokumentacja n8n zaleca do stałej pracy. Serwer z n8n musi mieć dostęp do folderu, z którego Optima importuje.
Model AI rozlicza dostawca, nie my, w dolarach. Przy tysiącu stron miesięcznie wychodzi około 20–35 USD (liczę na Claude Sonnet 5). Faktury z KSeF nic nie kosztują, bo ich nie czytamy. Dokładną kwotę podam po teście na Waszych dokumentach.
Czas i przykłady
Etap 1, dni robocze 1–10: pobieranie z Drive i poczty, sprawdzanie w KSeF, odczyt faktur, WZ i zamówień, kontrola sum, NIP-u i rachunku, folder do sprawdzenia z mailem, nazwy i archiwum. Na koniec test na 50 Waszych dokumentach i raport: ile przeszło, ile trafiło do sprawdzenia i dlaczego. 5 400 zł netto.
Etap 2, dni 11–15: dopasowanie towarów i kontrahentów, pliki do importu faktur zakupu, test na kopii bazy, uruchomienie. 3 500 zł netto.
Etap 3, dni 16–20, jeśli chcecie: import WZ jako przyjęć zewnętrznych i zamówień u dostawcy. 2 600 zł netto.
Etapy 1 i 2 to razem 15 dni roboczych i 8 900 zł netto. Z Etapem 3 wychodzi 20 dni i 11 500 zł netto. Dni liczymy od momentu, gdy mamy dostęp do Drive, skrzynki, serwera i kopii bazy Optimy. 50 dokumentów do testu potrzebujemy w ciągu pierwszych 5 dni roboczych, inaczej raport z Etapu 1 się przesunie.
Płacicie za odebrany etap. Przez pierwszy miesiąc po uruchomieniu poprawiamy reguły na dokumentach, które przyjdą, a przez 12 miesięcy naprawiamy nasze błędy bez dopłaty.
Automatyzację faktur prowadzimy też u siebie. W naszym produkcie BetterCX faktury za płatności w Stripe wystawiają się same i trafiają do KSeF. Z realizacji dla klientów najbliżej tego zlecenia jest automatyzacja w n8n dla marki edukacyjnej: AI przygotowuje posty i grafiki, a nic nie wychodzi bez akceptacji człowieka. Tu byłby ten sam układ, automat robi robotę, człowiek decyduje tam, gdzie jest ryzyko.
Scenariusze w n8n, konfiguracja i instrukcje dla modelu są Wasze po zapłacie za etap. Wszystko działa na Waszych kontach.
Proponuję 45 minut rozmowy online w tym albo w przyszłym tygodniu. Przyda się kilka trudnych dokumentów, na przykład zdjęcie WZ z terenu i skan faktury z wieloma pozycjami. Zapytam też o dwie rzeczy: czy Optimę macie stacjonarnie, czy w Chmurze Comarch, i ile dokumentów przychodzi miesięcznie.
Antoni Łubisz, AppWave"""
    },
    "Kandydat C": {
        "podpis": "Ksawier (Wersja v5 - Stara Techniczna Ściana)",
        "wycena": "6 500 zł netto, 13 dni roboczych",
        "tekst": """Dzień dobry,

Główna pułapka to wrzucenie wszystkich dokumentów do jednego worka OCR. Faktury krajowe po 1 lutego 2026 są w KSeF jako XML FA(3), a Optima od 2026.4.1 pobiera je natywnie z pozycjami. PDF-y z warstwą tekstową parsuję bez tokenów, a skany i zdjęcia z terenu wymagają preprocessingu obrazu (prostowanie skosu, kontrast) i modelu Vision z progiem pewności. Rozdzielam odczyt AI od twardej walidacji matematycznej z tolerancją 1-2 gr (ustawa o VAT dopuszcza liczenie od sumy stawek lub pozycji), deduplikuję po NIP + numerze dokumentu + hashu pliku i weryfikuję Białą Listę MF przy 15 000 zł.

Połączenie z Optimą realizuję przez Pracę Rozproszoną XML lub Comarch ERP Web API, nigdy przez bezpośredni INSERT do bazy - zależnie od instalacji. n8n self-hosted na VPS redukuje koszty do 30-50 zł/mies. przy zerowych opłatach za wykonanie. Testy na kopii bazy, bez zatrzymywania fakturowania, plus 30 dni gwarancji. Na wolumenie 3500+ dokumentów osiągnąłem precyzję 99,4%, a w module Procesy Comarch ERP XL dla dystrybutora B2B (45 WZ/dzień) zredukowałem duplikaty FS do zera.

Czy Państwa Optima pracuje stacjonarnie, czy w Chmurze Comarch, i jaki procent faktur kosztowych to dokumenty spoza KSeF?

Wdrożenie: 6500 zł netto, 13 dni.

Ksawier Potrykus"""
    },
    "Kandydat D": {
        "podpis": "Dominik (grodev.pl - z wiadomości prywatnej)",
        "wycena": "7 500 zł + VAT, 18 dni roboczych",
        "tekst": """Dzień dobry,
Odpowiadam na oba pytania po kolei.
Połączenie z Optimą. Odradzam zapis bezpośrednio do bazy, mimo że wymienia to Pan jako opcję. Baza Optimy ma własną logikę numeracji, powiązań między dokumentami a rejestrami VAT i kontrahentami. Wpis z pominięciem aplikacji łamie tę spójność, a problem ujawnia się zwykle miesiąc później, przy zamknięciu okresu albo aktualizacji programu, i oznacza utratę wsparcia producenta. Właściwą drogą jest praca rozproszona, czyli oficjalny import plików XML, obsługujący rejestr faktur zakupu oraz dokumenty WZ, PZ, RW, PW i MM, a więc dokładnie to, o czym Pan pisze. Automatyzacja buduje plik zgodny z tym formatem, a Optima zaciąga go swoim mechanizmem i stosuje własne kontrole. Jedna rzecz do sprawdzenia przed startem: licencjonowanie pracy rozproszonej bywa osobne, więc warto potwierdzić u swojego partnera Comarcha, czy Państwa wariant je obejmuje.
Trudne skany. Pierwszy krok to sprawdzenie, czy plik w ogóle wymaga OCR. Faktury przychodzące mailem to najczęściej PDF z warstwą tekstową i wtedy dane odczytuje się wprost, bez rozpoznawania obrazu, co jest szybsze i bezbłędne. OCR uruchamiam dopiero dla skanów ze skanera i zdjęć z terenu, po wcześniejszym wyprostowaniu i oczyszczeniu obrazu. Do odczytu struktury używam modelu czytającego obraz, a nie płaskiego tekstu z OCR. Przy fakturach ma to duże znaczenie, bo każdy dostawca ma inny układ tabeli, a model widzący stronę rozumie, która liczba należy do której pozycji. Zdjęcia z telefonu od pracowników w terenie będą tu najsłabszym ogniwem i właśnie dlatego Pana punkt trzeci jest najważniejszy w całym procesie.
Weryfikację matematyczną robię kodem, nie modelem. Suma pozycji do podsumowania, netto plus VAT do brutto, kontrola stawek. Model może się pomylić i zrobi to w sposób wyglądający wiarygodnie, więc każdy dokument przechodzi deterministyczną kontrolę, a przy rozbieżności trafia do folderu wyjątków z powiadomieniem i wskazaniem, która pozycja się nie zgadza. Do Optimy nie trafia nic, co nie przeszło tego sprawdzenia.
Jedna uwaga do rozważenia: faktury zawierają dane kontrahentów, więc przy wyborze dostawcy modelu warto zostać przy przetwarzaniu na terenie Unii.
Czas realizacji: 18 dni roboczych, w tym testy na Państwa rzeczywistych dokumentach, bo bez nich nie da się dostroić odczytu. Wycena 7500 + VAT + opłata useme zł, w tym 30 dni asysty po uruchomieniu. Dalsza opieka nad n8n na Państwa serwerze według osobnego pakietu, bo instancja wymaga aktualizacji i kopii.
Doświadczenie, uczciwie: buduję narzędzia oparte na modelach językowych i integracje przez API, natomiast n8n nie wdrażałem dotąd produkcyjnie. Najtrudniejsza część tego zlecenia nie leży jednak w samym n8n, tylko w poprawnym odczycie dokumentów, kontroli danych i zbudowaniu pliku, który Optima przyjmie bez zastrzeżeń. I to jest praca, którą wykonuję na co dzień.
Dominik Gróński
grodev.pl"""
    },
    "Kandydat E": {
        "podpis": "Konrad (z wiadomości prywatnej - Pytający bez oferty)",
        "wycena": "Brak wyceny, brak terminu (samo pytanie)",
        "tekst": """Dzień dobry,
zanim złożę ofertę, jedno pytanie, bo od niego zależy połowa zakresu. Od 1 lutego 2026 faktury odbiera się w KSeF, a od 1 kwietnia większość dostawców wystawia je tylko tam. Optima po skonfigurowaniu uprawnień KSeF pobiera je sama: do modułu Handel z pozycjami albo do rejestru VAT. Takich faktur nie ma sensu czytać OCR-em, bo dane w XML są pewne. OCR z modelem AI zostaje wtedy dla WZ, zamówień, faktur zagranicznych i od najmniejszych dostawców.
Jeśli tak, proponuję zbudować odczyt AI tylko dla pozostałych dokumentów, co skraca wdrożenie i obniża koszt wywołań modelu.
Czy faktury kosztowe od polskich dostawców pobieracie już w Optimie z KSeF?"""
    },
    "Kandydat F": {
        "podpis": "Dawid (dawidweb - z oferty publicznej)",
        "wycena": "3 600 zł netto, 21 dni roboczych",
        "tekst": """Dzień dobry,
odpowiadam najpierw na dwa pytania z ogłoszenia. Trudniejsze skany rozwiązuję dwutorowo: plik przechodzi przez OCR, a potem tekst razem z obrazem strony trafia do modelu AI, który zwraca dane w stałej strukturze, czyli typ dokumentu, NIP, kontrahenta, datę, numer i pozycje z kwotami. Każdy wynik przechodzi przez Państwa bezwarunkowy test: suma pozycji musi dać netto, VAT i brutto z podsumowania, a NIP musi mieć poprawną cyfrę kontrolną, więc słaby skan nie przejdzie dalej po cichu, tylko trafi do folderu weryfikacji z powiadomieniem. Połączenie z Optimą planuję przez plik wymiany do importu, bez zapisu bezpośrednio do bazy, bo to bezpieczniejsze przy aktualizacjach programu, przy czym to, jaki format przyjmie Państwa Optima i do którego modułu, potwierdzę na pierwszym etapie na Państwa instalacji, to główna niewiadoma projektu.
Co do narzędzia: n8n na własnym serwerze ma tu sens, bo przy kilkunastu krokach na dokument Make szybko robi się droższy. Stałe koszty po Państwa stronie to serwer lub VPS oraz opłaty za model AI zależne od liczby dokumentów, ich szacunek podam po testach.
Najbliższa realizacja z mojego portfolio to integracja feedów Midocean (API JSON) i PF Concept (XML) z synchronizacją CRON dla AMC Group, czyli automatyczne pobieranie, sprawdzanie i zasilanie innego systemu danymi.
Etap pierwszy (7 dni) to pilot na 30 Państwa prawdziwych dokumentach i potwierdzony import do Optimy, etap drugi to pełny scenariusz z pocztą i Google Drive, nazewnictwem, archiwum i testami. Całość 3600 zł netto w 21 dni, w tym 30 dni asysty po uruchomieniu, w pełni pisemnie.
Pytanie zmieniające wycenę: ile dokumentów miesięcznie przetwarzacie i czy import ma trafiać do rejestru VAT, czy do dokumentów magazynowych w Optimie?
Pozdrawiam
Dawid"""
    }
}

PROMPT_SĘDZIOWSKI = f"""Cześć! Wystawiłem na Useme takie ogłoszenie o zleceniu:

\"\"\"
{ZLECENIE_OPIS}
\"\"\"

Dostałem 6 różnych odpowiedzi/ofert od programistów i agencji. Skopiowałem je poniżej (nazwałem ich Kandydat A, B, C, D, E, F):

============================================================
KANDYDAT A:
Wycena: {KANDYDACI['Kandydat A']['wycena']}
Treść:
{KANDYDACI['Kandydat A']['tekst']}

============================================================
KANDYDAT B:
Wycena: {KANDYDACI['Kandydat B']['wycena']}
Treść:
{KANDYDACI['Kandydat B']['tekst']}

============================================================
KANDYDAT C:
Wycena: {KANDYDACI['Kandydat C']['wycena']}
Treść:
{KANDYDACI['Kandydat C']['tekst']}

============================================================
KANDYDAT D:
Wycena: {KANDYDACI['Kandydat D']['wycena']}
Treść:
{KANDYDACI['Kandydat D']['tekst']}

============================================================
KANDYDAT E:
Wycena: {KANDYDACI['Kandydat E']['wycena']}
Treść:
{KANDYDACI['Kandydat E']['tekst']}

============================================================
KANDYDAT F:
Wycena: {KANDYDACI['Kandydat F']['wycena']}
Treść:
{KANDYDACI['Kandydat F']['tekst']}
============================================================

Jestem właścicielem firmy handlowo-produkcyjnej, nie jestem informatykiem. Chcę wybrać kogoś, kto to dowiezie, nie rozwali mi księgowości i nie naciągnie mnie na koszty.

Powiedz mi po ludzku, szczerze i bez owijania w bawełnę:
1. Które oferty są Twoim zdaniem najlepsze i dlaczego?
2. Co myślisz o kandydatach, którzy zamiast pełnej oferty zadają mi tylko pytania (np. Kandydat E)? Czy to profesjonalne podejście, czy po prostu strata czasu i brak konkretu?
3. Czy jeśli ktoś pisze bardzo dużo i zakłada różne rzeczy (jak Kandydat A czy B), to znaczy, że strzela na oślep i zgaduje za dużo, czy wręcz przeciwnie – że naprawdę zna się na robocie?
4. Kogo byś wybrał na moim miejscu i w jakiej kolejności? Ułóż pełny ranking od 1 do 6 z krótkim, dosadnym uzasadnieniem dla każdego miejsca.
"""

def run():
    out_dir = Path(__file__).resolve().parent
    report_file = out_dir / "RAPORT_NIEZALEZNYCH_SEDZIOW_AI.md"
    json_file = out_dir / "wyniki_niezaleznych_sedziow_ai.json"
    
    print("=" * 70)
    print("START: TEST NIEZALEŻNYCH SĘDZIÓW (BEZ SZTUCZNYCH PROMPTÓW / WAG)")
    print("=" * 70)
    
    wyniki = {}
    
    # 1. Sędzia Reasoning (DeepSeek-Reasoner / R1)
    print("\n[1/2] Odpytuję Sędziego 1: DeepSeek-Reasoner (Model Myślący / R1)...", flush=True)
    resp_reasoner = call_deepseek(
        system_prompt="",
        user_prompt=PROMPT_SĘDZIOWSKI,
        model="deepseek-reasoner",
        timeout=300,
        max_tokens=4000
    )
    if resp_reasoner:
        print("[OK] Sędzia 1 (Reasoner) zakończył ocenę!", flush=True)
        wyniki["sedzia_1_reasoner"] = resp_reasoner
    else:
        print("[ERROR] Sędzia 1 nie odpowiedział.", flush=True)
        wyniki["sedzia_1_reasoner"] = "BŁĄD TIMEOUT / BRAK ODPOWIEDZI"
        
    # 2. Sędzia Chat (DeepSeek-Chat / v4-pro)
    print("\n[2/2] Odpytuję Sędziego 2: DeepSeek-Chat (Standardowy Czat AI)...", flush=True)
    resp_chat = call_deepseek(
        system_prompt="",
        user_prompt=PROMPT_SĘDZIOWSKI,
        model="deepseek-chat",
        timeout=300,
        max_tokens=4000
    )
    if resp_chat:
        print("[OK] Sędzia 2 (Chat) zakończył ocenę!", flush=True)
        wyniki["sedzia_2_chat"] = resp_chat
    else:
        print("[ERROR] Sędzia 2 nie odpowiedział.", flush=True)
        wyniki["sedzia_2_chat"] = "BŁĄD TIMEOUT / BRAK ODPOWIEDZI"
        
    # Zapis JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(wyniki, f, ensure_ascii=False, indent=2)
        
    # Zapis Markdown
    md_content = f"""# RAPORT NIEZALEŻNYCH SĘDZIÓW AI (BEZ SZTUCZNYCH PROMPTÓW)
**Data badania:** 2026-09-26  
**Zlecenie:** Automatyzacja obiegu faktur i dokumentów kosztowych (#144890)  
**Cel:** Sprawdzenie, jak modele AI (oceniające surowym promptem klienta biznesowego) oceniają oferty oraz jak interpretują dylemat: "Oferta z gotową architekturą vs Zadawanie pytań".

---

## 1. OCENA SĘDZIEGO 1: DeepSeek-Reasoner (Model Wnioskujący / R1)
*Model pracujący z łańcuchem myślenia (Chain of Thought), weryfikujący logikę biznesową i architektoniczną.*

{wyniki.get('sedzia_1_reasoner', 'Brak')}

---

## 2. OCENA SĘDZIEGO 2: DeepSeek-Chat (Standardowy Model Konwersacyjny)
*Model odpowiadający w roli doradcy biznesowego / pragmatycznego przedsiębiorcy.*

{wyniki.get('sedzia_2_chat', 'Brak')}

---
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\n[SUKCES] Raport zapisany w: {report_file}")

if __name__ == "__main__":
    run()
