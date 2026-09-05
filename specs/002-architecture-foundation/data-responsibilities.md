# NOMAD Ops — Data Responsibilities

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `data-responsibilities.md`
**Status:** APPROVED

---

## 1. System of Record Ownership

NOMAD Ops does not become the authoritative source for enterprise data owned by Asteria systems of record.

> NOMAD Ops may store, index, transform and derive data required for its operation, but it does not become the authoritative source for enterprise data owned by Asteria systems of record.

Asteria systems remain authoritative for their respective domains:

- Simulated ITSM: incidents, service requests, SLA state and incident history;
- Simulated ERP: suppliers, purchase orders, invoices, stock and cost centres;
- Simulated HR: employees, departments, positions and onboarding/offboarding state;
- Simulated Plant Operations: production lines, equipment, operational states, alarms and maintenance state;
- Document / Knowledge Management: source documents, document versions and document lifecycle state.

NOMAD Ops may consume and reference these records, but it must not silently replace their authoritative state.

---

## 2. Enterprise-Owned Data and NOMAD Ops-Owned Data

NOMAD Ops must distinguish between:

```text
Enterprise-owned data
```

and:

```text
NOMAD Ops-owned data
```

Enterprise-owned data has its authoritative state in Asteria systems of record. NOMAD Ops may read, reference, retrieve, index, transform, derive from or temporarily cache it where allowed, and may request controlled writes through approved integrations. Local representations must not be treated as the authoritative enterprise record.

NOMAD Ops may be authoritative for its own application state, including:

- local lab users;
- roles and scopes;
- application configuration;
- approval requests and decisions;
- workflow state owned by NOMAD Ops;
- audit references;
- request metadata and correlation identifiers;
- source references and retrieval metadata;
- usage, model-usage and cost records;
- operational telemetry metadata.

PostgreSQL may hold this operational state, but it must not silently replace a system of record for enterprise business data.

---

## 3. Copies Do Not Become Authoritative

> A copy, cache, embedding, chunk, summary, extracted field, transformed representation or derived record in NOMAD Ops does not replace the original system of record.

If a local representation conflicts with its authoritative source, the authoritative source wins unless an approved specification defines a reconciliation process.

This document does not define such a reconciliation process.

---

## 4. Derived Data

NOMAD Ops may create derived artifacts such as:

- chunks and embeddings;
- summaries;
- extracted entities and structured extractions;
- classifications;
- retrieval metadata;
- model outputs;
- cached responses;
- normalized representations;
- source references.

Derived data must remain traceable to its source where technically and operationally appropriate. Source lineage should support auditability, troubleshooting, source and version validation, deletion or re-indexing, access control and classification handling.

---

## 5. Classification Inheritance

> Derived data inherits the security and handling requirements of its source unless an approved classification process explicitly determines otherwise.

This applies to chunks, embeddings, summaries, extracted fields, cached results, prompts containing enterprise data, model outputs derived from protected data and retrieval artifacts.

> An embedding is not considered anonymized merely because the original text is no longer directly readable.

A summary of `SENSITIVE` information must not automatically become `INTERNAL`.

Unknown classification must default to the restricted handling posture defined by the approved system-context specification.

---

## 6. Existing Data Classifications

NOMAD Ops uses the approved classification model:

```text
INTERNAL
CONFIDENTIAL
SENSITIVE
CRITICAL
```

Classification affects access, retrieval, indexing, model-provider eligibility, logging, tool exposure, masking, retention and external processing.

This document does not redefine the classification model. Authentication and authorization remain separate from classification.

---

## 7. Critical Secrets

Critical secrets must never be:

- provided to an LLM;
- indexed into RAG;
- embedded;
- stored in Qdrant;
- written into application, model, workflow or audit logs;
- exposed through tool outputs.

Examples include passwords, private keys, API secrets, privileged access tokens, signing secrets and infrastructure credentials.

This document does not select a secrets-management technology.

---

## 8. Data Minimization

NOMAD Ops must process only the data required for the current business need.

Minimization applies to retrieval, prompt construction, tool inputs and outputs, workflow payloads, audit events, model calls, API responses and cached data.

