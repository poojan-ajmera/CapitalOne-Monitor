# Final Analysis Report

# Capital One Post-Discover Integration Monitor

## 1. Executive Summary

This project analyzes Capital One's quarterly financial and credit-risk performance from 2023 Q1 through 2026 Q1, with a specific focus on the Discover acquisition period. The purpose of the project is to understand whether the acquisition expanded Capital One's revenue and credit card portfolio while also identifying the risk, profitability, and integration-cost pressures that followed.

The analysis shows that Capital One's average quarterly revenue increased from $9.54B in the Pre-Discover phase to $15.39B in the Post-Discover phase. Credit card loans also increased sharply, from an average of $151.18B before Discover to $273.72B after Discover. This suggests that the acquisition meaningfully expanded the scale of Capital One's card business.

However, the transition quarter, 2025 Q2, showed major pressure. Net income fell to -$4.28B, and provision for credit losses reached 91.5% of revenue. This made 2025 Q2 the highest risk-pressure quarter in the dataset. After the transition quarter, profitability recovered, but credit-risk metrics and Discover-related costs remained important monitoring areas.

The main recommendation is that Capital One should evaluate the Discover acquisition not only through revenue growth, but through a recurring monitoring scorecard that tracks credit card loan growth, net income margin, provision-to-revenue pressure, net charge-off rate, delinquency rate, efficiency ratio, and Discover integration cost pressure.

## 2. Business Problem

Capital One's acquisition of Discover created a major strategic shift in its credit card business. The acquisition expanded the size of the card portfolio, but it also introduced integration costs, amortization expenses, and additional credit-risk exposure.

The core business question for this project is:

How did Capital One's revenue, profitability, credit card loans, credit-risk profile, and Discover-related cost pressure change before, during, and after the Discover acquisition?

To answer this question, the project groups quarterly data into three phases:

* Pre-Discover: quarters before the major acquisition impact
* Transition: the acquisition close and transition quarter
* Post-Discover: quarters after Discover results were included

This structure allows the analysis to compare normal pre-acquisition performance, the acquisition shock period, and the early post-acquisition performance.

## 3. Data Scope and Sources

The dataset covers 13 quarters:

* 2023 Q1 to 2026 Q1

The data was manually compiled from official Capital One quarterly financial supplement PDFs available through Capital One Investor Relations. The project uses consolidated financial metrics, credit quality metrics, credit card loan values, and Discover-related cost disclosures.

The main raw dataset is stored in:

```text
data/raw/capitalone_quarterly_raw.csv
```

The processed dataset is stored in:

```text
data/processed/capitalone_quarterly_clean.csv
```

The scorecard output tables are stored in:

```text
outputs/tables/
```

The chart outputs are stored in:

```text
outputs/charts/
```

## 4. Methodology

The project was built as an end-to-end analytics workflow rather than a one-time spreadsheet analysis.

The workflow included:

1. Collecting official quarterly data from Capital One financial supplements
2. Creating a raw structured dataset
3. Cleaning the dataset using Python and Pandas
4. Running automated data quality checks
5. Building a DuckDB database
6. Creating SQL schema documentation
7. Creating reusable SQL views
8. Writing SQL business questions
9. Exporting scorecard tables
10. Generating static charts
11. Building an interactive Streamlit dashboard
12. Writing business-facing documentation

The main tools used were:

* Python
* Pandas
* DuckDB
* SQL
* Matplotlib
* Plotly
* Streamlit
* Git and GitHub

## 5. KPI Scorecard Results

The phase-level scorecard summarizes performance across the three acquisition phases.

