# Architecture Document — Automated Onboarding Coordinator

**Document Version:** 1.0
**Architecture Role:** Principal Software Architect
**Product:** Automated Onboarding Coordinator
**Architecture Type:** Track A — Business Process Automation
**Primary Design Principle:** Automation with Human-in-the-Loop traceability

---

# 1. Architecture Overview

The **Automated Onboarding Coordinator** is a workflow-driven business process automation application.

Its architecture separates the system into five major responsibilities:

1. **Input & User Interface** — Receives onboarding information and documents.
2. **Workflow/API Backend** — Coordinates tasks and controls business rules.
3. **AI/Automation Processing** — Classifies and validates documents or information.
4. **Human Approval Layer** — Routes uncertain or sensitive decisions to authorized users.
5. **Execution & Audit Layer** — Executes approved actions and records every decision.

The core architectural principle is:

> **AI can recommend or perform predefined low-risk operations, but important decisions must remain reviewable and traceable by humans.**

---

# 2. High-Level Tech Stack

## 2.1 Recommended Stack

| Layer                  | Technology                                      | Purpose                                   |
| ---------------------- | ----------------------------------------------- | ----------------------------------------- |
| Frontend               | HTML5, CSS3, JavaScript                         | Web-based user interface                  |
| Alternative UI         | CLI                                             | Lightweight development/testing interface |
| Backend                | Node.js + Express                               | REST API and workflow orchestration       |
| AI/Document Processing | Python                                          | Document classification and validation    |
| Database               | SQLite                                          | Persistent relational storage             |
| Containerization       | Docker                                          | Reproducible application environment      |
| API Format             | REST/JSON                                       | Frontend-backend communication            |
| Authentication         | Session/JWT-based authentication                | User authentication                       |
| Logging                | Structured application logs + SQLite audit logs | Operational and business traceability     |
| Testing                | Jest / Pytest                                   | Automated testing                         |

### Recommended Architecture

```text
Frontend
HTML + CSS + JavaScript
        │
        │ REST/JSON
        ▼
Node.js / Express Backend
        │
        ├──────────────► SQLite
        │
        ├──────────────► Workflow Engine
        │
        ├──────────────► Audit Logger
        │
        ▼
Python AI Service
        │
        └──────────────► Document Processing
```

---

# 3. Technology Responsibilities

## 3.1 Frontend

The frontend provides interfaces for:

* User login
* Onboarding case creation
* Document upload
* Task dashboard
* Human approval dashboard
* Escalation dashboard
* Audit history
* Case status

### Technologies

```text
HTML5
CSS3
JavaScript
Fetch API
```

The MVP does not require a large frontend framework.

A simple HTML/CSS/JavaScript application reduces deployment complexity and is sufficient for the initial product.

---

# 4. Node.js Backend

Node.js acts as the primary application server.

### Responsibilities

* Authentication
* Authorization
* REST APIs
* User management
* Task management
* Workflow orchestration
* Approval management
* Escalation handling
* Database access
* Audit event generation
* Communication with Python AI service

### Example API Structure

```text
/api
    /auth
        POST /login

    /users
        GET    /
        POST   /
        PATCH  /:id

    /onboarding
        POST   /
        GET    /
        GET    /:id

    /documents
        POST   /
        GET    /:id

    /tasks
        GET    /
        GET    /:id
        PATCH  /:id

    /approvals
        GET    /
        POST   /:id/approve
        POST   /:id/reject

    /escalations
        GET    /
        POST   /:id/resolve

    /audit
        GET    /case/:caseId
```

---

# 5. Python AI Processing Service

Python is responsible for AI-assisted document processing.

### Responsibilities

* Document classification
* Text extraction
* Field extraction
* Validation
* Confidence calculation
* Anomaly detection
* AI recommendation generation

### Example Flow

```text
Document
   ↓
Python Processing Service
   ↓
Extract Text
   ↓
Classify Document
   ↓
Extract Required Fields
   ↓
Validate Fields
   ↓
Calculate Confidence
   ↓
Return Result
```

