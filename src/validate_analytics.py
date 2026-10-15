import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://pulseiq_user:pulseiq_password@postgres:5432/pulseiq_warehouse"
)

engine = create_engine(DB_URL)
DATA_DIR = Path("data/clean")


def check_test(name, csv_data, sql_data, keys, values):
    csv_data = csv_data.sort_values(keys).reset_index(drop=True)
    sql_data = sql_data.sort_values(keys).reset_index(drop=True)

    if not csv_data[keys].equals(sql_data[keys]):
        print(f"FAIL: {name} - grouping keys differ")
        return False

    for col in values:
        left = pd.to_numeric(csv_data[col], errors="coerce")
        right = pd.to_numeric(sql_data[col], errors="coerce")

        if not (left - right).abs().fillna(0).lt(0.02).all():
            print(f"FAIL: {name} - mismatch in {col}")
            print(pd.DataFrame({"CSV": left, "SQL": right}).head())
            return False

    print(f"PASS: {name}")
    return True


def main():
    results = []

    # Test 1: Department payroll
    payroll = pd.read_csv(DATA_DIR / "fact_payroll.csv")

    csv1 = payroll.groupby("department_id", as_index=False).agg(
        employee_count=("employee_id", "nunique"),
        gross_pay=("gross_pay", "sum"),
        employer_cost=("employer_cost", "sum"),
    )

    sql1 = pd.read_sql(text("""
        SELECT department_id,
               COUNT(DISTINCT employee_id) AS employee_count,
               SUM(gross_pay) AS gross_pay,
               SUM(employer_cost) AS employer_cost
        FROM fact_payroll
        GROUP BY department_id
    """), engine)

    results.append(check_test(
        "Department payroll", csv1, sql1,
        ["department_id"],
        ["employee_count", "gross_pay", "employer_cost"]
    ))

    # Test 2: Monthly payroll
    csv2 = payroll.groupby(["year", "month"], as_index=False).agg(
        employee_count=("employee_id", "nunique"),
        gross_pay=("gross_pay", "sum"),
        employer_cost=("employer_cost", "sum"),
    )

    sql2 = pd.read_sql(text("""
        SELECT EXTRACT(YEAR FROM period_end_date)::int AS year,
               EXTRACT(MONTH FROM period_end_date)::int AS month,
               COUNT(DISTINCT employee_id) AS employee_count,
               SUM(gross_pay) AS gross_pay,
               SUM(employer_cost) AS employer_cost
        FROM fact_payroll
        GROUP BY 1, 2
    """), engine)

    results.append(check_test(
        "Monthly payroll", csv2, sql2,
        ["year", "month"],
        ["employee_count", "gross_pay", "employer_cost"]
    ))

    # Test 3: Monthly attendance
    attendance = pd.read_csv(DATA_DIR / "fact_attendance_monthly.csv")

    csv3 = attendance.groupby(["year", "month"], as_index=False).agg(
        employee_count=("employee_id", "nunique"),
        scheduled_days=("scheduled_days", "sum"),
        present_days=("present_days", "sum"),
        avg_attendance_rate=("attendance_rate", "mean"),
    )

    sql3 = pd.read_sql(text("""
        SELECT EXTRACT(YEAR FROM period_end_date)::int AS year,
               EXTRACT(MONTH FROM period_end_date)::int AS month,
               COUNT(DISTINCT employee_id) AS employee_count,
               SUM(scheduled_days) AS scheduled_days,
               SUM(present_days) AS present_days,
               AVG(attendance_rate) AS avg_attendance_rate
        FROM fact_attendance_monthly
        GROUP BY 1, 2
    """), engine)

    results.append(check_test(
        "Monthly attendance", csv3, sql3,
        ["year", "month"],
        ["employee_count", "scheduled_days", "present_days",
         "avg_attendance_rate"]
    ))

    print("\n===== VALIDATION SUMMARY =====")
    print(f"Passed: {sum(results)} / 3")
    print(f"Failed: {len(results) - sum(results)} / 3")

    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
