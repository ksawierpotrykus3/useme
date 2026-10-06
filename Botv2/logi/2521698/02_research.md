## Wyniki researchu

### 1. Ograniczenia standardowego konektora Office 365 Outlook w Power Platform

Standardowy konektor Office 365 Outlook **nie agreguje automatycznie wiadomości ze wszystkich skrzynek pracowników**. Działa w kontekście zalogowanego użytkownika i obsługuje tylko pojedyncze skrzynki użytkownika.

**Potwierdzone ograniczenia:**
- „Actionable Messages are only supported with single user mailboxes. Group and shared mailboxes are not supported.”
- Konektor wymaga, aby skrzynka była prawidłową skrzynką Microsoft 365; nie działa z dedykowanymi serwerami Exchange ani kontami sandbox.
- Aby uzyskać dostęp do skrzynek w kontekście aplikacji (a nie użytkownika), konieczne jest użycie uprawnień aplikacji Microsoft Graph, a następnie ograniczenie ich za pomocą polityki dostępu aplikacji w Exchange Online.

**Konsekwencja dla zlecenia:** Jeśli klient oczekuje, że standardowy konektor Outlook w Power Automate/Logic Apps sam zagreguje maile ze wszystkich skrzynek, projekt zatrzyma się na etapie uprawnień i konfiguracji. Wymagane jest niestandardowe rozwiązanie oparte na Microsoft Graph z uprawnieniami aplikacji.

### 2. Wymagania Microsoft Graph (Mail.Read application permissions, Exchange Online Application Access Policy)

Uprawnienie aplikacji `Mail.Read` w Microsoft Graph **domyślnie przyznaje dostęp do odczytu poczty we wszystkich skrzynkach w organizacji** bez zalogowanego użytkownika.

**Kluczowe fakty:**
- „the Mail.Read application permission allows apps to read mail in all mailboxes without a signed-in user.”
- Administratorzy mogą ograniczyć dostęp aplikacji do określonych skrzynek za pomocą polecenia `New-ApplicationAccessPolicy` (PowerShell) oraz grup zabezpieczeń z włączoną pocztą.
- Polityka dostępu aplikacji dotyczy uprawnień aplikacji do zasobów Exchange Online (kalendarze, kontakty, ustawienia skrzynki, poczta).
- Bez skonfigurowania polityki dostępu aplikacja z uprawnieniem `Mail.Read` ma dostęp do **wszystkich** skrzynek w dzierżawie.

**Konsekwencja dla zlecenia:** Konieczne jest uzyskanie zgody administratora M365 na uprawnienia aplikacji oraz skonfigurowanie polityki dostępu aplikacji, aby ograniczyć dostęp do wybranych skrzynek. W przeciwnym razie rozwiązanie będzie miało dostęp do całej poczty w organizacji, co rodzi wysokie ryzyko RODO i bezpieczeństwa.

### 3. Licencje Power Platform / Dataverse

Dostęp do środowiska z Dataverse wymaga **odpowiedniej licencji Power Platform dla każdego użytkownika**.

**Potwierdzone wymagania:**
- „Truy cập môi trường với Dataverse yêu cầu tất cả người dùng phải có một giấy phép Power Platform độc lập tương ứng cho mỗi dịch vụ đang được sử dụng.”
- Użytkownicy aplikacji opartych na Dataverse muszą być licencjonowani przez Power Apps (na aplikację lub na użytkownika, w zależności od scenariusza).
- Microsoft 365 Business Premium zapewnia jedynie podstawowe uprawnienia Power Apps z Dataverse for Teams, a nie pełny Dataverse.
- Premium connectors, Dataverse i custom connectors wymagają płatnych licencji – standardowe uprawnienia w Microsoft 365 obejmują tylko standardowe konektory.

**Konsekwencja dla zlecenia:** Jeśli organizacja nie posiada już licencji Power Apps/Dataverse, należy je uwzględnić w kosztach wdrożenia. Bez nich aplikacja CRM oparta na Dataverse nie będzie działać.

### 4. Limity Microsoft Graph

Microsoft Graph nakłada limity na liczbę żądań do skrzynek pocztowych, co ma bezpośredni wpływ na architekturę agregacji maili.

**Potwierdzone limity:**
- **10 000 żądań na 10 minut na aplikację na skrzynkę**, z maksymalnie **4 równoczesnymi żądaniami** na pojedynczą skrzynkę.
- Po przekroczeniu limitu Graph zwraca `429 Too Many Requests` z nagłówkiem `Retry-After`, którego należy przestrzegać.
- Globalny limit dla aplikacji w Microsoft Graph wynosi 130 000 żądań na 10 sekund, ale usługi takie jak Outlook mają własne, niższe limity.

**Konsekwencja dla zlecenia:** Przy dużej liczbie skrzynek i wysokim wolumenie maili konieczne jest zastosowanie kolejkowania, mechanizmu retry oraz ewentualnie subskrypcji zmian (change notifications) zamiast ciągłego odpytywania. Bez tego rozwiązanie będzie stale napotykać błędy 429 i nie będzie wydajne.

---

## Kluczowe wnioski dla zlecenia

| Obszar | Fakt potwierdzony | Źródło |
|--------|-------------------|--------|
| Konektor Outlook | Nie agreguje wszystkich skrzynek; tylko pojedyncze skrzynki użytkownika | Microsoft Learn (Connectors) |
| Graph Mail.Read | Domyślnie dostęp do wszystkich skrzynek; wymaga polityki ograniczającej | Microsoft Learn (Graph auth-limit-mailbox-access) |
| Licencje | Dataverse wymaga licencji Power Platform na użytkownika | Microsoft Learn (Power Platform licensing FAQ) |
| Limity Graph | 10 000 req/10 min/skrzynka, max 4 równoczesne | Nylas (cytujące Microsoft Graph throttling) |

**Niepotwierdzone:** Dokładny wolumen maili i liczba skrzynek w organizacji klienta – brak danych w ogłoszeniu. Wpływ na architekturę i koszty Azure wymaga doprecyzowania.