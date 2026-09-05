# NOMAD Ops — Request Flow

**Product:** NOMAD Ops  
**Organization:** Asteria Manufacturing Group  
**Spec:** 002-architecture-foundation  
**File:** `request-flow.md`  
**Status:** APPROVED

---

## 1. Purpose

This document defines the conceptual lifecycle of a request inside NOMAD Ops.

Its purpose is to establish:

- how requests enter the platform;
- how identity and context are attached;
- when authorization is evaluated;
- how the platform selects the appropriate capability;
- where retrieval, LLM reasoning, tools, workflows and HITL may participate;
- how execution states are represented;
- how results are validated;
- how audit and observability are produced.

This document does not define:

- API endpoint structure;
- message formats;
- queue implementation;
- deployment topology;
- concrete framework behaviour;
- frontend interaction details.

---

## 2. Core Request-Flow Principle

A NOMAD Ops request must pass through controlled stages.

The platform must not allow an LLM, tool, workflow or frontend component to skip required:

- identity;
- authorization;
- policy;
- validation;
- approval;
- audit.

The general principle is:

> Every request follows the minimum safe path required to satisfy the business need.

---

## 3. Request Sources

Requests may originate from:

- a human user through the web interface;
- the global command bar;
- an approved internal service;
- an approved workflow;
- a scheduled process;
- an external integration;
- a future event-driven source.

The request source does not determine authorization by itself.

All protected requests must carry or resolve an appropriate identity and context.

---

## 4. Request Intake

When a request enters NOMAD Ops, the backend must establish a request context.

This context may include:

- request identifier;
- initiating identity;
- service identity where applicable;
- role;
- department;
- site;
- requested capability;
- target resource;
- relevant environment;
- correlation identifier.

The request must not proceed using unverified identity claims from the frontend.

---

## 5. Authentication

If the request requires an authenticated identity, authentication must be established before protected processing begins.

Authentication determines:

**Who or what is making the request?**

Authentication does not determine:

**What may that identity do?**

That decision belongs to authorization.

---

## 6. Context Resolution

After identity is known, NOMAD Ops resolves the minimum business context required for the request.

Context may include:

- assigned role;
- department;
- site;
- resource scope;
- data classification;
- action type;
- environment;
- business process;
- risk context.

Context resolution must follow data-minimization principles.

The platform must not automatically enrich every request with all available user or enterprise data.

---

## 7. Authorization Stage

Protected requests must pass through deterministic authorization.

Possible outcomes are:

- `ALLOW`
- `DENY`
- `REQUIRE_APPROVAL`

Authorization occurs before protected execution.

Where protected data retrieval is involved, authorization must also constrain the retrieval universe before restricted content is returned.

---

## 8. DENY Flow

If authorization returns:

`DENY`

then:

- execution must not begin;
- execution state remains `NOT_STARTED`;
- protected tools must not be invoked;
- protected workflows must not be triggered;
- protected data must not be retrieved;
- the denial must be auditable where appropriate.

The response should communicate the denial without exposing information the requester is not authorized to know.

---

## 9. Capability Selection

If the request is allowed to continue, the backend/orchestrator selects the least complex approved capability capable of satisfying the request.

Possible paths include:

- deterministic application logic;
- direct controlled integration;
- keyword or structured search;
- retrieval;
- RAG;
- LLM reasoning;
- tool execution;
- n8n workflow;
- human-only decision;
- combinations of the above.

An LLM must not be invoked merely because the platform has access to one.

---

## 10. Deterministic Request Path

A request that does not require AI should remain deterministic.

Example:

> Show open critical incidents for Plant 2.

Possible conceptual flow:

**Request  
→ Identity  
→ Context  
→ Authorization  
→ ITSM integration  
→ Output validation  
→ Response**

No LLM is required.

---

## 11. Retrieval-Only Path

Some requests may require evidence retrieval without generated reasoning.

Example:

> Show the current supplier onboarding procedure.

Possible flow:

**Request  
→ Identity  
→ Context  
→ Authorization  
→ Authorized retrieval  
→ Current-version validation  
→ Source presentation**

An LLM is optional and must not be added without a reason.

---

## 12. RAG Path

Where a user requests reasoning or natural-language synthesis over enterprise knowledge, the platform may use RAG.

Possible flow:

**Request  
→ Identity  
→ Context  
→ Authorization  
→ Restricted retrieval universe  
→ Evidence retrieval  
→ Evidence validation  
→ Approved LLM  
→ Structured or cited answer  
→ Output validation  
→ Response**

Only authorized evidence may enter model context.

---

## 13. LLM-Only Reasoning Path

