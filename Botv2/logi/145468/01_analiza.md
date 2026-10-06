KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wdrożenie nowej strony) z elementem audytu/doradztwa na starcie
INTENCJA: wykonawcze
DECYDENT_I_BOL: Prawdopodobnie dział komunikacji/IR/IT w spółce finansowej, być może publicznej (ESPI/EBI). Ból: stara/trudna w utrzymaniu strona, wymogi WCAG/RODO/CMP, bezpieczeństwo danych i formularzy, potrzeba samodzielnego rozwoju przez zespół.
WYKONALNE: TAK. Najbliższa opcja: realizacja etapowa — audyt i IA → UX/UI → CMS → migracja treści i archiwum → compliance → testy. Jeśli archiwum nie ma eksportu/API, migracja półautomatyczna lub ręczna.
POLE_DO_POPISU: JEST. WCAG 2.2 AA dla dokumentów PDF w archiwum ESPI/EBI; mapowanie 301 dla tysięcy URL-i; CMP a RODO; Core Web Vitals; bezpieczeństwo formularzy.
SCIEZKA_MERYTORYKI: B
MINY_I_CIEKAWOSTKI:
- Dowód: „kompletną migrację archiwum relacji inwestorskich / ESPI / EBI” + „wdrożenie zgodne z WCAG 2.1/2.2 AA”. Mina: WCAG AA obejmuje także dokumenty PDF w archiwum; sama strona zgodna nie wystarczy. Konsekwencja: formalny brak zgodności. Alternatywa: audyt/remediacja PDF lub dostępne wersje dokumentów.
- Dowód: „przekierowania 301” + „kompletna migracja archiwum”. Mina: archiwum IR ma często tysiące unikalnych URL-i do PDF; bez mapy 301 utrata linków i ruchu. Alternatywa: inwentaryzacja URL i mapa przekierowań.
ODMOWA: puste
PYTANIA:
1. Ile podstron i ile dokumentów w archiwum ESPI/EBI (lata, formaty) obejmuje migracja? — od tego zależy pracochłonność, ryzyko i wycena.
2. W jakim systemie/CMS działa obecna strona i skąd będą migrowane treści oraz archiwum (eksport, API, baza, ręcznie)? — od tego zależy metoda migracji i koszt.
CO_ZLECENIE_MOWI: nowa strona spółki finansowej; nowoczesna, bezpieczna, wydajna; możliwa do samodzielnego rozwijania przez zespół; zakres: analiza struktury, UX/UI, CMS, migracja treści i archiwum ESPI/EBI, WCAG 2.1/2.2 AA, RODO/CMP, bezpieczeństwo formularzy, Core Web Vitals, SEO/301, przygotowanie do self-service i integracji.
CZEGO_NIE_MOWI: technologii obecnej strony, CMS, liczby podstron, wolumenu archiwum, źródła danych, kto decyduje, terminu, budżetu poza „do negocjacji”, konkretnych integracji, hostingu, języków.
GRANICA_CIECIA: Zlecenie obszerne, ale bez danych o skali i obecnym środowisku. Odpowiedź średnia, skupiona na pytaniach o migrację i propozycjach; bez wchodzenia w szczegóły technologiczne ponad brief.
RESEARCH_POTRZEBNY: TAK. Po co: zweryfikować wymogi WCAG 2.2 AA dla PDF i archiwów IR, standardy CMP/RODO w finansach, Core Web Vitals i praktyki 301 przy migracji ESPI/EBI.