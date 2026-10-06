=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
Wycena: **360–450 zł** (4–5h × 90 zł/h: 2–3h spotkań + 1–2h analizy materiałów i przygotowania rekomendacji).  
Czas: **3–5 dni roboczych** od otrzymania materiałów.

Uzasadnienie: To doradztwo, nie wdrożenie — diagnoza obecnego pipeline’u i wskazanie kierunku (pre-processing, segmentacja, detekcja symboli, routing dokumentów). Nie oddaję pełnej architektury w ofercie, to materiał na płatne spotkania. Uwaga: fine-tuning Gemini 3 Pro nie jest obecnie dostępny — SFT dla 3.x Pro nie istnieje, więc warto to zweryfikować przed wyborem ścieżki.

Brakuje mi:  
1. Jak liczysz te 70% — per rysunek, per pole, per dokument?  
2. Czy masz ręcznie zweryfikowany ground-truth?  
3. Czy PDF-y z programów do wycen są wektorowe, czy to skany?

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: poprzednia wycena 360–450 zł była zaniżona, a ta z sekcji DECYZJE (1200–1500 zł) to już inflacja — przy 2–3h spotkań klient porówna to z rynkiem i może odpaść nie na wartościach, tylko na liczbie. Realistycznie: 2–3h spotkań + 3–5h analizy materiałów i przygotowania rekomendacji = 5–8h × 90 zł/h, czyli **450–720 zł**, i to jest uczciwe. Wartość „min" (brak SFT dla Gemini 3.x Pro, limit 1120 tokenów) jest duża, ale klient kupuje 2–3h konsultacji, nie projekt — nie mogę windować stawki za sam research, który robię niezależnie od zlecenia. Korekta: **600–750 zł za całość**, z jasnym rozbiciem (X zł/h × Y h), bez widełek w widełkach.

=== DeepSeek-B — RUNDA 1 ===
**Wycena:** 400–500 zł za całość (2–3 spotkania online + analiza materiałów + spisana rekomendacja).  
Jeśli liczyć wyłącznie godziny spotkań: 180–270 zł, ale wtedy nie ma czasu na rzetelne przygotowanie i wskazanie kierunku.

**Czas:** 3–5 dni roboczych od otrzymania materiałów.

**Uzasadnienie:** 2–3h spotkań + ok. 2h analizy i spisania wniosków = 4–5h × 90 zł/h. To doradztwo, nie wdrożenie, więc zakres zamyka się w konsultacji i rekomendacji.  
Uwaga: fine-tuning Gemini 3 Pro nie jest obecnie dostępny — SFT mają tylko 3.5 Flash / 3.1 Flash-Lite, więc rekomendacja musi to uwzględnić.

**Braki:**  
- Jak liczysz te 70% — per rysunek, per pole, per dokument?  
- Czy masz ground-truth, czyli ręcznie zweryfikowane rysunki z etykietami?  
- Czy PDF-y z programów do wycen są wektorowe, czy to skany?  
- Czy dopuszczasz zejście z Gemini 3 Pro na inny model?

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: 400–500 zł za 4–5h przy 90 zł/h to matematycznie spójne (360–450 zł), ale **zaniżone** — bo research i przygotowanie do konsultacji AI/OCR to realnie 3–4h poza spotkaniami, których nikt nie widzi, a klient dostaje wartość w postaci "nie przepalcie pół roku na ślepą uliczkę". Przy 90 zł/h uczciwa wycena całości to **700–900 zł** (8–10h: analiza materiałów + 2–3h spotkań + spisanie rekomendacji + research uzupełniający po materiałach), a widełki 400–500 zł traktowałbym jako *floor* na wypadek, gdyby klient z góry powiedział "budżet max 500".

Gdybym miał wskazać jedną rzecz do korekty: nie zgadywałem na siłę, ale **nie dopytałem o potencjał follow-upu** (czy po konsultacji jest szansa na audyt wdrożenia / wsparcie przy prototypie) — przy zleceniu za 500 zł to istotne, bo sprzedajemy de facto wejście do dłuższej relacji, nie jednorazową konsultację.

