=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena: 22 000 – 30 000 zł netto** (przy 90 zł/h to ~245–335 h pracy). **Czas: 8–12 tygodni** przy pracy równoległej z Twoją firmą (dostępy, akceptacje etapów).

**Etapowanie (propozycja):**
- **Etap 1 – fundament (ok. 6 000–7 500 zł):** auth, role (admin/dyspozytor/kierowca), klienci + adresy, zamówienia CRUD + historia, szkielet pod Figmę.
- **Etap 2 – operacje (ok. 9 000–12 000 zł):** magazyn, panel dyspozytora, planowanie tras (ręczne), lista kierowcy na dzień.
- **Etap 3 – domknięcie (ok. 7 000–10 500 zł):** powiadomienia, raporty/statystyki, wdrożenie na Waszym serwerze, szlify responsywności.

**Uzasadnienie (krótko):** To nie jest prosty CRUD – macie pełny łańcuch zamówienie → trasa → kierowca → raport, z trzema rolami i magazynem. Figma i specyfikacja skracają pracę, ale kluczowe decyzje (optymalizacja tras, kanały powiadomień, integracje) zmieniają wycenę nawet o 30–40%.

**Czego brakuje w ogłoszeniu (wpływa na cenę):**
1. **Trasy: ręczne układanie czy automatyczna optymalizacja?** Ręczne = CRUD. Automatyczne = osobny moduł + abonament mapowy (Google/Mapbox) + koszt per request.
2. **Powiadomienia: in-app, e-mail, SMS czy push?** SMS to koszt zmienny od wolumenu (Twilio ~0,20 zł/szt.), push (FCM) darmowy, ale wymaga konfiguracji Firebase.
3. **Integracje z ERP/księgowością (Symfonia, Comarch, KSeF)?** Każda to osobny moduł i ryzyko.
4. **Czy Figma i specyfikacja są kompletne dla wszystkich modułów?** Jeśli brakuje widoków raportów/dyspozytora – doliczam projektowanie.

Daj znać, czy wchodzimy w etapowanie – wtedy wycena etapu 1 jest wiążąca, kolejne po akceptacji poprzedniego.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 22–30k jest uczciwa jako widełki przy braku Figmy i specyfikacji, ale to nie znaczy, że jest precyzyjna — przy ręcznym planowaniu tras i kompletnych makietach realnie zszedłbym do ~18–20k (200–220 h), a przy automatycznej optymalizacji + SMS + integracji ERP (Symfonia/KSeF) poszedłbym do 35k+ i to bez gwarancji, że się zmieści. Nie zgadywałem na siłę — 4 pytania w ofercie są dokładnie tym, co realnie przesuwa kwotę o 30–40%, i bez odpowiedzi każda liczba będzie widełkowa. Research (Google Maps, Mapbox, Twilio, FCM) jest przygotowany warunkowo, nie wliczony w cenę — to poprawne, bo klient nie potwierdził ani optymalizacji, ani SMS. Zostawiłbym kwotę jako „od 18 000 zł netto, po Figmie zaokrąglimy do konkretu” zamiast sztywnego 22–30k, bo sztywne widełki przy nieznanym zakresie to strzał, nie wycena.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna:** **30 000 – 42 000 zł** (330–470 h × 90 zł/h).  
**Czas:** **45–65 dni roboczych** przy pracy ok. 8 h/dzień; przy part-time proporcjonalnie dłużej.  
**Uzasadnienie:** To pełny system z backendem, frontendem, rolami, zamówieniami, magazynem, trasami, powiadomieniami, raportami i wdrożeniem — Figma skraca UI, ale nie implementację. Po zobaczeniu Figmy i specyfikacji zaokrąglę wycenę do konkretu.

**Brakuje mi:**
1. Czy Figma i specyfikacja są kompletne i obejmują wszystkie moduły?
2. Planowanie tras: ręczne przez dyspozytora czy automatyczna optymalizacja?
3. Powiadomienia: in-app, e-mail, SMS, push?
4. Integracje: ERP/księgowość/mapy, czy aplikacja samodzielna?

**Proponuję etapy:**  
1. Fundament, auth, role, klienci, magazyn.  
2. Zamówienia, panel dyspozytora, lista kierowcy.  
3. Trasy, powiadomienia, raporty, wdrożenie.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: 330–470 h na pełny system z backendem, frontendem, rolami, magazynem, trasami, raportami i wdrożeniem to dolna granica — sam backend Spring Boot z tymi modułami i testami to realnie 250–350 h, frontend React drugie tyle. Przy Twojej stawce 90 zł/h widełki 30–42k są OK jako „od”, ale nie jako „do” — jeśli klient potwierdzi automatyczną optymalizację tras, SMS i jakąkolwiek integrację ERP, bezpieczniej mówić 40–60k. Nie zgadywałem na siłę — 4 pytania są realnie potrzebne, bo każde z nich może dodać 40–100 h. Kurs 90 zł/h jest niski dla Java+React, więc nie zaniżaj godzin, żeby „wyjść na swoim” — lepiej podnieść widełki niż potem dopłacać z własnej kieszeni.

