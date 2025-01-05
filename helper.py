from GoogleSheetHandler import GoogleSheetHandler
from CategorySorter import CategorySorter
import pandas as pd
import os

def populate(df, worksheet_name, credentials_file):
        
    # Categorize data
    category_sorter = CategorySorter()
    category_data =category_sorter.categorize_data(df)

    sheet_handler = GoogleSheetHandler(credentials_file, worksheet_name)

    # Use the worksheet name from the .env file
    sheet_handler.update_worksheet(category_data)

def format_csv(csv_file):
        # input file

        # Read the CSV into dataframe
        df = pd.read_csv(csv_file, skiprows=3)

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

def execute(credentials_file, data_file, month):
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if not credentials_file or not data_file:
         return False
    
    credentials_path = os.path.join(UPLOAD_FOLDER, credentials_file.filename)
    credentials_file.save(credentials_path)
    
    formatted_csv = format_csv(data_file)

    populate(formatted_csv, month, credentials_path)
    
    os.remove(credentials_path)
    return True