# NOMAD Ops — Trust Boundaries

**Product:** NOMAD Ops  
**Organization:** Asteria Manufacturing Group  
**Spec:** 001-system-context  
**File:** `trust-boundaries.md`  
**Status:** APPROVED

---

## 1. Purpose

This document defines the trust boundaries that govern interactions between users, NOMAD Ops components, AI models, tools, workflows, external systems and business data.

Its purpose is to establish:

- which components may be trusted for which responsibilities;
- which components must never be treated as security authorities;
- how untrusted input is handled;
- where authorization decisions occur;
- how sensitive actions cross trust boundaries;
- how credentials and secrets are protected.

This document does not define the detailed technical implementation of authentication, network segmentation, encryption or secrets management.

---

## 2. Core Trust Principle

NOMAD Ops follows this principle:

> No component receives authority merely because it is inside the system.

Trust must be explicit, scoped and limited to a defined responsibility.

A component may be trusted for one purpose and untrusted for another.

Example:

An LLM may be trusted to generate a recommendation.

The same LLM must not be trusted to decide whether the user is authorized to execute that recommendation.

---

## 3. Trust Is Not Binary

NOMAD Ops must not model trust as simply:

- trusted;
- untrusted.

Trust is contextual.

Examples:

- the frontend may be trusted to display data but not to enforce authorization;
- a tool may be trusted to execute one defined operation but not arbitrary operations;
- n8n may be trusted to run an approved workflow but not to grant permissions;
- an LLM may be trusted for language reasoning but not for security decisions;
- an external API may be trusted as a source of specific business data but not as an instruction source.

---

## 4. Frontend Boundary

The web frontend is a user-interface layer.

It may:

- collect user input;
- display authorized data;
- request backend operations;
- present approval requests;
- display system state.

It must not be trusted to:

- enforce authorization;
- decide whether a user may access a resource;
- determine whether an action requires approval;
- store privileged secrets;
- bypass backend policy decisions.

Any permission or policy logic implemented in the frontend is considered usability logic only.

Security enforcement must occur server-side.

---

## 5. Backend Boundary

The NOMAD Ops backend is the primary enforcement boundary for platform behaviour.

It is responsible for coordinating:

- authentication context;
- authorization;
- data access;
- tool invocation;
- approval state;
- integration boundaries;
- audit events;
- policy enforcement.

The backend may rely on specialized internal services, but it remains responsible for ensuring that untrusted components cannot bypass security policy.

The backend must not blindly trust:

- frontend claims;
- LLM outputs;
- tool outputs;
- workflow results;
- external API responses;
- document instructions.

---

## 6. LLM Boundary

All LLMs must be treated as non-authoritative components.

An LLM may:

- reason over authorized context;
- classify information;
- summarize evidence;
- recommend actions;
- produce structured proposals;
- select from explicitly exposed tools where permitted by design.

An LLM must not be trusted to:

- authorize users;
- modify permissions;
- waive HITL requirements;
- determine final policy outcomes;
- access secrets directly;
- expand its own tool set;
- bypass scope restrictions;
- assume that external content is trustworthy.

LLM output must be treated as:

**proposal, inference or generated content**

unless independently validated by deterministic logic or authoritative data.

---

## 7. Prompt Injection Boundary

Documents, emails, API responses, retrieved text and other business content must be treated as potentially hostile input.

Content may include instructions such as:

- ignore previous instructions;
- disclose restricted information;
- call a tool;
- change permissions;
- execute a workflow;
- reveal secrets.

Such instructions are data, not system authority.

NOMAD Ops must not allow retrieved or external content to redefine:

- system instructions;
- authorization policy;
- tool permissions;
- HITL requirements;
- data-access scope;
- security constraints.

---

## 8. Tool Boundary

Tools are controlled capabilities exposed to NOMAD Ops.

Each tool must have a narrow and explicit contract defining:

- purpose;
- allowed operation;
- required inputs;
- permitted outputs;
- authorization requirements;
- risk level;
- audit requirements.

A tool must not provide broader capabilities than required for its intended use.

Example:

A tool for retrieving supplier approval status should not expose arbitrary ERP queries.

Tool access must follow least privilege.

---

## 9. Tool Output Is Not Automatically Trusted

A successful tool invocation does not mean the returned data is necessarily valid, complete or current.

Tool responses may be:

- stale;
- malformed;
- incomplete;
- inconsistent;
- unavailable;
- unexpected.

NOMAD Ops must validate tool outputs where appropriate before using them in subsequent operations.

A model must not transform an invalid tool response into an apparently successful result.

