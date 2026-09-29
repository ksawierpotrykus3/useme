# OPERACJE I DANE — sesja i struktura danych ofert
**STATUS: AKTUALNE** | Scalenie: sesja/cookies + dane ofert + decyzje architektoniczne.

---

## 1. Sesja i logowanie
- Brak logowania skryptem. Playwright laduje cookies.json (sesja Useme) -> strona widzi uzytkownika jako zalogowanego.
- Cookies NIE sa potrzebne do ominiecia Cloudflare na listach (decyduje playwright-stealth).
- Cookies SA niezbedne do bycia zalogowanym (wysylka, pelne dane).
- Formularz /offer/start/ przywraca szkic z konta — nadpisanie pol wymagane.
- Awaryjny solver Turnstile istnieje jako backup, ale nie jest uzywany (widoczna przegladarka wystarcza).

## 2. Dane z listy ofert (krotkie)
Tytul, nazwa zleceniodawcy, czy ma avatar, liczba wyslanych ofert, czas do konca, kategoria szczegolowa, budzet, krotki opis, link.

## 3. Dane ze strony szczegolow (pelne)
Tytul, zleceniodawca, "opublikowano", kategoria, prawa autorskie, opis krotki i pelny (po kliknieciu "pokaz pelny opis"), umiejetnosci, budzet, waznosc, przycisk "Dodaj oferte".
- Przyciski "pokaz pelny opis" i "Dodaj oferte" wymagaja fizycznego klikniecia przez Playwright (elementy JS, nie HTML).

## 4. Kluczowe decyzje architektoniczne
- Bezpiecznik DRY_RUN: system potrafi zatrzymac sie na stronie podsumowania przed wyslaniem (flaga w config.py).
- Bez interfejsu CMD: stan meldowany do pliku stanu / logow.
- Prawa autorskie: zaznaczane tylko gdy formularz zawiera "decyzja freelancera".
- Bez screenshotow dla AI: model nie obsluguje wizji — dane jako tekst (BeautifulSoup).