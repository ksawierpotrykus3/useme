# Teorie i Pomysły Badawcze (Projekty Przyszłościowe)

Folder gromadzący koncepcje, pomysły architektoniczne i teorie psychologiczno-techniczne do wdrożenia w kolejnych iteracjach bota `useme_core`.

---

## Indeks Pomysłów:

1. [**Pomysł 01: Detekcja Priv vs Oferta Publiczna i Zmiana Zakresu**](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/teorie/pomysly/pomysl_01_detekcja_priv_vs_oferta_i_zmiana_zakresu.md)
   * **Problem:** Klient na privie całkowicie zmienia zasady gry (np. ze wstępnego briefu na zaawansowany runtime exploit na TrustZone warty 100k+ PLN).
   * **Rozwiązanie:** Rozbicie bota na dwa stany (Ofertownik vs Asystent Priv), detektor `Scope Shift` i generowanie merytorycznych odpowiedzi prostujących nierealne oczekiwania klienta.

2. [**Pomysł 02: Kradzież Stylu Pisania Konkurenta (Style Mimicry)**](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/teorie/pomysly/pomysl_02_kradziez_stylu_konkurenta_style_mimicry.md)
   * **Problem:** Dylemat między twardą inżynierią a lekkim, chwytliwym stylem czołowych freelancerów z Useme.
   * **Rozwiązanie:** Oddzielenie warstwy merytorycznej (Orchestrator) od warstwy tonu głosu (Few-Shot Style Transfer) – zachowanie prawdy technicznej przy jednoczesnym kopiowaniu dynamiki i lekkości najlepszych ofert.

3. [**Pomysł 03: Niemożność Weryfikacji Prac Fizycznych i Ułomność Portfolio na Useme**](file:///c:/Users/Ksawier/Pictures/Screenshots/Projekty_autorskie/useme_core/badania/teorie/pomysly/pomysl_03_hermetyczne_portfolio_z_bazy_zlecen.md)
   * **Problem:** Brak linków do portfolio nie wynika z żadnego NDA. Na Useme można dodać dowolne zdjęcie i opis, ale to wizualna galeria kafelków pod grafikę – nikt nie robi selfie ze sprzętem fizycznym na warsztacie ani nie wrzuca surowego technicznego tekstu bez grafiki, bo takie rzeczy wpisuje się do CV.
   * **Rozwiązanie:** Nikt nie będzie dzwonił do obcych firm weryfikować przeszłych zleceń. Jedynym sprawdzianem dla klienta jest merytoryczna głębia opisu w pierwszych zdaniach oferty. Bot czerpie specyficzne trudności brzegowe z bazy archiwalnej i podaje je jako bezpośrednie doświadczenie domenowe.
