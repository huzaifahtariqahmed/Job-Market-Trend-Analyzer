from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urlunparse

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

def scrape_multiple_pages(start=0, end=100, step=20):
    all_links = []
    for offset in range(start, end, step):
        url = f"https://www.rozee.pk/job/jsearch/q/all/fpn/{offset}"
        print(f"Scraping: {url}")
        links = scrape_job_links(url)
        all_links.extend(links)
    return list(set(all_links))  # remove duplicates

if __name__ == "__main__":
    links = scrape_multiple_pages(start=0, end=100, step=20)
    print(f"\nTotal unique job links found: {len(links)}")
    for l in links[:10]:
        print(l)