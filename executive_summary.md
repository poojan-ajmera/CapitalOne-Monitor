# Executive Summary

## Capital One Post-Discover Integration Monitor

This project analyzes Capital One's quarterly financial and credit-risk performance from 2023 Q1 through 2026 Q1, with a focus on understanding how the Discover acquisition changed the company's revenue base, credit card portfolio, risk profile, and integration cost pressure.

The project uses official Capital One financial supplement data and turns it into a repeatable analytics workflow. The pipeline includes raw data collection, data cleaning, quality checks, a DuckDB SQL database, reusable SQL views, business analysis queries, scorecard exports, static charts, and an interactive Streamlit dashboard.

## Business Question

The main question this project answers is:

How did Capital One's financial performance, credit card portfolio, credit risk, and acquisition-related cost pressure change before, during, and after the Discover acquisition?

To answer this, each quarter was labeled into one of three phases:

* Pre-Discover
* Transition
* Post-Discover

This structure makes it easier to compare performance before the acquisition, during the acquisition close quarter, and after Discover results were included.

## Methodology

The project follows an end-to-end analytics process:

1. Collected quarterly financial metrics from official Capital One financial supplements.
2. Built a raw dataset covering 13 quarters from 2023 Q1 to 2026 Q1.
3. Cleaned the data using Python and Pandas.
4. Added automated data quality checks for row count, missing values, duplicate quarters, valid source URLs, valid phases, and numeric consistency.
5. Loaded the cleaned dataset into DuckDB for SQL analysis.
6. Created reusable SQL views for profitability, expense pressure, credit-risk pressure, Discover cost pressure, and quarter-over-quarter growth.
7. Exported scorecard tables for dashboard use.
8. Generated static charts and built an interactive Streamlit dashboard.

## Key Findings

### 1. Revenue expanded meaningfully after Discover

Average quarterly revenue increased from about $9.5B in the Pre-Discover phase to about $15.4B in the Post-Discover phase. This suggests that the acquisition significantly expanded Capital One's revenue base.

### 2. The transition quarter carried major profitability pressure

2025 Q2 was the transition quarter and showed the largest stress point in the dataset. The quarter had negative net income and the highest provision-to-revenue pressure. This reflects the importance of separating one-time transition impact from ongoing post-acquisition performance.

### 3. Credit card loans increased sharply

Credit card loans rose significantly after Discover was included. This shows the portfolio expansion effect of the acquisition and makes credit-risk monitoring more important after the deal.

### 4. Credit-risk metrics remain central to performance monitoring

Net charge-off rate, delinquency rate, and provision-to-revenue ratio are key indicators for judging whether the larger card portfolio is generating healthy growth or adding risk pressure.

### 5. Discover-related costs should be tracked separately

Integration and amortization expenses became visible after the acquisition and affected reported performance. Tracking these separately helps distinguish core business performance from acquisition-related cost pressure.

## Recommendation

Capital One should monitor the post-Discover portfolio using a recurring quarterly scorecard focused on:

* Revenue growth
* Net income recovery
* Credit card loan growth
* Provision-to-revenue ratio
* Net charge-off rate
* 30+ day delinquency rate
* Efficiency ratio
* Discover integration and amortization cost pressure

The main recommendation is to evaluate the acquisition not only by revenue growth, but also by whether credit risk and integration costs normalize over time.

## Final Takeaway

The acquisition appears to have expanded Capital One's revenue and credit card portfolio, but the transition quarter created a major profitability and credit-loss pressure event. The most important question going forward is whether post-acquisition revenue growth continues while risk indicators and Discover-related cost pressure stabilize.

This project demonstrates a practical analyst workflow by connecting official financial data, SQL analysis, automated quality checks, dashboarding, and business recommendations into one monitoring case.
