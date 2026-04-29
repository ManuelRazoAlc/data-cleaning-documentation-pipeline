import pandas as pd
import numpy as np
import re
from pathlib import Path

# ---------------------------------------------------------
# 03_clean_data.py
# Purpose:
# Clean and standardize the raw synthetic dataset.
# Outputs:
# - clean_participants.csv
# - data_dictionary.csv
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "messy_participants.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_PATH = PROCESSED_DIR / "clean_participants.csv"
DICTIONARY_PATH = BASE_DIR / "data" / "data_dictionary.csv"

df = pd.read_csv(RAW_PATH)

# -----------------------------
# Helper functions
# -----------------------------

def clean_text(value):
    if pd.isna(value):
        return np.nan
    value = str(value).strip()
    if value == "":
        return np.nan
    return value

def is_valid_email(value):
    if pd.isna(value) or str(value).strip() == "":
        return False
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, str(value).strip()))

def standardize_state(value):
    value = clean_text(value)
    if pd.isna(value):
        return np.nan

    mapping = {
        "CDMX": "Ciudad de México",
        "Ciudad de México": "Ciudad de México",
        "Cd. México": "Ciudad de México",
        "Estado de México": "Estado de México",
        "EdoMex": "Estado de México",
        "Jalisco": "Jalisco",
        "Nuevo León": "Nuevo León",
        "Puebla": "Puebla",
        "Oaxaca": "Oaxaca",
        "Chiapas": "Chiapas",
        "Yucatán": "Yucatán"
    }

    return mapping.get(value, value)

def standardize_gender(value):
    value = clean_text(value)
    if pd.isna(value):
        return "Not specified"

    value_lower = value.lower()

    if value_lower in ["f", "female", "mujer"]:
        return "Female"
    if value_lower in ["m", "male", "hombre"]:
        return "Male"
    if value_lower in ["no especificado", "not specified"]:
        return "Not specified"

    return "Not specified"

def standardize_education(value):
    value = clean_text(value)
    if pd.isna(value):
        return "Not specified"

    mapping = {
        "Secundaria": "Secondary",
        "Preparatoria": "High school",
        "Bachillerato": "High school",
        "Licenciatura": "Undergraduate",
        "Universidad": "Undergraduate",
        "Posgrado": "Graduate"
    }

    return mapping.get(value, "Not specified")

def standardize_status(value):
    value = clean_text(value)
    if pd.isna(value):
        return "Unknown"

    value_lower = value.lower()

    if value_lower == "completed":
        return "Completed"
    if value_lower == "in progress":
        return "In progress"
    if value_lower in ["dropped", "abandoned"]:
        return "Dropped"

    return "Unknown"

def standardize_yes_no(value):
    value = clean_text(value)
    if pd.isna(value):
        return "Unknown"

    value_lower = value.lower()

    if value_lower in ["yes", "sí", "si"]:
        return "Yes"
    if value_lower == "no":
        return "No"

    return "Unknown"

def parse_money(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    if value in ["", "N/A", "NA", "nan"]:
        return np.nan

    value = value.replace("$", "").replace(",", "")

    try:
        return float(value)
    except ValueError:
        return np.nan

def parse_date(value):
    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()
    if value == "":
        return pd.NaT

    parsed = pd.to_datetime(value, errors="coerce", dayfirst=False)

    if pd.isna(parsed):
        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)

    return parsed

# -----------------------------
# Cleaning process
# -----------------------------

# Remove exact duplicate rows
df = df.drop_duplicates()

# Keep first record per participant_id
df = df.drop_duplicates(subset=["participant_id"], keep="first")

# Clean text fields
text_columns = [
    "participant_id", "full_name", "email", "state", "gender",
    "education_level", "program", "status", "employed_before",
    "employed_after"
]

for col in text_columns:
    df[col] = df[col].apply(clean_text)

# Validate email
df["email_valid"] = df["email"].apply(is_valid_email)
df.loc[~df["email_valid"], "email"] = np.nan

# Standardize categorical variables
df["state"] = df["state"].apply(standardize_state)
df["gender"] = df["gender"].apply(standardize_gender)
df["education_level"] = df["education_level"].apply(standardize_education)
df["status"] = df["status"].apply(standardize_status)
df["employed_before"] = df["employed_before"].apply(standardize_yes_no)
df["employed_after"] = df["employed_after"].apply(standardize_yes_no)

# Convert numeric variables
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df.loc[(df["age"] < 17) | (df["age"] > 65), "age"] = np.nan

df["attendance_pct"] = pd.to_numeric(df["attendance_pct"], errors="coerce")
df.loc[(df["attendance_pct"] < 0) | (df["attendance_pct"] > 100), "attendance_pct"] = np.nan

