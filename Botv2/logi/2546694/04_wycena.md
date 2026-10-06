=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena wstępna (do doprecyzowania):**

**Kwota:** 8 000 – 14 000 zł (umowa o dzieło, 90 zł/h → ok. 90–155 h)
**Czas:** 3–5 tygodni od startu

**Uzasadnienie:**
Poza samym scraperem dochodzi rekurencyjny unpacker (APK → ZIP → XAPK/APKM/split APK), parser tablicy `name` w TTF/OTF oraz panel web z kolejką zadań i eksportem XLSX — to trzy niezależne moduły plus warstwa web. Widełki są szerokie, bo nie znam serwera: APKPure/APKMirror są wykonalne (publiczne, choć niestabilne — Cloudflare, rate limit), Google Play wymaga konta Google i prywatnych endpointów, co zmienia architekturę i ryzyko. Skala (ile deweloperów × ile aplikacji) bezpośrednio przekłada się na storage, retry i czas realizacji.

**Czego brakuje w zleceniu:**
1. **Który serwer?** (Google Play / APKPure / APKMirror / własny klienta) — od tego zależy kanał dostępu i format paczek.
2. **Skala** — ilu deweloperów i rząd wielkości aplikacji (dziesiątki / setki / tysiące)?
3. **Jednorazowo czy cyklicznie?** — cykl = harmonogram + diff + powiadomienia, inna architektura i cena.
4. **Definicja „metadanych" fontu** — proponuję domyślnie: nazwa, rodzina, wersja, copyright, ścieżka w APK. Jeśli pasuje, nie trzeba odpowiadać.

Po odpowiedzi na pkt 1–3 podam kwotę sztywną zamiast widełek.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 8–14 tys. zł są uczciwe **tylko dla APKPure/APKMirror przy dziesiątkach–setkach aplikacji** — 90–155 h to realny zakres na rekurencyjny unpack + parser TTF + panel web z kolejką i eksportem, nic tu nie naciągnąłem. Zgadłem jedną rzecz: **kolejkę zadań i retry** — brief mówi tylko „webowo", ale bez tego przy setkach APK narzędzie się wysypie, więc traktuję to jako założenie do potwierdzenia, nie jako fakt z briefu. **Górna granica może być za niska**, jeśli serwer = Google Play i skala to tysiące aplikacji: wtedy dochodzi OAuth/AAS, scalanie split APK per konfiguracja i ryzyko zmian prywatnych endpointów — realnie **+6–12 tys. zł i +3–5 tygodni**, więc widełki przesunąłbym do **10–22 tys. zł** i poczekał z kwotą sztywną na odpowiedź o serwer i skalę. Nie dopisałem na siłę niczego o ToS ani RODO — research tego nie potwierdza cytatem, więc tego nie używam jako argumentu.

=== DeepSeek-B — RUNDA 1 ===
**Widełki:** 4000–6000 zł netto (45–65 h × 90 zł). Google Play: 6000–9000 zł. Cyklicznie (nowe wersje w czasie): +30–40%.

**Czas:** 7–12 dni roboczych dla wersji jednorazowej.

**Uzasadnienie:** APK to ZIP, ale XAPK/APKM/split APK to ZIP w ZIP-ie — bez rekurencyjnego rozpakowania część fontów wypada, a parser fontów (name table TTF/OTF) plus panel web z uploadem listy i eksportem XLSX to osobne moduły. Jeśli serwer to Google Play, dochodzi brak publicznego API, wymóg konta Google i ryzyko, że endpointy zmienią się bez ostrzeżenia — stąd wyższa wycena i zastrzeżenie o szarej strefie. APKPure/APKMirror są wykonalne taniej, ale podatne na Cloudflare i rate limit.

**Czego brakuje w zleceniu:**
1. **Który serwer?** (Google Play / APKPure / APKMirror / własny klienta / inny) — od tego zależą kanał dostępu, format paczek i ryzyko.
2. **Skala** — ilu deweloperów i rząd wielkości aplikacji (dziesiątki / setki / tysiące)? Od tego zależy storage, kolejka, retry i czas.
3. **Jednorazowo czy cyklicznie?** Jednorazowo = skrypt + raport; cyklicznie = harmonogram + diff + powiadomienia — inna architektura i cena.

**Propozycja domyślna (jeśli pasuje — nie trzeba odpowiadać):** metadane fontu = nazwa + rodzina + wersja + copyright + ścieżka w APK; panel web z uploadem listy deweloperów i eksportem XLSX.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: wycena 4000–6000 zł jest obroniona **tylko przy Google Play** i zakresie z panelem web — tam 45–65 h to realna praca (rekurencyjny unpack, parser name table, kolejka, XLSX, upload). Przy APKPure/APKMirror i zleceniu jednorazowym to zawyżenie — tam realnie 25–40 h, czyli **2200–3600 zł**, bo całość to skrypt + panel, bez walki z prywatnymi endpointami i tokenami. Zgadywałem w dwóch miejscach: „obfuskowane/subsetowane fonty" i „fonty w native libs" — wyciąłem to już w poprzedniej iteracji i słusznie, bo brief tego nie potwierdza. Google Play nie jest „automatyczną odmową", ale jest miną — i tak ją opisuję, dopóki nie znam serwera. Korekta: widełki zostają warunkowe — **2200–3600 zł (APKPure/APKMirror, jednorazowo)** vs **4000–6000 zł (Google Play lub zakres z panelem i kolejką)**; cyklicznie +30–40% w obu przypadkach.

