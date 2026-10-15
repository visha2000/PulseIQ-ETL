
# Data transformation logic

import re
import pandas as pd


def clean_column_name(value):
    value = re.sub(r"[^A-Za-z0-9]+", "_", str(value))
    return value.strip("_").lower()


def transform_data(sheets):
    transformed = {}

    for name, df in sheets.items():
        df = df.copy()

        # Standardize column names
        df.columns = [
            clean_column_name(col)
            for col in df.columns
        ]

        # Stop if column names become duplicates
        if df.columns.duplicated().any():
            raise ValueError(
                f"Duplicate column names after cleaning: {name}"
            )

        # Remove leading/trailing spaces
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].map(
                lambda value: (
                    value.strip()
                    if isinstance(value, str)
                    else value
                )
            )
            df[col] = df[col].replace("", pd.NA)

        # Remove fully duplicated rows only
        before = len(df)

        df = df.drop_duplicates().reset_index(drop=True)

        removed = before - len(df)

        print(
            f"Transformed: {name}; "
            f"removed {removed} duplicate rows"
        )

        transformed[name] = df

    return transformed