KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (redesign/rozbudowa front-endu + formularz kontaktowy)
INTENCJA: wykonawcze (z otwartością na propozycje)
DECYDENT_I_BOL: prawdopodobnie właściciel soft4fx / osoba decyzyjna; ból: strona główna nie wygląda profesjonalnie, brak responsywności, słaby product box → mniejsze zaufanie i konwersja
WYKONALNE: TAK; najbliższa opcja: redesign warstwy prezentacji na istniejącym PHP, jeśli struktura na to pozwala; jeśli nie – przebudowa widoków z zachowaniem treści i PayPro
POLE_DO_POPISU: JEST (podejście mobile-first, system komponentów, product box pod cel sprzedażowy, formularz z walidacją/antyspamem/RODO)
SCIEZKA_MERYTORYKI: ZADNA
MINY_I_CIEKAWOSTKI:
- PayPro – klient wprost wymienia jako do zachowania; przy redesignie trzeba odizolować warstwę płatności, żeby nie zepsuć ścieżki. Dowód: „obecną metodę płatności - PayPro”.
- PHP – narzucone. Dowód: „Musi być oparte o PHP”. Jeśli obecna strona nie jest w PHP, zakres rośnie.
- Formularz kontaktowy – zbiera dane osobowe; wymaga informacji RODO i zabezpieczenia antyspamowego. Dowód: „Wymagane funkcje formularz kontaktowy”. To standard, nie mina.
ODMOWA: puste (brak okazji do odmowy; RODO i antyspam to elementy do dodania w ramach projektu, nie blokada)
PYTANIA:
1. Na czym stoi obecna strona w PHP – własny kod, framework, CMS? Proponuję pozostawić obecny backend, jeśli się da; pytam, bo od tego zależy, czy redesign to warstwa prezentacji, czy przebudowa.
2. Czy mamy dostęp do kodu, repozytorium i środowiska testowego? Proponuję pracę na kopii; pytam, bo bez dostępu nie da się bezpiecznie wdrożyć zmian i oszacować pracochłonności.
3. Ile podstron obejmuje responsywność i czy są materiały źródłowe (logo, screenshoty, treści w edytowalnej formie)? Proponuję mobile-first dla całej witryny; pytam, bo liczba szablonów i stan materiałów zmienia zakres.
4. Formularz kontaktowy ma tylko zbierać wiadomości, czy wymaga integracji (CRM, e-mail, RODO, antyspam)? Proponuję prosty formularz z walidacją i zabezpieczeniem; pytam, bo od tego zależy zakres backendu.
CO_ZLECENIE_MOWI: nowa szata graficzna dla soft4fx.com; zachować treść, logo, nazwę firmy, nazwę produktu, PayPro, większość treści i screenshotów; poprawić wygląd strony głównej i product box lub zastąpić go czymś innym; wprowadzić responsywność całej witryny; dodać formularz kontaktowy; preferowane PHP; budżet do negocjacji; klient otwarty na propozycje.
CZEGO_NIE_MOWI: na jakim systemie/frameworku stoi strona; kto hostuje i czy jest dostęp do kodu; ile jest podstron; jakie są materiały źródłowe; jaki jest termin; czy PayPro ma być modyfikowane; jakie dokładnie ma być działanie formularza; czy są inne integracje; jakie są cele biznesowe poza „profesjonalny wygląd”.
GRANICA_CIECIA: oferta średnia – 3-4 pytania, propozycja podejścia, widełki orientacyjne. Bez wykładu o PHP, PayPro czy RODO ponad dowody ze zlecenia. Nie pytać o budżet.
RESEARCH_POTRZEBNY: TAK – sprawdzić soft4fx.com: strukturę, technologię, formularz, PayPro, dostępne materiały; po to, żeby nie pytać o rzeczy widoczne i trafnie dobrać pytania.