Z ogłoszenia rozumiem zakres tak: pipeline, który ciągnie dane firm z rejestrów, filtruje po PKD i parametrach, wzbogaca, czyści i odkłada do bazy gotowej do pracy. Dedup po NIP, standaryzacja pól, mapowanie. To wykonalne.

Domyślnie proponuję PKD 2025 jako podstawę, z dorobionym słownikiem na 2007 jeśli Twoje dane są w starym schemacie. Od stycznia 2025 obowiązuje nowa klasyfikacja, okres przejściowy trwa do końca 2026, więc stare i nowe wpisy będą się mieszać, a filtry po kodach mogą bez tego zwracać niepełne wyniki. Drugie założenie to dedup po NIP z warstwą staging przed celem, żeby brudne dane nie wpadały od razu do bazy. Jeśli masz już coś innego, dopasuję się.

Żeby wycenić konkretniej, potrzebuję trzech rzeczy. Skali, czyli ile firm docelowo i jak często aktualizacja. Punktu startu, czyli masz listę NIP, KRS, nazw, czy zbieramy od zera. I targetu, czyli gdzie trafia gotowa baza, plik, CRM czy panel. Od pierwszego zależy, czy limity rejestrów w ogóle bolą, od drugiego cały przepływ, bo KRS nie szuka po NIP i przy liście NIP-ów trzeba przejść przez REGON, od trzeciego format wyjściowy i to, czy w zakresie jest warstwa wizualna.

Widełki na ten zakres to 5 500 do 10 000 zł netto. Dolna granica dotyczy kilku tysięcy rekordów i prostego eksportu, górna większego wolumenu, integracji z Twoim systemem albo panelu. Czas orientacyjnie 10 do 20 dni roboczych, zależnie od tempa dostępu do rejestrów. GUS BIR1 wymaga zgłoszenia i kilka dni oczekiwania, więc część kalendarza to formalności, nie praca.

Jeśli po Twoich odpowiedziach okaże się, że potrzebna jest stała aktualizacja, to naturalny ciąg dalszy, ale najpierw ustalmy sam pipeline. Napisz te trzy rzeczy, a zawężę wycenę do konkretnej kwoty.

Ksawier