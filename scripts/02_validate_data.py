import pandas as pd
import re
from pathlib import Path

# ---------------------------------------------------------
# 02_validate_data.py
# Purpose:
# Validate the raw dataset and generate a data quality report.
# The script checks missing values, duplicate records, invalid
# emails, out-of-range ages, invalid percentages and date issues.
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "messy_participants.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTPUT_DIR / "data_quality_report.md"
SUMMARY_PATH = OUTPUT_DIR / "validation_summary.csv"

df = pd.read_csv(RAW_PATH)

def is_valid_email(value):
    if pd.isna(value) or str(value).strip() == "":
        return False
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, str(value).strip()))

def parse_date_flexible(value):
    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT
    parsed = pd.to_datetime(value, errors="coerce", dayfirst=False)
    if pd.isna(parsed):
        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
    return parsed

checks = []

# 1. Row count
checks.append({
    "check": "Total rows",
    "issue_count": len(df),
    "description": "Total number of rows in the raw dataset."
})

# 2. Missing values by column
for column in df.columns:
    missing_count = df[column].isna().sum() + (df[column].astype(str).str.strip() == "").sum()
    checks.append({
        "check": f"Missing values - {column}",
        "issue_count": int(missing_count),
        "description": f"Number of missing or blank values in {column}."
    })

# 3. Fully duplicated rows
checks.append({
    "check": "Fully duplicated rows",
    "issue_count": int(df.duplicated().sum()),
    "description": "Rows that are exact duplicates across all columns."
})

# 4. Duplicated participant IDs
checks.append({
    "check": "Duplicated participant_id",
    "issue_count": int(df["participant_id"].duplicated().sum()),
    "description": "Records with repeated participant identifiers."
})

# 5. Invalid emails
invalid_email_count = (~df["email"].apply(is_valid_email)).sum()
checks.append({
    "check": "Invalid emails",
    "issue_count": int(invalid_email_count),
    "description": "Emails that do not follow a valid email format."
})

# 6. Age out of expected range
age_numeric = pd.to_numeric(df["age"], errors="coerce")
invalid_age_count = ((age_numeric < 17) | (age_numeric > 65) | age_numeric.isna()).sum()
checks.append({
    "check": "Invalid age",
    "issue_count": int(invalid_age_count),
    "description": "Ages below 17, above 65 or non-numeric."
})

# 7. Invalid percentages and scores
attendance_numeric = pd.to_numeric(df["attendance_pct"], errors="coerce")
invalid_attendance_count = ((attendance_numeric < 0) | (attendance_numeric > 100) | attendance_numeric.isna()).sum()
checks.append({
    "check": "Invalid attendance_pct",
    "issue_count": int(invalid_attendance_count),
    "description": "Attendance values below 0, above 100 or non-numeric."
})

score_numeric = pd.to_numeric(df["final_score"], errors="coerce")
invalid_score_count = ((score_numeric < 0) | (score_numeric > 100) | score_numeric.isna()).sum()
checks.append({
    "check": "Invalid final_score",
    "issue_count": int(invalid_score_count),
    "description": "Final scores below 0, above 100 or non-numeric."
})

# 8. Invalid dates
start_dates = df["start_date"].apply(parse_date_flexible)
end_dates = df["end_date"].apply(parse_date_flexible)

invalid_start_dates = start_dates.isna().sum()
invalid_end_dates = end_dates.isna().sum()
end_before_start = (end_dates < start_dates).sum()

checks.append({
    "check": "Invalid start_date",
    "issue_count": int(invalid_start_dates),
    "description": "Start dates that could not be parsed."
})

checks.append({
    "check": "Invalid end_date",
    "issue_count": int(invalid_end_dates),
    "description": "End dates that could not be parsed."
})

checks.append({
    "check": "End date before start date",
    "issue_count": int(end_before_start),
    "description": "Records where end_date occurs before start_date."
})

summary = pd.DataFrame(checks)
summary.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

with open(REPORT_PATH, "w", encoding="utf-8") as report:
    report.write("# Data Quality Report\n\n")
    report.write("This report summarizes the main data quality issues detected in the raw synthetic dataset.\n\n")

    report.write("## Dataset overview\n\n")
    report.write(f"- Source file: `data/raw/messy_participants.csv`\n")
    report.write(f"- Total rows: {len(df)}\n")
    report.write(f"- Total columns: {len(df.columns)}\n\n")

    report.write("## Validation checks\n\n")
    report.write("| Check | Issue count | Description |\n")
    report.write("|---|---:|---|\n")

    for _, row in summary.iterrows():
        report.write(f"| {row['check']} | {row['issue_count']} | {row['description']} |\n")

    report.write("\n## Main findings\n\n")
    report.write("- The dataset contains duplicated records and duplicated participant identifiers.\n")
    report.write("- Several categorical variables use inconsistent labels.\n")
    report.write("- Some emails are missing or invalid.\n")
    report.write("- Some numeric fields contain invalid values or text values.\n")
    report.write("- Date fields use mixed formats and require standardization.\n\n")

    report.write("## Recommended cleaning actions\n\n")
    report.write("- Remove exact duplicate rows.\n")
    report.write("- Keep one record per participant identifier.\n")
    report.write("- Standardize categorical variables such as state, gender, status and education level.\n")
    report.write("- Convert numeric fields to consistent numeric formats.\n")
    report.write("- Standardize dates to ISO format: YYYY-MM-DD.\n")
    report.write("- Document all transformation rules in a data dictionary.\n")

print(f"Validation summary created at: {SUMMARY_PATH}")
print(f"Data quality report created at: {REPORT_PATH}")