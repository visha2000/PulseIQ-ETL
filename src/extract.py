 


from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
CLEAN_DIR = PROJECT_DIR / "data" / "clean"

TASK1_FILES = {
    "budget_payroll_dept_month",
    "dim_employee",
    "fact_attendance_monthly",
    "fact_leave",
    "fact_payroll",
}


def extract_data():
    source_dir = RAW_DIR

    if not source_dir.exists():
        raise FileNotFoundError(f"Folder not found: {source_dir}")

    all_files = (
        list(source_dir.glob("*.csv"))
        + list(source_dir.glob("*.xlsx"))
    )

    # Select only the five Task 1 files
    files = [
        file for file in all_files
        if any(
            file.stem.lower().endswith(name)
            for name in TASK1_FILES
        )
    ]

    if not files:
        raise FileNotFoundError(
            "None of the five Task 1 files were found in data/raw. "
            "Please check their filenames."
        )

    data = {}

    for file in files:
        if file.suffix.lower() == ".xlsx":
            data[file.stem] = pd.read_excel(file)
        else:
            data[file.stem] = pd.read_csv(file)

        print(f"Extracted: {file.name}")

    print(f"Total files extracted: {len(data)}")
    return data


if __name__ == "__main__":
    extract_data()