An entire record, document or user profile must not be sent when a smaller approved subset is sufficient.

The backend / orchestrator must enforce minimization before protected data is passed to optional capabilities such as LLMs or external providers.

---

## 9. Retrieval Responsibilities

Retrieval components may store or process chunks, embeddings, source identifiers, document-version metadata, classification metadata, scope metadata and retrieval metadata.

Qdrant is responsible for vector retrieval only. It is not an authorization authority.

Authorization must constrain the protected retrieval universe before protected content is returned. Vector similarity must never be treated as a permission decision.

Critical secrets must not be embedded.

---

## 10. Source Traceability

Knowledge derived from enterprise sources should retain sufficient source references.

Where relevant, traceability metadata may include:

- source system;
- source record ID;
- document ID and version;
- chunk ID;
- retrieval timestamp;
- classification;
- scope metadata.

These fields are appropriate traceability metadata, not a universal fixed schema required for every data type.

---

## 11. Version Responsibility

For versioned enterprise knowledge, the authoritative source controls which version is current.

NOMAD Ops must not knowingly present an obsolete version as current. Where current-version validation is required, retrieval and response generation must preserve that distinction.

If NOMAD Ops cannot establish whether a version is current, it must preserve that uncertainty rather than falsely claim currency.

---

## 12. Data Freshness

A locally stored representation may become stale.

NOMAD Ops must distinguish between authoritative current state, cached state, indexed state and derived state.

Freshness depends on the capability: direct operational status may require current source-system data, historical analysis may use a historical snapshot, and a knowledge request may require current-document validation.

This document does not define global TTL values, refresh cadence or synchronization strategies. Those remain implementation decisions unless a later feature specification defines them.

---

## 13. Cache Responsibility

Caching is permitted only where compatible with classification, authorization, freshness, privacy, provider restrictions, retention policy and business need.

A cache must not become an alternate system of record. Cached protected data must not bypass authorization on subsequent access.

This document does not select a caching technology or introduce a dependency.

---

## 14. PostgreSQL Responsibilities

PostgreSQL may act as the primary store for NOMAD Ops-owned operational state.

Where required, it may contain local identities, roles, scopes, approval state, workflow state, configuration, audit references, request metadata, cost and usage records, source references and retrieval metadata.

PostgreSQL must not silently become the system of record for enterprise-owned ITSM, ERP, HR, Plant Operations or DMS data.

Enterprise identifiers stored locally should normally be treated as references to the authoritative source.

---

## 15. Qdrant Responsibilities

Qdrant may contain embeddings, chunks, source references, retrieval metadata, classification metadata, scope metadata and version metadata required for retrieval.

It must not contain critical secrets.

Qdrant must not decide authorization. The presence of a vector in Qdrant does not mean every requester may retrieve it.

---

## 16. Model Input Responsibilities

Before enterprise data is sent to an LLM, the backend must ensure that:

- the request and selected data are authorized;
- classification permits the selected provider;
- data is minimized;
- prohibited secrets are removed;
- required masking or redaction has occurred;
- only necessary evidence is supplied.

The LLM must not receive broader enterprise context merely because it may improve answer quality.

---

## 17. Model Output Responsibilities

Model output is derived data and may inherit the sensitivity of its input.

It must not automatically be considered authoritative, correct, safe to execute, safe to log or safe to expose to another user.

Where required, validation may include schema, source and evidence validation, classification handling, authorization checks and tool-proposal validation.

A model-generated statement does not update a system of record.

---

## 18. Tool and Integration Data

Tools and integrations must receive only the minimum required data.

Inputs must be validated. Outputs must be validated before downstream capabilities trust them.

External-system responses must not automatically be considered safe merely because they came from an internal or approved integration. Existing trust-boundary rules remain applicable.

---

## 19. Workflow Data

Workflow orchestration, including n8n, may transport or transform enterprise data as part of approved workflows.

n8n is not a data authority or security authority.

Workflow payloads must preserve authorization constraints, classification handling, minimization, source traceability where required and auditability.

This document does not define or modify n8n infrastructure.

---

