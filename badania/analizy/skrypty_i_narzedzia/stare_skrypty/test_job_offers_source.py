# -*- coding: utf-8 -*-
import json
import re
import sys
from bs4 import BeautifulSoup
from curl_cffi import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def test_job(job_id, url):
    print(f"\n=== BADANIE ZLECENIA #{job_id}: {url} ===")
    r = requests.get(url, impersonate="chrome120", timeout=20)
    print("Status:", r.status_code, "Długość HTML:", len(r.text))
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 1. Sprawdz czy na samej liscie (wyszukiwarce Useme) pojawia sie to zlecenie
    # Np. szukajac po tytule lub id: https://useme.com/pl/jobs/?q=144834 lub q=TopSolid
    # 2. Sprawdz w tekscie strony
    for s in soup.find_all(string=re.compile(r"ofert", re.I)):
        parent = s.parent
        print(f"Tekst 'ofert': '{s.strip()}' w <{parent.name} class='{parent.get('class')}'>")

def test_search(query):
    search_url = f"https://useme.com/pl/jobs/?q={query}"
    print(f"\n=== TEST WYSZUKIWARKI: {search_url} ===")
    r = requests.get(search_url, impersonate="chrome120", timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.select("article.job")
    print(f"Znaleziono {len(articles)} artykułów")
    for art in articles:
        a_tag = art.select_one("a[href*='/jobs/']")
        title = a_tag.get_text(strip=True) if a_tag else "Brak"
        # Szczegoly z article
        details = [d.get_text(strip=True) for d in art.select(".job__detail, .job-detail, span")]
        print(f" - {title}: {details}")

if __name__ == "__main__":
    test_job("144092", "https://useme.com/pl/jobs/dopracowanie-istniejacego-konfiguratora-mebli-3d-i-przygotowanie-wersji-produkcy,144092/")
    test_search("144092")
    test_search("TopSolid")
