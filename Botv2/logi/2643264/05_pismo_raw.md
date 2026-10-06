Zacznę od tego, co widzę po lekturze zlecenia, bo dwie rzeczy mogą zmienić zakres bardziej niż cokolwiek innego.

Pierwsza dotyczy A+ Content. To funkcja Amazona dostępna wyłącznie dla marek zarejestrowanych w Brand Registry. Jeśli Waszej marki tam nie ma, moduł AI Editor w wersji z A+ nie zadziała i trzeba go zamienić na zwykłą optymalizację opisów i parametrów. Nie jest to problem nie do obejścia, ale wpływa na to, co realnie dostaniecie w pierwszej wersji.

Druga dotyczy monitoringu cen konkurencji przez API Allegro. Publiczny endpoint do listingu ofert wymaga zatwierdzonej aplikacji, bez tego zwraca błąd weryfikacji. Można to obejść dwojako. albo przejść przez proces weryfikacji aplikacji w Allegro, co potrafi potrwać, albo wejść przez BaseLinker, który ma moduł cenotworzenia i limit tysiąca sprawdzeń ofert dziennie w ramach konta Allegro. Proponuję BaseLinker na start i równolegle uruchomić weryfikację, żeby nie blokować wdrożenia.

Co do architektury, o którą pytacie. Proponuję hybrydę. Orkiestracja w n8n albo Make, bo szybko się ją składa i łatwo później Wam podejrzeć, co agent robi. Logika cenowa i synchronizacja stanów w Pythonie, bo tam potrzebne są bezpieczniki marżowe, batchowanie zapytań do LLM i obsługa limitów API, a tego w prosty sposób nie zrobi się wizualnie. Czysty Python od zera to więcej pracy bez zysku, czyste n8n nie utrzyma porządnie logiki cenowej przy 400 SKU i dwóch marketplace'ach. BaseLinker traktuję jako warstwę pośrednią tam, gdzie bezpośrednie API jest zbyt wąskie.

Przy auto-pricingu proponuję start w trybie sugestii z ręcznym zatwierdzaniem zmian. Automatyzację włączamy dopiero wtedy, gdy ustalicie reguły marżowe, bo bez podłogi marży, kosztów prowizji, VAT i dostawy agent może zjechać z ceną poniżej opłacalności. To nie jest kwestia zaufania do agenta, tylko brakującego parametru, którego na razie nie ma w zleceniu.

Koszty tokenów przy 400 SKU są do opanowania. Jednorazowa optymalizacja całego katalogu to rząd kilkudziesięciu złotych przy batchowaniu i cache. Miesięcznie zależy od częstotliwości regeneracji opisów, przy rozsądnym ustawieniu to nadal niskie kwoty, ale wolę je potwierdzić po ustaleniu zakresu monitoringu.

Wdrożenie wyceniam na 16 000 do 24 000 zł netto. Dolna granica obowiązuje, gdy macie już zatwierdzoną aplikację SP-API, dostępy do kont i idziemy przez BaseLinker. Górna, gdy część rejestracji robimy od zera albo wchodzimy w bezpośrednie API z pełną automatyzacją. Czas to około 25 do 45 dni roboczych od przekazania dostępów, głównie przez procesy weryfikacyjne po stronie marketplace'ów. Utrzymanie i koszty narzędzi po Waszej stronie wycenię osobno, gdy będziemy znać zakres monitoringu.

Żeby ruszyć, potrzebuję trzech rzeczy. Czy macie zatwierdzoną aplikację SP-API i dostępy do kont sprzedawcy. Czy marka jest w Amazon Brand Registry. Które rynki Amazon wchodzą w grę i czy monitoring cen ma być per ASIN i EAN, bo od tego zależy liczba wywołań API i koszt utrzymania.

Ksawier