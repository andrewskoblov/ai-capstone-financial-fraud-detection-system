# Case Management & Dashboard

**Owner:** Andrew Skoblov  
**Component:** Component 3  
**Project:** Financial Fraud Detection System

## What It Does

This component provides a Streamlit dashboard for fraud analysts to review high-risk transactions, manage investigation cases, update case status, assign cases, and inspect risk trends from the shared Airtable base.

## How It Connects

**Reads from Airtable**
- `Transactions` table: transaction details, risk scores, anomaly flags, explanations, and status
- `Cases` table: case IDs, transaction IDs, status, assignees, explanations, and timestamps

**Writes to Airtable**
- Updates case `status`, `assigned_to`, and `resolved_at`
- Creates manual investigation cases from the dashboard

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Airtable credentials:
   ```bash
   set AIRTABLE_TOKEN=your_personal_access_token
   set AIRTABLE_BASE_ID=appOBt37iEsQy2Nbd
   ```

   On macOS/Linux, use `export` instead of `set`.

3. Run the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

## Streamlit Secrets Option

For Streamlit Cloud or local `.streamlit/secrets.toml`, use:

```toml
AIRTABLE_TOKEN = "your_personal_access_token"
AIRTABLE_BASE_ID = "appOBt37iEsQy2Nbd"
```

Optional table overrides:

```toml
AIRTABLE_CASES_TABLE = "Cases"
AIRTABLE_TRANSACTIONS_TABLE = "Transactions"
```

## Dashboard Pages

- **Overview:** summary metrics, recent high-risk cases, transaction pipeline
- **Alert Queue:** filtered investigation queue with status and assignee updates
- **Case Manager:** all cases, CSV export, and manual case creation
- **Analytics:** risk distribution, transaction status breakdown, flagged merchants, flagged locations

## Files

```text
case-management-dashboard/
├── dashboard.py
├── requirements.txt
└── README.md
```

## Known Limitations

- Airtable credentials must be provided locally or through Streamlit secrets.
- The dashboard refreshes from Airtable every 30 seconds through Streamlit caching.
- Authentication and analyst roles are not implemented yet.