Czy zgadłem coś na siłę? Trochę teza o trzech dystrybucjach inputu — klient sam tego nie rozdziela, my to wnosimy, więc to raczej wartość na spotkanie niż powód do pytania w ofercie. Trzymałbym to krótko, jednym zdaniem.

**Rekomendacja: wystaw 700–900 zł za całość, z adnotacją "do negocjacji"** — 400–500 zł jest OK tylko jeśli zależy ci na szybkim zamknięciu i traktujesz to jako lead.

=== DeepSeek-C — RUNDA 1 ===
Wycena: **900–1100 zł netto** za całość (10–12 h × 90 zł/h).  
Czas: **5–7 dni roboczych** od otrzymania materiałów.

W tym: 2–3 spotkania online (2–3 h), analiza próbek i obecnego pipeline’u, pisemna rekomendacja kierunku. Uzasadnienie: same spotkania to 2–3 h, ale żeby dać konkretną rekomendację, trzeba przejrzeć materiały i ustalić, gdzie realnie tracisz dokładność. Trzy typy wejścia — PDF z wyceny, rysunek architekta, szkic — mają różne problemy, więc najpierw trzeba dobrać do nich osobne podejście. To konsultacja, nie wdrożenie.

Brakuje mi:
1. Jak liczysz te 70% — per rysunek, per pole czy per dokument?
2. Czy masz ground-truth, czyli ręcznie zweryfikowane rysunki z poprawnymi etykietami?
3. Czy PDF-y z programów do wycen są wektorowe, czy to skany?

Uwaga: fine-tuning Gemini 3 Pro **nie jest obecnie dostępny** — jeśli to była rozważana droga, trzeba ją skorygować.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: poprzednia wycena była **napompowana**. Klient sam określił zakres na „2–3 godziny całość + rozwiązanie", a ja wyceniłem 10–12 h, dokładając analizę próbek i pipeline'u, których przy konsultacji za 2–3 spotkania nikt nie kupuje. Realnie: 2–3 h spotkań + 3–4 h na przejrzenie materiałów i napisanie rekomendacji = **5–7 h × 90 zł/h = 450–650 zł netto**, ewentualnie 600 zł jako okrągła liczba. Mina o fine-tuningu Gemini 3 Pro zostaje — jest wprost w briefie i warta podania, ale nie uzasadnia wyceny dwa razy wyższej. Nie zgadywałem na siłę poza jednym: „2–3 spotkania (2–3 h)" przepisałem z ogłoszenia jako zakres, a potem policzyłem to jako własną pracę — to był błąd rachunkowy.

=== DeepSeek-D — RUNDA 1 ===
Tak, podejmę się konsultacji.

**Wycena:** 270–360 zł (przy 90 zł/h)  
- 2h spotkań + krótka rekomendacja: **270 zł**  
- 3h spotkań + pisemne podsumowanie/roadmapa: **360 zł**

**Czas:** 5–7 dni roboczych od otrzymania materiałów; 2–3 spotkania online po 60–90 min.

**Uzasadnienie:** Trzy różne typy dokumentów (PDF z wyceny, rysunek architekta, szkic) wymagają diagnozy całego pipeline’u, a nie tylko promptu. Bez ustalenia, jak liczycie 70% i czy macie ground-truth, każda rekomendacja będzie w ciemno. Osobno zweryfikuję realne opcje fine-tuningu — fine-tuning Gemini 3 Pro obecnie nie jest dostępny.

