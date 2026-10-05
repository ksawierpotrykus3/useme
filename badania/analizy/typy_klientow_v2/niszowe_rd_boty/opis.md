# Typ: Niszowe R&D / Integracje i Boty

> Źródło: typologia główna (persona_niszowe_rd_boty + kompendium Persona D). Worek B nie ma osobnego profilu — dostarcza taktyki.

## Kim jest
Klient techniczny, zaawansowany. Zleca: reverse engineering API, boty scrapingowe, integracje VoIP/SIP, wtyczki przeglądarkowe, ekstrakcję danych, scrapery z obejściem Cloudflare, streaming IPTV.

## Co realnie go boli (obserwowalne)
- Potrzebuje rozwiązania, które działa mimo zmian w zewnętrznych serwisach i captchach.
- Boi się, że rozwiązanie będzie wymagało ciągłego dostrajania.
- Ceni zrozumienie mechanizmów niskopoziomowych, nie marketing.

## Diagnoza tarcia
Wątki są ekstremalnie długie, bo scraper trzeba dostrajać do zmian w serwisach zewnętrznych i captchach. To źródło przewlekłego dialogu, nie brak decyzji klienta. Nie skracaj na siłę.

## Klucz do wygranej
Wykazanie zrozumienia mechanizmów niskopoziomowych: Headless browsers, protokoły SIP/RTP, sesje, captche, DXGI, deduplikacja iCal.

## Haczyk na priv
Pytanie o architekturę/repo: „Czy to natywny moduł czy zewnętrzny skrypt uderzający przez webhooki?"

## Ryzyko przejęcia cudzego kodu
Gdy klient mówi „dokończenie po kimś" — to osobna kategoria ryzyka. Kod bez repo/dokumentacji = ukryte błędy, wyceniaj z zapasem. Szczególnie kod z Lovable/AI = refaktoryzacja, nie rozwój.

## Modyfikatory (nakładki)
- **+Wymagający ekspert** — precyzyjnie definiuje deliverable.
- **+Rescue** — przejmowanie bałaganu po kimś.

## Demarkacje — kiedy odpuścić
- Klient nie jest techniczny (to inny typ).
- Zlecenie jednorazowe bez potencjału dostrajania.