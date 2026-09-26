# -*- coding: utf-8 -*-
import json
import re
from curl_cffi import requests
from bs4 import BeautifulSoup

def parse_job_articles(soup, source_name=""):
    jobs = []
    articles = soup.select("article.job")
    for art in articles:
        # Title and URL
        a_tag = art.select_one("a[href*='/jobs/']")
        if not a_tag:
            continue
        href = a_tag.get('href', '')
        if "/jobs/category/" in href:
            continue
        
        m = re.search(r',(\d+)/?$', href) or re.search(r'/jobs/(\d+)/?', href)
        job_id = m.group(1) if m else None
        if not job_id:
            continue
        
        full_url = href if href.startswith('http') else f"https://useme.com{href}"
        title = a_tag.get_text(strip=True)
        
        # Category tag
        cat_el = art.select_one(".job__category, .job-category, a[href*='/category/']")
        category = cat_el.get_text(strip=True) if cat_el else source_name
        
        # Budget
        budget_el = art.select_one(".job__budget, .job-budget, .job__details-budget, .job__detail--budget")
        budget = budget_el.get_text(strip=True) if budget_el else "Do negocjacji"
        
        # Author
        author_el = art.select_one(".job__author, .job-author, .user-name")
        author = author_el.get_text(strip=True) if author_el else "Anonim"
        
        # Number of offers / competitors
        offers_count = "0"
        for detail in art.select(".job__detail, .job-detail, .jobs-list__item-details"):
            txt = detail.get_text(strip=True)
            if "ofert" in txt.lower() or "zgłosze" in txt.lower():
                m_off = re.search(r'(\d+)', txt)
                if m_off:
                    offers_count = m_off.group(1)
        
        # Time / date published
        date_published = ""
        date_el = art.select_one(".job__date, .job-date, time, .job__details-date")
        if date_el:
            date_published = date_el.get_text(strip=True)
            
        # Description
        desc_el = art.select_one(".job__desc, .job-desc, p")
        desc = desc_el.get_text(strip=True) if desc_el else ""
        
        jobs.append({
            "id": job_id,
            "title": title,
            "url": full_url,
            "category": category,
            "budget": budget,
            "author": author,
            "offers_count": offers_count,
            "date_published": date_published,
            "desc": desc
        })
    return jobs

def main():
    print("=== POBIERANIE GLOWNEJ STRONY USEME (NAJNOWSZE OTWARTE ZLECENIA) ===")
    r = requests.get('https://useme.com/pl/jobs/', impersonate='chrome120', timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    latest_jobs = parse_job_articles(soup, "Główna")
    print(f"Pobrano {len(latest_jobs)} najnowszych zleceń z https://useme.com/pl/jobs/")
    
    # Zobaczmy kilka przykładowych
    for j in latest_jobs[:5]:
        print(f"[{j['id']}] {j['title']} | Kat: {j['category']} | Budżet: {j['budget']} | Ofert: {j['offers_count']} | Data: {j['date_published']}")

if __name__ == "__main__":
    main()
