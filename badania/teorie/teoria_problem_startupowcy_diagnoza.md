# TEORIA ATOMOWA: Problem Startupowców – Diagnoza i Hipotezy

> Status: **Otwarty Problem Badawczy / Hipoteza Robocza (Strefa 3: Brudna)**  
> Źródło: Historia zapytań z bazy (Startup Zdrowie Psychiczne 34k, Generator CV 15k, SaaS B2B 14k) oraz weryfikacja Ksawiera.

---

## 1. Co Mamy Zarejestrowane w Danych?

1. Zleceniodawcy startupowi o wysokich deklarowanych budżetach (10 000 – 35 000 PLN) **odpowiadają na nasze oferty**.
2. Wymieniają kilka wiadomości, zadają pytania o architekturę, po czym **wątek umiera bez podpisania umowy i bez wpłaty do Useme Escrow**.
3. Dotychczasowa konwersja do pieniędzy w tym segmencie: **0 PLN**.

---

## 2. Czy To Jest Teoria, Czy Coś Więcej?

To jest **Problem Badawczy z kilkoma konkurującymi teoriami**. Błędem było kategoryczne stwierdzenie *"startupowcy to w 100% bezużyteczni marzyciele"*. Fakt transakcyjny jest jeden: te zlecenia nie przyniosły zysku. Natomiast **powód** tego stanu rzeczy to otwarta teoria, która dzieli się na 4 hipotezy:

### Hipoteza A: Byliśmy za słabi merytorycznie / brak dowodu autorytetu
* Startupowiec powierza programiście swoje "dziecko życia".
* Jeśli nasza oferta brzmiała jak zwykły wykonawca od tasków, a nie jak techniczny partner (CTO), klient przestraszył się, że utopi budżet i uciekł szukać software house'u.

### Hipoteza B: Byliśmy za drodzy dla bootstrappingowca
* Wielu założycieli wpisuje budżet zlecenia 20k–30k na Useme, ale w rzeczywistości mają na koncie 3 000 zł oszczędności, a resztę "planują pozyskać".
* Kiedy zobaczyli twardą wycenę na 15k–34k bez elastyczności, sparaliżowało ich to finansowo.

### Hipoteza C: Błędny język i styl pisania do tego profilu
* Startupowiec nie chce specyfikacji protokołów ani suchych komend. On żyje rynkiem, MVP, użytkownikami i pozyskaniem trakcji.
* Pisanie do niego czystym inżynierskim żargonem mogło rozminąć się z jego potrzebą ("chcę szybko sprawdzić czy ludzie będą tego używać").

### Hipoteza D: Pułapka wyciągania darmowej wiedzy (Phantom Lead)
* Klient nigdy nie planował nikogo zatrudnić na Useme – potrzebował jedynie darmowej wyceny i architektury, by wpisać ją do wniosku o dotację PARP / do inwestora.

---

## 3. Plan Testowy (Dla Konta Testowego)

Nie zmieniamy głównego silnika bota. Wszelkie testy segmentu startupowego muszą iść przez **osobne konto testowe**:
1. **Wariant Testowy 1 (Styl CTO/MVP):** Skupienie na cięciu zakresu do 1 kluczowej funkcji, która weryfikuje rynek w 10 dni za ułamek ceny.
2. **Wariant Testowy 2 (Pytanie o finansowanie):** Szybka weryfikacja na priv, czy projekt ma już zabezpieczony budżet, czy jest na etapie pomysłu.
