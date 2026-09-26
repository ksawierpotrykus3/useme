# Scenariusze Psychologiczno-Operacyjne Klientów Useme

> **Zasada naczelna:** ZERO sztywnych reguł *„jeśli klient pisze X, to zrób Y”*. To jest naiwne i tworzy schematyczne, sztuczne oferty. 
> Poniższe dokumenty to **głębokie opisy wyjaśniające rzeczywistość człowieka po drugiej stronie ekranu** — jego ukryty ból, presję otoczenia, lęki, mechanizmy obronne oraz sposób myślenia o ryzyku i pieniądzach. 
> Model AI używa tych dokumentów jako **aparatu pojęciowego i soczewki psychologicznej**, elastycznie wyczuwając stopień podobieństwa w konkretnym zleceniu.

---

## 1. Architektura Katalogu Scenariuszy

```
badania/analizy/typy_klientow/scenariusze/
├── README.md                                    # Niniejszy katalog i filozofia rozumienia człowieka
│
├── [KOMERCYJNE FILARY BAZOWE]
├── klient_01_tradycyjne_msp_erp_przemysl.md     # Właściciel fabryki/hurtowni, Subiekt, Optima, KSeF, WZ
├── klient_02_ecommerce_merchant.md              # Merchant online, Shoper, Shopify, Presta, IdoSell, koszyk
│
├── [B2B I USŁUGI REGULOWANE]
├── klient_03_agencja_software_house.md          # PM w pożarze, podwykonawstwo B2B, code-review, staging
├── klient_04_ekspert_dziedzinowy_uslugi.md      # Gabinet medyczny, prawnik, komornik, realny ból finansowy
│
├── [PROCES I SZYBKIE REAGOWANIE]
├── klient_05_tech_agnostic_biznes.md            # 33% rynku, zero IT żargonu, kupuje święty spokój w pudełku
├── klient_06_quick_fix_awaria_hobbysta.md       # Pożar błędu 500, szybka łatka, mikro-zlecenia prywatne
│
└── [MODYFIKATORY PSYCHOLOGICZNE - STANY EMOCJONALNE]
    ├── modyfikator_rescue_klient_sparzony.md    # 12.1% rynku: trauma po ucieczce programisty / partaczu
    ├── modyfikator_delegowany_pracownik.md      # 4.3% rynku: asystentka/księgowa pisząca w imieniu szefa
    └── modyfikator_phantom_startup_wizjoner.md  # 2-3% rynku: founder bez kasy, equity, bariera escrow
```

---

## 2. Matryca 6 Typów Bazowych

