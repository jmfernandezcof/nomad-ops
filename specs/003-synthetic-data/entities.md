# NOMAD Ops — Synthetic Entity Catalogue

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 003-synthetic-data
**Status:** APPROVED

---

## 1. Shared Foundation

The canonical dataset must define:

- sites and their functions;
- departments and their site presence;
- fictional employees, managers and service identities;
- roles, department membership, site assignment and access scope;
- suppliers and business relationships;
- plant equipment and IT assets;
- documents, procedures and runbooks;
- incidents, requests and their history;
- monitoring alerts and measurements;
- approval requests, decisions and expiry;
- controlled actions and execution outcomes;
- audit events linking requests, decisions and results.

## 2. Stable Identity

Each record must have a stable, readable identifier with a type prefix, for example:

- `SITE-` for sites;
- `DEPT-` for departments;
- `USR-` for people;
- `AST-` for assets;
- `SUP-` for suppliers;
- `DOC-` for documents;
- `INC-` for incidents;
- `ALT-` for alerts;
- `APR-` for approvals;
- `ACT-` for actions.

Names may change, but identifiers must remain stable within a dataset version.

## 3. Required Relationships

The dataset must support relationships such as:

- an employee belongs to a department and one primary site;
- a manager has an explicit approval scope;
- an asset belongs to a site and has responsible teams;
- an alert refers to an existing asset;
- an incident refers to existing people, site, asset and related alerts;
- a runbook can support an incident without granting access to it;
- an approval refers to one requested action and an eligible approver;
- an action result refers to the approval and original request;
- audit events preserve the complete journey.

## 4. Time and State

Dates and states must tell a possible story:

- an alert cannot be resolved before it is created;
- an incident cannot cite a document version that did not yet exist;
- an approval cannot occur before its request;
- an expired approval cannot authorize a later action;
- a closed incident cannot contain unexplained later activity;
- superseded documents must remain identifiable as outdated.

## 5. Access and Classification

Records must include the information required to test:

- access by role;
- access by department;
- access by site;
- explicit cross-site assignments;
- allowed and denied actions;
- INTERNAL, CONFIDENTIAL and SENSITIVE classifications;
- restricted results when classification or scope is unknown.
