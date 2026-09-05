# NOMAD Ops — System Context Acceptance Criteria

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `acceptance.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines the mandatory acceptance criteria for `001-system-context`.

It validates conformance with the approved:

- system context;
- actor model;
- enterprise systems;
- data classification;
- trust boundaries;
- integration constraints;
- failure model;
- Codex constraints;
- environment and identity constraints.

These criteria define expected behaviour and boundaries.

They do not define detailed implementation architecture.

---

## 2. Requirement Level

All acceptance criteria in this document are mandatory.

`AC-001` through `AC-067` are `MUST` requirements unless a later approved specification explicitly replaces or refines the criterion.

A later module specification may define more precise test conditions, but it must not silently weaken these requirements.

Any intentional exception requires an approved decision record or SPEC change.

---

## 3. Authorization and Execution Are Separate State Machines

NOMAD Ops must maintain a strict distinction between authorization decisions and execution states.

### Authorization Decision

A request requiring authorization must resolve to one of:

- `ALLOW`
- `DENY`
- `REQUIRE_APPROVAL`

### Execution State

An operation capable of execution must use one of:

- `NOT_STARTED`
- `SUCCESS`
- `FAILED`
- `UNKNOWN`

Authorization and execution must not be collapsed into one status.

Example:

**Authorization:** `DENY`
**Execution:** `NOT_STARTED`

A denied operation is not an execution failure because execution never began.

---

# ACTORS AND AUTHORIZATION

## AC-001 — Role Does Not Grant Global Access

**GIVEN**
a user has an assigned business role

**WHEN**
the user requests a resource outside their authorized department, site or scope

**THEN**
authorization must return `DENY`

**AND**
the role alone must not provide access.

---

## AC-002 — Site Scope Is Enforced

**GIVEN**
a Plant Operations Manager is assigned only to Plant 2

**WHEN**
the user requests a Plant 1 restricted operational resource

**THEN**
authorization must return `DENY`

**UNLESS**
explicit Plant 1 scope exists.

---

## AC-003 — Admin Does Not Automatically Access Business Data

**GIVEN**
a NOMAD Ops Admin lacks business-data authorization for a protected resource

**WHEN**
the administrator requests that resource

**THEN**
platform administration privileges must not grant access.

---

## AC-004 — Authentication and Authorization Are Separate

**GIVEN**
a user is successfully authenticated

**WHEN**
the user requests a protected resource or action

**THEN**
authorization must still be evaluated independently.

---

## AC-005 — Human and Service Identities Are Distinguishable

**GIVEN**
a human initiates an operation that is executed by an internal service

**WHEN**
the operation is audited

**THEN**
the audit trail must identify both:

- initiating human identity;
- executing service identity.

---

## AC-006 — Service-to-Service Operations Are Scoped

**GIVEN**
an internal service calls another protected NOMAD Ops service

**WHEN**
the request crosses a protected service boundary

**THEN**
the caller must use an identifiable service identity

**AND**
the operation must be restricted to explicitly permitted capabilities.

---

# DATA ACCESS AND CLASSIFICATION

## AC-007 — Authorization Happens Before Protected Retrieval

**GIVEN**
potential retrieval results include content outside the user's authorized scope

**WHEN**
retrieval is performed

**THEN**
the search universe must be restricted before protected content is returned.

---

## AC-008 — Vector Similarity Cannot Override Authorization

**GIVEN**
a document is highly relevant semantically

**AND**
the user lacks access to it

**WHEN**
vector search runs

**THEN**
that document must not be returned to the user or LLM.

---

## AC-009 — Unknown Classification Is Restricted

**GIVEN**
a resource may contain protected information

**AND**
its classification is unknown

**WHEN**
processing is requested

**THEN**
the system must restrict processing until classification is resolved.

---

## AC-010 — Critical Secrets Do Not Enter LLM Context

**GIVEN**
an operation requires a credential

**WHEN**
an LLM participates

**THEN**
the secret value must not enter model context.

---

## AC-011 — Critical Secrets Do Not Enter RAG

**GIVEN**
content contains credentials or equivalent `CRITICAL` secrets

**WHEN**
knowledge indexing occurs

**THEN**
those secret values must not be embedded or indexed for semantic retrieval.

---

## AC-012 — Critical Secrets Do Not Enter Logs

**GIVEN**
an operation uses a secret

**WHEN**
logging occurs

**THEN**
the secret value must not appear in application, model, workflow or audit logs.

---

## AC-013 — Data Sent to Models Is Minimized

**GIVEN**
a model requires business context to perform an approved task

**WHEN**
context is assembled

**THEN**
only the minimum data required for that task may be provided.

---

## AC-014 — Data Sent to Tools Is Minimized

**GIVEN**
a tool requires specific information to execute its capability

**WHEN**
the tool is invoked

**THEN**
it must receive only the data necessary for that defined operation.

---

## AC-015 — Derived Data Retains Appropriate Classification

**GIVEN**
output is derived from protected information

**WHEN**
the output is stored, logged, retrieved or displayed

**THEN**
its classification must not automatically be lowered merely because the data was summarized, transformed or embedded.

---

## AC-016 — Logs Respect Classification

**GIVEN**
an operation processes protected information

**WHEN**
logging occurs

**THEN**
redaction and handling must respect the information's classification.

---

# AI AUTHORITY

## AC-017 — LLM Cannot Authorize

**GIVEN**
an LLM recommends an operation

**WHEN**
authorization is required

**THEN**
the final decision must come from deterministic policy logic.

---

## AC-018 — LLM Cannot Waive HITL

**GIVEN**
policy requires human approval

**WHEN**
the LLM considers the action safe, urgent or beneficial

**THEN**
the approval requirement must remain unchanged.

---

## AC-019 — AI Cannot Expand Data Scope

**GIVEN**
an LLM determines that inaccessible information would improve its answer

**WHEN**
the user lacks authorization for that information

**THEN**
the information must not be retrieved or supplied to the model.

---

## AC-020 — Retrieved Instructions Are Not System Authority

**GIVEN**
email, documents, API output or retrieved content contains instructions that conflict with NOMAD Ops policy

**WHEN**
that content is processed

**THEN**
those instructions must be treated as untrusted data

**AND**
must not alter:

- authorization;
- system instructions;
- HITL requirements;
- tool permissions;
- data scope.

---

# HUMAN-IN-THE-LOOP

## AC-021 — Sensitive Action Requires Approval

**GIVEN**
authorization returns `REQUIRE_APPROVAL`

**WHEN**
no valid approval exists

**THEN**
execution state must remain `NOT_STARTED`.

---

## AC-022 — Approval Is Action-Specific

**GIVEN**
approval exists for a specific action, target and context

**WHEN**
the target, action or relevant risk context changes materially

**THEN**
the prior approval must not authorize the modified operation.

---

## AC-023 — Approval Contains Sufficient Context

**GIVEN**
a human must approve a sensitive action

**WHEN**
the approval request is presented

**THEN**
it must include at minimum:

- proposed action;
- affected resource;
- reason;
- expected impact;
- known risk.

**AND**, when applicable:

- evidence;
- reversibility or rollback information.

---

## AC-024 — Rejected Approval Does Not Become FAILED Execution

**GIVEN**
an approver rejects an action

**WHEN**
the authorization flow completes

**THEN**
the action must remain unexecuted

**AND**
execution state must remain `NOT_STARTED`.

---

# TOOLS AND INTEGRATIONS

## AC-025 — Tools Are Narrowly Scoped

**GIVEN**
a business capability requires a specific operation

**WHEN**
a tool is exposed

**THEN**
the tool must expose only the approved capability and required data scope.

---

## AC-026 — Read Does Not Imply Write

**GIVEN**
a user or tool has read authorization

**WHEN**
a state-changing operation is requested

**THEN**
write authorization must be evaluated independently.

---

## AC-027 — LLM Has No Unrestricted Database Access

**GIVEN**
an LLM requires data stored in PostgreSQL

**WHEN**
the information is requested

**THEN**
access must occur through controlled application logic or approved narrow tools

**AND**
arbitrary SQL execution must not be available by default.

---

## AC-028 — LLM Has No Unrestricted n8n Access

**GIVEN**
an LLM needs automation

**WHEN**
n8n is involved

**THEN**
only explicitly approved workflow capabilities may be exposed.

---

## AC-029 — Integration Inputs Are Validated

**GIVEN**
an integration receives input

**WHEN**
required types, identifiers, structure or allowed values are invalid

**THEN**
execution must not start.

---

## AC-030 — Integration Outputs Are Validated

**GIVEN**
an integration returns output outside its expected contract

**WHEN**
NOMAD Ops receives it

**THEN**
the result must be treated as an integration failure.

---

## AC-031 — Contract Drift Is Detectable

**GIVEN**
a dependency changes required fields, types or response structure

**WHEN**
the incompatible response is received

**THEN**
the contract mismatch must be detectable and observable.

---

## AC-032 — Every Remote Operation Has a Timeout

**GIVEN**
NOMAD Ops calls a remote or cross-service dependency

**WHEN**
the dependency does not respond within the configured limit

**THEN**
the operation must terminate its wait

**AND**
the timeout must produce an explicit execution outcome.

---

## AC-033 — Timeouts Are Observable

**GIVEN**
an operation times out

**WHEN**
operational telemetry or diagnostics are inspected

**THEN**
the timeout must be identifiable as such.

---

## AC-034 — Retry Count Is Bounded

**GIVEN**
an operation has an approved retry policy

**WHEN**
retries occur

**THEN**
the number of automatic attempts must have an explicit maximum.

---

## AC-035 — Rate Limits Do Not Cause Retry Storms

**GIVEN**
a dependency returns a rate-limit response

**WHEN**
retry behaviour applies

**THEN**
NOMAD Ops must use an explicitly bounded retry/backoff policy

**AND**
must not generate uncontrolled repeated requests.

---

## AC-036 — Idempotent Operations Prevent Duplicate Effects

**GIVEN**
an operation is defined as idempotent

**WHEN**
the same request is safely repeated

**THEN**
it must not create duplicate business effects.

---

## AC-037 — Non-Idempotent Sensitive Operations Are Not Blindly Retried

**GIVEN**
a sensitive operation is not guaranteed to be idempotent

**WHEN**
its result cannot be confirmed

**THEN**
automatic repetition must not occur without state verification or explicit policy.

---

# EXECUTION AND FAILURE

## AC-038 — DENY Prevents Execution

**GIVEN**
authorization returns `DENY`

**WHEN**
the request is processed

**THEN**
execution state must remain `NOT_STARTED`

**AND**
no target action may be attempted.

---

## AC-039 — SUCCESS Requires Evidence

**GIVEN**
an operation is reported as `SUCCESS`

**THEN**
the platform must possess sufficient evidence that the intended operation completed.

---

## AC-040 — FAILED Means Execution Was Attempted or Processing Definitively Failed

**GIVEN**
processing or execution begins

**AND**
the platform can establish that it did not complete successfully

**WHEN**
the outcome is recorded

**THEN**
execution state must be `FAILED`.

---

## AC-041 — UNKNOWN Is Preserved

**GIVEN**
an action may have reached its target

**AND**
the final result cannot be established

**WHEN**
the outcome is recorded

**THEN**
execution state must be `UNKNOWN`.

---

## AC-042 — UNKNOWN Is Not Automatically Retried

**GIVEN**
a sensitive state-changing operation has execution state `UNKNOWN`

**WHEN**
automatic retry is considered

**THEN**
automatic retry must be blocked until the operation is proven safe to repeat under its defined retry policy.

---

## AC-043 — Partial Failure Is Visible

**GIVEN**
a multi-step process completes only some steps

**WHEN**
its result is reported

**THEN**
the platform must expose the state of relevant individual steps

**AND**
must not represent the entire process simply as successful.

---

## AC-044 — Dependency Failure Is Capability-Specific

**GIVEN**
one NOMAD Ops dependency fails

**WHEN**
other independent capabilities remain healthy

**THEN**
unrelated capabilities must not be marked unavailable solely because of that failure.

---

## AC-045 — No Silent Fallback

**GIVEN**
a configured dependency fails

**WHEN**
an alternative exists

**THEN**
the system must not switch automatically unless that fallback is explicitly approved by policy.

---

## AC-046 — Retrieval Failure and No Evidence Are Different

**GIVEN**
a knowledge request is processed

**WHEN**
retrieval succeeds but finds no sufficient evidence

**THEN**
the outcome must be distinguishable from retrieval-system failure.

---

## AC-047 — Insufficient Evidence Causes Abstention

**GIVEN**
retrieval provides insufficient authorized evidence

**WHEN**
a generated answer is requested

**THEN**
NOMAD Ops must communicate insufficient evidence or abstain from answering.

---

# PROVIDER GOVERNANCE

## AC-048 — Provider Fallback Respects Classification

**GIVEN**
the preferred AI provider is unavailable

**AND**
the request contains restricted information

**WHEN**
fallback is considered

**THEN**
the data must not be sent to a provider unauthorized for that classification.

---

## AC-049 — External Processing Can Be Prohibited

**GIVEN**
policy prohibits external AI processing for a data category

**WHEN**
AI processing is requested

**THEN**
NOMAD Ops must use an approved processing option or refuse the operation.

---

## AC-050 — Provider Policy Can Consider Residency and Retention

**GIVEN**
a model provider is evaluated for protected data

**WHEN**
processing eligibility is determined

**THEN**
policy must be capable of considering:

- processing location;
- retention;
- provider logging;
- training usage;
- contractual restrictions.

---

# DOCUMENT AND KNOWLEDGE INTEGRITY

## AC-051 — Superseded Documents Are Not Treated as Current

**GIVEN**
multiple versions of a controlled document exist

**AND**
one version is marked superseded or obsolete

**WHEN**
NOMAD Ops answers a question requiring the current procedure

**THEN**
the obsolete version must not be presented as the current authoritative procedure.

---

## AC-052 — Source Version Is Traceable

**GIVEN**
a controlled document contributes evidence to an answer

**WHEN**
the evidence is presented

**THEN**
the source and relevant document version must be identifiable.

---

# SIMULATION AND ENVIRONMENTS

## AC-053 — Sensitive Demo Actions Stay in Sandbox

**GIVEN**
a demonstration includes a high-risk or production-like action

**WHEN**
execution occurs

**THEN**
the target must be an approved mock, sandbox or synthetic system.

---

## AC-054 — Demo Actions Cannot Impact Unrelated Real VPS Services

**GIVEN**
a simulated sensitive action is executed

**WHEN**
the target is resolved

**THEN**
the operation must not be capable of modifying unrelated production services hosted on the VPS.

---

## AC-055 — Simulated Systems Preserve Enterprise Controls

**GIVEN**
the target enterprise system is simulated

**WHEN**
NOMAD Ops interacts with it

**THEN**
authorization, validation, audit, failure handling and HITL rules must still apply.

---

## AC-056 — Synthetic Cross-System Data Is Coherent

**GIVEN**
an entity appears in more than one simulated enterprise system

**WHEN**
the records are correlated

**THEN**
their identifiers and relationships must resolve coherently within the Asteria synthetic enterprise model.

---

## AC-057 — System-of-Record Ownership Is Preserved

**GIVEN**
business information originates from an authoritative enterprise system

**WHEN**
NOMAD Ops stores a reference, cache, index or derived representation

**THEN**
the authoritative ownership must remain associated with the original system.

---

# OBSERVABILITY AND COST

## AC-058 — Relevant Failures Are Traceable

**GIVEN**
an operationally relevant failure occurs

**WHEN**
the event is investigated

**THEN**
the platform must provide sufficient correlation information to identify the affected operation and dependency.

---

## AC-059 — Diagnostic Information Does Not Expose Secrets

**GIVEN**
diagnostic information is recorded for a failure

**WHEN**
logs or traces are inspected

**THEN**
protected secret values must not be present.

---

## AC-060 — Failed AI Operations Retain Usage Accounting

**GIVEN**
a model invocation consumes billable or measurable resources

**AND**
the operation ultimately fails

**WHEN**
usage accounting is performed

**THEN**
that consumption must remain associated with the operation rather than being discarded because it failed.

Detailed cost aggregation will be specified in the Cost Management module.

---

# DEVELOPMENT GOVERNANCE

## AC-061 — Local Identity Does Not Define Authorization Logic

**GIVEN**
V1 uses local authentication

**WHEN**
authorization is evaluated

**THEN**
business permission logic must remain independent of the local identity mechanism.

---

## AC-062 — Future IdP Replacement Does Not Redefine Business Permissions

**GIVEN**
a future external identity provider replaces local authentication

**WHEN**
business authorization is evaluated

**THEN**
existing role, scope and policy semantics must remain conceptually independent from the identity provider.

---

## AC-063 — Codex Follows Approved SPECs

**GIVEN**
Codex receives an implementation task

**WHEN**
the task conflicts with an approved SPEC

**THEN**
Codex must stop and report the conflict before implementation

**AND**
must not silently override either the approved SPEC or the requested task.

---

## AC-064 — Codex Stops on Product Ambiguity

**GIVEN**
an ambiguity affects:

- behaviour;
- permissions;
- security;
- data handling;
- HITL;
- architecture;
- acceptance criteria;

**WHEN**
Codex encounters it

**THEN**
Codex must stop and report the required decision.

---

## AC-065 — Protected Infrastructure Requires Explicit Authorization

**GIVEN**
a Codex task does not explicitly authorize infrastructure modification

**WHEN**
implementation would require changes to Docker, `docker-compose.yml`, Traefik or n8n

**THEN**
Codex must stop and report the required change before modifying it.

---

## AC-066 — New Dependencies Require Authorization

**GIVEN**
Codex determines that implementation requires a dependency not already approved for the task

**WHEN**
the dependency would need to be installed or upgraded

**THEN**
Codex must report the requirement before changing dependencies.

---

## AC-067 — Implementation Requires Validation Against SPEC

**GIVEN**
a future feature has been implemented

**WHEN**
the work is reported as complete

**THEN**
relevant acceptance criteria must have been evaluated

**AND**
unmet criteria must be reported.

---

## 4. Acceptance Completion

`001-system-context` is accepted only when:

- all acceptance criteria in this document are treated as mandatory;
- future module specifications remain compatible with these constraints;
- applicable criteria can be traced to implementation tests or explicit validation procedures;
- any deliberate exception is documented through an approved SPEC change or decision record.

A criterion may be refined into more specific module-level tests later.

Refinement must not silently weaken the requirement.

---

## 5. Final Acceptance Principle

> NOMAD Ops is not accepted merely because it produces the expected output.

It is accepted only when that output is produced within the approved boundaries for:

- identity;
- authorization;
- data;
- AI authority;
- human control;
- integrations;
- execution;
- failure;
- environments;
- governance;
- observability.

Correct output produced through an unauthorized or unsafe path is still incorrect system behaviour.