| Plik Scenariusza | Profil Człowieka | Gdzie Boli Najbardziej? | Czego Nienawidzi? | Co Buduje Natychmiastowe Zaufanie? |
|---|---|---|---|---|
| [`klient_01`](file:///badania/analizy/typy_klientow/scenariusze/klient_01_tradycyjne_msp_erp_przemysl.md) | **Tradycyjne MŚP & ERP / Przemysł** | Zablokowanie magazynu, rozjazd stanów, kary KSeF | Programistycznego żargonu, teorii, slajdów | Język operacji fizycznych: WZ, ZK, kolektory, ciągłość sprzedaży |
| [`klient_02`](file:///badania/analizy/typy_klientow/scenariusze/klient_02_ecommerce_merchant.md) | **E-commerce Merchant** | Spadek konwersji, porzucenia koszyka, awaria DPD/płatności | Zmian na żywej bazie, długich wdrożeń | Gwarancja prac na stagingu, testy transakcji, natychmiastowy fix |
| [`klient_03`](file:///badania/analizy/typy_klientow/scenariusze/klient_03_agencja_software_house.md) | **Agencja / Software House (B2B)** | Niezrealizowany sprint, utrata klienta końcowego | Marketingowego pitshu, pytań o rzeczy opisane w repo | Konkret: dostęp do repo, staging, deklaracja stawki B2B i terminu |
| [`klient_04`](file:///badania/analizy/typy_klientow/scenariusze/klient_04_ekspert_dziedzinowy_uslugi.md) | **Ekspert Dziedzinowy / Biznes Regulowany** | Puste przebiegi (np. puste rezerwacje lekarzy), wyciek RODO | Bezradności IT, obietnic bez pokrycia | Zrozumienie procedur medycznych/prawnych, prosty język bez żargonu |
| [`klient_05`](file:///badania/analizy/typy_klientow/scenariusze/klient_05_tech_agnostic_biznes.md) | **Tech-Agnostic Business Owner** | Zostanie oszukanym, kupienie zbyt skomplikowanego IT | Nazw frameworków (FastAPI, Docker, SQL) | Gotowe narzędzie "w pudełku", opis rezultatu: "system sam to zrobi" |
| [`klient_06`](file:///badania/analizy/typy_klientow/scenariusze/klient_06_quick_fix_awaria_hobbysta.md) | **Quick IT Fix & Hobbysta** | Trwający przestój strony, brak wiedzy technicznej | Wieloetapowych procesów i drogich audytów | Natychmiastowa diagnoza błędu, szybka naprawa "od ręki" |

---

## 3. Matryca 3 Modyfikatorów Psychologicznych

Modyfikatory nie są osobnymi branżami — to **stany emocjonalno-organizacyjne**, które mogą nałożyć się na dowolny typ bazowy:

1. [`modyfikator_rescue_klient_sparzony.md`](file:///badania/analizy/typy_klientow/scenariusze/modyfikator_rescue_klient_sparzony.md) – **12.1% Rynku ($n=57$)**
   * *Człowiek zraniony*: Poprzedni deweloper zniknął, zostawił błędy lub wziął zaliczkę i przestał odbierać telefon. Klient odczuwa wstyd i paranoję.
   * *Jak myśli:* Każda kolejna oferta brzmiąca jak poprzednia wywołuje atak paniki. Szuka kogoś, kto nie boi się powiedzieć prawdy o stanie kodu i zaproponuje mały krok (przegląd/diagnozę), zamiast obiecywać gruszki na wierzbie.
2. [`modyfikator_delegowany_pracownik.md`](file:///badania/analizy/typy_klientow/scenariusze/modyfikator_delegowany_pracownik.md) – **4.3% Rynku ($n=20$)**
   * *Pracownik pod presją*: Asystentka, księgowa lub junior PM piszący w imieniu szefa. Nie ma budżetu, nie podejmie decyzji. Jej główny lęk to wzięcie winy na siebie za wybór niekompetentnego wykonawcy.
   * *Jak myśli:* Potrzebuje czytelnej, punktowej oferty, którą może bez wstydu wydrukować i położyć prezesowi na biurku.
3. [`modyfikator_phantom_startup_wizjoner.md`](file:///badania/analizy/typy_klientow/scenariusze/modyfikator_phantom_startup_wizjoner.md) – **2-3% Rynku**
   * *Marzyciel bez płynności*: Oferuje equity, szuka "wspólnika technicznego" lub rzuca budżetem 30 000 zł, którego nie ma na koncie.
   * *Jak myśli:* Żyje wizją, generuje dziesiątki wiadomości na priv, ale znika, gdy Useme żąda wpłaty kaucji escrow. Wymaga natychmiastowego postawienia twardej granicy formalnej.

---

## 4. Wytyczne Adaptacji dla AI (Jak z tego korzystać w `kod/`)

1. **Szukaj kontekstu, a nie pojedynczych słów**: Model ocenia sytuację życiową i biznesową zleceniodawcy, a nie odhacza słowa kluczowe.
2. **Kombinacja Typ Bazowy + Modyfikator**: 
   * Przykład: Zlecenie na dokończenie integracji PrestaShop z Subiektem po ucieczce freelancera = **Typ 02 (E-commerce) + Modyfikator RESCUE**.
   * Reakcja: Szacunek dla sprzedaży live (staging) + ostrożna diagnoza zastanego kodu bez obwiniania klienta.
3. **Kiedy ignorować scenariusz**: Jeśli zlecenie wykazuje cechy czysto formalne, korporacyjne przetargi z restrykcyjnym SIWZ, lub zleceniodawca jest skrajnie roszczeniowy/agresywny — bot pomija personalizację psychologiczną i stosuje rygorystyczny, chłodny kosztorys.
