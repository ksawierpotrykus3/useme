Punkt 1. Stos i obsługa offline.

Proponuję SvelteKit po obu stronach, kierowca jako PWA i dashboard dyspozytora w tym samym frameworku. Jeden typ, jeden build, mniej pracy przy spójności formularzy i raportów. Backend Supabase zgodnie z wymogiem, RLS per org_id, JWT custom claims z org_id i rolą.

Przepływ offline w czterech krokach. Zdjęcie leci przez OffscreenCanvas z iteracyjnym toBlob po jakości aż do zejścia poniżej 500 KB przy maxWidth 1600 px, co trzyma czytelność kwitu. Blob zapisuję bezpośrednio w IndexedDB razem z rekordem formularza w jednej transakcji. Kolejka z deduplikacją po uuid rekordu, odporna na wielokrotne wywołania sync. Po powrocie zasięgu dane lecą same, bez klikania kierowcy.

Tu jedna rzecz, która dotyka wprost wymogu całkowicie w tle. Background Sync API działa wyłącznie w Chromium, Safari na iOS tego API nie ma. Jeśli we flocie są iPhone'y, dosłowne zero klikania przy zamkniętej aplikacji nie jest wykonalne. Rozwiązanie to dwie ścieżki. Android dostaje Background Sync i Periodic Background Sync po instalacji PWA. iOS dostaje auto-sync przy starcie PWA plus Web Push jako wybudzacz. Safari czyści IndexedDB po siedmiu dniach bez interakcji, jeśli PWA nie jest zainstalowana na ekranie głównym. Czyli dokładnie ten scenariusz, w którym giną kwity. Dlatego instalacja PWA na ekranie głównym jest twardym warunkiem onboardingu kierowcy, nie opcją do rozważenia.

Punkt 2. Portfolio.

Nie mam publicznego portfolio w tej niszy, więc nie wkleję tu cudzych linków. Nie chcę zmyślać realizacji. Mogę natomiast pokazać podejście na fragmencie Waszego zakresu, na przykład na logice kolejki z deduplikacją i schemacie RLS, jeszcze przed startem prac. Jeśli to za mało, uczciwie mówię, że nie spełniam tego warunku w tej chwili.

Punkt 3. Start.

Mogę wystartować w ciągu dwóch tygodni od ustalenia zakresu i dostępu do środowisk HotPay i Fakturownia.

HotPay obsługuje płatności cykliczne, więc webhook subskrypcji wystarczy do przedłużania konta. Jeśli w Waszym modelu jest inaczej, dostosuję moduł w trakcie discovery.

Cena. Za pełny zakres z briefu, z Fakturownią i PDF z miniaturami od startu, 20 000 do 28 000 zł netto. Termin zamyka się w ośmiu do dwunastu tygodni.

Ksawier