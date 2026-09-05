# NOMAD Ops — System Context

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 001-system-context
**File:** `context.md`
**Status:** APPROVED

---

## 1. Purpose

This document defines the business and operational context in which NOMAD Ops exists.

Its purpose is to establish:

- what Asteria Manufacturing Group is;
- what business environment NOMAD Ops operates within;
- what systems and organizational boundaries exist around the platform;
- which parts of the environment are real and which are simulated;
- what NOMAD Ops is responsible for;
- what NOMAD Ops is not responsible for.

This document does not define detailed technical architecture or implementation.

---

## 2. Organization Context

Asteria Manufacturing Group is a fictional European industrial group focused on the manufacturing and packaging of cosmetic and personal care products for large brands.

The organization operates multiple industrial plants and corporate functions.

Asteria is fictitious, but NOMAD Ops must be designed as if it were being deployed in a real enterprise environment.

This means that:

- business data may be synthetic;
- users may be fictional;
- external enterprise systems may be simulated;
- integrations may use controlled mock services;

but:

- permissions must be realistic;
- governance must be enforced;
- sensitive actions must be controlled;
- failures must be handled safely;
- operations must be auditable;
- AI usage must be observable;
- security constraints must be treated as real requirements.

The fictional nature of Asteria must not be used to bypass enterprise-grade controls.

---

## 3. Organizational Footprint

Asteria Manufacturing Group operates:

### Madrid HQ

Corporate headquarters.

Main functions:

- executive management;
- IT;
- finance;
- human resources;
- procurement;
- compliance;
- corporate operations.

### Plant 1 — Toledo

Primary functions:

- manufacturing;
- packaging;
- local operations.

### Plant 2 — Ciudad Real

Primary functions:

- manufacturing;
- packaging;
- warehouse operations;
- local operations.

### Plant 3 — Valencia

Primary functions:

- manufacturing;
- packaging;
- logistics;
- local operations.

This multi-site structure is intentional.

It allows NOMAD Ops to demonstrate:

- site-based access control;
- department-based permissions;
- cross-site workflows;
- local versus corporate knowledge;
- plant-specific incidents;
- shared suppliers and processes;
- centralized and decentralized decision-making.

---

## 4. NOMAD Ops Role

NOMAD Ops is an enterprise operational intelligence layer.

It sits above existing business systems and connects:

- users;
- documents;
- operational data;
- enterprise systems;
- workflows;
- APIs;
- AI models;
- approval mechanisms.

NOMAD Ops does not aim to replace core enterprise systems.

Its role is to:

- retrieve information;
- correlate context;
- reason when required;
- recommend actions;
- invoke controlled tools;
- orchestrate workflows;
- request human approval;
- record decisions and actions;
- provide operational visibility.

---

## 5. Operating Model

NOMAD Ops follows the principle:

**Use the simplest mechanism capable of solving the problem correctly.**

Depending on the use case, the platform may use:

- deterministic software;
- rules;
- search;
- retrieval;
- workflow automation;
- RAG;
- LLM reasoning;
- agents;
- human intervention;
- combinations of the above.

The platform must be capable of deciding that a process does not require AI.

---

## 6. Real vs Simulated Environment

The NOMAD Ops laboratory combines real platform components with simulated enterprise systems.

### Real components

The following are intended to operate as real services inside the NOMAD Ops environment:

- application backend;
- web frontend;
- PostgreSQL;
- Qdrant;
- RAG workflows;
- n8n;
- LLM integrations;
- authentication;
- authorization;
- approval workflows;
- observability;
- audit logging;
- cost tracking;
- internal APIs.

### Simulated enterprise systems

The following may be represented through realistic mock services or APIs:

- ITSM;
- ERP;
- HR system;
- plant operations systems;
- industrial monitoring systems;
- external document management systems.

These simulated services must behave coherently and expose realistic:

- data;
- permissions;
- errors;
- states;
- actions;
- API responses.

Simulation must not remove the operational constraints NOMAD Ops is intended to demonstrate.

