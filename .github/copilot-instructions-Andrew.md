# Capstone Project Context

## Project
- **Name:** Financial Fraud Detection System
- **Team:** Ergi Sula (Transaction Ingestion), Thomas Kamel (Anomaly Detection & AI Analysis), Andrew Skoblov (Case Management & Dashboard)
- **What it does:** Ingests simulated financial transaction records, analyzes them for anomalous patterns using AI, generates plain-English fraud explanations, and surfaces high-risk cases in a prioritized Streamlit dashboard for fraud analysts to review and act on.
- **Project type:** Financial Fraud Detection System

## Architecture
- **Ingestion:** n8n workflow receives transaction CSV files or webhook JSON records, parses and normalizes fields (transaction_id, amount, timestamp, account_id, merchant, location), writes structured records to Airtable Transactions table. Owner: Ergi Sula.
- **AI Core:** n8n workflow polls Airtable for new transactions (status: "pending"), runs anomaly detection using rule-based scoring + Groq LLaMA-3 for plain-English explanation, writes risk_score, anomaly_flags, and ai_explanation back to Airtable, updates status to "analyzed". Owner: Thomas Kamel.
- **Specialist (Case Management):** n8n workflow monitors Airtable for high-risk transactions (risk_score >= 0.7), creates investigation Case records, updates transaction status to "escalated". Streamlit dashboard displays alert queue with filtering by risk level and case status, allows analysts to mark cases resolved. Owner: Andrew Skoblov.
- **Integration:** Shared Airtable base with status field driving handoffs between components. Dashboard reads from both Transactions and Cases tables.

## Tech Stack
- n8n Cloud (workflow automation)
- Flowise Cloud (LLM chains — transaction risk classifier, pattern analyzer, investigation recommender)
- Groq API (LLM inference — llama-3.3-70b-versatile)
- Hugging Face Inference API (distilbert for transaction description classification)
- Airtable (shared database — 2 tables: Transactions, Cases)
- Streamlit (fraud analyst dashboard)
- GitHub (repo, documentation, portfolio)

## Airtable Schema

### Transactions
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| transaction_id | text | Ingestion | — |
| timestamp | datetime | Ingestion | — |
| account_id | text | Ingestion | — |
| amount | number | Ingestion | — |
| merchant | text | Ingestion | — |
| location | text | Ingestion | — |
| is_fraud | checkbox | Ingestion | true/false |
| status | select | Ingestion/AI Core | pending, analyzed, escalated |
| risk_score | number | AI Core | 0.0–1.0 |
| anomaly_flags | text | AI Core | — |
| ai_explanation | long text | AI Core | — |
| created_at | datetime | Ingestion | — |

### Cases
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| case_id | text | Case Management | — |
| transaction_id | text | Case Management | — |
| risk_score | number | Case Management | — |
| ai_explanation | long text | Case Management | — |
| status | select | Case Management/Dashboard | open, in_review, resolved |
| assigned_to | text | Dashboard | — |
| created_at | datetime | Case Management | — |
| resolved_at | datetime | Dashboard | — |

## Conventions
- Field names: snake_case
- Status values: lowercase
- Date fields end in _at
- Boolean fields use is_ prefix
- Risk scores are floats between 0.0 and 1.0
- High risk threshold: risk_score >= 0.7

## Current State
- **What's working:** Project proposal, architecture diagram, GitHub repo structure, individual component folders
- **What's in progress:** Shared Airtable base (not yet created — needs team coordination), n8n ingestion workflow, Streamlit dashboard skeleton
- **Known issues:** No shared Airtable base exists yet — all 3 components are blocked on this for end-to-end testing
- **Next milestone:** Checkpoint 2 (Week 9) — one complete transaction record flows through all 3 components end-to-end without manual intervention

## Repository Structure
```
ai-capstone-financial-fraud-detection-system/
├── Transaction Ingestion/        # Ergi — n8n workflow exports, sample CSVs
├── Anomaly Detection & AI Analysis/  # Thomas — n8n workflow exports, HF/Groq configs
├── Case Management & Dashboard/  # Andrew — Streamlit app, n8n workflow exports
├── docs/                         # Shared documentation, audit reports
├── .github/
│   └── copilot-instructions.md  # This file
├── architecture.png
└── README.md
```
