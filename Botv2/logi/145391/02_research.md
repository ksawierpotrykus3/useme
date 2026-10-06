**RESEARCH: Obsługa kosztu przesyłki przez Sferę w różnych wersjach**

**Wynik: brak potwierdzonych informacji o różnicach między wersjami Sfery w zakresie obsługi kosztu przesyłki.**

Publicznie dostępne źródła nie dokumentują, jak konkretnie Sfera dla Subiekta GT vs Sfera dla Subiekta nexo obsługują koszt przesyłki na dokumentach. Poniżej zestawienie tego, co udało się potwierdzić — oraz czego nie.

---

### Potwierdzone fakty o Sferze (kontekst ogólny)

| Fakt | Źródło |
|---|---|
| W Subiekcie GT Sfera jest **osobno płatnym dodatkiem** (ok. 1 045 zł netto za pierwsze stanowisko wg cennika od 2.01.2026) |  |
| W Subiekcie nexo Sfera jest **wbudowana w wersję PRO** — zdobycie API to podniesienie wersji całej instalacji, wyceniane per stanowisko |  |
| Sfera dla nexo ma dokumentację techniczną w **nexo SDK** |  |
| Sfera dla GT działa przez **COM/OLE Automation** |  |

---

### Potwierdzony problem z kosztem przesyłki (forum InsERT)

Na forum InsERT opisano konkretny przypadek różnicy w obsłudze transportu w zależności od **typu pozycji dokumentu**:

- Jeśli koszt transportu jest zapisany jako **usługa jednorazowa (UJ)** — przy tworzeniu EZ transport uzupełnia się automatycznie i **znika z listy asortymentu**.
- Jeśli koszt transportu jest zapisany jako **usługa w kartotece asortymentu (US)** — transport **NIE uzupełnia się** automatycznie i pozycja **pozostaje widoczna** na liście asortymentu.

Przedstawiciel InsERT (Bartosz Rosa) potwierdził: *„Z jakiegoś bliżej nieokreślonego powodu działanie oparliśmy o UJ. […] Zmienimy to tak, aby również zapisane w kartotece usługi były brane pod uwagę”*.

**To jest potencjalna mina dla tego zlecenia**: jeśli integracja WooCommerce ↔ Subiekt wysyła koszt przesyłki jako US (usługę z kartoteki), a nie UJ (usługę jednorazową), mechanizm może jej nie rozpoznać jako dostawy. **Nie potwierdzono jednak**, czy problem ten dotyczy Sfery bezpośrednio, czy warstwy Sello/EZ.

---

### Czego NIE potwierdzono (luka badawcza)

- **Brak informacji**, czy Sfera GT i Sfera nexo różnią się w sposobie obsługi kosztu przesyłki na dokumentach (ZK, FS, PA).
- **Brak informacji**, czy nowsze/starsze wersje Sfery (np. v57 vs wcześniejsze) zmieniły obsługę kosztu przesyłki. Jedyny ślad: *„Wycofanie wsparcia dla starszych wersji Sfery nexo (poniżej v57)”* — ale bez szczegółów dot. przesyłki.
- **Brak informacji**, czy koszt przesyłki w Sferze jest polem nagłówkowym dokumentu, czy pozycją asortymentową — to prawdopodobnie kluczowa różnica między integracjami.

---

### Wniosek dla zlecenia

Research nie dał twardego potwierdzenia, że wersja Sfery determinuje sposób obsługi kosztu przesyłki. **Nie można więc stwierdzić, czy skopiowanie rozwiązania z jednej platformy na drugą zadziała** — różnica może leżeć nie w wersji Sfery, lecz w **typie pozycji, jaką integracja tworzy dla kosztu przesyłki** (UJ vs US), oraz w **typie dokumentu** (ZK/FS/PA). To wymaga wglądu w kod integracji, a nie w dokumentację Sfery.