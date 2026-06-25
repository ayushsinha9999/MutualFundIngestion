# Bluestock Mutual Fund Analytics - Data Dictionary

## Overview
This database uses a Star Schema design to optimize analytical queries for mutual fund performance, NAV history, and investor transactions.

## Dimension Tables
### `dim_fund`
* **amfi_code (INTEGER):** Primary Key. Unique identifier for the mutual fund assigned by AMFI.
* **fund_name (TEXT):** The official name of the mutual fund.
* **category (TEXT):** The classification of the fund (e.g., Equity, Debt, Hybrid).
* **fund_house (TEXT):** The Asset Management Company (AMC) managing the fund.

### `dim_date`
* **date_id (TEXT):** Primary Key. Stored in YYYY-MM-DD format.
* **year (INTEGER):** The calendar year.
* **month (INTEGER):** The calendar month (1-12).
* **day (INTEGER):** The day of the month (1-31).
* **is_weekend (BOOLEAN):** True if the date falls on a Saturday or Sunday.

## Fact Tables
### `fact_nav`
* **nav_id (INTEGER):** Primary Key. Auto-incremented ID.
* **amfi_code (INTEGER):** Foreign Key linking to `dim_fund`.
* **date_id (TEXT):** Foreign Key linking to `dim_date`.
* **nav (REAL):** The Net Asset Value of the fund on that specific date.

### `fact_transactions`
* **transaction_id (TEXT):** Primary Key. Unique identifier for the transaction.
* **amfi_code (INTEGER):** Foreign Key linking to `dim_fund`.
* **transaction_date (TEXT):** Foreign Key linking to `dim_date`.
* **transaction_type (TEXT):** The category of transaction (SIP, LUMPSUM, REDEMPTION).
* **amount_inr (REAL):** The total monetary value of the transaction in Indian Rupees.

### `fact_performance`
* **perf_id (INTEGER):** Primary Key. Auto-incremented ID.
* **amfi_code (INTEGER):** Foreign Key linking to `dim_fund`.
* **expense_ratio (REAL):** The annual maintenance charge levied by the mutual fund (typically 0.1% - 2.5%).
* **is_anomaly (BOOLEAN):** Flag denoting if the fund's return metrics were missing or mathematically unrealistic.