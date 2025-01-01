import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

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