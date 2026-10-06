=== GLOSY 4 MODELI (DeepSeek x4, po 2 rundy) ===

=== DeepSeek-A — RUNDA 1 ===
## Wycena wstępna

**Kwota:** 12 000 – 20 000 zł netto (widełki)
**Czas:** 4–6 tygodni roboczych (start: do 3–5 dni od potwierdzenia zgody admina M365)

**Uzasadnienie:** To nie jest „prosty CRM” — kluczowe wymaganie (agregacja maili ze wszystkich skrzynek do jednego widoku klienta) wymaga Azure Function z Microsoft Graph (uprawnienia aplikacyjne Mail.Read), Application Access Policy w Exchange Online i przemyślanej logiki dopasowania maili do klienta. Do tego Power Apps + Dataverse (logowanie, role, karta klienta, historia, traceability) oraz warstwa automatyzacji. Widełki są szerokie, bo brakuje danych o skali i licencjach — przy małej skali zejdę niżej, przy dużej lub braku licencji pójdę wyżej.

---

**Czego brakuje, żeby wycenić celniej (4 pytania):**

1. **Jak system ma rozpoznawać, że dany mail należy do danego klienta** — po domenie, adresach kontaktowych, ręcznie? To decyzja projektowa, od której zależy cała automatyzacja.
2. **Ile jest skrzynek pracowników i jaki miesięczny wolumen maili** do agregacji? Od tego zależy architektura (kolejkowanie, limity Graph, koszt Azure).
3. **Czy macie już licencje Power Apps/Dataverse i subskrypcję Azure**, czy mam je uwzględnić w kosztach? Dataverse wymaga licencji na użytkownika.
4. **Czy jest zgoda administratora M365** na dostęp aplikacji do skrzynek? Bez tego agregacja nie ruszy — to warunek startu, nie formalność.

Uwaga techniczna: Graph Mail.Read domyślnie daje dostęp do **wszystkich** skrzynek w dzierżawie — trzeba to ograniczyć polityką dostępu aplikacji, inaczej ryzyko RODO/bezpieczeństwa. Zakładam, że to akceptujecie i zapewniacie zgodę admina. Jeśli planujecie inne podejście, dostroję wycenę.

=== DeepSeek-A — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 12–20k netto przy 90 zł/h to 133–222 h, czyli realnie 4–6 tygodni pracy solo — na CRM z Dataverse, logiką ról, kartą klienta, traceability i agregacją maili przez Graph to jest **dolna granica sensu**, a nie zawyżenie; 12k (133 h) jest ryzykowne, bo samo dopasowanie maili do klienta + Application Access Policy + obsługa błędów Graph potrafi zjeść pół budżetu. Nie zgadłem min o Graph Mail.Read ani o zgodzie admina — to fakty z Microsoft Learn i realny warunek startu, więc zostają. Czego nie dopisałem, a warto: załączniki, retencja/RODO, obsługa aliasów i współdzielonych skrzynek oraz utrzymanie po wdrożeniu — to typowe „ukryte” godziny, które przy „na już” i budżecie do negocjacji trzeba wycenić osobno. Korekta: podniósłbym dolną granicę do **14 000 zł netto** (ok. 155 h), górną zostawił 20 000 zł, i wyraźnie napisał, że 4–6 tygodni to przy założeniu szybkiej zgody admina i jasnych reguł dopasowania maili.

=== DeepSeek-B — RUNDA 1 ===
**Wycena: 12 000 – 20 000 zł** (przy 90 zł/h to ok. 130–220 h)
**Czas: 4–6 tygodni** od startu (po uzyskaniu zgód i licencji)
**Start: możliwy od zaraz**, warunkowo — patrz pytania niżej.

Uzasadnienie: to nie jest „prosty CRM" — sam formularz + karta klienta to kilka dni, ale kluczowa funkcja (agregacja maili ze wszystkich skrzynek przez MS Graph z uprawnieniami aplikacyjnymi) to najdroższy element: wymaga Azure Function/Logic Apps, polityki dostępu aplikacji w Exchange Online i decyzji projektowej „jak przypisać mail do klienta". Widełki zależą od liczby skrzynek, wolumenu maili i logiki dopasowania — bez tych danych nie zejdę niżej ani nie podniosę powyżej.

**Czego brakuje / muszę wiedzieć przed startem:**

