# NOMAD Ops — Simulated Service Capabilities

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 004-simulated-enterprise-services
**Status:** APPROVED

---

## 1. IT Service Management

First-version capabilities:

- retrieve one authorized incident;
- search authorized incidents;
- retrieve related incident history;
- add a controlled internal note;
- request incident escalation.

Reading an incident does not permit changing it. Every write requires a separate permission decision.

## 2. Document and Knowledge Management

First-version capabilities:

- search authorized documents;
- retrieve document metadata and content;
- retrieve the current version of a document family;
- identify superseded versions.

Search must exclude unauthorized documents before content is returned. A superseded version must never be labelled as current.

Document creation and editing are outside the first version.

## 3. Human Resources

First-version capabilities:

- retrieve the minimum user context needed for authorization;
- retrieve department, site and reporting information;
- confirm whether a fictional employee is active.

The service must not return unrestricted employee lists or unnecessary personal details. HR writes are outside the first version.

## 4. Enterprise Resource Planning

First-version capabilities:

- retrieve an authorized supplier;
- retrieve supplier status;
- search suppliers by approved business fields.

Purchase orders, invoices, payments and ERP writes are outside the first version.

## 5. Plant Operations

First-version capabilities:

- retrieve an authorized plant asset;
- retrieve its simulated operational state;
- retrieve relevant maintenance context;
- list assets within an authorized site.

No operation represents direct control of machinery, PLCs or safety equipment.

## 6. Monitoring

First-version capabilities:

- retrieve one authorized alert;
- list alerts for an authorized asset or site;
- retrieve simulated service health;
- correlate alert identifiers with incidents.

Monitoring data is evidence and must not be presented automatically as a confirmed root cause.

## 7. Controlled Demonstration Action

The first version supports one state-changing demonstration action:

`restart_simulated_service`

It acts only on a named sandbox service represented in the fictional environment. It requires explicit authorization and, when classified as sensitive, current human approval.

The action supports idempotency and can return `SUCCESS`, `FAILED` or `UNKNOWN`. It must never affect the host, unrelated containers, real machinery or real business systems.
