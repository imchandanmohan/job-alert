from playwright.sync_api import sync_playwright
from utils import extract_company_from_url
import time

def fetch_linkedin_jobs(url: str, source: str):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json",
                "Origin": "https://www.linkedin.com",
                "Referer": url,
            }
        )

        page = context.new_page()

        print(f"🌐 Navigating to {source} job search page...")
        page.goto(url, timeout=60000)
        page.wait_for_selector("ul.jobs-search__results-list", timeout=30000)

        # Get the job list container
        container_selector = "ul.jobs-search__results-list"
        previous_height = 0

        while True:
            page.evaluate(
                f'document.querySelector("{container_selector}").scrollTo(0, document.querySelector("{container_selector}").scrollHeight)'
            )
            time.sleep(2)

            current_height = page.evaluate(
                f'document.querySelector("{container_selector}").scrollHeight'
            )

            if current_height == previous_height:
                break  # No more jobs loading
            previous_height = current_height

        print("✅ Finished scrolling.")

        job_cards = page.query_selector_all("ul.jobs-search__results-list li")

        for card in job_cards:
            title_el = card.query_selector("h3.base-search-card__title")
            company_el = card.query_selector("h4.base-search-card__subtitle a")
            location_el = card.query_selector(".job-search-card__location")
            date_el = card.query_selector(".job-search-card__listdate--new")
            job_url = card.query_selector("a.base-card__full-link")

            # Skip Dice postings
            dice_link = card.query_selector('a.hidden-nested-link')
            if dice_link and dice_link.inner_text().strip() == "Jobs via Dice":
                continue

            if not (title_el and company_el and location_el and job_url):
                continue

            job_id_attr = card.query_selector("div.base-search-card").get_attribute("data-entity-urn")
            if not job_id_attr:
                continue

            job_id = job_id_attr.split(":")[-1]
            job_title = title_el.inner_text().strip()
            company_name = company_el.inner_text().strip()
            job_location = location_el.inner_text().strip()
            posted_date = date_el.inner_text().strip() if date_el else "Unknown"
            job_details_url = job_url.get_attribute("href").strip()

            jobs.append({
                "id": job_id,
                "title": job_title,
                "company": source,
                "location": job_location,
                "posted_date": posted_date,
                "url": job_details_url,
                "source": source
            })

        browser.close()

    print(f"✅ {source} scraper fetched {len(jobs)} jobs.")
    return jobs
