from urllib.parse import urlparse


def extract_company_from_url(job_url: str) -> str:
    domain = urlparse(job_url).netloc
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2].lower()  # e.g., servicenow from careers.servicenow.com
    return domain.lower()