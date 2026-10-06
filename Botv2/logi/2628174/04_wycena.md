=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
**Wycena całości:** 7 200–12 600 zł, ok. **10–18 dni roboczych**.  
**Minimalny sensowny etap 1:** audyt + projekt drzewa + reguły normalizacji + test na 500–1000 produktach: **1 800–2 700 zł, 3–5 dni**.

Budżet **500 zł** to ok. 5–6 godzin pracy, czyli tylko wstępna konsultacja/szkic — nie pokryje projektu drzewa, migracji 75k produktów ani konsolidacji rozmiarów.

Uzasadnienie: W WooCommerce warianty dopasowują się po slugach termów, nie po etykietach — sama zmiana nazwy na „39,5” nie scali trzech rozmiarów, trzeba przepiąć produkty między termami. Przy 75 000 produktów drzewo kategorii to decyzja o wydajności filtrów i kategorii, nie kosmetyka. Brakuje mi też dwóch informacji: czy rozmiar jest jednym globalnym atrybutem czy osobnym per typ produktu oraz skąd pochodzą dane produktów (feed/import/ręcznie) — to zmienia zakres.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: główna wycena 7 200–12 600 zł jest obroniona, ale **minimalny etap 1 na 1 800–2 700 zł jest lekko napompowany** — wliczyłem tam test na 500–1000 produktach, który jest już wykonawstwem, a nie konsultacją, więc realnie sam „audyt + drzewo + reguły" to ok. **1 200–1 800 zł (13–20 h)**. Zgadłem dwie rzeczy bez potwierdzenia: (1) że wtyczka klienta posłuży jako narzędzie wykonawcze naszych reguł — nie widziałem jej kodu, więc to założenie, nie fakt; (2) że stare URL-e kategorii mają wartość SEO — to moja propozycja 301, klient tego nie zgłaszał. Nie dopisałem nic „na siłę" poza tym — miny o slugach i `tax_query` mają dowód w researchu, nie są straszakami. Korekta: etap 1 **1 200–1 800 zł**, całość bez zmian, budżet 500 zł nadal pokrywa tylko wstępną konsultację i szkic.

=== DeepSeek-B — RUNDA 1 ===
## Wycena

**Budżet 500 PLN nie pokryje całości.** To trzy prace: projekt drzewa + reguły, migracja 75k produktów, konsolidacja termów rozmiaru.

**Etap 1 — projekt + reguły + próbka (500–1000 produktów):**
- 8–12 h → **720–1080 PLN**, ~2–3 dni roboczych.
- W tym: wspólny projekt drzewa pod skalę, mapa normalizacji rozmiarów, reguły pod Twoją wtyczkę, walidacja na próbce.

**Etap 2 — pełna migracja (75k) + konsolidacja termów:**
- 40–80 h → **3600–7200 PLN**, 1–2 tygodnie. Zależy od liczby termów do scalenia i tego, czy stare warianty/zamówienia muszą zostać.

**Uzasadnienie (3 zdania):**
Przy 75k produktów drzewo kategorii to decyzja architektoniczna — `tax_query` i `wp_term_relationships` siadają przy tej skali, więc projekt trzeba robić pod wydajność od pierwszego szkicu. Rozmiar jako wariant wymaga **konsolidacji termów**, nie zmiany etykiet — WooCommerce dopasowuje warianty po slugach, więc „39,5”, „39 1/2” i „39-1-2” zostaną trzema osobnymi wariantami, mimo że będą wyglądać identycznie. Twoja wtyczka jest OK jako narzędzie wykonawcze — brakuje jej reguł, i to jest główna wartość Etapu 1.

## Czego brakuje w zleceniu

1. **Czy rozmiar to jeden globalny atrybut (`pa_rozmiar`), czy osobny per typ produktu** (obuwie / odzież / dziecięce)? Obok EU pojawiają się US/UK?
2. **Skąd pochodzą dane produktów** — feed, import, ręcznie? Jeśli feed, normalizację trzeba wpiąć w import, żeby problem nie wrócił.

Odpowiedz na te dwa, dopnę zakres i podam sztywną kwotę za Etap 1.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: kwot nie zmieniam, bo 8–12 h na projekt drzewa + reguły + walidację na próbce przy 75k produktów i 40–80 h na masową migrację z konsolidacją termów to realne widełki, nie zawyżenie — mniej znaczyłoby albo „drzewo na kolanie", albo migrację bez zabezpieczenia wariantów. Ale przyznaję wprost: **budżet 500 PLN nie pokrywa nawet Etapu 1** (500 PLN = 5,5 h), więc moja poprzednia oferta była miękka — powinienem był to powiedzieć jednym zdaniem, zamiast zostawiać klientowi samodzielne wyciągnięcie wniosku. Jedno założenie było na wyrost: „wtyczka klienta jest OK jako narzędzie wykonawcze" — klient napisał tylko, że jest niedoskonała, nie wiemy, czy w ogóle się nada do reguł, więc to warto zaznaczyć jako warunek, nie fakt. Reszta (mechanizm slugów, degradacja `tax_query`, brak indeksu na `wp_term_relationships`) trzyma się źródeł i nie dopisałem tam nic na siłę.

