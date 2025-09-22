from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urlunparse
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

def scrape_job_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="domcontentloaded")

        # Wait until job titles appear
        page.wait_for_selector("h3.s-18 a")

        # Extract job posting links
        links = page.eval_on_selector_all(
            "h3.s-18 a",
            "els => els.map(e => e.href)"
        )

        browser.close()

    job_links = []
    for l in links:
        if l.startswith("//"):
            l = "https:" + l
        job_links.append(clean_url(l))
    return list(set(job_links))

def scrape_n_pages(n_pages=5, jobs_per_page=20):
    """
    Scrape multiple pages of job listings from Rozee.

    n_pages: number of listing pages to scrape (default 5)
    jobs_per_page: how many jobs per page (Rozee uses 20)
    """
    all_links = []
    for i in range(n_pages):
        offset = i * jobs_per_page
        url = f"https://www.rozee.pk/job/jsearch/q/all/fpn/{offset}"
        print(f"Scraping page {i+1}: {url}")
        links = scrape_job_links(url)
        all_links.extend(links)

    # Deduplicate
    return list(set(all_links))

def scrape_job_detail(page, url):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")

    # Title
    title = page.title()

    # Summary
    summary = page.locator("meta[name='description']").get_attribute("content")

    # --- Meta Keywords Fallback ---
    keywords = page.locator("meta[name='keywords']").get_attribute("content") or ""
    parts = [p.strip() for p in keywords.split(",")]

    company, location, industry = None, None, None
    if len(parts) >= 2:
        company = parts[1]
    if len(parts) >= 3:
        if len(parts) >= 4 and "Pakistan" in parts[3]:
            location = f"{parts[2]}, {parts[3]}"
        else:
            location = parts[2]
    if len(parts) >= 5:
        industry = parts[4]

    # --- Job ID ---
    job_id = None
    m = re.search(r"jobs-(\d+)", url)
    if m:
        job_id = m.group(1)

    return {
        "job_id": job_id,
        "url": url,
        "title": title,
        "summary": summary,
        "company": company,
        "location": location,
        "industry": industry,
    }

def collect_jobs(n_pages=3, output_file="data/rozee_jobs.json"):
    job_links = scrape_n_pages(n_pages=n_pages)
    print(f"Collected {len(job_links)} job links")

    jobs_by_id = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, url in enumerate(job_links, 1):
            print(f"[{i}/{len(job_links)}] Scraping {url}")
            try:
                job = scrape_job_detail(page, url)
                if job and job.get("job_id"):
                    jobs_by_id[job["job_id"]] = job
            except Exception as e:
                print(f"Failed {url}: {e}")

        browser.close()

    Path("data").mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(jobs_by_id, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(jobs_by_id)} unique jobs to {output_file}")

if __name__ == "__main__":
    no_of_pages = 1  
    collect_jobs(n_pages=no_of_pages)  # scrape first 3 pages (~60 jobs)