from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Capital One Post-Discover Monitor",
    page_icon="💳",
    layout="wide",
)


# -----------------------------
# File paths
# -----------------------------
TABLES_DIR = Path("outputs/tables")
QUARTERLY_METRICS_PATH = TABLES_DIR / "quarterly_metrics.csv"
PHASE_SUMMARY_PATH = TABLES_DIR / "phase_summary.csv"
RISK_PRESSURE_PATH = TABLES_DIR / "risk_pressure_top_quarters.csv"
DISCOVER_COST_PATH = TABLES_DIR / "discover_cost_pressure.csv"


# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data():
    quarterly = pd.read_csv(QUARTERLY_METRICS_PATH)
    phase_summary = pd.read_csv(PHASE_SUMMARY_PATH)
    risk_pressure = pd.read_csv(RISK_PRESSURE_PATH)
    discover_cost = pd.read_csv(DISCOVER_COST_PATH)

    return quarterly, phase_summary, risk_pressure, discover_cost


quarterly, phase_summary, risk_pressure, discover_cost = load_data()


# -----------------------------
# Header
# -----------------------------
st.title("Capital One Post-Discover Integration Monitor")

st.markdown(
    """
    This dashboard tracks Capital One's quarterly financial, credit-risk, and integration-cost metrics
    before and after the Discover acquisition. The goal is to monitor whether the expanded card portfolio
    is translating into stronger revenue while keeping credit risk and integration costs under control.
    """
)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

selected_phases = st.sidebar.multiselect(
    "Select acquisition phase",
    options=quarterly["acquisition_phase"].unique(),
    default=list(quarterly["acquisition_phase"].unique()),
)

filtered = quarterly[quarterly["acquisition_phase"].isin(selected_phases)]


# -----------------------------
# KPI cards
# -----------------------------
latest_quarter = quarterly.iloc[-1]
pre_discover_avg = phase_summary.loc[
    phase_summary["acquisition_phase"] == "Pre-Discover", "avg_revenue_m"
].iloc[0]
post_discover_avg = phase_summary.loc[
    phase_summary["acquisition_phase"] == "Post-Discover", "avg_revenue_m"
].iloc[0]

revenue_lift_pct = (post_discover_avg - pre_discover_avg) / pre_discover_avg * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Quarter",
    latest_quarter["quarter"],
)

col2.metric(
    "Latest Revenue",
    f"${latest_quarter['total_net_revenue_m']:,.0f}M",
)

col3.metric(
    "Latest Net Income",
    f"${latest_quarter['net_income_m']:,.0f}M",
)

col4.metric(
    "Post vs Pre Avg Revenue Lift",
    f"{revenue_lift_pct:.1f}%",
)


# -----------------------------
# Phase summary
# -----------------------------
st.subheader("Phase-Level Business Summary")

st.dataframe(
    phase_summary,
    use_container_width=True,
)


# -----------------------------
# Revenue and net income trend
# -----------------------------
st.subheader("Revenue and Net Income Trend")

fig_revenue = px.line(
    filtered,
    x="quarter",
    y=["total_net_revenue_m", "net_income_m"],
    markers=True,
    title="Quarterly Revenue and Net Income",
    labels={
        "value": "Dollars in millions",
        "quarter": "Quarter",
        "variable": "Metric",
    },
)

st.plotly_chart(fig_revenue, use_container_width=True)


# -----------------------------
# Credit card loans trend
# -----------------------------
st.subheader("Credit Card Portfolio Growth")

fig_loans = px.line(
    filtered,
    x="quarter",
    y="credit_card_loans_m",
    markers=True,
    title="Credit Card Loans Over Time",
    labels={
        "credit_card_loans_m": "Credit card loans ($M)",
        "quarter": "Quarter",
    },
)

st.plotly_chart(fig_loans, use_container_width=True)


# -----------------------------
# Risk monitoring
# -----------------------------
st.subheader("Credit Risk Monitoring")

col_risk1, col_risk2 = st.columns(2)

with col_risk1:
    fig_provision = px.line(
        filtered,
        x="quarter",
        y="provision_to_revenue_pct",
        markers=True,
        title="Provision-to-Revenue Pressure",
        labels={
            "provision_to_revenue_pct": "Provision-to-revenue (%)",
            "quarter": "Quarter",
        },
    )
    st.plotly_chart(fig_provision, use_container_width=True)

with col_risk2:
    fig_credit_risk = px.line(
        filtered,
        x="quarter",
        y=["net_charge_off_rate_pct", "delinquency_30_plus_pct"],
        markers=True,
        title="Charge-Off and Delinquency Rates",
        labels={
            "value": "Rate (%)",
            "quarter": "Quarter",
            "variable": "Metric",
        },
    )
    st.plotly_chart(fig_credit_risk, use_container_width=True)

st.markdown("Highest credit-risk pressure quarters:")
st.dataframe(risk_pressure, use_container_width=True)


# -----------------------------
# Discover cost pressure
# -----------------------------
st.subheader("Discover Integration Cost Pressure")

fig_discover = px.line(
    filtered,
    x="quarter",
    y="discover_cost_to_revenue_pct",
    markers=True,
    title="Discover Integration and Amortization Cost-to-Revenue",
    labels={
        "discover_cost_to_revenue_pct": "Discover cost-to-revenue (%)",
        "quarter": "Quarter",
    },
)

st.plotly_chart(fig_discover, use_container_width=True)

st.dataframe(discover_cost, use_container_width=True)


# -----------------------------
# Executive takeaway
# -----------------------------
st.subheader("Executive Takeaway")

st.markdown(
    """
    The analysis shows that Capital One's post-Discover revenue base is meaningfully larger than the
    pre-Discover period. However, the 2025 Q2 transition quarter shows a major profitability and
    provision-pressure shock. The monitoring recommendation is to track whether post-acquisition revenue
    growth continues while credit losses, delinquencies, and Discover-related cost pressure normalize over time.
    """
)