=== DeepSeek-C — RUNDA 1 ===
**Nie da się tego zrobić za 500 PLN — nawet sam etap doradczy jest na granicy.**

**Widełki:**

| Etap | Zakres | Kwota | Czas |
|---|---|---|---|
| 1. Projekt drzewa + reguły | warsztat, dokument z drzewem, reguły przypisania, mapa normalizacji rozmiaru, walidacja na próbce 500–1000 produktów | **900–1200 zł** | 2–3 dni |
| 2. Wykonanie masowe | przypisanie ~75k produktów, konsolidacja termów rozmiaru (scalenie slugów, nie etykiet) | **3500–7000 zł** | 5–10 dni roboczych, po audycie danych |

**Uzasadnienie (3 zdania):**
500 PLN to ~5,5h przy mojej stawce — nie pokrywa nawet warsztatu + reguł + walidacji na próbce. Kluczowa mina: WooCommerce dopasowuje warianty po **slugach termów**, nie po etykietach — samo przemalowanie „39 1/2" na „39,5" zostawi trzy osobne warianty w bazie, więc trzeba scalić termy. Przy 75k produktów drzewo kategorii to decyzja architektoniczna (wydajność `tax_query` i `wp_term_relationships`), nie kosmetyka — dlatego etap 2 wyceniam po audycie, a nie z góry.

**Czego brakuje w zleceniu (2 pytania, które zmieniają wycenę):**
1. Czy rozmiar to **jeden globalny atrybut** (`pa_rozmiar`) na wszystkich produktach, czy osobny per typ (obuwie / odzież / dziecięce)? Obok EU są US/UK?
2. Skąd pochodzą dane produktów — **feed dostawcy / import / ręcznie**? Jeśli feed, normalizacja musi być wpięta w import, inaczej problem wróci.

Jeśli budżet 500 PLN jest sztywny — mogę w tej kwocie zrobić **wyłącznie warsztat + dokument z drzewem i regułami** (bez walidacji na próbce i bez wykonania). Reszta osobno.

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Szczerze: etap 1 (900–1200 zł) jest OK — to realne 10–13h na warsztat, dokument drzewa, reguły i walidację na próbce. Etap 2 zaniżyłem po stronie dolnej — 3500 zł to ~39h na 75k produktów, konsolidację termów rozmiaru i weryfikację edge-case'ów; przy tej skali, bez znajomości struktury bazy i tego, czy trzeba zachować stare warianty/zamówienia, **bezpieczniejsza dolna granica to 5000 zł, górna 8000–9000 zł**. Nie zgaduję już nic na siłę — widełki etapu 2 zostają „po audycie”, ale zawężam je do 5000–9000 zł, żeby nie obiecywać ceny, której nie dowiozę. Reszta wyceny i dwa pytania do klienta bez zmian.

=== DeepSeek-D — RUNDA 1 ===
**Kwota:**
- **Etap 1 – w budżecie: 500 zł** (konsultacja + projekt drzewa kategorii + reguły normalizacji rozmiaru + walidacja na próbce 500–1000 produktów).
- **Etap 2 – po danych: 2000–4500 zł** (masowe przypisanie 75k produktów + konsolidacja termów rozmiaru z zachowaniem wariantów).

**Czas:**
- Etap 1: **2–3 dni**.
- Etap 2: **5–10 dni roboczych** (zależnie od liczby termów i stanu bazy).

**Uzasadnienie:**
500 zł to jedna praca, a zlecenie zawiera trzy: projekt drzewa, migrację 75k produktów i konsolidację rozmiarów — dlatego w budżecie robię plan i próbkę, a etap masowy wyceniam osobno po zobaczeniu danych. Rozmiar w WooCommerce dopasowuje się po **slugach termów, nie po etykietach** — sama zmiana nazwy na „39,5” zostawi Ci nadal trzy osobne warianty, więc trzeba scalać termy, a nie przemalowywać labelki. Przy 75k produktów drzewo to też decyzja wydajnościowa (zapytania `tax_query` i tabela `wp_term_relationships` sypią się przy dużych kategoriach), więc projektuję je od początku pod skalę.