=== DeepSeek-C — RUNDA 1 ===
## Wycena

**Kwota:** 35 000 – 45 000 zł netto (przy 90 zł/h to ok. **390–500 h**)
**Czas:** 3–4 miesiące kalendarzowo, przy pracy ~30–35 h/tydz. Etapami.

### Proponowany podział na etapy

| Etap | Zakres | Kwota | Czas |
|---|---|---|---|
| 1 | Fundament: auth, role (admin/dyspozytor/kierowca), klienci + adresy, zamówienia (CRUD + historia + statusy), wdrożenie Docker na serwerze | 9 000 – 11 000 zł | 3–4 tyg. |
| 2 | Magazyn (butle/zbiorniki), panel dyspozytora, przydzielanie dostaw, lista kierowcy | 9 000 – 11 000 zł | 3 tyg. |
| 3 | Trasy i harmonogramowanie, powiadomienia (in-app), raporty i statystyki | 10 000 – 13 000 zł | 3–4 tyg. |
| 4 | Dopracowanie, testy, poprawki, responsywność mobile, dokumentacja, odbiór | 7 000 – 10 000 zł | 2–3 tyg. |

Etap 1 jest wiążący po zobaczeniu Figmy i specyfikacji. Reszta — po zamknięciu etapu 1.

### Uzasadnienie (3 zdania)

Zakres obejmuje 6 modułów + role + raporty + wdrożenie na własnym serwerze — to nie jest MVP, tylko kompletny system operacyjny dla firmy dystrybucyjnej; przy Figmie gotowej schodzi z tego głównie projektowanie UI, ale backend i logika biznesowa (statusy, uprawnienia, magazyn, trasy) to wciąż ~400 h roboty. Stawka 90 zł/h jest uczciwa i nie zawiera kosztów zewnętrznych (mapy, SMS, hosting) — te są po stronie klienta albo doliczane osobno. Etapowanie chroni obie strony: klient widzi działającą część po 3–4 tyg., ja nie zarywam się na 4 miesiące bez odbioru.

### Czego brakuje w zleceniu (wpływa na wycenę)

1. **Planowanie tras: ręczne czy automatyczne?** Ręczne (dyspozytor układa sam) = zwykły CRUD, mieści się w etapie 3. Automatyczna optymalizacja = osobny moduł + zewnętrzne API map (Google/Mapbox, koszt abonamentowy po stronie klienta) i +40–60 h. **To największy mnożnik wyceny w tym zleceniu.**
2. **Powiadomienia: in-app, e-mail, SMS, push?** In-app i push (FCM) — bez kosztów per wiadomość. SMS (Twilio ~0,19 zł/szt.) — koszt zmienny zależny od wolumenu, bez danych o liczbie dostaw/dzień nie da się oszacować.
3. **Integracje z ERP / księgowością (Symfonia, Comarch, KSeF, bank)?** Ogłoszenie milczy — każda integracja to osobny moduł i osobne ryzyko.
4. **Czy Figma i specyfikacja są kompletne i obejmują wszystkie moduły z ogłoszenia (panel dyspozytora, lista kierowcy, raporty)?** Od tego zależy, czy etap 1 jest wiążący, czy trzeba doliczyć projektowanie brakujących widoków.
5. **Szczegóły serwera** (OS, Docker, dostęp, backupy) i **wolumen** (użytkownicy, zamówienia/dzień) — do oszacowania kosztów zewnętrznych i konfiguracji.

Portfolio i linki do realizacji wyślę w ofercie po kontakcie.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: wycena jest obroniona, ale na dolnej granicy widełek — 400 h na 6 modułów w Java/Spring Boot + React z RBAC, magazynem, raportami i wdrożeniem to optymistyczne założenie, bliżej realiów byłoby 450–550 h, czyli ~40–50 tys. zł. Nie zgadywałem tam, gdzie klient podał wprost (stack, moduły, Figma), ale **dopisałem od siebie Docker** — klient napisał tylko „własny serwer”, więc konteneryzacja to moja decyzja, nie wymóg, i lekko zawyża etap 1; bez Dockera etap 1 mógłby być tańszy o ~1 tys. zł. Największe ryzyko to wciąż nierozstrzygnięte: ręczne vs automatyczne trasy (mnożnik +40–60 h i abonament map) oraz kanały powiadomień — jeśli klient potwierdzi auto-optymalizację i/lub SMS, całość realnie rośnie do **50–65 tys. zł**, więc trzymam widełka 35–45 tys. tylko jako wycenę bazową przy ręcznym planowaniu i powiadomieniach in-app/push. Nie poprawiam kwoty na siłę — koryguję interpretację: to nie jest „cena za całość”, tylko „cena za zakres domyślny, wiążąca dla etapu 1 po zobaczeniu Figmy”.

=== DeepSeek-D — RUNDA 1 ===
**Wycena:** 36 000 – 54 000 zł (przy 90 zł/h, ok. 400–600 h).  
**Czas:** 60–90 dni roboczych (3–4,5 miesiąca) przy pracy solo i etapowych odbiorach.

