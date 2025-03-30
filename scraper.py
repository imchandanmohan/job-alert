from playwright.sync_api import sync_playwright
from utils import extract_company_from_url

BASE_URL = "https://careers.servicenow.com"
JOBS_URL = (
    f"{BASE_URL}/jobs/?search=&"
    "team=Digital+Technology&team=Early+In+Career&"
    "team=Engineering%2C+Infrastructure+and+Operations&"
    "team=Support+and+Product+Success&"
    "location=San+Francisco&location=Santa+Clara&pagesize=100"
)

def fetch_servicenow_jobs():
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 1024},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/122.0.0.0 Safari/537.36"
        )

        page = context.new_page()
        print("Navigating to job page...")

        try:
            page.goto(JOBS_URL, timeout=60000)
            page.wait_for_selector("#js-job-search-results .card.card-job", timeout=60000)
        except Exception as e:
            print(f"❌ Failed to load jobs: {e}")
            browser.close()
            return []

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        job_cards = page.query_selector_all("#js-job-search-results .card.card-job")
        print(f"✅ Found {len(job_cards)} job cards")

        seen_ids = set()

        for card in job_cards:
            title_el = card.query_selector("a.js-view-job")
            location_el = card.query_selector("ul.job-meta li.list-inline-item")
            job_actions = card.query_selector("div.card-job-actions")

            if not (title_el and location_el and job_actions):
                continue

            job_id = job_actions.get_attribute("data-id").strip()
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            job_url = BASE_URL + title_el.get_attribute("href").strip()

            job = {
                "id": job_id,
                "title": title_el.inner_text().strip(),
                "location": location_el.inner_text().strip(),
                "url": job_url,
                "company": extract_company_from_url(job_url),
                "source": "servicenow_site"
            }

            jobs.append(job)

        browser.close()
    return jobs

if __name__ == "__main__":
    jobs = fetch_servicenow_jobs()
    for job in jobs:
        print(f"{job['title']} - {job['location']}\n{job['url']}\n")
