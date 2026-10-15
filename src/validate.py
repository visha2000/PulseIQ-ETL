

import pandas as pd

def validate_data(data):
    validated_data = {}

    for name, df in data.items():
        print(f"\nValidating: {name}")

        if df.empty:
            raise ValueError(f"{name} is empty.")

        duplicate_count = int(df.duplicated().sum())
        missing_count = int(df.isna().sum().sum())

        print(f"Rows: {len(df)}")
        print(f"Duplicate rows: {duplicate_count}")
        print(f"Missing values: {missing_count}")

        validated_data[name] = df

    print("\nValidation completed successfully.")
    return validated_data