### Example Response

```json
{
  "document_type": "government_id",
  "confidence": 0.94,
  "validation_status": "VALID",
  "recommendation": "ACCEPT",
  "reason": "Required fields detected and valid"
}
```

The AI service does **not** directly approve sensitive business decisions.

The Node.js workflow layer remains responsible for enforcing business rules.

---

# 6. SQLite Database

SQLite is appropriate for the MVP because the application requires:

* Relational data
* Transactions
* Simple deployment
* Local persistence
* No separate database server

The SQLite database should be stored on a persistent Docker volume.

```text
Docker Container
      │
      ▼
/data/onboarding.db
      │
      ▼
Persistent Docker Volume
```

For a production-scale deployment with multiple application instances, SQLite should eventually be replaceable with PostgreSQL.

---

# 7. Docker Architecture

The application should be containerized.

### MVP Container Structure

```text
Docker Environment
│
├── Backend Container
│   └── Node.js + Express
│
├── AI Container
│   └── Python processing service
│
└── Persistent Volume
    └── SQLite database
```

An optional frontend container may be added later if static assets are served separately.

### Example Project Structure

```text
automated-onboarding/
│
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── database/
│   │   └── audit/
│   ├── package.json
│   └── Dockerfile
│
├── ai-service/
│   ├── app/
│   │   ├── classifier/
│   │   ├── validator/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── data/
│   └── onboarding.db
│
├── docker-compose.yml
└── README.md
```

---

# 8. Data Model

The core database entities are:

```text
Users
  │
  ├──────────────┐
  ▼              ▼
Tasks          Approvals
  │              │
  └──────┬───────┘
         ▼
       Logs
```

The four mandatory core tables are:

1. `users`
2. `tasks`
3. `approvals`
4. `logs`

Additional tables such as `onboarding_cases` and `documents` are recommended because they make the domain model clearer.

---

# 9. Database Schema

## 9.1 Users

Stores application users and their roles.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Important Fields

| Field           | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `id`            | Unique user identifier                         |
| `name`          | User's display name                            |
| `email`         | Login identifier                               |
| `password_hash` | Secure password representation                 |
| `role`          | Coordinator, Reviewer, Manager, Admin, Auditor |
| `status`        | ACTIVE / INACTIVE                              |
| `created_at`    | Account creation time                          |

---

# 10. Onboarding Cases

Although not one of the four mandatory tables, this entity should exist to represent the primary business process.

```sql
CREATE TABLE onboarding_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_reference TEXT NOT NULL UNIQUE,
    subject_name TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'NORMAL',
    assigned_user_id INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (assigned_user_id)
        REFERENCES users(id)
);
```

### Example Statuses

```text
CREATED
DOCUMENTS_PENDING
PROCESSING
REVIEW_REQUIRED
APPROVED
COMPLETED
BLOCKED
ESCALATED
REJECTED
CANCELLED
```

---

# 11. Tasks

Tasks represent actionable workflow work.

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    assigned_to INTEGER,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'NORMAL',
    description TEXT,
    due_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,

    FOREIGN KEY (case_id)
        REFERENCES onboarding_cases(id),

    FOREIGN KEY (assigned_to)
        REFERENCES users(id)
);
```

### Example Task Types

```text
DOCUMENT_REVIEW
MISSING_DOCUMENT
APPROVAL
ESCALATION
VALIDATION_EXCEPTION
INFORMATION_REQUEST
```

### Example Task Lifecycle

```text
CREATED
   ↓
ASSIGNED
   ↓
IN_PROGRESS
   ↓
COMPLETED
```

---

# 12. Documents

Documents should be stored separately from tasks.

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    document_type TEXT,
    status TEXT NOT NULL,
    confidence REAL,
    uploaded_by INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (case_id)
        REFERENCES onboarding_cases(id),

    FOREIGN KEY (uploaded_by)
        REFERENCES users(id)
);
```

