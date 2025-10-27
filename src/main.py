# src/main.py
from requests_scraper import get_job_details
from linkedin_scraper import fetch_job_details
from sheets import append_to_sheet
from datetime import date
import os
import csv

worksheet_name = "Automated Jobs"

def add_single_job(job_url, worksheet_name=worksheet_name, source="Added via script"):
    """
    Add a single LinkedIn job to the sheet. Returns (success, message).
    """
    if not job_url:
        return False, "No URL entered."
    job_data = fetch_job_details(job_url)
    if job_data and job_data.get("title") != "N/A":
        append_to_sheet([
            job_data["title"],
            job_data["company"],
            job_data["location"],
            job_data["url"],
            date.today().strftime("%Y-%m-%d"),
            "Yet to Apply",
            source
        ], worksheet_name=worksheet_name)
        return True, f"Job '{job_data['title']}' at '{job_data['company']}' added to your tracker!"
    else:
        return False, "Could not find job details. Please check the URL and try again."


def add_jobs_from_file(file_path, worksheet_name=worksheet_name, source="Imported from file"):
    """
    Import jobs from a file. Returns (added_count, error_message).
    """
    if not file_path:
        return 0, "No file path entered."
    if not os.path.exists(file_path):
        return 0, "File not found."

    _, ext = os.path.splitext(file_path)
    urls = []

    try:
        if ext.lower() == ".csv":
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        urls.append(row[0].strip())
        else:  # treat as TXT
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return 0, f"Error reading file: {e}"

    if not urls:
        return 0, "No job URLs found in the file."

    added = 0
    for url in urls:
        job_data = fetch_job_details(url)
        if job_data and job_data.get("title") != "N/A":
            append_to_sheet([
                job_data["title"],
                job_data["company"],
                job_data["location"],
                job_data["url"],
                date.today().strftime("%Y-%m-%d"),
                "Yet to Apply",
                source
            ], worksheet_name=worksheet_name)
            added += 1
    return added, None


def main_menu():
    print("\nWelcome to LinkedIn Job Tracker!")
    print("This tool helps you save LinkedIn jobs to your personal tracker.")
    while True:
        print("\n------------------------------")
        print("What would you like to do?")
        print("1. Add a single LinkedIn job link")
        print("2. Import multiple jobs from a file")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == "1":
            job_url = input("Enter LinkedIn Job URL: ").strip()
            success, msg = add_single_job(job_url)
            print(msg)
        elif choice == "2":
            file_path = input("Enter the path to the file containing job URLs: ").strip()
            added, error = add_jobs_from_file(file_path)
            if error:
                print(error)
            else:
                print(f"Imported {added} jobs from the file.")
        elif choice == "3":
            print("Thank you for using LinkedIn Job Tracker. Goodbye!")
            break
        else:
            print("Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
