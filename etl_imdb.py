### IMPORTS
import os
import sqlite3
import logging
import requests
import pandas as pd

# Logging config
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

#log_format: Defines the format of log messages, including:
#
#   - %(asctime)s: Timestamp (when the message was logged).
#
#   - %(levelname)s: Log level (DEBUG, INFO, WARNING, etc.).
#
#   - %(message)s: The actual message.
#
#logging.basicConfig(): Sets the log detail level to DEBUG and applies the defined format.


# Add a handler for files
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script_logs.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

#log_file_path: Sets the absolute path of the file where the logs will be saved (script_logs.log) in the same directory as the script.
#
#FileHandler: Creates a file handler that logs the messages to the specified file.
#
#setLevel(logging.DEBUG): Sets the minimum level of messages that will be logged to the file.
#
#setFormatter: Applies the same log format to the file, using log_format.
#
#addHandler: Adds the file handler to the main logger so that the logs are written to both the console and the file.


# Local folder
DATA_PATH = 'data'
PREPROCESSED_DATA_PATH = os.path.join(DATA_PATH, 'preprocessed')

# URL
DB_URL = 'https://datasets.imdbws.com/'

# DB
DB = 'imdb_data.db'

# File names from URL
GZ_FILES = [
    'name.basics.tsv.gz',
    'title.akas.tsv.gz',
    'title.basics.tsv.gz',
    'title.crew.tsv.gz',
    'title.episode.tsv.gz',
    'title.principals.tsv.gz',
    'title.ratings.tsv.gz'
]




def extract(
        db_url: str = DB_URL,
        data_path: str = DATA_PATH,
        files: list = GZ_FILES
) -> None:
    """
    TODO: Docstring.
    """

    os.makedirs(data_path, exist_ok=True)

    for file in files:
        url = db_url + file
        local_path = os.path.join(data_path, file)

        if not os.path.exists(local_path):
            logging.info(f'Downloading {file}...')
            response = requests.get(url)

            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                logging.info(f'{file} downloaded!')
            else:
                logging.error(f'Download failed... Status code: {response.status_code}')
            
            del response

        else:
            logging.info(f'{file} already exists. The process will continue.')

    logging.info('All downloads were concluded!')




def transform(
        data_path: str = DATA_PATH,
        preprocessed_data_path: str = PREPROCESSED_DATA_PATH,
        files: list = GZ_FILES
) -> None:
    """
    TODO: Docstring.
    """

    os.makedirs(preprocessed_data_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(data_path, file)

        if os.path.isfile(file_path) and file.endswith('.gz'):
            logging.debug(f'Reading and preprocessing the file {file}...')

            df = pd.read_csv(
                file_path,
                sep='\t',
                compression='gzip',
                low_memory=False,
                nrows=1_000
            )

            df.replace({'\\N': None}, inplace=True)

            destiny_path = os.path.join(preprocessed_data_path, file[:-3]) # remove .gz extension
            df.to_csv(destiny_path, sep='\t', index=False)

            logging.debug(f'Preprocess concluded for {file}! File saved on {preprocessed_data_path}')

            os.remove(file_path)

    logging.info(f'All the files were preprocessed and downloaded on "preprocessed" directory!')




def load(
        conn,
        file_path: str = DATA_PATH,
        preprocessed_data_path: str = PREPROCESSED_DATA_PATH
) -> None:
    """
    TODO: Docstring.
    """

    files = os.listdir(preprocessed_data_path)

    for file in files:
        file_path = os.path.join(preprocessed_data_path, file)

        if os.path.isfile(file_path) and file.endswith('.tsv'):

            df = pd.read_csv(file_path, sep='\t', low_memory=False)

            table_name = os.path.splitext(file)[0]

            table_name = table_name.replace('.', '_').replace('-', '_')

            df.to_sql(table_name, conn, index=False, if_exists='replace')

            logging.info(f'File {file} was saved as table {table_name} and uploaded into the SQLite DB.')

    logging.info('All the files were saved into DB!')




def create_views(
        conn
) -> None:
    """
    TODO: Docstring.
    """

    analytics_titles = '''
    CREATE TABLE IF NOT EXISTS analytics_titles AS

    WITH principals AS (
        SELECT
            tconst,
            COUNT(DISTINCT nconst) AS numParticipants
        FROM title_principals
        GROUP BY 1
    ),

    languages AS (
        SELECT DISTINCT
            titleId AS tconst,
            language
        FROM title_akas
        WHERE language IS NOT NULL
    )

    SELECT DISTINCT
        tb.tconst,
        tb.titleType,
        tb.originalTitle,
        tb.startYear,
        tb.endYear,
        tb.genres,
        ta.language,
        tr.averageRating,
        tr.numVotes,
        tp.numParticipants
    FROM title_basics AS tb
    LEFT JOIN languages AS ta
        ON tb.tconst = ta.tconst
    LEFT JOIN title_ratings AS tr
        ON tb.tconst = tr.tconst
    LEFT JOIN principals AS tp
        ON tb.tconst = tp.tconst
    '''

    analytics_principals = '''
    CREATE TABLE IF NOT EXISTS analytics_principals AS

    SELECT DISTINCT
        tp.nconst,
        tp.tconst,
        tp.ordering,
        tp.category,
        tb.genres
    FROM title_principals AS tp
    LEFT JOIN title_basics AS tb
        ON tp.tconst = tb.tconst
    '''

    queries = [
        'DROP TABLE analytics_titles', # We have to drop existing tables
        'DROP TABLE analytics_principals',     # to update with new data
        analytics_titles,
        analytics_principals
        ]

    cursor = conn.cursor()

    for query in queries:

        cursor.execute(query)

    logging.info('Analytical tables were created succesfully!')
    logging.info('ETL finished!')




if __name__ == '__main__':

    extract()
    transform()

    conn = sqlite3.connect(DB)

    load(conn=conn)
    create_views(conn=conn)

    conn.close()

## Schedule the script execution
#schedule.every().day.at('09:00').do(execute_imdb_etl_script)
#
## Execute the script
#while True:
#    schedule.run_pending() # Verify pending tasks on schedule object
#    time.sleep(1) # Wait 1s