The actual document file should normally be stored outside the SQLite database.

SQLite stores the metadata and secure file reference.

---

# 13. Approvals

The `approvals` table represents explicit human decisions.

```sql
CREATE TABLE approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    decision TEXT NOT NULL,
    reason TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (task_id)
        REFERENCES tasks(id),

    FOREIGN KEY (reviewer_id)
        REFERENCES users(id)
);
```

### Decision Values

```text
APPROVED
REJECTED
REQUEST_INFORMATION
ESCALATED
```

### Important Principle

An approval record must always identify:

```text
WHO
WHAT
WHEN
WHY
```

---

# 14. Logs / Audit Events

The `logs` table is the central traceability mechanism.

```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    case_id INTEGER,
    actor_type TEXT NOT NULL,
    actor_id TEXT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    previous_state TEXT,
    new_state TEXT,
    reason TEXT,
    workflow_id TEXT,
    correlation_id TEXT,
    automation_version TEXT,
    metadata TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (case_id)
        REFERENCES onboarding_cases(id)
);
```

---

# 15. Database Relationships

```text
                    ┌─────────────┐
                    │    USERS    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          CASE OWNER     TASKS       APPROVALS
              │            │            │
              │            ▼            │
              │       ONBOARDING        │
              │          CASE           │
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                         LOGS
```

---

# 16. High-Level System Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                       USER                               │
│                                                          │
│  Coordinator / Reviewer / Manager / Admin / Auditor     │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    FRONTEND                              │
│                                                          │
│              HTML + CSS + JavaScript                     │
│                                                          │
│  Case UI | Document Upload | Approval Dashboard          │
│  Escalations | Audit History                             │
└─────────────────────────┬────────────────────────────────┘
                          │
                     REST / JSON
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                 NODE.JS BACKEND                          │
│                                                          │
│  Authentication / Authorization                          │
│  API Controllers                                         │
│  Workflow Engine                                         │
│  Task Manager                                            │
│  Approval Manager                                        │
│  Escalation Manager                                      │
│  Audit Logger                                            │
└───────┬──────────────────────┬───────────────────────────┘
        │                      │
        │                      │
        ▼                      ▼
┌───────────────┐       ┌────────────────────┐
│    SQLite     │       │ Python AI Service  │
│               │       │                    │
│ Users         │       │ Classification     │
│ Cases         │       │ Extraction         │
│ Tasks         │       │ Validation         │
│ Approvals     │       │ Confidence         │
│ Logs          │       │ Recommendation     │
└───────────────┘       └─────────┬──────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ AI Result       │
                         │                 │
                         │ Type            │
                         │ Confidence      │
                         │ Validation      │
                         │ Recommendation  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Workflow Engine │
                         └────────┬────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              High Confidence            Low Confidence
                    │                           │
                    ▼                           ▼
              AUTOMATED PATH              HUMAN REVIEW
                    │                           │
                    │                    ┌──────┴──────┐
                    │                    │             │
                    │                 APPROVE       REJECT
                    │                    │             │
                    └──────────┬─────────┴─────────────┘
                               │
                               ▼
                         EXECUTION
                               │
                               ▼
                         AUDIT LOGGER
                               │
                               ▼
                            LOGS
```

---

# 17. End-to-End Data Flow

## Step 1 — Input

A coordinator creates an onboarding case.

```text
User
 ↓
Frontend
 ↓
POST /api/onboarding
 ↓
Node.js
 ↓
SQLite
```

The system creates the case and writes an audit event.

---

## Step 2 — Document Submission

```text
User
 ↓
Document Upload
 ↓
Node.js
 ↓
Document Storage
 ↓
SQLite Metadata
```

An audit event records:

```text
DOCUMENT_UPLOADED
```

---

# 18. AI Processing Flow

The backend sends the document to Python.

```text
Node.js
   │
   │ document
   ▼
Python AI Service
   │
   ├── Extract text
   ├── Classify
   ├── Validate
   └── Calculate confidence
   │
   ▼
