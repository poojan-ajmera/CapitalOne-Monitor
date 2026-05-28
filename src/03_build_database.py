from pathlib import Path

import duckdb
import pandas as pd


# -----------------------------
# File paths
# -----------------------------
PROCESSED_DATA_PATH = Path("data/processed/capitalone_quarterly_clean.csv")
DATABASE_PATH = Path("data/processed/capitalone_monitor.duckdb")


def build_database() -> None:
    """
    Build a DuckDB database from the cleaned Capital One quarterly dataset.
    """

    # Read cleaned data
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Connect to DuckDB database
    # If the file does not exist, DuckDB creates it automatically.
    conn = duckdb.connect(str(DATABASE_PATH))

    # Replace the table if it already exists
    conn.execute("DROP TABLE IF EXISTS capitalone_quarterly")

    # Create table from the pandas DataFrame
    conn.register("capitalone_df", df)
    conn.execute("""
        CREATE TABLE capitalone_quarterly AS
        SELECT *
        FROM capitalone_df
    """)

    # Quick SQL validation
    row_count = conn.execute("""
        SELECT COUNT(*) AS row_count
        FROM capitalone_quarterly
    """).fetchone()[0]

    phase_summary = conn.execute("""
        SELECT
            acquisition_phase,
            COUNT(*) AS quarter_count,
            ROUND(AVG(total_net_revenue_m), 2) AS avg_revenue_m,
            ROUND(AVG(net_income_m), 2) AS avg_net_income_m
        FROM capitalone_quarterly
        GROUP BY acquisition_phase
        ORDER BY quarter_count DESC
    """).fetchdf()

    conn.close()

    print("DuckDB database created successfully.")
    print(f"Database saved to: {DATABASE_PATH}")
    print(f"Rows loaded: {row_count}")

    print("\nPhase summary:")
    print(phase_summary)


if __name__ == "__main__":
    build_database()