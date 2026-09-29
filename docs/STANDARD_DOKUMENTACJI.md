# STANDARD DOKUMENTACJI — useme_core
**STATUS: AKTUALNE (zasady)** | Wdrożone 2026-09-29.

## Cel
AI wchodzi w projekt i od razu wie, co jest prawdą. Dokumentacja nie kłamie i nie powtarza tego samego w wielu miejscach.

## 5 żelaznych zasad
1. **Status/stan = kod i dane.** Liczby (statusy, liczniki "wysłano X", "Y testów") NIE są zapisywane w plikach .md. Sprawdza się je komendą (patrz README w docs).
2. **Kod = twarda prawda liczb.** Progi, stawki, limity żyją w kod/config.py i kod/wycena_kalkulator.py. Dokumentacja cytuje z dopiskiem "wartość w config.py".
3. **Każdy plik ma nagłówek:** STATUS: AKTUALNE / PLAN / HISTORYCZNE.
4. **Przeszłość trafia do docs/historia/** i jest zamrożona (opisuje DLACZEGO, nie liczniki).
5. **Jeden temat = jeden plik.** Zero duplikatów folderów.

## Zasada PRISTINE (dla plików badawczych)
- Plik badawczy = surowe dane z jawnym N + hipoteza + pomysł.
- NIE zapisujemy "gotowych rozwiązań" ani "wdrożono X" (od tego jest historia kodu).
- Każdy wniosek z małej próby musi jawnie podawać N (np. "N=11, wstępne").
- Rozdzielać: DANE, HIPOTEZA, POMYSŁ — nie mieszać w jednym akapicie.

## Struktura docs/
| Folder | Rola | Żywy? |
|---|---|---|
| README.md | Wejście + jak sprawdzić stan komendami | tak |
| architektura/ | Jak działa silnik | tak |
| referencje/ | Trwała wiedza o platformie i operacjach | tak |
| plany/ | Pomysły i hipotezy (STATUS: PLAN) | tak |
| historia/ | Zamrożona przeszłość | nie |

## Struktura badania/
- Tylko dane i raporty. Każdy raport z nagłówkiem: N, charakter (fakt/hipoteza/poszlaka), data.
- Jeden plik LICZNIKI.md definiuje, czym są różne N używane w badaniach.