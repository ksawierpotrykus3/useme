# Pomysł: Kradzież Stylu Pisania Konkurenta (Competitor Style Mimicry)

> **Status:** Pomysł badawczy / Koncepcja  
> **Lokalizacja:** `teorie/pomysly/pomysl_02_kradziez_stylu_konkurenta_style_mimicry.md`  
> **Geneza:** Pytanie użytkownika o mechanizm podpatrywania i naśladowania najlepszego konkurenta z Useme.

---

## 1. Koncepcja Bazowa: Dlaczego kradzież stylu konkurenta kusi?

Na portalach freelancerskich (jak Useme czy Oferia) istnieją wykonawcy z wieloletnim stażem, setkami pozytywnych opinii i bardzo wysokim współczynnikiem wygranych zleceń. 
Ich styl komunikacji został ukształtowany w boju przez setki interakcji z polskimi klientami.

### Pytanie użytkownika:
> *„Miałem taką opcję zrobioną, że AI ma kraść styl od jednego mojego konkurenta pisania. Czy jest coś takiego? Czy przy inżynierii całkowicie o tym zapominamy?”*

---

## 2. Inżynieria Merytoryczna vs Styl Konkurenta: Gdzie leży granica?

Nie musimy wybierać „albo styl konkurenta, albo twarda inżynieria”. Te dwa elementy realizują zupełnie inne zadania w architekturze promptu:

| Warstwa | Za co odpowiada? | Co daje? |
| :--- | :--- | :--- |
| **Rdzeń Merytoryczny (Domain Expert / Orchestrator)** | Prawda technologiczna, trafne pojęcia (TrustZone, jitter, VFI, ORM, Webhooks, CI/CD). | **Szacunek i wiarygodność.** Klient widzi, że rozmawia ze specjalistą, a nie agencją marketingową. |
| **Warstwa Stylistyczna (Style Mimicry / Tone of Voice)** | Rytm zdań, stopień bezpośredniości, sposób zadawania pytań, interpunkcja, długość akapitów. | **Przyjazność i łatwość czytania.** Zdejmuje z oferty „sztywność AI” i korporacyjny chłód. |

### Dlaczego czysta inżynieria bez stylu bywa trudna?
Surowy inżynier potrafi napisać ofertę, która brzmi jak dokumentacja z Linux Kernel Archives – jest w 100% poprawna, ale dla nietechnicznego klienta (lub zabieganego PM-a) może być zbyt ciężkostrawna.

### Dlaczego styl konkurenta bez inżynierii przegrywa?
Jeśli konkurent pisze świetnym, lekkim stylem, ale bazuje na ogólnikach („Zrobimy to sprawnie i solidnie”), wygrywa tylko proste, tanie zlecenia. Przy zleceniach za 5k–15k PLN (Tegra 2, zaawansowane API, reverse engineering) klient potrzebuje **konkretnego dowodu kompetencji w pierwszych 3 zdaniach**.

---

## 3. Jak zaimplementować bezpieczne "Style Mimicry" w AI?

W nowoczesnej inżynierii promptów nie kopiuje się ofert konkurenta 1:1 (ryzyko plagiatu, zbieżności fraz, nieadekwatności do innego zlecenia). Zamiast tego stosuje się **ekstrakcję parametrów stylu (Few-Shot Style Transfer)**:

### Krok 1: Profilowanie Stylu Konkurenta (Style Profiler)
Zamiast wrzucać całą ofertę konkurenta, analizujemy zbiór jego 5–10 wygranych ofert pod kątem parametrów:
1. **Długość zdań:** Średnio 8–15 słów na zdanie (dynamika, brak tasiemców).
2. **Sposób witania się:** Brak „Dzień dobry, z chęcią podejmę się...”, tylko bezpośrednie wejście w temat (np. „Cześć, przeglądałem specyfikację modułu...”).
3. **Konstrukcja CTA (Call to Action):** Zamiast „Zapraszam do kontaktu”, proste, otwarte pytanie o szczegół techniczny („Czy moduł ma wyprowadzony UART?”, „Na jakiej wersji bazy stoi produkcja?”).
4. **Stosunek technologii do korzyści:** 60% techniczny konkret, 40% spokój i bezpieczeństwo wdrożenia.

### Krok 2: Wstrzykiwanie w Slot 02a (Generator Treści)
W pliku generatora (np. `agent_02a_opis_oferty.md`) możemy umieścić sekcję:
```markdown
### WZORZEC RYTMU I PROZY (FEW-SHOT TONE REFERENCE):
- Zachowaj bezpośredni, rzeczowy ton doświadczonego freelancera.
- Nie używaj korporacyjnych ozdobników.
- Każdy akapit to maksymalnie 2-3 zdania.
- Zamiast podsumowań w stylu 'Gwarantuję najwyższą jakość', napisz jak wygląda pierwszy krok techniczny.
```

---

## 4. Wnioski do wdrożenia
* Kradzież stylu jest bardzo skuteczna na poziomie **rytmu językowego i naturalności**, ale **silnik merytoryczny musi pozostać w 100% autorski i oparty na briefie zlecenia**.
* Połączenie: `Głęboka analiza zlecenia przez Orkiestratora` + `Lekki, sprawdzony rytm wypowiedzi zapożyczony od czołowych wykonawców` to idealny punkt równowagi.
