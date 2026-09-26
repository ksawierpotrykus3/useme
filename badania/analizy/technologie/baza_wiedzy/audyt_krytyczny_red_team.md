# RAPORT AUDYTU RED TEAM (SKORYGOWANY O REALIA EMPIRYCZNE)
## BEZLITOSNY OSTRZAŁ TAKTYK, KANAŁÓW I ARCHITEKTURY OFERTOWANIA USEME 2026

> **Status:** Wersja po korekcie operacyjnej na podstawie rzeczywistych testów na koncie zleceniodawcy.
> **Kluczowa korekta dowództwa:** 
> 1. Priv na Useme to **nie** jest kanał widmo. W rzeczywistości wiadomości prywatne wyświetlają się w interfejsie **dokładnie, szeroko i wyraźnie**, a konkurencja na priv jest **zawsze wielokrotnie mniejsza niż w ofertach publicznych**. Klient skupia się na konwersacji 1:1, zamiast przedzierać się przez śmietnik 30 ofert.
> 2. „Podkładka dla szefa” wylatuje – to sztuczne, korporacyjne over-engineering, które jest „za dużo” dla polskiego rynku B2B.

---

### CZĘŚĆ 1: KANAŁ DOTARCIA — OFERTA PUBLICZNA VS PRIV VS HYBRYDA
*(Decyzja o docelowym trybie pozostaje otwarta — badamy faktyczne właściwości obu ścieżek)*

#### 1.1. Prawdziwa Anatomia Wiadomości Prywatnej (Priv) na Useme:
- **Zaleta 1 (Brak tłumu / Drastycznie mniejsza konkurencja):** W ofertach publicznych pod każdym zleceniem ląduje natychmiast 25–40 ofert. Na priv pisze ułamek tej liczby. Oznacza to, że Twoja wiadomość nie tonie w masowym wyścigu szczurów.
- **Zaleta 2 (Format i uwaga):** W panelu Useme wiadomości prywatne mają dedykowany, szeroki, czysty widok czatu. Klient czyta tekst jak bezpośrednią rozmowę inżyniera z człowiekiem, a nie jako kolejny kafelek z ceną.
- **Zaleta 3 (Ochrona know-how):** Twój celny insight techniczny (np. zaokrąglenia VAT, KSeF FA(3), deadlocki w Subiekcie) trafia wyłącznie do zleceniodawcy. Żaden konkurent go nie widzi i nie może go skopiować 15 minut później, żeby zaoferować to samo 20% taniej.
- **Na co uważać przy privie:**
  * Musi to być uderzenie merytoryczne od pierwszego zdania (diagnoza problemu + 1 konkretne pytanie).
  * Jeśli priv brzmi jak spam („dzień dobry, napisałem też ofertę, zapraszam”), klient go zamknie. Jeśli brzmi jak robocza notatka architekta – wywołuje odpowiedź w 5 minut.

#### 1.2. Prawdziwa Anatomia Oferty Publicznej:
- **Zaleta 1 (Formalna obecność w rankingu):** Część zleceniodawców (szczególnie ci, którzy porównują tylko arkusze kalkulacyjne) klika w kafelki w formularzu wyboru wykonawcy Useme.
- **Wada (Kradzież insightów):** Publiczny insight natychmiast staje się darmową wiedzą dla reszty rynku. Oferenci poniżej Ciebie kopiują Twoje argumenty.

#### 1.3. Opcja Hybrydowa (Warunkowa):
- Złożenie oferty publicznej (aby figurować w zestawieniu) + natychmiastowe uderzenie na priv z pogłębioną diagnozą inżynierską i pytaniem kwalifikującym.
- **Wniosek:** Kanał priv jest jednym z najpotężniejszych narzędzi konwersji na Useme, o ile niesie natychmiastową wartość techniczną.

---

### CZĘŚĆ 2: ROZSTRZELANIE ARSENAŁU — CO JEST GŁUPIE, SZTUCZNE I ODPADA?

#### 1. Jawna „Podkładka dla Szefa” $\rightarrow$ ODPADA (ZBYT HOPSIUP DO PRZODU)
- **Zarzut:** Pracownicy firm (księgowe, project managerowie, asystenci) jak najbardziej normalnie tam siedzą i zlecają zadania na zlecenie zarządu/szefa. ALE jawne wklejanie do oferty ramki zatytułowanej „Podsumowanie dla Zarządu / Podkładka dla Szefa” brzmi **zbyt hopsiup do przodu** i protekcjonalnie — jakbyśmy wchodzili w czyjeś relacje służbowe i pouczali pracownika, jak ma raportować do przełożonego.
- **Werdykt:** **WYRZUCAMY jawną podkładkę.** Oferta ma być po prostu ułożona tak czysto, rzeczowo i przejrzyście (zrozumiałe punkty, jasna cena, bezpieczeństwo w sandboxie), żeby pracownik mógł ją naturalnie przekazać szefowi, jeśli będzie taka potrzeba — ale bez żadnego naszego wyrywania się przed szereg i bez sztucznego korpo-szablonu.

