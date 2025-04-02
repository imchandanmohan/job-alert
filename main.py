import subprocess
import os

# 📦 Ensure Chromium is installed before scraping
def ensure_playwright_browser_installed():
    browser_path = os.path.expanduser("~/.cache/ms-playwright/chromium")
    if not os.path.exists(browser_path):
        print("📦 Installing Chromium (Playwright)...")
        subprocess.run(["playwright", "install", "chromium"], check=True)

# Your imports
from scrapers.servicenow import fetch_jobs as fetch_servicenow_jobs
from supabase_utils import fetch_existing_job_ids, insert_new_jobs
from email_utils import send_job_alert_email
from scrapers.adobe import fetch_jobs as fetch_adobe_jobs
from scrapers.apple import fetch_jobs as fetch_apple_jobs
from scrapers.nvidia import fetch_jobs as fetch_nvidia_jobs
from scrapers.paypal import fetch_jobs as fetch_paypal_jobs
from scrapers.uber import fetch_jobs as fetch_uber_jobs

SCRAPERS = [
    fetch_servicenow_jobs,
    fetch_adobe_jobs,
    fetch_apple_jobs,
    fetch_nvidia_jobs,
    fetch_paypal_jobs,
    fetch_uber_jobs,
]

def main():
    ensure_playwright_browser_installed()

    for scraper in SCRAPERS:
        jobs = scraper()
        if not jobs:
            continue

        company = jobs[0]["company"]
        source = jobs[0]["source"]

        print(f"📡 [{source}] Found {len(jobs)} jobs from {company}")

        existing_ids = fetch_existing_job_ids(source, company)
        new_jobs = [job for job in jobs if job["id"] not in existing_ids]

        if new_jobs:
            print(f"🆕 {len(new_jobs)} new job(s) for {company}")
            insert_new_jobs(new_jobs, source, company)
            send_job_alert_email(new_jobs, company)
        else:
            print(f"✅ No new jobs for {company}")

if __name__ == "__main__":
    main()
