# src/sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Path to credentials.json relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_PATH = os.path.join(BASE_DIR, "creds", "sa-credentials.json")

def connect_to_sheet(sheet_name="LinkedIn Job Tracker"):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def append_to_sheet(row, sheet_name="LinkedIn Job Tracker"):
    """
    Appends a single row to the Google Sheet
    """
    sheet = connect_to_sheet(sheet_name)
    sheet.append_row(row)
