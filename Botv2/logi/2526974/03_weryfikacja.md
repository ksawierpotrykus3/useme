```
KWALIFIKOWALNOSC: TAK — osoba prywatna, projekt jednorazowy, budżet "do negocjacji", brak znamion scamu/rekrutacji.

TYP_ZLECENIA: projekt jednorazowy (budowa portalu na WP). Dalsza opieka/moderacja/monetyzacja — poza tym zleceniem.

INTENCJA: wykonawcze ("stworzenie portalu"), z domieszką doradczą (wybór stacku, zakres compliance).

DECYDENT_I_BOL: osoba prywatna, Polak w Wiedniu. Ból nazwany: brak lokalnego odpowiednika waw4free. Ból pod spodem: budowa niszowego portalu z monetyzacją (AdSense, artykuły sponsorowane, wyróżnienia) — brief sam to wymienia, nie zgaduję modelu.

WYKONALNE: TAK. Standardowy stack WP: wtyczka eventowa z UGC + moderacją (The Events Calendar + Community Events), taksonomie (tagi/dzielnice), i18n (Polylang Free na start), formularze, newsletter, AdSense + CMP z TCF. "Wierna kopia waw4free" — nie; "ten sam model, nowy wygląd i prostota" — tak.

POLE_DO_POPISU: JEST (wąskie) — konkretny stack wtyczek, i18n od startu, CMP pod AdSense, Impressum AT + RODO w zakresie. Reszta to propozycje TYP 2. Bez wykładu o PHP vs WP (patrz niżej — to nie jest mina dla klienta).

SCIEZKA_MERYTORYKI: B (dwie miny compliance) + TYP 2 (propozycje stacku/i18n/zakresu).

MINY_I_CIEKAWOSTKI:
- Mina 1 (RODO/UE + Google, typ 4): newsletter + konta użytkowników + AdSense → Google wymaga IAB TCF v2.2+ dla monetyzacji w UE; bez certyfikowanego CMP AdSense może odrzucić/ograniczyć monetyzację. Do tego RODO: double opt-in, polityka prywatności, banner zgód. Dowód: "zapis do newslettera", "dodawanie wydarzeń przez użytkowników", "integracja z Google AdSense". Rozwiązanie: CMP z TCF (np. Okito lub consentmanager) + polityka + double opt-in — w zakresie.
- Mina 2 (Austria, typ 4): ECG §5 — wszystkie "kommerzielle Websites" muszą mieć Impressum (adres, e-mail + telefon, WKO, nadzór). Reklamy + artykuły sponsorowane kwalifikują stronę jako komercyjną, nawet przy osobie prywatnej. Dowód: "Wiedeń", "po niemiecku", "reklamy", "artykuły sponsorowane". Rozwiązanie: Impressum + regulamin w zakresie; dane wypełnia klient.

(Research: waw4free prawdopodobnie nie stoi na WP — PHP/8.2.24, ścieżka /strona/wydarzenie.php, brak wp-content. To NIE jest mina dla klienta: nie zmienia jego decyzji, nie zabije projektu, nie wpływa na wycenę. Research wewnętrzny — zostaje u mnie. Klientowi nie mówimy "wasz wzór nie jest na WP", bo to brzmi jak podważanie wzoru.)

ODMOWA: typ 4 — dwie pominięte warstwy zgodności (Impressum AT, RODO/TCF pod newsletter + AdSense). Nie blokują projektu, wchodzą w zakres. Poza tym brak okazji: żadnego brakującego API, twardego limitu, konfliktu zakresu ani nieistniejącego terminu.

PYTANIA:
1. Skąd mają pochodzić wydarzenia na start — zasilisz bazę samodzielnie (ręcznie lub z listy, którą masz), czy ma powstać import/panel importu z istniejących źródeł? — Pytam, bo od tego zależy, czy wchodzi dodatkowy moduł importu (osobna warstwa prac), czy wystarczy panel moderacji zgłoszeń UGC. Bez tej odpowiedzi wycena jest widełkowa w bardzo szerokim zakresie.

(Pozostałe potencjalne pytania rozstrzygam propozycją TYP 2: język — proponuję niemiecki jako główny i i18n od startu gotowe na polski, żeby dodanie drugiego języka nie wymagało refaktoryzacji; monetyzacja — brief wymienia ją jako wymaganą funkcję, więc wchodzi od razu; moderacja — budujemy panel, moderuje klient.)

CO_ZLECENIE_MOWI: WordPress; portal o darmowych i tanich (≤30 €) wydarzeniach w Wiedniu; wzór waw4free.pl (funkcjonalny/UX, nie techniczny); nowoczesny, ale prosty i czytelny; lista funkcji (strona główna z polecanymi, kalendarz, tagi/filtry, stałe darmowe wydarzenia, stopka z regulaminem i newsletterem, zgłaszanie wydarzeń przez użytkowników z moderacją, formularz kontakt/reklama, sekcja artykułów + sponsorowane, responsywność, język niemiecki, wydarzenia cykliczne/płatne/wyróżnione, reklamy + AdSense); stocki Canva/Pexels; SEO, UX, WP.

CZEGO_NIE_MOWI: hosting/domena; kto fizycznie moderuje; źródło wydarzeń (import? ręcznie?); provider newslettera; skala (ilu użytkowników/wydarzeń); czy ma być też wersja polska; konkretny budżet; termin; czy klient ma działalność w Austrii.

GRANICA_CIECIA: zlecenie wielowarstwowe (i18n, źródło treści, monetyzacja, compliance), ale brief jest gęsty — klient podał dużo. Warstwy rozstrzygnięte: i18n (propozycja), monetyzacja (wymóg w briefie), compliance (my dodajemy). Jedna warstwa otwarta: źródło wydarzeń → 1 pytanie. Do tego krótka propozycja stacku + 2 miny compliance bez straszenia. Bez wykładu o PHP/WP (research wewnętrzny). Wycena: zakres otwarty tylko w jednym punkcie → widełki orientacyjne + otwartość ("dopasuję po jednej odpowiedzi").

RESEARCH_POTRZEBNY: TAK (już wykonany). Potwierdzone: The Events Calendar + Community Events dla UGC z moderacją; Polylang Free dla i18n; CMP z TCF v2.3 dla AdSense (Okito / consentmanager); wymogi Impressum AT z ECG §5. Wystarczy do konkretnej propozycji. Nie obiecywać funkcji, których wtyczki nie mają (np. Community Events sam nie ogranicza zgłoszeń do Wiednia — wymaga dopisania reguł poza wtyczką).

DECYZJE:
- DOPISAĆ do oferty: konkretny stack (The Events Calendar + Community Events; Polylang Free z i18n od startu pod ewentualny drugi język; CMP z TCF pod AdSense; Impressum AT + polityka RODO w zakresie); widełki orientacyjne + zdanie otwartości ("dopasuję po odpowiedzi o źródło wydarzeń"); propozycję i18n od razu (niemiecki główny + przygotowanie pod polski) — TYP 2, nie pytanie; potwierdzenie, że wzór waw4free traktujemy jako wzór UX, nie do klonowania.
- ODPOWIEDZIEĆ na brief: potwierdzić zrozumienie zakresu, wypunktować, które funkcje wchodzą w standardzie WP a które wymagają dodatkowego modułu, wskazać dwie miny compliance (Impressum AT, AdSense+TCF/RODO) i jak je rozwiązujemy — ton rzeczowy, bez straszenia.
- DOPYTAĆ: tylko o źródło wydarzeń na start (jedno pytanie, TYP 1, z uzasadnieniem wycenowym).
```