Podzielenie rachunku po pozycjach tak, żeby opłacone pozycje zostawały na rachunku jako wyszarzone, to nie funkcja bramki płatniczej, tylko osobny silnik rozliczeniowy. Żadna z polskich bramek nie daje tego z pudełka, więc w architekturze traktuję to jako własny moduł, i to on jest głównym kosztem w całym projekcie. Podobnie stany UNSENT, SENT, PAID i DO WYJAŚNIENIA oraz wysyłka na kuchnię bez zamykania rachunku wymagają zaprojektowania od zera, bo to logika rachunku, nie koszyka.

Proponuję React Native na POS i web appkę QR gościa, z backendem Node i PostgreSQL. Mniejszy bundle i jeden ekosystem JS dają szybszy prototyp na małych ekranach i łatwiejsze utrzymanie przy etapowym rozwoju. Zastrzeżenie: jeśli POS ma gadać z fizycznym terminalem przez certyfikowane SDK producenta, cross-platform może nie wystarczyć i wtedy wchodzi natywny moduł, co podnosi kwotę.

Kolejność, którą widzę: najpierw makiety, architektura i backlog, około tygodnia, 4 do 6 tysięcy złotych. Potem wąskie MVP na jednym lokalu. Dopiero potem rollout na osiem i rozwój. Bez etapu pierwszego wycena wersji produkcyjnej byłaby zgadywaniem po mojej stronie, a decyzja o budżecie na osiem lokali zapadłaby w ciemno.

Całość, czyli makieta, MVP na jeden lokal i wersja produkcyjna na osiem, to 80 do 140 tysięcy złotych netto, rozłożone na etapy. Czas od około czterech do siedmiu miesięcy. Górna granica może się ruszyć, jeśli dojdą terminale fizyczne, integracja z istniejącym KDS, integracje z agregatorami dostaw albo okaże się, że każdy lokal potrzebuje własnego menu, cen i rozliczeń.

Trzy rzeczy, które muszę wiedzieć, zanim zawężę widełki. Kelner rozlicza rachunek przez terminal fizyczny, a jeśli tak, to jakiego producenta, czy przez płatność online wywoływaną z aplikacji, bo od tego zależy, czy split częściowy domknie się w jednym silniku razem z QR gościa. Czy macie już drukarki kuchenne albo KDS, z którymi mamy się zintegrować, czy system ma sam generować ticket, bo to dwa różne zakresy i dwie różne wyceny. Czy osiem lokali dzieli jedną bazę, jedno menu i jeden raport, czy każde ma własne menu, ceny i rozliczenia, bo to decyduje, czy rollout jest konfiguracją, czy osobnym wdrożeniem za każdym razem.

Jeśli okaże się, że KDS trzeba dopiero postawić, zrobiłbym to jako osobny kawałek, ale najpierw ustalmy zakres.

Ksawier