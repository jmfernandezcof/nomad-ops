# NOMAD Ops — Application Stack Acceptance

**Product:** NOMAD Ops
**Organization:** Asteria Manufacturing Group
**Spec:** 006-application-stack
**Status:** APPROVED

---

## 1. Stack Criteria

The application foundation is acceptable when:

1. The FastAPI backend starts locally and exposes health information.
2. Request and response contracts are validated and documented.
3. Backend modules keep web, policy, business logic, storage and integrations separated.
4. The React and TypeScript frontend builds without type errors.
5. The interface retains the approved character of the supplied mockup.
6. Mockup-only facts, users, providers, metrics and fake status are removed.
7. The browser obtains protected data only through the backend.
8. Session cookies do not contain user permissions or readable identity context.
9. Password hashing, session expiry, logout and revocation follow the approved identity specification.
10. State-changing browser requests are protected against cross-site request forgery.
11. The backend, not the browser or AI, enforces authorization.
12. The backend reaches the simulator only through its approved narrow contract.
13. No real system, industrial equipment or unrelated host service can be affected.
14. Automated backend, frontend and contract tests pass.
15. Installed dependency versions are pinned and reproducible.

## 2. Initial Implementation Slice

The first implementation slice includes:

- application health;
- local login and logout;
- current-user context;
- policy decisions for the six fictional actor types;
- authorized search for the current Procurement procedure;
- an allowed and denied plant-alert example;
- frontend login and the corresponding authenticated views.

AI, RAG, Qdrant and n8n behaviour are not part of this initial slice.

## 3. Implementation Gate

Implementation begins after product-owner approval of this stack and explicit authorization to install its required dependencies.
