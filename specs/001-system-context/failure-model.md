# NOMAD Ops — Failure Model

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `failure-model.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines how NOMAD Ops represents, handles and communicates failures across models, tools, workflows, APIs, retrieval systems and enterprise integrations.

Its purpose is to establish:

- common execution states;
- behaviour for known failures;
- behaviour for uncertain outcomes;
- timeout handling;
- retry constraints;
- partial failure handling;
- degraded operation;
- user-facing error behaviour;
- audit and observability expectations.

This document does not define the detailed technical implementation of retries, queues, circuit breakers or monitoring infrastructure.

---

## 2. Core Failure Principle

NOMAD Ops must fail visibly, safely and traceably.

A failed dependency or uncertain operation must never be converted into an apparently successful result.

The platform must prefer an explicit limitation over fabricated continuity.

---

## 3. Primary Execution States

NOMAD Ops uses three primary execution states:

- `SUCCESS`
- `FAILED`
- `UNKNOWN`

These states describe what the platform knows about the result of an operation.

---

## 4. SUCCESS

`SUCCESS` means NOMAD Ops has sufficient evidence that the requested operation completed as expected.

Examples:

- an API returned a valid confirmed response;
- a workflow completed successfully;
- a tool returned a validated result;
- a retrieval operation returned authorized evidence;
- a ticket creation response confirms the new ticket identifier.

Success must not be inferred solely from:

- absence of an exception;
- an LLM claiming success;
- an ambiguous text response;
- a request being sent successfully.

---

## 5. FAILED

`FAILED` means NOMAD Ops has sufficient evidence that the operation did not complete successfully.

Examples:

- authentication rejected;
- authorization denied;
- API returned a known error;
- workflow execution failed;
- response failed schema validation;
- required dependency is unavailable;
- model invocation failed before producing a valid result.

Where possible, the failure reason should be captured explicitly.

---

## 6. UNKNOWN

`UNKNOWN` means NOMAD Ops cannot reliably determine whether an operation completed.

Typical examples:

- timeout after sending a write request;
- connection dropped after the target system may have received the action;
- workflow acknowledgement lost;
- external system returned an ambiguous or incomplete response.

`UNKNOWN` is not equivalent to `FAILED`.

The platform must not automatically repeat a sensitive operation simply because its result is unknown.

---

## 7. Unknown State Handling

When an operation becomes `UNKNOWN`, NOMAD Ops should attempt state verification where possible.

Example:

If a request to restart a simulated production service times out, NOMAD Ops should check the service state before retrying.

Possible resolution:

`UNKNOWN`
→ state check
→ `SUCCESS`

or:

`UNKNOWN`
→ state check
→ `FAILED`

or:

`UNKNOWN`
→ state cannot be verified
→ remain `UNKNOWN`

---

## 8. Timeout Behaviour

Every remote or cross-service operation must have a defined timeout.

Timeouts must not result in indefinite waiting.

A timeout may produce:

- `FAILED`, when it is known the operation did not execute;
- `UNKNOWN`, when execution may have occurred but confirmation was not received.

Timeouts must be observable and auditable.

---

## 9. Retry Principle

Retries must be deliberate.

The system must consider:

- whether the operation is read-only;
- whether it is idempotent;
- whether it changes business state;
- whether it is financially significant;
- whether it is operationally sensitive.

Retries must not be used simply to hide instability.

---

## 10. Safe Retry Examples

Controlled retries may be appropriate for:

- read-only API requests;
- transient retrieval failures;
- temporary rate-limit responses with approved backoff;
- idempotent operations with a stable request identifier.

Retry count and backoff policy must be bounded.

---

## 11. Unsafe Retry Examples

Automatic retry should normally be avoided for:

- payment actions;
- irreversible business updates;
- non-idempotent ticket creation;
- production-impacting actions;
- approval decisions;
- destructive operations.

Where retry is required, the target state should be verified first where possible.

---

## 12. Partial Failure

A workflow may complete only some of its steps.

Example:

1. retrieve supplier;
2. create onboarding record;
3. notify Procurement;
4. update ERP note.

If steps 1–3 succeed and step 4 fails, the overall result must not be reported simply as `SUCCESS`.

The system must expose:

- which steps succeeded;
- which step failed;
- what state remains;
- whether compensation or manual intervention is required.

---

## 13. Partial Success Must Be Visible

NOMAD Ops must not collapse multi-step outcomes into a misleading binary result.

Where relevant, the platform should represent:

- completed steps;
- failed steps;
- skipped steps;
- pending steps;
- unknown steps.

This is especially important for workflows executed through n8n or external orchestration.

---

## 14. Dependency Failure

When a dependency fails, NOMAD Ops must identify the affected capability.

Examples:

- ITSM unavailable;
- ERP unavailable;
- Qdrant unavailable;
- LLM provider unavailable;
- n8n unavailable;
- monitoring API unavailable.

The platform must distinguish between:

- platform-wide failure;
- capability-specific failure;
- degraded functionality.

---

## 15. Degraded Operation

A dependency failure does not always require the entire platform to fail.

Example:

If the LLM provider is unavailable:

- deterministic incident filtering may still work;
- existing dashboard data may still display;
- authorized document search may still function without generated answers.

If Qdrant is unavailable:

- NOMAD Ops must not pretend RAG evidence exists;
- unrelated deterministic functions may remain operational.

Degradation must be explicit.

---

## 16. No Silent Fallback

Fallback behaviour must be predefined.

The platform must not silently switch:

- LLM provider;
- model;
- retrieval source;
- workflow;
- data source;

unless policy explicitly allows it.

Fallback must preserve:

- authorization;
- data classification;
- security;
- expected quality constraints.

---

## 17. LLM Failure

LLM failures may include:

- provider unavailable;
- timeout;
- rate limit;
- invalid response;
- malformed structured output;
- policy rejection;
- context limit exceeded.

When the LLM fails:

- the failure must be visible;
- no model-generated result should be fabricated;
- deterministic capabilities should continue where possible;
- fallback may be used only if explicitly authorized.

---

## 18. Invalid LLM Output

A successful provider response does not automatically mean the model output is usable.

Examples:

- invalid JSON;
- missing required fields;
- unsupported tool request;
- response contradicts structured evidence;
- output violates expected schema.

Invalid LLM output must be treated as a controlled failure or validation error.

---

## 19. Retrieval Failure

Retrieval failures may include:

- Qdrant unavailable;
- no authorized documents found;
- index unavailable;
- metadata inconsistency;
- retrieval timeout;
- stale index detected.

“No evidence found” is not necessarily a system failure.

It may be a valid outcome.

NOMAD Ops must distinguish:

- retrieval system failed;
- retrieval succeeded but found no evidence.

---

## 20. No Evidence Behaviour

When retrieval succeeds but evidence is insufficient, NOMAD Ops should respond with uncertainty or abstention.

It must not generate an unsupported answer merely to avoid an empty result.

Valid output may include:

- insufficient evidence;
- no authorized source found;
- current documentation unavailable;
- escalation required.

---

## 21. Tool Failure

Tool failures may include:

- invalid input;
- denied authorization;
- target unavailable;
- schema mismatch;
- timeout;
- execution failure;
- unexpected output.

The model must not reinterpret a failed tool call as success.

---

## 22. n8n Workflow Failure

n8n workflow outcomes must be visible to NOMAD Ops.

Relevant information may include:

- workflow identifier;
- execution identifier;
- status;
- failed step;
- error;
- retry state;
- start time;
- completion time.

A failed workflow must not be represented as successfully completed.

---

## 23. External API Failure

External API failures must preserve the original failure category where possible.

Examples:

- `401/403` → authentication or authorization failure;
- `404` → expected resource unavailable;
- `409` → state conflict;
- `429` → rate limit;
- `5xx` → dependency/server failure.

NOMAD Ops should not collapse all failures into a generic “AI error”.

---

## 24. Contract Failure

If an API or tool response no longer matches its expected contract, NOMAD Ops must treat this as an integration failure.

Examples:

- missing required field;
- renamed field;
- changed type;
- invalid enum;
- incompatible schema.

Contract failures must be observable because they may indicate version drift.

---

## 25. Authentication and Authorization Failure

Security failures must not be hidden or automatically bypassed.

Possible outcomes include:

- `DENIED`
- authentication required;
- approval required;
- insufficient scope.

The system must never respond to authorization failure by attempting another path that grants broader access unless explicitly designed and authorized.

---

## 26. Human Approval Failure

An approval process may fail because:

- no authorized approver exists;
- approval expires;
- approver rejects;
- approval service unavailable;
- approval context becomes stale.

In those cases, the sensitive action must not proceed.

---

## 27. Stale Approval

Approval must apply to a defined action and context.

If relevant context changes after approval, the platform may require re-approval.

Examples:

- target resource changed;
- proposed action changed;
- risk level changed;
- underlying incident changed materially.

An old approval must not become a blanket permission.

---

## 28. User-Facing Failure Behaviour

Users should receive clear failure information appropriate to their role.

A useful error should communicate:

- what failed;
- what capability is affected;
- whether anything was executed;
- whether retry is safe;
- whether human intervention is required.

The interface should avoid technical noise where it does not help the user.

---

## 29. Internal Diagnostic Detail

Detailed diagnostics may include:

- dependency;
- error code;
- exception class;
- latency;
- retry count;
- request reference;
- workflow execution ID;
- model/provider;
- validation error.

Diagnostic detail must not expose secrets or protected data.

---

## 30. Error Correlation

Failures should carry a correlation or trace identifier where appropriate.

This identifier allows the same operation to be traced across:

- frontend;
- backend;
- LLM;
- tool;
- n8n;
- API;
- database;
- audit log.

The detailed tracing implementation will be defined later.

---

## 31. Failure Auditability

Relevant failures must be recorded with enough information to understand:

- what operation was attempted;
- who initiated it;
- which dependency failed;
- execution state;
- whether retries occurred;
- whether approval existed;
- whether any side effect may have happened.

Audit logs must respect data-classification requirements.

---

## 32. Failure and Cost

Failed operations may still consume resources.

NOMAD Ops must eventually be able to attribute cost to:

- failed model calls;
- retries;
- failed workflows;
- duplicate attempts;
- fallback processing.

Failure cost is part of operational cost.

---

## 33. Failure Trend Detection

Observability should eventually allow detection of patterns such as:

- rising model error rate;
- repeated tool failures;
- repeated workflow failures;
- increased timeout rate;
- API contract drift;
- dependency degradation.

A single failure and a systemic failure are not the same operational problem.

---

## 34. Failure Model Principle

The central principle is:

> NOMAD Ops must never hide uncertainty or dependency failure behind a confident-looking result.

When the system knows, it should say what happened.

When it knows something failed, it should say it failed.

When it cannot know, it should say `UNKNOWN`.