| Acquisition Phase | Quarter Count | Avg Revenue ($M) | Avg Net Income ($M) | Avg Net Income Margin (%) | Avg Credit Card Loans ($M) | Avg Net Charge-Off Rate (%) | Avg 30+ Day Delinquency Rate (%) | Avg Efficiency Ratio (%) | Avg Provision-to-Revenue (%) | Avg Discover Cost-to-Revenue (%) |
| ----------------- | ------------: | ---------------: | ------------------: | ------------------------: | -------------------------: | --------------------------: | -------------------------------: | -----------------------: | ---------------------------: | -------------------------------: |
| Pre-Discover      |             9 |         9,544.33 |            1,226.78 |                     12.85 |                 151,181.44 |                        3.08 |                             3.65 |                    55.48 |                        28.61 |                             0.38 |
| Transition        |             1 |        12,492.00 |           -4,277.00 |                    -34.24 |                 269,709.00 |                        3.24 |                             3.32 |                    55.96 |                        91.50 |                             5.12 |
| Post-Discover     |             3 |        15,391.00 |            2,500.00 |                     16.25 |                 273,721.67 |                        3.35 |                             3.44 |                    56.44 |                        23.65 |                             5.94 |

### Interpretation

The Pre-Discover phase shows a stable baseline, with average quarterly revenue of about $9.54B and average net income of about $1.23B. Credit card loans averaged about $151.18B.

The Transition phase shows the major acquisition impact. Revenue increased to $12.49B, and credit card loans jumped to $269.71B, but net income fell sharply to -$4.28B. The provision-to-revenue ratio reached 91.5%, making this the most stressed quarter in the dataset.

The Post-Discover phase shows a stronger revenue base and profitability recovery. Average quarterly revenue rose to $15.39B, average net income improved to $2.50B, and credit card loans averaged $273.72B. However, Discover cost-to-revenue remained higher than the Pre-Discover period, showing that acquisition-related costs continued after the close.

## 6. Chart-by-Chart Analysis

## Chart 1: Revenue and Net Income Trend

File:

```text
outputs/charts/01_revenue_net_income_trend.png
```

This chart compares total net revenue and net income across all quarters.

The revenue trend shows a clear increase after the Discover transition period. Before 2025 Q2, revenue stayed mostly between $8.9B and $10.2B. In 2025 Q2, revenue rose to $12.49B. In the Post-Discover period, revenue moved above $15B for three consecutive quarters.

Net income tells a more complicated story. Before the acquisition transition, net income was generally positive but uneven. In 2025 Q2, net income dropped to -$4.28B, showing the major transition impact. After that, net income recovered to $3.19B in 2025 Q3, $2.13B in 2025 Q4, and $2.17B in 2026 Q1.

The main insight is that revenue expanded strongly after Discover, but the transition quarter created a major profitability shock.

## Chart 2: Credit Card Loans Trend

File:

```text
outputs/charts/02_credit_card_loans_trend.png
```

This chart tracks credit card loans over time.

Before the Discover acquisition, credit card loans grew gradually from $135.98B in 2023 Q1 to $157.19B in 2025 Q1. In 2025 Q2, credit card loans jumped to $269.71B. This was the largest quarter-over-quarter increase in the dataset, with credit card loans increasing by 71.58%.

After the transition quarter, credit card loans remained elevated, reaching $271.04B in 2025 Q3, $279.57B in 2025 Q4, and $270.56B in 2026 Q1.

The main insight is that the acquisition materially expanded the credit card portfolio. This supports the strategic value of the acquisition from a scale perspective, but it also means credit-risk monitoring becomes more important because the larger portfolio carries more exposure.

## Chart 3: Provision-to-Revenue Pressure

File:

```text
outputs/charts/03_provision_to_revenue_pressure.png
```

This chart measures provision for credit losses as a share of revenue.

The highest pressure quarter was 2025 Q2, with a provision-to-revenue ratio of 91.5%. This was far above the Pre-Discover average of 28.61% and the Post-Discover average of 23.65%.

Other high-pressure quarters included:

| Quarter | Phase        | Revenue ($M) | Provision for Credit Losses ($M) | Provision-to-Revenue (%) |
| ------- | ------------ | -----------: | -------------------------------: | -----------------------: |
| 2025 Q2 | Transition   |       12,492 |                           11,430 |                    91.50 |
| 2024 Q2 | Pre-Discover |        9,506 |                            3,909 |                    41.12 |
| 2023 Q1 | Pre-Discover |        8,903 |                            2,795 |                    31.39 |
| 2023 Q4 | Pre-Discover |        9,506 |                            2,857 |                    30.05 |
| 2024 Q1 | Pre-Discover |        9,402 |                            2,683 |                    28.54 |