1. **Jak system ma rozpoznać, że mail należy do danego klienta** — po domenie nadawcy, liście adresów kontaktowych, temacie, ręcznie? To determinuje architekturę dopasowania i wycenę.
2. **Ile skrzynek pracowników i jaki miesięczny wolumen maili** do agregacji? Od tego zależy, czy wystarczy proste odpytywanie Graph, czy trzeba kolejek i subskrypcji zmian.
3. **Czy macie już licencje Power Apps/Dataverse i subskrypcję Azure**, czy mam je uwzględnić? Dataverse wymaga płatnej licencji per użytkownik — to koszt po Waszej stronie, nie w mojej wycenie.
4. **Czy jest zgoda admina M365** na uprawnienia aplikacyjne Graph (Mail.Read) i gotowość na skonfigurowanie Application Access Policy ograniczającej dostęp do wybranych skrzynek? Bez tego agregacja nie ruszy, a samo uprawnienie Mail.Read daje domyślnie dostęp do całej poczty w dzierżawie — kwestia RODO.

Odpowiedz na te 4 punkty, a zawężę widełki do konkretnej kwoty i podam datę startu.

=== DeepSeek-B — RUNDA 2 (autokrytyka) ===
Szczerze: dolna granica 12 000 zł jest zaniżona — przy 130 h zakładam, że dopasowanie maili będzie banalne (np. tylko po domenie) i że nie ma załączników, wątków współdzielonych ani deduplikacji, a to rzadko się zdarza w praktyce. Górna granica 20 000 zł jest obroniona, ale tylko jeśli zakres faktycznie zamknie się w kartach klientów + agregacji maili bez dodatków (Teams, kalendarz, RODO-retention, import starych maili). Nie zgadywałem na siłę — mina o Graph Mail.Read i zgodzie admina jest realna i kluczowa — ale świadomie zszedłem z widełkami w dół, żeby nie odstraszyć na starcie, i to było naciągane. Koryguję: **14 000 – 24 000 zł** (ok. 155–265 h), z zastrzeżeniem, że po odpowiedziach na 4 pytania zawężę do konkretu i wtedy albo zejdę, albo podniosę — zależnie od wolumenu i logiki dopasowania.

=== DeepSeek-C — RUNDA 1 ===
**Wycena:** 12 000 – 16 000 zł (widełki, zależne od skali i licencji)  
**Czas:** 18–25 dni roboczych  
**Uzasadnienie:** Wycena obejmuje Power Apps z Dataverse, role, kartę klienta oraz Azure Function z Microsoft Graph do agregacji maili. Kluczowe ryzyko to dostęp do wszystkich skrzynek – bez Application Access Policy i zgody admina M365 projekt nie ruszy. Brak danych o skali i licencjach uniemożliwia podanie kwoty ostatecznej.

**Czego brakuje:**
1. Jak system ma przypisywać mail do klienta – po domenie, adresie, temacie, ręcznie?
2. Ile jest skrzynek pracowników i jaki miesięczny wolumen maili?
3. Czy macie już licencje Power Apps/Dataverse i subskrypcję Azure?
4. Czy jest zgoda administratora M365 na dostęp aplikacji do skrzynek?

=== DeepSeek-C — RUNDA 2 (autokrytyka) ===
Wycena 12–16 tys. zł przy 90 zł/h to 133–178 godzin — na Power Apps z Dataverse, Azure Function z Graph, polityką dostępu i traceability to raczej dolna granica zdrowego zakresu, a nie kwota „za wysoko". Nie zgadłem niczego w architekturze — Graph z uprawnieniami aplikacyjnymi to jedyna sensowna droga przy „wszystkich skrzynkach pracowników", a Application Access Policy i zgoda admina to warunki, nie straszaki. Nie dopisałem na siłę konektora Outlook ani limitów Graph, bo klient wprost napisał „MS Graph", a wolumenu nie znam — słusznie zostawiłem to w pytaniach, nie w wycenie. Jeśli okaże się, że skrzynek jest kilkadziesiąt albo dochodzi RODO/retention, kwota powinna pójść w górę — nie w dół. Na teraz widełki są uczciwe, ale gdybym miał je zawęzić bez odpowiedzi na 4 pytania, zaniżyłbym ryzyko.

=== DeepSeek-D — RUNDA 1 ===
**Wycena: 12 000 – 18 000 zł netto** (ok. 135–200 h × 90 zł/h)
**Czas: 5–7 tygodni** od startu (przy założeniu dostępu do środowiska i zgody admina)
**Start: możliwy od zaraz**, po potwierdzeniu zakresu i licencji

**Uzasadnienie (3 zdania):**
Zakres jest realny (Power Apps + Dataverse + integracja z Graph), ale kluczowy element — automatyczna agregacja maili ze wszystkich skrzynek — wymaga niestandardowego rozwiązania (Azure Function + uprawnienia aplikacyjne Graph), bo standardowy konektor Outlook tego nie zrobi. Bez danych o skali i sposobie dopasowania maili do klienta wycena jest widełkowa — im więcej skrzynek i bardziej złożone dopasowanie, tym bliżej górnej granicy. „Na już” jest wykonalne tylko warunkowo: start blokuje zgoda administratora M365 i licencje Dataverse.

