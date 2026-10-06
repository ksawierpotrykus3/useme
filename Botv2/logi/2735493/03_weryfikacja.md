```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (budowa pipeline'u ETL + struktura bazy) z możliwym retainerem na aktualizację. Nie rekrutacja — "poszukuję freelancera" to standardowe słownictwo Useme.
INTENCJA: mieszane — projektowanie = doradcze, budowa/wdrożenie = wykonawcze
DECYDENT_I_BOL: osoba fizyczna lub mała firma ("pomóż mi"). Ból: ręczne pozyskiwanie i czyszczenie danych firm zjada czas; chce procesu, który sam ciągnie z rejestrów i porządkuje. Hipoteza "poprzednie próby się sypały" (z frazy "bez błędu") — ZGADUJĘ, zostaje u mnie, nie wchodzi do oferty. Domysł "pod sprzedaż/outreach" — też nie wchodzi.
WYKONALNE: TAK. ETL z rejestrów publicznych (KRS, CEIDG, GUS BIR1/REGON) + dedup po NIP + standaryzacja pól → staging → target. Zależne od skali i źródła danych wejściowych (NIP/KRS/nazwa).
POLE_DO_POPISU: JEST, ale wąskie. Realne pole: (1) PKD 2025 obowiązuje od 1.01.2025 z przejściowym do 31.12.2026 — zakładam domyślnie 2025 i dorabiam słownik, jeśli dane są w 2007; (2) krajobraz rejestrów — co darmowe, gdzie są wąskie gardła (GUS BIR1 rejestracja nie-self-serve; CEIDG max 25 wyników/żądanie); (3) propozycja architektury (dedup po NIP, staging, batch nocny). Reszta researchu zostaje dla nas.
SCIEZKA_MERYTORYKI: A (klient wprost prosi o automatyzację i wzbogacanie). B — NIE. PKD bez wersji to nie mina, to normalne słownictwo; nie mam dowodu, że klient ma dane w 2007. KRS-bez-NIP-lookup też nie wchodzi, bo nie wiem, czy jego input to NIP-y.
MINY_I_CIEKAWOSTKI: puste.
ODMOWA: puste. Żadna z okazji 1–6 nie zachodzi — brak nazwy systemu klienta, brak liczby, brak API do zakwestionowania. Wąskie gardła GUS/CEIDG to sprawa architektury i wyceny, nie odmowy.
PYTANIA (3, TYP 1 — tylko to, czego nie da się rozstrzygnąć bez klienta):
1. Skala — ile firm docelowo w bazie i jak często aktualizacja? Od tego zależy architektura (sync ciągły vs batch nocny) i czy limity CEIDG (25 wyników/żądanie) są wąskim gardłem.
2. Źródła wejściowe — jak wygląda punkt startu: lista NIP-ów, KRS-ów, nazw firm, czy zbieramy od zera? Od tego zależy cały przepływ (KRS API nie szuka po NIP — pośrednictwo REGON bywa konieczne).
3. Target — gdzie ma trafiać gotowa baza: plik/eksport, CRM, panel www? Determinuje format wyjściowy i czy w zakresie jest warstwa wizualna.
(TYP 2 — propozycje, NIE pytania: PKD domyślnie 2025 z dorobieniem słownika 2007↔2025; dedup po NIP; staging przed target; stack dobrany do wolumenu po punkcie 1.)
CO_ZLECENIE_MOWI: budowa bazy B2B firm, filtrowanie po PKD i parametrach biznesowych, automatyczne wzbogacanie z rejestrów/API, czyszczenie (mapowanie pól, dedup, standaryzacja). Budżet: do negocjacji.
CZEGO_NIE_MOWI: skala, konkretne rejestry/źródła, wersja PKD, system docelowy, format danych wejściowych, technologia, czy dane już istnieją, konkretny budżet.
GRANICA_CIECIA: krótka odpowiedź. Brief 1 akapit, zero konkretów → 3 pytania + krótki szkic podejścia + 3 propozycje domyślne. Bez rozpisywania stacku bez danych o skali. Bez PKD jako "miny".
RESEARCH_POTRZEBNY: TAK, lekki — potwierdzony: PKD 2025 obowiązuje od 1.01.2025, przejściowy do 31.12.2026; GUS BIR1 rejestracja nie-self-serve (mail, IP, kilka dni); CEIDG 25 wyników/żądanie + limity czasowe; KRS API tylko po numerze KRS (brak lookup po NIP). Research NIE wchodzi do oferty jako mina — wchodzi jako uzasadnienie propozycji (domyślne PKD 2025) i jako wiedza dla wyceny (wąskie gardła).

DECYZJE:
- DOPISAĆ: 3 propozycje TYP 2 (PKD 2025 domyślnie + słownik; dedup po NIP; staging→target) + krótki szkic pipeline'u.
- ODPOWIEDZIEĆ: zakres rozumiem jako ETL z rejestrów → dedup → standaryzacja → target; chcę to wycenić po 3 odpowiedziach.
- DOPYTAĆ: skala (1), źródła wejściowe (2), target (3).
- WYWALIĆ: PKD jako minę (brak dowodu), hipotezę o "poprzednich próbach się sypały" (zgadywanie), KRS-bez-NIP jako minę (brak dowodu, że input to NIP-y).
- ZAMIENIĆ: czwarte pytanie o PKD → na propozycję domyślną z zastrzeżeniem.
```