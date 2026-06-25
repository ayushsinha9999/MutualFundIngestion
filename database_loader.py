import sqlite3
import pandas as pd
import os

def build_and_load_db():
    db_path = 'data/processed/bluestock_mf.db'
    
    print("1. Initializing SQLite Database...")
    # This creates the .db file if it doesn't exist
    conn = sqlite3.connect(db_path)
    
    # Read and execute your schema.sql
    with open('sql/schema.sql', 'r') as f:
        conn.executescript(f.read())
        
    print("2. Loading Cleaned Data into Tables...")
    
    # --- Load Fact NAV ---
    nav_df = pd.read_csv('data/processed/cleaned_nav_history.csv')
    # Rename column to match your SQL schema exactly
    nav_df.rename(columns={'date': 'date_id'}, inplace=True)
    # Select only the columns needed for the database
    nav_df[['amfi_code', 'date_id', 'nav']].to_sql('fact_nav', conn, if_exists='append', index=False)
    
    # --- Load Fact Transactions ---
    txn_df = pd.read_csv('data/processed/cleaned_investor_transactions.csv')
    # Generate a unique transaction ID using investor_id + the row index
    txn_df['transaction_id'] = txn_df['investor_id'].astype(str) + '_' + txn_df.index.astype(str)
    txn_cols = ['transaction_id', 'amfi_code', 'transaction_date', 'transaction_type', 'amount_inr']
    txn_df[txn_cols].to_sql('fact_transactions', conn, if_exists='append', index=False)
    
    # --- Load Fact Performance ---
    perf_df = pd.read_csv('data/processed/cleaned_scheme_performance.csv')
    perf_cols = ['amfi_code', 'expense_ratio', 'is_anomaly']
    perf_df[perf_cols].to_sql('fact_performance', conn, if_exists='append', index=False)
    
    print("\n3. Verifying Row Counts...")
    for table in ['fact_nav', 'fact_transactions', 'fact_performance']:
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
        print(f" - {table}: {count} rows")
        
    conn.close()
    print("\nDatabase build complete! 🚀")

if __name__ == "__main__":
    build_and_load_db()