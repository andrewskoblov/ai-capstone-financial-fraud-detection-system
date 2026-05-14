## Checkpoint 2 Readiness Assessment

### Status: **NOT READY**

Checkpoint 2 requires one complete record to flow through all 3 components end-to-end without manual intervention. Currently, only Component 1 (Ingestion) is operational. Components 2 (Anomaly Detection) and 3 (Case Management & Dashboard) do not exist.

---

### What's Working

✅ **Component 1 — Ingestion (Ergi)**
- n8n workflow successfully fetches CSV from GitHub
- Data normalization pipeline operational
- 35 test records written to Airtable Transactions table
- Status field correctly set to `"unprocessed"` for all records
- No data quality issues reported

---

### Critical Gaps (must fix before Checkpoint 2)

🔴 **Component 2 — Anomaly Detection (Thomas) — Does Not Exist**
- No workflow built to read `status = "unprocessed"` records from Airtable
- No integration with Groq/HuggingFace for AI anomaly scoring
- No mechanism to populate `risk_score`, `anomaly_flags`, `ai_explanation`, `is_fraud` fields
- No status update logic to set `status = "analyzed"` after processing

🔴 **Component 3 — Case Management & Dashboard (Andrew) — Does Not Exist**
- No workflow to read `status = "analyzed"` records from Transactions table
- No case creation logic in Cases table
- No Streamlit dashboard built
- No mechanism to link Cases back to Transactions via `transaction_id`

🔴 **End-to-End Handoff — Not Tested**
- No data flow validation between any two components
- Risk of field name mismatches between Components 2 and 3
- No confirmation that Flowise integration works in context

---

### Schema Issues Found

⚠️ **Field Name Contract Not Yet Defined**
- **Risk:** Thomas will populate fields in Transactions table (e.g., `risk_score`, `anomaly_flags`), but Andrew may not know the exact field names or data types to expect
- **Impact:** Component 2 → Component 3 handoff may fail due to missing/misnamed fields
- **Solution:** Team must agree on exact field names, types, and expected values before Thomas builds Component 2

⚠️ **Cases Table Schema Incomplete**
- The Cases table exists with basic fields (`case_id`, `transaction_id`, `status`, `risk_score`, `assigned_to`, `created_at`, `source`)
- **Risk:** It's unclear whether Andrew will auto-populate all fields or if some require manual input
- **Impact:** Violates Checkpoint 2 requirement of "no manual intervention"

---

### Recommended Fix Order

1. **This week — Define Component 2 ↔ Component 3 Field Contract**
   - Thomas and Andrew must meet and agree on:
     - Exact field names Thomas will write to Transactions table
     - Data types and expected value ranges for each field
     - Exact fields Andrew will read from Transactions to create Cases
     - How `case_id` will be generated (auto-increment, UUID, etc.)
   - Document in a shared schema doc or Airtable view

2. **Days 1–2 — Build Component 2 (Anomaly Detection) — Thomas**
   - Create n8n workflow that:
     - Polls Airtable for `status = "unprocessed"` records
     - Calls Groq or HuggingFace API with transaction data
     - Populates `risk_score`, `anomaly_flags`, `ai_explanation`, `is_fraud` in Transactions table
     - Updates `status = "analyzed"` when done
   - Test with 2–3 records first, then all 35

3. **Days 2–3 — Build Component 3 (Case Management) — Andrew**
   - Create workflow that:
     - Polls Airtable for `status = "analyzed"` records in Transactions table
     - Reads risk_score and fraud flags
     - Auto-creates records in Cases table with `status = "new"` (or similar)
     - Sets `transaction_id` linkage
   - Build basic Streamlit dashboard that displays Cases table

4. **Day 3 — Integration Testing**
   - Pick 1 test record from Transactions table with `status = "unprocessed"`
   - Manually trigger Component 2 workflow, verify `status` → `"analyzed"` and fields populated
   - Manually trigger Component 3 workflow, verify case created in Cases table
   - Verify Streamlit dashboard displays the case
   - Repeat with 2–3 more records

5. **Day 4 — End-to-End Automation**
   - Set up Airtable automation or n8n trigger to auto-invoke Component 2 when new records arrive
   - Set up Component 2 → Component 3 trigger (e.g., Component 2 webhook calls Component 3 on completion)
   - Test with fresh CSV record from GitHub through full pipeline
   - Demonstrate to instructors

---

### Test Data Gaps

- ✅ You have 35 records (good volume)
- ⚠️ **Missing edge cases:** No malformed data, no extremely high/low amounts, no null fields, no timezone edge cases
- ⚠️ **Missing failure scenarios:** What happens if Groq API fails? What if a field is missing? How does the system recover?
- **Recommendation:** Before Checkpoint 2, add 3–5 edge case records (missing merchant, zero amount, future timestamp, etc.) to test error handling

---

### Summary for Checkpoint 2

**To pass Checkpoint 2, you must:**

1. ✅ Keep Component 1 (Ingestion) running as-is
2. 🔴 **Build Component 2 (Anomaly Detection) — Thomas** in next 2–3 days
3. 🔴 **Build Component 3 (Case Management & Dashboard) — Andrew** in next 2–3 days
4. 🔴 **Define the field contract between Components 2 & 3** BEFORE Thomas codes
5. ✅ **Test one record end-to-end** (unprocessed → analyzed → case created → displayed in dashboard)

**Current blocker:** Timeline. Components 2 and 3 must be built and integrated in ~7 days. Recommend:
- Thomas and Andrew meet today to align on schema/field names
- Thomas builds in parallel (doesn't need to wait for Andrew)
- Andrew can build in parallel (can use mock data from Transactions table)
- Integration test on Day 3–4 of build cycle

**Risk level: HIGH** — but achievable if both teams execute immediately and avoid scope creep.
