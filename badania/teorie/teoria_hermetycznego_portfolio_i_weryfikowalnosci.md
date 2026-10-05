# Teoria Hermetycznego Portfolio i Nieweryfikowalnych Realizacji Niszowych
**Status:** Hipoteza robocza (zweryfikowana empirycznie na zleceniu #145003 Tegra 2)  
**Data:** 28 września 2026  
**Autorzy:** Ksawier Potrykus & Antigravity AI  
**Lokalizacja:** `badania/teorie/teoria_hermetycznego_portfolio_i_weryfikowalnosci.md`  

---

## 1. Geneza Pomysłu (Obserwacja ze zlecenia Tegra 2)

Podczas analizy zlecenia `#145003` (Voltage Glitching na NVIDIA Tegra 2 dla klienta `Naviproject`) pojawiło się fundamentalne pytanie biznesowe:
> *„Gdybyśmy wykonali takie zlecenie, to jak to w ogóle dać do portfolio na Useme? Nikt nie robi selfie ze sprzętem fizycznym na stole warsztatowym. Useme pozwala wrzucać tylko miniaturki stron www i linki do repozytoriów. Poza tym, nikt nie będzie dzwonił do obcych ludzi i sprawdzał, czy ktoś faktycznie lutował taką płytkę.”*

Z tego spostrzeżenia wynika potężna dźwignia psychologiczna: **Asymetria Weryfikowalności w Niszach Fizycznych i Specjalistycznych**.

---

## 2. Dlaczego Weryfikacja Portfolio w Hardware/Inżynierii Nie Istnieje?

W standardowych zleceniach webowych (np. WordPress, sklep Shopify, landing page) klient **żąda linków do portfolio**:
- Chce zobaczyć żywe strony, kliknąć, ocenić design.
- Brak linku rodzi podejrzenia, bo strony internetowe z definicji są publicznie dostępne w sieci.

W zleceniach **hardware, embedded, inżynieryjnych i niskopoziomowych**:
1. **Brak „selfie ze sprzętem”:** Nikt normalny nie robi sesji zdjęciowych lutownicy, oscyloskopu, analizatora stanów logicznych ani podpiętych przewodów UART/JTAG, żeby wrzucać to na portal z ogłoszeniami. Prace fizyczne nie generują klikalnych linków.
2. **Galeria Useme to format wizualny, a nie CV:** Na Useme technicznie można dodać dowolne zdjęcie, opis i link, ale portfolio to galeria kafelków pod grafikę i layouty. Nikt nie będzie wrzucał selfie z lutownicą ani publikował pustego kafelka z surowym, technicznym opisem architektury bez zdjęcia – takie rzeczy wpisuje się do CV, a nie do galerii portfolio. Klient zlecający zaawansowany problem doskonale to rozumie.
3. **Poważna inżynieria dzieje się poza platformami:** Większość takich kontraktów zawierana jest bezpośrednio B2B, offline lub przez rekomendacje. Useme to tylko ułamek działalności.
4. **Zerowe ryzyko weryfikacji telefonicznej:** Żaden klient nie ma czasu, numerów ani ochoty dzwonić do obcych firm, by pytać „czy pan X rok temu diagnozował wam magistralę CAN”.
5. **Jedyną walutą zaufania jest gęstość pojęciowa w ofercie:**
   Klient weryfikuje wykonawcę **wyłącznie po tym, co i jak pisze w pierwszych 3 zdaniach oferty**:
   - Czy zna architekturę procesora (np. `BootROM`, `OTP`, `AP20H/AP25`, `TRM Tegra 2`),
   - Czy rozumie realne wyzwania fizyczne (filtracja na szynie zasilania, zbocza glitcha, jitter zegara w wielozadaniowym OS),
   - Czy operuje właściwym żargonem laboratoryjnym.

---

## 3. Implikacje dla Architektury Ofertowarki (Orchestrator)

1. **Segmentacja poziomu dowodu:**
   - Zlecenie web/e-commerce -> podawać wyłącznie sprawdzone case studies z twardymi liczbami (zgodnie z `portfolio_baza.md`).
   - Zlecenie inżynieryjne / sprzętowe / niszowe -> **zero tłumaczenia się z braku linków (żadnego wspominania o NDA!)**. Zamiast tego 100% nacisku na precyzyjny opis problemu technicznego z bazy wiedzy.
2. **Baza archiwalna jako źródło dowodu kompetencji:**
   Orchestrator dobiera z bazy archiwalnych zleceń analogiczny problem techniczny i formułuje go bezpośrednio w ofercie (*„Przerabialiśmy dokładnie to zagadnienie przy układzie X, gdzie największym wyzwaniem była stabilizacja zasilania...”*).
3. **Efekt natychmiastowej przewagi:**
   Konkurencja pisze generyczne banały, a nasza oferta trafia w sedno problemu, budząc natychmiastowe zaufanie bez potrzeby jakichkolwiek linków zewnętrznych.
