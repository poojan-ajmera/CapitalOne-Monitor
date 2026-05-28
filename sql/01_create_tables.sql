-- Capital One Post-Discover Monitoring Project
-- Table Creation Script
-- This script defines the main quarterly financial table.

DROP TABLE IF EXISTS capitalone_quarterly;

CREATE TABLE capitalone_quarterly (
    quarter VARCHAR,
    period_end DATE,
    acquisition_phase VARCHAR,

    total_net_revenue_m DOUBLE,
    net_income_m DOUBLE,
    diluted_eps DOUBLE,
    adjusted_eps DOUBLE,
    non_interest_expense_m DOUBLE,
    provision_credit_losses_m DOUBLE,
    net_interest_margin_pct DOUBLE,
    efficiency_ratio_pct DOUBLE,
    credit_card_loans_m DOUBLE,
    net_charge_off_rate_pct DOUBLE,
    delinquency_30_plus_pct DOUBLE,
    discover_integration_expense_m DOUBLE,
    discover_amortization_expense_m DOUBLE,
    marketing_expense_m DOUBLE,
    operating_expense_m DOUBLE,

    source_name VARCHAR,
    source_url VARCHAR,
    notes VARCHAR,

    year INTEGER,
    quarter_num INTEGER
);