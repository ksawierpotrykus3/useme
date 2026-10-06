=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena:**
- **Całość:** 22 000–36 000 zł, **30–50 dni roboczych**.
- **Etap 1 (moduł wycen: cennik → VAT 8/23 → zaliczka 30% → zapis do Sheets + workflow n8n):** 2 700–4 500 zł, **4–7 dni roboczych**.

**Uzasadnienie:** Opis obejmuje 8+ integracji, analizę maili/PDF, Fakturownię, SMS, kalendarz, generowanie dokumentów i odbiór „w pełni działający” z 14-dniowym bugfixem — przy 90 zł/h to setki godzin. Budżet 2890 zł pokrywa tylko wąski moduł, dlatego proponuję start od wycen i kolejne etapy. Umowy/faktury robiłbym szablonowo, a LLM tylko do wypełniania pól — nie jako generator dokumentów.

**Brakuje:** wolumenu (maile/dzień, wyceny/mc), formatów cenników i plików producentów, dostawcy SMS/poczty/kalendarza, planu Fakturowni, decyzji n8n cloud vs self-hosted i budżetu na OpenAI. RODO: wysyłanie maili/faktur do OpenAI wymaga DPA/DPIA — bez tego nie wdrażam na produkcję.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena etapu 1 (2 700–4 500 zł) jest OK i realnie mieści się w budżecie 2 890 zł tylko na dolnej granicy — przy 90 zł/h to 30–50 h, co na moduł wycen z VAT, zaliczką i zapisem do arkusza wystarcza, ale bez zapasu na iteracje z klientem. Wycena całości 22–36 tys. zł jest raczej **zaniżona niż zawyżona** — 8+ integracji z API (Fakturownia, SMS, Google, OpenAI), analiza PDF/maili, RODO i 14 dni darmowego bugfixu to spokojnie 300–450 h, czyli 27–40 tys. zł, a „w pełni działający system” bez definicji per moduł to otwarte ryzyko zakresu. Nie zgadłem na siłę żadnej pozycji — raczej nie doliczyłem utrzymania n8n self-hosted (VPS, backup, monitoring) po stronie klienta ani czasu na DPIA/DPA, co jest poza moją pracą, ale wpływa na harmonogram. Korekta: górną granicę całości podniósłbym do **40 000 zł**, a etap 1 zostawił jako 2 700–3 500 zł (żeby realnie zmieścić się w 2 890 zł z małym buforem) — ale nadal twierdzę, że bez zawężenia zakresu do jednego modułu ten budżet nie pokryje całości.

=== DeepSeek-B — RUNDA 1 ===
**KWOTA:** Całość realnie **12 000 – 18 000 zł** (przy 90 zł/h to ok. 130–200 h). Za budżet 2890 zł da się domknąć **jeden moduł** — proponuję start od wycen: cennik → VAT 8/23% → zaliczka 30% → zapis do arkusza. Wycena etapu 1: **2500–3000 zł**.

**CZAS:** Całość 6–8 tygodni (przy pracy part-time). Moduł wycen: 3–5 dni roboczych.

**UZASADNIENIE:** W briefie jest 8 integracji (n8n, OpenAI, mail, Drive, Sheets, Fakturownia, SMS, kalendarz) plus generowanie umów, faktur, protokołów i zleceń montażu — to nie jest projekt na 2890 zł, tylko na wiele tygodni. Budżet 2890 zł pokrywa rzetelnie jeden moduł, nie całość. Uczciwiej powiedzieć to teraz niż wpaść w niedokończony projekt za dwa miesiące.

**CZEGO BRAKUJE:**
1. **Formaty cenników i plików producentów** („WEB”, „Kosztorys WEB”) — Excel/CSV, PDF z tabelami, skany? Od tego zależy metoda ekstrakcji i czy da się to domknąć.
2. **Wolumen:** ile maili/dzień, wycen/mc, klientów, plików/mc — to bezpośrednio wpływa na koszty OpenAI API i liczbę wykonań n8n (przy cloud Starter 2500/mc szybko się skończy — rekomenduję self-hosted).
3. **Dostawca SMS i poczty/kalendarza** (domyślnie: SMSAPI + Google Workspace?).
4. **Plan Fakturowni** — czy API jest włączone w Waszym pakiecie.

**UWAGA:** Wymagania RODO — wysyłanie maili klientów i faktur do OpenAI API oznacza transfer danych osobowych i finansowych do USA. Bez DPA i aktualizacji polityki prywatności system nie powinien iść na produkcję.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: kwota 12–18k za całość jest raczej zaniżona, nie zawyżona — 8 integracji plus deterministyczne dokumenty (umowa, faktury, protokoły) i 14 dni darmowego bugfixu to raczej 180–280 h, czyli 16–25k zł, a nie 130–200 h. Etap 1 (moduł wycen) za 2500–3000 zł jest OK tylko przy cennikach w Excelu/CSV — jeśli przyjdą jako PDF-y lub skany, to 3500–4000 zł i tak będzie uczciwe. Nie zgadywałem na siłę: RODO przy transferze maili i faktur do OpenAI to realna mina (typ 4), a „LLM nie generuje faktur/umów — szablon + LLM do pól” to nie ozdoba, tylko warunek, żeby to w ogóle przeszło odbiór. Domyślne SMSAPI/Google Workspace i rekomendacja n8n self-hosted to założenia — oznaczyłem je jako założenia, nie jako ustalenia, więc jeśli klient ma inaczej, wycena się nie zmienia, tylko konfiguracja. Korekta: całość 16–25k, etap 1 3000–4000 zł zależnie od formatu cenników.

