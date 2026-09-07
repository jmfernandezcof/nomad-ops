# ADR-0002 — Local Identity and In-Application Policy

**Status:** ACCEPTED
**Decision:** OD-004 and first-version portion of OD-003
**Approved by:** Product owner
**Approval date:** 2026-09-06

## Context

The first-version sandbox needs realistic fictional users and deterministic permission decisions without coupling business permissions to a future enterprise identity provider.

## Decision

- Use local accounts for synthetic `@asteria.example` users.
- Keep passwords outside the synthetic business dataset and never store readable passwords.
- Use server-controlled sessions with 30-minute inactivity and a 2-hour absolute maximum.
- Do not extend sessions for background work.
- Implement versioned deterministic permission rules inside the application for the first version.
- Keep authentication, authorization and human approval as separate decisions.

## Consequences

- No external identity or policy service is required for the laboratory.
- Future identity-provider integration can replace login without redefining business permissions.
- OD-004 is resolved for the first version.
- OD-003 remains open for exact authentication technology and future identity-provider mechanism.
- OD-018 remains open for production authentication controls.

## Evidence

Approved specification: `specs/005-local-identity-and-authorization/`.
