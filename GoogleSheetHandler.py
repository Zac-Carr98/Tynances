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
    def __init__(self, credentials_path, worksheet_name):
        self.credentials = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.open_or_create_spreadsheet()
        self.worksheet = self.get_worksheet(worksheet_name)
        
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

    def update_worksheet(self, category_data, padding_rows=0, padding_cols=7):

        self.worksheet.clear()

        # Prepare headers and data
        headers = self.prepare_headers(category_data)
        self.worksheet.update_cell(1 + padding_rows, 1 + padding_cols, headers[0])
        self.worksheet.update(f"{chr(65 + padding_cols)}{1 + padding_rows}", [headers])

        all_data = self.prepare_data_for_update(category_data)
        self.worksheet.update(f"{chr(65 + padding_cols)}{2 + padding_rows}", all_data)

        self.calculate_sums()
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

    def calculate_sums(self):
        # Calculate Sums
        # Total
        self.worksheet.update_cell(1, 1, 'Net:')
        self.worksheet.update_cell(1, 2, '=sum(E2:E)')

        categories = ['Eating Out:', 'Groceries', 'Home Reno', 'Utilities','Payroll', 'Gas', 'Venmo', 'Amazon', 'Subscriptions', 'Fun Money', 'Medical', 'Unplanned', 'Other']
        catTotals = ['=sum(K2:K)', '=sum(O2:O)', '=sum(S2:S)', '=sum(W2:W)', '=sum(AA2:AA)', '=sum(AE2:AE)', '=sum(AI2:AI)', '=sum(AM2:AM)', '=sum(AQ2:AQ)', 
                     '=sum(AU2:AU)', '=sum(AY2:AY)', '=sum(BC2:BC)', '=sum(BG2:BG)']

        total_cells = self.worksheet.range('E2:E14')
        title_cells = self.worksheet.range('D2:D14')
        for i in range(len(categories)):
            title_cells[i].value = categories[i]
            total_cells[i].value = catTotals[i]

        self.worksheet.update_cells(title_cells)
        self.worksheet.update_cells(total_cells,value_input_option='USER_ENTERED')

        

