"""
scraper.py — Real-time scheme scraper for Schemo
Scrapes india.gov.in and myscheme.gov.in for latest scheme updates.
"""

import os, re, requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SOURCES = [
    {
        "name": "MyScheme.gov.in",
        "url": "https://www.myscheme.gov.in/search",
        "type": "myscheme",
    },
    {
        "name": "India.gov.in",
        "url": "https://www.india.gov.in/spotlight",
        "type": "india_gov",
    },
]


def scrape_myscheme(limit=10):
    """Scrape scheme titles from myscheme.gov.in API."""
    results = []
    try:
        # MyScheme has a public API
        api_url = "https://api.myscheme.gov.in/search/v4/schemes"
        params = {"lang": "en", "q": "", "from": 0, "size": limit}
        resp = requests.get(api_url, params=params, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            schemes = data.get("data", {}).get("hits", {}).get("hits", [])
            for s in schemes:
                src = s.get("_source", {})
                results.append({
                    "scheme_name": src.get("schemeName", ""),
                    "description": src.get("briefDescription", "")[:300],
                    "eligibility": src.get("eligibility", "")[:200] if isinstance(src.get("eligibility"), str) else "",
                    "benefits": src.get("benefits", "")[:200] if isinstance(src.get("benefits"), str) else "",
                    "official_link": f"https://www.myscheme.gov.in/schemes/{src.get('schemeId','')}",
                    "community": "All",
                    "source": "MyScheme.gov.in",
                    "scraped_at": datetime.utcnow().isoformat(),
                })
    except Exception as e:
        print(f"[Scraper] MyScheme error: {e}")
    return results


def scrape_india_gov():
    """Scrape spotlight schemes from india.gov.in."""
    results = []
    try:
        from bs4 import BeautifulSoup
        resp = requests.get("https://www.india.gov.in/spotlight", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".views-row") or soup.select(".spotlight-item") or soup.select("article")
            for card in cards[:10]:
                title_el = card.select_one("h2, h3, .title, a")
                desc_el  = card.select_one("p, .description, .field-content")
                link_el  = card.select_one("a[href]")
                if title_el:
                    href = link_el["href"] if link_el else ""
                    if href and not href.startswith("http"):
                        href = "https://www.india.gov.in" + href
                    results.append({
                        "scheme_name": title_el.get_text(strip=True)[:150],
                        "description": desc_el.get_text(strip=True)[:300] if desc_el else "",
                        "official_link": href,
                        "source": "India.gov.in",
                        "scraped_at": datetime.utcnow().isoformat(),
                    })
    except ImportError:
        print("[Scraper] BeautifulSoup not installed. Run: pip install beautifulsoup4")
    except Exception as e:
        print(f"[Scraper] India.gov error: {e}")
    return results


def run_scraper():
    """Run all scrapers and return combined results."""
    print("[Scraper] Starting...")
    results = []
    results.extend(scrape_myscheme(limit=15))
    results.extend(scrape_india_gov())
    print(f"[Scraper] Found {len(results)} schemes")
    return results
