Punkt 1. Stos i obsługa offline.

Proponuję SvelteKit po obu stronach, kierowca jako PWA i dashboard dyspozytora w tym samym frameworku. Jeden typ, jeden build, mniej pracy przy spójności formularzy i raportów. Backend Supabase zgodnie z wymogiem, RLS per org_id, JWT custom claims z org_id i rolą.

Przepływ offline w czterech krokach. Zdjęcie leci przez OffscreenCanvas z iteracyjnym toBlob po jakości aż do zejścia poniżej 500 KB przy maxWidth 1600 px, co trzyma czytelność kwitu. Blob zapisuję bezpośrednio w IndexedDB razem z rekordem formularza w jednej transakcji. Kolejka z deduplikacją po uuid rekordu, odporna na wielokrotne wywołania sync. Po powrocie zasięgu dane lecą same, bez klikania kierowcy.

Tu jedna rzecz, która dotyka wprost wymogu całkowicie w tle. Background Sync API działa wyłącznie w Chromium, Safari na iOS tego API nie ma. Jeśli we flocie są iPhone'y, dosłowne zero klikania przy zamkniętej aplikacji nie jest wykonalne. Rozwiązanie to dwie ścieżki. Android dostaje Background Sync i Periodic Background Sync po instalacji PWA. iOS dostaje auto-sync przy starcie PWA plus Web Push jako wybudzacz. Drugie, Safari czyści IndexedDB po siedmiu dniach bez interakcji, jeśli PWA nie jest zainstalowana na ekranie głównym. Czyli dokładnie ten scenariusz, w którym giną kwity. Dlatego instalacja PWA na ekranie głównym jest twardym warunkiem onboardingu kierowcy, nie opcją do rozważenia.

Punkt 2. Portfolio.

Nie mamy gotowego portfolio w tej niszy, więc nie będę wpisywał tu cudzych linków. Podejście mogę pokazać na fragmencie Waszego zakresu, na przykład na logice kolejki z deduplikacją i schemacie RLS, jeszcze przed startem prac.

Punkt 3. Start.

Mogę wystartować w ciągu dwóch tygodni od ustalenia zakresu i dostępu do środowisk HotPay i Fakturownia.

Jedno pytanie, zanim wycenię. Czy Wasz HotPay obsługuje płatności cykliczne, czy tylko jednorazowe? Od tego zależy, czy webhook subskrypcji wystarcza do przedłużania konta, czy buduję harmonogram i przypomnienia po Waszej stronie. To zmienia architekturę modułu sprzedaży.

Cena. Przy zakresie ograniczonym do MVP, czyli Fakturownia w drugiej fazie i raport PDF bez miniatur w pierwszej wersji, 20 000 zł netto. Przy pełnym zakresie z briefu, z Fakturownią i PDF-em z miniaturami od startu, 24 000 do 28 000 zł netto. Termin w obu przypadkach zamyka się w ośmiu do dwunastu tygodni.

Ksawier