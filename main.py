import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

""" To use this code, go to the .env file and change the worksheet name to the month that you would
 to do finances for. First you have to create the worksheet in google sheets."""


# Load environment variables from .env file
load_dotenv()

# Google Sheets setup from .env file
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')

# Define categories and keywords from .env or hardcoded values
CATEGORY_ORDER = os.getenv('CATEGORY_ORDER', '').split(',')


class CategorySorter:
    def __init__(self):
        self.categories = {
            'EatingOut': ['HOUSE', 'ANGEL', 'Canadian Bakin', 'BELL', 'STARBUCKS', 'Rock N Roll', 'POPEYES',
                          'BOOT PIZZERIA HUNTSVILLE', 'CHICK-FIL-A', 'BLANCA', '*ROOSTER\'S CROW', '*TURBO COFFEE',
                          'TACO MAMA', 'Hatch Cafe', '#352103', 'DRIVE IN #5842', 'GUADALAJARA', 'BUS BREWING',
                          'MOON HUNTSVILLE', 'MERCADO LA COLONIHUNTSVILLE', '*GOLD SPRINT', 'House HUNTSVILLE',
                          'BRUEGGERS', 'WINDMILL BEVERAGES', 'CAVA WHITESBURG 256-696-5970', 'HATCH CAFE',
                          'MASON DIXON BAKERYHUNTSVILLE', 'LES JOURS', 'TST* HOUND & HARVEST', 'EL HERRADURA',
                          'TROPICAL SMOOTHIE CAFE', 'UAH HUNTSVILLE DUNKIN', 'WHATABURGER', 'GOOD COMPANY CAFE',
                          'Waffle House', '*DOMINO\'S'],
            'Groceries': ['Walmart', 'Wal-Mart', 'T-1367', 'WAL-MART', '70080', '9040', 'HTTPSINSTACARCAUS', '#1785 HUNTSVILLE',
                          '70080', '70083', 'WM SUPERCENTER', 'PUBLIX', 'JOE S #69'],
            'Home Reno': ['HOME DEPOT', 'HOMEDEPOT', 'FLOORING', '#41 10050', '866-483-7521', '10012 S MEMORIAL PKWY'],
            'Utilities': ['866-496-9669', 'UNITEDWHOLESALE', 'UTILITIES', '*Prime Pest LLC', 'HMFUSA.com', 'FARM RO',
                          'MORTGAGE MTG SERVICING'],
            'Payroll': ['TECHNOLO', 'CITY - PAYROLL'],
            'Gas': ['SERVICE STATION', 'OIL', 'MARATHON', 'CHEVRON', 'EXXON', 'SUNOCO'],
            'Venmo': ['Visa Direct', 'CASHOUT',],
            'Amazon': ['Mktp', 'AMAZON', 'Amazon', 'Amzn.com/billWAUS'],
            'Subscriptions': ['APPLE', 'Spotify', 'Reformed', 'NEXUSMODS', 'OF THE VALLEY', 'MICROSOFT', 'DISCORD',
                              'POSHERVA', 'Money - Premium', '*CLOUDFLARE', 'BUBBLES EXPRESS WASH'],
            'Fun Money': ['GAMES', 'Etsy.com', 'GOODWILL', 'BUY #514', 'NASA EXCHANGE', '*BESTBUY', '4112 VAL BEND 18',
                          'ONLINE 9640 888', 'NASA Bldg. 4203', '*G2A', 'MICHAELS', 'POSHMARK', 'HOBBYLOBBY',
                          'SAVING WAY - SOUTH', '*STEAM PURCHASE', '*PARTSEXPRES', 'HUNTSVILLE 26'],
            'Unplanned': ['FIRESTONE1', 'STAPLES', 'Supplies Plus', 'TOUCH GARDEN', 'ROCKET CAR WASH', 'PETSMART',
                          'AUTOZONE', 'ADVANCE AUTO PARTS', 'DIXIE WASH', 'MADISON COUNTY LICENSE'],
            'Medical': ['HUNTSVILLE HOSPITAL', 'WWW.HSCCOFAL.COM DECATUR', 'ALABAMA DERMATOLOGY', '*GREEN PRIMARY CARE',
                        'WHITESBURG ANIMAL HOSPIHUNTSVILLE', 'COUNSELING 101 LOWE', 'WWW.ROCKETCITYCOLLECTIVHUNTSVILLE',
                        'CRESTWOOD PHYS', 'WOMEN4WOMEN']
        }
        self.categories = {category: self.categories[category] for category in CATEGORY_ORDER}

    def categorize_data(self, df):
        category_data = {category: [] for category in self.categories}
        category_data['Other'] = []
        for _, row in df.iterrows():
            for category, keywords in self.categories.items():
                if any(str(keyword) in str(row[2]) for keyword in keywords):
                    category_data[category].append(row.to_dict())
                    break
            else:
                category_data['Other'].append(row.to_dict())
        return category_data


class GoogleSheetHandler:
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        self.gc = gspread.authorize(self.credentials)
        self.sheet = self.open_or_create_spreadsheet()

    def open_or_create_spreadsheet(self):
        try:
            return self.gc.open(SPREADSHEET_NAME)
        except gspread.exceptions.SpreadsheetNotFound:
            return self.gc.create(SPREADSHEET_NAME)

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




class FileUploader:
    def __init__(self, category_sorter, sheet_handler):
        self.category_sorter = category_sorter
        self.sheet_handler = sheet_handler
        # Load the worksheet name from the .env file
        self.worksheet_name = os.getenv('WORKSHEET_NAME')

    def upload_file(self):
        # Open file dialog to select a CSV file
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Categorize data
        category_data = self.category_sorter.categorize_data(df)

        # Use the worksheet name from the .env file
        if self.worksheet_name:
            worksheet = self.sheet_handler.get_worksheet(self.worksheet_name)
            if worksheet:
                self.sheet_handler.update_worksheet(worksheet, category_data)
        else:
            print("No worksheet name found in .env file.")


# Main execution
if __name__ == "__main__":
    category_sorter = CategorySorter()
    sheet_handler = GoogleSheetHandler()
    file_uploader = FileUploader(category_sorter, sheet_handler)

    # Create a GUI window with a button to upload the CSV file
    root = tk.Tk()
    upload_button = tk.Button(root, text="Upload CSV file", command=file_uploader.upload_file)
    upload_button.pack()
    root.mainloop()
