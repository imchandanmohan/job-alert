from playwright.sync_api import sync_playwright
from utils import extract_company_from_url

UBER_URL = "https://www.uber.com/us/en/careers/list/?department=Engineering&location=USA-California-San%20Francisco&location=USA-California-Sunnyvale"

def fetch_jobs():
    jobs = []
    job_response_json = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Navigating to Uber job search page...")

        # Intercept the JSON response
        def handle_response(response):
            nonlocal job_response_json
            if "/api/loadSearchJobsResults" in response.url and response.request.method == "POST":
                try:
                    job_response_json = response.json()
                    print(f"✅ Captured Uber job response with {len(job_response_json['data']['results'])} jobs")
                except Exception as e:
                    print(f"⚠️ Failed parsing Uber jobs response: {e}")

        page.on("response", handle_response)
        page.goto(UBER_URL, timeout=60000)

        # Give time for filters + request
        page.wait_for_timeout(7000)
        browser.close()

    results = job_response_json.get("data", {}).get("results", [])
    for job in results:
        job_id = job.get("id")
        title = job.get("title")
        location = job.get("location", {}).get("city", "Unknown")
        url = f"https://www.uber.com/careers/job/{job_id}"
        posted_date = job.get("creationDate", "unknown")

        jobs.append({
            "id": str(job_id),
            "title": title,
            "location": location,
            "url": url,
            "company": extract_company_from_url(url),
            "source": "uber_site",
            "posted_date": posted_date
        })

    print(f"🚘 Uber scraper fetched {len(jobs)} jobs.")
    return jobs
