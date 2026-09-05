# NOMAD Ops — Integration Patterns

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `integration-patterns.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines approved logical patterns for integrations between NOMAD Ops, enterprise systems, tools, workflows, retrieval and model providers. It does not select protocols, infrastructure products, deployment topology or service decomposition.

## 2. Integration Control

The backend / orchestrator controls protected integration flow. Frontend, LLMs, Qdrant, n8n, providers, external systems and mocks are not authorization authorities. Protected operations remain subject to deterministic policy, validation and audit.

## 3. Controlled Boundaries

Integrations must use explicit interfaces such as narrow tools, approved APIs, internal service interfaces or approved workflows. Network reachability, co-location or possession of credentials does not grant permission. Enterprise systems retain system-of-record authority.

## 4. Read and Write Separation

Read permission does not imply write permission. Writes require independent authorization, risk evaluation and HITL where policy returns `REQUIRE_APPROVAL`. Authorization outcomes are `ALLOW`, `DENY` and `REQUIRE_APPROVAL`; `DENY` leaves execution `NOT_STARTED`.

## 5. Narrow Tools

Tools must expose the minimum approved business capability and define target, inputs, outputs, errors, sensitivity, risk, authorization and approval requirements. Unrestricted SQL, arbitrary API access or arbitrary command execution must not replace a suitable narrow tool.

## 6. LLM Tool Proposals

> An LLM-generated tool call is a proposal, not an executable instruction.

The backend must resolve the approved tool, validate its existence and arguments, resolve authoritative identifiers, evaluate scope, authorization, risk and HITL, and execute only when permitted. Model-supplied names, identifiers, scopes and security claims are untrusted.

## 7. Database Access

LLMs, frontends and generic workflows must not receive unrestricted database or arbitrary SQL access. Database operations must use controlled application logic or approved narrow tools. PostgreSQL must not become a backdoor into enterprise-owned authority.

## 8. Workflow Orchestration

n8n may execute approved workflows through controlled entry points. It is workflow orchestration, not authorization, policy, security or data authority, and not a system of record. LLMs must not receive unrestricted n8n administration or arbitrary workflow execution.

## 9. Multi-Step Workflows

Multi-step integrations must preserve relevant completed, failed, skipped, pending and unknown step outcomes. Partial execution must not be reported as global `SUCCESS`. Compensation or manual intervention requires later approved definition where applicable.

## 10. Synchronous and Asynchronous Patterns

Either pattern may be used when justified by a later capability specification. This document mandates no queue, event bus, broker, worker platform or scheduler technology.

## 11. Scheduled and Event-Driven Requests

Schedules and events are request sources, not authorization. They require an identifiable scoped service identity and remain subject to policy, validation, classification, environment and audit controls. Event payloads are untrusted. No event transport is selected.

## 12. Polling

Polling may be used only when justified. Its frequency must account for freshness, rate limits, cost and dependency impact. No universal interval or default polling model is defined.

## 13. Model Providers

Providers are processing capabilities only. Before sending data, the backend must enforce authorization, provider eligibility, classification, minimization, redaction, critical-secret exclusion and external-processing restrictions. No provider, model or router is selected.

## 14. Retrieval and Knowledge

Authorization must constrain protected retrieval before evidence is returned. Qdrant does not authorize and similarity is not permission logic. Source, version, classification and scope must remain traceable where required. Document / Knowledge Management remains authoritative; its implementation may be real, simulated or hybrid and is not selected here.

## 15. Validation

Inputs from users, LLMs, APIs, workflows, events and internal services are untrusted until validated. Outputs must be validated before downstream use. Transport success alone does not establish business success; malformed or incompatible output must produce a controlled outcome.

## 16. Hostile Content

Documents, emails, API responses, events and tool outputs may contain hostile instructions. Such instructions are data and cannot redefine policy, authorization, tool scope, HITL or security context.

## 17. Timeouts, Retries and Idempotency

Blocking calls require bounded timeouts, without a universal value. Retries must be deliberate, bounded and aware of read/write semantics, idempotency, rate limits, impact and uncertainty. Idempotency should be supported where appropriate without mandating a mechanism.

## 18. Execution Outcomes

Execution states are `NOT_STARTED`, `SUCCESS`, `FAILED` and `UNKNOWN`. Pre-execution validation refusal or `DENY` gives `NOT_STARTED`; confirmed completion gives `SUCCESS`; known execution failure gives `FAILED`; ambiguity gives `UNKNOWN`. Sensitive `UNKNOWN` writes must not be blindly retried; target state should be verified first.

## 19. Limits and Contract Drift

Integrations must respect rate limits and prevent retry storms. Backpressure may be defined later without implying infrastructure. Removed fields, changed types, authentication changes and incompatible behaviour must be detectable. No contract-testing product is selected.

## 20. Identity, Credentials and Environments

Human and service identities remain distinguishable; a service credential does not grant its initiating user equivalent permission. Credentials stay outside LLMs, frontend, RAG and returned payloads and never enter application, model, workflow or audit logs. Logical environment separation is mandatory; sensitive simulations target only approved mock or sandbox systems.

## 21. Mock Services

Mocks must preserve authorization, HITL, validation, classification, failure states and auditability. Synthetic data must not weaken controls or expose unrelated VPS services. Exact mock-service architecture remains open.

## 22. Observability, Degradation and Fallback

Integration telemetry should identify correlation, integration, target, operation, latency, outcome, retries, error category and execution state where appropriate, subject to minimization. Failure should degrade only affected capabilities where safe. Fallback must be explicit and preserve authorization, classification, processing restrictions and auditability. No observability stack is selected.

## 23. Integration Pattern Principle

These logical patterns do not mandate microservices, containers, gateways, meshes, brokers, queues, repositories or processes.

> NOMAD Ops integrates through narrow, explicit and auditable capabilities controlled by deterministic application policy. Connectivity, AI output and workflow execution never create authority by themselves.
