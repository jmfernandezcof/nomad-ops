# NOMAD Ops — Data Classification

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `data-classification.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines how NOMAD Ops classifies and handles business data according to sensitivity.

Its purpose is to establish:

- data-classification levels;
- examples of information belonging to each level;
- rules for access;
- rules for retrieval and RAG;
- rules for LLM processing;
- logging and redaction requirements;
- restrictions on tools and integrations;
- principles for permission-aware retrieval.

This document does not define the technical implementation of encryption, storage, identity or policy enforcement.

---

## 2. Classification Model

NOMAD Ops uses four data-classification levels:

1. `INTERNAL`
2. `CONFIDENTIAL`
3. `SENSITIVE`
4. `CRITICAL`

Classification affects:

- who may access the information;
- whether it may be indexed;
- whether it may be retrieved;
- whether it may be processed by an LLM;
- which model or provider may process it;
- what information may appear in logs;
- which tools may receive it;
- whether masking or redaction is required.

Classification does not replace authorization.

A user must satisfy both:

- the authorization policy;
- the handling rules associated with the data classification.

---

# 3. INTERNAL

## Definition

Business information intended for use inside Asteria but whose disclosure would not normally create significant operational, financial, legal or privacy impact.

## Examples

May include:

- general internal procedures;
- standard employee guidance;
- general IT documentation;
- non-sensitive runbooks;
- corporate announcements;
- common operational manuals;
- non-sensitive training material.

## Access

May be accessible to authenticated users where role, department and site policy allow it.

`INTERNAL` does not mean universally accessible.

## RAG

May be indexed and used for retrieval when authorized.

## LLM Processing

May be processed by approved LLM providers where the use case permits.

## Logging

Relevant operational metadata may be logged.

Full content should only be logged when explicitly necessary.

---

# 4. CONFIDENTIAL

## Definition

Business information whose unauthorized disclosure could create meaningful commercial, financial or operational impact.

## Examples

May include:

- supplier contracts;
- procurement records;
- internal financial reports;
- project documentation;
- commercial proposals;
- supplier performance information;
- internal business analysis;
- selected operational reports.

## Access

Requires explicit role, department, site or resource authorization.

## RAG

May be indexed only when:

- access controls can be preserved;
- document ownership and sensitivity metadata are available;
- retrieval can enforce authorization before content is returned.

## LLM Processing

May be processed only by approved models/providers and only when:

- the user is authorized;
- the use case requires the information;
- the minimum necessary data is provided.

## Logging

Logs should prefer metadata over raw business content.

Confidential content should be redacted or omitted when it is not required for auditability.

---

# 5. SENSITIVE

## Definition

Information whose unauthorized disclosure could cause significant privacy, legal, compliance, financial or security impact.

## Examples

May include:

- personal employee information;
- restricted HR records;
- selected payroll-related information;
- legal or compliance-sensitive records;
- sensitive financial information;
- security-relevant operational data;
- protected personal identifiers.

## Access

Must be explicitly restricted.

Authorization should consider:

- role;
- department;
- site;
- purpose;
- resource;
- action.

Access must follow least-privilege and data-minimization principles.

## RAG

Sensitive content must not be placed into a general-purpose knowledge index.

If retrieval is required, it must use an access-controlled retrieval context specifically designed for the permitted scope.

## LLM Processing

Sensitive information may only be processed when:

- the business requirement clearly justifies it;
- the requesting user is authorized;
- the chosen model/provider is approved for that sensitivity;
- unnecessary fields are removed or masked where possible.

## Logging

Raw sensitive content must not be logged by default.

Logs should use:

- identifiers;
- hashes;
- metadata;
- redacted values;

where those are sufficient for traceability.

---

# 6. CRITICAL

## Definition

Information whose exposure or misuse could directly compromise systems, security controls, production operations or highly protected business assets.

## Examples

May include:

- passwords;
- API keys;
- authentication tokens;
- private keys;
- encryption secrets;
- privileged credentials;
- highly sensitive security configuration;
- secrets capable of granting system access;
- information specifically capable of enabling critical production actions.

## Access

Access must be extremely limited and explicitly justified.

## RAG

Critical data must not be indexed into the general RAG system.

Secrets and credentials must never be embedded for semantic retrieval.

## LLM Processing

Critical secrets must not be provided to LLMs.

A model should receive only the minimum abstracted information required to reason about a task.

Example:

Instead of providing an API key, a model may receive:

`credential_available = true`

The controlled tool layer is responsible for using the actual credential.

## Logging

Critical secrets must never appear in application, model, workflow or audit logs.

Where required for observability, logs must record only safe metadata such as:

- secret identifier;
- credential reference;
- operation type;
- outcome.

Never the secret value.

---

# 7. Classification and Authorization

Data classification and user authorization are independent controls.

Example:

A user may hold the role:

`IT Operator`

but that role alone does not provide access to every `SENSITIVE` IT resource.

Similarly, a `Department Manager` does not automatically gain access to all `CONFIDENTIAL` information.

The platform must evaluate:

**User context + resource scope + requested action + data classification**

before access is granted.

---

# 8. Authorization Before Retrieval

NOMAD Ops must enforce authorization before protected content is retrieved.

The platform must not:

1. retrieve all semantically relevant documents;
2. expose them to an LLM;
3. remove unauthorized documents afterward.

The required conceptual flow is:

**User request
→ identify authorization context
→ determine accessible resource universe
→ perform retrieval only within that permitted universe
→ return authorized evidence**

This applies to:

- keyword search;
- vector search;
- RAG;
- document retrieval;
- incident history;
- cross-system context retrieval.

---

# 9. AI Cannot Expand Data Access

An LLM or agent must not expand the data available to a user.

If the model determines that additional information would be useful but the user is not authorized to access it, the correct outcome is:

- continue without that information;
- explain that required information is unavailable where appropriate;
- or request an authorized escalation.

The system must never grant additional access because the model considers it necessary.

---

# 10. Data Minimization

NOMAD Ops must provide models, tools and workflows only with the information required for the current task.

Example:

If a workflow needs:

- employee ID;
- department;
- manager;

it should not automatically retrieve the employee's full HR record.

The same principle applies to prompts.

---

# 11. Redaction and Masking

Sensitive information should be masked or redacted where full values are unnecessary.

Examples may include:

- personal identifiers;
- financial account information;
- email addresses;
- internal identifiers;
- security-related fields.

Redaction must occur before data is sent to a model or written to a log where the original value is not required.

---

# 12. Tool Data Exposure

A tool must receive only the data required to perform its defined action.

Tool access does not imply unrestricted access to the source system.

Example:

A tool designed to retrieve supplier status may receive:

- supplier ID;

and return:

- approved / suspended / pending.

It should not automatically expose the complete ERP supplier record.

---

# 13. Model and Provider Restrictions

Not every approved model or provider must be authorized to process every data classification.

The platform must support policy decisions such as:

- model allowed for `INTERNAL`;
- model allowed for `CONFIDENTIAL`;
- model not allowed for `SENSITIVE`;
- local or specially approved processing required for selected data.

Provider eligibility must be determined by policy, not by the LLM itself.

Specific model/provider policies will be defined later.

---

# 14. Logs Are Data

Logs must be treated as a separate data store with their own security requirements.

Observability does not justify storing unrestricted raw data.

Logging must avoid accidental creation of a secondary uncontrolled repository containing:

- prompts;
- credentials;
- employee data;
- sensitive documents;
- tool payloads.

Where detailed logging is required, sensitive fields must be redacted or excluded according to policy.

---

# 15. Derived Data

Data produced from protected source information may retain the sensitivity of the source.

Examples:

- a summary of a confidential contract may remain `CONFIDENTIAL`;
- an embedding generated from restricted HR documentation must not be considered harmless simply because it is numerical;
- a model-generated answer containing sensitive employee information remains `SENSITIVE`.

Transformation does not automatically reduce classification.

---

# 16. Classification Metadata

Where applicable, protected resources must carry classification metadata.

At minimum, a document or data resource should be capable of exposing:

- classification level;
- owner;
- department;
- site scope;
- resource type;
- source system.

Additional metadata may be required by later specifications.

---

# 17. Unknown Classification

If NOMAD Ops cannot determine the classification of a resource that may contain protected information, it must not assume the lowest classification.

The safe default is to restrict processing until classification is known or explicitly resolved.

---

# 18. Data Classification Principle

The central principle is:

> NOMAD Ops must never expose more data merely because an AI system would perform better with additional context.

The platform must optimize AI behaviour within authorized data boundaries, not expand those boundaries for the AI.
