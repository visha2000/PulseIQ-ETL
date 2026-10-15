
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "processed"

DATABASE_URL = (
    "postgresql+psycopg2://pulseiq_user:"
    "pulseiq_password@postgres:5432/pulseiq_warehouse"
)

# PostgreSQL table names and their conflict keys
TABLES = {
    "dim_department": ("dim_department", ["department_id"]),
    "dim_location": ("dim_location", ["work_location"]),
    "dim_role": ("dim_role", ["role_id"]),
    "dim_date": ("dim_date", ["date_key"]),
    "dim_leave_type": ("dim_leave_type", ["leave_type_code"]),
    "dim_employee": ("dim_employee", ["employee_key"]),
    "fact_attendance_monthly": (
        "fact_attendance_monthly", ["attendance_fact_id"]
    ),
    "fact_payroll": ("fact_payroll", ["payroll_item_id"]),
    "fact_leave": ("fact_leave", ["leave_request_id"]),
    "fact_headcount_monthly": (
        "fact_headcount_monthly", ["date_key", "department_id"]
    ),
}

NUMERIC_COLUMNS = {
    "dim_role": [
        "level",
        "band_min_annual",
        "band_mid_annual",
        "band_max_annual",
        "band_reference_year",
    ],
    "dim_leave_type": [
        "annual_quota_days",
        "max_carry_forward_days",
    ],
    "dim_date": [
        "date_key",
        "year",
        "quarter",
        "month_number",
        "week_of_year",
        "fiscal_month_number",
    ],
    "fact_attendance_monthly": [
        "date_key",
        "scheduled_days",
        "present_days",
        "wfh_days",
        "half_days_unpaid",
        "paid_leave_days",
        "unpaid_absence_days",
        "late_arrivals",
        "avg_hours_worked",
        "overtime_hours",
        "attendance_rate",
    ],
    "fact_payroll": [
        "date_key",
        "payable_days",
        "lop_days",
        "overtime_hours_paid",
        "monthly_fixed_gross",
        "basic",
        "hra",
        "conveyance",
        "medical",
        "special_allowance",
        "earned_fixed_pay",
        "overtime_pay",
        "variable_pay",
        "gross_pay",
        "pf_employee",
        "esi_employee",
        "professional_tax",
        "tds",
        "other_deductions",
        "total_deductions",
        "net_pay",
        "pf_employer",
        "esi_employer",
        "employer_cost",
        "headcount_flag",
    ],
    "fact_leave": [
        "start_date_key",
        "end_date_key",
        "days",
    ],
    "fact_headcount_monthly": [
        "date_key",
        "headcount_start",
        "hires",
        "exits",
        "voluntary_exits",
        "transfers_in",
        "transfers_out",
        "headcount_end",
        "attrition_rate_monthly_pct",
    ],
}

DATE_COLUMNS = {
    "dim_date": [
        "date",
        "month_start_date",
        "month_end_date",
    ],
    "dim_employee": [
        "date_of_birth",
        "hire_date",
        "exit_date",
        "valid_from",
        "valid_to",
    ],
    "fact_attendance_monthly": ["period_end_date"],
    "fact_payroll": ["period_end_date"],
    "fact_leave": [
        "start_date",
        "end_date",
        "applied_on",
        "decided_on",
    ],
    "fact_headcount_monthly": ["month_start_date"],
}


def normalize_columns(df):
    """Normalize column names."""
    df = df.copy()
    df.columns = [
        str(col).strip().lower().replace(" ", "_")
        for col in df.columns
    ]
    return df


def prepare_dataframe(df, table):
    """Prepare numeric and date columns."""
    df = normalize_columns(df)

    for col in NUMERIC_COLUMNS.get(table, []):
        if col in df.columns:
            values = df[col].astype("string").str.replace(
                ",", "", regex=False
            )
            df[col] = pd.to_numeric(values, errors="coerce")

    for col in DATE_COLUMNS.get(table, []):
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
            )

    return df


