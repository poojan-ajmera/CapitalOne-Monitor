from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# -----------------------------
# File paths
# -----------------------------
QUARTERLY_METRICS_PATH = Path("outputs/tables/quarterly_metrics.csv")
CHARTS_DIR = Path("outputs/charts")


def save_chart(fig: plt.Figure, filename: str) -> None:
    """
    Save a matplotlib chart to the outputs/charts folder.
    """

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CHARTS_DIR / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")


def generate_charts() -> None:
    """
    Generate core monitoring charts for the Capital One project.
    """

    df = pd.read_csv(QUARTERLY_METRICS_PATH)

    # Keep quarter order from the scorecard table
    x = df["quarter"]

    # -----------------------------
    # Chart 1: Revenue and net income trend
    # -----------------------------
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, df["total_net_revenue_m"], marker="o", label="Total net revenue ($M)")
    ax.plot(x, df["net_income_m"], marker="o", label="Net income ($M)")
    ax.axvline(x=df.index[df["quarter"] == "2025 Q2"][0], linestyle="--", label="Discover transition quarter")
    ax.set_title("Capital One Revenue and Net Income Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Dollars in millions")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_chart(fig, "01_revenue_net_income_trend.png")

    # -----------------------------
    # Chart 2: Credit card loans trend
    # -----------------------------
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, df["credit_card_loans_m"], marker="o")
    ax.axvline(x=df.index[df["quarter"] == "2025 Q2"][0], linestyle="--")
    ax.set_title("Credit Card Loans Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Credit card loans ($M)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    save_chart(fig, "02_credit_card_loans_trend.png")

    # -----------------------------
    # Chart 3: Provision-to-revenue pressure
    # -----------------------------
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, df["provision_to_revenue_pct"], marker="o")
    ax.axvline(x=df.index[df["quarter"] == "2025 Q2"][0], linestyle="--")
    ax.set_title("Provision for Credit Losses as Share of Revenue")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Provision-to-revenue (%)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    save_chart(fig, "03_provision_to_revenue_pressure.png")

    # -----------------------------
    # Chart 4: Charge-off and delinquency trend
    # -----------------------------
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, df["net_charge_off_rate_pct"], marker="o", label="Net charge-off rate (%)")
    ax.plot(x, df["delinquency_30_plus_pct"], marker="o", label="30+ day delinquency rate (%)")
    ax.axvline(x=df.index[df["quarter"] == "2025 Q2"][0], linestyle="--")
    ax.set_title("Credit Risk Monitoring: Charge-Off and Delinquency Rates")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Rate (%)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_chart(fig, "04_credit_risk_rates_trend.png")

    # -----------------------------
    # Chart 5: Discover cost pressure
    # -----------------------------
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, df["discover_cost_to_revenue_pct"], marker="o")
    ax.axvline(x=df.index[df["quarter"] == "2025 Q2"][0], linestyle="--")
    ax.set_title("Discover Integration and Amortization Cost Pressure")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Discover cost-to-revenue (%)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    save_chart(fig, "05_discover_cost_pressure.png")

    print("\nAll charts generated successfully.")


if __name__ == "__main__":
    generate_charts()