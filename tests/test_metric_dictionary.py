
import csv
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
METRIC_FILE = PROJECT_ROOT / "data" / "processed" / "metric_dictionary.csv"


class TestMetricDictionary(unittest.TestCase):

    def test_metric_dictionary_exists(self):
        self.assertTrue(
            METRIC_FILE.exists(),
            f"Metric dictionary file not found: {METRIC_FILE}",
        )

    def test_metric_dictionary_has_required_columns(self):
        with METRIC_FILE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            reader = csv.DictReader(file)
            actual_columns = set(reader.fieldnames or [])

        required_columns = {
            "metric_name",
            "description",
            "formula",
            "source_table",
            "unit",
            "aggregation",
        }

        missing_columns = required_columns - actual_columns

        self.assertFalse(
            missing_columns,
            f"Missing columns: {missing_columns}",
        )

    def test_expected_metrics_are_present(self):
        with METRIC_FILE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file))

        metric_names = {
            row["metric_name"].strip()
            for row in rows
            if row.get("metric_name")
        }

        expected_metrics = {
            "Total Gross Payroll",
            "Total Net Payroll",
            "Total Employer Cost",
            "Attendance Coverage Rate",
            "Payroll Budget Variance",
        }

        missing_metrics = expected_metrics - metric_names

        self.assertFalse(
            missing_metrics,
            f"Missing expected metrics: {missing_metrics}",
        )

    def test_metric_fields_are_not_empty(self):
        with METRIC_FILE.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            rows = list(csv.DictReader(file))

        self.assertGreater(
            len(rows),
            0,
            "Metric dictionary contains no records",
        )

        required_fields = [
            "metric_name",
            "description",
            "formula",
            "source_table",
            "unit",
            "aggregation",
        ]

        for row in rows:
            with self.subTest(metric=row.get("metric_name")):
                for field in required_fields:
                    self.assertTrue(
                        row.get(field, "").strip(),
                        f"Empty field '{field}' for metric "
                        f"{row.get('metric_name')}",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
