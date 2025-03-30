from scrapers.servicenow import fetch_jobs as fetch_servicenow_jobs
from supabase_utils import fetch_existing_job_ids, insert_new_jobs

SCRAPERS = [
    fetch_servicenow_jobs,
    # Add more scrapers here like:
    # fetch_greenhouse_jobs,
    # fetch_lever_jobs,
]

def main():
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
        else:
            print(f"✅ No new jobs for {company}")

if __name__ == "__main__":
    main()
