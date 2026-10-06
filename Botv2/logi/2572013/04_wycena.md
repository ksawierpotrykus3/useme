=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena: 3 200–4 200 zł netto** (35–47 h × 90 zł/h)

**Czas: 7–10 dni roboczych**

**Uzasadnienie:** Zakres obejmuje konfigurację agenta głosowego (ElevenLabs Conversational AI + oficjalny widget WP), wdrożenie RAG na bazie wiedzy HVAC, strojenie barge-in i latencji pod polski głos, wpięcie widgetu w stronę oraz testy scenariuszy. Widełki, bo nie znam rozmiaru i formatu bazy wiedzy ani miejsca docelowego zbieranych danych — to dwa czynniki, które najmocniej zmieniają nakład pracy. Do tego dochodzi element RODO (klauzula + zgoda na nagrywanie + retencja), którego w zleceniu nie ma, a przy zbieraniu danych osobowych przez rozmowę jest konieczny.

**Uwaga:** koszty API (ElevenLabs, LLM) są po stronie klienta — orientacyjnie 100–300 zł/mies. przy niewielkim ruchu.

**Czego brakuje do wyceny w punkt:**
1. Gdzie i w jakim formacie jest baza wiedzy firmy (dokumenty, FAQ, arkusze, CRM)?
2. Gdzie mają trafiać dane zebrane od klienta (CRM, kalendarz, e-mail, zapis w WP)?
3. WordPress self-hosted czy WordPress.com (i jaki plan)?

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 3 200–4 200 zł są obronne, ale górna granica lekko naciągnięta — 47 h zakłada najgorszy scenariusz (bajzel w bazie wiedzy + integracja z CRM-em), którego nie znam, więc to zabezpieczenie, nie realna prognoza. Realistycznie przy ElevenLabs Conversational AI + oficjalnym pluginie WP większość pracy to RAG i testy scenariuszy, nie samo wpięcie widgetu — 28–38 h (2 500–3 400 zł) to uczciwsze centrum, jeśli baza wiedzy jest w sensownym formacie. Nie zgadywałem przy RODO i przy „WP = host widgetu, nie backend” — to realne luki w ogłoszeniu, nie dopisane na siłę. Nie zmyślałem case studies HVAC, bo research potwierdził, że takich w PL nie ma — i tego bym nie ruszał. Jak klient odpowie na 3 pytania, wycena zwęzi się do punktu; na razie trzymam widełki, ale dół bym opuścił do 2 800 zł.

=== DeepSeek-B — RUNDA 1 ===
**Wycena: 4500–7000 zł netto** (ok. 50–75 h × 90 zł/h) — widełki, bo zakres zależy od bazy wiedzy i integracji.
**Czas: 10–15 dni roboczych** (kalendarzowo ~3 tygodnie przy pracy równoległej z Twoją stroną).

**Uzasadnienie:** Zakres to nie „wtyczka”, tylko integracja z zewnętrznym pipeline’em głosowym (STT strumieniowe → LLM + RAG → TTS z VAD/barge-in), plus widget JS na WordPressie i kalibracja pod naturalny polski głos i niską latencję. Najwięcej pracy pochłania RAG na Waszej bazie wiedzy i testy jakości rozmowy, nie samo wpięcie na stronę. Dolna granica widełek zakłada gotową, uporządkowaną bazę wiedzy i prosty eksport danych (e-mail/zapis w WP); górna — porządkowanie treści i integrację z CRM/kalendarzem.

**Czego brakuje do wyceny w punkt:**
1. Gdzie i w jakim formacie jest baza wiedzy firmy (dokumenty, FAQ, arkusz, CRM)?
2. Gdzie mają trafiać dane zbierane od klienta — CRM, kalendarz, e-mail, zapis w WP?
3. WordPress self-hosted czy WordPress.com (i na jakim planie)? To decyduje, czy w ogóle da się wstawić własny widget JS.

