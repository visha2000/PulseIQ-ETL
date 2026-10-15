
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

print("=" * 70)
print("TASK 2 - SOURCE DATA INSPECTION")
print("=" * 70)

if not RAW_DIR.exists():
    raise FileNotFoundError(f"Folder not found: {RAW_DIR}")

files = sorted(RAW_DIR.glob("*.csv"))

print(f"\nTotal CSV files found: {len(files)}")

# 1. List all files and identify attendance-related files
print("\n1. FILES RELATED TO ATTENDANCE")
attendance_files = [
    f for f in files
    if "attendance" in f.name.lower()
]

if attendance_files:
    for f in attendance_files:
        print(f"  - {f.name}")
else:
    print("No attendance-related CSV filename found.")

# 2. Display columns and sample rows for attendance files
for file in attendance_files:
    print(f"\n2. INSPECTING: {file.name}")

    df = pd.read_csv(file, nrows=5)
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.to_string(index=False))

# 3. Check whether payroll has duplicate employee/month records
payroll_files = [
    f for f in files
    if "fact_payroll" in f.name.lower()
]

for file in payroll_files:
    print(f"\n3. PAYROLL CHECK: {file.name}")

    df = pd.read_csv(file, low_memory=False)

    print(f"Total rows: {len(df)}")

    required = {"employee_id", "period_end_date"}

    if required.issubset(df.columns):
        df["_month"] = pd.to_datetime(
            df["period_end_date"],
            dayfirst=True,
            errors="coerce"
        ).dt.to_period("M")

        valid = df.dropna(subset=["employee_id", "_month"])

        duplicate_mask = valid.duplicated(
            subset=["employee_id", "_month"],
            keep=False
        )

        duplicates = valid.loc[
            duplicate_mask
        ].sort_values(["employee_id", "_month"])

        print(
            "Duplicate employee/month rows:",
            int(duplicate_mask.sum())
        )

        if not duplicates.empty:
            cols = [
                c for c in [
                    "payroll_item_id",
                    "run_id",
                    "employee_id",
                    "period_end_date",
                    "gross_pay"
                ]
                if c in duplicates.columns
            ]

            print(duplicates[cols].head(20).to_string(index=False))
    else:
        print("Required columns not found:", required)

print("\n4. INSPECTION COMPLETED")
