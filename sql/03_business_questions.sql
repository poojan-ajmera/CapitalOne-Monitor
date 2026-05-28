-- Capital One Post-Discover Monitoring Project
-- Business Questions
-- These queries translate the cleaned data into business-facing insights.

-- Question 1:
-- How did revenue, profitability, and credit card loans change across
-- Pre-Discover, Transition, and Post-Discover phases?
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
    END;


-- Question 2:
-- Which quarters had the highest credit risk pressure?
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
LIMIT 5;


-- Question 3:
-- Which quarters had the highest Discover-related cost pressure?
SELECT
    quarter,
    acquisition_phase,
    total_net_revenue_m,
    discover_integration_expense_m,
    discover_amortization_expense_m,
    discover_cost_to_revenue_pct
FROM v_capitalone_metrics
ORDER BY discover_cost_to_revenue_pct DESC
LIMIT 5;


-- Question 4:
-- How did credit card loans grow quarter over quarter?
SELECT
    quarter,
    acquisition_phase,
    credit_card_loans_m,
    prior_quarter_credit_card_loans_m,
    credit_card_loans_qoq_growth_pct
FROM v_capitalone_metrics
ORDER BY period_end;


-- Question 5:
-- What quarters show the strongest revenue growth but also elevated risk?
SELECT
    quarter,
    acquisition_phase,
    total_net_revenue_m,
    revenue_qoq_growth_pct,
    net_charge_off_rate_pct,
    delinquency_30_plus_pct,
    provision_to_revenue_pct
FROM v_capitalone_metrics
WHERE revenue_qoq_growth_pct IS NOT NULL
ORDER BY revenue_qoq_growth_pct DESC;


-- Question 6:
-- What is the quarterly trend of the core monitoring metrics?
SELECT
    quarter,
    acquisition_phase,
    total_net_revenue_m,
    net_income_m,
    adjusted_eps,
    efficiency_ratio_pct,
    provision_to_revenue_pct,
    net_charge_off_rate_pct,
    delinquency_30_plus_pct,
    discover_cost_to_revenue_pct
FROM v_capitalone_metrics
ORDER BY period_end;