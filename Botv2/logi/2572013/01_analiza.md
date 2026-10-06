```
KWALIFIKOWALNOSC: TAK
TYP_ZLECENIA: projekt jednorazowy (wdrożenie voicebota na WWW) z opcją późniejszej rozbudowy o inne kanały jako osobny etap
INTENCJA: mieszane (wykonawcze + doradcze)
DECYDENT_I_BOL: Decydent: prawdopodobnie właściciel/menedżer firmy HVAC. Ból: sezonowy napływ powtarzalnych pytań, potrzeba wstępnej kwalifikacji klientów, odciążenie obsługi, standaryzacja informacji o kosztach i montażu, obawa przed halucynacjami.
WYKONALNE: TAK. Najbliższa opcja: widget JS/iframe na WordPressie + backend voice (streaming STT -> LLM + RAG -> TTS) z obsługą barge-in, np. LiveKit/Vapi + ElevenLabs + LLM.
POLE_DO_POPISU: JEST. Klient nie wie, jak zbudować, pyta wprost o architekturę, narzędzia, rozwiązanie głosu, przerwania i latencję.
SCIEZKA_MERYTORYKI: A (klient wprost pyta o technologię i rozwiązania)
MINY_I_CIEKAWOSTKI:
- RODO: voicebot zbiera dane osobowe i prawdopodobnie nagrywa rozmowę. Dowód: "zbieranie podstawowych danych od klienta", "rozmowa głosowa". Klient nie wspomina o zgodach, informacji o przetwarzaniu, retencji. Mina compliance (typ 4). Alternatywa: klauzula informacyjna przed rozmową, zgoda na nagrywanie, określona retencja.
- Latencja/barge-in: klient wymaga natychmiastowego przerwania i krótkich przerw. Dowód: "użytkownik mógł w każdej chwili wejść w słowo voicebot natychmiast przerywał", "przerwy między wypowiedziami możliwie krótkie". Standardowy pipeline bez streamingu da opóźnienia >1s. Alternatywa: streaming STT/LLM/TTS, WebRTC, VAD.
- WordPress: tytuł "na WordPressa" i "działający z poziomu strony" sugeruje, że klient może oczekiwać pluginu. Wyjaśnić: to widget JS + backend poza WP, WP tylko hostuje stronę.
ODMOWA: Brak twardej odmowy. RODO do dodania w ramach projektu, nie blokuje.
PYTANIA:
1. W jakim formacie i gdzie jest obecnie baza wiedzy firmy (dokumenty, FAQ, strona, CRM)? Czy zawiera informacje o kosztach kucia, metrażu, czasie oczekiwania? – bo od tego zależy implementacja RAG i zakres prac.
2. Czy strona WordPress jest self-hosted i czy mamy możliwość wstawienia własnego JS/backendu, czy jest to WordPress.com z ograniczeniami? – bo od tego zależy architektura integracji.
3. Czy voicebot ma po zebraniu danych zapisywać je do istniejącego CRM/kalendarza, czy wystarczy wysyłka e-mail lub zapis w WP? – bo od tego zależy zakres integracji.
4. Czy klient ma politykę prywatności i zgodę na nagrywanie rozmów? – bo to warunek zgodności RODO i wpływa na zakres wdrożenia.
CO_ZLECENIE_MOWI: Voicebot AI na stronie WWW (WordPress), język polski, baza wiedzy firmy HVAC. Zakres: informacje o wycenie, czas oczekiwania w sezonie, montaż, serwis, montaż dwuetapowy, koszty kucia, rodzaj ściany, metraż, zbieranie danych, kierowanie do kontaktu/wideokonsultacji. Jakość głosu: naturalny, ludzki, barge-in, krótkie przerwy, nie sztuczny. Doświadczenie LLM/RAG, ElevenLabs. Start: WWW. Później inne kanały.
CZEGO_NIE_MOWI: Nie mówi, jaki jest obecny stack WordPress (self-hosted/com), gdzie jest baza wiedzy i w jakim formacie, jaki CRM/kalendarz, jakie dokładnie dane zbierać, o RODO/zgodach, o budżecie (poza do negocjacji), o terminie, wolumenie ruchu, preferencjach STT/LLM (poza ElevenLabs), dostępności 24/7, przekazaniu do człowieka.
GRANICA_CIECIA: Długość średnia – zlecenie ma dużo wymagań, klient wprost prosi o konkretne informacje. Głębokość umiarkowana – przedstawiamy architekturę i narzędzia, ale bez szczegółów implementacyjnych, bo brak danych o bazie wiedzy, WordPressie, CRM. Pytania ograniczone do 4.
RESEARCH_POTRZEBNY: TAK – potwierdzić aktualne opcje voice pipeline (np. LiveKit, Vapi, Retell) i integrację z WordPressem oraz API ElevenLabs.
```