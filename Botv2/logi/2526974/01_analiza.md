```
KWALIFIKOWALNOSC: TAK — realny decydent (osoba prywatna), projekt jednorazowy, budżet "do negocjacji", brak znamion scamu/rekrutacji/phantomu.

TYP_ZLECENIA: projekt jednorazowy (budowa portalu na WP). Ewentualna dalsza opieka (moderacja, monetyzacja) — poza tym zleceniem.

INTENCJA: wykonawcze ("stworzenie portalu").

DECYDENT_I_BOL: osoba prywatna, Polak mieszkający w Wiedniu. Ból nazwany: brak lokalnego odpowiednika waw4free. Ból pod spodem: prawdopodobnie chęć monetyzacji (AdSense, artykuły sponsorowane, wyróżnienia) i/lub projekt społecznościowy — nie przesądzam, ale brief sam podaje reklamy.

WYKONALNE: TAK. Standardowy stack WP: wtyczka eventowa z modułem zgłoszeń UGC + moderacją (np. The Events Calendar + Community Events), taksonomie (tagi/dzielnice), i18n (Polylang/WPML albo tylko niemiecki), formularze, newsletter, wpięcie AdSense. Jeśli klient chciałby "wiernej kopii" waw4free — nie; "ten sam model, nowy wygląd i prostota" — tak.

POLE_DO_POPISU: JEST (wąskie) — zgodność prawna dla strony w Wiedniu z reklamami (Impressum, RODO/cookies) + konkretny stack. Reszta to propozycje TYP 2.

SCIEZKA_MERYTORYKI: B (mina compliance) + TYP 2 (propozycje stacku/zakresu).

MINY_I_CIEKAWOSTKI:
- Mina (RODO/UE, typ 4): newsletter + konta użytkowników + AdSense → double opt-in, polityka prywatności, banner zgód (TCF pod AdSense). Dowód: "zapis do newslettera", "dodawanie wydarzeń przez użytkowników", "integracja z Google AdSense". Skutek: bez tego AdSense może odrzucić/ograniczyć, a RODO to realne ryzyko.
- Mina (Austria, typ 4): komercyjna strona w Wiedniu po niemiecku → Impressumspflicht (ECG). Dowód: "Wiedeń", "po niemiecku", "reklamy", "artykuły sponsorowane". Rozwiązanie: dodaję stronę Impressum + regulamin w zakresie.
- Ciekawostka/architektura: "stałe darmowe wydarzenia (muzea w poniedziałki)" modelować jako reguły cykliczne, nie jako kopie wpisów — inaczej kalendarz puchnie. To raczej propozycja niż mina.

ODMOWA: typ 4 — dwa pominięte elementy zgodności (Impressum AT, RODO/cookies pod newsletter + AdSense). Nie blokują projektu, wchodzą w zakres. Poza tym brak okazji do odmowy: żadnego brakującego API, twardego limitu, konfliktu zakresu ani nieistniejącego terminu.

PYTANIA:
1. Czy portal ma być tylko po niemiecku, czy też po polsku (dla polskiej społeczności w Wiedniu)? — "język niemiecki" w briefie jest niejednoznaczne; od tego zależy architektura i18n i zakres tłumaczeń.
2. Skąd mają pochodzić wydarzenia na start: tylko zgłoszenia użytkowników, czy też sam/a będziesz zasilać bazę (ręcznie lub importem)? — decyduje, czy wchodzi import/scraper, czy wystarczy panel moderacji.
3. Monetyzacja (AdSense, artykuły sponsorowane, wyróżnienia) ma być gotowa na start czy w drugim etapie? — od tego zależy zakres i wycena.

CO_ZLECENIE_MOWI: WordPress; portal o darmowych i tanich (≤30 €) wydarzeniach w Wiedniu; wzór waw4free.pl; nowoczesny, ale prosty i czytelny; lista funkcji (strona główna z polecanymi, kalendarz, tagi/filtry, stałe darmowe wydarzenia, stopka z regulaminem i newsletterem, zgłaszanie wydarzeń przez użytkowników z moderacją, formularz kontakt/reklama, sekcja artykułów + sponsorowane, responsywność, język niemiecki, wydarzenia cykliczne/płatne/wyróżnione, miejsce na reklamy + AdSense); stocki Canva/Pexels; SEO, UX, WP.

CZEGO_NIE_MOWI: hosting/domena; kto moderuje; źródło wydarzeń (import?); provider newslettera; skala (ilu użytkowników/wydarzeń); czy też polski; konkretny budżet; termin; czy ma działalność/firmę w Austrii (dla Impressum).

GRANICA_CIECIA: zlecenie wielowarstwowe (język, źródło treści, monetyzacja, technika) → 3 pytania + krótka propozycja stacku + 1–2 miny compliance. Bez rozbudowanej merytoryki — klient podał funkcje, nie pyta o technologię, więc research zostaje u mnie. Wycena: zakres otwarty → widełki orientacyjne + otwartość ("dopasuję po doprecyzowaniu"), nie defensywne "to byłoby zgadywanie".

RESEARCH_POTRZEBNY: TAK — potwierdzić, na czym stoi waw4free (inspiracja, nie kopia), dobrać aktualne wtyczki WP do eventów UGC + i18n + AdSense, zweryfikować wymogi Impressum/RODO dla Austrii. Po to, żeby propozycja była konkretna i wykonalna, a nie obiecywała funkcji, których wtyczki nie dają.
```