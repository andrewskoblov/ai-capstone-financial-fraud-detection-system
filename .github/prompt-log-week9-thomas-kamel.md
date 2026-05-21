# Prompt Log - Thomas Kamel

**Project:** Automated Financial Fraud Detection System
**Team:** Fraud Detection Team
**My Component:** Integration & Pipeline Management
**AI Tools Used:** GitHub Copilot, Copilot Chat

## How to Use This Log
Tracks significant interactive learning milestones, custom logic refinements, and programmatic debugging sessions across development iterations.

---

## Entry 1: 2026-04-15
**Brief description:** Configuring initial OpenSSL benchmark performance parameters.
**Context:** Working on system speed validations comparing asymmetric and symmetric payload handling speeds inside the local execution environment.
**Prompt:**
> "Write a script comparing the relative encryption processing speeds between AES-256-GCM and RSA-2048 using local system OpenSSL benchmarking hooks. Format the comparison output as an explicit markdown table."
**Result:** Generated a shell script using `openssl speed aes-256-gcm rsa2048` and bundled execution instructions alongside a basic output formatting block.
**Evaluation:** The script executed correctly but lacked dynamic parsing, dumping standard system terminal logs rather than mapping data cleanly to a custom summary list.
**What I changed:** Modified the script output parameters to capture raw byte records and use basic `awk` formatting to display clean processing metrics.
**What I learned:** System benchmarking tools require strict output stream filters to translate verbose console arrays into readable project readmes.

---

## Entry 2: 2026-05-02
**Brief description:** Structuring recursive path tracking logic rules.
**Context:** Creating modular path assessment scripts over directed and undirected network graph components.
**Prompt:**
> "Develop a Prolog program using recursive rule structures to identify valid path routes between defined coordinates over directed graph nodes, preventing infinite looping states."
**Result:** Copilot generated a standard recursive path lookup rule sequence incorporating a classic accumulator tracking list (`Visited`).
**Evaluation:** Highly functional code logic that handled acyclic paths beautifully but failed when managing heavily interconnected circular matrix structures.
**What I changed:** Updated checking constraints to explicitly check historical trace records before matching deep step rules.
**What I learned:** Complex state tracking inside rule languages requires strict historical accumulator checks to avoid infinite evaluation loops.

---

## Entry 3: 2026-05-10
**Brief description:** Initial generation of Capstone system documentation assets.
**Context:** Building out basic system architecture contexts inside the global configuration workspace files.
**Prompt:**
> "Review my current Airtable database table fields and draft a comprehensive `.github/copilot-instructions.md` context template framing our Ingestion and AI Core configurations."
**Result:** Created a clean markdown template containing clear formatting tiers for project tech stack blocks and column variables.
**Evaluation:** The generated database framework reflected our structural design flawlessly, though it left the current operational milestone values blank.
**What I changed:** Added precise operational context descriptions outlining our upcoming Checkpoint 2 target goals directly into the file.
**What I learned:** Standard documentation models build clean functional shells, but precise project context must be added by hand to make it accurate.

---

## Entry 4: 2026-05-19
**Brief description:** Constructing the Checkpoint 2 automated group audit report.
**Context:** Running the required 10-question course engineering audit via the live workspace context window.
**Prompt:**
> "Act as our capstone project advisor for this AI integration course. I need you to interview me with the standard 10-question readiness script one question at a time to evaluate our data pipeline state."
**Result:** Initiated a systematic 10-step chat interview assessing schema details, operational handoffs, and active data validation metrics.
**Evaluation:** Generated a comprehensive, highly accurate gap assessment identifying our data pipeline strengths alongside structural mapping risks.
**What I changed:** Adjusted tracking fields to clearly differentiate successful multi-node AI loops from downstream formatting bugs.
**What I learned:** Stale project context yields generic advice; running live interviews with actual data surfaces true workflow bottlenecks.

---

## Entry 5: 2026-05-20
**Brief description:** Troubleshooting a corrupted database field expression.
**Context:** Resolving an integration bug where a literal text block (`{{ $json.fields.risk_score ... }}`) printed to Airtable columns instead of the data value.
**Prompt:**
> "My n8n Specialist node successfully triggers when AI Core marks rows as processed, but it is writing the literal text code '{{ $json.fields.risk_score }}' into the Airtable Cases column. How do I fix this mapping reference?"
**Result:** Copilot explained that because the field was nested inside an ongoing loop collection, it needed a direct incoming data map look-up format: `{{ $json.risk_score }}` or a proper sub-item element block reference instead of calling database metadata.
**Evaluation:** The proposed syntax change completely resolved the bug, causing the string value to evaluate correctly as an explicit name/score token upon execution.
**What I changed:** Replaced the deep nested database look-up format inside our parameter definitions with a direct context data reference token.
**What I learned:** Downstream automation engines lose parental variable scopes inside loops. Variables must reference the direct incoming step parameters to evaluate properly.
