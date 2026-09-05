# NOMAD Ops — Architecture Foundation Acceptance Criteria

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `acceptance.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines mandatory acceptance criteria for `002-architecture-foundation`. They validate architectural boundaries without selecting technologies or requiring each logical responsibility to be a separate service.

## 2. Requirement Level

All criteria `AC-002-001` through `AC-002-032` are mandatory unless an approved later SPEC explicitly refines or replaces them.

## 3. Component and Control Criteria

### AC-002-001 — Backend Controls Requests

Protected request routing, authorization, validation, HITL and execution must remain controlled by the backend / orchestrator.

### AC-002-002 — AI Is Optional

Capabilities that do not require AI must have a first-class non-AI path; an LLM must not be invoked merely because one is available.

### AC-002-003 — Logical Does Not Mean Microservice

Logical components must not require separate services, containers, repositories or processes without an approved decision.

### AC-002-004 — Canonical States

Authorization must use `ALLOW`, `DENY`, `REQUIRE_APPROVAL`; execution must use `NOT_STARTED`, `SUCCESS`, `FAILED`, `UNKNOWN`; `DENY` must leave execution `NOT_STARTED`.

### AC-002-005 — HITL Revalidation

After approval and before execution, context, authorization and approval binding must be revalidated. Approval must not override authorization or become reusable authority.

### AC-002-006 — LLM Tool Proposal

An LLM-generated tool call must remain a proposal until the backend validates tool identity, arguments, authoritative identifiers, scope, authorization, risk and HITL.

## 4. Data Criteria

### AC-002-007 — Systems of Record Remain Authoritative

Local copies, caches, chunks, embeddings, summaries and model outputs must not replace authoritative enterprise records.

### AC-002-008 — NOMAD Ops Operational State

PostgreSQL may hold NOMAD Ops-owned operational state but must not silently become the system of record for ITSM, ERP, HR, Plant Operations or controlled documents.

### AC-002-009 — Qdrant Does Not Authorize

Qdrant may hold approved retrieval representations, but authorization must constrain protected retrieval before evidence is returned.

### AC-002-010 — Derived Classification

Derived data must retain source handling requirements unless an approved classification process determines otherwise; embeddings must not be presumed anonymous.

### AC-002-011 — Data Minimization

Retrieval, model context, tools, workflows, APIs, caches, audit and telemetry must use only data necessary for their approved purpose.

### AC-002-012 — Lineage and Currency

Derived knowledge must preserve appropriate source and version traceability; obsolete content must not knowingly be presented as current, and uncertain currency must remain explicit.

### AC-002-013 — Current Authorization Applies

Cached or indexed protected data and cross-user reuse must be evaluated against current authorization, scope and classification.

### AC-002-014 — Invalidation Is Possible

Derived or indexed representations must be conceptually invalidatable when source eligibility, version, classification or scope changes, without prescribing a mechanism.

## 5. Integration Criteria

### AC-002-015 — Read and Write Are Separate

Read permission must not imply write permission; state-changing operations require independent authorization and risk handling.

### AC-002-016 — Tools Are Narrow

Approved narrow capabilities must be used instead of unrestricted SQL, API or command execution.

### AC-002-017 — n8n Is Orchestration

n8n must not become authorization, policy, security or data authority, or an unrestricted execution surface for an LLM.

### AC-002-018 — Inputs and Outputs Are Validated

Inputs from every source must be treated as untrusted, and integration output must be validated before downstream use; transport success alone must not imply business success.

### AC-002-019 — Hostile Content Is Data

Instructions in documents, email, events, APIs or tool output must not redefine policy, authorization, scope, tools or HITL.

### AC-002-020 — Multi-Step Outcomes Remain Visible

Partial workflows must preserve relevant step outcomes and must not be collapsed into global `SUCCESS`.

### AC-002-021 — Timeout and Retry Safety

Blocking calls must have bounded timeouts; retries must be bounded and sensitive to idempotency, rate limits, impact and execution uncertainty.

### AC-002-022 — UNKNOWN Writes Are Protected

Sensitive writes in `UNKNOWN` must not be blindly retried; target state must be checked where possible and retry must follow approved policy.

### AC-002-023 — Fallback Is Explicit

Fallback must not be silent and must preserve authorization, classification, processing restrictions and auditability.

### AC-002-024 — Service Identity Is Scoped

Scheduled, event-driven and service-to-service requests must use identifiable scoped service identities; credentials must not confer initiating-user permission.

### AC-002-025 — Mock Controls Are Real Controls

Mock and sandbox integrations must preserve authorization, HITL, validation, classification, failure and audit semantics and must not affect unrelated real services.

## 6. Observability and Secret Criteria

### AC-002-026 — Request Correlation

Relevant request stages must be reconstructable through appropriate correlation and identity references without exposing unauthorized content.

### AC-002-027 — Failure and Degradation Are Visible

Telemetry must distinguish canonical execution states, partial outcomes and capability-specific degradation without fabricated success.

### AC-002-028 — Usage Survives Failure

Measurable model, embedding, workflow and retry usage must remain attributable when the associated operation fails.

### AC-002-029 — Telemetry Is Minimized

Audit, logs, metrics and traces must respect classification, authorization, minimization, masking and environment boundaries.

### AC-002-030 — Critical Secrets Never Leak

Critical secrets must not enter LLMs, RAG, embeddings, Qdrant, clients, tool outputs, source, tests, or application, model, workflow and audit telemetry.

### AC-002-031 — Configuration Cannot Override Policy

Frontend, models, retrieved content and external responses must not redefine security configuration; missing configuration must fail explicitly rather than weaken policy.

### AC-002-032 — Open Decisions Stay Open

Conformance must not require an unapproved choice of framework, provider, cache, observability or secrets stack, queue, broker, topology, service decomposition, SLO or retention period.

## 7. Gate Completion

The architecture foundation is conformant when all applicable criteria can be traced to later design, implementation tests or explicit validation and any deliberate exception is approved and recorded.

## 8. Final Acceptance Principle

> NOMAD Ops architecture is acceptable only when correct outcomes are produced through authorized, controlled, observable and appropriately minimized paths without silently resolving open decisions.