---

## 7. Shared Enterprise Universe

All simulated systems must represent the same organizational reality.

They must share coherent entities where applicable, including:

- users;
- departments;
- plants;
- suppliers;
- incidents;
- documents;
- equipment;
- processes;
- projects;
- business units.

For example:

an incident in Plant 2 may reference:

- a synthetic employee;
- a specific packaging line;
- a runbook stored in the knowledge system;
- an earlier ITSM ticket;
- a maintenance event;
- an approval performed by an authorized manager.

Mock data must not behave as unrelated demo datasets.

---

## 8. Core System Categories Around NOMAD Ops

Asteria operates or is assumed to operate systems in the following categories:

### IT Service Management

Provides:

- incidents;
- requests;
- priorities;
- assignments;
- SLA information;
- historical cases.

### Document and Knowledge Management

Provides:

- SOPs;
- runbooks;
- policies;
- postmortems;
- compliance documentation;
- internal procedures;
- corporate knowledge.

### ERP

Provides:

- suppliers;
- purchase orders;
- invoices;
- stock;
- cost centers;
- master data.

### HR

Provides:

- employees;
- departments;
- positions;
- onboarding and offboarding information.

### Plant Operations

Provides:

- production lines;
- equipment;
- operational states;
- alarms;
- maintenance events.

### Monitoring

Provides:

- system health;
- technical events;
- alerts;
- service availability.

### Email

Provides:

- messages;
- attachments;
- document entry points;
- workflow triggers.

---

## 9. System of Record Principle

NOMAD Ops is not the master system for business data owned by external systems.

Where possible, authoritative data remains in the corresponding system of record.

Examples:

- employee data belongs to HR;
- supplier data belongs to ERP;
- incidents belong to ITSM;
- production state belongs to plant systems.

NOMAD Ops may store:

- references;
- normalized metadata;
- cached information where justified;
- audit information;
- approval records;
- workflow state;
- cost data;
- observability data;
- configuration required for its own operation.

NOMAD Ops must not silently become a duplicate ERP, ITSM, HR or document platform.

---

## 10. Industrial Systems Boundary

NOMAD Ops must not directly control:

- PLCs;
- industrial machinery;
- safety-critical systems;
- production equipment.

It may:

- read operational state;
- retrieve telemetry;
- consume alarms;
- consult maintenance information;
- interact through controlled intermediate systems.

For demonstration purposes, NOMAD Ops may execute simulated sensitive actions against:

- sandbox services;
- mock production systems;
- controlled fictitious APIs.

These simulated actions may be used to demonstrate:

- tool calling;
- risk classification;
- authorization;
- human-in-the-loop;
- auditability;
- rollback behaviour;
- failure handling.

No simulated action may be represented as direct control of real industrial equipment.

---

## 11. Development Context

NOMAD Ops is developed using Spec Driven Development.

The implementation workflow is:

**Business need**
**→ SPEC**
**→ acceptance criteria**
**→ design**
**→ implementation**
**→ tests**
**→ validation against SPEC**

The human project owner is responsible for:

- defining business needs;
- approving product decisions;
- approving architecture decisions;
- defining behavioural expectations;
- reviewing risks;
- approving acceptance criteria;
- validating outcomes.

Codex is used on the VPS as the primary implementation agent.

Codex is responsible for implementing approved specifications.

Codex must not independently redefine:

- product scope;
- permissions;
- security policies;
- HITL rules;
- system boundaries;
- architecture decisions;
- acceptance criteria.

Any ambiguity that materially affects product behaviour must be resolved before implementation.

---

## 12. Context Principle

The central system-context principle is:

> NOMAD Ops operates as a controlled intelligence and orchestration layer over a coherent enterprise environment, using real platform capabilities against synthetic but realistic business systems.

The quality of NOMAD Ops will be judged by how realistically it handles:

- information;
- permissions;
- uncertainty;
- failures;
- actions;
- risk;
- cost;
- auditability.

Not by how many integrations or AI features it contains.
