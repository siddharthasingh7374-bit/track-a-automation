# Custom Agents and Skills

## Custom Agent: Document Triage Agent
* **Role**: Processes incoming employee onboarding documents (e.g., ID cards, tax forms).
* **Location**: `agents/document_triage_agent.py`
* **Purpose**: Extracts key metadata, checks for validity, and queues the document for human verification.

## Custom Skill: Human Approval Logger
* **Function**: `log_human_approval()`
* **Location**: `skills/approval_logger.py`
* **Purpose**: Generates audit trails whenever a human manager approves or rejects an onboarding step, ensuring full traceability.