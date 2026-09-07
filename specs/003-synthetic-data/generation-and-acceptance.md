# NOMAD Ops — Synthetic Data Generation and Acceptance

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 003-synthetic-data
**Status:** APPROVED

---

## 1. Generation Process

The approved dataset will be produced in this order:

1. Define fixed catalogues for sites, departments, roles and classifications.
2. Generate the canonical people, suppliers, assets and documents.
3. Add incidents, alerts, approvals, actions and audit history around those records.
4. Add the six named demonstration scenarios.
5. Derive the separate exports required by each simulated enterprise system.
6. Run automated consistency, privacy, access and timeline checks.
7. Produce a report containing the dataset version, generation seed, record counts and validation result.

Derived exports must not be edited manually. A source correction must be followed by regeneration.

## 2. Required Checks

The dataset is acceptable only when:

- generation succeeds from the documented fixed seed;
- a second generation produces the same approved result;
- all identifiers are unique;
- every relationship points to an existing record;
- all required fields and classifications are present;
- dates, versions and state changes follow a possible sequence;
- all six scenario manifests are complete;
- allowed and denied access examples both exist;
- approved, rejected, expired, failed and uncertain outcomes exist;
- shared entities agree across system exports;
- current and superseded documents are distinguishable;
- no real personal data, secrets or credentials are detected;
- no validation error is hidden or silently corrected.

## 3. Quality Report

Each generation must create a human-readable report showing:

- dataset version and seed;
- generated record counts;
- passed and failed checks;
- unresolved warnings;
- scenario coverage;
- a statement that only synthetic data is intended.

Failed mandatory checks make the dataset unusable until corrected and regenerated.

## 4. Change Control

Changing the seed, generation rules, entity relationships or scenario facts creates a new dataset version. Tests and demonstrations must state which version they use.

## 5. Acceptance Gate

No data generator or bulk dataset should be implemented until this specification is approved. Approval authorizes implementation of the generator, not the invention of additional product scope.
