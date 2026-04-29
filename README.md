# Data Cleaning and Documentation Pipeline

This project demonstrates a reproducible data cleaning, validation and documentation workflow using a synthetic dataset.

The dataset simulates common data quality issues found in real-world administrative databases, such as missing values, duplicated records, inconsistent categorical labels, invalid emails, mixed date formats and out-of-range numeric values.

## Objective

The objective of this project is to transform a raw and messy dataset into a clean, documented and analysis-ready dataset through a reproducible pipeline.

This project is especially relevant for data analysis, social impact evaluation, program monitoring, reporting and institutional data management.

## Project structure

```text
data-cleaning-documentation-pipeline/
│
├── data/
│   ├── raw/
│   │   └── messy_participants.csv
│   ├── processed/
│   │   └── clean_participants.csv
│   └── data_dictionary.csv
│
├── outputs/
│   ├── data_quality_report.md
│   └── validation_summary.csv
│
├── scripts/
│   ├── 01_generate_synthetic_data.py
│   ├── 02_validate_data.py
│   └── 03_clean_data.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Dataset description

The synthetic dataset represents participants from a social impact training program. It includes demographic, program participation, attendance, performance, employment, income and satisfaction variables.

The raw dataset intentionally contains data quality issues, including:

- Missing values
- Duplicated rows
- Duplicated participant IDs
- Invalid email formats
- Inconsistent state names
- Inconsistent gender labels
- Inconsistent education levels
- Mixed date formats
- Invalid numeric values
- Out-of-range percentages and scores

## Workflow

### 1. Generate synthetic raw data

The first script creates a synthetic dataset with intentional data quality issues.

```bash
python3 scripts/01_generate_synthetic_data.py
```

Output:

```text
data/raw/messy_participants.csv
```

### 2. Validate raw data

The second script scans the raw dataset and produces a data quality report.

```bash
python3 scripts/02_validate_data.py
```

Outputs:

```text
outputs/data_quality_report.md
outputs/validation_summary.csv
```

### 3. Clean and document the dataset

The third script cleans the dataset and creates a data dictionary.

```bash
python3 scripts/03_clean_data.py
```

Outputs:

```text
data/processed/clean_participants.csv
data/data_dictionary.csv
```

## Cleaning rules

The cleaning pipeline applies the following rules:

- Exact duplicate rows are removed.
- Duplicated participant IDs are reduced to one record.
- Invalid emails are identified and set to missing.
- State names are standardized.
- Gender labels are standardized.
- Education levels are standardized.
- Program status labels are standardized.
- Employment variables are standardized to `Yes`, `No` or `Unknown`.
- Numeric variables are converted to consistent numeric formats.
- Invalid age values outside the range 17-65 are set to missing.
- Attendance percentages outside 0-100 are set to missing.
- Final scores outside 0-100 are set to missing.
- Dates are parsed and standardized to `YYYY-MM-DD`.
- Derived variables are created for program duration, income change and employment transition.

## Main outputs

### Clean dataset

The clean dataset is located at:

```text
data/processed/clean_participants.csv
```

### Data dictionary

The data dictionary is located at:

```text
data/data_dictionary.csv
```

### Data quality report

The validation report is located at:

```text
outputs/data_quality_report.md
```

## Tools used

- Python
- pandas
- numpy
- Git
- GitHub


## Author

Manuel Razo Alcántara  
Actuarial Science student  
Facultad de Ciencias, UNAM