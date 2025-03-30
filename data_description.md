# IMDb Non-Commercial Datasets

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