**Czego brakuje w zleceniu:**
1. Czy rozmiar to jeden globalny atrybut (`pa_rozmiar`) na wszystkich produktach, czy osobny per typ (obuwie / odzież / dziecięce) — i czy obok EU są US/UK?
2. Skąd pochodzą dane produktów: feed dostawcy, import, ręcznie? (Jeśli z feedu, normalizacja musi być wpięta w import, inaczej problem wróci.)
3. Ile masz obecnie kategorii/termów i czy stare URL-e kategorii mają wartość SEO (przekierowania 301)?

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Wycena jest uczciwa, ale dopisek „Etap 2: 2000–4500 zł” jest za szeroki i częściowo zgadywany — nie widziałem bazy, liczby termów ani tego, czy warianty muszą przetrwać w historii zamówień, więc dolna widełka może być równie dobrze 1500, jak i 6000 zł. Etap 1 za 500 zł jest OK tylko jako płatna diagnoza z próbką 500–1000 produktów; jeśli klient oczekuje, że te 500 zł pokryje też pełne drzewo i wykonanie na 75k, to nie jest już konflikt zakresu, a po prostu strata — wtedy lepiej powiedzieć wprost, że za 500 zł robię wyłącznie projekt + reguły + walidację, a reszta to osobna wycena. Nie zgadywałem mechanizmu slugów ani wydajności `tax_query` — to potwierdzone. Zgadywałem natomiast, że „39,5 EUR” pochodzi z feedu i że rozmiar jest globalny; oba zostają jako pytania, nie założenia w ofercie. Korekta: zostawiam 500 zł na etap 1 i piszę w ofercie, że etap 2 startuje od ~2500 zł i zamyka się dopiero po audycie termów, bo bez tego każda kwota to wróżenie.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 5000,
  "kwota_gorna": 10000,
  "definitywna": false,
  "od_czego_zaleza": [
    "potwierdzenia, czy rozmiar jest jednym globalnym atrybutem, czy osobnym per typ produktu (obuwie/odzież/dziecięce, EU/US/UK)",
    "źródła danych produktów (feed/import/ręcznie) i konieczności wpięcia normalizacji w import",
    "liczby i głębokości istniejących kategorii oraz termów, a także stanu wydajności bazy (tax_query, wp_term_relationships, indeksy)",
    "zakresu etapu masowego: czy trzeba zachować historyczne warianty/zamówienia i stare URL-e kategorii",
    "rzeczywistej przydatności wtyczki klienta do wykonania reguł przypisania i normalizacji"
  ],
  "dni_od": 10,
  "dni_do": 18,
  "uzasadnienie": "Modele zgodnie potwierdzają, że budżet 500 PLN nie pokrywa całości: to co najmniej trzy prace — projekt drzewa, migracja ok. 75 tys. produktów i konsolidacja termów rozmiaru. Zbieżność dotyczy też min: WooCommerce dopasowuje warianty po slugach termów, nie po etykietach, a przy 75 tys. produktów drzewo kategorii jest decyzją wydajnościową, nie kosmetyczną. Rozbieżność dotyczy głównie etapu masowego: DeepSeek-D zaniżył go do 2000–4500 PLN, podczas gdy B i C oscylują wokół 3600–9000 PLN za sam etap 2, a A dochodzi do 12600 PLN za całość. Finalne widełki 5000–10000 PLN są kompromisem dla pełnego zakresu; przy sztywnym budżecie 500 PLN realny jest wyłącznie płatny etap diagnostyczny: projekt drzewa, reguły i walidacja na próbce."
}

=== FINALNA WYCENA ===
5000-10000 zl netto | 10-18 dni | WIDELKI
Od czego zalezy: potwierdzenia, czy rozmiar jest jednym globalnym atrybutem, czy osobnym per typ produktu (obuwie/odzież/dziecięce, EU/US/UK), źródła danych produktów (feed/import/ręcznie) i konieczności wpięcia normalizacji w import, liczby i głębokości istniejących kategorii oraz termów, a także stanu wydajności bazy (tax_query, wp_term_relationships, indeksy), zakresu etapu masowego: czy trzeba zachować historyczne warianty/zamówienia i stare URL-e kategorii, rzeczywistej przydatności wtyczki klienta do wykonania reguł przypisania i normalizacji
Uzasadnienie rozjemcy: Modele zgodnie potwierdzają, że budżet 500 PLN nie pokrywa całości: to co najmniej trzy prace — projekt drzewa, migracja ok. 75 tys. produktów i konsolidacja termów rozmiaru. Zbieżność dotyczy też min: WooCommerce dopasowuje warianty po slugach termów, nie po etykietach, a przy 75 tys. produktów drzewo kategorii jest decyzją wydajnościową, nie kosmetyczną. Rozbieżność dotyczy głównie etapu masowego: DeepSeek-D zaniżył go do 2000–4500 PLN, podczas gdy B i C oscylują wokół 3600–9000 PLN za sam etap 2, a A dochodzi do 12600 PLN za całość. Finalne widełki 5000–10000 PLN są kompromisem dla pełnego zakresu; przy sztywnym budżecie 500 PLN realny jest wyłącznie płatny etap diagnostyczny: projekt drzewa, reguły i walidacja na próbce.
