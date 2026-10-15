
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

EXPECTED_FILES = {
    "dim_employee.csv",
    "fact_attendance_monthly.csv",
    "fact_leave.csv",
    "fact_payroll.csv",
    "budget_payroll_dept_month.csv",
}


class TestETL(unittest.TestCase):

    def test_clean_directory_exists(self):
        self.assertTrue(
            CLEAN_DIR.is_dir(),
            "Clean data directory does not exist",
        )

    def test_expected_clean_files_exist(self):
        missing_files = [
            name for name in EXPECTED_FILES
            if not (CLEAN_DIR / name).is_file()
        ]

        self.assertEqual(
            missing_files,
            [],
            f"Missing clean files: {missing_files}",
        )

    def test_clean_csv_files_are_readable(self):
        for filename in EXPECTED_FILES:
            file_path = CLEAN_DIR / filename

            with self.subTest(file=filename):
                self.assertTrue(file_path.is_file())
                dataframe = pd.read_csv(file_path)
                self.assertGreater(
                    len(dataframe.columns),
                    0,
                    f"{filename} has no columns",
                )

    def test_pipeline_run_log_exists(self):
        log_file = PROCESSED_DIR / "pipeline_run_log.csv"

        self.assertTrue(
            log_file.is_file(),
            "Pipeline run log does not exist",
        )

    def test_pipeline_run_log_has_required_columns(self):
        log_file = PROCESSED_DIR / "pipeline_run_log.csv"

        self.assertTrue(log_file.is_file(), "Run log is missing")

        log = pd.read_csv(log_file)

        required_columns = {
            "start_time",
            "end_time",
            "status",
            "message",
        }

        self.assertTrue(
            required_columns.issubset(log.columns),
            f"Missing run log columns: "
            f"{required_columns - set(log.columns)}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
