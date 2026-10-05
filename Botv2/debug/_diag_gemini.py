import requests
import json

payload = {
    "model": "gemini-3.8-flash",
    "messages": [
        {"role": "system", "content": "Zwróć TYLKO JSON: {\"status\": \"ok\"}"},
        {"role": "user", "content": "Test"}
    ],
    "max_tokens": 1000,
    "temperature": 0.3
}
try:
    r = requests.post("http://127.0.0.1:8045/v1/chat/completions", json=payload, timeout=30)
    print("status:", r.status_code)
    print("text:", repr(r.text)[:300])
except Exception as e:
    print("error:", e)
