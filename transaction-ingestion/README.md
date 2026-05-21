# Component 1: Transaction Ingestion

**Owner:** Ergi Sula  
**Project:** Financial Fraud Detection System  
**Tools:** n8n, Airtable  

---

## Overview

This component is the entry point of the Financial Fraud Detection pipeline. It fetches raw transaction data from a CSV file hosted on GitHub, normalizes each record into a structured schema, and writes the results to an Airtable base where downstream components can process them.

---

## How It Works

The n8n workflow runs in 4 steps:

1. **Manual Trigger** — Workflow is started manually (used for demo and testing)
2. **Fetch CSV** — HTTP GET request pulls the raw CSV from GitHub
3. **Parse & Normalize** — Code node parses each row, cleans the data, converts timestamps to ISO format, and tags each record with `status: unprocessed` and `source: csv_ingestion`
4. **Write to Airtable** — Each normalized record is written as a new row in the Transactions table

---

## Input

Raw transaction CSV file hosted on GitHub with the following columns:

| Column | Description |
|---|---|
| transaction_id | Unique transaction identifier (e.g. TXN-026) |
| timestamp | Date and time of transaction |
| account_id | Account identifier (e.g. ACCT-1234-5678) |
| amount | Transaction amount in USD |
| merchant | Merchant name |
| location | City/country of transaction |

---

## Output

Structured records written to the **Transactions** table in Airtable with the following schema:

| Field | Type | Description |
|---|---|---|
| transaction_id | Text | Unique transaction ID |
| timestamp | Date | ISO 8601 formatted timestamp |
| account_id | Text | Account identifier |
| amount | Currency | Transaction amount in USD |
| merchant | Text | Merchant name |
| location | Text | Transaction location |
| status | Text | Processing state — set to `unprocessed` on ingestion |
| source | Text | Origin of record — set to `csv_ingestion` |
| created_at | Date | Timestamp when record was written to Airtable |

---

## How to Run

1. Open the n8n workflow: `Financial Fraud Detection - Transaction Ingestion`
2. Make sure the Airtable credential is connected
3. Click **Test Workflow** or **Execute Workflow**
4. Check the Airtable Transactions table — new records will appear with `status: unprocessed`

---

## For Downstream Components

**Member 2 (Anomaly Detection):** Filter the Transactions table for records where `status = "unprocessed"`. After processing, update `status` to `"analyzed"` and write back `risk_score`, `anomaly_flags`, and `ai_explanation`.

---

## Files

| File | Description |
|---|---|
| [`../workflows/transaction-ingestion.json`](../workflows/transaction-ingestion.json) | Exported n8n workflow |
| [`../data/transactions_sample.csv`](../data/transactions_sample.csv) | Sample transaction dataset (35 records) |
| `README.md` | This file |

---

## Sample Data

The sample dataset contains 35 transactions including:
- Normal everyday transactions (Starbucks, Netflix, Amazon)
- Suspicious large wire transfers (Lagos, Cyprus, Nigeria)
- Velocity fraud patterns (same account used in multiple countries within minutes)
- Late night ATM withdrawals
- High-value unknown merchant purchases
