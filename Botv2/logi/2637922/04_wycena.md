=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena wstępna (warunkowa): 1200–1800 zł, czas: 4–6 dni roboczych.**

Uzasadnienie: skrypt klikający za Ciebie jest **zabroniony** przez regulamin pokewars.pl (§7.6 – boty i skrypty), więc mogę zrobić wyłącznie wariant zgodny z regulaminem: skrypt, który **informuje Cię przez NVDA**, gdzie jest przycisk „walcz z bossem” i jaki jest stan walki – a Ty klikasz sam. To wymaga diagnozy DOM po zalogowaniu (nie wiemy, czy przycisk jest w ogóle selektywny, czy np. w canvasie) i integracji z czytnikiem ekranu. Kwota obejmuje diagnozę, kod i testy z NVDA.

**Czego brakuje:**
1. Konta testowego (lub zgody na założenie własnego) – bez tego nie sprawdzę DOM.
2. Informacji, czy walka jest automatyczna, czy wymaga decyzji.
3. Potwierdzenia, że akceptujesz wariant „informuję, nie klikam” – inaczej nie składam oferty.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 1200–1800 zł jest uczciwa dla wariantu „informuję, nie klikam”, bo nadal obejmuje diagnozę DOM po zalogowaniu, integrację z NVDA i testy — a bez dostępu do konta nie mogę jej zawęzić. Nie zgadłem canvasu ani „braku latarki” — oba wycofałem do weryfikacji, więc żadnej miny na siłę nie dopisałem; jedyna twarda mina to §7.6 z cytatem. Czego nie wiem: czy przycisk w ogóle da się selektywnie złapać i czy walka wymaga decyzji — to może rozszerzyć zakres (obsługa całej walki) i podnieść kwotę w górę widełek, albo wręcz skrócić do samego komunikatu. Korekta: trzymam 1200–1800 jako warunkowe, ale jeśli okaże się, że mapa jest w canvasie i trzeba iść ścieżką zgłoszenia dostępności do twórców, kwota spada do ok. 300–500 zł za diagnozę i rekomendację.

=== DeepSeek-B — RUNDA 1 ===
**Wycena wstępna: 900–1500 zł** (10–17 h × 90 zł), **3–5 dni roboczych** — pod warunkiem że zgadzasz się na wariant zgodny z regulaminem gry.

**Uzasadnienie:** Regulamin pokewars.pl §7 pkt 7.6 wprost zabrania skryptów automatycznie wykonujących akcje w grze („automatyczne wędrowanie do lokacji”, boty, bindy) — skrypt, który sam klika „walcz z bossem”, to ban konta, więc tego nie napiszę. Proponuję to samo w bezpiecznej wersji: skrypt czyta strukturę strony i **mówi Ci przez NVDA** (komunikat na żywo), gdzie jesteś, czy boss jest dostępny i czego brakuje (np. latarki) — klikasz sam, jednym klawiszem. To rozwiązuje Twój ból (nie widzisz przycisku) i nie łamie regulaminu. Zakres: diagnoza DOM mapy/lokacji, obsługa komunikatów NVDA, testy z Tobą. Jeśli okaże się, że mapa jest w `<canvas>`, wariant informacyjny może być niewykonalny — wtedy zostaje ścieżka zgłoszenia problemu dostępności do twórców gry.

**Czego brakuje, żeby wycena była wiążąca:**
1. **Konto testowe** (Twoje lub założone przez nas) — bez wejścia po zalogowaniu nie wiem, czy przycisk da się w ogóle wybrać selektywnie. To warunek konieczny.
2. **Czy akceptujesz wariant „skrypt informuje, Ty klikasz”** — bez tego nie składam oferty wykonawczej (automatyczne klikanie = sprzeczne z §7.6).
3. **Czy po „walcz z bossem” walka toczy się sama, czy wymaga decyzji** (atak, przedmiot) — od tego zależy, czy zakres kończy się na jednym komunikacie, czy na obsłudze całej walki, a to zmienia wycenę w górę.

Przeglądarkę zakładam Chrome + Tampermonkey na Windows (najprostsze dla NVDA) — jeśli masz inną, dostroję.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: 900–1500 zł było **zawyżone na zapas** — sam w myśleniu przyznałem, że przy czystym DOM to 4–8 h (360–720 zł), a 17 h wpisałem pod niepewność, nie pod realną pracę. Zgadywałem w dwóch miejscach: (1) że walka może wymagać decyzji — nie mam dowodu, to tylko możliwość; (2) w researchu wrócił canvas, mimo że w myśleniu go wycofałem — to niespójność, nie fakt. Nie zgadywałem w jednym: §7.6 regulaminu jest potwierdzony z linkiem i to realnie zmienia kształt zlecenia — za to się nie wycofuję.

