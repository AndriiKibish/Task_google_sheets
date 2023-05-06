import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

USER_EMAIL = os.getenv("EMAIL")
TABLE_NAME = input('Table name: ')


class GoogleSheet:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = self.authorize()

    def authorize(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return gspread.authorize(creds)

    def create_sheet(self):
        sheet = self.client.create(TABLE_NAME)

        # Link to the sheet
        print(sheet.url)

        # Share the sheet with your email
        email_address = USER_EMAIL
        self.client.insert_permission(sheet.id, value=email_address, perm_type='user', role='writer')

        return sheet.url

    def write_data(self, sheet_url, data):
        # Open the sheet using the provided URL
        sheet = self.client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)  # Get the first worksheet

        # Write data to the sheet
        worksheet.update("A1:C4", data)


if __name__ == '__main__':
    credentials_file = "credentials.json"

    google_sheet = GoogleSheet(credentials_file)
    sheet_url = google_sheet.create_sheet()

    data = [
        ["Name", "Age", "City"],
        ["John", 25, "New York"],
        ["Alice", 30, "London"],
        ["Bob", 35, "Paris"]
    ]
    google_sheet.write_data(sheet_url, data)
