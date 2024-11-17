import pandas as pd

def read_csv_data(filename):
    """
    Reads data from a CSV file and returns a pandas DataFrame.
    """
    try:
        data = pd.read_csv(filename)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found

def get_latest_data(filename, num_rows=1):
    """
    Reads the latest `num_rows` rows from the CSV file.
    """
    try:
        data = pd.read_csv(filename)
        return data.tail(num_rows)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame()
