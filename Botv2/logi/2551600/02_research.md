## 1. API Fakturowni — endpointy do faktur zaliczkowych/końcowych i raportów

**Potwierdzone:** Fakturownia udostępnia REST API. GitHub (fakturownia/API) wymienia m.in. „Dodanie faktury podobnej (po ID innej faktury, np. zaliczkowej z zamówienia, końcowej z zaliczkowych itp.)”. Dokumentacja developerska wskazuje pojedynczy endpoint `POST /external/v1/documents`, który obsługuje wszystkie typy dokumentów, w tym `FakturaZaliczka` i `FakturaRozliczeniowa`. Dla `FakturaZaliczka` wymagane jest pole `linkedOrderId` oraz `advancePaymentAmount`. Dla `FakturaRozliczeniowa` wymagane są `linkedAdvanceInvoiceIds` (ID faktur zaliczkowych do rozliczenia).

**Niepotwierdzone:** Nie udało się potwierdzić istnienia dedykowanego endpointu do „raportów sprzedaży” w publicznej dokumentacji API.

**Dostępność API w planach:** Zgodnie z recenzją z 2026 r., API REST jest dostępne w Fakturowni, ale nie sprecyzowano, od którego planu jest włączone. Pakiety zaczynają się od Free (0 PLN, 5 dokumentów/mc), Mini (39 PLN, 50 dokumentów), Standard (79 PLN, 200 dokumentów) i Pro (159 PLN, 1000 dokumentów). Należy zweryfikować u dostawcy, czy API wymaga płatnego planu.

## 2. Polscy dostawcy SMS z REST API — model cenowy

**Twilio (Polska):** Cena za SMS wychodzący do Polski: **0,0431 USD** (ok. 0,17 PLN) za wiadomość. Opłata za nieudane wiadomości: 0,001 USD za każdą. Model pay-as-you-go, bez opłat stałych.

**SerwerSMS.pl:** Platforma udostępnia WebAPI do komunikacji zdalnej z aplikacjami klienta. W materials z 2012 r. podano, że większość funkcji systemu jest dostępna gratis w ramach posiadanego konta, a WebAPI nie generuje dodatkowych opłat za dostęp. **Zastrzeżenie:** źródło jest archiwalne (2012), aktualne warunki wymagają weryfikacji u dostawcy.

**SMSAPI:** Nie znaleziono w wynikach wyszukiwania konkretnych danych o cenniku.

## 3. Koszt OpenAI API dla trybu ciągłej analizy maili i dokumentów

**Aktualny model (GPT-6.1 Sol, wrzesień/październik 2026):**
- **Input:** 2 USD / 1 mln tokenów
- **Output:** 10 USD / 1 mln tokenów
- **Cached input:** 0,10 USD / 1 mln tokenów

**Średni koszt na zadanie:** 5,47 USD przy maksymalnym wysiłku reasoningowym (benchmark dla złożonych zadań). Model jest pozycjonowany m.in. do „document analysis” i „multi-step business workflows”.

**Szybkie oszacowanie dla firmy Magnus (niepotwierdzone):** Przy założeniu, że system przetwarza np. 100 maili/dzień i kilka dokumentów, koszt tokenów wejściowych może wynieść od kilkudziesięciu do kilkuset PLN miesięcznie. Dokładne oszacowanie wymaga danych o wolumenie (dziennej liczbie maili, plików, zapytań do danych).

## 4. Ograniczenia n8n cloud vs self-hosted

**n8n Cloud (2026):**
- **Starter:** 24 €/mc (20 €/mc przy płatności rocznej), 2 500 wykonań/mc, 5 równoległych uruchomień
- **Pro:** 60 €/mc (50 €/mc), 10 000 wykonań/mc, 20 równoległych uruchomień
- **Business:** 800 €/mc (667 €/mc), 40 000 wykonań/mc, 30 równoległych uruchomień

**Self-hosted (Community Edition):** **Bezpłatny**, z nieograniczoną liczbą wykonań i workflow. Koszt to wyłącznie serwer (VPS od kilku EUR/mc; produkcyjny hosting z backupem i monitoringiem — drożej).

**Kluczowa różnica:** Cloud rozliczany jest za **wykonania workflow** (jedno uruchomienie = jedno wykonanie, niezależnie od liczby kroków). Self-hosted nie ma limitu wykonań, ale wymaga własnej infrastruktury i utrzymania (patchowanie, backup, skalowanie).

**Wniosek dla zlecenia:** Przy ciągłej analizie maili, plików i pytań do danych liczba wykonań może szybko przekroczyć 2 500/mc (plan Starter). Self-hosted eliminuje ten limit, ale przenosi na klienta koszt serwera i utrzymania. **Niepotwierdzone:** Czy n8n Cloud oferuje wystarczającą przepustowość dla tego konkretnego przypadku — zależy od wolumenu, którego brief nie precyzuje.