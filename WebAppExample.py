import os, shutil
import pandas as pd

from flask import Flask, send_file, request, url_for
from werkzeug.utils import redirect

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Flask Button</title>
        </head>
        <body>
            <h1>Click Below to View PDF</h1>
            <form action="/downloads">
                <button type="submit">Download</button>
            </form>
            <h1>Click this button to upload CSV file for formatting</h1>
            <form action="/upload">
                <button type="submit">Upload</button>
            </form>
        </body>
    </html>
    '''


@app.route('/upload')
def upload_form():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload JSON and CSV</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #343a40; /* Dark gray background for the body */
            font-family: 'Lato', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white; /* White text for contrast */
            position: relative; /* To position the copyright at the bottom */
        }

        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            max-width: 600px;
            background-color: #495057; /* Darker gray for the form container */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        h1 {
            color: #f8f9fa; /* Light text color for the title */
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        .form-label {
            font-weight: bold;
            font-size: 1rem;
            color: #f8f9fa; /* Light text color for labels */
        }

        .file-input-wrapper {
            display: flex;
            justify-content: center;
            width: 100%;
        }

        .form-control {
            height: 45px;
            width: 100%;
            margin-bottom: 15px;
            background-color: #6c757d; /* Darker background for inputs */
            border: 1px solid #ced4da; /* Light border for inputs */
            color: white; /* White text inside inputs */
        }

        .btn-upload {
            background-color: #28a745;
            color: white;
            font-size: 1.1rem;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background-color 0.3s ease, transform 0.2s ease;
            width: 100%;
        }

        .btn-upload:hover {
            background-color: #218838;
            transform: translateY(-2px);
        }

        .btn-upload:active {
            transform: translateY(0);
        }

        /* Footer copyright styling */
        .footer {
            position: absolute;
            bottom: 10px;
            text-align: center;
            width: 100%;
            font-size: 0.9rem;
            color: #f8f9fa;
        }

    </style>
</head>
<body>

<div class="container">
    <h3>Upload JSON and CSV then click the populate button to update your spreadsheet!</h3>

    <form action="/csv-formatting" method="post" enctype="multipart/form-data">
        <div class="mb-3">
            <label for="credentials" class="form-label">Upload Credentials (JSON):</label>
            <div class="file-input-wrapper">
                <input type="file" class="form-control" name="credentials" accept=".json" required />
            </div>
        </div>

        <div class="mb-3">
            <label for="data" class="form-label">Upload CSV:</label>
            <div class="file-input-wrapper">
                <input type="file" class="form-control" name="data" accept=".csv" required />
            </div>
        </div>

        <div class="mb-3">
            <label for="month">Select Month:</label>
            <select name="Month" required>
                <option value="Jan">January</option>
                <option value="Feb">February</option>
                <option value="Mar">March</option>
                <option value="Apr">April</option>
                <option value="May">May</option>
                <option value="Jun">June</option>
                <option value="Jul">July</option>
                <option value="Aug">August</option>
                <option value="Sep">September</option>
                <option value="Oct">October</option>
                <option value="Nov">November</option>
                <option value="Dec">December</option>
            </select>
            <br><br>
        </div>

        <button type="submit" class="btn-upload btn-lg">Populate</button>
    </form>
</div>

<div class="footer">
    &copy; 2025 Tynances. All rights reserved.
</div>

</body>
</html>

'''


@app.route('/csv-formatting', methods=['POST'])
def upload_files():
    # Get the files from the form
    credentials_file = request.files['credentials']
    data_file = request.files['data']
    month = request.form['Month']

    if not credentials_file or not data_file:
        return 'Both files are required', 400

    formatted_csv = format_csv(data_file)
    formatted_csv.to_csv('output.csv', index=False)
    print(month)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Upload Successful</title>
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {
                    background-color: #343a40; /* Dark gray background for the body */
                    font-family: 'Lato', sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: white; /* White text for contrast */
                    position: relative; /* To position the copyright at the bottom */
                }

                .container {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                    max-width: 600px;
                    background-color: #495057; /* Darker gray for the form container */
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }

                h1 {
                    color: #f8f9fa; /* Light text color for the title */
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                }

                .btn-return {
                    background-color: #007bff;
                    color: white;
                    font-size: 1.1rem;
                    padding: 10px 20px;
                    border-radius: 5px;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                    width: 100%;
                    margin-top: 20px;
                }

                .btn-return:hover {
                    background-color: #0056b3;
                    transform: translateY(-2px);
                }

                .footer {
                    position: absolute;
                    bottom: 10px;
                    text-align: center;
                    width: 100%;
                    font-size: 0.9rem;
                    color: #f8f9fa;
                }

            </style>
        </head>
        <body>

        <div class="container">
            <h1>Success!</h1>
            <p>The files have been uploaded and processed successfully.</p>
            <p>The CSV file has been formatted and saved.</p>
            <a href="/upload" class="btn-return">Return to Upload</a>
        </div>

        <div class="footer">
            &copy; 2025 Tynances. All rights reserved.
        </div>

        </body>
        </html>
    '''


@app.route('/downloads')
def download_file():
    return send_file("test.pdf", as_attachment=True)


def format_csv(file):
    # input file

    # Read the CSV into dataframe
    df = pd.read_csv(file, skiprows=3)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
