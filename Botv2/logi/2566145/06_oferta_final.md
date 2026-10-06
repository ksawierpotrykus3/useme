1.6 do 8.x to nie aktualizacja, którą się klika. Między tymi wersjami zmienił się framework, szablony i moduły, więc u Pana realnie robimy czystą instalację PS 8.x na stagingu i przeniesienie danych. Stary Warehouse nie zadziała na PS 8, trzeba wgrać nową wersję szablonu i odtworzyć to, co Pan w nim pozmieniał. Jeśli customizacji było sporo, to jest główne źródło niepewności w wycenie.

Druga rzecz to BaseLinker. Oficjalny moduł pod PS 8 jest, ale klucz WebService musi mieć zaznaczone wszystkie uprawnienia. Bez tego synchronizacja stanów, cen i zamówień potrafi działać połowicznie i wygląda, jakby działała, dopóki nie zacznie brakować stanów.

Trzecia to SEO. Same przekierowania 301 przepisane ze starych URLi to za mało. Lepiej zmapować je z Search Console, bo tam siedzą adresy, które faktycznie mają ruch, a nie tylko te, które pamięta baza.

Zakładam jeden język, jedną walutę, bez multistore. Jeśli jest inaczej, wycena idzie w górę.

Zanim podam konkretną kwotę, potrzebuję trzech rzeczy. Listy aktywnych modułów i integracji, z zaznaczeniem które muszą działać po migracji, bo część z nich może nie mieć odpowiednika na PS 8. Odpowiedzi, czy Warehouse był modyfikowany i czy są pliki lub dokumentacja. Oraz wolumenu, czyli liczby produktów, kombinacji, klientów, zamówień i rozmiaru bazy ze zdjęciami.

Przy tak niepełnym obrazie orientacyjnie mieszczę się w 8000 do 14000 zł netto, a całość razem z testami i przełączeniem na domenę to około 15 do 25 dni. Kwota zależy głównie od liczby modułów do zastąpienia, wolumenu danych i tego, ile pracy włożymy w odtworzenie szablonu. Po Państwa odpowiedziach zawężę to do jednej liczby.

Ksawier