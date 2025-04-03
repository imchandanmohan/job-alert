from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_existing_job_ids(source: str, company: str) -> set:
    """Fetch all job IDs for a given source + company from Supabase."""
    response = (
        supabase
        .table("jobs")
        .select("id")
        .eq("source", source)
        .eq("company", company)
        .execute()
    )
    if not response.data:
        return set()
    return {item["id"] for item in response.data}

def insert_new_jobs(jobs: list, source: str, company: str):
    """Insert new jobs into Supabase with source and company metadata, skipping duplicates."""
    for job in jobs:
        # Check if job already exists in the database by its ID
        existing_job = supabase.table("jobs").select("id").eq("id", job["id"]).execute()

        # If the job already exists, skip it
        if existing_job.data:
            continue  # Skip this job

        # Add source and company metadata
        job["source"] = source
        job["company"] = company
        
        # Insert the job into the database
        supabase.table("jobs").insert(job).execute()
