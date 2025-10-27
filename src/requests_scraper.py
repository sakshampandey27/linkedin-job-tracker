# src/scraper.py

import requests
from bs4 import BeautifulSoup

def get_job_details(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch job page")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"
    company = soup.find("a", {"class": "topcard__org-name-link"}).get_text(strip=True) if soup.find("a", {"class": "topcard__org-name-link"}) else "N/A"
    location = soup.find("span", {"class": "topcard__flavor topcard__flavor--bullet"}).get_text(strip=True) if soup.find("span", {"class": "topcard__flavor topcard__flavor--bullet"}) else "N/A"

    return {
        "title": title,
        "company": company,
        "location": location,
        "url": job_url
    }