=== DeepSeek-C — RUNDA 1 ===
**Kwota:**
- **Cały opisany zakres: 22 500–36 000 PLN** (250–400 h), 6–10 tygodni. Budżet 2890 PLN to ~32 h — pokrywa może 1 moduł, nie całość.
- **Realny etap 1 (moduł wycen): 2 700–3 200 PLN**, 5–7 dni. Zakres: cennik → VAT 8%/23% → zaliczka 30% → zapis do arkusza Google, z odbiorem na 10 przypadkach testowych.

**Uzasadnienie:** 8+ integracji (Fakturownia, Google, OpenAI, SMS, kalendarz, PDF) plus asystent AI to nie jest projekt na 32 h — sam moduł dokumentów (umowa, faktury, protokół) to osobne dni. Budżet 2890 PLN traktuję jako sygnał, że klient nie zna skali — dlatego proponuję start od jednego modułu, reszta etapami z osobnymi wycenami.

**Czego brakuje w zleceniu:**
1. **Formaty cenników i plików producentów** („WEB”, „Kosztorys WEB”) — Excel/CSV czy PDF/skan? Od tego zależy metoda ekstrakcji i czy da się to domknąć.
2. **Wolumen:** ile maili/dzień, wycen/mc, plików producentów/mc? To bezpośrednio przekłada się na koszt OpenAI API i liczbę wykonań n8n (miesięczny rachunek po stronie klienta, niezależny od mojej pracy).
3. **Plan Fakturowni** — czy API jest aktywne w Waszym pakiecie (Free/Mini/Standard/Pro)? Bez tego integracja faktur może wymagać upgrade'u.
4. **RODO** — wysyłka maili klientów, faktur i plików ofertowych do OpenAI API wymaga min. DPA z OpenAI i prawdopodobnie DPIA; bez tego system nie powinien iść na produkcję.

**Uwaga techniczna:** faktury i umowy generowałbym szablonem (docx/PDF) z LLM wypełniającym tylko zatwierdzone pola — nie „niech ChatGPT pisze fakturę”. To taniej w utrzymaniu i bezpieczniej.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Tak, wycena jest uczciwa — 250–400 h na 8+ integracji plus asystent AI to realistyczny rząd wielkości, a budżet 2890 PLN pokrywa ledwie 1 moduł i to założenie podtrzymuję. Skorygowałbym tylko jeden element: kwota „22 500–36 000 PLN” jest szacunkiem przy mojej stawce 90 zł/h i nie zawiera kosztów operacyjnych klienta (OpenAI, n8n, SMS) — to trzeba wyraźnie oddzielić, bo inaczej wygląda jak zawyżanie. Etap 1 (moduł wycen) zostawiłbym na 2 700–3 200 PLN, ale z twardym kryterium odbioru na 10 przypadkach testowych — bez tego „w pełni działający” z briefu zrobi z tego projektu studnię. Nie dopisałem na siłę niczego poza tym, co faktycznie wynika z treści zlecenia; RODO i koszty operacyjne to realne ryzyka, nie straszaki.

=== DeepSeek-D — RUNDA 1 ===
**Wycena całości: 15 000 – 20 000 zł netto (170–220 h), termin 6–8 tygodni.**

Za 2890 zł (≈32 h) nie da się zrobić 8 integracji z API, modułu wycen, generowania dokumentów, analizy maili przez LLM i odbioru „w pełni działającego systemu” z 14-dniową gwarancją. To zakres na wiele tygodni pracy, nie na tydzień.

**Propozycja realna w budżecie:** Etap 1 — sam moduł wycen (cennik → VAT 8/23 → zaliczka 30% → zapis do arkusza Google) za **2 890 zł, ok. 5–7 dni roboczych**. Reszta etapami po osobnym zleceniu.

