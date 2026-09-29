# Indeks Badań, Turniejów i Benchmarków: Audyt 100 (`badania/audyt_100/`)

Katalog `badania/audyt_100/` gromadzi czyste raporty syntetyczne (Strefa 2) oraz ustrukturyzowane wyniki badań laboratoryjnych, ślepych testów i turniejów sędziowskich, na bazie których powstał i został zweryfikowany generator **Human Voice v6**.

> [!NOTE]
> Zgodnie z wyrokiem Izby Segregacji (Sprawa #13), surowe logi (`PELNE_LOGI_27_OFERT_RUNDA1_I_RUNDA2.md`, `task-*.log`) zostały przeniesione do `badania/_archiwum/logi/`, a skrypty wykonawcze zgrupowano w `badania/audyt_100/logi_i_skrypty/` oraz w stałym przyborniku [`kod/narzedzia_badawcze/`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/kod/narzedzia_badawcze/README.md).

---

## 📑 Spis Raportów Analitycznych (.md)

| Raport | Opis i Zakres Badania | Wynik / Werdykt |
| :--- | :--- | :--- |
| **[`RAPORT_NOWE_OFERTY_I_PV_144890_AKTUALIZACJA.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_NOWE_OFERTY_I_PV_144890_AKTUALIZACJA.md)** | **NOWY (28.09.2026):** Audyt AI ostatnich **16 ofert publicznych (`#2893397..#2896662`)** oraz **5 nowych wątków PV** po zamknięciu zlecenia `#144890` (stan końcowy: **101 ofert + 19 wątków PV = 112 wykonawców**). | Nasza oferta v6 utrzymuje **#1 miejsce (~95/100)**. Do Top 5 wchodzą `natalia-szczepanik` (#2895200, 92 pkt) i `tomaszmyszak` / cerbIT (#2896654, 90 pkt). |
| [`RAPORT_4_ROZNE_DOMENY_V6.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_4_ROZNE_DOMENY_V6.md) | Test elastyczności nowego generatora w 4 skrajnych domenach: 3D WebGL (#144092), BaseLinker (#144038), Notion VoIP (#143981) oraz przemysłowe CNC po angielsku (#144165). | Średnia ocena **86.3/100**, 100% decyzji „TAK na priv”, pełna adaptacja terminologii. |
| [`RAPORT_GEMINI_SEDZIOWIE.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_GEMINI_SEDZIOWIE.md) | Niezależny arbitraż modelu **Gemini 3.8 Flash** oceniający 6 kandydatów dla zlecenia #144890 (Nasza nowa v6, Antoni, Stara oferta, Konrad, Grzegorz, Dariusz). | **1. miejsce: Nasza Nowa v6 (91/100)**, 2. Antoni (88/100). |
| [`RAPORT_NIEZALEZNYCH_SEDZIOW_AI.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_NIEZALEZNYCH_SEDZIOW_AI.md) | Turniej sędziowski podwójnego sędziego: **DeepSeek-Chat** oraz **DeepSeek-Reasoner (R1)** na zleceniu #144890. | Jednogłośne odrzucenie pytań na priv bez wyceny; Nowa v6 na podium z Antonim. |
| [`RAPORT_ZAGRYWKI_JEZYK_PSYCHOLOGIA_100.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_ZAGRYWKI_JEZYK_PSYCHOLOGIA_100.md) | Głęboka dekonstrukcja psychologii, języka i taktyk rynkowych w oparciu o autentyczne oferty konkurencji i wiadomości PV. | Wyodrębnienie 7 kluczowych przewag rynkowych (architektura v6). |
| [`POROWNANIE_STARA_VS_NOWA_OFERTA_LUDZKA.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/POROWNANIE_STARA_VS_NOWA_OFERTA_LUDZKA.md) | Zestawienie bezpośrednie (side-by-side) starej formuły bota z nowym podejściem Human Voice v6. | Wykazanie eliminacji sztucznego żargonu i wdrożenie hooka darmowej próbki. |
| [`RAPORT_SLEPY_TEST_144890_Z_PV.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_SLEPY_TEST_144890_Z_PV.md) | Ślepy test 99 anonimowych kandydatów w realnym zleceniu fakturowym `#144890`. | Analiza zachowań decydentów wobec różnych długości i struktur ofert. |
| [`slepy_test_bez_ceny.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/slepy_test_bez_ceny.md) | Ślepa ewaluacja jakości czysto merytorycznej i językowej z usuniętymi kwotami i nazwiskami. | Potwierdzenie, że treść inżynierska v6 broni się bez względu na cenę. |
| [`RAPORT_META_AUDYTU_RED_TEAM_ARCHITEKT.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_META_AUDYTU_RED_TEAM_ARCHITEKT.md) | Bezwzględna krytyka Red-Team weryfikująca potencjalny overfitting promptów i luki integracyjne. | Wyznaczenie planu naprawczego dla uogólnienia bazy portfolio i dual-track. |
| [`RAPORT_META_AUDYTU_ZMIAN_I_DANYCH.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_META_AUDYTU_ZMIAN_I_DANYCH.md) | Statystyczny i merytoryczny audyt spójności wyników 27 ofert testowych. | Wskazanie konieczności re-testu wczesnych fal na zaktualizowanym generatorze. |
| [`RAPORT_RE_AUDYTU_PO_POPRAWKACH.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/RAPORT_RE_AUDYTU_PO_POPRAWKACH.md) | Ponowna ewaluacja ofert Fali 1 i Fali 2 po wdrożeniu poprawek architektonicznych. | Wzrost średniej ocen z 56/100 do **93.8/100**. |
| [`CHANGELOG_OD_POCZATKU_ROZMOWY.md`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/CHANGELOG_OD_POCZATKU_ROZMOWY.md) | Szczegółowa kronika krok po kroku: hipotezy, eksperymenty, zmiany kodu. | Pełna audytowalność procesu badawczego. |

---

## 📊 Zbiory Danych i Wyniki (.json)

- [`wyniki_audytu_nowych_16_ofert_5_pv_144890.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_audytu_nowych_16_ofert_5_pv_144890.json) — wyniki audytu AI dla 16 nowych ofert i 5 nowych wątków PV (#144890).
- [`audyt_100_wyniki_27_ofert.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/audyt_100_wyniki_27_ofert.json) — baza 27 ofert, punktacji Rundy 1 i Rundy 2 oraz szczegółowych uwag.
- [`wyniki_4_rozne_domeny_v6.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_4_rozne_domeny_v6.json) — wyniki ewaluacji dla WebGL 3D, BaseLinkera, Notion i CNC.
- [`wyniki_gemini_sedziowie.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_gemini_sedziowie.json) — surowy json z oceną Gemini 3.8 Flash.
- [`wyniki_niezaleznych_sedziow_ai.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_niezaleznych_sedziow_ai.json) — surowy json z ocenami DeepSeek-Chat i Reasoner.
- [`wyniki_audyt_po_poprawkach.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_audyt_po_poprawkach.json) — wyniki re-audytu wczesnych fal.
- [`wyniki_slepego_testu_144890_99_kandydatow.json`](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/audyt_100/wyniki_slepego_testu_144890_99_kandydatow.json) — anonimizowany zbiór 99 ofert rynkowych z pierwszej tury.
