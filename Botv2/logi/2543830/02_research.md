## 1. Fine-tuning Gemini 3 Pro

**Niepotwierdzone / wymaga weryfikacji u klienta:** Na dziś (październik 2026) **supervised fine-tuning nie jest dostępny dla Gemini 3 Pro** — i prawdopodobnie nigdy nie będzie w obecnej generacji.

- Dokumentacja Google Cloud dla Gemini 3 Pro Image wprost oznacza „调优" (tuning) jako **不支持** — nieobsługiwane.
- Oficjalny wątek na Google Developer Forum (kwiecień–maj 2026): *„supervised fine-tuning is not yet available for any Gemini 3.x model (3.1 Pro is still in Preview)"*. Jeden z użytkowników produkcyjnych pisze wprost: *„there is no option to finetune any gemini 3 model at all"*.
- Jedyne modele z rodziny 3.x, które mają SFT, to **Gemini 3.5 Flash** i **Gemini 3.1 Flash-Lite**. Dla porównania — Gemini 2.5 Pro był fine-tunowalny przez Vertex AI.

**Wniosek dla zlecenia:** Jeśli klient planuje fine-tuning, jego realne opcje to (a) pozostać na Gemini 2.5 Pro (mimo zbliżającego się wyłączenia — obecnie przesuniętego na październik), (b) użyć Gemini 3.5 Flash z SFT zamiast 3 Pro, (c) fine-tunować model open-weight poza ekosystemem Google. **Żadnej z tych opcji nie wolno przedstawiać jako oczywistej** — wymaga to pytania do klienta, czy w ogóle rozważa zejście z 3 Pro.

---

## 2. Limity rozdzielczości Gemini 3 Pro dla inputu wizualnego

- Domyślna rozdzielczość tokenów dla obrazu: **1 120 tokenów** na obraz.
- Parametr `media_resolution` pozwala ustawić **low (280) / medium (560) / default (1120)** tokenów na obraz.
- Limit obrazów na jedno zapytanie (Pro Image preview): **14**, rozmiar pliku **7 MB** (inline) lub **30 MB** (GCS).

**Mina potwierdzona:** Rysunek okna z detalami kwater i kierunku otwierania na wielostronicowym PDF trafia do modelu w rozdzielczości ograniczonej do ~1120 tokenów — to jest współdzielone z całą resztą strony. Detale geometryczne giną **przed** dotarciem do modelu. 70% może być artefaktem downsamplingu, nie modelu. Potwierdzenie z literatury: badanie AEC z 2025 r. wprost wskazuje, że *„inherent high-resolution nature of AEC drawings poses a significant challenge for standard deep learning pipelines; standard resizing inevitably leads to the loss of fine-grained textual features and thin geometric lines"*.

---

## 3. Wyspecjalizowane modele do detekcji symboli architektonicznych

Rynek istnieje, ale **modele ogólnodokumentowe działają gorzej na rysunkach architektonicznych** — to kluczowy fakt.

| Model | Kontekst | Wynik | Źródło |
|---|---|---|---|
| **RF-DETR (m)** | Layout detection AEC | mAP₅₀ = **0.949** |  |
| **Qwen3-VL-8B** | AEC, VLM | F1 = **0.911** (najlepszy F1) |  |
| **YOLOv8** | Symbole architektoniczne (18 klas, plany pięter) | mAP₅₀ = **92.3%** |  |
| **DocLayout-YOLO** (pre-trained na dokumentach) | AEC | mAP₅₀:₉₅ = **0.589** — katastrofa |  |
| **YOLOv10m** (COCO) | AEC | mAP₅₀:₉₅ = 0.772 |  |

Kluczowy wniosek z benchmarku AEC: **modele pre-trenowane na dokumentach tekstowych (LayoutLM, DocLayout-YOLO) działają na rysunkach architektonicznych GORZEJ niż modele ogólne (YOLO na COCO)** — zjawisko nazwane „domain interference". Priory strukturalne nauczone na fakturach i gazetach **aktywnie szkodzą** na rysunkach technicznych.

Istnieje też praca oceniająca VLLM (w tym Gemini) zero-shot i few-shot na planach pięter z symbolami okien i drzwi — bezpośrednio relevantna metodologicznie, choć nie dostarcza twardych liczb dla Geminiego 3 Pro.

**Alternatywa do zaproponowania:** hybryda — wyspecjalizowany detektor (YOLOv8 fine-tunowany na symbolach okien) jako pierwszy etap + VLM (Qwen3-VL lub Gemini) jako drugi etap klasyfikacji na wycinkach (cropach). To adresuje zarówno problem rozdzielczości, jak i problem „jednego promptu na trzy zadania".

---

## Implikacje dla zlecenia

1. **Fine-tuning Gemini 3 Pro: nie jest opcją.** To trzeba zakomunikować jako fakt rynkowy, nie jako opinię — z odesłaniem do dokumentacji Google. Klient może o tym nie wiedzieć.
2. **Limit 1120 tokenów na obraz to twardy sufit.** Nawet idealny prompt nie ominie downsamplingu — to argument za pre-processingiem/segmentacją (wycinki rysunku jako osobne obrazy) i/lub podejściem hybrydowym.
3. **LayoutLM/DocLayout-YOLO jako pierwszy strzał = mina.** Klient może spotkać te nazwy w researchu i uznać je za oczywisty wybór. Benchmark AEC z 2025 pokazuje, że to ślepa uliczka dla rysunków technicznych.