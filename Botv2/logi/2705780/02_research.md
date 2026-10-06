## Research: Płatności marketplace i regulacje

### 1. Stripe Connect – split payments
Stripe Connect obsługuje model marketplace z podziałem płatności za pomocą **„separate charges and transfers”** – platforma pobiera jedną płatność od kupującego, a następnie wykonuje osobne transfery na konta połączonych sprzedawców .

**Problem z poolem środków:** W modelu Stripe Connect środki z płatności trafiają na **wspólny bilans platformy** i nie są „ogrodzone” (ring-fenced), dopóki platforma jawnie nie przekaże ich na konto sprzedawcy. W praktyce oznacza to, że:
- automatyczne wypłaty zaplanowane na koncie platformy mogą przypadkowo zużyć środki przeznaczone dla sprzedawcy,
- niepowiązane chargebacki mogą obciążać wspólną pulę,
- opłaty Stripe są pobierane z tej samej puli,
- błędy operacyjne (np. przypadkowy zwrot) mogą pozostawić sprzedawców bez środków bez jasnego śladu audytowego .

Stripe wprowadził nowy typ transakcji **„Segregated Separate Charges and Transfers”** z powodu zmian w PSD3 (przewidywane wejście w życie pod koniec 2027 r.) i prawdopodobnego zaostrzenia wyłączenia dla agentów handlowych (Commercial Agent Exemption) .

**Wymogi regulacyjne:** W ramach PSD2 większość marketplace’ów działa na wyłączeniu Commercial Agent Exemption, co pozwala przetwarzać płatności bez formalnej licencji instytucji płatniczej. Jednak PSD3 ma to zmienić – regulacje coraz częściej wymagają od platform wykazania, że środki klientów są **safeguarded**, oddzielone od funduszy operacyjnych i chronione przed wierzycielami platformy .

### 2. Przelewy24 – Marketplace
Przelewy24 oferuje usługę **Marketplace**, która pozwala na obsługę płatności platformy integrującej produkty różnych sprzedawców, z rozdzielaniem środków na właściciela platformy oraz poszczególnych sprzedawców .

**Przebieg transakcji:** Klient finalizuje zakup jedną płatnością; po potwierdzeniu płatności Przelewy24 automatycznie przekazuje potwierdzenie właścicielowi marketplace. **Wysokość prowizji oraz podział kwoty na poszczególne konta mogą być ustalane indywidualnie** .

**Dwa modele:**
- **Model 1:** Naliczenie prowizji i wystawienie faktury odbywa się z konta technicznego Marketplace (właściciela platformy). Prowizja naliczana jest od pełnej kwoty koszyka. Podział pozostałych środków między sprzedawców ustala właściciel platformy .
- **Model 2:** Naliczenie prowizji i faktura odbywa się z kont rozliczeniowych poszczególnych subpartnerów (sprzedawców). Po podziale 100% kwoty koszyka prowizja naliczana jest od kwot przekazywanych sprzedawcom .

### 3. PayU – Marketplace
PayU Marketplace to rozwiązanie dla platform działających jako pośrednicy, łączące kupujących i sprzedających (submerchantów). PayU oferuje **usługę weryfikacji submerchantów**, zdejmując z platformy odpowiedzialność za ten proces .

**Mechanizm:** PayU Marketplace wykorzystuje mechanizm **„single shopping cart”** – kupujący może nabyć produkty od wielu sprzedawców w jednej transakcji. Płatność jest **automatycznie dzielona na odpowiednie konta w systemie PayU**, więc platforma **nie musi obsługiwać funduszy submerchantów** .

**Wymogi AML/KYC:** PayU jest zobowiązana przepisami prawa o przeciwdziałaniu praniu pieniędzy do weryfikacji klientów w tym kontekście. PayU oferuje dwie metody rejestracji submerchantów .

### 4. Tpay – Marketplace
Tpay oferuje rozwiązanie **Marketplace** dla platform e-commerce łączących ofertę wielu sprzedawców. Klient płaci za produkty od kilku dostawców tylko raz, a **proces rozdzielania transakcji pomiędzy poszczególne sklepy odbywa się automatycznie** .

**Wymagania wstępne:** Aby korzystać z Marketplace Tpay, platforma musi być w **Programie Partnerskim Tpay**. Konieczne jest podpisanie odpowiedniej umowy z opiekunem Programu Partnerskiego .

**Rejestracja sprzedawców:** Sprzedawcy są powiązani z marketplace za pomocą kodu oferty lub API. Można ich rejestrować poprzez generator ofert w Panelu Partnera lub przez Open API .

### 5. Wymogi KYC dla platform sprzedających bilety
Przykład platformy Fienta (sprzedaż biletów) pokazuje typowe wymogi KYC:
- **Przed rozpoczęciem sprzedaży biletów** sprzedawca musi zweryfikować dane oraz konto bankowe.
- Weryfikacja odbywa się przez **płatność testową** (1 EUR, zwracana) lub **potwierdzenie danych osobowych w Veriff**.
- Wymagany jest ważny dokument tożsamości oraz komputer/urządzenie mobilne z kamerą .

### 6. Regulacje płatnicze w Polsce – kiedy potrzebny wpis do KNF?
Według kancelarii Silesia Legal House: **„Nawet niepozorny model rozliczeń może zostać uznany za usługę płatniczą wymagającą wpisu MIP w rejestrze KNF”** .

**Kluczowy moment:** Jeśli w modelu biznesowym dochodzi do **przyjmowania środków od użytkowników lub przekazywania ich innym podmiotom**, może to zostać uznane za prowadzenie działalności w zakresie usług płatniczych, wymagającej wpisu do rejestru KNF .

**Mała Instytucja Płatnicza (MIP):** Uproszczona kategoria dostawcy usług płatniczych (wpis do rejestru zamiast pełnego zezwolenia KNF), wprowadzona w wyniku implementacji PSD2. Status MIP może uzyskać nawet przedsiębiorca prowadzący jednoosobową działalność gospodarczą .

**Ograniczenie obrotowe:** Dopuszczalna wielkość obrotu wykonanego przez MIP **nie może przekroczyć 1 500 000 euro miesięcznie** .

---

### Wnioski dla zlecenia

| Aspekt | Ustalenie | Źródło |
|--------|-----------|--------|
| Stripe Connect | Obsługuje split payments, ale wymaga fund segregation przy PSD3 |  |
| Przelewy24 | Oferuje Marketplace z dwoma modelami podziału prowizji |  |
| PayU | Automatyczny split, nie trzeba obsługiwać funduszy submerchantów |  |
| Tpay | Automatyczny podział, wymaga Programu Partnerskiego | ,  |
| KYC (bilety) | Weryfikacja tożsamości + konto bankowe przed startem sprzedaży |  |
| Regulacje PL | Przyjmowanie/przekazywanie środków → potencjalny obowiązek MIP/KNF |  |

**Niepotwierdzone:** Brak w źródłach konkretnych stawek prowizji dla poszczególnych PSP w modelu marketplace, brak szczegółów dot. wymogów KYC specyficznych dla platform biletowych w Polsce (poza przykładem Fienta), brak potwierdzenia czy wyłączenie Commercial Agent Exemption ma zastosowanie do modelu opisanego w zleceniu (wymaga indywidualnej oceny prawnej).