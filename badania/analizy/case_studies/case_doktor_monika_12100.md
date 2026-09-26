# CASE STUDY: DOKTOR MONIKA SP. Z O.O. (12 100 PLN)

## Status Finansowy
- **Faktura:** 12 100,00 PLN netto (14 883,00 PLN brutto).
- **Wypłacono na rękę:** **11 083,52 PLN**.
- **Data realizacji:** Utworzono 30.04.2026, wypłacono 22.06.2026.
- **ID Zlecenia / Oferty:** `136462` / `2625963`.

## Klient i Ból Biznesowy
Działająca klinika medyczna (4 lekarzy, docelowo 10, tysiące pacjentek).
Pacjentki klikały w Calendly, rezerwowały termin i porzucały płatność, blokując czas lekarzy.

## Dlaczego Ta Oferta Wygrała i Została Wypłacona?
1. **Analiza briefu PDF:** Odpowiedź punkt po punkcie na dostarczone makiety ekranów.
2. **Odwrócona logika rezerwacji:** Blokada w bazie danych -> webhook z Tpay -> dopiero uderzenie do Calendly API (eliminacja nieopłaconych rezerwacji).
3. **Pessimistic Locking:** Zabezpieczenie przed double-bookingiem przy jednoczesnym kliknięciu przez 50 pacjentek.
4. **Rate Limiting:** Zabezpieczenie SMSAPI przed atakami brute-force.
5. **Warunki:** 12 100 zł fix price, 4 tygodnie na stagingu, 1 miesiąc gwarancji.

## Połączenia
- [Karta: Persona Działające MŚP / Klinika](../typy_klientow/persona_dzialajace_msp_klinika.md)
- [Surowy rekord umowy: umowa_oplacona_doktor_monika_12100.json](../../baza/ksawierpotrykus3/03_odpisane/umowa_oplacona_doktor_monika_12100.json)
