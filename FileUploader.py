import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
from GoogleSheetHandler import GoogleSheetHandler
from CategorySorter import CategorySorter

class FileUploader:
    def __init__(self):
        self.category_sorter = CategorySorter()
        # Load the worksheet name from the .env file
        self.worksheet_name = os.getenv('WORKSHEET_NAME')

        self.csvFilePath = ""
        self.credentials_path = ""

        self.window = tk.Tk()
        self.window.title("Tynances")
        self.window.geometry("300x300")

       
        
        #CSV Filepath TextBox
        self.csv_text_box = tk.Entry(self.window, width=30)
        self.csv_text_box.pack(pady=10)

         # Upload CSV Button
        self.upload_csv_button = tk.Button(self.window, width=30, text="Upload CSV File", command=self.on_choose_csv)
        self.upload_csv_button.pack(pady=10)

        # Credentials Filepath Text Box
        self.credentials_path_text_box = tk.Entry(self.window, width=30)
        self.credentials_path_text_box.pack(pady=10)

        #Get Credentials Button
        self.get_credentials_button = tk.Button(self.window, width=30, text="Upload Credentials JSON", command=self.on_get_credentials_json)
        self.get_credentials_button.pack(pady=10)

        # Do The Thing button
        self.action_button = tk.Button(self.window, width=30, text="Populate Sheet", command=self.on_populate_sheet)
        self.action_button.pack(pady=10)

    def on_choose_csv(self):
        filepath = filedialog.askopenfilename()
        if(os.path.exists(filepath)):
            self.csvFilePath = filepath
            self.csv_text_box.insert(0, filepath)

    def on_get_credentials_json(self):
        filepath = filedialog.askopenfilename()
        if(os.path.exists(filepath)):
            self.credentials_path = filepath
            self.credentials_path_text_box.insert(0, filepath)

    def on_populate_sheet(self):
        # Read the CSV file
        df = pd.read_csv(self.csvFilePath)

        # Categorize data
        category_data = self.category_sorter.categorize_data(df)

        sheet_handler = GoogleSheetHandler(self.credentials_path)

        # Use the worksheet name from the .env file
        if self.worksheet_name:
            worksheet = sheet_handler.get_worksheet(self.worksheet_name)
            if worksheet:
                sheet_handler.update_worksheet(worksheet, category_data)
        else:
            print("No worksheet name found in .env file.")

    def run(self):
        self.window.mainloop()