### IMPORTS
import os
import requests
import pandas as pd
import sqlite3

### EXTRACT

# Download files

# URL
db_url = "https://datasets.imdbws.com/"

# File names from URL
files = [
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz"
]

# Local folder
data_path = "data"

# Check: path exists
os.makedirs(data_path, exist_ok=True)

# Download files
for file in files:
    url = db_url + file
    local_path = os.path.join(data_path, file)

    # If the file exists, then ignore, else download locally
    if not os.path.exists(local_path):
        print(f'Downloading {file}...')
        response = requests.get(url)

        # Request done? (status = 200)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f'{file} downloaded!')
        else:
            print(f'Download failed... Status code: {response.status_code}')
    else:
        print(f'{file} already exists.')

print('Download concluded!')

### TRANSFORM

# Directories
data_path = "data"
data_preprocessed_path = os.path.join(data_path, "preprocessed")

# Check: path exists
os.makedirs(data_preprocessed_path, exist_ok=True)

# Files
files = os.listdir(data_path)

# Open, preprocess and save data
for file in files:
    file_path = os.path.join(data_path, file)

    if os.path.isfile(file_path) and file.endswith('.gz'):
        print(f'Reading and preprocessing the file {file}...')

        # Read the file and transform to pandas
        df = pd.read_csv(file_path, sep='\t', compression='gzip', low_memory=False)

        # Replace "\\N" by NaN
        df.replace({'\\N': None}, inplace=True)

        # Save the DataFrame on preprocessed folder without compression
        destiny_path = os.path.join(data_preprocessed_path, file[:-3]) # remove .gz extension
        df.to_csv(destiny_path, sep='\t', index=False)

        print(f'Preprocess concluded for {file}! File saved on {data_preprocessed_path}')

print(f'All the files were preprocessed and downloaded on "preprocessed" directory!')

### LOAD RAW TABLES

# Save on DB using SQLite

# Directories
preprocessed_path = os.path.join("data", "preprocessed")
db = "imdb_data.db"

# Connect to SQLite DB
conn = sqlite3.connect(db)

# List all the saved files
files = os.listdir(preprocessed_path)

# Read and save the files into DB
for file in files:
    file_path = os.path.join(preprocessed_path, file)

    if os.path.isfile(file_path) and file.endswith('.tsv'):
        # Read the TSV file using pandas
        df = pd.read_csv(file_path, sep='\t', low_memory=False)

        # Remove extension from the file name
        table_name = os.path.splitext(file)[0]

        # Replace special characters in the file name
        table_name = table_name.replace('.', '_').replace('-', '_')

        # Save the DataFrame into DB
        df.to_sql(table_name, conn, index=False, if_exists='replace')

        print(f'File {file} was saved as table {table_name} and uploaded into the SQLite DB.')

# Close the connection with DB
conn.close()

print('All the files were saved into DB!')

### LOAD ANALYTICAL TABLES

analytics_titles = """
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
"""

analytics_principals = """
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
"""

# Lists of create table queries
create_table_queries = [analytics_titles, analytics_principals]

# DB name
db = 'imdb_data.db'

# Save tables into DB
create_table_queries_indexes = zip(
    create_table_queries,
    range(1, len(create_table_queries)) # Index for print
    )

for query, i in create_table_queries_indexes:

    # Connection to DB
    conn = sqlite3.connect(db)

    # Cursor
    cursor = conn.cursor()

    # Execute query
    cursor.execute(query)

    # Close connection
    conn.close()

    print(f'Analytical table {i} was created succesfully.')

print('Tables were created succesfully!')