---

## 10. n8n Boundary

n8n is an orchestration engine, not a security authority.

n8n may execute explicitly approved workflows.

It must not independently decide:

- user authorization;
- security policy;
- access scope;
- whether HITL can be bypassed;
- whether a restricted action may proceed.

Before a protected workflow is triggered, required authorization and approval must already be established or explicitly enforced through an approved control point.

n8n credentials and workflow permissions must be limited to the operations required by each workflow.

---

## 11. External Systems Boundary

Connected systems such as ITSM, ERP, HR, plant operations, monitoring and email are separate trust domains.

NOMAD Ops must interact with them through controlled integration boundaries.

An external system may be authoritative for specific data while still being untrusted for:

- instructions;
- authorization decisions inside NOMAD Ops;
- security policy;
- tool selection.

Data from external systems must be validated according to its use.

---

## 12. Data Boundary

Authorization must be enforced before protected data crosses into:

- retrieval;
- LLM context;
- tool input;
- workflow input;
- frontend output.

NOMAD Ops must not retrieve restricted data first and attempt to hide it later.

This requirement applies across all trust boundaries.

---

## 13. Secret Boundary

Secrets must remain outside LLM and user-facing contexts.

Secrets include:

- passwords;
- API keys;
- tokens;
- private keys;
- privileged credentials;
- signing secrets;
- encryption secrets.

LLMs must not receive secret values.

Tools and services that require credentials must resolve them through an approved secret-handling mechanism outside the model context.

A model may receive a safe abstraction such as:

`credential_available = true`

but not the credential itself.

---

## 14. Service-to-Service Trust

Internal services must not assume that another service is trusted solely because both run inside the same infrastructure.

Service-to-service communication should be treated as a separate authorization boundary where risk justifies it.

Critical internal operations should require:

- authenticated service identity;
- scoped permissions;
- explicit allowed operations;
- auditability.

The detailed mechanism will be defined later.

---

## 15. Zero-Trust Internal Principle

NOMAD Ops adopts a practical zero-trust principle for sensitive operations:

> Internal network location does not equal authorization.

Running inside:

- the same VPS;
- the same Docker network;
- the same host;
- the same private subnet;

must not automatically grant unrestricted access.

---

## 16. Human Approval Boundary

Human-in-the-loop creates a formal trust boundary between proposal and execution.

For actions requiring approval:

**proposal  
→ authorization check  
→ approval request  
→ authorized human decision  
→ execution**

The execution must not occur before valid approval exists.

The LLM, frontend, tool or workflow must not be able to skip this boundary.

---

## 17. Approval Context Integrity

Approval requests must contain enough trustworthy context for the approver to make a meaningful decision.

The approver should be able to understand:

- what action is proposed;
- what resource is affected;
- why the action is proposed;
- expected impact;
- known risk;
- relevant evidence;
- whether the action is reversible.

Approval must not consist only of:

> “The AI recommends this. Approve?”

---

## 18. Simulated Systems Boundary

Simulated enterprise systems remain separate trust domains.

The fact that they are mock services must not allow NOMAD Ops to bypass:

- authorization;
- validation;
- error handling;
- approval;
- audit.

Mock systems exist to reproduce enterprise behaviour, not to remove enterprise controls.

---

## 19. Model Provider Boundary

External model providers are separate processing domains.

Sending data to a model provider must be governed by policy based on:

- data classification;
- provider approval;
- model approval;
- business purpose;
- minimum necessary context.

A model provider must never receive data merely because it improves answer quality.

---

## 20. Failure Across Trust Boundaries

When a component cannot confirm the result of an operation across a trust boundary, NOMAD Ops must not assume success.

Possible outcomes include:

- `SUCCESS`
- `FAILED`
- `UNKNOWN`

`UNKNOWN` must be treated as a legitimate state when execution cannot be verified.

The detailed behaviour is defined in `failure-model.md`.

---

## 21. Audit Across Trust Boundaries

Sensitive boundary crossings must be auditable where applicable.

Audit events may include:

- user request;
- authorization decision;
- retrieval decision;
- model invocation;
- tool invocation;
- workflow trigger;
- approval request;
- approval decision;
- external-system operation;
- execution result.

Audit data must itself respect data-classification and redaction requirements.

---

## 22. Trust Boundary Principle

The central principle is:

> NOMAD Ops must separate reasoning authority, security authority and execution authority.

An LLM may reason.

A policy layer authorizes.

A tool or workflow executes.

A human approves when risk requires it.

No single component should silently collapse all four responsibilities into one.
