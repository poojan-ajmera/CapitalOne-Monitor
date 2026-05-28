from pathlib import Path

import duckdb


# -----------------------------
# File paths
# -----------------------------
DATABASE_PATH = Path("data/processed/capitalone_monitor.duckdb")
VIEWS_SQL_PATH = Path("sql/02_analysis_views.sql")
OUTPUT_TABLES_DIR = Path("outputs/tables")


def export_query(conn: duckdb.DuckDBPyConnection, query: str, output_path: Path) -> None:
    """
    Run a SQL query and export the result to CSV.
    """

    df = conn.execute(query).fetchdf()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Exported: {output_path} | Rows: {len(df)}")


def generate_scorecard_tables() -> None:
    """
    Generate reusable business scorecard tables from DuckDB views.
    """

    conn = duckdb.connect(str(DATABASE_PATH))

    # Make sure SQL views exist
    conn.execute(VIEWS_SQL_PATH.read_text())

    # 1. Phase-level summary
    export_query(
        conn,
        """
        SELECT
            acquisition_phase,
            quarter_count,
            avg_revenue_m,
            avg_net_income_m,
            avg_net_income_margin_pct,
            avg_credit_card_loans_m,
            avg_net_charge_off_rate_pct,
            avg_delinquency_30_plus_pct,
            avg_efficiency_ratio_pct,
            avg_provision_to_revenue_pct,
            avg_discover_cost_to_revenue_pct
        FROM v_phase_summary
        ORDER BY
            CASE acquisition_phase
                WHEN 'Pre-Discover' THEN 1
                WHEN 'Transition' THEN 2
                WHEN 'Post-Discover' THEN 3
            END
        """,
        OUTPUT_TABLES_DIR / "phase_summary.csv",
    )

    # 2. Quarter-level monitoring table
    export_query(
        conn,
        """
        SELECT
            quarter,
            period_end,
            acquisition_phase,
            total_net_revenue_m,
            net_income_m,
            adjusted_eps,
            credit_card_loans_m,
            net_interest_margin_pct,
            efficiency_ratio_pct,
            provision_to_revenue_pct,
            net_charge_off_rate_pct,
            delinquency_30_plus_pct,
            discover_cost_to_revenue_pct,
            revenue_qoq_growth_pct,
            credit_card_loans_qoq_growth_pct
        FROM v_capitalone_metrics
        ORDER BY period_end
        """,
        OUTPUT_TABLES_DIR / "quarterly_metrics.csv",
    )

    # 3. Highest credit risk pressure quarters
    export_query(
        conn,
        """
        SELECT
            quarter,
            acquisition_phase,
            total_net_revenue_m,
            provision_credit_losses_m,
            provision_to_revenue_pct,
            net_charge_off_rate_pct,
            delinquency_30_plus_pct
        FROM v_capitalone_metrics
        ORDER BY provision_to_revenue_pct DESC
        LIMIT 5
        """,
        OUTPUT_TABLES_DIR / "risk_pressure_top_quarters.csv",
    )

    # 4. Discover-related cost pressure
    export_query(
        conn,
        """
        SELECT
            quarter,
            acquisition_phase,
            total_net_revenue_m,
            discover_integration_expense_m,
            discover_amortization_expense_m,
            discover_cost_to_revenue_pct
        FROM v_capitalone_metrics
        ORDER BY discover_cost_to_revenue_pct DESC
        """,
        OUTPUT_TABLES_DIR / "discover_cost_pressure.csv",
    )

    conn.close()

    print("\nScorecard tables generated successfully.")


if __name__ == "__main__":
    generate_scorecard_tables()