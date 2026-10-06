**RESEARCH — TYLKO POTWIERDZONE FAKTY**

---

**1. NA CZYM STOI waw4free.pl (inspiracja, nie kopia)**

**NIE POTWIERDZONE:** brak jednoznacznego dowodu, że waw4free.pl działa na WordPressie. Informacje techniczne wskazują na PHP/8.2.24 i serwer PleskLin, a ścieżka `/strona/wydarzenie.php` sugeruje autorską aplikację PHP, nie WordPress. Brak śladów `wp-content` w wynikach wyszukiwania.

**Wniosek dla zlecenia:** klient chce WordPressa, ale oryginał prawdopodobnie **nie jest** na WP. To nie blokuje projektu — oznacza tylko, że „wzorowanie się na waw4free” to wzór **funkcjonalny/UX**, nie techniczny. Nie da się „sklonować” wtyczek, bo ich nie ma.

---

**2. WTYCZKI WP DO EVENTÓW UGC + MODERACJA (potwierdzone)**

- **The Events Calendar + Community Events** — użytkownicy zgłaszają wydarzenia z frontendu; administrator ustawia, czy wpisy idą od razu live, czy trafiają do moderacji jako draft. Moderacja: approve/reject, edycja przed publikacją.
- **Sugar Calendar** — zgłoszenia przez formularz (WPForms, Gravity Forms), wydarzenie trafia jako „pending review” i nie jest widoczne publicznie do akceptacji.
- **Nex Directory** — szersze rozwiązanie: frontend submissions, moderation queue, event directory, mapy, kalendarz, import CSV/JSON.

**Ograniczenie potwierdzone:** Community Events **nie ma** wbudowanego limitu zgłoszeń wg miejsca lub daty. Jeśli klient chce ograniczać zgłoszenia (np. „tylko Wiedeń”), trzeba to dopisać poza wtyczką.

---

**3. i18n (niemiecki + ewentualnie polski)**

- **Polylang** — wersja darmowa (wordpress.org), tłumaczenie ręczne; **Polylang Pro** ~99 €/rok za 1 stronę, zniżka 50% na odnowienie w 2. roku.
- **WPML** — Multilingual CMS ~99 €/rok (3 strony); Blog ~39 €/rok (ograniczony).

Dla portalu z jednym językiem docelowym (niemiecki) + ewentualnym polskim dla społeczności: **Polylang Free** wystarczy na start; Pro dopiero jeśli potrzebne tłumaczenia CPT (wydarzenia) i taksonomii.

---

**4. AdSense + RODO (potwierdzone wymogi)**

Google wymaga **IAB TCF v2.2/v2.3** dla stron monetyzowanych przez AdSense w UE. Bez certyfikowanego CMP Google może **odrzucić lub ograniczyć monetyzację**.

Dostępne wtyczki CMP dla WP z TCF v2.3:
- **Okito Cookie Consent** — IAB TCF v2.3, obsługa AdSense.
- **consentmanager Cookie Banner** — Google-certified CMP, Consent Mode v2, AdSense/Ad Manager/AdMob.
- **Clickio Consent** — TCF v2, Google Consent Mode v2, AdSense integration.

---

**5. IMPRESSUMSPFLICHT ÖSTERREICH (potwierdzone)**

ECG §5 nakłada obowiązek Impressum na **wszystkie „kommerzielle Websites”** — czyli wszystkie strony prowadzone **unternehmerisch**, niezależnie od tego, czy sprzedają towary, czy tylko prezentują działalność.

Wymagane dane (§ 5 ECG):
- pełny adres geograficzny siedziby,
- kontakt: **e-mail + telefon** (min. dwa kanały),
- członkostwo w Wirtschaftskammer,
- organ nadzoru (jeśli dotyczy),
- wskazanie przepisów zawodowych + link do RIS.

**Mina:** nawet jeśli klient działa jako osoba prywatna, **reklamy + artykuły sponsorowane** kwalifikują stronę jako komercyjną → Impressum obowiązkowe. Brak = ryzyko kary.

---

**MINY — PODSUMOWANIE**

| Mina | Dowód | Skutek |
|---|---|---|
| **Mina 1 — waw4free ≠ WordPress** | PHP/8.2.24, `/strona/wydarzenie.php`; brak `wp-content` | Klient prosi o WP, ale oryginał to autorski PHP → „wzór” ≠ „kopia 1:1”. Nie blokuje. |
| **Mina 2 — Impressumspflicht AT** | ECG §5: wszystkie kommerzielle Websites | Strona z reklamami = komercyjna → Impressum obowiązkowe. Brak = kara. |
| **Mina 3 — AdSense + RODO/TCF** | Google wymaga IAB TCF v2.2+ dla AdSense w UE | Bez CMP z TCF: AdSense może odrzucić monetyzację. Newsletter + konta = dodatkowe obowiązki RODO. |

---

**NIE POTWIERDZONE / DO DOPRECYZOWANIA**
- Dokładna technologia waw4free.pl (brak twardego dowodu).
- Czy wybrane wtyczki obsługują **wszystkie** funkcje z briefu: wydarzenia cykliczne, płatne/wyróżnione, integracja z AdSense w treści wydarzeń.
- Czy klient ma działalność w Austrii (dla Impressum: GewO vs. prywatna osoba).