# NOMAD Ops — Synthetic Data Overview

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 003-synthetic-data
**Status:** APPROVED

---

## 1. Purpose

This specification defines how the fictional Asteria dataset will be created, connected and checked before it is used by NOMAD Ops.

It does not choose the final database technology or the physical design of the simulated enterprise services.

## 2. Storage Layout

Synthetic-data assets will live under:

- `data/synthetic/source/`: the canonical Asteria records;
- `data/synthetic/exports/`: derived records prepared for each simulated system;
- `data/synthetic/scenarios/`: named cross-system demonstration stories;
- `data/synthetic/reports/`: generated quality and consistency results.

Generated exports must never become a second source of truth. They must be reproducible from the canonical source.

## 3. Core Principle

Asteria must behave as one fictional company, not as unrelated sample files.

Every shared person, site, department, asset, supplier, document and event must use a stable identifier wherever it appears.

## 4. Data Safety

- No real personal, customer, employee or confidential business data may be used.
- Names, addresses, contact details and business events must be fictional.
- No real secrets, credentials or access tokens may appear.
- Data must carry an appropriate classification.
- CRITICAL data is not required for the first-version dataset.

## 5. Initial Dataset Size

The first dataset should contain at least:

- 4 sites;
- 8 departments;
- 60 employees across the six approved actor types;
- 24 operational or IT assets;
- 12 suppliers;
- 40 documents and runbooks;
- 60 incidents or service requests;
- 80 monitoring alerts;
- 12 approval requests with mixed outcomes;
- sufficient audit events to reconstruct every demonstration journey.

These numbers provide variety for testing without attempting to represent an entire large enterprise.

## 6. Generation Principle

The dataset must be generated from a fixed seed so the same approved version can be recreated and tested repeatedly.