AI Result
   │
   ▼
Node.js Workflow Engine
```

The AI service returns a structured result rather than directly changing the business state.

---

# 19. Human-in-the-Loop Flow

The workflow engine evaluates the AI result.

```text
AI Result
    │
    ▼
Confidence / Business Rules
    │
    ├───────────────┐
    │               │
    ▼               ▼
ACCEPTABLE       UNCERTAIN
    │               │
    ▼               ▼
Continue        Create Task
                    │
                    ▼
             Human Approval
                    │
             ┌──────┴──────┐
             ▼             ▼
          APPROVE        REJECT
             │             │
             └──────┬──────┘
                    ▼
                Workflow
                 Continues
```

The AI recommendation and human decision are stored independently.

---

# 20. Execution Layer

After an authorized decision, the workflow engine performs the appropriate action.

Example:

```text
Human Approval
      ↓
Workflow Engine
      ↓
Validate Permission
      ↓
Execute Action
      ↓
Update Case
      ↓
Create Audit Event
      ↓
Notify User
```

No execution should occur without a valid authorization check.

---

# 21. Audit & Logging Architecture

Audit logging is implemented as a cross-cutting service.

```text
┌─────────────────────────────────────┐
│          Application Events          │
├─────────────────────────────────────┤
│ Case Created                        │
│ Document Uploaded                   │
│ AI Classification                   │
│ Validation                          │
│ Approval                            │
│ Rejection                           │
│ Escalation                          │
│ Execution                           │
│ Workflow Failure                    │
└──────────────────┬──────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │  Audit Logger   │
          └────────┬────────┘
                   │
                   ▼
             ┌───────────┐
             │   Logs    │
             │  SQLite   │
             └───────────┘
```

---

# 22. Audit Event Structure

Every business-critical event should produce an event similar to:

```json
{
  "event_id": "evt_8f92ab",
  "timestamp": "2026-08-07T14:31:22Z",
  "actor_type": "AUTOMATION",
  "actor_id": "document-triage-service",
  "action": "DOCUMENT_CLASSIFIED",
  "entity_type": "DOCUMENT",
  "entity_id": "DOC-1023",
  "previous_state": "PROCESSING",
  "new_state": "NEEDS_REVIEW",
  "reason": "Low confidence classification",
  "workflow_id": "WF-9982",
  "correlation_id": "CORR-55421",
  "automation_version": "triage-v1.4",
  "metadata": {
    "document_type": "government_id",
    "confidence": 0.61
  }
}
```

This allows an auditor to reconstruct exactly what happened.

---

# 23. Actor Model

The system distinguishes three actor types.

## HUMAN

```text
actor_type = HUMAN
actor_id = user_123
```

Example:

```text
Reviewer approved document.
```

## AUTOMATION

```text
actor_type = AUTOMATION
actor_id = document-triage-service
```

Example:

```text
AI classified document.
```

## SYSTEM

```text
actor_type = SYSTEM
actor_id = escalation-scheduler
```

Example:

```text
SLA automatically breached.
```

This distinction is critical for Human-in-the-Loop traceability.

---

# 24. Correlation IDs

Related events must share a correlation ID.

Example:

```text
CORR-12345

    ├── CASE_CREATED
    ├── DOCUMENT_UPLOADED
    ├── DOCUMENT_CLASSIFIED
    ├── VALIDATION_COMPLETED
    ├── REVIEW_REQUESTED
    ├── HUMAN_APPROVED
    └── CASE_COMPLETED
```

This allows the complete lifecycle of one workflow execution to be reconstructed.

---

# 25. Automation Versioning

Every AI/automation decision must identify the version that produced it.

Example:

```text
automation_version:
"document-triage-v1.4.2"
```

If the AI model or business rule changes later, historical decisions remain attributable to the exact version that produced them.

This is particularly important when investigating:

* Incorrect classifications
* Unexpected workflow behavior
* Model regressions
* Policy changes
* Historical approvals

---

# 26. State Transition Logging

Every meaningful state transition must be logged.

Example:

```text
BEFORE:
REVIEW_REQUIRED

