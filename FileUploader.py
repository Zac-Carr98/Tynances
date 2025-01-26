import pandas as pd
import tkinter as tk
from tkinter.ttk import *
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
        self.window.geometry("375x120")
        
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

        # self.month_combo = Combobox(self.window, textvariable=self.worksheet_name)
        # self.month_combo['values'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # self.month_combo.grid(row=2, column=1)



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
        if not self.worksheet_name.get():
            print("No worksheet name given")
            return

        # Read the CSV file
        df = self.format_csv()

        # Categorize data
        category_data = self.category_sorter.categorize_data(df)

        sheet_handler = GoogleSheetHandler(self.credentials_path, self.worksheet_name.get())

        # Use the worksheet name from the .env file
        sheet_handler.update_worksheet(category_data)
            

    def run(self):
        self.window.mainloop()

    def format_csv(self):
        # input file

        # Read the CSV into dataframe
        df = pd.read_csv(self.csvFilePath, skiprows=3)

        # Drop first transaction number column
        df = df.drop(df.columns[0], axis=1)

        # Check column 5 for values
        positive = df.iloc[:, 4] > 0

        # Shift column 5 values into column 4
        df.loc[positive, df.columns[3]] = df.loc[positive, df.columns[4]]

        # Delete last 4 columns
        deleted_columns = [4, 5, 6, 7]

        # Final dataframe to use
        return df.drop(df.columns[deleted_columns], axis=1)