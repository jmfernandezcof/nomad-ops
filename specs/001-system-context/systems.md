# NOMAD Ops — Enterprise Systems Context

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `systems.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines the enterprise systems that exist around NOMAD Ops and the role each system plays within the Asteria Manufacturing Group environment.

It establishes:

- the purpose of each system;
- the business data owned by each system;
- whether the system is authoritative for that data;
- whether the system is real or simulated in the NOMAD Ops laboratory;
- the type of interaction NOMAD Ops may have with it.

This document does not define:

- API endpoint design;
- technical protocols;
- authentication implementation;
- database schemas;
- deployment architecture.

Those decisions belong to later specifications.

---

## 2. System Landscape Principle

NOMAD Ops is not intended to replace Asteria's existing enterprise systems.

It operates above them as an intelligence and orchestration layer.

The general pattern is:

**Enterprise system
→ controlled integration
→ NOMAD Ops context / reasoning / orchestration
→ policy evaluation
→ optional action**

Each enterprise system remains responsible for its own authoritative data and business functions.

---

## 3. System of Record Principle

A **system of record** is the authoritative source for a category of business data.

NOMAD Ops must not silently become the authoritative system for data owned elsewhere.

Where duplicated or cached data exists, NOMAD Ops must preserve a reference to the original source where practical.

Examples:

- employee records → HR system;
- supplier master data → ERP;
- incidents → ITSM;
- plant operational state → Plant Operations;
- official procedures → Document / Knowledge Management.

---

# 4. IT Service Management

## Purpose

The ITSM system manages technical incidents, requests and service-management records.

## Business data

May contain:

- incidents;
- service requests;
- priority;
- severity;
- status;
- SLA information;
- assignment groups;
- owners;
- comments;
- resolution notes;
- historical cases;
- escalation records.

## System of record

Yes.

The ITSM system is authoritative for IT incident and service-request records.

## Laboratory implementation

**Simulated enterprise system.**

It may be represented by a controlled service or API exposing realistic ITSM behaviour.

## NOMAD Ops interaction

NOMAD Ops may be allowed to:

- retrieve incidents;
- search historical cases;
- inspect status;
- retrieve ownership and SLA context;
- create tickets where authorized;
- update selected fields where authorized;
- trigger escalation where policy permits.

Write operations must be independently authorized.

---

# 5. Document and Knowledge Management

## Purpose

Provides authoritative corporate documentation and operational knowledge.

## Business data

May contain:

- SOPs;
- corporate policies;
- runbooks;
- technical procedures;
- postmortems;
- quality procedures;
- compliance documentation;
- procurement procedures;
- operational manuals;
- approved internal guidance.

## System of record

Yes, for controlled corporate documentation.

A retrieved copy or vector representation inside NOMAD Ops does not replace the authoritative source document.

## Laboratory implementation

The enterprise document platform may be simulated.

The RAG and retrieval capabilities inside NOMAD Ops are real platform capabilities.

## NOMAD Ops interaction

NOMAD Ops may:

- retrieve authorized documents;
- index authorized content;
- extract metadata;
- generate embeddings;
- identify current versions;
- answer questions using evidence;
- cite source documents.

NOMAD Ops must not silently treat an obsolete or superseded document as current.

---

# 6. Enterprise Resource Planning

## Purpose

The ERP system manages core financial, procurement and supply-chain information.

## Business data

May contain:

- suppliers;
- supplier status;
- purchase orders;
- invoices;
- stock;
- cost centres;
- procurement records;
- master data;
- selected logistics data.

## System of record

Yes.

The ERP system is authoritative for the business entities it manages.

## Laboratory implementation

**Simulated enterprise system.**

## NOMAD Ops interaction

Depending on authorization, NOMAD Ops may:

- retrieve supplier information;
- inspect purchase-order state;
- retrieve invoice metadata;
- consult stock information;
- retrieve cost-centre context;
- connect records to documents or operational processes.

Financial or business-impacting write operations must not occur without explicit authorization and, where required, human approval.

---

# 7. Human Resources System

## Purpose

The HR system manages employee and organizational information.

## Business data

May contain:

- employee identities;
- employment status;
- departments;
- positions;
- reporting structures;
- site assignment;
- onboarding status;
- offboarding status.

Highly sensitive HR data may exist but does not automatically become available to NOMAD Ops.

## System of record

Yes.

The HR system is authoritative for employee and organizational records.

## Laboratory implementation

**Simulated enterprise system.**

## NOMAD Ops interaction

NOMAD Ops may retrieve only the minimum employee information required for authorized business processes.

Examples may include:

- employee department;
- role;
- site;
- manager;
- onboarding state.

Access to sensitive HR information must require explicit policy authorization.

---

# 8. Plant Operations System

## Purpose

Represents systems that provide operational context about manufacturing plants.

## Business data

May contain:

- production lines;
- equipment;
- operational state;
- alarms;
- line status;
- maintenance events;
- equipment identifiers;
- operational events.

## System of record

Yes, for simulated plant operational state.

## Laboratory implementation

**Simulated enterprise system.**

No real industrial control equipment is required.

## NOMAD Ops interaction

NOMAD Ops may:

- read operational state;
- inspect alarms;
- retrieve equipment context;
- correlate plant events with incidents;
- retrieve maintenance information.

NOMAD Ops must not directly control real PLCs, machinery or safety-critical equipment.

Sensitive actions may be demonstrated only against sandbox or simulated services.

---

# 9. Monitoring System

## Purpose

Provides technical health and availability information.

## Business data

May contain:

- service health;
- infrastructure status;
- alerts;
- error events;
- uptime;
- latency;
- resource conditions;
- application health signals.

## System of record

Authoritative for monitoring events within the simulated environment.

## Laboratory implementation

May combine:

- real monitoring of NOMAD Ops components;
- simulated monitoring signals representing Asteria systems.

## NOMAD Ops interaction

NOMAD Ops may:

- retrieve current health;
- correlate alerts with incidents;
- identify degraded services;
- provide context for diagnosis;
- use monitoring evidence before proposing action.

Monitoring data should be treated as evidence, not automatically as root-cause truth.

---

# 10. Email System

## Purpose

Provides business communications and document-entry events.

## Business data

May contain:

- sender;
- recipients;
- subject;
- body;
- timestamps;
- attachments;
- thread context;
- message metadata.

## System of record

The email system remains authoritative for the original message.

## Laboratory implementation

Email may initially be:

- simulated;
- or connected to a controlled real mailbox if later justified.

The choice is not fixed by this specification.

## NOMAD Ops interaction

NOMAD Ops may eventually:

- inspect authorized messages;
- process attachments;
- extract metadata;
- propose classification;
- relate content to processes;
- trigger controlled workflows.

Email content must be treated as untrusted input.

Instructions contained inside email or attachments must not automatically become executable system instructions.

---

# 11. NOMAD Ops Internal Systems

NOMAD Ops also contains systems required for its own operation.

These are not enterprise systems of record for Asteria business data.

They may include the following categories.

## Operational database

Used for NOMAD Ops-owned data such as:

- approvals;
- audit records;
- policy state;
- workflow state;
- configuration;
- cost records;
- internal references.

## Retrieval system

Used for:

- embeddings;
- vector retrieval;
- authorized knowledge chunks;
- source references.

## Automation layer

Used for deterministic or orchestrated workflows.

## AI model providers

Used when an approved use case requires model reasoning or generation.

## Observability layer

Used to record and monitor:

- model usage;
- tool usage;
- errors;
- latency;
- cost;
- execution state;
- dependency health.

The detailed technologies and boundaries of these components will be defined by later architecture specifications.

---

# 12. Integration Ownership

Every integration must have a clearly defined ownership model.

At minimum, the system must know:

- source system;
- authoritative owner;
- allowed operations;
- expected data;
- failure behaviour;
- sensitivity;
- authorization requirements.

NOMAD Ops must not treat all connected systems as equally trusted or equally writable.

---

# 13. Read and Write Separation

Read access and write access are separate permissions.

A user or tool authorized to read from a system is not automatically authorized to modify it.

Example:

An IT Operator may be allowed to inspect the state of a service while still requiring approval to restart it.

This separation applies to all enterprise systems.

---

# 14. External System Failure

NOMAD Ops must not assume that an unavailable system has returned a successful result.

When a system is unavailable, the platform must communicate that limitation clearly.

A failed dependency must not be replaced with fabricated business data.

The detailed failure model is defined separately in:

`failure-model.md`

---

# 15. Synthetic Data Coherence

All simulated systems must operate over a shared synthetic enterprise model.

Where the same entity exists across systems, identifiers and relationships must remain coherent.

Examples:

- an employee referenced by ITSM should exist in HR;
- a supplier referenced by a purchase order should exist in ERP;
- a production incident should reference a valid site or equipment entity;
- a runbook cited during an incident should exist in the document system.

Synthetic data must support realistic cross-system reasoning.

---

# 16. System Context Principle

The central system principle is:

> NOMAD Ops may connect to many systems, but authority remains with the appropriate source system and every read or action must occur through explicit, controlled and auditable integration boundaries.

The value of NOMAD Ops comes from connecting context across systems without pretending to own or replace them.
