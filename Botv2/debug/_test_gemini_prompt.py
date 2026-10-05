# -*- coding: utf-8 -*-
import json
import sys
import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GEMINI_URL = "http://127.0.0.1:8045/v1/chat/completions"

z = json.loads(open("badania/baza/weronikabuchholc13/04_moje_zlecenia/145287/zlecenie.json", encoding="utf-8").read())
tresc = z.get("description") or z.get("opis")

system_prompt = """Jesteś bezwzględnym, doświadczonym recenzentem zleceń freelancerskich na polskim Useme.
Widzisz treść zlecenia oraz propozycję wyceny przesłaną przez innego freelancera.

TWOJA ROLA:
Oceń szczerze, czy ta wycena ma realną szansę wygrać zlecenie u polskiego klienta MŚP na Useme:
1. PAMIĘTAJ: To jest rynek freelancingu, a nie body-leasing korporacyjny. Nie przeliczaj dni na stawkę dzienną. Dni to czas kalendarzowy z testami i rezerwą.
2. Zdiagnozuj:
   - Czy kwota to "ZA_MALA" (dumping, niedoszacowanie ryzyka i skali, robienie z siebie taniej siły roboczej)?
   - Czy kwota to "ZA_DUZA" (przestrzelenie realiów budżetowych MŚP, wejście w stawki agencji enterprise, które odstraszą klienta)?
   - Czy kwota to "OK" (maksymalna profesjonalna marża, która wciąż mieści się w granicach akceptowalności dla decydenta MŚP)?

Zwróć WYŁĄCZNIE JSON:
{
  "werdykt": "ZA_MALA" lub "OK" lub "ZA_DUZA",
  "kwota_sugerowana": <int>,
  "dni_sugerowane_do": <int>,
  "uzasadnienie": "2-3 zdania twardej krytyki lub potwierdzenia",
  "twoje_oszacowanie_rynku": "Twoje widełki w PLN netto dla tego zlecenia na Useme"
}"""

user_prompt = f"""ZLECENIE KLIENTA NA USEME:
{tresc}

--- PROPOZYCJA WYCENIACZA (DeepSeek-v4-Pro) ---
KWOTA: 24000 zł netto
TERMIN: 40-55 dni kalendarzowych
UZASADNIENIE: Wycena obejmuje architekturę offline-first, lokalną bazę, kolejkę synchronizacji i zdjęcia z kompresją.

Oceń tę propozycję obiektywnie dla rynku Useme."""

payload = {
    "model": "gemini-3.8-flash",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "max_tokens": 1000,
    "temperature": 0.3
}

r = requests.post(GEMINI_URL, json=payload, timeout=60)
print("status:", r.status_code)
data = r.json()
content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
print("CONTENT LENGTH:", len(content))
print("RAW CONTENT:")
print(content)