**Uzasadnienie:** Zakres to pełny system wewnętrzny — backend, frontend, role, magazyn, trasy, raporty i wdrożenie — a nie prosty CRUD. Wycena zakłada ręczne planowanie tras, powiadomienia in-app i brak integracji z ERP/księgowością; automatyzacja tras, SMS/push lub integracje zewnętrzne zwiększają kwotę i czas.

**Czego brakuje:**  
- czy planowanie tras ma być ręczne czy automatyczne (optymalizacja),  
- kanały powiadomień: in-app / e-mail / SMS / push,  
- integracje z istniejącymi systemami (ERP, księgowość, mapy),  
- czy Figma i specyfikacja są kompletne i obejmują wszystkie moduły,  
- wolumen użytkowników/zamówień/dostaw, dostęp do serwera, etapy akceptacji i termin.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: kwota 36–54 tys. jest obroniona dla zakresu **z ręcznym planowaniem tras** i powiadomieniami in-app — to najbezpieczniejsze założenie, ale właśnie dlatego dolna granica jest zaniżona, jeśli klient dopowie „optymalizacja automatyczna” (wtedy +15–25 tys. i +3–4 tyg.). Nie zgadywałem integracji ERP/SMS/KSeF — słusznie, bo ich w ogłoszeniu nie ma, a doklejanie ich na siłę zawyżałoby ofertę bez podstawy. Jedno realne niedoszacowanie: **wdrożenie na „własnym serwerze” klienta** — nieznany OS, brak info o Dockerze, backupach i monitoringu; to potrafi zjeść 20–40 h, których w widełkach nie wyróżniłem. Druga rzecz: testy, dokumentacja i poprawki po odbiorach etapowych — przy 8 modułach i 3 rolach to nie jest „dodatek”, tylko osobna pozycja; realnie dodałbym 3–5 tys. do górnej granicy. Nie zmieniam widełek, ale jeśli klient potwierdzi automatykę tras — koryguję ofertę do **55–75 tys. zł**.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 35000,
  "kwota_gorna": 50000,
  "definitywna": false,
  "od_czego_zaleza": [
    "kompletności i zakresu Figmy oraz specyfikacji wymagań",
    "czy planowanie tras ma być ręczne, czy automatycznie optymalizowane z API map",
    "kanałów powiadomień: in-app, e-mail, push, SMS",
    "integracji z ERP, księgowością, KSeF, bankiem lub mapami",
    "szczegółów wdrożenia na własnym serwerze: OS, Docker, backupy, monitoring, dostęp",
    "wolumenu użytkowników i dostaw oraz zakresu testów, dokumentacji i poprawek poodbiorowych"
  ],
  "dni_od": 60,
  "dni_do": 90,
  "uzasadnienie": "Większość modeli (B, C, D) lokuje bazowy zakres przy ręcznym planowaniu tras, powiadomieniach in-app i braku integracji ERP w przedziale ok. 30–54 tys. zł; A jest wyraźnie niższy (22–30 tys., po autokrytyce nawet od 18 tys.), co przy pełnym systemie z 3 rolami, magazynem, trasami i raportami wygląda na niedoszacowanie. Zbieżność dotyczy też etapowania i tego, że Figma skraca UI, ale nie backend ani logikę biznesową. Rozbieżność pojawia się głównie przy automatycznej optymalizacji tras, SMS i integracjach ERP/KSeF, które podnoszą wycenę do ok. 50–75 tys. zł. Dlatego finalnie przyjmuję widełki 35–50 tys. zł netto jako bazę dla zakresu domyślnego, ale nie definitywną, dopóki klient nie odpowie na pytania zakresowe."
}

=== FINALNA WYCENA ===
35000-50000 zl netto | 60-90 dni | WIDELKI
Od czego zalezy: kompletności i zakresu Figmy oraz specyfikacji wymagań, czy planowanie tras ma być ręczne, czy automatycznie optymalizowane z API map, kanałów powiadomień: in-app, e-mail, push, SMS, integracji z ERP, księgowością, KSeF, bankiem lub mapami, szczegółów wdrożenia na własnym serwerze: OS, Docker, backupy, monitoring, dostęp, wolumenu użytkowników i dostaw oraz zakresu testów, dokumentacji i poprawek poodbiorowych
Uzasadnienie rozjemcy: Większość modeli (B, C, D) lokuje bazowy zakres przy ręcznym planowaniu tras, powiadomieniach in-app i braku integracji ERP w przedziale ok. 30–54 tys. zł; A jest wyraźnie niższy (22–30 tys., po autokrytyce nawet od 18 tys.), co przy pełnym systemie z 3 rolami, magazynem, trasami i raportami wygląda na niedoszacowanie. Zbieżność dotyczy też etapowania i tego, że Figma skraca UI, ale nie backend ani logikę biznesową. Rozbieżność pojawia się głównie przy automatycznej optymalizacji tras, SMS i integracjach ERP/KSeF, które podnoszą wycenę do ok. 50–75 tys. zł. Dlatego finalnie przyjmuję widełki 35–50 tys. zł netto jako bazę dla zakresu domyślnego, ale nie definitywną, dopóki klient nie odpowie na pytania zakresowe.
