# src/scraper.py
import os
import pickle
import re
from linkedin_api import Linkedin
SESSION_FILE = "creds/linkedin_session.pkl"

def get_linkedin_api(username, password):
    # Try loading saved session
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "rb") as f:
                api = pickle.load(f)
            api.get_profile("me")  # test if session still valid
            return api
        except Exception:
            print("Saved session expired or session file corrupted. Logging in again...")

    # If no valid session, login with username/password
    api = Linkedin(username, password)

    # Save session for future
    with open(SESSION_FILE, "wb") as f:
        pickle.dump(api, f)
    return api

# Authenticate your LinkedIn account using environment variables
username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')
if not username or not password:
    print("LinkedIn credentials not set. Please edit your .env file.")
    exit(1)
api = get_linkedin_api(username, password)

def extract_job_id_from_url(url: str) -> str:
    """
    Extracts the numeric LinkedIn job ID from a job URL.
    """
    match = re.search(r'/jobs/view/(\d+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid LinkedIn job URL")

def fetch_job_details(job_url: str) -> dict:
    """
    Fetches job title, company, location, and link from LinkedIn.
    Returns a dictionary.
    """
    try:
        job_id = extract_job_id_from_url(job_url)
        job = api.get_job(job_id)

        return {
            'title': job.get('title', 'N/A'),
            'company': job.get('companyName', 'N/A'),
            'location': job.get('formattedLocation', 'N/A'),
            'url': job.get('applyUrl', job_url)
        }

    except Exception as e:
        print(f"Failed to fetch job {job_url}: {e}")
        return {
            'title': 'N/A',
            'company': 'N/A',
            'location': 'N/A',
            'url': job_url
        }