**Braki:** Jak liczysz te 70% (per rysunek / pole / dokument)? Czy masz ground-truth? Czy PDF-y z programów do wycen są wektorowe, czy to skany?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: **zaniosłem cenę za nisko.** Przy 90 zł/h i samym "2-3h spotkań" wychodzi 270-360 zł, ale klient kupuje nie godziny, a **decyzję architektoniczną** — a do tego dochodzi 2-4h mojego researchu i analizy materiałów przed spotkaniami (sam research do tej oferty to już ~2h). Realny nakład to 5-8h, więc uczciwa wycena to **450-720 zł**, a biorąc pod uwagę wartość decyzji (klient uniknie miesięcy na ślepej uliczce), śmiało **600-800 zł za całość** zamiast 270-360 zł.

Po drugie — **mina o fine-tuningu Gemini 3 Pro jest postawiona trochę na siłę.** Research mówi "brak SFT dla 3.x Pro", ale klient pisze "Gemini 3 PRO" — możliwe, że ma na myśli 3.5 Pro albo po prostu myli nazwy. Lepiej sformułować to warunkowo ("jeśli planujecie SFT na 3 Pro…") niż jako fakt — inaczej ryzykuję, że klient mnie złapie na nieaktualności za 3 miesiące.

Po trzecie: **trzecie pytanie (vector/raster PDF) bym wyciął** — jest wartościowe merytorycznie, ale oferta robi się długa, a to pytanie i tak sprowadza się do "przyślij materiały". Zostawiłbym dwa: metryka 70% i ground-truth.

Nie zgadłem też jednego: klient wprost pyta o **doświadczenie w podobnych projektach**, a ja w ofercie nie mam konkretu — to luka, którą trzeba zaadresować albo uczciwie powiedzieć "brak wprost stolarki, ale VLM na dokumentach technicznych / detekcja symboli".

**Korekta: 600 zł za 2-3 spotkania + krótką rekomendację pisemną, 800 zł z roadmapą.**

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 600,
  "kwota_gorna": 800,
  "definitywna": false,
  "od_czego_zaleza": [
    "liczba spotkań: 2 vs 3",
    "zakres pisemnej rekomendacji: krótka notatka vs roadmapa",
    "czas analizy materiałów i researchu przed spotkaniami",
    "liczba typów dokumentów do diagnozy: PDF z wyceny, rysunek architekta, szkic",
    "potrzeba follow-upu po konsultacji"
  ],
  "dni_od": 3,
  "dni_do": 7,
  "uzasadnienie": "Po autokrytyce czterech modeli widać zbieżność w przedziale 600–800 zł: skrajne 270–500 zł oraz 900–1100 zł zostały przez same modele skorygowane jako zaniżone lub napompowane. Zakres to doradztwo, nie wdrożenie: 2–3 h spotkań plus 3–5 h analizy materiałów i spisania rekomendacji, co daje realnie 5–8 h pracy. Rozbieżność wynika głównie z tego, czy wycena obejmuje tylko spotkania, czy także research, analizę próbek i roadmapę. Niepewność podnosi brak informacji, jak liczone jest 70%, czy istnieje ground-truth i czy PDF-y są wektorowe czy rastrowe."
}

=== FINALNA WYCENA ===
600-800 zl netto | 7-7 dni | WIDELKI
Od czego zalezy: liczba spotkań: 2 vs 3, zakres pisemnej rekomendacji: krótka notatka vs roadmapa, czas analizy materiałów i researchu przed spotkaniami, liczba typów dokumentów do diagnozy: PDF z wyceny, rysunek architekta, szkic, potrzeba follow-upu po konsultacji
Uzasadnienie rozjemcy: Po autokrytyce czterech modeli widać zbieżność w przedziale 600–800 zł: skrajne 270–500 zł oraz 900–1100 zł zostały przez same modele skorygowane jako zaniżone lub napompowane. Zakres to doradztwo, nie wdrożenie: 2–3 h spotkań plus 3–5 h analizy materiałów i spisania rekomendacji, co daje realnie 5–8 h pracy. Rozbieżność wynika głównie z tego, czy wycena obejmuje tylko spotkania, czy także research, analizę próbek i roadmapę. Niepewność podnosi brak informacji, jak liczone jest 70%, czy istnieje ground-truth i czy PDF-y są wektorowe czy rastrowe.
