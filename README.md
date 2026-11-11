# Data cleaning, validation and documentation pipeline

A Python project that takes a messy participant database and turns it into a clean, documented dataset ready for analysis. I built it around problems that are common in administrative and program-monitoring data: duplicates, inconsistent labels, impossible values and mixed date formats.

## The data

The dataset is synthetic, so it can be shared. It simulates 265 records of participants from a social impact training program, with demographic, attendance, performance, employment, income and satisfaction variables. The first script generates it with the errors on purpose.

## What I did

- **Validation.** A script scans the raw file and writes a data quality report with every check and how many records fail it. Some of what it found:

  | Check | Records |
  |---|---:|
  | Fully duplicated rows | 10 |
  | Repeated participant IDs | 15 |
  | Invalid emails | 42 |
  | Ages outside 17–65 or non-numeric | 44 |
  | Attendance outside 0–100% | 44 |
  | Final scores outside 0–100 | 38 |
  | End date before start date | 6 |

- **Cleaning.** Clear rules applied in order: drop exact duplicates, keep one record per participant ID, standardize states, gender, education level and program status, convert numbers and dates to consistent formats (`YYYY-MM-DD`), and set impossible values to missing instead of guessing them.
- **Derived variables.** Program duration, change in income and change in employment status.
- **Documentation.** A data dictionary that describes all 22 variables of the clean dataset, with type and notes.

The result is a clean file with 250 participants, one row each.

## How it is organized

- `scripts/01_generate_synthetic_data.py`: creates the messy raw data.
- `scripts/02_validate_data.py`: runs the checks and writes [`outputs/data_quality_report.md`](outputs/data_quality_report.md) and `outputs/validation_summary.csv`.
- `scripts/03_clean_data.py`: applies the cleaning rules and writes `data/processed/clean_participants.csv` and `data/data_dictionary.csv`.

## How to reproduce it

You need Python 3:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/01_generate_synthetic_data.py
python3 scripts/02_validate_data.py
python3 scripts/03_clean_data.py
```

---

Manuel Razo Alcántara · [LinkedIn](https://www.linkedin.com/in/manuel-razo-alcantara) · Code under the [MIT License](LICENSE)