An LLM may be used without RAG when the task requires reasoning or generation that does not depend on protected enterprise knowledge.

Examples may include:

- analyzing a user-described process;
- producing a structured proposal;
- classifying a non-sensitive input.

The business need must justify model use.

---

## 14. Tool Request Path

When a request requires interaction with another system, the backend may expose an approved narrow tool.

Conceptually:

**Request  
→ Authorization  
→ Tool selection  
→ Input validation  
→ Policy evaluation  
→ Tool invocation  
→ Output validation  
→ Execution state  
→ Audit  
→ Response**

The LLM may propose a tool invocation where permitted.

The LLM may propose:

```text
tool
arguments
```

> An LLM-generated tool call is a proposal, not an executable instruction.

Before execution, the backend must follow this conceptual flow:

```text
Receive proposal
→ Resolve approved tool
→ Validate tool existence
→ Validate arguments
→ Resolve authoritative resource identifiers
→ Evaluate authorization
→ Evaluate risk
→ Determine HITL requirement
→ Execute only if permitted
```

The backend must not trust model-supplied:

- tool names;
- resource identifiers;
- scopes;
- authorization claims;
- security context.

The LLM:

- cannot create a new capability by naming a non-existent tool;
- cannot widen the scope of a tool;
- cannot bypass policy by changing arguments;
- cannot authorize its own proposal.

The backend remains responsible for deciding whether the proposal may be executed.

---

## 15. REQUIRE_APPROVAL Flow

If policy returns:

`REQUIRE_APPROVAL`

then:

- execution state remains `NOT_STARTED`;
- an approval request is created;
- the proposed action must not execute yet.

The approval request must include sufficient context for the approver to understand:

- proposed action;
- target resource;
- reason;
- expected impact;
- known risk;
- relevant evidence where applicable;
- reversibility where applicable.

---

## 16. Approval Decision

An authorized approver may:

- approve;
- reject;
- allow the request to expire according to later policy.

### Approved

Human approval does not override authorization or freeze the authorization context.

After approval and before execution, NOMAD Ops must revalidate the relevant request context.

Conceptually:

```text
Request
→ Authorization
→ REQUIRE_APPROVAL
→ Human Approval
→ Revalidate Context + Authorization
→ Execution
```

Revalidation may include, where relevant:

- identity;
- authorization;
- role;
- scope;
- site;
- resource;
- action;
- classification;
- risk;
- environment;
- material input values.

Revalidation must evaluate both the current request context and whether the approval remains valid and bound to that exact context.

The revalidation outcome must be handled as follows:

- if authorization returns `ALLOW`, the request may proceed to execution when all other execution conditions remain valid;
- if authorization returns `DENY`, execution must remain `NOT_STARTED`;
- if authorization returns `REQUIRE_APPROVAL` and an existing approval remains valid for the unchanged action and context, that approval satisfies the approval gate and the request may proceed;
- if authorization returns `REQUIRE_APPROVAL` but approval is absent, expired, stale or no longer matches the action and context, execution must remain `NOT_STARTED` and a new approval is required.

A valid approval satisfies an approval requirement for its bound action and context; it does not change or replace the deterministic authorization decision.

Approval must not be treated as permanent or reusable authorization outside the action and context that were approved.

### Rejected

If rejected:

- execution must remain `NOT_STARTED`;
- the action must not execute.

### Stale Context

If relevant context changes materially after approval, the approval must not automatically remain valid.

Re-authorization or re-approval may be required.

---

## 17. Execution Stage

Execution occurs only after all required:

- identity checks;
- authorization;
- validation;
- approvals;
- post-approval context and authorization revalidation where HITL applies;

have completed successfully.

Execution may occur through:

- controlled application logic;
- Tool Gateway;
- approved n8n workflow;
- controlled enterprise integration.

Execution must never be performed directly by unrestricted LLM access.

---

## 18. Execution States

The execution lifecycle uses:

- `NOT_STARTED`
- `SUCCESS`
- `FAILED`
- `UNKNOWN`

### NOT_STARTED

No target execution has begun.

Typical causes:

- authorization denied;
- approval pending;
- approval rejected;
- validation failure before execution.

### SUCCESS

There is sufficient evidence that the intended operation completed.

### FAILED

Processing or execution began and the system can establish that it did not complete successfully.

### UNKNOWN

The action may have executed, but final state cannot be established reliably.

---

## 19. Execution Result Validation

A successful request transmission does not imply successful execution.

Before returning `SUCCESS`, NOMAD Ops must validate available evidence such as:

- confirmed API response;
- workflow completion state;
- returned resource identifier;
- verified target state;
- valid tool result.

