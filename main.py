
from FileUploader import FileUploader

""" To use this code, go to the .env file and change the worksheet name to the month that you would
 to do finances for. First you have to create the worksheet in google sheets."""

# Main execution
if __name__ == "__main__":
    file_uploader = FileUploader()
    file_uploader.run()
