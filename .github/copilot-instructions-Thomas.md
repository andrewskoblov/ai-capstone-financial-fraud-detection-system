# Capstone Project Context

## Project
* **Name:** Financial Fraud Detection System
* **Team:** Thomas Kamel (AI Core & Process Integration), Ergi (Ingestion Component), Andrew (Specialist Component)
* **What it does:** Automates the ingestion, evaluation, and mitigation of high-risk financial anomalies. Raw system logs are parsed via webhooks, passed to AI agents for risk classification, and formatted into actionable defensive playbooks.
* **Project type:** Threat Intelligence & Financial Fraud Mitigation Hub

## Architecture
* **Ingestion:** n8n webhook receives raw transaction/system alerts, parses out core indicator fields, and logs a clean tracking payload into the main database.
* **AI Core:** Core execution runs through multi-layered Flowise inference pipelines via n8n HTTP requests. Uses llama-3.3-70b-versatile to output structured alert classification (Chain 1) and indicator threat analysis (Chain 2).
* **Specialist:** n8n consumes the threat assessments to auto-generate response playbooks (Chain 3) and sends high-priority security notifications.
* **Integration:** Shared data ecosystem driven by specific state-change handoffs, utilizing unified status tracking views to cleanly sync the individual components.

## Tech Stack
* n8n Cloud (workflow automation)
* Flowise Cloud (LLM orchestration & prompt chain execution)
* Groq API (Inference Engine: llama-3.3-70b-versatile)
* Airtable (Shared tracking relational data infrastructure)
* GitHub (Version control and technical repository tracking)

## Conventions
* Field names: snake_case
* Status values: lowercase
* Date fields end in _at
* Boolean fields use is_ prefix

## Current State
* **What's working:** Flowise core classification, analyzer, and responder agent logic built and successfully validated. n8n multi-chain loop fully wired and working over mock alert webhooks.
* **What's in progress:** Final hardening of Airtable automated status triggers and real-time dashboard data mapping.
* **Known issues:** Database state tracking mismatch errors resolved by creating dedicated workflow canvases.
* **Next milestone:** Checkpoint 2 (Week 9) one complete record flows through all 4 components end-to-end smoothly.
