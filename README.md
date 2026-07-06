# Airbnb Data Warehouse

## Project Overview

This project consists of building a complete Data Warehouse from Airbnb Paris public data.

The objective is to demonstrate the implementation of an ETL pipeline in Python, the construction of a Star Schema, data storage in SQLite, and the creation of an analytical dashboard using Power BI.

---

## Objectives

- Extract Airbnb datasets
- Clean and transform the data
- Build a dimensional model (Star Schema)
- Create fact and dimension tables
- Load the data into SQLite
- Visualize KPIs with Power BI

---

## Technologies

- Python
- Pandas
- SQLite
- Power BI
- Git & GitHub
## Project Structure

```text
Airbnb-DataWarehouse
│
├── Data/                # Raw Airbnb datasets
├── Images/              # Dashboard screenshots
├── Notebooks/           # Exploratory notebooks
├── Power BI/            # Power BI dashboard
├── sql/                 # SQL scripts
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── utils.py
│
├── Warehouse/           # Generated Data Warehouse
├── README.md
├── requirements.txt
└── .gitignore
```

## ETL Pipeline

The pipeline is divided into three main phases:

### Extract

- Read Airbnb CSV files
- Load data using Pandas

### Transform

- Clean missing values
- Convert dates
- Convert prices
- Build dimensions
- Build fact tables
- Generate surrogate keys

### Load

- Export CSV files
- Load all tables into SQLite

## Key Features

- Automated ETL pipeline
- Star Schema Data Warehouse
- Surrogate Keys
- Data Quality Checks
- SQLite Database
- Power BI Dashboard
- Modular Python Architecture

## How to Run

Clone the repository

```bash
git clone https://github.com/FatoumataMBALLO/Airbnb-DataWarehouse.git
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the ETL pipeline

```bash
python src/pipeline.py
```

## Dataset

The project uses the public Airbnb Paris dataset.

The original raw data is stored in the `Data/` folder.

The ETL pipeline cleans and transforms the raw files into a dimensional model stored in SQLite.

## Future Improvements

* Build an interactive Power BI dashboard
* Add incremental loading
* Add logging
* Add unit tests
* Deploy the pipeline using Docker

## Author

**Fatoumata MBALLO**

Data Analyst | Python | SQL | Power BI
