# ADR-0003 — First-Version Application Stack

**Status:** ACCEPTED
**Decisions:** OD-001 and OD-002
**Approved by:** Product owner
**Approval date:** 2026-09-06

## Decision

- Build the browser application with React and TypeScript using Vite.
- Build the modular NOMAD Ops backend with Python and FastAPI.
- Reuse the supplied static prototype as a visual reference only.
- Use versioned JSON contracts below `/api/v1`.
- Keep business policy, storage and integrations outside web-route code.

## Boundaries

This decision does not approve Docker topology, ports, Traefik routes, domain names or production deployment. Those changes require the deployment specification and pre/post-change checks.

## Evidence

Approved specification: `specs/006-application-stack/`.