=== DeepSeek-C — RUNDA 1 ===
## Wstępna wycena (widełki, zależne od odpowiedzi)

**Kwota:** 3 600 – 7 200 zł netto (40–80 h × 90 zł/h)
**Czas:** 7–12 dni roboczych

**Rozbicie:**
- Rdzeń (scraper + rekurencyjny unpacker APK/XAPK/APKM + parser fontów TTF/OTF + panel web z eksportem XLSX): ~40–50 h
- Jeśli serwer = Google Play (auth OAuth/AAS, split APK, niestabilne endpointy): +20–30 h
- Jeśli tryb cykliczny (harmonogram + diff + powiadomienia): +15–20 h

**Uzasadnienie:** APK to ZIP, a XAPK/APKM/split APK to ZIP-y w ZIP-ie — bez rekurencyjnego rozpakowania część fontów z `res/font` i `assets` po prostu wypadnie, więc to nie jest „prosty scraper", a pipeline pobieranie → unpack → parsowanie name table → raport. Do tego dochodzi panel web (upload listy deweloperów, kolejka zadań, eksport XLSX). Widełki są szerokie, bo bez nazwy serwera i skali nie wiem, czy walczę z Cloudflare i rate limitem, czy z brakiem publicznego API.

## Czego brakuje w zleceniu

1. **Który serwer?** (Google Play / APKPure / APKMirror / własny klienta / inny) — od tego zależy kanał dostępu, format paczek i ryzyko. Trzy główne serwery mają różne mechanizmy.
2. **Skala** — ile kont deweloperów i rząd wielkości (dziesiątki / setki / tysiące aplikacji)? Od tego zależy storage, kolejka i czas realizacji.
3. **Jednorazowo czy cyklicznie?** Jednorazowo = skrypt + raport; cyklicznie = harmonogram + diff + powiadomienia.

**Propozycja domyślna (jeśli pasuje — nie trzeba odpowiadać):** metadane fontu = nazwa + rodzina + wersja + copyright + ścieżka w APK; panel web z uploadem listy deweloperów i eksportem XLSX.

Po odpowiedzi na pytanie 1–3 podam kwotę sztywną, nie widełki.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: dolna granica 3 600 zł była zaniżona — sam rdzeń (scraper + rekurencyjny unpack + parser fontów + panel web z kolejką i eksportem) to realistycznie 50–60 h, czyli **4 500–5 400 zł**, a nie 40 h. Widełki powinny być **4 500–10 800 zł netto** (50–120 h), bo górna granica rośnie mocno, jeśli wchodzi Google Play (konto, split APK, kruche endpointy) albo tryb cykliczny z diffem. Zgadywałem dwie rzeczy: „ból = audyt licencyjny fontów" (słusznie oznaczyłem jako niepewnik, nie wpisałem do oferty) oraz domyślny zestaw metadanych fontu — to nadal propozycja, nie fakt. Nie zgadywałem serwera ani skali, i dobrze, bo bez nich każda sztywna kwota byłaby strzałem. Kwota sztywna dopiero po Q1–Q3, ale widełki podnoszę już teraz.

=== DeepSeek-D — RUNDA 1 ===
**Wycena (przy założeniach: APKPure/APKMirror, dziesiątki deweloperów, jednorazowo):**
- **Kwota:** 4500–7000 zł netto (umowa o dzieło, 90 zł/h → ok. 50–75 h)
- **Czas:** 7–12 dni roboczych
- **Widełki zależą głównie od serwera:** Google Play podnosi ryzyko i pracochłonność (split APK, konto Google, prywatne endpointy) → górna granica lub więcej.

**Uzasadnienie (3 zdania):**
APK to ZIP, ale XAPK/APKM i split APK to archiwa w archiwach — bez rekurencyjnego rozpakowania część fontów wypadnie, więc sam unpacker to kilka godzin. Do tego parser fontów (odczyt tabel `name` z TTF/OTF), panel web z kolejką i uploadem listy deweloperów oraz eksport XLSX. Przy APKPure/APKMirror trzeba doliczyć obsługę rate-limitu i retry (Cloudflare).

**Czego brakuje w zleceniu — 3 pytania:**
1. **Który serwer?** (Google Play / APKPure / APKMirror / własny klienta) — od tego zależy kanał dostępu, format paczek i ryzyko.
2. **Skala** — ilu deweloperów i rząd wielkości (dziesiątki / setki / tysiące aplikacji)? Od tego zależy storage i czas.
3. **Jednorazowo czy cyklicznie?** Cyklicznie = harmonogram, diff wersji, powiadomienia — inna architektura i cena.