**Czego brakuje w zleceniu, żeby wycenić rzetelnie:**
1. Format cenników i plików od producentów („WEB”, „Kosztorys WEB”) — Excel/CSV czy PDF/skan? Od tego zależy metoda ekstrakcji.
2. Wolumen: ile maili/dzień, wycen/mc, klientów, plików/mc? Od tego zależą koszty OpenAI API i liczba wykonań n8n.
3. Czy Fakturownia ma plan z API; kto ponosi koszty OpenAI, n8n i SMS po wdrożeniu.
4. Kto jest administratorem danych klientów w kontekście RODO (przepływ maili i faktur przez OpenAI API wymaga DPA i najpewniej DPIA po stronie firmy).

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena jest zasadna, ale nie „na pewno" — opiera się na zakresie, nie na wolumenie, a to największa niewiadoma. Nie zgadłem na siłę integracji (API Fakturowni, OpenAI, Google, SMS faktycznie istnieją), natomiast przyjąłem domyślnie SMSAPI i Google Workspace oraz n8n self-hosted — to założenia, nie ustalenia, więc mogą przesunąć wycenę. Kwoty 15–20 tys. zł bym nie zmieniał, ale realnie to dolna granica widełek: przy ciągłej analizie maili i dokumentów przez LLM oraz 8 integracjach raczej 18–22 tys. zł i 8–10 tygodni, nie 6–8. Etap 1 (moduł wycen) za 2 890 zł nadal aktualny — cena uczciwa za 5–7 dni, ale tylko przy założeniu, że cennik jest w Excelu/CSV, nie w skanach PDF. Największe ryzyko to nie technika, a kryterium odbioru „w pełni działający system" bez definicji per moduł — i to bym w ofercie nazwał wprost, bo inaczej każda wycena jest zaniżona.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 18000,
  "kwota_gorna": 30000,
  "definitywna": false,
  "od_czego_zaleza": [
    "Format cenników i plików producentów („WEB”, „Kosztorys WEB”) — Excel/CSV vs PDF/skan istotnie zmienia nakład na ekstrakcję",
    "Wolumen: liczba maili/dzień, wycen/mc, klientów i plików/mc — bezpośrednio wpływa na koszt OpenAI API i liczbę wykonań n8n",
    "Decyzja n8n cloud vs self-hosted oraz plan Fakturowni (czy API jest aktywne w pakiecie klienta)",
    "Zakres RODO (DPA/DPIA, rozdzielenie strumieni danych osobowych) i definicja odbioru per moduł zamiast „w pełni działający system”",
    "Domyślne założenia: SMSAPI + Google Workspace oraz stawka ~90 zł/h"
  ],
  "dni_od": 30,
  "dni_do": 50,
  "uzasadnienie": "Wszystkie cztery modele w obu rundach zgodnie twierdzą, że budżet 2890 zł nie pokrywa opisanego zakresu — realnie wystarcza na jeden moduł (wyceny: cennik → VAT 8/23% → zaliczka 30% → zapis do arkusza), wyceniany na 2500–4000 zł. Co do całości głosy rozjeżdżają się: po autokrytyce dolne granice to 16k (B) i 18k (D), a górne 22k (D), 25k (B), 36–40k (A, C) — stąd widełki 18–30k, nie punkt. Zbieżność dotyczy też jakościowej diagnozy: LLM nie powinien generować umów/faktur (szablon + LLM do pól), odbiór musi być per moduł, a RODO przy transferze maili i faktur do OpenAI to warunek wstępny, nie ozdoba. Wycena jest niepewna (niedefinitywna), bo brakuje wolumenu i formatów plików — bez nich każde oszacowanie opiera się na założeniach, nie na danych.",
  "uwaga_etap1": "Moduł wycen mieści się w budżecie 2890 zł (widełki 2700–3200 zł, 5–7 dni roboczych) i powinien być pierwszym etapem z odbiorem na 10 przypadkach testowych."
}

=== FINALNA WYCENA ===
18000-30000 zl netto | 30-50 dni | WIDELKI
Od czego zalezy: Format cenników i plików producentów („WEB”, „Kosztorys WEB”) — Excel/CSV vs PDF/skan istotnie zmienia nakład na ekstrakcję, Wolumen: liczba maili/dzień, wycen/mc, klientów i plików/mc — bezpośrednio wpływa na koszt OpenAI API i liczbę wykonań n8n, Decyzja n8n cloud vs self-hosted oraz plan Fakturowni (czy API jest aktywne w pakiecie klienta), Zakres RODO (DPA/DPIA, rozdzielenie strumieni danych osobowych) i definicja odbioru per moduł zamiast „w pełni działający system”, Domyślne założenia: SMSAPI + Google Workspace oraz stawka ~90 zł/h
Uzasadnienie rozjemcy: Wszystkie cztery modele w obu rundach zgodnie twierdzą, że budżet 2890 zł nie pokrywa opisanego zakresu — realnie wystarcza na jeden moduł (wyceny: cennik → VAT 8/23% → zaliczka 30% → zapis do arkusza), wyceniany na 2500–4000 zł. Co do całości głosy rozjeżdżają się: po autokrytyce dolne granice to 16k (B) i 18k (D), a górne 22k (D), 25k (B), 36–40k (A, C) — stąd widełki 18–30k, nie punkt. Zbieżność dotyczy też jakościowej diagnozy: LLM nie powinien generować umów/faktur (szablon + LLM do pól), odbiór musi być per moduł, a RODO przy transferze maili i faktur do OpenAI to warunek wstępny, nie ozdoba. Wycena jest niepewna (niedefinitywna), bo brakuje wolumenu i formatów plików — bez nich każde oszacowanie opiera się na założeniach, nie na danych.
