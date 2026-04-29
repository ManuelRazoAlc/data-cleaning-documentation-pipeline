import pandas as pd
import numpy as np
import random
from pathlib import Path

# ---------------------------------------------------------
# 01_generate_synthetic_data.py
# Purpose:
# Generate a synthetic messy dataset
# The dataset intentionally includes common data
# quality issues such as duplicates, inconsistent categories,
# missing values, invalid emails and out-of-range values.
# ---------------------------------------------------------

np.random.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

n = 250

states = [
    "CDMX", "Ciudad de México", "Cd. México", "Estado de México", "EdoMex",
    "Jalisco", "Nuevo León", "Puebla", "Oaxaca", "Chiapas", "Yucatán"
]

genders = [
    "F", "Female", "M", "Male", "Mujer", "Hombre", "No especificado", "", None
]

education_levels = [
    "Secundaria", "Preparatoria", "Bachillerato", "Licenciatura",
    "Universidad", "Posgrado", "", None
]

programs = [
    "Data Analytics", "Excel for Business", "Employability Skills",
    "Digital Marketing", "Python Basics"
]

status_values = [
    "Completed", "completed", "COMPLETED", "In progress", "Dropped", "Abandoned", "", None
]

def random_email(name_id):
    domains = ["gmail.com", "outlook.com", "yahoo.com", "example.org"]
    valid = np.random.choice([True, False], p=[0.87, 0.13])
    if valid:
        return f"participant{name_id}@{random.choice(domains)}"
    invalid_options = [
        f"participant{name_id}gmail.com",
        f"participant{name_id}@",
        f"participant{name_id}.com",
        "",
        None
    ]
    return random.choice(invalid_options)

data = []

for i in range(1, n + 1):
    age = int(np.random.normal(24, 6))

    # Introduce unrealistic values
    if np.random.rand() < 0.04:
        age = random.choice([15, 16, 80, 95, -3])

    attendance_pct = round(np.random.normal(78, 18), 1)

    # Introduce invalid percentages
    if np.random.rand() < 0.05:
        attendance_pct = random.choice([-10, 105, 150, None])

    final_score = round(np.random.normal(82, 12), 1)

    # Introduce invalid scores
    if np.random.rand() < 0.05:
        final_score = random.choice([-5, 110, None])

    employed_before = np.random.choice(["Yes", "No", "yes", "no", "Sí", "No", "", None])
    employed_after = np.random.choice(["Yes", "No", "yes", "no", "Sí", "No", "", None])

    income_before = round(max(0, np.random.normal(5500, 2500)), 2)
    income_after = round(income_before + np.random.normal(1200, 1800), 2)

    if np.random.rand() < 0.05:
        income_before = random.choice(["$5,000", "N/A", "", None])
    if np.random.rand() < 0.05:
        income_after = random.choice(["$7,200", "N/A", "", None])

    start_date = pd.Timestamp("2025-01-01") + pd.to_timedelta(np.random.randint(0, 240), unit="D")
    end_date = start_date + pd.to_timedelta(np.random.randint(20, 120), unit="D")

    # Introduce inconsistent date format
    if np.random.rand() < 0.10:
        start_date_value = start_date.strftime("%d/%m/%Y")
    else:
        start_date_value = start_date.strftime("%Y-%m-%d")

    if np.random.rand() < 0.10:
        end_date_value = end_date.strftime("%d/%m/%Y")
    else:
        end_date_value = end_date.strftime("%Y-%m-%d")

    row = {
        "participant_id": f"P{i:04d}",
        "full_name": f"Participant {i}",
        "email": random_email(i),
        "state": random.choice(states),
        "age": age,
        "gender": random.choice(genders),
        "education_level": random.choice(education_levels),
        "program": random.choice(programs),
        "start_date": start_date_value,
        "end_date": end_date_value,
        "status": random.choice(status_values),
        "attendance_pct": attendance_pct,
        "final_score": final_score,
        "employed_before": employed_before,
        "employed_after": employed_after,
        "income_before": income_before,
        "income_after": income_after,
        "satisfaction_score": random.choice([1, 2, 3, 4, 5, "", None])
    }

    data.append(row)

df = pd.DataFrame(data)

# Add duplicated rows intentionally
duplicates = df.sample(10, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Add duplicated participant_id with modified values
duplicated_ids = df.sample(5, random_state=100).copy()
duplicated_ids["email"] = None
df = pd.concat([df, duplicated_ids], ignore_index=True)

output_path = RAW_DIR / "messy_participants.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Synthetic messy dataset created at: {output_path}")
print(f"Rows generated: {len(df)}")