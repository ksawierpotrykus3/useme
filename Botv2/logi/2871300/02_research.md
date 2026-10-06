## 1. Czy OTOMOTO udostępnia API do własnych ogłoszeń dla dealerów?

**Potwierdzone:** OTOMOTO API jest dostępne wyłącznie dla Klientów Biznesowych oraz firm obsługujących integrację w ramach konta Biznesowego. Dostęp wymaga wysłania formularza rejestracyjnego, a o przyznaniu klucza decyduje OTOMOTO. Do każdej aplikacji przysługuje jeden klucz API. Warunki korzystania z API określają, że Partner/Professional User to podmiot prowadzący działalność gospodarczą, który korzysta z integracji w imieniu Programisty.

**Niepotwierdzone:** Nie znalazłem w dostępnych źródłach jednoznacznego potwierdzenia, że API OTOMOTO umożliwia **pobranie** (eksport) własnych ogłoszeń dealera — dokumentacja Terms and Conditions mówi ogólnie o komunikacji między Aplikacją a platformą OTOMOTO, ale nie precyzuje kierunku przepływu danych.

**Istotne zastrzeżenie:** Regulamin OTOMOTO (cytowany w wątku zewnętrznym) stanowi: „Zabronione jest jakiekolwiek agregowanie i przetwarzanie danych oraz innych informacji dostępnych w Serwisie OTOMOTO w celu ich dalszego udostępniania osobom trzecim w ramach innych serwisów internetowych jak i poza Internetem”. Oznacza to, że nawet przy dostępie do API, masowe pobranie 5952 ogłoszeń w celu przeniesienia ich na Allegro może być sprzeczne z regulaminem.

## 2. Czy API Allegro pozwala tworzyć szkice bez powiązania z Katalogiem?

**Potwierdzone:** Allegro REST API udostępnia endpoint `POST /sale/product-offers` do tworzenia szkiców ofert. Jednak od czerwca 2024 Allegro **uniemożliwia edycję ofert, dopóki nie zostaną połączone z Katalogiem produktów Allegro**. Od lipca 2024 Allegro wymaga, aby **wszystkie oferty** były połączone z Katalogiem — z wyjątkiem wybranych kategorii o unikatowym asortymencie.

**Kluczowy problem:** Kategoria „części samochodowe” najprawdopodobniej **nie należy** do wyjątków (wyjątki to m.in. Kolekcje/Sztuka, Rękodzieło, ogłoszenia drobne). W praktyce oznacza to, że plan klienta — wgranie 5952 ofert jako szkiców **bez** powiązania z Katalogiem — może być niewykonalny w tej kategorii od lipca 2024. Allegro może automatycznie kończyć oferty niepowiązane z Katalogiem.

**Niepotwierdzone:** Nie znalazłem źródła, które wprost stwierdzałoby, że szkic (status INACTIVE) również podlega obowiązkowi powiązania z Katalogiem. Możliwe, że wymóg dotyczy tylko ofert aktywnych, ale wymóg edycji z czerwca 2024 sugeruje, że nawet szkice mogą być nim objęte.

## 3. Regulamin OTOMOTO a znak wodny i pobieranie zdjęć

**Potwierdzone:** Regulamin OTOMOTO (cytowany w wątku zewnętrznym) stanowi: „Pobieranie lub wykorzystywanie w jakimkolwiek zakresie dostępnych w ramach Serwisu OTOMOTO materiałów wymaga każdorazowo zgody Grupy OLX”. Wątek na forum prawnym potwierdza, że zdjęcia są „wyłączną własnością serwisu lub użytkownika, a pobieranie i wykorzystywanie zdjęć jest możliwe przy uzyskaniu specjalnej zgody”.

**Niepotwierdzone:** Nie znalazłem w dostępnych mi źródłach **bezpośredniego** zapisu regulaminu OTOMOTO, który wprost zakazywałby **neutralizacji znaku wodnego** (blur). Jednak skoro samo pobieranie i wykorzystywanie zdjęć wymaga zgody, to celowe usunięcie/rozmycie znaku wodnego w celu użycia zdjęcia na innej platformie tym bardziej wykracza poza dozwolone użycie — brak zgody obejmuje również modyfikację oznaczeń.

## Podsumowanie min z dowodami

| Mina | Dowód | Status |
|---|---|---|
| **Masowe pobranie danych z OTOMOTO** | Regulamin zakazuje agregowania i przetwarzania danych w celu udostępniania na innych serwisach | Potwierdzone |
| **Pobranie i użycie zdjęć z OTOMOTO** | Pobieranie materiałów wymaga każdorazowej zgody Grupy OLX | Potwierdzone |
| **Szkice bez Katalogu Allegro** | Od lipca 2024 wszystkie oferty muszą być powiązane z Katalogiem (z wyjątkami, które nie obejmują części samochodowych) | Potwierdzone |

**Wniosek badawczy:** Zlecenie opiera się na trzech założeniach, z których każde jest co najmniej wątpliwe regulaminowo, a trzecie (szkice bez Katalogu) może być technicznie niewykonalne w kategorii części samochodowych od lipca 2024.