The main insight is that 2025 Q2 was not just a normal quarter with higher revenue. It was a major risk and accounting pressure quarter. For a financial institution, this matters because revenue growth is only valuable if credit losses remain manageable.

## Chart 4: Credit Risk Rates Trend

File:

```text
outputs/charts/04_credit_risk_rates_trend.png
```

This chart tracks two credit-risk indicators:

* Net charge-off rate
* 30+ day delinquency rate

The Pre-Discover average net charge-off rate was 3.08%, while the Post-Discover average was 3.35%. This shows a modest increase after the acquisition. The 30+ day delinquency rate averaged 3.65% before Discover and 3.44% after Discover, which means delinquency did not spike in the early Post-Discover quarters based on this dataset.

The transition quarter had a net charge-off rate of 3.24% and a delinquency rate of 3.32%. These were not the highest values in the dataset, but the provision-to-revenue pressure was extremely high. This suggests that the transition stress came more from provision expense and acquisition-related accounting impact than from an immediate delinquency spike.

The main insight is that credit risk must continue to be monitored, but the early Post-Discover period does not show a dramatic delinquency spike in the data used here.

## Chart 5: Discover Cost Pressure

File:

```text
outputs/charts/05_discover_cost_pressure.png
```

This chart tracks Discover integration and amortization costs as a share of revenue.

In the Pre-Discover period, Discover cost-to-revenue was very low, averaging 0.38%. This increased to 5.12% in the transition quarter and averaged 5.94% in the Post-Discover period.

This shows that Discover-related expenses became a meaningful part of the cost structure after the acquisition. These costs do not necessarily mean the acquisition is unsuccessful, but they should be separated from core business performance so analysts can understand whether normal operations are improving.

The main insight is that management should continue tracking Discover-related costs separately until they stabilize.

## 7. SQL Business Question Findings

The SQL analysis focused on six business questions.

## Question 1: How did performance change by acquisition phase?

The phase summary showed that Post-Discover average revenue was much higher than Pre-Discover revenue. Average revenue increased from $9.54B to $15.39B. Average credit card loans increased from $151.18B to $273.72B.

This confirms that Discover changed the size and scale of Capital One's credit card business.

## Question 2: Which quarters had the highest credit risk pressure?

The highest risk-pressure quarter was 2025 Q2, with provision-to-revenue of 91.5%. This was much higher than every other quarter.

This quarter should be treated separately in analysis because it represents a major transition event, not a normal operating quarter.

## Question 3: Which quarters had the highest Discover-related cost pressure?

Discover-related cost pressure increased sharply after the acquisition. The Post-Discover period had an average Discover cost-to-revenue ratio of 5.94%, compared to 0.38% in the Pre-Discover period.

This means acquisition-related costs remained visible even after the transition quarter.

## Question 4: How did credit card loans grow quarter over quarter?

Credit card loans increased 71.58% in 2025 Q2. This was the largest portfolio growth point in the dataset and reflects the inclusion of Discover.

After 2025 Q2, credit card loans remained near the new higher base, showing that the acquisition permanently changed the portfolio scale.

## Question 5: Which quarters show strong revenue growth but elevated risk?

2025 Q2 and 2025 Q3 are the most important quarters for this question. 2025 Q2 showed strong revenue growth but extremely high provision pressure and negative net income. 2025 Q3 showed further revenue growth and profitability recovery, while provision-to-revenue normalized to 17.67%.

This suggests that the immediate transition quarter was highly pressured, but early post-transition performance improved.

## Question 6: What is the quarterly trend of core monitoring metrics?

The quarterly monitoring table shows that after 2025 Q2, Capital One operated at a higher revenue and loan base. The key question going forward is whether this higher base can remain profitable while credit losses and integration costs stay controlled.

