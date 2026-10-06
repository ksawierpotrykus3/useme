KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wdrożenie nowej strony) z elementem audytu/doradztwa na starcie
INTENCJA: wykonawcze
DECYDENT_I_BOL: Decydent nieznany — brief nie mówi, kto pisze (dział IR/IT/komunikacji, agencja, pośrednik). Nie zakładam. Ból z treści: nowa strona ma być bezpieczna, wydajna, zgodna z WCAG/RODO/CMP, z migracją archiwum ESPI/EBI i możliwością samodzielnego rozwoju przez zespół.
WYKONALNE: TAK. Najbliższa opcja: realizacja etapowa — analiza i IA → UX/UI → CMS → migracja treści i archiwum → compliance → testy. Jeśli archiwum nie ma eksportu/API, migracja półautomatyczna lub ręczna.
POLE_DO_POPISU: JEST, ale warunkowo: WCAG dla dokumentów w archiwum (jeśli są to PDF/Office) oraz mapa 301 dla starych URL-i archiwum. Bez potwierdzenia formatu i skali nie rozbudowuję tego w fakt.
SCIEZKA_MERYTORYKI: B warunkowo. Część min zależy od odpowiedzi klienta; bez potwierdzenia formatu archiwum zamieniam minę na pytanie.
MINY_I_CIEKAWOSTKI:
- Mina warunkowa 1: Dowód: „kompletną migrację archiwum relacji inwestorskich / ESPI / EBI” + „wdrożenie zgodne z WCAG 2.1/2.2 AA”. Mechanizm: WCAG/EN 301 549 obejmuje także dokumenty niebędące stronami (PDF/Office) udostępniane przez witrynę. Konsekwencja: jeśli archiwum zawiera takie pliki, sama zgodność szablonu strony nie wystarczy — audyt obejmie również dokumenty. Brak dowodu: brief nie mówi wprost o PDF. Dlatego nie twierdzę, że są — pytam. Alternatywa: inwentaryzacja i remediacja dokumentów albo dostępne wersje alternatywne.
- Mina warunkowa 2: Dowód: „przekierowania 301” + „kompletna migracja archiwum”. Mechanizm: każdy stary URL wymaga mapy; stare linki do dokumentów archiwum mogą nie mieć odpowiedników w nowej strukturze. Konsekwencja: 404 i utrata linków/ruchu. Brak dowodu: liczba URL i format nieznane. Alternatywa: crawl starej strony, eksport URL i mapa 301.
ODMOWA: puste. Na tym etapie brak okazji z typów 1–6; compliance jest w zakresie, nie blokuje realizacji.
PYTANIA:
1. W jakim systemie/CMS działa obecna strona i skąd będą migrowane treści oraz archiwum (eksport, API, baza, ręcznie)? — od tego zależy metoda migracji i koszt.
2. Ile podstron obejmuje nowa strona oraz ile dokumentów/wpisów liczy archiwum ESPI/EBI i w jakich formatach? — od tego zależą pracochłonność, mapa 301 i zakres ewentualnej remediacji WCAG.
CO_ZLECENIE_MOWI: nowa strona spółki finansowej; nowoczesna, bezpieczna, wydajna; możliwa do samodzielnego rozwijania przez zespół; zakres: analiza struktury, UX/UI, CMS, migracja treści i archiwum ESPI/EBI, WCAG 2.1/2.2 AA, RODO/CMP, bezpieczeństwo formularzy, Core Web Vitals, SEO/301, przygotowanie do self-service i integracji.
CZEGO_NIE_MOWI: technologii obecnej strony, CMS, liczby podstron, wolumenu i formatów archiwum, źródła danych, decydenta, terminu, budżetu poza „do negocjacji”, konkretnych integracji, hostingu, języków, zakresu self-service.
GRANICA_CIECIA: Zlecenie obszerne, ale bez danych o skali i środowisku. Odpowiedź średnia, oparta na pytaniach i warunkowych minach; bez wchodzenia w szczegóły technologiczne ponad brief.
RESEARCH_POTRZEBNY: TAK, ale tylko do potwierdzenia min warunkowych: WCAG dla dokumentów niebędących stronami oraz 301/CWV przy migracji archiwum. Research nie uzasadnia dodatkowej merytoryki poza briefem.

DECYZJE: DOPISAĆ: w ofercie warunkowe zdania — (1) jeśli archiwum zawiera PDF/Office, WCAG 2.1/2.2 AA obejmuje również te dokumenty i zaproponuję remediację; (2) dla starych URL-i archiwum potrzebna inwentaryzacja i mapa 301. ODPOWIEDZIEĆ: realizacja etapowa, otwartość na dopasowanie ceny po poznaniu materiału. DOPYTAĆ: (1) obecny CMS/system i źródło migracji; (2) liczba podstron oraz liczba i formaty dokumentów archiwum ESPI/EBI.