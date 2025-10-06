from scraper import get_job_details
from sheets import append_to_sheet
from datetime import date

job_url = input("Enter LinkedIn Job URL: ")
job_data = get_job_details(job_url)

if job_data:
    append_to_sheet([
        job_data["title"],
        job_data["company"],
        job_data["location"],
        job_data["url"],
        date.today().strftime("%Y-%m-%d"),
        "Applied",  # default status
        ""
    ])
    print("Job added to tracker!")
else:
    print("Failed to get job details.")