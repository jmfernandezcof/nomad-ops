# NOMAD Ops — Simulated Enterprise Services

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 004-simulated-enterprise-services
**Status:** APPROVED

---

## 1. Purpose

This specification defines the first-version behaviour of Asteria's simulated enterprise systems.

The simulations must provide realistic information, permissions, state changes and failures without connecting to any real company or industrial equipment.

## 2. Proposed Shape

The first version will use one deployable simulation service with six clearly separated business modules:

1. IT service management;
2. document and knowledge management;
3. human resources;
4. enterprise resource planning;
5. plant operations;
6. monitoring.

This keeps the demonstration manageable while preserving separate rules, data ownership and interfaces for each system. The modules may be separated into independent services later without changing their approved behaviour.

Approval of this proposal resolves the first-version mock-service shape only. It does not decide the final NOMAD Ops backend, frontend or production deployment.

## 3. Source of Data

Each module loads its generated view from `data/synthetic/exports/`.

The canonical source remains `data/synthetic/source/`. A simulated service must not silently create conflicting copies of shared Asteria entities.

## 4. System-of-Record Behaviour

Within the demonstration, each module acts as the authoritative source for its own records:

- ITSM for incidents;
- document management for controlled documents;
- HR for people and organization;
- ERP for suppliers;
- plant operations for assets and plant state;
- monitoring for alerts.

NOMAD Ops may cache or index authorized information, but those copies never become authoritative.

## 5. First-Version Boundary

Email is excluded until its simulated-versus-controlled-real-mailbox decision is approved.

No module may connect to real ERP, HR, ITSM, email, industrial-control or customer systems.