Dodatkowo: w zleceniu nie ma słowa o zgodach na nagrywanie rozmowy i klauzuli informacyjnej RODO — to trzeba dołożyć w ramach projektu (klauzula przed startem rozmowy + zgoda + retencja), inaczej wdrożenie jest ryzykowne prawnie.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 4500–7000 zł są obronne, ale dolna granica jest zbyt optymistyczna — jeśli baza wiedzy okaże się nieuporządkowana (PDF-y, maile, brak FAQ), samo RAG + kalibracja polskiego głosu zjada 30–40 h, zanim dotknę integracji. Górna granica też może pęknąć przy CRM/kalendarzu — wtedy realnie 8000–10000 zł, bo dochodzi mapping danych i testy end-to-end. Nie zmyśliłem żadnego case study HVAC (bo go nie mam), ale „ElevenLabs ma oficjalny widget WP” potwierdziłem w researchu, więc to nie zgadywanie. RODO nie jest miną z powietrza — klient wprost pisze o zbieraniu danych i rozmowie głosowej, więc to realna luka, nie straszenie. Korekta: **4500–9000 zł netto**, z zastrzeżeniem, że po odpowiedziach na 3 pytania zawężę do punktu.

=== DeepSeek-C — RUNDA 1 ===
Wycena: **5 400–8 100 zł** (60–90 h × 90 zł/h).  
Czas: **10–15 dni roboczych** od przekazania kompletnych materiałów.

Uzasadnienie: To nie jest wtyczka, która sama robi voicebota — WordPress dostaje widget, a pipeline głosowy (streaming STT → LLM + RAG → TTS, barge-in, niska latencja) działa poza WP; najkrótsza droga to ElevenLabs Conversational AI + widget WP. Wycena zależy głównie od uporządkowania bazy wiedzy, integracji z CRM/kalendarzem/e-mail i obsługi zgód RODO. Brakuje: gdzie i w jakim formacie jest baza wiedzy, gdzie mają trafiać dane klienta, czy WP jest self-hosted czy WordPress.com oraz czy są zgody/klauzula na nagrywanie i retencję.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: trochę zawyżyłem, bo wyceniałem jak custom build (LiveKit/Vapi), a sam w uzasadnieniu wskazałem krótszą ścieżkę — ElevenLabs Conversational AI + oficjalny widget WP, gdzie barge-in, VAD i streaming są out-of-the-box. Przy managed platform realna praca to głównie RAG/baza wiedzy, prompt i strażniki (żeby nie halucynował cen), integracja z CRM/kalendarzem/e-mail, RODO (klauzula, zgoda na nagranie, retencja) i testy — czyli bliżej **35–50 h = 3 150–4 500 zł** na MVP. Widełki 5 400–8 100 zł bronią się tylko przy wariancie custom (LiveKit/Vapi) lub gdy baza wiedzy jest w chaosie i dochodzi głębsza integracja. Rekomendacja: podać klientowi **3 500–6 000 zł** na start (managed) i zaznaczyć, że kwota rośnie, jeśli wchodzimy w custom pipeline albo skomplikowane integracje — inaczej wycena wygląda na strzał w ciemno i przepłaca na starcie. Nic nie dopisałem na siłę poza RODO, ale to akurat realna luka w ogłoszeniu, nie watolina.

=== DeepSeek-D — RUNDA 1 ===
**Wycena wstępna:** 4500–8500 zł netto (przy 90 zł/h to ok. 50–95 h).  
**Czas:** 15–25 dni roboczych od dostarczenia materiałów.

**Uzasadnienie:**  
Zakres obejmuje widget na WordPressa oraz zewnętrzny pipeline głosowy PL (streaming STT → LLM + RAG → TTS) z obsługą barge-in i niskiej latencji, co wymaga starannego strojenia i testów. Największa niepewność to format i miejsce bazy wiedzy oraz integracje z CRM/kalendarzem – to może wydłużyć prace. Dodatkowo RODO (zgody, klauzula, retencja) trzeba wpiąć przed startem, co również wpływa na zakres.

