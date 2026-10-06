```
KWALIFIKOWALNOSC: TAK. Realna marka osobista, realny decydent (Łukasz Zembold lub osoba z jego otoczenia), projekt wykonalny. Budżet "do negocjacji" = słaby sygnał, ale nie dyskwalifikuje.

TYP_ZLECENIA: projekt jednorazowy (budowa strony WWW). Ewentualna opieka/rozwój - nie wspomniane, więc nie zakładam.

INTENCJA: wykonawcze (chcą, żebyśmy zbudowali stronę).

DECYDENT_I_BOL: Łukasz Zembold - Niezależny Doradca i Selekcjoner Wykończeń Wnętrz, 18 lat stażu. Ból: potrzebuje strony, która z jednej strony pozycjonuje go jako ekskluzywnego eksperta (Stealth Wealth / Apple Style), a z drugiej ładuje się błyskawicznie i nie ma "zbędnych bajerów". Prawdopodobnie chce odróżnić się od konkurencji w branży wykończeń (ciężkie, szablonowe strony) i przyciągać klientów high-end.

WYKONALNE: TAK. Najbliższa opcja: Jamstack (Astro / Next static export) + lekki headless CMS (Sanity / Decap) na edycję treści. To daje najniższy czas ładowania i najniższy TCO. Webflow i WordPress Gutenberg też wykonalne, ale z kompromisami (patrz miny).

POLE_DO_POPISU: JEST. Klient wrzucił trzy technologie do jednego worka ("Jamstack / Webflow / WordPress Gutenberg") jakby były wymienne, a mają fundamentalnie różne kompromisy: performance, koszt miesięczny, edytowalność, vendor lock-in. Tu jest realna wiedza, której klient nie ma.

SCIEZKA_MERYTORYKI: C (udowodniona alternatywa - Jamstack jako najlepsza droga do celu "ultra-light"). W tle B (ciekawostka o różnicach między trzema technologiami).

MINY_I_CIEKAWOSTKI:
- Ciekawostka 1: "WordPress Gutenberg" i "ultra-light / instant loading / brak zbędnych bajerów" to cele częściowo sprzeczne. WordPress (PHP + baza + pluginy) wymaga agresywnej optymalizacji (cache, CDN, dyscyplina pluginów), żeby zbliżyć się do static. Dowód: sam cel klienta w briefie ("ultra-szybka", "błyskawiczne ładowanie", "brak zbędnych bajerów spowalniających kod").
- Ciekawostka 2: Webflow = miesięczny abonament + vendor lock-in (trudno wyjść z platformy, kod nie jest w pełni wasz). Jamstack = jednorazowy koszt + tanie hosting static. Dowód: brak budżetu w briefie ("do negocjacji") - warto znać TCO przed wyborem.
- Ciekawostka 3: inspiracja menshealthweek.com.au - to nie jest "ciężka" strona eventowa, tylko lekka struktura typograficzna. Warto sprawdzić, co dokładnie klient chce skopiować (typografia? struktura? lekkość?), żeby nie wpaść w pułapkę "zróbmy tak samo".

ODMOWA: Puste. Wszystkie trzy technologie są wykonalne - to nie odmowa, to rekomendacja. Żadna z okazji 1-6 nie zachodzi (jest dostęp do API/hostingu, brak twardych limitów, brak narzuconej technologii sprzecznej z celem, brak regulacji blokujących, brak nieistniejącego terminu, brak bariery prawno-autorskiej).

PYTANIA:
1. Ile podstron i czy blog? (pytam, bo od tego zależy zakres i cena - single-page z sekcjami to inny projekt niż 6 podstron + blog; nie pisaliście o strukturze)
2. Kto dostarcza treści (copy) i zdjęcia? (pytam, bo jeśli my piszemy copy i organizujemy sesję, to osobny zakres i cena; nie pisaliście o treściach)

CO_ZLECENIE_MOWI: marka osobista Łukasz Zembold (Niezależny Doradca i Selekcjoner Wykończeń Wnętrz), 18 lat stażu, estetyka Stealth Wealth / Apple Style, inspiracja menshealthweek.com.au, priorytet ultra-light / instant loading / brak zbędnych bajerów, technologie do wyboru: Jamstack / Webflow / WordPress Gutenberg, SEO/A (ucięte - nie wiadomo dokładnie co), budżet do negocjacji.

CZEGO_NIE_MOWI: struktura strony (liczba podstron, blog), źródło treści i zdjęć, integracje (formularz kontaktowy, kalendarz rezerwacji, newsletter), konkretny zakres SEO (tytuł ucięty na "SEO/A"), hosting/domain, czy właściciel chce sam edytować treści po launchu, termin realizacji, konkretny budżet.

GRANICA_CIECIA: Brief daje estetykę i cel, ale nie zakres. Odpowiedź: rekomendacja technologii (Jamstack) + propozycja domyślnego zakresu + max 2 pytania o zakres. Bez rozwijania każdego kompromisu technologicznego - to research dla nas, nie dla klienta.

RESEARCH_POTRZEBNY: TAK (krótki) - sprawdzić, co konkretnie na menshealthweek.com.au jest "ultra-light" (jaki stack, typografia, co klient chce skopiować: strukturę, lekkość, kontrast). To research dla nas, nie dla klienta.
```