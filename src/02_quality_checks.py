from pathlib import Path

import pandas as pd


# -----------------------------
# File paths
# -----------------------------
PROCESSED_DATA_PATH = Path("data/processed/capitalone_quarterly_clean.csv")


# -----------------------------
# Expected values
# -----------------------------
EXPECTED_ROW_COUNT = 13

EXPECTED_PHASES = {
    "Pre-Discover",
    "Transition",
    "Post-Discover",
}

REQUIRED_COLUMNS = [
    "quarter",
    "period_end",
    "acquisition_phase",
    "total_net_revenue_m",
    "net_income_m",
    "diluted_eps",
    "adjusted_eps",
    "non_interest_expense_m",
    "provision_credit_losses_m",
    "net_interest_margin_pct",
    "efficiency_ratio_pct",
    "credit_card_loans_m",
    "net_charge_off_rate_pct",
    "delinquency_30_plus_pct",
    "discover_integration_expense_m",
    "discover_amortization_expense_m",
    "marketing_expense_m",
    "operating_expense_m",
    "source_name",
    "source_url",
    "notes",
    "year",
    "quarter_num",
]

NON_NEGATIVE_COLUMNS = [
    "total_net_revenue_m",
    "non_interest_expense_m",
    "provision_credit_losses_m",
    "net_interest_margin_pct",
    "efficiency_ratio_pct",
    "credit_card_loans_m",
    "net_charge_off_rate_pct",
    "delinquency_30_plus_pct",
    "discover_integration_expense_m",
    "discover_amortization_expense_m",
    "marketing_expense_m",
    "operating_expense_m",
]


def run_quality_checks() -> None:
    """
    Run basic data quality checks on the processed Capital One dataset.
    If a check fails, raise an error. If all pass, print a success message.
    """

    # Check file exists
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(f"Processed file not found: {PROCESSED_DATA_PATH}")

    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Check row count
    if len(df) != EXPECTED_ROW_COUNT:
        raise ValueError(f"Expected {EXPECTED_ROW_COUNT} rows, found {len(df)} rows.")

    # Check required columns
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Check missing values
    missing_values = df.isna().sum()
    if missing_values.sum() > 0:
        raise ValueError(f"Missing values found:\n{missing_values[missing_values > 0]}")

    # Check duplicate quarters
    duplicate_quarters = df[df["quarter"].duplicated()]
    if not duplicate_quarters.empty:
        raise ValueError(f"Duplicate quarters found:\n{duplicate_quarters}")

    # Check acquisition phase values
    invalid_phases = set(df["acquisition_phase"]) - EXPECTED_PHASES
    if invalid_phases:
        raise ValueError(f"Invalid acquisition phases found: {invalid_phases}")

    # Check source URLs
    invalid_urls = df[
        ~df["source_url"].astype(str).str.startswith("https://investor.capitalone.com/")
    ]
    if not invalid_urls.empty:
        raise ValueError(f"Invalid source URLs found:\n{invalid_urls[['quarter', 'source_url']]}")

    # Check placeholder text
    placeholder_rows = df[
        df.astype(str).apply(lambda col: col.str.contains("SOURCE_URL|PLACEHOLDER", case=False, na=False)).any(axis=1)
    ]
    if not placeholder_rows.empty:
        raise ValueError(f"Placeholder text found:\n{placeholder_rows}")

    # Check non-negative columns
    for col in NON_NEGATIVE_COLUMNS:
        negative_rows = df[df[col] < 0]
        if not negative_rows.empty:
            raise ValueError(f"Unexpected negative values found in {col}:\n{negative_rows[['quarter', col]]}")

    # Check date ordering
    df["period_end"] = pd.to_datetime(df["period_end"])
    if not df["period_end"].is_monotonic_increasing:
        raise ValueError("period_end is not sorted from oldest to newest.")

    print("All data quality checks passed.")
    print(f"Rows checked: {len(df)}")
    print(f"Columns checked: {len(df.columns)}")
    print("Dataset is ready for SQL database creation.")


if __name__ == "__main__":
    run_quality_checks()