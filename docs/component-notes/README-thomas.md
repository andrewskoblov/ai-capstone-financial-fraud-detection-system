# AI Core Component - Financial Fraud Detection System

## Overview
The AI Core component acts as the central analytical intelligence engine for our fraud pipeline. It ingests unstructured text alert notifications caught by our webhooks and orchestrates them through three distinct processing layers using **Flowise** and **Groq (llama-3.3-70b-versatile)** to automatically tag, parse, and generate incident resolution runbooks.

## Multi-Chain Architecture
1. **Chain 1 (Alert Classifier):** Evaluates raw text payloads to determine security severity classifications (e.g., CRITICAL, HIGH, INFO) and calculates confidence metrics.
2. **Chain 2 (Threat Analyzer):** Breaks down flagged vulnerabilities, isolates specific suspicious metrics, and compiles structured threat vector fields.
3. **Chain 3 (Response Recommender):** Consumes the generated threat assessments and formats structured, step-by-step containment procedures into a final payload configuration.

## System Integration (n8n Data Flow)
* **Input Node:** Receives structured payloads extracted from transactional logs via an automated webhook container.
* **Output Node:** Transmits stringified data strings directly forward to update database records and trigger real-time notifications.

## Environment Configuration
To initialize this component, ensure the following keys are verified within your execution block environments:
* `GROQ_API_KEY`: Required to route language processing across the central inference nodes.
* `FLOWISE_HEADER_AUTH`: Used to grant safe transit permissions between the automation pipeline and the secure Flowise endpoints.

## Known Limitations & Enhancements
* **Nested String Collisions:** Raw data vectors with pre-existing double-quotes or raw newlines used to break string parsing constraints. 
* **Mitigation Strategy:** Implemented programmatic serialization filters (`jsonStringify()`) on all active expression properties inside the n8n engine to ensure error-free serialization.
