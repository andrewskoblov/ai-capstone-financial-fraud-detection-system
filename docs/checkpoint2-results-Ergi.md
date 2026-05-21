Checkpoint 2 Results
Date: 2026-05-19
Team: Financial Fraud Detection System
Members: Ergi Sula (Ingestion), Thomas Kamel (Anomaly Detection), Andrew Skoblov (Case Management & Dashboard)
Test record: TXN-028 — Wire Transfer of $78,500 to Lagos, Nigeria on 2024-01-19 from account ACCT-3456-7890

End-to-End Status: PASSED

Component-by-Component Results
Component 1 — Ingestion (Owner: Ergi Sula)

Status: Working
What happened: Manual trigger fetched the CSV from GitHub raw URL, Parse & Normalize code node processed all 35 rows, and records were written to the Airtable Transactions table with correct field mapping (transaction_id, timestamp, account_id, amount, merchant, location, status=unprocessed). Duplicate check prevents re-ingestion on repeat runs.
Screenshot: screenshot-component1-airtable.png

Component 2 — Anomaly Detection & AI Analysis (Owner: Thomas Kamel)

Status: Working
What happened: Workflow fetched all unprocessed records from Airtable, looped through each transaction, sent to both HF Zero-Shot classifier (facebook/bart-large-mnli) and Groq LLaMA-3.1 in parallel. Results merged and risk scores calculated. Airtable updated with risk_score, anomaly_flags, and ai_explanation. High-risk transactions (Wire Transfers to Lagos, Cyprus, Nigeria) correctly scored at 1.0 and flagged. Status updated to "processed".
Known issue: ai_explanation field populating with text but anomaly_flags outputting label text ("High Risk") rather than semantic tags (wire_transfer, offshore, geo_mismatch). Groq prompt refinement needed.
Screenshot: screenshot-component2-airtable.png

Component 3 — Case Management (Owner: Andrew Skoblov)

Status: Working
What happened: Workflow queried Airtable for transactions with status="processed" and risk_score > 0.7. Found 4 high-risk transactions (TXN-028, TXN-050, TXN-057, TXN-032). Created corresponding case records in the Cases table with case_id, transaction_id, risk_score, status=open, source=anomaly_detection. Transaction status updated to case_created.
Screenshot: screenshot-component3-cases.png

Integration Dashboard (Owner: Andrew Skoblov)

Status: Built, pending live data verification
What happened: Streamlit dashboard at ~/fraud-dashboard/dashboard.py connects to Airtable API. Shows KPIs, alert feed with risk filter, trend analytics, and case management with status updates.
Screenshot: screenshot-dashboard.png


Gaps Found

Anomaly flags not semantic — Groq returning "High Risk"/"Low Risk" text labels instead of structured tags like wire_transfer, offshore, geo_mismatch. Groq prompt needs updating to return JSON array of tags. Owner: Thomas Kamel.
ai_explanation inconsistent — Some transactions returning "Analysis unavailable" due to JSON parse failures on Groq response. Extract Groq code node needs more robust fallback parsing. Owner: Thomas Kamel.
Cases table missing assigned_to — assigned_to field empty for all cases. No auto-assignment logic implemented. Owner: Andrew Skoblov.
Dashboard not fully tested with live data — Dashboard built but not verified end-to-end with real enriched records and cases. Owner: Andrew Skoblov.
Component 2 status field mismatch — Component 3 filter expected "analyzed" but Component 2 was writing "processed". Fixed by updating filter formula, but status naming needs standardization across components. All owners.
Loop halting on error — Component 3 loop was stopping mid-run when Update Transaction Status failed. Fixed by enabling Continue on Error and correcting field reference paths ($json.fields.* vs $json.*). Owner: Thomas Kamel / Andrew Skoblov.


Fix Plan

Fix Groq prompt to return semantic anomaly flags (Thomas Kamel — 1 hour) — Update system prompt to output JSON array with specific flag names. Update Extract Groq parser to handle array. Re-run anomaly detection on all 35 records.
Test Streamlit dashboard end-to-end (Andrew Skoblov — 1 hour) — Launch dashboard, verify KPIs populate from live Airtable data, test risk filter, test case status update flow.
Standardize status field values across all components (All — 30 min) — Agree on status progression: unprocessed → analyzed → case_created → resolved. Update all filters and node configs.
Add assigned_to logic to Case Management (Andrew Skoblov — 30 min) — Add static "Fraud Analysis Team" or risk-based assignment (risk >= 0.9 → Senior Analyst).
Improve ai_explanation reliability (Thomas Kamel — 1 hour) — Add retry logic or fallback prompt if Groq JSON parse fails. Log raw Groq responses for debugging.
