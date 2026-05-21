# Prompt Log — Ergi Sula

**Project:** Financial Fraud Detection System
**Team:** Ergi Sula, Thomas Kamel, Andrew Skoblov
**My Component:** Transaction Ingestion (Component 1)
**AI Tools Used:** GitHub Copilot (via github.com)

---

## 2026-05-14 — Capstone Audit for Checkpoint 2

**Context:** Working on Week 8 lab. Capstone repo open on GitHub. Used GitHub Copilot Chat to run a structured audit of our project before Checkpoint 2.

**Prompt:**
> I need you to act as a capstone project advisor for a university AI integration course. Interview me about my project's current state and produce a structured gap analysis with a Checkpoint 2 Readiness Assessment.

**Result:** Copilot interviewed me with 10 questions one at a time, then produced a full report. Status came back as NOT READY. It correctly identified that Component 1 (Ingestion) is working but Components 2 and 3 have not been built yet.

**Evaluation:** The report was accurate and specific. It correctly listed all the missing fields Thomas needs to write (risk_score, anomaly_flags, ai_explanation, is_fraud) and all the missing pieces Andrew needs to build (case creation workflow, Streamlit dashboard).

**What I changed:** Nothing — the report matched reality. Saved it as docs/checkpoint2-audit.md and shared with the team.

**What I learned:** Giving the AI detailed context (actual field names, actual status values, actual team member names) produced a much more useful report than vague answers would have. The audit is only as good as the honesty of your answers.
