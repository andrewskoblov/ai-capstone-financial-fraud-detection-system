# Case Management & Dashboard

This is Andrew Skoblov's Component 3 for the Financial Fraud Detection System. It is a Streamlit dashboard that helps fraud analysts review high-risk transactions, manage investigation cases, update case statuses, assign cases, and view fraud trends from Airtable data.

## What The Dashboard Shows

- **Overview:** total transactions, analyzed transactions, escalated transactions, open cases, recent high-risk cases, and transaction pipeline counts
- **Alert Queue:** high-risk case list with risk badges, AI explanations, status updates, and assignee updates
- **Case Manager:** all cases table, CSV export, and manual case creation
- **Analytics:** risk score distribution, transaction status breakdown, top flagged merchants, and top flagged locations

## How It Connects

**Reads from Airtable**

- `Transactions` table: transaction details, risk scores, anomaly flags, explanations, and status
- `Cases` table: case IDs, transaction IDs, status, assignees, explanations, and timestamps

**Writes to Airtable**

- Updates case `status`, `assigned_to`, and `resolved_at`
- Creates manual investigation cases from the dashboard

## Setup

1. Open this folder:

   ```bash
   cd case-management-dashboard
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set Airtable credentials on Windows PowerShell:

   ```powershell
   $env:AIRTABLE_TOKEN="your_personal_access_token"
   $env:AIRTABLE_BASE_ID="appOBt37iEsQy2Nbd"
   ```

   On macOS/Linux:

   ```bash
   export AIRTABLE_TOKEN="your_personal_access_token"
   export AIRTABLE_BASE_ID="appOBt37iEsQy2Nbd"
   ```

4. Run the dashboard:

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

## How To Present The Dashboard

Use this as a 2-4 minute demo script.

### 1. Start With The Purpose

Say:

> “My component is the analyst-facing case management dashboard. The previous components ingest transactions and generate fraud risk scores. My dashboard turns those scores into an investigation workflow.”

Show the sidebar and point out the four pages: Overview, Alert Queue, Case Manager, and Analytics.

### 2. Show The Overview Page

Click **Overview** and explain:

- **Total Transactions** shows how much data is in the system.
- **Analyzed** shows transactions already processed by the AI/risk workflow.
- **Escalated** shows transactions that became fraud cases.
- **Open Cases** shows what analysts still need to review.

Say:

> “This gives the fraud team a quick operational summary before they start reviewing individual alerts.”

### 3. Show The Alert Queue

Click **Alert Queue**.

Demo steps:

1. Move the **Min Risk Score** slider to filter for higher-risk cases.
2. Open a high-risk case.
3. Point out the transaction ID, case ID, assigned analyst, created date, and AI explanation.
4. Change the status from `open` to `in_review` or `resolved`.
5. Add or update the assignee.
6. Click **Save Changes**.

Say:

> “This is the main analyst workflow. The highest-risk alerts are prioritized, the AI explanation gives context, and the analyst can update the case directly from the dashboard.”

### 4. Show The Case Manager

Click **Case Manager**.

Demo steps:

1. Show the full case table.
2. Point out the CSV export button.
3. Open **Create Manual Case**.
4. Explain that analysts can manually create a case if they find suspicious activity outside the automated flow.

Say:

> “The dashboard supports both automated cases from the pipeline and manual cases created by analysts.”

### 5. Show Analytics

Click **Analytics**.

Point out:

- Risk score distribution
- Transaction status breakdown
- Top flagged merchants
- Top flagged locations
- High-risk transaction log

Say:

> “This page helps the team move from individual case review to trend analysis. They can see where risky activity is concentrated and which merchants or locations appear most often.”

### 6. Close With Impact

Say:

> “Overall, my dashboard completes the pipeline by turning AI-generated fraud signals into a usable review process for human analysts.”

## Files

```text
case-management-dashboard/
├── dashboard.py       # Streamlit dashboard app
├── requirements.txt   # Python dependencies
└── README.md          # Setup and demo instructions
```

## Known Limitations

- Airtable credentials must be provided locally or through Streamlit secrets.
- The dashboard refreshes from Airtable every 30 seconds through Streamlit caching.
- Authentication and analyst roles are not implemented yet.
- This is a local demo dashboard unless deployed through Streamlit Cloud or another hosting service.