Korekta wyceny: **po diagnozie DOM 360–720 zł (4–8 h), ale ofertę składam dopiero po wglądzie w konto** — bo jeśli mapa jest w canvas, projekt jest niewykonalny w wariancie dostępnościowym i żadna kwota nie ma sensu. Widełki 900–1500 zł wycofuję jako nieuczciwe zawyżenie pod niepewność.

=== DeepSeek-C — RUNDA 1 ===
## Wycena wstępna

**Wariant zgodny z regulaminem (skrypt informuje, Ty klikasz): 900–1500 zł**
Czas: **2–3 dni roboczych** od momentu dostępu do konta testowego.
Stawka: 90 zł/h × ok. 10–16 h (diagnoza DOM, userscript, komunikaty NVDA, testy, poprawki).

**Wariant, o który prosisz wprost (skrypt sam klika „walcz z bossem”) — nie podejmuję się.**
Regulamin pokewars.pl §7 pkt 7.6: *„Zabronione jest korzystanie z botów, skryptów, bindów… (np. poprzez automatyczne wędrowanie do lokacji)”*. Ryzyko: blokada Twojego konta. Nie chcę Ci tego zafundować.

**Co proponuję zamiast tego:** ten sam efekt — skrypt czyta stronę i mówi Ci przez NVDA, gdzie jest boss, czy możesz walczyć, czego brakuje (np. latarki). Naciśnięcie przycisku zostaje po Twojej stronie — jedno kliknięcie / skrót klawiszowy.

---

**Czego brakuje do wiążącej wyceny:**

1. **Konto testowe** — bez wejścia po zalogowaniu nie wiem, czy przycisk da się wybrać selektywnie, czy mapa nie jest w `<canvas>` (wtedy wariant informacyjny może być niewykonalny i zostaje tylko zgłoszenie do twórców gry).
2. **Czy walka jest automatyczna, czy wymaga decyzji** (atak, przedmiot)? Od tego zależy zakres — jeden komunikat vs. obsługa całej walki.
3. **Czy akceptujesz wariant „informuję, nie klikam”?** Jeśli nie — nie składam oferty, bo nie złamię regulaminu za Twoje pieniądze i Twoje konto.

Zakładam Chrome + Tampermonkey na Windows (najprostsze dla NVDA). Jeśli masz inną przeglądarkę — dostroję.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: 900–1500 zł to widełki **obronne, nie wyliczone** — wyceniłem robotę, której jeszcze nie widziałem, więc górna granica jest asekuracją przed canvasem i obsługą całej walki, a nie realnym szacunkiem. Jeśli po zalogowaniu okaże się, że przycisk to zwykły `<button>` z selektorem, realny czas spada do **6–8 h, czyli ~540–720 zł** — i wtedy dolna granica 900 zł jest zawyżona. Zaniżone mam natomiast dwie rzeczy: czas na założenie/weryfikację konta testowego oraz ścieżkę awaryjną (zgłoszenie problemu dostępności do twórców), której w ogóle nie wyceniłem, a która może być jedynym wyjściem. Wniosek: **nie zmieniam kwoty na sztywno, ale zawężam widełki do 700–1300 zł i zastrzegam, że wiążąca jest dopiero po diagnozie DOM** — wcześniej każda liczba to zgadywanie.

=== DeepSeek-D — RUNDA 1 ===
**Wycena wstępna: 650–1150 zł** (7–13 h × 90 zł), czas: **3–5 dni roboczych** po uzyskaniu dostępu do konta testowego.

**Uzasadnienie:** Muszę najpierw zobaczyć DOM po zalogowaniu, bo nie wiem, czy przycisk „walcz z bossem” jest w ogóle klikalny selektywnie, czy mapa nie jest renderowana w `<canvas>`. Regulamin pokewars.pl §7.6 **zakazuje skryptów automatyzujących grę** — więc proponuję wariant zgodny: skrypt **informuje** (gdzie jest boss, jaki jest stan walki, czego brakuje), a Ty klikasz sam. To rozwiązuje Twój ból i nie grozi banem konta.

