```
KWALIFIKOWALNOSC: TAK (projekt jednorazowy, realny budżet 1100 PLN, realny decydent, nie śmierdzi rekrutacją ani spekulacją)

TYP_ZLECENIA: projekt jednorazowy (dopracowanie istniejącej strony + naprawa błędu technicznego)

INTENCJA: wykonawcze

DECYDENT_I_BOL: osoba/firma z gotową stroną na WP+Divi. Ból: strona jest "na 80%", wizualnie niedokończona, teksty i zdjęcia nieułożone, do tego blokada logowania (403), która realnie przeszkadza w korzystaniu. Klient chce domknąć temat, nie zaczynać od zera — i tak to formułuje ("nie chodzi o tworzenie strony od zera").

WYKONALNE: TAK. Standardowy WP/Divi. 403 przy logowaniu to zwykle: reguła w .htaccess, wtyczka bezpieczeństwa (Wordfence, iThemes), WAF na hostingu, błędna konfiguracja REST/cookies, albo wymuszone HTTPS. Bez dostępu do logów/kodu nie da się powiedzieć, KTÓRE — ale naprawa jest w zakresie każdego z tych scenariuszy.

POLE_DO_POPISU: NIE MA. Klient nie podał ani nazwy wtyczki bezpieczeństwa, ani hostingu, ani wersji WP/PHP — nie ma kotwicy na żadną tezę. 403 to temat diagnozy, nie popisu. Jeśli w odpowiedzi klient napisze "mamy Wordfence" albo "na hostingu X" — wtedy owszem, wchodzi konkret, ale teraz nie mamy nic. Merytoryka nie wchodzi.

SCIEZKA_MERYTORYKI: ZADNA (brak dowodu, brak kotwicy — nie wiemy nawet, przy jakim logowaniu jest 403, więc każda teza byłaby strzelaniem)

MINY_I_CIEKAWOSTKI: puste. Brak dowodu. Nie wiemy: czy 403 jest u klienta czy u wszystkich, jaki hosting, jakie wtyczki, czy było ostatnio coś zmieniane (migracja, update, HTTPS). Bez tego żadna "mina" nie ma podstawy.

ODMOWA: puste. Nie ma okazji 1-6: kanał dostępu do WP jest standardowy (admin), żadnego twardego limitu zewnętrznego, brak konfliktu zakresu (klient NIE każe przenosić, każe dopracować), brak wymogu compliance poza standardem, terminów nie wymyślał, praw autorskich nie kombinuje.

PYTANIA (3 warstwy: zakres wizualny / diagnoza 403 / zależność hostingowa):

1. Logowanie do czego dokładnie blokuje 403 — do wp-admin, do konta użytkownika na stronie, czy do jakiegoś panelu zewnętrznego? I czy błąd widzisz tylko Ty, czy każdy próbujący się zalogować? Pytam, bo mechanizm i miejsce szukania są różne (reguły WP vs .htaccess vs WAF hostingu vs konfiguracja cookies/HTTPS), a od tego zależy, czy naprawa jest w kodzie strony, czy wymaga współpracy z supportem hostingu.

2. Ile podstron obejmuje "poprawa wizualna" i co wchodzi w "drobne zmiany" poza tekstami i zdjęciami (układ sekcji? kolory? typografia? coś jeszcze)? Pytam, bo od tego zależy, czy budżet 1100 PLN pokrywa całość, czy trzeba priorytetyzować.

3. Gdzie jest strona hostowana i czy masz kontakt do supportu hostingu? Pytam, bo jeśli 403 siedzi w WAF/mod_security, zmiany robi się po stronie hostingu, a to wymaga Twojej zgody i kontaktu — wolę to wiedzieć przed startem niż w trakcie.

CO_ZLECENIE_MOWI: WordPress + Divi, strona istnieje i ma dobrą bazę, do zrobienia: poprawa wizualna, uporządkowanie tekstów i zdjęć, naprawa błędu 403 przy logowaniu, drobne zmiany, budżet 1100 PLN.

CZEGO_NIE_MOWI: gdzie konkretnie 403 (wp-admin / konto użytkownika / panel zewnętrzny), ile podstron, jaki hosting, jaka wersja WP/PHP, aktywne wtyczki (w szczególności bezpieczeństwa), czy był ostatnio update/migracja, kiedy ma być gotowe.

GRANICA_CIECIA: krótko — 2-3 zdania oferty + 3 pytania. Merytoryki zero, bo nie ma na czym jej oprzeć. Bez proszenia o dostępy na etapie oferty (to po akceptacji, nie teraz). Bez pytania o budżet (jest podany).

RESEARCH_POTRZEBNY: NIE. Standardowy stack WP/Divi, brak nietypowych integracji. Bez wiedzy, gdzie siedzi 403 i jaki jest hosting, research to strzelanie — czekam na odpowiedź klienta.

DECYZJE:
- DOPISAĆ: nic merytorycznego. W samej ofercie (poza dziennikiem) — krótko: "Mam doświadczenie z WP/Divi, dopracowuję istniejące strony i diagnozuję 403. Chętnie zrobię, potrzebuję tylko doprecyzować zakres i miejsce błędu."
- ODPOWIEDZIEĆ: na trzy pytania powyżej — pytanie 1 to diagnostyka, pytanie 2 to wycena, pytanie 3 to zależność, która może przesunąć zakres na support hostingu. Żadnych tez, żadnych min — brak dowodu.
- DOPYTAĆ: usunąłem z iteracji 1 prośbę o konto admina i panel hostingu — na etapie oferty to przedwczesne (po akceptacji, nie teraz). Zamiast tego pytam o hosting i support, bo to realnie zmienia zakres pracy. Zredukowałem też pytanie 1: klient WPROST napisał "problem z logowaniem", więc pytam o RODZAJ logowania i zasięg błędu (tylko u niego vs u wszystkich) — to realnie zmienia diagnozę, nie jest echem.
```