ACTION:
Reviewer approves document

AFTER:
APPROVED
```

Audit event:

```text
ACTION = APPROVAL_GRANTED

previous_state = REVIEW_REQUIRED
new_state = APPROVED
actor_type = HUMAN
actor_id = reviewer_42
```

Invalid state transitions must be rejected by the workflow engine.

---

# 27. Failure Logging

Failures must be treated as first-class events.

Example:

```json
{
  "action": "AI_PROCESSING_FAILED",
  "actor_type": "AUTOMATION",
  "actor_id": "document-service",
  "reason": "Processing timeout",
  "metadata": {
    "attempt": 3,
    "max_attempts": 3,
    "error_code": "AI_TIMEOUT"
  }
}
```

The workflow engine can then create a human task:

```text
AI_PROCESSING_FAILED
        ↓
Retry
        ↓
Retry Failed
        ↓
Create HUMAN_REVIEW task
        ↓
Escalate if SLA exceeded
```

---

# 28. Audit Immutability

The application must treat audit records as append-only.

Normal users must not be able to:

* UPDATE audit events
* DELETE audit events
* Change timestamps
* Change actors
* Rewrite historical decisions

If a correction is required:

```text
Original Event
      ↓
Correction Event
      ↓
New Current State
```

The original event remains preserved.

---

# 29. Transactional Consistency

Business state changes and corresponding audit events should be committed atomically where practical.

Example:

```text
BEGIN TRANSACTION

UPDATE onboarding_cases
SET status = 'APPROVED'

INSERT INTO logs
(action, previous_state, new_state, actor_type)
VALUES
('CASE_APPROVED',
 'REVIEW_REQUIRED',
 'APPROVED',
 'HUMAN')

COMMIT
```

If either operation fails, the transaction should roll back.

This prevents a dangerous state where:

```text
Case = APPROVED
Audit Log = Missing
```

---

# 30. Security Architecture

The backend must enforce authorization rather than relying on frontend controls.

```text
User
 ↓
Authentication
 ↓
Identity
 ↓
Role
 ↓
Permission Check
 ↓
Business Operation
 ↓
Audit Event
```

For example:

```text
Reviewer → Can approve
Coordinator → Cannot approve
Auditor → Read-only
Admin → Can manage users
```

The UI should hide unavailable actions, but the API must independently reject unauthorized requests.

---

# 31. Recommended Service Boundaries

For the MVP, the system should remain relatively simple.

### Node.js Modules

```text
AuthService
UserService
CaseService
TaskService
DocumentService
WorkflowService
ApprovalService
EscalationService
AuditService
NotificationService
```

### Python Modules

```text
DocumentProcessor
TextExtractor
DocumentClassifier
FieldExtractor
Validator
ConfidenceEvaluator
```

These should initially be implemented as modular services rather than immediately splitting everything into independent microservices.

---

# 32. Architectural Decision: Modular Monolith + AI Service

The recommended MVP architecture is:

```text
             ┌─────────────────────┐
             │     Node.js App     │
             │                     │
             │ Modular Monolith    │
             │                     │
             │ Auth                │
             │ Cases               │
             │ Tasks               │
             │ Workflow            │
             │ Approvals           │
             │ Escalations         │
             │ Audit               │
             └──────────┬──────────┘
                        │
                        ▼
                ┌───────────────┐
                │ Python AI     │
                │ Service       │
                └───────────────┘
                        │
                        ▼
                  AI Processing
```

This avoids unnecessary microservice complexity during the MVP while keeping the AI workload isolated.

---

# 33. Future Scalability

The architecture can evolve from:

```text
Node.js + Python + SQLite
```

to:

```text
                 API Gateway
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
   User Service   Workflow       Document
                   Service        Service
        │             │              │
        └─────────────┼──────────────┘
                      │
                PostgreSQL
                      │
              ┌───────┴────────┐
              ▼                ▼
         Object Storage     Event Bus
