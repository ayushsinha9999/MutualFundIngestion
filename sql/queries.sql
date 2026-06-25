-- 1. Top 5 funds by AUM (Assets Under Management)
SELECT f.fund_name, f.category, a.aum_value
FROM fact_aum a
JOIN dim_fund f ON a.amfi_code = f.amfi_code
ORDER BY a.aum_value DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT d.year, d.month, ROUND(AVG(n.nav), 2) AS avg_monthly_nav
FROM fact_nav n
JOIN dim_date d ON n.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year DESC, d.month DESC;

-- 3. SIP YoY (Year-over-Year) Growth
SELECT d.year, SUM(t.amount_inr) AS total_sip_volume
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year ASC;

-- 4. Transactions by State (Assuming state data exists in a dimension or raw table)
SELECT state, COUNT(transaction_id) AS total_transactions, SUM(amount_inr) AS total_volume
FROM raw_investor_transactions -- Using raw table name as state wasn't in our core fact table
GROUP BY state
ORDER BY total_volume DESC;

-- 5. Funds with expense_ratio < 1%
SELECT f.fund_name, p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. Highest single Lumpsum investments
SELECT transaction_id, amfi_code, transaction_date, amount_inr
FROM fact_transactions
WHERE transaction_type = 'LUMPSUM'
ORDER BY amount_inr DESC
LIMIT 10;

-- 7. Count of performance anomalies detected
SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE is_anomaly = TRUE;

-- 8. Total Redemption Volume vs SIP Volume
SELECT transaction_type, SUM(amount_inr) AS total_amount, COUNT(transaction_id) AS transaction_count
FROM fact_transactions
GROUP BY transaction_type;

-- 9. NAV Volatility (Max vs Min NAV per fund)
SELECT amfi_code, MAX(nav) AS highest_nav, MIN(nav) AS lowest_nav, (MAX(nav) - MIN(nav)) AS nav_spread
FROM fact_nav
GROUP BY amfi_code
ORDER BY nav_spread DESC
LIMIT 10;

-- 10. Number of funds by Category
SELECT category, COUNT(amfi_code) as total_funds
FROM dim_fund
GROUP BY category
ORDER BY total_funds DESC;