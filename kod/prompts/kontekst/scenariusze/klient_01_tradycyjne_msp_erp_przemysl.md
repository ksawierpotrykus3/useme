# PROFIL OPERACYJNY KLIENTA: TRADYCYJNE MŚP & ERP / PRZEMYSŁ (msp_erp)

## 1. Minimum Operacyjne (Kim jest i czego się boi)
- **Kto to jest:** Właściciel lub dyrektor operacyjny hurtowni, zakładu produkcyjnego, firmy budowlanej lub handlowej (8–80 osób). Czyta oferty wieczorem po zmianie, zmęczony problemami na hali/magazynie.
- **Główny lęk:** Rozjazd stanów magazynowych z fakturami, blokada wydań towaru (WZ), błędy przy inwentaryzacji, kary z KSeF/US, przestój produkcji lub uzależnienie od jednego skryptu, który przestanie działać po aktualizacji ERP.
- **Stosunek do ceny:** Decyzyjny (Win Rate 17.2%, budżety 2800–8500+ zł). Nie szuka najtańszego studenta — kupuje ciągłość operacji i brak błędów ludzkich na magazynie.

## 2. Konkret, który MUSI paść w ofercie
- Używaj języka fizycznych operacji i dokumentów: **WZ, PZ, MM, kompletacja, BOM (zestawienie materiałów), stany magazynowe, bufor bezpieczeństwa, inwentaryzacja, KSeF, baza SQL Enova / Subiekt Sfera / Comarch Optima / TopSolid**.
- Pokaż, że rozumiesz proces na hali/magazynie (np. że magazynier nie może przeklepywać pozycji ręcznie, a synchronizacja musi mieć obsługę ponowień i logowanie błędów).
- **Jeśli zlecenie dotyczy obiegu faktur / OCR / księgowości / ERP:**
  - **Podział na 3 strumienie dokumentów (zamiast pchania wszystkiego przez drogi OCR Vision):**
    1. *KSeF (XML):* Polskie faktury ustrukturyzowane warto pobierać bezpośrednio jako XML (uwaga: Comarch Optima w nowych wersjach ma już natywny odbiór KSeF z pozycjami — w automatyzacji n8n nie dublujemy tego mechanizmu na ślepo, lecz uzupełniamy go o automatyczne przypisanie MPK/kategorii lub parowanie z dokumentami WZ/zamówieniami).
    2. *Cyfrowe PDF-y z maila:* Mają gotową warstwę tekstową — parsujemy je bezpośrednio (100% dokładności znakowej, zero kosztu tokenów Vision).
    3. *Skany papierowe i zdjęcia z telefonów (pracownicy w terenie, WZ, paragony):* Tu stosujemy preprocessing obrazu (prostowanie skosu, poprawa kontrastu) + model Vision z progiem pewności (confidence score) dla każdego pola.
  - **Walidacja matematyczna z tolerancją zaokrągleń VAT (1–2 gr) i deduplikacja:** Wskaż, że ustawa o VAT dopuszcza liczenie podatku od sumy stawek lub od pojedynczych pozycji (co daje legalne różnice 1–2 gr), a deduplikacja po kluczu `NIP + numer dokumentu` (oraz sumie kontrolnej pliku) blokuje podwójne wprowadzenie tej samej faktury ze skanera, maila i KSeF.
  - **Bezpieczna integracja z ERP:** Podkreśl import przez oficjalne struktury (np. **Praca Rozproszona XML** lub API w Comarch Optima, Sfera w Subiekcie, WebAPI w Enova365), które bezpiecznie przenoszą zarówno rejestry VAT, jak i dokumenty magazynowe (`WZ, PZ, RW, PW`), zamiast ślepego zapisu `INSERT` do tabel SQL produkcyjnej bazy (który rozwala numerację i narusza gwarancję producenta). Dla niszowych systemów produkcyjnych bez API (opartych na MS SQL) — zadeklaruj weryfikację schematu bazy na kopii testowej.
- Zaproponuj bezpieczne wdrożenie: najpierw testy na kopii bazy / środowisku testowym na próbce realnych dokumentów, bez zatrzymywania bieżącego fakturowania, 30 dni gwarancji rozruchowej na własny kod oraz krótką instrukcję dla pracowników.

## 3. Czego kategorycznie UNIKAĆ
- Zero korpo-nowomowy i startupowych haseł (`transformacja cyfrowa`, `cloud-native`, `synergia`, `end-to-end`, `scalability`).
- Zakaz proponowania przepisania całego systemu firmy od zera, gdy klient chce zintegrować lub naprawić obecny ERP.
- Zakaz coachingowego wstępu („Doskonale rozumiem trudy prowadzenia hurtowni..."). Wchodź od pierwszego zdania w mechanikę systemu klienta.

## 4. Konstrukcja Question CTA (na koniec oferty)
Zadaj precyzyjne pytanie techniczno-procesowe o środowisko klienta, np.:
- o dokładną wersję systemu ERP i posiadane rozszerzenia licencyjne (np. Sfera dla Subiekta, WebAPI w Enova365),
- o wolumen dokumentów dziennie i kierunek synchronizacji (jednokierunkowo czy dwukierunkowo z blokadą stanów).
