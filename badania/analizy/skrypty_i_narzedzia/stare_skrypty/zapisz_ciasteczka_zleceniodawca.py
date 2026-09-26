# -*- coding: utf-8 -*-
import json
from pathlib import Path

raw_netscape = """
.useme.com	TRUE	/	FALSE	1809962940	_uetvid	05b499e02d2811f1823c41aebfe9727c
useme.com	FALSE	/	FALSE	0	tz	Europe/Warsaw
useme.com	FALSE	/	FALSE	0	ab_experiments__homepage-cta	""
useme.com	FALSE	/	FALSE	1805728153	g_state	{"i_l":0,"i_ll":1790176153384,"i_e":{"enable_itp_optimization":24},"i_et":1790176153384,"i_b":"lV4mFbbBS3YHSP+B4Vv9qMK9HZdlJBD162AOS3rnufI"}
useme.com	FALSE	/	TRUE	1821625972	csrftoken	9GTK3Hl4jmOsy1pxJ3JgiDxyi9E43RlT
useme.com	FALSE	/	FALSE	1791385972	sessionid	sypzjem4tvgiwlzfhjlbwo1m84mzq01h
useme.com	FALSE	/	FALSE	0	user_id	702683
.useme.com	TRUE	/	TRUE	1821712434	cf_clearance	nEMox5VOwy3EZUXP_5.4e0IAcRWtttMFP9Yn0m2pG.c-1790176415-1.2.1.1-XV5_AleiN8eLNxPBzV_rJuJTb4TqnbnX.78iDrgWfT.rsSvQcrS2K_l6goBVxXa0fPnjOlSnsDqTrrep4yAgk0otJp5qx0_CVgF4ia4vWlvoqto_.MRharLfCzRiT4q4LQWBTfrd5jCzc4c6Ql3lMJS5OJNMmzFwz0XmBOgsvvV4vpIqQwc8VTxAnAiaDizrkaU_76M5RmHrYhZIvjLhLM0SJ9SZfql7v6S_y.MFf27HAZrk0pShmR_WkX.Js1YUF_x25QthO4ZTtpjXsrTV4jzVicdqE5Z8UbxdzgvR4hrS6x_UgYD3TopCmF6MuVSau6NQu02OJItzI.J7epfYN4cvbwKzizQ.Rwqk41rNptq9CeHMKFZOTrreAr1K1f7GHURteeakW9T7jXqIwOKqw3ZgVL0tCDD_MFZEBS04kSsbO3x4cSaP4P6L.JAAvQsQeqnrQlP0Sylijdn6X0puTbEeb_IPfPoy1TxUWzNUKFu6U5ksm7TtsH96X6d2Wl2v
""".strip()

tech_dir = Path("tech")
tech_dir.mkdir(parents=True, exist_ok=True)

# 1. Zapis surowego pliku Netscape
txt_path = tech_dir / "cookies_zleceniodawca.txt"
txt_path.write_text(raw_netscape, encoding="utf-8")

# 2. Parsowanie do formatu Playwright JSON
cookies_json = []
for line in raw_netscape.split("\n"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split("\t")
    if len(parts) >= 7:
        domain, flag, path, secure, expires, name, value = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        c = {
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
            "expires": float(expires) if float(expires) > 0 else -1,
            "httpOnly": False,
            "secure": secure.lower() == "true",
            "sameSite": "Lax"
        }
        cookies_json.append(c)

json_path = tech_dir / "cookies_zleceniodawca.json"
json_path.write_text(json.dumps(cookies_json, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Zapisano {len(cookies_json)} ciasteczek do:")
print(f" - {txt_path}")
print(f" - {json_path}")
