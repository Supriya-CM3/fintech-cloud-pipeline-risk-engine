import pandas as pd
from google.cloud import bigquery
import os

def load_csv_to_bigquery():
    print("⏳ Starting database upload sequence...")
    
    project_id = "fintech-genai-pipeline"
    dataset_id = "fintech_raw"
    table_id = "mock_transactions"
    
    full_table_path = f"{project_id}.{dataset_id}.{table_id}"
    local_csv_file = "raw_market_snapshot.csv"
    key_file_path = "bigquery_key.json"
    
    if not os.path.exists(local_csv_file):
        print(f"⚠️ Error: '{local_csv_file}' not found! Run extract_market_data.py first.")
        return
    if not os.path.exists(key_file_path):
        print(f"⚠️ Error: Authentication key '{key_file_path}' missing from your directory!")
        return
        
    try:
        # Initialize connection using your new JSON credentials file
        client = bigquery.Client.from_service_account_json(key_file_path, project=project_id)
        
        # Read the local transactional data snapshot
        df = pd.read_csv(local_csv_file)
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND", 
            autodetect=True                   
        )
        
        print(f"🚀 Pushing data payload directly to cloud table: {full_table_path}...")
        
        job = client.load_table_from_dataframe(df, full_table_path, job_config=job_config)
        job.result() # Wait for job completion
        
        print(f"🎉 Success! Data successfully loaded into BigQuery table '{table_id}'.")
        
    except Exception as e:
        print(f"⚠️ Pipeline execution failed: {e}")

if __name__ == "__main__":
    load_csv_to_bigquery()