**Czego brakuje:**
1. Konto testowe — bez tego nie ustalę, czy wariant informacyjny jest wykonalny.
2. Czy po kliknięciu „walcz z bossem” walka toczy się automatycznie, czy wymaga decyzji (atak/przedmiot) — to zmienia zakres.
3. Czy akceptujesz wariant „skrypt informuje, Ty klikasz”? Bez tego nie składam oferty wykonawczej — realizacja wprost (auto-klik) łamie §7.6 i może skończyć się blokadą Twojego konta.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 650–1150 zł była oparta na domysłach, nie na diagnozie — zgadłem, że zakres to 7–13 h, a tak naprawdę nie wiem nawet, czy przycisk jest w DOM, czy w `<canvas>`. Jeśli okaże się, że to zwykły `<div>` z klasą i wystarczy nasłuch + live region dla NVDA, realny czas to 4–6 h, czyli ~360–540 zł i moja poprzednia wycena byłaby zawyżona. Jeśli natomiast mapa jest w canvasie albo walka wymaga obsługi kolejnych kroków, 1150 zł może być za mało. Poprawna odpowiedź brzmi: **nie da się uczciwie wycenić przed wglądem w DOM po zalogowaniu** — dlatego podtrzymuję widełki tylko warunkowo, z zastrzeżeniem, że po diagnozie je skoryguję w dół albo w górę, i tak to powinienem był napisać od początku, zamiast opierać się na spekulacji o canvasie.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 400,
  "kwota_gorna": 1300,
  "definitywna": false,
  "od_czego_zaleza": [
    "uzyskania dostępu do konta testowego i diagnozy DOM po zalogowaniu",
    "czy przycisk 'walcz z bossem' jest selektywny (button/div/ARIA), czy interfejs jest w canvas",
    "akceptacji wariantu zgodnego z regulaminem: skrypt informuje przez NVDA, klient sam klika",
    "czy walka po kliknięciu jest automatyczna, czy wymaga dalszych decyzji (atak, przedmiot)",
    "przeglądarki i systemu klienta oraz sposobu integracji z NVDA",
    "zakresu testów i ewentualnej ścieżki awaryjnej: zgłoszenie problemu dostępności do twórców gry"
  ],
  "dni_od": 3,
  "dni_do": 6,
  "uzasadnienie": "Finalna wycena jest widełkowa i warunkowa, bo wszyscy modele zgodnie wskazują, że automatyczne klikanie 'walcz z bossem' narusza §7.6 regulaminu pokewars.pl i nie może być przedmiotem oferty wykonawczej. Wyceniamy więc tylko wariant zgodny: skrypt informuje przez NVDA, a kliknięcie pozostaje po stronie klienta. Rozbieżność dotyczyła kwot: wstępne propozycje sięgały 650–1800 zł, ale po autokrytyce część modeli zeszła do 360–720 zł przy prostym DOM lub 700–1300 zł przy większej niepewności, dlatego odrzucam górne 1800 zł jako zawyżenie pod niepewność. Bez wglądu w DOM nie wiadomo, czy przycisk da się selektywnie wybrać, czy mapa nie jest w canvas oraz czy walka wymaga obsługi całej sekwencji, co może zmienić zakres i kwotę. Dlatego definitywna=false, a widełki 400–1300 zł należy potwierdzić po diagnozie konta testowego."
}

=== FINALNA WYCENA ===
500-1300 zl netto | 7-7 dni | WIDELKI
Od czego zalezy: uzyskania dostępu do konta testowego i diagnozy DOM po zalogowaniu, czy przycisk 'walcz z bossem' jest selektywny (button/div/ARIA), czy interfejs jest w canvas, akceptacji wariantu zgodnego z regulaminem: skrypt informuje przez NVDA, klient sam klika, czy walka po kliknięciu jest automatyczna, czy wymaga dalszych decyzji (atak, przedmiot), przeglądarki i systemu klienta oraz sposobu integracji z NVDA, zakresu testów i ewentualnej ścieżki awaryjnej: zgłoszenie problemu dostępności do twórców gry
Uzasadnienie rozjemcy: Finalna wycena jest widełkowa i warunkowa, bo wszyscy modele zgodnie wskazują, że automatyczne klikanie 'walcz z bossem' narusza §7.6 regulaminu pokewars.pl i nie może być przedmiotem oferty wykonawczej. Wyceniamy więc tylko wariant zgodny: skrypt informuje przez NVDA, a kliknięcie pozostaje po stronie klienta. Rozbieżność dotyczyła kwot: wstępne propozycje sięgały 650–1800 zł, ale po autokrytyce część modeli zeszła do 360–720 zł przy prostym DOM lub 700–1300 zł przy większej niepewności, dlatego odrzucam górne 1800 zł jako zawyżenie pod niepewność. Bez wglądu w DOM nie wiadomo, czy przycisk da się selektywnie wybrać, czy mapa nie jest w canvas oraz czy walka wymaga obsługi całej sekwencji, co może zmienić zakres i kwotę. Dlatego definitywna=false, a widełki 400–1300 zł należy potwierdzić po diagnozie konta testowego.