An LLM statement that an action succeeded is not sufficient evidence.

---

## 20. UNKNOWN Handling

If an execution result becomes `UNKNOWN`, NOMAD Ops must preserve that state.

For sensitive state-changing actions:

- automatic blind retry is prohibited;
- target state should be verified where possible;
- retry must follow explicit policy.

The system must not convert uncertainty into a confident success or failure.

---

## 21. Failure Before Execution

Some failures occur before target execution begins.

Examples:

- invalid input;
- authentication failure;
- authorization denial;
- required approval missing;
- malformed request;
- policy violation.

These failures must not be confused with a failed target execution.

Where no execution began, execution state remains `NOT_STARTED`.

---

## 22. Partial Execution

Multi-step operations may produce mixed outcomes.

Where relevant, NOMAD Ops must preserve individual step states such as:

- completed;
- failed;
- skipped;
- pending;
- unknown.

The overall response must not hide partial failure behind a single successful status.

---

## 23. Dependency Degradation

If a dependency is unavailable, the request flow should determine whether the requested capability can continue without it.

Example:

If the LLM provider fails:

- deterministic queries may continue;
- AI synthesis may be unavailable.

If Qdrant fails:

- RAG may be unavailable;
- unrelated direct integrations may remain healthy.

Degradation must be explicit.

---

## 24. No Silent Fallback

The request flow must not silently switch:

- model provider;
- tool;
- workflow;
- data source;
- retrieval source;

unless an approved policy explicitly permits that fallback.

Any fallback must preserve:

- authorization;
- classification;
- security;
- processing restrictions.

---

## 25. Output Validation

Before returning a result to the requester, NOMAD Ops must validate outputs where required.

Validation may include:

- schema;
- source;
- authorization;
- evidence;
- execution status;
- version;
- data classification;
- required citations.

Invalid output must not be presented as successful merely because it was generated.

---

## 26. Response Construction

The final response should communicate the information relevant to the requester.

Depending on the request, it may include:

- requested result;
- evidence or sources;
- authorization outcome;
- approval status;
- execution result;
- uncertainty;
- degraded capability;
- next required action.

The response must not expose restricted internal diagnostic data to unauthorized users.

---

## 27. Audit and Observability

Relevant stages of a request should generate traceable operational events.

These may include:

- request received;
- authentication;
- authorization;
- capability selection;
- retrieval;
- model invocation;
- tool invocation;
- workflow execution;
- approval;
- execution outcome;
- failure;
- response.

The request should carry a correlation identifier where appropriate so that its lifecycle can be reconstructed.

---

## 28. Usage and Cost

Where a request consumes measurable resources, usage should remain associated with the request.

Examples:

- LLM tokens;
- model cost;
- embedding generation;
- workflow execution;
- retries;
- failed model calls.

A failed request may still have cost.

---

## 29. Request Flow Examples

### Example A — Deterministic Incident Query

Request:

> Show critical incidents from Plant 2.

Flow:

**User  
→ Authentication  
→ User context  
→ Authorization  
→ Controlled ITSM query  
→ Validate result  
→ Response**

AI usage:

**None**

---

### Example B — Enterprise Knowledge Question

Request:

> What is the current supplier onboarding procedure?

Flow:

**User  
→ Authentication  
→ Context  
→ Authorization  
→ Authorized retrieval  
→ Current-version filtering  
→ Evidence  
→ Optional LLM synthesis  
→ Citations  
→ Response**

AI usage:

**Optional**

---

### Example C — Incident Reasoning

Request:

> Compare this packaging outage with previous incidents and suggest the next step.

Flow:

**User  
→ Authentication  
→ Authorization  
→ Incident retrieval  
→ Historical incident retrieval  
→ Runbook retrieval  
→ Approved LLM reasoning  
→ Structured recommendation  
→ Evidence validation  
→ Response**

AI usage:

**Required by this capability**

---

### Example D — Sensitive Operational Action

Request:

> Restart the simulated packaging service.

Flow:

**User  
→ Authentication  
→ Context  
→ Authorization  
→ REQUIRE_APPROVAL  
→ Approval request  
→ Human approval  
→ Revalidate Context + Authorization  
→ Tool Gateway  
→ Sandbox execution  
→ Verify outcome  
→ Audit  
→ Response**

If verification is lost:

`UNKNOWN`

must be preserved.

---

## 30. Request Flow Principle

The central principle is:

> A NOMAD Ops request is controlled by deterministic application policy from entry to completion. AI may contribute reasoning, but it does not control identity, authorization, approval or execution.

Every request should take the simplest safe path capable of satisfying the business need.
