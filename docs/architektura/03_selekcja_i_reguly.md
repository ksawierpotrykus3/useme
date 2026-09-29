# SELEKCJA ZLECEN I REGULY PISANIA OFERT
**STATUS: AKTUALNE** | Reguly filtrow i TIER: kod/config.py + kod/ai_pipeline.py.

---

## 1. Klasyfikacja TIER
- **TIER A (priorytet):** aplikacje mobilne (Flutter/Kotlin/iOS), .NET/C#, ERP/KSeF/FinTech, boty/scraping, AI/LLM/RAG, konfiguratory 3D, systemy rezerwacji.
- **TIER B (standard):** sklepy dedykowane, aplikacje webowe, integracje API.
- **TIER C (odrzut):** marketing bez kodu, szkolenia, WordPress tani z duza konkurencja.
- **VIP Fast-Track (omija filtr tłumu):** lista VIP_FAST_TRACK_KEYWORDS w config.py.

## 2. Twarde filtry deterministyczne (przed AI)
- is_hard_reject() — Czerwony Ocean (wizytowki, WordPress, copywriting, Ads, grafika) chyba ze VIP keyword.
- is_blocked_author() — wlasne profile / wykluczeni autorzy (BLOCKED_AUTHORS).
- Anty-tlum — powyzej MAX_COMPETITOR_LIMIT ofert odrzut (chyba ze VIP).
- Lokalizacja on-site NIE jest twardym odrzutem (swiadoma decyzja — pozwala lapac perelki).

## 3. Czarna lista pisania ofert (zelazne zasady)
1. ZERO szablonow — kazda oferta od zera pod brief.
2. ZERO coachingu ("Doskonale rozumiem, jak wazne...").
3. ZERO obcych case study.
4. ZERO over-engineeringu.
5. ZERO korpomowy ("synergia", "innowacyjny", "kompleksowe rozwiazanie").
6. ZERO straszenia regulacjami bez zwiazku z tematem.
7. ZERO tanich chwytow ("prototyp w 15 min" przy zleceniu za 20k).
8. ZERO spamowego CTA ("Zdzwońmy sie na 15 minut").
9. ZERO anonimowosci — podpis zgodny z kontem.
10. Jezyk 1:1 — angielski do angielskiego, polski do polskiego.

## 4. Format oferty
- **Dual-Track:** oferta publiczna + osobna wiadomosc priv z pytaniem o niszowy detal techniczny.
- **Question CTA:** jedno naturalne pytanie decyzyjne zamiast propozycji calla.
- **Demo Guard:** darmowa mikro-probka na danych testowych tylko przy zleceniach na przetwarzanie dokumentow/PDF/XML/CSV/Excel.
- Dlugosc bez sztywnego limitu — zalezna od zlozonosci ogloszenia.
- Zakaz em-dash, nawiasow okraglych, markdownu; gwarancja tylko 30 dni; zakaz nieproszonego wideo.