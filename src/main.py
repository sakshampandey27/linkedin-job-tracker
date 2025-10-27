from requests_scraper import get_job_details
from linkedin_scraper import fetch_job_details
from sheets import append_to_sheet
from datetime import date


def main():
    worksheet_name = "Automated Jobs"
    
    job_url = input("Enter LinkedIn Job URL: ")
    
    # job_data = get_job_details(job_url)   # Original scraper function
    job_data = fetch_job_details(job_url)   # New scraper function from linkedin_scraper.py

    if job_data:
        append_to_sheet([
            job_data["title"],
            job_data["company"],
            job_data["location"],
            job_data["url"],
            date.today().strftime("%Y-%m-%d"),
            "Yet to Apply",  # default status
            "Added via script"  # default notes
        ], worksheet_name=worksheet_name)
        print("Job added to tracker!")
    else:
        print("Failed to get job details.")

if __name__ == "__main__":
    main()