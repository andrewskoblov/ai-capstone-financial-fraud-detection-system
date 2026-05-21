# Copilot Instructions — Financial Fraud Detection System

## Project Overview
A three-component fraud detection pipeline that ingests transaction CSV data, analyzes it with AI for anomaly detection, and manages investigation cases through a dashboard.

## Architecture
- **Component 1 — Ingestion** (n8n + Airtable): Fetches CSV from GitHub, parses/normalizes 35 transaction records, writes to Airtable Transactions table
- **Component 2 — Anomaly Detection** (n8n + Groq + HuggingFace): Loops unprocessed transactions, runs HF bart-large-mnli zero-shot classification + Groq LLaMA-3.1 analysis in parallel, merges results, writes risk_score/anomaly_flags/ai_explanation back to Airtable
- **Component 3 — Case Management** (n8n + Airtable + Streamlit): Queries high-risk records, creates Cases table entries, updates transaction status, Streamlit dashboard for analyst review

## Airtable Schema

### Transactions Table (Base ID: appOBt37iEsQy2Nbd)
- transaction_id (text)
- timestamp (datetime)
- account_id (text)
- amount (number)
- merchant (text)
- location (text)
- status (text) — values: unprocessed → processed → case_created
- source (text)
- created_at (datetime)
- risk_score (number, 0.0-1.0)
- anomaly_flags (text)
- ai_explanation (text)

### Cases Table
- case_id (text) — format: CASE-TXN-XXX
- transaction_id (text)
- assigned_to (text)
- Status (text) — values: open, investigating, resolved
- risk_score (number)
- source (text)
- created_at (datetime)

## Current State (Post-Checkpoint 2)

### What's Working
- Full end-to-end pipeline passing
- Ingestion: 35 records ingesting correctly with duplicate check
- Anomaly detection: Risk scores accurate (0.1 routine → 1.0 critical fraud)
- Wire transfers to high-risk locations correctly scoring 0.95-1.0
- Case management: High-risk cases auto-created (4 cases from 35 transactions)
- Airtable data flows correctly between all components
- n8n expressions fixed to use $json.fields.* for Airtable Search node output

### Known Issues / In Progress
- anomaly_flags returning text labels ("High Risk") not semantic tags (wire_transfer, offshore)
- ai_explanation reliability ~70% — ~30% returning "Analysis unavailable" due to Groq JSON parse failures
- assigned_to field empty — no auto-assignment logic yet
- Dashboard not fully tested with live enriched data
- Status field naming: "processed" vs "analyzed" — standardize to "processed"

### Critical n8n Gotchas
- Airtable Search node returns data under $json.fields.fieldname, NOT $json.fieldname
- When referencing across branches in loop, use $('NodeName').item.json.fields.fieldname
- Groq LLM JSON body user content must use n8n expression syntax (={{ }}) not nested JSON
- Extract Groq is a Code node (not Manual Mapping) to handle JSON parsing
- Loop node needs "Continue on Error" enabled to prevent single failures halting all iterations

## API Keys Location
- Airtable token: stored as "Final Airtable Capstone" credential in n8n
- Groq API: stored as "Header Auth account 22" in n8n
- HuggingFace API: stored as "Header Auth account 22" in n8n

## File Locations
- Streamlit dashboard: ~/fraud-dashboard/dashboard.py
- Run dashboard: streamlit run ~/fraud-dashboard/dashboard.py
- CSV dataset: hosted on GitHub raw URL (35 transactions, TXN-026 to TXN-060)
