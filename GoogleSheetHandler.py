import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Google Sheets setup from .env file
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')

class GoogleSheetHandler:
    def __init__(self, credentials_path):
        self.credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.open_or_create_spreadsheet()

    def open_or_create_spreadsheet(self):
        try:
            return self.client.open(SPREADSHEET_NAME)
        except gspread.exceptions.SpreadsheetNotFound:
            return self.client.create(SPREADSHEET_NAME)

    def get_worksheet(self, worksheet_name):
        try:
            return self.sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{worksheet_name}' not found.")
            return None

    def update_worksheet(self, worksheet, category_data, padding_rows=0, padding_cols=7):
        worksheet.clear()

        # Prepare headers and data
        headers = self.prepare_headers(category_data)
        worksheet.update_cell(1 + padding_rows, 1 + padding_cols, headers[0])
        worksheet.update(f"{chr(65 + padding_cols)}{1 + padding_rows}", [headers])

        all_data = self.prepare_data_for_update(category_data)
        worksheet.update(f"{chr(65 + padding_cols)}{2 + padding_rows}", all_data)

        self.calculate_sums(worksheet)
        print("Data successfully uploaded and formatted in Google Sheets.")

    def prepare_headers(self, category_data):
        headers = []
        for category in category_data.keys():
            headers.extend(
                [f"{category}", f"{category} - Description", f"{category} - Memo", f"{category} - Amount"])
        return headers

    def prepare_data_for_update(self, category_data):
        max_rows = max(len(data) for data in category_data.values())
        all_data = []

        for i in range(max_rows):
            row = []
            for category, rows in category_data.items():
                if i < len(rows):
                    transaction = rows[i]
                    row.extend([
                        transaction.get('Date', ''),
                        transaction.get('Description', ''),
                        transaction.get('Memo', ''),
                        transaction.get('Amount Debit', ''),
                    ])
                else:
                    row.extend(['', '', '', ''])
            row = [value if pd.notna(value) else '' for value in row]
            all_data.append(row)
        return all_data

    def calculate_sums(self, worksheet):
        # Calculate Sums
        # Total
        worksheet.update_cell(1, 1, 'Net:')
        worksheet.update_cell(1, 2, '=sum(E2:E)')
        # Eating Out
        worksheet.update_cell(2, 4, 'Eating Out')
        worksheet.update_cell(2, 5, '=sum(K2:K)')

        # Groceries
        worksheet.update_cell(3, 4, 'Groceries')
        worksheet.update_cell(3, 5, '=sum(O2:O)')

        # Home Reno
        worksheet.update_cell(4, 4, 'Home Reno')
        worksheet.update_cell(4, 5, '=sum(S2:S)')  # Home Reno

        # Utilities
        worksheet.update_cell(5, 4, 'Utilities')
        worksheet.update_cell(5, 5, '=sum(W2:W)')

        # Payroll
        worksheet.update_cell(6, 4, 'Payroll')
        worksheet.update_cell(6, 5, '=sum(AA2:AA)')

        # Gas
        worksheet.update_cell(7, 4, 'Gas')
        worksheet.update_cell(7, 5, '=sum(AE2:AE)')

        # Venmo
        worksheet.update_cell(8, 4, 'Venmo')
        worksheet.update_cell(8, 5, '=sum(AI2:AI)')

        # Amazon
        worksheet.update_cell(9, 4, 'Amazon')
        worksheet.update_cell(9, 5, '=sum(AM2:AM)')

        # Subscriptions
        worksheet.update_cell(10, 4, 'Subscriptions')
        worksheet.update_cell(10, 5, '=sum(AQ2:AQ)')

        # Fun Money
        worksheet.update_cell(11, 4, 'Fun Money')
        worksheet.update_cell(11, 5, '=sum(AU2:AU)')

        # Medical
        worksheet.update_cell(12, 4, 'Medical')
        worksheet.update_cell(12, 5, '=sum(AY2:AY)')

        # Unplanned
        worksheet.update_cell(13, 4, 'Unplanned')
        worksheet.update_cell(13, 5, '=sum(BC2:BC)')

        # Other
        worksheet.update_cell(14, 4, 'Other')
        worksheet.update_cell(14, 5, '=sum(BG2:BG)')

