# NOMAD Ops — Open Architecture Decisions

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 002-architecture-foundation
**File:** `open-decisions.md`
**Status:** APPROVED

---

## 1. Purpose

This document is the register of architecture decisions that remain deliberately unresolved.

An entry records a decision that must be made later; it does not authorize an implementation choice.

Codex must not resolve these entries implicitly while implementing another task.

---

## 2. Decision Governance

Each open decision has a stable identifier and must remain `OPEN` until an approved SPEC or ADR records the decision.

A resolution should identify:

- the approved choice;
- the requirement that justifies it;
- alternatives considered;
- security and operational consequences;
- the approving authority;
- the approval date;
- affected SPECs and acceptance criteria.

Resolving an item in code, configuration, a prompt or an undocumented workflow does not close the decision.

---

## 3. Open Decision Register

| ID | Decision required | Source / dependency | Status |
|---|---|---|---|
| `OD-001` | Frontend framework | `specs/002-architecture-foundation/components.md` §22 | `OPEN` |
| `OD-002` | Backend framework and its exact configuration | `specs/002-architecture-foundation/components.md` §22 | `OPEN` |
| `OD-003` | Authentication implementation and future IdP integration mechanism | `specs/002-architecture-foundation/components.md` §22; `specs/001-system-context/environment-and-identity-constraints.md` §§2–4 | `OPEN` |
| `OD-004` | Policy-engine implementation | `specs/002-architecture-foundation/components.md` §22 | `OPEN` |
| `OD-005` | Secret-management technology and credential lifecycle | `specs/002-architecture-foundation/components.md` §22; `specs/001-system-context/trust-boundaries.md` §13 | `OPEN` |
| `OD-006` | Observability stack and implementation | `specs/002-architecture-foundation/components.md` §22; `specs/002-architecture-foundation/observability.md` | `OPEN` |
| `OD-007` | Model routing, approved providers and classification eligibility | `specs/002-architecture-foundation/components.md` §22; `specs/001-system-context/data-classification.md` §13 | `OPEN` |
| `OD-008` | Physical service decomposition | `specs/002-architecture-foundation/components.md` §§21–22 | `OPEN` |
| `OD-009` | Deployment topology and physical environment isolation | `specs/002-architecture-foundation/components.md` §22; `specs/001-system-context/environment-and-identity-constraints.md` §6 | `OPEN` |
| `OD-010` | Network layout, service boundaries and outbound-access controls | `specs/002-architecture-foundation/components.md` §22; `specs/001-system-context/trust-boundaries.md` §§14–15 | `OPEN` |
| `OD-011` | Exact mock-enterprise-service architecture | `specs/002-architecture-foundation/components.md` §22 | `OPEN` |
| `OD-012` | Email integration mode: simulated or controlled real mailbox | `specs/001-system-context/systems.md` §10 | `OPEN` |
| `OD-013` | Cache technology, capability-specific freshness targets, TTLs and synchronization strategy | `specs/002-architecture-foundation/data-responsibilities.md` §§12–13 | `OPEN` |
| `OD-014` | Workload assumptions, capacity targets, performance objectives and SLOs | `specs/000-product/success-criteria.md`; `specs/002-architecture-foundation/observability.md` | `OPEN` |
| `OD-015` | Availability, backup, restoration and recovery objectives | `specs/001-system-context/failure-model.md`; `specs/002-architecture-foundation/observability.md` | `OPEN` |
| `OD-016` | Audit integrity, access, retention and deletion rules | `specs/001-system-context/data-classification.md` §14; `specs/002-architecture-foundation/observability.md` | `OPEN` |
| `OD-017` | Business-data retention and deletion rules and derived-data invalidation implementation | `specs/002-architecture-foundation/data-responsibilities.md` §23 | `OPEN` |
| `OD-018` | Production authentication controls, including session, revocation and additional authentication requirements | `specs/001-system-context/environment-and-identity-constraints.md` §§2–4 | `OPEN` |
| `OD-019` | Encryption and key-rotation implementation | `specs/001-system-context/trust-boundaries.md` §1; `specs/002-architecture-foundation/secrets-and-config.md` | `OPEN` |
| `OD-020` | Dependency and vulnerability-management policy | `specs/001-system-context/codex-constraints.md` §19 | `OPEN` |

---

## 4. Gate Dependencies

The following documents are not yet approved and may supply requirements needed to resolve entries in this register:

- `specs/000-product/vision.md`;
- `specs/000-product/scope.md`;
- `specs/000-product/principles.md`;
- `specs/000-product/success-criteria.md`;
- later approved module specifications that supply requirements relevant to an open entry.

An unresolved entry is not permission to select the most convenient implementation.

---

## 5. Open Decision Principle

> A deferred architecture decision must remain visible, traceable and unresolved until approved evidence justifies a choice.

Implementation must not silently turn an open decision into an architectural commitment.
