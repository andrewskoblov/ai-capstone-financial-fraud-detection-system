# Prompt Log — Financial Fraud Detection System

---

## Entry 1
**Date:** 2026-05-15
**Context:** Component 2 anomaly detection not producing correct risk scores — all transactions returning 0.4-0.6 flat scores regardless of fraud signals.

**Prompt used:**
"The HF Zero-Shot node is sending candidate labels 'fraudulent activity', 'routine transaction', 'requires review' but the Calculate Risk Score node checks for 'fraudulent', 'suspicious', 'legitimate'. How do I fix this label mismatch?"

**What Copilot suggested:**
Update HF HTTP request body to use matching candidate labels: ["fraudulent", "suspicious", "legitimate"]. Update Calculate Risk Score conditionals to match exactly.

**Evaluation:** Correct diagnosis. The label string mismatch was the root cause. After fixing, scores began differentiating properly.

**Reflection:** Always verify that the labels sent to the model match exactly what your downstream code expects. String comparison bugs are silent — no error, just wrong output.

---

## Entry 2
**Date:** 2026-05-15
**Context:** Amount field being wiped to $0.00 after Component 2 runs.

**Prompt used:**
"After running anomaly detection, all transaction amounts show as $0.00 in Airtable. The Update Airtable node only maps 4 fields: risk_score, anomaly_flags, ai_explanation, status. Why is amount being overwritten?"

**What Copilot suggested:**
Check previous runs — if amount was ever mapped with a broken expression ($json.amount returning undefined/0), it would have written 0 to Airtable. The current mapping isn't the issue; it's a legacy run artifact. Verify Update node has no amount field.

**Evaluation:** Partially correct. The issue was from a previous run where amount was incorrectly mapped. Confirmed Update node no longer maps amount — won't recur.

**Reflection:** Always reset test data to clean state before debugging. Stale data from broken previous runs can look like current bugs.

---

## Entry 3
**Date:** 2026-05-15
**Context:** Groq LLM node returning error instead of analysis.

**Prompt used:**
"Groq LLM is returning an error field instead of choices[0].message.content. The JSON body has nested expressions like {{ $json.merchant }} but Airtable Search returns data under $json.fields.merchant. How do I fix the body?"

**What Copilot suggested:**
Change all $json.merchant to $json.fields.merchant throughout the Groq body. Use string concatenation in a single n8n expression for the user content field to avoid nested JSON quote conflicts.

**Evaluation:** Correct. After switching to $json.fields.* references and using expression concatenation, Groq began returning valid responses.

**Reflection:** n8n's Airtable Search node wraps all field values under a fields object. This is different from other nodes and causes silent failures if you forget it. Always check the Schema tab in the INPUT panel.

---

## Entry 4
**Date:** 2026-05-18
**Context:** Component 3 not running — Get High Risk Transactions returning 0 records.

**Prompt used:**
"Component 3 filter is AND({status} = 'analyzed', {risk_score} > 0.7) but all my transactions show status = 'processed'. Zero records returned. How do I fix?"

**What Copilot suggested:**
Update filter formula to match the actual status value written by Component 2: AND({status} = "processed", {risk_score} > 0.7).

**Evaluation:** Correct and immediate fix. Status naming mismatch was the entire problem.

**Reflection:** Status field values are a contract between components. They need to be explicitly agreed on and documented. A one-word difference ("analyzed" vs "processed") completely breaks the pipeline with no error message.

---

## Entry 5
**Date:** 2026-05-18
**Context:** Create Case node creating CASE-undefined because transaction_id was undefined.

**Prompt used:**
"Create Case shows case_id: CASE-undefined and transaction_id: undefined in the output. The expression is {{ $json.transaction_id }} but I can see in the INPUT panel that data is under $json.fields.transaction_id. What do I change?"

**What Copilot suggested:**
Change all $json.transaction_id to $json.fields.transaction_id. Also update risk_score reference to $json.fields.risk_score. For Update Transaction Status node which runs after Create Case, reference back to the original source: $('Get High Risk Transactions').item.json.fields.transaction_id.

**Evaluation:** Correct. After fixing all three field references, cases created correctly with proper IDs and risk scores.

**Reflection:** When data passes through multiple nodes in a loop, the "current item" context changes at each node. After Create Case runs, $json refers to the Create Case output, not the original Airtable record. Always explicitly reference the source node by name when you need data from earlier in the chain.