**Brakuje mi:**  
1. Gdzie i w jakim formacie jest baza wiedzy firmy?  
2. Gdzie mają trafiać dane z rozmów (CRM, kalendarz, e-mail, zapis w WP)?  
3. WordPress jest self-hosted czy na WordPress.com (i na jakim planie)?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena 4500–8500 zł jest OK jako widełki, ale dół jest zaniżony, jeśli RAG + integracje (CRM/kalendarz) + RODO wejdą w zakres — realnie celowałbym 6000–12000 zł netto. Nie zgadłem na siłę: brak danych o bazie wiedzy i miejscu zapisu danych to główne zmienne, które mogą rozjechać wycenę w obie strony. Barge-in i latencja to nie zgadywanie — klient wprost o to pyta, a to jest wykonalne przy streamingu na każdym etapie. RODO dopisałem świadomie jako element zakresu, nie straszenie — bez tego wdrożenie jest po prostu niezgodne. Jak chcesz, mogę dać dwie wersje wyceny: minimalny zakres (tylko widget + FAQ) i pełny (z integracjami i RODO).

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 3500,
  "kwota_gorna": 8000,
  "definitywna": false,
  "od_czego_zaleza": [
    "format i uporządkowanie bazy wiedzy firmowej pod RAG",
    "miejsce i sposób zapisu danych z rozmów: CRM, kalendarz, e-mail, zapis w WP",
    "czy WordPress jest self-hosted, czy na WordPress.com i na jakim planie",
    "zakres RODO: klauzula, zgoda na nagrywanie, retencja danych",
    "wybór ścieżki managed (np. ElevenLabs) vs custom pipeline oraz głębokość integracji"
  ],
  "dni_od": 10,
  "dni_do": 20,
  "uzasadnienie": "Modele zgodnie wskazują, że to nie jest zwykła wtyczka WordPress, lecz widget na stronie plus zewnętrzny pipeline głosowy STT → LLM + RAG → TTS, a najkrótsza ścieżka to ElevenLabs Conversational AI i oficjalny widget WP. Zbieżność dotyczy też kluczowych niewiadomych: brakuje danych o bazie wiedzy, miejscu zapisu danych, typie WordPressa oraz zgodach RODO. Rozbieżność wycen jest duża: po autokrytyce modele podają od ok. 2 800–4 200 zł do 6 000–12 000 zł, bo część zakłada managed MVP, a część custom pipeline i głębsze integracje. Dlatego finalnie przyjmuję widełki 3 500–8 000 zł netto: dolna granica dla prostego, dobrze przygotowanego wdrożenia managed, górna dla uporządkowania wiedzy, integracji z CRM/kalendarzem i pełnego RODO. Wycena nie jest definitywna do odpowiedzi na pytania o bazę wiedzy, integracje i plan WordPressa."
}

=== FINALNA WYCENA ===
3500-8000 zl netto | 10-20 dni | WIDELKI
Od czego zalezy: format i uporządkowanie bazy wiedzy firmowej pod RAG, miejsce i sposób zapisu danych z rozmów: CRM, kalendarz, e-mail, zapis w WP, czy WordPress jest self-hosted, czy na WordPress.com i na jakim planie, zakres RODO: klauzula, zgoda na nagrywanie, retencja danych, wybór ścieżki managed (np. ElevenLabs) vs custom pipeline oraz głębokość integracji
Uzasadnienie rozjemcy: Modele zgodnie wskazują, że to nie jest zwykła wtyczka WordPress, lecz widget na stronie plus zewnętrzny pipeline głosowy STT → LLM + RAG → TTS, a najkrótsza ścieżka to ElevenLabs Conversational AI i oficjalny widget WP. Zbieżność dotyczy też kluczowych niewiadomych: brakuje danych o bazie wiedzy, miejscu zapisu danych, typie WordPressa oraz zgodach RODO. Rozbieżność wycen jest duża: po autokrytyce modele podają od ok. 2 800–4 200 zł do 6 000–12 000 zł, bo część zakłada managed MVP, a część custom pipeline i głębsze integracje. Dlatego finalnie przyjmuję widełki 3 500–8 000 zł netto: dolna granica dla prostego, dobrze przygotowanego wdrożenia managed, górna dla uporządkowania wiedzy, integracji z CRM/kalendarzem i pełnego RODO. Wycena nie jest definitywna do odpowiedzi na pytania o bazę wiedzy, integracje i plan WordPressa.
