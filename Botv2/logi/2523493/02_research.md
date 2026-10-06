## Wynik researchu: PMS Lite + WooCommerce — kluczowe ograniczenie

**Główna mina potwierdzona.** Paid Member Subscriptions w wersji **Lite nie obsługuje płatności cyklicznych (recurring payments)**. Jest to funkcja dostępna wyłącznie w wersji **Pro** (płatnej).️

### 1. Integracja PMS Lite z WooCommerce — co działa

PMS Lite **integruje się z WooCommerce** i pozwala na:

- **Restrykcje dostępu do treści** — blokowanie stron, wpisów i custom post types na podstawie poziomu członkostwa
- **Restrykcje produktów WooCommerce** — ograniczanie przeglądania i zakupu produktów w zależności od planu subskrypcji
- **Przypisanie dostępu per produkt** — treści mogą być widoczne tylko dla członków z określonym planem

To pokrywa wymóg „użytkownik widzi wyłącznie treści przypisane do wykupionego produktu” — **pod warunkiem, że dostęp jest jednorazowy lub przypisany ręcznie**.

### 2. Subskrypcje (recurring) — tu jest problem

| Funkcja | PMS Lite | PMS Pro |
|---|---|---|
| Integracja z WooCommerce | ✅ | ✅ |
| Content restriction per plan | ✅ | ✅ |
| **Płatności cykliczne (recurring)** | ❌ | ✅ |
| **Stripe / PayPal Pro jako gateway** | ❌ | ✅ |
| Automatyczne odnawianie subskrypcji | ❌ | ✅ |

Źródło: Kinsta — *„Você tem que pagar pela versão Pro para ter acesso a pagamentos recorrentes ou gateways de pagamento como Stripe e PayPal Pro”*. Także Cozmoslabs potwierdza, że PMS sam w sobie może obsłużyć **manualne** subskrypcje WooCommerce (bez automatycznego odnowienia), a do automatycznego recurring billing potrzebny jest dodatkowy mechanizm.

**Konsekwencja dla zlecenia:** Jeśli „2 subskrypcje” mają być **cykliczne z automatycznym odnawianiem**, PMS Lite **nie wystarczy**. Automatyczne przypisanie dostępu po opłaceniu subskrypcji nie zadziała bez Pro (lub alternatywy).

### 3. Wymagania WooCommerce Subscriptions (jeśli klient zdecyduje się na to rozszerzenie)

Jeśli zamiast PMS Pro miałby być użyty WooCommerce Subscriptions, wymagania są następujące:

- **PHP**: 7.0+
- **MySQL**: 5.6+
- **WordPress**: 5.9+
- **WooCommerce**: 6.5+

### 4. Wnioski dla decyzji o przyjęciu zlecenia

| Scenariusz | Wykonalność na wskazanym stacku | Uwaga |
|---|---|---|
| Produkty jednorazowe + dostęp przypisany ręcznie | ✅ PMS Lite wystarczy | |
| 2 subskrypcje **cykliczne** z automatycznym dostępem | ❌ PMS Lite **nie wystarczy** | Wymaga PMS Pro lub WooCommerce Subscriptions |
| Subskrypcje **czasowe** (dostęp na X dni, bez odnowienia) | ✅ PMS Lite + ręczna weryfikacja | Możliwe, ale nie w pełni automatyczne |

**Werdykt:** Zlecenie jest wykonalne **warunkowo** — tylko jeśli klient dopuści PMS Pro (lub inne płatne rozszerzenie) w ramach tego samego stacku WP/Woo. Jeśli upiera się przy **wyłącznie Lite**, a subskrypcje mają być cykliczne, wówczas kluczowy wymóg funkcjonalny nie zostanie spełniony.

### Pytanie weryfikacyjne do klienta (priorytet)

> **Czy subskrypcje mają być cykliczne z automatycznym odnawianiem, czy to dostęp czasowy (np. na 30 dni bez odnowienia)? Jeśli cykliczne — czy dopuszczają Państwo PMS Pro lub WooCommerce Subscriptions w ramach tego samego stacku WordPress + WooCommerce?**

To jedno pytanie rozstrzyga, czy zlecenie jest wykonalne na wskazanym przez klienta stacku, czy wymaga zmiany licencji.