## 8. Risk and Integration Cost Interpretation

The biggest risk signal in the project is not simply that credit card loans increased. The larger issue is whether the larger portfolio creates higher losses or higher provisions over time.

The analysis shows three different types of pressure:

1. Transition pressure
   2025 Q2 had a major negative net income event and very high provision-to-revenue.

2. Credit-risk pressure
   Net charge-off rates and delinquency rates remained important but did not show an extreme post-acquisition spike in the available data.

3. Integration cost pressure
   Discover-related costs became meaningful after the acquisition and should be tracked separately from normal operations.

This separation matters because an analyst should not treat every expense increase the same way. Some costs may be one-time or acquisition-related, while others may reflect ongoing business risk.

## 9. Business Recommendations

Based on the analysis, Capital One should continue monitoring the Discover acquisition using a recurring quarterly scorecard.

The scorecard should include:

* Total net revenue
* Net income
* Net income margin
* Credit card loans
* Credit card loan quarter-over-quarter growth
* Provision-to-revenue ratio
* Net charge-off rate
* 30+ day delinquency rate
* Efficiency ratio
* Discover integration and amortization cost-to-revenue

The most important recommendation is to evaluate the acquisition through both growth and risk.

Revenue growth alone is not enough. Capital One should monitor whether the larger credit card portfolio continues to produce stronger revenue while credit losses, delinquencies, and acquisition-related costs normalize.

A simple decision framework could be:

* If revenue grows and credit-risk metrics stay stable, the acquisition is strengthening the portfolio.
* If revenue grows but provisions and charge-offs rise faster, the acquisition may be adding risk pressure.
* If Discover-related costs remain elevated, reported profitability may continue to be affected even if core operations improve.

## 10. Limitations

This project uses publicly available quarterly financial supplement data. That means the analysis is based on company-level and segment-level reported metrics, not internal customer-level data.

Important limitations include:

* The dataset has only 13 quarters.
* The Post-Discover phase has only three quarters.
* The analysis does not include individual customer behavior.
* The project does not model credit risk at the account level.
* Some acquisition-related effects may be accounting-driven and require deeper financial statement context.
* Public data limits the ability to separate all one-time costs from recurring operating costs.

Because of these limitations, this project should be viewed as a monitoring and strategy analytics case, not as a full credit-risk model.

## 11. Future Improvements

Future versions of this project could include:

1. Risk scoring logic
   Create a quarterly risk flag such as Normal, Watch, or High Pressure based on provision-to-revenue, charge-off rate, delinquency rate, net income margin, and Discover cost pressure.

2. Forecasting
   Build a simple forecast for revenue, credit card loans, or provision-to-revenue using time-series methods.

3. Peer comparison
   Compare Capital One's credit card performance with other card issuers using public financial data.

4. More detailed segment analysis
   Add business segment-level data from Capital One's credit card business tables.

5. Dashboard deployment
   Deploy the Streamlit dashboard online so users can access it without running the project locally.

6. Automated data collection
   Build a script to download new quarterly supplements and update the dataset as new results are released.

## 12. Conclusion

This project shows that the Discover acquisition significantly expanded Capital One's revenue base and credit card portfolio. Average quarterly revenue increased from $9.54B in the Pre-Discover period to $15.39B in the Post-Discover period, and average credit card loans increased from $151.18B to $273.72B.

At the same time, the transition quarter created a major profitability and provision-pressure event. 2025 Q2 had negative net income and the highest provision-to-revenue ratio in the dataset. This makes it important to separate transition-quarter effects from the early post-acquisition operating trend.

The early Post-Discover period shows stronger revenue and profitability recovery, but continued monitoring is necessary. The key question is whether the larger portfolio can produce sustainable revenue growth while credit-risk indicators and Discover-related costs remain controlled.

Overall, the project demonstrates how official financial data can be converted into a structured analytics pipeline, SQL analysis layer, dashboard, and business recommendation framework.
