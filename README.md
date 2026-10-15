# PulseIQ ETL Pipeline & Analytics Warehouse

An end-to-end data engineering project that extracts, validates, transforms, and loads HR and payroll data using Python, Pandas, Docker, and PostgreSQL.

The project implements an ETL pipeline and a dimensional data warehouse to support employee, attendance, leave, payroll, and department-level analytics.

## Project Overview

The project is organized into two main phases:

- **Task 1 – ETL Pipeline:** Extracts source CSV files, validates and transforms data, generates clean outputs, and records pipeline execution details.
- **Task 2 – Analytics Warehouse:** Uses PostgreSQL to store dimensional and fact tables for structured reporting and business analysis.

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Database:** PostgreSQL
- **ETL & Containerization:** Docker, Docker Compose
- **SQL:** Schema design, table relationships, analytical queries
- **Testing:** Python unittest
- **Version Control:** Git and GitHub

## Project Structure

```text
PulseIQ-ETL/
│
├── data/
│   ├── raw/                 # Source CSV files
│   ├── clean/               # Validated and cleaned data
│   └── processed/           # Processed CSV files and reports
│
├── docs/
│   └── schema_diagram.md    # Warehouse schema documentation
│
├── sql/
│   ├── schema.sql           # Warehouse table definitions
│   ├── analytics.sql        # Analytical SQL queries
│   └── fact_grain_checks.sql
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── main.py
│   └── validate_analytics.py
│
├── tests/
│   ├── test_etl.py
│   ├── test_docker.py
│   ├── test_metric_dictionary.py
│   └── test_warehouse.py
│
├── Dockerfile
├── compose.yaml
├── compose.task1-backup.yaml
├── requirements.txt
└── README.md
```

*Note: The structure above describes the intended organization of the project. Individual files may vary depending on the current implementation.*

## ETL Pipeline

The pipeline follows these steps:

1. **Extract:** Reads source CSV files.
2. **Validate:** Checks data structure, required fields, and data quality rules.
3. **Transform:** Cleans and prepares data for downstream use.
4. **Load:** Loads the prepared data into the target database.
5. **Log:** Records pipeline execution status and generates supporting reports.

### Run the ETL Pipeline

## How to Run the Project

### Prerequisites

Install the following tools before running the project:

- Python 3.11+
- Docker Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/visha2000/PulseIQ-ETL.git
cd PulseIQ-ETL
```

### 2. Build the Docker Image

```bash
docker compose build
```

### 3. Run the ETL Pipeline

```bash
docker compose run --rm etl
```

This command runs the ETL pipeline, which extracts, validates, transforms, and loads data according to the project configuration.

### 4. Check the Processed Data

In PowerShell:

```powershell
Get-ChildItem .\data\processed
```

Check the pipeline execution log:

```powershell
Get-Content .\data\processed\pipeline_run_log.csv
```

### 5. Run Unit Tests

```bash
python -m unittest discover -s tests -v
```

### 6. Validate the Analytics Warehouse

Run this command if the PostgreSQL service is configured and running:

```bash
docker compose run --rm etl python -m src.validate_analytics
```

### 7. View the Warehouse Tables

Connect to the PostgreSQL container:

```bash
docker compose exec postgres psql -U postgres -d postgres
```

Inside the PostgreSQL prompt, list the tables:

```sql
\dt
```

Exit PostgreSQL:

```sql
\q
```

**Note:** The PostgreSQL service name, username, database name, and container configuration must match `compose.yaml`. Update the connection command if your configuration uses different values.

## Data Quality and Validation

The pipeline is designed to support data-quality checks such as:

- Required column and field validation
- Missing-value checks
- Duplicate and key validation
- Date and numeric data parsing
- Validation of business rules
- Identification of rejected records
- Pipeline execution logging

The `data/clean/` directory stores cleaned datasets, while the `data/processed/` directory contains processed CSV files and reports.

## PostgreSQL Analytics Warehouse

Task 2 introduces a PostgreSQL dimensional warehouse to organize HR and payroll information for analytics.

### Dimension Tables

- `dim_employee`
- `dim_department`
- `dim_role`
- `dim_date`
- `dim_leave_type`
- `dim_location`

### Fact Tables

- `fact_attendance_monthly`
- `fact_payroll`
- `fact_leave`
- `fact_headcount_monthly`

The warehouse connects fact records to relevant dimensions using keys and relationships defined in the SQL schema.

### Warehouse Capabilities

The warehouse is designed to support analysis of:

- Employee headcount and workforce trends
- Monthly attendance and attendance rates
- Payroll costs and salary components
- Leave requests and leave trends
- Department-level payroll and cost comparisons

### SQL Files

- `sql/schema.sql` – Defines warehouse tables and relationships.
- `sql/analytics.sql` – Contains analytical SQL queries.
- `sql/fact_grain_checks.sql` – Supports fact-table grain validation.

## Metrics and Reporting

The project includes metric definitions and supporting CSV reports for consistent business analysis.

Example analytical measures include:

- Total gross payroll
- Total net payroll
- Employer payroll cost
- Attendance coverage rate
- Payroll budget variance
- Employee headcount trends

Metric calculations should follow the definitions and aggregation rules implemented in the project.

## Running Tests

Run the project tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks selected ETL outputs, Docker configuration, metric definitions, and warehouse SQL files.

**Note:** Run the tests after installing the required Python dependencies and ensure the expected data files and SQL scripts are available.

## Installation

To install the Python dependencies locally:

```bash
python -m pip install -r requirements.txt
```

For the Docker-based workflow, ensure Docker Desktop is running before executing the Compose commands.

## Learning Outcomes

This project demonstrates practical experience with:

- Building an ETL pipeline
- Data cleaning and validation
- Python-based data processing
- Docker-based execution
- PostgreSQL warehouse design
- Fact and dimension modeling
- SQL-based business analytics
- Test organization and GitHub project documentation

## Author

**Vishalachi A. G.**

GitHub: [visha2000](https://github.com/visha2000)

## License

Add a license file if this project is intended for public reuse. Ensure that source datasets are permitted to be shared before distributing them publicly.


