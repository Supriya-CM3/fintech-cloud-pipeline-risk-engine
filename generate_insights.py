import warnings
warnings.filterwarnings("ignore")

import os
import pandas as pd
from google.cloud import bigquery

def run_advanced_analytics():
    print("⏳ Activating Deep Cloud Analytics Suite...")
    project_id = "fintech-genai-pipeline"
    key_file_path = "../bigquery_key.json" 
    
    try:
        client = bigquery.Client.from_service_account_json(key_file_path, project=project_id)
        
        # SQL Query to pull raw metrics data fields from the warehouse table schema
        sql_query = f"""
            SELECT 
                ticker, 
                market_price, 
                risk_score, 
                transaction_volume
            FROM `{project_id}.fintech_raw.mock_transactions`
        """
        print("📊 Fetching live transaction rows from BigQuery...")
        df = client.query(sql_query).to_dataframe()
        
        print("\n🏆 COMPREHENSIVE ADVANCED PORTFOLIO RISK REPORT:")
        print("==========================================================================")
        
        # Iterating across transaction groups to parse financial metrics fields
        for ticker, group in df.groupby('ticker'):
            avg_price = group['market_price'].mean()
            avg_risk = group['risk_score'].mean()
            total_vol = group['transaction_volume'].sum()
            
            # Compute consolidated capital metrics indicators
            capital_exposure = (group['market_price'] * group['transaction_volume']).sum()
            price_spread = group['market_price'].max() - group['market_price'].min()
            
            # Anomaly detection counts mapping risk threshold limits
            high_risk_trades = int((group['risk_score'] > 0.75).sum())
            total_trades = int(group.shape[0])
            high_risk_rate = (high_risk_trades / total_trades) * 100 if total_trades > 0 else 0.0
            
            whale_trades = int((group['transaction_volume'] > 40000).sum())
            
            print(f"🔹 ASSET SUMMARY: {ticker}")
            print(f"  • Baseline: Avg Price: \${avg_price:,.2f} | Avg Risk Score: {avg_risk:.2f}")
            print(f"  • Total Capital Exposure: \${capital_exposure:,.2f}")
            print(f"  • Price Volatility Spread: \${price_spread:,.2f}")
            print(f"  • High-Risk Anomaly Rate: {high_risk_rate:.1f}% ({high_risk_trades} flags)")
            print(f"  • Institutional 'Whale' Trades Detected: {whale_trades}")
            print("-" * 74)
            
        print("\n🎉 SUCCESS! Advanced Data Engineering Indicators Generated successfully!")
        
    except Exception as e:
        print(f"⚠️ Error running analytics layer: {e}")

if __name__ == "__main__":
    run_advanced_analytics()
