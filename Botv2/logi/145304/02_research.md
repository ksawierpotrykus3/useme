Research wykonany w zakresie wskazanym przez dziennik: sprawdzenie, co konkretnie na `menshealthweek.com.au` jest „ultra-light” oraz jaki stack stoi za stroną inspiracyjną.

**Ustalenie kluczowe:** strona `menshealthweek.com.au` **nie jest zbudowana w Jamstack** – została zaprojektowana w Figmie i wdrożona w **Webflow**. Potwierdza to wywiad z zespołem projektowym: „The site was designed in Figma, then built in Webflow. Webflow gave us full control over the editorial layout and the custom features the campaign leans on, plus a CMS to manage the 101 reasons, guides and stories.”

---

### Mina 1: Rozbieżność między deklarowanymi technologiami a rzeczywistą inspiracją

Klient w briefie wymienia „Jamstack / Webflow / WordPress Gutenberg” jako wymienne opcje, a jako wzór lekkości podaje stronę, która **jest Webflow**. To oznacza, że jeśli klient oczekuje „ultra-light” na wzór `menshealthweek.com.au`, to de facto akceptuje Webflow – ale może nie być świadomy, że to nie Jamstack. Ryzyko: klient może oczekiwać jednocześnie „Jamstack” i „jak ta strona”, nie rozumiejąc, że to dwa różne paradygmaty (static site generator + headless CMS vs. zamknięta platforma SaaS).

### Mina 2: WordPress Gutenberg vs. cel „ultra-light / instant loading”

Brief wprost mówi: „ultra-szybka”, „błyskawiczne ładowanie”, „brak zbędnych bajerów spowalniających kod”. WordPress (PHP + baza danych + pluginy) osiąga takie parametry tylko po agresywnej optymalizacji (cache, CDN, dyscyplina pluginów). Domyślny WordPress nie jest „instant loading” – to cel częściowo sprzeczny z technologią, którą klient dopuszcza. Źródło: treść ogłoszenia.

### Mina 3: Webflow – ukryty koszt i vendor lock-in

`menshealthweek.com.au` jest w Webflow, co oznacza miesięczny abonament i zamknięcie kodu w platformie (trudno wyeksportować i rozwijać poza Webflow). Klient nie podał budżetu („do negocjacji”), a wybór między Webflow a Jamstack fundamentalnie zmienia TCO: Webflow = stały koszt + ograniczenia; Jamstack = jednorazowy koszt + tanie hosting statyczne. Źródło: model biznesowy Webflow (ogólnie znany) + brak budżetu w briefie.

---

**Czego nie potwierdzono:** nie udało się zweryfikować konkretnych metryk wydajności (PageSpeed/GTmetrix) ani użytych fontów na `menshealthweek.com.au`. Nie potwierdzono też, czy klient świadomie wybrał tę stronę jako wzór „lekkości”, czy tylko estetyki. To pozostaje niepotwierdzone.

**Wniosek dla decyzji:** rekomendacja Jamstack (Astro + headless CMS) jest spójna z celem „ultra-light”, ale trzeba wyraźnie zaznaczyć klientowi, że jego własna inspiracja stoi na Webflow – i że wybór między tymi drogami to nie kwestia gustu, lecz TCO i kontroli nad kodem.