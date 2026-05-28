from pathlib import Path

import pandas as pd


# -----------------------------
# File paths
# -----------------------------
RAW_DATA_PATH = Path("data/raw/capitalone_quarterly_raw.csv")
PROCESSED_DATA_PATH = Path("data/processed/capitalone_quarterly_clean.csv")


# -----------------------------
# Columns
# -----------------------------
NUMERIC_COLUMNS = [
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
]


def clean_capitalone_data() -> pd.DataFrame:
    """
    Read raw Capital One quarterly data, clean data types,
    sort the quarters, and save a processed CSV.
    """

    # Read raw CSV
    df = pd.read_csv(RAW_DATA_PATH)

    # Convert period_end into a real date column
    df["period_end"] = pd.to_datetime(df["period_end"])

    # Convert numeric columns from text to numeric values
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Create year and quarter number for easier sorting/analysis
    df["year"] = df["period_end"].dt.year
    df["quarter_num"] = df["period_end"].dt.quarter

    # Sort from oldest quarter to newest quarter
    df = df.sort_values("period_end").reset_index(drop=True)

    # Save clean dataset
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    return df


if __name__ == "__main__":
    cleaned_df = clean_capitalone_data()

    print("Cleaned dataset created successfully.")
    print(f"Rows: {len(cleaned_df)}")
    print(f"Columns: {len(cleaned_df.columns)}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")

    print("\nPreview:")
    print(
        cleaned_df[
            [
                "quarter",
                "period_end",
                "acquisition_phase",
                "total_net_revenue_m",
                "net_income_m",
                "credit_card_loans_m",
            ]
        ]
    )