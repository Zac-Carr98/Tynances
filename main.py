import CategorySorter
import GoogleSheetHandler
import FileUploader
import tkinter as tk

""" To use this code, go to the .env file and change the worksheet name to the month that you would
 to do finances for. First you have to create the worksheet in google sheets."""

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