**Domyślnie proponuję** (jeśli pasuje — nie trzeba odpowiadać): kolumny XLSX = nazwa app, nazwa fontu, rodzina, wersja, copyright, ścieżka w APK; panel web z uploadem listy deweloperów i eksportem XLSX.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: kwota 4500–7000 zł netto (50–75 h) jest uczciwa dla **jednorazowego MVP na APKPure/APKMirror przy dziesiątkach deweloperów** — tam praca to głównie scraper + rekurencyjny unpack + parser `name` + panel z uploadem i eksportem XLSX, i realnie te 50–75 h się broni. Nie zgadywałem na siłę w tej iteracji — wyciąłem obfuskację/subsetowanie fontów i zarzut ToS, bo research ich nie potwierdza, a wcześniej były wstawione bez dowodu. Ale mam jedno realne zastrzeżenie: **panel web z kolejką zadań bywa niedoszacowany** — jeśli klient oczekuje czegoś więcej niż upload listy + download XLSX (np. statusy per deweloper, retry z UI, historia runów, auth), to samo UI zjada 15–25 h, nie 5. Jeśli po Q1 okaże się, że serwer to Google Play, albo tryb jest cykliczny, albo skala idzie w setki deweloperów — **górna granica 7000 zł jest za niska i powinienem ją podnieść do 9000–12000 zł netto**, bo dochodzi kanał zależny od konta Google (tokeny, prywatne endpointy, split APK do scalania) plus harmonogram i diff wersji. Na razie nie zmieniam kwoty, bo bez odpowiedzi na Q1–Q3 każda korekta byłaby strzelaniem.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 4500,
  "kwota_gorna": 12000,
  "definitywna": false,
  "od_czego_zaleza": [
    "serwer źródłowy: APKPure/APKMirror vs Google Play vs własny klienta",
    "skala: liczba deweloperów i aplikacji (dziesiątki/setki/tysiące)",
    "tryb: jednorazowy vs cykliczny (harmonogram, diff wersji, powiadomienia)",
    "zakres panelu web: upload listy + eksport XLSX vs kolejka, retry, historia, auth",
    "format paczek: APK/XAPK/APKM/split APK i konieczność rekurencyjnego rozpakowania"
  ],
  "dni_od": 10,
  "dni_do": 30,
  "uzasadnienie": "Finalne widełki 4 500–12 000 zł netto wynikają ze zbieżności autokrytyk C i D co do dolnej granicy dla jednorazowego MVP na APKPure/APKMirror przy dziesiątkach deweloperów oraz z konieczności podniesienia górnej granicy, gdy wchodzi Google Play, setki aplikacji lub tryb cykliczny. Modele zgodnie wskazują brak nazwy serwera, skali i trybu jako główne źródło niepewności, a także potrzebę rekurencyjnego unpackera, parsera fontów i panelu web. Największa rozbieżność jest między B (2 200–3 600 zł dla najprostszego wariantu) a A (10 000–22 000 zł przy Google Play i tysiącach aplikacji); C i D zajmują środkowe, bardziej uzasadnione pozycje. Nie wybieram kwoty definitywnej, bo bez odpowiedzi na pytania o serwer, skalę i cykliczność każda sztywna cena byłaby strzałem. Czas 10–30 dni roboczych obejmuje prostszy wariant oraz wariant z Google Play i rozbudowanym panelem."
}

=== FINALNA WYCENA ===
4500-12000 zl netto | 10-30 dni | WIDELKI
Od czego zalezy: serwer źródłowy: APKPure/APKMirror vs Google Play vs własny klienta, skala: liczba deweloperów i aplikacji (dziesiątki/setki/tysiące), tryb: jednorazowy vs cykliczny (harmonogram, diff wersji, powiadomienia), zakres panelu web: upload listy + eksport XLSX vs kolejka, retry, historia, auth, format paczek: APK/XAPK/APKM/split APK i konieczność rekurencyjnego rozpakowania
Uzasadnienie rozjemcy: Finalne widełki 4 500–12 000 zł netto wynikają ze zbieżności autokrytyk C i D co do dolnej granicy dla jednorazowego MVP na APKPure/APKMirror przy dziesiątkach deweloperów oraz z konieczności podniesienia górnej granicy, gdy wchodzi Google Play, setki aplikacji lub tryb cykliczny. Modele zgodnie wskazują brak nazwy serwera, skali i trybu jako główne źródło niepewności, a także potrzebę rekurencyjnego unpackera, parsera fontów i panelu web. Największa rozbieżność jest między B (2 200–3 600 zł dla najprostszego wariantu) a A (10 000–22 000 zł przy Google Play i tysiącach aplikacji); C i D zajmują środkowe, bardziej uzasadnione pozycje. Nie wybieram kwoty definitywnej, bo bez odpowiedzi na pytania o serwer, skalę i cykliczność każda sztywna cena byłaby strzałem. Czas 10–30 dni roboczych obejmuje prostszy wariant oraz wariant z Google Play i rozbudowanym panelem.
