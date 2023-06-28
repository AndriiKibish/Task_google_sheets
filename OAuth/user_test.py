from google_sheet_toolkit import GoogleSheetToolKit


if __name__ == '__main__':
    CREDENTIALS_FILE = 'credentials.json'

    google_sheet = GoogleSheetToolKit(CREDENTIALS_FILE)
    table_url = google_sheet.create_sheet()
    data_to_write = google_sheet.enter_data()

    if data_to_write:
        google_sheet.write_by_url(table_url, data_to_write)
        # print("Data added to table successfully.")
    else:
        print("No data to write to table.")
