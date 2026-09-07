# NOMAD Ops — Application Stack Decision

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 006-application-stack
**Status:** APPROVED

---

## 1. Purpose

This specification selects the first-version application technologies needed to implement the approved product without changing its behaviour.

## 2. Proposed Backend

Use Python and FastAPI for the NOMAD Ops backend.

Reasons:

- the data generator and enterprise simulator already use Python;
- request and response validation is central to the approved design;
- FastAPI provides typed validation and documented interfaces;
- the backend can remain one modular application rather than premature microservices;
- AI, retrieval, PostgreSQL, Qdrant and n8n integrations can be added behind controlled boundaries.

The backend will contain separated modules for:

- local authentication and sessions;
- user context;
- authorization policy;
- request routing;
- approvals;
- enterprise integrations;
- audit and operational records;
- later retrieval and AI capabilities.

## 3. Proposed Frontend

Use React with TypeScript, built with Vite.

Reasons:

- the supplied mockup already behaves as a single interactive application;
- its visual sections can become reusable components;
- TypeScript provides checked contracts between the interface and backend;
- Vite produces a static build and keeps local development simple;
- server-side rendering is not required for this private internal application.

## 4. Mockup Use

`app/frontend/nomad-ops-static-v1.zip` is the visual and interaction reference, not a source of approved business facts.

The implementation will preserve its overall character, responsive layout, navigation and command-bar concept.

It must replace:

- the unapproved example user;
- invented incidents and documents;
- named AI providers that have not been approved;
- fabricated costs, readiness percentages and system status;
- buttons that only display demo notifications.

Replacement content must come from approved Asteria data and real NOMAD Ops state.

## 5. Application Shape

The first version consists logically of:

1. a React browser application;
2. one modular FastAPI NOMAD Ops backend;
3. the approved Asteria simulation service;
4. the already approved PostgreSQL, Qdrant and n8n capabilities when their modules require them.

This decision does not authorize deployment, ports, proxy, Docker or network changes.
