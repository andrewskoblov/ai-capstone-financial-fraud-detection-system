# Capstone Project Context

## Project
- **Name:** Financial Fraud Detection System
- **Team:** Ergi Sula (Component 1 - Transaction Ingestion), Thomas Kamel (Component 2 - Anomaly Detection & AI Analysis), Andrew Skoblov (Component 3 - Case Management & Dashboard)
- **What it does:** Ingests simulated financial transaction data via n8n, runs AI-powered anomaly detection using Groq and Hugging Face, creates investigation cases for high-risk transactions, and displays results on a Streamlit dashboard for fraud analysts to review.
- **Project type:** Financial Fraud Detection System

## Architecture
- **Ingestion (Ergi):** n8n workflow fetches transactions_sample.csv from GitHub raw URL, parses and normalizes 35 records, writes to Airtable Transactions table with status "unprocessed" and source "csv_ingestion"
- **AI Core (Thomas):** n8n workflow reads records where status = "unprocessed" from Airtable, runs Groq LLaMA-3 and Hugging Face distilbert for anomaly scoring, writes back risk_score, anomaly_flags, ai_explanation, updates status to "analyzed"
- **Specialist (Andrew):** n8n workflow reads high-risk analyzed records, creates Cases in Airtable, Streamlit dashboard shows fraud alert queue with filters for risk level and case status
- **Integration:** All components share one Airtable base — status field drives handoffs between components

## Tech Stack
- n8n Cloud (workflow automation)
- Flowise Cloud (LLM chains)
- Groq API (llama-3.3-70b-versatile)
- Hugging Face Inference API (distilbert for classification)
- Airtable (shared database — 2 tables)
- Streamlit (dashboard)
- GitHub (repo and CSV hosting)

## Airtable Schema

### Transactions (primary table — owned by Ergi, enriched by Thomas)
| Field | Type | Written By | Notes |
|-------|------|-----------|-------|
| transaction_id | Single line text | Ingestion | Primary field |
| timestamp | Date with time | Ingestion | ISO format |
| account_id | Single line text | Ingestion | e.g. ACCT-1234-5678 |
| amount | Currency USD | Ingestion | |
| merchant | Single line text | Ingestion | |
| location | Single line text | Ingestion | |
| status | Single line text | Both | "unprocessed" → "analyzed" |
| source | Single line text | Ingestion | Always "csv_ingestion" |
| created_at | Date with time | Ingestion | |
| risk_score | Number | AI Core | Written by Thomas |
| anomaly_flags | Single line text | AI Core | Written by Thomas |
| ai_explanation | Long text | AI Core | Written by Thomas |
| is_fraud | Checkbox | AI Core | Written by Thomas |

### Cases (owned by Andrew — Case Management)
| Field | Type | Written By | Notes |
|-------|------|-----------|-------|
| case_id | Single line text | Specialist | Primary field |
| transaction_id | Single line text | Specialist | Links to Transactions |
| status | Single line text | Specialist | |
| risk_score | Number | Specialist | |
| assigned_to | Single line text | Specialist | |
| created_at | Date with time | Specialist | |
| source | Single line text | Specialist | |

## Conventions
- Field names: snake_case
- Status values: lowercase (unprocessed, analyzed)
- Date fields end in _at
- Boolean fields use is_ prefix

## Current State
- **What's working:** Ergi's ingestion pipeline fully working — n8n fetches CSV from GitHub, normalizes 35 records, writes to Airtable with status "unprocessed"
- **What's in progress:** Thomas anomaly detection (Component 2), Andrew case management and dashboard (Component 3)
- **Known issues:** Components 2 and 3 not yet built, end-to-end handoff not yet tested
- **Next milestone:** Checkpoint 2 (Week 9) — one record flowing end-to-end through all 3 components automatically

## Repository Structure
- Transaction Ingestion/ (Ergi's component)
- Anomaly Detection & AI Analysis/ (Thomas's component)
- Case Management & Dashboard/ (Andrew's component)
- docs/
- .github/copilot-instructions.md
