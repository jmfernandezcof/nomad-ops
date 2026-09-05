# NOMAD Ops — Architecture Components

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `components.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines the major logical components of NOMAD Ops and the responsibility of each one.

Its purpose is to establish:

- which major components exist;
- what responsibility belongs to each component;
- which responsibilities must remain separated;
- where AI fits within the platform;
- which components may make security or execution decisions;
- which boundaries must remain explicit.

This document does not define:

- deployment topology;
- ports;
- container layout;
- specific libraries;
- API endpoints;
- database schemas;
- detailed implementation.

Those decisions belong to later architecture or module specifications.

---

## 2. Core Architecture Principle

NOMAD Ops is controlled by application logic, not by an LLM.

The central architectural rule is:

> The backend orchestrator determines how a request should be handled. AI is one optional capability among several.

The platform may resolve a request using:

- deterministic application logic;
- direct data retrieval;
- search;
- RAG;
- workflow automation;
- LLM reasoning;
- tool execution;
- human approval;
- combinations of the above.

The presence of an AI model must not force every request through an LLM.

---

## 3. High-Level Logical Flow

Conceptually:

**User
→ Web Frontend
→ NOMAD Ops Backend / Orchestrator
→ authorization and context
→ appropriate capability selection
→ validation
→ optional execution
→ response**

Possible capability paths include:

**Direct deterministic path**

User
→ Backend
→ Authorization
→ Controlled Integration
→ Result

**RAG path**

User
→ Backend
→ Authorization
→ Retrieval
→ LLM reasoning over authorized evidence
→ Validated answer

**Sensitive action path**

User
→ Backend
→ Authorization
→ `REQUIRE_APPROVAL`
→ Human approval
→ Tool Gateway / Workflow
→ Execution
→ Audit

---

## 4. Web Frontend

### Responsibility

The Web Frontend provides the primary user interface for NOMAD Ops.

It is responsible for:

- presenting operational information;
- collecting user requests;
- presenting search results;
- displaying incidents;
- displaying evidence and sources;
- showing approvals;
- presenting execution state;
- presenting errors and degraded capability;
- providing the global command bar.

### Security Boundary

The frontend is not a security authority.

It must not make final decisions about:

- authorization;
- data access;
- HITL requirements;
- execution permission;
- security policy.

Frontend permission logic is for user experience only.

The backend must enforce actual policy.

---

## 5. NOMAD Ops Backend / Orchestrator

### Responsibility

The backend is the central application-control component.

It coordinates:

- authenticated user context;
- authorization;
- request classification;
- capability selection;
- retrieval;
- model invocation;
- tool invocation;
- workflow orchestration;
- HITL;
- validation;
- audit;
- usage and cost recording;
- failure-state management.

The backend is responsible for ensuring that a request follows approved system policy.

### Important Constraint

The backend must not automatically invoke an LLM for every request.

It should choose the least complex approved mechanism capable of satisfying the request.

---

## 6. Authentication and User Context

### Responsibility

This component establishes who is making the request and the business context associated with that identity.

It provides information such as:

- user identity;
- role;
- department;
- site;
- assigned scope;
- service identity where applicable.

### Constraint

Authentication establishes identity.

It does not grant authorization by itself.

Business permissions remain independent from the identity mechanism.

---

## 7. Policy and Authorization

### Responsibility

This component makes deterministic authorization decisions.

It evaluates factors such as:

- user;
- role;
- department;
- site;
- resource;
- requested action;
- data classification;
- operational context;
- action risk.

Possible authorization outcomes include:

- `ALLOW`
- `DENY`
- `REQUIRE_APPROVAL`

### Constraint

LLMs must not produce final authorization decisions.

This component is a security authority.

The AI Orchestration component is not.

---

## 8. Request Routing and Capability Selection

### Responsibility

The backend must determine which platform capabilities are required to satisfy a request.

Possible paths may include:

- deterministic application logic;
- source-system query;
- retrieval;
- RAG;
- LLM reasoning;
- tool invocation;
- n8n workflow;
- human approval.

### Example

Request:

> Show critical incidents from Plant 2.

Possible path:

- authenticate;
- authorize;
- query controlled ITSM integration;
- return structured results.

No LLM is required.

Request:

> Compare the current Plant 2 packaging incident with similar historical incidents and suggest the likely next step.

Possible path:

- authenticate;
- authorize;
- retrieve incident;
- retrieve related history;
- retrieve runbooks;
- invoke an approved LLM with authorized context;
- validate output;
- return recommendation and evidence.

---

## 9. AI Orchestration

### Responsibility

AI Orchestration manages approved interactions with LLMs.

It may be responsible for:

- selecting an approved model according to policy;
- constructing authorized context;
- applying data minimization;
- requesting structured output;
- validating model responses;
- recording usage;
- handling model failures;
- enforcing provider restrictions.

### Constraint

AI Orchestration does not decide:

- user authorization;
- business permissions;
- HITL bypass;
- secret access;
- infrastructure permissions.

It operates within constraints established by deterministic platform logic.

---

## 10. Retrieval Component

### Responsibility

The Retrieval component provides authorized access to enterprise knowledge.

It may support:

- metadata filtering;
- keyword retrieval;
- vector retrieval;
- document version filtering;
- source tracing;
- retrieval of authorized evidence.

### Constraint

Authorization must constrain the search universe before protected content is returned.

Retrieval relevance must never override access policy.

---

## 11. Tool Gateway

### Responsibility

The Tool Gateway exposes controlled operational capabilities.

Its purpose is to prevent models or users from receiving unrestricted access to underlying systems.

Tools must be:

- narrow;
- explicitly defined;
- authorized;
- auditable;
- validated;
- risk-classified.

Examples may include:

- `get_incident_details`
- `get_supplier_status`
- `check_service_health`
- `create_incident`
- `request_service_restart`

### Constraint

The Tool Gateway must not expose generic unrestricted capabilities where a narrow business tool is sufficient.

---

## 12. Human Approval / HITL

### Responsibility

The Approval component manages actions requiring human authorization.

It is responsible for:

- creating approval requests;
- storing approval state;
- identifying authorized approvers;
- presenting approval context;
- recording approval or rejection;
- preventing execution before valid approval;
- detecting stale approvals.

### Constraint

Approval must occur before execution for actions classified as `REQUIRE_APPROVAL`.

An LLM, workflow or tool must not bypass this component.

---

## 13. Workflow Orchestration

### Responsibility

Deterministic and multi-step business workflows may be delegated to the automation layer.

The currently approved automation platform is n8n.

Appropriate use cases may include:

- notifications;
- multi-system deterministic processes;
- document-routing workflows;
- controlled operational procedures;
- business-process automation.

### Constraint

n8n is an execution/orchestration component, not a security authority.

NOMAD Ops must expose approved business workflows rather than unrestricted n8n control.

---

## 14. PostgreSQL

### Responsibility

PostgreSQL is the primary relational data store for NOMAD Ops-owned operational state.

It may hold data such as:

- local users and identity references;
- role and scope assignments;
- authorization-related configuration;
- approvals;
- audit references;
- workflow state;
- cost and usage records;
- platform configuration;
- source-system references.

### Constraint

PostgreSQL is not automatically the system of record for Asteria business data owned by external enterprise systems.

Detailed schemas will be defined later.

---

## 15. Qdrant

### Responsibility

Qdrant provides vector retrieval capabilities for approved knowledge content.

It may store:

- embeddings;
- authorized chunks;
- document references;
- retrieval metadata;
- classification and scope metadata required for filtering.

### Constraint

Qdrant is a retrieval component, not an authorization authority.

Vector similarity alone must never determine data access.

Critical secrets must not be embedded.

---

## 16. Mock Enterprise Services

### Responsibility

Mock Enterprise Services simulate external Asteria systems.

They may represent:

- ITSM;
- ERP;
- HR;
- Plant Operations;
- industrial monitoring;
- document-management systems;
- other enterprise services justified later.

### Purpose

They exist to provide realistic:

- data;
- states;
- failures;
- permissions;
- API behaviour;
- write operations;
- sandbox actions.

### Constraint

Simulation must preserve enterprise controls.

Mock services must not become shortcuts around:

- authorization;
- HITL;
- failure handling;
- audit;
- data classification.

---

## 17. Model Providers

### Responsibility

Model providers supply LLM inference when a business use case requires reasoning or generation.

Possible providers may include:

- external model providers;
- local models;
- restricted processing options.

This document does not select specific models.

### Constraint

Provider access must be governed by:

- model approval;
- data classification;
- business purpose;
- privacy requirements;
- retention;
- processing location;
- cost;
- latency.

A provider is not selected merely because it is available.

---

## 18. Audit and Operational Telemetry

### Responsibility

NOMAD Ops must produce audit and operational telemetry from relevant components.

This includes events related to:

- authorization;
- retrieval;
- model invocation;
- tool execution;
- workflow execution;
- approval;
- failure;
- external integrations;
- cost and usage.

This logical capability may later be implemented through multiple technical components.

### Constraint

Observability must not create a secondary uncontrolled repository of sensitive data or secrets.

---

## 19. Component Responsibility Separation

Responsibilities must remain separated.

Conceptually:

**Frontend**
→ interaction

**Backend / Orchestrator**
→ control and coordination

**Policy**
→ authorization

**Retrieval**
→ evidence

**LLM**
→ reasoning and generation

**Tool Gateway**
→ controlled capabilities

**n8n**
→ deterministic workflow execution

**Human**
→ approval where required

**Audit / Observability**
→ traceability

No single component should silently absorb all of these responsibilities.

---

## 20. No Mandatory AI Path

Every feature specification must explicitly state whether AI is required.

Valid outcomes include:

- no AI;
- deterministic logic;
- retrieval only;
- retrieval + LLM;
- LLM only where justified;
- workflow automation;
- agentic/tool-based behaviour;
- human-only decision.

The architecture must support non-AI paths as first-class behaviour.

---

## 21. Component Evolution Principle

The components defined here are logical responsibilities.

They do not imply that every component must become:

- a separate container;
- a separate service;
- a microservice;
- a separate repository;
- a separate process.

Physical separation must be justified later by:

- security;
- scale;
- reliability;
- deployment;
- operational complexity;
- business need.

The architecture must not adopt microservices merely to appear enterprise.

---

## 22. Open Architecture Decisions

This specification intentionally does not decide:

- frontend framework;
- exact backend framework configuration;
- authentication implementation;
- policy-engine technology;
- secret-management technology;
- observability stack;
- model-routing implementation;
- service decomposition;
- deployment topology;
- network layout;
- exact mock-service architecture.

These decisions must be made later when requirements justify them.

---

## 23. Component Architecture Principle

The central principle is:

> NOMAD Ops is an application-controlled operations platform that may use AI when reasoning adds value, while deterministic policy, controlled integrations and human authority remain responsible for security and execution boundaries.

The LLM is a capability inside NOMAD Ops.

It is not NOMAD Ops itself.