#### 2. 12 Miesięcy Gwarancji na Kod $\rightarrow$ ODPADA (PĘTLA NA SZYJĘ)
- **Zarzut:** W integracjach z zewnętrznymi systemami (KSeF, Comarch, Allegro, Subiekt, bramki płatności) API zmieniają się co kilka miesięcy. Obiecywanie rocznej gwarancji oznacza, że klient za 8 miesięcy zadzwoni z pretensją, że rząd zmienił schemat XML, a Ty masz mu to poprawić za darmo w ramach gwarancji.
- **Werdykt:** **REDUKCJA DO 30 DNI NA KOD WŁASNY.** Gwarantujemy brak błędów w logice wykonanej przez nas. Wszelkie zmiany w zewnętrznych systemach i API są wyłączone z gwarancji. 12 miesięcy możliwe wyłącznie przy płatnym abonamencie serwisowym (retainerze).

#### 3. Darmowy Mikro-Proof 24h na 2 plikach klienta $\rightarrow$ ODPADA W TEJ FORMIE
- **Zarzut:** Proszenie klienta, by wysłał swoje 2 najtrudniejsze pliki, to darmowa konsultacja. Klient dostanie sparsowane dane i zniknie.
- **Werdykt:** **KASUJEMY propozycję darmowego przetwarzania plików klienta przed zleceniem.** Jeśli chcemy pokazać dowód – pokazujemy własny 1-zdaniowy fakt architektoniczny lub anonimowy fragment ze sprawdzonego wdrożenia.

#### 4. 8-modułowe tabele przy małych zleceniach $\rightarrow$ ODPADA
- **Zarzut:** Rozbijanie zlecenia za 1 500 – 2 500 zł na 8 modułów wygląda groteskowo i odstrasza klientów szukających szybkiego rozwiązania.
- **Werdykt:**
  * Zlecenia małe ($<3\ 000$ zł): Krótko, 3 liczby (**Cena, Czas, Ryzyko**), zero wielkich tabel.
  * Zlecenia większe ($>5\ 000$ zł): Proste rozbicie na 3–4 etapy logiczne.

#### 5. Power Inversion w aroganckim tonie („Zanim łaskawie rozważę...”) $\rightarrow$ ODPADA
- **Zarzut:** Granica między profesjonalizmem a bufonadą jest cienka. Agresywne pouczanie klienta powoduje natychmiastowe odrzucenie.
- **Werdykt:** Zachowujemy wyłącznie **spokojne, merytoryczne pytanie o architekturę** („Zanim oszacuję ostateczny zakres, muszę doprecyzować jedną kwestię: [pytanie]”).

---

### CZĘŚĆ 3: CO BEZWZGLĘDNIE ZOSTAJE (ŻELAZNY ARSENAŁ BOTA)

1. **Insight w pierwszych 2 zdaniach (Otwarcie Problemem)**:
   * Klient w 5 sekund widzi, że autor oferty zna problem pod maską (np. FA(3) vs OCR, zaokrąglenia VAT na 15% faktur, deadlocki na `st__Stan`). To deklasuje 90% konkurencji bez pisania o swoim „doświadczeniu”.
2. **Pytanie kwalifikujące w 3. akapicie (Anti-CTA)**:
   * Zamiast banalnego „zapraszam do kontaktu” na końcu, pytanie techniczne jest wplecione w środek analizy. Klient musi na nie odpisać, bo od niego zależy powodzenie wdrożenia.
3. **Decyzja Odwracalna (Sandbox-First / Rollback w 5 min)**:
   * Zapewnienie klienta, że etap wstępny działa na kopii/sandboxie bez dotykania żywej bazy produkcyjnej. Zdejmuje paraliż decyzyjny i lęk przed awarią.
4. **Proste, modułowe etapy przy większych projektach**:
   * Rozbicie na 3–4 logiczne klocki. Klient czuje kontrolę nad budżetem, a w razie negocjacji wykreśla moduł zamiast zbijać naszą marżę.
5. **Gwarancja 30 dni na kod własny**:
   * Precyzyjna, bezpieczna deklaracja serwisowa eliminująca ryzyko ukrytych wad kodu, bez wpadania w pułapkę darmowego supportu przy zmianach API.

---

### CZĘŚĆ 4: SKORYGOWANA ARCHITEKTURA OFERTOWANIA

Bot w procesie generowania oferty/wiadomości stosuje prosty, bezwzględny lejek:

```
[Nowe Zlecenie]
       │
       ▼
[KROK 1: Analiza skali i persony]
 ├─ Małe zlecenie (< 3 000 zł)  ──► 300–450 znaków, 1 insight, 3 liczby (Cena/Czas/Gwarancja), 1 pytanie.
 └─ Duże zlecenie (> 5 000 zł)  ──► 600–900 znaków, insight otwierający, pytanie w 3. akapicie, 3-4 etapy, sandbox-first.
       │
       ▼
[KROK 2: Dobór kanału]
 ├─ Priv bezpośredni ──► Szeroki, wyrazisty, 10x mniejsza konkurencja, skupiona uwaga klienta.
 └─ Oferta publiczna ──► Formalne wejście do zestawienia z precyzyjną wyceną.
       │
       ▼
[KROK 3: Wyczyszczenie tekstu]
 └─ Zero pustosłowia, zero „chętnie pomogę”, zero korpo-podkładek, czysty inżynierski konkret.
```