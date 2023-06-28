# -*- coding: utf-8 -*-

import os
import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread
import psutil
import time


# def measure_execution_time(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         execution_time = end_time - start_time
#         print(f"Execution time of {func.__name__}: {execution_time} seconds")
#         return result
#     return wrapper
#
#
# def memory_usage(func):
#     def wrapper(*args, **kwargs):
#         # Получаем текущий процесс
#         process = psutil.Process()
#
#         # Получаем использование памяти до выполнения кода
#         memory_before = process.memory_info().rss
#
#         # Запускаем функцию
#         result = func(*args, **kwargs)
#
#         # Получаем использование памяти после выполнения кода
#         memory_after = process.memory_info().rss
#
#         # Вычисляем использованную память
#         memory_used = memory_after - memory_before
#
#         # Выводим результат
#         print(f"Использованная память для {func}: {memory_used} байт")
#
#         # Возвращаем результат выполнения функции
#         return result
#
#     return wrapper


class GoogleSheetToolKit:
    """A set of tools for working with GoogleSheet"""
    name = 'google sheet toolkit'
    description = 'toolkit works with google sheet'
    secrets_list = None
    settings_list = None

    def __init__(self, credentials):
        self.credentials = credentials
        self.client = self.authorize()

    # @memory_usage
    def authorize(self):
        """This function will authorize you to the Google Sheets API using the OAuth 2.0 credentials"""

        creds = None
        # Check if we already have a token.json file with valid credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file(
                'token.json',
                ['https://www.googleapis.com/auth/spreadsheets']
            )
        # If there are no valid credentials, try to get new ones by running the OAuth 2.0 flow
        if not creds or not creds.valid:
            # If the credentials have expired and can be refreshed, refresh them
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    pass
            else:
                # Otherwise, run the OAuth 2.0 flow to get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials,
                    ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return gspread.authorize(creds)

    # @memory_usage
    def create_sheet(self, table_name=None):
        """This function creates a table on the Google Drive of the authenticated user, grants access to edit
        the table to the user with the specified email, and returns a link to the created table."""

        if not table_name:
            table_name = f'NewTable({datetime.datetime.now().replace(microsecond=0)})'

        sheet_obj = self.client.create(table_name)

        return sheet_obj.url

    # @memory_usage
    def write_by_url(self, sheet_url, data):
        """This function adds data to the table by table URL"""
        sheet = self.client.open_by_url(sheet_url).sheet1
        sheet.append_rows(data)
        print('Data added to table successfully')

    # @memory_usage
    def get_column_names(self, num_columns):
        """This function gets column names from the user"""
        column_names = []
        for i in range(num_columns):
            name = input(f"Enter the name of column {i + 1}: ")
            column_names.append(name)
        return column_names

    # @memory_usage
    def get_row_data(self, column_names):
        """This function gets data from the user and puts them to the appropriate columns"""
        row_data = []
        for name in column_names:
            value = input(f"Enter the value for column '{name}' (or enter 'q' to finish): ")
            if value.lower() == 'q':
                break
            row_data.append(value)
        return row_data

    # @memory_usage
    def enter_data(self):
        """This function gets column names and data from the user and puts them to the appropriate columns"""
        num_columns = int(input("Enter the number of columns for data entering: "))
        column_names = self.get_column_names(num_columns)
        data_to_write = [column_names]  # Add column names to the data
        while True:
            row_data = self.get_row_data(column_names)
            if not row_data:
                break
            data_to_write.append(row_data)

        return data_to_write
