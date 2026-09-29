# PLAN: Lista hipotez awarii wysylki (do testowania)
**STATUS: PLAN / HIPOTEZY** — lista mozliwych przyczyn. Kazda wymaga testu falsyfikujacego. To NIE sa potwierdzone fakty.

Legenda: krytyczna / wysoka / srednia / niska.

## A. Formularz / falszywy sukces
1. Falszywy WYSLANO po samym URL (bez potwierdzenia).
2. Opis nie trafia do rich-editora.
3. Turnstile nieobsluzony w formularzu.
4. Draft przywracany i nienadpisany.
5. Kruche selektory przyciskow ("Wyslij", "Przejdz do podsumowania").
6. Zbyt krotkie czekanie po submit.
7. Brak walidacji pol przed submitem.
8. Radio praw autorskich tylko przy "decyzja freelancera".
9. Baner cookies przykrywa przycisk.
10. int(dni) wybucha przy "7 dni".

## B. Lancuch AI
11. Proxy nie dziala.
12. Pusty lancuch -> RuntimeError.
13. Brak [WYNIK_KONCOWY] -> ValueError.
14. Selekcja timeout -> przepuszcza wszystkie / zly format -> 0 ofert.
15. Zegar abortuje lancuch.
16. Pusty output x3 -> None.
17. Circuit breaker / watchdog / timeout -> None.
18. Cicha akceptacja FAIL; zbyt lagodny _is_pass.
19. Brak kalkulatora -> slot 02b bez wyceny.
20. Anty-powtorka zostawia podobna wersje.
21. Anomalie JSON z proxy (BOM/escape).

## C. Gubienie ofert
22. Zlecenia utkniete na POBRANO_DETALE bez pipeline.
23. Dedup per konto pomija cicho.
24. Podwojna blokada.
25. Zapisana propozycja pomija AI.
26. Marker blokuje starsze.
27. GLOBAL-DUP tylko loguje (nie blokuje).
28. Wyjatek detali polkniety.
29. Parser gubi oferty bez article.job.

## D. Infrastruktura
30. Cookies wygasle -> break.
31. Loader cookies cicho ignoruje blad.
32. Cloudflare przy headless.
33. Statyczny User-Agent.
34. Kill switch STOP.
35. Rate-limit przy delay=0.

## E. Konfiguracja
36. Sanity-blok progu stawki.
37. DRY_RUN / USE_MOCK_AI / ZBIERACZ_AKTYWNY — flagi.
38. Walidatory wylaczone.
39. Rozjazd progów prompt vs kalkulator.

## F. Timing / proces
40. Wyscig marker vs zapis.
41. Checkpoint wznawia od zlego slotu.
42. Zapis atomowy zostawia stary plik.
43. Brak logu zbiorczego (brak jednego zrodla prawdy o wysylce).
</parameter>