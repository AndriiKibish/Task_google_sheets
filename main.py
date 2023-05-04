import os
from dotenv import load_dotenv

import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

USER_EMAIL = os.getenv("EMAIL")
TABLE_NAME = input('Table name: ')

def table_create():
    # Way to credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    # Authorization
    client = gspread.authorize(creds)

    # Creating new table
    sheet = client.create(TABLE_NAME)

    # Link on table
    print(sheet.url)

    # Share the sheet with your email
    email_address = USER_EMAIL
    client.insert_permission(sheet.id, value=email_address, perm_type='user', role='writer')


if __name__ == '__main__':
    table_create()
