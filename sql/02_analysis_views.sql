-- Capital One Post-Discover Monitoring Project
-- Analysis Views
-- These views create reusable business metrics for analysis and dashboarding.

CREATE OR REPLACE VIEW v_capitalone_metrics AS
SELECT
    quarter,
    period_end,
    year,
    quarter_num,
    acquisition_phase,

    total_net_revenue_m,
    net_income_m,
    diluted_eps,
    adjusted_eps,
    non_interest_expense_m,
    provision_credit_losses_m,
    net_interest_margin_pct,
    efficiency_ratio_pct,
    credit_card_loans_m,
    net_charge_off_rate_pct,
    delinquency_30_plus_pct,
    discover_integration_expense_m,
    discover_amortization_expense_m,
    marketing_expense_m,
    operating_expense_m,

    -- Profitability metrics
    ROUND(net_income_m / total_net_revenue_m * 100, 2) AS net_income_margin_pct,

    -- Expense mix
    ROUND(non_interest_expense_m / total_net_revenue_m * 100, 2) AS non_interest_expense_to_revenue_pct,
    ROUND(marketing_expense_m / total_net_revenue_m * 100, 2) AS marketing_to_revenue_pct,
    ROUND(operating_expense_m / total_net_revenue_m * 100, 2) AS operating_expense_to_revenue_pct,

    -- Credit risk pressure
    ROUND(provision_credit_losses_m / total_net_revenue_m * 100, 2) AS provision_to_revenue_pct,

    -- Discover-related cost pressure
    ROUND(
        (discover_integration_expense_m + discover_amortization_expense_m)
        / total_net_revenue_m * 100,
        2
    ) AS discover_cost_to_revenue_pct,

    -- Credit card portfolio growth
    LAG(credit_card_loans_m) OVER (ORDER BY period_end) AS prior_quarter_credit_card_loans_m,
    ROUND(
        (credit_card_loans_m - LAG(credit_card_loans_m) OVER (ORDER BY period_end))
        / LAG(credit_card_loans_m) OVER (ORDER BY period_end) * 100,
        2
    ) AS credit_card_loans_qoq_growth_pct,

    -- Revenue growth
    LAG(total_net_revenue_m) OVER (ORDER BY period_end) AS prior_quarter_revenue_m,
    ROUND(
        (total_net_revenue_m - LAG(total_net_revenue_m) OVER (ORDER BY period_end))
        / LAG(total_net_revenue_m) OVER (ORDER BY period_end) * 100,
        2
    ) AS revenue_qoq_growth_pct,

    source_name,
    source_url,
    notes

FROM capitalone_quarterly;


CREATE OR REPLACE VIEW v_phase_summary AS
SELECT
    acquisition_phase,
    COUNT(*) AS quarter_count,

    ROUND(AVG(total_net_revenue_m), 2) AS avg_revenue_m,
    ROUND(AVG(net_income_m), 2) AS avg_net_income_m,
    ROUND(AVG(net_income_margin_pct), 2) AS avg_net_income_margin_pct,

    ROUND(AVG(credit_card_loans_m), 2) AS avg_credit_card_loans_m,
    ROUND(AVG(net_charge_off_rate_pct), 2) AS avg_net_charge_off_rate_pct,
    ROUND(AVG(delinquency_30_plus_pct), 2) AS avg_delinquency_30_plus_pct,

    ROUND(AVG(efficiency_ratio_pct), 2) AS avg_efficiency_ratio_pct,
    ROUND(AVG(provision_to_revenue_pct), 2) AS avg_provision_to_revenue_pct,
    ROUND(AVG(discover_cost_to_revenue_pct), 2) AS avg_discover_cost_to_revenue_pct

FROM v_capitalone_metrics
GROUP BY acquisition_phase;