## 20. Audit Data

Auditability must not turn logs into an uncontrolled secondary data repository.

Audit events should prefer references and necessary metadata over full protected payloads where possible. They may include request and correlation IDs, identity and resource references, action, authorization, approval and execution outcomes, provider, tool and workflow references, error classification, and cost or usage metadata.

Critical secrets must never be written to audit records.

Other protected payloads should be included only where policy permits and they are strictly necessary. References and necessary metadata should be preferred over full protected payloads.

---

## 21. Observability Data

Operational telemetry follows the same handling principles as other data.

Metrics, traces and logs may reveal user or resource identifiers, prompts, tool arguments, errors, source names and operational state.

Observability data must therefore be designed with minimization, masking, classification awareness, access control and retention awareness.

This document does not define the observability stack; that responsibility belongs to `observability.md`.

---

## 22. Cost and Usage Data

NOMAD Ops may store usage and cost metadata required for governance and operational analysis.

Examples include model provider and identifier, input and output tokens, embedding usage, model-call cost, workflow execution count, retry count and failed-call cost.

Usage records should be correlated with requests where appropriate. Usage telemetry must not require full prompts or protected payloads when metadata is sufficient.

---

## 23. Data Deletion and Invalidation

Where NOMAD Ops stores derived or indexed representations of enterprise data, it must be conceptually possible to invalidate or rebuild them when the source changes or becomes ineligible for use.

Relevant events may include a superseded or deleted source, classification or access-scope change, source correction, or index rebuild.

This document does not define implementation-specific deletion mechanisms. Derived representations must not be treated as permanently valid independent copies.

---

## 24. Authorization Changes

Changes in authorization, role, site or scope must affect future access to protected data.

Previously indexed or cached protected data must not remain accessible merely because it was retrieved when permissions were broader.

Authorization must be evaluated at each relevant access to protected cached or indexed data, in accordance with the approved request-flow architecture.

Historical successful access is not a permanent entitlement.

---

## 25. Cross-User Isolation

Data retrieved, generated or cached for one identity must not automatically become available to another identity.

Any reuse must independently satisfy authorization, scope, classification and business purpose.

One user's authorized context must not become another user's implicit retrieval context.

---

## 26. Environment Separation

Data belonging to different conceptual environments must remain logically separated.

Relevant environments include local development, sandbox / demo, production-like and future production.

Synthetic Asteria data must remain distinct from future real enterprise data. Sensitive simulated actions must remain confined to approved mock or sandbox targets.

This document does not define physical deployment topology.

---

## 27. Synthetic-Data Responsibility

Asteria business systems and business data are synthetic.

NOMAD Ops must treat synthetic enterprise data according to the same logical security, authorization, classification and audit architecture expected in a real enterprise environment.

Synthetic data must not justify bypassing designed controls. Its purpose is to demonstrate production-grade architecture over simulated enterprise systems.

---

## 28. Data Conflicts

When a local derived or cached representation conflicts with an authoritative Asteria system:

- the system of record remains authoritative;
- NOMAD Ops must not silently overwrite authoritative state from its local copy;
- uncertainty or staleness should be surfaced where relevant.

This document does not define automatic reconciliation behaviour.

---

## 29. Responsibility Boundaries

The logical responsibility boundaries are:

```text
Asteria Systems of Record
→ authoritative enterprise state

NOMAD Ops Backend / Orchestrator
→ controls access, minimization, routing and lifecycle

PostgreSQL
→ NOMAD Ops-owned operational state

Qdrant
→ vector retrieval representations

Model Providers
→ approved processing capability, never system of record

n8n
→ workflow orchestration, never security or data authority

Audit / Observability
→ operational evidence and telemetry, not uncontrolled business-data copies
```

These are logical responsibilities and do not imply separate microservices, containers, repositories or processes.

---

## 30. Data Responsibility Principle

> NOMAD Ops may consume, reference, transform and derive enterprise data, but authority remains with the appropriate system of record. Every copy and derived artifact must preserve the security, classification, authorization and traceability requirements required by its source and business use.

> Data convenience must not override authority, minimization or security.
