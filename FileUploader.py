import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
from GoogleSheetHandler import GoogleSheetHandler
from CategorySorter import CategorySorter

class FileUploader:
    def __init__(self):
        self.category_sorter = CategorySorter()
        self.csvFilePath = ""
        self.credentials_path = ""

        self.window = tk.Tk()
        self.window.title("Tynances")
        self.window.geometry("500x200")
        
        self.worksheet_name = tk.StringVar()
        #CSV Filepath TextBox
        tk.Label(self.window, text="CSV File Path: ").grid(row=0, column=0, sticky="w")
        self.csv_text_box = tk.Entry(self.window, width=30)
        self.csv_text_box.grid(row=0, column=1)
        self.upload_csv_button = tk.Button(self.window, text=" ... ", command=self.on_choose_csv).grid(row=0, column=2, padx=3)

        # Credentials Filepath
        tk.Label(self.window, text="Credentials JSON File Path: ").grid(row=1, column=0, sticky="w")
        self.credentials_path_text_box = tk.Entry(self.window, width=30)
        self.credentials_path_text_box.grid(row=1, column=1)
        self.get_credentials_button = tk.Button(self.window, text=" ... ", command=self.on_get_credentials_json).grid(row=1, column=2)

        # WorkSheet Name Text Box
        tk.Label(self.window, text="Worksheet Title: ").grid(row=2, column=0, sticky="w")
        self.worksheet_name_text_box = tk.Entry(self.window, width=30, textvariable=self.worksheet_name)
        self.worksheet_name_text_box.grid(row=2, column=1)

        # Do The Thing button
        self.action_button = tk.Button(self.window, width=30, text="Populate Sheet", command=self.on_populate_sheet).grid(row=3, column=0, columnspan=3)

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
            worksheet = sheet_handler.get_worksheet(self.worksheet_name.get())
            if worksheet:
                sheet_handler.update_worksheet(worksheet, category_data)
        else:
            print("No worksheet name found in .env file.")

    def run(self):
        self.window.mainloop()