```

Potential future technologies include:

* PostgreSQL instead of SQLite
* Object storage for documents
* Redis for caching
* Message queue/event bus for asynchronous processing
* Dedicated AI inference infrastructure
* Centralized observability platform

These are **not required for the MVP**.

---

# 34. End-to-End Reference Flow

The complete system flow is:

```text
┌──────────┐
│   USER   │
└────┬─────┘
     │
     ▼
┌──────────────┐
│   FRONTEND   │
└────┬─────────┘
     │
     ▼
┌───────────────────┐
│   NODE.JS API     │
└────┬─────────┬────┘
     │         │
     │         └──────────────┐
     │                        ▼
     │                  ┌───────────┐
     │                  │ AUDIT LOG │
     │                  └─────┬─────┘
     │                        │
     ▼                        ▼
┌──────────────┐        ┌───────────┐
│   WORKFLOW   │───────►│  SQLITE   │
│    ENGINE    │        └───────────┘
└──────┬───────┘
       │
       ▼
┌────────────────┐
│ PYTHON AI      │
│ PROCESSING     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ AI RESULT      │
│ + CONFIDENCE   │
└───────┬────────┘
        │
        ▼
┌────────────────────┐
│ WORKFLOW DECISION  │
└────────┬───────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
 AUTOMATE    HUMAN
    │        REVIEW
    │          │
    │     ┌────┴────┐
    │     ▼         ▼
    │  APPROVE    REJECT
    │     │         │
    └─────┴────┬────┘
               ▼
        ┌─────────────┐
        │  EXECUTION  │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │ AUDIT EVENT │
        └──────┬──────┘
               ▼
             LOGS
```

---

# 35. Architecture Principles

## Principle 1 — Human decisions are explicit

An AI recommendation must never be represented as a human approval.

## Principle 2 — Auditability is part of the workflow

Audit events are generated as part of business operations, not as an afterthought.

## Principle 3 — Backend owns business rules

Frontend validation improves UX but cannot be trusted for authorization or workflow enforcement.

## Principle 4 — AI is advisory unless explicitly authorized

The AI service returns structured results. The workflow engine decides what those results are allowed to trigger.

## Principle 5 — Preserve historical truth

Historical events are immutable. Corrections are represented by new events.

## Principle 6 — Fail visibly

Automation failures must result in retry, exception handling, or human intervention rather than silent failure.

## Principle 7 — Start simple

The MVP uses:

```text
HTML/CSS/JS
       +
Node.js
       +
Python
       +
SQLite
       +
Docker
```

rather than introducing unnecessary infrastructure.

---

# 36. Final Architecture Summary

The **Automated Onboarding Coordinator** should be implemented as a **Dockerized modular Node.js application with a dedicated Python AI-processing service and SQLite persistence layer**.

The fundamental data path is:

```text
INPUT
  ↓
NODE.JS API
  ↓
WORKFLOW ENGINE
  ↓
PYTHON AI PROCESSING
  ↓
AI RESULT + CONFIDENCE
  ↓
BUSINESS RULES
  ↓
┌─────────────────┐
│                 │
▼                 ▼
AUTOMATION     HUMAN APPROVAL
│                 │
└────────┬────────┘
         ▼
     EXECUTION
         ↓
     AUDIT LOG
         ↓
       SQLITE
```

The architecture's most important property is **decision traceability**.

For any completed onboarding case, an authorized auditor should be able to reconstruct:

```text
Who initiated it?
        ↓
What data was submitted?
        ↓
What did automation do?
        ↓
Which automation version was used?
        ↓
What result did it produce?
        ↓
Why was human review required?
        ↓
Who reviewed it?
        ↓
What decision did they make?
        ↓
Why did they make it?
        ↓
What action was executed?
        ↓
What was the final outcome?
```

That trace must remain available even after corrections, reassignment, escalation, or workflow failure.
