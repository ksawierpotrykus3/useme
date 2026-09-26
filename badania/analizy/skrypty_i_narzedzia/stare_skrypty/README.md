# Skrypty analityczne — narzędzia do utrzymania

> 27 skryptów Python do analizy danych z badań. To **kod do utrzymania**, nie jednorazowe śmieci.
> Uruchamiane ponownie po zebraniu nowych danych. Wymagają ścieżek względnych od roota `useme_core/`.

## Uwaga o ścieżkach

Skrypty używają ścieżek względnych typu `badania/rynek/...`, więc **uruchamiaj je z katalogu `useme_core/`**, nie z tego folderu.

## Grupy skryptów

### Analiza bazy zamkniętych ofert (406)
| Skrypt | Rola |
|---|---|
| `analiza_406_statystyka.py` | Statystyki z bazy 406 ofert |
| `analiza_gleboka_406.py` | Głęboka analiza 406 ofert |
| `analiza_przegranych.py` | Analiza przegranych ofert |
| `cluster_369.py` | Klastrowanie 369 zaakceptowanych zleceń |
| `cluster_accepted.py` | Klastrowanie zaakceptowanych |
| `wybierz_prawdziwe_wzorce.py` | Wybór wzorców z bazy |

### Analiza rynku i kategorii
| Skrypt | Rola |
|---|---|
| `analiza_snapshot_live.py` | Analiza live snapshot rynku |
| `analiza_trendow_w_czasie.py` | Trendy czasowe (czyta `rynek/archiwum/`) |
| `badanie_kategorii.py` | Badanie kategorii (zapisuje `rynek/kategorie_useme.json`) |
| `pobierz_analiza_kategorii_live.py` | Pobiera analizę kategorii live |
| `analiza_potrzeb_wystawienia.py` | Analiza potrzebnych zleceń do wystawienia |

### Benchmark #144890
| Skrypt | Rola |
|---|---|
| `odpal_benchmark_144890.py` | Uruchamia benchmark (czyta `../PROMPT_OCENA_KLIENTA.md`) |
| `generuj_nasza_oferte_144890.py` | Generuje naszą ofertę do benchmarku |
| `analizuj_pobrane_oferty_144890.py` | Analizuje pobrane oferty |
| `pobierz_aktualne_wiadomosci_144890.py` | Pobiera wiadomości z wątku |

### Parsery i scrapery ofert
| Skrypt | Rola |
|---|---|
| `parsuj_oferty_test.py` | Test parsera ofert |
| `test_dokladny_parser.py` | Dokładny parser |
| `test_parse_cards.py` | Test parsowania kart ofert |
| `test_job_offers_source.py` | Test źródła ofert |
| `zbadaj_id_ofert.py`, `zbadaj_karty_ofert.py`, `zbadaj_linki_i_hooki.py`, `zbadaj_tekst_caly.py` | Narzędzia diagnostyczne do HTML |
| `zrzut_wzorcow_1do1.py` | Zrzut wzorców 1:1 |

### Audyt i jakość
| Skrypt | Rola |
|---|---|
| `audyt_jakosci_plikow.py` | Audyt jakości plików w `katalog_ofert/` |
| `pokaz_perelki.py` | Pokazuje wyselekcjonowane perełki |
| `zapisz_podglad.py` | Zapisuje podgląd tekstów |
| `zapisz_ciasteczka_zleceniodawca.py` | Zapisuje cookies zleceniodawcy |

## Checkpointy

Folder `checkpointy/` — stany pośrednie pobierania (wygrane, przegrane, zamknięte, oferty 144890, cache detali). Pozwalają wznowić pracę bez ponownego scrapowania.