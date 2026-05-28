# Capital One Post-Discover Integration Monitor

## Project Overview

This project analyzes Capital One's financial and credit-risk performance before and after the Discover acquisition. The goal is to build a practical analytics monitor that tracks whether the acquisition is expanding Capital One's credit card portfolio and revenue base while also identifying pressure from credit losses, integration costs, and profitability changes.

The project is designed as an end-to-end business analytics case using official Capital One quarterly financial supplement data from 2023 Q1 through 2026 Q1.

Instead of only creating charts, this project follows a structured analytics workflow:

1. Collect official quarterly financial data
2. Clean and validate the dataset
3. Build a local SQL database using DuckDB
4. Create reusable SQL analysis views
5. Answer business questions using SQL
6. Export scorecard tables
7. Generate static chart outputs
8. Build an interactive Streamlit dashboard

## Business Problem

Capital One completed the Discover acquisition in 2025. A major strategic question after the acquisition is whether the larger credit card portfolio creates stronger revenue growth while keeping credit risk, losses, and integration costs under control.

This project focuses on a monitoring-style question:

> After the Discover acquisition, how did Capital One's revenue, profitability, credit card loans, credit risk, and integration costs change?

## Key Metrics Tracked

The project tracks quarterly metrics including:

* Total net revenue
* Net income
* Diluted EPS
* Adjusted EPS
* Non-interest expense
* Provision for credit losses
* Net interest margin
* Efficiency ratio
* Credit card loans
* Net charge-off rate
* 30+ day delinquency rate
* Discover integration expense
* Discover amortization expense
* Marketing expense
* Operating expense

## Project Phases

Each quarter is labeled into one of three acquisition phases:

* Pre-Discover: quarters before the acquisition impact
* Transition: the acquisition close and major transition quarter
* Post-Discover: quarters after Discover results are included

This allows the analysis to compare performance before, during, and after the acquisition.

## Tools Used

* Python: data cleaning, validation, automation, and chart generation
* Pandas: data processing and transformation
* DuckDB: local SQL analytics database
* SQL: schema design, views, and business analysis queries
* Streamlit: interactive dashboard
* Plotly: interactive dashboard charts
* Matplotlib: static chart image generation
* Git and GitHub: version control and portfolio publishing

## Project Structure

```text
CapitalOne-Monitor/
│
├── app.py
├── README.md
├── executive_summary.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── capitalone_quarterly_raw.csv
│   │   └── source_tracker.csv
│   │
│   └── processed/
│       └── capitalone_quarterly_clean.csv
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_analysis_views.sql
│   └── 03_business_questions.sql
│
├── src/
│   ├── 01_clean_data.py
│   ├── 02_quality_checks.py
│   ├── 03_build_database.py
│   ├── 04_generate_scorecard.py
│   ├── 05_generate_charts.py
│   └── 06_export_summary_tables.py
│
└── outputs/
    ├── charts/
    │   ├── 01_revenue_net_income_trend.png
    │   ├── 02_credit_card_loans_trend.png
    │   ├── 03_provision_to_revenue_pressure.png
    │   ├── 04_credit_risk_rates_trend.png
    │   └── 05_discover_cost_pressure.png
    │
    └── tables/
        ├── phase_summary.csv
        ├── quarterly_metrics.csv
        ├── risk_pressure_top_quarters.csv
        └── discover_cost_pressure.csv
```

## Data Source

The dataset was manually compiled from official Capital One quarterly financial supplement PDFs available through Capital One Investor Relations.

The project uses quarterly data from:

* 2023 Q1 to 2026 Q1
* Capital One financial supplement tables
* Consolidated financial summary
* Selected metrics
* Loan information and performance statistics
* Non-GAAP adjusted EPS reconciliation

## Data Pipeline

### 1. Raw Data Collection

The raw quarterly dataset is stored in:

```text
data/raw/capitalone_quarterly_raw.csv
```

The source tracker is stored in:

```text
data/raw/source_tracker.csv
```

### 2. Data Cleaning

The cleaning script is:

```text
src/01_clean_data.py
```

It performs the following steps:

* Reads the raw CSV
* Converts date columns
* Converts financial fields to numeric values
* Adds year and quarter fields
* Sorts the dataset from oldest to newest
* Saves the cleaned file to `data/processed/`

