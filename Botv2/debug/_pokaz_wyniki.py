import json
from pathlib import Path

p = Path("Botv2/debug/eksperyment_debata_dwumodelowa.json")
data = json.loads(p.read_text(encoding="utf-8"))
for item in data:
    print("=" * 80)
    print(f"{item['nazwa']} | {item['wyceniacz_model']} -> {item['reviewer_model']}")
    print(f"Finalna kwota: {item['kwota_finalna']} zł | {item['dni_od']}-{item['dni_do']} dni")
    print(f"Uzasadnienie: {item.get('uzasadnienie_finalne')}")
    for r in item["log_rund"]:
        if "werdykt" in r:
            print(f"  [{r['aktor']}] Werdykt: {r.get('werdykt')} | Sugeruje: {r.get('kwota_sugerowana')} zł | Rynek: {r.get('twoje_oszacowanie_rynku')}")
            print(f"     Komentarz: {r.get('uzasadnienie')}")
        else:
            print(f"  [{r['aktor']}] Propozycja: {r.get('kwota')} zł / {r.get('dni_od')}-{r.get('dni_do')} dni")
            print(f"     Uzasadnienie: {r.get('uzasadnienie')}")
