

from pathlib import Path
from datetime import datetime
import csv
import traceback

from src.extract import extract_data
from src.validate import validate_data
from src.transform import transform_data
from src.load import load_data


PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_DIR / "data" / "processed" / "pipeline_run_log.csv"

def write_run_log(start_time, end_time, status, message):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_FILE.exists() and LOG_FILE.stat().st_size > 0

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "start_time",
                "end_time",
                "status",
                "message"
            ])

        writer.writerow([
            start_time.isoformat(timespec="seconds"),
            end_time.isoformat(timespec="seconds"),
            status,
            message
        ])


def run_pipeline():
    start_time = datetime.now()

    try:
        print("STEP 1: EXTRACT")
        raw_data = extract_data()

        print("\nSTEP 2: VALIDATE")
        valid_data = validate_data(raw_data)

        print("\nSTEP 3: TRANSFORM")
        clean_data = transform_data(valid_data)

        print("\nSTEP 4: LOAD")
        load_data(clean_data)

        print("\nETL PIPELINE COMPLETED")
        write_run_log(
            start_time,
            datetime.now(),
            "SUCCESS",
            "ETL pipeline completed successfully"
        )

    except Exception as error:
        write_run_log(
            start_time,
            datetime.now(),
            "FAILED",
            str(error)
        )
        raise


if __name__ == "__main__":
    run_pipeline()

