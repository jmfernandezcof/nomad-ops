# NOMAD Ops — Product Scope

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 000-product
**Status:** APPROVED

---

## First-Version Scope

The first version will demonstrate a complete, safe operational journey using the fictional Asteria environment.

It will include:

- secure access for the approved user types;
- information limited by role, department and site;
- search across authorized internal documents;
- consultation of IT incidents and operational alerts;
- evidence-based assistance to understand and summarize incidents;
- recommendations that clearly distinguish facts from suggestions;
- a small set of controlled, low-risk actions;
- human approval before sensitive actions;
- visible results, failures and incomplete outcomes;
- records of access, decisions, approvals, actions and AI usage;
- realistic simulated services for ITSM, documents, ERP, HR, plant operations and monitoring;
- one coherent synthetic dataset shared by those services.

## Initial Demonstration Journeys

The first version should prove at least these journeys:

1. An employee finds an authorized company procedure.
2. An IT operator reviews an incident, related monitoring information and a relevant runbook.
3. A plant manager reviews an alert affecting their own plant but cannot access another plant without permission.
4. An authorized user requests a controlled action and the system obtains human approval before execution.
5. A compliance user reviews the evidence, decision and action history without gaining permission to perform the action.
6. The system reports a failed or uncertain action honestly and does not repeat it unsafely.

## Synthetic Data Scope

The dataset must cover Madrid HQ and the plants in Toledo, Ciudad Real and Valencia. It must include enough connected fictional records to support the approved demonstration journeys, including users, departments, equipment, incidents, alerts, documents, suppliers and approval history.

No real personal, customer, employee or confidential business data is required.

## Out of Scope for the First Version

- connection to real industrial control systems;
- actions that can affect unrelated production services;
- replacement of ERP, HR, ITSM or document systems;
- unrestricted database, workflow or infrastructure access;
- fully autonomous sensitive actions;
- production rollout, production service levels or disaster-recovery commitments;
- every possible business process at Asteria;
- mobile applications and public customer access.

Any expansion requires a later approved specification.
