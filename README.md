# 1. Context
---
In this project, we will work at a media company that is assembling a new product squad. The goal of this squad is to start working on marketing campaigns based on movie releases. For this purpose, we will need to understand some consumption behaviors of users engaging with this type of media and the market trends. One of the suggestions made by the product team was exploring IMDb data.

# 2. Possible dimensions for analysis
---
- Volume of releases per year;
- Releases by language;
- Release trend by genre;
- Number of participants per release;
- Number of genres in which each participant works;
- Most frequent genres by type of release;
- Average rating by genre over the years.

# 3. Data structures
---
Create two tables that will provide informations in BI. They'll have these main columns:

1. **Realese table:** release, type of release, year, language, genre, number of participants, avg rating

2. **Participant table:** participant, genre

# 4. Data description: IMDb Non-Commercial Datasets
---
Subsets of IMDb data are available for access to customers for personal and non-commercial use. You can hold local copies of this data, and it is subject to our **terms and conditions**. Please refer to the **Non-Commercial Licensing** and verify compliance.

The link of data description is here: [https://developer.imdb.com/non-commercial-datasets/](https://developer.imdb.com/non-commercial-datasets/).

## Data Location
The dataset files can be accessed and downloaded from [https://datasets.imdbws.com/](https://datasets.imdbws.com/). The data is refreshed daily.

## IMDb Dataset Details
Each dataset is contained in a gzipped, tab-separated-values (**TSV**) formatted file in the **UTF-8** character set. The first line in each file contains **headers** that describe what is in each column. A `\N` is used to denote that a particular field is missing or null for that title/name.

### The available datasets are as follows:

#### **title.akas.tsv.gz**
- `titleId` (string) - a tconst, an alphanumeric unique identifier of the title.
- `ordering` (integer) – a number to uniquely identify rows for a given `titleId`.
- `title` (string) – the localized title.
- `region` (string) - the region for this version of the title.
- `language` (string) - the language of the title.
- `types` (array) - enumerated set of attributes like "dvd", "festival", "tv", etc.
- `attributes` (array) - additional terms to describe this alternative title.
- `isOriginalTitle` (boolean) – 0: not original title; 1: original title.

#### **title.basics.tsv.gz**
- `tconst` (string) - alphanumeric unique identifier of the title.
- `titleType` (string) – the type/format of the title (e.g., movie, series, episode).
- `primaryTitle` (string) – the popular title/promotional title.
- `originalTitle` (string) - original title in the original language.
- `isAdult` (boolean) - 0: non-adult title; 1: adult title.
- `startYear` (YYYY) – release year or series start year.
- `endYear` (YYYY) – series end year (only for series).
- `runtimeMinutes` - primary runtime in minutes.
- `genres` (array) – up to three genres associated with the title.

#### **title.crew.tsv.gz**
- `tconst` (string) - alphanumeric unique identifier of the title.
- `directors` (array) - director(s) of the title.
- `writers` (array) – writer(s) of the title.

#### **title.episode.tsv.gz**
- `tconst` (string) - episode identifier.
- `parentTconst` (string) - parent series identifier.
- `seasonNumber` (integer) – season number.
- `episodeNumber` (integer) – episode number.

#### **title.principals.tsv.gz**
- `tconst` (string) - alphanumeric unique identifier of the title.
- `ordering` (integer) – a number to uniquely identify rows.
- `nconst` (string) - alphanumeric unique identifier of the person.
- `category` (string) - the category of the work (e.g., actor, director).
- `job` (string) - specific job title, if applicable.
- `characters` (string) - name of the character portrayed.

#### **title.ratings.tsv.gz**
- `tconst` (string) - alphanumeric unique identifier of the title.
- `averageRating` – weighted average of all individual ratings.
- `numVotes` - number of votes received by the title.

#### **name.basics.tsv.gz**
- `nconst` (string) - alphanumeric unique identifier of the person.
- `primaryName` (string) – most credited name of the person.
- `birthYear` – in YYYY format.
- `deathYear` – in YYYY format, if applicable.
- `primaryProfession` (array) – top 3 professions of the person.
- `knownForTitles` (array of tconsts) – titles the person is known for.

# 5. Files
---
1. I 've started the ETL tests on `automation_etl_imdb.ipynb`
2. I've done a python script (`etl_imdb.py`) to put in production all the ETL process
3. I've used **Github Actions** to schedule at 06:00AM the new data ingestion on `imdb_data.db`
    - I've created the `requirements.txt` to install all the dependencies with GA
    - I've created the `data_pipeline.yml` to configure GA

**Observation:** in the `etl_imdb.py` file, to get all the dataframe rows, it is necessary to delete the argument `n_rows` on pandas `read_csv` (`transform` function). I just push 1.000 rows because of Github Actions, it doesn't support large files in the server! It is a next improve, **make all the ETL process on another platform**, maybe **Apache Airflow** or some other orquestration app.