df["final_score"] = pd.to_numeric(df["final_score"], errors="coerce")
df.loc[(df["final_score"] < 0) | (df["final_score"] > 100), "final_score"] = np.nan

df["income_before"] = df["income_before"].apply(parse_money)
df["income_after"] = df["income_after"].apply(parse_money)

df["satisfaction_score"] = pd.to_numeric(df["satisfaction_score"], errors="coerce")
df.loc[(df["satisfaction_score"] < 1) | (df["satisfaction_score"] > 5), "satisfaction_score"] = np.nan

# Parse dates
df["start_date"] = df["start_date"].apply(parse_date)
df["end_date"] = df["end_date"].apply(parse_date)

# Remove invalid date logic
df.loc[df["end_date"] < df["start_date"], "end_date"] = pd.NaT

# Create derived variables
df["program_duration_days"] = (df["end_date"] - df["start_date"]).dt.days
df["income_change"] = df["income_after"] - df["income_before"]

df["employment_change"] = np.where(
    (df["employed_before"] == "No") & (df["employed_after"] == "Yes"),
    "Entered employment",
    np.where(
        (df["employed_before"] == "Yes") & (df["employed_after"] == "Yes"),
        "Remained employed",
        np.where(
            (df["employed_before"] == "Yes") & (df["employed_after"] == "No"),
            "Lost employment",
            np.where(
                (df["employed_before"] == "No") & (df["employed_after"] == "No"),
                "Remained unemployed",
                "Unknown"
            )
        )
    )
)

# Format dates as YYYY-MM-DD
df["start_date"] = df["start_date"].dt.strftime("%Y-%m-%d")
df["end_date"] = df["end_date"].dt.strftime("%Y-%m-%d")

# Reorder columns
ordered_columns = [
    "participant_id",
    "full_name",
    "email",
    "email_valid",
    "state",
    "age",
    "gender",
    "education_level",
    "program",
    "start_date",
    "end_date",
    "program_duration_days",
    "status",
    "attendance_pct",
    "final_score",
    "employed_before",
    "employed_after",
    "employment_change",
    "income_before",
    "income_after",
    "income_change",
    "satisfaction_score"
]

df = df[ordered_columns]

# Save clean dataset
df.to_csv(CLEAN_PATH, index=False, encoding="utf-8-sig")

# Create data dictionary
dictionary = pd.DataFrame([
    ["participant_id", "Unique participant identifier", "Text", "Original field"],
    ["full_name", "Synthetic participant name", "Text", "Original field"],
    ["email", "Participant email. Invalid emails were set to missing.", "Text", "Cleaned field"],
    ["email_valid", "Indicates whether the original email had a valid format.", "Boolean", "Derived field"],
    ["state", "Participant state, standardized to consistent labels.", "Categorical", "Cleaned field"],
    ["age", "Participant age. Values outside 17-65 were set to missing.", "Numeric", "Cleaned field"],
    ["gender", "Standardized gender category.", "Categorical", "Cleaned field"],
    ["education_level", "Standardized education level.", "Categorical", "Cleaned field"],
    ["program", "Training program name.", "Categorical", "Original field"],
    ["start_date", "Program start date in YYYY-MM-DD format.", "Date", "Cleaned field"],
    ["end_date", "Program end date in YYYY-MM-DD format.", "Date", "Cleaned field"],
    ["program_duration_days", "Duration between start_date and end_date.", "Numeric", "Derived field"],
    ["status", "Standardized participant status.", "Categorical", "Cleaned field"],
    ["attendance_pct", "Attendance percentage. Values outside 0-100 were set to missing.", "Numeric", "Cleaned field"],
    ["final_score", "Final score. Values outside 0-100 were set to missing.", "Numeric", "Cleaned field"],
    ["employed_before", "Employment status before the program.", "Categorical", "Cleaned field"],
    ["employed_after", "Employment status after the program.", "Categorical", "Cleaned field"],
    ["employment_change", "Derived employment transition category.", "Categorical", "Derived field"],
    ["income_before", "Monthly income before the program.", "Numeric", "Cleaned field"],
    ["income_after", "Monthly income after the program.", "Numeric", "Cleaned field"],
    ["income_change", "Difference between income_after and income_before.", "Numeric", "Derived field"],
    ["satisfaction_score", "Participant satisfaction score from 1 to 5.", "Numeric", "Cleaned field"]
], columns=["variable", "description", "type", "notes"])

dictionary.to_csv(DICTIONARY_PATH, index=False, encoding="utf-8-sig")

print(f"Clean dataset created at: {CLEAN_PATH}")
print(f"Data dictionary created at: {DICTIONARY_PATH}")
print(f"Rows in clean dataset: {len(df)}")