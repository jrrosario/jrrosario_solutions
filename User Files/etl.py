import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from datetime import datetime
import pytz
import os

def get_csv_file_path(file):
    """
    Get the full file path of a CSV file located in the same folder as the script.

    :param file: Name of the CSV file
    :return: Full file path of the CSV file
    :raises FileNotFoundError: If the file is not found in the directory
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(directory, file)
    if os.path.exists(file_path):
        return file_path
    else:
        raise FileNotFoundError(f"{file} not found in: {directory}")


conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS employee_check_in
(
    user TEXT,
    timestamp DATETIME,
    hours DECIMAL,
    project TEXT
)
'''
)
conn.commit()

csv_filepath = get_csv_file_path("dailycheckins.csv")
df = pd.read_csv(csv_filepath)

def parse_timestamp(timestamp):
    """
    Detect if a string timestamp is using Russian Language.
    Parse various timestamp formats and convert them to UTC.

    :param timestamp: Timestamp string in various formats
    :return: Parsed datetime object in UTC
    :raises ValueError: If the timestamp format is unrecognized
    """
    months_translation = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
    }

    for russian_month, english_month in months_translation.items():
        timestamp = timestamp.replace(russian_month, english_month)

    date_formats = [
        "%Y-%m-%d %H:%M:%S %Z",
        "%m/%d/%Y %I:%M %p",
        "%d %B %Y %H:%M",
        "%Y-%m-%d %H:%M:%S.%f %Z"
    ]

    for x in date_formats:
        try:
            dt = datetime.strptime(timestamp, x)
            if dt.tzinfo is not None:
                dt = dt.astimezone(pytz.UTC)
            return dt
        except ValueError:
            continue
    raise ValueError(f"Timestamp format not recognized: {timestamp}")

df['timestamp'] = df['timestamp'].apply(parse_timestamp)

df = df.groupby(['user', 'timestamp', 'project'], as_index=False)['hours'].sum()

engine = create_engine('sqlite:///employee.db')
df.to_sql('employee_check_in', con=engine, if_exists='replace', index=False)

result = pd.read_sql('SELECT * FROM employee_check_in', con=engine)

def read_data():
    """
    Read and display all data from the employee_check_in table in the SQLite database.

    :return: None
    """
    conn = sqlite3.connect('employee.db')
    query = "SELECT * FROM employee_check_in"
    df = pd.read_sql(query, conn)
    # print(df)
    conn.close()

print("Reading data from DB:")
read_data()

conn.close()
