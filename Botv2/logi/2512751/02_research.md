## Research: LSA w Polsce, Consent Mode v2 i zasady Google Ads dla usług lokalnych

**1. Local Services Ads (LSA) w Polsce — NIEDOSTĘPNE**

LSA to format reklam Google, w którym płaci się wyłącznie za kontakt (telefon/wiadomość), a nie za kliknięcie. Dla firmy ogrodniczej byłby to potencjalnie tańszy i skuteczniejszy kanał niż klasyczny Google Ads.

**Kluczowy fakt:** Polska **nie znajduje się** na liście krajów, w których LSA są dostępne. Google uruchomił LSA w Europie (Niemcy, Wielka Brytania, Francja, Austria, Belgia, Irlandia, Włochy, Holandia, Szwajcaria, Hiszpania), ale Polska nie wchodzi w skład tych państw.

W materiałach Google (wersja polska) pojawiają się kategorie usług takie jak „Architektura krajobrazu", „Pielęgnacja trawników" i „Pielęgnacja drzew" — co sugeruje, że gdy LSA zostaną rozszerzone na Polskę, kategoria usług ogrodniczych będzie obsługiwana. Obecnie jednak jest to niepotwierdzone co do terminu.

**Wniosek:** W chwili obecnej nie ma możliwości uruchomienia LSA dla firmy z Polski. Jedyną opcją pozostaje klasyczny Google Ads (Search + ewentualnie Performance Max z lokalnym targetowaniem).

**2. Consent Mode v2 — obowiązkowy dla kampanii w EEA (w tym PL)**

Od **marca 2024** wdrożenie Google Consent Mode v2 jest **wymagane** dla wszystkich reklamodawców kierujących kampanie do użytkowników w Europejskim Obszarze Gospodarczym (EEA) i Wielkiej Brytanii.

- Wymóg wynika z Digital Markets Act (DMA) oraz unijnej polityki zgody użytkownika Google (EU User Consent Policy).
- Bez Consent Mode v2 tagi Google nie zbierają danych od użytkowników EEA, co oznacza: **brak remarketingu, brak modelowania konwersji, kurczące się odbiorcy reklamowe**.
- Od **15 czerwca 2026** zaszła istotna zmiana: zbieranie danych z tagu GA4 jest teraz kontrolowane przez ustawienia Consent Mode w Google Ads, a Google Signals zostało zawężone wyłącznie do raportowania zalogowanych użytkowników.
- **Kluczowy parametr:** `ad_storage` stał się jedynym parametrem zarządzającym danymi reklamowymi w połączonym koncie GA4.

**Wniosek dla zlecenia:** Kampania Google Ads targetująca Polskę **musi** mieć wdrożony Consent Mode v2 (wraz z bannerem cookies i polityką prywatności). Bez tego śledzenie konwersji (formularz/telefon) będzie poważnie ograniczone.

**3. Zasady Google Ads dla usług lokalnych w Polsce — stan bieżący**

W kontekście klasycznego Google Ads (Search) dla usług lokalnych w Polsce:

- **Kluczowe jest geotargetowanie na promień**, a nie na całe województwo — klient lokalny szuka „tu i teraz".
- Jakość first-party data i poprawność modelowania danych mają rosnące znaczenie dla skuteczności kampanii w 2026 roku.
- **Landing page jest ważniejszy niż sama reklama** — musi być szybki, czytelny, mobilny i nastawiony na jedną główną konwersję (telefon, formularz).
- Rozszerzenia reklamowe (połączenie, lokalizacja) są szczególnie istotne dla firm lokalnych — użytkownik mobilny często chce po prostu nacisnąć numer i zadzwonić.

**Ograniczenie:** Nie udało się potwierdzić żadnych dodatkowych, specyficznych wymogów Google Ads dla kategorii „usługi ogrodnicze" w Polsce poza standardowymi zasadami platformy. LSA pozostają niedostępne — to główna bariera dla tańszego kanału leadów lokalnych.

**Podsumowanie min:**

| Mina | Status | Źródło |
|------|--------|--------|
| LSA w Polsce | ❌ Niedostępne | Potwierdzone: Polska poza listą krajów LSA |
| Consent Mode v2 | ⚠️ Obowiązkowy od marca 2024 | Potwierdzone: wymóg EEA |
| Zmiana z 15.06.2026 (GA4/Ads consent) | ⚠️ Wpływa na śledzenie konwersji | Potwierdzone: nowe zasady |
| GBP jako kanał leadów | ✅ Potwierdzone pośrednio | GBP wymagany przy LSA; niezależnie kluczowy dla lokalnych |

**Niepotwierdzone:** Dokładny termin rozszerzenia LSA na Polskę — brak oficjalnych deklaracji Google.