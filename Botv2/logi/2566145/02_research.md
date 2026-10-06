### 1. Zgodność PrestaShop 8.1/8.2 z PHP 8.1/8.2, MariaDB 11.4.9 i LiteSpeed

**PHP:** PrestaShop 8.0–8.2 oficjalnie wspiera PHP 8.1 (rekomendowana) oraz PHP 8.2. PHP 7.2–8.0 są kompatybilne, ale niezalecane ze względu na zakończenie wsparcia. Tabela kompatybilności potwierdza: dla PS 8.0–8.2 PHP 8.1 jest wersją rekomendowaną, a ≥8.2 — wspieraną.

**MariaDB:** Minimalna wersja to MariaDB 10.2; nowsze wersje są zalecane. MariaDB 11.4.9 **znacznie przewyższa minimum** — nie potwierdzono jednak w oficjalnej dokumentacji explicitnej listy przetestowanych wersji powyżej 10.2. Można uznać, że wymóg jest spełniony (nowsza wersja), ale **brak oficjalnego potwierdzenia dla konkretnie 11.4.9**.

**LiteSpeed:** PrestaShop 8 działa na Apache 2.4+, Nginx 1.0+ oraz LiteSpeed — LiteSpeed jest wymieniany jako kompatybilny serwer WWW.

> **Niepotwierdzone:** Brak oficjalnego testu zgodności PS 8.1/8.2 z MariaDB 11.4.9 na LiteSpeed w konfiguracji łącznej. Wymogi cząstkowe są spełnione, ale pełna zgodność kombinacji nie została zweryfikowana w dokumentacji.

---

### 2. Dostępność szablonu Warehouse pod PrestaShop 8

Szablon Warehouse **jest dostępny i aktywnie utrzymywany dla PrestaShop 8.x**. Aktualna wersja to Warehouse 4.7.x dla PS 8.x (oraz 4.8.x dla PS 9.x). Produkt na PrestaShop Addons deklaruje zgodność z wersjami od 1.7.8 do 9.2, a więc obejmuje PS 8.1/8.2. Deweloper potwierdza, że wersja dla PS8 będzie nadal utrzymywana, a przepisanie szablonu planowane jest dopiero dla PrestaShop 9 z brakiem wstecznej kompatybilności.

**Kluczowa mina:** Customizacje z wersji 1.6 **nie przeniosą się 1:1** — konieczna jest instalacja nowej, kompatybilnej wersji szablonu i odtworzenie modyfikacji.

---

### 3. Kompatybilność BaseLinker / WebService z PrestaShop 8

BaseLinker posiada **oficjalny moduł API dla PrestaShop**, który działa również na PS 8.x. Instalacja polega na: instalacji modułu w PrestaShop, wygenerowaniu klucza API w panelu (Narzędzia → Webowe usługi → „Povolit PrestaShop Webservis” → „Přidat nový klíč webové služby”) i wpisaniu go w BaseLinkerze. Po połączeniu synchronizowane są produkty, zamówienia i stany magazynowe.

**Uwaga:** Wymagane jest zaznaczenie **wszystkich uprawnień dostępu** dla klucza WebService — w przeciwnym razie integracja nie będzie działać niezawodnie. BaseLinker zaleca również instalację dedykowanego pluginu dla poprawnego pobierania informacji o przesyłkach.

---

### 4. Typowe pułapki migracji 1.6 → 8.x

**To nie jest upgrade, lecz migracja do czystej instalacji.** Między 1.6 a 8.x zmieniło się praktycznie wszystko:

- **Framework:** 1.6 używa własnego MVC; nowe wersje oparte są na Symfony.
- **Szablony:** Motywy z 1.6 są **całkowicie niekompatybilne** z 1.7+ — szablon musi zostać wymieniony.
- **Moduły:** Wiele modułów 1.6 wymaga zastąpienia lub przepisania — zmieniły się hooki, kontrolery admina i całe API modułów. W praktyce 90% modułów z 1.7/8.0 działa z PHP 7.4, ale z PHP 8.1 pojawiają się błędy deprecated functions i bugi.
- **Baza danych:** Zmiany schematu, nowe tabele, zmodyfikowane relacje — migracja danych jest możliwa, ale wymaga transformacji.
- **PHP:** 1.6 działał na PHP 5.x/7.0; nowe wersje wymagają PHP 8.1+.
- **SEO:** Złe zarządzanie adresami URL podczas migracji może **zniszczyć lata wypracowanych pozycji w Google**. Konieczne jest zmapowanie wszystkich indeksowanych URL-i z Google Search Console i przygotowanie przekierowań 301.

**1-Click Upgrade nie jest rekomendowanym rozwiązaniem** dla ścieżki 1.6 → 8.x. Nawet jeśli aktualizacja się powiedzie, motyw i moduły customowe nie będą działać — trzeba zacząć od nowa. Rekomendowane podejście to czysta instalacja PS 8.x na stagingu + migracja danych.