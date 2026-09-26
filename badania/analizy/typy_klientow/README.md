# Strefa 2: Typologia i Psychologia Zleceniodawców Useme

Obszar gromadzi kompletną wiedzę behawioralną, psychologiczną i operacyjną o zleceniodawcach na platformie Useme, wywiedzioną z audytu **470 zleceń** (w tym 56 wygranych z pełnymi wątkami prywatnymi oraz 414 zamkniętych zleceń rynkowych).

---

## 1. Struktura Katalogu `typy_klientow/`

```
badania/analizy/typy_klientow/
├── README.md                                    # Niniejszy katalog główny
├── raport_falsyfikacji_i_weryfikacji_typow.md   # Bezwzględny audyt falsyfikacyjny (Red Team)
├── analiza_gleboka_typow_i_technologii.md       # Pogłębiona dekonstrukcja psychologiczna i analiza cross-tech
├── 02_kompendium_archetypow_klient_x_tech.md   # Kompendium przecięcia archetypów z technologiami
├── 02_matryca_2d_klient_x_tech.json            # Macierz 2D (klienci x technologie) w JSON
├── 03_nowa_gleboka_typologia_klientow.md        # Wstępna typologia 8 person
├── 03_nowa_gleboka_typologia_klientow.json      # Dane typologii w formacie maszynowym
├── filtr_phantom_leads.md                       # Filtr eliminujący fałszywe zapytania founderów bez budżetu
├── filtr_pulapki_ogloszen.md                    # Filtr niebezpiecznych ogłoszeń i pułapek prawnych
│
└── scenariusze/                                 # POGŁĘBIONE SCENARIUSZE ZROZUMIENIA CZŁOWIEKA (Zero if-else)
    ├── README.md                                # Katalog scenariuszy i wytyczne interpretacji dla AI
    ├── klient_01_tradycyjne_msp_erp_przemysl.md # Właściciel MŚP, Subiekt, Optima, WZ, KSeF, magazyn
    ├── klient_02_ecommerce_merchant.md          # Merchant online, Shoper, Presta, Shopify, IdoSell
    ├── klient_03_agencja_software_house.md      # PM w pożarze, podwykonawstwo B2B, code-review
    ├── klient_04_ekspert_dziedzinowy_uslugi.md  # Lekarz (case Doktor Monika), prawnik, komornik
    ├── klient_05_tech_agnostic_biznes.md        # 33% rynku, zero żargonu, gotowe narzędzie w pudełku
    ├── klient_06_quick_fix_awaria_hobbysta.md   # Pożar błędu 500, szybka łatka, mikro-zlecenia
    ├── modyfikator_rescue_klient_sparzony.md    # 12.1% rynku: trauma po ucieczce programisty / partaczu
    ├── modyfikator_delegowany_pracownik.md      # 4.3% rynku: asystentka/księgowa pisząca w imieniu szefa
    └── modyfikator_phantom_startup_wizjoner.md  # 2-3% rynku: founder bez kasy, equity, filtr escrow
```

---

## 2. Zweryfikowane Filary Behawioralne

1. **ZERO sztywnych formułek if-then**: Klient to nie funkcja matematyczna. Model AI otrzymuje w scenariuszach głęboki kontekst psychologiczny, świat operacyjny i mechanizmy obronne człowieka, elastycznie adaptując ton oferty.
2. **Podział na 6 Typów Bazowych + 3 Modyfikatory**:
   * Zamiast sztucznego mnożenia 20 drobnych profili, system operuje na 6 stabilnych filarach rynkowych oraz 3 modyfikatorach psychologicznych (`RESCUE`, `ODDELEGOWANY PRACOWNIK`, `PHANTOM STARTUP`).
3. **Korelacja Technologiczna (Cross-Tech)**:
   * W **ERP** klient wymaga terminologii systemowej (WZ, ZK, KSeF), a odrzuca programistyczny bełkot (.NET, deadlocks). Decyzja zapada w 1–2 wiadomościach.
   * W **Scrapingu** klient jest techniczny i wymaga twardych dowodów (TLS JA4, obejścia Cloudflare).
   * W **Tech-Agnostic (33% rynku)** klient reaguje alergicznie na IT — kupuje gotowe rozwiązanie w języku rezultatu biznesowego.
4. **Zdemaskowanie Phantom Leads**:
   * Zlecenia startupowe z budżetami 10k–35k w 90% nie kończą się wpłatą escrow w Useme. Bot stosuje bezwzględny filtr kaucji.
   * Jedynym zweryfikowanym, w 100% opłaconym dużym kontraktem w historii konta była **Doktor Monika sp. z o.o. (12 100 PLN netto)** — działający biznes medyczny z realnym bólem operacyjnym.