**Czego brakuje w zleceniu (4 pytania):**
1. **Jak system ma przypisać mail do klienta** — po domenie, adresach kontaktowych, temacie, ręcznie? Od tego zależy architektura i wycena.
2. **Ile skrzynek pracowników i jaki miesięczny wolumen maili?** Od tego zależy kolejkowanie, limity Graph i koszt Azure.
3. **Czy macie już licencje Power Apps/Dataverse i subskrypcję Azure**, czy mam je uwzględnić? Dataverse wymaga licencji na użytkownika.
4. **Czy jest zgoda administratora M365** na dostęp aplikacji do skrzynek (Application Access Policy)? Bez tego agregacja nie ruszy — to warunek startu, nie formalność.

Zakładam, że agregacja maili idzie przez Graph z uprawnieniami aplikacyjnymi, ograniczonymi polityką dostępu do wybranych skrzynek. Jeśli planujecie inaczej — dostroję wycenę.

=== DeepSeek-D — RUNDA 2 (autokrytyka) ===
Szczerze: widełki 12–18 tys. są obronne, ale dolna granica jest ryzykowna — „prosty CRM” z pełną agregacją maili ze wszystkich skrzynek, traceability i historią wątków to nie jest 135 h, jeśli dopasowanie maili do klienta okaże się nietrywialne (domeny, aliasy, skrzynki współdzielone). Nie zgadywałem przy konektorze ani limitach Graph — świadomie, bo klient sam wskazał Graph, a wolumenu nie znamy — więc nie widzę tu dociągania na siłę. Skorygowałbym raczej w górę: realniej **15 000 – 22 000 zł netto** (ok. 165–245 h), z zastrzeżeniem, że to nadal widełki do zawężenia po odpowiedziach na 4 pytania. Gdyby okazało się, że skrzynek jest kilkanaście, a dopasowanie maili wymaga reguł plus ręcznej weryfikacji — górna granica może pęknąć.

=== WERDYKT ROZJEMCY ===
{
  "kwota_dolna": 14000,
  "kwota_gorna": 22000,
  "definitywna": false,
  "od_czego_zaleza": [
    "liczba skrzynek pracowników i miesięczny wolumen maili do agregacji",
    "sposób dopasowania maili do klienta: domena, adresy kontaktowe, temat, reguły ręczne",
    "posiadane licencje Power Apps/Dataverse oraz subskrypcja Azure",
    "zgoda administratora M365 i skonfigurowanie Application Access Policy dla Graph",
    "zakres dodatkowy: załączniki, aliasy, skrzynki współdzielone, RODO/retention, import historii, utrzymanie"
  ],
  "dni_od": 25,
  "dni_do": 35,
  "uzasadnienie": "Finalne widełki 14 000–22 000 zł netto są wyceną niedefinitywną, bo brakuje danych o skali i logice dopasowania maili. Modele zgodnie wskazują, że główny koszt to agregacja maili przez Microsoft Graph z uprawnieniami aplikacyjnymi, zgoda admina M365 i Application Access Policy, a nie sam formularz CRM. Po autokrytyce zbieżność jest przy dolnej granicy 14–15 tys. zł i górnej 20–24 tys. zł; DeepSeek-C pozostaje niżej, ale sam zaznacza ryzyko zaniżenia przy większej skali. Rozbieżność wynika głównie z nieznanej liczby skrzynek, wolumenu maili, licencji oraz zakresu dodatkowego, dlatego po odpowiedziach na pytania widełki należy zawęzić."
}

=== FINALNA WYCENA ===
14000-22000 zl netto | 25-35 dni | WIDELKI
Od czego zalezy: liczba skrzynek pracowników i miesięczny wolumen maili do agregacji, sposób dopasowania maili do klienta: domena, adresy kontaktowe, temat, reguły ręczne, posiadane licencje Power Apps/Dataverse oraz subskrypcja Azure, zgoda administratora M365 i skonfigurowanie Application Access Policy dla Graph, zakres dodatkowy: załączniki, aliasy, skrzynki współdzielone, RODO/retention, import historii, utrzymanie
Uzasadnienie rozjemcy: Finalne widełki 14 000–22 000 zł netto są wyceną niedefinitywną, bo brakuje danych o skali i logice dopasowania maili. Modele zgodnie wskazują, że główny koszt to agregacja maili przez Microsoft Graph z uprawnieniami aplikacyjnymi, zgoda admina M365 i Application Access Policy, a nie sam formularz CRM. Po autokrytyce zbieżność jest przy dolnej granicy 14–15 tys. zł i górnej 20–24 tys. zł; DeepSeek-C pozostaje niżej, ale sam zaznacza ryzyko zaniżenia przy większej skali. Rozbieżność wynika głównie z nieznanej liczby skrzynek, wolumenu maili, licencji oraz zakresu dodatkowego, dlatego po odpowiedziach na pytania widełki należy zawęzić.
