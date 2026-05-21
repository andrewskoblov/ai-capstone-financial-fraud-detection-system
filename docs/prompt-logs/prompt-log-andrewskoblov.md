# Prompt Log -- Andrew Skoblov
 
**Project:** Financial Fraud Detection System  
**Team:** Ergi Sula (Ingestion), Thomas Kamel (AI Analysis), Andrew Skoblov (Case Management & Dashboard)  
**My Component:** Case Management & Dashboard (Specialist)  
**AI Tools Used:** Claude (claude.ai) -- used as alternative to GitHub Copilot per lab instructions
 
---
 
## How to Use This Log
 
Add an entry for each significant AI interaction:
- Claude/Copilot Chat conversations where you asked it to generate, explain, or debug something
- Moments where the AI was wrong and you had to fix it (these are the most valuable entries)
- Cases where you refined a prompt to get a better result
Don't log: every autocomplete of a bracket or variable name.
 
---
 
## 2026-05-11 -- Capstone Checkpoint 2 Audit
 
**Context:** Week 8 lab, Part 2.3. Capstone repo open, copilot-instructions.md already committed to GitHub. Used claude.ai as alternative to GitHub Copilot per lab instructions.
 
**Prompt:**
> I need you to act as a capstone project advisor for a university AI integration course. Interview me about my project's current state and produce a structured gap analysis. [Full 10-question audit prompt from lab instructions]
 
**Result:** Claude interviewed me with 10 questions one at a time about the Financial Fraud Detection System. Produced a full Checkpoint 2 Readiness Assessment with status AT RISK, critical gaps, schema issues, recommended fix order, and test data gaps.
 
**Evaluation:** The audit was accurate and honest. The critical gaps it identified (no n8n workflows built yet, no end-to-end test run, Streamlit not connected to Airtable) are all real. The recommended fix order was logical -- start with my own component first so I'm not blocked by teammates. The schema issues section correctly identified that the Cases table uses "Name" and "Notes" as column headers instead of case_id and transaction_id.
 
**What I changed:** Deleted the header row in the Cases table that had been imported as a data record. Otherwise accepted the audit report as-is.
 
**What I learned:** Giving specific, honest answers produces a much more useful audit than vague responses. When I gave detailed answers about actual field names and status values, the gap analysis was concrete and actionable. Vague answers would have produced generic advice.
 
---
 
## 2026-05-11 -- Case Management & Dashboard README
 
**Context:** Week 8 lab, Part 2.4. Generating a real deliverable for the capstone repo using AI assistance.
 
**Prompt:**
> Using the project context from copilot-instructions.md, write a complete README for my Case Management & Dashboard component. Include: what it does, how it connects to other components, setup instructions, how to test it, and known limitations.
 
**Result:** Claude generated a full README with all required sections -- component description, architecture diagram showing data flow, setup instructions for n8n and Streamlit, step-by-step test procedure, and known limitations including the lack of real-time refresh and no public deployment URL.
 
**Evaluation:** The README was accurate and specific to the project. It correctly referenced the Airtable base ID, the risk_score >= 0.7 threshold, and the status values (open, in_review, resolved). The known limitations section was honest and matched the actual state of the component. One thing it included (dashboard.py filename) was an assumption -- the file doesn't exist yet.
 
**What I changed:** Committed it to GitHub at Case Management & Dashboard/README.md, replacing the placeholder README that was there before. Did not change the content since it was accurate.
 
**What I learned:** The AI-generated README was useful because the copilot-instructions.md file gave it real context -- actual field names, actual tools, actual thresholds. Without that context file, the README would have been generic. The instructions file is what made the output project-specific instead of a template.
