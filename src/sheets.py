# src/sheets.py
from typing import List, Any
import gspread
from gspread.worksheet import Worksheet
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
import os
from pathlib import Path

class SheetConnectionError(Exception):
    """Raised when there's an error connecting to the Google Sheet."""
    pass

class CredentialsError(Exception):
    """Raised when there's an issue with the service account credentials."""
    pass

class DataValidationError(Exception):
    """Raised when the data to be written is invalid."""
    pass

# Path to credentials.json relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_PATH = os.path.join(BASE_DIR, "creds", "sa-credentials.json")

class SheetManager:
    """
    A singleton class to manage Google Sheets connections efficiently.
    Reuses authenticated client to prevent multiple authentications.
    """
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SheetManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the Google Sheets client with credentials."""
        if not os.path.exists(CREDS_PATH):
            raise CredentialsError(f"Credentials file not found at: {CREDS_PATH}")
            
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
            self._client = gspread.authorize(creds)
        except ValueError as e:
            raise CredentialsError(f"Invalid credentials file: {e}")
        except Exception as e:
            raise SheetConnectionError(f"Failed to initialize client: {e}")
    
    def get_worksheet(self, spreadsheet_name: str, worksheet_name: str = None) -> Worksheet:
        """
        Get a specific worksheet from the specified Google Spreadsheet.
        
        Args:
            spreadsheet_name (str): Name of the Google Spreadsheet
            worksheet_name (str, optional): Name of the specific worksheet (tab).
                                         If None, returns the first worksheet.
            
        Returns:
            Worksheet: The requested worksheet
            
        Raises:
            SheetConnectionError: If the spreadsheet or worksheet cannot be accessed
        """
        try:
            spreadsheet = self._client.open(spreadsheet_name)
            if worksheet_name is None:
                return spreadsheet.sheet1
            try:
                return spreadsheet.worksheet(worksheet_name)
            except WorksheetNotFound:
                raise SheetConnectionError(f"Worksheet '{worksheet_name}' not found in '{spreadsheet_name}'")
        except SpreadsheetNotFound:
            raise SheetConnectionError(f"Spreadsheet '{spreadsheet_name}' not found")
        except Exception as e:
            raise SheetConnectionError(f"Failed to get worksheet: {e}")

def connect_to_sheet(spreadsheet_name: str = "LinkedIn Job Tracker", worksheet_name: str = None) -> Worksheet:
    """
    Establishes a connection to a Google Sheet and returns the specified worksheet.
    Uses SheetManager to reuse authenticated connections.
    
    Args:
        spreadsheet_name (str): The name of the Google Spreadsheet to connect to. 
                               Defaults to "LinkedIn Job Tracker".
        worksheet_name (str, optional): The name of the specific worksheet (tab) to access.
                                      If None, returns the first worksheet.
    
    Returns:
        Worksheet: A gspread Worksheet object representing the requested sheet.
        
    Raises:
        CredentialsError: If the service account credentials are invalid or missing.
        SheetConnectionError: If unable to connect to the specified sheet.
        
    Note:
        Requires valid service account credentials in the creds directory.
    """
    sheet_manager = SheetManager()
    return sheet_manager.get_worksheet(spreadsheet_name, worksheet_name)

def append_to_sheet(row: List[Any], spreadsheet_name: str = "LinkedIn Job Tracker", worksheet_name: str = None) -> None:
    """
    Appends a single row of data to the specified Google Sheet worksheet.
    
    Args:
        row (List[Any]): The data to append as a new row. Can contain strings, 
                        numbers, or boolean values.
        spreadsheet_name (str): The name of the Google Spreadsheet to append to.
                               Defaults to "LinkedIn Job Tracker".
        worksheet_name (str, optional): The name of the specific worksheet (tab) to append to.
                                      If None, uses the first worksheet.
                         
    Raises:
        DataValidationError: If the row data is invalid or empty.
        SheetConnectionError: If there's an error connecting to or writing to the sheet.
        
    Returns:
        None
    """
    if not row:
        raise DataValidationError("Row data cannot be empty")
    
    if not all(isinstance(item, (str, int, float, bool)) for item in row):
        raise DataValidationError("Row can only contain strings, numbers, or boolean values")
    
    try:
        sheet = connect_to_sheet(spreadsheet_name, worksheet_name)
        sheet.append_row(row)
    except (CredentialsError, SheetConnectionError):
        raise
    except Exception as e:
        raise SheetConnectionError(f"Failed to append row: {e}")