def get_target_columns(conn, table):
    """Get columns from the PostgreSQL target table."""
    result = conn.execute(
        text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = :table
            ORDER BY ordinal_position
        """),
        {"table": table},
    )

    return [row[0] for row in result]


def upsert_dataframe(conn, table, df, keys):
    """Insert new rows and update existing rows."""
    target_columns = get_target_columns(conn, table)

    if not target_columns:
        raise ValueError(
            f"PostgreSQL table not found: {table}"
        )

    df = normalize_columns(df)

    columns = [
        col for col in df.columns
        if col in target_columns
    ]

    if not columns:
        raise ValueError(
            f"No matching columns for table: {table}"
        )

    missing_keys = [
        key for key in keys
        if key not in columns
    ]

    if missing_keys:
        raise ValueError(
            f"{table}: missing conflict keys {missing_keys}"
        )

    df = df[columns].copy()

    if df.empty:
        print(f"No rows to load into {table}.")
        return

    # Remove duplicate source keys before upsert
    df = df.drop_duplicates(
        subset=keys,
        keep="last",
    )

    staging = f"stg_{table}"

    df.to_sql(
        staging,
        con=conn,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    quoted_cols = ", ".join(
        f'"{col}"' for col in columns
    )

    conflict_keys = ", ".join(
        f'"{key}"' for key in keys
    )

    updates = [
        col for col in columns
        if col not in keys
    ]

    if updates:
        update_sql = ", ".join(
            f'"{col}" = EXCLUDED."{col}"'
            for col in updates
        )

        conflict_sql = (
            f"ON CONFLICT ({conflict_keys}) "
            f"DO UPDATE SET {update_sql}"
        )
    else:
        conflict_sql = (
            f"ON CONFLICT ({conflict_keys}) DO NOTHING"
        )

    sql = f"""
        INSERT INTO "{table}" ({quoted_cols})
        SELECT {quoted_cols}
        FROM "{staging}"
        {conflict_sql}
    """

    conn.execute(text(sql))
    conn.execute(text(f'DROP TABLE "{staging}"'))

    print(
        f"Loaded into PostgreSQL: {table} "
        f"({len(df)} rows)"
    )


def load_data(sheets):
    """Save processed CSVs and load all warehouse tables."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save current Task 1 processed files
    for name, df in sheets.items():
        output_file = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved CSV: {output_file.name}")

    source_prefix = (
        "03_PulseIQ_Analytics_Star_Schema_Dataset.xlsx - "
    )

    # Read the additional tables from their existing CSV files
    extra_tables = [
        "dim_department",
        "dim_role",
        "dim_date",
        "dim_leave_type",
        "fact_headcount_monthly",
    ]

    extra_data = {}

    for table in extra_tables:
        source_file = (
            OUTPUT_DIR / f"{source_prefix}{table}.csv"
        )

        if not source_file.exists():
            raise FileNotFoundError(
                f"Required source CSV not found: {source_file}"
            )

        extra_data[table] = pd.read_csv(source_file)
        print(
            f"Read source CSV: {source_file.name} "
            f"({len(extra_data[table])} rows)"
        )

    # Locate employee data from the current ETL input
    employee_df = None

    for source_name, source_df in sheets.items():
        if source_name.lower().endswith("dim_employee"):
            employee_df = normalize_columns(source_df)
            break

    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as conn:

            # 1. Load reference tables first
            for table in [
                "dim_department",
                "dim_location",
                "dim_role",
                "dim_date",
                "dim_leave_type",
            ]:
                if table == "dim_location":
                    if (
                        employee_df is None
                        or "work_location" not in employee_df.columns
                    ):
                        print(
                            "Warning: employee location data "
                            "not available."
                        )
                        continue

                    locations = (
                        employee_df["work_location"]
                        .dropna()
                        .astype(str)
                        .str.strip()
                    )

                    locations = (
                        locations[locations != ""]
                        .drop_duplicates()
                    )

                    df = pd.DataFrame({
                        "work_location": locations.tolist()
                    })
                else:
                    df = extra_data[table]

                df = prepare_dataframe(df, table)

                upsert_dataframe(
                    conn,
                    table,
                    df,
                    TABLES[table][1],
                )

            # 2. Load employee and existing fact tables
            for table in [
                "dim_employee",
                "fact_attendance_monthly",
                "fact_payroll",
                "fact_leave",
            ]:
                for source_name, source_df in sheets.items():
                    if source_name.lower().endswith(table):
                        df = prepare_dataframe(
                            source_df,
                            table,
                        )

                        upsert_dataframe(
                            conn,
                            table,
                            df,
                            TABLES[table][1],
                        )
                        break

            # 3. Load monthly headcount after dimensions
            table = "fact_headcount_monthly"

            df = prepare_dataframe(
                extra_data[table],
                table,
            )

            upsert_dataframe(
                conn,
                table,
                df,
                TABLES[table][1],
            )

        print(
            "CSV output and PostgreSQL warehouse "
            "load completed successfully."
        )

    finally:
        engine.dispose()


