KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wdrożenie) z potencjałem stałej współpracy/utrzymania; element przedwdrożeniowy ma charakter egzaminu wiedzy (propozycja architektury i kosztów)
INTENCJA: mieszane — wykonawcze (budowa agenta) + doradcze (rekomendacja architektury, koszty wdrożenia i utrzymania)
DECYDENT_I_BOL: Decydent nieznany; prawdopodobnie firma e-commerce. Ból: ręczne zarządzanie 400 SKU na Allegro i Amazon, pilnowanie cen, jakości ofert i stanów na dwóch marketplace’ach.
WYKONALNE: TAK, pod warunkiem dostępu do kont i API. Najbliższa opcja: hybryda — n8n/Make do orkiestracji + Python do logiki cenowej i synchronizacji; BaseLinker jako warstwa pośrednia, jeśli bezpośrednie API okażą się zbyt wąskie.
POLE_DO_POPISU: JEST. Rekomendacja architektury (n8n vs Python vs hybryda), koszt tokenów LLM, limity API, zabezpieczenia auto-pricing, kolejność modułów.
SCIEZKA_MERYTORYKI: A + B. A: klient wprost pyta o architekturę i koszty. B: A+ Content wymaga Brand Registry; auto-zmiany cen wymagają podłóg marży i limitów; API mają limity i wymagają zatwierdzeń.
MINY_I_CIEKAWOSTKI:
- A+ Content: klient pisze „A+ Content”, a to funkcja Amazon wymagająca Brand Registry. Jeśli marki nie ma w Brand Registry, moduł A+ nie zadziała — trzeba zastąpić go zwykłą optymalizacją opisów.
- Dynamic Pricing: klient pisze „sugerować zmiany (lub wprowadzać je w oparciu o ustalone reguły marżowe)”. Bez podłogi marży, kosztów prowizji, VAT i dostawy agent może wyzerować marżę. Trzeba wbudować bezpieczniki.
- Amazon SP-API: klient wymaga „Amazon Selling Partner API (SP-API)”. To nie jest zwykły klucz — wymaga zatwierdzonej aplikacji i zgodności z politykami.
- Koszty tokenów: klient pyta o „koszty tokenów API”. Przy 400 SKU można je kontrolować batchami i cache, ale przy ciągłej optymalizacji rosną.
ODMOWA: puste — brak twardej odmowy na tym etapie; ryzyka warunkowe ujęte w minach i pytaniach.
PYTANIA:
1. Czy macie już konta sprzedawcy Allegro i Amazon oraz dostęp do SP-API (aplikacja zatwierdzona)? Pytam, bo od tego zależy, czy startujemy od razu, czy od etapu rejestracji i czy doliczyć go do wyceny.
2. Czy używacie BaseLinkera / ERP / CSV, czy stany mają iść bezpośrednio z Google Sheets/Airtable? Pytam, bo to zmienia architekturę synchronizacji i koszt integracji.
3. Czy marka jest zarejestrowana w Amazon Brand Registry? Pytam, bo bez tego A+ Content nie zadziała i trzeba go zastąpić zwykłą optymalizacją opisów.
4. Które rynki Amazon mają być obsługiwane (PL, DE, inne) i czy ceny konkurencji mają być zbierane dla konkretnych ASIN/EAN? Pytam, bo liczba rynków i zakres monitoringu zmienia liczbę wywołań API i koszt utrzymania.
CO_ZLECENIE_MOWI: 400 SKU; Allegro i Amazon; moduły: dynamic pricing, AI Editor (LLM), inventory sync; API Allegro, Amazon SP-API, BaseLinker lub bezpośrednie API; Google Sheets/Airtable; Python/Node; n8n/Make/CrewAI/LangChain; oczekiwana propozycja architektury i kosztów wdrożenia, utrzymania i tokenów.
CZEGO_NIE_MOWI: kto decyduje; konkretny budżet; obecne systemy i dostępy; rynki Amazon; Brand Registry; reguły marżowe; wolumen zamówień; częstotliwość synchronizacji; auto vs ręczne zatwierdzanie zmian; RODO/AI Act; SLA; kto utrzymuje po wdrożeniu.
GRANICA_CIECIA: Oferta krótka: rekomendacja architektury, widełki wdrożenia, model utrzymania i tokenów, 3–4 pytania. Bez pełnego projektu za darmo i bez funkcji spoza ogłoszenia.
RESEARCH_POTRZEBNY: TAK. Sprawdzić aktualne API Allegro pod kątem cen konkurencji, limity i wymagania Amazon SP-API, BaseLinker API, koszty tokenów GPT-4o/Gemini dla 400 SKU oraz wymagania Brand Registry dla A+.