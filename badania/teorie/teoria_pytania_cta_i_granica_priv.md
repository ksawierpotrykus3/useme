# TEORIA ATOMOWA: Konstrukcja Pytań CTA i Granica Automatyzacji Priv

> Status: **Otwarty Dylemat Operacyjny (Strefa 3: Brudna)**  
> Kwestie do zbadania i przetestowania w praktyce bez ryzykowania głównego konta.

---

## 1. Dylemat: 1 Pytanie CTA czy Kilka Pytań?

### Obawa: Czy 1 Pytanie Nie Staje Się Nowym Szablonem?
* Jeśli każdy bot i wykonawca kończy ofertę formułą: *"Wolisz opcję A czy opcję B?"*, zleceniodawcy zaczną to ignorować jako kolejny wyuczony trick sprzedażowy.

### Alternatywa: 2–3 Precyzyjne Pytania Inżynierskie
* Zamiast jednego pytania z dychotomią A/B, zadajemy 2 konkretne pytania o parametry techniczne:
  * *"1. Czy API sklepu ma już aktywny klucz z uprawnieniami do zapisu produktów?"*
  * *"2. W jakiej częstotliwości ma działać synchronizacja (webhook w czasie rzeczywistym czy cron raz na dobę)?"*
* **Hipoteza**: Zleceniodawca widzi, że wykonawca nie stosuje sztuczek perswazyjnych, tylko od razu zbiera parametry techniczne do uruchomienia pracy.

---

## 2. Granica Odpowiedzialności: Co Robi Bot, a Gdzie Wchodzi Człowiek?

Kluczowy dylemat operacyjny: **Czy bot powinien w ogóle automatycznie odpowiadać na priv?**

| Wariant | Plusy | Minusy / Ryzyka | Status |
|:---|:---|:---|:---:|
| **Wariant 1: Bot tylko składa ofertę, priv w 100% ręczny (Ksawier)** | Zero ryzyka halucynacji AI w negocjacjach, pełna elastyczność, wyczucie intencji klienta | Ryzyko opóźnienia odpowiedzi (jeśli Ksawier nie jest przy komputerze, klient może uciec) | **Aktualny model domyślny** |
| **Wariant 2: Bot wysyła 1. wiadomość na priv (np. żądanie pliku), potem Ksawier** | Błyskawiczny czas reakcji (< 2 minuty), klient czuje natychmiastową opiekę | Ryzyko, że klient zadał niestandardowe pytanie, a bot odpowie nie na temat | Do przetestowania |
| **Wariant 3: Pełna automatyzacja priva przez AI** | Skrajna skalowalność | Ekstremalne ryzyko spalenia leada; AI nie czuje subtelności budżetowych i negocjacyjnych | Zdecydowanie odrzucone |

---

## 3. Wnioski do Testów

1. W ofercie publicznej przetestować wariant z **dwoma szybkimi pytaniami technicznymi** zamiast jednego dylematu A/B.
2. Na priv nie wdrażać pełnej automatyzacji – dopuszcza się co najwyżej natychmiastowy asynchroniczny alert na telefon Ksawiera w momencie pojawienia się nowej wiadomości od zleceniodawcy.
