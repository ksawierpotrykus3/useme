Zakładam, że agregację maili robimy przez Microsoft Graph z uprawnieniami aplikacyjnymi, bo tylko tak da się czytać skrzynki bez logowania użytkownika. Warto wiedzieć zawczasu, że samo uprawnienie Mail.Read daje domyślnie dostęp do całej poczty w dzierżawie. Trzeba je ograniczyć polityką dostępu aplikacji w Exchange Online do wybranych skrzynek i mieć zgodę administratora M365. Bez tej zgody agregacja nie ruszy, a to wpływa na datę startu, nie na samą kwotę.

Druga rzecz, którą widzę po treści zlecenia. Pełna historia wątków i traceability na pracowników to nie jest prosty formularz. Najwięcej pracy siedzi w tym, żeby system sam wiedział, który mail należy do którego klienta, a to decyzja projektowa, nie oczywistość.

Kwota to od 14 000 do 22 000 zł netto, przy około pięciu do siedmiu tygodniach. Widełki zależą od liczby skrzynek i miesięcznego wolumenu maili, od sposobu dopasowania maili do klienta, od tego czy macie już licencje Power Apps i Dataverse oraz subskrypcję Azure, a także od tego, czy wchodzą załączniki, aliasy i skrzynki współdzielone. Im mniej z tych rzeczy dochodzi, tym bliżej dolnej granicy.

Żeby zawęzić to do konkretnej kwoty, potrzebuję czterech rzeczy. Po czym system ma rozpoznawać klienta w mailu, domena, adresy kontaktowe, temat, reguły ręczne. Ile jest skrzynek pracowników i jaki miesięczny wolumen maili. Czy licencje i Azure są po waszej stronie. I czy jest zgoda admina M365 na dostęp aplikacji do skrzynek.

Jak odpowiesz, zawężę kwotę i podam realną datę startu. Jeśli okaże się, że trzeba dopiero postawić politykę dostępu, zrobiłbym to osobno, ale najpierw ustalmy zakres.

Ksawier