# ADR-0001 — First-Version Simulated Enterprise Service Shape

**Status:** ACCEPTED
**Decision:** OD-011
**Approved by:** Product owner
**Approval date:** 2026-09-06

## Context

NOMAD Ops needs realistic but safe versions of six Asteria enterprise systems for its first demonstration. The systems must keep separate responsibilities while remaining practical to develop and operate.

## Decision

Use one deployable simulation service containing six logically separated modules: ITSM, documents, HR, ERP, plant operations and monitoring.

Each module owns its approved operations and reads its generated view from `data/synthetic/exports/`. Narrow contracts preserve the boundaries so modules can be separated later if a proven need appears.

## Consequences

- The first version has lower operational complexity.
- Business ownership and access rules remain separate.
- No real enterprise or industrial system is connected.
- Email remains outside the first version.
- Overall NOMAD Ops service decomposition, deployment and network decisions remain open.

## Evidence

Approved specification: `specs/004-simulated-enterprise-services/`.
