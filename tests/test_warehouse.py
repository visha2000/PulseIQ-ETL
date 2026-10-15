
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = PROJECT_ROOT / "sql" / "schema.sql"
ANALYTICS_FILE = PROJECT_ROOT / "sql" / "analytics.sql"

EXPECTED_TABLES = {
    "dim_employee",
    "dim_department",
    "dim_role",
    "dim_date",
    "dim_leave_type",
    "dim_location",
    "fact_attendance_monthly",
    "fact_payroll",
    "fact_leave",
    "fact_headcount_monthly",
}


class TestWarehouse(unittest.TestCase):

    def test_schema_file_exists(self):
        self.assertTrue(
            SCHEMA_FILE.is_file(),
            f"Schema file not found: {SCHEMA_FILE}",
        )

    def test_analytics_sql_file_exists(self):
        self.assertTrue(
            ANALYTICS_FILE.is_file(),
            f"Analytics SQL file not found: {ANALYTICS_FILE}",
        )

    def test_schema_defines_expected_tables(self):
        self.assertTrue(SCHEMA_FILE.is_file())

        sql = SCHEMA_FILE.read_text(encoding="utf-8").lower()

        missing_tables = {
            table for table in EXPECTED_TABLES
            if table not in sql
        }

        self.assertFalse(
            missing_tables,
            f"Table names missing from schema: {missing_tables}",
        )

    def test_analytics_file_contains_queries(self):
        self.assertTrue(ANALYTICS_FILE.is_file())

        sql = ANALYTICS_FILE.read_text(encoding="utf-8").strip().lower()

        self.assertIn(
            "select",
            sql,
            "Analytics SQL should contain SELECT queries",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
