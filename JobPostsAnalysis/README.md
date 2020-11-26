JobPostsAnalysis
==============================

NLP analysis of Indeed job posts

# Job Post Analysis

  It is within the nature of the tech industry to continuously renew itself. It is of vital importance that businesses capitalize on the new trend to prosper and disrupt the status quo. This principle also applies to tech employees. The ability to capitalize on the new trend will reward them highly. Covid-19 brings about unparalleled challenges to the U.S economy as the whole and to the tech industry in particular. How do tech job seekers prosper during this difficult time? One way to capture and take advantage of the new trend in tech is to analyze companies' behavior. One important aspect is their hiring practices. I'll be performing text analysis of job postings from Indeed to see the trend in tech industry by states in the U.S

# Data

  Data is scraped directly from [Indeed](https://www.indeed.com/) using BeautifulSoup and Python. The data include two files. The IndeedJobPosts.csv file contains information about job title, company name, location and the url link for job description. The JobDescription contains information about the job description for each url link from the IndeedJobPosts.csv. The job postings are scraped within a valid time period defined by Indeed (jobs that are still valid).

# Requirements

Run the following commands to setup environment (make sure Anaconda is installed)

> make create_environment

Activate the environment

> conda activate JobPostsAnalysis

Run script to scrape from Indeed

> make Indeedscrape

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. 
    │   └── JobPostsAnalysis <- analyzing job posts from Indeed
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── async <- in progress 
    │   │   └── sequential < scripts to sequentially scrape job posts from Indeed
    │   │        └── IndeedCrawler.py <- main script to crawl job posts from Indeed 
    |   |       
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── text_normalize <- feature preprocessing text scripts
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
