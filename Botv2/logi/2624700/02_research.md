**Research wykonany w zakresie wskazanym przez dziennik: API map, kanały powiadomień (SMS/push), integracje ERP/księgowe. Poniżej wyłącznie potwierdzone fakty ze źródłami.**

---

### 1. API map (planowanie i optymalizacja tras)

**Google Maps Platform** oferuje trzy plany subskrypcyjne z limitem połączonych wywołań: Starter (50 000 wywołań/mies., $100/mies.), Essentials (100 000, $275/mies.) i Pro (250 000, $1 200/mies.). W planach zawarte są m.in. SKU: *Compute Routes*, *Compute Route Matrix*, *Route Optimization – Single Vehicle Routing*.

**Routes API** działa w modelu pay-as-you-go; rozliczenie zależy od użytych funkcji (Basic, Advanced, Preferred SKU). Użycie argumentu optymalizacji waypointów jest rozliczane po wyższej stawce.

**Mapbox** rozlicza routing i optymalizację osobno od standardowego ładowania map: **$0.50–$5 za 1 000 requestów**. Optimization API ma limit 12 współrzędnych na request, 25 dystrybucji na request i 300 requestów na minutę.

**Ocena „groźności” (diagnoza, nie recepta):** Automatyczna optymalizacja tras to największy mnożnik pracochłonności i kosztów operacyjnych (abonament mapowy + koszt za request). Brak w ogłoszeniu wskazania, czy planowanie ma być ręczne (panel dyspozytora), czy automatyczne — to luka w zakresie, która bezpośrednio przekłada się na architekturę i wycenę.

---

### 2. Kanały powiadomień (SMS / push)

**Twilio SMS – Polska:** stawka za wysłanie SMS na numer komórkowy wynosi **$0.0457** za wiadomość (segment). Odbieranie SMS: $0.0075. Alphanumeric Sender ID: $0.0457. Opłata za obsługę nieudanej wiadomości (status „Failed”): $0.001 za wiadomość.

**Firebase Cloud Messaging (FCM)** jest jednym z produktów Firebase dostępnych **bez opłat** — niezależnie od planu (Spark lub Blaze), nawet w aplikacjach produkcyjnych i przy milionach użytkowników. FCM nie jest rozliczany per wiadomość.

**Ocena „groźności”:** Powiadomienia push (FCM) nie generują kosztu per message, ale wymagają utrzymania projektu Firebase i konfiguracji po stronie klienta (Android/iOS/Web). SMS (Twilio) generuje koszt zmienny zależny od wolumenu — przy braku danych o liczbie dostaw/dzień nie da się oszacować miesięcznego kosztu SMS. Brak w ogłoszeniu wskazania kanałów powiadomień (in-app / e-mail / SMS / push) to luka w zakresie.

---

### 3. Integracje ERP / księgowe (Polska)

**Symfonia ERP WebAPI** udostępnia usługę internetową (WebServices, REST, JSON) do wymiany danych między modułami Handel oraz Finanse i Księgowość a rozwiązaniami zewnętrznymi. W standardzie obsługuje m.in. zarządzanie kontrahentami, stanami magazynowymi, zamówieniami własnymi/obcymi, dokumentami sprzedaży. Działa przez HTTPS.

**Comarch ERP Optima / XL** — integracja z bankowością przez **CitiConnect API** (Citi Handlowy) umożliwia bezpośrednie połączenie systemu ERP z systemem banku.

**Merit Aktiva (360 Księgowość)** — popularne oprogramowanie księgowe w chmurze w Polsce i regionie bałtyckim; **kompatybilne z KSeF** (faktury tworzone przez API są przechwytywane przez wbudowaną integrację KSeF).

**Fakturownia** — integracja z Odoo przez API Key; obsługa KSeF.

**Ocena „groźności”:** Ogłoszenie nie wskazuje, z jakim systemem ERP/księgowym aplikacja ma się integrować. Każda integracja (zwłaszcza z KSeF, bankiem czy Symfonią) to osobny moduł, wymagający dostępu do API i konfiguracji po stronie klienta — bez tej informacji zakres i wycena są niepełne.

---

### Niepotwierdzone / brak danych

- **Kto jest decydentem** w firmie dystrybucyjnej — ogłoszenie nie podaje.
- **Budżet** — „do negocjacji”, brak widełek.
- **Wolumen** użytkowników, zamówień, dostaw na dzień — brak danych, uniemożliwia oszacowanie kosztów SMS i ewentualnych limitów API map.
- **Szczegóły serwera** (OS, konteneryzacja, dostępność) — ogłoszenie mówi tylko „własny serwer”.
- **Czy Figma i specyfikacja są kompletne i dostępne** — ogłoszenie deklaruje ich dostarczenie, ale nie potwierdza gotowości.
- **Termin realizacji** — nie podano.
- **Etapy akceptacyjne** — nie wskazano.

Źródła: Google Maps Platform Subscriptions; Routes API Usage and Billing; Mapbox pricing (softwarefinder); Mapbox Optimization API limits (mapbox.com); Twilio SMS Pricing Poland; Firebase Pricing Plans; Symfonia ERP WebAPI; Citi Handlowy CitiConnect API (citigold.pl); Merit Aktiva API (pypi.org); Odoo–Fakturownia Integration (cetmix.com).