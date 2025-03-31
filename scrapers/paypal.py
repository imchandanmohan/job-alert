import requests
from utils import extract_company_from_url

PAYPAL_JOBS_URL = "https://paypal.eightfold.ai/api/apply/v2/jobs/274904526691/jobs?domain=paypal.com"

def fetch_jobs():
    jobs = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Referer": (
            "https://paypal.eightfold.ai/careers?query=Engineering&location=San%20Jose%2C%20CA%2C%20United%20States"
            "&pid=274904526691&Job%20Category=Software%20Development&domain=paypal.com"
        )
    }

    try:
        response = requests.get(PAYPAL_JOBS_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        positions = data.get("positions", [])
    except Exception as e:
        print(f"❌ PayPal scraper failed: {e}")
        return []

    for job in positions:
        job_id = job.get("ats_job_id") or job.get("id")
        title = job.get("name")
        location = job.get("location")
        url = job.get("canonicalPositionUrl")
        posted_date = job.get("t_update", None)

        jobs.append({
            "id": job_id,
            "title": title,
            "location": location,
            "url": url,
            "company": extract_company_from_url(url),
            "source": "paypal_site",
            "posted_date": str(posted_date) if posted_date else "unknown"
        })

    print(f"💸 PayPal scraper fetched {len(jobs)} jobs.")
    return jobs
