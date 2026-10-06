Poniżej zestawienie zweryfikowanych faktów dotyczących znanych problemów z integracją Shopify – Google Merchant Center (GMC) przez aplikację Google & YouTube, wymagań OAuth/API oraz zidentyfikowanych pułapek. Wszystkie informacje pochodzą z publicznie dostępnych źródeł.

---

### 1. Potwierdzone problemy z rozłączeniem integracji

**Samoistne rozłączenie aplikacji Google & YouTube jest zgłaszane przez wielu użytkowników.** W recenzjach Shopify App Store merchant z 8-letnim stażem napisał: *„This app has disconnected itself from my Shopify store. The links do not work either to be able to decipher yourself what might be wrong.”* Google odpowiedziało, że był to skutek jednogodzinnej awarii UI, ale przyznało, że *„certain links or modules not loading properly”* i że awaria mogła wyglądać jak rozłączenie.

**Problem nie jest jednorazowy.** Wiele źródeł branżowych potwierdza, że rozłączenia GMC zdarzają się „randomly”, nawet gdy konfiguracja wygląda poprawnie. Jako częste przyczyny wskazuje się:
- niedopasowanie domeny (primary domain vs. URL w GMC),
- konflikty uprawnień,
- wiele kont GMC,
- „stale API connections” po wielokrotnych próbach ponownego połączenia.

**GMC może blokować synchronizację niezależnie od aplikacji.** Jeśli konto GMC zostanie zawieszone (np. za „Misrepresentation” lub „Website Needs Improvement”), Google **blokuje lub wstrzymuje** synchronizację produktów z Shopify do GMC. W efekcie lista produktów w GMC zostaje wyczyszczona lub oznaczona jako nieaktywna. Co gorsza, GMC może zablokować przycisk „Poproś o ponowną weryfikację”, dopóki w koncie nie ma co najmniej jednego ważnego, dostępnego produktu – a ten nie pojawi się, dopóki synchronizacja jest zablokowana.

**Aplikacja Google & YouTube ma ograniczone możliwości diagnostyczne.** Merchant z 8-letnim doświadczeniem opisuje, że *„feedback provided by the system is vague and unhelpful, leaving users guessing about what actually needs to be fixed”*. Inny użytkownik nazywa API między Google a Shopify *„buggy and lacking in features”* z *„severely lacking”* wsparciem.


### 2. Wymagania i pułapki OAuth / API

**Tokeny dostępu i odświeżania mają ściśle określony cykl życia.** Dla „expiring offline tokens” (wprowadzonych w grudniu 2025):
- **access token wygasa po 1 godzinie** (3600 sekund),
- **refresh token wygasa po 90 dniach bezczynności** – jeśli nie zostanie użyty w tym oknie, autoryzacja przepada i merchant musi ponownie autoryzować aplikację.

**Rotacja refresh tokenów to najczęstsza przyczyna błędu `invalid_grant`.** Shopify rotuje refresh tokeny: gdy refresh token zostanie wymieniony, poprzednie tokeny (access i refresh) są unieważniane, a zwracane są nowe. Jeśli system nadal używa starego tokena (np. z powodu wyścigu między procesami), kolejne odświeżenia kończą się błędem `invalid_grant`.

**Błąd `invalid_grant` może też wynikać z:**
- odinstalowania aplikacji przez merchanta,
- ręcznego odebrania dostępu w ustawieniach,
- odrzucenia żądania odświeżenia (np. przy odpowiedzi 400/401).

**Wybieranie konta Google podczas OAuth to znana pułapka.** Przeglądarka może automatycznie wybrać prywatne konto Gmail zamiast służbowego, co prowadzi do połączenia z niewłaściwym GMC lub utworzenia nowego konta. Zalecane obejście: użycie osobnego profilu Chrome z odpowiednimi uprawnieniami administratora w docelowym GMC.


### 3. Zmiany w API i ich wpływ na integrację

**Content API for Shopping zostało wyłączone 18 sierpnia 2026 r.** Zostało zastąpione przez **Merchant API** – Google potwierdziło, że migracja dla aplikacji Google & YouTube odbywa się automatycznie i **nie wymaga ręcznych działań** ze strony merchanta.

**Google oficjalnie odradza odinstalowywanie i reinstalowanie aplikacji** w związku z przejściem na Merchant API. Google przyznało, że takie działania **mogą obecnie powodować problemy techniczne** i że pracuje z Shopify nad ich rozwiązaniem.

**Wpływ na identyfikatory produktów.** W związku z migracją na Merchant API niektórzy agenci i reklamodawcy zaobserwowali, że **ID produktów mogą się zmieniać**, jeśli sklep używa aplikacji Google & YouTube jako głównego źródła danych.

**Content API sunset nie dotyczy wszystkich.** Standardowy kanał Google & YouTube w Shopify **nie jest dotknięty** wyłączeniem Content API – dotyczy ono tylko zewnętrznych aplikacji, które programowo pushują dane przez stare API.


### 4. Inne znane problemy z synchronizacją

**Feed może nie aktualizować się dla niektórych krajów.** Zgłoszono przypadek, gdzie Shopify API data source w GMC przestał aktualizować produkty dla części krajów, podczas gdy dla innych działał normalnie (aktualizacja w ciągu ~1 godziny).

**Zdarzają się „phantom products” i błędy backendu.** W grudniu 2025 r. zgłoszono krytyczny błąd synchronizacji, który spowodował pojawienie się 6 000+ „phantom products” w GMC i doprowadził do zawieszenia konta. Problem nie został rozwiązany do marca 2026 r. Zalecanym obejściem było odłączenie natywnego feedu Shopify Content API i przejście na Scheduled Fetch.

**Problemy z atrybutami produktów.** Zgłaszane są błędy typu: brakujące atrybuty `[Color]` i `[Size]`, nieprawidłowe wartości GTIN, niezgodność walut w informacjach o dostawie.


### 5. Czego nie udało się potwierdzić

- **Dokładna przyczyna „samoistnego rozłączenia” w opisanym przypadku** – źródła potwierdzają, że takie zjawisko istnieje, ale nie wskazują jednej uniwersalnej przyczyny. Może to być awaria UI, wygaśnięcie tokena OAuth, konflikt uprawnień lub problem po stronie GMC.
- **Czy support Shopify rzeczywiście „nie ma pomysłu”** – to informacja wyłącznie od zlecającego, niepotwierdzona niezależnie.
- **Skala problemu w 2026 r.** – recenzje i zgłoszenia są rozproszone; brak oficjalnych statystyk Google/Shopify na temat częstotliwości rozłączeń.