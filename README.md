# fintech-cloud-pipeline-risk-engine

# FinTech Cloud Data Ingestion & Portfolio Risk Analytics Engine

An automated pipeline that loads **simulated** multi-asset market data into Google BigQuery, calculates portfolio risk metrics with Pandas, generates an executive summary with Gemini, and serves a live Looker Studio dashboard.

> **Note:** All data is simulated (100 records across 5 assets, about 20 per asset). Results demonstrate the pipeline, not real market conclusions.

## Business problem
Risk reporting normally means ad-hoc SQL, manual spreadsheet work and a long wait before leadership sees numbers. This project replaces that with a one-click run.

## Pipeline
1. **Ingest:** a Python script simulates a market stream (BTC-USD, ETH-USD, AAPL, PYPL, VISA-US) with price, timestamp, volume and a risk score.
2. **Store:** records are loaded into BigQuery using an IAM service account.
3. **Analyze:** Pandas calculates capital exposure, price volatility spread, high-risk anomaly rate and whale-trade counts per asset.
4. **Summarize:** Gemini 1.5 Flash writes a plain-English executive summary of the metrics.
5. **Visualize:** Looker Studio reads the BigQuery table directly.

## Key results (simulated sample)
| Asset | Avg risk | Anomaly rate | Capital exposure |
|---|---|---|---|
| BTC-USD | 0.54 | 18.2% | $36.97B |
| PYPL | 0.49 | 30.0% | $29.996M |
| VISA-US | 0.52 | 28.6% | $103.16M |
| AAPL | 0.48 | 20.0% | $106.33M |
| ETH-USD | 0.41 | 16.7% | $1.909B |

**Recommendation:** review BTC-USD exposure limits first, then investigate PYPL and VISA-US anomalies. Validate on a larger dataset before acting.

## Technical note: Gemini API key
New API keys with an `AQ.` prefix returned 404 errors when passed in the URL (`?key=...`). Sending the key in the `x-goog-api-key` request header fixed it.

## Tech stack
Python, Pandas, Google BigQuery, Google IAM, Gemini 1.5 Flash, Looker Studio

## Setup
```bash
pip install pandas google-cloud-bigquery
```
1. Create a BigQuery project, dataset and service account.
2. Download the service-account JSON key and set `GOOGLE_APPLICATION_CREDENTIALS` to its path.
3. Set your Gemini key as an environment variable (never hard-code it).
4. Run the ingestion script, then the analytics script.

## Security
Never commit the service-account JSON key or API keys. Add them to `.gitignore`:
```
*.json
.env
```

## Limitations and next steps
- Replace simulated data with thousands of real market rows
- Apply the same pipeline to lending data (NPA, DPD buckets, collateral risk)
- Schedule automatic refresh
- Add unit tests for the metric calculations

## Author
Supriya, Business Analyst | Data Analyst
