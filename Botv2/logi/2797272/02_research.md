**1. Czy Mirakl Superpharm obsługuje import plikowy (CSV/XML)?**

**TAK — potwierdzone.** Mirakl (platforma, na której działa marketplace Superpharm) natywnie obsługuje import produktów i ofert za pomocą plików w formatach **CSV, XML oraz XLSX**. W dokumentacji API Mirakl wprost wskazano, że plik importu może mieć format CSV, XML lub XLSX, a przykładowy format CSV zawiera kolumny takie jak `sku`, `product-id`, `description`, `price`, `quantity`. Niezależne źródło potwierdza, że Mirakl umożliwia import przez pliki Excel, CSV lub XML, z opcją użycia narzędzia mapowania atrybutów.

**Uwaga:** Nie znalazłem źródła, które wprost potwierdzałoby, że **konkretnie Superpharm (wersja polska)** ma włączony import plikowy dla sprzedawców — potwierdzona jest ogólna funkcjonalność platformy Mirakl. To należy oznaczyć jako **niepotwierdzone w 100% dla tego konkretnego marketplace'u**, choć wysoce prawdopodobne, bo Superpharm działa na standardowym Miraklu.

---

**2. Czy Shoper ma eksport pod marketplace (CSV/XML)?**

**TAK — potwierdzone.** Shoper umożliwia eksport produktów do pliku **CSV** z poziomu panelu administracyjnego. W dokumentacji Shoper opisano: „Eksport plików CSV jest możliwy z zakładek: zamówienia, klienci, produkty, kupony rabatowe”. Istnieje również możliwość tworzenia własnych profili eksportu CSV z wyborem pól i separatorów.

**Ważne zastrzeżenie:** Shoper **nie ma gotowej integracji z Mirakl Superpharm** — co potwierdza sam zleceniodawca w opisie („wg mojej wiedzy nie posiada automatycznej integracji”). Eksport CSV z Shopera wymaga ręcznego dostosowania kolumn do formatu wymaganego przez Mirakl (mapowanie pól). To nie jest „wtyczka”, tylko surowy plik do obróbki.

---

**Wnioski dla wyceny (diagnoza, nie recepta):**

- **Najszybsza ścieżka techniczna:** eksport CSV z Shopera → mapowanie kolumn do formatu Mirakl → import pliku CSV do panelu Mirakl Superpharm. To eliminuje ręczne wklejanie 35 SKU.
- **Mina:** mapowanie kolumn może być czasochłonne, jeśli wytyczne Superpharm (PDF-y załączone do zlecenia) wymagają specyficznych atrybutów, których nie ma w standardowym eksporcie Shopera.
- **Niepotwierdzone:** czy Superpharm PL przyjmuje import plikowy dla sprzedawców zewnętrznych (wymaga potwierdzenia w panelu Mirakl lub u opiekuna marketplace'u).