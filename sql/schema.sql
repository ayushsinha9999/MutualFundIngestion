-- ==========================================
-- DIMENSION TABLES (The "Who, What, When")
-- ==========================================

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_name TEXT,
    category TEXT,
    fund_house TEXT
);

CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY, -- Stored as YYYY-MM-DD
    year INTEGER,
    month INTEGER,
    day INTEGER,
    is_weekend BOOLEAN
);

-- ==========================================
-- FACT TABLES (The "Metrics and Events")
-- ==========================================

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id TEXT,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY, -- Using investor_id or generated ID
    amfi_code INTEGER,
    transaction_date TEXT,
    transaction_type TEXT,
    amount_inr REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_performance (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    expense_ratio REAL,
    is_anomaly BOOLEAN,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id TEXT,
    aum_value REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);