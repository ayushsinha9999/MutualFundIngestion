import pandas as pd
import os

def clean_nav_history():
    input_file = 'data/raw/02_nav_history.csv'
    output_dir = 'data/processed'
    output_file = f'{output_dir}/cleaned_nav_history.csv'

    # Ensure the processed folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    print("Starting NAV History cleaning process...")
    
    # 1. Load the dataset
    df = pd.read_csv(input_file)

    # 2. Parse dates to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # 3. Remove duplicates
    df = df.drop_duplicates(subset=['amfi_code', 'date'], keep='last')

    # 4. Validate NAV > 0
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df[df['nav'] > 0]

    # 5. Sort by amfi_code + date
    df = df.sort_values(by=['amfi_code', 'date'])

    # 6. Forward-fill missing NAV for holidays/weekends
    df = df.set_index('date')
    
    clean_df = (
        df.groupby('amfi_code')['nav']
          .resample('D')
          .ffill()
          .reset_index()
    )

    
    clean_df.to_csv(output_file, index=False)
    print(f"Cleaning complete. File saved to {output_file} with shape: {clean_df.shape}")

def clean_investor_transactions():
    input_file = 'data/raw/08_investor_transactions.csv' 
    output_dir = 'data/processed'
    output_file = f'{output_dir}/cleaned_investor_transactions.csv'
    
    os.makedirs(output_dir, exist_ok=True)
    print("\nStarting Investor Transactions cleaning process...")
    
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # 1. Fix date formats
    date_col = 'transaction_date' if 'transaction_date' in df.columns else 'date'
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # 2. Standardize transaction_type values (SIP/Lumpsum/Redemption)
    df['transaction_type'] = df['transaction_type'].astype(str).str.strip().str.upper()
    df['transaction_type'] = df['transaction_type'].replace({'LUMP SUM': 'LUMPSUM'})
    
    valid_types = ['SIP', 'LUMPSUM', 'REDEMPTION']
    df = df[df['transaction_type'].isin(valid_types)]
    
    # 3. Validate amount > 0
    df['amount_inr'] = pd.to_numeric(df['amount_inr'], errors='coerce')
    df = df[df['amount_inr'] > 0]
    
    # 4. Check KYC status enum values
    if 'kyc_status' in df.columns:
        df['kyc_status'] = df['kyc_status'].astype(str).str.strip().str.upper()
        
    # Save to processed folder
    df.to_csv(output_file, index=False)
    print(f"Cleaning complete. File saved to {output_file} with shape: {df.shape}")
    
def clean_scheme_performance():
    input_file = 'data/raw/07_scheme_performance.csv' 
    output_dir = 'data/processed'
    output_file = f'{output_dir}/cleaned_scheme_performance.csv'
    
    print("\nStarting Scheme Performance cleaning process...")
    
   # Load the dataset
    df = pd.read_csv(input_file)
    
    # Rename the column to match our SQL schema
    df.rename(columns={'expense_ratio_pct': 'expense_ratio'}, inplace=True)
    
    # 1. Validate all return values are numeric
    # Automatically find any columns that contain the word 'return' (e.g., 1Y_return, 3Y_return)
    return_cols = [col for col in df.columns if 'return' in col.lower()]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 2. Flag anomalies
    # We will flag a row as True if any of its return values turned into NaN (bad data)
    # or if the return is completely unrealistic (e.g., > 500% or < -100%)
    df['is_anomaly'] = False
    for col in return_cols:
        anomaly_condition = df[col].isna() | (df[col] > 500) | (df[col] < -100)
        df.loc[anomaly_condition, 'is_anomaly'] = True

    # 3. Check expense_ratio range (0.1% - 2.5%)
    # Keep only rows where expense ratio is within limits, or handle missing ones
    if 'expense_ratio' in df.columns:
        df['expense_ratio'] = pd.to_numeric(df['expense_ratio'], errors='coerce')
        df = df[(df['expense_ratio'] >= 0.1) & (df['expense_ratio'] <= 2.5)]
        
    # Save to processed folder
    df.to_csv(output_file, index=False)
    print(f"Cleaning complete. File saved to {output_file} with shape: {df.shape}")

if __name__ == "__main__":
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()