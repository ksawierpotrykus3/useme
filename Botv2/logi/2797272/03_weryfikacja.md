```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wprowadzenie 35 SKU na marketplace)
INTENCJA: wykonawcze
DECYDENT_I_BOL: Sprzedawca w Shoper wchodzący na Superpharm. Ból realny: brak natywnej integracji Shoper–Mirakl, klient zakłada, że zostaje mu ręczne wklepywanie 35 SKU. Bolączka drugoplanowa: chce mieć to zrobione raz i poprawnie, bo od tego zależy publikacja oferty.
WYKONALNE: TAK. Ścieżka plikowa (eksport z Shopera → mapowanie → import do Mirakl) albo ręczna przez panel. Obie wykonalne.
POLE_DO_POPISU: JEST — klient NIE WIE, że Mirakl standardowo obsługuje import plikowy (CSV/XML/XLSX). Zakłada ręczne wprowadzanie. To nie mina, to alternatywna, lepsza droga (ścieżka C).
SCIEZKA_MERYTORYKI: C (udowodniona alternatywa — droga plikowa zamiast ręcznej, oparta na standardzie Mirakl)
MINY_I_CIEKAWOSTKI: brak realnych min. Kolumna „dane niekompletne” to zwykłe ryzyko projektowe, nie mina — nie wchodzi.
ODMOWA: puste — żaden z 6 typów nie zachodzi. Shoper ma eksport CSV (kanał dostępu istnieje), Mirakl standardowo ma import (kanał dostępu istnieje), brak konfliktu zakresu, brak regulacji specyficznych dla tego zlecenia w treści.
PYTANIA:
1. Czy dane produktów (zdjęcia, opisy, parametry, EAN, ceny, stany) są kompletne i gotowe, czy wymagają uzupełnienia/konwersji? Pytam, bo to różnica między „wklejenie” a „przygotowanie treści” — zmienia czas i wycenę.
2. Czy możemy dostać eksport produktów z Shopera (CSV) i czy w Waszym panelu Mirakl jest widoczna opcja Import (plik CSV/XML)? Pytam, bo jeśli tak — proponuję drogę plikową zamiast ręcznego wprowadzania 35 SKU: szybciej i zostaje szablon na kolejne produkty. Nie pisałem „wycena byłaby zgadywaniem” — jeśli droga plikowa odpada, robimy ręcznie i też się wyceni.
3. Czy po wprowadzeniu i publikacji oczekujecie sprawdzenia poprawności (zdjęcia, atrybuty, ceny) i ewentualnych poprawek, czy tylko samego wprowadzenia? Pytam, bo QA po publikacji to osobny zakres i wpływa na kwotę.
CO_ZLECENIE_MOWI: 35 SKU, Mirakl Superpharm, Shoper, brak automatycznej integracji, klient ma konto Mirakl i wytyczne (2 PDF-y: Multimedia_i_treści_produktowe_MANUAL.pdf, Instrukcja_dla_użytkowników.pdf).
CZEGO_NIE_MOWI: kompletność danych, format danych, czy panel Mirakl ma aktywny import plikowy, czy jest dostęp do Shopera (eksport), zakres QA po publikacji, termin, budżet poza „do negocjacji”.
GRANICA_CIECIA: Zlecenie średnio informacyjne. Wycena niejasna → widełki orientacyjne + 3 pytania. Krótko. Żadnej merytoryki poza jedną alternatywą (droga plikowa) wpisaną w pytanie 2, bo tam ma dowód i falsyfikowalność.
RESEARCH_POTRZEBNY: NIE — research z iteracji 1 wyczerpał potrzebę. Ustalone: Mirakl obsługuje import CSV/XML/XLSX (standard platformy), Shoper ma eksport CSV. Niepotwierdzone „na 100%” dla samego Superpharm PL — dlatego NIE twierdzę, tylko pytam w pytaniu 2. Dalszy research nic nie zmieni; rozstrzygnięcie jest u klienta w panelu.

DECYZJE:
- DOPISAĆ do oferty (jedno zdanie, wplecione w pytanie 2, nie jako osobny akapit): „Mirakl standardowo ma import plikowy — jeśli w Waszym panelu Superpharm widzicie opcję Import, proponuję eksport CSV z Shopera → mapowanie kolumn → import, zamiast ręcznego wklepywania 35 SKU; szybciej i zostaje szablon na kolejne produkty.” To realizuje ścieżkę C bez straszenia i bez zgadywania (bo falsyfikowalne: klient sprawdza panel i mówi tak/nie).
- ODPOWIEDZIEĆ: nie — intencja wykonawcza, odpowiadamy ofertą + widełki + 3 pytania.
- DOPYTAĆ: 3 pytania powyżej. Q1 i Q3 nieredukowalne (zmieniają wycenę). Q2 rozstrzyga, czy idziemy drogą plikową czy ręczną — to zmienia pracochłonność, więc też nieredukowalne.
- SKREŚLONE z iteracji 1: teza o „mapowaniu kolumn jako minie” (brak dowodu, słabe) oraz fragment pytania 2 o „dostęp do konta Mirakl” (klient napisał, że ma konto — pytanie o oczywiste = sygnał „nie przeczytałem”).
```