Run:

```bash
python3 src/01_clean_data.py
```

### 3. Data Quality Checks

The quality check script is:

```text
src/02_quality_checks.py
```

It checks:

* Correct row count
* Required columns
* Missing values
* Duplicate quarters
* Valid acquisition phase labels
* Valid Capital One source URLs
* Placeholder text
* Unexpected negative values
* Correct date ordering

Run:

```bash
python3 src/02_quality_checks.py
```

### 4. Build DuckDB Database

The database build script is:

```text
src/03_build_database.py
```

It creates a local DuckDB database and loads the cleaned quarterly data into a table called:

```text
capitalone_quarterly
```

Run:

```bash
python3 src/03_build_database.py
```

### 5. SQL Analysis Layer

SQL files are stored in:

```text
sql/
```

The SQL layer includes:

* `01_create_tables.sql`: documents the table schema
* `02_analysis_views.sql`: creates reusable analysis views
* `03_business_questions.sql`: contains business-facing SQL queries

Key views:

```text
v_capitalone_metrics
v_phase_summary
```

### 6. Scorecard Tables

The scorecard script is:

```text
src/04_generate_scorecard.py
```

It exports analysis-ready CSV tables into:

```text
outputs/tables/
```

Run:

```bash
python3 src/04_generate_scorecard.py
```

### 7. Static Charts

The chart generation script is:

```text
src/05_generate_charts.py
```

It creates PNG charts in:

```text
outputs/charts/
```

Run:

```bash
python3 src/05_generate_charts.py
```

### 8. Streamlit Dashboard

The interactive dashboard is built in:

```text
app.py
```

Run:

```bash
python3 -m streamlit run app.py
```

Note: Running Streamlit with `python3 -m streamlit` ensures the app uses the project virtual environment.

## Dashboard Features

The Streamlit dashboard includes:

* Latest quarter KPI cards
* Latest revenue and net income
* Post-Discover vs Pre-Discover revenue lift
* Phase-level business summary table
* Revenue and net income trend
* Credit card loan growth trend
* Provision-to-revenue pressure trend
* Net charge-off and delinquency rate trend
* Discover integration cost pressure analysis
* Risk pressure table

## Key Insights

### 1. Revenue increased after the Discover acquisition

Average quarterly revenue increased from about $9.5B in the Pre-Discover phase to about $15.4B in the Post-Discover phase.

### 2. The transition quarter created major profitability pressure

2025 Q2 had a large net loss and the highest provision-to-revenue pressure in the dataset. This makes it the key quarter to monitor when studying acquisition-related risk and accounting impact.

### 3. Credit card loans expanded sharply

Credit card loans increased significantly after Discover was included, showing the portfolio expansion effect of the acquisition.

### 4. Credit risk needs continued monitoring

Net charge-off and delinquency rates remained important indicators after the acquisition. The project highlights the need to monitor whether higher revenue growth is being achieved without creating excessive credit risk.

### 5. Discover-related costs became a visible performance driver

Integration and amortization expenses became meaningful after the acquisition and should be tracked separately from normal operating performance.

## Business Recommendation

Capital One should monitor the post-Discover portfolio through a recurring quarterly scorecard focused on:

* Revenue growth
* Net income recovery
* Credit card loan growth
* Net charge-off rate
* 30+ day delinquency rate
* Provision-to-revenue ratio
* Discover integration and amortization cost pressure

The key recommendation is not only to track whether the acquisition increases revenue, but also whether risk and integration costs normalize over time.

## How to Run the Project

After cloning the repository, create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full project pipeline:

```bash
python3 src/01_clean_data.py
python3 src/02_quality_checks.py
python3 src/03_build_database.py
python3 src/04_generate_scorecard.py
python3 src/05_generate_charts.py
```

Launch the dashboard:

```bash
python3 -m streamlit run app.py
```

## Why This Project Matters

This project demonstrates a practical business analytics workflow that connects financial reporting, credit-risk monitoring, SQL analysis, and dashboarding.

It is especially relevant for analyst roles because it shows the ability to:

* Work with official financial data
* Create a clean and traceable dataset
* Build an ETL-style pipeline
* Perform data quality checks
* Use SQL for business analysis
* Create reusable metrics and views
* Build executive-facing dashboards
* Translate numbers into business recommendations
