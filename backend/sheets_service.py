
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your Google API credentials
SERVICE_ACCOUNT_FILE = '/home/bhaskar/Projects/Email/backend/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def read_google_sheet(spreadsheet_id: str, range_name: str):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    # Convert to DataFrame if there is data
    if not values:
        return pd.DataFrame()
    
    df = pd.DataFrame(values[1:], columns=values[0])  # Assumes first row is headers
    return df
