import requests
import pandas as pd
import os
import time

# Ensure the target directory exists
os.makedirs('data/raw', exist_ok=True)

def fetch_and_save_nav(scheme_code, scheme_name):
    print(f"Fetching NAV for: {scheme_name} (Code: {scheme_code})...")
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors
        
        json_data = response.json()
        
        # Extract the historical NAV data array
        if 'data' in json_data and len(json_data['data']) > 0:
            df = pd.DataFrame(json_data['data'])
            
            # Add scheme code and name for identification
            df['scheme_code'] = scheme_code
            df['scheme_name'] = scheme_name
            
            # Save as raw CSV
            file_path = f"data/raw/nav_{scheme_code}.csv"
            df.to_csv(file_path, index=False)
            print(f"  -> Successfully saved {len(df)} records to {file_path}\n")
        else:
            print(f"  -> No data found for {scheme_name}.\n")
            
    except requests.exceptions.RequestException as e:
        print(f"  -> API Request failed for {scheme_name}: {e}\n")

if __name__ == "__main__":
    # Dictionary of the specific schemes requested in the task
    target_schemes = {
        "125497": "HDFC Top 100 Direct",
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    
    print("--- Starting Live NAV Fetch ---")
    for code, name in target_schemes.items():
        fetch_and_save_nav(code, name)
        time.sleep(1) # Polite delay between API calls
        
    print("--- Fetch Complete ---")
    import pandas as pd
import glob
import os

RAW_DATA_DIR = "data/raw"

def load_and_inspect_datasets():
    print("=== TASK: LOAD AND INSPECT 10 CSV DATASETS ===\n")
    csv_files = glob.glob(f"{RAW_DATA_DIR}/*.csv")
    
    if not csv_files:
        print(f"No CSV files found in {RAW_DATA_DIR}. Please place your 10 provided datasets here.")
        return {}
        
    dataframes = {}
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        print(f"--- Inspecting: {filename} ---")
        try:
            df = pd.read_csv(file_path)
            dataframes[filename] = df
            
            print(f"Shape: {df.shape}")
            print(f"\nData Types:\n{df.dtypes}")
            print(f"\nHead (First 2 rows):\n{df.head(2)}")
            print("-" * 50 + "\n")
        except Exception as e:
            print(f"Error reading {filename}: {e}\n")
            
    return dataframes

def explore_fund_master(fund_master_df):
    print("=== TASK: EXPLORE FUND MASTER ===\n")
    # Adjust these column names if your provided CSV uses different headers
    columns_to_explore = ['fund_house', 'category', 'sub_category', 'risk_grade']
    
    for col in columns_to_explore:
        if col in fund_master_df.columns:
            unique_vals = fund_master_df[col].dropna().unique()
            print(f"Unique {col}s ({len(unique_vals)} total):")
            print(unique_vals[:10]) # Printing first 10 for brevity, remove [:10] to see all
            print("\n")
        else:
            print(f"Column '{col}' not found. Check your CSV headers.\n")

def validate_amfi_codes(fund_master_df, nav_history_df):
    print("=== TASK: VALIDATE AMFI CODES ===\n")
    
    # Adjust column names based on the actual CSV headers provided to you
    master_code_col = 'amfi_code' 
    nav_code_col = 'amfi_code' 
    
    if master_code_col in fund_master_df.columns and nav_code_col in nav_history_df.columns:
        master_codes = set(fund_master_df[master_code_col].dropna().astype(str))
        nav_codes = set(nav_history_df[nav_code_col].dropna().astype(str))
        
        missing_in_nav = master_codes - nav_codes
        
        print("--- Data Quality Summary ---")
        print(f"Total unique codes in Fund Master: {len(master_codes)}")
        print(f"Total unique codes in NAV History: {len(nav_codes)}")
        
        if not missing_in_nav:
            print("Status: PERFECT MATCH. Every code in fund_master exists in nav_history.")
        else:
            print(f"Status: ANOMALY DETECTED. {len(missing_in_nav)} codes in fund_master are missing from nav_history.")
            print(f"Sample of missing codes: {list(missing_in_nav)[:5]}")
    else:
        print("Validation failed: Could not find the correct amfi_code columns in the dataframes.")

if __name__ == "__main__":
    # 1. Load data and print shape, dtypes, and head
    loaded_dfs = load_and_inspect_datasets()
    
    # 2. Explore Fund Master & Validate
    # NOTE: You must update 'fund_master.csv' and 'nav_history.csv' below 
    # to match the EXACT filenames of the datasets provided by Bluestock.
    
    fund_master_filename = '01_fund_master.csv' # CHANGE THIS IF NEEDED
    nav_history_filename = '02_nav_history.csv' # CHANGE THIS IF NEEDED
    
    if fund_master_filename in loaded_dfs and nav_history_filename in loaded_dfs:
        explore_fund_master(loaded_dfs[fund_master_filename])
        validate_amfi_codes(loaded_dfs[fund_master_filename], loaded_dfs[nav_history_filename])
    else:
        print(f"Skipping exploration and validation. Make sure {fund_master_filename} and {nav_history_filename} exist in data/raw/")