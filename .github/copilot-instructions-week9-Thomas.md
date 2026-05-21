# Capstone Project Context

## Project
**Name:** Automated Financial Fraud Detection System
**Team:** Fraud Detection Team
**What it does:** Automates the ingestion of financial ledger entries, enriches records through a split-conditional AI loop utilizing Hugging Face and Groq, and escalates high-risk anomalies directly to a dedicated case management database interface for fraud investigators.
**Project type:** Financial Fraud Detection System

## Architecture
**Ingestion:** Manual trigger kicks off an automated worker that fetches transaction data from a remote CSV endpoint, parses the schema, and writes clean transaction logs directly to Airtable with an initial status value of `unprocessed`.
**AI Core:** An automation workflow queries rows flagged as `unprocessed`, splits them conditionally based on high-dollar thresholds, pipes records to Hugging Face and Groq LLM nodes for anomaly checking, and records risk scores and explanations back to Airtable under a `processed` status flag.
**Specialist:** A dedicated background flow monitors the database, catches entries carrying high-risk scores (`1.0`), creates corresponding entries inside a `Cases` tracking table with unique Case tracking IDs, and shifts status flags.
**Integration:** Shared Airtable relational database interfaces map transactions back to active investigator case logs, which fuel live monitoring dashboards.

## Tech Stack
* n8n Cloud (workflow automation)
* Flowise Cloud (LLM chains / analysis pipelines)
* Groq API (LLM inference via llama-3.3-70b-versatile)
* Hugging Face Inference API (anomaly flag scoring)
* Airtable (relational database backend)
* GitHub (repository and documentation management)

## Airtable Schema

### Transactions
| Field | Type | Written By | Status Values |
|---|---|---|---|
| transaction_id | Single line text | Ingestion | Unique record index |
| amount | Currency | Ingestion | Numerical value |
| merchant | Single line text | Ingestion | Vendor identity |
| status | Single select | All Components | `unprocessed`, `processed` |
| risk_score | Number | AI Core | Scale values (0.0 - 1.0) |
| anomaly_flags | Single line text | AI Core | Text tags (e.g., Low Risk, High Risk) |
| ai_explanation | Long text | AI Core | Generated structural text analysis |

### Cases
| Field | Type | Written By | Status Values |
|---|---|---|---|
| case_id | Single line text | Specialist | Unique case index |
| transaction_id | Link to Transactions | Specialist | Relational database mapping |
| assigned_to | Single line text | Specialist | Intended investigator tier |
| status | Single select | Specialist | `open`, `under_review`, `resolved` |

## Conventions
* Field names: snake_case
* Status values: lowercase
* Date fields end in `_at`
* Boolean fields use `is_` prefix

## Current State
**What's working:** * Automated transactional ingestion engine from remote endpoints.
* Bifurcated high/low dollar automation logic branches.
* Multi-model API classification integration loop (Hugging Face + Groq).
* Automatic case profile separation for top-tier anomalous threats.

**What's in progress:**
* Resolving data syntax conversion errors inside downstream data-saving steps.
* Configuring operational summary dashboards inside the integration tier.

**Known issues:**
* The Specialist case creation workflow experiences an expression evaluation failure, dropping raw n8n variable strings directly into the `assigned_to` field columns.

**Next milestone:** Checkpoint 2 (Week 9) verification pass following data mapping syntax corrections.

## Repository Structure
* `.github/copilot-instructions.md`
* `docs/checkpoint2-results.md`
* `docs/checkpoint2-audit.md`
* `prompt-log-thomas-kamel.md`
